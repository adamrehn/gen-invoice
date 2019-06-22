from .Configuration import Configuration
from .DataFileLoader import DataFileLoader
from .InvoiceGenerator import InvoiceGenerator
from .Utility import Utility
import argparse, json, os, sys

# Prints a list of paths to data directories/files
def _print_data_paths(message, paths):
	print(message)
	for name, path in paths.items():
		print('{:11} {}'.format(name.title() + ':', path))
	print()

def main():
	
	# Retrieve our list of data subdirectories
	dirs = Configuration.list_data_dirs()
	
	# Our supported command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('payee', help='Payee name')
	parser.add_argument('payer', help='Payer name')
	parser.add_argument('items', help='CSV file containing line items')
	parser.add_argument('number', help='Invoice/quote number')
	parser.add_argument('--tax', type=float, default=0.0, help='Tax to apply, as a percentage (e.g. 0.0 for 0%%, 1.0 for 100%%)')
	parser.add_argument('--quote', action='store_true', help='Generate a quote (default is an invoice)')
	parser.add_argument('--international', action='store_true', help='Marks the invoice/quote as intended for an international recipient')
	parser.add_argument('--expiry', metavar='DATE', default=None, help='Sets the expiry date when generating a quote (default is six months from the date of generation)')
	parser.add_argument('--purchase', metavar='ORDER', default=None, help='Specifies a purchase order reference number to include when generating an invoice')
	parser.add_argument('--template', default='default', help='Specifies the HTML template to use')
	parser.add_argument('--style', default='default', help='Specifies the CSS stylesheet to use')
	parser.add_argument('-y', '--overwrite', dest='overwrite', action='store_true', help='Overwrite existing output files without prompting for confirmation')
	parser.add_argument('--no-pdf', action='store_true', help='Disable PDF generation even if electron-pdf is available')
	parser.add_argument('--context', metavar='KEY=VALUE', action='append', help='Specify custom data to include in the template rendering context (can be specified multiple times)')
	parser.add_argument('--dump-context', action='store_true', help='Print the template rendering context (for debugging purposes)')
	
	# If no arguments were supplied, display the help message and exit
	if len(sys.argv) < 2:
		
		# Print our usage syntax
		parser.print_help()
		
		# List our data subdirectories so users know where to place files
		_print_data_paths('\nData files will be loaded from the following locations:', {
			name: os.path.join(details['path'], details['pattern'])
			for name, details in dirs.items()
		})
		
		sys.exit(0)
	
	# Parse the supplied arguments
	args = parser.parse_args()
	
	try:
		
		# Parse any custom context data arguments
		context_overrides = {}
		if args.context is not None:
			for pair in args.context:
				try:
					key, value = pair.split('=')
					context_overrides[key] = value
				except:
					raise RuntimeError('invalid key/value pair "{}"'.format(pair))
		
		# Ensure our data directories and default files exist
		Configuration.create_directories()
		Configuration.create_defaults()
		
		# Create a loader to parse our input data files
		loader = DataFileLoader(
			dirs['payees']['path'],
			dirs['payers']['path'],
			dirs['styles']['path'],
			dirs['templates']['path']
		)
		
		# Display the resolved file paths we are attempting to load our data from
		_print_data_paths('Loading data from the following files:', {
			'items': loader.resolve_items(args.items),
			'payee': loader.resolve_payee(args.payee),
			'payer': loader.resolve_payer(args.payer),
			'stylesheet': loader.resolve_stylesheet(args.style),
			'template': loader.resolve_template(args.template)
		})
		
		# Attempt to load our data files
		items = loader.load_items(args.items)
		payee = loader.load_payee(args.payee)
		payer = loader.load_payer(args.payer)
		stylesheet = loader.load_stylesheet(args.style)
		template = loader.load_template(args.template)
		
		# Determine the full paths for our output files
		html = Utility.replace_extension(os.path.abspath(args.items), '.html')
		pdf = Utility.replace_extension(html, '.pdf')
		
		# If the output HTML file already exists, prompt for overwrite
		if os.path.exists(html) == True and args.overwrite == False:
			if Utility.prompt_overwrite(html) == False:
				return
		
		# Generate the HTML file
		generator = InvoiceGenerator()
		context = generator.generate(
			outfile = html,
			number = args.number,
			items = items,
			payee = payee,
			payer = payer,
			template = template,
			stylesheet = stylesheet,
			tax = args.tax,
			is_international = args.international,
			is_quote = args.quote,
			expiry = args.expiry,
			purchase_order = args.purchase,
			context_overrides = context_overrides
		)
		
		# Dump the template rendering context if the user requested it
		if args.dump_context == True:
			print(json.dumps(context, indent=4))
		
		# Determine if we are generating a PDF file
		if args.no_pdf == False:
			
			# If the output PDF file already exists, prompt for overwrite
			if os.path.exists(pdf) == True and args.overwrite == False:
				if Utility.prompt_overwrite(pdf) == False:
					return
			
			# Attempt to render to PDF
			if generator.render(html, pdf) == False:
				print('Could not find electron-pdf 4.0.6 or newer, skipping PDF generation.')
		
		# If we reach this point then generation was successful
		print('Generation complete!')
		
	except Exception as err:
		print('Error: {}'.format(err), file=sys.stderr)
