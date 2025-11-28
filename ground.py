import Defer
import Globals
import UnlocksPath

def onlyPrepareGround(type):
	if type == None or get_ground_type() == type:
		return
	def harvestAndTill():
		harvest()
		till()
	Defer.everyTile(harvestAndTill)
def prepareGround(type, afterTilling):
	if type == None or get_ground_type() == type:
		return False
	def prepareTile():
		harvest()
		till()
		afterTilling()
		return True
	Defer.everyTile(prepareTile)
	return True
def waterSoil(level=0.75):
	if get_water() < level or (get_entity_type() == Entities.Tree and get_water() < 0.75):
		use_item(Items.Water)

Globals.GLOBALS["AREA"]=1
def updateArea():
	if num_unlocked(Unlocks.Expand) == 1:
		Globals.GLOBALS["AREA"]=3
		return True
	Globals.GLOBALS["AREA"]=get_world_size()**2
	return True
UnlocksPath.afterUnlockDo(Unlocks.Expand, updateArea)

Globals.GLOBALS["MINIMUM_WATER"]=0
def increaseMinimumWater():
	Globals.GLOBALS["MINIMUM_WATER"]=min(0.75, num_unlocked(Unlocks.Speed) * 0.05 - 0.1)
	return Globals.GLOBALS["MINIMUM_WATER"] < 0.75
UnlocksPath.afterUnlockDo(Unlocks.Speed, increaseMinimumWater)
