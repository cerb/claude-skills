---
id: "docs-records-types-workflow"
title: "Workflow Records"
url: "https://cerb.ai/docs/records/types/workflow/"
summary: "This page provides detailed information about workflow records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `name`, `created_at`, and `updated_at`, and describes how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also details the search query fields that can be used to filter workflows, such as `created`, `description`, and `name`, and lists the columns available in workflow worklists, including `a_created_at`, `a_description`, and `a_name`. Additionally, it explains the concept of key expansion for optional placeholders, which allows for more detailed customization and linking of records."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Workflow |
| **Name (plural):** | Workflows |
| **Alias (uri):** | workflow |
| **Identifier (ID):** | cerb.contexts.workflow |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `config_kata` | text | &nbsp; |
| &nbsp; | `created_at` | timestamp | The date/time when this record was created |
| &nbsp; | `description` | text | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this workflow |
| &nbsp; | `resources_kata` | text | &nbsp; |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `version` | number | (0-4294967296) |
| &nbsp; | `workflow_kata` | text | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `created_at` | date | Created |
| `description` | text | Description |
| `has_extensions` | number | Has Extensions |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `resources_kata` | text | Resources Kata |
| `updated_at` | date | Updated |
| `version` | date | Version |
| `workflow_kata` | text | Workflow Kata |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in workflow search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `description:` | text | Description |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `version:` | date | Version |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on workflow worklists:

| Column | Description |
| --- | --- |
| `a_created_at` | Created |
| `a_description` | Description |
| `a_id` | Id |
| `a_name` | Name |
| `a_updated_at` | Updated |
| `a_version` | Version |
| `cf_<id>` | Custom Field |

\< Record Types

