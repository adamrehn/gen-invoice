# Command-line interface

Generate invoices and quotes from shell scripts or an interactive terminal.


## Installation

The gen-invoice command-line interface is bundled as part of the Python package. To start using the command-line interface, first install the package via pip:

```
pip3 install gen-invoice
```

Once the package is installed you will be able to run the gen-invoice command-line tool like so (the command below displays the usage syntax details):

```
gen-invoice --help
```

If you want to generate PDFs then you will also need to install [electron-pdf](https://www.npmjs.com/package/electron-pdf) v4.0.6 or newer:

```
npm install electron-pdf -g
```


## Data directory location

The command-line tool searches for input data files in a user-specific directory that varies based on the platform:

- **Linux:** `~/.config/gen-invoice` (unless overridden using the `XDG_CONFIG_HOME` environment variable)
- **macOS:** `~/Library/Preferences/gen-invoice`
- **Windows:** `%APPDATA%\gen-invoice`

Specific subdirectories under the root data directory are scanned for different types of input files:

- `payees`: [payee YAML](../input-data/payees.md) files
- `payers`: [payer YAML](../input-data/payers.md) files
- `stylesheets`: [stylesheet CSS](../input-data/stylesheets.md) files
- `templates`: [template HTML](../input-data/templates.md) files

> [!NOTE]
> **The root data directory and its subdirectories will be created automatically the first time the command-line tool is run and recreated on subsequent runs if they have been deleted.** The default template HTML file and stylesheet CSS file will also be (re)created in their respective subdirectories if they do not exist.

You can see the exact list of search directories by running `gen-invoice --help`, which will display the search directories beneath the usage syntax details.


## Basic usage

The minimum set of required arguments for generating an invoice is as follows:

```bash
gen-invoice PAYEE PAYER ITEMS NUMBER
```

The first three positional arguments specify the [payee](../input-data/payees.md) YAML filename, [payer](../input-data/payers.md) YAML filename, and [line items](../input-data/items.md) CSV filename, respectively. The fourth positional argument specifies the invoice number.

The key thing to note is the manner in which filenames are resolved based on the specified arguments. For example, imagine that we were to run the following command:

```bash
# Note that since we don't specify a template or stylesheet here, the defaults will be used
gen-invoice us them goods.csv 1234
```

The command-line tool would look for the input files in the following locations (these examples use the data directory location for Linux, but this will vary based on platform):

- Line items CSV file: `goods.csv` in the current working directory
- Payee YAML file: `~/.config/gen-invoice/payees/us.yml`
- Payer YAML file: `~/.config/gen-invoice/payees/them.yml`
- Stylesheet CSS file: `~/.config/gen-invoice/stylesheets/default.css`
- Template HTML file: `~/.config/gen-invoice/templates/default.html`

**The line items CSV file argument is treated as an actual file path**, which can be an absolute path or a path relative to the current working directory. The payee and payer arguments are treated as filenames without an extension, and the command-line tool will look for them in the appropriate subdirectory of the [root data directory](#data-directory-location) for the current user. The latter behaviour is also applied to the template and stylesheet, which both default to the name `default` when not otherwise specified by the user.

> [!NOTE]
> Resolved input file paths will be displayed each time you run the command-line tool, so you can easily observe the results of file resolution behaviour during actual usage without needing to refer to the documentation.

The command-line tool will use the path of the line items CSV file for generating the output HTML and PDF filenames, simply replacing the `.csv` extension with `.html` and `.pdf`, respectively. If the output file(s) already exist then the user will be prompted to confirm that they should be overwritten. You can specify the `-y` or `--overwrite` flags to automatically overwrite output files without prompting:

```bash
# Will create the output files goods.html and goods.pdf
gen-invoice us them goods.csv 1234

# Will prompt the user to confirm overwrite of the output files goods.html and goods.pdf
gen-invoice us them goods.csv 1234

# Will automatically overwrite the output files goods.html and goods.pdf without prompting
gen-invoice us them goods.csv 1234 --overwrite
gen-invoice us them goods.csv 1234 -y
```


## Controlling PDF generation

The command-line tool will automatically use [electron-pdf](https://www.npmjs.com/package/electron-pdf) to render HTML output files to PDF if electron-pdf v4.0.6 or newer is installed and available in the `PATH` environment variable. You can disable PDF generation by specifying the `--no-pdf` flag:

```bash
# Will create the output file goods.html, but not goods.pdf
gen-invoice us them goods.csv 1234 --no-pdf
```


## Using specific templates and stylesheets

You can specify a template name using the `--template` argument and/or a stylesheet name using the `--stylesheet` argument. The possible combinations are shown below:

```bash
# Template: default, Stylesheet: default
gen-invoice us them goods.csv 1234

# Template: detailed, Stylesheet: default
gen-invoice us them goods.csv 1234 --template=detailed

# Template: default, Stylesheet: fancy
gen-invoice us them goods.csv 1234 --stylesheet=fancy

# Template: detailed, Stylesheet: fancy
gen-invoice us them goods.csv 1234 --template=detailed --stylesheet=fancy
```

The HTML and CSS files for templates and stylesheets are resolved using the same rules as described in the [Basic usage](#basic-usage) section:

- Example 1 (Template: default, Stylesheet: default)
  
  - Stylesheet CSS file: `~/.config/gen-invoice/stylesheets/default.css`
  - Template HTML file: `~/.config/gen-invoice/templates/default.html`

- Example 2 (Template: detailed, Stylesheet: default)
  
  - Stylesheet CSS file: `~/.config/gen-invoice/stylesheets/default.css`
  - Template HTML file: `~/.config/gen-invoice/templates/detailed.html`

- Example 3 (Template: default, Stylesheet: fancy)
  
  - Stylesheet CSS file: `~/.config/gen-invoice/stylesheets/fancy.css`
  - Template HTML file: `~/.config/gen-invoice/templates/default.html`

- Example 4 (Template: detailed, Stylesheet: fancy)
  
  - Stylesheet CSS file: `~/.config/gen-invoice/stylesheets/fancy.css`
  - Template HTML file: `~/.config/gen-invoice/templates/detailed.html`


## Generating quotes

You can generate a quote instead of an invoice by specifying the `--quote` flag:

```bash
# Generates a quote with an expiry date six months from the current date
gen-invoice us them goods.csv 1234 --quote
```

All generated quotes have an expiry date associated with them, which defaults to six months from the date when the quote is generated. You can specify a custom expiry date using the `--expiry` flag:

```bash
# Generates a quote with an expiry date of 1st December 2099
gen-invoice us them goods.csv 1234 --quote --expiry=2099-12-01
```


## Generating invoices for purchase orders

You can specify a purchase order number to associate with an invoice using the `--purchase` flag:

```bash
# Generates an invoice associated with purchase order number 12345678
# (Note that this is separate from the invoice number, which is 1234)
gen-invoice us them goods.csv 1234 --purchase=12345678
```


## Generating international invoices and quotes

You can specify that an invoice or quote is intended for an international recipient by specifying the `--international` flag:

```bash
# Generates an international invoice rather than a domestic invoice
gen-invoice us them goods.csv 1234 --international
```


## Specifying tax

The invoice generator supports calculating tax for [value-added tax systems such as GST or VAT](https://en.wikipedia.org/wiki/Value-added_tax) that add a percentage to the total value of the line items. You can specify the tax percentage by specifying the `--tax` flag with a decimal value representing the tax percentage (e.g. 0.0 for 0% tax and 1.0 for 100% tax):

```bash
# Specifies 0% tax (the default)
gen-invoice us them goods.csv 1234 --tax=0.0

# Specifies 10% tax
gen-invoice us them goods.csv 1234 --tax=0.1

# Specifies 30% tax
gen-invoice us them goods.csv 1234 --tax=0.3
```


## Inspecting and manipulating context data

As per the terminology used in the documentation for the [Jinja template engine](http://jinja.pocoo.org/), the **context** is the data passed from a Python program to the Jinja template. The context data represents all of the information available to the template, and is the mechanism by which the invoice generator supplies all input data (including calculated subtotals and totals) to a [template](../input-data/templates.md). It can be useful to inspect or manipulate the context data when [writing templates](../overview/writing-templates.md) or when you need to specify arbitrary data that is associated with an invoice or quote itself rather than the payee or payer:

- You can use the `--dump-context` flag when generating an invoice or quote to print the context data (a Python [dictionary](https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries)) that the invoice generator passes to the selected template. This is particularly useful when writing or debugging templates.

- You can use the `--context` flag when generating an invoice or quote to specify custom context data that will be applied to the context dictionary before it is passed to the selected template. This flag can be specified multiple times to provide multiple dictionary keys. Any keys that are already present in the dictionary (including those created by the invoice generator itself) will be overridden by values subsequently specified via this flag.

An example of using both of these flags together is show below:

```bash
# Specifies custom context data and prints the resulting context dictionary
gen-invoice us them goods.csv 1234 \
	--dump-context \
	--context "key1='value1'" \
	--context "key2={'subkey':['item1','item2','item3']}"
```
