import Utils


def getPos():
	return (get_pos_x(), get_pos_y())
def toPos(coordinatesTuple):
	toCoordinates(coordinatesTuple[0], coordinatesTuple[1])
def toCoordinates(x,y):
	goWest=(get_pos_x() - x + get_world_size()) % get_world_size() < get_world_size() / 2
	direction=Utils.ternary(goWest, West, East)
	while get_pos_x() != x:
		move(direction)
	goSouth=(get_pos_y() - y + get_world_size()) % get_world_size() < get_world_size() / 2
	direction=Utils.ternary(goSouth, South, North)
	while get_pos_y() != y:
		move(direction)
def actMoveAct(action, count, direction):
	for _ in range(count - 1):
		action()
		move(direction)
	action()
def toRegion(c1, c2):
	def toAxis(self, p1, m1, p2, m2):
		if self >= p1 and self < p2:
			return
		m1Moves=p1 - (self - get_world_size() * (self >= p1))
		m2Moves=(self + get_world_size() * (self < p2)) - p2 + 1
		if m1Moves < m2Moves:
			for _ in range(m1Moves):
				move(m1)
		else:
			for _ in range(m2Moves):
				move(m2)
	toAxis(get_pos_x(), c1[0], East, c2[0], West)
	toAxis(get_pos_y(), c1[1], North, c2[1], South)
def toCorner(c1, c2, action):
	toRegion(c1, c2)
	x1=c1[0]
	if get_pos_x() == x1:
		toPos(c1)
		return
	y2e=c2[1] - 1
	goNorth=(x1 + get_pos_x()) % 2 == 0
	direction=Utils.ternary(goNorth, North, South)
	while get_pos_y() not in [c1[1], y2e]:
		move(direction)
		action()
	while get_pos_x() != c2[0] - 1:
		move(East)
		goNorth=not goNorth
		actMoveAct(action, c2[1] - c1[1], Utils.ternary(goNorth, North, South))
	toPos(c1)