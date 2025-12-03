import Globals

REPEATABLE={Unlocks.Speed, Unlocks.Expand, Unlocks.Watering, Unlocks.Fertilizer, Unlocks.Megafarm}
IMPROVES_YIELD=set(REPEATABLE)
IMPROVES_YIELD.add(Unlocks.Trees)
IMPROVES_YIELD.add(Unlocks.Sunflowers)
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
	available=[]
	awaiting={}
	def addToAvailable(unlock):
		if len(available) == 0 or effort[available[-1]] <= effort[unlock]:
			available.append(unlock)
			return
		for i in range(len(available)):
			if effort[available[i]] > effort[unlock]:
				available.insert(i, unlock)
				return
	def testAvailable(unlock):
		item=firstUnavailableItem(get_cost(unlock, simUnlocked[unlock]), simUnlocked)
		if item:
			itemUnlock=Globals.ITEM_TO_UNLOCK[item]
			if itemUnlock not in awaiting:
				awaiting[itemUnlock]=set()
			awaiting[itemUnlock].add(unlock)
		else:
			addToAvailable(unlock)
	for unlock in unlockable:
		effort[unlock]=calcEffort(unlock, simUnlocked[unlock])
		testAvailable(unlock)
	def simUnlock(unlock):
		simUnlocked[unlock]+=1
		available.remove(unlock)
		if simUnlocked[unlock] < Globals.UNLOCKS[unlock] and unlock in REPEATABLE:
			effort[unlock]=calcEffort(unlock, simUnlocked[unlock])
			testAvailable(unlock)
		else:
			unlockable.remove(unlock)
			if unlock in awaiting:
				for nowAvailable in awaiting[unlock]:
					testAvailable(nowAvailable)
	group=[]
	groupedEffort=0
	while len(unlockable):
		lowest=available[0]
		group.append(lowest)
		groupedEffort+=effort[lowest]
		simUnlock(lowest)
		if lowest in IMPROVES_YIELD:
			path.append((group, groupedEffort))
			group=[]
			groupedEffort=0
	path.append((group, groupedEffort))
	return path
def calcEffort(unlock, level):
	cost=get_cost(unlock, level)
	effort=0
	for item in cost:
		effort+=cost[item]*Globals.ITEM_EFFORT[item]
	if unlock == Unlocks.Speed:
		effort*=2 + level
	elif unlock == Unlocks.Expand:
		effort-=1
	else:
		effort*=1 + level
	if unlock in Globals.UNLOCK_PREFERENCE:
		effort/=Globals.UNLOCK_PREFERENCE[unlock]
	return effort
def firstUnavailableItem(cost, simUnlocked):
	for item in cost:
		if simUnlocked[Globals.ITEM_TO_UNLOCK[item]] == 0:
			return item
	return None
def afterUnlockDo(key, action):
	if num_unlocked(key) > 0:
		action()
		return
	if key not in Globals.AFTER_UNLOCK:
		Globals.AFTER_UNLOCK[key]={action}
	else:
		Globals.AFTER_UNLOCK[key].add(action)
