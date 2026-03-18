import unittest
from scr.main import writeOutline, parseOutline
import pikepdf

class TestMain(unittest.TestCase):
	def write(self, pdf_file, ref_file):
		# write the outline items to the pdf file and compare them with the reference if provided
		with pikepdf.open(pdf_file) as pdf:
			writeOutline(pdf, self.outline_items)
			with pikepdf.open(ref_file) as ref:
				self.assertEqual(pdf.Root.Outlines, ref.Root.Outlines)
	def test_toEmpty(self):
		# test wrriting an empty outline
		self.outline_items = parseOutline("tests/sample1/index.txt")
		self.write("tests/sample1/input.pdf", "tests/sample1/pdf_ref.pdf")
	def test_fromEmpty(self):
		# test writing an outline to a pdf that does not have one
		self.outline_items = parseOutline("tests/sample5/index.txt")
		self.write("tests/sample5/input.pdf", "tests/sample5/pdf_ref.pdf")
	def test_fromNonEmpty(self):
		# test writing an outline to a pdf that already has one
		self.outline_items = parseOutline("tests/sample3/index.txt")
		self.write("tests/sample3/input.pdf", "tests/sample3/pdf_ref.pdf")
	def test_NonExistingPage(self):
		# test what happens when the outline contains a page number that is bigger than the last page number of the pdf
		self.outline_items = parseOutline("tests/sample7/index.txt")
		with self.assertRaises(IndexError):
			self.write("tests/sample7/input.pdf", "tests/sample7/pdf_ref.pdf")
	
if __name__ == '__main__':
	unittest.main()