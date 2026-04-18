---
id: "docs-records-types-org"
title: "Organization Records"
url: "https://cerb.ai/docs/records/types/org/"
summary: "This page provides detailed information about organization records in Cerb, including their structure and usage within the platform. It outlines the fields available in the Records API, such as city, country, email, and website, and specifies which fields are required. The page also describes dictionary placeholders for automations, snippets, and API responses, offering a comprehensive list of fields like name, phone, and address. Additionally, it details search query fields that can be used to filter organization records, such as city, country, and email, and lists the columns available in organization worklists, which include city, country, and created date. The page serves as a guide for managing and utilizing organization records effectively within Cerb."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Organization |
| **Name (plural):** | Organizations |
| **Alias (uri):** | org |
| **Identifier (ID):** | cerberusweb.contexts.org |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `city` | text | City |
| &nbsp; | `country` | text | Country |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `email_id` | number | Primary email address |
| &nbsp; | `image` | image | The profile image, base64-encoded in data URI format |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| **x** | **`name`** | text | The name of this organization |
| &nbsp; | `phone` | text | Phone |
| &nbsp; | `postal` | text | Postal code / ZIP |
| &nbsp; | `province` | text | State / Province |
| &nbsp; | `street` | text | Street address |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |
| &nbsp; | `website` | url | Website |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `city` | text | City |
| `country` | text | Country |
| `created` | date | Created |
| `email_` | record | Email |
| `id` | number | Id |
| `name` | text | Name |
| `phone` | text | Phone |
| `postal` | text | Postal |
| `province` | text | State/Prov |
| `record_url` | text | Record Url |
| `street` | text | Street |
| `updated` | date | Updated |
| `website` | text | Website |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `last_recipient_message` | record | Latest Message Received To |
| `last_sender_message` | record | Latest Message Sent From |
| `links` | links | Links |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in organization search queries:

| Field | Type | Description |
| --- | --- | --- |
| `alias:` | virtual | Aliases |
| `city:` | text | City |
| `comments:` | fulltext | Comment Content |
| `contacts:` | record | Contacts |
| `country:` | text | Country |
| `created:` | date | Created |
| `email:` | record | Email |
| `email.id:` | chooser | Email |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `phone:` | text | Phone |
| `postal:` | text | Postal |
| `state:` | text | State/Prov |
| `street:` | text | Street |
| `ticket:` | record | Ticket |
| `ticket.id:` | chooser | Ticket |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |
| `website:` | text | Website |

### Worklist Columns

These columns are available on organization worklists:

| Column | Description |
| --- | --- |
| `c_city` | City |
| `c_country` | Country |
| `c_created` | Created |
| `c_email_id` | Email |
| `c_id` | Id |
| `c_name` | Name |
| `c_phone` | Phone |
| `c_postal` | Postal |
| `c_province` | State/Prov |
| `c_street` | Street |
| `c_updated` | Updated |
| `c_website` | Website |
| `cf_<id>` | Custom Field |

\< Record Types

