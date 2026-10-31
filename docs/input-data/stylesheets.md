# Stylesheets


## Description

Stylesheets provide a way of customising the appearance of invoices or quotes when they are displayed in a web browser, or rendered to PDF. Because [templates](./templates.md) can specify any arbitrary HTML structure that the user desires, stylesheets will typically be designed for compatibility with a specific template or a set of conventions that one or more templates adhere to.

It is worth noting that templates may opt to ignore stylesheets altogether by not including the `{{ css }}` template tag. If you are encountering issues whereby the CSS from a stylesheet is not being honoured, be sure to check that the template you are using actually includes the stylesheet CSS in its output.


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
			<td>CSS file</td>
		</tr>
		<tr>
			<td><a href="../interfaces/api.md">Python API</a></td>
			<td><a href="https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str">str</a> (string containing CSS code)</td>
		</tr>
		<tr>
			<td><a href="../interfaces/microservice.md">gRPC Microservice</a></td>
			<td><em>(coming soon)</em></td>
		</tr>
	</tbody>
</table>


## Examples

You can find the default stylesheet that ships with the command-line interface for gen-invoice here: <https://github.com/adamrehn/gen-invoice/blob/master/gen_invoice/defaults/default.css>

The default stylesheet is designed to be compatible with the default template that ships with the command-line interface for gen-invoice.
