# Payers


## Description

Payer information represents the details of the entity that is receiving an invoice or quote. Unlike [line item](./items.md) data, payer data is completely freeform and is passed unmodified to [templates](./templates.md) by the invoice generator. This means the information schema for payer data is prescribed entirely by the template, providing users with the freedom to incorporate any type of payer information they like when writing templates.

Unlike [payee](./payees.md) data, there are no special circumstances under which the invoice generator will inspect the contents of payer data and transform it.


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
			<td>YAML file</td>
		</tr>
		<tr>
			<td><a href="../interfaces/api.md">Python API</a></td>
			<td><a href="https://docs.python.org/3/glossary.html#term-mapping">Mapping</a>[<a href="https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str">str</a>, <a href="https://docs.python.org/3/library/typing.html#typing.Any">Any</a>]</td>
		</tr>
		<tr>
			<td><a href="../interfaces/microservice.md">gRPC Microservice</a></td>
			<td><em>(coming soon)</em></td>
		</tr>
	</tbody>
</table>


## Examples

**Note: the examples provided below follow the information schema prescribed by the default template that ships with the command-line interface for gen-invoice. Your own payer data may look very different if your template prescribes a different schema.**

Example YAML file for use with the command-line interface:

```yaml
name: XYZ Widget Company
address:
  - 1 Widget Road
  - Widgetville
  - WID 9999

due: Within 30 days of receipt
```

Example data for use with the API:

```json
{
  "name": "XYZ Widget Company",
  "address": [
    "1 Widget Road",
    "Widgetville",
    "WID 9999"
  ],
  "due": "Within 30 days of receipt"
}
```
