import Debug
import Defer
import Globals
import Harvesting
import Preperations
import UnlockHelper
import Utils
from WeirdSubstance import harvestWeirdSubstance
import mazeExplorer
from MazeUtils import getTile, moveTreasure, nextCoordinates
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
def harvestGold(amount, currentlyUnlocking, indent):
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
			solveMaze(size)
		if size != get_world_size():
			cleanup(size)
def calcSize(required):
	oneTreasure=2**(num_unlocked(Unlocks.Mazes)-1)
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
def createMaze(size):
	if size != get_world_size():
		movement.toCoordinates(0, 0)
	Harvesting.forceHarvest()
	plant(Entities.Bush)
	while get_entity_type() == Entities.Bush:
		if not use_item(Items.Weird_Substance, size * 2**(num_unlocked(Unlocks.Mazes)-1)):
			return False
	return True
def solveMaze(size):
	treasureMap=mazeExplorer.exploreMaze(size)
	def manageRegion(c1, c2):
		c1=Defer.splitRegion(c1, c2, manageRegion)
		moveToRegion(c1, c2, treasureMap)
		while waitUntilInBounds(c1, c2, treasureMap):
			createInstructions(treasureMap)
			folowInstructions(treasureMap)
			if not moveTreasure(size):
				harvest()
				return
	manageRegion((0, 0), (size, size))
	Defer.joinAll()
def waitUntilInBounds(c1, c2, treasureMap):
	lastCheck=get_time()
	while True:
		pos=measure()
		if get_entity_type() != Entities.Hedge:
			if get_entity_type() == Entities.Treasure:
				return True
			return False
		treasureInBoundingBox=movement.isWithin(pos, c1, c2)
		if treasureInBoundingBox:
			return True
		if get_time() - lastCheck > 640 / get_world_size():
			lastCheck=get_time()
			if retestRegion(treasureMap, c1, c2):
				lastCheck*=16
def createInstructions(tiles):
	if get_entity_type() == Entities.Treasure:
		return
	treasureLocation=measure()
	queue=[treasureLocation]
	drawnOn=set()
	# resetOrigin(tiles, tiles[-1], drawnOn)
	if tiles[treasureLocation[0]][treasureLocation[1]]["origin"]!=None:
		followReverseInstructions(tiles, treasureLocation, drawnOn)
		resetOrigin(tiles, tiles[-1], drawnOn)
		tiles[-1]=drawnOn
		return
	while True:
		x,y=queue.pop(0)
		tile=tiles[x][y]
		origin=Globals.REVERSE[tile["origin"]]
		for direction in tile["knownGood"]:
			if direction == origin:
				continue
			tuple=nextCoordinates(x,y,direction)
			if tuple in drawnOn:
				continue
			nextX,nextY=tuple
			nextTile=tiles[nextX][nextY]
			if nextTile["origin"] != None:
				followReverseInstructions(tiles, tuple, drawnOn)
			nextTile["origin"]=direction
			drawnOn.add(tuple)
			if nextX == get_pos_x() and nextY == get_pos_y():
				resetOrigin(tiles, tiles[-1], drawnOn)
				tiles[-1]=drawnOn
				return
			queue.append(tuple)
def resetOrigin(tiles, toReset, dontReset):
	for pos in toReset:
		if pos not in dontReset:
			tiles[pos[0]][pos[1]]["origin"]=None
def folowInstructions(tiles):
	while get_entity_type() != Entities.Treasure:
		tile=retestWalls(tiles, get_pos_x(), get_pos_y())
		move(Globals.REVERSE[tile["origin"]])
	retestWalls(tiles, get_pos_x(), get_pos_y())
def retestWalls(tiles, x, y):
	tile=tiles[x][y]
	if not len(tile["knownWalls"]):
		return tile
	becamePath=set()
	for direction in tile["knownWalls"]:
		if can_move(direction):
			targetTile=getTile(tiles, x, y, direction)
			becamePath.add(direction)
			tile["knownGood"].add(direction)
			targetTile["knownWalls"].remove(Globals.REVERSE[direction])
			targetTile["knownGood"].add(Globals.REVERSE[direction])
	for path in becamePath:
		tile["knownWalls"].remove(path)
	return tile
def followReverseInstructions(tiles, treasureLocation, drawnOn):
	instructions=[]
	pos=treasureLocation
	x,y=pos
	direction=tiles[x][y]["origin"]
	while direction != None:
		instructions.append(direction)
		reverse=Globals.REVERSE[direction]
		tiles[x][y]["origin"]=reverse
		# drawnOn.add(pos)
		pos=nextCoordinates(x, y, reverse)
		x,y=pos
		direction=tiles[x][y]["origin"]
	for direction in instructions[::-1]:
		move(direction)
def retestRegion(tiles, c1, c2):
	if not movement.isWithin((get_pos_x(), get_pos_y()), c1, c2):
		return
	x1, y1=c1
	x2, y2=c2
	region=[]
	for x in range(x1, x2):
		row=[]
		region.append(row)
		for y in range(y1, y2):
			row.append(list(tiles[x][y]["knownGood"]))
	history=[]
	visited=set()
	while len(history) > 0 or len(region[get_pos_x()-x1][get_pos_y()-y1]):
		x,y=movement.getPos()
		if len(region[x-x1][y-y1]):
			retestWalls(tiles, x, y)
			direction=region[x-x1][y-y1].pop()
			nx,ny=nextCoordinates(x,y,direction)
			if not movement.isWithin((nx, ny), c1, c2):
				continue
			if (nx, ny) in visited:
				continue
			visited.add((nx, ny))
			move(direction)
			region[nx-x1][ny-y1].remove(Globals.REVERSE[direction])
			if len(history) or len(region[x-x1][y-y1]):
				history.append(direction)
		else:
			move(Globals.REVERSE[history.pop()])
		treasurePosition=measure()
		if treasurePosition == None or len(treasurePosition) != 2:
			return False
		if movement.isWithin(treasurePosition, c1, c2):
			resetOrigin(tiles, tiles[-1], {})
			return False
	resetOrigin(tiles, tiles[-1], {})
	for row in region:
		for tile in row:
			if len(tile):
				return False
	return True
def moveToRegion(c1, c2, tiles):
	if movement.isWithin((get_pos_x(), get_pos_y()), c1, c2):
		return
	if movement.isWithin(measure(), c1, c2):
		return
	queue=[(get_pos_x(), get_pos_y())]
	drawnOn=set()
	resetOrigin(tiles, tiles[-1], drawnOn)
	while True:
		x,y=queue.pop(0)
		tile=tiles[x][y]
		origin=Globals.REVERSE[tile["origin"]]
		for direction in tile["knownGood"]:
			if direction == origin:
				continue
			tuple=nextCoordinates(x,y,direction)
			if tuple in drawnOn:
				continue
			nextX,nextY=tuple
			nextTile=tiles[nextX][nextY]
			nextTile["origin"]=direction
			drawnOn.add(tuple)
			if movement.isWithin(tuple, c1, c2):
				instructions=[]
				tile=tiles[nextX][nextY]
				while tile["origin"] != None:
					instructions.append(tile["origin"])
					nextX, nextY=nextCoordinates(nextX, nextY, Globals.REVERSE[instructions[-1]])
					tile=tiles[nextX][nextY]
				while len(instructions):
					move(instructions.pop())
				resetOrigin(tiles, drawnOn, set())
				tiles[-1]=set()
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
				direction=Utils.ternary(direction == North, South, North)
		movement.actMoveAct(deferTill, size, East)
		Defer.joinAll()
if __name__ == "__main__":
	Debug.startBenchmark(Items.Gold, goal, 0)
