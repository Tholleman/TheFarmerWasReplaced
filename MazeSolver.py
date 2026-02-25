import Debug
import Defer
import Globals
import Harvesting
import MazeWaiter
import Preperations
import UnlockHelper
import Utils
from WeirdSubstance import harvestWeirdSubstance
import mazeExplorer
from MazeUtils import getTile, moveTreasure, nextCoordinates, resetOrigin, retestWalls
import movement

def gracefulRecover():
	if get_entity_type() not in [Entities.Hedge, Entities.Treasure]:
		return
	history=[]
	visited={movement.getPos(): [North, East, South, West]}
	while True:
		if get_entity_type() == Entities.Treasure:
			harvest()
			return
		while len(visited[movement.getPos()]) == 0:
			move(Globals.REVERSE[history.pop()])
		direction=visited[movement.getPos()].pop()
		if not move(direction):
			continue
		if movement.getPos() in visited:
			move(Globals.REVERSE[direction])
			continue
		history.append(direction)
		toTest=[North, East, South, West]
		toTest.remove(Globals.REVERSE[direction])
		visited[movement.getPos()]=toTest
def harvestGold(amount: int, currentlyUnlocking, indent: str):
	if num_items(Items.Gold) >= amount:
		return
	quick_print(indent, amount, "Gold")
	UnlockHelper.workToUnlock(Unlocks.Mazes, currentlyUnlocking, "  " + indent)
	while num_items(Items.Gold) < amount:
		size=calcSize(amount - num_items(Items.Gold))
		prepareItems(size, currentlyUnlocking, indent)
		if num_items(Items.Gold) >= amount:
			return
		quick_print(indent, "301 *", str(size) + "x" + str(size), "maze for", amount - num_items(Items.Gold), "gold")
		if createMaze(size):
			solveMaze(size, amount)
		if size != get_world_size():
			cleanup(size)
def calcSize(required: float) -> int:
	oneTreasure=Preperations.expectedYield(Unlocks.Mazes)
	# fiveFullTreasures=oneTreasure * get_world_size() ** 2 * 5
	# if required > fiveFullTreasures:
	# 	return get_world_size()
	fullYield=301*oneTreasure
	for size in range(get_world_size() - 1, 0, -1):
		sizeYield=size ** 2 * fullYield
		if sizeYield < required:
			return size + 1
	if required <= oneTreasure:
		return 1
	return 2
def prepareItems(size, currentlyUnlocking, indent):
	indent+="  "
	substanceNeeded=300 * size * 2**(num_unlocked(Unlocks.Mazes)-1)
	harvestWeirdSubstance(substanceNeeded, currentlyUnlocking, indent)
	while True:
		Preperations.orderPowerNeeded(Items.Gold, 301 * size**2, currentlyUnlocking)
		if not Preperations.workForPower(currentlyUnlocking, indent):
			break
def createMaze(size: int):
	if size != get_world_size():
		movement.toCoordinates(0, 0)
	Harvesting.forceHarvest()
	plant(Entities.Bush)
	while get_entity_type() == Entities.Bush:
		if not use_item(Items.Weird_Substance, size * 2**(num_unlocked(Unlocks.Mazes)-1)):
			return False
	return True
def solveMaze(size: int, amount: int):
	oneTreasure = Preperations.expectedYield(Unlocks.Mazes)
	tiles = mazeExplorer.exploreMaze(size)
	context: MazeContext = {"connectedRegion": max_drones() == 1, "drawnOn": set(), "lastCheck": get_time()} # pyright: ignore[reportAssignmentType]
	def manageRegion(c1: Coordinate, c2: Coordinate):
		c1 = Defer.splitRegion(c1, c2, manageRegion)
		moveToRegion(c1, c2, tiles)
		while MazeWaiter.waitUntilInBounds(c1, c2, tiles, context):
			createInstructions(tiles, context)
			folowInstructions(tiles)
			if num_items(Items.Gold) + oneTreasure >= amount or not moveTreasure(size):
				harvest()
				return
	manageRegion((0, 0), (size, size))
	Debug.changeHat(Hats.Straw_Hat)
	Defer.joinAll()
def createInstructions(tiles: MazeField, context: MazeContext):
	if get_entity_type() == Entities.Treasure:
		return
	resetOrigin(tiles, context["drawnOn"])
	treasureLocation: Coordinate = measure() # pyright: ignore[reportAssignmentType]
	context["drawnOn"] = set()
	queue = [treasureLocation]
	context["drawnOn"].add(treasureLocation)
	tiles[treasureLocation[0]][treasureLocation[1]]["distance"] = 0
	while True:
		x, y = queue.pop(0)
		tile = tiles[x][y]
		origin = Globals.REVERSE[tile["origin"]]
		furtherDistance: int = tile["distance"] + 1 # pyright: ignore[reportOptionalOperand]
		for direction in tile["knownGood"]:
			if direction == origin:
				continue
			coordinate = nextCoordinates(x, y, direction)
			if coordinate in context["drawnOn"]:
				continue
			nextX, nextY = coordinate
			nextTile = tiles[nextX][nextY]
			nextTile["origin"] = direction
			nextTile["distance"] = furtherDistance
			context["drawnOn"].add(coordinate)
			if nextX == get_pos_x() and nextY == get_pos_y():
				return
			queue.append(coordinate)
def folowInstructions(tiles: MazeField):
	while get_entity_type() != Entities.Treasure:
		becamePath = retestWalls(tiles, get_pos_x(), get_pos_y())
		shorterPath = getShorterPath(tiles, becamePath)
		if shorterPath:
			move(shorterPath)
			continue
		tile = tiles[get_pos_x()][get_pos_y()]
		move(Globals.REVERSE[tile["origin"]])
	retestWalls(tiles, get_pos_x(), get_pos_y())
def getShorterPath(tiles: MazeField, becamePath: set[Direction]):
	if len(becamePath):
		tile = tiles[get_pos_x()][get_pos_y()]
		for direction in becamePath:
			targetTile = getTile(tiles, get_pos_x(), get_pos_y(), direction)
			if targetTile["distance"] != None and targetTile["distance"] < tile["distance"]: # pyright: ignore[reportOperatorIssue]
				return direction
	return None
def moveToRegion(c1: Coordinate, c2: Coordinate, tiles: MazeField):
	if movement.isWithin(movement.getPos(), c1, c2):
		return
	if movement.isWithin(measure(), c1, c2): # pyright: ignore[reportArgumentType]
		return
	queue = [movement.getPos()]
	drawnOn = set()
	while True:
		x, y = queue.pop(0)
		tile = tiles[x][y]
		origin = Globals.REVERSE[tile["origin"]]
		for direction in tile["knownGood"]:
			if direction == origin:
				continue
			tuple = nextCoordinates(x,y,direction)
			if tuple in drawnOn:
				continue
			nextX, nextY = tuple
			nextTile = tiles[nextX][nextY]
			nextTile["origin"] = direction
			drawnOn.add(tuple)
			if movement.isWithin(tuple, c1, c2):
				instructions = []
				tile = tiles[nextX][nextY]
				while tile["origin"] != None:
					instructions.append(tile["origin"])
					nextX, nextY = nextCoordinates(nextX, nextY, Globals.REVERSE[instructions[-1]])
					tile = tiles[nextX][nextY]
				while len(instructions):
					move(instructions.pop())
				resetOrigin(tiles, drawnOn)
				return
			queue.append(tuple)
def printDirectionMap(tiles):
	for y in range(get_world_size() - 1, -1, -1):
		output=[]
		for x in range(get_world_size()):
			tile=tiles[x][y]
			if tile["origin"] == None:
				output.append(" ")
			elif tile["origin"] == North:
				output.append("↓")
			elif tile["origin"] == South:
				output.append("↑")
			elif tile["origin"] == East:
				output.append("←")
			else:
				output.append("→")
		quick_print(output)
	quick_print("")
def cleanup(size):
	end=get_world_size() - 1
	movement.toCoordinates(end, end)
	if get_ground_type() != Grounds.Grassland:
		move(North)
		move(East)
		direction=North
		def tillMazeColumn():
			movement.actMoveAct(till, size, direction)
		def deferTill():
			if not spawn_drone(tillMazeColumn):
				tillMazeColumn()
				global direction
				direction=Utils.ternary(direction == North, South, North) # pyright: ignore[reportUnboundVariable]
		movement.actMoveAct(deferTill, size, East)
		Defer.joinAll()
if __name__ == "__main__":
	Debug.startBenchmark(Items.Gold, goal, 0) # pyright: ignore[reportUndefinedVariable]
