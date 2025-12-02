import Debug
import Defer
import UnlockHelper
import Preperations
import Globals
import Harvesting
import Utils
import movement
import ground

def harvestCactus(amount, currentlyUnlocking, indent):
	if num_items(Items.Cactus) > amount:
		return
	quick_print(indent, amount, "Cactus")
	UnlockHelper.workToUnlock(Unlocks.Cactus, currentlyUnlocking, "  " + indent)
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Cactus, Unlocks.Cactus, amount, False, Globals.GLOBALS["AREA"])
		return Utils.roundTo(tiles, Globals.GLOBALS["AREA"])
	while num_items(Items.Cactus) < amount:
		tiles=Preperations.preperations(Items.Cactus, calculateTilesNeeded, currentlyUnlocking, indent)
		ground.onlyPrepareGround(Grounds.Soil)
		quick_print(indent, amount, "Cactus using", tiles / Globals.GLOBALS["AREA"], "fields")
		for _ in range(0, tiles, Globals.GLOBALS["AREA"]):
			plantFieldFullOfCactus()
def plantFieldFullOfCactus():
	movement.toCoordinates(0, 0)
	for action, direction in [(plantColumn, East), (sortRow, North)]:
		for i in range(get_world_size()):
			if (i+1) % max_drones():
				while num_drones() == max_drones() and max_drones() > 1:
					pass
			Defer.defer(action)
			move(direction)
		Defer.joinAll()
	Harvesting.forceHarvest()
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
	Debug.startBenchmark(Items.Cactus, goal, 0, prepareTill)
