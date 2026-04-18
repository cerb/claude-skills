---
id: "docs-records-types-sensor"
title: "Sensor Records"
url: "https://cerb.ai/docs/records/types/sensor/"
summary: "This page provides detailed information about sensor records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and types of data associated with sensors, such as metrics, status, and tags, and explains how these can be utilized in various Cerb functionalities like automations and API responses. The page also describes how to filter and display sensor data using search queries and worklist columns, offering a comprehensive guide for managing sensor records within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Sensor |
| **Name (plural):** | Sensors |
| **Alias (uri):** | sensor |
| **Identifier (ID):** | cerberusweb.contexts.datacenter.sensor |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `metric` | text | The metric's raw value |
| &nbsp; | `metric_delta` | text | The change in the metric between the last two samples |
| &nbsp; | `metric_type` | text | The metric's type |
| **x** | **`name`** | text | The name of this sensor |
| &nbsp; | `output` | text | The metric's displayed value |
| &nbsp; | `status` | text | `O` (OK), `W` (Warning), `C` (Critical) |
| &nbsp; | `tag` | text | A human-friendly nickname for this sensor |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_label` | text | Label |
| `id` | number | Id |
| `metric` | text | Metric |
| `metric_delta` | number | Change |
| `metric_type` | text | Metric Type |
| `name` | text | Name |
| `output` | text | Output |
| `status` | text | Status |
| `tag` | text | Tag |
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in sensor search queries:

| Field | Type | Description |
| --- | --- | --- |
| `change:` | number | Change |
| `comments:` | fulltext | Comment Content |
| `fail.count:` | number | Fail Count |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isDisabled:` | boolean | Is Disabled |
| `links:` | links | Record Links |
| `metric:` | number | Metric |
| `metricType:` | text | Metric Type |
| `name:` | text | Name |
| `output:` | text | Output |
| `status:` | virtual | Status |
| `tag:` | text | Tag |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `watchers:` | watchers | Watchers |

### Worklist Columns

These columns are available on sensor worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `ftcc_content` | Comment Content |
| `p_extension_id` | Type |
| `p_fail_count` | Fail Count |
| `p_is_disabled` | Is Disabled |
| `p_metric` | Metric |
| `p_metric_delta` | Change |
| `p_metric_type` | Metric Type |
| `p_name` | Name |
| `p_output` | Output |
| `p_status` | Status |
| `p_tag` | Tag |
| `p_updated` | Updated |

\< Record Types

