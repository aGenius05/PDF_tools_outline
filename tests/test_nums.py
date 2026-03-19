import unittest
from scr.main import addLogicNums
from types import SimpleNamespace
import pikepdf

class TestLogicNumbers(unittest.TestCase):
	def setUp(self):
		self.args = SimpleNamespace(debug=False, dry=False)
		self.start = 1
	def writeNums(self, file, ref=None):
		# write logical page numbers to the pdf file and compare them with the reference if provided
		with pikepdf.open(file) as pdf:
			addLogicNums(pdf, self.start)
			if ref is not None:
				with pikepdf.open(ref) as ref:
					self.assertEqual(pdf.Root.PageLabels, ref.Root.PageLabels)
			pdf.save('/tmp/out.pdf')
	def test_onlyRealPages(self):
		# start=1
		self.writeNums("tests/sample1/input.pdf", "tests/sample1/pdf_ref.pdf")
	def test_nonExistingPage(self):
		# start>last page number
		with self.assertRaises(IndexError) as exc:
			self.start = 17
			self.writeNums("tests/sample7/input.pdf")
	def test_standard(self):
		self.start = 2
		self.writeNums("tests/sample5/input.pdf", "tests/sample5/pdf_shifted_ref.pdf")
	def test_fromExisting(self):
		# write on a pdf that already has logical page numbers, with a different start
		self.writeNums("tests/sample4/input.pdf", "tests/sample4/pdf_ref.pdf")
	
if __name__ == '__main__':
	unittest.main()