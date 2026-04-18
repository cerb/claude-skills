---
id: "docs-records-types-snippet"
title: "Snippet Records"
url: "https://cerb.ai/docs/records/types/snippet/"
summary: "This page provides detailed information about Snippet Records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, which are essential for managing snippets, such as content, context, owner details, and usage statistics. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive list of fields and their descriptions. Additionally, it covers search query fields that allow users to filter snippets based on various criteria, such as content, owner, and usage. Lastly, it details the worklist columns available for organizing and displaying snippet information, emphasizing the flexibility and customization options for managing snippets in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Snippet |
| **Name (plural):** | Snippets |
| **Alias (uri):** | snippet |
| **Identifier (ID):** | cerberusweb.contexts.snippet |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`content`** | text | The template of the snippet |
| &nbsp; | `context` | text | The record type to add the profile tab to |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`owner__context`** | context | The record type of this snippet's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this snippet's owner |
| &nbsp; | `prompts_kata` | text | Prompted placeholders in KATA format |
| **x** | **`title`** | text | The name of the snippet |
| &nbsp; | `total_uses` | number | The total number of times this snippet has been used by all workers |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `content` | text | Content |
| `context` | text | Context |
| `id` | number | Id |
| `owner_` | record | Owner |
| `title` | text | Title |
| `total_uses` | number | All Uses |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in snippet search queries:

| Field | Type | Description |
| --- | --- | --- |
| `content:` | text | Content |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `myUses:` | number | My Uses |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner |
| `owner.bot:` | record | Owner |
| `owner.group:` | record | Owner |
| `owner.role:` | record | Owner |
| `owner.worker:` | record | Owner |
| `title:` | text | Title |
| `totalUses:` | number | All Uses |
| `type:` | virtual | Type |
| `updated:` | date | Updated |
| `usableBy.worker:` | virtual | Usable by Worker |

### Worklist Columns

These columns are available on snippet worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `cf_<id>` | Custom Field |
| `s_context` | Type |
| `s_title` | Title |
| `s_total_uses` | All Uses |
| `s_updated_at` | Updated |
| `suh_my_uses` | My Uses |

\< Record Types

