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
		return Preperations.expectedTilesNeeded(Items.Cactus, Unlocks.Cactus, amount, False, Globals.GLOBALS["AREA"])
	while num_items(Items.Cactus) < amount:
		tiles=Preperations.preperations(Items.Cactus, calculateTilesNeeded, currentlyUnlocking, indent, 1.1)
		ground.onlyPrepareGround(Grounds.Soil)
		quick_print(indent, amount, "Cactus using ~", tiles, "tiles")
		for _ in range(0, tiles, Globals.GLOBALS["AREA"]):
			dimensions=calcSize(amount - num_items(Items.Cactus))
			plantFieldFullOfCactus(dimensions)
def calcSize(missing):
	multiplier=Preperations.expectedYield(Unlocks.Cactus)
	for length in range(get_world_size() - 1, 0, -1):
		tiles=length ** 2
		cactusYield=tiles ** 2 * multiplier
		if cactusYield < missing:
			height=length + 1
			width=height
			while True:
				width -= 1
				cactusYield=(width * height) ** 2 * multiplier
				if cactusYield < missing:
					break
			return (width + 1, height)
	return (1, 1)
def plantFieldFullOfCactus(dimensions):
	movement.toCoordinates(0, 0)
	def plantColumn(start, end):
		start=Defer.splitAxis(start, end, plantColumn)
		for column in range(start, end):
			movement.toCoordinates(column, 0)
			plantCactus()
			for _ in range(dimensions[1] - 1):
				move(North)
				plantCactus()
				if measure() < measure(South): # pyright: ignore[reportOperatorIssue]
					swap(South)
			movement.toCoordinates(get_pos_x(), 0)
			sortRow(North, South, 1, dimensions[1])
	plantColumn(0, dimensions[0])
	Defer.joinAll()
	fullyGrownAt=get_time() + 1
	def sortHorizontal(start, end):
		start=Defer.splitAxis(start, end, sortHorizontal)
		for row in range(start, end):
			movement.toCoordinates(0, row)
			sortRow(East, West, 0, dimensions[0])
	sortHorizontal(0, dimensions[1])
	movement.toCoordinates(0, 0)
	Defer.joinAll()
	while get_time() < fullyGrownAt:
		pass
	Harvesting.forceHarvest()
def plantCactus():
	Harvesting.onlyKeep([Entities.Cactus])
	plant(Entities.Cactus)
def sortRow(direction, reverse, sortedTopRows, length):
	for round in range(1, length):
		if measure() > measure(direction): # pyright: ignore[reportOperatorIssue]
			swap(direction)
		stepsToDirection=length - round - sortedTopRows - 1
		if stepsToDirection <= 0:
			return
		newlySortedRows=1
		for _ in range(stepsToDirection):
			move(direction)
			if measure() > measure(direction): # pyright: ignore[reportOperatorIssue]
				newlySortedRows=1
				swap(direction)
			else:
				newlySortedRows+=1
		action=False
		for _ in range(stepsToDirection - 1):
			if measure() < measure(reverse): # pyright: ignore[reportOperatorIssue]
				action=swap(reverse)
			move(reverse)
		if measure() < measure(reverse): # pyright: ignore[reportOperatorIssue]
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
	Debug.startBenchmark(Items.Cactus, goal, 0, prepareTill) # pyright: ignore[reportUndefinedVariable]
