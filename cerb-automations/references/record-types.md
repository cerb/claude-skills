# Record Types and Schemas

## Record Types

Use the following table to find a record type ID or extension ID.

| Type | Name | Extension ID |
|-|-|-|
| activity_log | Activity Logs | cerberusweb.contexts.activity_log |
| address | Email Addresses | cerberusweb.contexts.address |
| app | Applications | cerberusweb.contexts.app |
| attachment | Attachments | cerberusweb.contexts.attachment |
| automation | Automations | cerb.contexts.automation |
| automation_event | Automation Events | cerb.contexts.automation.event |
| automation_event_listener | Automation Event Listeners | cerb.contexts.automation.event.listener |
| automation_resource | Automation Resources | cerb.contexts.automation.resource |
| automation_timer | Automation Timers | cerb.contexts.automation.timer |
| behavior | Behaviors | cerberusweb.contexts.behavior |
| bot | Bots | cerberusweb.contexts.bot |
| bucket | Buckets | cerberusweb.contexts.bucket |
| calendar | Calendars | cerberusweb.contexts.calendar |
| calendar_event | Calendar Events | cerberusweb.contexts.calendar_event |
| calendar_recurring_event  | Calendar Recurring Events  | cerberusweb.contexts.calendar_event.recurring |
| card_widget | Card Widgets | cerb.contexts.card.widget |
| comment | Comments | cerberusweb.contexts.comment |
| community_portal | Portals | cerberusweb.contexts.portal |
| connected_account | Connected Accounts | cerberusweb.contexts.connected_account |
| connected_service | Connected Services | cerberusweb.contexts.connected_service |
| contact | Contacts | cerberusweb.contexts.contact |
| currency | Currencies | cerberusweb.contexts.currency |
| custom_field | Custom Fields | cerberusweb.contexts.custom_field |
| custom_fieldset | Custom Fieldsets | cerberusweb.contexts.custom_fieldset |
| custom_record | Custom Records | cerberusweb.contexts.custom_record |
| draft | Drafts | cerberusweb.contexts.mail.draft |
| email_signature | Email Signatures | cerberusweb.contexts.email.signature |
| file_bundle | File Bundles | cerberusweb.contexts.file_bundle |
| gpg_private_key | Pgp Private Keys | cerb.contexts.gpg.private.key |
| gpg_public_key | Pgp Public Keys | cerberusweb.contexts.gpg_public_key |
| group | Groups | cerberusweb.contexts.group |
| html_template | Email Templates | cerberusweb.contexts.mail.html_template |
| mail_delivery_log | Email Delivery Logs | cerb.contexts.mail.delivery.log |
| mail_inbound_log | Email Inbound Logs | cerb.contexts.mail.inbound.log |
| mail_routing_rule | Email Routing Rules | cerb.contexts.mail.routing.rule |
| mail_transport | Email Transports | cerberusweb.contexts.mail.transport |
| mailbox | Email Mailboxes | cerberusweb.contexts.mailbox |
| message | Messages | cerberusweb.contexts.message |
| metric | Metrics | cerb.contexts.metric |
| notification | Notifications | cerberusweb.contexts.notification |
| oauth_app | Oauth Apps | cerberusweb.contexts.oauth.app |
| org | Organizations | cerberusweb.contexts.org |
| package | Packages | cerberusweb.contexts.package.library |
| profile_tab | Profile Tabs | cerberusweb.contexts.profile.tab |
| profile_widget | Profile Widgets | cerberusweb.contexts.profile.widget |
| project_board | Project Boards | cerberusweb.contexts.project.board |
| project_board_column | Project Board Columns | cerberusweb.contexts.project.board.column |
| queue | Queues | cerb.contexts.queue |
| reminder | Reminders | cerberusweb.contexts.reminder |
| resource | Resources | cerb.contexts.resource |
| role | Roles | cerberusweb.contexts.role |
| saved_search | Saved Searches | cerberusweb.contexts.context.saved.search |
| scheduled_behavior | Behavior Schedules | cerberusweb.contexts.behavior.scheduled |
| search_index | Search Indexes | cerb.contexts.search.index |
| snippet | Snippets | cerberusweb.contexts.snippet |
| task | Tasks | cerberusweb.contexts.task |
| ticket | Tickets | cerberusweb.contexts.ticket |
| time_entry | Time Tracking Entries | cerberusweb.contexts.timetracking |
| timetracking_activity | Time Tracking Activities | cerberusweb.contexts.timetracking.activity |
| toolbar | Toolbars | cerb.contexts.toolbar |
| toolbar_section | Toolbar Sections | cerb.contexts.toolbar.section |
| webapi_credentials | Api Keys | cerberusweb.contexts.webapi.credential |
| webhook_listener | Webhooks | cerberusweb.contexts.webhook_listener |
| worker | Workers | cerberusweb.contexts.worker |
| workflow | Workflows | cerb.contexts.workflow |
| workspace_list | Workspace Worklists | cerberusweb.contexts.workspace.list |
| workspace_page | Workspace Pages | cerberusweb.contexts.workspace.page |
| workspace_tab | Workspace Tabs | cerberusweb.contexts.workspace.tab |
| workspace_widget | Workspace Widgets | cerberusweb.contexts.workspace.widget |

## Record Schemas

The following tables describe the fields available on each record type.

Fields marked with a `*` are required when creating a new record.

Table of contents:
* [activity_log](#activity_log)
* [app](#app)
* [attachment](#attachment)
* [automation_event_listener](#automation_event_listener)
* [automation_event](#automation_event)
* [automation_resource](#automation_resource)
* [automation_timer](#automation_timer)
* [automation](#automation)
* [scheduled_behavior](#scheduled_behavior)
* [behavior](#behavior)
* [bot](#bot)
* [bucket](#bucket)
* [calendar_event](#calendar_event)
* [calendar_recurring_event](#calendar_recurring_event)
* [calendar](#calendar)
* [card_widget](#card_widget)
* [comment](#comment)
* [connected_account](#connected_account)
* [connected_service](#connected_service)
* [contact](#contact)
* [currency](#currency)
* [custom_field](#custom_field)
* [custom_fieldset](#custom_fieldset)
* [custom_record](#custom_record)
* [draft](#draft)
* [address](#address)
* [mail_delivery_log](#mail_delivery_log)
* [mail_inbound_log](#mail_inbound_log)
* [mailbox](#mailbox)
* [mail_routing_rule](#mail_routing_rule)
* [email_signature](#email_signature)
* [html_template](#html_template)
* [mail_transport](#mail_transport)
* [file_bundle](#file_bundle)
* [group](#group)
* [message](#message)
* [metric](#metric)
* [notification](#notification)
* [oauth_app](#oauth_app)
* [org](#org)
* [package](#package)
* [gpg_private_key](#gpg_private_key)
* [gpg_public_key](#gpg_public_key)
* [community_portal](#community_portal)
* [profile_tab](#profile_tab)
* [profile_widget](#profile_widget)
* [project_board_column](#project_board_column)
* [project_board](#project_board)
* [queue](#queue)
* [reminder](#reminder)
* [resource](#resource)
* [role](#role)
* [saved_search](#saved_search)
* [search_index](#search_index)
* [snippet](#snippet)
* [task](#task)
* [ticket](#ticket)
* [timetracking_activity](#timetracking_activity)
* [time_entry](#time_entry)
* [toolbar_section](#toolbar_section)
* [toolbar](#toolbar)
* [webapi_credentials](#webapi_credentials)
* [webhook_listener](#webhook_listener)
* [worker](#worker)
* [workflow](#workflow)
* [workspace_page](#workspace_page)
* [workspace_tab](#workspace_tab)
* [workspace_widget](#workspace_widget)
* [workspace_list](#workspace_list)

## activity_log

| Field | Type | Description |
|-|-|-|
| *activity_point  | string | The event ID that occurred (or `custom.other`) |
| *actor__context  | context | The actor's record type |
| *actor_id | id | The actor's record ID |
| created | timestamp | The date/time when this record was created |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| params | object | JSON-encoded key/value object |
| *target__context | context | The target's record type |
| *target_id | id | The target's record ID |

## app

| Field | Type  | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |

## attachment

| Field | Type | Description |
|-|-|-|
| attach | links | An array of `type:id` tuples to attach this file to |
| content | string | The optional content of this file. For binary, base64-encode in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme). For `application/vnd.cerb.uri` this should be a URI like `cerb:automation_resource:3ed620aa-a4b5-11ec-89ea-6b1bb00ef554` |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mime_type | string | The MIME type of this file (e.g. `image/png`); defaults to `application/octet-stream`. Can be `application/vnd.cerb.uri` for an [automation resource](/docs/records/types/automation_resource/) URI in `content`. |
| *name | string | The filename |
| updated | timestamp | The date/time when this record was last modified |
| url_download | string | The download URL for the attachment |

## automation_event_listener

| Field | Type | Description |
|-|-|-|
| event_kata  | string | |
| *event_name | string | |
| is_disabled | number | (0-1) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this automation event listener |
| priority | number | (0-255) |
| updated_at  | timestamp | The date/time when this record was last modified |
| workflow_id | id | |

## automation_event

| Field | Type | Description |
|-|-|-|
| description | string | |
| *extension_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this automation event |
| updated_at | timestamp | The date/time when this record was last modified |

## automation_resource

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mime_type  | string | |
| name | string | The name of this automation resource |
| *token | string | |
| updated_at | timestamp | The date/time when this record was last modified |

## automation_timer

| Field | Type | Description |
|-|-|-|
| automations_kata | string | |
| created_at | timestamp | The date/time when this record was created |
| is_disabled | bit | |
| is_recurring | bit | |
| last_ran_at | timestamp | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this automation timer |
| next_run_at | timestamp | |
| recurring_patterns | string | |
| recurring_timezone | string | |
| updated_at | timestamp | The date/time when this record was last modified |

## automation

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| description | string | |
| *extension_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| name | string | The name of this automation |
| policy_kata | string | |
| script | string | |
| updated_at | timestamp | The date/time when this record was last modified |

## scheduled_behavior

| Field | Type | Description |
|-|-|-|
| *behavior_id | id | The ID of the [behavior](/docs/records/types/behavior/) to be scheduled |
| *run_date | timestamp | The date/time to run the scheduled behavior |
| *target__context | context | The [record type](/docs/records/types/) of the target record to run the behavior against |
| *target_id | id | The ID of the target record |
| variables | object | JSON-encoded key/value object |

## behavior

| Field | Type | Description |
|-|-|-|
| *bot_id | id | [Bot](/docs/records/types/bot/) |
| *event_point | string | The event of the behavior |
| is_disabled  | bit | Is this behavior disabled? |
| is_private | bit | Is this behavior only visible to the parent bot? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The behavior's name |
| priority | uint | Any positive number; `0` is highest priority |
| updated_at | timestamp | The date/time when this record was last modified |
| uri | string | |

## bot

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| image | image | The profile image, base64-encoded in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme) |
| is_disabled | bit | Is this bot disabled? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mention_name | string | (deprecated) |
| *name | string | The name of this bot |
| *owner__context | context | The [record type](/docs/records/types/) of this bot's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this bot's owner |
| updated_at | timestamp | The date/time when this record was last modified |

## bucket

| Field | Type | Description |
|-|-|-|
| *group_id | id | The ID of the parent [group](/docs/records/types/group/) containing this bucket |
| is_default | bit | Is this the default (inbox) bucket of the group? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this bucket |
| reply_address_id | id | The ID of the [email address](/docs/records/types/address/) used when sending replies from this bucket |
| reply_html_template_id | id | The ID of the default [mail template](/docs/records/types/html_template/) used when sending HTML mail from this bucket |
| reply_personal | string | The default personal name in the `From:` of replies |
| reply_signature_id | id | The ID of the default [signature](/docs/records/types/email_signature/) used when sending replies from this bucket |
| reply_signing_key_id | id | The [private key](/docs/records/types/gpg_private_key/) used when signing outgoing mail from this bucket |
| updated_at | timestamp | The date/time when this record was last modified |

## calendar_event

| Field | Type | Description |
|-|-|-|
| *calendar_id | id | The parent [calendar](/docs/records/types/calendar/) of this event |
| date_end | timestamp | The end date/time of the event |
| *date_start  | timestamp | The start date/time of the event |
| is_available | bit | `true` for available; `false` for busy |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of the event |

## calendar_recurring_event

| Field | Type | Description |
|-|-|-|
| *calendar_id | id | The parent [calendar](/docs/records/types/calendar/) of this event |
| event_end | string | The end date/time of the event |
| event_start  | string | The start date/time of the event |
| is_available | bit | `true` for available; `false` for busy |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of the event |
| *patterns | string | One pattern per line |
| recur_end | timestamp | The end date/time of the recurring range |
| recur_start  | timestamp | The start date/time of the recurring range |
| tz | string | The timezone of the recurring event (e.g. `America/Los_Angeles`) |

## calendar

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this calendar |
| *owner__context | context | The [record type](/docs/records/types/) of this calendar's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this calendar's owner |
| params | object | JSON-encoded key/value object |
| timezone | string | |
| updated_at | timestamp | The date/time when this record was last modified |

## card_widget

| Field | Type | Description |
|-|-|-|
| *extension_id | string | [Card Widget Type](/docs/plugins/extensions/points/cerb.card.widget/) |
| extension_params | object | JSON-encoded key/value object |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this card widget |
| options_kata | string | |
| pos | number | The order of the widget on the card; `0` is first (top-left) proceeding in rows then columns |
| *record_type | context | The record type of the card containing this widget |
| updated_at | timestamp | The date/time when this record was last modified |
| width_units | number | `1` (25%), `2` (50%), `3` (75%), `4` (100%) |
| zone | string | The name of the dashboard zone containing the widget; this varies by layout; generally `sidebar` and `content` |

## comment

| Field | Type | Description |
|-|-|-|
| *author__context | context | The [record type](/docs/records/#record-type) of the comment's author |
| *author_id | id | The ID of the comment's author |
| *comment | string | The text of the comment |
| created | timestamp | The date/time when this record was created |
| is_markdown | bit | `0`=plaintext, `1`=Markdown |
| is_pinned | bit | `0`=not pinned, `1`=pinned |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *target__context | context | The [record type](/docs/records/#record-type) of the target record |
| *target_id | id | The ID of the target record |

## connected_account

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this connected account |
| *owner__context | context | The [record type](/docs/records/types/) of this connected account's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this connected account's owner |
| params | object | JSON-encoded key/value object |
| service_id | id | [Service Provider](/docs/plugins/extensions/points/cerb.connected_service.provider/) |
| updated_at | timestamp | The date/time when this record was last modified |
| uri | string | |

## connected_service

| Field | Type | Description |
|-|-|-|
| *extension_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this connected service |
| params | object | JSON-encoded key/value object |
| updated_at | timestamp | The date/time when this record was last modified |
| uri | string | |

## contact

| Field | Type | Description |
|-|-|-|
| dob | string | Date of birth: `YYYY-MM-DD` |
| email | string | Email address (e.g. `customer@example.com`); alternative to `email_id` |
| email_id | id | ID of this contact's primary [email address](/docs/records/types/address/) |
| *first_name | string | Given name |
| gender | string | Gender: `F` (female), `M` (male), or blank |
| image | image | The profile image, base64-encoded in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme) |
| language | string | Language: `en_US` |
| last_login_at | timestamp | Date of their last [community portal](/docs/portals/) login |
| last_name | string | Surname |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| location | string | Location (e.g. `Los Angeles, California, USA`) |
| mobile | string | Mobile number |
| org | string | Organization (e.g. `Fiaflux Software`); alternative to `org_id` |
| org_id | id | ID of this contact's [organization](/docs/records/types/org/) |
| phone | string | Phone number |
| timezone | string | Timezone (e.g. `America/Los_Angeles`) |
| title | string | Job title / Position |
| username | string | Username for public display |

## currency

| Field | Type | Description |
|-|-|-|
| code | string | Currency code; e.g. `USD` |
| decimal_at  | number | The number of significant decimal places (0-16); e.g. `2` for `0.00` |
| is_default  | bit | Is this the default currency? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| name | string | The singular name of this currency; `Dollar` |
| name_plural | string | The plural name of this currency; `Dollars` |
| symbol | string | Symbol; `$`, `£`, `€` |
| updated_at  | timestamp | The date/time when this record was last modified |

## custom_field

| Field | Type | Description |
|-|-|-|
| *context | context | The [record type](/docs/records/#record-type) to add the field to |
| custom_fieldset_id | id | The ID of the parent [custom fieldset](/docs/records/types/custom_fieldset/); if any |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this custom field |
| params | object | JSON-encoded key/value object |
| pos | uint | Display order; positive integer; `0` is first |
| *type | string | `C` (checkbox), `D` (picklist), `E` (date), `F` (file), `I` (files), `L` (record link), `M` (list), `N` (number), `O` (decimal), `S` (single line of text), `T` (multiple lines of text), `U` (url), `W` (worker), `X` (multiple checkboxes), `Y` (currency) |
| updated_at | timestamp | The date/time when this record was last modified |
| *uri | string | The unique alias for this custom field |

## custom_fieldset

| Field | Type | Description |
|-|-|-|
| *context | context | The [record type](/docs/records/types/) of the fieldset |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this custom fieldset |
| *owner__context | context | The [record type](/docs/records/types/) of this custom fieldset's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this custom fieldset's owner |
| updated_at | timestamp | The date/time when this record was last modified |

## custom_record

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The singular name of the record; `Issue` |
| *name_plural | string | The plural name of the record; `Issues` |
| params | object | JSON-encoded key/value object |
| updated_at | timestamp | The date/time when this record was last modified |
| *uri | string | The alias of the record (e.g. `issue`); used in URLs, API, etc. |

## draft

| Field | Type | Description |
|-|-|-|
| is_queued | bit | `1` for true, `0` for false |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| name | string | The subject line of the draft message (display hint; `params:subject:` controls actual subject) |
| params | object | JSON-encoded key/value object (see params keys by type below) |
| queue_delivery_date | uint | (0-4294967296) |
| queue_fails | uint | (0-4294967296) |
| ticket_id | id | The ID of the [ticket](/docs/records/types/ticket/) for `ticket.reply` or `ticket.forward` |
| to | string | The `To:` line of the draft message |
| token | string | A random unique token for this draft, copied to the eventual message for tracing |
| *type | string | The type of draft: `mail.compose`, `mail.transactional`, `ticket.reply`, or `ticket.forward` |
| updated | timestamp | The date/time when this record was last modified |
| worker_id | id | The ID of the [worker](/docs/records/types/worker/) who owns the draft |

### draft params by type

**Note:** `fields:to:` and `fields:name:` are display hints. The `params:to:` and `params:subject:` control the actual sent message. Currently both need to be set.

#### mail.transactional

| Param | Description |
|-|-|
| to | Recipient email address(es) |
| subject | Email subject line |
| content | Plain text message body |
| cc | CC recipients |
| bcc | BCC recipients |
| from | Sender address |
| from_personal | Sender display name |
| reply_to | Reply-to address |
| return_path | Return path address |
| format | `parsedown` or `plaintext` |
| file_ids | Attachment file IDs |
| headers | Custom email headers |
| html_template_id | HTML template to wrap content |
| options_gpg_encrypt | GPG encrypt the message |
| options_gpg_sign | GPG sign the message |

#### mail.compose

| Param | Description |
|-|-|
| to | Recipient email address(es) |
| subject | Email subject line |
| content | Plain text message body |
| cc | CC recipients |
| bcc | BCC recipients |
| format | `parsedown` or `plaintext` |
| file_ids | Attachment file IDs |
| headers | Custom email headers |
| group_id | **Required.** Group to create the ticket in |
| bucket_id | Bucket within the group |
| org_id | Organization to link |
| org_name | Organization name (alternative to `org_id`) |
| owner_id | Worker to assign |
| status_id | Initial ticket status |
| ticket_reopen | Reopen date if status is waiting |
| custom_fields | Ticket custom fields |
| message_custom_fields | Message custom fields |
| html_template_id | HTML template to wrap content |
| send_at | Scheduled send timestamp |
| options_gpg_encrypt | GPG encrypt the message |
| options_gpg_sign | GPG sign the message |

#### ticket.reply / ticket.forward

Inherits `to` (existing participants) and `subject` from the ticket. Only set in params if overriding.

| Param | Description |
|-|-|
| to | Override recipients |
| subject | Override subject |
| content | Plain text message body |
| cc | CC recipients |
| bcc | BCC recipients |
| format | `parsedown` or `plaintext` |
| file_ids | Attachment file IDs |
| headers | Custom email headers |
| group_id | Move ticket to group |
| bucket_id | Move ticket to bucket |
| status_id | Set ticket status after send |
| owner_id | Set ticket owner after send |
| custom_fields | Ticket custom fields |
| message_custom_fields | Message custom fields |
| html_template_id | HTML template to wrap content |
| in_reply_message_id | Specific message ID to reply to |
| is_autoreply | Mark as auto-reply |
| send_at | Scheduled send timestamp |
| ticket_reopen | Reopen date if status is waiting |
| options_gpg_encrypt | GPG encrypt the message |
| options_gpg_sign | GPG sign the message |

## address

| Field | Type | Description |
|-|-|-|
| contact_id | id | The [contact](/docs/records/types/contact/) linked to this email |
| created_at | timestamp | The date/time when this record was created |
| *email | string | An email address |
| host | string | The hostname of the email address |
| is_banned | bit | Is incoming email blocked? |
| is_defunct | bit | Is this address non-deliverable? |
| is_trusted | bit | Is this sender trusted to display external images and links? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mail_transport_id | id | If this address is used for outgoing mail, the [mail transport](/docs/records/types/mail_transport/) to use; otherwise empty |
| org | string | The exact name of the [organization](/docs/records/types/org/) linked to this email address; alternative to `org_id` |
| org_id | id | The [organization](/docs/records/types/org/) linked to this email |
| updated | timestamp | The date/time when this record was last modified |
| worker_id | id | Is this address owned by a [worker](/docs/records/types/worker/)? |

## mail_delivery_log

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| from_id | id | |
| header_message_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mail_transport_id | id | |
| status_id | number | (0-2) |
| status_message | string | |
| subject | string | |
| to | string | |
| type | string | |

## mail_inbound_log

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| events_log_json | string | |
| from_id | id | |
| header_message_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mailbox_id | id | |
| message_id | id | |
| parse_time_ms | uint | (0-4294967296) |
| status_id | number | (0-2) |
| status_message | string | |
| subject | string | |
| ticket_id | id | |
| to | string | |

## mailbox

| Field | Type | Description |
|-|-|-|
| checked_at | timestamp | The date/time this mailbox was last checked for new messages |
| connected_account_id | id | The optional connected account to use for XOAUTH2 |
| *host | string | The mail server hostname |
| is_enabled | bit | Is this mailbox enabled? `1` for true and `0` for false |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| max_msg_size_kb | uint | The maximum message size to download (in kilobytes); `0` to disable limits |
| *name | string | The name of this email mailbox |
| num_fails | uint | The number of consecutive failures |
| password | string | The mailbox password |
| port | uint | The port to connect to; e.g. `587` |
| protocol | string | The protocol to use: `pop3`, `pop3-ssl`, `imap`, `imap-ssl` |
| timeout_secs | uint | The socket timeout in seconds when downloading mail |
| updated_at | timestamp | The date/time when this record was last modified |
| *username | string | The mailbox username |

## mail_routing_rule

| Field | Type | Description |
|-|-|-|
| is_disabled  | bit | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this email routing rule |
| priority | number | (0-255) |
| routing_kata | string | |
| updated_at | timestamp | The date/time when this record was last modified |
| workflow_id  | id | |

## email_signature

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this email signature |
| *owner__context | context | The [record type](/docs/records/types/) of this email signature's owner: `app`, `role`, `group`, or `worker` |
| owner_id | id | The ID of this email signature's owner |
| *signature | string | The [template](/docs/scripting/) of the signature |
| signature_html  | string | The HTML [template](/docs/scripting/) of the signature |
| updated_at | timestamp | The date/time when this record was last modified |

## html_template

| Field | Type | Description |
|-|-|-|
| content | string | The content of the template |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this email template |
| *owner__context | context | The [record type](/docs/records/types/) of this email template's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this email template's owner |
| signature_id | id | The optional [email signature](/docs/records/types/email_signature/) of this template |
| updated_at | timestamp | The date/time when this record was last modified |

## mail_transport

| Field | Type | Description |
|-|-|-|
| created | timestamp | The date/time when this record was created |
| *extension_id | string | [Mail Transport Type](/docs/plugins/extensions/points/cerberusweb.mail.transport/) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this email transport |
| updated_at | timestamp | The date/time when this record was last modified |

## file_bundle

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this file bundle |
| *owner__context | context | The [record type](/docs/records/types/) of this file bundle's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this file bundle's owner |
| tag | string | A human-friendly nickname for the bundle; e.g. `tax_forms` |
| updated_at | timestamp | The date/time when this record was last modified |

## group

| Field | Type | Description |
|-|-|-|
| created | timestamp | The date/time when this record was created |
| image | image | The profile image, base64-encoded in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme) |
| is_default | bit | [Tickets](/docs/tickets/) are assigned to the default group when no other routing rules match |
| is_private | bit | The content in public (`0`) groups is visible to everyone; in private (`1`) groups content is only visible to members |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| members | string | JSON-encoded array of [worker](/docs/records/types/worker/) IDs; `[1,2,3]` |
| *name | string | The name of this group |
| reply_address_id | id | The ID of the [email address](/docs/records/types/address/) used when sending replies from this group |
| reply_html_template_id | id | The ID of the default [mail template](/docs/records/types/html_template/) used when sending HTML mail from this group |
| reply_personal | string | The default personal name in the `From:` of replies |
| reply_signature_id | id | The ID of the default [signature](/docs/records/types/email_signature/) used when sending replies from this group |
| reply_signing_key_id | id | The [private key](/docs/records/types/gpg_private_key/) used to cryptographically sign outgoing mail |
| routing_kata | string | Routing rules in KATA format |
| updated | timestamp | The date/time when this record was last modified |

## message

| Field | Type | Description |
|-|-|-|
| *content | string | Message content |
| content_html | string | Optional alternative content for the HTML version of a message |
| created | timestamp | The date/time when this record was created |
| hash_header_message_id | string | A SHA-1 hash of the `Message-Id:` header; used for message threading |
| *headers | string | Message headers |
| html_attachment_id | id | The [attachment](/docs/records/types/attachment/) ID containing the HTML message content |
| is_broadcast | bit | Was this message sent using the broadcast feature? |
| is_not_sent | bit | Was this message saved without sending? |
| is_outgoing | bit | Was this an outgoing reply from a worker? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| response_time | uint | Response time in seconds |
| sender | string | The [email address](/docs/records/types/address/) of the sender; alternative to `sender_id` |
| *sender_id | id | The ID of the sender's [email address](/docs/records/types/address/) record |
| storage_size | uint | Size of the message in bytes |
| *ticket_id | id | The ID of the message's [ticket](/docs/records/types/ticket/) record |
| ticket_mask | string | The parent [ticket](/docs/records/types/ticket/) mask; alternative to `ticket_id` |
| token | string | A random unique identifier for the message (synchronized with draft) |
| was_encrypted | bit | Was the message sent encrypted? |
| worker | string | The [worker](/docs/records/types/worker/) who sent the message (if any); alternative to `worker_id` |
| worker_id | id | If outgoing, the ID of the [worker](/docs/records/types/worker/) who sent the message |

## metric

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| description | string | |
| dimensions_kata | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this metric |
| type | string | [counter, gauge] |
| updated_at | timestamp | The date/time when this record was last modified |

## notification

| Field | Type | Description |
|-|-|-|
| *activity_point | string | The event that triggered the notification (or `custom.other`) |
| created | timestamp | The date/time when this record was created |
| is_read | bit | Has this been read by the worker? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *params | object | A key/value object of notification properties |
| target__context | context | The [record type](/docs/records/types/) of the target record |
| target_id | id | The ID of the target record |
| *worker_id | id | The ID of the [worker](/docs/records/types/worker/) who received the notification |

## oauth_app

| Field | Type | Description |
|-|-|-|
| access_token_ttl  | string | The expiration of the access token (e.g. '1 hour') |
| *callback_url | url | The OAuth2 callback URL of the app |
| *client_id | string | The client identifier of the app |
| *client_secret | string | The client secret of the app |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this oauth app |
| refresh_token_ttl | string | The expiration of the refresh token (e.g. '1 month') |
| scopes | string | The app's available scopes in YAML format |
| updated_at | timestamp | The date/time when this record was last modified |
| url | url | The app's URL |

## org

| Field | Type | Description |
|-|-|-|
| city | string | City |
| country  | string | Country |
| created  | timestamp | The date/time when this record was created |
| email_id | id | Primary [email address](/docs/records/types/address/) |
| image | image | The profile image, base64-encoded in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this organization |
| phone | string | Phone |
| postal | string | Postal code / ZIP |
| province | string | State / Province |
| street | string | Street address |
| updated  | timestamp | The date/time when this record was last modified |
| website  | url | Website |

## package

| Field | Type | Description |
|-|-|-|
| description | string | A description of this library package's contents |
| image | image | The profile image, base64-encoded in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this package |
| *package_json | string | |
| *point | string | The library section containing this package |
| updated_at | timestamp | The date/time when this record was last modified |
| *uri | string | The unique identifier of this package |

## gpg_private_key

| Field | Type | Description |
|-|-|-|
| expires_at | timestamp | |
| *fingerprint | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this pgp private key |
| updated_at | timestamp | The date/time when this record was last modified |

## gpg_public_key

| Field | Type | Description |
|-|-|-|
| expires_at | timestamp | The expiration date of the public key |
| *fingerprint | string | The fingerprint of the public key |
| *key_text | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this pgp public key |
| updated_at | timestamp | The date/time when this record was last modified |

## community_portal

| Field | Type | Description |
|-|-|-|
| code | string | Randomized internal ID for the portal |
| *extension_id | string | [Community Portal Type](/docs/plugins/extensions/points/cerb.portal/) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this portal |
| params | object | JSON-encoded key/value object |
| updated_at | timestamp | The date/time when this record was last modified |
| *uri | string | Human-friendly nickname for the portal. Must be unique. |

## profile_tab

| Field | Type | Description |
|-|-|-|
| *context | context | The [record type](/docs/records/types/) to add the profile tab to |
| *extension_id | string | [Profile Tab Type](/docs/plugins/extensions/points/cerb.profile.tab/) |
| extension_params | object | JSON-encoded key/value object |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this profile tab |
| pos | uint | (0-65536) |
| updated_at | timestamp | The date/time when this record was last modified |

## profile_widget

| Field | Type | Description |
|-|-|-|
| *extension_id | string | [Profile Widget Type](/docs/plugins/extensions/points/cerb.profile.tab.widget/) |
| extension_params | object | JSON-encoded key/value object |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this profile widget |
| options_kata | string | |
| pos | number | The order of the widget on the profile; `0` is first (top-left) proceeding in rows then columns |
| *profile_tab_id  | id | The ID of the [profile tab](/docs/records/types/profile_tab/) dashboard containing this widget |
| updated_at | timestamp | The date/time when this record was last modified |
| width_units | number | `1` (25%), `2` (50%), `3` (75%), `4` (100%) |
| zone | string | The name of the dashboard zone containing the widget; this varies by layout; generally `sidebar` and `content` |

## project_board_column

| Field | Type | Description |
|-|-|-|
| *board_id | id | The [project board](/docs/records/types/project_board/) containing this column |
| cards | links | An array of record `type:id` tuples to add to this column |
| cards_kata | string | |
| functions_kata | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this project board column |
| pos | uint | (0-4294967296) |
| toolbar_kata | string | |
| updated_at | timestamp | The date/time when this record was last modified |

## project_board

| Field | Type | Description |
|-|-|-|
| cards_kata | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this project board |
| owner__context | context | The [record type](/docs/records/types/) of this project board's owner: `app`, `role`, `group`, or `worker` |
| owner_id | id | The ID of this project board's owner |
| updated_at | timestamp | The date/time when this record was last modified |

## queue

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this queue |
| updated_at | timestamp | The date/time when this record was last modified |

## reminder

| Field | Type | Description |
|-|-|-|
| is_closed  | bit | Has this reminder elapsed? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this reminder |
| *remind_at | timestamp | The date/time of the reminder |
| updated_at | timestamp | The date/time when this record was last modified |
| *worker_id | id | The ID of the [worker](/docs/records/types/worker/) receiving the reminder |

## resource

| Field | Type | Description |
|-|-|-|
| automation_kata | string | |
| cache_until | timestamp | |
| content | string | The optional content of this resource. For text, use a string. For binary, base64-encode in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme). This may also be an automation resource URI (e.g. `cerb:automation_resource:TOKEN`) |
| description | string | |
| *extension_id | string | A [cerb.resource.type](/docs/plugins/extensions/points/cerb.resource.type/#extensions) extension ID. |
| is_dynamic | bit | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this resource |
| updated_at | timestamp | The date/time when this record was last modified |

## role

| Field | Type | Description |
|-|-|-|
| editor_query_worker | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| member_query_worker | string | |
| *name | string | The name of this role |
| privs_mode | string | ["", all, itemized] |
| reader_query_worker | string | |
| updated_at | timestamp | The date/time when this record was last modified |

## saved_search

| Field | Type | Description |
|-|-|-|
| *context | context | The [record type](/docs/records/types/) of this search query; e.g. `ticket` |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this saved search |
| *owner__context | context | The [record type](/docs/records/types/) of this saved search's owner: `app`, `role`, `group`, or `worker` |
| owner_id | id | The ID of this saved search's owner |
| *query | string | The [search query](/docs/search/); e.g. `status:o` |
| tag | string | A human-friendly nickname for this search (e.g. `open_tickets`) |
| updated_at | timestamp | The date/time when this record was last modified |

## search_index

| Field | Type | Description |
|-|-|-|
| *extension_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this search index |
| priority | uint | (0-255) |
| record_filter | string | |
| record_type | string | |
| updated_at | timestamp | The date/time when this record was last modified |
| uri | string | |

## snippet

| Field | Type | Description |
|-|-|-|
| *content | string | The [template](/docs/scripting/) of the snippet |
| context | string | The [record type](/docs/records/types/) to add the profile tab to |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *owner__context | context | The [record type](/docs/records/types/) of this snippet's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this snippet's owner |
| prompts_kata | string | Prompted placeholders in [KATA](/docs/snippets/#prompts) format |
| *title | string | The name of the snippet |
| total_uses | uint | The total number of times this snippet has been used by all workers |
| updated_at | timestamp | The date/time when this record was last modified |

## task

| Field | Type | Description |
|-|-|-|
| completed  | timestamp | The date/time this task was completed |
| created | timestamp | The date/time when this record was created |
| due | timestamp | The date/time of this task's deadline |
| fieldsets  | fieldsets | An array or comma-separated list of [custom fieldset](/docs/records/types/custom_fieldset/) IDs. Prefix an ID with `-` to remove. |
| importance | uint | A number from `0` (least) to `100` (most) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| owner_id | id | The ID of the [worker](/docs/records/types/worker/) responsible for this task |
| reopen | timestamp | If the status is `waiting`, the date/time to automatically change the status back to `open` |
| status | string | `o` (open), `w` (waiting), `c` (closed); alternative to `status_id` |
| status_id  | uint | `0` (open), `1` (closed), `2` (waiting); alternative to `status` |
| *title | string | The name of this task |
| updated | timestamp | The date/time when this record was last modified |

## ticket

| Field | Type | Description |
|-|-|-|
| bucket | string | The [bucket](/docs/records/types/bucket/) name of the ticket; alternative to `bucket_id`. If used, a `group` or `group_id` must also be provided at the same time. |
| bucket_id | id | The ID of the [bucket](/docs/records/types/bucket/) containing this ticket |
| closed | timestamp | The date/time this ticket was first set to status `closed` |
| created | timestamp | The date/time when this record was created |
| fieldsets | fieldsets | An array or comma-separated list of [custom fieldset](/docs/records/types/custom_fieldset/) IDs. Prefix an ID with `-` to remove. |
| group | string | The [group](/docs/records/types/group/) of the ticket; alternative to `group_id` |
| *group_id | id | The ID of the [group](/docs/records/types/group/) containing this ticket |
| importance | number | A number from `0` (least) to `100` (most) |
| last_opened_at  | timestamp | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| mask | string | The randomized reference number for this ticket; auto-generated if blank |
| org | string | The exact name of the [organization](/docs/records/types/org/) linked to this ticket; alternative to `org_id` |
| org_id | id | The ID of the [organization](/docs/records/types/org/) linked to this ticket; alternative to `org` |
| owner_id | id | The ID of the [worker](/docs/records/types/worker/) responsible for this ticket |
| participant_ids | string | A comma-separated list of email addresses IDs to add or remove as participants. Prefix an ID with `-` to remove |
| participants | string | A comma-separated list of email addresses to add as participants |
| reopen_date | timestamp | If status `waiting`, the date/time to automatically change the status back to `open` |
| spam_score | float | `0.0001` (not spam) to `0.9999` (spam); automatically generated |
| spam_training | string | `S` (spam), `N` (not spam); blank for non-trained |
| status | string | `o` (open), `w` (waiting), `c` (closed), `d` (deleted); alternative to `status_id` |
| status_id | number | `0` (open), `1` (waiting), `2` (closed), `3` (deleted); alternative to `status` |
| *subject | string | The subject of the ticket |
| updated | timestamp | The date/time when this record was last modified |

## timetracking_activity

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this time tracking activity |
| updated_at | timestamp | The date/time when this record was last modified |

## time_entry

| Field | Type | Description |
|-|-|-|
| activity_id | id | The ID of the [activity](/docs/records/types/timetracking_activity/) for the work |
| is_closed | bit | Is this time entry archived? |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| log_date | timestamp | The date/time of the work |
| *mins | uint | The number of minutes worked (alternative to `secs`) |
| *secs | uint | The number of seconds worked (alternative to `mins`) |
| *worker_id  | id | The ID of the [worker](/docs/records/types/worker/) who completed the work |

## toolbar_section

| Field | Type | Description |
|-|-|-|
| is_disabled | bit | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this toolbar section |
| priority | number | (0-255) |
| toolbar_kata  | string | |
| *toolbar_name | string | |
| updated_at | timestamp | The date/time when this record was last modified |
| workflow_id | id | |

## toolbar

| Field | Type | Description |
|-|-|-|
| created_at | timestamp | The date/time when this record was created |
| description | string | |
| *extension_id | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this toolbar |
| updated_at | timestamp | The date/time when this record was last modified |

## webapi_credentials

| Field | Type | Description |
|-|-|-|
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this api key |
| updated_at | timestamp | The date/time when this record was last modified |
| *worker_id | id | The ID of the [worker](/docs/records/types/worker/) who owns these API credentials |

## webhook_listener

| Field | Type | Description |
|-|-|-|
| automations_kata | object | KATA object |
| *guid | string | The random unique alias of the webhook used in its URL; automatically generated if blank |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this webhook |
| updated_at | timestamp | The date/time when this record was last modified |

## worker

| Field | Type | Description |
|-|-|-|
| at_mention_name | string | The nickname used for `@mention` notifications in comments |
| calendar_id | id | The ID of the [calendar](/docs/records/types/calendar/) used to compute worker availability |
| dob | string | Date of birth in `YYYY-MM-DD` format |
| email | string | The primary email address of the worker; alternative to `email_id` |
| *email_id | id | The ID of the primary [email address](/docs/records/types/address/); alternative to `email` |
| email_ids | string | A comma-separated list of IDs for alternative [email addresses](/docs/records/types/address/) |
| *first_name | string | Given name |
| gender | string | `F` (female), `M` (male), or blank or unknown |
| image | image | The profile image, base64-encoded in [data URI format](https://en.wikipedia.org/wiki/Data_URI_scheme) |
| is_disabled | bit | Is this worker deactivated and prevented from logging in? |
| is_mfa_required | bit | Is this worker required to use multi-factor authentication? |
| is_password_disabled | bit | Is this worker allowed to log in with a password? |
| is_superuser | bit | Is this worker an administrator with full privileges? |
| *language | string | ISO-639 language code and ISO-3166 country code; e.g. `en_US` |
| last_name | string | Surname |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| location | string | Location description; `Los Angeles, CA, USA` |
| mobile | string | Mobile number |
| password | string | The worker's password, if applicable; stored security; will be automatically generated if blank |
| phone | string | |
| time_format | string | Preference for displaying timestamps, `DateTime()` syntax |
| timeout_idle_secs | number | Consider a session idle after this many seconds of inactivity |
| *timezone | string | IANA tz/zoneinfo timezone; `America/Los_Angeles` |
| title | string | Job title / Position |
| updated | timestamp | The date/time when this record was last modified |

## workflow

| Field | Type | Description |
|-|-|-|
| config_kata | string | |
| created_at | timestamp | The date/time when this record was created |
| description | string | |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this workflow |
| resources_kata | string | |
| updated_at | timestamp | The date/time when this record was last modified |
| version | uint | (0-4294967296) |
| workflow_kata  | string | |

## workspace_page

| Field | Type | Description |
|-|-|-|
| *extension_id | string | [Workspace Page Type](/docs/plugins/extensions/points/cerberusweb.ui.workspace.page/) |
| extension_params | object | JSON-encoded key/value object |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this workspace page |
| *owner__context  | context | The [record type](/docs/records/types/) of this workspace page's owner: `app`, `role`, `group`, or `worker` |
| *owner_id | id | The ID of this workspace page's owner |
| updated_at | timestamp | The date/time when this record was last modified |

## workspace_tab

| Field | Type | Description |
|-|-|-|
| *extension_id | string | [Workspace Tab Type](/docs/plugins/extensions/points/cerberusweb.ui.workspace.tab/) |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this workspace tab |
| options_kata  | string | |
| *page_id | id | The ID of the [workspace page](/docs/records/types/workspace_page/) containing this tab |
| params | object | JSON-encoded key/value object |
| pos | uint | The position of this tab on the workspace page; `0` is first |
| updated_at | timestamp | The date/time when this record was last modified |

## workspace_widget

| Field | Type | Description |
|-|-|-|
| *extension_id | string | [Workspace Widget Type](/docs/plugins/extensions/points/cerberusweb.ui.workspace.widget/) |
| *label | string | The human-friendly name of the widget |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| options_kata  | string | |
| params | object | JSON-encoded key/value object |
| pos | number | The position of the widget on the dashboard; `0` is first (top-right); rows before columns |
| *tab_id | id | The ID of the [workspace tab](/docs/records/types/workspace_tab/) containing this widget |
| updated_at | timestamp | The date/time when this record was last modified |
| width_units | number | `1` (25%), `2` (50%), `3` (75%), `4` (100%) |
| zone | string | The name of the dashboard zone containing the widget; this varies by layout; generally `sidebar` and `content` |

## workspace_list

| Field | Type | Description |
|-|-|-|
| columns | object | JSON-encoded key/value array of column names |
| *context | context | The [record type](/docs/records/types/) of the worklist |
| links | links | An array of record `type:id` tuples to link to. Prefix with `-` to unlink. |
| *name | string | The name of this workspace worklist |
| options | object | JSON-encoded key/value object |
| params_required_query | string | The [search query](/docs/search/) for required filters |
| pos | uint | The order of the worklist on the workspace tab; `0` is first |
| render_limit | uint | The number of records per page |
| *tab_id | id | The ID of the [workspace tab](/docs/records/types/workspace_tab/) containing this worklist |
| updated_at | timestamp | The date/time when this record was last modified |

