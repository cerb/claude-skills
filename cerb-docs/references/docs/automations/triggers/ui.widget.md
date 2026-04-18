---
id: "docs-automations-triggers-ui-widget"
title: "ui.widget"
url: "https://cerb.ai/docs/automations/triggers/ui.widget/"
summary: "This page provides information on the 'ui.widget' automations in Cerb, which enable custom output for card, profile, or workspace widgets, replacing the deprecated bot behavior-based widgets. It details the use of event handler KATA for triggering automations, with the first enabled automation being executed. The page outlines the structure of the automation dictionary, including inputs such as custom input values, current record dictionaries, widget records, and worker records. It also describes the expected output, specifically the HTML to be rendered for the widget."
tags: ["docs", "docs-automations"]
---
**ui.widget** automations allow custom output to be implemented for card, profile, or workspace widgets. This replaces bot behavior-based widgets, which are now deprecated.

This trigger uses event handler KATA, and the first enabled automation is executed.

- Inputs
- Outputs
  - return:

# Inputs

The automation dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `inputs` | dictionary | Custom input values from the caller |
| `record_*` | record | The current record dictionary (supports key expansion). Only available on card and profile widgets. |
| `widget_*` | record | The card, profile, or workspace widget record (supports key expansion) |
| `worker_*` | record | The current worker record (supports key expansion) |

# Outputs

## return:

| Key | Type | Notes |
| --- | --- | --- |
| `html` | text | The HTML to render for the widget |

