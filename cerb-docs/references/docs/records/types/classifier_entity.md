---
id: "docs-records-types-classifierentity"
title: "Classifier Entity Records"
url: "https://cerb.ai/docs/records/types/classifier_entity/"
summary: "This page provides detailed information about Classifier Entity Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as name, type, description, and links, and specifies which fields are required. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like context, label, and record URL. Additionally, it lists search query fields that can be used to filter classifier entities, such as description, fieldset, and updated date. Lastly, it details the worklist columns available for classifier entities, including description, ID, name, type, and updated date, providing a comprehensive guide for managing and utilizing classifier entities within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Classifier Entity |
| **Name (plural):** | Classifier Entities |
| **Alias (uri):** | classifier\_entity |
| **Identifier (ID):** | cerberusweb.contexts.classifier.entity |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `description` | text | A description of this entity |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this classifier entity |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| **x** | **`type`** | text | The type of this entity: `list`, `regexp`, or `text` |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

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
| `params` | &nbsp; | Params |
| `record_url` | text | Record Url |
| `type` | text | Type |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `links` | links | Links |

### Search Query Fields

These filters are available in classifier entity search queries:

| Field | Type | Description |
| --- | --- | --- |
| `description:` | text | Description |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on classifier entity worklists:

| Column | Description |
| --- | --- |
| `c_description` | Description |
| `c_id` | Id |
| `c_name` | Name |
| `c_type` | Type |
| `c_updated_at` | Updated |

\< Record Types

