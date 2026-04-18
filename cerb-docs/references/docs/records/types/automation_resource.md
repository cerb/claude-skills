---
id: "docs-records-types-automationresource"
title: "Automation Resource Records"
url: "https://cerb.ai/docs/records/types/automation_resource/"
summary: "This page provides detailed information about Automation Resource Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as links, mime type, name, token, and updated timestamp. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering fields like context, label, type, id, mime type, name, record URL, size, token, and updated date. Additionally, it lists search query fields that can filter automation resource searches, including fieldset, id, links, mimetype, name, size, token, and updated date. Lastly, it details the worklist columns available for automation resources, which include custom fields, id, mime type, name, storage extension, storage key, storage profile, size, token, and updated timestamp."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Automation Resource |
| **Name (plural):** | Automation Resources |
| **Alias (uri):** | automation\_resource |
| **Identifier (ID):** | cerb.contexts.automation.resource |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mime_type` | text | &nbsp; |
| &nbsp; | `name` | text | The name of this automation resource |
| **x** | **`token`** | text | &nbsp; |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `mime_type` | text | Mime Type |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `size` | number | Size |
| `token` | text | Token |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `custom_<id>` | mixed | Custom Fields |

### Search Query Fields

These filters are available in automation resource search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `mimetype:` | text | Mime Type |
| `name:` | text | Name |
| `size:` | number | Size |
| `token:` | text | Token |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on automation resource worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `r_id` | Id |
| `r_mime_type` | Mime Type |
| `r_name` | Name |
| `r_storage_extension` | Storage Extension |
| `r_storage_key` | Storage Key |
| `r_storage_profile_id` | Storage Profile |
| `r_storage_size` | Size |
| `r_token` | Token |
| `r_updated_at` | Updated |

\< Record Types

