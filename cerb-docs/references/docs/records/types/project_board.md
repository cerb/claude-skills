---
id: "docs-records-types-projectboard"
title: "Project Board Records"
url: "https://cerb.ai/docs/records/types/project_board/"
summary: "This page provides detailed information about the Project Board records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and types of data available for Project Boards, such as the required and optional fields in the Records API, which include attributes like `name`, `owner__context`, and `updated_at`. The page also describes the dictionary placeholders used in automations and API responses, offering a range of fields from basic identifiers to custom fields and links. Additionally, it specifies the search query filters available for Project Boards, allowing users to search by attributes like `name`, `id`, and `updated`. Lastly, it lists the columns available in worklists for Project Boards, which help in organizing and displaying data efficiently."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Project Board |
| **Name (plural):** | Project Boards |
| **Alias (uri):** | project\_board |
| **Identifier (ID):** | cerberusweb.contexts.project.board |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `cards_kata` | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this project board |
| &nbsp; | `owner__context` | context | The record type of this project board's owner: `app`, `role`, `group`, or `worker` |
| &nbsp; | `owner_id` | number | The ID of this project board's owner |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `cards_kata` | text | Common.cards\_Kata |
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

These filters are available in project board search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on project board worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `p_id` | Id |
| `p_name` | Name |
| `p_updated_at` | Updated |

\< Record Types

