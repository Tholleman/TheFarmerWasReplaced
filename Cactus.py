import Defer
import UnlockHelper
import Preperations
import Globals
import Harvesting
import movement
import ground

def harvestCactus(amount, currentlyUnlocking, indent):
	if num_items(Items.Cactus) > amount:
		return
	quick_print(indent, amount, "Cactus")
	UnlockHelper.workToUnlock(Unlocks.Cactus, currentlyUnlocking, "  " + indent)
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Cactus, Unlocks.Cactus, amount, False, Globals.GLOBALS["AREA"])
		return tiles + Globals.GLOBALS["AREA"] - (tiles % Globals.GLOBALS["AREA"])
	while num_items(Items.Cactus) < amount:
		tiles=Preperations.preperations(Items.Cactus, calculateTilesNeeded, [Items.Power], currentlyUnlocking, indent)
		ground.onlyPrepareGround(Grounds.Soil)
		quick_print(indent, amount, "Cactus using", tiles / Globals.GLOBALS["AREA"], "fields")
		for _ in range(0, tiles, Globals.GLOBALS["AREA"]):
			plantFieldFullOfCactus()
def plantFieldFullOfCactus():
	movement.toCoordinates(0, 0)
	for _ in range(get_world_size()):
		Defer.defer(plantColumn)
		move(East)
	Defer.joinAll()
	for _ in range(get_world_size()):
		Defer.defer(sortRow)
		move(North)
	Defer.joinAll()
	Harvesting.forceHarvest()
	return True
def plantColumn():
	plantCactus()
	for _ in range(get_world_size()-1):
		move(North)
		plantCactus()
		if measure() < measure(South):
			swap(South)
	move(North)
	sortRow(North, South, 1)
def plantCactus():
	Harvesting.onlyKeep([Entities.Cactus])
	plant(Entities.Cactus)
def sortRow(direction=East, reverse=West, sortedTopRows=0):
	for round in range(1,get_world_size()):
		if measure() > measure(direction):
			swap(direction)
		stepsToDirection=max(1, get_world_size() - round - sortedTopRows - 1)
		newlySortedRows=1
		for _ in range(stepsToDirection):
			move(direction)
			if measure() > measure(direction):
				newlySortedRows=1
				swap(direction)
			else:
				newlySortedRows+=1
		action=False
		for _ in range(stepsToDirection - 1):
			if measure() < measure(reverse):
				action=swap(reverse)
			move(reverse)
		if measure() < measure(reverse):
			action=swap(reverse)
		if not action:
			return
		sortedTopRows+=newlySortedRows
def printCactus():
	quick_print("~~~~~~~~~~~~~~~~")
	movement.toCoordinates(0,get_world_size()-1)
	for _ in range(get_world_size()):
		output=[]
		for _ in range(get_world_size()):
			output.append(measure())
			move(East)
		quick_print(output)
		move(South)
	movement.toCoordinates(0, 0)

Globals.ITEM_TO_FUNCTION[Items.Cactus]=harvestCactus

if __name__ == "__main__":
	Globals.SETUP_FUNCTION_MAPS()
	harvestCactus(goal, [Unlocks.Cactus], "")
	quick_print(num_items(Items.Cactus))