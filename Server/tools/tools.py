def member(list, newPath):
	for path in list:
		if newPath == path:
			return True
	return False
