''' SORTING THEMES '''

# Sort in ascending order
def asc(val):
	n = len(val)
	for x in range(n):
		for y in range(0,n - x - 1):
			if val[y] > val[y + 1]:
				val[y], val[y + 1] = val[y + 1],val[y]
	return val
# Sort value in dictionary
def dictkey(item):
  sorts = sorted(item.items())
  for x, y in sorts:
    print(f"{x} {y}")

# Sort value in dictionary
def dictval(item):
  formats = sorted(item.items(), key=lambda x: x[1])
  for x, y in formats:
    print(f"{x} {y}")

# Sort reverse dictionary
def desckey(item):
  formats = sorted(item.items(), reverse=True)
  for x, y in formats:
    print(f"{x} {y}")
def descval(item):
  formats = sorted(item.items(), key=lambda x: x[1], reverse=True)
  for x, y in formats:
    print(f"{x} {y}")
    
# Sort in descending order			
def desc(val):
	n = len(val)
	for x in range(n):
		for y in range(0,n - x - 1):
			if val[y] < val[y + 1]:
				val[y], val[y + 1] = val[y + 1],val[y]
	return val
	
# All caps in sorted items			
def caps(val):
	value = [str(x).capitalize() for x in val]
	return value
def keycaps(item):
  sorts = sorted(item.items())
  for x, y in sorts:
    print(f"{x.capitalize()} {y}")
def valcaps(item):
  sorts = sorted(item.items(), key=lambda x: x[1])
  for x, y in sorts:
    print(f"{x} {y.capitalize()}")
    
# All lowercase items
def lows(val):
	val = [str(x).lower() for x in val]
	return val
	
# All uppercase items
def ups(val):
	val = [str(x).upper() for x in val]
	return val
	
# Sort by length
def bylen(val):
  items = sorted(val, key=len, reverse=True)
  return items
  
# Sort items in last character
def last(val):
  val.sort(key=lambda x: x[-1])
  return val
  
# Remove duplicate items
def duple(val):
  pair = list(set(val))
  return pair
  

