from os.path import abspath, dirname, join
from setuptools import setup

# Read the README markdown data from README.md
with open(abspath(join(dirname(__file__), 'README.md')), 'rb') as readmeFile:
	__readme__ = readmeFile.read().decode('utf-8')

setup(
	name='gen-invoice',
	version='0.0.3',
	description='Template-based invoice generator',
	long_description=__readme__,
	long_description_content_type='text/markdown',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Environment :: Console'
	],
	keywords='invoice template html pdf',
	url='http://github.com/adamrehn/gen-invoice',
	author='Adam Rehn',
	author_email='adam@adamrehn.com',
	license='MIT',
	packages=['gen_invoice'],
	zip_safe=False,
	python_requires = '>=3.5',
	install_requires = [
		'appdirs>=1.4.3',
		'humanfriendly>=8.2',
		'Jinja2>=2.10.1',
		'python-dateutil>=2.8.0',
		'PyYAML>=5.1.1',
		'setuptools>=38.6.0',
		'twine>=1.11.0',
		'wheel>=0.31.0'
	],
	package_data = {
		'gen_invoice': [
			'defaults/*'
		]
	},
	entry_points = {
		'console_scripts': ['gen-invoice=gen_invoice.cli:main']
	}
)
