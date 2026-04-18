---
id: "docs-records-types-gpgprivatekey"
title: "PGP Private Key Records"
url: "https://cerb.ai/docs/records/types/gpg_private_key/"
summary: "This page provides detailed information about PGP Private Key records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `fingerprint`, `name`, and `updated_at`, and describes how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also details the search query fields that can be used to filter PGP private key records, such as `expires`, `fingerprint`, and `name`. Additionally, it lists the worklist columns available for organizing and displaying PGP private key data, including custom fields and key attributes like `expires_at` and `fingerprint`. This comprehensive guide is essential for managing and integrating PGP private key records within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Pgp Private Key |
| **Name (plural):** | Pgp Private Keys |
| **Alias (uri):** | gpg\_private\_key |
| **Identifier (ID):** | cerb.contexts.gpg.private.key |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `expires_at` | timestamp | &nbsp; |
| **x** | **`fingerprint`** | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this pgp private key |
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
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in pgp private key search queries:

| Field | Type | Description |
| --- | --- | --- |
| `expires:` | date | Expires |
| `fieldset:` | record | Fieldset |
| `fingerprint:` | virtual | Fingerprint |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on pgp private key worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `g_expires_at` | Expires |
| `g_fingerprint` | Fingerprint |
| `g_id` | Id |
| `g_name` | Name |
| `g_updated_at` | Updated |

\< Record Types

