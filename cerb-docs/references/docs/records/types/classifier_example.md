---
id: "docs-records-types-classifierexample"
title: "Classifier Example Records"
url: "https://cerb.ai/docs/records/types/classifier_example/"
summary: "This page provides detailed information about the structure and functionality of 'Classifier Example' records in Cerb. It outlines the fields available in the Records API, including required fields like `classifier_id` and `expression`, and optional fields such as `links` and `updated_at`. The page also describes dictionary placeholders used in automations, snippets, and API responses, offering a comprehensive list of fields like `_context`, `class_`, and `record_url`. Additionally, it details search query fields that can be used to filter classifier example records, such as `class:`, `classifier:`, and `expression:`. Lastly, it lists the worklist columns available for organizing classifier example data, including `c_class_id`, `c_classifier_id`, and `c_updated_at`. This information is crucial for users looking to manage and utilize classifier examples effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Classifier Example |
| **Name (plural):** | Classifier Examples |
| **Alias (uri):** | classifier\_example |
| **Identifier (ID):** | cerberusweb.contexts.classifier.example |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `class_id` | number | The ID of the classification this example trains |
| **x** | **`classifier_id`** | number | The ID of the classifier this example belongs to |
| **x** | **`expression`** | text | The expression used for training the classifier |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `class_` | record | Classification |
| `classifier_` | record | Classifier |
| `classifier_owner_` | record | Classifier Owner |
| `expression` | text | Expression |
| `id` | number | Id |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `links` | links | Links |

### Search Query Fields

These filters are available in classifier example search queries:

| Field | Type | Description |
| --- | --- | --- |
| `class:` | record | Class |
| `class.id:` | chooser | Classification |
| `classifier:` | record | Classifier |
| `classifier.id:` | chooser | Classifier |
| `expression:` | text | Expression |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `updated:` | date | Updated |

### Worklist Columns

These columns are available on classifier example worklists:

| Column | Description |
| --- | --- |
| `c_class_id` | Classification |
| `c_classifier_id` | Classifier |
| `c_expression` | Expression |
| `c_id` | Id |
| `c_updated_at` | Updated |

\< Record Types

