---
id: "docs-records-types-mailbox"
title: "Mailbox Account Records"
url: "https://cerb.ai/docs/records/types/mailbox/"
summary: "This page provides detailed information about the structure and functionality of email mailbox account records in Cerb. It outlines the fields available in the Records API, including essential fields like host, name, and username, and describes their types and purposes. The page also explains dictionary placeholders used in automations and API responses, offering a comprehensive list of fields and their descriptions. Additionally, it covers search query fields that can be used to filter mailbox accounts and lists the columns available in mailbox account worklists, which help in organizing and managing email mailbox data effectively."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Mailbox |
| **Name (plural):** | Email Mailboxes |
| **Alias (uri):** | mailbox |
| **Identifier (ID):** | cerberusweb.contexts.mailbox |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `checked_at` | timestamp | The date/time this mailbox was last checked for new messages |
| &nbsp; | `connected_account_id` | number | The optional connected account to use for XOAUTH2 |
| **x** | **`host`** | text | The mail server hostname |
| &nbsp; | `is_enabled` | boolean | Is this mailbox enabled? `1` for true and `0` for false |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `max_msg_size_kb` | number | The maximum message size to download (in kilobytes); `0` to disable limits |
| **x** | **`name`** | text | The name of this email mailbox |
| &nbsp; | `num_fails` | number | The number of consecutive failures |
| &nbsp; | `password` | text | The mailbox password |
| &nbsp; | `port` | number | The port to connect to; e.g. `587` |
| &nbsp; | `protocol` | text | The protocol to use: `pop3`, `pop3-ssl`, `imap`, `imap-ssl` |
| &nbsp; | `timeout_secs` | number | The socket timeout in seconds when downloading mail |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| **x** | **`username`** | text | The mailbox username |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `checked_at` | date | Checked At |
| `connected_account_id` | number | Connected Account |
| `host` | text | Host |
| `id` | number | Id |
| `is_enabled` | boolean | Enabled |
| `max_msg_size_kb` | number | Max Msg Size |
| `name` | text | Name |
| `num_fails` | number | Num Fails |
| `port` | number | Port |
| `protocol` | text | Protocol |
| `record_url` | text | Record Url |
| `timeout_secs` | number | Timeout Secs |
| `updated_at` | date | Updated |
| `username` | text | Username |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in mailbox account search queries:

| Field | Type | Description |
| --- | --- | --- |
| `checkedAt:` | date | Checked At |
| `enabled:` | boolean | Enabled |
| `fail.count:` | number | Num Fails |
| `fieldset:` | record | Fieldset |
| `host:` | text | Host |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `protocol:` | text | Protocol |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on mailbox account worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `p_checked_at` | Checked At |
| `p_connected_account_id` | Connected Account |
| `p_delay_until` | Delay Until |
| `p_enabled` | Enabled |
| `p_host` | Host |
| `p_id` | Id |
| `p_max_msg_size_kb` | Max Msg Size |
| `p_name` | Name |
| `p_num_fails` | Num Fails |
| `p_port` | Port |
| `p_protocol` | Protocol |
| `p_timeout_secs` | Timeout Secs |
| `p_updated_at` | Updated |
| `p_username` | User |

\< Record Types

