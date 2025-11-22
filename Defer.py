import movement

def defer(action):
	pid=spawn_drone(action)
	if pid:
		return pid
	pos=movement.getPos()
	action()
	movement.toPos(pos)
	return None
def spawnMoveAct(action, dronesNeeded, direction, rows=1):
	for _ in range(dronesNeeded - 1):
		spawn_drone(action)
		for _ in range(rows):
			move(direction)
	action()
	joinAll()
def joinAll():
	while num_drones() > 1:
		pass
def join(pids):
	for pid in pids:
		wait_for(pid)
def everyTile(action):
	def fullColumn():
		movement.actMoveAct(action, get_world_size(), North)
	if num_unlocked(Unlocks.Expand) < 2:
		fullColumn()
		return
	if max_drones() == 1:
		movement.actMoveAct(fullColumn, get_world_size(), East)
		return
	halfColumnDroneCount=min(max((max_drones() - get_world_size()) // 2, 0), get_world_size())
	fullColumnDroneCount=get_world_size() - halfColumnDroneCount
	def splitColumn():
		def act(direction=North, minus=0):
			movement.actMoveAct(action, (get_world_size() - minus) / 2, direction)
		if spawn_drone(act):
			move(South)
			act(South, 1)
		else:
			fullColumn()
	def halfField(direction=West, minus=0):
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
def dronesNeeded(tiles):
	dronesNeeded=max(min(tiles/get_world_size(), get_world_size(), max_drones()), 1)
	tilesPerDrone=tiles/dronesNeeded
	return dronesNeeded, tilesPerDrone
if __name__ == "__main__":
	everyTile(till)