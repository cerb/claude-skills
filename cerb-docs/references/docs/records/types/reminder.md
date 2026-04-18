---
id: "docs-records-types-reminder"
title: "Reminder Records"
url: "https://cerb.ai/docs/records/types/reminder/"
summary: "This page provides detailed information about Reminder Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `name`, `remind_at`, and `worker_id`, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also describes the search query fields that can be used to filter reminders, such as `closed`, `name`, and `worker`, and lists the worklist columns available for displaying reminder data, including custom fields and status indicators like `is_closed` and `remind_at`. This comprehensive guide is essential for managing and integrating reminder functionalities within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Reminder |
| **Name (plural):** | Reminders |
| **Alias (uri):** | reminder |
| **Identifier (ID):** | cerberusweb.contexts.reminder |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `is_closed` | boolean | Has this reminder elapsed? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this reminder |
| **x** | **`remind_at`** | timestamp | The date/time of the reminder |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| **x** | **`worker_id`** | number | The ID of the worker receiving the reminder |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `is_closed` | boolean | Is Closed |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `remind_at` | date | Remind At |
| `updated_at` | date | Updated |
| `worker_` | record | Worker |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in reminder search queries:

| Field | Type | Description |
| --- | --- | --- |
| `closed:` | boolean | Is Closed |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `remindAt:` | date | Remind At |
| `updated:` | date | Updated |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on reminder worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `r_id` | Id |
| `r_is_closed` | Is Closed |
| `r_name` | Name |
| `r_remind_at` | Remind At |
| `r_updated_at` | Updated |
| `r_worker_id` | Worker |

\< Record Types

