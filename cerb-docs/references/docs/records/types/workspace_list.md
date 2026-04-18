---
id: "docs-records-types-workspacelist"
title: "Workspace Worklist Records"
url: "https://cerb.ai/docs/records/types/workspace_list/"
summary: "This page provides detailed information about Workspace Worklist Records in Cerb, including their structure and functionality. It outlines the fields available in the Records API, such as context, name, and tab ID, and describes how these fields are used in JSON-encoded objects for managing workspace worklists. The page also explains the use of dictionary placeholders for automations, snippets, and API responses, offering a comprehensive list of fields like columns, context, and options. Additionally, it covers search query fields that can be used to filter workspace worklists, including fieldset, id, and name. Lastly, it details the available worklist columns, which include custom fields, type, id, name, and updated date, providing a robust framework for organizing and accessing workspace worklist data within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Workspace Worklist |
| **Name (plural):** | Workspace Worklists |
| **Alias (uri):** | workspace\_list |
| **Identifier (ID):** | cerberusweb.contexts.workspace.list |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `columns` | object | JSON-encoded key/value array of column names |
| **x** | **`context`** | context | The record type of the worklist |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this workspace worklist |
| &nbsp; | `options` | object | JSON-encoded key/value object |
| &nbsp; | `params_required_query` | text | The search query for required filters |
| &nbsp; | `pos` | number | The order of the worklist on the workspace tab; `0` is first |
| &nbsp; | `render_limit` | number | The number of records per page |
| **x** | **`tab_id`** | number | The ID of the workspace tab containing this worklist |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `columns` | object | Columns |
| `context` | text | Context |
| `id` | number | Id |
| `name` | text | Name |
| `options` | object | Options |
| `params` | object | Params |
| `pos` | number | Order |
| `record_url` | text | Record Url |
| `render_limit` | number | Render Limit |
| `render_sort` | object | Sort |
| `render_subtotals` | text | Subtotals |
| `tab_` | record | Tab |
| `tab_extension_` | record | Tab Type |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in workspace worklist search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `tab:` | record | Tab |
| `tab.id:` | chooser | Workspace Tab |
| `tab.pos:` | number | Order |
| `type:` | text | Type |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on workspace worklist worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `w_context` | Type |
| `w_id` | Id |
| `w_name` | Name |
| `w_updated_at` | Updated |
| `w_workspace_tab_id` | Workspace Tab |
| `w_workspace_tab_pos` | Order |

\< Record Types

