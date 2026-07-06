# CSS utilities (`cerb-u-*`) + the grayscale design system

The atomic, single-purpose utility layer (Bootstrap/Tailwind-style) that sits alongside the `cerb-ui-*`
components. Use it to kill ad-hoc inline CSS and normalize spacing/text/color across the UI. Parallel
sessions converting pages should lean on this so every page lands on the same vocabulary.

## Where things live

- **Source:** `install/extras/developers/css/cerb.css/layout/cerb-utilities.scss` — `@import`ed **last**
  in `cerb.css/cerb.scss` so a utility wins the cascade against an *equal-specificity* component class.
- **Build:** `composer build-css` (regenerates `features/cerberusweb.core/resources/css/cerb.css`); then
  `composer cache-clear`. Hard-refresh (stylesheet is `?v=APP_BUILD`).
- **Living reference / docs:** Setup → Developers → UI Reference → **Utilities**. Edit the partial
  `features/cerberusweb.core/templates/configuration/section/developers/ui_reference/components/utilities.tpl`
  (not the `index.tpl` orchestrator).
- **Theme color vars** (the grays/tags these alias): `cerb.css/theme/cerb-theme.scss` (`:root` light +
  `.dark`). Reference only — don't hand-edit grays in component SCSS.

**Principle:** one class = one declaration; atomic and composable. No `!important` except `cerb-u-hide`.

## Inventory (keep current)

- **Display/visibility:** `cerb-u-hide` (`display:none !important`), `cerb-u-block`, `cerb-u-flex-inline`.
- **Flex:** `cerb-u-flex`, `-flex-inline`, `-flex-wrap`, `-items-start|center|stretch`,
  `-justify-center|between`, `-flex-shrink-0`, `-flex-1..4` (grow ratios), `-gap-0..5`.
- **Spacing:** `cerb-u-{m,p}{,t,r,b,l,x,y}-0..5` (× `--cerb-u-spacer` 1rem → 0/.25/.5/1/1.5/3), plus
  `-ml-auto` / `-mr-auto` / `-mx-auto`.
- **Sizing:** `cerb-u-w-25|50|75|100`.
- **Text:** `cerb-u-bold` (alias of `fw-700`), `-italic`, `-text-center`, `-text-uppercase`,
  `-text-muted`, `-nowrap`; `cerb-u-fw-400|500|600|700|800` (the step **is** the CSS weight);
  font-size = an **anchored** scale: `cerb-u-fs` (1em), `-fs-1..10` up / `-fs-n1..10` down (0.05em/step),
  `-fs-2x` (2em). The number is the *step count*, not the value.
- **Borders:** `cerb-u-border-0..5` (all-side width), `cerb-u-border-{t,r,b,l}-0..5` (per-side width);
  `cerb-u-rounded-0..4` + `-rounded-full`.
- **Effects:** `cerb-u-opacity-0|25|50|75|100`; `cerb-u-bg-none`.
- **Position/cursor:** `cerb-u-relative`; `cerb-u-cursor-{pointer,default,move,grab,grabbing,text,not-allowed,crosshair}`.
- **Animation:** `cerb-u-anim-{spin,pulse,ping,shake}` (+ `-hover` variants), `cerb-u-anim-group`.
- **Grayscale:** `cerb-u-{bgg,fgg,bdg}-1..10` + `cerb-u-bgg-hover` — see next section.

Naming idioms (follow when adding): numbered scales mirror existing ones (spacing 0–5, fs anchored, fw =
literal CSS value); **own prefix per axis** for autocomplete grouping (`fs-` size, `fw-` weight,
`bgg/fgg/bdg` gray, `cursor-` cursor). Add the utility, apply it, then document it in the gallery.

## Grayscale: `cerb-u-bgg / fgg / bdg` (+ adaptive hover)

A **relative** ladder over the hand-tuned `--cerb-color-background-contrast-*` vars. The number means
**distance from the page background** (1 = subtlest/nearest bg, 10 = max contrast) — the *same* mental
model in light and dark (the raw `contrast-NNN` names invert by brightness; this fixes that). The prefix
picks the property; all three share one ladder:

- `cerb-u-bgg-N` → `background-color`
- `cerb-u-fgg-N` → `color` (foreground/text)
- `cerb-u-bdg-N` → `border-color` (element supplies width/style)

Ladder (`$cerb-u-grays` map — retune there): `1:245 2:240 3:230 4:220 5:200 6:180 7:150 8:125 9:100 10:50`.
**Anchors:** `4` = default border (220), `7` = muted text (150), `2` = hover/fill (240).

`cerb-u-bgg-hover` is **one adaptive class**: each `bgg-N` also sets `--cerb-u-bgg-hover` to one tier more
contrast; the hover reads it and **falls back to 240** when there's no base. So a transparent element +
`cerb-u-bgg-hover` → hovers to 240; `cerb-u-bgg-2` + `cerb-u-bgg-hover` → shifts to 230. No manual
base/hover pairing. (`:hover` out-specifies the plain `bgg-N`, so the hover always wins when both apply.)

**Why alias, not `color-mix()`:** the contrast vars are hand-tuned per theme (dark mode isn't a clean
formula), so aliasing reuses them with zero drift and auto-handles light/dark. `color-mix()` *is*
available (modern-browser baseline, already used for one-off tints in `_node.scss`, `_dialog.scss`, etc.)
— use it for bespoke washes, not for the curated gray scale.

**Latent theme bug:** `--cerb-color-background-contrast-130` and `-140` are *referenced* in code but **not
defined** in `cerb-theme.scss` → they resolve to nothing. When migrating, replace with the nearest defined
step (e.g. `fgg-8` = 125).

## Methodology — converting a page's ad-hoc CSS to utilities

The repeatable pass (proved on `configuration/section/records/`):

1. **Inventory the `<style>` block / `style=""`.** Classify each declaration:
   (a) pure layout/atom that already maps to a utility → hoist to a class in markup, delete the rule;
   (b) a repeated value that's a real gap in the utility set → add a small atomic utility, then hoist;
   (c) genuine component CSS → keep.
2. **Don't shred a rule that must stay.** If a rule persists for *any* non-utility property (letter-spacing,
   transition, an `!important` override, an off-scale value), keep its utility-able siblings in it too —
   splitting one element's styling across the stylesheet *and* the markup is harder to read, not easier.
3. **Stateful / structural selectors stay.** `:hover`, `.is-open`, `:last-child`, descendant combinators,
   ID-scoped overrides — a single utility class can't express these. In particular `cerb-u-hide` is
   `!important`, so it **breaks** a togglable element whose "show" state has lower specificity — never use
   it for a toggle.
4. **Dynamic values stay inline.** `style="color:var(--cerb-color-tag-{$row.color})"` carries a runtime
   value a static utility can't.
5. **DRY check before hoisting.** A rule that styles many loop-generated rows (e.g. every `<td>`) is better
   left as one component rule than repeated as N classes in markup. Hoist when it's a single element or a
   clean win.
6. **Migrate grays last:** contrast-var `background` → `bgg`, `color` → `fgg`, `border-color` → `bdg`,
   ad-hoc `:hover{background}` → `cerb-u-bgg-hover` (standardizes the de-facto 240 hover).
7. When you add a missing atom (used ≥2×), document it in the gallery the same session.

Net effect on records: a ~52-line `<style>` block shrank to its irreducible component core (card surface,
table layout, fieldset-accordion mechanics, stateful hovers), with all spacing/flex/text/gray one-offs on
utilities.

## Documenting a utility in the gallery

- Edit `…/ui_reference/components/utilities.tpl`. It's a 2-col grid: left
  `<code class="cerb-uiref-utils--name" data-cerb-uiref-copy data-cerb-uiref-source>cerb-u-x</code>`
  (click copies its `textContent`), right a live example `<div>`.
- Group with `<div class="cerb-uiref-utils--full cerb-ui-header--label cerb-u-mt-3">Group</div>`
  subheaders; full-width notes use `cerb-uiref-utils--note cerb-uiref-utils--full`.
- **Collapse scale families onto ONE row:** left heading is the range pattern (`cerb-u-m-[0-5]`,
  `cerb-u-fw-[400-800]`), right demos the steps inline in a `cerb-u-flex` row. Keeps it scannable.
  Distinct-behavior utilities (text-center, nowrap, width bars) stay one-per-row.
- **Self-demonstrating chips** for format toggles: a single `<code>` that is BOTH the copyable name and the
  demo, e.g. `<code class="cerb-uiref-utils--name cerb-u-bold" data-cerb-uiref-copy …>cerb-u-bold</code>`.

### GOTCHA — inline `<style>` beats utilities (cascade order)

A utility only wins at **equal specificity AND when it's later in source order.** It LOSES to higher
specificity (ID, `.a.b`, and `:hover`/`:where` that add a level) **and** to a later-in-document inline
`<style>` at equal specificity. The gallery's own demo classes live in `ui_reference/index.tpl`'s inline
`<style>`, which loads *after* external `cerb.css` — so e.g. `.cerb-uiref-utils--box { background:… }`
(0,1,0, later) overrides a `cerb-u-bgg-N` (0,1,0, earlier) on the same element, and your color swatch shows
the box's gray, not yours. Fix: demo color utilities on a helper element that sets **no** background —
`.cerb-uiref-grayswatch` / `.cerb-uiref-hoverchip` (border + size only) — so the `bgg/fgg/bdg` shows
through. Same trap bites any page whose inline `<style>` restyles a property you're trying to set with a
utility.

## House style

- `const`/`let`, never `var`; scripts carry `nonce="{DevblocksPlatform::getRequestNonce()}"`.
- Sanitize/resolve in PHP, emit `{$x nofilter}` in Smarty; keep existing inline comments.
- Verify icon names exist: `grep -oE "^  [a-z0-9-]+:" install/extras/developers/css/cerb.css/layout/cerb-icons.scss`.
- Related: `references/scss-build.md` (build mechanics), `references/cerb-ui.md` (the component system),
  the repo-root `PLAN-jquery-ui-to-cerb-ui.md` (page-conversion playbook — utility normalization is part
  of each page's pass).
