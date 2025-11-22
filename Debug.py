import Globals

def startBenchmark(item, goal, delta=0):
	Globals.SETUP_FUNCTION_MAPS()
	Globals.ITEM_TO_FUNCTION[item](goal, {"currentlyUnlocking":[Globals.ITEM_TO_UNLOCK[item]], "items":{}}, "")
	if num_items(item) / goal > 1+delta:
		quick_print("ERROR: Accuracy failure", num_items(item), item, "which is more than", goal, "with a delta of", str(delta*100+100) + "%")
		while True:
			do_a_flip()
	else:
		quick_print("Accuracy:", 100 * num_items(item) / goal)
def formatSeconds(seconds):
	time=""
	if seconds >= 3600:
		time+=str(seconds//3600)+":"
		seconds%=3600
	if seconds >= 60:
		if seconds >= 600:
			time+=str(seconds//60)+":"
		else:
			if time != "":
				time+="0"
			time+=str(seconds//60)+":"
		seconds%=60
	elif time != "":
		time+="00:"
	if seconds >= 10:
		time+=str(seconds)
	else:
		if time != "":
			time+="0"
		time+=str(seconds)
	return time