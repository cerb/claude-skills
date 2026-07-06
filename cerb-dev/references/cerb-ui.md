# cerb-ui Design System

`cerb-ui-*` is a new, self-contained design-system namespace (CSS + plain-JS components) deliberately
kept separate from all legacy Cerb classes. The long-term goal is a consistent component library that
replaces jQuery UI. Built incrementally; Setup→Storage, Setup→Scheduler, and Setup→Plugins are the first adopters.

**Adopting a page onto cerb-ui:** build the new markup, and (when it's a redesign, not a 1:1 swap) leave the
old markup in place below it for visual comparison, then remove the old once approved. Page layout that needs
flexbox/grid lives in a small **page-local scoped `<style>`** with app-specific `.cerb-<page>-*` classes that
*compose* the cerb-ui components inside (there are no flex utilities in `cerb-u-*` yet) — e.g.
`.cerb-storage-*` and `.cerb-sched-*`. Real data is wired where available; not-yet-tracked metrics (e.g. the
scheduler charts) render from sample data via JS until the backend lands.

## Live reference: the gallery

**Don't hand-document component markup/APIs here — it drifts.** The gallery is the source of truth and is
always current:

- **In-app:** Setup → Developers → **UI Reference** (superuser only).
- **Templates — one partial per component:**
  `…/ui_reference/components/<slug>.tpl` — each holds that component's markup **and its own init `<script>`**.
  `…/ui_reference/index.tpl` is the slim orchestrator (page-local `<style>`, the left nav, the `{include}`s,
  and the shared bottom `<script>` = copy-button handler + the nav's scrollspy/sticky IIFE).
- **Page section:** `api/uri/config/ui_reference.php` (`PageSection_SetupDevelopersUiReference`).

**Gallery layout** (page-local `cerb-uiref-*` prefix, separate from the shipped `cerb-ui-*`): a
`cerb-ui-sidebar-layout` with a **persistent left nav** (`#uiref-nav` — a `CerbUI.Sidebar` of 8 functional
`--section` groups, items `<li data-target="<slug>" data-icon="…">`; smooth-scroll + scrollspy + filter +
collapse) beside a `cerb-uiref-content` column. The content holds the `{include …/components/<slug>.tpl}` lines
grouped under `cerb-uiref-grouplabel` headings. Each partial = a `cerb-uiref-component` with **bare** `id="<slug>"`
(no `uiref-c-` prefix; the nav scrolls to it) + a `--label` heading → one or more `cerb-uiref-example`
(a `cerb-uiref-demo` + its `cerb-uiref-code` block(s)), then a trailing `<script>` with that component's wiring.
**To add a component: create its partial, add an `{include}` in the right group, and a nav `<li>` — keep those
three in sync** (the nav item's `data-icon` should match the partial's `--label` icon).

**Snippet conventions**:
- Each `<pre data-cerb-uiref-source>` must be **self-contained and paste-ready** — the copy button copies one
  `<pre>` verbatim. Prefer the realistic variant over a stripped-down one.
- **One example = one demo + the code that reproduces it.** Split variants into separate examples (don't cram
  several into one demo with stacked code blocks). Exception: a demo that needs markup AND JS to work
  (Switcher/Legend/Distbar/Sparkchart/TimeRing/Toggle/Menu/Tabs) is one example with two code blocks (HTML, then JS).
- **The FIRST/top snippet is the copy target → 100% option coverage.** For a JS component it shows EVERY
  constructor option with a one-line `//` comment (what it is, units/format, default); options you'd usually
  leave at default (e.g. `tooltip`, `palette`) are still shown but **commented out at their default**. Later
  variant snippets show only the *changed* options (`[/* … */]` placeholders for the rest) — they're for
  understanding the delta, not for copying. ("Verbose over mysterious.")
- **Smarty `{literal}` gotcha:** the gallery is a Smarty template, so a literal `{` in a snippet is parsed as
  a tag *unless* followed by whitespace/newline (auto-literal spares `{ foo }` and `{`+newline). A tight
  `{x,y}` / `{color}` (e.g. in a JS object or comment) breaks compilation with "unknown tag" — wrap that
  `<pre>` body in `{literal}…{/literal}` (stripped at compile time, so the copied text stays clean). Cerb uses
  `{literal}`, never Twig's `{raw}`.
- **Special sections may break the demo/code convention** when a `<pre>` doesn't fit: **Utilities** is a 2-col
  grid where the class name itself is the clickable copy target (a self-`data-cerb-uiref-source` element +
  the shared copy handler); the **Icon** browser shows the whole icon set (filter + show-labels toggle +
  click-to-copy markup, no code block) — its list comes from `PageSection_SetupDevelopersReferenceIcons::getCerbIcons()`,
  assigned in `ui_reference.php` (never call statics from the template).

**When you add/change a component, update the gallery** — that keeps this reference accurate by construction.

## Component inventory

| Component | Classes | JS class | Notes |
|---|---|---|---|
| Page | `cerb-ui-page`, `--max-width` | — | full-width default; `--max-width` caps ~1100px |
| Header | `cerb-ui-header`, `--title` / `--title-sm` / `--label`, `--subtitle`, `--right`, `--summary`, `--tight`, `--center` | — | two-part flex (left grows / right). **`--right`** = flex toolbar for controls (has gap); **`--summary`** = muted right-aligned text. Need both (text + a control)? nest a `--summary` inside `--right`. `--tight` = in-panel margin + baseline align; `--center` = center-align a title with its controls (pair with `--tight`) |
| Button | `cerb-ui-button` | — | opt-in port of the legacy global `<button>` (gradient base + hover, `--cerb-color-button-*` tokens); supports a leading `cerb-icons` glyph. The bare `<button>` element stays globally styled until callers migrate |
| Panel | `cerb-ui-panel`, `--spaced`, `--accent` | — | bordered surface; **a card = `--spaced` + a `--title-sm` head**; `--accent` left border via `--cerb-ui-accent` CSS var (use a palette color) |
| Chip | `cerb-ui-chip`, `--head` / `--label` / `--value` | — | CSS-only segmented label/value cells |
| Tile | `cerb-ui-tile`, `--icon` / `--text` / `--kind` / `--name`, `--block` | — | a "fancy label": colored icon square + uppercase `--kind` eyebrow + bold `--name`. `inline-flex` by default (content-sized; stretches as a grid item or with `flex:1`); `--block` forces full width. Icon bg is consumer-set inline to a palette color (e.g. `var(--cerb-color-tag-green)`) |
| Pill | `cerb-ui-pill` | — | small rounded **pill** label (a status/value, e.g. "every 2 minutes"); filled by default (bg + border), `inline-flex`, supports a leading `cerb-icons` glyph. Bare marker = strip the fill with `cerb-u-bg-none` + `cerb-u-border-0` and set an accent color inline. Distinct from **Pip** (status dot) and **Chip** (segmented label/value cells) |
| Separator | `cerb-ui-separator`, `--dashed`, `--arrow-start-left/right`, `--arrow-end-left/right`, `--thick` | — | a horizontal rule you can write on (centered label flanked by lines); block-level. Solid by default, `--dashed` variant; **empty = a plain rule** (`:empty` collapses the gap). Arrowhead modifiers cap either line (combine freely: flow `start-right`+`end-right`, inward `start-right`+`end-left`, etc); compose with `--dashed`; `--thick` swaps the filled triangle heads for exaggerated open chevrons (icon-set style) |
| Pip | `cerb-ui-pip`, `--live` | — | small status dot; color = `currentColor` (set a palette color inline or via modifier; default gray). `--live` adds a pulsing "ping" ring. CSS-only |
| Kbd | `cerb-ui-kbd` | — | a keyboard **key cap** for shortcut hints (e.g. `<kbd class="cerb-ui-kbd">⌘</kbd>`); inline-flex, fixed-width font, subtle bottom-edge shadow for a "physical key" look — sit several in a row for a combo. CSS-only. Used by the command bar's trailing keys + active `CerbUI.Menu` rows |
| TimeRing | `cerb-ui-time-ring` (+ generated `--track`/`--prog`/`--text`/`--value`/`--key`) | `CerbUI.TimeRing` | SVG progress/countdown ring + center value/key; JS builds the SVG. **Dumb** — no internal timer; the page drives it via `setFraction(0..1)` / `setValue` / `setKey` / `setLabel`. Arc = `currentColor`. (Future: one shared orchestrator ticks registered rings.) |
| Tooltip | `cerb-ui-tooltip` (+ `--interactive`/`--arrow`) | `CerbUI.Tooltip` | floating `position:fixed` panel, two modes. **Point** (hover): `show(nodeOrHtml, clientX, clientY)` / `move(x,y)` / `hide()` — above the point, flips/clamps to viewport, `pointer-events:none` (chart hover details). **Anchored** (callout): `anchor(nodeOrHtml, targetEl, {my, at, interactive})` — pins to an element with an **SVG arrow that points at the target**, interactive by default (`--interactive` → inverse palette to grab attention + dismiss on click / outside-click). Position is jQuery-UI-style (`my` = point on the tooltip, `at` = point on the target; `"center bottom"`/`"left top"`/`"middle bottom"`, tokens in any order); **default `my:"center bottom"` / `at:"center top"`** sits it above the target pointing at the top-middle, then flips below + slides along the cross-axis (arrow tracks toward a corner) to stay in the viewport. Both auto-hide if the owner/target leaves the DOM. Now the basis for the automation callout (`Devblocks.tooltip`), replacing jQuery UI. Reuse one instance per trigger |
| Sparkchart | `cerb-ui-sparkchart` (+ generated `--plot`/`--bar`/`--line`/`--hover`/`--axis`; tooltip body `cerb-ui-sparkchart-tip--title`/`--row`/`--swatch`) | `CerbUI.Sparkchart` | compact **categorical** multi-series chart (bars 0-based + lines own min→max, independent units). Data `{categories, series:[{type:'bar'|'line',label,values,text}]}` — renders `text[]` verbatim (never formats), `values[]` for geometry. SVG; ResizeObserver. Options: `caption` (extents below the plot: `[start,end]`=ends, single string=centered, omit=none), `ticks` (default true; one tick per category → false = bare sparkline), `height`, `barWidth` (band fraction → compact vs roomy), `tooltip` (default true; one **shared** Tooltip across all charts), `palette`. Always **publishes** bubbling `cerb-ui-sparkchart:hover`/`:leave`/`:click` (`detail={index,category,point,series}`) — use `tooltip:false` to fully own it. Sparkchart is the compact worklist/panel sparkline; **the full axis-based chart family (Cartesian/Pie/Scatter/Gauge/Timeblocks + the chart-KATA engine) is its own doc → `references/cerb-ui-charts.md`** |
| Map | `cerb-ui-map` (+ `--plot`/`--region`/`--point`/`--toolbar`/`--tool`/`--legend`/`--legend-swatch`/`--coords`/`--label`) | `CerbUI.Map` | self-contained SVG region+point map (choropleth + POIs); **replaced d3.v5 + topojson.v3** (no geo lib). Client-side TopoJSON decode (`CerbUI.Map.decodeTopology`), **Mercator + AlbersUsa** projections (`CerbUI.Map.projection()` factory; AK/HI insets automatic; `naturalEarth`/unknown → mercator), evenodd path fill + antimeridian split, choropleth (HCL ramp) / color_key / color_map + legend, region property-join + `is`/`not` filters, pan/zoom, selection + label popup + `mapClicked` automation POST. Config = the parsed map KATA under `{map:{projection,regions,points}}`; geometry sources = a fetch-URL **or** a preloaded object. Builds its own chrome; plot bg = `var(--cerb-color-background)`. `from(el)`/`destroy()`. Patterns → "Interactive SVG viz" below; deep retrospective → `PLANS/DONE/PLAN-geojson-d3-to-cerb-ui.md` |
| QrCode | (no classes — renders an `<svg>` into the container) | `CerbUI.QrCode` | **clean-room** QR generator (ISO/IEC 18004 byte mode + Reed–Solomon over GF(256), 8 masks + penalty scoring, auto version) + SVG renderer — **replaced the `jquery.qrcode` plugin**. `new CerbUI.QrCode(el, {text, size=192, margin=4, correctLevel:'L'|'M'|'Q'|'H' (default 'H'), foreground='#000', background='#fff'})`; `setText(text)`; static `create(opts)` → detached `<svg>`; `from(el)`; pure-logic test seam `_encodeMatrix(text,level)` → `{size,modules}`. **Renders dark-on-white regardless of theme** (phone cameras need dark-on-light — do NOT tint with `currentColor`; the white bg rect + quiet-zone `margin` keep it scannable inside a dark card). Consumers = the two-factor TOTP setup screens (payload = an otpauth Key URI — see `references/login-flow.md`). No SCSS (SVG self-styles) |
| Switcher | `cerb-ui-switcher`, `--active` | `CerbUI.Switcher` | segmented control — a row of mutually-exclusive buttons (e.g. 24h/7d, objects/size); `onSelect(value,button,switcher)`; `getValue/setValue/destroy`; `storageKey`; `data-value` per button; opt-in (CSS works bare) |
| Toggle | `cerb-ui-toggle` (+ `--slider`) | `CerbUI.Toggle` | an **on/off switch** (styled checkbox): `<label class="cerb-ui-toggle"><input type=checkbox><span class="cerb-ui-toggle--slider"></span></label>`. CSS works bare; `CerbUI.Toggle(inputOrLabel, {onChange(checked,input), checked})` + `getValue/setValue/setDisabled`. (Lifted from the legacy `cerb-toggle-switch`) |
| Distbar | `cerb-ui-distbar` (segments = bare `> span` children) | `CerbUI.Distbar` | horizontal stacked bar; computes width %, colors segs by palette index (or a shared `scale`); `setKey/getKey/getLegend`; `legend:true` clones segs into a matching Legend |
| Legend | `cerb-ui-legend` (+ generated `--swatch`/`--value`/`--muted`) | `CerbUI.Legend` | color key; items are bare `<div>` children (`:scope > div`) carrying only data — JS builds the inner DOM; `setKey/getKey`; honors the same `scale` option |
| Menu | `cerb-ui-menu` (+ `--panel`/`--item`/`--item-has-sub`/`--item-active`/`--separator`/`--label`/`--filter`/`--virt`) | `CerbUI.Menu` | lightweight cascading menu — **replaces jQuery UI for large/deep trees**. `new CerbUI.Menu(ul, opts)` parses a `<ul>/<li>` tree once; opts `onSelect`/`onClose`/`onRenderItem`/`inline`/`filter`/`fixed`/`hoverTrigger`/`captureKeys`/`virtThreshold` (60). **Virtualizes** panels past the threshold (windowed DOM), lazy cascade rendering, type-to-filter with breadcrumb context, keyboard nav, viewport flip/clamp. **Every panel caps at `maxHeight` and scrolls** — non-virtualized ones too (a list of ~14–60 items used to grow unbounded). `open(anchor)/close()/isOpen()/destroy()`; `from(el)` |
| Sidebar | `cerb-ui-sidebar` (+ `--head`/`--body`/`--foot`/`--section`/`--label`/`--item`/`--item-label`/`--item-active`/`--icon`/`--badge`/`--right`/`--collapsed`/`--full-height`/`--palette`; layout `cerb-ui-sidebar-layout`) | `CerbUI.Sidebar` | collapsible nav rail **or** draggable palette. Enhances `--head`(fixed)/`--body`(scrolls)/`--foot`(fixed) slots; items = icon/pip + label + badge rows (`variant:'nav'`) **or** `cerb-ui-tile`s (`variant:'tile'`/`palette:true` → wires `CerbUI.Draggable` for drag-out). **Item label is `--item-label` (normal case); `--label` is the uppercase section header — don't conflate.** Opts `side`/`collapsed`/`fullHeight`/`storageKey`/`filter`/`onToggle`/`onSelect`/`onRenderItem`/`onFilterItem`/`contentTarget`/`draggable`/`palette`/`tooltips` (collapsed-only label tooltips via `CerbUI.Tooltip`, default on). Chevron toggle → icon strip; default item action routes `data-item-url` (ext new-tab / relative full-page) + `data-item-ajax` (tabs-style `genericAjaxGet` into `contentTarget`). `toggle/collapse/expand/setActive/setFilter/destroy`; `from(el)`; static `defaultSelect(li,sb)` |
| Draggable | `cerb-ui-draggable--item`/`--helper`/`--tilt`/`--reverting` (+ body `cerb-ui-draggable-dragging`/`-no`) | `CerbUI.Draggable` | drag a **clone** out (original stays) toward a Droppable — the palette→canvas half of DnD (vs `Sortable`, which reorders). `new CerbUI.Draggable(elOrContainer, {items, handle, helper:'clone', tilt, distance, data, onStart/onMove/onStop})`; tilted floating helper, hit-tests live droppables, Esc-cancel, revert-on-miss. `refresh()/destroy()`; `from(el)` |
| Droppable | `cerb-ui-droppable` (+ `--over`/`--reject`/`--overlay`/`--overlay-reject`) | `CerbUI.Droppable` | a drop zone for `CerbUI.Draggable` (static live-registry — any draggable finds it, no explicit wiring). `new CerbUI.Droppable(el, {accept, overlay, rejectOverlay, hoverClass, onOver/onReject/onOut/onDrop})`; `accept` = selector \| `(item,payload)=>bool` \| null; `onDrop` returns false to reject (helper reverts); opt-in accept (`--overlay`) + reject (`--overlay-reject`) highlights. `from(el)` |
| Spinner | `cerb-ui-spinner` | `CerbUI.Spinner` | pure-CSS animated SVG (no timer/state). `CerbUI.Spinner.create()` → a fresh `<svg>`; `new CerbUI.Spinner()` exposes `.el`; or author `<svg class="cerb-ui-spinner">` directly. **No `from()`.** Loaded globally via the header; used by Scheduler async charts + worklist sparkline loaders. Replaces legacy `svg.cerb-spinner` |
| Form | `cerb-ui-form` (+ `--section`/`--section-head`/`--section-body`, `--field`/`--label`/`--required`/`--hint`/`--help`/`--row`/`--control`/`--control-icon`) | — | low-markup form layer; **auto-styles `input`/`textarea`/`select` inside** a `.cerb-ui-form` (type-qualified, beats the global `cerb-base` rules). The form is a flex-column whose gap spaces its **direct** children — so for more than a few fields group them into **`--section`** panels (banded `--section-head` label + `--section-body` that re-establishes the field gap inside). `--field` = label-above + full-width control; `--row` lays fields side-by-side and **collapses to one column when narrow** (flex-wrap, no media query); equal width by default, but add `cerb-u-flex-{1..4}` on the fields for an explicit split (`flex-1`+`flex-2` = a third + two-thirds; the `--row > field` rule uses `:where()` so the utility wins); `--label`+`--required` (red `*`)/`--hint` (inline muted "optional"); `--help` (muted text below); `--control`+`--control-icon` = leading-icon input (mirrors the login `.cerb-login-input-wrap`). A small form can skip sections (the form's own gap spaces the fields directly). **Auto-styling is a *descendant* rule** (so a control nested in a `cerb-u-flex` wrapper is still styled) — which means a component that embeds its own input (RecordChooser/ContextChooser) inherits the form chrome + the blue focus outline inside a form; such components **opt out** via a `.cerb-ui-form input.<their-input-class> { border:0;padding:0;background:none;outline:none }` reset in `_form.scss` (same specificity, later source → wins). Live adopter: the scheduler peek popup `templates/configuration/section/scheduler/job_peek.tpl` (a single `--section` with `--row`s of `--field`s). CSS-only |
| Tabs | `cerb-ui-tabs` (+ `--tab`/`--tab-active`/`--panel`/`--panel-active`/`--panel-loading`/`--panel-error`) | `CerbUI.Tabs` | lightweight accessible (ARIA) tabs — **replaces jQuery UI**. `new CerbUI.Tabs(ul, opts)` enhances `<ul> > <li> > <a>`; static panels (`#` href) or **AJAX** (non-`#` href fetched on first activation via `genericAjaxGet`, cached, Spinner shown while loading); localStorage persistence (`remember`/`storagePrefix`); keyboard nav. Opts `active`/`variant`/`onTabSelected`/`onBeforeTabLoad`/`onAfterTabLoad`/`onTabLoadError`; `select(i)/refresh(i)/sync()/setVariant(name)/destroy()`; `from(el)`. **Visual variants (skins)** are modifier classes on the `<ul>` — `--folder` (default; flat folder tabs on a bottom bar, active "opens" into the panel), `--underline` (flat labels + accent underline), `--segmented` (toolbar-strip frame, active = filled foreground pill). Pick via the `variant:'folder'|'underline'|'segmented'` opt (default `folder`) OR author the class (an explicit opt wins; else an authored skin class is honored); `setVariant(name)` switches at runtime. Skins are per-instance, so **mix them for nested tab sets** (outer `--folder`, inner `--underline`). Active marker uses `--cerb-color-text` / `--cerb-color-text-inverse`, NOT `--cerb-color-action-primary` (the blue reads oddly in dark mode). Structural base resets the browser `<ul>` `padding-left`; skins own their padding |
| Dialog | `cerb-ui-dialog` (+ `--titlebar`/`--content`/`--loading`/`--scroll`/`--backdrop`/`--resize`/`--minimized`/…) | `CerbUI.Dialog` | draggable/resizable/minimizable floating dialog — **replaces jQuery-UI dialog**. `new CerbUI.Dialog(contentEl, opts)` wraps an element; opts `title`/`header` (`bar`/`floating`/`none`)/`modal`/`width`/`namespace` (siblings share position + auto-close each other — supersedes the old `layer`/`reuse`)/`position {x,y}`/`scrollBody`/`autoHeight`/`onOpen`/`onClose`/… `open()/close()/minimize()/restore()/setTitle()/reflow()/destroy()`. **Minimize:** a minimize button (next to close — on both `bar` and `floating` headers, default on except `header:'none'`; never on `modal`) docks the dialog into a single shared **top-right tray** button (a `cerb-icon-window-top` glyph + a count, titlebar-blue); clicking the tray opens a `CerbUI.Menu` of the minimized dialogs' titles (`opts.title`, else "Untitled"), and choosing one restores it to the default top-center position (`onMinimize(bool)` still fires). The menu's **"Restore all"** cascades — `restore(cascade)` takes an offset-step index (× `_CASCADE_STEP`, 28px) so multiple dialogs **fan out** down-right instead of stacking exactly; a single restore passes no arg (default position). **Placement:** centered horizontally, near the **top** (one-titlebar gap, like legacy `genericAjaxPopup`) — not vertically centered. **Width:** defaults to 75% of the viewport capped at 1100px (the `cerb-ui-page` max-width); a number is fixed px; an **`'<n>%'` string is relative** (optionally capped via **`widthCap`** px); **mobile (≤768px) is always 95%**, ignoring width directives. **Viewport reflow:** relative/default/mobile widths **re-resolve when the window resizes** (debounced to resize-*end*) — untouched dialogs also **re-center**, while dragged or explicitly-`position`ed ones just **clamp on-screen**, and a hand-resized width (e/w drag) is left alone. **`autoHeight:true`:** an n/s resize **refits height to content on release** (keeping the new width) — the legacy jQuery-UI `resizeStop` behavior; the `genericAjaxPopup` adapter enables it so migrated popups match. **Tall/growing dialogs:** the dialog grows vertically and **never repositions** (wide non-wrapping content scrolls horizontally inside the body, not out of the frame); being an out-of-flow absolute box, while open it bumps `body` min-height (+ a titlebar margin) so the **page** scrolls to its bottom, and a ResizeObserver re-syncs that as content grows in place (accordion/inline-search/async); `reflow()` is a manual page re-sync. Pass **`scrollBody:true`** (`--scroll`) to cap to the viewport (a titlebar margin top + bottom — the whole frame visible) and scroll the body internally instead. **`CerbUI.Dialog.from(el)`** resolves the dialog from its content element **or any descendant** (the `genericAjaxPopupFind` replacement). **`CerbUI.Dialog.fromAjax(request, opts)`** = the `genericAjaxPopup` replacement: builds the DOM, shows a `--loading` spinner, fetches via `genericAjaxGet` (string ⇒ GET args) / `genericAjaxPost` (FormData ⇒ POST) so response `<script>` runs under the nonce, closes on HTTP error (helper toasts it), and self-destroys on close (`opts` += `onLoad(content, html)`). **`CerbUI.Dialog.Loading.show(msg)` / `.hide()`** = the `showLoadingPanel`/`hideLoadingPanel` replacement: a **singleton**, chrome-less (`header:'none'`, no close/drag/resize, Esc-locked) **modal** overlay with a spinner + message (a second `show()` just updates the message) |
| SearchQuery | `cerb-ui-searchquery` (+ `--icon`/`--field`/`--highlight`/`--input`/`--caret-anchor`/`--right`/`--tok-field`/`--tok-string`/`--tok-bool`/`--tok-number`/`--tok-paren`) | `CerbUI.SearchQuery` | textarea editor for **Cerb search-query syntax** (filters, lists, quoted literals, deep `sender:(org:(name:"x"))`) — the **Ace replacement** for worklist quick-search. **Live highlighting via overlay** (transparent-text textarea over a `--highlight` mirror div with color-only token spans — see the overlay gotcha in Conventions). One small JS tokenizer (`_scopePathAt`) drives BOTH the colors and the **caret scope path** (the enclosing filter chain). Keys: **Enter always submits `onSearch`**; autocomplete is opt-in (↓ into the menu to select; Shift / ⌘·Ctrl+Enter = newline; Ctrl/⌘+Space forces it). Suggestions come from `onAutocomplete(ctx)` and render in a `CerbUI.Menu` anchored at the caret (**absolute, so it scrolls with the page** — not `fixed`). `ctx = {path,prefix,context,query,caret}`; `item = {caption,value,snippet?(`$0`=caret),hint?,icon?,suppressAutocomplete?,score?}`. **Filtering is the source's job**: `CerbUI.SearchQuery.match(text,query,mode)` / `filterItems(items,query,mode)` / `MATCH_MODES` — `subsequence` (default), `substring`, `prefix`; results ordered by `score` (default `DEFAULT_SCORE` 1000, higher first; stable). **`queryFieldSource(context,{filterMode})`** = a drop-in `onAutocomplete` that lazy-loads from the existing `c=ui&a=querySuggestions` / `c=ui&a=dataQuery` endpoints (per-scope cache + a `_contexts` map for nested record contexts), converting backend Ace `${1}`/`${1:def}` snippets → our single `$0` caret marker. **Group-key scope convention**: when the caret is inside a parameterized `field:(…)`, `_scopePathAt` tags the path's FINAL segment with a trailing `()` (e.g. `closed:()`), so a source serves that group's fixed sub-keys (date params: since/until/days/dom/weeks/months/time); look up `field:()` first, fall back to the plain `field:` key (record contexts nest via `_contexts`, value fields show value forms). `getValue/setValue/focus/openAutocomplete/destroy`; `from(el)`. Backend autocomplete lives in `DAO_*::getQuickSearchFields()` → `getQueryAutocompleteSuggestions()` (`abstract_view.php`, a flat `scopeKey → suggestions[]` map) + the `_uiAction_querySuggestions` expand loop (`api/uri/ui.php`); the same `queryFieldSource` cache logic mirrors the legacy Ace completer in `cerberus.js` |

| Calendar | `cerb-ui-calendar` (+ `--toolbar`/`--legend`/`--month`/`--week`/`--day-view`/`--year`/`--strip`/`--minimonth`/…) | `CerbUI.Calendar` | **inline** day/week/month/year calendar; multiple event **sources** + a click-to-toggle legend, true multi-day **spanning strips** (not per-day repeats), year pips + `CerbUI.Tooltip` + drill-down, click-empty-to-create peek. Feed a source's `fetch(startSec,endSec)` (epoch seconds) or static `events[]`; `serverShape:true` accepts the raw day-keyed `Model_Calendar::getEvents()` map (auto de-duped). Pure logic in `calendar-core.js` (`CerbUI.cal`). **Full reference → `references/cerb-ui-calendar.md`** (DST-safe IANA timezone model, the widget JSON-endpoint host, spanning-strip lanes, `CerbUI.color`) |

## Utilities (`cerb-u-*`) — a separate layer from the components

Bootstrap-style **single-purpose utility classes**, dropped onto any element/component independently — a
distinct namespace from the `cerb-ui-*` components. Source: `install/extras/developers/css/cerb.css/layout/cerb-utilities.scss`,
`@import`ed **after** the component partials in `cerb.scss` (so an equal-specificity utility wins the cascade,
e.g. `.cerb-u-border-medium` overrides `.cerb-ui-panel`'s border width). Keep them atomic (one class = one
declaration); no `!important` unless a utility must beat a higher-specificity selector (e.g. `cerb-u-hide`
uses it). `composer build-css` to compile. Current set:
- `cerb-u-hide` (display:none !important), `cerb-u-block` (display:block)
- Flex container: `cerb-u-flex`, `cerb-u-flex-wrap`, `cerb-u-items-center` / `cerb-u-items-stretch`,
  `cerb-u-justify-center` / `cerb-u-justify-between`, `cerb-u-flex-shrink-0`; child grow ratios
  `cerb-u-flex-{1..4}` (compose any split — two `flex-1` = halves); `cerb-u-gap-{0..5}` between children
- Text: `cerb-u-bold`, `cerb-u-text-center`, `cerb-u-text-uppercase`, `cerb-u-nowrap`
- `cerb-u-relative` (position:relative), `cerb-u-cursor-pointer`, `cerb-u-bg-none` (strip a component's fill)
- `cerb-u-w-{25,50,75,100}` — width %
- `cerb-u-border-{0..5}` — 0–5px border-width (the element must already have a border style)
- `cerb-u-rounded-{0..4}` — border-radius 0/4/6/8/10px (2=inputs/buttons, 3=chips/menus, 4=panels); `cerb-u-rounded-full` (999px) pills it
- Spacing (Bootstrap-like): `cerb-u-{m,p}{,t,r,b,l,x,y}-{0..5}` — margin/padding, side = all/t/r/b/l/x/y,
  step multiplies `--cerb-u-spacer` (default `1rem`) by the Bootstrap scale 0, .25, .5, 1, 1.5, 3; plus
  auto margins `cerb-u-ml-auto` / `cerb-u-mr-auto` / `cerb-u-mx-auto` (flex "push"). The spacing/border/gap
  scales are generated by SCSS loops in `cerb-utilities.scss`.

## Icons (`cerb-icons`)

Cerb's icon set is **Lucide**, rendered as monochrome CSS masks (not `<img>`/`<svg>` elements), so they
tint with text color and scale with font size.

- **Use:** `<span class="cerb-icons cerb-icon-<name>"></span>`. `.cerb-icons` is the box (`display:inline-block`,
  `width/height:1em`, `vertical-align:middle`); `.cerb-icon-<name>` supplies the glyph. It's a **mask**
  filled by **`currentColor`**, so `color:` tints it and `opacity` dims it; size follows `font-size` (it's
  `1em`). Many wrappers auto-bump size (e.g. `.worklist td > a > span.cerb-icons` → 1.2em).
- **Mechanism / source of truth:** `install/extras/developers/css/cerb.css/layout/cerb-icons.scss` — a
  `$icons` SCSS map (`name: "<path …/>"`), the `@mixin icon-svg($svg)` that wraps each path in a viewBox-24
  `<svg>` data-URI as `mask-image` + `background-color: currentColor`, and an `@each` that generates one
  `.cerb-icon-<name>` per entry. **Add an icon** = add a row to `$icons` (Lucide path markup), then
  `composer build-css`.
- **Discover names:** the in-app **UI Reference → Icons** browser (filter / show-labels / click-to-copy
  markup); enumerated server-side by `getCerbIcons()` in `libs/devblocks/api/services/ui.php` (assign in
  PHP, never call the static from a template).
- **From JS-built markup:** emit the same classes as a string (e.g. the editor autocomplete-menu icons and
  the KataEditor gutter fold chevrons). An icon needs no text content — a classed **empty** element still
  paints (the glyph is the mask), which is how KataEditor draws its end-of-line fold indicator.

## Files & build (not shown in the gallery)

**CSS** — split into **per-component partials** `install/extras/developers/css/cerb.css/layout/cerb-ui/_<name>.scss`
(mirroring the JS split); `layout/cerb-ui.scss` is the ordered `@import` index — **order is load-bearing**
(a few in-component cascade tricks depend on it, keep it stable) — and is itself `@import`ed in `cerb.scss`.
Structural only — chart colors come from JS. `composer build-css` → `cerb.css`. See `references/scss-build.md`.
**Caching gotcha:** `cerb.css` (and `cerberus.js`) are served with `?v=APP_BUILD`, **not** live like the dev
cerb-ui JS below — so a CSS edit needs a **hard refresh** (or an APP_BUILD bump) to show. A normal reload keeps
serving the old stylesheet; "the fix didn't work" is usually this.

**JS** — one ES-class file per component under `features/cerberusweb.core/resources/js/cerb-ui/`
(committed, web-served, dev-only): `_core.js` (defines `window.CerbUI` + the `valueAttr`/`textAttr`
helpers), `palettes.js`, then one file per component. No bundler, no `import/export`, no TypeScript — each
file attaches a class to the `CerbUI` global, so files concatenate cleanly and load standalone.

Besides components, a few **non-component utility namespaces** attach as plain objects (like `palettes`):
`CerbUI.date` (`date.js`) — `remain(sec)` (countdown: "now"/"45s"/"2:05"/"20h"/"1d") and `ago(sec)`
(relative past: "just now"/"3m ago"/…); `CerbUI.num` (`num.js`) — `compact(n)` (1500→"1.5k"). Both take a
plain seconds delta / number, not Date objects. Register a new utility file right after `palettes.js` in
both the `composer.json` `build-js` list and the `header.tpl` dev `<script>` block.

- **Dev (`DEVELOPMENT_MODE`):** the per-file `<script>` list lives in **`templates/cerb_ui_scripts.tpl`**
  (a `DEVELOPMENT_MODE` conditional — raw sources in dev, the one minified bundle in prod), `{include}`d by
  `header.tpl` **and** `explorer/index.tpl` + `explorer/automation/index.tpl` (so one edit covers all entry
  points). Files load in dependency order with `?v={$smarty.now}` (defeats the 1-week resource cache → edit +
  refresh, no build). **When "Adding a component" (below) says header.tpl, edit `cerb_ui_scripts.tpl`.**
- **Prod:** a single minified `resources/js/cerb-ui.js` (committed, like `cerb.css`).
- **Build:** `composer build-js` = concat + minify with **terser** (a dev/release-env tool installed like
  `sass`; `npx --yes terser …` for a one-off) — its file list must stay in the **same order** as
  `cerb_ui_scripts.tpl`. `composer dist` = `build-css` + `build-js`.

**Retiring a legacy jQuery plugin** (e.g. porting `jquery.qrcode` → `CerbUI.QrCode`): the served jQuery bundle
`libs/devblocks/resources/js/jquery/jquery.combined.min.js` is **hand-concatenated — there is NO build script**
for it (the `_development/*.js` files are its sources). To drop a plugin, **excise its IIFE segment directly**
from the combined file (each plugin = a `(function(r){…})(jQuery);` block; adjacent plugins share the line at
their seam, so keep the previous plugin's `})(…);` close) and delete its `_development/*.js` source. `node
--check` the result. The inventory of remaining plugins + what each is used for lives in
`PLANS/DONE/PLAN-jquery-ui-to-cerb-ui.md`.

## Conventions (not obvious from the gallery)

**Class names:** `block`, `block--element`, `block--modifier` — **double-dash for both** elements and
modifiers (matches existing Cerb, e.g. `cerb-card-widget--header`). No BEM `__`.

**Naming a new component:** check for collisions across `cerb.css` + the SCSS partials first, and avoid words
already overloaded in Cerb's *domain* even if the `.cerb-ui-*` class is free — e.g. `token` (placeholders /
API & CSRF tokens), `tag` (the `--cerb-color-tag-*` palette + legacy `.tag-*` labels). Reserve the obvious
word for its literal future use (a real tag/token component) rather than spending it on a lookalike.

**Tokens only:** every color is `var(--cerb-color-*)` (or the JS palette) → dark mode is automatic via
`html.dark`. Never `prefers-color-scheme`.

**Explicit markup, no magic:** components attach behavior to authored markup; they don't infer structure
(exception: Legend generates its inner DOM, since items are pure data).

**Popup title via `data-cerb-dialog-title` (not inline-JS `setTitle`):** the `genericAjaxPopup` adapter reads a
`data-cerb-dialog-title="…"` attribute off the **top-level element** of the fetched content (`$popup.children('[data-cerb-dialog-title]').first()`)
on load and calls `dlg.setTitle()`. So a popup template sets its title by adding that attribute to its outermost
`<form>`/`<div>` — **not** by the legacy `popup_open` → `$popup.dialog('option','title',"{'…'|…|escape:'javascript' nofilter}")`
shim. Wins: an HTML attribute **auto-escapes** in attribute context (no `nofilter`, no JS-string emission), and
`setTitle()` assigns via `textContent` (the security boundary) so it's XSS-safe. Opt-in: templates without the attr
are untouched; **JS-runtime-computed** titles still call `CerbUI.Dialog.from($popup[0]).setTitle(X)`. Exemplar:
`internal/cards/card.tpl`. This is the preferred conversion for the `PLAN-genericAjaxPopup-to-cerb-ui.md` Phase-5
title sweep ("add an attribute, delete a line").

**Menu/Sidebar item icons go on `data-icon`, not an inline `<span>`:** both `CerbUI.Menu` and `CerbUI.Sidebar`
**rebuild** each item row from its *text label* — a leading `<span class="cerb-icons …">` child is discarded
(Menu) or, worse, makes the `<li>` a caller-built **"raw" passthrough** that skips the icon-slot + hideable
`--item-label` entirely (Sidebar `_enhanceItem`: any non-anchor child element ⇒ raw — this is why collapse
"smashes" the text instead of hiding it). Always: `<li data-icon="<cerb-icons name>">Label</li>` (leading `.`
= raw CSS class list). Menu injects via `onRenderItem(li, srcLi)` reading `srcLi.dataset.icon`.

**`CerbUI.Menu` filter:** `filter:true` is reveal-on-type and **flattens** a nested menu (searches all leaves
with breadcrumb context) — exactly how to make submenu items findable by name. **Gotcha:** `filterIcon` only
works with `filterAlways:true`; with plain reveal-on-type the icon's wrapper row stays `hidden` (`_showFilter`
un-hides only the input), so the filter box never appears and typing breaks the menu. Build a floating dropdown
with `new CerbUI.Menu(ul, opts)` + `menu.open(anchorEl)` (floats below; outside-click ignores the anchor, so the
trigger's own handler toggles via `isOpen()`/`close()`); clean up the source `<ul>` in `onClose`.

**`CerbUI.Menu` keyboard hygiene for triggered filter menus (`captureKeys`):** a floating menu's keydown
listener defaults to the **bubble** phase (so the editor autocompletes, whose host editor must see the keydown
first, keep working). For a *standalone* triggered filter dropdown (e.g. a record/bucket picker opened from a
button **behind which a page has hotkeys** — a worklist `r`=reply), pass **`captureKeys:true`**: the menu then
listens in the **capture** phase and `stopPropagation()`s the keys it consumes (the filter-reveal keystroke,
arrows, Enter, Esc, Home/End), so type-to-filter no longer leaks to those page shortcuts. Capture is opt-in
precisely because it would otherwise fire *before* an editor's own textarea keydown and break autocomplete nav.
Independently (always on), the menu now **returns focus to the anchor/trigger on select or Esc** (`_returnFocus`)
so keyboard TAB order continues from the trigger — a no-op when the anchor isn't focusable (e.g. an
autocomplete's caret span).

**Nested type-to-filter picker recipe (group→bucket, "Move"/"From"):** a `cerb-ui-button--subtle` trigger
(carrying `data-group-id`/`-label`/`-avatar` + a `[data-…-icon]`/`[data-…-label]` span) over a hidden nested
`<ul>` (parent `<li data-group-id …>` with a bucket-submenu `<ul>` of `<li data-group-id data-bucket-id …>`),
hidden inputs for the posted ids, and `new CerbUI.Menu(ul, {filter:true, captureKeys:true,
panelClass:'cerb-bucket-menu', onRenderItem, onSelect})`. `onRenderItem` swaps a flattened/pathed leaf for an
avatar + eyebrow(group)/main(bucket) stack (`cerb-bucket-menu--avatar/--text/--eyebrow/--main`); `onSelect`
writes the hidden ids + updates the trigger label/avatar (only leaves with `data-bucket-id` select). Live in
`display/rpc/reply.tpl` (Move) and `mail/section/compose/peek.tpl` (From).

**Firing `cerb-bot-trigger` interactions from a `CerbUI.Menu`:** bind `jQuery(li).cerbBotTrigger(opts)` to the
**source** `<li>`s (keep the fetched `<ul>` in the DOM, hidden), then in `onSelect(rendered, source, e)` call
`jQuery(source).trigger('click')` — the menu renders new rows, but `source` is the original `<li>` carrying the
`data-interaction-*` attrs + the binding (same shim `CerbUI.Toolbar` uses). Toolbar `parse()` only normalizes
**top-level** items (resolves `cerb:` URIs, adds `type`, runs caller-policy); nested `menu/…  items:` keep their
raw fields, so a submenu interaction's `uri:` must be the already-resolved automation name (not `cerb:automation:…`).

**Syntax-highlighting a `<textarea>` (overlay technique — SearchQuery, future KATA editor):** a textarea
can't hold colored spans, so render its text **transparent** (keep the caret via `caret-color`) over a mirror
`--highlight` div that carries the colored token spans, scroll-synced. The two layers MUST share **identical
glyph metrics** — wrap/font/padding/line-height/box-sizing — so highlight tokens are **color only**: never
`font-weight`/`font-style`/`letter-spacing` differences, or wider glyphs push the colored text off the real
caret (the caret visibly drifts left of the `:` it sits on). Measure the caret pixel for an anchored dropdown
with the standard **mirror-div** trick (clone the textarea's text styles, slice at the caret, read a marker
span's offset). Two raw-`<input>`/`<textarea>` chrome gotchas you'll hit: (1) a **global `TEXTAREA:focus {
border: … }`** (and the UA focus ring) — beat them with a **`:focus`-qualified** reset on your class
(`.cerb-ui-searchquery--input:focus { border/outline/box-shadow: none }`, specificity (0,2,1) > the element
selector's (0,1,1)), not an unqualified rule; (2) WebKit/Safari draws **native textarea chrome** that
`border:0` alone won't remove — add `appearance: none`. Also turn off `spellcheck`/`autocomplete`/`autocorrect`/
`autocapitalize` on the textarea (set in JS) — it's a query editor, not prose.

**Instance lookup — `CerbUI.X.from(el)`:** every JS component registers itself in a private static `WeakMap`
keyed on the element you construct it with, and exposes `static from(el)` to retrieve that instance later
(returns `undefined` if none). Use it when you only have the DOM node — re-key a Switcher, push a value into
a TimeRing, open a Menu — without threading the instance through your own state. Add this to any new JS
component (`static _instances = new WeakMap()` + register `this.el` in the constructor + `static from`).
Toggle keys on **both** the `<input>` and the `<label>` you passed. Tooltip is the lone exception (it creates
its own element, so there's no source node to look it up by).

**Focus ring — one shared treatment (`cerb-ui-focus-ring`):** every text-like control shows the SAME keyboard/active
focus: a saturated `--cerb-color-action-primary` border **+** a 2px outline (offset 1px). It lives as a mixin-only
partial `cerb-ui/_focus.scss` (`@mixin cerb-ui-focus-ring`), imported **first** in `cerb-ui.scss` (emits no CSS, so it
doesn't disturb the order-sensitive cascade). Apply it with the pseudo-class that fits the control: native inputs/
textarea/select → `&:focus` (`_form.scss`); the chooser family + file-upload **containers and chips** → `&:focus-within`;
SelectMenu (a focusable button-like div) → `&:focus-visible`. **Do not** use `--cerb-color-form-element-focus` for focus
— it's a lighter blue that is **not** redefined in `html.dark`, so it renders washed-out (this is exactly why the old
form inputs "had no nice blue"). Per-control gotchas: **Toggle** — the real `<input>` is `0×0`/`opacity:0`, so paint the
ring on the slider: `input:focus-visible + .cerb-ui-toggle--slider`. **Switcher** — the container is `overflow:hidden`,
which clips an *outward* outline; **inset** it (`outline-offset:-2px`) + `position:relative; z-index:1`. **Chip/tile** —
an element's own `overflow:hidden` clips its *children*, **not** its own outline, so `.…--tile:focus-within { @include
cerb-ui-focus-ring; }` rings the whole chip fine.

**Keyboard-reachable peek chips:** `jQuery.fn.cerbPeekTrigger()` (in `cerberus.js`) **only binds `click`**, and Cerb's
peek anchors are rendered **href-less** — so a chip's `<a class="cerb-peek-trigger">` label is **not a tab stop** and
can't be opened by keyboard. To fix a chip label: `setAttribute('tabindex','0')` + `setAttribute('role','button')` +
a `keydown` that maps Enter/Space → `el.click()` (preventDefault on Space). Then ring the tile via `:focus-within`. Doing
this once in `RecordChooser._buildTile` covers **ContextChooser/Owner, TagInput, ValuePicker** (they reuse that tile);
`FileUpload._finishTile` is the parallel spot for upload chips. Leave non-peek labels (e.g. the `id===0` "Everyone"
plain `<span>`) non-focusable.

**Visually-hidden-but-focusable = dead tab stop:** a control hidden via `position:absolute;width:1px;clip:rect(0,0,0,0)`
(not `display:none`) is **still focusable** — e.g. FileUpload's real `<input type=file>`, which the button/well proxy
clicks to. Take it out of the tab order: `tabIndex = -1` + `aria-hidden="true"`. Also: a bare authored `<button>` defaults
to `type=submit`; a JS component that enhances authored buttons (Switcher) should force `type="button"` so keyboard Enter
doesn't submit a surrounding form.

**`.cerb-ui-form` out-specifies component input rules (0,2,1 > 0,1,1):** the form layer's `.cerb-ui-form input[type=text]
{ padding: … }` (and its `:focus`) **beats** a component partial's `.cerb-ui-foo--wrap > input` (0,1,1) — so e.g. a
leading-icon indent set in the partial gets reset by the form's `padding` shorthand. Established fix: add an *equal-
specificity* rule **inside `.cerb-ui-form`**, declared **later in source order**, so it wins (precedents in `_form.scss`:
`.cerb-ui-text-chooser--has-icon > input` and `.cerb-ui-datepicker-forminput > input`, both `padding-left:` overrides).
Diagnose padding/focus that "won't apply" by checking the form layer first, not just the component partial.

**Chart data — two parallel namespaces**, keyed the same way (a suffix, or none = default):

| Purpose | Default | Named (`key='size'`) | Helper |
|---|---|---|---|
| numeric (math) | `data-value` | `data-value-size` | `CerbUI.valueAttr(key)` |
| formatted display | `data-text` | `data-text-size` | `CerbUI.textAttr(key)` |
| series label | `data-label` | — | — |

Separate `data-value*` / `data-text*` namespaces avoid the `data-value-text` vs. `key="text"` collision.
`data-text-{key}` carries locale-formatted numbers/bytes (`data-text-size="2.1 GB"`,
`data-text-objects="1,234"`); the legend value falls back to raw `data-value-{key}` when absent.

**Palette** (`palettes.js`): colors assigned by **element index**, so a distbar and legend built from the
same list match. `CerbUI.resolvePalette(p)` accepts an array or name — `category10` (default, 10, D3
category10) or `rainbow` (12). A widget's **key** is what a Toggle selects; the canonical cross-component
wiring is a Toggle's `onSelect` calling `setKey` on a Distbar (which forwards to its `legend:true` legend).

**Color math (`CerbUI.color`, in `palettes.js`)** — general, not chart-specific: `parseHex(c)` (`'#rgb'`/
`'#rrggbb'` → `{r,g,b}`, null if not hex), `luminance(c)` (WCAG relative luminance 0–1), `contrastRatio(a,b)`
(1–21), and **`idealTextColor(bg)`** → near-black `#141414` or white `#ffffff`, whichever has the higher
contrast on `bg` (null for a non-hex value → let CSS decide). Use it for **legible label text on any arbitrary
fill** (tag/event/chart/user-chosen color) now that light+dark themes exist — white-on-light-pastel is
illegible. Apply it inline where you set a solid `background-color` from data (e.g. calendar event strips).
Demoed in the UI Reference **Utilities** gallery ("Color · contrast").

**Color consistency across related charts** — index coloring means the same series gets different colors in
different charts (it's positional). When charts must agree (e.g. a summary bar + per-row bars + swatches for
the same set of things), share one **`CerbUI.colorScale(palette)`** (an ordinal scale, D3 `scaleOrdinal`
style): its `.color(key)` assigns a palette color on first sight of a key and memoizes it. Pass the same
instance as `{scale}` to every Distbar/Legend that should agree; they color by `data-color-key` (falling back
to `data-label`) instead of index. Build the "canonical" chart first so it primes the scale's order. Index
stays the default for standalone arbitrary datasets.

### Interactive SVG viz — the d3-replacement playbook (pan/zoom, drag, wheel, validation)

Built for `CerbUI.Map` (`cerb-ui/map.js`) but **reusable for any hand-rolled SVG viz that pans/zooms**. These
are the non-obvious wins:

- **Validate a homegrown port against the lib it replaces, as a Node oracle.** `d3.v5.min.js` and
  `topojson.v3.min.js` `require()` cleanly in Node (UMD) — so a pure-logic harness computed projections / decode
  / color with BOTH and asserted equality (projections + HCL ramp + quantize match d3 exactly; TopoJSON decode
  byte-identical over ~250k pts) **before deleting the lib**. This is the standard gate for the whole d3/c3
  phase-out: port → assert-equal-to-oracle → delete. Charts/Timeblocks use the same DOM-stub harness pattern
  (fake `document.createElementNS`/`El`), so the build path is testable without a browser.
- **Keep strokes constant under a `<g>` zoom via `vector-effect="non-scaling-stroke"`** (set once at creation) —
  the browser holds stroke width regardless of the parent `scale()`, so you never loop elements to rescale
  strokes. NB it covers **stroke only**; `<circle>` `r` still needs a counter-scale on zoom.
- **Gate per-frame per-element loops on actual state change.** A pan changes only the `<g>` translate (zoom `k`
  unchanged), so rescaling every element on every `mousemove` is pure waste (thousands of `setAttribute` on a
  dense map). Track `_lastK`; only run the point-rescale loop when `k` changed → pan is O(1)/frame. This, not
  WebGL, was the real fix for dense-map jank. (Canvas 2D — not WebGL — is the escalation past ~tens of thousands
  of features; SVG stays default for a11y/theming/crisp text.)
- **Drag-vs-click = a capture-phase click suppressor** (replaces d3 `zoom.clickDistance`). Track pointer travel
  from the press point; past a small threshold set a flag and let a **capture-phase** `click` listener on the
  container `stopPropagation()` (eats the trailing click before it reaches the feature's target-phase handler);
  reset on next `pointerdown`. Without it, releasing a pan selects whatever's under the cursor.
- **Cooperative wheel scroll — don't trap the page.** A single **shared, page-wide** passive capture-phase
  `wheel` listener records where the current gesture *began* (nearest `.cerb-ui-map`, or the page; a new gesture
  starts after a ~250 ms idle gap); each instance zooms only when it owns the active gesture. So a dashboard
  scroll passing over a map falls through instead of stopping at it. (Plain always-`preventDefault` wheel = the
  trapping bug.)
- **CSS `fill`/`stroke` beat the SVG presentation attribute** — set per-datum colors via `setAttribute('fill',…)`,
  then dim/override via a `.is-dimmed { fill: … }` CSS class (property > presentation attribute; no `!important`).
- **Porting d3 color: HCL uses the Bradford-adapted D50 matrix** (`0.4360747…`), NOT the sRGB-D65 matrix
  (`0.4124564…`). Mixing the D65 matrix with d3's D50 white point makes a choropleth ramp diverge ~14 rgb units
  mid-scale while the endpoints still match — a subtle bug the oracle catches instantly.

## Converting legacy `<fieldset class="peek">` chrome to panels

The bread-and-butter migration (config fragments, peeks, widget configs): swap legacy chrome for the panel
+ form layer. Editors inside are usually **already** CerbUI (DataQuery/KataEditor/JsonEditor/SearchQuery/
ScriptingEditor/Slider/ColorPicker), so it's chrome + form-field work, not editor work.

**Markup recipe:**
- `<fieldset class="peek"><legend>X</legend> … </fieldset>` →
  `<div class="cerb-ui-panel cerb-ui-panel--spaced"><div class="cerb-ui-header cerb-ui-header--tight"><div class="cerb-ui-header--title-sm">X</div></div> … </div>`.
  A legend that carries a docs button → header `--center` + the button in a `cerb-ui-header--right`.
- `<b>Label:</b>` + an indented control → a `cerb-ui-form--field` (`--label`, `--hint` for "(optional)")
  inside a `<div class="cerb-ui-form">`. Drop inline width/margin; native `<select>` stays native (the form
  auto-styles it), long ones get `CerbUI.SelectMenu`. **Preserve every POST `name`/`value` verbatim.**
- boolean checkbox → `CerbUI.Toggle` (CSS-only); binary/enum radios → `CerbUI.Switcher` (hidden input + buttons
  + `new CerbUI.Switcher`); inline-flow ("Cache for [N] seconds") → a `cerb-u-flex cerb-u-items-center cerb-u-gap-1`
  row. A toolbar strip directly above an editor → wrap both in `cerb-ui-kataeditor-wrap` (floats the strip).
- Multi-select checkbox **groups** (e.g. sum/mean/min/max) — leave as inline checkboxes in a flex row; don't
  force a row of toggles.

**JS-coupling traps (the only real risks — grep each converted file's `<script>` first):**
- **`closest('fieldset')` / `$('fieldset#id')` break the moment the fieldset becomes a `<div>`.** Retarget:
  add a `data-*` hook (e.g. `data-cerb-results-panel`, `data-cerb-series`) and `closest('[data-…]')`, or move
  the `id` onto the panel `<div>` and use `$('#id')`. Dynamically shown/hidden result/preview fieldsets → a
  hidden `cerb-ui-panel` carrying that data-hook (mirror `internal/renderers/test_results.tpl`).
- **Event-handler tester panels break `closest('fieldset')` once the editor lives in a `cerb-ui-panel`** —
  the tester KataEditor never instantiates → **types black-on-black, no gutter**. **Fix (2026-06-30): call the
  shared helper** `CerbUI.editorCore.attachEventHandlerTester($scope, mainEditor)` (editor-core.js) — $scope is
  `$popup`/`$frm`/the editor's panel; it finds `[data-cerb-event-tester]` within, builds the placeholders
  KataEditor, and wires Run → `automation_event/tester` (results = clickable handler bubbles that `gotoLine`).
  Do NOT hand-inline the ~55-line block (the old advice). The legacy `$.fn.cerbCodeEditorToolbarEventHandler`
  now DELEGATES to this helper, so its `<fieldset>` callers still work. **Toolbar-editor tester** (different
  endpoint) = `$el.cerbCodeEditorToolbarHandler({editor, scope:$popup})` — pass `scope` when the editor is in a
  panel (falls back to `closest('fieldset')`). Show-hide toggles come from the editor toolbar's `onAction`
  (`placeholders`/`tester`), not the helper. Exemplar: `records/types/automation_event_listener/peek_edit.tpl`.
- **Radios that drove show/hide become a `Switcher` — move the logic into `onSelect`.** Once the radios are
  gone there's no `change` event to listen on; the Switcher's `onSelect(value)` is where you toggle the
  dependent panel (and still write the hidden POST input). For MULTIPLE switchers in one peek, init them in a
  single `$popup.find('.cerb-ui-switcher[data-cerb-input]').each(...)` loop and branch on `input.name` inside
  `onSelect` to run each one's dependent-panel toggle (calendar peek: `params[manual_disabled]` ↔ color panel,
  `params[sync_enabled]` ↔ datasource panels).
- **RESERVED peek button classes — never reuse `delete`/`save`/`save-continue`/`delete-prompt`/`create` on any
  other button inside a peek.** The peek wires them UNSCOPED: `$popup.find('button.delete')` →
  `callbackPeekEditSave({mode:'delete'})` (deletes the whole record), `button.save` → save, etc. A component
  button that happens to carry `class="delete"` (e.g. a custom-fieldset **remove** ✕) gets caught by that
  binding and nukes the record. Give component action buttons a namespaced class (the custom-fieldset remove is
  `cerb-custom-fieldset--remove`, wired by its own scoped `#{$fieldset_domid} > .cerb-ui-header button…`
  selector). The `delete_confirm.tpl` "Yes" button is the ONE legitimate `button.delete` in a peek.
- **`CerbUI.SelectMenu` only on STATIC `<select>`s.** It builds its source `<ul>` from the options once at init,
  so a select whose `<option>`s are populated later via AJAX (calendar datasource, profile-tab type-by-context)
  must stay native. Enhance only server-rendered selects (name/type/timezone/record).
- **AJAX-populated select → `.trigger('change')` to auto-load its dependent config.** After appending options to
  a native select from an AJAX response, fire `change` so the dependent config loads for the (auto-selected
  first) option — picking an option that's already shown wouldn't fire `change`, leaving the config empty (the
  profile-tab fresh-create "Dashboard has no layout options" bug).
- **AJAX-injected `renderConfig()` partials can't rely on their own inline `<script>`** (injected via
  `innerHTML`/`genericAjaxGet`, so scripts don't execute). Use pure-CSS controls that work without JS init: a
  bare `cerb-ui-toggle` (label toggles the checkbox, slider is CSS) or a `cerb-ui-layout-choice` (visual radio
  card: hidden radio + `input:checked + svg` accent border). Both survive AJAX injection.
- **`.cerb-peek-trigger` / any once-wired jQuery plugin must be RE-wired on AJAX-injected content.** A peek wires
  `$popup.find('.cerb-peek-trigger').cerbPeekTrigger()` once on `popup_open`; markup injected into a lazy tab
  later (e.g. the automation Usage tiles) misses it. Re-run `.cerbPeekTrigger()` (scoped to the injected panel)
  in the inject callback. Give clickable elements a real `href` too so they degrade to plain navigation.

Verify each with the in-container `template()->fetch()` harness (see `references/smarty-conventions.md`).
Full living playbook + the per-family file inventory: repo `PLAN-jquery-ui-to-cerb-ui.md`.

## Editor family internals (`editorCore`) — patterns for textarea editors

`CerbUI.SearchQuery`, `CerbUI.KataEditor`, and `CerbUI.JsonEditor` share `CerbUI.editorCore` (overlay
highlight, caret-anchored autocomplete, the `kataScript` tokenizer, and a keyboard matcher). Full depth +
roadmap live in `PLAN-kata-editor.md` (repo root); the reusable patterns:

- **Author just a `<textarea>` — the editor builds its own shell.** Every editor family (Kata/Scripting/
  DataQuery/Json/Markdown/SearchQuery) is **polymorphic**: pass a **bare `<textarea>`** (carrying `name`,
  value, `data-editor-lines`, `data-editor-readonly`, `placeholder`) to the constructor and it generates the
  `--gutter?/--field/--highlight/--input/--caret-anchor` shell around it — no 6-line boilerplate. A pre-built
  `.cerb-ui-<NS>` wrapper still works (backward compatible), so point JS at the textarea
  (`new CerbUI.KataEditor($frm.find('textarea[name=x]')[0], opts)`) OR the wrapper. There's also a named
  factory `CerbUI.X.enhance(field, opts)` (handles wrapping an `<input>` as a hidden `--value` carrier + shadow
  textarea). Mechanism: `CerbUI.editorCore.buildEditorShell/resolveEditorEl/enhanceEditor` + each class's
  `static _NS`. MarkdownEditor = no gutter; SearchQuery self-builds the search icon + a suggestions button (for
  custom `--right` actions, still author the full shell). Recipe + status = `PLANS/PLAN-texteditor-enhance.md`.
  Gotchas when converting: keep a `cerb-ui-<NS>-wrap` + its embedded toolbar `<ul>` (only the inner shell
  collapses); retarget any `.cerb-ui-<NS>(--input)` JS lookups to the textarea or `ed.textarea`.
  - **Sweep status (2026-06-29):** all 5 CODE-editor families (kata/scripting/json/markdown/dataquery) are
    fully collapsed to bare textareas across `features/`+`plugins/` (0 shells left). **SearchQuery deferred**
    (11 files) — most carry a custom `--right`, so they stay explicit. NOTE the SQ filter trap: a path like
    `*/portal/.../configuration/*` is NOT the config section — don't exclude it with `grep -v /configuration/`.
  - **Shared tester editors (2026-06-30):** the ONE implementation of the event-handler tester (placeholders
    KataEditor + Run + results) is `CerbUI.editorCore.attachEventHandlerTester($scope, mainEditor)`
    (editor-core.js). `$.fn.cerbCodeEditorToolbarEventHandler` (cerberus.js) delegates to it; the toolbar-editor
    variant `$.fn.cerbCodeEditorToolbarHandler` takes an optional `scope` (else `closest('fieldset')`). The
    shared tester/help/preview includes — `automations/triggers/editor_event_handler{,_placeholders}.tpl`,
    `toolbars/editor_toolbar{,_help}.tpl`, `ui/toolbar/preview.tpl` — are now `cerb-ui-panel`s, so any peek that
    includes them gets a modern tester/preview for free. The placeholders-editor toolbar strip is the modern
    `cerb-ui-editor-toolbar` (see styling playbook), NOT `cerb-code-editor-toolbar`.
  - **Re-parenting gotcha:** the shell builder inserts a wrapper between the textarea and its original parent,
    so `$(textarea).parent()/.siblings()/.next()` break — use `.closest('[data-…]')` on a stable ancestor.
  - **DataQuery suggest button:** collapsing drops any inline `--right` autocomplete `<a>`; restore it with
    `toolbar: true` (built-in Suggestions). Keyboard Ctrl/⌘+Space works regardless. Chart widget configs were
    normalized to `toolbar: true`; compact decision-node/await DataQuery editors stay keyboard-only.

- **Keyboard shortcuts (`CerbUI.editorCore.keys`):** match on **`e.code`, not `e.key`** — Opt/Alt+letter
  on Mac yields a *different* `e.key` (Opt+D → `∂`), but `e.code` stays `KeyD`. `Mod` = Cmd ‖ Ctrl (one
  spec covers both); specs like `Mod-D`, `Alt-ArrowUp`, `Mod-Shift-ArrowDown`, `Mod-BracketLeft`. `label()`
  renders OS-aware hints in each platform's order (Apple HIG `⌃⌥⇧⌘`, no separators; Windows `Ctrl+Shift+…`).
  Per-editor registry = declarative descriptors `{id, keys, label, menu, run}` + a dispatcher that runs
  before menu/Enter handling + `getShortcuts()` (enumerable, for a future shortcuts-hint popup).
- **Edit a `<textarea>` without nuking native undo:** a direct `el.value = …` **wipes the browser's undo
  stack** (Cmd+Z then escapes to the browser — e.g. reopens a closed tab). Instead select the changed span
  and apply it via **`document.execCommand('insertText' | 'delete')`**, which records a real undo entry;
  guard with a flag so the *echoed* `input` event is ignored. On the `input` event, check
  **`e.inputType === 'historyUndo' | 'historyRedo'`** to skip side effects (don't re-pop autocomplete on undo).
- **Code folding = model + projection:** a native textarea **can't hide rows**, so KataEditor keeps the
  full text in a `_model` (source of truth — `getValue()`/`onChange` return it) and shows a *projection*
  (model minus folded line-ranges) in the textarea; every projection edit is diffed back into the model.
  Invariant: **model = projection with hidden rows reinserted**. Public rows/coords are model-space;
  caret/pixel math is view-space. Fold toggles are intentionally **not** undoable (written via direct
  assignment, not `execCommand`).
- **Autocomplete pipeline (`editorCore.Autocomplete`) = `onScope` + `onItems`:** the host wires two
  callbacks. `onScope(text,caret)` → `{path,prefix,…}` parses the caret context (KataEditor's
  **`_scopePathAt`** decides KEY vs VALUE position with the key regex `^(\s*)(key/id@anno):` — a `key:` left
  of the caret on the line ⇒ value position, prefix = the word after it). `onItems(ctx)` returns the
  suggestion array — **return `[]` to keep the menu closed** (there is no separate "should I open" flag; an
  empty result *is* the close signal). KataEditor centralizes every "stay quiet" rule in one predicate,
  **`_autocompleteSuppressed(text,caret)`**, which `onItems` consults: `#` comment lines, inside an
  `@annotation` text block, **and** the caret glued to a just-completed `key:` before its separator (KATA
  writes `key: value` (space) or `key:`+CRLF+indent — the indent case lands the caret on a fresh line with no
  same-line key, so it's allowed; only no-whitespace same-line is suppressed). **To gate suggestions in a new
  caret context, extend `_autocompleteSuppressed` — don't patch the trigger.** Gotcha that makes this matter:
  after accepting an item, `Autocomplete._apply()` **re-triggers when the post-apply scope `prefix` is empty**
  (an empty prefix matches everything), so completing a key (caret right after `:`) would otherwise re-pop a
  value menu instantly. SearchQuery's `item.suppressAutocomplete` is the *per-item* version of the same idea.
- **`CerbUI.JsonEditor` (`cerb-ui/jsoneditor.js`, `_jsoneditor.scss`, `cerb-ui-jsoneditor--*`):** a JSON
  sibling of KataEditor built by **reusing KataEditor's entire fold model/projection + gutter + editing
  machinery verbatim** and swapping only the two language-specific methods — proof the fold machinery is
  agnostic to *how* ranges are computed (all downstream code consumes `{headerRow, startRow, endRow}`
  descriptors). (1) **`_tokenize`** = a simple line tokenizer: a `"…"` before a `:` is `property`, else
  `string`; plus `number` and the `true`/`false`/`null` `keyword`; structural punctuation/whitespace is
  unclassed `text`. Token colors reuse the shared `--cerb-editor-syntax-*` palette (property=tag/teal,
  keyword=type/purple). (2) **`_foldableRanges`** = string-aware **bracket matching** (`{}`/`[]`, ignoring
  brackets inside strings; in-string flag resets each line since JSON strings can't span lines) instead of
  KATA's indentation scan; `endRow = closeLine − 1` so the **closing-bracket line stays visible** (trailing
  commas survive folded), and same-line opens (`"a": [{`) keep only the widest range per header row (one
  chevron). **Dropped** vs KataEditor: annotations/text-blocks, `#` comments, `cerb:` URIs, the `kataScript`
  `{{ }}` path, the KATA path helpers, and **autocomplete entirely** (so no `editorCore.Autocomplete`; the
  `--caret-anchor` is a reserved no-op). **Kept**: the gutter **marker** API (`setMarker`/`_MARKER_TYPES`/
  `highlightLine`) as the hook for future client-side JSON validation. New **`readOnly`** option (or
  `data-editor-readonly`): textarea `readonly` + only the fold/resize shortcuts registered + no Enter-newline;
  folding still works because projection rebuilds set `.value` programmatically. Enter auto-indent adds a
  level after a line ending in `{`/`[`. Same markup contract as KataEditor (gutter/field/highlight/input/
  caret-anchor) and the same named-textarea **value-carrier clone** for form submit.
  **Opt-in validation** (`validate:true` + `validateDelay`/`onValidate`, or call `validate()` manually):
  the static `CerbUI.JsonEditor.lint(text)` → `{valid}` | `{valid:false,row,column,position,message}` is a
  **hybrid** — `JSON.parse` is the authority on *validity* (so valid JSON is never falsely rejected), and a
  small internal recursive-descent `_locate()` finds *where*, because engine error messages don't reliably
  carry a location (modern V8 often returns `"Unexpected token …"` with no position; Safari none). `validate()`
  surfaces the first error as a single **owned** `error` gutter marker on its line (revealing the line if
  folded), the message as the marker's hover note. **XSS:** the note renders only via the escaped `title=`
  attribute (JsonEditor's `_renderGutter` additionally escapes `"` since `editorCore.escapeHtml` doesn't), the
  authored lint messages are quote-free, and `lint()` returns plain data — no markup is ever built from user
  content.
- **`CerbUI.MarkdownEditor` (prose, the 3rd editor-core member; `cerb-ui/markdowneditor.js`):** replaces the
  retired jQuery `cerbTextEditor*` stack (reply/compose composers, comments, KB, markdown custom fields). Same
  overlay/textarea/caret-anchor contract; adds the built-in formatting toolbar (`toolbar:{buttons,mode,onMode,
  sections,onAction,toolbarOpts}` — see `cerb-ui-toolbar.md`), `@mention`/`#command`/`#snippet`/`#attach`
  autocomplete scopes (`_scopePathAt`), inline-image paste (`onImage`), and the textarea command API
  (`insertText`/`replaceSelection`/`getSelection`/`getValue`/`setValue`/`setMode`/etc.). Full status in
  `PLANS/DONE/PLAN-markdown-editor.md`.
- **Host-specific autocomplete sources belong in the APP layer, not the component.** `_scopePathAt` only
  *classifies* the caret scope (returns `{trigger,path,prefix,…}`; `#snippet`/`#attach` match anywhere on the
  line via `lastIndexOf`, not just column 0); the host passes `onAutocomplete(ctx)` that branches on
  `ctx.path[0]` (`'@'`→`CerbUI.MarkdownEditor.mentionSource()`, `'#'`→commands, `'#snippet'`/`'#attach'`→record
  lookups). The reply/compose source lives in `cerberus.js` (`cerbMailReplyAutocompleteSource({mode})`), NOT on
  `MarkdownEditor` — keeps the prose component domain-agnostic. The `#command` list is a server endpoint
  (`c=ui&a=getReplyCommandsJson&mode=reply|compose`, gates `#attach` on `cerb.file_bundles`).
- **`editorCore.Autocomplete` rich-row / interaction extensions (2026-06):**
  (1) **per-item `onSelect(editor, ac)`** — when an item carries it, it FULLY handles the pick (the engine skips
  its default "value replaces the typed word"); for non-default insertions like `#delete_quote_from_here` or a
  `#snippet` pick that fires a toolbar paste event. (2) **two-line rows without an avatar** — an item with a
  `subtitle` (no `avatar`) renders label-over-description; such rows are treated as "rich" (taller `itemHeight:40`
  + a wider panel via `panelClass:'cerb-ui-editor-menu--wide'`, min 340 / max 520px) so a `#command` label isn't
  truncated by its description. (3) **`pointerInMenu()`** — tracks `mouseover`/`mouseleave` on the panel so a
  host Enter handler can select a **mouse-hovered** row even when the user never arrowed in (the menu popped up
  under a resting mouse); markdowneditor's Enter selects when `navigated || pointerInMenu()`.
- **`c=ui&a=dataQuery` of `worklist.records` returns `data` as an object keyed by record id** (PHP assoc array →
  JS object), NOT a 0-indexed array — so a JS consumer must `Array.isArray(d) ? d : Object.values(d)`. An
  `Array.isArray(json.data)` guard silently drops every row (cost real debugging time on the `#snippet` source).

## Testing cerb-ui JS in Node (no browser)

`node --check <file>` catches syntax (so does `composer build-js`, since terser parses). For **pure logic**
(keyboard matcher, fold row/offset mappers, tokenizer round-trips), stub the browser globals and `eval` the
module — no jsdom needed: `Object.defineProperty(globalThis,'navigator',{value:{platform:'MacIntel'}})`,
set `globalThis.window/document/CerbUI = {}`, then `eval(fs.readFileSync('…/editor-core.js','utf8'))` and
call the helpers directly. For instance methods, borrow the real prototype: `Object.create(Cls.prototype)`
with a stub `textarea` (`{value, selectionStart, setSelectionRange(){}, …}`) and no-op render methods, then
assert state after each operation. These are throwaway harnesses (run in `/tmp`), not committed tests.

**Spec algorithms: verify the DATA layer, not just the geometry.** For a component implementing a published
algorithm (QR/Reed–Solomon, hashing, encodings), a structural/geometry check is *necessary but not
sufficient* — a wrong inner value leaves the visible structure perfect. `CerbUI.QrCode` shipped once with a
**reversed Reed–Solomon generator polynomial** (built low-to-high, consumed high-to-low): finders, timing,
alignment, and format bits were all flawless and a structural smoke test passed, yet **nothing scanned**
because every code carried garbage ECC. Two offline gates catch this: (1) a **known-answer test** against a
published spec vector (QR v1‑M `"01234567"` → ECC `165,36,212,193,237,54,199,135,44,85`), and (2) an
**invariant check** (a valid RS codeword evaluates to 0 at generator roots α^0..α^(eccLen-1) — zero
syndromes). Both run in plain Node via the `_encodeMatrix`-style test seam; add such a seam to any
spec-algorithm component. Real-device scanning is the final confirmation, but these catch the bug first.

## Adding a component

Many components are **CSS-only** (e.g. Button, Tile, Separator) — for those, do only steps 3 and 5.
Steps 1, 2, 4 are JS-only.

1. `resources/js/cerb-ui/<name>.js` → `CerbUI.<Name> = class { … }` (attach to the global; no exports).
   Add the `from(el)` registry: `static _instances = new WeakMap()` + `static from(el) { … }`, and register
   `this.el` in the constructor (see the **Instance lookup** convention above).
2. Append the file to the `build-js` list in `composer.json` **and** the `DEVELOPMENT_MODE` `<script>`
   block in `header.tpl` (same order).
3. Structural CSS in a new per-component partial `layout/cerb-ui/_<name>.scss`, `@import`ed (in order)
   from `layout/cerb-ui.scss`; `composer build-css`.
4. `composer build-js` (or `npx --yes terser …`) to refresh the minified dist; commit source + dist.
5. **Add a gallery partial** `…/ui_reference/components/<slug>.tpl` = a `cerb-uiref-component#<slug>` (bare id)
   with one or more `cerb-uiref-example`s **+ a trailing `<script>`** with the demo wiring (this doubles as the
   component's docs). Then in `…/ui_reference/index.tpl` add an `{include …/components/<slug>.tpl}` in the right
   group and a nav `<li data-target="<slug>" data-icon="…">` (icon matching the partial's `--label`). `composer
   cache-clear`; hard-refresh for CSS (dev loads raw JS source live).
