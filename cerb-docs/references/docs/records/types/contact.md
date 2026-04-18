---
id: "docs-records-types-contact"
title: "Contact Records"
url: "https://cerb.ai/docs/records/types/contact/"
summary: "This page provides comprehensive information about contact records in Cerb, detailing the fields available in the Records API, dictionary placeholders for automations and API responses, search query fields, and worklist columns. It outlines the structure and types of data that can be associated with a contact, such as personal information (name, email, phone, etc.), organizational details, and metadata like comments and custom fields. The page also explains how these fields can be utilized in search queries and displayed in worklists, offering a robust framework for managing and interacting with contact data within the Cerb platform."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Contact |
| **Name (plural):** | Contacts |
| **Alias (uri):** | contact |
| **Identifier (ID):** | cerberusweb.contexts.contact |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `dob` | text | Date of birth: `YYYY-MM-DD` |
| &nbsp; | `email` | text | Email address (e.g. `customer@example.com`); alternative to `email_id` |
| &nbsp; | `email_id` | number | ID of this contact's primary email address |
| **x** | **`first_name`** | text | Given name |
| &nbsp; | `gender` | text | Gender: `F` (female), `M` (male), or blank |
| &nbsp; | `image` | image | The profile image, base64-encoded in data URI format |
| &nbsp; | `language` | text | Language: `en_US` |
| &nbsp; | `last_login_at` | timestamp | Date of their last community portal login |
| &nbsp; | `last_name` | text | Surname |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `location` | text | Location (e.g. `Los Angeles, California, USA`) |
| &nbsp; | `mobile` | text | Mobile number |
| &nbsp; | `org` | text | Organization (e.g. `Fiaflux Software`); alternative to `org_id` |
| &nbsp; | `org_id` | number | ID of this contact's organization |
| &nbsp; | `phone` | text | Phone number |
| &nbsp; | `timezone` | text | Timezone (e.g. `America/Los_Angeles`) |
| &nbsp; | `title` | text | Job title / Position |
| &nbsp; | `username` | text | Username for public display |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `dob` | text | Date Of Birth |
| `email_` | record | Email |
| `first_name` | text | First Name |
| `gender` | text | Gender |
| `id` | number | Id |
| `language` | text | Language |
| `last_login_at` | date | Last Login |
| `last_name` | text | Last Name |
| `location` | text | Location |
| `mobile` | text | Mobile |
| `name` | text | Name |
| `org_` | record | Org |
| `phone` | text | Phone |
| `record_url` | text | Record Url |
| `timezone` | text | Timezone |
| `title` | text | Title |
| `updated_at` | date | Updated |
| `username` | text | Username |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `emails` | records | Email Addresses |
| `last_recipient_message` | record | Latest Message Received To |
| `last_sender_message` | record | Latest Message Sent From |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in contact search queries:

| Field | Type | Description |
| --- | --- | --- |
| `alias:` | virtual | Aliases |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Created |
| `email:` | record | Email |
| `email.id:` | chooser | Email |
| `fieldset:` | record | Fieldset |
| `firstName:` | text | First Name |
| `gender:` | text | Gender |
| `id:` | number | Id |
| `lang:` | text | Language |
| `lastLogin:` | date | Last Login |
| `lastName:` | text | Last Name |
| `links:` | links | Record Links |
| `mobile:` | text | Mobile |
| `org:` | record | Org |
| `org.id:` | chooser | Organization |
| `phone:` | text | Phone |
| `timezone:` | text | Timezone |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `username:` | text | Username |
| `watchers:` | record | Watchers |

### Worklist Columns

These columns are available on contact worklists:

| Column | Description |
| --- | --- |
| `c_created_at` | Created |
| `c_dob` | D.o.b. |
| `c_first_name` | First Name |
| `c_gender` | Gender |
| `c_id` | Id |
| `c_language` | Language |
| `c_last_login_at` | Last Login |
| `c_last_name` | Last Name |
| `c_location` | Location |
| `c_mobile` | Mobile |
| `c_org_id` | Organization |
| `c_phone` | Phone |
| `c_primary_email_id` | Email |
| `c_timezone` | Timezone |
| `c_title` | Title |
| `c_updated_at` | Updated |
| `c_username` | Username |
| `cf_<id>` | Custom Field |

\< Record Types

