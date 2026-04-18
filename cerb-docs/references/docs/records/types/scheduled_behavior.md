---
id: "docs-records-types-scheduledbehavior"
title: "Behavior Scheduled Records"
url: "https://cerb.ai/docs/records/types/scheduled_behavior/"
summary: "This page provides detailed information about Behavior Scheduled Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for scheduling behaviors, such as `behavior_id`, `run_date`, `target__context`, and `target_id`. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `_context`, `_label`, `behavior_`, and `run_date`. Additionally, it covers search query fields that facilitate filtering behavior schedules, with options like `behavior:`, `bot:`, and `runDate:`. Lastly, it lists the worklist columns available for behavior scheduled worklists, which include columns like `*_target`, `b_behavior_bot_id`, and `c_run_date`, providing a comprehensive guide for managing and utilizing behavior schedules in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Behavior Schedule |
| **Name (plural):** | Behavior Schedules |
| **Alias (uri):** | scheduled\_behavior |
| **Identifier (ID):** | cerberusweb.contexts.behavior.scheduled |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`behavior_id`** | number | The ID of the behavior to be scheduled |
| **x** | **`run_date`** | timestamp | The date/time to run the scheduled behavior |
| **x** | **`target__context`** | context | The record type of the target record to run the behavior against |
| **x** | **`target_id`** | number | The ID of the target record |
| &nbsp; | `variables` | object | JSON-encoded key/value object |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `behavior_` | record | Behavior |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `run_date` | date | Run Date |
| `target_` | record | Target |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in behavior scheduled search queries:

| Field | Type | Description |
| --- | --- | --- |
| `behavior:` | record | Behavior |
| `behavior.id:` | chooser | Behavior |
| `bot:` | record | Bot |
| `bot.id:` | chooser | Bot |
| `id:` | number | Id |
| `on:` | text | On |
| `on.<type>:` | record | On |
| `runDate:` | date | Run Date |

### Worklist Columns

These columns are available on behavior scheduled worklists:

| Column | Description |
| --- | --- |
| `*_target` | On |
| `b_behavior_bot_id` | Bot |
| `b_behavior_name` | Name |
| `c_id` | Id |
| `c_repeat_json` | Repeat |
| `c_run_date` | Run Date |
| `cf_<id>` | Custom Field |

\< Record Types

