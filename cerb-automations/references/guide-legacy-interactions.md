# Guide: Legacy behavior worker interactions (form + chat)

This covers the **legacy** bot/decision-tree interactions provided by the `cerb.behaviors.legacy`
plugin — distinct from modern KATA automations (`interaction.worker`). Modern automations are
preferred for new work, but legacy behaviors are still fully supported and are what you author when
a request says "legacy behavior". All packages here require `"plugins": ["cerb.behaviors.legacy"]`.

There are two worker interaction styles, each a different event with a different prompt vocabulary:

| Style | Event | Prompt model |
|-|-|-|
| **Form** | `event.form.interaction.worker` | All prompts render on one form; only `prompt_submit` suspends |
| **Chat** | `event.message.chat.worker` | Each prompt suspends immediately (one step per message) |

Plus two plumbing events used to launch chat interactions:

| Event | Role |
|-|-|
| `event.interactions.get.worker` (`@deprecated`) | Registrar — lists interactions for a "point" (e.g. the global menu) |
| `event.interaction.chat.worker` | Opener — launched by the menu; hands off to a message behavior |

---

## Form interaction prompt actions (`event.form.interaction.worker`)

Each entry below is one item in an action node's `params.actions[]` array as `{"action": "<token>", …}`.
Prompts accumulate into a single form; `prompt_submit` renders it and suspends. After the worker
submits, the answer vars are populated and execution continues past the submit node.

| Action token | Demonstrates | Key params |
|-|-|-|
| `prompt_text` | Text input (`mode: multiple` = textarea) | `label`, `placeholder`, `default`, `mode`, `var`, `var_format`, `var_validate` |
| `prompt_radios` | Single choice | `label`, `style` (`radios`\|`buttons`), `orientation` (`horizontal`\|`vertical`), `options` (newline list), `default`, `var`, `var_format`, `var_validate` |
| `prompt_checkboxes` | Multiple choices | `label`, `options` (newline list), `default`, `var`, `var_validate` |
| `prompt_chooser` | Record chooser | `label`, `record_type` (context), `record_query`, `record_query_required`, `selection` (`single`\|`multiple`), `autocomplete` (`0`\|`1`), `default`, `var`, `var_validate` |
| `prompt_files` | File upload | `label`, `selection`, `var`, `var_validate` |
| `prompt_sheet` | Tabular sheet input | `label`, `data` (JSON rows), `schema` (sheet KATA), `var`, `var_format`, `var_validate` |
| `prompt_captcha` | CAPTCHA challenge | `var` |
| `prompt_compose` | Email compose popup | `draft_id`, `var` |
| `prompt_reply` | Email reply popup | `draft_id`, `var` |
| `prompt_submit` | Submit/reset buttons — **suspends** | *(none)* |
| `respond_text` | Display formatted output | `message`, `format` (`markdown`\|`html`\|omit) |
| `respond_sheet` | Display a sheet | `data_query`, `sheet_kata`, `placeholder_simulator_kata` |
| `interaction_end` | Terminate the interaction | *(none)* |

Source: `plugins/cerb.behaviors.legacy/src/events/form_interaction/form_interaction_worker.php`
(`getActionExtensions()` / `runActionExtension()`).

**`prompt_sheet` schema shape.** `layout:` and `columns:` are **siblings at the top level** (not
`columns:` nested under `layout:`), and to capture the worker's pick the sheet needs a `selection/`
column keyed on a field present in `data` (e.g. `selection/id` with `params.mode: single`). `data` is
a JSON array of row objects; each row must include that key.

```
layout:
  style: table
  headings@bool: yes
  filtering@bool: no
  paging@bool: no
columns:
  selection/id:
    params:
      mode: single
  text/name:
    label: Name
  text/qty:
    label: Qty
```

See `toolbars.md` and the Sheets docs for the full sheet schema (column types, layout options).

---

## Chat interaction prompt actions (`event.message.chat.worker`)

Each prompt sets `__exit = 'suspend'` on its own, so the natural structure is a **linear sequence of
action nodes** — one prompt per node. On the next message the tree replays to the suspended node
(without re-running it), saves the answer to the prompt's `var`, and continues to the next node.

| Action token | Demonstrates | Key params |
|-|-|-|
| `send_message` | Bot message (markdown, typing delay) | `message`, `format`, `delay_ms` |
| `prompt_text` | Text input | `placeholder`, `default`, `mode` (`single`\|`multiple`), `var`, `var_format`, `var_validate` |
| `prompt_date` | Date input | `placeholder`, `default`, `mode`, `var`, `var_format`, `var_validate` |
| `prompt_buttons` | Colored buttons | `options` (newline list), `color_from`/`color_mid`/`color_to`, `style`, `var`, `var_format`, `var_validate` |
| `prompt_chooser` | Record chooser | `context` (record type), `query`, `selection`, `autocomplete`, `var` |
| `prompt_file` | File upload | `var`, `var_format`, `var_validate` |
| `prompt_images` | Image picker | `images` (array of `data:` URIs), `labels` (array), `var`, `var_format`, `var_validate` |
| `prompt_wait` | Waiting indicator | *(none)* |
| `send_script` | Run JS in the browser | `script` |
| `switch_behavior` | Hand off / call another behavior | `behavior_id`, `var_*` (inputs), `return` (`0`\|`1`), `var` |
| `worklist_open` | Open a worklist popup | `context`, `quick_search` |
| `window_close` | Close the chat — **exits** | *(none)* |

Convention: chooser/file `var` names ending in `_id` (e.g. `var_record_id`) enable lazy record /
attachment expansion — `var_record_name`, `var_record_*` resolve after the answer is saved.

Source: `plugins/cerb.behaviors.legacy/src/events/interaction/new_message_chat_worker.php`.

---

## Packaging a legacy behavior

Legacy behaviors live under a **bot** in a package. Required keys are enforced by the importer
(`features/cerberusweb.core/api/packages.php`).

```jsonc
{
  "package": {
    "name": "…", "revision": 1,
    "requires": { "cerb_version": "11.0.0", "plugins": ["cerb.behaviors.legacy"] }
  },
  "bots": [{
    "uid": "bot_x",
    "name": "…",
    "owner": { "context": "cerberusweb.contexts.app", "id": 0 },   // app-owned = readable by all
    "is_disabled": false,
    "params": { "events": {"mode":"all","items":[]}, "actions": {"mode":"all","items":[]} },
    "behaviors": [{
      "uid": "behavior_x",
      "uri": "my_stable_uri",          // optional but recommended — lets toolbars reference it by URI
                                       // (alphanumeric + underscore only — NO dots)
      "title": "…",
      "is_disabled": false, "is_private": false, "priority": 50,
      "event": { "key": "event.form.interaction.worker", "label": "…",
                 "params": { } },      // event-specific params (e.g. listen_points for the registrar)
      "variables": {
        "var_text": {"key":"var_text","label":"Text","type":"S","is_private":"0","params":{"widget":"single"}}
      },
      "nodes": [ /* decision tree */ ]
    }]
  }]
}
```

**Node shape** (recursive — `recursiveImportDecisionNodes`):

```jsonc
{
  "type": "action",          // action | outcome | switch | loop | subroutine
  "title": "…",
  "status": "live",          // live | disabled | simulator
  "params": { "actions": [ {"action":"prompt_text", "label":"…", "var":"var_text"} ] },
  "nodes": [ /* children */ ]
}
```

- **action** node: `params.actions[]`, each `{"action":"<token>", …token params}`.
- **outcome** node: `params.groups[]`, each `{"any": 0|1, "conditions": [ {"condition":"<key>","oper":"…","value":"…"} ]}`.
  - For a behavior **variable** condition, `condition` = the var key; `oper` is `is` / `like` /
    `contains` / `regexp`, prefix `!` to negate (e.g. `!is`); `value: ""` tests blank.
- A **switch** runs only its first passing outcome child.

Because each prompt suspends and the tree replays past it, **linear action-node sequences usually need
no condition branches** — that's the simplest structure for both form and chat behaviors.

### Cross-referencing another record/behavior in the same package — use **triple braces**

To reference the generated ID of a sibling record/behavior, use `{{{uid.<uid>}}}` (TRIPLE brace):

```jsonc
{"action": "switch_behavior", "behavior_id": "{{{uid.behavior_chat_prompts}}}", "return": "0"}
```

The importer's `findTemplates` pass (`packages.php`) only builds strings whose `{{` is followed by
`#`, `%`, or `{` — so a plain `{{uid.x}}` is **not** resolved; it must be `{{{uid.x}}}`. All bot and
behavior uids are assigned before this pass, so references resolve regardless of order. (Node `params`
are otherwise stored verbatim.) `{{{uid.…}}}` works for any package record cross-reference, not just
behaviors.

---

## Binding interactions to the global menu

The global menu (`cerb.toolbar.global.menu`) is built from the `global.menu` Toolbar record **plus**
auto-injected legacy chat interactions. The two styles bind differently.

### Chat — a 3-behavior chain via the registrar

The menu launch path (`PageSection_ProfilesBot::startBotInteractionAsConvoBehavior`) enforces the
chain, so all three are required:

1. **Registrar** — `event.interactions.get.worker`, event param `listen_points: global`, with a
   `return_interaction` action pointing at the opener.
   ```jsonc
   "event": { "key": "event.interactions.get.worker", "params": { "listen_points": "global" } },
   // action:
   {"action":"return_interaction", "behavior_id":"{{{uid.behavior_chat_opener}}}",
    "name":"My Chat", "interaction":"my.chat.slug", "interaction_params_json":"{}"}
   ```
   `listen_points` accepts `global`, `mail.compose`, `mail.reply`, `record:<context>`, or `*`.
2. **Opener** — `event.interaction.chat.worker` (the menu launch *requires this event*); openers only
   have `switch_behavior`, so they just hand off:
   ```jsonc
   {"action":"switch_behavior", "behavior_id":"{{{uid.behavior_chat_message}}}", "return":"0", "var":"_behavior"}
   ```
3. **Message** — `event.message.chat.worker` (the switch target *must be this event*); holds the
   `prompt_*` actions.

Note: `getInteractionsForWorker` caches per point for 900s (`interactions_<point>`); saving a
registrar behavior clears the relevant cache key.

### Form — a toolbar section + a behavior URI

Form interactions are **not** auto-injected by the registrar. Bind them by adding an `interaction/`
toolbar entry that points at the behavior's URI. Clicking it posts to `startInteraction`, which
resolves the URI via `DAO_TriggerEvent::getByUri()` and routes to
`startBotInteractionAsFormBehavior()` (the form-rendering path).

1. Give the form behavior a stable `"uri"` (e.g. `showcase_form`). Behavior URIs are **alphanumeric +
   underscore only — no dots** (unlike automation names, which are dotted).
2. Add a top-level `toolbars[]` entry to the package:
   ```jsonc
   "toolbars": [{
     "toolbar": "global.menu",
     "kata": "interaction/showcaseForm:\n  label: Prompt Showcase (form)\n  icon: form\n  uri: cerb:behavior:showcase_form\n"
   }]
   ```

Package toolbar import is **non-destructive**: it creates a named `DAO_ToolbarSection` appended to the
existing toolbar (it does **not** overwrite the toolbar's KATA), and `DAO_Toolbar::getKata()` merges
all sections at render time. The target toolbar must already exist (`global.menu` is seeded by core).
The same pattern binds a form interaction to any toolbar (`record.card`, `record.profile`, a
`form_interaction` card/profile/workspace widget's `interactions_kata`, etc.) — see `toolbars.md`.
