---
id: "docs-records-types-mailtransport"
title: "Email Transport Records"
url: "https://cerb.ai/docs/records/types/mail_transport/"
summary: "This page provides detailed information about Email Transport records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for creating and managing email transport records, such as `created`, `extension_id`, `name`, and `updated_at`. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `id`, `name`, and `record_url`. Additionally, it lists the search query fields that can be used to filter email transport records, such as `created`, `id`, and `name`. Lastly, it details the worklist columns available for organizing and displaying email transport records, including custom fields and standard fields like `m_created_at` and `m_name`."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Transport |
| **Name (plural):** | Email Transports |
| **Alias (uri):** | mail\_transport |
| **Identifier (ID):** | cerberusweb.contexts.mail.transport |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| **x** | **`extension_id`** | text | Mail Transport Type |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this email transport |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created` | date | Created |
| `extension_id` | text | Type |
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

These filters are available in email transport search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `type:` | text | Extension |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on email transport worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_created_at` | Created |
| `m_extension_id` | Extension |
| `m_id` | Id |
| `m_name` | Name |
| `m_updated_at` | Updated |

\< Record Types

