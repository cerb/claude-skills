---
id: "docs-automations-commands-record-update"
title: "Automations: record.update"
url: "https://cerb.ai/docs/automations/commands/record.update/"
summary: "This page provides detailed information on the 'record.update' command in Cerb automations, which is used to update existing records with specified fields. It outlines the syntax and parameters required for the command, including inputs such as record type, record ID, and fields to update. The page also explains optional parameters like disabling events for modified records and handling different scenarios through on_simulate, on_success, and on_error commands. The output of the command is a dictionary that reflects the updated record, and error handling is addressed with a structured error message output."
tags: ["docs", "docs-automations"]
---
The **record.update:** command updates an existing record with the given fields.

```
start: record.update: output: updated_record inputs: record_type: task record_id: 123 # See: https://cerb.ai/docs/records/types/task/#records-api
        fields: importance: 90
```

- Syntax
  - inputs:
  - output:
  - on\_simulate:
  - on\_success:
  - on\_error:

# Syntax

## inputs:

| Key | &nbsp; |
| --- | --- |
| `record_type:` | The record type to update. |
| `record_id:` | The ID of the given record type to update. |
| `fields:` | The fields to set based on the record type. |
| `disable_events@bool:` | Avoid triggering events for modified records. |

## output:

Save the record dictionary to this placeholder.

## on\_simulate:

The commands to run during simulation instead of updating the record.

If omitted, the record is updated during simulation.

## on\_success:

The commands to run on success.

The `output:` placeholder is a dictionary based on the record type.

## on\_error:

The commands to run on failure. If omitted, the automation exits in the `error` state.

The `output:` placeholder receives a dictionary with these keys:

| Key | &nbsp; |
| --- | --- |
| `error` | The error message. |

