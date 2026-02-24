import Defer
import Globals
import Harvesting
import UnlockHelper
import Preperations
import Utils

def harvestBones(amount, currentlyUnlocking, indent):
	if num_items(Items.Bone) > amount:
		return
	quick_print(indent, amount, "Bones")
	UnlockHelper.workToUnlock(Unlocks.Dinosaurs, currentlyUnlocking, "  " + indent)
	def calculateTilesNeeded():
		tiles=Preperations.expectedTilesNeeded(Items.Bone, Unlocks.Dinosaurs, amount, False, Globals.GLOBALS["AREA"]-1)
		return Utils.roundTo(tiles, Globals.GLOBALS["AREA"])
	while num_items(Items.Bone) < amount:
		tiles=Preperations.preperations(Items.Bone, calculateTilesNeeded, currentlyUnlocking, indent)
		quick_print(indent, amount, "Bones using", tiles / Globals.GLOBALS["AREA"], "fields")
		Defer.everyTile(Harvesting.forceHarvest)
		for _ in range(0, tiles, Globals.GLOBALS["AREA"]):
			change_hat(Hats.Dinosaur_Hat)
			b2s()
			if num_unlocked(Unlocks.Top_Hat):
				change_hat(Hats.Top_Hat)
			else:
				change_hat(Hats.Straw_Hat)
			if num_items(Items.Cactus) < get_cost(Entities.Apple)[Items.Cactus]:
				break
def b2s():
	chargeFromY=0
	for size in range((get_world_size() ** 2) / 2):
		appleX, appleY=measure()
		
		# Move to column 0 if the apple is in a lower y
		if appleY < get_pos_y() and get_pos_x() != 0:
			if get_pos_y() % 2 == 0:
				move(North)
			while move(West):
				pass
			if get_pos_x() != 0:
				while True:
					move(North)
					if move(West):
						break
		# Move towards 0,0 if in the 0 column
		if get_pos_x() == 0:
			# Move to the apple if both it and snake are in column 0
			if appleX == 0 and appleY < get_pos_y():
				for _ in range(get_pos_y() - appleY):
					move(South)
				continue
			while move(South):
				pass
			chargeFromY=size/get_world_size()
		
		# The apple is now always in the same row or higher
		
		while appleY > get_pos_y():
			if get_pos_y() >= chargeFromY + (get_world_size() - get_pos_x()) / get_world_size():
				if get_pos_x() == 0:
					move(East)
				for _ in range(appleY - get_pos_y() - 1):
					move(North)
			if get_pos_y() % 2 == 0:
				while move(East):
					pass
			else:
				for _ in range(get_pos_x() - 1):
					move(West)
			move(North)
		
		# The apple is now in the same row
		
		if appleX == get_pos_x():
			continue
		direction=East
		if get_pos_y() % 2 != 0:
			direction=West
		requiredDirection=East
		if appleX < get_pos_x():
			requiredDirection=West
		if direction != requiredDirection:
			_=move(North) or move(South)
			for _ in range(abs(appleX - get_pos_x())):
				move(requiredDirection)
			if appleY > get_pos_y():
				move(North)
			else:
				move(South)
		else:
			for _ in range(abs(appleX - get_pos_x())):
				move(direction)
	if get_pos_x() != 0:
		while get_pos_y() < get_world_size() - 1:
			if get_pos_y() % 2 == 0:
				while move(East):
					pass
			else:
				for _ in range(get_pos_x() - 1):
					move(West)
			move(North)
	move(North)
	while True:
		while move(West):
			pass
		while move(South):
			pass
		while True:
			while move(East):
				pass
			if not move(North):
				return
			if get_pos_y() == get_world_size() - 1:
				break
			for _ in range(get_pos_x() - 1):
				move(West)
			if not move(North):
				return
if __name__ == "__main__":
	Globals.SETUP_FUNCTION_MAPS()
	harvestBones(goal, {"currentlyUnlocking":[Unlocks.Dinosaurs],"items":{}}, "")
	quick_print(num_items(Items.Bone))