import Defer
import Globals
import Harvesting
import Preperations
import Wood
import ground
import movement


def harvestWeirdSubstance(amount, currentlyUnlocking, indent):
	if num_items(Items.Weird_Substance) >= amount:
		return
	quick_print(indent, amount, "Weird Substance")
	def calculateTilesNeeded():
		return Preperations.expectedTilesNeeded(Items.Weird_Substance, Unlocks.Trees, amount, False, 3.5)
	ground.onlyPrepareGround(Grounds.Soil)
	ensureOneWeirdSubstance()
	while num_items(Items.Weird_Substance) < amount:
		Preperations.preperations(Items.Weird_Substance, calculateTilesNeeded, currentlyUnlocking, indent)
		def behaviour():
			while num_items(Items.Weird_Substance) < amount:
				weirdSubstancePatch()
				move(North)
				move(North)
		movement.toCoordinates(0, 1)
		while spawn_drone(behaviour) and num_items(Items.Weird_Substance) < amount:
			move(East)
			move(East)
			move(East)
			move(North)
			if get_pos_x() <= 1:
				movement.toCoordinates(0, 1)
		behaviour()
		Defer.joinAll()
def ensureOneWeirdSubstance():
	if num_items(Items.Weird_Substance) == 0:
		Harvesting.forceHarvest()
		plant(Entities.Tree)
		use_item(Items.Fertilizer)
		while not can_harvest():
			use_item(Items.Fertilizer)
		harvest()
def weirdSubstancePatch():
	drownHarvest()
	plantCarrot()
	move(East)
	if get_pos_y() != 0:
		move(South)
		drownHarvest()
		plantCarrot()
		move(North)
	if get_pos_x() != get_world_size() - 1:
		move(East)
		drownHarvest()
		plantCarrot()
		move(West)
	if get_pos_y() != get_world_size() - 1:
		move(North)
		drownHarvest()
		plantCarrot()
		move(South)
	drownHarvest()
	Harvesting.forceHarvest()
	_=plant(Entities.Carrot) or plant(Entities.Grass)
	use_item(Items.Weird_Substance)
def plantCarrot():
	Harvesting.forceHarvest()
	Wood.simplePlantWood()
	ground.waterSoil(0.75)
def drownHarvest():
	while not can_harvest() and get_entity_type() != None:
		ground.waterSoil(0.75)
	harvest()
if __name__ == "__main__":
	Globals.SETUP_FUNCTION_MAPS()
	harvestWeirdSubstance(goal, [], "")
	quick_print(num_items(Items.Weird_Substance))
