---
id: "docs-records-types-maildeliverylog"
title: "Email Delivery Log Records"
url: "https://cerb.ai/docs/records/types/mail_delivery_log/"
summary: "This page provides detailed information about the Email Delivery Log records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for creating and managing email delivery logs. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive guide to the available fields and their types. Additionally, it details the search query fields that can be used to filter email delivery logs, as well as the worklist columns that can be displayed in email delivery log worklists. This information is crucial for users looking to effectively manage and utilize email delivery logs within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Delivery Log |
| **Name (plural):** | Email Delivery Logs |
| **Alias (uri):** | mail\_delivery\_log |
| **Identifier (ID):** | cerb.contexts.mail.delivery.log |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `from_id` | number | &nbsp; |
| &nbsp; | `header_message_id` | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mail_transport_id` | number | &nbsp; |
| &nbsp; | `status_id` | number | (0-2) |
| &nbsp; | `status_message` | text | &nbsp; |
| &nbsp; | `subject` | text | &nbsp; |
| &nbsp; | `to` | text | &nbsp; |
| &nbsp; | `type` | text | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `header_message_id` | text | Header Message-Id |
| `id` | number | Id |
| `record_url` | text | Record Url |
| `status_id` | number | Status |
| `status_message` | text | Status Message |
| `subject` | text | Subject |
| `to` | text | To |
| `type` | text | Type |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `properties` | object | Properties |

### Search Query Fields

These filters are available in email delivery log search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `from:` | record | From |
| `from.id:` | chooser | From |
| `header.messageId:` | text | Header Message-Id |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `mailTransport:` | record | Mailtransport |
| `mailTransport.id:` | chooser | Email Transport |
| `status:` | virtual | Status |
| `status.id:` | number | Status |
| `subject:` | text | Subject |
| `to:` | text | To |
| `type:` | text | Type |

### Worklist Columns

These columns are available on email delivery log worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_created_at` | Created |
| `m_from_id` | From |
| `m_header_message_id` | Header Message-Id |
| `m_id` | Id |
| `m_mail_transport_id` | Email Transport |
| `m_status_id` | Status |
| `m_status_message` | Status Message |
| `m_subject` | Subject |
| `m_to` | To |
| `m_type` | Type |

\< Record Types

