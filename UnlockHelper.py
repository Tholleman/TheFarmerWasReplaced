import Defer
import Globals
import UnlocksPath


def unlockAll(pathStep):
	unlocks, effort=pathStep
	items={}
	for unlock in unlocks:
		Globals.UNLOCK_EFFORT[unlock]=effort
		cost=get_cost(unlock)
		for item in cost:
			if item in items:
				items[item]+=cost[item]
			else:
				items[item]=cost[item]
	orders={"currentlyUnlocking":[],"items":items}
	quick_print(unlocks, "(", effort, ")")
	for unlock in unlocks:
		workToUnlock(unlock, orders, "", True)
def workToUnlock(toUnlock, orders={"currentlyUnlocking":[],"items":{}}, indent="", itemsIncludesCost=False):
	if toUnlock in orders["currentlyUnlocking"]:
		return
	if num_unlocked(toUnlock) >= Globals.UNLOCKS[toUnlock]:
		return
	cost=get_cost(toUnlock)
	if toUnlock not in Globals.AVAILABLE_UNLOCKS:
		for item in cost:
			if num_unlocked(item) == 0:
				return
	if len(orders["currentlyUnlocking"]) and getEffort(toUnlock) > getEffort(orders["currentlyUnlocking"][0]):
		return
	orders["currentlyUnlocking"].append(toUnlock)
	quick_print(indent, toUnlock, num_unlocked(toUnlock) + 1, "/", Globals.UNLOCKS[toUnlock], "(", getEffort(toUnlock), ")")
	while not unlock(toUnlock):
		if itemsIncludesCost:
			itemsIncludesCost=False
		else:
			for item in cost:
				# quick_print(indent, "-", cost[item], item)
				if item in orders["items"]:
					orders["items"][item]+=cost[item]
				else:
					orders["items"][item]=cost[item]
		for item in Globals.HARVEST_ORDER:
			if item in cost and item in orders["items"]:
				Globals.ITEM_TO_FUNCTION[item](orders["items"].pop(item), orders, indent + "  ")
		if toUnlock == Unlocks.Expand:
			Defer.everyTile(harvest)
	orders["currentlyUnlocking"].pop()
	afterUnlockActions(toUnlock)
	Globals.UNLOCK_EFFORT.pop(toUnlock)
def afterUnlockActions(unlocked):
	if unlocked not in Globals.AFTER_UNLOCK:
		return
	toRemove=set()
	for postUnlockAction in Globals.AFTER_UNLOCK[unlocked]:
		if not postUnlockAction():
			toRemove.add(postUnlockAction)
	if len(Globals.AFTER_UNLOCK[unlocked]) == len(toRemove):
		Globals.AFTER_UNLOCK.pop(unlocked)
	else:
		for action in toRemove:
			Globals.AFTER_UNLOCK[unlocked].remove(action)
def getEffort(unlock):
	if unlock not in Globals.UNLOCK_EFFORT:
		Globals.UNLOCK_EFFORT[unlock]=UnlocksPath.calcEffort(unlock, num_unlocked(unlock))
	return Globals.UNLOCK_EFFORT[unlock]
