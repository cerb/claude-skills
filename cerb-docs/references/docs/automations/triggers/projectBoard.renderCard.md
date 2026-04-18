---
id: "docs-automations-triggers-projectboard-rendercard"
title: "projectBoard.renderCard"
url: "https://cerb.ai/docs/automations/triggers/projectBoard.renderCard/"
summary: "This page provides detailed information about the 'projectBoard.renderCard' automations in Cerb, which are triggered when a card is displayed on a project board. It explains the use of event handler KATA, where the first enabled automation is executed based on criteria such as the record type of the card. The page outlines the inputs required for the automation, including details about the project board, card record, custom input values, and the active worker. It also describes the output, which is a sheet schema used to display the card's layout."
tags: ["docs", "docs-automations"]
---
**projectBoard.renderCard** automations are triggered when a card is displayed on a project board.

This trigger uses event handler KATA, and the first enabled automation is executed.

For instance, the match can be based on the record type of the card. The output is sheet KATA describing the card's layout.

- Inputs
- Outputs
  - return:

# Inputs

The automation dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `board_*` | record | The project board. Supports key expansion. |
| `card_*` | record | The card record. Supports key expansion. |
| `inputs` | dictionary | Custom input values from the caller |
| `worker_*` | record | The active worker |

# Outputs

## return:

| Key | Type | Notes |
| --- | --- | --- |
| `sheet` | string | A sheet schema to display for the card |

