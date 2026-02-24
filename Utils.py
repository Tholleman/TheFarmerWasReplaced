def ternary[T](predicate: bool, whenTrue: T, whenFalse: T):
	if predicate:
		return whenTrue
	return whenFalse
def dimensions(c1: Coordinate, c2: Coordinate) -> Tuple[int, int]:
	width=c2[0] - c1[0]
	height=c2[1] - c1[1]
	return width, height
def divideCeil(a: int, b: int):
	return -a // b * -1
def roundTo(num: int, multipleOf: int):
	return -num // multipleOf * -multipleOf
def randBetween(min: int, maxExclusive: int) -> int:
	return ((maxExclusive - min) * random() + min) // 1 # pyright: ignore[reportReturnType]
def safeRemove(arr: list | set, toRemove):
	if toRemove in arr:
		arr.remove(toRemove)