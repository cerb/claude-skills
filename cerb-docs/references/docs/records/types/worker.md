---
id: "docs-records-types-worker"
title: "Worker Records"
url: "https://cerb.ai/docs/records/types/worker/"
summary: "This page provides detailed information about worker records in Cerb, including the fields available in the Records API, dictionary placeholders for automations and API responses, search query fields, and worklist columns. It outlines the various attributes associated with worker records, such as personal information (e.g., name, email, date of birth), account settings (e.g., language, timezone, MFA requirements), and administrative roles. The page also describes how these fields can be used in search queries and displayed in worklists, offering a comprehensive guide for managing and utilizing worker data within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Worker |
| **Name (plural):** | Workers |
| **Alias (uri):** | worker |
| **Identifier (ID):** | cerberusweb.contexts.worker |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `at_mention_name` | text | The nickname used for `@mention` notifications in comments |
| &nbsp; | `calendar_id` | number | The ID of the calendar used to compute worker availability |
| &nbsp; | `dob` | text | Date of birth in `YYYY-MM-DD` format |
| &nbsp; | `email` | text | The primary email address of the worker; alternative to `email_id` |
| **x** | **`email_id`** | number | The ID of the primary email address; alternative to `email` |
| &nbsp; | `email_ids` | text | A comma-separated list of IDs for alternative email addresses |
| **x** | **`first_name`** | text | Given name |
| &nbsp; | `gender` | text | `F` (female), `M` (male), or blank or unknown |
| &nbsp; | `image` | image | The profile image, base64-encoded in data URI format |
| &nbsp; | `is_disabled` | boolean | Is this worker deactivated and prevented from logging in? |
| &nbsp; | `is_mfa_required` | boolean | Is this worker required to use multi-factor authentication? |
| &nbsp; | `is_password_disabled` | boolean | Is this worker allowed to log in with a password? |
| &nbsp; | `is_superuser` | boolean | Is this worker an administrator with full privileges? |
| **x** | **`language`** | text | ISO-639 language code and ISO-3166 country code; e.g. `en_US` |
| &nbsp; | `last_name` | text | Surname |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `location` | text | Location description; `Los Angeles, CA, USA` |
| &nbsp; | `mobile` | text | Mobile number |
| &nbsp; | `password` | text | The worker's password, if applicable; stored security; will be automatically generated if blank |
| &nbsp; | `phone` | text | &nbsp; |
| &nbsp; | `time_format` | text | Preference for displaying timestamps, `DateTime()` syntax |
| &nbsp; | `timeout_idle_secs` | number | Consider a session idle after this many seconds of inactivity |
| **x** | **`timezone`** | text | IANA tz/zoneinfo timezone; `America/Los_Angeles` |
| &nbsp; | `title` | text | Job title / Position |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `address_` | record | Email |
| `at_mention_name` | text | @Mention |
| `calendar_` | record | Calendar |
| `calendar_owner_` | record | Calendar Owner |
| `dob` | text | Date Of Birth |
| `first_name` | text | First Name |
| `full_name` | text | Full Name |
| `gender` | text | Gender |
| `id` | worker | Id |
| `is_disabled` | boolean | Disabled |
| `is_superuser` | boolean | Administrator |
| `language` | text | Language |
| `last_name` | text | Last Name |
| `location` | text | Location |
| `mobile` | text | Mobile |
| `phone` | text | Phone |
| `record_url` | text | Record Url |
| `time_format` | text | Time Format |
| `timeout_idle_secs` | number | Idle Timeout (Secs) |
| `timezone` | text | Timezone |
| `title` | text | Title |
| `updated` | date | Updated |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `emails` | records | Emails |
| `groups` | records | Groups |
| `links` | links | Links |
| `roles` | records | Roles |

### Search Query Fields

These filters are available in worker search queries:

| Field | Type | Description |
| --- | --- | --- |
| `alias:` | virtual | Aliases |
| `calendar:` | record | Calendar |
| `calendar.id:` | chooser | Calendar |
| `email:` | record | Email |
| `email.id:` | chooser | Email |
| `fieldset:` | record | Fieldset |
| `firstName:` | text | First Name |
| `gender:` | text | Gender |
| `group:` | record | Groups |
| `group.manager:` | record | Group Manager |
| `id:` | number | Id |
| `isAdmin:` | boolean | Administrator |
| `isAvailable:` | virtual | Calendar Availability |
| `isBusy:` | virtual | Calendar Availability |
| `isDisabled:` | boolean | Disabled |
| `isMfaRequired:` | boolean | Mfa Required |
| `isPasswordDisabled:` | boolean | Password Disabled |
| `language:` | text | Language |
| `lastActivity:` | date | Last Activity |
| `lastName:` | text | Last Name |
| `links:` | links | Record Links |
| `location:` | text | Location |
| `mention:` | text | @Mention |
| `mobile:` | text | Mobile |
| `phone:` | text | Phone |
| `role:` | record | Role |
| `role.editor:` | record | Role Editor |
| `role.reader:` | record | Role Reader |
| `timezone:` | text | Timezone |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `using.workspace:` | record | Using Workspace |

### Worklist Columns

These columns are available on worker worklists:

| Column | Description |
| --- | --- |
| `*_calendar_availability` | Calendar Availability |
| `a_address_email` | Email Address |
| `cf_<id>` | Custom Field |
| `w_at_mention_name` | @Mention |
| `w_calendar_id` | Calendar |
| `w_dob` | D.o.b. |
| `w_first_name` | First Name |
| `w_gender` | Gender |
| `w_id` | Id |
| `w_is_disabled` | Disabled |
| `w_is_mfa_required` | Mfa Required |
| `w_is_password_disabled` | Password Disabled |
| `w_is_superuser` | Administrator |
| `w_language` | Language |
| `w_last_name` | Last Name |
| `w_location` | Location |
| `w_mobile` | Mobile |
| `w_phone` | Phone |
| `w_time_format` | Time Format |
| `w_timeout_idle_secs` | Idle Timeout (Secs) |
| `w_timezone` | Timezone |
| `w_title` | Title |
| `w_updated` | Updated |

\< Record Types

