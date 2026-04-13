from pikepdf import OutlineItem, Array, Page, String, Name, NameTree
import sys
class OutlineElement:
	def __init__(self, title, level, page_number, parent: OutlineElement = None):
		self.title = title
		self.level = level
		self.page_number = page_number
		self.parent = parent
		# TODO: set start variable
		if parent is not None:
			if parent.page_number > self.page_number:
				raise Exception("Error: page numbers must be in increasing order: page title: %s, page number: %s, level: %s but parent is at page %s\n" % (title, page_number, level, parent.page_number))
		self.children = []
	
	def from_OutlineItem(item: OutlineItem, pdf, level=0, start=None):
		page = resolve_page_from_item(pdf, item)
		page_number = page.index+1 if page is not None else None
		if page_number is None:
			print("ERROR: cannot retrive outline page number!!", file=sys.stderr)
		if start is not None:
			# TODO: get start from outline
			if page_number>start:
				page_number-=start
		element = OutlineElement(item.title, level, page_number=page_number)
		for child in item.children:
			element.add_child(OutlineElement.from_OutlineItem(child, pdf, level+1, start))
		return element

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
		# TODO: use roman number for index
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

def resolve_page_from_item(pdf, item):
    dest = item.destination

    # 1) Caso int: numero di pagina 0-based
    if isinstance(dest, int):
        return pdf.pages[dest]

    # 2) Caso array esplicito: [page.obj, /Fit..., ...]
    if isinstance(dest, Array) or isinstance(dest, list):
        return Page(dest[0])

    # 3) Caso named destination: String (Root.Names.Dests)
    if isinstance(dest, String):
        # NameTree su Root.Names.Dests
        names = pdf.Root.Names
        if names is None or Name.Dests not in names:
            return None  # oppure alza errore
        nt = NameTree(names.Dests)
        key = str(dest)          # stringa Python
        dest_array = nt[key]     # è un Array [page.obj, /Fit...]
        return Page(dest_array[Name.D][0])

    # 4) Caso named destination: Name (Root.Dests)
    if isinstance(dest, Name):
        dests = pdf.Root.get(Name.Dests)
        if dests is None:
            return None
        dest_array = dests.get(dest)
        if dest_array is None:
            return None
        return Page(dest_array[0])

    # 5) Nessuna destination: prova da action
    if dest is None and item.action is not None:
        act = item.action
        # Consideriamo solo azioni locali /GoTo
        if act.get(Name.S) == Name.GoTo and Name.D in act:
            d = act[Name.D]      # può essere Array / String / Name
            # Riusa la stessa logica ricorsivamente
            fake = type('Fake', (), {'destination': d, 'action': None})
            return resolve_page_from_item(pdf, fake)

    return None  # non risolvibile