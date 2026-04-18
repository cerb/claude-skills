---
id: "docs-records-types-connectedservice"
title: "Connected Service Records"
url: "https://cerb.ai/docs/records/types/connected_service/"
summary: "This page provides detailed information about Connected Service records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for managing connected services, such as `extension_id`, `name`, and `updated_at`. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `id`, `name`, and `record_url`. Additionally, it covers search query fields that facilitate filtering connected services based on criteria like `id`, `name`, and `updated`. Lastly, it lists the worklist columns available for displaying connected service data, including `c_extension_id`, `c_name`, and custom fields. This comprehensive guide is crucial for developers and users who need to integrate and manage connected services within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Connected Service |
| **Name (plural):** | Connected Services |
| **Alias (uri):** | connected\_service |
| **Identifier (ID):** | cerberusweb.contexts.connected\_service |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`extension_id`** | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this connected service |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `uri` | text | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `extension_id` | text | Type Common.id |
| `extension_name` | text | Type |
| `id` | number | Id |
| `name` | text | Name |
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

### Search Query Fields

These filters are available in connected service search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `uri:` | text | Uri |

### Worklist Columns

These columns are available on connected service worklists:

| Column | Description |
| --- | --- |
| `c_extension_id` | Type |
| `c_id` | Id |
| `c_name` | Name |
| `c_updated_at` | Updated |
| `c_uri` | Uri |
| `cf_<id>` | Custom Field |

\< Record Types

