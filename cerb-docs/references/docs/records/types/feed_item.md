---
id: "docs-records-types-feeditem"
title: "Feed Item Records"
url: "https://cerb.ai/docs/records/types/feed_item/"
summary: "This page provides detailed information about Feed Item Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `created_at`, `feed_id`, `guid`, `is_closed`, `title`, and `url`, which are essential for managing feed items. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `_context`, `_label`, `created_at`, and `record_url`. Additionally, it covers search query fields that allow users to filter feed items based on criteria like comments, creation date, feed, and title. Lastly, it lists the worklist columns available for organizing feed items, including custom fields, creation date, feed ID, and title. This comprehensive guide is crucial for developers and users looking to effectively manage and interact with feed items in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Feed Item |
| **Name (plural):** | Feed Items |
| **Alias (uri):** | feed\_item |
| **Identifier (ID):** | cerberusweb.contexts.feed.item |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| **x** | **`feed_id`** | number | The ID of the feed containing this item |
| &nbsp; | `guid` | text | The globally unique ID of this item in the feed |
| &nbsp; | `is_closed` | boolean | Is this item viewed/resolved? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`title`** | text | The title of this feed item |
| **x** | **`url`** | text | The URL of this feed item |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `feed_` | record | Feed |
| `guid` | text | Guid |
| `id` | number | Id |
| `is_closed` | boolean | Is Closed |
| `record_url` | text | Record Url |
| `title` | text | Title |
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

These filters are available in feed item search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Created |
| `feed:` | record | Feed |
| `feed.id:` | chooser | Feed |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isClosed:` | boolean | Is Closed |
| `links:` | links | Record Links |
| `title:` | text | Title |
| `url:` | text | Url |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on feed item worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `fi_created_date` | Created |
| `fi_feed_id` | Feed |
| `fi_is_closed` | Is Closed |
| `fi_title` | Title |
| `fi_url` | Url |

\< Record Types

