import Debug
import Defer
import Globals
import Harvesting
import Preperations
import UnlockHelper
import Utils
import ground
import movement

def harvestCarrot(amount, currentlyUnlocking, indent):
	if num_items(Items.Carrot) > amount:
		return
	quick_print(indent, amount, "Carrot")
	UnlockHelper.workToUnlock(Unlocks.Carrots, currentlyUnlocking, "  " + indent)
	def calculateTilesNeeded():
		return Preperations.expectedTilesNeeded(Items.Carrot, Unlocks.Carrots, amount, num_unlocked(Unlocks.Polyculture), 1)
	tiles=Preperations.preperations(Items.Carrot, calculateTilesNeeded, currentlyUnlocking, indent)
	if num_items(Items.Carrot) >= amount:
		return
	quick_print(indent, amount, "Carrot using ~" + str(tiles), "tiles")
	ground.prepareGround(Grounds.Soil, simplePlantCarrot)
	def manageRegion(c1, c2):
		c1=Defer.splitRegion(c1, c2, manageRegion)
		width=c2[0] - c1[0]
		height=c2[1] - c1[1]
		while num_items(Items.Carrot) < amount:
			movement.toCorner(c1, c2, plantCarrot)
			north=True
			for _ in range(width - 1):
				movement.actMoveAct(plantCarrot, height, Utils.ternary(north, North, South))
				if num_items(Items.Carrot) >= amount:
					return
				north=not north
				move(East)
			movement.actMoveAct(plantCarrot, height, Utils.ternary(north, North, South))
	topRight=(get_world_size(), get_world_size())
	if tiles < get_world_size() ** 2:
		topRight=(max(1, tiles // get_world_size()), get_world_size())
	manageRegion((0,0), topRight)
	Defer.joinAll()
def plantCarrot():
	if get_entity_type() == Entities.Carrot:
		Harvesting.companionCheck([Entities.Carrot])
	if not Harvesting.harvestCheck():
		return
	simplePlantCarrot()
	ground.waterSoil()
def simplePlantCarrot():
	if not plant(Entities.Carrot):
		Globals.ITEM_TO_SINGLE_PLANT[Preperations.lowestSimplePlant(None, [Items.Hay, Items.Wood])]()

if __name__ == "__main__":
	Debug.startBenchmark(Items.Carrot, goal, delta)
