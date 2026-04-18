---
id: "docs-records-types-bot"
title: "Bot Records"
url: "https://cerb.ai/docs/records/types/bot/"
summary: "This page provides detailed information about the bot records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and types of data associated with bot records, such as creation and update timestamps, owner information, and status indicators like whether a bot is disabled. The page also describes how these fields can be used in various contexts, such as automations, snippets, and API responses, and provides guidance on how to filter and display bot records using search queries and worklist columns."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Bot |
| **Name (plural):** | Bots |
| **Alias (uri):** | bot |
| **Identifier (ID):** | cerberusweb.contexts.bot |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `image` | image | The profile image, base64-encoded in data URI format |
| &nbsp; | `is_disabled` | boolean | Is this bot disabled? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mention_name` | text | (deprecated) |
| **x** | **`name`** | text | The name of this bot |
| **x** | **`owner__context`** | context | The record type of this bot's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this bot's owner |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `config` | object | Configuration |
| `created_at` | date | Created |
| `id` | number | Id |
| `is_disabled` | boolean | Disabled |
| `mention_name` | text | @Mention |
| `name` | text | Name |
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `behaviors` | records | Behaviors |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in bot search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `disabled:` | boolean | Disabled |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `mentionName:` | text | @Mention |
| `name:` | text | Name |
| `owner:` | text | Owner Type |
| `owner.<type>:` | record | Owner |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on bot worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `cf_<id>` | Custom Field |
| `v_at_mention_name` | @Mention |
| `v_created_at` | Created |
| `v_id` | Id |
| `v_is_disabled` | Disabled |
| `v_name` | Name |
| `v_updated_at` | Updated |

\< Record Types

