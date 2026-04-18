---
id: "docs-records-types-kbcategory"
title: "Knowledgebase Category Records"
url: "https://cerb.ai/docs/records/types/kb_category/"
summary: "This page provides detailed information about Knowledgebase Category records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `name`, `parent_id`, and `updated_at`, and explains how these fields can be used to manage knowledgebase categories. The page also describes dictionary placeholders for automations, snippets, and API responses, offering fields like `id`, `name`, and `updated_at`, along with optional placeholders for comments, custom fields, and links. Additionally, it details search query fields that can be used to filter knowledgebase categories, including `article.id`, `name`, and `updated`. Lastly, it lists the worklist columns available for displaying knowledgebase category information, such as `kbc_id`, `kbc_name`, and `kbc_updated_at`."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Knowledgebase Category |
| **Name (plural):** | Knowledgebase Categories |
| **Alias (uri):** | kb\_category |
| **Identifier (ID):** | cerberusweb.contexts.kb\_category |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this knowledgebase category |
| &nbsp; | `parent_id` | number | The ID of the parent category; if `0` this is a top-level topic |
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
| `parent_id` | number | Parent |
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

These filters are available in knowledgebase category search queries:

| Field | Type | Description |
| --- | --- | --- |
| `article.id:` | chooser | Knowledgebase Article |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `parent.id:` | chooser | Parent |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on knowledgebase category worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `katc_article_id` | Knowledgebase Article |
| `kbc_id` | Id |
| `kbc_name` | Name |
| `kbc_parent_id` | Parent |
| `kbc_updated_at` | Updated |

\< Record Types

