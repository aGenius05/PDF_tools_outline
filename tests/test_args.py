import unittest
from scr.main import getArgs
from io import StringIO
from contextlib import redirect_stderr

class TestArgs(unittest.TestCase):
	def setUp(self):
		self.parser = getArgs()
	def test_standard(self):
		args = self.parser.parse_args(["input.pdf", "22", "index.txt", "output.pdf"])
		self.assertEqual(args.input_pdf_file, "input.pdf")
		self.assertEqual(args.first_page, 22)
		self.assertEqual(args.outline_file, "index.txt")
		self.assertEqual(args.output_pdf_file, "output.pdf")
	def test_verbose(self):
		args = self.parser.parse_args(["input.pdf", "12", "index.txt", "output.pdf", "--verbose"])
		self.assertTrue(args.verbose)
	def test_debug(self):
		args = self.parser.parse_args(["input.pdf", "12", "index.txt", "output.pdf", "--debug"])
		self.assertTrue(args.debug)
	def test_missing_args(self):
		stderr = StringIO()
		with redirect_stderr(stderr):
			with self.assertRaises(SystemExit) as exc:
				self.parser.parse_args(["input.pdf", "12", "index.txt"])
		self.assertEqual(exc.exception.code, 2)
		self.assertIn("required", stderr.getvalue())
	def test_wrong_args(self):
		stderr = StringIO()
		with redirect_stderr(stderr):
			with self.assertRaises(SystemExit) as exc:
				self.parser.parse_args(["input.pdf", "ciao", "index.txt", "output.pdf"])
		self.assertEqual(exc.exception.code, 2)
		self.assertIn("invalid int value", stderr.getvalue())
	# TODO: handle extract arguments

if __name__ == '__main__':
	unittest.main()