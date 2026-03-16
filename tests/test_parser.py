import unittest
from scr.main import parseOutline
from types import SimpleNamespace
from io import StringIO
from contextlib import redirect_stdout

class TestParser(unittest.TestCase):
	def setUp(self):
		self.buf = StringIO()
		self.args = SimpleNamespace(debug=False, verbose=True)
		self.start = 1
	def test_noOut(self):
		with redirect_stdout(self.buf):
			self.args.verbose = False
			parseOutline("tests/sample5/index.txt", args=self.args)
			self.assertEqual("", self.buf.getvalue().strip())
	def test_wrongSyntax(self):
		with self.assertRaises(Exception) as exc:
			self.args = SimpleNamespace(debug=False, verbose=False)
			parseOutline("tests/sample2/index.txt", args=self.args)
			self.assertIn("Error: line does not match the expected format:", exc.exception.args[0])
	def test_wrongPageNumber(self):
		with self.assertRaises(Exception) as exc:
			self.args = SimpleNamespace(debug=False, verbose=False)
			parseOutline("tests/sample2/index2.txt", args=self.args)
			self.assertIn("Error: line does not match the expected format:", exc.exception.args[0])
	def test_decreasingPageNumbers(self):
		with self.assertRaises(Exception) as exc:
			self.args = SimpleNamespace(debug=False, verbose=False)
			parseOutline("tests/sample2/index3.txt", args=self.args)
			self.assertIn("Error: page numbers must be in increasing order:", exc.exception.args[0])
	def test_debug(self):
		with redirect_stdout(self.buf):
			self.args = SimpleNamespace(debug=True, verbose=False)
			parseOutline("tests/sample4/index.txt", args=self.args)
			for line in self.buf.getvalue().strip().split("\n"):
				self.assertRegex(line, "title: .+, page number: \\d+, level: \\d+, prev: \\d+")
	def parseFile(self, file, ref=None):
		if ref is None:
			ref = file
		with redirect_stdout(self.buf):
			parseOutline(file, start=self.start, args=self.args)
			with open(ref, 'r') as f:
				self.assertEqual(f.read().strip(), self.buf.getvalue().strip())
	def test_onlyChapters(self):
		self.parseFile("tests/sample3/index.txt")
	def test_singleLevel(self):
		self.parseFile("tests/sample4/index.txt")
	def test_forwardJump(self):
		self.args.verbose = False
		with self.assertRaises(Exception) as exc:
			parseOutline("tests/sample6/index.txt", args=self.args)
			self.assertIn("Error: the difference between the next subsection level and this one must not be bigger than one:", exc.exception.args[0])
	def test_backwardJump(self):
		self.args.verbose = False
		parseOutline("tests/sample7/index.txt", args=self.args)
	def test_multiLevel(self):
		self.parseFile("tests/sample5/index.txt")
	def test_multiLevelShifted(self):
		self.start = 2
		self.parseFile("tests/sample5/index_shifted.txt", "tests/sample5/index_ref_shifted.txt")

if __name__ == '__main__':
	unittest.main()