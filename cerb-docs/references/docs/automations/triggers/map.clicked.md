---
id: "docs-automations-triggers-map-clicked"
title: "map.clicked"
url: "https://cerb.ai/docs/automations/triggers/map.clicked/"
summary: "This page provides detailed information about the 'map.clicked' automations in Cerb, which are activated when users click on regions or points within a map widget. It outlines the structure of the automation dictionary, including key inputs such as the type of feature clicked, its properties, custom input values, and details about the widget and active worker. The page also describes the expected output, specifically the 'sheet' key, which determines the schema to display based on the clicked feature's properties."
tags: ["docs", "docs-automations"]
---
**map.clicked** automations are triggered by clicks on map widget regions and points.

- Inputs
- Outputs
  - return:

# Inputs

The automation dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `feature_type` | string | `region` or `point` |
| `feature_properties` | dictionary | The key/value properties of the clicked feature |
| `inputs` | dictionary | Custom input values from the caller |
| `widget_*` | record | A card, profile, or workspace widget. Supports key expansion. |
| `worker_*` | record | The active worker |

# Outputs

## return:

| Key | Type | Notes |
| --- | --- | --- |
| `sheet` | string | A sheet schema to display for the clicked feature based on the properties dictionary |

