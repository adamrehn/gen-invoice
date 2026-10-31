# Templates


## Description

Templates are the core mechanism by which users can customise the generation of invoices or quotes. After processing all other input data and calculating subtotals and totals, the invoice generator passes all data to the user's selected template for formatting. Templates control how this information is presented and acted upon, using powerful features of the [Jinja template engine](http://jinja.pocoo.org/) including loops and conditional statements.

Although [line item](./items.md) data must follow a predetermined information schema, all other input data adheres to whatever schema is prescribed by the selected template. This provides users with the flexibility to incorporate any arbitrary information of their choosing when generating invoices and quotes.

Templates can opt to allow visual customisation via [stylesheets](./stylesheets.md) by including the `{{ css }}` template tag. This allows users to create any number of different visual themes that are compatible with a single template, or with a set of conventions that one or more templates adhere to. If users do not want to make use of this functionality then they can simply omit the `{{ css }}` template tag and embed CSS code directly in templates.


**For a full guide on writing templates, see the [Writing templates](../overview/writing-templates.md) page.**


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
			<td>HTML file</td>
		</tr>
		<tr>
			<td><a href="../interfaces/api.md">Python API</a></td>
			<td><a href="https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str">str</a> (string containing HTML code)</td>
		</tr>
		<tr>
			<td><a href="../interfaces/microservice.md">gRPC Microservice</a></td>
			<td><em>(coming soon)</em></td>
		</tr>
	</tbody>
</table>


## Examples

You can find the default template that ships with the command-line interface for gen-invoice here: <https://github.com/adamrehn/gen-invoice/blob/master/gen_invoice/defaults/default.html>

The default template is designed to be as generic and flexible as possible, serving as a potential basis for other templates. The default template is also designed for visual customisation via [stylesheets](./stylesheets.md), including the default stylesheet that ships with the command-line interface for gen-invoice.
