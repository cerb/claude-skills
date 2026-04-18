---
id: "docs-records-types-calendar"
title: "Calendar Records"
url: "https://cerb.ai/docs/records/types/calendar/"
summary: "This page provides detailed information about Calendar Records in Cerb, including their structure, fields, and functionalities. It outlines the Records API, specifying required and optional fields such as `name`, `owner__context`, and `owner_id`, along with parameters for customization like event colors and synchronization settings. The page also describes dictionary placeholders available for automations and API responses, offering fields like `id`, `name`, and `timezone`. Additionally, it covers search query fields for filtering calendar records and lists available worklist columns for organizing calendar data. The document serves as a comprehensive guide for managing and utilizing calendar records within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Calendar |
| **Name (plural):** | Calendars |
| **Alias (uri):** | calendar |
| **Identifier (ID):** | cerberusweb.contexts.calendar |

- Records API
  - params
  - series

- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this calendar |
| **x** | **`owner__context`** | context | The record type of this calendar's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this calendar's owner |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `timezone` | text | &nbsp; |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

#### params

| Key | Value |
| --- | --- |
| `color_available` | The hex color code for available events (e.g. `#a0d95b`) |
| `color_busy` | The hex color code for busy events (e.g. `#c8c8c8`) |
| `hide_start_time` | `0` to show event start times, `1` to disable |
| `manual_disabled` | `0` to enable manual event creation, `1` to disable |
| `series` | An optional array of **series** objects |
| `start_on_mon` | `0` to start weeks on Sunday, `1` to start on Monday |
| `sync_enabled` | `0` to disable event synchronization, `1` to enable |

#### series

| Key | Value |
| --- | --- |
| `datasource` | `calendar.datasource.worklist` |
| `color` | &nbsp; |
| `field_end_date` | &nbsp; |
| `field_end_date_offset` | &nbsp; |
| `field_start_date` | &nbsp; |
| `field_start_date_offset` | &nbsp; |
| `is_available` | &nbsp; |
| `label` | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `name` | text | Name |
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `timezone` | text | Timezone |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `events` | &nbsp; | Events |
| `events_occluded` | &nbsp; | Events (Occluded) |
| `links` | links | Links |
| `scope` | &nbsp; | Scope |
| `watchers` | watchers | Watchers |
| `weeks` | &nbsp; | Weeks |
| `weeks_events` | &nbsp; | Weeks Events |
| `weeks_events_occluded` | &nbsp; | Weeks Events (Occluded) |

### Search Query Fields

These filters are available in calendar search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner |
| `owner.bot:` | record | Owner |
| `owner.group:` | record | Owner |
| `owner.role:` | record | Owner |
| `owner.worker:` | record | Owner |
| `timezone:` | text | Timezone |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |
| `workerAvailability:` | record | Workers |

### Worklist Columns

These columns are available on calendar worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `c_id` | Id |
| `c_name` | Name |
| `c_timezone` | Timezone |
| `c_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

