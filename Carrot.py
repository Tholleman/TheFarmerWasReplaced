import Debug
import Defer
import Globals
import Harvesting
import Preperations
import UnlockHelper
import ground
import movement

def harvestCarrot(amount, currentlyUnlocking, indent):
	if num_items(Items.Carrot) > amount:
		return
	quick_print(indent, amount, "Carrot")
	UnlockHelper.workToUnlock(Unlocks.Carrots, currentlyUnlocking, "  " + indent)
	requirements=[Items.Power]
	def calculateTilesNeeded():
		return Preperations.expectedTilesNeeded(Items.Carrot, Unlocks.Carrots, amount, num_unlocked(Unlocks.Polyculture), 1)
	tiles=Preperations.preperations(Items.Carrot, calculateTilesNeeded, requirements, currentlyUnlocking, indent)
	if num_items(Items.Carrot) >= amount:
		return
	quick_print(indent, amount, "Carrot using ~" + str(tiles), "tiles")
	if ground.prepareGround(Grounds.Soil, simplePlantCarrot):
		tiles-=Globals.GLOBALS["AREA"]
		move(East)
	dronesNeeded, tilesPerDrone=Defer.dronesNeeded(tiles)
	rowsPerDrone=min(get_world_size()/dronesNeeded, tilesPerDrone/get_world_size())
	def behaviour():
		start=movement.getPos()
		while num_items(Items.Carrot) < amount:
			for _ in range(rowsPerDrone - 1):
				movement.actMoveAct(plantCarrot, get_world_size(), North)
				if rowsPerDrone > 1:
					move(East)
			movement.actMoveAct(plantCarrot, get_world_size(), North)
			movement.toPos(start)
	Defer.spawnMoveAct(behaviour, dronesNeeded, East, rowsPerDrone)
def plantCarrot():
	if get_entity_type() == Entities.Carrot:
		Harvesting.companionCheck([Entities.Carrot])
	Harvesting.clearHarvest([Entities.Carrot])
	simplePlantCarrot()
	ground.waterSoil()
def simplePlantCarrot():
	if not plant(Entities.Carrot):
		Globals.ITEM_TO_SINGLE_PLANT[Preperations.lowestSimplePlant(None, [Items.Hay, Items.Wood])]()

if __name__ == "__main__":
	Debug.startBenchmark(Items.Carrot, goal, delta)
