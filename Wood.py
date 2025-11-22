import Defer
import Harvesting
import Globals
import Preperations
import UnlockHelper
import ground
import movement
import Debug


def harvestWood(amount, currentlyUnlocking, indent):
	if num_items(Items.Wood) > amount:
		return
	quick_print(indent, amount, "Wood")
	UnlockHelper.workToUnlock(Unlocks.Trees, currentlyUnlocking, "  " + indent)
	if num_unlocked(Unlocks.Polyculture):
		def calculateTilesNeeded():
			return Preperations.expectedTilesNeeded(Items.Wood, Unlocks.Trees, amount, num_unlocked(Unlocks.Polyculture), 3.625)
	elif num_unlocked(Unlocks.Trees):
		def calculateTilesNeeded():
			return max(Preperations.expectedTilesNeeded(Items.Wood, Unlocks.Trees, amount, num_unlocked(Unlocks.Polyculture), 3.625), Globals.GLOBALS["AREA"])
	else:
		def calculateTilesNeeded():
			return Preperations.expectedTilesNeeded(Items.Wood, Unlocks.Trees, amount, False)
	tiles=Preperations.preperations(Items.Wood, calculateTilesNeeded, [Items.Power], currentlyUnlocking, indent)
	quick_print(indent, amount, "Wood using ~" + str(tiles), "tiles")
	dronesNeeded,tilesPerDrone=Defer.dronesNeeded(tiles)
	rowsPerDrone=min(get_world_size()/dronesNeeded, tilesPerDrone/get_world_size())
	if num_unlocked(Unlocks.Expand) < 2:
		rowsPerDrone=1
	def behaviour():
		start=movement.getPos()
		while num_items(Items.Wood) < amount:
			for _ in range(rowsPerDrone - 1):
				movement.actMoveAct(woodStrategyTree, get_world_size(), North)
				if num_items(Items.Wood) >= amount:
					return
				move(East)
			movement.actMoveAct(woodStrategyTree, get_world_size(), North)
			movement.toPos(start)
	Defer.spawnMoveAct(behaviour, dronesNeeded, East, rowsPerDrone)
def woodStrategyTree():
	if get_entity_type() in [Entities.Bush, Entities.Tree]:
		if get_entity_type() == Entities.Tree and not can_harvest():
			ground.waterSoil(0.75)
			return
		Harvesting.companionCheck([Entities.Bush, Entities.Tree])
	Harvesting.clearHarvest([Entities.Tree, Entities.Bush])
	if canPlantTree():
		plant(Entities.Tree)
		ground.waterSoil(0.75)
	else:
		plant(Entities.Bush)
		ground.waterSoil()
def canPlantTree(x=get_pos_x(), y=get_pos_y()):
	return num_unlocked(Unlocks.Trees) and (x + y) % 2 == 0
def simplePlantWood():
	if num_unlocked(Unlocks.Trees) and canPlantTree():
		plant(Entities.Tree)
		if get_ground_type() == Grounds.Soil:
			ground.waterSoil(0.75)
	else:
		plant(Entities.Bush)
		if get_ground_type() == Grounds.Soil:
			ground.waterSoil()
if __name__ == "__main__":
	if prepareTill:
		ground.onlyPrepareGround(Grounds.Soil)
	Debug.startBenchmark(Items.Wood, goal, delta)
