---
id: "docs-records-types-workspacewidget"
title: "Workspace Widget Records"
url: "https://cerb.ai/docs/records/types/workspace_widget/"
summary: "This page provides detailed information about Workspace Widget Records in Cerb, including their structure and usage within the system. It covers the fields available in the Records API, which are essential for defining and managing workspace widgets, such as `extension_id`, `label`, `tab_id`, and `updated_at`. The page also explains the Dictionary Placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `id`, `label`, and `zone`. Additionally, it outlines the Search Query Fields that can be used to filter workspace widget searches, including `id`, `name`, and `updated`. Lastly, it lists the Worklist Columns available for workspace widget worklists, providing options for displaying information like `w_label`, `w_pos`, and `w_zone`. This comprehensive guide is crucial for users looking to effectively utilize and customize workspace widgets within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Workspace Widget |
| **Name (plural):** | Workspace Widgets |
| **Alias (uri):** | workspace\_widget |
| **Identifier (ID):** | cerberusweb.contexts.workspace.widget |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`extension_id`** | text | Workspace Widget Type |
| **x** | **`label`** | text | The human-friendly name of the widget |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `options_kata` | text | &nbsp; |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `pos` | number | The position of the widget on the dashboard; `0` is first (top-right); rows before columns |
| **x** | **`tab_id`** | number | The ID of the workspace tab containing this widget |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `width_units` | number | `1` (25%), `2` (50%), `3` (75%), `4` (100%) |
| &nbsp; | `zone` | text | The name of the dashboard zone containing the widget; this varies by layout; generally `sidebar` and `content` |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `extension_id` | text | Type |
| `id` | number | Id |
| `label` | text | Label |
| `params` | object | Params |
| `pos` | text | Order |
| `tab_` | record | Tab |
| `tab_extension_` | record | Tab Type |
| `updated_at` | date | Updated |
| `width_units` | number | Width |
| `zone` | text | Zone |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `data` | hashmap | Data |
| `links` | links | Links |

### Search Query Fields

These filters are available in workspace widget search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Label |
| `tab:` | record | Tab |
| `tab.id:` | chooser | Workspace Tab |
| `tab.pos:` | number | Order |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `width:` | text | Width |
| `zone:` | text | Zone |

### Worklist Columns

These columns are available on workspace widget worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `w_extension_id` | Type |
| `w_id` | Id |
| `w_label` | Label |
| `w_pos` | Order |
| `w_updated_at` | Updated |
| `w_width_units` | Width |
| `w_workspace_tab_id` | Workspace Tab |
| `w_zone` | Zone |

\< Record Types

