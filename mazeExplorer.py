from Globals import REVERSE
import MazeSolver
from movement import *
from MazeUtils import popSet, moveTreasure

def exploreMaze():
	log=createExplorer(None)()
	tiles=initTiles()
	while len(log["orphans"]):
		mergeLog(log, wait_for(log["orphans"].pop(0)))
		mapTiles(tiles, log)
	mapTiles(tiles, log)
	size=get_world_size()
	for i in range(size):
		tiles[0][i]["knownWalls"].remove(West)
		tiles[size-1][i]["knownWalls"].remove(East)
		tiles[i][0]["knownWalls"].remove(South)
		tiles[i][size-1]["knownWalls"].remove(North)
	# printMap(tiles)
	return tiles
def mapTiles(tiles, log):
	added=set()
	for key in log:
		if key == "orphans":
			continue
		x,y=key
		tiles[x][y]=log[key]
		added.add(key)
	for pos in added:
		log.pop(pos)
def initTiles():
	tiles=[]
	size=get_world_size()
	for _ in range(size):
		column=[]
		for _ in range(size):
			# column.append({"untested":{North, East, South, West},"knownGood":set(),"knownWalls":set(),"origin":None})
			column.append(None)
		tiles.append(column)
	tiles.append(set())
	return tiles
def createExplorer(direction):
	def explorer():
		history=[]
		currentTile={"untested":{North, East, South, West},"knownGood":{REVERSE[direction]},"knownWalls":set(),"origin":None}
		if direction != None:
			currentTile["untested"].remove(REVERSE[direction])
			move(direction)
		else:
			currentTile["knownGood"].remove(None)
		log={(get_pos_x(), get_pos_y()): currentTile}
		children=[]
		while len(history) or len(currentTile["untested"]):
			setWalls(currentTile)
			newDirection=popSet(currentTile["untested"])
			if newDirection != None:
				currentTile["knownGood"].add(newDirection)
				pid=None
				if len(currentTile["untested"]):
					pid=spawn_drone(createExplorer(newDirection))
				if pid:
					children.append(pid)
				else:
					if len(history) or len(currentTile["untested"]):
						history.append(newDirection)
					move(newDirection)
					currentTile={"untested":{North, East, South, West},"knownGood":{REVERSE[newDirection]},"knownWalls":set(),"origin":None}
					currentTile["untested"].remove(REVERSE[newDirection])
					log[(get_pos_x(), get_pos_y())]=currentTile
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
def mergeLog(log, childLog):
	for orphan in childLog.pop("orphans"):
		if has_finished(orphan):
			mergeLog(log, wait_for(orphan))
		else:
			log["orphans"].append(orphan)
	for pos in childLog:
		if pos in log:
			a=0/0
		else:
			log[pos]=childLog[pos]
def printMap(tiles):
	pathMap=["╨", "╞", "╚", "╥",
			 "║", "╔", "╠", "╡",
			 "╝", "═", "╩", "╗",
			 "╣", "╦", "╬"]
	for y in range(get_world_size() - 1, -1, -1):
		output=""
		for x in range(get_world_size()):
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
if __name__ == "__main__":
	Globals.SETUP_FUNCTION_MAPS()
	MazeSolver.createMaze()
	exploreMaze()