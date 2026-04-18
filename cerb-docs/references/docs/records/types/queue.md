---
id: "docs-records-types-queue"
title: "Queue Records"
url: "https://cerb.ai/docs/records/types/queue/"
summary: "This page provides detailed information about Queue Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as creation and update timestamps, links, and the queue name. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a range of fields like context, label, and record URL. Additionally, it covers search query fields that can be used to filter queue records based on criteria like creation date, fieldset, and watchers. Lastly, it lists the worklist columns available for displaying queue records, including custom fields and standard attributes like ID, name, and timestamps."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Queue |
| **Name (plural):** | Queues |
| **Alias (uri):** | queue |
| **Identifier (ID):** | cerb.contexts.queue |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this queue |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
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

These filters are available in queue search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on queue worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `q_created_at` | Created |
| `q_id` | Id |
| `q_name` | Name |
| `q_updated_at` | Updated |

\< Record Types

