---
id: "docs-records-types-filebundle"
title: "File Bundle Records"
url: "https://cerb.ai/docs/records/types/file_bundle/"
summary: "This page provides detailed information about File Bundle Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as name, owner context, and tags, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also describes the search query fields that can be used to filter file bundles, such as by comments, owner, and tags. Additionally, it lists the worklist columns available for organizing file bundle data, including owner, custom fields, and update timestamps. This comprehensive guide is essential for users looking to manage and interact with file bundles effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | File Bundle |
| **Name (plural):** | File Bundles |
| **Alias (uri):** | file\_bundle |
| **Identifier (ID):** | cerberusweb.contexts.file\_bundle |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this file bundle |
| **x** | **`owner__context`** | context | The record type of this file bundle's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this file bundle's owner |
| &nbsp; | `tag` | text | A human-friendly nickname for the bundle; e.g. `tax_forms` |
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
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `tag` | text | Tag |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `attachments` | attachments | Attachments |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in file bundle search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner |
| `owner.bot:` | record | Owner |
| `owner.group:` | record | Owner |
| `owner.role:` | record | Owner |
| `owner.worker:` | record | Owner |
| `tag:` | text | Tag |
| `updated:` | date | Updated |
| `usableBy.worker:` | virtual | Usable by Worker |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on file bundle worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `cf_<id>` | Custom Field |
| `f_id` | Id |
| `f_name` | Name |
| `f_tag` | Tag |
| `f_updated_at` | Updated |

\< Record Types

