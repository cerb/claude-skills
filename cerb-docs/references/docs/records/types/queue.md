---
id: "docs-records-types-queue"
title: "Queue Records"
url: "https://cerb.ai/docs/records/types/queue/"
summary: "This page provides detailed information about Queue Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as creation and update timestamps, links, and the queue name. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a range of fields like context, label, and record URL. Additionally, it covers search query fields that can be used to filter queue records based on criteria like creation date, fieldset, and watchers. Lastly, it lists the worklist columns available for displaying queue records, including custom fields and standard attributes like ID, name, and timestamps."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Queue |
| **Name (plural):** | Queues |
| **Alias (uri):** | queue |
| **Identifier (ID):** | cerb.contexts.queue |

- [Records API](#records-api)
- [Dictionary Placeholders](#dictionary-placeholders)
- [Search Query Fields](#search-query-fields)
- [Worklist Columns](#worklist-columns)

### Records API

These fields are available in the [Records API](/docs/api/endpoints/records/) and [packages](/docs/packages/):

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | [timestamp](/docs/records/fields/types/timestamp/) | The date/time when this record was created |
| &nbsp; | `links` | [links](/docs/records/fields/types/links/) | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | [text](/docs/records/fields/types/text/) | The name of this queue |
| &nbsp; | `updated_at` | [timestamp](/docs/records/fields/types/timestamp/) | The date/time when this record was last modified |

### Dictionary Placeholders

These [placeholders](/docs/scripting/variables/#placeholders) are available in [dictionaries](/docs/guide/developers/dictionaries/) for [automations](/docs/automations/), [snippets](/docs/snippets/), and [API](/docs/api/) responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | [Record type](/docs/records/types/) extension ID |
| `_label` | text | Label |
| `_type` | text | [Record type](/docs/records/types/) alias |
| `created_at` | date | Created |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in [dictionaries](/docs/guide/developers/dictionaries/#key-expansion) and the [API](/docs/api/responses/#expanding-keys-in-api-requests):

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | [Comment](/docs/records/types/comments/) count on the record |
| `comments` | comments | [Comments](/docs/guide/developers/dictionaries/#key-expansion) |
| `custom_<id>` | mixed | [Custom Fields](/docs/guide/developers/dictionaries/#key-expansion) |
| `links` | links | [Links](/docs/guide/developers/dictionaries/#key-expansion) |
| `watchers` | watchers | [Watchers](/docs/guide/developers/dictionaries/#key-expansion) |

### Search Query Fields

These [filters](/docs/search/#filters) are available in queue [search queries](/docs/search/):

| Field | Type | Description |
| --- | --- | --- |
| `created:` | [date](/docs/search/#dates) | Created |
| `fieldset:` | [record](/docs/search/#deep-search) | [Fieldset](/docs/records/types/custom_fieldset/) |
| `id:` | [number](/docs/search/#numbers) | Id |
| `links:` | [links](/docs/search/#links) | Record Links |
| `name:` | [text](/docs/search/#text) | Name |
| `updated:` | [date](/docs/search/#dates) | Updated |
| `watchers:` | [record](/docs/search/#deep-search) | [Watchers](/docs/records/types/worker/) |

### Worklist Columns

These columns are available on queue [worklists](/docs/worklists/):

| Column | Description |
| --- | --- |
| `cf_<id>` | [Custom Field](/docs/records/types/custom_field/) |
| `q_created_at` | Created |
| `q_id` | Id |
| `q_name` | Name |
| `q_updated_at` | Updated |

[\< Record Types](/docs/records/types/)

