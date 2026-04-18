---
id: "docs-records-types-notification"
title: "Notification Records"
url: "https://cerb.ai/docs/records/types/notification/"
summary: "This page provides detailed information about notification records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as activity points, creation timestamps, read status, and worker IDs. The page also describes the parameters for notifications, including customizable messages and variable URLs. Additionally, it covers dictionary placeholders for automations and API responses, search query fields for filtering notifications, and worklist columns for organizing notification data. This comprehensive guide is essential for understanding how notifications are managed and utilized within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Notification |
| **Name (plural):** | Notifications |
| **Alias (uri):** | notification |
| **Identifier (ID):** | cerberusweb.contexts.notification |

- Records API
  - params

- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`activity_point`** | text | The event that triggered the notification (or `custom.other`) |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `is_read` | boolean | Has this been read by the worker? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`params`** | object | A key/value object of notification properties |
| &nbsp; | `target__context` | context | The record type of the target record |
| &nbsp; | `target_id` | number | The ID of the target record |
| **x** | **`worker_id`** | number | The ID of the worker who received the notification |

#### params

| Key | Value |
| --- | --- |
| `message` | The notification message with your own `{{variables}}` |
| `variables` | A key/value object of placeholder values |
| `urls` | A key/value object of optional variable urls in the format `ctx://record_type:123` |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `activity_point` | text | Activity |
| `assignee_` | record | Assignee |
| `created` | date | Created |
| `event_json` | text | Event Json |
| `id` | number | Id |
| `is_read` | boolean | Is Read |
| `message` | text | Message |
| `message_html` | text | Message (Html) |
| `target_` | record | Target |
| `url` | text | Url |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `links` | links | Links |

### Search Query Fields

These filters are available in notification search queries:

| Field | Type | Description |
| --- | --- | --- |
| `activity:` | text | Activity |
| `created:` | date | Created |
| `id:` | number | Id |
| `isRead:` | boolean | Is Read |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on notification worklists:

| Column | Description |
| --- | --- |
| `we_activity_point` | Activity |
| `we_created_date` | Created |
| `we_id` | Id |
| `we_is_read` | Is Read |
| `we_worker_id` | Worker |

\< Record Types

