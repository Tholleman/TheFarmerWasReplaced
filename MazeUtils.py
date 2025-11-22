def moveTreasure():
	return use_item(Items.Weird_Substance, get_world_size() * 2**(num_unlocked(Unlocks.Mazes)-1))
def popSet(set):
	for first in set:
		set.remove(first)
		return first
def getTile(tiles,x,y,direction):
	x,y=nextCoordinates(x,y,direction)
	return tiles[x][y]
def nextCoordinates(x,y,direction):
	if direction == North:
		return x,y+1
	if direction == South:
		return x,y-1
	if direction == East:
		return x+1,y
	if direction == West:
		return x-1,y
	return x,y