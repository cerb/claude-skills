---
id: "docs-records-types-projectboardcolumn"
title: "Project Board Column Records"
url: "https://cerb.ai/docs/records/types/project_board_column/"
summary: "This page provides detailed information about the Project Board Column records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and types of data associated with project board columns, such as board IDs, card links, names, positions, and timestamps. The page also describes how these fields can be utilized in the Records API, automation dictionaries, and search queries, offering a comprehensive guide for managing and interacting with project board columns within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Project Board Column |
| **Name (plural):** | Project Board Columns |
| **Alias (uri):** | project\_board\_column |
| **Identifier (ID):** | cerberusweb.contexts.project.board.column |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`board_id`** | number | The project board containing this column |
| &nbsp; | `cards` | links | An array of record `type:id` tuples to add to this column |
| &nbsp; | `cards_kata` | text | &nbsp; |
| &nbsp; | `functions_kata` | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this project board column |
| &nbsp; | `pos` | number | (0-4294967296) |
| &nbsp; | `toolbar_kata` | text | &nbsp; |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `board_` | record | Project Board |
| `cards_kata` | text | Cards Kata |
| `functions_kata` | text | Functions Kata |
| `id` | number | Id |
| `name` | text | Name |
| `pos` | number | Order |
| `record_url` | text | Record Url |
| `toolbar_kata` | text | Toolbar Kata |
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

These filters are available in project board column search queries:

| Field | Type | Description |
| --- | --- | --- |
| `board:` | record | Board |
| `board.id:` | chooser | Project Board |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on project board column worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `p_board_id` | Project Board |
| `p_id` | Id |
| `p_name` | Name |
| `p_updated_at` | Updated |

\< Record Types

