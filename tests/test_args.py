import unittest
from scr.main import getArgs
from contextlib import redirect_stderr
from io import StringIO

class TestArgs(unittest.TestCase):
	def setUp(self):
		self.parser = getArgs()
		self.buf = StringIO()
		redirect_stderr(self.buf).__enter__()
	def test_standard(self):
		args = self.parser.parse_args(["input.pdf", "--start", "22", "index.txt", "output.pdf"])
		self.assertEqual(args.input_pdf_file, "input.pdf")
		self.assertEqual(args.first_page, 22)
		self.assertEqual(args.outline_file, "index.txt")
		self.assertEqual(args.output_pdf_file, "output.pdf")
	def test_dry(self):
		# test the dry flag
		args = self.parser.parse_args(["input.pdf", "--start", "12", "index.txt", "output.pdf", "--dry"])
		self.assertTrue(args.dry)
	def test_debug(self):
		# test the debug flag
		args = self.parser.parse_args(["input.pdf", "--start", "12", "index.txt", "output.pdf", "--debug"])
		self.assertTrue(args.debug)
	def test_missing_args(self):
		# test what happens when some required arguments are missing
		with self.assertRaises(SystemExit) as exc:
			self.parser.parse_args(["input.pdf", "--start", "12", "index.txt"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("required", exc.exception.args[0])
	def test_wrong_args(self):
		# test what happens when the arguments are not in the expected format
		with self.assertRaises(SystemExit) as exc:
			self.parser.parse_args(["input.pdf", "--start", "ciao", "index.txt", "output.pdf"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("invalid int value", exc.exception.args[0])
	def test_negative_start(self):
		# test what happens when the start argument is negative
		with self.assertRaises(Exception) as exc:
			self.parser.parse_args(["input.pdf", "--start", "-1", "index.txt", "output.pdf"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("the first real page number must be greater than or equal to 1", exc.exception.args[0])
	# TODO: handle extract arguments

if __name__ == '__main__':
	unittest.main()