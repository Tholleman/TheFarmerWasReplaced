import Defer
import Harvesting
import Globals
import Preperations
import UnlockHelper
import Utils
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
	def manageRegion(c1, c2):
		c1=Defer.splitRegion(c1, c2, manageRegion)
		width=c2[0] - c1[0]
		height=c2[1] - c1[1]
		while num_items(Items.Wood) < amount:
			movement.toCorner(c1, c2, woodStrategyTree)
			north=True
			for _ in range(width - 1):
				movement.actMoveAct(woodStrategyTree, height, Utils.ternary(north, North, South))
				if num_items(Items.Wood) >= amount:
					return
				north=not north
				move(East)
			movement.actMoveAct(woodStrategyTree, height, Utils.ternary(north, North, South))
	topRight=(Utils.ternary(num_unlocked(Unlocks.Expand) > 1, get_world_size(), 1), get_world_size())
	if tiles < get_world_size() ** 2:
		topRight=(max(1, tiles // get_world_size()), get_world_size())
	manageRegion((0,0), topRight)
	Defer.joinAll()
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
		ground.waterSoil(0.75)
	else:
		plant(Entities.Bush)
		ground.waterSoil()
if __name__ == "__main__":
	if prepareTill:
		ground.onlyPrepareGround(Grounds.Soil)
	Debug.startBenchmark(Items.Wood, goal, delta)
