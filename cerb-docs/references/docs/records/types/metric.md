---
id: "docs-records-types-metric"
title: "Metric Records"
url: "https://cerb.ai/docs/records/types/metric/"
summary: "This page provides detailed information about Metric Records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as creation and update timestamps, descriptions, and types. The page also describes dictionary placeholders for automations, snippets, and API responses, offering a comprehensive list of fields like context, label, and record URL. Additionally, it covers search query fields that can be used to filter metrics based on various criteria, and lists the columns available in metric worklists for organizing and displaying metric data. The document serves as a guide for understanding and utilizing metric records within Cerb's ecosystem."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Metric |
| **Name (plural):** | Metrics |
| **Alias (uri):** | metric |
| **Identifier (ID):** | cerb.contexts.metric |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `description` | text | &nbsp; |
| &nbsp; | `dimensions_kata` | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this metric |
| &nbsp; | `type` | text | [counter, gauge] |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `description` | text | Description |
| `dimensions_kata` | text | Dao.metric.dimensions\_Kata |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `type` | text | Type |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `custom_<id>` | mixed | Custom Fields |
| `dimensions` | hashmap | Dimensions |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in metric search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `description:` | text | Description |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on metric worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_created_at` | Created |
| `m_description` | Description |
| `m_id` | Id |
| `m_name` | Name |
| `m_type` | Type |
| `m_updated_at` | Updated |

\< Record Types

