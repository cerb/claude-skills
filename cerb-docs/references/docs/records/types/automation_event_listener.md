---
id: "docs-records-types-automationeventlistener"
title: "Automation Event Listener Records"
url: "https://cerb.ai/docs/records/types/automation_event_listener/"
summary: "This page provides detailed information about Automation Event Listener records in Cerb. It covers the fields available in the Records API, including required fields like `event_name` and `name`, and optional fields such as `event_kata`, `is_disabled`, and `priority`. The page also outlines dictionary placeholders for use in automations, snippets, and API responses, offering a range of fields like `event_name`, `id`, and `updated_at`. Additionally, it describes search query fields that can be used to filter automation event listener records, such as `created:`, `event:`, and `isDisabled:`. Lastly, it lists the worklist columns available for displaying these records, including `a_created_at`, `a_event_name`, and `a_priority`. This comprehensive guide is essential for managing and utilizing automation event listeners within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Automation Event Listener |
| **Name (plural):** | Automation Event Listeners |
| **Alias (uri):** | automation\_event\_listener |
| **Identifier (ID):** | cerb.contexts.automation.event.listener |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `event_kata` | text | &nbsp; |
| **x** | **`event_name`** | text | &nbsp; |
| &nbsp; | `is_disabled` | number | (0-1) |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this automation event listener |
| &nbsp; | `priority` | number | (0-255) |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `workflow_id` | number | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `event_kata` | text | Event Kata |
| `event_name` | text | Automation Event |
| `id` | number | Id |
| `is_disabled` | boolean | Disabled |
| `name` | text | Name |
| `priority` | number | Priority |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |
| `workflow_id` | number | Common.workflow.id |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in automation event listener search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `event:` | text | Event |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isDisabled:` | boolean | Disabled |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `priority:` | number | Priority |
| `updated:` | date | Updated |
| `workflow.id:` | chooser | Workflow |

### Worklist Columns

These columns are available on automation event listener worklists:

| Column | Description |
| --- | --- |
| `a_created_at` | Created |
| `a_event_name` | Event |
| `a_id` | Id |
| `a_is_disabled` | Disabled |
| `a_name` | Name |
| `a_priority` | Priority |
| `a_updated_at` | Updated |
| `a_workflow_id` | Workflow |
| `cf_<id>` | Custom Field |

\< Record Types

