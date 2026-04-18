---
id: "docs-records-types-customfield"
title: "Custom Field Records"
url: "https://cerb.ai/docs/records/types/custom_field/"
summary: "This page provides detailed information about custom field records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as context, name, type, and URI, and explains their types and requirements. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a comprehensive list of fields and their descriptions. Additionally, it covers search query fields that can be used to filter custom field records and lists the available columns for custom field worklists, providing a complete guide for managing and utilizing custom fields in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Custom Field |
| **Name (plural):** | Custom Fields |
| **Alias (uri):** | custom\_field |
| **Identifier (ID):** | cerberusweb.contexts.custom\_field |

- Records API
  - Types

- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`context`** | context | The record type to add the field to |
| &nbsp; | `custom_fieldset_id` | number | The ID of the parent custom fieldset; if any |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this custom field |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `pos` | number | Display order; positive integer; `0` is first |
| **x** | **`type`** | text | See Types below |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| **x** | **`uri`** | text | The unique alias for this custom field |

#### Types

| Type | ID | Params |
| --- | --- | --- |
| Checkbox | `C` | &nbsp; |
| Currency | `Y` | `currency_id` (record ID of a currency record) |
| Date | `E` | &nbsp; |
| Decimal | `O` | `decimal_at` (number of decimal places; e.g. `4` for 3.1415) |
| File | `F` | &nbsp; |
| Files | `I` | &nbsp; |
| Latitude/Longitude | `cerb.custom_field.geo.point` | &nbsp; |
| List | `M` | `context` (record type alias) |
| Multiple Checkboxes | `X` | `options` (one per line, linefeed delimited) |
| Multiple Lines of Text | `T` | `format` (blank for plaintext, or `markdown`) |
| Number | `N` | &nbsp; |
| Picklist | `D` | `options` (one per line, linefeed delimited) |
| Record Link | `L` | `context` (record type alias) |
| Record Links | `cerb.custom_field.record.links` | `context` (record type alias) |
| Single Line of Text | `S` | &nbsp; |
| Slider | `cerb.custom_field.slider` | `value_min`, `value_max` |
| URL | `U` | &nbsp; |
| Worker | `W` | `send_notifications` (`0` disabled, `1` enabled) |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `context` | text | Context |
| `id` | number | Id |
| `name` | text | Name |
| `pos` | number | Order |
| `search_filter` | text | Search Filter Name |
| `type` | text | Type |
| `type_label` | text | Type Label |
| `updated_at` | date | Updated |
| `uri` | text | Uri |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |

### Search Query Fields

These filters are available in custom field search queries:

| Field | Type | Description |
| --- | --- | --- |
| `context:` | text | Context |
| `fieldset:` | record | Fieldset |
| `fieldset.id:` | chooser | Custom Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `pos:` | number | Order |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `uri:` | text | Uri |

### Worklist Columns

These columns are available on custom field worklists:

| Column | Description |
| --- | --- |
| `c_context` | Context |
| `c_custom_fieldset_id` | Custom Fieldset |
| `c_id` | Id |
| `c_name` | Name |
| `c_pos` | Order |
| `c_type` | Type |
| `c_updated_at` | Updated |
| `c_uri` | Uri |

\< Record Types

