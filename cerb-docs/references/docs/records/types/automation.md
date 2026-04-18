---
id: "docs-records-types-automation"
title: "Automation Records"
url: "https://cerb.ai/docs/records/types/automation/"
summary: "This page provides detailed information about automation records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as creation and update timestamps, descriptions, and links. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like context, label, and policy. Additionally, it covers search query fields that allow filtering automations based on criteria like creation date, name, and script content. Lastly, it lists the worklist columns available for displaying automation records, including fields for creation date, description, and custom fields. This comprehensive guide is essential for understanding and utilizing automation records effectively in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Automation |
| **Name (plural):** | Automations |
| **Alias (uri):** | automation |
| **Identifier (ID):** | cerb.contexts.automation |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `description` | text | &nbsp; |
| **x** | **`extension_id`** | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `name` | text | The name of this automation |
| &nbsp; | `policy_kata` | text | &nbsp; |
| &nbsp; | `script` | text | &nbsp; |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `description` | text | Description |
| `extension_id` | text | Trigger |
| `extension_params` | &nbsp; | Trigger Params |
| `id` | number | Id |
| `name` | text | Name |
| `policy_kata` | text | Policy |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `script` | text | Script |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in automation search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `script:` | fulltext | Fulltext |
| `trigger:` | text | Extension |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on automation worklists:

| Column | Description |
| --- | --- |
| `a_created_at` | Created |
| `a_description` | Description |
| `a_extension_id` | Extension |
| `a_id` | Id |
| `a_name` | Name |
| `a_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

