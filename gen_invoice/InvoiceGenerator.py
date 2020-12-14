import collections, csv, datetime, json, locale, os, platform, shutil, subprocess, tempfile, yaml
from jinja2 import Environment, FileSystemLoader, Template
from dateutil.relativedelta import relativedelta
from pkg_resources import parse_version
from .Utility import Utility


# The minimum version of electron-pdf that we require in order to generate PDF files
ELECTRON_PDF_MIN_VERSION = '4.0.6'


class InvoiceGenerator(object):
	'''
	Provides functionality for generating HTML and PDF files for invoices/quotes.
	'''
	
	def __init__(self):
		'''
		Creates a new generator.
		'''
		pass
	
	def generate_string(self, number, items, payee, payer, template, stylesheet, tax=0.0, is_international=False, is_quote=False, expiry=None, purchase_order=None, context_overrides=None):
		'''
		Generates the HTML for an invoice/quote with the specified options and returns it.
		'''
		with tempfile.TemporaryDirectory() as tempDir:
			outfile = os.path.join(tempDir, 'output.html')
			self.generate(outfile, number, items, payee, payer, template, stylesheet, tax, is_international, is_quote, expiry, purchase_order, context_overrides)
			return Utility.read_file(outfile)
	
	def generate(self, outfile, number, items, payee, payer, template, stylesheet, tax=0.0, is_international=False, is_quote=False, expiry=None, purchase_order=None, context_overrides=None):
		'''
		Generates an invoice/quote with the specified options.
		'''
		
		# If the payee details object has top-level "domestic" and "international" keys, use the appropriate details
		if 'domestic' in payee and 'international' in payee:
			payee = payee['international'] if is_international == True else payee['domestic']
		
		# Process the line items data, grouping line items by section
		# (Note that we use an OrderedDict to maintain section ordering based on the CSV ordering)
		sections = collections.OrderedDict()
		for line in items:
			
			# Parse the line item details
			item = {
				'description': line['Item'],
				'units': line['Units'],
				'quantity': float(line['Quantity']) if '.' in line['Quantity'] else int(line['Quantity']),
				'price': float(line['Price'])
			}
			
			# Calculate the total for the line item
			item['total'] = item['price'] * item['quantity']
			
			# Create a section entry for the line item's section if we don't already have one
			section = line.get('Section', '')
			if section not in sections:
				sections[section] = {
					'description': section,
					'lines': [],
					'total': 0.0
				}
			
			# Add the line item details to the list for its section
			sections[section]['lines'].append(item)
		
		# Compute the subtotal for each section
		for section in sections:
			sections[section]['total'] = sum([i['total'] for i in sections[section]['lines']])
		
		# Compute the overall total
		total = sum([sections[section]['total'] for section in sections])
		
		# Apply any tax (GST/VAT)
		tax = total * tax
		total += tax
		
		# If no expiry date was specified, set the expiry to six months from the date of generation
		if expiry is None:
			expiry = (datetime.date.today() + relativedelta(months=6)).strftime('%Y-%m-%d')
		
		# Prepare our context for template rendering
		context = {
			'invoice': is_quote == False,
			'quote': is_quote == True,
			'domestic': is_international == False,
			'international': is_international == True,
			'number': number,
			'date': datetime.datetime.now().strftime('%Y-%m-%d'),
			'expiry': expiry,
			'purchase_order': purchase_order,
			'payee': payee,
			'payer': payer,
			'sections': list(sections.values()),
			'tax': tax,
			'total': total,
			'css': stylesheet
		}
		
		# If any context overrides were supplied, apply them
		if context_overrides is not None and isinstance(context_overrides, dict):
			context.update(context_overrides)
		
		# Create our Jinja template environment and add a "currency" filter for formatting currency values
		environment = Environment(autoescape=False)
		environment.filters['currency'] = InvoiceGenerator._format_currency
		
		# Attempt to instantiate our HTML template
		templateInstance = environment.from_string(template)
		
		# Render the template to our HTML output file
		rendered = templateInstance.render(context)
		Utility.write_file(outfile, rendered)
		
		# Return the context so it can be used for diagnostic purposes
		return context
	
	def render(self, html, pdf):
		'''
		Renders an invoice/quote HTML file to a PDF using electron-pdf.
		'''
		
		# Use the system shell to run commands under Windows
		useShell = platform.system().lower() == 'windows'
		
		# Determine whether a compatible version electron-pdf is installed or if we need to force the version number
		versionOverride = ''
		try:
			
			# Attempt to retrieve the version string from electron-pdf
			output = subprocess.run(
				['npx', 'electron-pdf', '--version'],
				stdout=subprocess.PIPE,
				check=True,
				shell=useShell
			)
			
			# Verify that the version meets our minimum requirement
			version = parse_version(output.stdout.decode('utf-8').strip())
			if version < parse_version(ELECTRON_PDF_MIN_VERSION):
				raise RuntimeError('')
			
		except:
			versionOverride = '@{}'.format(ELECTRON_PDF_MIN_VERSION)
		
		# Remove the PDF file if it already exists
		if os.path.exists(pdf):
			os.unlink(pdf)
		
		# Generate the PDF file
		subprocess.run(
			[
				'npx',
				'electron-pdf{}'.format(versionOverride),
				'file:///' + html.replace('\\', '/'),
				pdf.replace('\\', '/'),
				'--printBackground',
				'--pageSize=A4',
				'--marginsType=0',
				'--waitForJSEvent', 'did-finish-load'
			],
			check=True,
			shell=useShell
		)
		
		# Verify that the PDF file was generated successfully
		if os.path.exists(pdf) == False:
			raise RuntimeError('failed to generate PDF using electron-pdf')
		
		return True
	
	
	# "Private" methods
	
	@staticmethod
	def _format_currency(value):
		'''
		Formats a numeric value as a currency string using the system's locale settings
		'''
		
		# Set our locale to the system default
		locale.setlocale(locale.LC_ALL, '')
		
		# Format the value using the currency settings for our locale
		return locale.currency(value, symbol=True, grouping=True)
