---
id: "docs-records-types-communityportal"
title: "Portal Records"
url: "https://cerb.ai/docs/records/types/community_portal/"
summary: "This page provides detailed information about the 'Portal' record type in Cerb, including its API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and requirements for interacting with portal records through the Records API, specifying fields such as `code`, `extension_id`, `name`, `uri`, and `updated_at`. The page also describes the available dictionary placeholders for use in automations and API responses, as well as optional placeholders with key expansion. Additionally, it lists the search query fields that can be used to filter portal records and the columns available for display in portal worklists. This comprehensive guide is essential for developers and users managing portal records within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Portal |
| **Name (plural):** | Portals |
| **Alias (uri):** | community\_portal |
| **Identifier (ID):** | cerberusweb.contexts.portal |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `code` | text | Randomized internal ID for the portal |
| **x** | **`extension_id`** | text | Community Portal Type |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this portal |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| **x** | **`uri`** | text | Human-friendly nickname for the portal. Must be unique. |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `code` | text | Code |
| `extension_id` | text | Extension |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |
| `uri` | text | Path |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in portal search queries:

| Field | Type | Description |
| --- | --- | --- |
| `code:` | text | Code |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `name:` | text | Name |
| `path:` | text | Path |
| `type:` | text | Extension |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on portal worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `ct_code` | Code |
| `ct_extension_id` | Extension |
| `ct_id` | Id |
| `ct_name` | Name |
| `ct_updated_at` | Updated |
| `ct_uri` | Path |

\< Record Types

