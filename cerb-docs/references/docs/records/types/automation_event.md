---
id: "docs-records-types-automationevent"
title: "Automation Event Records"
url: "https://cerb.ai/docs/records/types/automation_event/"
summary: "This page provides detailed information about Automation Event Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `description`, `extension_id`, `name`, and `updated_at`, and explains how these fields can be utilized in packages. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `id`, `name`, and `record_url`. Additionally, it details the search query fields that can be used to filter automation events, such as `description`, `extension`, and `name`. Lastly, it lists the worklist columns available for automation events, which include `a_description`, `a_extension_id`, and `a_name`, among others. This comprehensive guide is essential for understanding and managing automation events within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Automation Event |
| **Name (plural):** | Automation Events |
| **Alias (uri):** | automation\_event |
| **Identifier (ID):** | cerb.contexts.automation.event |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `description` | text | &nbsp; |
| **x** | **`extension_id`** | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this automation event |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `description` | text | Description |
| `extension_id` | &nbsp; | Extension |
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

These filters are available in automation event search queries:

| Field | Type | Description |
| --- | --- | --- |
| `description:` | text | Description |
| `extension:` | text | Extension |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on automation event worklists:

| Column | Description |
| --- | --- |
| `a_description` | Description |
| `a_extension_id` | Extension |
| `a_id` | Id |
| `a_name` | Name |
| `a_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

