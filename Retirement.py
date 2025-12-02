import Globals
import UnlockHelper
import UnlocksPath
import MazeSolver

Globals.SETUP_FUNCTION_MAPS()
MazeSolver.gracefulRecover()
clear()
if num_unlocked(Unlocks.Top_Hat):
	change_hat(Hats.Top_Hat)

def farmItemsExact(item, amount):
	emptyUnlock={"currentlyUnlocking":[Globals.ITEM_TO_UNLOCK[item]], "items":{}}
	Globals.ITEM_TO_FUNCTION[item](amount + num_items(item), emptyUnlock, "")

while len(Globals.AVAILABLE_UNLOCKS) > 0:
	UnlockHelper.workToUnlock(UnlocksPath.getNextUnlock())

plants=[]
for item in Globals.ITEM_TO_FUNCTION:
	plants.append(item)
while True:
	lowest={"item": plants[0], "amount": num_items(plants[0])}
	goal=num_items(plants[0])
	for item in plants[1::]:
		amount=num_items(item)
		if amount < lowest["amount"]:
			lowest={"item":item, "amount":amount}
		elif amount > goal:
			goal=amount
	amount=min(goal, lowest["amount"]*2)
	emptyUnlock={"currentlyUnlocking":[Globals.ITEM_TO_UNLOCK[item]], "items":{}}
	Globals.ITEM_TO_FUNCTION[lowest["item"]](amount, emptyUnlock, "")
