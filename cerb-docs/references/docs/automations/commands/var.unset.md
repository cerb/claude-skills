---
id: "docs-automations-commands-var-unset"
title: "Automations: var.unset"
url: "https://cerb.ai/docs/automations/commands/var.unset/"
summary: "This page provides detailed information on the 'var.unset' command used in Cerb automations to remove a placeholder using a specified key path. It includes an example demonstrating how to unset a phone number from a nested data structure. The page outlines the syntax for using 'var.unset,' including required inputs, optional outputs, and commands to execute during simulation, on success, and on error. It explains how to specify key paths, handle simulation scenarios, and manage success and error states, providing a comprehensive guide for users to effectively utilize this command in their automation workflows."
tags: ["docs", "docs-automations"]
---
The **var.unset:** command removes a placeholder using a key path.

```
start: set: person: name: first: Kina last: Halpue phone: +15551234321 var.unset: inputs: key: person:phone return: person@key: person
```

Result:

```
person: name: first: Kina last: Halpue
```

- Syntax
  - inputs:
  - output:
  - on\_simulate:
  - on\_success:
  - on\_error:

# Syntax

## inputs:

| Key | Req'd | &nbsp; |
| --- | --- | --- |
| `key:` | **x** | One or more key paths to unset, delimited with colons (`:`). |

## output:

The optional placeholder to store the result.

## on\_simulate:

The commands to run during simulation instead of unsetting the value.

If omitted, the value is not unset during simulation.

## on\_success:

The commands to run on success.

The optional `output:` placeholder is set to `true` if the key was found, and `false` otherwise.

## on\_error:

The commands to run on failure. If omitted, the automation exits in the `error` state.

The `output:` placeholder receives a dictionary with these keys:

| Key | &nbsp; |
| --- | --- |
| `error` | The error message. |

