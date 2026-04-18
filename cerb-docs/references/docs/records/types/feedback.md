---
id: "docs-records-types-feedback"
title: "Feedback Records"
url: "https://cerb.ai/docs/records/types/feedback/"
summary: "This page provides detailed information about feedback records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as author ID, creation timestamp, mood, and feedback content. The page also describes dictionary placeholders for automations and API responses, offering fields like author, mood, and quote. Additionally, it covers search query fields for filtering feedback based on criteria like creation date, email, mood, and worker. Lastly, it lists the columns available in feedback worklists, which include custom fields, log date, mood, quote, and source URL."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Feedback |
| **Name (plural):** | Feedback |
| **Alias (uri):** | feedback |
| **Identifier (ID):** | cerberusweb.contexts.feedback |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `author_id` | number | The ID of the email address of the feedback author |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`quote_mood_id`** | number | `0` (neutral), `1` (praise), `2` (criticism) |
| **x** | **`quote_text`** | text | The feedback content |
| &nbsp; | `url` | url | (optional) The URL where the feedback was received |
| &nbsp; | `worker_id` | number | The ID of the worker who captured the feedback |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_label` | text | Label |
| `author_` | record | Author |
| `created` | date | Log Date |
| `id` | number | Id |
| `quote_mood` | text | Mood |
| `quote_text` | text | Quote |
| `url` | text | Link |
| `worker_` | record | Worker |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in feedback search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Log Date |
| `email:` | record | Email |
| `email.id:` | chooser | Author Email |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `mood:` | text | Mood |
| `quote:` | text | Quote |
| `watchers:` | watchers | Watchers |
| `worker:` | record | Worker |

### Worklist Columns

These columns are available on feedback worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `f_log_date` | Log Date |
| `f_quote_mood` | Mood |
| `f_quote_text` | Quote |
| `f_source_url` | Link |
| `f_worker_id` | Created By |

\< Record Types

