import unittest
from scr.main import getArgs
from contextlib import redirect_stderr
from io import StringIO

# general operations
class ArgsTestCase(unittest.TestCase):
	def redirect_stderr(self):
		self.buf = StringIO()
		redirect_stderr(self.buf).__enter__()
	def returnArgs(self, args_list):
		args = getArgs([self.mode] + args_list)
		return args

# tests for general arguments
class TestArgsGlobal(ArgsTestCase):
	def setUp(self):
		self.mode = "write"
		self.redirect_stderr()
	def test_WrongMode(self):
		# test what happens when the mode is not 'write' or 'extract'
		with self.assertRaises(SystemExit) as exc:
			getArgs(["wrongmode"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("invalid mode", exc.exception.args[0])
	def test_MissingMode(self):
		# test what happens when the mode is missing
		with self.assertRaises(SystemExit) as exc:
			getArgs()
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("invalid mode", exc.exception.args[0])
	def test_version(self):
		# test the version flag
		with self.assertRaises(SystemExit) as exc:
			getArgs(["--version"])
			self.assertEqual(exc.exception.code, 0)
			self.assertIn("version", exc.exception.args[0])

class TestArgsWriter(ArgsTestCase):
	def setUp(self):
		self.mode = "write"
		self.redirect_stderr()
	def test_standard(self):
		args = self.returnArgs(["input.pdf", "--start", "22", "index.txt", "-o", "output.pdf"])
		self.assertEqual(args.mode, "write")
		self.assertEqual(args.input_pdf_file, "input.pdf")
		self.assertEqual(args.first_page, 22)
		self.assertEqual(args.outline_file, "index.txt")
		self.assertEqual(args.output_file, "output.pdf")
	def test_dry(self):
		# test the dry flag
		args = self.returnArgs(["input.pdf", "--start", "12", "index.txt", "-o", "output.pdf", "--dry"])
		self.assertTrue(args.dry)
	def test_debug(self):
		# test the debug flag
		args = self.returnArgs(["input.pdf", "--start", "12", "index.txt", "-o", "output.pdf", "--debug"])
		self.assertTrue(args.debug)
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
	def test_missing_args(self):
		# test what happens when some required arguments are missing
		with self.assertRaises(SystemExit) as exc:
			self.returnArgs([])
			print(exc)
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("required", exc.exception.args[0])
	def test_wrong_args(self):
		# test what happens when the arguments are not in the expected format
		with self.assertRaises(SystemExit) as exc:
			self.returnArgs(["input", "-o", "output", "error"])
			self.assertEqual(exc.exception.code, 2)
			self.assertIn("invalid int value", exc.exception.args[0])
	def test_debug(self):
		# test the debug flag
		args = self.returnArgs(["input.pdf", "--debug"])
		self.assertTrue(args.debug)
	def test_standard(self):
		# test the standard case
		args = self.returnArgs(["input.pdf", "-o", "output.txt"])
		self.assertEqual(args.mode, "extract")
		self.assertEqual(args.input_pdf_file, "input.pdf")
		self.assertEqual(args.output_file, "output.txt")


# TODO: handle edit arguments
	# TODO: test missing arguments
	# TODO: test wrong arguments

if __name__ == '__main__':
	unittest.main()