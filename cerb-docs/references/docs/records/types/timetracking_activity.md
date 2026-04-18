---
id: "docs-records-types-timetrackingactivity"
title: "Time Tracking Activity Records"
url: "https://cerb.ai/docs/records/types/timetracking_activity/"
summary: "This page provides detailed information about Time Tracking Activity Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `name` and `updated_at`, and describes how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also details the search query fields that can be used to filter time tracking activities, such as `id`, `name`, and `updated`. Additionally, it lists the worklist columns available for displaying time tracking activities, including custom fields and standard identifiers. This comprehensive guide is essential for users looking to manage and integrate time tracking activities within Cerb effectively."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Time Tracking Activity |
| **Name (plural):** | Time Tracking Activities |
| **Alias (uri):** | timetracking\_activity |
| **Identifier (ID):** | cerberusweb.contexts.timetracking.activity |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this time tracking activity |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in time tracking activity search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on time tracking activity worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `t_id` | Id |
| `t_name` | Name |
| `t_updated_at` | Updated |

\< Record Types

