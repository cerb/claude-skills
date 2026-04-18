---
id: "docs-records-types-draft"
title: "Draft Records"
url: "https://cerb.ai/docs/records/types/draft/"
summary: "This page provides detailed information about the draft records in Cerb, including their structure, fields, and usage within the system. It outlines the Records API, specifying the fields available for drafts such as `is_queued`, `name`, `params`, `ticket_id`, and `worker_id`, among others. The page also describes the parameters for different types of drafts, including `mail.compose`, `mail.transactional`, and `ticket.reply/ticket.forward`, detailing the keys and values for each. Additionally, it covers dictionary placeholders for automations and API responses, search query fields for filtering drafts, and worklist columns for organizing draft records. This comprehensive guide is essential for understanding how to manage and utilize draft records within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Draft |
| **Name (plural):** | Drafts |
| **Alias (uri):** | draft |
| **Identifier (ID):** | cerberusweb.contexts.mail.draft |

- Records API
  - params (mail.compose)
  - params (mail.transactional)
  - params (ticket.reply / ticket.forward)

- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `is_queued` | boolean | `1` for true, `0` for false |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `name` | text | The subject line of the draft message |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `queue_delivery_date` | number | (0-4294967296) |
| &nbsp; | `queue_fails` | number | (0-4294967296) |
| &nbsp; | `ticket_id` | number | The ID of the ticket for `ticket.reply` or `ticket.forward` |
| &nbsp; | `to` | text | The `To:` line of the draft message |
| &nbsp; | `token` | text | A random unique token for this draft, copied to the eventual message for tracing |
| **x** | **`type`** | text | The type of draft: `mail.compose`, `mail.transactional`, `ticket.reply`, or `ticket.forward` |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |
| &nbsp; | `worker_id` | number | The ID of the worker who owns the draft |

#### params (mail.compose)

| Req'd | Key | Value |
| --- | --- | --- |
| &nbsp; | `bcc` | The `Bcc:` recipients |
| &nbsp; | `bucket_id` | The bucket ID to move the ticket to |
| &nbsp; | `cc` | The `Cc:` recipients |
| &nbsp; | `content` | The message content |
| &nbsp; | `custom_fields` | An object with custom field IDs as keys and their values |
| &nbsp; | `custom_fields_uri` | A read-only object with custom field URIs as keys and their values |
| &nbsp; | `format` | `parsedown` (Markdown), or blank for plaintext |
| &nbsp; | `file_ids` | An array of attachment IDs |
| **x** | `group_id` | The group ID to move the ticket to |
| &nbsp; | `headers` | An array of email headers to set, with header names as keys |
| &nbsp; | `html_template_id` | An optional HTML template ID if `format` is `parsedown` |
| &nbsp; | `message_custom_fields` | An object with message custom field IDs as keys and their values |
| &nbsp; | `message_custom_fields_uri` | A read-only object with message custom field URIs as keys and their values |
| &nbsp; | `options_gpg_encrypt` | `1` to enable PGP encryption, `0` (or omit) to disable |
| &nbsp; | `options_gpg_sign` | `1` to enable PGP signatures, `0` (or omit) to disable |
| &nbsp; | `org_id` | The org ID to assign |
| &nbsp; | `org_name` | The org name to assign |
| &nbsp; | `owner_id` | The worker ID to assign |
| &nbsp; | `send_at` | The optional timestamp to deliver the message at |
| &nbsp; | `status_id` | `0` (open), `1` (waiting), `2` (closed) |
| &nbsp; | `subject` | The message `Subject:` |
| &nbsp; | `ticket_reopen` | When the status is waiting or closed, the timestamp to reopen at |
| **x** | `to` | The `To:` recipients |

#### params (mail.transactional)

| Req'd | Key | Value |
| --- | --- | --- |
| &nbsp; | `bcc` | The `Bcc:` recipients |
| &nbsp; | `cc` | The `Cc:` recipients |
| &nbsp; | `content` | The message content |
| &nbsp; | `file_ids` | An array of attachment IDs |
| &nbsp; | `format` | `parsedown` (Markdown), or blank for plaintext |
| &nbsp; | `from` | The `From:` sender (uses system default if omitted) |
| &nbsp; | `from_personal` | The personal `From:` sender (uses system default if omitted) |
| &nbsp; | `headers` | An array of email headers to set, with header names as keys |
| &nbsp; | `html_template_id` | An optional HTML template ID if `format` is `parsedown` |
| &nbsp; | `options_gpg_encrypt` | `1` to enable PGP encryption, `0` (or omit) to disable |
| &nbsp; | `options_gpg_sign` | `1` to enable PGP signatures, `0` (or omit) to disable |
| &nbsp; | `reply_to` | The optional `Reply-To:` |
| &nbsp; | `return_path` | The optional `Return-Path:` |
| **x** | `subject` | The message `Subject:` |
| **x** | `to` | The `To:` recipients |

#### params (ticket.reply / ticket.forward)

| Req'd | Key | Value |
| --- | --- | --- |
| &nbsp; | `bcc` | The `Bcc:` recipients |
| &nbsp; | `bucket_id` | The bucket ID to move the ticket to |
| &nbsp; | `cc` | The `Cc:` recipients |
| &nbsp; | `content` | The message content |
| &nbsp; | `custom_fields` | An object with custom field IDs as keys and their values |
| &nbsp; | `custom_fields_uri` | A read-only object with custom field URIs as keys and their values |
| &nbsp; | `file_ids` | An array of attachment IDs |
| &nbsp; | `format` | `parsedown` (Markdown), or blank for plaintext |
| &nbsp; | `group_id` | The group ID to move the ticket to |
| &nbsp; | `headers` | An array of email headers to set, with header names as keys |
| &nbsp; | `html_template_id` | An optional HTML template ID if `format` is `parsedown` |
| &nbsp; | `in_reply_message_id` | The message ID being responded to |
| &nbsp; | `is_autoreply` | `1` to avoid saving a copy of the reply on the ticket, `0` (or omit) to include |
| &nbsp; | `message_custom_fields` | An object with message custom field IDs as keys and their values |
| &nbsp; | `message_custom_fields_uri` | A read-only object with message custom field URIs as keys and their values |
| &nbsp; | `options_gpg_encrypt` | `1` to enable PGP encryption, `0` (or omit) to disable |
| &nbsp; | `options_gpg_sign` | `1` to enable PGP signatures, `0` (or omit) to disable |
| &nbsp; | `owner_id` | The worker ID to assign |
| &nbsp; | `send_at` | The optional timestamp to deliver the message at |
| &nbsp; | `status_id` | `0` (open), `1` (waiting), `2` (closed) |
| &nbsp; | `subject` | The message `Subject:` |
| &nbsp; | `ticket_reopen` | When the status is waiting or closed, the timestamp to reopen at |
| &nbsp; | `to` | The `To:` recipients |

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
| `params` | dictionary | Params |
| `ticket_` | record | Ticket |
| `to` | text | To |
| `token` | text | Token |
| `type` | text | Type |
| `updated` | date | Updated |
| `worker_` | record | Worker |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |

### Search Query Fields

These filters are available in draft search queries:

| Field | Type | Description |
| --- | --- | --- |
| `id:` | number | Id |
| `is.queued:` | boolean | Is Queued |
| `name:` | text | Name |
| `queue.deliverAt:` | date | Delivery Date |
| `queue.fails:` | number | # Fails |
| `ticket.id:` | chooser | Ticket Id |
| `to:` | text | To |
| `token:` | text | Token |
| `type:` | text | Message Type |
| `updated:` | date | Updated |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on draft worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_hint_to` | To |
| `m_id` | Id |
| `m_is_queued` | Is Queued |
| `m_name` | Name |
| `m_queue_delivery_date` | Delivery Date |
| `m_queue_fails` | # Fails |
| `m_token` | Token |
| `m_type` | Message Type |
| `m_updated` | Updated |
| `m_worker_id` | Worker |

\< Record Types

