---
id: "docs-records-types-savedsearch"
title: "Saved Search Records"
url: "https://cerb.ai/docs/records/types/saved_search/"
summary: "This page provides detailed information about Saved Search records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as context, name, owner, and query, and explains how these fields can be utilized in packages. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive list of fields and their types. Additionally, it covers search query fields that can be used to filter saved searches and lists the worklist columns available for displaying saved search data. This information is crucial for users looking to manage and utilize saved searches effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Saved Search |
| **Name (plural):** | Saved Searches |
| **Alias (uri):** | saved\_search |
| **Identifier (ID):** | cerberusweb.contexts.context.saved.search |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`context`** | context | The record type of this search query; e.g. `ticket` |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this saved search |
| **x** | **`owner__context`** | context | The record type of this saved search's owner: `app`, `role`, `group`, or `worker` |
| &nbsp; | `owner_id` | number | The ID of this saved search's owner |
| **x** | **`query`** | text | The search query; e.g. `status:o` |
| &nbsp; | `tag` | text | A human-friendly nickname for this search (e.g. `open_tickets`) |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `context` | text | Type |
| `id` | number | Id |
| `name` | text | Name |
| `owner_` | record | Owner |
| `query` | text | Query |
| `record_url` | text | Record Url |
| `tag` | text | Tag |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in saved search search queries:

| Field | Type | Description |
| --- | --- | --- |
| `context:` | text | Record Type |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `name:` | text | Name |
| `query:` | text | Query |
| `tag:` | text | Tag |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on saved search worklists:

| Column | Description |
| --- | --- |
| `c_context` | Record Type |
| `c_id` | Id |
| `c_name` | Name |
| `c_query` | Query |
| `c_tag` | Tag |
| `c_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

