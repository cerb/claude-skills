---
id: "docs-records-types-message"
title: "Message Records"
url: "https://cerb.ai/docs/records/types/message/"
summary: "This page provides detailed information about message records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, which are essential for managing message content, headers, sender information, and related metadata. The page also describes dictionary placeholders used in automations and API responses, offering a comprehensive list of fields and their types. Additionally, it covers search query fields that facilitate filtering messages based on various criteria such as content, sender, and encryption status. Lastly, it details the worklist columns available for organizing and displaying message data, highlighting key attributes like response time, broadcast status, and associated ticket information. This resource is crucial for developers and users looking to integrate or utilize message records effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Message |
| **Name (plural):** | Messages |
| **Alias (uri):** | message |
| **Identifier (ID):** | cerberusweb.contexts.message |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`content`** | text | Message content |
| &nbsp; | `content_html` | text | Optional alternative content for the HTML version of a message |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `hash_header_message_id` | text | A SHA-1 hash of the `Message-Id:` header; used for message threading |
| **x** | **`headers`** | text | Message headers |
| &nbsp; | `html_attachment_id` | number | The attachment ID containing the HTML message content |
| &nbsp; | `is_broadcast` | boolean | Was this message sent using the broadcast feature? |
| &nbsp; | `is_not_sent` | boolean | Was this message saved without sending? |
| &nbsp; | `is_outgoing` | boolean | Was this an outgoing reply from a worker? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `response_time` | number | Response time in seconds |
| &nbsp; | `sender` | text | The email address of the sender; alternative to `sender_id` |
| **x** | **`sender_id`** | number | The ID of the sender's email address record |
| &nbsp; | `storage_size` | number | Size of the message in bytes |
| **x** | **`ticket_id`** | number | The ID of the message's ticket record |
| &nbsp; | `ticket_mask` | text | The parent ticket mask; alternative to `ticket_id` |
| &nbsp; | `token` | text | A random unique identifier for the message (synchronized with draft) |
| &nbsp; | `was_encrypted` | boolean | Was the message sent encrypted? |
| &nbsp; | `worker` | text | The worker who sent the message (if any); alternative to `worker_id` |
| &nbsp; | `worker_id` | number | If outgoing, the ID of the worker who sent the message |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created` | date | Created |
| `html_attachment_id` | number | Html Attachment Id |
| `id` | number | Id |
| `is_broadcast` | boolean | Is Broadcast |
| `is_not_sent` | boolean | Is Not Sent |
| `is_outgoing` | boolean | Is Outgoing |
| `record_url` | text | Record Url |
| `response_time` | seconds | Response Time |
| `sender_` | record | Sender |
| `signed_at` | date | Signed At |
| `signed_key_fingerprint` | text | Signed By |
| `storage_size` | number | Size (Bytes) |
| `ticket_` | record | Ticket |
| `token` | text | Token |
| `was_encrypted` | boolean | Is Encrypted |
| `worker_` | record | Sender Worker |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `attachments` | attachments | Attachments |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `content` | text | Content |
| `content_html` | text | Content (Html) |
| `custom_<id>` | mixed | Custom Fields |
| `headers` | hashmap | Headers |
| `links` | links | Links |
| `reply_cc` | text | `Cc:` recipients (comma-separated) |
| `reply_to` | text | `To:` recipients (comma-separated) |

### Search Query Fields

These filters are available in message search queries:

| Field | Type | Description |
| --- | --- | --- |
| `attachments:` | record | Attachments |
| `content:` | fulltext | Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `header.cc:` | text | Cc |
| `header.deliveredTo:` | text | Delivered-To |
| `header.from:` | text | From |
| `header.messageId:` | text | Message-Id Header |
| `header.to:` | text | To |
| `id:` | context | Id |
| `isBroadcast:` | boolean | Is Broadcast |
| `isEncrypted:` | boolean | Is Encrypted |
| `isNotSent:` | boolean | Is Not Sent |
| `isOutgoing:` | boolean | Is Outgoing |
| `links:` | links | Record Links |
| `notes:` | record | Notes |
| `responseTime:` | number | Response Time |
| `sender:` | record | Sender |
| `sender.id:` | chooser | Sender |
| `signed.at:` | date | Signed At |
| `signed.fingerprint:` | text | Signed By |
| `size:` | number | Size |
| `ticket:` | record | Ticket |
| `ticket.bucket.id:` | chooser | Bucket |
| `ticket.bucket.name:` | chooser | Bucket |
| `ticket.group.id:` | chooser | Group |
| `ticket.group.name:` | chooser | Bucket |
| `ticket.id:` | chooser | Ticket Id |
| `token:` | text | Token |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on message worklists:

| Column | Description |
| --- | --- |
| `*_has_fieldset` | Fieldset |
| `a_email` | Email |
| `cf_<id>` | Custom Field |
| `m_address_id` | Sender |
| `m_created_date` | Created |
| `m_is_broadcast` | Is Broadcast |
| `m_is_not_sent` | Is Not Sent |
| `m_is_outgoing` | Is Outgoing |
| `m_response_time` | Response Time |
| `m_signed_at` | Signed At |
| `m_signed_key_fingerprint` | Signed By |
| `m_ticket_id` | Ticket Id |
| `m_token` | Token |
| `m_was_encrypted` | Is Encrypted |
| `m_worker_id` | Worker |
| `t_bucket_id` | Bucket |
| `t_group_id` | Group |
| `t_mask` | Mask |
| `t_subject` | Subject |

\< Record Types

