---
id: "docs-records-types-currency"
title: "Currency Records"
url: "https://cerb.ai/docs/records/types/currency/"
summary: "This page provides detailed information about currency records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as currency code, decimal places, default status, and symbols. The page also describes dictionary placeholders for automations and API responses, offering fields like context, label, and record URL. Additionally, it covers search query fields for filtering currency records and worklist columns for organizing and displaying currency data. The document serves as a comprehensive guide for managing and utilizing currency records within Cerb's platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Currency |
| **Name (plural):** | Currencies |
| **Alias (uri):** | currency |
| **Identifier (ID):** | cerberusweb.contexts.currency |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `code` | text | Currency code; e.g. `USD` |
| &nbsp; | `decimal_at` | number | The number of significant decimal places (0-16); e.g. `2` for `0.00` |
| &nbsp; | `is_default` | boolean | Is this the default currency? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `name` | text | The singular name of this currency; `Dollar` |
| &nbsp; | `name_plural` | text | The plural name of this currency; `Dollars` |
| &nbsp; | `symbol` | text | Symbol; `$`, `£`, `€` |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `code` | text | Code |
| `decimal_at` | number | Decimal Places |
| `id` | number | Id |
| `is_default` | boolean | Default |
| `name` | text | Name |
| `name_plural` | text | Plural |
| `record_url` | text | Record Url |
| `symbol` | text | Symbol |
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

These filters are available in currency search queries:

| Field | Type | Description |
| --- | --- | --- |
| `code:` | text | Code |
| `decimalPlaces:` | number | Decimal Places |
| `default:` | boolean | Default |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `symbol:` | text | Symbol |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on currency worklists:

| Column | Description |
| --- | --- |
| `c_code` | Code |
| `c_decimal_at` | Decimal Places |
| `c_id` | Id |
| `c_is_default` | Default |
| `c_name` | Name |
| `c_name_plural` | Plural |
| `c_symbol` | Symbol |
| `c_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

