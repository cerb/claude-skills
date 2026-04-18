---
id: "docs-automations-triggers-interaction-worker-elements-chooser"
title: "Chooser - Interaction Form Element"
url: "https://cerb.ai/docs/automations/triggers/interaction.worker/elements/chooser/"
summary: "This page introduces the 'chooser' interaction form element added in Cerb 11.0, which is used in web forms to display a search popup for selecting records. It provides a code example demonstrating how to implement a chooser element, including options for setting a label, specifying the record type, applying a search query for filtering, allowing multiple selections, and marking the input as required. The page details the syntax for configuring these options, enabling users to customize the chooser element according to their needs."
tags: ["docs", "docs-automations"]
---
(Added in 11.0)

In interaction web forms, a **chooser** element displays a search popup for selecting records.

```
start: await: form: title: Chooser elements: chooser/prompt_chooser: label: Choose records: record_type: worker query@text: isDisabled:n multiple@bool: yes required@bool: yes await/response: form: elements: say: content@text: You selected record IDs: {{ prompt_chooser|join(', ') }}
```

 

# Syntax

### label:

The optional label to display above the form element.

### record\_type:

The record type to choose from.

### query:

The optional search query for filtering the search worklist.

### hidden:

This form element can be conditionally hidden.

```
hidden@bool: {{ not worker_is_superuser }}
```

### multiple:

If `yes` then multiple records may be selected at once. The default is `no` for single selection.

### required@bool:

If user input is required on this element use a value of `yes`. Otherwise, omit.

