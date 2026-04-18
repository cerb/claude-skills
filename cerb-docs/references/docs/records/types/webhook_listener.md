---
id: "docs-records-types-webhooklistener"
title: "Webhook Listener Records"
url: "https://cerb.ai/docs/records/types/webhook_listener/"
summary: "This page provides detailed information about Webhook Listener Records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as `guid`, `name`, and `updated_at`, and explains their types and purposes. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive list of fields like `automations_kata`, `guid`, and `record_url`. Additionally, it details the search query fields that can be used to filter webhook listener records, such as `guid:`, `id:`, and `name:`, and lists the worklist columns available for organizing these records, including custom fields and update timestamps. This information is crucial for users looking to integrate and manage webhooks effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Webhook |
| **Name (plural):** | Webhooks |
| **Alias (uri):** | webhook\_listener |
| **Identifier (ID):** | cerberusweb.contexts.webhook\_listener |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `automations_kata` | object | KATA object |
| **x** | **`guid`** | text | The random unique alias of the webhook used in its URL; automatically generated if blank |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this webhook |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `automations_kata` | text | Automations |
| `guid` | text | Guid |
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
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in webhook listener search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `guid:` | text | Url |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on webhook listener worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `w_guid` | Url |
| `w_id` | Id |
| `w_name` | Name |
| `w_updated_at` | Updated |

\< Record Types

