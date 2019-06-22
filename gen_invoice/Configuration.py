import appdirs, os, shutil

# The identifier we use to represent gen-invoice in directory paths
APPLICATION_NAME = 'gen-invoice'

class Configuration(object):
	'''
	Provides functionality for managing invoice generation configuration.
	'''
	
	@staticmethod
	def create_defaults():
		'''
		Creates our default template and style files if they don't already exist.
		'''
		for name, details in Configuration.list_data_dirs().items():
			filename = details['pattern'].replace('*', 'default')
			source = os.path.join(os.path.dirname(__file__), 'defaults', filename)
			dest = os.path.join(details['path'], filename)
			
			# Copy the default file if we have one and it doesn't exist in the data directory
			if os.path.exists(source) == True and os.path.exists(dest) == False:
				shutil.copy2(source, dest)
	
	@staticmethod
	def create_directories():
		'''
		Ensures all of the application's data subdirectories exist.
		'''
		for name, details in Configuration.list_data_dirs().items():
			os.makedirs(details['path'], exist_ok=True)
	
	@staticmethod
	def list_data_dirs():
		'''
		Lists our application's data subdirectories.
		
		Returns a dictionary mapping from named subdirectory to directory details.
		'''
		return {
			'payees': {
				'path': Configuration.get_payees_dir(),
				'pattern': '*.yml'
			},
			
			'payers': {
				'path': Configuration.get_payers_dir(),
				'pattern': '*.yml'
			},
			
			'styles': {
				'path': Configuration.get_styles_dir(),
				'pattern': '*.css'
			},
			
			'templates': {
				'path': Configuration.get_templates_dir(),
				'pattern': '*.html'
			}
		}
	
	@staticmethod
	def get_data_dir():
		'''
		Determines the path of the application's data directory.
		'''
		return appdirs.user_config_dir(APPLICATION_NAME, False, roaming=True)
	
	@staticmethod
	def get_payees_dir():
		'''
		Determines the path of the payees data subdirectory.
		'''
		return Configuration._resolve_subdir('payees')
	
	@staticmethod
	def get_payers_dir():
		'''
		Determines the path of the payers data subdirectory.
		'''
		return Configuration._resolve_subdir('payers')
	
	@staticmethod
	def get_styles_dir():
		'''
		Determines the path of the styles data subdirectory.
		'''
		return Configuration._resolve_subdir('styles')
	
	@staticmethod
	def get_templates_dir():
		'''
		Determines the path of the templates data subdirectory.
		'''
		return Configuration._resolve_subdir('templates')
	
	
	# "Private" methods
	
	@staticmethod
	def _resolve_subdir(subdir):
		'''
		Resolves a subdirectory with respect to the application's data directory.
		'''
		return os.path.join(Configuration.get_data_dir(), subdir)
