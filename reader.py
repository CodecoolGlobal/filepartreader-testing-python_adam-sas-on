import os
import chardet

class FilePartReader:
	def __init__(self):
		self.file_path = ""
		self.from_line = -1
		self.to_line = -1
		self.file_exists = False
		self.charset = ""
	#
	def setup(self, path, from_line, to_line):
		if from_line < 1 or (from_line > to_line and to_line != -1):
			self.file_exists = False
			raise ValueError("FilePartReader.setup: wrong arguments from_line and/or to_line!")

		self.file_path = path
		self.from_line = from_line
		self.to_line = to_line
		if os.path.isfile(path):
			self.file_exists = True
			with open(self.file_path, 'rb') as f:
				rawdata = f.read()
				chars = chardet.detect(rawdata)
				self.charset = chars['encoding']
				if self.to_line < 0:
					self.to_line = self.lines_in_file()
		else:
			self.file_exists = False

	def read(self):
		if not self.file_exists:
			raise FileNotFoundError

		file_content = ""
		with open(self.file_path, encoding=self.charset) as f:
			file_content = f.read()

		return file_content
	#

	def read_lines(self):
		if not self.file_exists:
			raise FileNotFoundError

		pass
	#

	def get_read_range(self):
		return (self.from_line, self.to_line)

	def set_read_range(self, from_line, to_line=-1):
		if from_line < 1 or (from_line > to_line and to_line != -1):
			raise ValueError("FilePartReader.setup: wrong arguments from_line and/or to_line!")

		self.from_line = from_line
		self.to_line = to_line

	def set_file_path(self, new_file):
		self.file_path = new_file
		if os.path.isfile(path):
			self.file_exists = True
		else:
			self.file_exists = False
	#

	def lines_in_file(self):
		lines = 0
		with open(self.file_path, encoding=self.charset) as f:
			buf_size = 1024 * 1024
			read_f = f.read

			buf = read_f(buf_size)
			while buf:
				lines += buf.count('\n')
				buf = read_f(buf_size)

		return lines
	#

