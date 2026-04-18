---
id: "docs-records-types-behavior"
title: "Behavior Records"
url: "https://cerb.ai/docs/records/types/behavior/"
summary: "This page provides detailed information about behavior records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as bot ID, event point, and priority, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also describes the search query fields that can be used to filter behaviors, such as by bot, event, and priority, and lists the columns available in behavior worklists for organizing and displaying behavior data. The document serves as a comprehensive guide for managing and interacting with behavior records in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Behavior |
| **Name (plural):** | Behaviors |
| **Alias (uri):** | behavior |
| **Identifier (ID):** | cerberusweb.contexts.behavior |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`bot_id`** | number | Bot |
| **x** | **`event_point`** | text | The event of the behavior |
| &nbsp; | `is_disabled` | boolean | Is this behavior disabled? |
| &nbsp; | `is_private` | boolean | Is this behavior only visible to the parent bot? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The behavior's name |
| &nbsp; | `priority` | number | Any positive number; `0` is highest priority |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `uri` | text | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `bot_` | record | Bot |
| `bot_owner_` | record | Bot Owner |
| `event_point` | text | Event |
| `event_point_name` | text | Event |
| `id` | number | Id |
| `is_disabled` | boolean | Is Disabled |
| `is_private` | boolean | Is Private |
| `name` | text | Name |
| `priority` | number | Priority |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |
| `uri` | text | Uri |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in behavior search queries:

| Field | Type | Description |
| --- | --- | --- |
| `bot:` | record | Bot |
| `bot.id:` | chooser | Bot |
| `disabled:` | boolean | Is Disabled |
| `event:` | text | Event |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Title |
| `priority:` | number | Priority |
| `private:` | boolean | Is Private |
| `updated:` | date | Updated |
| `uri:` | text | Uri |
| `usableBy.bot:` | chooser | Usableby Bot |

### Worklist Columns

These columns are available on behavior worklists:

| Column | Description |
| --- | --- |
| `*_has_fieldset` | Fieldset |
| `*_workers` | Watchers |
| `cf_<id>` | Custom Field |
| `t_bot_id` | Bot |
| `t_event_point` | Event |
| `t_id` | Id |
| `t_is_disabled` | Is Disabled |
| `t_is_private` | Is Private |
| `t_priority` | Priority |
| `t_title` | Title |
| `t_updated_at` | Updated |
| `t_uri` | Uri |

\< Record Types

