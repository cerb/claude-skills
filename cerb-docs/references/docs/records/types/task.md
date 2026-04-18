---
id: "docs-records-types-task"
title: "Task Records"
url: "https://cerb.ai/docs/records/types/task/"
summary: "This page provides detailed information about task records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as timestamps for creation, completion, and deadlines, as well as fields for task importance, ownership, and status. The page also describes dictionary placeholders for automations and API responses, offering a range of fields like task title, status, and owner. Additionally, it covers search query fields that allow filtering tasks based on various criteria, and it lists worklist columns that can be used to display task information in a structured format. This comprehensive guide is essential for users looking to manage and automate tasks effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Task |
| **Name (plural):** | Tasks |
| **Alias (uri):** | task |
| **Identifier (ID):** | cerberusweb.contexts.task |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `completed` | timestamp | The date/time this task was completed |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `due` | timestamp | The date/time of this task's deadline |
| &nbsp; | `fieldsets` | fieldsets | An array or comma-separated list of custom fieldset IDs. Prefix an ID with `-` to remove. |
| &nbsp; | `importance` | number | A number from `0` (least) to `100` (most) |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `owner_id` | number | The ID of the worker responsible for this task |
| &nbsp; | `reopen` | timestamp | If the status is `waiting`, the date/time to automatically change the status back to `open` |
| &nbsp; | `status` | text | `o` (open), `w` (waiting), `c` (closed); alternative to `status_id` |
| &nbsp; | `status_id` | number | `0` (open), `1` (closed), `2` (waiting); alternative to `status` |
| **x** | **`title`** | text | The name of this task |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `completed` | date | Completed Date |
| `created` | date | Created |
| `due` | date | Due Date |
| `id` | number | Id |
| `importance` | number | Importance |
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `reopen` | date | Reopen At |
| `status` | text | Status |
| `title` | text | Title |
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in task search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `completed:` | date | Completed Date |
| `created:` | date | Created |
| `due:` | date | Due Date |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `importance:` | number | Importance |
| `links:` | links | Record Links |
| `owner:` | record | Owner |
| `owner.id:` | chooser | Owner |
| `reopen:` | date | Reopen At |
| `status:` | virtual | Status |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on task worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `t_completed_date` | Completed Date |
| `t_created_at` | Created |
| `t_due_date` | Due Date |
| `t_importance` | Importance |
| `t_owner_id` | Owner |
| `t_reopen_at` | Reopen At |
| `t_status_id` | Status |
| `t_title` | Title |
| `t_updated_date` | Updated |

\< Record Types

