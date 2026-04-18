---
id: "docs-records-types-comment"
title: "Comment Records"
url: "https://cerb.ai/docs/records/types/comment/"
summary: "This page provides detailed information about the structure and functionality of comment records in Cerb. It outlines the fields available in the Records API, including required fields such as author context, author ID, comment text, target context, and target ID. The page also describes dictionary placeholders used in automations, snippets, and API responses, highlighting fields like author, comment content, and creation date. Additionally, it covers search query fields that allow filtering comments based on various criteria such as attachments, author, comment content, creation date, and more. Lastly, it lists the worklist columns available for organizing comment data, including target, creation date, ID, markdown status, and custom fields. This comprehensive guide is essential for understanding and utilizing comment records within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Comment |
| **Name (plural):** | Comments |
| **Alias (uri):** | comment |
| **Identifier (ID):** | cerberusweb.contexts.comment |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`author__context`** | context | The record type of the comment's author |
| **x** | **`author_id`** | number | The ID of the comment's author |
| **x** | **`comment`** | text | The text of the comment |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `is_markdown` | boolean | `0`=plaintext, `1`=Markdown |
| &nbsp; | `is_pinned` | boolean | `0`=not pinned, `1`=pinned |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`target__context`** | context | The record type of the target record |
| **x** | **`target_id`** | number | The ID of the target record |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `author_` | record | Author |
| `comment` | text | Content |
| `created` | date | Created |
| `id` | number | Id |
| `target_` | record | Target |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `attachments` | attachments | Attachments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in comment search queries:

| Field | Type | Description |
| --- | --- | --- |
| `attachments:` | record | Attachments |
| `author:` | text | Actor |
| `author.<type>:` | record | Actor |
| `comment:` | fulltext | Comment Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isMarkdown:` | boolean | Markdown |
| `isPinned:` | boolean | Is Pinned |
| `links:` | links | Record Links |
| `on:` | text | On Type |
| `on.<type>:` | record | Target |

### Worklist Columns

These columns are available on comment worklists:

| Column | Description |
| --- | --- |
| `*_target` | Target |
| `c_created` | Created |
| `c_id` | Id |
| `c_is_markdown` | Markdown |
| `c_is_pinned` | Is Pinned |
| `cf_<id>` | Custom Field |

\< Record Types

