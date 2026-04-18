---
id: "docs-records-types-mailroutingrule"
title: "Mail Routing Rule Records"
url: "https://cerb.ai/docs/records/types/mail_routing_rule/"
summary: "This page provides detailed information about the structure and functionality of Email Routing Rule records in Cerb. It outlines the fields available in the Records API, including required and optional fields such as `name`, `priority`, and `workflow_id`. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields like `created_at`, `id`, and `routing_kata`. Additionally, it lists search query fields that can be used to filter mail routing rules, such as `created:`, `isDisabled:`, and `workflow.id:`. Lastly, it details the worklist columns available for displaying mail routing rules, including custom fields and standard fields like `m_name`, `m_priority`, and `m_updated_at`. This comprehensive guide is essential for managing and utilizing email routing rules within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Email Routing Rule |
| **Name (plural):** | Email Routing Rules |
| **Alias (uri):** | mail\_routing\_rule |
| **Identifier (ID):** | cerb.contexts.mail.routing.rule |

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
| **x** | **`name`** | text | The name of this email routing rule |
| &nbsp; | `priority` | number | (0-255) |
| &nbsp; | `routing_kata` | text | &nbsp; |
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
| `routing_kata` | text | Routing Kata |
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

These filters are available in mail routing rule search queries:

| Field | Type | Description |
| --- | --- | --- |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isDisabled:` | boolean | Disabled |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `priority:` | number | Priority |
| `updated:` | date | Updated |
| `workflow.id:` | chooser | Workflow |

### Worklist Columns

These columns are available on mail routing rule worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `m_created_at` | Created |
| `m_id` | Id |
| `m_is_disabled` | Disabled |
| `m_name` | Name |
| `m_priority` | Priority |
| `m_updated_at` | Updated |
| `m_workflow_id` | Workflow |

\< Record Types

