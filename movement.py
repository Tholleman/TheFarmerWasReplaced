def getPos():
	return (get_pos_x(), get_pos_y())
def toPos(coordinatesTuple):
	toCoordinates(coordinatesTuple[0], coordinatesTuple[1])
def toCoordinates(x,y):
	direction=East
	distanceWest=(get_pos_x()-x+get_world_size()) % get_world_size()
	if distanceWest < get_world_size() / 2:
		direction=West
	while get_pos_x() != x:
		move(direction)
	
	direction=North
	distanceSouth=(get_pos_y()-y+get_world_size()) % get_world_size()
	if distanceSouth < get_world_size() / 2:
		direction=South
	while get_pos_y() != y:
		move(direction)
def actMoveAct(action, count, direction):
	for _ in range(count - 1):
		action()
		move(direction)
	action()
