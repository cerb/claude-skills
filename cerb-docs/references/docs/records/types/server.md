---
id: "docs-records-types-server"
title: "Server Records"
url: "https://cerb.ai/docs/records/types/server/"
summary: "This page provides detailed information about server records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the essential fields available in the Records API, such as creation and update timestamps, server name, and links. The page also describes dictionary placeholders used in automations and API responses, including context, label, and record URL. Additionally, it lists optional placeholders for comments, custom fields, and watchers. The search query fields section details filters for server searches, like comments, creation date, and record links. Lastly, the worklist columns section specifies the columns available for server worklists, including custom fields and server details like ID, name, and timestamps."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Server |
| **Name (plural):** | Servers |
| **Alias (uri):** | server |
| **Identifier (ID):** | cerberusweb.contexts.datacenter.server |

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
| **x** | **`name`** | text | The name of this server |
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
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in server search queries:

| Field | Type | Description |
| --- | --- | --- |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on server worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `s_created` | Created |
| `s_id` | Id |
| `s_name` | Name |
| `s_updated` | Updated |

\< Record Types

