import unittest
from scr.main import getArgs

class TestArgs(unittest.TestCase):
	def setUp(self):
		self.parser = getArgs()
	def test_standard(self):
		return
	def test_verbose(self):
		return
	def test_debug(self):
		return
	def test_missing_args(self):
		return
	def test_wrong_args(self):
		return
	# TODO: handle extract arguments

if __name__ == '__main__':
	unittest.main()