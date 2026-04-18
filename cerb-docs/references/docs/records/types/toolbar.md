---
id: "docs-records-types-toolbar"
title: "Toolbar Records"
url: "https://cerb.ai/docs/records/types/toolbar/"
summary: "This page provides detailed information about toolbar records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and requirements for toolbar records, such as mandatory fields like `extension_id` and `name`, and optional fields like `links` and `description`. The page also describes how these records can be utilized in automations, snippets, and API responses through dictionary placeholders. Additionally, it lists the available filters for toolbar search queries and the columns that can be displayed in toolbar worklists, offering a comprehensive guide for managing and interacting with toolbar records in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Toolbar |
| **Name (plural):** | Toolbars |
| **Alias (uri):** | toolbar |
| **Identifier (ID):** | cerb.contexts.toolbar |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `description` | text | &nbsp; |
| **x** | **`extension_id`** | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this toolbar |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `description` | text | Description |
| `extension_id` | text | Extension |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in toolbar search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `description:` | text | Description |
| `extension:` | text | Extension |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on toolbar worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `t_created_at` | Created |
| `t_description` | Description |
| `t_extension_id` | Extension |
| `t_id` | Id |
| `t_name` | Name |
| `t_updated_at` | Updated |

\< Record Types

