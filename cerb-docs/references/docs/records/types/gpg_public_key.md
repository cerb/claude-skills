---
id: "docs-records-types-gpgpublickey"
title: "PGP Public Key Records"
url: "https://cerb.ai/docs/records/types/gpg_public_key/"
summary: "This page provides detailed information about PGP Public Key records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `fingerprint`, `key_text`, and `name`, and explains their types and purposes. The page also describes dictionary placeholders for automations, snippets, and API responses, offering fields like `expires_at`, `fingerprint`, and `record_url`. Additionally, it details search query fields that can be used to filter PGP public key records, such as `expires:`, `fingerprint:`, and `name:`. Lastly, it lists the worklist columns available for displaying PGP public key information, including `g_expires_at`, `g_fingerprint`, and `g_name`. This comprehensive guide is essential for managing and utilizing PGP Public Key records within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Pgp Public Key |
| **Name (plural):** | Pgp Public Keys |
| **Alias (uri):** | gpg\_public\_key |
| **Identifier (ID):** | cerberusweb.contexts.gpg\_public\_key |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `expires_at` | timestamp | The expiration date of the public key |
| **x** | **`fingerprint`** | text | The fingerprint of the public key |
| **x** | **`key_text`** | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this pgp public key |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `expires_at` | date | Expires |
| `fingerprint` | text | Fingerprint |
| `id` | number | Id |
| `key_text` | &nbsp; | Key |
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

These filters are available in pgp public key search queries:

| Field | Type | Description |
| --- | --- | --- |
| `expires:` | date | Expires |
| `fieldset:` | record | Fieldset |
| `fingerprint:` | virtual | Fingerprint |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `uid:` | virtual | Uid |
| `uid.email:` | virtual | Uid.email |
| `uid.name:` | virtual | Uid.name |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on pgp public key worklists:

| Column | Description |
| --- | --- |
| `*_uid` | Uid |
| `*_uid_email` | Uid.email |
| `*_uid_name` | Uid.name |
| `cf_<id>` | Custom Field |
| `g_expires_at` | Expires |
| `g_fingerprint` | Fingerprint |
| `g_id` | Id |
| `g_name` | Name |
| `g_updated_at` | Updated |

\< Record Types

