---
id: "docs-records-types-resource"
title: "Resource Records"
url: "https://cerb.ai/docs/records/types/resource/"
summary: "This page provides detailed information about Resource Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for managing resources, such as `automation_kata`, `content`, `extension_id`, and `name`. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive list of fields like `description`, `is_dynamic`, and `record_url`. Additionally, it covers search query fields that facilitate filtering resources based on attributes like `cacheUntil`, `description`, and `type`. Lastly, it details the worklist columns available for resource management, providing insights into fields like `r_cache_until`, `r_name`, and `r_updated_at`. This resource is crucial for developers and users looking to effectively utilize and manage resources within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Resource |
| **Name (plural):** | Resources |
| **Alias (uri):** | resource |
| **Identifier (ID):** | cerb.contexts.resource |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `automation_kata` | text | &nbsp; |
| &nbsp; | `cache_until` | timestamp | &nbsp; |
| &nbsp; | `content` | text | The optional content of this resource. For text, use a string. For binary, base64-encode in data URI format. This may also be an automation resource URI (e.g. `cerb:automation_resource:TOKEN`) |
| &nbsp; | `description` | text | &nbsp; |
| **x** | **`extension_id`** | text | A cerb.resource.type extension ID. |
| &nbsp; | `is_dynamic` | boolean | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this resource |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `automation_kata` | text | Automation |
| `cache_until` | date | Cache Until |
| `description` | text | Description |
| `extension_id` | text | Type |
| `id` | number | Id |
| `is_dynamic` | boolean | Is Dynamic |
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

These filters are available in resource search queries:

| Field | Type | Description |
| --- | --- | --- |
| `cacheUntil:` | date | Cache |
| `description:` | text | Description |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isDynamic:` | boolean | Is Dynamic |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `size:` | number | Size |
| `type:` | text | Type |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on resource worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `r_cache_until` | Cache |
| `r_description` | Description |
| `r_extension_id` | Type |
| `r_id` | Id |
| `r_is_dynamic` | Is Dynamic |
| `r_name` | Name |
| `r_storage_extension` | Storage Extension |
| `r_storage_key` | Storage Key |
| `r_storage_profile_id` | Storage Profile |
| `r_storage_size` | Size |
| `r_updated_at` | Updated |

\< Record Types

