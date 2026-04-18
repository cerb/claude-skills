---
id: "docs-records-types-oauthapp"
title: "OAuth App Records"
url: "https://cerb.ai/docs/records/types/oauth_app/"
summary: "This page provides detailed information about OAuth App records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as access token expiration, callback URL, client ID, and client secret, which are essential for managing OAuth applications. The page also describes dictionary placeholders for automations and API responses, search query fields for filtering OAuth app records, and worklist columns for organizing and displaying these records. This comprehensive guide is designed to help users effectively manage and integrate OAuth applications within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Oauth App |
| **Name (plural):** | Oauth Apps |
| **Alias (uri):** | oauth\_app |
| **Identifier (ID):** | cerberusweb.contexts.oauth.app |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `access_token_ttl` | text | The expiration of the access token (e.g. '1 hour') |
| **x** | **`callback_url`** | url | The OAuth2 callback URL of the app |
| **x** | **`client_id`** | text | The client identifier of the app |
| **x** | **`client_secret`** | text | The client secret of the app |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this oauth app |
| &nbsp; | `refresh_token_ttl` | text | The expiration of the refresh token (e.g. '1 month') |
| &nbsp; | `scopes` | text | The app's available scopes in YAML format |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `url` | url | The app's URL |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `access_token_ttl` | text | Access Token Expires |
| `callback_url` | text | Callback Url |
| `client_id` | text | Client Id |
| `id` | number | Id |
| `name` | text | Name |
| `record_url` | text | Record Url |
| `refresh_token_ttl` | text | Refresh Token Expires |
| `scopes` | text | Scopes |
| `updated_at` | date | Updated |
| `url` | text | Url |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |

### Search Query Fields

These filters are available in oauth app search queries:

| Field | Type | Description |
| --- | --- | --- |
| `accessTokenExpires:` | text | Access Token Expires |
| `callbackUrl:` | text | Callback Url |
| `clientId:` | text | Client Id |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `refreshTokenExpires:` | text | Refresh Token Expires |
| `updated:` | date | Updated |
| `url:` | text | Url |

### Worklist Columns

These columns are available on oauth app worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `o_access_token_ttl` | Access Token Expires |
| `o_callback_url` | Callback Url |
| `o_client_id` | Client Id |
| `o_id` | Id |
| `o_name` | Name |
| `o_refresh_token_ttl` | Refresh Token Expires |
| `o_scopes` | Scopes |
| `o_updated_at` | Updated |
| `o_url` | Url |

\< Record Types

