---
id: "docs-records-types-profiletab"
title: "Profile Tab Records"
url: "https://cerb.ai/docs/records/types/profile_tab/"
summary: "This page provides detailed information about Profile Tab records in Cerb, including their structure and usage within the system. It covers the fields available in the Records API, which are essential for adding profile tabs to specific record types, and includes required fields such as context, extension ID, and name. The page also outlines dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like context, extension ID, and updated timestamps. Additionally, it describes search query fields that facilitate filtering profile tabs based on criteria like fieldset, ID, and name. Lastly, it lists the worklist columns available for organizing and displaying profile tab data, including custom fields and update timestamps. This comprehensive guide is crucial for developers and users looking to integrate and manage profile tabs within Cerb effectively."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Profile Tab |
| **Name (plural):** | Profile Tabs |
| **Alias (uri):** | profile\_tab |
| **Identifier (ID):** | cerberusweb.contexts.profile.tab |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`context`** | context | The record type to add the profile tab to |
| **x** | **`extension_id`** | text | Profile Tab Type |
| &nbsp; | `extension_params` | object | JSON-encoded key/value object |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this profile tab |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `context` | context | Record |
| `extension_id` | extension | Type |
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
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in profile tab search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `record:` | text | Record |
| `type:` | text | Type |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on profile tab worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `p_context` | Record |
| `p_extension_id` | Type |
| `p_id` | Id |
| `p_name` | Name |
| `p_updated_at` | Updated |

\< Record Types

