# Line Items


## Description

Line items represent the individual products or services whose prices are to be communicated to the recipient of the invoice or quote. Unlike freeform [payee](./payees.md) or [payer](./payers.md) data, line item data must follow a prescribed information schema in order to be processed correctly by the invoice generator. Each line item must contain the following fields:

- **Section:** *(optional)* specifies a named group to which the line item belongs. If not present then the item will be assigned to the default unnamed group. Subtotals will be calculated for all groups that are present in an invoice or quote.

- **Item:** *(required)* the description of the product or service that this line item represents.

- **Quantity:** *(required)* the quantity of the product or service that this line item represents.

- **Units:** *(optional)* specifies the numerical units in which the Quantity field is expressed (e.g. hours, pieces, etc.) Templates will commonly choose to suffix the Quantity value with the Units value when formatting line items.

- **Price:** *(required)* the price of each individual unit, which will be multiplied by the Quantity value to calculate the total cost for the line item.


## Data format

<table>
	<thead>
		<tr>
			<th>When using this interface:</th>
			<th>Use this data format:</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td><a href="../interfaces/cli.md">Command-line interface</a></td>
			<td>Comma-separated values (CSV) file</td>
		</tr>
		<tr>
			<td><a href="../interfaces/api.md">Python API</a></td>
			<td><a href="https://docs.python.org/3/glossary.html#term-sequence">Sequence</a>[<a href="https://docs.python.org/3/glossary.html#term-mapping">Mapping</a>[<a href="https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str">str</a>, <a href="https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str">str</a>]]</td>
		</tr>
		<tr>
			<td><a href="../interfaces/microservice.md">gRPC Microservice</a></td>
			<td><em>(coming soon)</em></td>
		</tr>
	</tbody>
</table>


## Examples

Example CSV file for use with the command-line interface:

```
Section,Item,Quantity,Units,Price
Materials,Widget A,20,pcs,12.99
Materials,Widget B,15,pcs,22.50
Labour,Assembly,5,hours,50.0
```

Example data for use with the API:

```json
[
  {
    "Section": "Materials",
    "Item": "Widget A",
    "Quantity": "20",
    "Units": "pcs",
    "Price": "12.99"
  },
  {
    "Section": "Materials",
    "Item": "Widget B",
    "Quantity": "15",
    "Units": "pcs",
    "Price": "22.50"
  },
  {
    "Section": "Labour",
    "Item": "Assembly",
    "Quantity": "5",
    "Units": "hours",
    "Price": "50.0"
  }
]
```
