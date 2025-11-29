import Debug
import Defer
import Globals
import Harvesting
from Preperations import workForPower
import UnlockHelper
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
		fullMaze=300
		prepareItems(fullMaze, currentlyUnlocking, indent)
		if num_items(Items.Gold) >= amount:
			return
		quick_print(indent, fullMaze , "/", -(amount - num_items(Items.Gold)) // (Globals.GLOBALS["AREA"] * -num_unlocked(Unlocks.Mazes)), "treasure chests")
		if not createMaze():
			continue
		solveMaze()
def prepareItems(fullMaze, currentlyUnlocking, indent):
	indent+="  "
	substanceNeeded=fullMaze * get_world_size() * 2**(num_unlocked(Unlocks.Mazes)-1)
	while True:
		harvestWeirdSubstance(substanceNeeded, currentlyUnlocking, indent)
		if not workForPower(Items.Gold, fullMaze, currentlyUnlocking, indent):
			break
def createMaze():
	Harvesting.forceHarvest()
	plant(Entities.Bush)
	while get_entity_type() == Entities.Bush:
		if not use_item(Items.Weird_Substance, get_world_size() * 2**(num_unlocked(Unlocks.Mazes)-1)):
			return False
	return True
def solveMaze():
	treasureMap=mazeExplorer.exploreMaze()
	regionSize=calcRegionSize()
	splitRegion(0, 0, get_world_size(), get_world_size(), regionSize, treasureMap, True)
	Defer.joinAll()
def calcRegionSize():
	sqrt=1
	if max_drones() > 1:
		if max_drones() >= 36:
			quick_print("WARNING: MORE DRONES THAN THOUGHT POSSIBLE")
			sqrt=6
		elif max_drones() >= 25:
			sqrt=5
		elif max_drones() >= 16:
			sqrt=4
		elif max_drones() >= 9:
			sqrt=3
		else:
			sqrt=2
	return get_world_size() // sqrt
def splitRegion(x1, y1, x2, y2, size, treasureMap, exec=False):
	def manage():
		while split():
			pass
		moveToRegion(insideBounds, treasureMap)
		while waitUntilInBounds():
			createInstructions(treasureMap)
			folowInstructions(treasureMap)
			if not moveTreasure():
				harvest()
				return
	def split():
		if x2 - x1 >= size * 2:
			newX2=(x2 - x1) / 2 // size * size + x1
			if splitRegion(x1, y1, newX2, y2, size, treasureMap):
				global x1
				x1=newX2
				return True
			return False
		if y2 - y1 >= size * 2:
			newY2=(y2 - y1) / 2 // size * size + y1
			if splitRegion(x1, y1, x2, newY2, size, treasureMap):
				global y1
				y1=newY2
				return True
		return False
	def waitUntilInBounds():
		lastCheck=get_time()
		while True:
			pos=measure()
			if get_entity_type() != Entities.Hedge:
				if get_entity_type() == Entities.Treasure:
					return True
				return False
			tx,ty=pos
			treasureInBoundingBox=insideBounds(tx, ty)
			if treasureInBoundingBox:
				return True
			if get_time() - lastCheck > 640 / get_world_size():
				lastCheck=get_time()
				if retestRegion(treasureMap, x1, y1, x2, y2, insideBounds):
					lastCheck*=16
	def insideBounds(x, y):
		return x >= x1 and x < x2 and y >= y1 and y < y2
	if exec:
		manage()
		return
	return spawn_drone(manage)
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
def retestRegion(tiles, x1, y1, x2, y2, insideBounds):
	if not insideBounds(get_pos_x(), get_pos_y()):
		return
	region=[]
	for x in range(x1, x2):
		row=[]
		region.append(row)
		for y in range(y1, y2):
			row.append(list(tiles[x][y]["knownGood"]))
	history=[]
	visited=set()
	while len(history) > 0 or len(region[get_pos_x()-x1][get_pos_y()-y1]):
		pos=movement.getPos()
		x,y=pos
		if len(region[x-x1][y-y1]):
			retestWalls(tiles, x, y)
			direction=region[x-x1][y-y1].pop()
			nx,ny=nextCoordinates(x,y,direction)
			if not insideBounds(nx, ny):
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
		if insideBounds(treasurePosition[0], treasurePosition[1]):
			resetOrigin(tiles, tiles[-1], {})
			return False
	resetOrigin(tiles, tiles[-1], {})
	for row in region:
		for tile in row:
			if len(tile):
				return False
	return True
def moveToRegion(insideBounds, tiles):
	if insideBounds(get_pos_x(), get_pos_y()):
		return
	tx,ty=measure()
	if insideBounds(tx, ty):
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
			if insideBounds(nextX, nextY):
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
if __name__ == "__main__":
	Debug.startBenchmark(Items.Gold, goal, 0)
