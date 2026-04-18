---
id: "docs-records-types-timeentry"
title: "Time Tracking Records"
url: "https://cerb.ai/docs/records/types/time_entry/"
summary: "This page provides detailed information about time tracking records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for managing time tracking entries, such as activity ID, log date, and worker ID. The page also describes dictionary placeholders used in automations and API responses, offering a range of fields like record type, log date, and time spent. Additionally, it covers search query fields that facilitate filtering time tracking data based on various criteria, such as activity, comments, and worker details. Lastly, it lists the worklist columns available for displaying time tracking information, including custom fields, activity, log date, and time spent. This comprehensive guide is crucial for users looking to effectively manage and query time tracking data within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Time Tracking Entry |
| **Name (plural):** | Time Tracking Entries |
| **Alias (uri):** | time\_entry |
| **Identifier (ID):** | cerberusweb.contexts.timetracking |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `activity_id` | number | The ID of the activity for the work |
| &nbsp; | `is_closed` | boolean | Is this time entry archived? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `log_date` | timestamp | The date/time of the work |
| **x** | **`mins`** | number | The number of minutes worked (alternative to `secs`) |
| **x** | **`secs`** | number | The number of seconds worked (alternative to `mins`) |
| **x** | **`worker_id`** | number | The ID of the worker who completed the work |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `is_closed` | boolean | Is Closed |
| `log_date` | date | Log Date |
| `mins` | minutes | Time Spent |
| `record_url` | text | Record Url |
| `summary` | text | Summary |
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

These filters are available in time tracking search queries:

| Field | Type | Description |
| --- | --- | --- |
| `activity.id:` | chooser | Activity |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Log Date |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isClosed:` | boolean | Is Closed |
| `links:` | links | Record Links |
| `timeSpent:` | number | Time Spent |
| `watchers:` | record | Watchers |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on time tracking worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `tt_activity_id` | Activity |
| `tt_is_closed` | Is Closed |
| `tt_log_date` | Log Date |
| `tt_time_actual_mins` | Time Spent |
| `tt_time_actual_secs` | Time Spent |
| `tt_worker_id` | Worker |

\< Record Types

