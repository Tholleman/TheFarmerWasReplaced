def ternary(predicate, whenTrue, whenFalse):
	if predicate:
		return whenTrue
	return whenFalse
def dimensions(c1, c2):
	width=c2[0] - c1[0]
	height=c2[1] - c1[1]
	return width, height
def divideCeil(a, b):
	return -a // b * -1
def roundTo(num, multipleOf):
	return -num // multipleOf * -multipleOf
def randBetween(min, maxExclusive):
	return ((maxExclusive - min) * random() + min) // 1