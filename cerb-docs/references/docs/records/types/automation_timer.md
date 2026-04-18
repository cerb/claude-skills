---
id: "docs-records-types-automationtimer"
title: "Automation Timer Records"
url: "https://cerb.ai/docs/records/types/automation_timer/"
summary: "This page provides detailed information about Automation Timer records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and attributes of Automation Timer records, such as creation and update timestamps, recurring patterns, and links. The page also describes how these records can be queried and displayed in worklists, offering a comprehensive guide for managing and utilizing Automation Timers within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Automation Timer |
| **Name (plural):** | Automation Timers |
| **Alias (uri):** | automation\_timer |
| **Identifier (ID):** | cerb.contexts.automation.timer |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `automations_kata` | text | &nbsp; |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `is_disabled` | boolean | &nbsp; |
| &nbsp; | `is_recurring` | boolean | &nbsp; |
| &nbsp; | `last_ran_at` | timestamp | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this automation timer |
| &nbsp; | `next_run_at` | timestamp | &nbsp; |
| &nbsp; | `recurring_patterns` | text | &nbsp; |
| &nbsp; | `recurring_timezone` | text | &nbsp; |
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
| `is_disabled` | boolean | Disabled |
| `is_recurring` | boolean | Is Recurring |
| `last_ran_at` | date | Last Ran At |
| `name` | text | Name |
| `next_run_at` | date | Next Run At |
| `record_url` | text | Record Url |
| `recurring_patterns` | text | Recurring Patterns |
| `recurring_timezone` | text | Timezone |
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

These filters are available in automation timer search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isRecurring:` | boolean | Is Recurring |
| `lastRanAt:` | date | Last Ran At |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `nextRunAt:` | date | Next Run At |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on automation timer worklists:

| Column | Description |
| --- | --- |
| `a_created_at` | Created |
| `a_id` | Id |
| `a_is_disabled` | Disabled |
| `a_is_recurring` | Is Recurring |
| `a_last_ran_at` | Last Ran At |
| `a_name` | Name |
| `a_next_run_at` | Next Run At |
| `a_recurring_patterns` | Recurring Patterns |
| `a_recurring_timezone` | Timezone |
| `a_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

