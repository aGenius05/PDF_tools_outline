import unittest
from scr.main import getArgs
from contextlib import redirect_stderr
from io import StringIO

class ArgsTestCase(unittest.TestCase):
	def redirect_stderr(self):
		self.buf = StringIO()
		redirect_stderr(self.buf).__enter__()
	def returnArgs(self, args_list):
		args = getArgs([self.mode] + args_list)
		return args


class TestArgsGlobal(ArgsTestCase):
	def setUp(self):
		self.mode = "write"
		self.redirect_stderr()
	def test_debug(self):
		# test the debug flag
		args = self.returnArgs(["input.pdf", "--start", "12", "index.txt", "-o", "output.pdf", "--debug"])
		self.assertTrue(args.debug)
	# TODO: test wrong mode argument
	# TODO: test version flag

class TestArgsWriter(ArgsTestCase):
	def setUp(self):
		self.mode = "write"
		self.redirect_stderr()
	def test_standard(self):
		args = self.returnArgs(["input.pdf", "--start", "22", "index.txt", "-o", "output.pdf"])
		self.assertEqual(args.input_pdf_file, "input.pdf")
		self.assertEqual(args.first_page, 22)
		self.assertEqual(args.outline_file, "index.txt")
		self.assertEqual(args.output_file, "output.pdf")
	def test_dry(self):
		# test the dry flag
		args = self.returnArgs(["input.pdf", "--start", "12", "index.txt", "-o", "output.pdf", "--dry"])
		self.assertTrue(args.dry)
	def test_missing_args(self):
		# test what happens when some required arguments are missing
		with self.assertRaises(SystemExit) as exc:
			self.returnArgs(["input.pdf", "--start", "12"])
			print(exc)
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("required", exc.exception.args[0])
	def test_wrong_args(self):
		# test what happens when the arguments are not in the expected format
		with self.assertRaises(SystemExit) as exc:
			self.returnArgs(["input.pdf", "--start", "ciao", "index.txt", "-o", "output.pdf"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("invalid int value", exc.exception.args[0])
	def test_negative_start(self):
		# test what happens when the start argument is negative
		with self.assertRaises(Exception) as exc:
			self.returnArgs(["input.pdf", "--start", "-1", "index.txt", "-o", "output.pdf"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("the first real page number must be greater than or equal to 1", exc.exception.args[0])

class TestArgsExtractor(ArgsTestCase):
	def setUp(self):
		self.mode = "extract"
		self.redirect_stderr()
# TODO: handle extract arguments
	# TODO: test missing arguments
	# TODO: test wrong arguments

# TODO: handle edit arguments
	# TODO: test missing arguments
	# TODO: test wrong arguments
if __name__ == '__main__':
	unittest.main()