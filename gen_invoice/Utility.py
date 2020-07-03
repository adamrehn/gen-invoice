from humanfriendly import prompts
import os

class Utility(object):
	'''
	Provides utility functionality.
	'''
	
	@staticmethod
	def prompt_overwrite(filename):
		'''
		Prompts the user to overwrite an existing output file
		'''
		return prompts.prompt_for_confirmation(
			'Output file {} already exists, overwrite?'.format(filename),
			padding=False
		)
	
	@staticmethod
	def replace_extension(path, extension):
		'''
		Replaces the file extension of a filename
		'''
		filename, ext = os.path.splitext(path)
		return filename + extension
	
	@staticmethod
	def read_file(filename):
		'''
		Reads data from a file
		'''
		with open(filename, 'rb') as f:
			return f.read().decode('utf-8')
	
	@staticmethod
	def write_file(filename, data):
		'''
		Writes data to a file
		'''
		with open(filename, 'wb') as f:
			f.write(data.encode('utf-8'))
