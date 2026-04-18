---
id: "docs-records-types-cardwidget"
title: "Card Widget Records"
url: "https://cerb.ai/docs/records/types/card_widget/"
summary: "This page provides detailed information about Card Widget records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and attributes of Card Widgets, such as their extension ID, name, position, record type, and update timestamp. The page also describes how these widgets can be linked to other records and customized with JSON-encoded parameters. Additionally, it explains the available dictionary placeholders for automations and API responses, as well as the search filters and worklist columns that can be used to manage and organize Card Widgets effectively."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Card Widget |
| **Name (plural):** | Card Widgets |
| **Alias (uri):** | card\_widget |
| **Identifier (ID):** | cerb.contexts.card.widget |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`extension_id`** | text | Card Widget Type |
| &nbsp; | `extension_params` | object | JSON-encoded key/value object |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this card widget |
| &nbsp; | `pos` | number | The order of the widget on the card; `0` is first (top-left) proceeding in rows then columns |
| **x** | **`record_type`** | context | The record type of the card containing this widget |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `width_units` | number | `1` (25%), `2` (50%), `3` (75%), `4` (100%) |
| &nbsp; | `zone` | text | The name of the dashboard zone containing the widget; this varies by layout; generally `sidebar` and `content` |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in card widget search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `pos:` | number | Order |
| `type:` | text | Name |
| `updated:` | date | Updated |
| `width:` | number | Width |
| `zone:` | text | Zone |

### Worklist Columns

These columns are available on card widget worklists:

| Column | Description |
| --- | --- |
| `c_created_at` | Created |
| `c_extension_id` | Type |
| `c_id` | Id |
| `c_name` | Name |
| `c_pos` | Order |
| `c_record_type` | Record Type |
| `c_updated_at` | Updated |
| `c_width_units` | Width |
| `c_zone` | Zone |
| `cf_<id>` | Custom Field |

\< Record Types

