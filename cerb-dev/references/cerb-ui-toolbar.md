# CerbUI.Toolbar (toolbars)

The plain-JS `CerbUI.Toolbar` is the single toolbar implementation — it replaced the legacy jQuery
`$.fn.cerbToolbar()` plugin (deleted) and its `<button>`+`<ul class="cerb-float">` template. A toolbar is a
nested `<ul class="cerb-ui-toolbar">`; the component hides that source list and renders a visible
`.cerb-ui-toolbar--strip` after it. Menu items (a `<li>` with a child `<ul>`) open a `CerbUI.Menu`.

Component: `features/cerberusweb.core/resources/js/cerb-ui/toolbar.js` (bundled into `cerb-ui.js` via
`composer build-js`). Live examples: Setup → Developers → UI Reference → Toolbar.

## The render → enhance contract

1. PHP builds toolbar KATA into a parsed array: `DevblocksPlatform::services()->ui()->toolbar()->parse($kata, $dict, $error)`.
2. PHP emits markup: `->toolbar()->render($toolbar)` (echo) or `->fetch($toolbar, $opts)` (return). Both
   render `libs/devblocks/templates/ui/toolbar/render_cerbui.tpl` → a `<ul class="cerb-ui-toolbar">` placed
   inside whatever wrapper the template provides (e.g. `<div data-cerb-toolbar>…</div>`).
   - `$opts = ['class' => 'extra wrapper classes', 'attr' => 'raw wrapper attrs']`. (A legacy string 2nd arg
     — the old `$interaction_class` — is accepted but ignored; CerbUI finds interactions by attribute.)
   - There is no longer a `fetchCerbUi()`/`renderCerbUi()`; `fetch()`/`render()` ARE the CerbUI emitters.
   - `parse()` and `extractKeyboardShortcuts()` are unchanged.
3. Host JS grabs the `<ul>` and constructs the component:
   ```js
   let ul = $wrapper.find('ul.cerb-ui-toolbar')[0];
   if(ul && window.CerbUI && CerbUI.Toolbar)
       new CerbUI.Toolbar(ul, OPTS);
   ```

**Gotcha — enhance EVERY sub-toolbar, not `[0]`.** One container can host multiple `[data-cerb-toolbar]` sub-toolbars (the mail editors have a `formatting` AND a `custom` one). Construct over all of them — `$el.find('[data-cerb-toolbar] ul.cerb-ui-toolbar').each(function(){ new CerbUI.Toolbar(this, OPTS); })` — not `…[0]`, or the un-enhanced one renders as a raw bulleted `<ul>`. The bug hides when the first sub-toolbar is `display:none` (e.g. plaintext mode) and the second is the visible one.

**Gotcha — don't set `display` on the source `<ul>`.** The component hides the authored `<ul class="cerb-ui-toolbar">` via the `hidden` attribute and renders the visible `--strip` as its sibling. An inline `style="display:…"` (or a class that sets `display`) on that `<ul>` overrides `[hidden]{display:none}`, so the raw source list stays visible **beside** the strip → duplicated items. Style/position the visible `--strip` (or a wrapper `<div>` around the `<ul>`) instead — never the `<ul>` itself.

`OPTS` pass straight through to `$.fn.cerbBotTrigger` (the interaction startInteraction/await flow):
`caller: {name, params}` (cerbBotTrigger reads `caller.name`), `start(formData)`, `done(e)`, `error(e)`,
`reset(e)`, `target` (jQuery el → inline; null → popup), `width`. Plus toolbar-only: `bare` (`true` |
`'tiny'`), `onSelect(item, sourceLi, e)`, `hover`, `badgeStyle` (`'pill'` default = floating corner alert
pill; `'count'` = calm leading inline tally left of the label, echoing the old `DIV.badge-count`),
`overflow` (`'wrap'` default = flow to multiple rows; `'menu'` = collapse trailing items into a trailing
`…` more-vertical menu; `'none'` = clip).

### Overflow (`overflow:'menu'`)

A too-wide strip **wraps to rows by default** (`.cerb-ui-toolbar--strip` is `flex-wrap:wrap`; so is the
hybrid rail). `overflow:'menu'` instead keeps a single row: a `ResizeObserver` on the strip's container
runs `_reflow()`, which measures the container width and, for the trailing items that don't fit, **moves
their source `<li>` into a trailing `…` (more-vertical) `CerbUI.Menu`** (rebuilt each reflow since
`CerbUI.Menu` snapshots its source) — so `cerbBotTrigger` bindings, nested submenus, and `sourceLi` stay
real (no clone/key-mapping). **Toggles are pinned** (never collapse — their state lives on the strip
button). The container should be width-constrained (e.g. a sidebar), not `fit-content`, or there's nothing
to measure against. `overflow` is a component option; hand-coded `.cerb-ui-toolbar-rail` wrappers just wrap.

### `e.trigger` and the `cerb-bot-trigger` shim

In a `done`/`start`/`reset` callback, `e.trigger` is the element cerbBotTrigger was bound to — under
CerbUI that is the **source `<li>`** (not a rendered strip button). The `<li>` carries
`class="cerb-bot-trigger"` plus `data-interaction-uri` / `-params` / `-done`, so the common legacy gate
still works:
```js
done: function(e) {
    if(!e.trigger.is('.cerb-bot-trigger')) return;          // still true
    let done_params = new URLSearchParams(e.trigger.attr('data-interaction-done'));
    …
}
```
New code may prefer `e.trigger.is('[data-interaction-uri]')`.

**The component owns `cerbBotTrigger` for its source `<li>`s — don't double-bind.** `_bindInteractions`
already calls `jQuery(li).cerbBotTrigger(passthrough)` on every `li[data-interaction-uri]` in the source list
(with the toolbar's caller / `start` / `done`). `$.fn.cerbBotTrigger` is **not idempotent** — it just does
`$el.on('click', …)`, so a second call stacks a second handler and the interaction fires twice (two
`startInteraction` round-trips, `done` twice). A host that binds `cerbBotTrigger` *broadly* over a region that
contains a CerbUI.Toolbar (e.g. the sheet body partials' `$sheet.find('.cerb-bot-trigger')`) must therefore
exclude the component's source `<li>`s:
```js
$sheet.find('.cerb-bot-trigger, .cerb-interaction-trigger')
    .not('.cerb-ui-toolbar .cerb-bot-trigger, .cerb-ui-toolbar .cerb-interaction-trigger') // component owns these
    .cerbBotTrigger({ … });
```
`.cerb-ui-toolbar` is the hidden source list; the visible `--strip` buttons are `<button>` (not
`.cerb-bot-trigger`), so this only drops the component-owned source `<li>`s — row-level interaction/card cells
keep their host binding.

### Refresh-aware toolbars

Toolbars that re-fetch their own HTML (`$el.html(newHtml).trigger('cerb-toolbar--refreshed')`) — record
card/profile, sheet widgets, the automation editor — must **reconstruct** on that event, since the old
strip is wiped with the replaced `<ul>`:
```js
let buildToolbar = function() {
    let ul = $toolbar.find('ul.cerb-ui-toolbar')[0];
    if(!ul || !(window.CerbUI && CerbUI.Toolbar)) return;
    new CerbUI.Toolbar(ul, OPTS);
};
$toolbar.on('cerb-toolbar--refreshed', buildToolbar);
buildToolbar();
```

**Idempotent construction (no double strips).** `new CerbUI.Toolbar(ul)` is safe to call again on a
source `<ul>` that was already enhanced — the constructor tears down a prior instance for that `<ul>`
(removing its strip) before rendering, and `_render` also drops any stale `--strip` left immediately after
the `<ul>`. This is what keeps re-render paths that reconstruct on the *same* list (e.g. a sheet/widget
column toolbar redrawn after an interaction reports a status change) from stacking a second strip. Don't
rely on this to paper over a genuine double-enhance bug — but it makes reconstruction the safe default.

### Keyboard shortcuts

`render_cerbui.tpl` emits both `data-keyboard` (the component reads it for the tooltip hint) AND
**`data-interaction-keyboard` on the source `<li>`** — the dispatch hook. Host keydown dispatchers
(editor toolbars, sheet/widget toolbars) do `$scope.find('[data-interaction-keyboard="…"]').click()`; this
**must resolve to the server-rendered source `<li>`, NOT the JS-built strip button** — the `<li>` is present
immediately, so the lookup doesn't race the toolbar's enhancement. Clicking the (hidden) source `<li>` fires
the interaction via its bound `cerbBotTrigger`, exactly like a strip-button click. The component deliberately
does NOT copy the attribute onto the rendered button (that caused widget toolbars to silently lose shortcuts
when the keydown binding ran before/without enhancement). `extractKeyboardShortcuts()` (PHP) still feeds the
host's keydown bindings; `CerbUI.Toolbar.from(ul).triggerShortcut(keys)` clicks the source `<li>` for a shortcut.

## render_cerbui.tpl item attributes

Per parsed item the template emits (interaction/behavior `<li>` also get `class="cerb-bot-trigger"`):
`data-icon` (bare name → `cerb-icons cerb-icon-<name>`; leading `.` → raw class list), `data-icon-at`
(`end` = icon after label), `data-class` (extra class(es) copied onto the rendered button, e.g.
`action-always-show`), `title` (tooltip), `data-keyboard`, `data-badge` + `data-badge-color`,
`data-value`, `data-interaction-uri`/`-params`/`-done`. Behavior items (deprecated): `data-behavior-id` +
`data-interaction`. Menus nest a child `<ul>`; an empty `<li>` is a divider; `data-toggle`/`data-pressed`
makes a client-state toggle button (drive via `isPressed(key)`/`setPressed(key,on)`).

## Reusable styling hooks (`cerb-ui/_toolbar.scss`)

The strip/button/active visuals are mixins so hand-coded toolbars can match the dynamic strip:

- `@mixin cerb-ui-toolbar-strip` — the boxed inline-flex rail.
- `@mixin cerb-ui-toolbar-button` — one item (28px, radius, hover wash **+ hover color**, focus ring, icon sizing).
- `@mixin cerb-ui-toolbar-button-active` — pressed/"on" state (reuses `--cerb-color-button-icon-enabled*`).

The component's `--strip` / `--item` / `--item-active` `@include` them. Public classes for plain markup:
`.cerb-ui-toolbar-strip`, `.cerb-ui-toolbar-button`, `.cerb-ui-toolbar-button--active`, and
`.cerb-ui-toolbar-config-button` (a muted inline gear-style config button). `cerb-ui.scss` imports the
toolbar partial **before** `cerb-styles.scss`, so the mixins are usable in later partials.

**Styling a standalone action button as a strip item (no JS).** The public classes are pure CSS, so a lone
`<button>` (e.g. a form's *Save changes*) can borrow the strip look without a `CerbUI.Toolbar` instance — wrap
it in `.cerb-ui-toolbar-strip` and give the button `.cerb-ui-toolbar-button`. It reads as a flat item in a
light frame instead of the gradient `.cerb-ui-button`. **Gotcha inside a `.cerb-ui-form`:** the form is a
flex column with `align-items:stretch`, so a `.cerb-ui-toolbar-strip` (inline-flex) placed as a *direct* form
child stretches full-width (a wide empty frame). Nest it one level — `<div><div class="cerb-ui-toolbar-strip">
…</div></div>` — so the strip stays content-width. (Adopted by the worker-settings sub-tab save buttons.)

### Hybrid toolbar recipe (built-in + dynamic, seamless)

When hand-coded `<button>`s sit beside an injected CerbUI strip (record profile/card top toolbar, the
message action bar), fuse them into one rail with **`@mixin cerb-ui-toolbar-hybrid`** (or the one-class
**`.cerb-ui-toolbar-rail`**). It makes the wrapper the strip frame, styles plain built-in `<button>`s as
items, **collapses the inner `[data-cerb-toolbar]` wrapper with `display:contents`** so the dynamic
buttons line up as rail items, and flattens the injected `--strip`. Exclusions baked in: the setup gear
(`[data-cerb-toolbar-setup]`) and `.cerb-ui-button`s (so a `--split` primary action keeps its gradient).
```html
<div class="cerb-ui-toolbar-rail">
  <button …>Card</button>                         <!-- built-in → styled as an item -->
  <div data-cerb-toolbar>{…->render($tb)}</div>   <!-- dynamic → display:contents, flattened into the rail -->
  <button data-cerb-toolbar-setup class="cerb-ui-toolbar-config-button">…</button>
</div>
```
**Drop any inline `display` on the `[data-cerb-toolbar]` element** in the template — an inline
`display:inline-block` outranks the rail's `display:contents` and the dynamic buttons won't flatten in.
Used by `.cerb-profile-toolbar form.toolbar` (cerb-styles.scss), `card.tpl`, and `message.tpl`.

**Hover specificity gotcha (important).** The hover *color* must live in the `cerb-ui-toolbar-button` mixin
(`color: var(--cerb-color-button-icon--hover)`), NOT be left to the global
`button:has(> span.cerb-icons):hover` rule in `cerb-icons.scss` (specificity 0,2,2). A hybrid wrapper sets a
resting color at higher specificity (e.g. `.cerb-profile-toolbar form.toolbar button` = 0,3,1) which
outranks that global hover → the icon/text never changes on hover. Keeping the color in the mixin makes it
ride at the button's own `:hover` specificity so it wins everywhere. (Label-only buttons — no
`span.cerb-icons` — also depend on this, since the global rule wouldn't match them at all.)

### Inline config-gear pattern

The superuser gear that opens a toolbar's own setup/KATA is a real button, not a hand-styled `<a>`:
```html
<button type="button" data-cerb-toolbar-setup class="cerb-ui-toolbar-config-button"
        title="{'common.configure'|devblocks_translate|capitalize}"
        data-context="{CerberusContexts::CONTEXT_TOOLBAR}" data-context-id="record.profile" data-edit="true">
    <span class="cerb-icons cerb-icon-gear"></span>
</button>
```
```js
$widget.find('[data-cerb-toolbar-setup]').cerbPeekTrigger().on('cerb-peek-saved', /* re-render toolbar */);
```
It opens a peek (config editor), so `cerbPeekTrigger` is correct — it is NOT a worker interaction and does
not go through the toolbar KATA.

### Non-interaction items (search buttons) pattern

Items that do something other than fire an interaction (e.g. the fields-widget search buttons) live in a
CerbUI toolbar but are fired from `onSelect`. Counts use `data-badge` (component-rendered pill):
```html
<ul class="cerb-ui-toolbar" data-cerb-search-buttons>
    <li class="cerb-search-trigger" data-context="ticket" data-query="status:o" data-badge="{$count}">Open</li>
</ul>
```
```js
$properties.find('.cerb-search-trigger').cerbSearchTrigger();   // still binds the source <li>s
new CerbUI.Toolbar(ul, { onSelect: (item, sourceLi) => { if(sourceLi) $(sourceLi).trigger('click'); } });
```
`onSelect` fires for every leaf; the component only auto-clicks the source `<li>` when it has
`data-interaction-uri`/`data-behavior-id`, so non-interaction rows need the explicit `trigger('click')`.

### Editor-family bridge

Toolbars hosted in `.cerb-code-editor-toolbar` (mail compose/reply, comments, KATA/code editors) get a
scoped flatten so the strip doesn't double-frame inside the editor chrome:
```scss
.cerb-code-editor-toolbar .cerb-ui-toolbar--strip { background: transparent; border: 0; border-radius: 0; padding: 0; }
```

**Built-in editor toolbar (`editorCore.attachToolbar`) — the mail reply/compose recipe.** The editor OWNS its
strip: pass `toolbar:{ onMode, sections, onAction, toolbarOpts }` (no hand-authored `.cerb-code-editor-toolbar`).
The native **format menu + markdown↔plaintext switcher come free**; `onMode(v)` maps the mode to host state (the
`format` field + show/hide the HTML-template field). Host buttons ride as **`sections`** = hidden
`<ul class="cerb-ui-toolbar">` (+ the worker-configured `$toolbar_custom` ul); `onAction(value, ed, item,
sourceLi, e)` handles them by `data-value` (return truthy = handled). **Stateful buttons (GPG encrypt/sign)** are
`<li data-value data-toggle data-key data-pressed>` items — `onAction` reads the NEW state from `item.pressed`
and writes the hidden field; encrypt auto-enables sign via `ed._editorToolbar.toolbar.setPressed('gpg_sign',
true)` / `isPressed(...)`. `toolbarOpts.{caller,start,done}` carry the `cerb-bot-trigger` interaction wiring for
the custom section. Live in `display/rpc/reply.tpl` + `mail/section/compose/peek.tpl`.

## Key files

- `features/cerberusweb.core/resources/js/cerb-ui/toolbar.js` — the component.
- `libs/devblocks/templates/ui/toolbar/render_cerbui.tpl` — server markup.
- `libs/devblocks/api/services/ui.php` — `DevblocksUiToolbar` (`parse`/`fetch`/`render`/`extractKeyboardShortcuts`).
- `install/extras/developers/css/cerb.css/layout/cerb-ui/_toolbar.scss` — mixins, public classes, editor bridge.
- KATA autocomplete + validation for toolbar KATA: see `kata-autocomplete.md` (`kataToolbar` map in `cerberus.js`).

See also `cerb-ui.md` (design system + component inventory) and `scss-build.md` (`composer build-css`).
