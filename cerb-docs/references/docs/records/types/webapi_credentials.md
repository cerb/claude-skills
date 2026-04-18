---
id: "docs-records-types-webapicredentials"
title: "Web Api Credentials Records"
url: "https://cerb.ai/docs/records/types/webapi_credentials/"
summary: "This page provides detailed information about Web API Credentials Records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `name`, `worker_id`, and `updated_at`, and explains how these fields can be utilized in automations, snippets, and API responses through dictionary placeholders. The page also describes the search query fields that can be used to filter web API credentials, such as `accessKey`, `name`, and `worker`, and lists the worklist columns available for organizing and displaying these records, including custom fields and worker information."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Api Key |
| **Name (plural):** | Api Keys |
| **Alias (uri):** | webapi\_credentials |
| **Identifier (ID):** | cerberusweb.contexts.webapi.credential |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this api key |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| **x** | **`worker_id`** | number | The ID of the worker who owns these API credentials |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `access_key` | text | Access Key |
| `id` | number | Id |
| `name` | text | Name |
| `params` | object | Params |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |
| `worker_` | record | Worker |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in web api credentials search queries:

| Field | Type | Description |
| --- | --- | --- |
| `accessKey:` | text | Access Key |
| `fieldset:` | record | Fieldset |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `worker:` | record | Worker |
| `worker.id:` | chooser | Worker |

### Worklist Columns

These columns are available on web api credentials worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `w_access_key` | Access Key |
| `w_name` | Name |
| `w_updated_at` | Updated |
| `w_worker_id` | Worker |

\< Record Types

