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

Always use `let` (or `const`) — never `var`. Old code still uses `var` and is being updated incrementally, but all new code must use `let`/`const`.

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
