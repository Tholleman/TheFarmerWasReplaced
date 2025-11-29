import Defer
import Globals
import UnlocksPath


def workToUnlock(toUnlock, orders={"currentlyUnlocking":[],"items":{}}, indent=""):
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
		for item in cost:
			# quick_print(indent, "-", cost[item], item)
			if item in orders["items"]:
				orders["items"][item]+=cost[item]
			else:
				orders["items"][item]=cost[item]
		for item in Globals.HARVEST_ORDER:
			if item in orders["items"]:
				Globals.ITEM_TO_FUNCTION[item](orders["items"].pop(item), orders, indent + "  ")
		if toUnlock == Unlocks.Expand:
			Defer.everyTile(harvest)
	orders["currentlyUnlocking"].pop()
	afterUnlockActions(toUnlock)
	Globals.UNLOCK_EFFORT.pop(toUnlock)
	if toUnlock in UnlocksPath.REPEATABLE:
		if UnlocksPath.addToUnavailable(toUnlock, get_cost(toUnlock)):
			Globals.AVAILABLE_UNLOCKS.remove(toUnlock)
	elif toUnlock in Globals.AVAILABLE_UNLOCKS:
		Globals.AVAILABLE_UNLOCKS.remove(toUnlock)
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
		return updateEffort(unlock)
	return Globals.UNLOCK_EFFORT[unlock]
def updateEffort(unlock):
	cost=get_cost(unlock)
	effort=0
	for item in cost:
		effort+=cost[item]*Globals.ITEM_EFFORT[item]
	if unlock == Unlocks.Speed:
		effort*=2 + num_unlocked(unlock)
	elif unlock == Unlocks.Expand:
		effort-=1
	else:
		effort*=1 + num_unlocked(unlock)
	if unlock in Globals.UNLOCK_PREFERENCE:
		effort/=Globals.UNLOCK_PREFERENCE[unlock]
	Globals.UNLOCK_EFFORT[unlock]=effort
	return effort
