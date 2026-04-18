---
id: "docs-records-types-feed"
title: "Feed Records"
url: "https://cerb.ai/docs/records/types/feed/"
summary: "This page provides detailed information about Feed Records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as `name` and `url`, and describes how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also details the search query fields that can be used to filter feed records, such as `id`, `name`, and `url`, and lists the worklist columns available for organizing feed data, including custom fields and identifiers. This comprehensive guide is essential for users looking to manage and integrate feed records effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Feed |
| **Name (plural):** | Feeds |
| **Alias (uri):** | feed |
| **Identifier (ID):** | cerberusweb.contexts.feed |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this feed |
| **x** | **`url`** | url | The URL of the RSS feed |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `name` | text | Name |
| `url` | text | Url |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in feed search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `url:` | text | Url |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on feed worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `t_id` | Id |
| `t_name` | Name |
| `t_url` | Url |

\< Record Types

