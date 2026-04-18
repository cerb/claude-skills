---
id: "docs-records-types-classifier"
title: "Classifier Records"
url: "https://cerb.ai/docs/records/types/classifier/"
summary: "This page provides detailed information about classifier records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for creating and managing classifier records, such as `name`, `owner__context`, and timestamps for creation and updates. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `id`, `name`, and `record_url`. Additionally, it covers search query fields that facilitate filtering classifier records based on various criteria, including creation date, owner, and links. Lastly, it lists the worklist columns available for organizing and displaying classifier records, such as `c_created_at`, `c_name`, and custom fields. This comprehensive guide is crucial for users looking to effectively manage and utilize classifier records within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Classifier |
| **Name (plural):** | Classifiers |
| **Alias (uri):** | classifier |
| **Identifier (ID):** | cerberusweb.contexts.classifier |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this classifier |
| **x** | **`owner__context`** | context | The record type of this classifier's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this classifier's owner |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `id` | number | Id |
| `name` | text | Name |
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in classifier search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner |
| `owner.bot:` | record | Owner |
| `owner.group:` | record | Owner |
| `owner.role:` | record | Owner |
| `owner.worker:` | record | Owner |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on classifier worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `c_created_at` | Created |
| `c_dictionary_size` | Dictionary Size |
| `c_id` | Id |
| `c_name` | Name |
| `c_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

