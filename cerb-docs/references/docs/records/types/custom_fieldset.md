---
id: "docs-records-types-customfieldset"
title: "Custom Fieldset Records"
url: "https://cerb.ai/docs/records/types/custom_fieldset/"
summary: "This page provides detailed information about Custom Fieldset records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as context, name, owner context, and updated timestamp, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. Additionally, it describes the search query fields that can be used to filter custom fieldset records and the worklist columns available for organizing and displaying these records. The page serves as a comprehensive guide for managing and interacting with custom fieldsets in Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Custom Fieldset |
| **Name (plural):** | Custom Fieldsets |
| **Alias (uri):** | custom\_fieldset |
| **Identifier (ID):** | cerberusweb.contexts.custom\_fieldset |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`context`** | context | The record type of the fieldset |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this custom fieldset |
| **x** | **`owner__context`** | context | The record type of this custom fieldset's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this custom fieldset's owner |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `context` | text | Context |
| `id` | number | Id |
| `name` | text | Name |
| `owner_` | record | Owner |
| `updated_at` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `links` | links | Links |

### Search Query Fields

These filters are available in custom fieldset search queries:

| Field | Type | Description |
| --- | --- | --- |
| `context:` | text | Context |
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

These columns are available on custom fieldset worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `c_context` | Context |
| `c_id` | Id |
| `c_name` | Name |
| `c_updated_at` | Updated |

\< Record Types

