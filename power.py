import Carrot
import Debug
import Defer
import Harvesting
import Globals
import Preperations
import Utils
import ground
import movement


def harvestPower(amount, currentlyUnlocking, indent):
	if num_items(Items.Power) >= amount:
		return
	quick_print(indent, amount, "Power")
	totalArea=get_world_size() ** 2
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Power, Unlocks.Sunflowers, amount, False, (5-10/get_world_size()**2))
		return Utils.roundTo(tiles, totalArea)
	Preperations.preperations(Items.Power, calculateTilesNeeded, currentlyUnlocking, indent)
	quick_print(indent, amount, "Power")
	while num_items(Items.Power) < amount:
		harvestField(currentlyUnlocking, amount)
def harvestField(currentlyUnlocking, amount: int):
	arr = plantField()
	move(North)
	replaceWith = Preperations.lowestSimplePlant(currentlyUnlocking)
	previous: list[Drone] = []
	for powerCoords in arr[:-1]:
		previous = harvestPetalPower(powerCoords, replaceWith, previous)
	if num_items(Items.Power) < amount:
		previous = harvestPetalPower(arr[-1], replaceWith, previous)
	Defer.join(previous)
def plantField() -> list[set[Coordinate]]:
	def plantColumn():
		planted = newPowerStructure()
		def plantTile():
			if get_ground_type() != Grounds.Soil:
				till()
			Harvesting.spamFertilizer()
			if plant(Entities.Sunflower):
				if num_items(Items.Power) == 0 and measure() == 15:
					Harvesting.spamFertilizer()
					if not plant(Entities.Sunflower):
						Carrot.simplePlantCarrot()
						return
				planted[15 - measure()].add(movement.getPos()) # type: ignore
				if measure() == 15:
					ground.waterSoil()
			else:
				Carrot.simplePlantCarrot()
		movement.actMoveAct(plantTile, get_world_size(), North)
		return planted
	pids: list[Drone] = []
	arr = newPowerStructure()
	def mergeResult(result: list[set[Coordinate]]):
		for i in range(len(result)):
			for coordinate in result[i]:
				arr[i].add(coordinate)
	def spawnPlanter():
		pid = spawn_drone(plantColumn)
		if pid:
			pids.append(pid)
		else:
			mergeResult(plantColumn())
	def halfField(direction = East, minus = 0):
		for _ in range(get_world_size() // 2 - minus - 1):
			spawnPlanter()
			move(direction)
		mergeResult(plantColumn())
		for pid in pids:
			mergeResult(wait_for(pid))
		return arr
	eastHalf = spawn_drone(halfField)
	if eastHalf:
		move(West)
		halfField(West, get_world_size() % 2)
		mergeResult(wait_for(eastHalf))
	else:
		halfField()
		move(East)
		halfField(East, get_world_size() % 2)
	return arr
def newPowerStructure() -> list[set[Coordinate]]:
	return [set(), set(), set(), set(), set(), set(), set(), set(), set()]
def harvestPetalPower(coordinates: set[Coordinate], replaceWith: Item, wait: list[Drone]):
	byColumn: dict[int, set[int]] = {}
	for coordinate in coordinates:
		if coordinate[0] in byColumn:
			byColumn[coordinate[0]].add(coordinate[1])
		else:
			byColumn[coordinate[0]] = {coordinate[1]}
	half = get_world_size() // 2
	def eastHalf():
		return eastWestHarvest(East, half, byColumn, replaceWith, wait)
	pids: list[Drone] = []
	northDrone = []
	if spawnWaiter(eastHalf, northDrone, wait):
		move(West)
		pids = eastWestHarvest(West, half, byColumn, replaceWith, wait)
		for pid in wait_for(northDrone[0]):
			pids.append(pid)
	else:
		direction = East
		for i in range(1, get_world_size()):
			if Utils.wrapped(get_pos_x() + i, get_world_size()) in byColumn:
				break
			if Utils.wrapped(get_pos_x() - i, get_world_size()) in byColumn:
				direction = West
				break
		eastWestHarvest(direction, get_world_size(), byColumn, replaceWith, wait)
	return pids
def eastWestHarvest(direction: Direction, amount: int, byColumn: dict[int, set[int]], replaceWith: Item, wait: list[Drone]):
	dir = Utils.ternary(direction == East, 1, -1)
	while amount > 0 and Utils.wrapped(get_pos_x() + dir * (amount - 1), get_world_size()) not in byColumn:
		amount -= 1
	pids: list[Drone] = []
	def act():
		if get_pos_x() in byColumn:
			sameY = byColumn[get_pos_x()]
			def toDefer():
				columnHarvest(sameY, replaceWith, wait)
			_ = spawnWaiter(toDefer, pids, wait) or toDefer()
	movement.actMoveAct(act, amount, direction)
	return pids
def columnHarvest(yCoordinates: set[int], replaceWith: Item, wait : list[Drone]):
	# Debug.assertion(len(yCoordinates) != 0)
	havested = 0
	direction = North
	for i in range(1, get_world_size()):
		if Utils.wrapped(get_pos_y() + i, get_world_size()) in yCoordinates:
			break
		if Utils.wrapped(get_pos_y() - i, get_world_size()) in yCoordinates:
			direction = South
			break
	while get_pos_y() not in yCoordinates:
		move(direction)
	Defer.join(wait)
	for _ in range(get_world_size()):
		if get_pos_y() in yCoordinates:
			Harvesting.forceHarvest()
			Globals.ITEM_TO_SINGLE_PLANT[replaceWith]()
			havested += 1
			if havested == len(yCoordinates):
				return
		move(direction)
def spawnWaiter(action, pids: list[Drone], wait: list[Drone]):
	while len(wait):
		pid = spawn_drone(action)
		if pid:
			pids.append(pid)
			return True
		for older in wait:
			if has_finished(older):
				wait.remove(older)
				break
	pid = spawn_drone(action)
	if pid:
		pids.append(pid)
		return True
	return False
if __name__ == "__main__":
	Debug.startBenchmark(Items.Power, goal, 1) # type: ignore
