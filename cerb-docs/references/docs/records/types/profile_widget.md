---
id: "docs-records-types-profilewidget"
title: "Profile Widget Records"
url: "https://cerb.ai/docs/records/types/profile_widget/"
summary: "This page provides detailed information about Profile Widget records in Cerb, including their structure and usage within the system. It outlines the fields available in the Records API, such as `extension_id`, `name`, and `profile_tab_id`, and describes their types and purposes. The page also explains the dictionary placeholders that can be used in automations, snippets, and API responses, offering a comprehensive list of fields like `id`, `name`, and `zone`. Additionally, it details the search query fields that can be used to filter profile widget records, such as `id:`, `name:`, and `updated:`, and lists the worklist columns available for organizing these records, including `p_name`, `p_pos`, and `p_zone`. This information is crucial for developers and users who need to manage and customize profile widgets within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Profile Widget |
| **Name (plural):** | Profile Widgets |
| **Alias (uri):** | profile\_widget |
| **Identifier (ID):** | cerberusweb.contexts.profile.widget |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| **x** | **`extension_id`** | text | Profile Widget Type |
| &nbsp; | `extension_params` | object | JSON-encoded key/value object |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this profile widget |
| &nbsp; | `pos` | number | The order of the widget on the profile; `0` is first (top-left) proceeding in rows then columns |
| **x** | **`profile_tab_id`** | number | The ID of the profile tab dashboard containing this widget |
| &nbsp; | `updated_at` | timestamp | The date/time when this record was last modified |
| &nbsp; | `width_units` | number | `1` (25%), `2` (50%), `3` (75%), `4` (100%) |
| &nbsp; | `zone` | text | The name of the dashboard zone containing the widget; this varies by layout; generally `sidebar` and `content` |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `extension_id` | extension | Extension |
| `id` | number | Id |
| `name` | text | Name |
| `pos` | number | Order |
| `profile_tab_` | record | Tab |
| `record_url` | text | Record Url |
| `updated_at` | date | Updated |
| `width_units` | number | Width |
| `zone` | text | Zone |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in profile widget search queries:

| Field | Type | Description |
| --- | --- | --- |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `pos:` | number | Order |
| `tab:` | record | Tab |
| `tab.id:` | chooser | Tab |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `width:` | number | Width Units |
| `zone:` | text | Zone |

### Worklist Columns

These columns are available on profile widget worklists:

| Column | Description |
| --- | --- |
| `cf_<id>` | Custom Field |
| `p_extension_id` | Type |
| `p_id` | Id |
| `p_name` | Name |
| `p_pos` | Order |
| `p_profile_tab_id` | Tab |
| `p_updated_at` | Updated |
| `p_width_units` | Width Units |
| `p_zone` | Zone |

\< Record Types

