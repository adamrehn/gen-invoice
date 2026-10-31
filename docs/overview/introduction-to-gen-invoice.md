# Introduction to gen-invoice


## Overview

The gen-invoice Python package provides a flexible, template-driven system for generating invoices and quotes in both HTML and PDF format. Great care has been taken to ensure users have complete control over the generated output, by delegating all formatting decisions to templates and minimising the use of predetermined information schemas to the greatest extent feasible.

Invoice generation can be invoked either directly by end users or programmatically by other software components as part of a larger system. The package is designed to cater primarily to individuals and small businesses in the technology industry who would like to automate invoice generation independently of other financial management software or systems.

Template functionality is provided by the [Jinja template engine](http://jinja.pocoo.org/) and PDF generation functionality is provided by [electron-pdf](https://www.npmjs.com/package/electron-pdf) v4.0.6 or newer when available.


## Writing templates

Irrespective of the interface that you will use to generate invoices and quotes, you should first familiarise yourself with [how to write invoice templates](./writing-templates.md).


## Available interfaces

There are a number of different interfaces available for gen-invoice that cater to various usage workflows:

- [**Python API**](../interfaces/api.md): generate invoices and quotes programmatically from Python code
- [**Command-line interface**](../interfaces/cli.md): generate invoices and quotes from shell scripts or an interactive terminal
- [**gRPC Microservice**](../interfaces/microservice.md): generate invoices and quotes programmatically from other microservices


## Links

- [gen-invoice GitHub repository](https://github.com/adamrehn/gen-invoice)
- [gen-invoice package on PyPI](https://pypi.org/project/gen-invoice/)
