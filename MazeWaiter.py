import Debug
import Globals
import MazeSolver
import MazeUtils
import Utils
import movement


def waitUntilInBounds(c1: Coordinate, c2: Coordinate, tiles: MazeField, context: MazeContext) -> bool:
	withinBounds = isWithinBounds(c1, c2)
	if withinBounds != "no":
		return withinBounds == "yes"
	if not context["connectedRegion"]:
		if theoraticalTesting(c1, c2, tiles):
			isolateRegion(c1, c2, tiles, context)
		elif get_time() - context["lastCheck"] > 640 / get_world_size():
			context["lastCheck"] = get_time()
			if retestRegion(tiles, c1, c2, context):
				isolateRegion(c1, c2, tiles, context)
		withinBounds = isWithinBounds(c1, c2)
		if withinBounds != "no":
			return withinBounds == "yes"
	precalc(c1, c2, tiles, context)
	return isWithinBounds(c1, c2) == "yes"
def isWithinBounds(c1: Coordinate, c2: Coordinate) -> Literal['yes', 'no', 'not a maze']:
	pos: Coordinate = measure() # pyright: ignore[reportAssignmentType]
	if get_entity_type() != Entities.Hedge:
		if get_entity_type() == Entities.Treasure:
			return "yes"
		return "not a maze"
	return Utils.ternary(movement.isWithin(pos, c1, c2), "yes", "no")
def theoraticalTesting(c1: Coordinate, c2: Coordinate, tiles: MazeField):
	width, height = Utils.dimensions(c1, c2)
	tracker: dict[Direction, MazeTracker] = {
		North: {"i": 1, "pos": c2[1] - 1, "remaining": width},
		East:  {"i": 0, "pos": c2[0] - 1, "remaining": height},
		South: {"i": 1, "pos": c1[1], "remaining": width},
		West:  {"i": 0, "pos": c1[0], "remaining": height}
	}
	def isAtEdge(pos: Coordinate):
		return pos[tracker[edge]["i"]] == tracker[edge]["pos"]
	queue = [c1]
	visited = {c1}
	while len(queue):
		pos = queue.pop(0)
		x, y = pos
		tile = tiles[x][y]
		directions = list(tile["knownGood"])
		for edge in tracker:
			if isAtEdge(pos):
				tracker[edge]["remaining"] -= 1
				if edge in directions:
					directions.remove(edge)
		for direction in directions:
			toAdd = MazeUtils.nextCoordinates(x, y, direction)
			if toAdd not in visited:
				queue.append(toAdd)
				visited.add(toAdd)
	for direction in tracker:
		if tracker[direction]["remaining"] > 0:
			return False
	return True
def isolateRegion(c1: Coordinate, c2: Coordinate, tiles: MazeField, context: MazeContext):
	Debug.changeHat(Hats.Green_Hat)
	context["connectedRegion"] = True
	for x in range(c1[0], c2[0]):
		Utils.safeRemove(tiles[x][c1[1]]["knownWalls"], South)
		Utils.safeRemove(tiles[x][c1[1]]["knownGood"], South)
		Utils.safeRemove(tiles[x][c2[1] - 1]["knownWalls"], North)
		Utils.safeRemove(tiles[x][c2[1] - 1]["knownGood"], North)
	for y in range(c1[1], c2[1]):
		Utils.safeRemove(tiles[c1[0]][y]["knownWalls"], West)
		Utils.safeRemove(tiles[c1[0]][y]["knownGood"], West)
		Utils.safeRemove(tiles[c2[0] - 1][y]["knownWalls"], East)
		Utils.safeRemove(tiles[c2[0] - 1][y]["knownGood"], East)
def retestRegion(tiles: MazeField, c1: Coordinate, c2: Coordinate, context: MazeContext):
	# if not movement.isWithin((get_pos_x(), get_pos_y()), c1, c2):
	# 	Debug.fail()
	# 	return False
	x1, y1 = c1
	x2, y2 = c2
	region: list[list[list[Direction]]] = []
	for x in range(x1, x2):
		row = []
		region.append(row)
		for y in range(y1, y2):
			row.append(list(tiles[x][y]["knownGood"]))
	for x in range(0, x2 - x1):
		Utils.safeRemove(region[x][0], South)
		Utils.safeRemove(region[x][-1], North)
	for y in range(0, y2 - y1):
		Utils.safeRemove(region[0][y], West)
		Utils.safeRemove(region[-1][y], East)
	history: list[Direction] = []
	visited: set[Coordinate] = set()
	while len(history) > 0 or len(region[get_pos_x()-x1][get_pos_y()-y1]):
		x, y = movement.getPos()
		for nowGood in MazeUtils.retestWalls(tiles, x, y):
			if movement.isWithin(MazeUtils.nextCoordinates(x, y, nowGood), c1, c2):
				region[x - x1][y - y1].append(nowGood)
		if len(region[x - x1][y - y1]):
			direction = region[x - x1][y - y1].pop()
			nPos = MazeUtils.nextCoordinates(x, y, direction)
			if nPos in visited:
				continue
			visited.add(nPos)
			move(direction)
			nx, ny = nPos
			Utils.safeRemove(region[nx - x1][ny - y1], Globals.REVERSE[direction])
			if len(history) or len(region[x-x1][y-y1]):
				history.append(direction)
		else:
			move(Globals.REVERSE[history.pop()])
		if isWithinBounds(c1, c2) != "no":
			return False
	width, height = Utils.dimensions(c1, c2)
	return len(visited) == width * height
def precalc(c1: Coordinate, c2: Coordinate, tiles: MazeField, context: MazeContext):
	width, height = Utils.dimensions(c1, c2)
	remaining = width * height - 1
	tilesProcessed = 0
	MazeUtils.resetOrigin(tiles, context["drawnOn"])
	coordinate = (get_pos_x(), get_pos_y())
	queue: list[Coordinate] = [coordinate]
	context["drawnOn"] = {coordinate}
	while remaining > 0:
		if shortEnd(c1, c2, tiles, tilesProcessed):
			return
		tilesProcessed += 1
		x, y = queue.pop(0)
		tile = tiles[x][y]
		origin = Globals.REVERSE[tile["origin"]]
		for direction in tile["knownGood"]:
			if direction == origin:
				continue
			coordinate = MazeUtils.nextCoordinates(x, y, direction)
			if coordinate in context["drawnOn"]:
				continue
			if movement.isWithin(coordinate, c1, c2):
				remaining -= 1
			nextX, nextY = coordinate
			nextTile = tiles[nextX][nextY]
			nextTile["origin"] = direction
			context["drawnOn"].add(coordinate)
			queue.append(coordinate)
	while True:
		withinBounds = isWithinBounds(c1, c2)
		while withinBounds == "no":
			withinBounds = isWithinBounds(c1, c2)
		if get_entity_type() == Entities.Treasure and MazeUtils.moveTreasure(len(tiles)):
			continue
		break
	if withinBounds == "not a maze":
		return
	moveToTreasure(tiles)
def shortEnd(c1: Coordinate, c2: Coordinate, tiles: MazeField, tilesProcessed: int) -> bool:
	if tilesProcessed % 20 != 0:
		return False
	withinBounds = isWithinBounds(c1, c2)
	if withinBounds == "no":
		return False
	if withinBounds == "not a maze":
		return True
	pos: Coordinate = measure() # pyright: ignore[reportAssignmentType]
	if tiles[pos[0]][pos[1]]["origin"] != None:
		moveToTreasure(tiles)
	return True
def moveToTreasure(tiles: MazeField):
	x, y = measure() # type: ignore
	distance = 0
	lastDirection = None
	while tiles[x][y]["origin"] != None:
		tiles[x][y]["origin"], lastDirection = lastDirection, Globals.REVERSE[tiles[x][y]["origin"]]
		tiles[x][y]["distance"] = distance
		distance += 1
		x, y = MazeUtils.nextCoordinates(x, y, lastDirection)
	# if (x, y) != movement.getPos():
	# 	Debug.fail()
	tiles[get_pos_x()][get_pos_y()]["origin"] = lastDirection
	tiles[get_pos_x()][get_pos_y()]["distance"] = distance
	MazeSolver.folowInstructions(tiles)