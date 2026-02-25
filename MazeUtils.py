import Globals


def moveTreasure(size: int):
	return use_item(Items.Weird_Substance, size * 2**(num_unlocked(Unlocks.Mazes)-1))
def popSet[T](set: set[T]):
	for first in set:
		set.remove(first)
		return first
def getTile(tiles: MazeField, x: int, y: int, direction: Direction):
	x, y = nextCoordinates(x, y, direction)
	return tiles[x][y]
def nextCoordinates(x: int, y: int, direction: Direction) -> Coordinate:
	if direction == North:
		return x, y + 1
	if direction == South:
		return x, y - 1
	if direction == East:
		return x + 1, y
	if direction == West:
		return x - 1, y
	return x, y
def retestWalls(tiles: list[list[MazeCell]], x: int, y: int):
	tile = tiles[x][y]
	becamePath: set[Direction] = set()
	if not len(tile["knownWalls"]):
		return becamePath
	for direction in tile["knownWalls"]:
		if can_move(direction):
			targetTile = getTile(tiles, x, y, direction)
			becamePath.add(direction)
			tile["knownGood"].add(direction)
			targetTile["knownWalls"].remove(Globals.REVERSE[direction])
			targetTile["knownGood"].add(Globals.REVERSE[direction])
	for path in becamePath:
		tile["knownWalls"].remove(path)
	return becamePath
def resetOrigin(tiles: MazeField, toReset: set[Coordinate]):
	for pos in toReset:
		tile = tiles[pos[0]][pos[1]]
		tile["origin"] = None
		tile["distance"] = None
