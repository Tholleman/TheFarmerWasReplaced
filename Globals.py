UNLOCK_EFFORT={}
GLOBALS={}
AVAILABLE_UNLOCKS=[]
AFTER_UNLOCK={}
REPLACABLE_FUNCTIONS={}

ITEM_TO_UNLOCK={
	Items.Hay: Unlocks.Grass,
	Items.Wood: Unlocks.Plant,
	Items.Carrot: Unlocks.Carrots,
	Items.Power: Unlocks.Sunflowers,
	Items.Pumpkin: Unlocks.Pumpkins,
	Items.Gold: Unlocks.Mazes,
	Items.Cactus: Unlocks.Cactus,
	Items.Bone: Unlocks.Dinosaurs,
	Items.Weird_Substance: Unlocks.Fertilizer
}
UNLOCKS={
	Unlocks.Grass:10,
	Unlocks.Trees:10,
	Unlocks.Speed:5,
	Unlocks.Plant:1,
	Unlocks.Expand:9,
	Unlocks.Pumpkins:10,
	Unlocks.Carrots:10,
	Unlocks.Cactus:6,
	Unlocks.Dinosaurs:6,
	Unlocks.Fertilizer:4,
	Unlocks.Leaderboard:1,
	Unlocks.Mazes:6,
	Unlocks.Polyculture:5,
	Unlocks.Sunflowers:1,
	Unlocks.Watering:9,
	Unlocks.MegaFarm: 5,
	Unlocks.Hats: 1,
	Unlocks.Top_Hat: 1,
	Unlocks.The_Farmers_Remains: 1
}
UNLOCK_PREFERENCE={
	Unlocks.Polyculture: 5,
	Unlocks.Pumpkins: 2,
	Unlocks.Sunflowers: 2,
	Unlocks.Speed: 1.5,
	Unlocks.Megafarm: 2,
	Unlocks.Hats: 0.01
}
HARVEST_ORDER=[
	Items.Bone,
	Items.Cactus,
	Items.Gold,
	Items.Power,
	Items.Pumpkin,
	Items.Carrot,
	Items.Wood,
	Items.Hay,
	Items.Weird_Substance
]
ITEM_TO_SINGLE_PLANT={}
ITEM_EFFORT={
	Items.Weird_Substance:1,
	Items.Hay:1,
	Items.Wood:1,
	Items.Carrot:3,
	Items.Pumpkin:4,
	Items.Power:4,
	Items.Gold:2,
	Items.Cactus:3,
	Items.Bone:4
}
# powerStart=num_items(Items.Power)
# ...
# quick_print((powerStart - num_items(Items.Power)) / tiles)
POWER_USAGE_PER_TILE={
	Items.Hay: 0.3,
	Items.Wood: 0.45,
	Items.Carrot:0.5,
	Items.Pumpkin:0.3,
	Items.Power:0,
	Items.Weird_Substance:0.01,
	Items.Gold:0.02,
	Items.Cactus:1.15,
	Items.Bone:0.95
}
ITEM_TO_FUNCTION={}
ITEM_TO_ENTITY={
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Bush,
	Items.Carrot: Entities.Carrot,
	Items.Power: Entities.Sunflower,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Gold: Entities.Treasure,
	Items.Cactus: Entities.Cactus,
	Items.Bone: Entities.Apple,
}
REVERSE: dict[Direction | None, Direction | None] ={
	North: South,
	South: North,
	East: West,
	West: East,
	None: None
}

def SETUP_FUNCTION_MAPS():
	from Hay import simplePlantHay, harvestHay
	from Wood import simplePlantWood, harvestWood
	from Carrot import simplePlantCarrot, harvestCarrot
	from power import harvestPower
	from pumpkin import harvestPumpkin
	from MazeSolver import harvestGold
	from Cactus import harvestCactus
	from Dinosaur import harvestBones
	from WeirdSubstance import harvestWeirdSubstance
	ITEM_TO_SINGLE_PLANT[Items.Hay]= simplePlantHay
	ITEM_TO_SINGLE_PLANT[Items.Wood] = simplePlantWood
	ITEM_TO_SINGLE_PLANT[Items.Carrot] = simplePlantCarrot
	ITEM_TO_FUNCTION[Items.Hay] = harvestHay
	ITEM_TO_FUNCTION[Items.Wood] = harvestWood
	ITEM_TO_FUNCTION[Items.Carrot] = harvestCarrot
	ITEM_TO_FUNCTION[Items.Power] = harvestPower
	ITEM_TO_FUNCTION[Items.Pumpkin] = harvestPumpkin
	ITEM_TO_FUNCTION[Items.Gold] = harvestGold
	ITEM_TO_FUNCTION[Items.Cactus] = harvestCactus
	ITEM_TO_FUNCTION[Items.Bone] = harvestBones
	ITEM_TO_FUNCTION[Items.Weird_Substance] = harvestWeirdSubstance
