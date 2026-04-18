---
id: "docs-automations-triggers-behavior-action"
title: "behavior.action"
url: "https://cerb.ai/docs/automations/triggers/behavior.action/"
summary: "This page provides information on the **behavior.action** automations in Cerb, which are executed from legacy bot behaviors. It explains the use of event handler KATA to trigger the first enabled automation. The page details the structure of inputs and outputs for these automations, including how the automation dictionary is initialized with custom input values and how the function returns key/value pairs to the caller, with the possibility of nested keys for returning dictionaries."
tags: ["docs", "docs-automations"]
---
**behavior.action** automations are executed from legacy bot behaviors.

This trigger uses event handler KATA, and the first enabled automation is executed.

- Inputs
- Outputs
  - return:

# Inputs

The automation dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `inputs` | dictionary | Custom input values from the caller |

# Outputs

## return:

When the function concludes in the `return` state, it returns any number of key/value pairs to the caller. Keys may be nested to return dictionaries.

```
return: key1: value1 key2: value2 ...
```
