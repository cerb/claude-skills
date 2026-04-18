---
id: "docs-records-types-activitylog"
title: "Activity Log Records"
url: "https://cerb.ai/docs/records/types/activity_log/"
summary: "This page provides detailed information about the Activity Log records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `activity_point`, `actor__context`, and `target__context`, and explains their types and requirements. The page also describes the parameters for logging messages, including placeholders and variable URLs. Additionally, it covers dictionary placeholders for automations and API responses, search query fields for filtering activity logs, and worklist columns for organizing and displaying log data. This comprehensive guide is essential for understanding how to manage and utilize activity logs within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Activity Log |
| **Name (plural):** | Activity Logs |
| **Alias (uri):** | activity\_log |
| **Identifier (ID):** | cerberusweb.contexts.activity\_log |

- Records API
  - params

- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`activity_point`** | text | The event ID that occurred (or `custom.other`) |
| **x** | **`actor__context`** | context | The actor's record type |
| **x** | **`actor_id`** | number | The actor's record ID |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| **x** | **`target__context`** | context | The target's record type |
| **x** | **`target_id`** | number | The target's record ID |

#### params

| Key | Value |
| --- | --- |
| `message` | The log message with your own `{{variables}}` |
| `variables` | A key/value object of placeholder values |
| `urls` | A key/value object of optional variable urls in the format `ctx://record_type:123` |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `activity_point` | text | Event Id |
| `actor_` | record | Actor |
| `created` | date | Created |
| `event` | text | Event |
| `id` | number | Id |
| `target_` | record | Target |

### Search Query Fields

These filters are available in activity log search queries:

| Field | Type | Description |
| --- | --- | --- |
| `activity:` | text | Activity |
| `actor:` | text | Actor Type |
| `actor.<type>:` | record | Actor |
| `created:` | date | Created |
| `id:` | number | Id |
| `target:` | text | Target Type |
| `target.<type>:` | record | Target |

### Worklist Columns

These columns are available on activity log worklists:

| Column | Description |
| --- | --- |
| `*_actor` | Actor |
| `*_target` | Target |
| `c_activity_point` | Activity |
| `c_actor_context` | Actor Context |
| `c_created` | Created |
| `c_entry_json` | Entry |
| `c_id` | Id |
| `c_target_context` | Target Context |

\< Record Types

