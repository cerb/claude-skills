---
id: "docs-records-types-calendarevent"
title: "Calendar Event Records"
url: "https://cerb.ai/docs/records/types/calendar_event/"
summary: "This page provides detailed information about Calendar Event records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as calendar ID, start and end dates, availability status, and event name. The page also describes dictionary placeholders for use in automations, snippets, and API responses, offering fields like context, label, calendar details, and record URL. Additionally, it lists search query fields that can be used to filter calendar events, including calendar, end date, start date, and status. Lastly, it details the worklist columns available for displaying calendar events, covering aspects like calendar ID, start and end dates, availability, and custom fields."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Calendar Event |
| **Name (plural):** | Calendar Events |
| **Alias (uri):** | calendar\_event |
| **Identifier (ID):** | cerberusweb.contexts.calendar\_event |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`calendar_id`** | number | The parent calendar of this event |
| &nbsp; | `date_end` | timestamp | The end date/time of the event |
| **x** | **`date_start`** | timestamp | The start date/time of the event |
| &nbsp; | `is_available` | boolean | `true` for available; `false` for busy |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of the event |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `calendar_` | record | Calendar |
| `calendar_owner_` | record | Calendar Owner |
| `date_end` | date | End Date |
| `date_start` | date | Start Date |
| `id` | number | Id |
| `is_available` | boolean | Is Available |
| `name` | text | Name |
| `record_url` | text | Record Url |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in calendar event search queries:

| Field | Type | Description |
| --- | --- | --- |
| `calendar:` | record | Calendar |
| `calendar.id:` | chooser | Calendar |
| `endDate:` | date | End Date |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `startDate:` | date | Start Date |
| `status:` | boolean | Is Available |

### Worklist Columns

These columns are available on calendar event worklists:

| Column | Description |
| --- | --- |
| `*_has_fieldset` | Fieldset |
| `c_calendar_id` | Calendar |
| `c_date_end` | End Date |
| `c_date_start` | Start Date |
| `c_is_available` | Is Available |
| `c_name` | Name |
| `cf_<id>` | Custom Field |

\< Record Types

