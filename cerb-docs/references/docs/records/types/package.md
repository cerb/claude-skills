---
id: "docs-records-types-package"
title: "Package Records"
url: "https://cerb.ai/docs/records/types/package/"
summary: "This page provides detailed information about the structure and functionality of Package Records in Cerb. It outlines the fields available in the Records API, including required fields like name, package_json, point, and uri, as well as optional fields such as description, image, and links. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a comprehensive list of fields and their types. Additionally, it covers search query fields that can be used to filter package records and lists the columns available in package worklists, providing a complete guide for managing and utilizing package records within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Package |
| **Name (plural):** | Packages |
| **Alias (uri):** | package |
| **Identifier (ID):** | cerberusweb.contexts.package.library |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `description` | text | A description of this library package's contents |
| &nbsp; | `image` | image | The profile image, base64-encoded in data URI format |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this package |
| **x** | **`package_json`** | text | &nbsp; |
| **x** | **`point`** | text | The library section containing this package |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| **x** | **`uri`** | text | The unique identifier of this package |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `description` | text | Description |
| `id` | number | Id |
| `name` | text | Name |
| `point` | text | Extension Point |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |
| `uri` | text | Uri |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `links` | links | Links |

### Search Query Fields

These filters are available in package search queries:

| Field | Type | Description |
| --- | --- | --- |
| `description:` | text | Description |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `point:` | text | Extension Point |
| `updated:` | date | Updated |
| `uri:` | text | Uri |

### Worklist Columns

These columns are available on package worklists:

| Column | Description |
| --- | --- |
| `p_description` | Description |
| `p_id` | Id |
| `p_name` | Name |
| `p_point` | Extension Point |
| `p_updated_at` | Updated |
| `p_uri` | Uri |

\< Record Types

