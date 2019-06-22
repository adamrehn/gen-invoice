from .Utility import Utility
import csv, os, yaml

class DataFileLoader(object):
	'''
	Provides functionality for loading invoice/quote input data from filesystem files.
	'''
	
	def __init__(self, payees_dir, payers_dir, styles_dir, templates_dir):
		'''
		Creates a new loader for the specified data directories.
		'''
		self._payees_dir = payees_dir
		self._payers_dir = payers_dir
		self._styles_dir = styles_dir
		self._templates_dir = templates_dir
	
	
	# Path resolution
	
	def resolve_items(self, items):
		'''
		Resolves the absolute path to a line items CSV file.
		'''
		return os.path.abspath(items)
	
	def resolve_payee(self, payee):
		'''
		Resolves the absolute path to a payee data YAML file.
		'''
		return os.path.join(self._payees_dir, payee + '.yml')
	
	def resolve_payer(self, payer):
		'''
		Resolves the absolute path to a payer data YAML file.
		'''
		return os.path.join(self._payers_dir, payer + '.yml')
	
	def resolve_stylesheet(self, style):
		'''
		Resolves the absolute path to a stylesheet CSS file.
		'''
		return os.path.join(self._styles_dir, style + '.css')
	
	def resolve_template(self, template):
		'''
		Resolves the absolute path to a Jinja HTML template file.
		'''
		return os.path.join(self._templates_dir, template + '.html')
	
	
	# Data loading
	
	def load_items(self, items):
		'''
		Loads line item data from a CSV file.
		'''
		with open(self.resolve_items(items), newline='') as f:
			return list([row for row in csv.DictReader(f)])
	
	def load_payee(self, payee):
		'''
		Loads payee data from a named YAML file.
		'''
		return yaml.safe_load(Utility.read_file(self.resolve_payee(payee)))
	
	def load_payer(self, payer):
		'''
		Loads payer data from a named YAML file.
		'''
		return yaml.safe_load(Utility.read_file(self.resolve_payer(payer)))
	
	def load_stylesheet(self, style):
		'''
		Loads stylesheet data from a named CSS file.
		'''
		return Utility.read_file(self.resolve_stylesheet(style))
	
	def load_template(self, template):
		'''
		Loads Jinja template data from a named HTML template file.
		'''
		return Utility.read_file(self.resolve_template(template))
