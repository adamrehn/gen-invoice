# Payees


## Description

Payee information represents the details of the entity that is issuing an invoice or quote. Unlike [line item](./items.md) data, payee data is completely freeform and is passed unmodified to [templates](./templates.md) by the invoice generator. This means the information schema for payee data is prescribed entirely by the template, providing users with the freedom to incorporate any type of payee information they like when writing templates.

There is one special case where the invoice generator will inspect the contents of payee data and transform it. If the payee data includes two top-level keys named `domestic` and `international` then the contents of the appropriate key for the current invoice type (domestic or international) will be passed to the template instead of the entire payee data. This functionality is provided as a convenience for users who commonly include different information about themselves depending on whether an invoice or quote is being issued to an overseas recipient (e.g. different company name for international trading, excluding the country from their address details in domestic communications, etc.)


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

**Note: the examples provided below follow the information schema prescribed by the default template that ships with the command-line interface for gen-invoice. Your own payee data may look very different if your template prescribes a different schema.**

Example YAML file for use with the command-line interface:

```yaml
domestic:
  
  name: XYZ Widget Company
  identifier: "123456789"
  email: domestic@example.com
  address:
    - 1 Widget Road
    - Widgetville
    - WID 9999
  
  bank:
    holder: XYZ Widget Company
    bank: Acme Banking Co
    code: 123-456
    account: "192837465"

international:
  
  name: XYZ Widget Company International
  identifier: "987654321"
  email: international@example.com
  address:
    - 123 Shellcorp Lane
    - Tax Haven City
    - Obscure Island
    - Atlantic Ocean
  
  bank:
    holder: XYZ Widget Company International
    bank: Ace Banking & Offshore Holding Co
    swift: ACEBTX2H
    code: 987-654
    account: "918273645"
```

Example data for use with the API:

```json
{
  "domestic":
  {
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
  "international":
  {
    "name": "XYZ Widget Company International",
    "identifier": "987654321",
    "email": "international@example.com",
    "address": [
      "123 Shellcorp Lane",
      "Tax Haven City",
      "Obscure Island",
      "Atlantic Ocean"
    ],
    "bank": {
      "holder": "XYZ Widget Company International",
      "bank": "Ace Banking & Offshore Holding Co",
      "swift": "ACEBTX2H",
      "code": "987-654",
      "account": "918273645"
    }
  }
}
```
