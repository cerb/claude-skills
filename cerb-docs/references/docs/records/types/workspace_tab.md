---
id: "docs-records-types-workspacetab"
title: "Workspace Tab Records"
url: "https://cerb.ai/docs/records/types/workspace_tab/"
summary: "This page provides detailed information about the structure and functionality of Workspace Tab records in Cerb. It outlines the fields available in the Records API, including required fields like `extension_id`, `name`, and `page_id`, as well as optional fields such as `links` and `params`. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a comprehensive list of fields and their types. Additionally, it covers search query fields that can be used to filter workspace tab searches, and lists the columns available in workspace tab worklists, such as custom fields, type, ID, name, order, and updated date. This information is crucial for developers and users who need to manage and interact with workspace tabs within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Workspace Tab |
| **Name (plural):** | Workspace Tabs |
| **Alias (uri):** | workspace\_tab |
| **Identifier (ID):** | cerberusweb.contexts.workspace.tab |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`extension_id`** | text | Workspace Tab Type |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this workspace tab |
| &nbsp; | `options_kata` | text | &nbsp; |
| **x** | **`page_id`** | number | The ID of the workspace page containing this tab |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `pos` | number | The position of this tab on the workspace page; `0` is first |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `extension_` | record | Type |
| `extension_id` | text | Extension Id |
| `id` | number | Id |
| `name` | text | Name |
| `order` | number | Order |
| `page_` | record | Page |
| `page_extension_` | record | Page Type |
| `page_owner_` | record | Page Owner |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `widgets` | records | Widgets |
| `widgets_data` | hashmap | Widgets Data |
| `worklists` | records | Worklists |

### Search Query Fields

These filters are available in workspace tab search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `page.id:` | chooser | Workspace Page |
| `pos:` | number | Order |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `workspace:` | record | Workspace |
| `workspace.id:` | chooser | Workspace Page |

### Worklist Columns

These columns are available on workspace tab worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `w_extension_id` | Type |
| `w_id` | Id |
| `w_name` | Name |
| `w_pos` | Order |
| `w_updated_at` | Updated |
| `w_workspace_page_id` | Workspace Page |

\< Record Types

