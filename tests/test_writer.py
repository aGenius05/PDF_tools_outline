import unittest
from scr.main import writeOutline, parseOutline

class TestMain(unittest.TestCase):
	def setUp(self):
		self.outline_items = parseOutline("test_outline.txt")	# TODO: change file
	def test_toEmpty(self):
		return
	def test_fromEmpty(self):
		return
	def test_fromNonEmpty(self):
		return
	def test_NonExistingFile(self):
		return
	def test_NonExistingPage(self):
		return
	
if __name__ == '__main__':
	unittest.main()