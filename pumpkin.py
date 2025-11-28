import Debug
import Defer
import Globals
import Harvesting
import Preperations
import UnlockHelper
import Utils
import ground
import movement


def harvestPumpkin(amount, currentlyUnlocking, indent):
	if num_items(Items.Pumpkin) > amount:
		return
	quick_print(indent, amount, "Pumpkin")
	UnlockHelper.workToUnlock(Unlocks.Pumpkins, currentlyUnlocking, "  " + indent)
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Pumpkin, Unlocks.Pumpkins, amount, False, min(get_world_size(), 6))
		return (-tiles // Globals.GLOBALS["AREA"]) * -Globals.GLOBALS["AREA"]
	while num_items(Items.Pumpkin) < amount:
		tiles=Preperations.preperations(Items.Pumpkin, calculateTilesNeeded, [Items.Power], currentlyUnlocking, indent, 1.2)
		quick_print(indent, amount, "Pumpkin using", tiles / Globals.GLOBALS["AREA"], "fields")
		for _ in range(0, tiles, Globals.GLOBALS["AREA"]):
			plantFieldFullOfPumpkins()
			harvest()
def plantFieldFullOfPumpkins():
	if not ground.prepareGround(Grounds.Soil, plantPumpkin):
		Defer.everyTile(plantPumpkin)
	def manageRegion(c1, c2):
		c1=Defer.splitRegion(c1, c2, manageRegion)
		width=c2[0] - c1[0]
		height=c2[1] - c1[1]
		notFullyGrown=[]
		def storeGrowingPumpkins():
			if get_entity_type() == Entities.Pumpkin and can_harvest():
				return
			notFullyGrown.append(movement.getPos())
			ground.waterSoil()
			plantPumpkin()
		movement.toPos(c1)
		north=True
		for _ in range(width - 1):
			movement.actMoveAct(storeGrowingPumpkins, height, Utils.ternary(north, North, South))
			north=not north
			move(East)
		movement.actMoveAct(storeGrowingPumpkins, height, Utils.ternary(north, North, South))
		while len(notFullyGrown) > 0:
			movement.toPos(notFullyGrown.pop(0))
			storeGrowingPumpkins()
	manageRegion((0,0), (get_world_size(), get_world_size()))
	Defer.joinAll()
def plantPumpkin():
	if get_entity_type() == Entities.Pumpkin:
		return
	ground.waterSoil()
	if not plant(Entities.Pumpkin):
		if get_entity_type() != Entities.Dead_Pumpkin:
			Harvesting.spamFertilizer()
		plantRequirement()
def plantRequirement():
	cost=get_cost(Entities.Pumpkin)
	for item in cost:
		if num_items(item) < cost[item]:
			Globals.ITEM_TO_SINGLE_PLANT[item]()

if __name__ == "__main__":
	Debug.startBenchmark(Items.Pumpkin, goal)
