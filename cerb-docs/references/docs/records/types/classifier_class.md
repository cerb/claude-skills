---
id: "docs-records-types-classifierclass"
title: "Classifier Classification Records"
url: "https://cerb.ai/docs/records/types/classifier_class/"
summary: "This page provides detailed information about the classification records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, which are essential for managing classifications, such as `classifier_id`, `name`, and `updated_at`. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a range of fields like `_context`, `id`, and `record_url`. Additionally, it covers search query fields that facilitate filtering classification records based on criteria like `classifier`, `id`, and `name`. Lastly, it lists the worklist columns available for viewing classification data, including `c_classifier_id`, `c_name`, and `c_updated_at`, providing a comprehensive guide for users to effectively manage and utilize classification records in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Classification |
| **Name (plural):** | Classifications |
| **Alias (uri):** | classifier\_class |
| **Identifier (ID):** | cerberusweb.contexts.classifier.class |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`classifier_id`** | number | The ID of the parent classifier |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this classification |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `classifier_` | record | Classifier |
| `classifier_owner_` | record | Classifier Owner |
| `id` | number | Id |
| `name` | text | Name |
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

These filters are available in classifier classification search queries:

| Field | Type | Description |
| --- | --- | --- |
| `classifier:` | record | Classifier |
| `classifier.id:` | chooser | Classifier |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on classifier classification worklists:

| Column | Description |
| --- | --- |
| `c_classifier_id` | Classifier |
| `c_dictionary_size` | Dictionary Size |
| `c_id` | Id |
| `c_name` | Name |
| `c_training_count` | Examples |
| `c_updated_at` | Updated |
| `cf_<id>` | Custom Field |

\< Record Types

