import Globals
import UnlockHelper

REPEATABLE={Unlocks.Speed, Unlocks.Expand, Unlocks.Watering, Unlocks.Fertilizer, Unlocks.Megafarm}
IMPROVES_YIELD=set(REPEATABLE)
IMPROVES_YIELD.add(Unlocks.Trees)
IMPROVES_YIELD.add(Unlocks.Leaderboard)

# Returns (Unlocks[], effort)[]
def calculatePath():
	simUnlocked={}
	unlockable=[]
	for unlock in Globals.UNLOCKS:
		simUnlocked[unlock]=num_unlocked(unlock)
		if num_unlocked(unlock) == 0 or (num_unlocked(unlock) < Globals.UNLOCKS[unlock] and unlock in REPEATABLE):
			unlockable.append(unlock)
	path=[]
	effort={}
	for unlock in unlockable:
		effort[unlock]=calcEffort(unlock, simUnlocked)
	available=[]
	unavailable=list(unlockable)
	def simUnlock(unlock):
		simUnlocked[unlock]+=1
		available.remove(unlock)
		if simUnlocked[unlock] < Globals.UNLOCKS[unlock] and unlock in REPEATABLE:
			unavailable.append(unlock)
			effort[unlock]=calcEffort(unlock, simUnlocked)
		else:
			unlockable.remove(unlock)
	group=[]
	groupedEffort=0
	while len(unlockable):
		added=[]
		# TODO: only check the unavailable unlocks that have become available
		for unlock in unavailable:
			cost=get_cost(unlock, simUnlocked[unlock])
			if isAvailable(cost, simUnlocked):
				available.append(unlock)
				added.append(unlock)
		for unlock in added:
			unavailable.remove(unlock)
		lowest=(available[0], effort[available[0]])
		for unlock in available[1:]:
			if effort[unlock] < lowest[1]:
				lowest=(unlock, effort[unlock])
		simUnlock(lowest[0])
		group.append(lowest[0])
		groupedEffort+=lowest[1]
		if lowest[0] in IMPROVES_YIELD:
			path.append((group, groupedEffort))
			group=[]
			groupedEffort=0
	path.append((group, groupedEffort))
	return path
def calcEffort(unlock, simUnlocked):
	cost=get_cost(unlock, simUnlocked[unlock])
	effort=0
	for item in cost:
		effort+=cost[item]*Globals.ITEM_EFFORT[item]
	if unlock == Unlocks.Speed:
		effort*=2 + simUnlocked[unlock]
	elif unlock == Unlocks.Expand:
		effort-=1
	else:
		effort*=1 + simUnlocked[unlock]
	if unlock in Globals.UNLOCK_PREFERENCE:
		effort/=Globals.UNLOCK_PREFERENCE[unlock]
	return effort
def isAvailable(cost, simUnlocked):
	for item in cost:
		if simUnlocked[Globals.ITEM_TO_UNLOCK[item]] == 0:
			return False
	return True
def afterUnlockDo(key, action):
	if num_unlocked(key) > 0:
		action()
		return
	if key not in Globals.AFTER_UNLOCK:
		Globals.AFTER_UNLOCK[key]={action}
	else:
		Globals.AFTER_UNLOCK[key].add(action)
