---
id: "docs-automations-commands-record-search"
title: "Automations: record.search"
url: "https://cerb.ai/docs/automations/commands/record.search/"
summary: "This page provides detailed documentation on the `record.search` command used in Cerb automations. It explains how to configure the command to return record dictionaries based on a search query, specifying the syntax for inputs, outputs, and handling different events like simulation, success, and error. Key elements include defining the record type, constructing search queries with parameters, and using validation templates to manage errors. The page also outlines how to handle simulation scenarios and the structure of the output and error messages."
tags: ["docs", "docs-automations"]
---
The **record.search:** command returns record dictionaries from a search query.

```
start: record.search: inputs: record_type: ticket record_query: status:${status} record_query_params: status: o output: results
```

- Syntax
  - inputs:
    - validation@raw:

  - output:
  - on\_simulate:
  - on\_success:
  - on\_error:

# Syntax

## inputs:

| Key | &nbsp; |
| --- | --- |
| `record_type:` | The record type to search. |
| `record_query:` | The search query to match. Use `limit:1` to return a single dictionary rather than an array of dictionaries. |
| `record_query_params:` | Query parameters with untrusted user input as keys/values. Reference these as `${param}` in queries. |
| `validation@raw:` | An optional template to validate results. Any non-empty output triggers the `on_error:` event. |

### validation@raw:

A template with scripting syntax where any output is considered to be an error that triggers the `on_error:` event.

For instance, a `record.search:` with an `id:123 limit:1` query that fails the automation if the expected record is not found. This is a shortcut for adding an `on_success:outcome:if@bool:` for every lookup.

## output:

Save the search results as record dictionaries in this placeholder.

## on\_simulate:

The commands to run during simulation instead of searching records.

If omitted, records are searched during simulation.

## on\_success:

The commands to run on success.

The `output:` placeholder is an array of record dictionaries.

## on\_error:

The commands to run on failure. If omitted, the automation exits in the `error` state.

The `output:` placeholder receives a dictionary with these keys:

| Key | &nbsp; |
| --- | --- |
| `error` | The error message. |

