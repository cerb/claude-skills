---
id: "docs-records-types-connectedaccount"
title: "Connected Account Records"
url: "https://cerb.ai/docs/records/types/connected_account/"
summary: "This page provides detailed information about Connected Account Records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, which are essential for linking, identifying, and managing connected accounts. The page also describes dictionary placeholders that can be used in automations, snippets, and API responses, offering a range of fields such as record type, owner, and service provider. Additionally, it lists search query fields that facilitate filtering connected accounts based on various criteria like creation date, owner, and service. Lastly, it details the worklist columns available for organizing and displaying connected account data, highlighting key attributes such as owner, creation date, and service provider."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Connected Account |
| **Name (plural):** | Connected Accounts |
| **Alias (uri):** | connected\_account |
| **Identifier (ID):** | cerberusweb.contexts.connected\_account |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this connected account |
| **x** | **`owner__context`** | context | The record type of this connected account's owner: `app`, `role`, `group`, or `worker` |
| **x** | **`owner_id`** | number | The ID of this connected account's owner |
| &nbsp; | `params` | object | JSON-encoded key/value object |
| &nbsp; | `service_id` | number | Service Provider |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `uri` | text | &nbsp; |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `id` | number | Id |
| `name` | text | Name |
| `owner_` | record | Owner |
| `record_url` | text | Record Url |
| `service` | text | Service Provider |
| `service_` | record | Service |
| `updated_at` | date | Updated |
| `uri` | text | Uri |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in connected account search queries:

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
| `service:` | record | Service |
| `service.id:` | chooser | Service Provider |
| `updated:` | date | Updated |
| `uri:` | text | Uri |

### Worklist Columns

These columns are available on connected account worklists:

| Column | Description |
| --- | --- |
| `*_owner` | Owner |
| `c_created_at` | Created |
| `c_id` | Id |
| `c_name` | Name |
| `c_service_id` | Service Provider |
| `c_updated_at` | Updated |
| `c_uri` | Uri |
| `cf_<id>` | Custom Field |

\< Record Types

