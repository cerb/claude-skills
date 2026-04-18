---
id: "docs-records-types-bucket"
title: "Bucket Records"
url: "https://cerb.ai/docs/records/types/bucket/"
summary: "This page provides detailed information about Bucket records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for managing bucket records, such as group ID, name, and reply settings. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like record type, name, and updated timestamp. Additionally, it covers search query fields that allow users to filter bucket records based on various criteria, such as group, name, and email template. Lastly, it lists the worklist columns available for displaying bucket records, including group ID, name, and custom fields, providing a comprehensive guide for managing and utilizing bucket records in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Bucket |
| **Name (plural):** | Buckets |
| **Alias (uri):** | bucket |
| **Identifier (ID):** | cerberusweb.contexts.bucket |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`group_id`** | number | The ID of the parent group containing this bucket |
| &nbsp; | `is_default` | boolean | Is this the default (inbox) bucket of the group? |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this bucket |
| &nbsp; | `reply_address_id` | number | The ID of the email address used when sending replies from this bucket |
| &nbsp; | `reply_html_template_id` | number | The ID of the default mail template used when sending HTML mail from this bucket |
| &nbsp; | `reply_personal` | text | The default personal name in the `From:` of replies |
| &nbsp; | `reply_signature_id` | number | The ID of the default signature used when sending replies from this bucket |
| &nbsp; | `reply_signing_key_id` | number | The private key used when signing outgoing mail from this bucket |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `group_` | record | Group |
| `id` | number | Id |
| `is_default` | boolean | Default |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `reply_html_template_` | record | Email Template |
| `reply_personal` | text | Send As |
| `reply_signature_` | record | Signature |
| `reply_signature_owner_` | record | Signature Owner |
| `reply_signing_key_` | record | Signing Key |
| `replyto_` | record | Send From |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in bucket search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `group:` | record | Group |
| `group.id:` | chooser | Group |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `send.as:` | text | Send As |
| `send.from.id:` | chooser | Send From |
| `signature.id:` | chooser | Signature |
| `signing.key.id:` | chooser | Signing Key |
| `template.id:` | chooser | Email Template |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on bucket worklists:

| Column | Description |
| --- | --- |
| `b_group_id` | Group |
| `b_id` | Id |
| `b_is_default` | Default |
| `b_name` | Name |
| `b_reply_address_id` | Send From |
| `b_reply_html_template_id` | Email Template |
| `b_reply_personal` | Send As |
| `b_reply_signature_id` | Signature |
| `b_reply_signing_key_id` | Signing Key |
| `b_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

