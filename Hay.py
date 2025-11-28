import Debug
import Defer
import Preperations
import UnlockHelper
import ground
import Harvesting
import Globals

def harvestHay(amount, currentlyUnlocking, indent):
	if num_items(Items.Hay) >= amount:
		return
	quick_print(indent, amount, "Hay")
	UnlockHelper.workToUnlock(Unlocks.Grass, currentlyUnlocking, "  " + indent)
	def calculateTilesNeeded():
		return Preperations.expectedTilesNeeded(Items.Hay, Unlocks.Grass, amount, num_unlocked(Unlocks.Polyculture))
	tiles=Preperations.preperations(Items.Hay, calculateTilesNeeded, [Items.Power], currentlyUnlocking, indent)
	if num_items(Items.Hay) >= amount:
		return
	dronesNeeded, _=Defer.dronesNeeded(tiles)
	quick_print(indent, amount, "Hay using ~" + str(tiles), "tiles")
	def behaviour():
		while num_items(Items.Hay) < amount:
			plantHay()
			move(North)
	Defer.spawnMoveAct(behaviour, dronesNeeded, East)
def plantHay():
	while not ((can_harvest() and harvest()) or get_entity_type() == None):
		move(North)
	if get_entity_type() != Entities.Grass:
		plant(Entities.Grass)
	Harvesting.companionCheck([Entities.Grass])
def simplePlantHay():
	if get_entity_type() != Entities.Grass:
		plant(Entities.Grass)
def cleanup(goal):
	for _ in range(get_world_size()):
		if num_items(Items.Hay) >= goal:
			return
		move(North)
		plantHay()
if __name__ == "__main__":
	Globals.SETUP_FUNCTION_MAPS()
	if prepareTill:
		ground.onlyPrepareGround(Grounds.Soil)
	Debug.startBenchmark(Items.Hay, goal, 0.2)
