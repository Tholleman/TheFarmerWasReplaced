import Globals
import UnlocksPath
import Wood
import ground
import movement

def harvestCheck():
	if can_harvest():
		harvest()
		return True
	return get_entity_type() in [None, Entities.Grass]
def forceHarvestNoFertilizer():
	while not harvestCheck():
		if get_ground_type() == Grounds.Soil:
			ground.waterSoil()
def forceHarvestWithFertilizer():
	while not harvestCheck():
		if get_entity_type() == Entities.Tree:
			spamFertilizer()
			return
		elif get_ground_type() == Grounds.Soil:
			ground.waterSoil()
def forceHarvest():
	Globals.REPLACABLE_FUNCTIONS["forceHarvest"]()
def onlyKeep(wanted):
	if get_entity_type() in wanted:
		return
	spamFertilizer()
def spamFertilizer():
	while not harvestCheck():
		use_item(Items.Fertilizer)
		if get_ground_type() == Grounds.Soil:
			ground.waterSoil()
def spamWater():
	while not harvestCheck():
		ground.waterSoil(0.75)
def clearHarvest(wanted):
	if get_entity_type() in wanted:
		forceHarvestNoFertilizer()
	else:
		spamFertilizer()
def companionCheck(wanted):
	if num_unlocked(Unlocks.Polyculture) == 0:
		return False
	# if num_items(Items.Fertilizer) == 0:
	# 	return False
	companion = get_companion()
	if companion == None:
		return False
	requiredCompanionGround=getRequiredCompanionGround(companion[0])
	if requiredCompanionGround != None and requiredCompanionGround != get_ground_type():
		return False
	if companion[0] == Entities.Tree and not Wood.canPlantTree(companion[1][0], companion[1][1]):
		return False
	previous=movement.getPos()
	movement.toCoordinates(companion[1][0], companion[1][1])
	if get_entity_type() != companion[0]:
		clearHarvest(wanted)
		if not plant(companion[0]):
			movement.toCoordinates(previous[0],previous[1])
			return False
	movement.toCoordinates(previous[0],previous[1])
	forceHarvest()
	return True
def getRequiredCompanionGround(companion):
	if companion == Entities.Carrot:
		return Grounds.Soil
	return None

Globals.REPLACABLE_FUNCTIONS["forceHarvest"]=forceHarvestNoFertilizer
def setupHarvestWithFertilizer():
	Globals.REPLACABLE_FUNCTIONS["forceHarvest"]=forceHarvestWithFertilizer
	return False
UnlocksPath.afterUnlockDo(Unlocks.Fertilizer, setupHarvestWithFertilizer)
