---
id: "docs-records-types-ticket"
title: "Ticket Records"
url: "https://cerb.ai/docs/records/types/ticket/"
summary: "This page provides comprehensive information about ticket records in Cerb, detailing the fields and functionalities available through the Records API, dictionary placeholders, search query fields, and worklist columns. It outlines the structure and attributes of ticket records, including identifiers, timestamps, group and bucket associations, importance levels, and status indicators. The page also explains how to utilize these fields in automations, snippets, and API responses, and offers guidance on constructing search queries and organizing worklists to efficiently manage and analyze ticket data."
tags: ["docs", "docs-records-types"]
---
| **Name (singular):** | Ticket |
| **Name (plural):** | Tickets |
| **Alias (uri):** | ticket |
| **Identifier (ID):** | cerberusweb.contexts.ticket |

- Records API
- Dictionary Placeholders
- Search Query Fields
- Worklist Columns

### Records API

These fields are available in the Records API and packages:

| Req'd | Field | Type | Notes |
| --- | --- | --- | --- |
| &nbsp; | `bucket` | text | The bucket name of the ticket; alternative to `bucket_id`. If used, a `group` or `group_id` must also be provided at the same time. |
| &nbsp; | `bucket_id` | number | The ID of the bucket containing this ticket |
| &nbsp; | `closed` | timestamp | The date/time this ticket was first set to status `closed` |
| &nbsp; | `created` | timestamp | The date/time when this record was created |
| &nbsp; | `fieldsets` | fieldsets | An array or comma-separated list of custom fieldset IDs. Prefix an ID with `-` to remove. |
| &nbsp; | `group` | text | The group of the ticket; alternative to `group_id` |
| **x** | **`group_id`** | number | The ID of the group containing this ticket |
| &nbsp; | `importance` | number | A number from `0` (least) to `100` (most) |
| &nbsp; | `last_opened_at` | timestamp | &nbsp; |
| &nbsp; | `links` | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| &nbsp; | `mask` | text | The randomized reference number for this ticket; auto-generated if blank |
| &nbsp; | `org` | text | The exact name of the organization linked to this ticket; alternative to `org_id` |
| &nbsp; | `org_id` | number | The ID of the organization linked to this ticket; alternative to `org` |
| &nbsp; | `owner_id` | number | The ID of the worker responsible for this ticket |
| &nbsp; | `participant_ids` | text | A comma-separated list of email addresses IDs to add or remove as participants. Prefix an ID with `-` to remove |
| &nbsp; | `participants` | text | A comma-separated list of email addresses to add as participants |
| &nbsp; | `reopen_date` | timestamp | If status `waiting`, the date/time to automatically change the status back to `open` |
| &nbsp; | `spam_score` | float | `0.0001` (not spam) to `0.9999` (spam); automatically generated |
| &nbsp; | `spam_training` | text | `S` (spam), `N` (not spam); blank for non-trained |
| &nbsp; | `status` | text | `o` (open), `w` (waiting), `c` (closed), `d` (deleted); alternative to `status_id` |
| &nbsp; | `status_id` | number | `0` (open), `1` (waiting), `2` (closed), `3` (deleted); alternative to `status` |
| **x** | **`subject`** | text | The subject of the ticket |
| &nbsp; | `updated` | timestamp | The date/time when this record was last modified |

### Dictionary Placeholders

These placeholders are available in dictionaries for automations, snippets, and API responses:

| Field | Type | Description |
| --- | --- | --- |
| `_context` | text | Record type extension ID |
| `_label` | text | Label |
| `_type` | text | Record type alias |
| `bucket_` | record | Bucket |
| `closed` | date | Closed |
| `created` | date | Created |
| `elapsed_resolution_first` | seconds | First Resolution |
| `elapsed_response_first` | seconds | First Response |
| `elapsed_status_open` | seconds | Time Spent Open |
| `group_` | record | Group |
| `id` | number | Id |
| `importance` | number | Importance |
| `initial_message_` | record | Initial Message |
| `initial_response_message_` | record | Initial Response Message |
| `latest_message_` | record | Latest Message |
| `mask` | text | Mask |
| `num_messages` | number | # Messages |
| `num_messages_in` | number | # Messages In |
| `num_messages_out` | number | # Messages Out |
| `org_` | record | Org |
| `owner_` | record | Owner |
| `reopen_date` | date | Reopen At |
| `spam_score` | percent | Spam Score |
| `spam_training` | text | Spam Training |
| `status` | text | Status |
| `subject` | text | Subject |
| `updated` | date | Updated |
| `url` | text | Url |

These optional placeholders are also available with **key expansion** in dictionaries and the API:

| Field | Type | Description |
| --- | --- | --- |
| `_messages` | records | Messages |
| `attachments` | attachments | Attachments |
| `comment_count` | number | Comment count on the record |
| `comments` | comments | Comments |
| `custom_<id>` | mixed | Custom Fields |
| `latest_incoming_activity` | date | Latest Incoming Activity |
| `latest_outgoing_activity` | date | Latest Outgoing Activity |
| `links` | links | Links |
| `participants` | records | Participants |
| `requester_emails` | text | Requester Emails (Comma-Separated) |
| `requesters` | hashmap | Requesters |
| `signature` | text | Signature |
| `watchers` | watchers | Watchers |

### Search Query Fields

These filters are available in ticket search queries:

| Field | Type | Description |
| --- | --- | --- |
| `bucket:` | record | Bucket |
| `bucket.id:` | chooser | Bucket |
| `closed:` | date | Closed |
| `comments:` | record | Comments |
| `comments.first:` | record | Comments First |
| `comments.last:` | record | Comments Last |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `group:` | record | Group |
| `group.id:` | chooser | Group |
| `id:` | number | Id |
| `importance:` | number | Importance |
| `inGroupsOf:` | virtual | In Groups Of Worker |
| `lastOpenedAt:` | date | Last Opened At |
| `links:` | links | Record Links |
| `mask:` | text | Mask |
| `mask.merged:` | text | Masks Previously Merged Into Ticket |
| `messages:` | record | Messages |
| `messages.count:` | number | # Messages |
| `messages.count.in:` | number | # Messages In |
| `messages.count.out:` | number | # Messages Out |
| `messages.first:` | record | Messages First |
| `messages.firstOutgoing:` | record | Messages First Outgoing |
| `messages.last:` | record | Messages Last |
| `org:` | record | Org |
| `org.id:` | chooser | Organization |
| `owner:` | record | Owner |
| `owner.id:` | chooser | Owner |
| `participant:` | record | Participant |
| `participant.id:` | chooser | Participant Id |
| `reopen:` | date | Reopen At |
| `resolution.first:` | number | First Resolution |
| `response.first:` | number | First Response |
| `responsibility:` | number | Responsibility |
| `sender.first:` | record | Sender First |
| `sender.last:` | record | Sender Last |
| `spam.score:` | number | Spam Score |
| `spam.training:` | virtual | Spam Training |
| `status:` | virtual | Status |
| `status.id:` | number | Status |
| `subject:` | text | Subject |
| `timeSpentOpen:` | number | Time Spent Open |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |
| `watchers.count:` | virtual | Watchers Count |
| `worker.commented:` | virtual | Worker Commented |
| `worker.replied:` | virtual | Worker Replied |

### Worklist Columns

These columns are available on ticket worklists:

| Column | Description |
| --- | --- |
| `*_participant_search` | Participants |
| `*_status` | Status |
| `cf_<id>` | Custom Field |
| `t_bucket_id` | Bucket |
| `t_closed_at` | Closed |
| `t_created_date` | Created |
| `t_elapsed_resolution_first` | First Resolution |
| `t_elapsed_response_first` | First Response |
| `t_elapsed_status_open` | Time Spent Open |
| `t_first_wrote_address_id` | First Wrote |
| `t_group_id` | Group |
| `t_id` | Id |
| `t_importance` | Importance |
| `t_last_opened_at` | Last Opened At |
| `t_last_wrote_address_id` | Last Wrote |
| `t_mask` | Mask |
| `t_num_messages` | # Messages |
| `t_num_messages_in` | # Messages In |
| `t_num_messages_out` | # Messages Out |
| `t_org_id` | Organization |
| `t_owner_id` | Owner |
| `t_reopen_at` | Reopen At |
| `t_spam_score` | Spam Score |
| `t_spam_training` | Spam Training |
| `t_subject` | Subject |
| `t_updated_date` | Updated |
| `wtb_responsibility` | Responsibility |

\< Record Types

