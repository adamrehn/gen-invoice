# Python API

Generate invoices and quotes programmatically from Python code.


## Installation

To start using the gen-invoice Python API, first install the package via pip:

```bash
pip3 install gen-invoice
```

Once the package is installed you will be able to import the API from Python code like so:

```python
import gen_invoice
```

If you want to generate PDFs then you will also need to install [electron-pdf](https://www.npmjs.com/package/electron-pdf) v4.0.6 or newer:

```bash
npm install electron-pdf -g
```


## InvoiceGenerator class

Invoice generation functionality is exposed via the [InvoiceGenerator](https://github.com/adamrehn/gen-invoice/blob/master/gen_invoice/InvoiceGenerator.py) class, which provides two public methods. These methods are documented below.

### generate() Method

Generates an invoice/quote with the specified options.

Arguments:

- **outfile**: *(string)* the path to the output HTML file.
- **number**: *(string)* the invoice number.
- **items**: *(list)* the list of [line items](../input-data/items.md).
- **payee**: *(dictionary)* the [payee details](../input-data/payees.md).
- **payer**: *(dictionary)* the [payer details](../input-data/payers.md).
- **template**: *(string)* the Jinja [template HTML](../input-data/templates.md).
- **stylesheet**: *(string)* the [stylesheet CSS](../input-data/stylesheets.md).
- **tax**: *(float)* the tax (GST, VAT, etc.) to apply to the total of all line items. Defaults to 0.0.
- **is_international**: *(boolean)* specifies whether the invoice/quote is for an international recipient. Defaults to False.
- **is_quote**: *(boolean)* specifies whether we are generating a quote rather than an invoice. Defaults to False.
- **expiry**: *(string)* if we are generating a quote, specifies the expiry date of the quote. Defaults to `None`.
- **purchase_order**: *(string)* if we are generating an invoice, specifies the purchase order number that the invoice relates to. Defaults to `None`.
- **context_overrides**: *(dictionary)* custom overrides to apply to our context data prior to passing it to the Jinja template. Defaults to `None`.

Returns:

- *(dictionary)* the context data that was passed to the Jinja template.

Throws:

- May throw system-generated errors in the event of file permission issues or receiving malformed line item data. May also throw Jinja-generated errors in the event of receiving malformed template HTML.

### render() Method

Renders an invoice/quote HTML file to a PDF using [electron-pdf](https://www.npmjs.com/package/electron-pdf).

Arguments:

- **html**: *(string)* the path to the input HTML file.
- **pdf**: *(string)* the path to the output PDF file.

Returns:

- *(boolean)* True if the PDF was rendered successfully, or False if electron-pdf v4.0.6 or newer could not be found.

Throws:

- `RuntimeError` if the PDF could not be rendered successfully, or `CalledProcessError` if the electron-pdf subprocess returned a non-zero exit code. May also throw other system-generated errors in the event of file permission issues.


## Usage example

Example code for using these methods is shown below:

```python
#!/usr/bin/env python3
from gen_invoice import InvoiceGenerator, Utility

# Our output file paths
OUTFILE_HTML = "/path/to/output.html"
OUTFILE_PDF = "/path/to/output.pdf"

# Load our template and stylesheet data from file
template = Utility.read_file("template.html")
stylesheet = Utility.read_file("stylesheet.css")

# Generate our invoice
generator = InvoiceGenerator()
generator.generate(
  
  # Our output HTML file
  outfile = OUTFILE_HTML,
  
  # Our invoice number
  number = "INV001",
  
  # Our line items
  items = [
    {
      "Section": "Materials",
      "Item": "Widget A",
      "Quantity": "20",
      "Units": "pcs",
      "Price": "12.99"
    }
  ],
  
  # Our payee details
  payee = {
    "name": "XYZ Widget Company",
    "identifier": "123456789",
    "email": "domestic@example.com",
    "address": [
      "1 Widget Road",
      "Widgetville",
      "WID 9999"
    ],
    "bank": {
      "holder": "XYZ Widget Company",
      "bank": "Acme Banking Co",
      "code": "123-456",
      "account": "192837465"
    }
  },
  
  # Our payer details
  payer = {
    "name": "XYZ Widget Company",
    "address": [
      "1 Widget Road",
      "Widgetville",
      "WID 9999"
    ],
    "due": "Within 30 days of receipt"
  },
  
  # Our template and stylesheet
  template = template,
  stylesheet = stylesheet,
  
  # No tax
  tax = 0.0,
  
  # Generate a domestic invoice rather than an international one
  is_international = False,
  
  # Generate an invoice rather than a quote
  is_quote = False
)

# Render the invoice HTML to a PDF file using electron-pdf
generator.render(OUTFILE_HTML, OUTFILE_PDF)
```
