# peek_edit Form Patterns

## Smarty Gotchas

- **No inline array literals in `{foreach}`** — assign arrays from PHP; don't use `{foreach ['a'=>1] as $k => $v}`.
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

## Space-Delimited Value Lists (OAuth-Style)

For fields that store a set of string tokens (e.g., access scopes, feature flags), a space-delimited string is simple and interoperable:

```
parent child:specific other
```

- A short token (`parent`) grants broad access; a qualified token (`child:specific`) is more specific.
- Parse into a lookup: `array_flip(array_filter(explode(' ', $value)))`
- Save from a `name="field[]"` checkbox array: `implode(' ', DevblocksPlatform::sanitizeArray($_POST['field'] ?? [], 'string'))`
- Fully-qualified checkbox values (`value="child:specific"`) and parent-only values (`value="parent"`) work together naturally: when a parent is checked, its children are disabled and won't post, leaving only the parent token in the submitted array.
