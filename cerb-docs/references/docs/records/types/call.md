---
id: "docs-records-types-call"
title: "Call Records"
url: "https://cerb.ai/docs/records/types/call/"
summary: "This page provides detailed information about the call records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as creation and update timestamps, call resolution status, and phone numbers. The page also describes dictionary placeholders for automations and API responses, offering fields like record type, subject, and links. Additionally, it lists search query fields that can be used to filter call records based on various criteria, such as comments, creation date, and call status. Lastly, it details the columns available in call worklists, which include fields like creation date, call status, and custom fields. This comprehensive guide is essential for managing and utilizing call records effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Call |
| **Name (plural):** | Calls |
| **Alias (uri):** | call |
| **Identifier (ID):** | cerberusweb.contexts.call |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `is_closed` | boolean | Is this call resolved? |
| &nbsp; | `is_outgoing` | boolean | `0` (incoming), `1` (outgoing) |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `phone` | text | The phone number of the caller or target |
| **x** | **`subject`** | text | A brief summary of the call |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created` | date | Created |
| `id` | number | Id |
| `is_closed` | boolean | Is Closed |
| `is_outgoing` | boolean | Is Outgoing |
| `phone` | text | Phone |
| `record_url` | text | Record Url |
| `subject` | text | Subject |
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

These filters are available in call search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isClosed:` | boolean | Is Closed |
| `isOutgoing:` | boolean | Is Outgoing |
| `links:` | links | Record Links |
| `phone:` | text | Phone |
| `subject:` | text | Subject |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on call worklists:

| Column | Description |
| --- | --- |
| `c_created_date` | Created |
| `c_is_closed` | Is Closed |
| `c_is_outgoing` | Is Outgoing |
| `c_phone` | Phone |
| `c_subject` | Subject |
| `c_updated_date` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

