# Search Queries

Search queries filter records using the syntax `filter:expression`. Multiple filters are AND-ed by default. Queries are used in `record.search` and `record_query` parameters throughout automations.

**Formatting:** Search queries are single-line strings with filters separated by spaces. In automation KATA (e.g. `record_query:` inside `record.search:`), long queries may be split across multiple indented lines for readability. In all other contexts (Cerb UI search bars, saved searches, general use), queries should be on a single line.

---

## Table of Contents

- [Text Filters](#text-filters)
- [Fulltext Filters](#fulltext-filters)
- [Numeric Filters](#numeric-filters)
- [Boolean Filters](#boolean-filters)
- [Date Filters](#date-filters)
- [Nullness Filters](#nullness-filters)
- [Chooser Filters](#chooser-filters)
- [Link Filters](#link-filters)
- [Watcher Filters](#watcher-filters)
- [Deep Search](#deep-search)
- [Boolean Groups (AND/OR/NOT)](#boolean-groups)
- [Sorting](#sorting)
- [Limit](#limit)
- [Query Parameters](#query-parameters)
- [Search Query Fields by Record Type](#search-query-fields-by-record-type)
  - [activity_log](#activity_log)
  - [address](#address)
  - [attachment](#attachment)
  - [automation](#automation)
  - [automation_event](#automation_event)
  - [automation_event_listener](#automation_event_listener)
  - [automation_resource](#automation_resource)
  - [automation_timer](#automation_timer)
  - [behavior](#behavior)
  - [bot](#bot)
  - [bucket](#bucket)
  - [calendar](#calendar)
  - [calendar_event](#calendar_event)
  - [calendar_recurring_event](#calendar_recurring_event)
  - [card_widget](#card_widget)
  - [comment](#comment)
  - [community_portal](#community_portal)
  - [connected_account](#connected_account)
  - [connected_service](#connected_service)
  - [contact](#contact)
  - [currency](#currency)
  - [custom_field](#custom_field)
  - [custom_fieldset](#custom_fieldset)
  - [custom_record](#custom_record)
  - [draft](#draft)
  - [email_signature](#email_signature)
  - [file_bundle](#file_bundle)
  - [gpg_private_key](#gpg_private_key)
  - [gpg_public_key](#gpg_public_key)
  - [group](#group)
  - [html_template](#html_template)
  - [mail_delivery_log](#mail_delivery_log)
  - [mail_routing_rule](#mail_routing_rule)
  - [mail_transport](#mail_transport)
  - [mailbox](#mailbox)
  - [message](#message)
  - [metric](#metric)
  - [notification](#notification)
  - [oauth_app](#oauth_app)
  - [org](#org)
  - [package](#package)
  - [profile_tab](#profile_tab)
  - [profile_widget](#profile_widget)
  - [project_board](#project_board)
  - [project_board_column](#project_board_column)
  - [queue](#queue)
  - [reminder](#reminder)
  - [resource](#resource)
  - [role](#role)
  - [saved_search](#saved_search)
  - [scheduled_behavior](#scheduled_behavior)
  - [snippet](#snippet)
  - [task](#task)
  - [ticket](#ticket)
  - [time_entry](#time_entry)
  - [timetracking_activity](#timetracking_activity)
  - [webapi_credentials](#webapi_credentials)
  - [webhook_listener](#webhook_listener)
  - [worker](#worker)
  - [workflow](#workflow)
  - [workspace_list](#workspace_list)
  - [workspace_page](#workspace_page)
  - [workspace_tab](#workspace_tab)
  - [workspace_widget](#workspace_widget)
- [Examples](#examples)

---

## Text Filters

| Syntax | Description | Example |
|-|-|-|
| `filter:term` | Simple text (no spaces) | `firstName:Kina` |
| `filter:"phrase"` | Text with spaces | `subject:"This has spaces"` |
| `filter:wild*` | Wildcard matching | `mask:abc*` |
| `filter:[set]` | Match any value in set  | `color:[red,green,blue]` |
| `filter:!value` | Negation | `status:!open` |

## Fulltext Filters

For large text content (messages, comments). More efficient than text filters for large volumes.

| Syntax | Description | Example |
|-|-|-|
| `terms` | All terms must match | `bug bluetooth report` |
| `"phrase"` | Exact phrase | `"bug report"` |
| `filter:("phrase" terms)` | Mixed phrases and terms | `content:("exact phrase" other terms)` |
| `filter:!(terms)` | Negation | `text:!(not these words)` |

## Numeric Filters

| Operator | Description | Example |
|-|-|-|
| `filter:N` | Equal to | `age:35` |
| `filter:!N` | Not equal to | `priority:!1` |
| `filter:>N` | Greater than | `age:>21` |
| `filter:>=N` | Greater than or equal | `age:>=21` |
| `filter:<N` | Less than | `order:<100` |
| `filter:<=N` | Less than or equal | `order:<=100` |
| `filter:N...M` | Between (inclusive) | `importance:25...75` |
| `filter:[N,M,O]` | Match any in set | `importance:[0,50,75]` |

## Boolean Filters

| True | False |
|-|-|
| `y`, `yes`, `true` | `n`, `no`, `false` |

Example: `isAdmin:y` or `isDisabled:no`

## Date Filters

**Important:** Date ranges must be in chronological order — **OLD to NEW** (earliest date first, latest date second). To express "before" a certain time, use `"big bang to <date>"` or a parameterized expression with `until:`.

### Relative and absolute dates

A single date value matches from that point forward (to now):

| Example | Description |
|-|-|
| `created:today` | Since start of today  |
| `created:"-1 month"` | Since one month ago |
| `created:"2024-01-01"` | Since a specific date |
| `created:"January 1 2024"` | Natural language date |
| `created:"first day of this month"` | Computed date |

### Date ranges (two dates separated by `to`)

Ranges use the format `"OLD to NEW"` — the earlier date comes first:

| Example | Description |
|-|-|
| `created:"today to now"` | Start of today to current moment |
| `created:"January 1 to June 30"` | Specific range |
| `created:"-1 year to -6 months"` | Relative range |
| `created:"big bang to first day of this month"` | All time up to start of month |
| `created:"big bang to -1 day"` | More than 1 day ago (before cutoff)  |

To filter for records **before** a certain time, use `"big bang to <date>"`:
- `updated:"big bang to -1 week"` — updated more than a week ago
- `closed:"big bang to -6 months"` — closed more than 6 months ago

### Parameterized date expressions

For complex date filtering, use parameterized expressions with `since:` and `until:`:

```
created:(since:"-1 week" until:now months:Jan,Feb,Mar days:Weekdays times:9a-5p)
```

This is especially useful for "before" queries — set `until:` to the cutoff:
```
lastActivity:(until:"-1 day")
```

| Parameter | Description | Default  |
|-|-|-|
| `since:`  | Start of range (oldest) | big bang |
| `until:`  | End of range (newest) | now |
| `months:` | Comma-delimited months | all |
| `weeks:`  | Week numbers 00-53 | all |
| `days:` | Weekday names, `Weekdays`, `Weekends` | all |
| `dom:` | Days of month (1-31) | all |
| `times:`  | Time ranges (e.g. `8a-noon,1-6p`) | all |

## Nullness Filters

| Syntax | Description | Example |
|-|-|-|
| `filter:null`  | Field is null/empty | `sla.level:null` |
| `filter:!null` | Field is NOT null | `checkbox:!null` |

## Chooser Filters

Match record ID fields (names typically end with `.id`).

| Syntax | Description | Example |
|-|-|-|
| `filter.id:N` | Single record ID | `group.id:1` |
| `filter.id:[N,M,O]` | Multiple record IDs | `group.id:[1,2,3]` |

Supports all numeric operators (`>`, `<`, `>=`, `<=`, ranges).

## Link Filters

| Syntax | Description | Example |
|-|-|-|
| `links:type` | Linked to a record type | `links:ticket` |
| `links.type:(query)` | Deep search on linked records | `links.ticket:(mask:a*)` |

## Watcher Filters

| Syntax | Description | Example |
|-|-|-|
| `watchers:name,name` | Partial worker names | `watchers:kina,karl` |
| `watchers:me` | Current user watches | `watchers:me` |
| `watchers:any` | Watched by anyone | `watchers:any` |
| `watchers:none` | Not watched | `watchers:none` |
| `watchers:N,M` | Worker IDs | `watchers:1,2,3` |

## Deep Search

Filter records based on properties of related records. Queries chain to any depth.

### Syntax

```
filter:(nested query)
```

### Single deep search

```
status:open group:(name:S*)
```

### Multiple deep searches

```
owner:(gender:f) group:(name:[support,sales]) org:(sla.plan:!null)
```

### Nested deep searches (any depth)

```
messages.first:(sender:(org:(country:Germany sla.plan:Priority)))
```

### Negated deep search

```
group:!(name:S*)
```

Use negated deep search to assert that **no** related records match a condition. This is more precise than count-based filters when the distinction matters:

```
# Waiting tickets with no worker reply (but allowing automated outgoing messages like broadcasts)
status:waiting messages:!(worker.id:>0)

# vs. messages.count.out:0 which excludes ALL outgoing messages including broadcasts
```

The `messages:!(worker.id:>0)` pattern checks that no message exists where a worker is assigned (worker.id > 0), while still permitting outgoing messages with worker_id=0 (e.g. broadcasts, auto-replies).

### Deep search on links

```
links.ticket:(mask:a*)
```

### The `on.<type>:` deep search (comments/attachments)

Searches into the target record the comment/attachment is attached to.

```
on.ticket:(id:123)
```

**Important:** Use nested query syntax, not simple values:
```
# Correct
on.ticket:(id:${id})

# Wrong
on.ticket:${id}
```

### The `author.<type>:` deep search (comments)

```
author.worker:(firstName:Kina)
```

## Boolean Groups

### AND (default — filters separated by spaces)

```
status:open created:today group:support
```

### OR

```
owner.id:me OR owner.id:none
```

### NOT

```
!(mimetype:image/png size:<100KB)
```

### Complex combinations with parentheses

```
(mimetype:image/png size:>100KB) OR (mimetype:image/jpeg size:<100KB)
```

### OR within deep search

```
status:open group:(sales OR support)
```

## Sorting

| Syntax | Description | Example |
|-|-|-|
| `sort:field`  | Ascending (A-Z, oldest first)  | `sort:subject` |
| `sort:-field` | Descending (Z-A, newest first) | `sort:-updated` |
| `sort:f1,f2`  | Multiple fields | `sort:-importance,created` |

## Limit

Use `limit:N` inline in the query string:

```
status:open sort:-updated limit:10
```

With `limit:1` in `record.search`, a single dictionary is returned instead of an array.

## Query Parameters

Use `record_query_params` to safely inject untrusted user input:

```kata
record.search:
  inputs:
    record_type: ticket
    record_query: status:${status} group.id:${group_id}
    record_query_params:
      status: o
      group_id: 5
```

Parameters are referenced as `${param}` in the query string.

---

## Search Query Fields by Record Type

### activity_log

| Field | Type | Description |
|-|-|-|
| `activity:` | text | Activity |
| `actor:` | text | Actor Type |
| `actor.<type>:`  | record | Actor (deep search by type)  |
| `created:` | date | Created |
| `id:` | number | Id |
| `target:` | text | Target Type |
| `target.<type>:` | record | Target (deep search by type) |

### address

| Field | Type | Description |
|-|-|-|
| `comments:` | fulltext | Comment Content |
| `contact:` | record | Contact (deep search) |
| `contact.id:` | chooser  | Contact |
| `created:` | date | Created |
| `email:` | text | Email |
| `fieldset:` | record | Fieldset |
| `host:` | text | Host |
| `id:` | number | Id |
| `isBanned:` | boolean  | Is Banned |
| `isDefunct:` | boolean  | Is Defunct |
| `isTrusted:` | boolean  | Is Trusted |
| `links:` | links | Record Links |
| `mailTransport.id:` | chooser  | Email Transport |
| `nonspam:` | number | # Nonspam |
| `org:` | record | Organization (deep search) |
| `org.id:` | chooser  | Organization |
| `spam:` | number | # Spam |
| `ticket:` | record | Ticket (deep search) |
| `ticket.id:` | chooser  | Ticket |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |
| `worker:` | record | Worker (deep search) |
| `worker.id:` | chooser  | Worker |

### attachment

| Field | Type | Description |
|-|-|-|
| `bundle:` | record | Bundle (deep search) |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `mimetype:` | text | MIME Type |
| `name:` | text | Name |
| `on:` | text | On Type |
| `on.<type>:` | record | On (deep search into target record) |
| `size:` | number | Size |
| `storage.extension:` | text | Storage Extension |
| `updated:` | date | Updated |

### automation

| Field | Type | Description  |
|-|-|-|
| `created:`  | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `script:` | fulltext | Script |
| `trigger:`  | text | Extension |
| `updated:`  | date | Updated |
| `watchers:` | record | Watchers |

### automation_event

| Field | Type | Description  |
|-|-|-|
| `description:` | text | Description  |
| `extension:` | text | Extension |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |

### automation_event_listener

| Field | Type | Description  |
|-|-|-|
| `created:` | date | Created |
| `event:` | text | Event |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `isDisabled:`  | boolean | Disabled |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `priority:` | number  | Priority |
| `updated:` | date | Updated |
| `workflow.id:` | chooser | Workflow |

### automation_resource

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `mimetype:` | text | MIME Type |
| `name:` | text | Name |
| `size:` | number | Size |
| `token:` | text | Token |
| `updated:`  | date | Updated |

### automation_timer

| Field | Type | Description  |
|-|-|-|
| `created:` | date | Created |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `isRecurring:` | boolean | Is Recurring |
| `lastRanAt:` | date | Last Ran At  |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `nextRunAt:` | date | Next Run At  |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |

### behavior

| Field | Type | Description |
|-|-|-|
| `bot:` | record  | Bot (deep search) |
| `bot.id:` | chooser | Bot |
| `disabled:` | boolean | Disabled |
| `event:` | text | Event |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `priority:` | number  | Priority |
| `private:` | boolean | Private |
| `updated:` | date | Updated |
| `uri:` | text | URI |
| `usableBy.bot:` | chooser | Usable By Bot |

### bot

| Field | Type | Description |
|-|-|-|
| `created:` | date | Created |
| `disabled:` | boolean | Disabled |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `mentionName:`  | text | @Mention |
| `name:` | text | Name |
| `owner:` | text | Owner Type |
| `owner.<type>:` | record  | Owner (deep search by type) |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |

### bucket

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `group:` | record  | Group (deep search) |
| `group.id:` | chooser | Group |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `send.as:` | text | Send As |
| `send.from.id:` | chooser | Send From |
| `signature.id:` | chooser | Signature |
| `signing.key.id:` | chooser | Signing Key |
| `template.id:` | chooser | Email Template |
| `updated:` | date | Updated |

### calendar

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner (App) |
| `owner.bot:` | record  | Owner (Bot, deep search) |
| `owner.group:` | record  | Owner (Group, deep search)  |
| `owner.role:` | record  | Owner (Role, deep search) |
| `owner.worker:` | record  | Owner (Worker, deep search) |
| `timezone:` | text | Timezone |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |
| `workerAvailability:` | record  | Workers |

### calendar_event

| Field | Type | Description |
|-|-|-|
| `calendar:` | record  | Calendar (deep search) |
| `calendar.id:` | chooser | Calendar |
| `endDate:` | date | End Date |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `startDate:` | date | Start Date |
| `status:` | boolean | Is Available |

### calendar_recurring_event

| Field | Type | Description |
|-|-|-|
| `calendar:` | record  | Calendar (deep search) |
| `calendar.id:` | chooser | Calendar |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Event Name |
| `status:` | boolean | Is Available |
| `timezone:` | text | Timezone |
| `watchers:` | record  | Watchers |

### card_widget

| Field | Type | Description  |
|-|-|-|
| `created:`  | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `pos:` | number | Order |
| `type:` | text | Type |
| `updated:`  | date | Updated |
| `width:` | number | Width |
| `zone:` | text | Zone |

### comment

| Field | Type | Description |
|-|-|-|
| `attachments:` | record | Attachments |
| `author:` | text | Actor |
| `author.<type>:` | record | Actor (deep search by type) |
| `comment:` | fulltext | Comment Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isMarkdown:` | boolean  | Is Markdown |
| `isPinned:` | boolean  | Is Pinned |
| `links:` | links | Record Links |
| `on:` | text | Target Record Type |
| `on.<type>:` | record | Target Record (deep search) |

### community_portal

| Field | Type | Description |
|-|-|-|
| `code:` | text | Code |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `name:` | text | Name |
| `path:` | text | Path |
| `type:` | text | Extension |
| `updated:`  | date | Updated |

### connected_account

| Field | Type | Description |
|-|-|-|
| `created:` | date | Created |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner (App) |
| `owner.bot:` | record  | Owner (Bot, deep search) |
| `owner.group:`  | record  | Owner (Group, deep search)  |
| `owner.role:` | record  | Owner (Role, deep search) |
| `owner.worker:` | record  | Owner (Worker, deep search) |
| `service:` | record  | Service |
| `service.id:` | chooser | Service |
| `updated:` | date | Updated |
| `uri:` | text | URI |

### connected_service

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `type:` | text | Type |
| `updated:`  | date | Updated |
| `uri:` | text | URI |

### contact

| Field | Type | Description |
|-|-|-|
| `alias:` | virtual  | Aliases |
| `comments:`  | fulltext | Comment Content |
| `created:` | date | Created |
| `email:` | record | Email (deep search) |
| `email.id:`  | chooser  | Email |
| `fieldset:`  | record | Fieldset |
| `firstName:` | text | First Name |
| `gender:` | text | Gender |
| `id:` | number | Id |
| `lang:` | text | Language |
| `lastLogin:` | date | Last Login |
| `lastName:`  | text | Last Name |
| `links:` | links | Record Links |
| `mobile:` | text | Mobile |
| `org:` | record | Org (deep search) |
| `org.id:` | chooser  | Organization |
| `phone:` | text | Phone |
| `timezone:`  | text | Timezone |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `username:`  | text | Username |
| `watchers:`  | record | Watchers |

### currency

| Field | Type | Description |
|-|-|-|
| `code:` | text | Currency Code  |
| `decimalPlaces:` | number  | Decimal Places |
| `default:` | boolean | Default |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `symbol:` | text | Symbol |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |

### custom_field

| Field | Type | Description |
|-|-|-|
| `context:` | text | Context |
| `fieldset:` | record  | Fieldset |
| `fieldset.id:` | chooser | Custom Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `pos:` | number  | Order |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `uri:` | text | URI |

### custom_fieldset

| Field | Type | Description |
|-|-|-|
| `context:` | text | Context |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner (App) |
| `owner.bot:` | record  | Owner (Bot, deep search) |
| `owner.group:`  | record  | Owner (Group, deep search)  |
| `owner.role:` | record  | Owner (Role, deep search) |
| `owner.worker:` | record  | Owner (Worker, deep search) |
| `updated:` | date | Updated |

### custom_record

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `name.plural:` | text | Plural |
| `updated:` | date | Updated |
| `uri:` | text | URI |

### draft

| Field | Type | Description |
|-|-|-|
| `id:` | number  | Id |
| `is.queued:` | boolean | Queued |
| `name:` | text | Subject |
| `queue.deliverAt:` | date | Scheduled Delivery |
| `queue.fails:` | number  | Failure Count |
| `ticket.id:` | chooser | Ticket |
| `to:` | text | Recipient |
| `token:` | text | Token |
| `type:` | text | Type (compose, transactional, reply, forward) |
| `updated:` | date | Updated |
| `worker:` | record  | Worker (deep search) |
| `worker.id:` | chooser | Worker |

### email_signature

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner (App) |
| `owner.bot:` | record  | Owner (Bot, deep search) |
| `owner.group:`  | record  | Owner (Group, deep search)  |
| `owner.role:` | record  | Owner (Role, deep search) |
| `owner.worker:` | record  | Owner (Worker, deep search) |
| `signature:` | text | Signature Content |
| `updated:` | date | Updated |

### file_bundle

| Field | Type | Description |
|-|-|-|
| `comments:` | fulltext | Comment Content |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `owner:` | virtual  | Owner |
| `owner.app:` | virtual  | Owner (App) |
| `owner.bot:` | record | Owner (Bot, deep search) |
| `owner.group:` | record | Owner (Group, deep search)  |
| `owner.role:` | record | Owner (Role, deep search) |
| `owner.worker:` | record | Owner (Worker, deep search) |
| `tag:` | text | Tag |
| `updated:` | date | Updated |
| `usableBy.worker:` | virtual  | Usable By Worker |
| `watchers:` | record | Watchers |

### gpg_private_key

| Field | Type | Description  |
|-|-|-|
| `expires:` | date | Expires |
| `fieldset:` | record  | Fieldset |
| `fingerprint:` | virtual | Fingerprint  |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |

### gpg_public_key

| Field | Type | Description  |
|-|-|-|
| `expires:` | date | Expires |
| `fieldset:` | record  | Fieldset |
| `fingerprint:` | virtual | Fingerprint  |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `uid:` | virtual | UID |
| `uid.email:` | virtual | UID Email |
| `uid.name:` | virtual | UID Name |
| `updated:` | date | Updated |

### group

| Field | Type | Description |
|-|-|-|
| `created:` | date | Created |
| `default:` | boolean | Default |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `manager:` | record  | Manager (Worker, deep search) |
| `member:` | record  | Member (Worker, deep search)  |
| `name:` | text | Name |
| `private:` | boolean | Private |
| `send.as:` | text | Send As |
| `send.from.id:` | chooser | Send From |
| `signature.id:` | chooser | Signature |
| `signing.key.id:` | chooser | Signing Key |
| `template.id:` | chooser | Template |
| `updated:` | date | Updated |

### html_template

| Field | Type | Description |
|-|-|-|
| `comments:` | fulltext | Comment Content |
| `content:` | text | Content |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `signature.id:` | number | Signature |
| `updated:` | date | Updated |

### mailbox

| Field | Type | Description  |
|-|-|-|
| `checkedAt:`  | date | Checked At |
| `enabled:` | boolean | Enabled |
| `fail.count:` | number  | Num Fails |
| `fieldset:` | record  | Fieldset |
| `host:` | text | Host |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `protocol:` | text | Protocol |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |

### mail_delivery_log

| Field | Type | Description |
|-|-|-|
| `created:` | date | Created |
| `fieldset:` | record  | Fieldset |
| `from:` | record  | From (deep search) |
| `from.id:` | chooser | From |
| `header.messageId:` | text | Message-Id Header |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `mailTransport:` | record  | Mail Transport (deep search) |
| `mailTransport.id:` | chooser | Email Transport |
| `status:` | virtual | Status |
| `status.id:` | number  | Status |
| `subject:` | text | Subject |
| `to:` | text | To |
| `type:` | text | Type |

### mail_routing_rule

| Field | Type | Description  |
|-|-|-|
| `created:` | date | Created |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `isDisabled:`  | boolean | Disabled |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `priority:` | number  | Priority |
| `updated:` | date | Updated |
| `workflow.id:` | chooser | Workflow |

### mail_transport

| Field | Type | Description  |
|-|-|-|
| `created:`  | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `type:` | text | Extension |
| `updated:`  | date | Updated |

### message

| Field | Type | Description |
|-|-|-|
| `attachments:` | record | Attachments (deep search) |
| `content:` | fulltext | Content |
| `created:` | date | Created |
| `fieldset:` | record | Fieldset |
| `header.cc:` | text | Cc |
| `header.deliveredTo:` | text | Delivered-To |
| `header.from:` | text | From |
| `header.messageId:` | text | Message-Id |
| `header.to:` | text | To |
| `id:` | context  | Id |
| `isBroadcast:` | boolean  | Is Broadcast |
| `isEncrypted:` | boolean  | Is Encrypted |
| `isNotSent:` | boolean  | Is Not Sent |
| `isOutgoing:` | boolean  | Is Outgoing |
| `links:` | links | Record Links |
| `notes:` | record | Notes (deep search) |
| `responseTime:` | number | Response Time |
| `sender:` | record | Sender (deep search) |
| `sender.id:` | chooser  | Sender |
| `signed.at:` | date | Signed At |
| `signed.fingerprint:` | text | Signed By |
| `size:` | number | Size |
| `ticket:` | record | Ticket (deep search) |
| `ticket.bucket.id:` | chooser  | Bucket |
| `ticket.bucket.name:` | chooser  | Bucket Name |
| `ticket.group.id:` | chooser  | Group |
| `ticket.group.name:`  | chooser  | Group Name |
| `ticket.id:` | chooser  | Ticket Id |
| `token:` | text | Token |
| `worker:` | record | Worker (deep search) |
| `worker.id:` | chooser  | Worker |

### metric

| Field | Type | Description  |
|-|-|-|
| `created:` | date | Created |
| `description:` | text | Description  |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### notification

| Field | Type | Description |
|-|-|-|
| `activity:`  | text | Activity |
| `created:` | date | Created |
| `id:` | number  | Id |
| `isRead:` | boolean | Is Read |
| `worker:` | record  | Worker (deep search) |
| `worker.id:` | chooser | Worker |

### oauth_app

| Field | Type | Description |
|-|-|-|
| `accessTokenExpires:`  | text | Access Token Expires  |
| `callbackUrl:` | text | Callback URL |
| `clientId:` | text | Client Id |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `refreshTokenExpires:` | text | Refresh Token Expires |
| `updated:` | date | Updated |
| `url:` | text | URL |

### org

| Field | Type | Description |
|-|-|-|
| `alias:` | virtual  | Aliases |
| `city:` | text | City |
| `comments:`  | fulltext | Comment Content |
| `contacts:`  | record | Contacts (deep search) |
| `country:` | text | Country |
| `created:` | date | Created |
| `email:` | record | Email (deep search) |
| `email.id:`  | chooser  | Email |
| `fieldset:`  | record | Fieldset |
| `id:` | number | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `phone:` | text | Phone |
| `postal:` | text | Postal |
| `state:` | text | State/Province |
| `street:` | text | Street |
| `ticket:` | record | Ticket (deep search) |
| `ticket.id:` | chooser  | Ticket |
| `updated:` | date | Updated |
| `watchers:`  | record | Watchers |
| `website:` | text | Website |

### package

| Field | Type | Description |
|-|-|-|
| `description:` | text | Description |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `point:` | text | Extension Point |
| `updated:` | date | Updated |
| `uri:` | text | URI |

### profile_tab

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `record:` | text | Record Type  |
| `updated:`  | date | Updated |

### profile_widget

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `pos:` | number  | Order |
| `tab:` | record  | Tab (deep search) |
| `tab.id:` | chooser | Tab |
| `type:` | text | Type |
| `updated:`  | date | Updated |
| `width:` | number  | Width Units |
| `zone:` | text | Zone |

### project_board

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `updated:`  | date | Updated |
| `watchers:` | record | Watchers |

### project_board_column

| Field | Type | Description |
|-|-|-|
| `board:` | record  | Board (deep search) |
| `board.id:` | chooser | Board |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `updated:`  | date | Updated |
| `watchers:` | record  | Watchers |

### queue

| Field | Type | Description  |
|-|-|-|
| `created:`  | date | Created |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `updated:`  | date | Updated |
| `watchers:` | record | Watchers |

### reminder

| Field | Type | Description |
|-|-|-|
| `closed:` | boolean | Is Closed |
| `fieldset:`  | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `remindAt:`  | date | Remind At |
| `updated:` | date | Updated |
| `worker:` | record  | Worker (deep search) |
| `worker.id:` | chooser | Worker |

### resource

| Field | Type | Description  |
|-|-|-|
| `cacheUntil:`  | date | Cache Until  |
| `description:` | text | Description  |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `isDynamic:` | boolean | Is Dynamic |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `size:` | number  | Size |
| `type:` | text | Type |
| `updated:` | date | Updated |

### role

| Field | Type | Description |
|-|-|-|
| `editor:` | record | Editor (Worker, deep search) |
| `fieldset:`  | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `member:` | record | Member (Worker, deep search) |
| `name:` | text | Name |
| `privsMode:` | text | Privileges Mode |
| `reader:` | record | Reader (Worker, deep search) |

### saved_search

| Field | Type | Description |
|-|-|-|
| `context:`  | text | Record Type |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `name:` | text | Name |
| `query:` | text | Query |
| `tag:` | text | Tag |
| `updated:`  | date | Updated |

### scheduled_behavior

| Field | Type | Description |
|-|-|-|
| `behavior:` | record  | Behavior (deep search) |
| `behavior.id:` | chooser | Behavior |
| `bot:` | record  | Bot (deep search) |
| `bot.id:` | chooser | Bot |
| `id:` | number  | Id |
| `on:` | text | Target Record Type |
| `on.<type>:` | record  | Target Record (deep search) |
| `runDate:` | date | Run Date |

### snippet

| Field | Type | Description |
|-|-|-|
| `content:` | text | Content |
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `myUses:` | number  | My Uses |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner (App) |
| `owner.bot:` | record  | Owner (Bot, deep search) |
| `owner.group:` | record  | Owner (Group, deep search)  |
| `owner.role:` | record  | Owner (Role, deep search) |
| `owner.worker:` | record  | Owner (Worker, deep search) |
| `title:` | text | Title |
| `totalUses:` | number  | All Uses |
| `type:` | virtual | Type |
| `updated:` | date | Updated |
| `usableBy.worker:` | virtual | Usable By Worker |

### task

| Field | Type | Description |
|-|-|-|
| `comments:` | fulltext | Comment Content |
| `completed:`  | date | Completed Date |
| `created:` | date | Created |
| `due:` | date | Due Date |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `importance:` | number | Importance |
| `links:` | links | Record Links |
| `owner:` | record | Owner (Worker, deep search) |
| `owner.id:` | chooser  | Owner |
| `reopen:` | date | Reopen At |
| `status:` | virtual  | Status |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `watchers:` | record | Watchers |

### ticket

| Field | Type | Description |
|-|-|-|
| `bucket:` | record  | Bucket (deep search) |
| `bucket.id:` | chooser | Bucket |
| `closed:` | date | Closed |
| `comments:` | record  | Comments (deep search) |
| `comments.first:` | record  | First Comment (deep search) |
| `comments.last:` | record  | Last Comment (deep search) |
| `created:` | date | Created |
| `fieldset:` | record  | Fieldset |
| `group:` | record  | Group (deep search) |
| `group.id:` | chooser | Group |
| `id:` | number  | Id |
| `importance:` | number  | Importance |
| `inGroupsOf:` | virtual | In Groups Of Worker |
| `lastOpenedAt:` | date | Last Opened At |
| `links:` | links | Record Links |
| `mask:` | text | Mask |
| `mask.merged:` | text | Merged Masks |
| `messages:` | record  | Messages (deep search) |
| `messages.count:` | number  | # Messages |
| `messages.count.in:` | number  | # Messages In |
| `messages.count.out:` | number  | # Messages Out |
| `messages.first:` | record  | First Message (deep search) |
| `messages.firstOutgoing:` | record  | First Outgoing Message (deep search) |
| `messages.last:` | record  | Last Message (deep search) |
| `org:` | record  | Org (deep search) |
| `org.id:` | chooser | Organization |
| `owner:` | record  | Owner (deep search) |
| `owner.id:` | chooser | Owner |
| `participant:` | record  | Participant — address record (deep search); use `participant:(contact:(...))` to filter by contact fields like `gender:` or `firstName:` |
| `participant.id:` | chooser | Participant Id |
| `reopen:` | date | Reopen At |
| `resolution.first:` | number  | First Resolution |
| `response.first:` | number  | First Response |
| `responsibility:` | number  | Responsibility |
| `sender.first:` | record  | First Sender (deep search) |
| `sender.last:` | record  | Last Sender (deep search) |
| `spam.score:` | number  | Spam Score |
| `spam.training:` | virtual | Spam Training |
| `status:` | virtual | Status (open, waiting, closed, deleted) |
| `status.id:` | number  | Status Id |
| `subject:` | text | Subject |
| `timeSpentOpen:` | number  | Time Spent Open |
| `updated:` | date | Updated |
| `watchers:` | record  | Watchers |
| `watchers.count:` | virtual | Watchers Count |
| `worker.commented:` | virtual | Worker Commented |
| `worker.replied:` | virtual | Worker Replied |

### time_entry

| Field | Type | Description |
|-|-|-|
| `activity.id:` | chooser  | Activity |
| `comments:` | fulltext | Comment Content |
| `created:` | date | Log Date |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `isClosed:` | boolean  | Is Closed |
| `links:` | links | Record Links |
| `timeSpent:` | number | Time Spent |
| `watchers:` | record | Watchers |
| `worker:` | record | Worker (deep search) |
| `worker.id:` | chooser  | Worker |

### timetracking_activity

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `updated:`  | date | Updated |

### webapi_credentials

| Field | Type | Description |
|-|-|-|
| `accessKey:` | text | Access Key |
| `fieldset:`  | record  | Fieldset |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `worker:` | record  | Worker (deep search) |
| `worker.id:` | chooser | Worker |

### webhook_listener

| Field | Type | Description  |
|-|-|-|
| `fieldset:` | record | Fieldset |
| `guid:` | text | URL |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `updated:`  | date | Updated |
| `watchers:` | record | Watchers |

### worker

| Field | Type | Description |
|-|-|-|
| `alias:` | virtual | Aliases |
| `calendar:` | record  | Calendar (deep search) |
| `calendar.id:` | chooser | Calendar |
| `email:` | record  | Email (deep search) |
| `email.id:` | chooser | Email |
| `fieldset:` | record  | Fieldset |
| `firstName:` | text | First Name |
| `gender:` | text | Gender |
| `group:` | record  | Groups (deep search) |
| `group.manager:` | record  | Group Manager (deep search) |
| `id:` | number  | Id |
| `isAdmin:` | boolean | Administrator |
| `isAvailable:` | virtual | Calendar Availability |
| `isBusy:` | virtual | Calendar Busy |
| `isDisabled:` | boolean | Disabled |
| `isMfaRequired:` | boolean | MFA Required |
| `isPasswordDisabled:` | boolean | Password Disabled |
| `language:` | text | Language |
| `lastActivity:` | date | Last Activity |
| `lastName:` | text | Last Name |
| `links:` | links | Record Links |
| `location:` | text | Location |
| `mention:` | text | @Mention |
| `mobile:` | text | Mobile |
| `phone:` | text | Phone |
| `role:` | record  | Role (deep search) |
| `role.editor:` | record  | Role Editor (deep search) |
| `role.reader:` | record  | Role Reader (deep search) |
| `timezone:` | text | Timezone |
| `title:` | text | Title |
| `updated:` | date | Updated |
| `using.workspace:` | record  | Using Workspace (deep search) |

### workflow

| Field | Type | Description  |
|-|-|-|
| `created:` | date | Created |
| `description:` | text | Description  |
| `fieldset:` | record | Fieldset |
| `id:` | number | Id |
| `links:` | links  | Record Links |
| `name:` | text | Name |
| `updated:` | date | Updated |
| `version:` | date | Version |
| `watchers:` | record | Watchers |

### workspace_list

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `tab:` | record  | Tab (deep search) |
| `tab.id:` | chooser | Tab |
| `tab.pos:`  | number  | Order |
| `type:` | text | Context Type |
| `updated:`  | date | Updated |

### workspace_page

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `name:` | text | Name |
| `owner:` | virtual | Owner |
| `owner.app:` | virtual | Owner (App) |
| `owner.bot:` | record  | Owner (Bot, deep search) |
| `owner.group:`  | record  | Owner (Group, deep search)  |
| `owner.role:` | record  | Owner (Role, deep search) |
| `owner.worker:` | record  | Owner (Worker, deep search) |
| `type:` | text | Type |
| `updated:` | date | Updated |

### workspace_tab

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Name |
| `page.id:` | chooser | Workspace Page |
| `pos:` | number  | Order |
| `type:` | text | Type |
| `updated:` | date | Updated |
| `workspace:` | record  | Workspace (deep search) |
| `workspace.id:` | chooser | Workspace Page |

### workspace_widget

| Field | Type | Description |
|-|-|-|
| `fieldset:` | record  | Fieldset |
| `id:` | number  | Id |
| `links:` | links | Record Links |
| `name:` | text | Label |
| `tab:` | record  | Tab (deep search) |
| `tab.id:` | chooser | Tab |
| `tab.pos:`  | number  | Order |
| `type:` | text | Type |
| `updated:`  | date | Updated |
| `width:` | text | Width |
| `zone:` | text | Zone |

---

## Examples

### Basic record searches in automations

```kata
# Find open tickets in the Support group
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:open group:(name:Support) sort:-updated limit:10

# Find a single ticket by mask
record.search:
  output: result
  inputs:
    record_type: ticket
    record_query: mask:ABC-12345 limit:1

# Find messages on a ticket with expanded content
record.search:
  output: messages
  inputs:
    record_type: message
    record_query: ticket.id:${ticket_id} sort:-created
    record_expand: content,sender_,worker_
```

### Text and wildcard filters

```kata
# Addresses matching a domain
record.search:
  output: results
  inputs:
    record_type: address
    record_query: host:example.com

# Tickets with subject wildcard
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: subject:"Invoice*" status:open

# Workers with name matching
record.search:
  output: results
  inputs:
    record_type: worker
    record_query: firstName:K* isDisabled:n
```

### Date filters

```kata
# Tickets created in the last week
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: created:"-1 week" status:open

# Tickets created in a date range
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: created:"2024-01-01 to 2024-06-30"

# Tickets created on weekdays during business hours
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: created:(since:"-1 month" days:Weekdays times:9a-5p)
```

### Numeric and boolean filters

```kata
# High importance tickets
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: importance:>=75 status:open

# Messages larger than 100KB
record.search:
  output: results
  inputs:
    record_type: message
    record_query: size:>100000

# Admin workers
record.search:
  output: results
  inputs:
    record_type: worker
    record_query: isAdmin:y isDisabled:n
```

### Deep search

```kata
# Tickets where the org is in a specific country
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:open org:(country:Germany)

# Tickets where the first message sender is at a specific org
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: messages.first:(sender:(org:(name:"Acme Corp")))

# Comments on a specific ticket (using on.<type>: deep search)
record.search:
  output: results
  inputs:
    record_type: comment
    record_query: on.ticket:(id:${ticket_id})
    record_expand: attachments

# Tasks owned by workers in the Support group
record.search:
  output: results
  inputs:
    record_type: task
    record_query: status:open owner:(group:(name:Support))
```

### Boolean groups (AND/OR/NOT)

```kata
# Tickets owned by me OR unassigned
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:open (owner.id:me OR owner.id:0)

# Tickets in Sales or Support groups
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:open group:(name:[Sales,Support])

# Attachments that are NOT images
record.search:
  output: results
  inputs:
    record_type: attachment
    record_query: mimetype:!image/*
```

### Fulltext search

```kata
# Messages containing specific terms
record.search:
  output: results
  inputs:
    record_type: message
    record_query: content:("payment failed" refund)

# Comments containing a phrase
record.search:
  output: results
  inputs:
    record_type: comment
    record_query: comment:("escalated to engineering")
```

### Sorting and limiting

```kata
# Most recently updated open tickets
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:open sort:-updated limit:20

# Tasks sorted by importance then due date
record.search:
  output: results
  inputs:
    record_type: task
    record_query: status:open sort:-importance,due

# Most recent notification
record.search:
  output: result
  inputs:
    record_type: notification
    record_query: worker.id:${worker_id} isRead:n sort:-created limit:1
```

### Safe query parameters

```kata
# Using record_query_params for user-supplied values
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:${status} group.id:${group_id} subject:${subject}
    record_query_params:
      status: o
      group_id: 5
      subject: Invoice*
```

### Link-based searches

```kata
# Records linked to a specific ticket
record.search:
  output: results
  inputs:
    record_type: task
    record_query: links.ticket:(id:${ticket_id})

# Tickets linked to tasks
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: links:task status:open
```

### Watcher searches

```kata
# Tickets I'm watching
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: watchers:me status:open sort:-updated

# Unwatched open tickets
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: watchers:none status:open
```

### Null checks

```kata
# Tickets without an organization
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: org.id:null status:open

# Contacts with a phone number set
record.search:
  output: results
  inputs:
    record_type: contact
    record_query: phone:!null
```
