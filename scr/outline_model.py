from pikepdf import OutlineItem

class OutlineElement:
	def __init__(self, title, level, page_number, parent: OutlineElement = None):
		self.title = title
		self.level = level
		self.page_number = page_number
		self.parent = parent
		if parent is not None:
			if parent.page_number > self.page_number:
				raise Exception("Error: page numbers must be in increasing order: page title: %s, page number: %s, level: %s but parent is at page %s\n" % (title, page_number, level, parent.page_number))
		self.children = []
	
	def add_child(self, child):
		self.children.append(child)
	
	# function to create corresponding OutlineItem structure for this element and its children
	def returnNode(self):
		if self.children == []:
			return OutlineItem(self.title, self.page_number-1)
		else:
			node = OutlineItem(self.title, self.page_number-1)
			for child in self.children:
				node.children.append(child.returnNode())
			return node
	
	def __repr__(self):
		text = (self.level*" ")+str(self.page_number)+" "+self.title
		if self.children != []:
			for child in self.children:
				text += "\n" + repr(child)
		return text

# this function returns value of a Roman symbol
def romanValue(r):
	if r == 'I' or r == 'i':
		return 1
	if r == 'V' or r == 'v':
		return 5
	if r == 'X' or r == 'x':
		return 10
	if r == 'L' or r == 'l':
		return 50
	if r == 'C' or r == 'c':
		return 100
	if r == 'D' or r == 'd':
		return 500
	if r == 'M' or r == 'm':
		return 1000
	return -1

# returns decimal value of page number
def getNumber(s, start=1):
	try:
		return(int(s))+start-1	# la numerazione reale parte da start(-1 perché l'indice parte da 0)
	except ValueError:
		pass
	res = 0
	i = 0
	while i < len(s):
		
		# get value of current symbol
		s1 = romanValue(s[i])
		if s1 == -1:
			raise Exception("Error: invalid page number: %s" % s)

		# compare with the next symbol if it exists
		if i + 1 < len(s):
			s2 = romanValue(s[i + 1])

			# if current value is greater or equal, 
			# add it to result
			if s1 >= s2:
				res += s1
			else:
				# else, add the difference and 
				# skip next symbol
				res += (s2 - s1)
				i += 1
		else:
			res += s1
		i += 1

	return res