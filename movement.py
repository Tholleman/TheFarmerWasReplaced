import Utils


def getPos() -> Coordinate:
	return (get_pos_x(), get_pos_y())
def toPos(pos: Coordinate):
	toCoordinates(pos[0], pos[1])
def toCoordinates(x: int, y: int):
	goWest=(get_pos_x() - x + get_world_size()) % get_world_size() < get_world_size() / 2
	direction = Utils.ternary(goWest, West, East)
	while get_pos_x() != x:
		move(direction)
	goSouth = (get_pos_y() - y + get_world_size()) % get_world_size() < get_world_size() / 2
	direction = Utils.ternary(goSouth, South, North)
	while get_pos_y() != y:
		move(direction)
def actMoveAct(action: Callable, count: int, direction: Direction):
	for _ in range(count - 1):
		action()
		move(direction)
	action()
def snakeAct(action: Callable, c1: Coordinate, c2: Coordinate):
	toPos(c1)
	width, height = Utils.dimensions(c1, c2)
	goNorth = True
	for _ in range(width - 1):
		actMoveAct(action, height, Utils.ternary(goNorth, North, South))
		goNorth = not goNorth
		move(East)
	actMoveAct(action, height, Utils.ternary(goNorth, North, South))
def snakeActCheck(action: Callable, c1: Coordinate, c2: Coordinate, predicate: Callable[[], bool]):
	toPos(c1)
	width, height = Utils.dimensions(c1, c2)
	goNorth = True
	for _ in range(width - 1):
		actMoveAct(action, height, Utils.ternary(goNorth, North, South))
		if not predicate():
			return
		goNorth=not goNorth
		move(East)
	actMoveAct(action, height, Utils.ternary(goNorth, North, South))
def isWithin(pos: Coordinate, c1: Coordinate, c2: Coordinate):
	return c1[0] <= pos[0] < c2[0] and c1[1] <= pos[1] < c2[1]
def toRegion(c1: Coordinate, c2: Coordinate):
	def toAxis(self: int, p1: int, m1: Direction, p2: int, m2: Direction):
		if p1 <= self < p2:
			return
		m1Moves = p1 - (self - get_world_size() * (self >= p1))
		m2Moves = (self + get_world_size() * (self < p2)) - p2 + 1
		if m1Moves < m2Moves:
			for _ in range(m1Moves):
				move(m1)
		else:
			for _ in range(m2Moves):
				move(m2)
	toAxis(get_pos_x(), c1[0], East, c2[0], West)
	toAxis(get_pos_y(), c1[1], North, c2[1], South)
def toCorner(c1: Coordinate, c2: Coordinate, action: Callable):
	toRegion(c1, c2)
	x1 = c1[0]
	if get_pos_x() == x1:
		toPos(c1)
		return
	goNorth = (x1 + get_pos_x()) % 2 == 0
	if goNorth:
		y2e = c2[1] - 1
		while get_pos_y() != y2e:
			move(North)
			action()
	else:
		while get_pos_y() != c1[1]:
			move(South)
			action()
	while get_pos_x() != c2[0] - 1:
		move(East)
		goNorth = not goNorth
		actMoveAct(action, c2[1] - c1[1], Utils.ternary(goNorth, North, South))
	toPos(c1)