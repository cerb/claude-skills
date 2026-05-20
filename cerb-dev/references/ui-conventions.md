# UI Conventions

## AJAX Functions

Always use the platform helpers — never write raw `$.ajax()` or `fetch()` calls:

| Need | Function |
|------|----------|
| GET request, update a div by ID | `genericAjaxGet(divId, url, callback)` |
| POST a form | `genericAjaxPost($form, divId, url, callback)` |
| Open a popup dialog | `genericAjaxPopup(popupId, url, $parent, modal, width)` |
| Find the popup containing an element | `genericAjaxPopupFind($element)` |

```javascript
// GET — load result into a div
genericAjaxGet('view123', 'c=internal&a=invoke&module=worklists&action=refresh&id=123');

// POST — submit a form
genericAjaxPost($frm, '', null, function(json) { ... });

// Popup — open and listen for close (GET, informational only)
let $popup = genericAjaxPopup('my_popup', 'c=profiles&a=invokeTab&...', null, false, '50%');
$popup.one('popup_close', function() { /* reload or refresh */ });

// Inside a popup template — find its container and close it
let $popup = genericAjaxPopupFind($frm);
$popup.one('popup_open', function() {
    $(this).dialog('option', 'title', 'My Title');
    $frm.find('button.submit').on('click', function() { $popup.dialog('close'); });
});
```

### Popups that modify data MUST use POST (FormData)

Pass a `FormData` object instead of a URL string to `genericAjaxPopup()`. This forces the request to POST, which is required for any action that creates, updates, or deletes data — and ensures CSRF protection applies.

```javascript
let formData = new FormData();
formData.set('c', 'profiles');
formData.set('a', 'invokeTab');
formData.set('tab_id', tab_id);
formData.set('action', 'myAction');
formData.set('worker_id', worker_id);

let $popup = genericAjaxPopup('my_popup', formData, null, false, '50%');
$popup.one('popup_close', function() { /* reload or refresh */ });
```

**Rule:** if the popup renders a form that writes data (regenerate codes, delete record, save settings, etc.), the popup request itself must be POST — not GET with a query string URL. A plain URL string always results in a GET request.

### Connected Service Provider AJAX Actions

Service providers can expose AJAX actions via `handleActionForService(string $action)`. Call them from a template using `genericAjaxPost` with a `FormData` targeting the service's `invoke` endpoint:

```javascript
let formData = new FormData();
formData.set('c', 'profiles');
formData.set('a', 'invoke');
formData.set('module', 'connected_service');
formData.set('action', 'invoke');
formData.set('service_action', 'myAction');   // dispatched to handleActionForService()
formData.set('id', '{$service->extension_id}'); // extension ID, not record ID

genericAjaxPost(formData, '', '', function(json) { ... });
```

In the provider PHP class:
```php
function handleActionForService(string $action) {
    switch($action) {
        case 'myAction':
            return $this->_connectedServiceAction_myAction();
    }
    return false; // 404 if unhandled
}

private function _connectedServiceAction_myAction() {
    if('POST' != DevblocksPlatform::getHttpMethod())
        DevblocksPlatform::dieWithHttpError(null, 405);

    DevblocksPlatform::services()->http()->setHeader('Content-Type', 'application/json; charset=utf-8');
    // ... do work ...
    echo json_encode(['result' => 'value']);
}
```

The action can receive additional POST fields (e.g. an account ID) by adding more `formData.set()` calls and reading them with `DevblocksPlatform::importGPC($_POST['field'] ?? null, ...)`.

## Notification Boxes

Use these CSS classes for inline messages — never plain `<p>` or custom styles:

- `.error-box` — warnings, errors, destructive-action notices (red/highlighted)
- `.help-box` — tips, informational notes (neutral/subdued)

```html
<div class="error-box">These codes will not be shown again.</div>
<div class="help-box">Each code can be used once as a login fallback.</div>
```

## Inline Toolbars

For rows of action buttons (download, print, copy, etc.), use `div.cerb-code-editor-toolbar` with `button.cerb-code-editor-toolbar-button`:

```html
<div class="cerb-code-editor-toolbar">
    <button type="button" class="cerb-code-editor-toolbar-button" title="Download"><span class="glyphicons glyphicons-download"></span></button>
    <button type="button" class="cerb-code-editor-toolbar-button" title="Print"><span class="glyphicons glyphicons-print"></span></button>
</div>
```

## Worklist Toolbar Button Order

In worklist view templates (`templates/records/types/{type}/view.tpl` and equivalents), the toolbar buttons below the worklist follow a fixed convention:

1. Custom toolbar items from `{$view->getToolbar()}` (via `view_toolbar.tpl`)
2. **Explore** (`action-explore`)
3. **Bulk update** (`action-bulkupdate` with `data-cerb-worklist-action-bulk="<module>"`)

```smarty
{$view_toolbar = $view->getToolbar()}
{include file="devblocks:cerberusweb.core::internal/views/view_toolbar.tpl" view_toolbar=$view_toolbar}
{if !$view_toolbar['explore']}<button type="button" class="action-always-show action-explore"><span class="glyphicons glyphicons-compass"></span> {'common.explore'|devblocks_translate|lower}</button>{/if}
{if $active_worker->hasPriv("contexts.{$view_context}.update.bulk")}<button data-cerb-worklist-action-bulk="<module>" type="button" class="action-always-show action-bulkupdate"><span class="glyphicons glyphicons-folder-closed"></span> {'common.bulk_update'|devblocks_translate|lower}</button>{/if}
```

Explore is the more common action and comes first; bulk update is more destructive/scoped and sits at the end. Mirror the existing ordering in `tickets/view.tpl`, `tasks/view.tpl`, `contacts/addresses/view.tpl`, `mail/queue/view.tpl`, etc. Don't place the bulk button before explore.

## Silent Actions — Feedback Notifications

When an action has no visible result (copy to clipboard, silent save, etc.), always show a brief notification so the user knows it worked. Use `Devblocks.createAlert()`:

```javascript
navigator.clipboard.writeText(text);
Devblocks.createAlert('Copied to clipboard!', 'note');
```

| Type | Use |
|------|-----|
| `'note'` | Success / confirmation (green) |
| `'error'` | Failure / warning (red) |

Never leave silent actions without feedback — users will click again thinking it didn't work.

## Hiding Elements

Use the `.cerb-hidden` CSS class to hide elements rather than `display:none` inline styles or the `disabled` attribute. Toggle visibility with jQuery's `.toggleClass()`:

```html
<!-- Hidden by default, revealed by JS -->
<button type="button" class="submit cerb-hidden">Done</button>
```

```javascript
// Show/hide based on a condition
$btn.toggleClass('cerb-hidden', !someCondition);
```

Prefer `.cerb-hidden` over `disabled` when the intent is progressive disclosure (e.g., a confirm button that appears only after an acknowledgment checkbox is checked) — hiding is friendlier than a greyed-out button that users try to click.

## Variable Declarations

Always use `let` (or `const`) — never `var`. Default to `const`; only switch to `let` when the binding is actually reassigned. Old code still uses `var` and is being updated incrementally — write new/edited code with `const`/`let` even when surrounding legacy code in the same file uses `var`. Don't introduce `var` to "match the style" — the legacy usages are paying down on their own schedule.

## No Unregistered Static Method Calls in Smarty Templates

Don't call static methods on classes that aren't registered with Smarty (e.g., `Extension_AutomationTrigger::get(...)`, `DAO_Foo::getById(...)`) directly inside `.tpl` files. Cerb logs a `[16384]` deprecation: *"Using unregistered static method ... in a template is deprecated and will be removed in a future release. Use Smarty::registerClass to explicitly register a class for access."*

Smarty is tightening its security defaults; unregistered static access is on the path to removal. Registering every class on every template touchpoint is noisy — pre-resolving in PHP is the consistent fix.

**Bad:**
```smarty
{$trigger = Extension_AutomationTrigger::get($trigger_id)}
{$trigger->name}
```

**Good:** resolve in PHP and `$tpl->assign()` the result.
```php
// In the controller / extension renderConfig / page section
$trigger = Extension_AutomationTrigger::get($trigger_id);
$tpl->assign('trigger', $trigger);
```
```smarty
{$trigger->name}
```

**Tolerated patterns** (not deprecated):

- Instance-chain method calls: `DevblocksPlatform::services()->...`
- Class constant reads: `CerberusContexts::CONTEXT_X`

The trigger is specifically *unregistered static method calls*. If you encounter this warning in another template you touch, hoist that specific call into PHP rather than calling `Smarty::registerClass()`.

## Peek Triggers Require Explicit Binding

Anchors with `class="cerb-peek-trigger"` open a record's peek popup when clicked. The binding is **not delegated** — each template that emits this markup must wire the click handler explicitly:

```js
$container.find('.cerb-peek-trigger').cerbPeekTrigger();
```

Required attributes on the anchor:
```html
<a class="cerb-peek-trigger"
   data-context="cerberusweb.contexts.attachment"
   data-context-id="{$attachment->id}"
   data-profile-url="{devblocks_url}c=files&id={$attachment->id}{/devblocks_url}">
   <b>{$attachment->name|escape}</b>
</a>
```

`data-context` and `data-context-id` are required. `data-profile-url` is optional (used for shift/cmd-click to open the profile in a new tab). `data-edit="1"` opens the peek directly in edit mode. Other supported attributes: `data-layer`, `data-width`.

Templates that include sub-templates which emit peek-triggers still need to do their own binding — the include doesn't magically wire its children. Card widget templates, marquee outputs, and sheet renders all follow this rule. View `border.tpl`, `sheets/render.tpl`, `peek_edit.tpl` for canonical examples.

## Reusable Attachment List

For "show attachments linked to this record" UIs, include `internal/attachments/list.tpl` rather than rolling your own list:

```smarty
{include file="devblocks:cerberusweb.core::internal/attachments/list.tpl"
    context="{CerberusContexts::CONTEXT_MY_RECORD}"
    context_id=$model->id
    attachments=$attachments}
```

If `$attachments` is omitted, the template runs `DAO_Attachment::getByContextIds($context, $context_id)` itself. Pass it explicitly when you've already loaded them.

Renders as a `bubbles`-styled list: paperclip glyph, name + size + mime type, peek-trigger anchor, kebab menu with **Download** and **Open in browser** actions. The template self-binds its own peek-trigger and menu handlers — you don't need to add anything.

Used by `internal/comments/comment.tpl`, `display/modules/conversation/draft.tpl`, `display/modules/conversation/message.tpl` for canonical examples.

## Confirmation Dialogs

**Never use the browser-native `confirm()`.** Always use `confirmPopup()` from `libs/devblocks/resources/js/devblocks.js`:

```javascript
confirmPopup(
    'Title',          // dialog title (default: 'Confirm')
    'Are you sure?',  // message body
    function() {      // OK callback
        // proceed
    },
    function() {      // optional Cancel callback
    }
);
```

`confirm()` blocks the browser's main thread, is unstyled, and cannot be used inside iframes on some browsers. `confirmPopup()` is the platform-standard modal.
