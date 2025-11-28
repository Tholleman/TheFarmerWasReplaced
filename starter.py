import Debug
import Globals

speed=100

def benchmark(expected, file, items, args, expansion, unlocks={}, locks=[], amount=10, seedStart=0):
	unlockOverride={}
	for unlock in Unlocks:
		lvl=1
		if unlock in unlocks:
			lvl=unlocks[unlock]
		elif unlock in Globals.UNLOCKS:
			lvl=Globals.UNLOCKS[unlock]
		else:
			if num_unlocked(unlock) != lvl:
				quick_print("hampering", unlock)
		unlockOverride[unlock]=lvl
	for unlock in locks:
		unlockOverride.pop(unlock)
	if expansion == 0:
		if Unlocks.Expand in unlockOverride:
			unlockOverride.pop(Unlocks.Expand)
	else:
		unlockOverride[Unlocks.Expand]=expansion
	quick_print("estimated duration:", Debug.formatSeconds(expected*amount))
	quick_print("With full speedup:", Debug.formatSeconds(expected*amount/speed))
	avg=0
	for seed in range(amount):
		seed+=seedStart
		quick_print("seed", seed)
		avg+=simulate(file, unlockOverride, items, args, seed, speed)
	actual=avg / amount * 10 // 1 / 10
	if actual != expected:
		quick_print("CHANGE:", expected, "to", actual)
		for _ in range(10):
			do_a_flip()

# benchmark("19.1", "Defer", {}, {}, 6, {}, [Unlocks.Megafarm], 1)
# benchmark("9.75", "Defer", {}, {}, 6, {Unlocks.Megafarm: 1}, [], 1)
# benchmark("0.64", "Defer", {}, {}, 2, {}, [], 1)
# benchmark("4.13", "Defer", {}, {}, 8, {}, [], 1)
# benchmark("6.45", "Defer", {}, {}, 9, {}, [], 1)

# quick_print("early")
# benchmark("13.75", "Hay", {Items.Power:99999}, {"goal":100, "prepareTill": False, "delta": 0}, 3, {Unlocks.Grass: 1}, [Unlocks.Polyculture, Unlocks.Megafarm], 1)
# benchmark("3.83", "Hay", {Items.Power:99999}, {"goal":100, "prepareTill": False, "delta": 0}, 3, {Unlocks.Grass: 3}, [Unlocks.Polyculture, Unlocks.Megafarm], 1)
# quick_print("Polyculture")
# benchmark("18.76", "Hay", {Items.Power:99999}, {"goal":1000000, "prepareTill": True, "delta": 0.2}, 6, {}, [Unlocks.Megafarm], 10)
# quick_print("Mega")
# benchmark("43.38", "Hay", {Items.Power:99999}, {"goal":100000000, "prepareTill": True, "delta": 0.2}, 9, {}, [], 10)

# quick_print("early")
# benchmark(11.6, "Wood", {Items.Power:99999}, {"goal":64, "prepareTill": False, "delta": 0}, 3, {}, [Unlocks.Trees, Unlocks.Polyculture, Unlocks.Megafarm], 1)
# benchmark(6.8, "Wood", {Items.Power:99999}, {"goal":116, "prepareTill": False, "delta": 0}, 3, {Unlocks.Trees: 1}, [Unlocks.Polyculture, Unlocks.Megafarm], 1)
# benchmark(69.1, "Wood", {Items.Power:99999}, {"goal":2000, "prepareTill": False, "delta": 0.2}, 6, {Unlocks.Trees: 1}, [Unlocks.Polyculture, Unlocks.Megafarm], 1)
# quick_print("Polyculture")
# benchmark(37.8, "Wood", {Items.Power:99999}, {"goal":10000000, "prepareTill": True, "delta": 5}, 6, {}, [Unlocks.Megafarm], 10)
# quick_print("Mega")
# benchmark(23.9, "Wood", {Items.Power:99999}, {"goal":100000000, "prepareTill": True, "delta": .6}, 9, {}, [], 10)

# benchmark("40.83", "Carrot", {Items.Power:999999}, {"goal":100, "prepareTill": False, "delta": 0}, 4, {Unlocks.Carrots: 1, Unlocks.Grass: 1, Unlocks.Trees: 1}, [Unlocks.Polyculture, Unlocks.Megafarm], 10)

# benchmark(48.63, "power", {Items.Carrot:2048}, {"goal":10000}, 9, {}, [], 5)

# benchmark("33.19", "pumpkin", {Items.Power:999999999,Items.Carrot:999999999}, {"goal":1080}, 4, {Unlocks.Pumpkins: 1}, [Unlocks.Megafarm], 10)
# quick_print("Recover")
# benchmark("73.55", "pumpkin", {Items.Power:999999999,Items.Carrot:308}, {"goal":1024}, 3, {Unlocks.Pumpkins: 1}, [Unlocks.Megafarm], 1)
# quick_print("Mega")
# benchmark(13.7, "pumpkin", {Items.Power:999999999,Items.Carrot:999999999}, {"goal":3145728}, 9)

# benchmark("75,69", "Cactus", {Items.Power:999999,Items.Pumpkin:9999999}, {"goal":1000}, 6, {Unlocks.Cactus: 1}, [Unlocks.Megafarm], 5)
# benchmark("50,64", "Cactus", {Items.Power:999999,Items.Pumpkin:9999999}, {"goal":1000}, 9, {}, [], 5)

# benchmark("31.81", "WeirdSubstance", {Items.Power:999999999, Items.Water: 999999999}, {"goal":100000000}, 9, {}, [], 1)

# benchmark("2.75", "mazeExplorer", {Items.Power:999999999, Items.Weird_Substance: 999999999}, {}, 4, {}, [Unlocks.Megafarm], 10)
# benchmark("1.74", "mazeExplorer", {Items.Power:999999999, Items.Weird_Substance: 999999999}, {}, 4, {Unlocks.Megafarm: 1}, [], 10)
# benchmark("19.47", "mazeExplorer", {Items.Power:999999999, Items.Weird_Substance: 999999999}, {}, 9, {}, [], 10)
# benchmark(95.2, "MazeSolver", {Items.Power:999999999, Items.Weird_Substance: 999999999}, {"goal":346752}, 4, {}, [Unlocks.Megafarm], 10)
# benchmark(293, "MazeSolver", {Items.Power:999999999, Items.Weird_Substance: 999999999}, {"goal":9863168}, 9, {}, [], 5)

# benchmark("138.21", "Dinosaur", {Items.Cactus: 999999999}, {"goal": 1000}, 6)
# benchmark("1865.85", "Dinosaur", {Items.Cactus: 999999999}, {"goal": 1000}, 9)

benchmark(5405.9, "Main", {}, {}, 0, {}, Unlocks, 5)
