---
id: "docs-records-types-calendarrecurringevent"
title: "Calendar Recurring Event Records"
url: "https://cerb.ai/docs/records/types/calendar_recurring_event/"
summary: "This page provides detailed information about Calendar Recurring Event Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for managing recurring events, such as calendar ID, event start and end times, availability status, and recurrence patterns. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive list of fields like event name, timezone, and record URL. Additionally, it details the search query fields that can be used to filter calendar recurring events, such as calendar ID, event name, and availability status. Lastly, it lists the worklist columns available for displaying recurring event data, including calendar ID, event name, and recurrence details. This information is crucial for developers and users who need to integrate or manage recurring events within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Calendar Recurring Event |
| **Name (plural):** | Calendar Recurring Events |
| **Alias (uri):** | calendar\_recurring\_event |
| **Identifier (ID):** | cerberusweb.contexts.calendar\_event.recurring |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`calendar_id`** | number | The parent calendar of this event |
| &nbsp; | `event_end` | text | The end date/time of the event |
| &nbsp; | `event_start` | text | The start date/time of the event |
| &nbsp; | `is_available` | boolean | `true` for available; `false` for busy |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of the event |
| **x** | **`patterns`** | text | One pattern per line |
| &nbsp; | `recur_end` | timestamp | The end date/time of the recurring range |
| &nbsp; | `recur_start` | timestamp | The start date/time of the recurring range |
| &nbsp; | `tz` | text | The timezone of the recurring event (e.g. `America/Los_Angeles`) |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `calendar_` | record | Calendar |
| `calendar_owner_` | record | Calendar Owner |
| `event_end` | text | End |
| `event_start` | text | Start |
| `id` | number | Id |
| `is_available` | boolean | Is Available |
| `name` | text | Name |
| `patterns` | text | Patterns |
| `record_url` | text | Record Url |
| `recur_end` | text | Recur End |
| `recur_start` | text | Recur Start |
| `tz` | text | Timezone |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in calendar recurring event search queries:

| Field | Type | Description |
| --- | --- | --- |
| `calendar:` | record | Calendar |
| `calendar.id:` | chooser | Calendar |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Event Name |
| `status:` | boolean | Is Available |
| `timezone:` | text | Timezone |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on calendar recurring event worklists:

| Column | Description |
| --- | --- |
| `c_calendar_id` | Calendar |
| `c_event_end` | End |
| `c_event_name` | Event Name |
| `c_event_start` | Start |
| `c_id` | Id |
| `c_is_available` | Is Available |
| `c_patterns` | Patterns |
| `c_recur_end` | Recur End |
| `c_recur_start` | Recur Start |
| `c_tz` | Timezone |
| `cf_<id>` | Custom Field |

\< Record Types

