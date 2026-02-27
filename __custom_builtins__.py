from collections.abc import Callable
from typing import TypedDict, Literal

type MazeField = list[list[MazeCell]]
class MazeCell(TypedDict):
	knownGood: set[Direction]
	knownWalls: set[Direction]
	origin: Direction | None
	distance: int | None
class MazeContext(TypedDict):
	connectedRegion: bool
	drawnOn: set[Coordinate]
	lastCheck: float
type Coordinate = Tuple[int, int]
class MazeTracker(TypedDict):
	pos: int
	remaining: int
	i: int
type Reducer[T] = Tuple[T, Callable[[T, T], T]]
