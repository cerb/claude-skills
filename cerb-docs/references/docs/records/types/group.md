---
id: "docs-records-types-group"
title: "Group Records"
url: "https://cerb.ai/docs/records/types/group/"
summary: "This page provides detailed information about the 'Group' record type in Cerb, including its API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and attributes of group records, such as creation and update timestamps, privacy settings, member lists, and email reply configurations. The page also describes how these fields can be used in the Records API, automation dictionaries, and search queries, offering a comprehensive guide for managing group records within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Group |
| **Name (plural):** | Groups |
| **Alias (uri):** | group |
| **Identifier (ID):** | cerberusweb.contexts.group |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `image` | image | The profile image, base64-encoded in data URI format |
| &nbsp; | `is_default` | boolean | Tickets are assigned to the default group when no other routing rules match |
| &nbsp; | `is_private` | boolean | The content in public (`0`) groups is visible to everyone; in private (`1`) groups content is only visible to members |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `members` | text | JSON-encoded array of worker IDs; `[1,2,3]` |
| **x** | **`name`** | text | The name of this group |
| &nbsp; | `reply_address_id` | number | The ID of the email address used when sending replies from this group |
| &nbsp; | `reply_html_template_id` | number | The ID of the default mail template used when sending HTML mail from this group |
| &nbsp; | `reply_personal` | text | The default personal name in the `From:` of replies |
| &nbsp; | `reply_signature_id` | number | The ID of the default signature used when sending replies from this group |
| &nbsp; | `reply_signing_key_id` | number | The private key used to cryptographically sign outgoing mail |
| &nbsp; | `routing_kata` | text | Routing rules in KATA format |
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
| `is_default` | boolean | Default |
| `is_private` | boolean | Private |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `reply_html_template_` | record | Email Template |
| `reply_personal` | text | Send As |
| `reply_signature_` | record | Signature |
| `reply_signature_owner_` | record | Signature Owner |
| `reply_signing_key_` | record | Signing Key |
| `replyto_` | record | Send From |
| `routing_kata` | text | Dao.bucket.routing\_Kata |
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `buckets` | records | Buckets |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `default_bucket_` | record | The group's default bucket |
| `links` | links | Links |
| `members` | records | Members |

### Search Query Fields

These filters are available in group search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `default:` | boolean | Default |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `manager:` | record | Manager |
| `member:` | record | Member |
| `name:` | text | Name |
| `private:` | boolean | Private |
| `send.as:` | text | Send As |
| `send.from.id:` | chooser | Send From |
| `signature.id:` | chooser | Signature |
| `signing.key.id:` | chooser | Signing Key |
| `template.id:` | chooser | Email Template |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on group worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `g_created` | Created |
| `g_id` | Id |
| `g_is_default` | Default |
| `g_is_private` | Private |
| `g_name` | Name |
| `g_reply_address_id` | Send From |
| `g_reply_html_template_id` | Email Template |
| `g_reply_personal` | Send As |
| `g_reply_signature_id` | Signature |
| `g_reply_signing_key_id` | Signing Key |
| `g_updated` | Updated |

\< Record Types

