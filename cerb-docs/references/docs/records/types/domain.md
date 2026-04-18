---
id: "docs-records-types-domain"
title: "Domain Records"
url: "https://cerb.ai/docs/records/types/domain/"
summary: "This page provides detailed information about domain records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as creation and update timestamps, domain name, and server ID. The page also describes dictionary placeholders for automations and API responses, offering fields like context, label, and record URL. Additionally, it lists search query fields for filtering domain records based on attributes like comments, creation date, and server details. Lastly, it specifies worklist columns for displaying domain information, including custom fields and timestamps. This comprehensive guide is essential for managing and interacting with domain records in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Domain |
| **Name (plural):** | Domains |
| **Alias (uri):** | domain |
| **Identifier (ID):** | cerberusweb.contexts.datacenter.domain |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this domain |
| &nbsp; | `server_id` | number | The ID of the server linked to this domain |
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
| `name` | text | Name |
| `record_url` | text | Record Url |
| `server_` | record | Server |
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `contacts` | records | Contacts |
| `contacts_list` | text | Contacts List |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in domain search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `server:` | record | Server |
| `server.id:` | chooser | Server |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on domain worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `w_created` | Created |
| `w_id` | Id |
| `w_name` | Name |
| `w_server_id` | Server |
| `w_updated` | Updated |

\< Record Types

