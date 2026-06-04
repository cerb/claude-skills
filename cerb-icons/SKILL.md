---
name: cerb-icons
description: Design SVG icons for Cerb's custom SCSS icon set. Use when creating, editing, or adding icons to the Cerb icon map (cerb-icons.scss / reference_icons.php), or designing mask-image SVG geometry in Cerb's style (line, filled-solid, compass, or punched-disc families).
---

# Cerb SVG Icons

Cerb icons live in an SCSS Sass map and render via CSS `mask-image`. **The icon's geometry determines opacity; the button's CSS text color provides the actual visible color.** Fill and stroke are both just "opaque" — there is no color contrast available. Every visual distinction must come from geometry: opaque shape vs transparent gap.

For the full design reference — common techniques, specific icon-by-icon notes, and style-anchor samples — see `references/icon-design.md`.

## Output format

Each icon is a single line in a Sass map:

```scss
  name:           "<inner-svg-geometry>",
```

Deliver ONLY the inner geometry — never the `<svg>` wrapper. Use **single quotes** on SVG attributes so the whole thing fits in the double-quoted Sass string.

## Outer template (applied automatically at render time)

```html
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'
     fill='none' stroke='black' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
  ...your inner geometry here...
</svg>
```

Your geometry inherits:
- 24×24 viewBox (everything must fit; stroke extends 1 unit past the path)
- `fill='none'` (override per-element with `fill='black'` to fill)
- `stroke='black' stroke-width='2'` (override per-element with `stroke='none'` to remove)
- `stroke-linecap='round'`, `stroke-linejoin='round'` — **sharp acute corners get rounded by ~1 unit**

## Workflow: where icons live & building

An icon isn't done until it's in **both** files (kept **alphabetized** in each) and the CSS is rebuilt:

1. **`install/extras/developers/css/cerb.css/layout/cerb-icons.scss`** — add the geometry to the `$icons` Sass map (this is the actual icon).
2. **`features/cerberusweb.core/api/uri/config/reference_icons.php`** — add the icon's **name** to the `getCerbIcons()` array (drives the Setup → Developers → Icons preview page).
3. Run **`composer build-css`** at the repo root. It compiles the SCSS into the live `features/cerberusweb.core/resources/css/cerb.css`; each icon becomes the class `.cerb-icon-<name>`.

**SCSS alignment convention:** 2-space indent, then `name:` padded with spaces so the opening value quote lands at a fixed column (~column 21). Names longer than that column (e.g. `circle-question-mark:`) just get a single space before the quote.

The `$icons` map + `getCerbIcons()` are the **source of truth for which icons exist**. This skill carries representative samples for *style*, not the full inventory — read those two files for the current list.

## The four pattern families

Pick a family up front and design within its constraints. Combining families in one icon usually fails because of the mask-image color limitation.

**1. Line icon (Lucide style, default).** `<path>`, `<rect>`, `<circle>`, `<line>`, `<polyline>`, `<polygon>` with no extra attributes — they inherit `fill='none'`, `stroke='black' stroke-width='2'`. Covers the vast majority of icons.
```scss
  mail:           "<rect x='2' y='4' width='20' height='16' rx='2'/><path d='m22 7-10 6L2 7'/>",
```

**2. Filled solid icon.** Add `fill='black'`. Add `stroke='none'` for crisp edges / sharp corners (small triangles, chevrons, arrow tips, pixel-precise cutouts); keep the template stroke when you want visual weight matching line icons.
```scss
  chevron-down:   "<path fill='black' stroke='none' d='M12 15.5l-7-7 2-2 5 5 5-5 2 2z'/>",
```

**3. Compass / ring-with-inner-element.** Outlined ring + filled inner element(s).
```scss
  play-button:    "<circle cx='12' cy='12' r='10'/><polygon fill='black' points='7.5 6 17.5 12 7.5 18'/>",
```

**4. Filled disc with a punched symbol (the `circle-*` family).** Filled r=10 disc centered at (12,12), symbol cut out via `fill-rule='evenodd'` + `stroke='none'`. The symbol MUST be a single continuous closed polygon (or non-overlapping subpaths) — overlapping subpaths push the winding count odd and re-fill the cutout. See `references/icon-design.md` for the winding math and traced polygons.
```scss
  circle-plus:    "<path stroke='none' fill='black' fill-rule='evenodd' d='M2 12A10 10 0 1 0 22 12A10 10 0 1 0 2 12ZM10.5 6 13.5 6 13.5 10.5 18 10.5 18 13.5 13.5 13.5 13.5 18 10.5 18 10.5 13.5 6 13.5 6 10.5 10.5 10.5Z'/>",
```

## Critical mask-image constraints

Non-negotiable consequences of `mask-image` rendering:

1. **No fill/stroke color contrast.** Both are opaque. Traditional outlining isn't possible — only geometric outline tricks (negative-space halo via evenodd, or a hollow stroked shape with no fill).
2. **Filled shape + stroke = bigger filled shape.** The 2px stroke adds ~1 unit of opacity in every direction. Inset a polygon by 1 unit to keep its visible size when it carries the template stroke.
3. **A transparent gap is required to "outline" anything.** Shape B is only visible against filled shape A if B is outside A, a cutout in A (evenodd), or both.
4. **`stroke-linejoin='round'` rounds every sharp corner by ~1 unit.** Use `stroke='none'` for true sharp corners.
5. **ViewBox edges clip.** A path at x=24 with a 2px stroke renders to x=25 and gets clipped. Pull paths in by 1 unit to preserve perimeter stroke. (The `circle-*` family can use a full r=10 disc only because it uses `stroke='none'`.)
6. **Masks can't occlude — no "in front / behind".** Overlapping shapes merge into one blob. Fanned decks, stacked cards, "one shape behind another" do NOT work — use distinct, spatially-separated elements.
7. **Stroke eats the gap between elements.** Each stroked shape extends half its `stroke-width` toward its neighbor. Budget ~4 geometric units of gap for ~2.5 visual units when spacing composites.
8. **SVG `transform` renders fine in the mask** (e.g. `transform='rotate(angle cx cy)'`) — but re-read #6 before overlapping.

## Working approach

1. **Start from Lucide.** Most icons map to an existing Lucide design — adapt rather than invent. Lucide path data drops in cleanly after converting double quotes to single quotes.
2. **Pick a pattern family up front** and design within its constraints.
3. **For complex evenodd paths, sanity-check winding at the center** — for a disc + symbol, the symbol center must be winding 2 (transparent).
4. **Parallelize independent icons via agents** when the user asks for several at once. Give each agent this format spec, the relevant reference samples, and warnings about the evenodd gotcha.
5. **Iterate on dimensions, not approach.** "Fatter / thinner / shorter / deeper" → adjust existing parameters. "Different style entirely" → switch pattern family.
6. **Round to 2 decimals max** unless precision matters (e.g. cutout sagitta math).
