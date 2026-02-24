import Utils
import movement

def defer(action: Callable):
	pid = spawn_drone(action)
	if pid:
		return pid
	pos = movement.getPos()
	action()
	movement.toPos(pos)
	return None
def spawnMoveAct(action: Callable, dronesNeeded: int, direction: Direction, rows = 1):
	for _ in range(dronesNeeded - 1):
		spawn_drone(action)
		for _ in range(rows):
			move(direction)
	action()
	joinAll()
def joinAll():
	while num_drones() > 1:
		pass
def join(pids: list[Drone]):
	for pid in pids:
		wait_for(pid)
def everyTile(action: Callable):
	def fullColumn():
		movement.actMoveAct(action, get_world_size(), North)
	if num_unlocked(Unlocks.Expand) < 2:
		fullColumn()
		return
	if max_drones() == 1:
		movement.actMoveAct(fullColumn, get_world_size(), East)
		return
	halfColumnDroneCount: int = min(max((max_drones() - get_world_size()) // 2, 0), get_world_size())
	fullColumnDroneCount: int = get_world_size() - halfColumnDroneCount
	def splitColumn():
		def act(direction = North, minus = 0):
			movement.actMoveAct(action, (get_world_size() - minus) / 2, direction)
		if spawn_drone(act):
			move(South)
			act(South, 1)
		else:
			fullColumn()
	def halfField(direction = West, minus = 0):
		for _ in range((fullColumnDroneCount // 2 - minus) - 1):
			_=spawn_drone(fullColumn) or fullColumn()
			move(direction)
		if halfColumnDroneCount > 0:
			if fullColumnDroneCount > 0:
				_=spawn_drone(fullColumn) or fullColumn()
				move(direction)
			for _ in range((halfColumnDroneCount / 2 - minus) - 1):
				_=spawn_drone(splitColumn) or fullColumn()
				move(direction)
			splitColumn()
		else:
			fullColumn()
	spawn_drone(halfField)
	move(East)
	halfField(East, get_world_size() % 2)
	joinAll()
def dronesNeeded(tiles: int) -> Tuple[int, float]:
	dronesNeeded: int = max(min(tiles / get_world_size(), get_world_size(), max_drones()), 1)
	tilesPerDrone = tiles / dronesNeeded
	return dronesNeeded, tilesPerDrone
# Returns the new corner1
# The action must take 2 arguments, the bottom left corner (incl) and the top right corner (excl)
# Example:
# def action(c1, c2):
# 	c1=Defer.splitRegion(c1, c2, action)
# 	movement.toRegion(c1, c2)
# action((0,0), (get_world_size(), get_world_size()))
def splitRegion(corner1: Coordinate, corner2: Coordinate, action: Callable[[Coordinate, Coordinate], None]) -> Coordinate:
	sizes=Utils.dimensions(corner1, corner2)
	changeI=Utils.ternary(sizes[0] > sizes[1], 0, 1)
	if sizes[changeI] == 1:
		return corner1
	unchangedI=(changeI + 1) % 2
	half=corner1[changeI] + sizes[changeI] // 2
	def makeCorner(other: int) -> Coordinate:
		if changeI == 0:
			return (half, other)
		return (other, half)
	def passCorner():
		action(corner1, makeCorner(corner2[unchangedI]))
	if spawn_drone(passCorner):
		return splitRegion(makeCorner(corner1[unchangedI]), corner2, action)
	return corner1
def splitAxis(axis1: int, axis2: int, action: Callable[[int, int]]) -> int:
	if axis2 - axis1 <= 1:
		return axis1
	half=(axis1 + axis2) // 2
	def passAxis():
		action(axis1, half)
	if spawn_drone(passAxis):
		return splitAxis(half, axis2, action)
	return axis1