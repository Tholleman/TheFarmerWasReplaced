import Debug
from Globals import REVERSE
import Globals
import MazeSolver
from movement import *
import MazeUtils

def exploreMaze(size: int) -> MazeField:
	log = createExplorer(None, size)()
	tiles = initTiles(size)
	while len(log["orphans"]):
		mergeLog(log, wait_for(log["orphans"].pop(0)))
		mapTiles(tiles, log)
	mapTiles(tiles, log)
	for i in range(size):
		tiles[0][i]["knownWalls"].remove(West)
		tiles[size-1][i]["knownWalls"].remove(East)
		tiles[i][0]["knownWalls"].remove(South)
		tiles[i][size-1]["knownWalls"].remove(North)
	# printMap(tiles)
	return tiles
def mapTiles(tiles, log):
	added = set()
	for key in log:
		if key == "orphans":
			continue
		x,y = key
		tiles[x][y] = log[key]
		added.add(key)
	for pos in added:
		log.pop(pos)
def initTiles(size: int):
	tiles=[]
	for _ in range(size):
		column=[]
		for _ in range(size):
			column.append(None)
		tiles.append(column)
	return tiles
def createExplorer(direction: Direction | None, size: int):
	def explorer():
		history=[]
		currentTile={
			"untested":{North, East, South, West},
			"knownGood":{REVERSE[direction]},
			"knownWalls":set(),
			"origin":None,
			"distance":None
		}
		if direction != None:
			currentTile["untested"].remove(REVERSE[direction])
			move(direction)
		else:
			currentTile["knownGood"].remove(None)
		log: dict[Any, Any]={(get_pos_x(), get_pos_y()): currentTile}
		children=[]
		while len(history) or len(currentTile["untested"]):
			setWalls(currentTile)
			if max_drones() == 1:
				handleTreasure(log, currentTile, size)
			newDirection = MazeUtils.popSet(currentTile["untested"])
			if newDirection != None:
				currentTile["knownGood"].add(newDirection)
				pid=None
				if len(currentTile["untested"]) or len(history):
					pid = spawn_drone(createExplorer(newDirection, size))
				if pid:
					children.append(pid)
				else:
					if len(history) or len(currentTile["untested"]):
						history.append(newDirection)
					move(newDirection)
					currentTile = {
						"untested":{North, East, South, West},
						"knownGood":{REVERSE[newDirection]},
						"knownWalls":set(),
						"origin":None,
						"distance":None
					}
					currentTile["untested"].remove(REVERSE[newDirection])
					log[(get_pos_x(), get_pos_y())] = currentTile
			elif len(history):
				move(REVERSE[history.pop()])
				currentTile=log[(get_pos_x(), get_pos_y())]
		for pos in log:
			log[pos].pop("untested")
		log["orphans"]=[]
		for pid in children:
			if has_finished(pid):
				childLog=wait_for(pid)
				mergeLog(log, childLog)
			else:
				log["orphans"].append(pid)
		return log
	return explorer
def setWalls(currentTile):
	walls=set()
	for direction in currentTile["untested"]:
		if not can_move(direction):
			walls.add(direction)
	for wall in walls:
		currentTile["untested"].remove(wall)
		currentTile["knownWalls"].add(wall)
def handleTreasure(log, currentTile, size):
	if get_entity_type() == Entities.Treasure:
		MazeUtils.moveTreasure(size)
	toRemove = set()
	for direction in currentTile["untested"]:
		coordinate = MazeUtils.nextCoordinates(get_pos_x(), get_pos_y(), direction)
		if coordinate in log:
			toRemove.add(direction)
			currentTile["knownGood"].add(direction)
			otherTile = log[coordinate]
			reverse = Globals.REVERSE[direction]
			Utils.safeRemove(otherTile["untested"], reverse)
			Utils.safeRemove(otherTile["knownWalls"], reverse)
			otherTile["knownGood"].add(reverse)
	for direction in toRemove:
		currentTile["untested"].remove(direction)
def mergeLog(log, childLog):
	for orphan in childLog.pop("orphans"):
		if has_finished(orphan):
			mergeLog(log, wait_for(orphan))
		else:
			log["orphans"].append(orphan)
	for pos in childLog:
		if pos in log:
			throw=0/0
		else:
			log[pos] = childLog[pos]
def printMap(tiles: MazeField):
	pathMap=["╨", "╞", "╚", "╥",
			 "║", "╔", "╠", "╡",
			 "╝", "═", "╩", "╗",
			 "╣", "╦", "╬"]
	for y in range(len(tiles) - 1, -1, -1):
		output=""
		for x in range(len(tiles) - 1):
			tile=tiles[x][y]
			index=-1
			if North in tile["knownGood"]:
				index+=1
			if East in tile["knownGood"]:
				index+=2
			if South in tile["knownGood"]:
				index+=4
			if West in tile["knownGood"]:
				index+=8
			output+=pathMap[index]
		quick_print(output)
	quick_print("")
