---
id: "docs-records-types-address"
title: "Email Address Records"
url: "https://cerb.ai/docs/records/types/address/"
summary: "This page provides detailed information about email address records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as contact ID, email, host, and various status indicators like whether an email is banned, defunct, or trusted. The page also describes dictionary placeholders for automations and API responses, offering fields like address, contact, and organization details. Additionally, it covers search query fields that allow filtering email addresses based on criteria like creation date, email content, and associated records. Lastly, it lists worklist columns that can be used to organize and display email address data, including fields for contact, email, host, and custom fields."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Address |
| **Name (plural):** | Email Addresses |
| **Alias (uri):** | address |
| **Identifier (ID):** | cerberusweb.contexts.address |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `contact_id` | number | The contact linked to this email |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| **x** | **`email`** | text | An email address |
| &nbsp; | `host` | text | The hostname of the email address |
| &nbsp; | `is_banned` | boolean | Is incoming email blocked? |
| &nbsp; | `is_defunct` | boolean | Is this address non-deliverable? |
| &nbsp; | `is_trusted` | boolean | Is this sender trusted to display external images and links? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mail_transport_id` | number | If this address is used for outgoing mail, the mail transport to use; otherwise empty |
| &nbsp; | `org` | text | The exact name of the organization linked to this email address; alternative to `org_id` |
| &nbsp; | `org_id` | number | The organization linked to this email |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |
| &nbsp; | `worker_id` | number | Is this address owned by a worker? |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `address` | text | Address |
| `contact_` | record | Contact |
| `created_at` | date | Created |
| `full_name` | text | Full Name |
| `host` | text | Host |
| `id` | number | Id |
| `is_banned` | boolean | Is Banned |
| `is_contact` | boolean | Is Contact |
| `is_defunct` | boolean | Is Defunct |
| `is_trusted` | boolean | Is Trusted |
| `mail_transport_` | record | Mail Transport |
| `num_nonspam` | number | # Nonspam |
| `num_spam` | number | # Spam |
| `org_` | record | Org |
| `record_url` | text | Record Url |
| `updated` | date | Updated |
| `worker_` | record | Worker |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `last_recipient_message` | record | Latest Message Received To |
| `last_sender_message` | record | Latest Message Sent From |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in email address search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `contact:` | record | Contact |
| `contact.id:` | chooser | Contact |
| `created:` | date | Created |
| `email:` | text | Email |
| `fieldset:` | record | Fieldset |
| `host:` | text | Host |
| `id:` | number | Id |
| `isBanned:` | boolean | Is Banned |
| `isDefunct:` | boolean | Is Defunct |
| `isTrusted:` | boolean | Is Trusted |
| `links:` | links | Record Links |
| `mailTransport.id:` | chooser | Email Transport |
| `nonspam:` | number | # Nonspam |
| `org:` | record | Org |
| `org.id:` | chooser | Organization Id |
| `spam:` | number | # Spam |
| `ticket:` | record | Ticket |
| `ticket.id:` | chooser | Ticket |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on email address worklists:

| Column | Description |
| --- | --- |
| `a_contact_id` | Contact |
| `a_created_at` | Created |
| `a_email` | Email |
| `a_host` | Host |
| `a_id` | Id |
| `a_is_banned` | Is Banned |
| `a_is_defunct` | Is Defunct |
| `a_is_trusted` | Is Trusted |
| `a_mail_transport_id` | Email Transport |
| `a_num_nonspam` | # Nonspam |
| `a_num_spam` | # Spam |
| `a_updated` | Updated |
| `a_worker_id` | Worker |
| `cf_<id>` | Custom Field |
| `o_name` | Organization |

\< Record Types

