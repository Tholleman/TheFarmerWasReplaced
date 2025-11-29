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
	regions=assignRegions()
	smallestRegionArea=getSmallestRegionArea(regions)
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Power, Unlocks.Sunflowers, amount, False, (5-10/get_world_size()**2)*0.9)
		if tiles < totalArea and get_ground_type() != Grounds.Soil:
			return totalArea
		return max(Utils.roundTo(tiles, smallestRegionArea), smallestRegionArea*4*(num_drones() > 4))
	replaceWith=Preperations.lowestSimplePlant(currentlyUnlocking)
	while num_items(Items.Power) < amount:
		tiles=Preperations.preperations(Items.Power, calculateTilesNeeded, currentlyUnlocking, indent)
		quick_print(indent, amount, "Power using", tiles / totalArea, "fields")
		for completed in range(0, tiles, totalArea):
			subregion=regions
			if tiles - completed < totalArea:
				regionsNeeded=Utils.divideCeil(tiles - completed, smallestRegionArea)
				subregion=regions[:regionsNeeded]
			map=plantField(subregion)
			harvestField(subregion, map, replaceWith)
def assignRegions():
	queue=[[(0, 0), (get_world_size(), get_world_size())]]
	while len(queue) < max_drones():
		current=queue.pop(0)
		sizes=(current[1][0] - current[0][0], current[1][1] - current[0][1])
		changeI=Utils.ternary(sizes[0] > sizes[1], 0, 1)
		if sizes[changeI] == 1:
			queue.append(current)
			break
		half=current[0][changeI] + sizes[changeI] // 2
		unchanged=(changeI + 1) % 2
		def makeCorner(other):
			if changeI == 0:
				return (half, other)
			return (other, half)
		newRegion=[current[0], makeCorner(current[1][unchanged])]
		current[0]=makeCorner(current[0][unchanged])
		queue.append(newRegion)
		queue.append(current)
	return queue
def getSmallestRegionArea(regions):
	smallestRegion=regions[-1]
	width, height=Utils.dimensions(smallestRegion[0], smallestRegion[1])
	return width * height
def plantField(regions):
	map={}
	PIDS=[]
	for region in regions:
		def inRegion():
			return region[0], fillRegion(region)
		pid=spawn_drone(inRegion)
		if pid:
			PIDS.append(pid)
		else:
			map[region[0]]=fillRegion(region)
	for pid in PIDS:
		c1, result=wait_for(pid)
		map[c1]=result
	return map
def fillRegion(region):
	planted=[[],[],[],[],[],[],[],[],[]]
	def plantSunflower():
		if get_ground_type() != Grounds.Soil:
			till()
		Harvesting.spamFertilizer()
		if plant(Entities.Sunflower):
			planted[15-measure()].append(movement.getPos())
			if measure() == 15:
				ground.waterSoil()
		else:
			Carrot.simplePlantCarrot()
	movement.snakeAct(plantSunflower, region[0], region[1])
	return planted
def harvestField(regions, map, replaceWith):
	previousDrones=[]
	for petal in range(9):
		currentDrones=[]
		for region in regions:
			def harvestRegion():
				for pos in map[region[0]][petal]:
					movement.toPos(pos)
					while len(previousDrones):
						wait_for(previousDrones.pop())
					Harvesting.forceHarvestNoFertilizer()
					Globals.ITEM_TO_SINGLE_PLANT[replaceWith]()
			if len(map[region[0]][petal]):
				if region != regions[-1] and len(previousDrones):
					waitForDroneAvailable()
				pid=spawn_drone(harvestRegion)
				if pid:
					currentDrones.append(pid)
				else:
					harvestRegion()
		previousDrones=currentDrones
	Defer.join(previousDrones)
def waitForDroneAvailable():
	while num_drones() == max_drones():
		pass
if __name__ == "__main__":
	Debug.startBenchmark(Items.Power, goal, .5)
