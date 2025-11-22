import Globals
import power


def preperations(item, calculateTilesNeeded, requirements, currentlyUnlocking, indent, seedsMargin=1):
	tiles=calculateTilesNeeded()
	oldTiles=-1
	cost=get_cost(Globals.ITEM_TO_ENTITY[item])
	indent+="  "
	while tiles != oldTiles:
		oldTiles=tiles
		if Items.Power in requirements:
			if workForPower(tiles, currentlyUnlocking, indent):
				tiles=calculateTilesNeeded()
		if len(cost) != 0:
			if workForSeeds(cost, tiles, currentlyUnlocking, indent, seedsMargin):
				tiles=calculateTilesNeeded()
	return tiles
def expectedTilesNeeded(item, unlock, amount, polyculture, baseYieldPerTile=1):
	tiles=amount - num_items(item)
	expectedYieldWithBonus=max(1, 2**(num_unlocked(unlock)-1) * baseYieldPerTile)
	if polyculture:
		expectedYieldWithBonus*=(5*2**polyculture)*0.5
	return tiles / expectedYieldWithBonus
def workForSeeds(cost, tiles, orders, indent, margin=1):
	amountOfSeeds=max(1, tiles*margin)
	if amountOfSeeds <= 0:
		return False
	totalCost={}
	for item in cost:
		totalCost[item]=cost[item] * amountOfSeeds
		if item in orders["items"]:
			totalCost[item]+=orders["items"].pop(item)
	didWork=False
	allInStock=False
	while not allInStock:
		allInStock = True
		for item in totalCost:
			if num_items(item) < totalCost[item]:
				Globals.ITEM_TO_FUNCTION[item](totalCost[item], orders, indent)
				didWork=True
				allInStock=False
	return didWork
def workForPower(tiles, currentlyUnlocking, indent):
	if num_unlocked(Unlocks.Sunflowers) == 0:
		return False
	if tiles <= Globals.GLOBALS["AREA"]:
		return False
	powerNeeded=tiles*0.05
	if num_items(Items.Power) >= powerNeeded//1:
		return False
	power.harvestPower(powerNeeded, currentlyUnlocking, indent)
	return True
def lowestSimplePlant(orders, of = [Items.Hay, Items.Wood, Items.Carrot]):
	if len(of) == 1:
		return of[0]
	if orders != None:
		greatestNeed={"item": None, "amount": 0}
		for item in orders["items"]:
			if item in Globals.ITEM_TO_SINGLE_PLANT:
				needed=orders["items"][item] - num_items(item)
				if needed > greatestNeed["amount"]:
					greatestNeed={"item": item, "amount": needed}
		if greatestNeed["item"] != None:
			return item
	lowest={"item":of[0], "amount":num_items(of[0])}
	for item in of[1::]:
		amount=num_items(item)
		if amount < lowest["amount"]:
			lowest={"item":item, "amount":amount}
	return lowest["item"]
