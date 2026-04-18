---
id: "docs-records-types-htmltemplate"
title: "Email Template Records"
url: "https://cerb.ai/docs/records/types/html_template/"
summary: "This page provides detailed information about email template records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as content, name, owner context, and updated timestamp, which are essential for managing email templates. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like content, name, and record URL. Additionally, it covers search query fields that allow users to filter email templates based on various criteria, such as comments, content, and updated date. Lastly, it lists the worklist columns available for organizing and displaying email templates, including custom fields, content, and signature information. This comprehensive guide is crucial for users looking to effectively manage and utilize email templates within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Template |
| **Name (plural):** | Email Templates |
| **Alias (uri):** | html\_template |
| **Identifier (ID):** | cerberusweb.contexts.mail.html\_template |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `content` | text | The content of the template |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this email template |
| **x** | **`owner__context`** | context | The record type of this email template's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this email template's owner |
| &nbsp; | `signature_id` | number | The optional email signature of this template |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `content` | text | Content |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `signature_` | record | Signature |
| `signature_owner_` | record | Signature Owner |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `attachments` | attachments | Attachments |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in email template search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `content:` | text | Content |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `signature.id:` | number | Signature |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on email template worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_content` | Content |
| `m_id` | Id |
| `m_name` | Name |
| `m_signature_id` | Signature |
| `m_updated_at` | Updated |

\< Record Types

