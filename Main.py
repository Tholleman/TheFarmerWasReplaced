import Globals
import UnlockHelper
import UnlocksPath

Globals.SETUP_FUNCTION_MAPS()
path=UnlocksPath.calculatePath()
clear()

while num_unlocked(Unlocks.Leaderboard) == 0:
	UnlockHelper.unlockAll(path.pop(0))
