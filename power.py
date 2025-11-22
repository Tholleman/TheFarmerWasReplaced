import Carrot
import Debug
import Defer
import Harvesting
import Globals
import Preperations
import movement


def harvestPower(amount, currentlyUnlocking, indent):
	if num_items(Items.Power) > amount:
		return
	quick_print(indent, amount, "Power")
	petals=[[],[],[],[],[],[],[],[],[]]
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Power, Unlocks.Sunflowers, amount, False, 5-10/get_world_size()**2)
		return tiles + Globals.GLOBALS["AREA"] - (tiles % Globals.GLOBALS["AREA"])
	replaceWith=Preperations.lowestSimplePlant(currentlyUnlocking)
	while num_items(Items.Power) < amount:
		tiles=Preperations.preperations(Items.Power, calculateTilesNeeded, [], currentlyUnlocking, indent)
		quick_print(indent, amount, "Power using", tiles / Globals.GLOBALS["AREA"], "fields")
		for _ in range(0, tiles, Globals.GLOBALS["AREA"]):
			plantField(petals)
			harvestField(petals, replaceWith)
def plantField(petals):
	PIDS=[]
	def planter():
		pid=spawn_drone(plantRow)
		if pid:
			PIDS.append(pid)
		else:
			plantRow(petals)
	movement.actMoveAct(planter, get_world_size(), East)
	for pid in PIDS:
		mergePetals(petals, wait_for(pid))
def plantRow(planted=[[],[],[],[],[],[],[],[],[]]):
	def plantSunflower():
		if get_ground_type() != Grounds.Soil:
			till()
		Harvesting.clearHarvest([Entities.Sunflower])
		if plant(Entities.Sunflower):
			planted[15-measure()].append(movement.getPos())
		else:
			Carrot.simplePlantCarrot()
	movement.actMoveAct(plantSunflower, get_world_size(), North)
	return planted
def mergePetals(petals, planted):
	for power in range(len(petals)):
		for pos in planted[power]:
			petals[power].append(pos)
def harvestField(petals, replaceWith):
	previousDrones=[]
	for positions in petals:
		currentDrones=[]
		while len(positions) > 0:
			pos=positions.pop()
			def harvester():
				movement.toPos(pos)
				Defer.join(previousDrones)
				Harvesting.forceHarvestNoFertilizer()
				Globals.ITEM_TO_SINGLE_PLANT[replaceWith]()
			pid=spawn_drone(harvester)
			if pid:
				currentDrones.append(pid)
			else:
				harvester()
		previousDrones=currentDrones
	Defer.join(previousDrones)
if __name__ == "__main__":
	Debug.startBenchmark(Items.Power, goal, 1)
