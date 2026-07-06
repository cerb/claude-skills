# Bot Behaviors (Virtual Attendants / VA)

> **Deprecated but widely used.** Bot behaviors (`trigger_event` / `decision_node` tables) are the legacy automation system, superseded by Automations. Many large clients still depend on them heavily. Do not remove existing behaviors without careful migration planning.

## Key Classes

| Class | File |
|---|---|
| `DAO_TriggerEvent` | `features/cerberusweb.core/api/dao/trigger_event.php` |
| `DAO_DecisionNode` | `features/cerberusweb.core/api/dao/decision_node.php` |
| `DAO_Bot` | `features/cerberusweb.core/api/dao/bot.php` |
| `Extension_DevblocksEvent` | `libs/devblocks/api/Extension.php:2252` |
| `Extension_DevblocksEventAction` | `libs/devblocks/api/Extension.php:4255` |
| `Extension_DevblocksEventCondition` | `libs/devblocks/api/Extension.php:4219` |

Abstract event base classes: `features/cerberusweb.core/api/events/abstract/`  
Action implementations: `features/cerberusweb.core/api/bots/actions/`

---

## Package Format

Bot behaviors are imported via packages. Behaviors can be nested inside a `bots[]` entry, or listed at the top level with `"bot_id": "{{{bot_id}}}"`.

### Nested inside bot (preferred for new bots)

```json
{
  "package": {
    "name": "My Bot",
    "revision": 1,
    "requires": { "cerb_version": "11.2.0", "plugins": [] },
    "configure": { "placeholders": [], "prompts": [] }
  },
  "bots": [
    {
      "uid": "bot_my_bot",
      "name": "My Bot",
      "owner": { "context": "app", "id": 0 },
      "is_disabled": false,
      "params": {
        "config": {},
        "events": { "mode": "all", "items": [] },
        "actions": { "mode": "all", "items": [] }
      },
      "behaviors": [
        {
          "uid": "behavior_example",
          "title": "Example behavior",
          "is_disabled": false,
          "is_private": false,
          "priority": 50,
          "event": { "key": "event.mail.received", "label": "New message added to ticket" },
          "variables": {},
          "nodes": [ /* decision tree */ ]
        }
      ]
    }
  ]
}
```

**Owner contexts:**

| Owner type | `context` value | `id` value | Notes |
|---|---|---|---|
| App (Cerb) | `"app"` | `0` | Short form; the only case where short form is used |
| Group | `"cerberusweb.contexts.group"` | group record id | Must use full context ID |
| Worker | `"cerberusweb.contexts.worker"` | worker record id | Must use full context ID |

For configurable import, use template vars `{{{prompt_owner_context}}}` / `{{{prompt_owner_context_id}}}`, or add an explicit chooser prompt (see Configure Prompts below).

---

## Configure Prompts (group- and worker-owned packages)

To let the admin pick the owning group or worker at import time, add a chooser prompt:

```json
"configure": {
  "placeholders": [],
  "prompts": [
    {
      "type": "chooser",
      "label": "Group",
      "key": "group_id",
      "hidden": false,
      "params": {
        "context": "cerberusweb.contexts.group",
        "single": true,
        "query": ""
      }
    }
  ]
}
```

Then reference the chosen value in the bot owner:

```json
"owner": { "context": "cerberusweb.contexts.group", "id": "{{{group_id}}}" }
```

For a worker chooser, use `"context": "cerberusweb.contexts.worker"` and key `"worker_id"`. To default the chooser to a specific record (e.g. worker 1), set `"query": "id:1"`.

---

## Event Availability by Owner Type

The framework (`Extension_DevblocksEvent::getByContext()` in `libs/devblocks/api/Extension.php`) filters available events per bot owner type:

| Owner | Events available |
|---|---|
| App (`app`) | All 42 events |
| Group (`cerberusweb.contexts.group`) | 8 group-scoped events (see below) |
| Worker (`cerberusweb.contexts.worker`) | ~25 events |

**Group-scoped events (all 8):**

- `event.mail.received.group` — New message in group
- `event.mail.assigned.group` — Ticket assigned in group
- `event.mail.closed.group` — Ticket closed in group
- `event.mail.moved.group` — Ticket moved in group
- `event.mail.sent.group` — Ticket sent by group
- `event.mail.after.sent.group` — After sending worker reply in group
- `event.comment.ticket.group` — New comment on a ticket in a group
- `event.macro.group` — Custom behavior on group

**Group event variables:** `group_id`, `group_name`, `group_is_private`, `group_is_default`, `group_reply_personal`.  
**Note:** `bucket_id` and `bucket_name` are **not** available in group events — they are scrubbed by the framework.

### Standalone behaviors referencing an existing bot

```json
{
  "behaviors": [
    {
      "uid": "behavior_example",
      "bot_id": "{{{bot_id}}}",
      "title": "...",
      "event": { "key": "event.mail.received", "label": "..." },
      "nodes": []
    }
  ]
}
```

### Standalone behavior nodes (library snippets)

Used for reusable action snippets that get inserted into existing behaviors:

```json
{
  "behavior_nodes": [
    {
      "uid": "node_close_chat",
      "behavior_id": "{{{behavior_id}}}",
      "parent_id": "{{{parent_id}}}",
      "type": "action",
      "title": "Close chat window",
      "status": "live",
      "params": { "actions": [{ "action": "window_close" }] }
    }
  ]
}
```

Package library point for these: `"point": "behavior_action:event.message.chat.worker"`

---

## Behavior Variables

Defined at the behavior level, available throughout the decision tree:

```json
"variables": {
  "var_example": {
    "key": "var_example",
    "label": "Example",
    "type": "S",
    "is_private": "0",
    "params": {}
  }
}
```

**Types:** `S` = single-line string, `M` = multi-line, `N` = number, `D` = date, `C` = checkbox/bool, `L` = list, `O` = object/dict

---

## Decision Tree Node Types

All node objects share:

```json
{
  "type": "switch|outcome|action|loop",
  "title": "Human-readable label",
  "status": "live",
  "params": { /* type-specific */ },
  "nodes": [ /* children */ ]
}
```

**`status` values:** `"live"` (active), `"disabled"`, `"simulator"` (only in simulator)

### switch

Decision branching point. Children must be `outcome` nodes.

```json
{ "type": "switch", "title": "Check conditions", "status": "live", "nodes": [ /* outcomes */ ] }
```

### outcome

Branch within a switch. Has condition groups; matched children execute.

```json
{
  "type": "outcome",
  "title": "First incoming message",
  "status": "live",
  "params": {
    "groups": [
      {
        "any": 0,
        "conditions": [
          { "condition": "is_first", "bool": "1" },
          { "condition": "is_outgoing", "bool": "0" }
        ]
      }
    ]
  },
  "nodes": [ /* child nodes */ ]
}
```

`"any": 0` = ALL conditions must match (AND). `"any": 1` = ANY condition matches (OR).  
Multiple groups: all groups must be true (groups are ANDed together).  
**Default/catch-all outcome:** `"conditions": []` (empty — always matches).

### action

Executes one or more actions in sequence.

```json
{
  "type": "action",
  "title": "Set variable and exit",
  "status": "live",
  "params": {
    "actions": [
      { "action": "_set_custom_var", "var": "my_var", "value": "hello", "format": "", "is_simulator_only": "0" },
      { "action": "_exit", "mode": "" }
    ]
  }
}
```

### loop

Iterates over a JSON array.

```json
{
  "type": "loop",
  "title": "For each ticket",
  "status": "live",
  "params": {
    "foreach_json": "{{_tickets|json_encode}}",
    "as_placeholder": "_ticket"
  },
  "nodes": [ /* executed each iteration */ ]
}
```

---

## Universal Conditions (available on all events)

### `_custom_script`

Evaluates a Twig template, compares result to a value.

```json
{
  "condition": "_custom_script",
  "tpl": "{% if ticket_subject|length > 0 %}true{% endif %}",
  "oper": "is",
  "value": "true"
}
```

**Operators:** `is`, `!is`, `contains`, `!contains`, `like`, `!like`, `regexp`, `!regexp`

### `_day_of_week`

```json
{ "condition": "_day_of_week", "oper": "is", "day": [1,2,3,4,5] }
```

`"oper"`: `"is"` or `"!is"`. Days: `1`=Mon … `7`=Sun (ISO 8601, uses PHP `date('N')`).

### `_day_of_month`

```json
{ "condition": "_day_of_month", "oper": "is", "value": 1 }
```

`"oper"`: `"is"`, `"!is"`, `"gt"`, `"lt"`. `"value"`: integer 1–31.

### `_month_of_year`

```json
{ "condition": "_month_of_year", "oper": "is", "month": [1,2,3] }
```

`"oper"`: `"is"` or `"!is"`. Months: `1`=Jan … `12`=Dec.

### `_time_of_day`

```json
{ "condition": "_time_of_day", "oper": "between", "from": "8am", "to": "5pm" }
```

`"oper"`: `"between"` or `"!between"`. Time strings: `"8am"`, `"17:30"`, `"noon"`, etc.

### `_calendar_availability`

```json
{
  "condition": "_calendar_availability",
  "calendar_id": "123",
  "is_available": "1",
  "from": "today",
  "to": "tomorrow"
}
```

`"is_available"`: `"1"` = available, `"0"` = busy. Dates use `strtotime()` format.

---

## Event-Specific Conditions

### Mail/message events (`event.mail.received`, `event.mail.received.group`, `event.macro.message`, etc.)

```json
{ "condition": "is_first", "bool": "1" }
{ "condition": "is_outgoing", "bool": "0" }
{ "condition": "sender_is_worker", "bool": "0" }
{ "condition": "ticket_has_owner", "bool": "1" }
{ "condition": "sender_address", "oper": "like", "value": "noreply@*" }
{ "condition": "headers", "header": "Auto-Submitted", "oper": "!is", "value": "" }
{ "condition": "ticket_status", "oper": "is", "value": "0" }
```

`ticket_status` values: `"0"` = open, `"1"` = waiting, `"2"` = closed.  
`headers` operators: `"is"`, `"!is"`, `"contains"`, `"like"`.

### Ajax/API events (`event.ajax.request`, `event.api.custom_request`)

```json
{ "condition": "http_verb", "oper": "is", "value": "GET" }
{ "condition": "http_path", "oper": "like", "value": "/api/test*" }
{ "condition": "http_param", "name": "action", "oper": "is", "value": "ping" }
{ "condition": "http_header", "name": "X-Token", "oper": "!is", "value": "" }
{ "condition": "http_body", "oper": "contains", "value": "query" }
{ "condition": "http_client_ip", "oper": "is", "value": "127.0.0.1" }
```

### Worker events (`event.ticket.viewed.worker`, `event.notification.received.worker`, `event.macro.worker`, etc.)

```json
{ "condition": "worker_is_superuser", "bool": "1" }
{ "condition": "worker_is_disabled", "bool": "0" }
{ "condition": "ticket_status", "oper": "is", "value": "0" }
{ "condition": "ticket_has_owner", "bool": "1" }
```

### Interactions event (`event.interactions.get.worker`)

```json
{ "condition": "point", "oper": "is", "value": "cerb.toolbar.global" }
```

---

## Surfacing worker interactions (binding & launch)

The two worker-interaction styles bind to a toolbar / the global menu **differently**. Launch is routed
by `PageSection_ProfilesAutomation::_profileAction_startInteraction()`
(`features/cerberusweb.core/api/uri/profiles/automation.php`):

- `interaction_uri` (numeric id, behavior `uri`, or `cerb:behavior:<id-or-uri>`) → `getByUri`/`get` →
  **`startBotInteractionAsFormBehavior()`** — used for `event.form.interaction.worker`.
- `behavior_id` POST field (emitted by legacy `behavior/` toolbar items) →
  **`startBotInteractionAsConvoBehavior()`** — requires `event.interaction.chat.worker`; that opener then
  `switch_behavior`s to an `event.message.chat.worker` behavior. **A form behavior launched this way 404s.**

**Chat = a 3-behavior chain, auto-injected into the global menu** (`Toolbar_GlobalMenu::getInteractionsMenu`
→ `Event_GetInteractionsForWorker::getInteractionsByPointAndWorker('global', …)`):
1. Registrar (`event.interactions.get.worker`, event param `listen_points: global`) → `return_interaction`
   → the opener's id.
2. Opener (`event.interaction.chat.worker`) → `switch_behavior` → the message behavior.
3. Message (`event.message.chat.worker`) — holds the prompts.

The registrar result is cached per point for 900s (`interactions_<point>`); saving a registrar clears it.

**Form = a toolbar section + a behavior URI** (NOT auto-injected). Add an `interaction/` item whose `uri`
is the behavior — a **record URI is a first-class interaction binding**, consistent with how many DAOs
implement `getByUri()` + resolve the record in `renderPeekPopup`:

```
interaction/myForm:
  label: My Form
  icon: form
  uri: cerb:behavior:my_behavior_uri   # or cerb:behavior:<id>
```

Package it via a top-level `toolbars: [{ toolbar: "global.menu", kata: "…" }]` (import is additive — it
appends a `DAO_ToolbarSection`, never overwrites). Behavior URIs are **alphanumeric + underscore only —
no dots** (unlike dotted automation names).

Gotchas (both bit us, both code-level):
- **`DevblocksUiToolbar::enforceCallerPolicy()`** hides an `interaction/` item whose `uri` doesn't resolve
  to an automation. To let a `cerb:behavior:` uri through, it must recognize the behavior (else the item is
  silently dropped from the menu). Behavior visibility is enforced at launch (readability), not by an
  automation caller policy.
- **`getByUri` prefix inconsistency:** `DAO_Automation::getByUri()` strips the `cerb:` prefix (via
  `parseURI`/`getByUris`); **`DAO_TriggerEvent::getByUri()` matches the stored uri verbatim** (no strip).
  When resolving a `cerb:behavior:x` reference, `parseURI()` to the bare token **first**, then branch
  numeric-id (`get`) vs uri (`getByUri`) — don't `is_numeric()` the still-prefixed string.

The Setup → Developers → Toolbars overview (`config/toolbars.php`) parses raw KATA (keeps the `cerb:`
prefix, unlike the runtime parser) and resolves each item to a clickable `{context, id, url}` peek — same
pattern automation-event bindings use.

---

## All Event Types

| Event key | Label |
|---|---|
| `event.ajax.request` | Respond to Ajax HTTP request |
| `event.api.custom_request` | Custom API request |
| `event.mail.received.app` | Filter new incoming message |
| `event.record.changed` | Record changed |
| `event.mail.received` | New message added to ticket |
| `event.mail.received.group` | New message in group |
| `event.mail.before.sent` | Before sending worker reply |
| `event.mail.after.sent` | After sending worker reply |
| `event.mail.after.sent.group` | After sending worker reply in group |
| `event.mail.assigned.group` | Ticket assigned in group |
| `event.mail.closed.group` | Ticket closed in group |
| `event.mail.moved.group` | Ticket moved in group |
| `event.mail.sent.group` | Ticket sent by group |
| `event.mail.received.watcher` | New message received (watcher) |
| `event.mail.compose.pre.ui.worker` | Before composing a new message (worker) |
| `event.mail.reply.pre.ui.worker` | Before composing a reply (worker) |
| `event.comment.created.worker` | Comment created by worker |
| `event.comment.ticket.group` | New comment on a ticket in a group |
| `event.interaction.chat.worker` | Conversation with worker |
| `event.interactions.get.worker` | Get chat interactions for worker |
| `event.message.chat.worker` | New message in chat with worker |
| `event.form.interaction.worker` | Form interaction with worker |
| `event.notification.received.worker` | Notification received by worker |
| `event.ticket.viewed.worker` | Ticket opened by worker |
| `event.data.query.datasource` | Data query datasource |
| `event.macro.address` | Custom behavior on address |
| `event.macro.bot` | Custom behavior on bot |
| `event.macro.calendar` | Custom behavior on calendar |
| `event.macro.calendar_event` | Custom behavior on calendar event |
| `event.macro.contact` | Custom behavior on contact |
| `event.macro.group` | Custom behavior on group |
| `event.macro.message` | Custom behavior on message |
| `event.macro.notification` | Custom behavior on notification |
| `event.macro.org` | Custom behavior on organization |
| `event.macro.reminder` | Custom behavior on reminder |
| `event.macro.task` | Custom behavior on task |
| `event.macro.ticket` | Custom behavior on ticket |
| `event.macro.worker` | Custom behavior on worker |
| `event.dashboard.widget.render` | Dashboard widget rendered |
| `event.dashboard.widget.get_metric` | Dashboard get metric for widget |
| `event.ui.worklist.render.worker` | Worklist rendered by worker |
| `event.behavior.recurrent` | Recurrent behavior (Legacy) |

---

## Actions Reference

### Built-in (available on all events)

#### `_set_custom_var`

```json
{
  "action": "_set_custom_var",
  "var": "var_result",
  "value": "{{ticket_mask}}",
  "format": "",
  "is_simulator_only": "0"
}
```

`"format"`: `""` (plain text) or `"json"` (parse output as JSON).

#### `_exit`

```json
{ "action": "_exit", "mode": "" }
```

### Registered extension actions

#### `core.bot.action.record.search`

```json
{
  "action": "core.bot.action.record.search",
  "context": "ticket",
  "query": "status:o worker:{{current_worker_id}} limit:25",
  "expand": "owner_,group_",
  "object_placeholder": "_records"
}
```

#### `core.bot.action.record.retrieve`

```json
{
  "action": "core.bot.action.record.retrieve",
  "context": "ticket",
  "id": "{{ticket_id}}",
  "expand": "custom_,owner_",
  "object_placeholder": "_record"
}
```

#### `core.bot.action.record.create`

```json
{
  "action": "core.bot.action.record.create",
  "context": "task",
  "changeset_json": "{% set json = {'title': 'Follow up', 'owner_id': current_worker_id} %}\n{{json|json_encode}}",
  "run_in_simulator": "0",
  "object_placeholder": "_new_record"
}
```

#### `core.bot.action.record.update`

```json
{
  "action": "core.bot.action.record.update",
  "context": "ticket",
  "id": "{{ticket_id}}",
  "changeset_json": "{% set json = {'status': 'o'} %}\n{{json|json_encode}}",
  "run_in_simulator": "0"
}
```

#### `core.bot.action.record.upsert`

```json
{
  "action": "core.bot.action.record.upsert",
  "context": "contact",
  "query": "email:{{sender_address}}",
  "changeset_json": "{% set json = {'email': sender_address, 'name': sender_name} %}\n{{json|json_encode}}",
  "run_in_simulator": "0",
  "object_placeholder": "_record"
}
```

#### `core.bot.action.record.delete`

```json
{
  "action": "core.bot.action.record.delete",
  "context": "notification",
  "id": "{{notification_id}}"
}
```

#### `core.va.action.http_request`

```json
{
  "action": "core.va.action.http_request",
  "http_verb": "POST",
  "http_url": "https://api.example.com/endpoint",
  "http_headers": "Content-Type: application/json\nAuthorization: Bearer {{token}}",
  "http_body": "{\"key\":\"value\"}",
  "auth": "",
  "auth_connected_account_id": "0",
  "options[ignore_ssl_errors]": "0",
  "options[raw_response_body]": "0",
  "run_in_simulator": "1",
  "response_placeholder": "_http_response"
}
```

#### `core.bot.action.data_query`

```json
{
  "action": "core.bot.action.data_query",
  "query": "type:worklist.records of:ticket query:(status:o) limit:50 format:dictionaries",
  "run_in_simulator": "1",
  "object_placeholder": "_results"
}
```

#### `core.bot.action.automation`

```json
{
  "action": "core.bot.action.automation",
  "automation_id": "0",
  "automation_params_json": "{\"ticket_id\":\"{{ticket_id}}\"}",
  "run_in_simulator": "0",
  "object_placeholder": "_automation_results"
}
```

#### `core.bot.action.create_reminder` (deprecated)

```json
{
  "action": "core.bot.action.create_reminder",
  "name": "Follow up on {{ticket_subject}}",
  "remind_at": "+1 day",
  "worker_id": "{{ticket_owner_id}}",
  "object_placeholder": "_reminder_meta",
  "run_in_simulator": "0"
}
```

#### `core.bot.action.calculate_time_elapsed`

```json
{
  "action": "core.bot.action.calculate_time_elapsed",
  "calendar_id": "0",
  "date_from": "{{ticket_created_at}}",
  "date_to": "now",
  "placeholder": "_elapsed_seconds"
}
```

#### `core.va.action.create_attachment` (deprecated)

```json
{
  "action": "core.va.action.create_attachment",
  "file_name": "export-{{ticket_mask}}.txt",
  "file_type": "text/plain",
  "content": "{{ticket_latest_message_content}}",
  "content_encoding": "",
  "object_placeholder": "_attachment_meta",
  "run_in_simulator": "0"
}
```

`"content_encoding"`: `""` (plain text) or `"base64"`.

#### `core.bot.action.email_parser`

```json
{
  "action": "core.bot.action.email_parser",
  "content": "From: {{sender_address}}\nSubject: {{ticket_subject}}\n\n{{ticket_latest_message_content}}",
  "object_placeholder": "_parsed_email"
}
```

#### `core.bot.action.package.import`

```json
{
  "action": "core.bot.action.package.import",
  "package_json": "{\"package\":{\"name\":\"...\",\"revision\":1,\"requires\":{\"cerb_version\":\"11.0.0\",\"plugins\":[]},\"configure\":{\"placeholders\":[],\"prompts\":[]}}}",
  "prompts_json": "{}",
  "run_in_simulator": "0",
  "object_placeholder": "_import_results"
}
```

#### `core.bot.action.pgp.encrypt`

```json
{
  "action": "core.bot.action.pgp.encrypt",
  "public_key_ids": [],
  "public_key_template": "",
  "message": "{{message_content}}",
  "object_placeholder": "_pgp_results"
}
```

#### `core.bot.action.interaction_proactive.schedule`

```json
{
  "action": "core.bot.action.interaction_proactive.schedule",
  "on": "{{current_worker__key}}",
  "behavior_id": "0",
  "interaction": "my.interaction.id",
  "interaction_params_json": "{\"ticket_id\":\"{{ticket_id}}\"}",
  "expires": "+5 minutes",
  "run_in_simulator": "0"
}
```

### Mail event actions (`event.mail.received`, `event.mail.received.group`, etc.)

#### `send_email`

```json
{
  "action": "send_email",
  "from_address_id": "0",
  "send_as": "",
  "to": "{{sender_address}}",
  "cc": "",
  "bcc": "",
  "subject": "Re: {{ticket_subject}}",
  "headers": "Auto-Submitted: auto-replied",
  "format": "",
  "content": "Thank you for your message.",
  "run_in_simulator": "0"
}
```

#### `send_email_recipients`

```json
{
  "action": "send_email_recipients",
  "headers": "",
  "format": "",
  "content": "An update has been added to your ticket.",
  "html_template_id": "0",
  "bundle_ids": [],
  "is_autoreply": "0",
  "attachment_vars": []
}
```

#### `relay_email`

```json
{
  "action": "relay_email",
  "to": "",
  "to_owner": "1",
  "to_watchers": "1",
  "subject": "FW: {{ticket_subject}}",
  "content": "{{ticket_latest_message_content}}",
  "include_attachments": "0"
}
```

#### `add_recipients` / `remove_recipients`

```json
{ "action": "add_recipients", "recipients": "{{sender_address}}" }
{ "action": "remove_recipients", "recipients": "{{sender_address}}" }
```

#### `schedule_email_recipients`

```json
{
  "action": "schedule_email_recipients",
  "content": "We are reviewing your request.",
  "delivery_date": "+1 hour"
}
```

#### `move_to`

```json
{ "action": "move_to", "group_id": "0", "bucket_id": "0" }
```

### Ajax/API/data-source actions

#### `set_http_status` / `set_http_header` / `set_http_body`

```json
{ "action": "set_http_status", "value": "200 OK" }
{ "action": "set_http_header", "name": "Content-Type", "value": "application/json" }
{ "action": "set_http_body", "value": "{\"status\":\"ok\"}" }
```

### Chat/interaction actions (`event.message.chat.worker`)

#### `send_message`

```json
{
  "action": "send_message",
  "message": "Hello, {{current_worker_first_name}}!",
  "format": "",
  "delay_ms": "500"
}
```

`"format"`: `""`, `"markdown"`, or `"html"`.

#### `prompt_buttons`

```json
{
  "action": "prompt_buttons",
  "options": "Yes\nNo\nCancel",
  "color_from": "#4d8cdd",
  "color_mid": "#2b6cad",
  "color_to": "#1a4f8a",
  "style": "",
  "var": "var_choice",
  "var_format": "",
  "var_validate": ""
}
```

#### `prompt_text`

```json
{
  "action": "prompt_text",
  "placeholder": "Type your message...",
  "default": "",
  "mode": "single",
  "var": "var_response",
  "var_format": "",
  "var_validate": ""
}
```

`"mode"`: `"single"` or `"multiple"`.

#### `prompt_date`

```json
{
  "action": "prompt_date",
  "placeholder": "Enter a date...",
  "default": "today",
  "mode": "single",
  "var": "var_date",
  "var_format": "",
  "var_validate": ""
}
```

#### `prompt_chooser`

```json
{
  "action": "prompt_chooser",
  "context": "worker",
  "query": "",
  "selection": "single",
  "autocomplete": "1",
  "var": "var_chosen"
}
```

#### `prompt_file`

```json
{ "action": "prompt_file", "var": "var_file", "var_format": "", "var_validate": "" }
```

#### `prompt_images`

```json
{
  "action": "prompt_images",
  "images": [],
  "labels": [],
  "var": "var_image_choice",
  "var_format": "",
  "var_validate": ""
}
```

#### `prompt_wait`

```json
{ "action": "prompt_wait" }
```

#### `window_close`

```json
{ "action": "window_close" }
```

### Interactions action (`event.interactions.get.worker`)

#### `return_interaction`

```json
{
  "action": "return_interaction",
  "behavior_id": "0",
  "name": "Search tickets",
  "interaction": "cerb.tickets.search",
  "interaction_params_json": "{}"
}
```

---

## Package Library Location

Packages: `features/cerberusweb.core/packages/library/`

Working examples (test suites):

| File | Owner | Coverage |
|---|---|---|
| `cerb_bot_test_suite.json` | App (Cerb) | All 42 events, all conditions, all actions |
| `cerb_bot_test_suite_group.json` | Group (prompted at import) | All 8 group events, contextual Support-group scenarios |
| `cerb_bot_test_suite_worker.json` | Worker (prompted, defaults to id:1) | 8 worker-specific events, UI/chat/macro scenarios |
