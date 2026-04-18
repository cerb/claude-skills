---
id: "docs-records-types-opportunity"
title: "Opportunity Records"
url: "https://cerb.ai/docs/records/types/opportunity/"
summary: "This page provides detailed information about Opportunity Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as amount, currency, status, and timestamps for creation and updates. The page also describes dictionary placeholders for automations and API responses, offering fields like context, label, and record URL. Additionally, it covers search query fields that allow filtering opportunities by attributes like amount, status, and creation date. Lastly, it lists the worklist columns available for displaying opportunity data, including custom fields, closed date, and status."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Opportunity |
| **Name (plural):** | Opportunities |
| **Alias (uri):** | opportunity |
| **Identifier (ID):** | cerberusweb.contexts.opportunity |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `amount` | float | The amount of the opportunity in the given currency |
| &nbsp; | `amount_currency_id` | number | The ID of the currency |
| &nbsp; | `closed_at` | timestamp | &nbsp; |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `status` | text | `open`, `closed_won`, `closed_lost`; alternative to `status_id` |
| &nbsp; | `status_id` | number | `0` (open), `1` (closed/won), `2` (closed/lost); alternaitve to `status` |
| **x** | **`title`** | text | The name of the opportunity |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `amount` | currency | Amount |
| `amount_` | record | Amount Label |
| `amount_currency_` | record | Currency |
| `closed_at` | date | Closed At |
| `created` | date | Created |
| `id` | number | Id |
| `record_url` | text | Record Url |
| `status` | text | Status |
| `title` | text | Title |
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in opportunity search queries:

| Field | Type | Description |
| --- | --- | --- |
| `amount:` | number | Amount |
| `closedDate:` | date | Closed Date |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Created |
| `currency.id:` | chooser | Currency |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Title |
| `status:` | number | Status |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on opportunity worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `o_closed_date` | Closed Date |
| `o_created_date` | Created |
| `o_currency_amount` | Amount |
| `o_currency_id` | Currency |
| `o_id` | Id |
| `o_name` | Title |
| `o_status_id` | Status |
| `o_updated_date` | Updated |

\< Record Types

