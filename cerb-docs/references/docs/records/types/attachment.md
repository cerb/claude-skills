---
id: "docs-records-types-attachment"
title: "Attachment Records"
url: "https://cerb.ai/docs/records/types/attachment/"
summary: "This page provides detailed information about attachment records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and types of data associated with attachments, such as file content, MIME type, and links to other records. The page also describes how to use these fields in the Records API and packages, and how to incorporate them into automations, snippets, and API responses. Additionally, it explains the available search filters for querying attachments and the columns that can be displayed in attachment worklists. This comprehensive guide is essential for managing and utilizing attachment records within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Attachment |
| **Name (plural):** | Attachments |
| **Alias (uri):** | attachment |
| **Identifier (ID):** | cerberusweb.contexts.attachment |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `attach` | links | An array of `type:id` tuples to attach this file to |
| &nbsp; | `content` | text | The optional content of this file. For binary, base64-encode in data URI format. For `application/vnd.cerb.uri` this should be a URI like `cerb:automation_resource:3ed620aa-a4b5-11ec-89ea-6b1bb00ef554` |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mime_type` | text | The MIME type of this file (e.g. `image/png`); defaults to `application/octet-stream`. Can be `application/vnd.cerb.uri` for an automation resource URI in `content`. |
| **x** | **`name`** | text | The filename |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

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
| `size` | number | Size (Bytes) |
| `storage_extension` | text | Storage Extension |
| `storage_key` | text | Storage Key |
| `storage_sha1hash` | text | Sha-1 Hash |
| `updated` | date | Updated |
| `url_download` | text | Url |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `on` | records | Records attached to (max 100) |
| `on.<type>` | records | Records attached to by record type |

### Search Query Fields

These filters are available in attachment search queries:

| Field | Type | Description |
| --- | --- | --- |
| `bundle:` | record | Bundle |
| `fieldset:` | record | Fieldset |
| `id:` | number | Attachment Id |
| `links:` | links | Record Links |
| `mimetype:` | text | Mime Type |
| `name:` | text | Name |
| `on:` | text | On Type |
| `on.<type>:` | record | On |
| `size:` | number | Size |
| `storage.extension:` | text | Storage Extension |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on attachment worklists:

| Column | Description |
| --- | --- |
| `a_id` | Attachment Id |
| `a_mime_type` | Mime Type |
| `a_name` | Name |
| `a_storage_extension` | Storage Extension |
| `a_storage_key` | Storage Key |
| `a_storage_profile_id` | Storage Profile |
| `a_storage_sha1hash` | Sha-1 Hash |
| `a_storage_size` | Size |
| `a_updated` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

