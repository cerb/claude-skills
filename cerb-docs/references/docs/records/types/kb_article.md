---
id: "docs-records-types-kbarticle"
title: "Knowledgebase Article Records"
url: "https://cerb.ai/docs/records/types/kb_article/"
summary: "This page provides detailed information about Knowledgebase Article records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as categories, content, format, and title, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also describes the search query fields that can be used to filter knowledgebase articles, such as category, content, format, and views. Additionally, it lists the worklist columns available for organizing and displaying knowledgebase articles, including custom fields, format, title, and updated date. This comprehensive guide is essential for managing and utilizing knowledgebase articles effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Knowledgebase Article |
| **Name (plural):** | Knowledgebase Articles |
| **Alias (uri):** | kb\_article |
| **Identifier (ID):** | cerberusweb.contexts.kb\_article |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `categories` | text | A comma-separated list of IDs of categories to assign this article to |
| &nbsp; | `content` | text | The content of the article |
| &nbsp; | `format` | text | `text`, `markdown`, or `html` |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`title`** | text | The title of the article |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |
| &nbsp; | `views` | number | The number of times the article has been viewed in a community portal |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `content` | text | Content |
| `format` | text | Format |
| `id` | number | Id |
| `record_url` | text | Record Url |
| `title` | text | Title |
| `updated` | date | Updated |
| `views` | number | Views |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `attachments` | attachments | Attachments |
| `categories` | hashmap | Categories |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in knowledgebase article search queries:

| Field | Type | Description |
| --- | --- | --- |
| `category.id:` | chooser | Category |
| `content:` | fulltext | Content |
| `fieldset:` | record | Fieldset |
| `format:` | text | Format |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `views:` | number | Views |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on knowledgebase article worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `kb_format` | Format |
| `kb_id` | Id |
| `kb_title` | Title |
| `kb_updated` | Updated |
| `kb_views` | Views |

\< Record Types

