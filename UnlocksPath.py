import Globals
import UnlockHelper

REPEATABLE=[Unlocks.Speed, Unlocks.Expand, Unlocks.Watering, Unlocks.Fertilizer, Unlocks.Megafarm]

def addToUnavailable(unlock, cost):
	if unlock not in Globals.UNLOCKS:
		if num_unlocked(unlock) == 0:
			quick_print("WARNING: ignoring", unlock)
		return True
	if num_unlocked(unlock) == Globals.UNLOCKS[unlock]:
		return True
	if cost == None:
		return True
	for item in Globals.HARVEST_ORDER:
		if item in cost:
			if num_unlocked(item) == 0:
				def addToAvailable():
					if not addToUnavailable(unlock, cost):
						Globals.AVAILABLE_UNLOCKS.append(unlock)
				afterUnlockDo(Globals.ITEM_TO_UNLOCK[item], addToAvailable)
				return True
	return False
def getNextUnlock():
	available=Globals.AVAILABLE_UNLOCKS
	# available=getAvailableUnlocks()
	first=available[0]
	lowest={"unlock":first, "effort": UnlockHelper.getEffort(first)}
	for unlock in available[1::]:
		effort=UnlockHelper.getEffort(unlock)
		if effort < lowest["effort"]:
			lowest={"unlock": unlock, "effort": effort}
	return lowest["unlock"]
def afterUnlockDo(key, action):
	if num_unlocked(key) > 0:
		action()
		return
	if key not in Globals.AFTER_UNLOCK:
		Globals.AFTER_UNLOCK[key]={action}
	else:
		Globals.AFTER_UNLOCK[key].add(action)

for unlock in Unlocks:
	if not addToUnavailable(unlock, get_cost(unlock)):
		Globals.AVAILABLE_UNLOCKS.append(unlock)
if Unlocks.Grass in Globals.AVAILABLE_UNLOCKS:
	Globals.AVAILABLE_UNLOCKS.remove(Unlocks.Grass)

def clearAvailableUnlocks():
	Globals.AVAILABLE_UNLOCKS=[]
Globals.AFTER_UNLOCK[Unlocks.Leaderboard]={clearAvailableUnlocks}
