---
id: "docs-records-types-workspacepage"
title: "Workspace Page Records"
url: "https://cerb.ai/docs/records/types/workspace_page/"
summary: "This page provides detailed information about Workspace Page records in Cerb, including their structure and usage within the system. It covers the Records API, which outlines the required and optional fields for Workspace Pages, such as `extension_id`, `name`, and `owner_id`. The page also explains Dictionary Placeholders used in automations, snippets, and API responses, offering a list of available fields and their descriptions. Additionally, it details the Search Query Fields that can be used to filter Workspace Page searches, such as `id`, `name`, and `owner`. Lastly, it describes the Worklist Columns available for displaying Workspace Page data, including columns for owner, custom fields, and update timestamps. This comprehensive guide is essential for developers and users looking to manage and interact with Workspace Pages in Cerb effectively."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Workspace Page |
| **Name (plural):** | Workspace Pages |
| **Alias (uri):** | workspace\_page |
| **Identifier (ID):** | cerberusweb.contexts.workspace.page |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`extension_id`** | text | Workspace Page Type |
| &nbsp; | `extension_params` | object | JSON-encoded key/value object |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this workspace page |
| **x** | **`owner__context`** | context | The record type of this workspace page's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this workspace page's owner |
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
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `tabs` | records | Tabs |
| `widgets` | records | Widgets |
| `worklists` | records | Worklists |

### Search Query Fields

These filters are available in workspace page search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner |
| `owner.bot:` | record | Owner |
| `owner.group:` | record | Owner |
| `owner.role:` | record | Owner |
| `owner.worker:` | record | Owner |
| `type:` | text | Type |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on workspace page worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `cf_<id>` | Custom Field |
| `w_extension_id` | Type |
| `w_name` | Name |
| `w_updated_at` | Updated |

\< Record Types

