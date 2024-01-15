''' DISPLAY FORMAT '''
# items display in column 	
def col(item):
  for x in item:
    return x

# items display in row
def row(item):
  val = ', '.join(map(str, item))
  return val

# items display in nunbered
def numbered(item):
  value = numbered_list = "\n".join(f"{x}. {item}" for x, item in enumerate(item, 1))
  return value
# items display in letters
def lett(item):
  temp = []
  for x, item in enumerate(item, start=1):
    temp.append(f'{chr(96 + x)}. {item}')
  val = [x for x in temp]
  form = '\n'.join(f'{x}' for x in val)
  return form
  
# dictionary mode
def dict_format(item):
  val = '{' + ', '.join(f'{x}' for x in item) + '}'
  return val

# set mode
def set_format(item):
  val = '(' + ', '.join(f'{x}' for x in item) + ')'
  return val
  
# loop display in list
def list_format(item):
  val = [x for x in item]
  return val
		
# count size of the list
def sizeOf(val):
	count = 0	
	for x in val:
		count += 1
	return count
	