---
id: "docs-records-types-mailinboundlog"
title: "Email Inbound Log Records"
url: "https://cerb.ai/docs/records/types/mail_inbound_log/"
summary: "This page provides detailed information about the Email Inbound Log records in Cerb. It outlines the fields available in the Records API, including timestamps, message IDs, and status information. The page also describes dictionary placeholders for use in automations, snippets, and API responses, offering fields like record type, status, and subject. Additionally, it lists search query fields that can be used to filter email inbound logs based on criteria such as creation date, mailbox, and ticket ID. Lastly, it details the worklist columns available for organizing and displaying email inbound log data, including custom fields and message details."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Inbound Log |
| **Name (plural):** | Email Inbound Logs |
| **Alias (uri):** | mail\_inbound\_log |
| **Identifier (ID):** | cerb.contexts.mail.inbound.log |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `events_log_json` | text | &nbsp; |
| &nbsp; | `from_id` | number | &nbsp; |
| &nbsp; | `header_message_id` | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mailbox_id` | number | &nbsp; |
| &nbsp; | `message_id` | number | &nbsp; |
| &nbsp; | `parse_time_ms` | number | (0-4294967296) |
| &nbsp; | `status_id` | number | (0-2) |
| &nbsp; | `status_message` | text | &nbsp; |
| &nbsp; | `subject` | text | &nbsp; |
| &nbsp; | `ticket_id` | number | &nbsp; |
| &nbsp; | `to` | text | &nbsp; |

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
| `parse_time_ms` | number | Parse Time (Ms) |
| `record_url` | text | Record Url |
| `status_id` | number | Status |
| `status_message` | text | Status Message |
| `subject` | text | Subject |
| `to` | text | To |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `events_log` | object[] | Events Log |
| `links` | links | Links |

### Search Query Fields

These filters are available in email inbound log search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `from:` | record | From |
| `from.id:` | chooser | From |
| `header.messageId:` | text | Header Message-Id |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `mailbox:` | record | Mailbox |
| `mailbox.id:` | chooser | Mailbox |
| `message:` | record | Message |
| `message.id:` | chooser | Message |
| `parseTime.ms:` | number | Parse Time (Ms) |
| `status:` | virtual | Status |
| `status.message:` | text | Status Message |
| `subject:` | text | Subject |
| `ticket:` | record | Ticket |
| `ticket.id:` | chooser | Ticket |
| `to:` | text | To |

### Worklist Columns

These columns are available on email inbound log worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_created_at` | Created |
| `m_from_id` | From |
| `m_header_message_id` | Header Message-Id |
| `m_id` | Id |
| `m_mailbox_id` | Mailbox |
| `m_message_id` | Message |
| `m_parse_time_ms` | Parse Time (Ms) |
| `m_status_id` | Status |
| `m_status_message` | Status Message |
| `m_subject` | Subject |
| `m_ticket_id` | Ticket |
| `m_to` | To |

\< Record Types

