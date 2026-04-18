---
id: "docs-automations-triggers-projectboard-cardaction"
title: "projectBoard.cardAction"
url: "https://cerb.ai/docs/automations/triggers/projectBoard.cardAction/"
summary: "This page provides detailed information about the 'projectBoard.cardAction' automations in Cerb, which are triggered when a project board card moves to a new column, either manually or automatically. It explains the use of event handler KATA for executing all enabled automations and outlines the initial values in the automation dictionary, including keys for the project board, card record, column, custom input values, and the active worker. The page specifies that there are no outputs for this automation."
tags: ["docs", "docs-automations"]
---
**projectBoard.cardAction** automations are triggered when a project board card enters a new board column, either through the UI or procedurally.

This trigger uses event handler KATA, and all enabled automations are executed.

- Inputs
- Outputs

# Inputs

The automation dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `board_*` | record | The project board. Supports key expansion. |
| `card_*` | record | The card record. Supports key expansion. |
| `column_*` | record | The project board column. Supports key expansion. |
| `inputs` | dictionary | Custom input values from the caller |
| `worker_*` | record | The active worker |

# Outputs

(none)

