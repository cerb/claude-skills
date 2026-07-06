# peek_edit Form Patterns

## Converting a legacy peek to cerb-ui (the current recipe)

Wrap the form body in `cerb-ui-panel cerb-ui-panel--spaced` + `cerb-ui-form`; group related fields in
`cerb-ui-form--row` (side-by-side, auto-50/50). **Preserve every POST field name + the save endpoint** — grep the
handler (`api/uri/profiles/<x>.php` / `api/uri/internal/<x>.php` / the DAO's `savePeekJson`) for the
`importGPC($_POST[...])` names first. Control mapping:

| Legacy | Cerb UI |
|---|---|
| `<table>` / `<fieldset><legend>` | `cerb-ui-form--field` / panel `cerb-ui-header--title-sm` (or `--label`) |
| binary/enum radio set | `CerbUI.Switcher` — hidden input + `div.cerb-ui-switcher[data-cerb-input]` + `button[data-value]`; wire via a generic `.cerb-ui-switcher[data-cerb-input]` loop that writes the hidden input on `onSelect` |
| `chooser-abstract` record picker | `CerbUI.RecordChooser` — `<div class="cerb-ui-record-chooser">` (**no static `id`** — see the multi-instance rule below) + seed `<li data-context-id data-label [data-image]>`; JS `context:"{CerberusContexts::CONTEXT_*}"` (full constant resolves via `getByAlias`), `name:`=POST field, keep `query`, `create:'if-null'`/`true`. Link two choosers via the first's `onSelect`→`other.setQuery(...)` |
| boolean checkbox | `CerbUI.Toggle` (`label.cerb-ui-toggle`+slider) + a `for=` caption; reveal dependents in `onChange` |
| long `<select>` | `CerbUI.SelectMenu` (`filter:true`); native `<select name>` stays (carries the POST value) |
| avatar / image | `data-cerb-image-editor` + `CerbUI.ImageEditor` — **not** the deleted `ajax.chooserAvatar` (the "Saving the Avatar" section below is superseded) |
| date input | `input_date` + `cerbDateInputHelper()`, wrapped in a `cerb-u-flex` row so the calendar trigger button doesn't wrap |
| `aliases`-style line list | `CerbUI.TagInput` (posts `name[]`; change the handler to read `'array'` + `implode("\n", …)` before the CRLF persist) |
| inline delete `<fieldset>` | `internal/peek/delete_confirm.tpl` + `CerbUI.Form.ConfirmDelete($popup[0])` (or a custom `cerb-ui-panel--alert [data-cerb-delete-confirm]` when it carries extra content, e.g. group bucket-move) |
| save/delete buttons | `cerb-ui-button save` / `--subtle delete-prompt`; retarget JS off `.save` (drop the CSS-bleeding `.submit`) |
| priority/order number | `input[type=number]` `min`/`max` + a `sort-asc` label icon (per `automation_event_listener`) |
| custom fields/fieldsets | `internal/custom_fields/cerb_ui_form.tpl custom_fields=$custom_fields` + `peek_custom_fieldsets.tpl … cerb_ui=true` |
| owner picker | keep `menu_actor_owner.tpl` (multi-context; no RecordChooser equivalent) — place in a `--field` |
| embedded Ace editor | keep verbatim for now → swap per `PLAN-editors-cerb-ui.md` (KataEditor/SearchQuery/DataQuery) |

Exemplars to copy: `tickets/`, `tasks/rpc/`, `workers/`, `groups/peek_edit.tpl`.

- **No static DOM `id` in a peek/popup/bulk template (they render multiple times):** a peek, bulk-update popup,
  compose window, or reply form can be open **more than once at a time** (and multiple appear on one worklist/
  display page), so a hard-coded `id="orgChooser"` collides — `$('#orgChooser')`/`getElementById` hits the wrong
  instance. Two sanctioned fixes:
  - **Namespace the id with a per-instance suffix** — the dominant peek convention. `{$form_id = uniqid()}` at the
    top (or a value already unique to the instance: `{$popup_uniqid}`, `{$message->id}`, `{$workspace_tab->id}`),
    then `id="orgChooser_{$form_id}"` + `$popup.find('#orgChooser_{$form_id}')`. Use this when the file already has
    such a var (most peeks do).
  - **Target by scoped `class`/`data-*` instead of an id** — cleanest when there's no uniqid handy (e.g. `bulk.tpl`,
    which scopes everything through `$popup`/`$frm`): `<div class="cerb-ui-record-chooser" data-cerb-chooser="org_id">`
    + `$popup.find('[data-cerb-chooser="org_id"]')`. The chooser's POST name comes from the JS `name:` option, **not**
    the id, so this never touches the submitted data. For 1-per-page config sections either is fine, but never a bare
    static id. Fixed across all 10 `*/bulk.tpl` + the compose/relay/workspace-tab/-widget peeks (2026-07-03).
  - **Also mind form ids** (`id="formBatchUpdate"`, `genericAjaxPost('formBatchUpdate',…)`): the framework's bulk
    convention still uses one, but scope every lookup through the captured `$popup`/`$frm`, never a fresh `$('#…')`.
- **The create-guard rule (cost real time):** a `{$x = $model->getY()}` that the *original* guarded with
  `{if $model}` MUST keep the guard — the **create** flow passes a null `$model`, so an unguarded `$model->getY()`
  500s on create (not edit). If the original was unguarded, that record's create passes a non-null empty model;
  match the original. Bit reminder/calendar_event/calendar_recurring_profile/custom_fields.
- **SelectMenu empty-option gotcha:** an `<option value="">` (blank label) renders as a phantom **divider** in
  `CerbUI.SelectMenu` (blank-`<li>`-as-separator). Give placeholder options a label: `(none)`/`(choose…)`.
- **SelectMenu icons per option:** add `data-cerb-ui-icon="<name>"` to each `<option>` — SelectMenu renders
  `<span class="cerb-icons cerb-icon-<name> cerb-ui-selectmenu--icon">` before the label on **both** the trigger and
  every menu item (no `onRender` needed). For widget-type pickers the foreach items are `DevblocksExtensionManifest`,
  so use `{$ext->params['icon']|default:'dashboard'}` (NOT `getIcon()`, which is the instance method). Exemplars: the
  three widget `peek_edit.tpl` (`internal/profiles/widgets`, `records/types/card_widget`, `internal/workspaces/widgets`).
- **SelectMenu `destroy()` un-hides the native select:** SelectMenu hides the `<select>` via the
  `.cerb-ui-selectmenu--source` class; `destroy()` REMOVES that class. So after a dynamic repopulate, never
  `$select.fadeIn()` (it reveals the raw select on top of the trigger) — fade the field **wrapper** instead, and hide
  the wrapper during the async reload to avoid a flash of the bare select. SelectMenu re-dispatches the native
  `change` event, so existing `$select.on('change')` handlers keep working unchanged.
- **SelectMenu over an AJAX-repopulated select:** build a `selectMenu` closure var + a `buildExtensionSelectMenu()`
  helper that does `if(selectMenu){selectMenu.destroy();selectMenu=null;}` then recreates (SelectMenu reads options
  only at construction). Call it once on open (server-rendered case) and again in the AJAX callback after appending
  `<option>`s. Have the JSON endpoint return the icon too — e.g. profile widgets'
  `_profileAction_getExtensionsByTabContextJson` now returns `id => {name, icon}` (was flat `id => name`).
- **Included partials may depend on a `<fieldset>` ancestor.** Some shared includes do `$x.closest('fieldset')`
  in their own JS (e.g. `automation_event/listeners.tpl`, mail_incoming `rules.tpl`) — wrapping them in a
  `cerb-ui-panel` `<div>` silently breaks that lookup (no error, just dead refresh/binding). Either keep a
  `<fieldset>` wrapper, or change the partial to `closest('[data-…]')` on an attribute the new wrapper carries.
- **Verify every peek in-container** — see the compile-check workflow in `references/smarty-conventions.md`.
- **Scalable membership/role matrix** (worker↔groups, group↔workers): don't render N `CerbUI.Switcher` instances.
  One delegated click handler over a filterable roster + sticky icon-only "set all" + **delta posting** (each row's
  hidden input starts `disabled`, enabled only when its value ≠ `data-orig`, so only changed rows POST — safe
  because `updateGroupMemberships` ignores unposted keys). Dim neither-rows `cerb-u-opacity-25`. Exemplars:
  `workers/peek_edit.tpl` (Groups tab) + `groups/peek_edit.tpl` (Members tab).

Full sweep status + the deferred per-record polish + the PASS-2 editor-heavy list live in
`PLAN-jquery-ui-to-cerb-ui.md` (repo root); `references/cerb-ui.md` is the component reference.

## Smarty Gotchas

- **No inline array literals in `{foreach}`** — assign arrays from PHP; don't use `{foreach ['a'=>1] as $k => $v}`.
- **Wrap JS/JSON blocks containing `{` in `{literal}…{/literal}`** — Smarty auto-treats a `{` followed by whitespace or a newline as plain text (so `function() {` at end of line, or `{ if(x) }` with a space, survive), but a `{` immediately followed by a non-space char (object literals `{key:1}`, empty `{}`, arrow bodies `=> {…}`) is parsed as a Smarty tag and breaks template compilation at runtime. This bites constantly in `<pre>` doc snippets and inline `<script>` object literals (e.g. the UI Reference gallery partials). Wrap such blocks in `{literal}…{/literal}`; this is also why an inline `<script>` of mostly end-of-line braces compiles fine but a single `new X({foo:1})` on one line does not. Note `{$var}`, `{DevblocksPlatform::...}`, and `{include}` are real tags and must stay OUTSIDE any `{literal}`.
- **`isset()` returns false for null values** — KATA parses `key:` (no children) as `['key' => null]`, so `{if isset($tree.key)}` is false. Pre-process in PHP into boolean-flag arrays instead.
- **No by-reference PHP function calls from Smarty** — functions like `kata()->parse()` take `&$error`; call in PHP and assign the result.
- **Bracket notation with special characters works** — `{if isset($map['a:b'])}` is valid; special characters inside string literals don't affect Smarty's parser.
- **Pre-compute everything in PHP** — derive all template state (lookups, flags, nested structures) in `renderPeekPopup`. Keep Smarty logic to simple `isset`/`{if}` checks.
- **`DevblocksPlatform::services()` is allowed in templates** — many existing templates call it directly.
- **Don't use `Context_*::ID` in templates** — Smarty 4 logs `"Using unregistered static method ... in a template is deprecated"` for any class not registered via `Smarty::registerClass`. Per-record context classes (`Context_QueueJob`, `Context_Ticket`, etc.) are not registered. Approved alternatives:
    - Use `CerberusContexts::CONTEXT_*` constants for core record types (`CerberusContexts` is pre-registered for static template access) — e.g., `{$peek_context = CerberusContexts::CONTEXT_QUEUE_JOB}`.
    - Hardcode the context ID string for non-core or new contexts — e.g., `data-context="cerb.contexts.queue.job"`.
  Reserve `Context_*::ID` for PHP files only.

## Checkbox Groups with Parent/Child Dependency

Use `data-cerb-scope-parent` / `data-cerb-scope-child` attributes to associate parents with children. In `popup_open`, run the same function for both initial state and `change` events:

```javascript
function applyParentState($parent) {
    let group = $parent.data('cerb-scope-parent');
    let $children = $popup.find('[data-cerb-scope-child="' + group + '"]');
    if($parent.prop('checked')) {
        $children.prop('checked', true).prop('disabled', true);
    } else {
        $children.prop('checked', false).prop('disabled', false);
    }
}

// Initialize server-rendered state, then bind
$popup.find('[data-cerb-scope-parent]').each(function() { applyParentState($(this)); });
$popup.find('[data-cerb-scope-parent]').on('change', function() { applyParentState($(this)); });
```

The `.each()` initialization pass is required — a `change` handler alone won't apply disabled state to inputs that are already checked when the popup opens.

**Disabled checkboxes aren't submitted** — jQuery's `serialize()` skips disabled inputs. This is useful: check+disable children when a "select all" parent is checked so only the parent value posts, implying all children are granted.

**Prevent text selection on checkbox tables:**
```javascript
$popup.find('.my-table').disableSelection(); // jQuery UI
```

## Building Dynamic Rows from Extension Points

Build the full nested data structure in PHP and pass one array to the template — don't iterate extension objects in Smarty:

```php
$extensions = DevblocksPlatform::getExtensions('some.extension.point', false);
DevblocksPlatform::sortObjects($extensions, 'name');

$available_items = [
    'group_key' => [
        'label' => 'Group label',
        'children' => array_column(
            array_map(
                fn($ext) => ['key' => 'group_key:' . $ext->id, 'value' => ['name' => $ext->id, 'label' => $ext->name]],
                $extensions
            ),
            'value', 'key'
        ),
    ],
];
$tpl->assign('available_items', $available_items);
```

The template loops `$available_items` generically with no hardcoded group names.

## Flat Lookup Sets for Pre-computing Checked State

When a field stores a list of values and the form needs to render which ones are checked, convert the stored value to a flat lookup set in PHP:

```php
// e.g. stored as space-delimited: "foo bar:baz"
$active = array_flip(array_filter(explode(' ', $model->field ?? '')));
$tpl->assign('active', $active);
```

Template checks become simple `isset` calls:
```smarty
{if isset($active['bar:baz'])}checked="checked"{/if}
```

## Radio-Toggled Fieldset Sections

For forms with mutually exclusive modes (e.g. "Create new" vs. "Import existing"), put a radio inside each `<fieldset>`'s `<legend>` and toggle the body visibility on change. Use `{$uid = uniqid()}` to avoid ID collisions when the form may appear multiple times on a page.

```smarty
{$uid = uniqid()}
<fieldset class="peek black">
    <legend><label><input type="radio" name="params[mode]" class="mode-radio-{$uid}" value="create" checked> Create new</label></legend>
    <div class="mode-body-{$uid}-create">
        ... fields for create ...
    </div>
</fieldset>

<fieldset class="peek black">
    <legend><label><input type="radio" name="params[mode]" class="mode-radio-{$uid}" value="import"> Import existing</label></legend>
    <div class="mode-body-{$uid}-import cerb-hidden">
        ... fields for import ...
    </div>
</fieldset>

<script nonce="{DevblocksPlatform::getRequestNonce()}" type="text/javascript">
$(function() {
    $('.mode-radio-{$uid}').on('change', function() {
        let is_import = ('import' === $(this).val());
        $('.mode-body-{$uid}-create').toggleClass('cerb-hidden', is_import);
        $('.mode-body-{$uid}-import').toggleClass('cerb-hidden', !is_import);
    });
});
</script>
```

- Use `.cerb-hidden` (not `style="display:none"`) for the initially hidden body — consistent with platform conventions and toggled cleanly with `.toggleClass('cerb-hidden', condition)`.
- Only show create/import fieldsets when `$record->id == 0` (new record); on edit, show only the current state.

## Saving the Avatar from peek_edit

> **Superseded for cerb-ui peeks:** `ajax.chooserAvatar` is deleted; use `data-cerb-image-editor` +
> `CerbUI.ImageEditor` (the avatar well + crop/zoom Dialog) — see the recipe table above. The **server save
> path is unchanged** (`DAO_ContextAvatar::upsertWithImage` reading the hidden `avatar_image` POST), so the PHP
> below still applies; only the template wiring + JS changed.

The (legacy) peek template wired the chooser button:

```smarty
<img class="cerb-avatar" src="{devblocks_url}c=avatars&context=my_record&context_id={$model->id}{/devblocks_url}?v={$model->updated_at}" style="height:50px;width:50px;">
<button type="button" class="cerb-avatar-chooser" data-context="{CerberusContexts::CONTEXT_MY_RECORD}" data-context-id="{$model->id}">{'common.edit'|devblocks_translate|capitalize}</button>
<input type="hidden" name="avatar_image">

{* in popup_open *}
ajax.chooserAvatar($popup.find('button.cerb-avatar-chooser'), $popup.find('img.cerb-avatar'));
```

…but **the template wiring alone doesn't persist anything** — the chooser only stuffs a data URL into the hidden `avatar_image` input. The profile action must read it and save:

```php
// In _profileAction_savePeekJson, after the record exists and params are set
$avatar_image = DevblocksPlatform::importGPC($_POST['avatar_image'] ?? null, 'string', '');
DAO_ContextAvatar::upsertWithImage(CerberusContexts::CONTEXT_MY_RECORD, $id, $avatar_image);
```

Empty string = no change; data URL = replace; sentinel = remove. Verify this call exists when adding a `<button class="cerb-avatar-chooser">` to a new peek — easy to forget and silently no-op.

## Space-Delimited Value Lists (OAuth-Style)

For fields that store a set of string tokens (e.g., access scopes, feature flags), a space-delimited string is simple and interoperable:

```
parent child:specific other
```

- A short token (`parent`) grants broad access; a qualified token (`child:specific`) is more specific.
- Parse into a lookup: `array_flip(array_filter(explode(' ', $value)))`
- Save from a `name="field[]"` checkbox array: `implode(' ', DevblocksPlatform::sanitizeArray($_POST['field'] ?? [], 'string'))`
- Fully-qualified checkbox values (`value="child:specific"`) and parent-only values (`value="parent"`) work together naturally: when a parent is checked, its children are disabled and won't post, leaving only the parent token in the submitted array.
