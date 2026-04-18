---
id: "docs-records-types-toolbarsection"
title: "Toolbar Section Records"
url: "https://cerb.ai/docs/records/types/toolbar_section/"
summary: "This page provides detailed information about the 'Toolbar Section' records in Cerb, including their API fields, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and attributes of toolbar sections, such as their name, priority, and associated workflows. The page also explains how these records can be linked, queried, and displayed within the Cerb platform, offering a comprehensive guide for developers and users to manage and utilize toolbar sections effectively."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Toolbar Section |
| **Name (plural):** | Toolbar Sections |
| **Alias (uri):** | toolbar\_section |
| **Identifier (ID):** | cerb.contexts.toolbar.section |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `is_disabled` | boolean | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this toolbar section |
| &nbsp; | `priority` | number | (0-255) |
| &nbsp; | `toolbar_kata` | text | &nbsp; |
| **x** | **`toolbar_name`** | text | &nbsp; |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `workflow_id` | number | &nbsp; |

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
| `priority` | text | Priority |
| `record_url` | text | Record Url |
| `toolbar_kata` | text | Toolbar Kata |
| `toolbar_name` | text | Toolbar |
| `updated_at` | date | Updated |
| `workflow_id` | number | Common.workflow.id |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in toolbar section search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isDisabled:` | boolean | Disabled |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `priority:` | number | Priority |
| `toolbar:` | text | Toolbar |
| `updated:` | date | Updated |
| `workflow.id:` | chooser | Workflow |

### Worklist Columns

These columns are available on toolbar section worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `t_created_at` | Created |
| `t_id` | Id |
| `t_is_disabled` | Disabled |
| `t_name` | Name |
| `t_priority` | Priority |
| `t_toolbar_name` | Toolbar |
| `t_updated_at` | Updated |
| `t_workflow_id` | Workflow |

\< Record Types

