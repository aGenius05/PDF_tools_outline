#!/usr/bin/env python3
import pikepdf
from pikepdf import Name, Dictionary, Array, OutlineItem
from sys import argv
import re

if len(argv) != 5:
	print ('Arguments: [input_pdf_file] [first_page] [outline_file] [output_pdf_file]')
	exit(-1)
      
# argomenti
start = int(argv[2])
file_input = argv[1]
file_outline = argv[3]
file_output = argv[4]


class OutlineElement:
	def __init__(self, title, level, page_number, parent=None):
		self.title = title
		self.level = level
		self.page_number = page_number
		self.parent = parent
		self.children = []
	
	def add_child(self, child):
		self.children.append(child)
	
	def returnNode(self):
		if self.children == []:
			return OutlineItem(self.title, self.page_number-1)
		else:
			node = OutlineItem(self.title, self.page_number-1)
			for child in self.children:
				node.children.append(child.returnNode())
			return node
	
	def __repr__(self):
		text = (self.level*"  ")+str(self.page_number)+" "+self.title
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
def getNumber(s):
	try:
		return(int(s))+start-1	# la numerazione reale parte da start(-1 perché l'indice parte da 0)
	except ValueError:
		pass
	res = 0
	i = 0
	while i < len(s):
        
		# get value of current symbol
		s1 = romanValue(s[i])

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

# parsing indice
r_entry = r"^(\s*)(([ivxlcdm]||\d)+)\s+(.*?)\s*$"          # Outline entry regex 
outline_items = []
with open("%s" % file_outline, 'r') as f:
	lines = [line.rstrip() for line in f.readlines() if not (line == '' or line == '\n' or line == '\r')]
	for line in lines:
		parts = re.match(r_entry, line).groups()
		prev = 0
		par = None
		if len(parts) >= 3:
			title = parts[3]
			page_number = getNumber(parts[1])
			level = int(parts[0].count(' '))
			if level == prev:
				outline_items.append(OutlineElement(title, level, page_number))
			elif level == prev+1:
				prev+=1
				outline_items[-1].add_child(OutlineElement(title, level, page_number, outline_items[-1]))
			elif level < prev:
				prev = level
				par = outline_items[-1]
				for i in range(prev):
					if par.children:
						par = par.children[-1]
				par.add_child(OutlineElement(title, level, page_number, par))
			else:
				raise Exception("Error: the difference between the next subsection level and this one must not be bigger than one.")

for item in outline_items:
	print(repr(item))

with pikepdf.open(file_input) as pdf:
	# inserisco numerazione logica con numeri romani
	# Creiamo la struttura dei numeri di pagina (PageLabels)
	# /Nums è un array dove ogni coppia è: [indice_pagina_inizio, dizionario_stile]
	# L'indice parte da 0 (0 = prima pagina del PDF)
	page_labels = Dictionary({
		"/Nums": Array([
			0, Dictionary({
				"/S": Name("/r"),  # Romano minuscolo
				"/St": 1
			}),
			(start-1), Dictionary({
				"/S": Name("/D"),  # Decimale (arabo)
				"/St": 1
			})
		])
		})
	# Inseriamo il dizionario nel 'Catalog' (la radice del PDF)
	pdf.Root.PageLabels = page_labels

	# scrittura indice da file
	with pdf.open_outline() as outline:
		outline.root = []
		for item in outline_items:
			# Aggiungiamo l'item all'indice del PDF
			outline.root.append(item.returnNode())

	# Salva il nuovo file
	pdf.save(file_output)

print(f"File salvato con successo come: {file_output}")