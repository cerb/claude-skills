---
id: "docs-records-types-emailsignature"
title: "Email Signature Records"
url: "https://cerb.ai/docs/records/types/email_signature/"
summary: "This page provides detailed information about email signature records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as name, owner context, and signature templates, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also describes the search query fields that can be used to filter email signature records and lists the worklist columns available for organizing these records. Additionally, it provides guidance on linking and unlinking records and managing custom fields and comments."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Signature |
| **Name (plural):** | Email Signatures |
| **Alias (uri):** | email\_signature |
| **Identifier (ID):** | cerberusweb.contexts.email.signature |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this email signature |
| **x** | **`owner__context`** | context | The record type of this email signature's owner: `app`, `role`, `group`, or `worker` |
| &nbsp; | `owner_id` | number | The ID of this email signature's owner |
| **x** | **`signature`** | text | The template of the signature |
| &nbsp; | `signature_html` | text | The HTML template of the signature |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `name` | text | Name |
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `signature` | text | Signature |
| `signature_html` | text | Signature (Html) |
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

These filters are available in email signature search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner |
| `owner.bot:` | record | Owner |
| `owner.group:` | record | Owner |
| `owner.role:` | record | Owner |
| `owner.worker:` | record | Owner |
| `signature:` | text | Signature |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on email signature worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `cf_<id>` | Custom Field |
| `e_id` | Id |
| `e_name` | Name |
| `e_signature` | Signature |
| `e_updated_at` | Updated |

\< Record Types

