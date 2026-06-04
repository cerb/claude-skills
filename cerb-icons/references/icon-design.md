# Cerb SVG Icon Design Reference

Deep reference for designing Cerb SCSS icons. Read `../SKILL.md` first for the output format, outer template, build workflow, the four pattern families, and the critical mask-image constraints. This file covers the punched-disc family in depth, common techniques, icon-by-icon notes, and style-anchor samples.

## The punched-disc family (`circle-*`) in depth

Filled circle of radius 10 centered at (12, 12), with a transparent symbol cut out via `fill-rule='evenodd'` and `stroke='none'`.

```scss
  circle-plus:    "<path stroke='none' fill='black' fill-rule='evenodd' d='M2 12A10 10 0 1 0 22 12A10 10 0 1 0 2 12ZM10.5 6 13.5 6 13.5 10.5 18 10.5 18 13.5 13.5 13.5 13.5 18 10.5 18 10.5 13.5 6 13.5 6 10.5 10.5 10.5Z'/>",
```

Structure:
1. Disc subpath: `M2 12A10 10 0 1 0 22 12A10 10 0 1 0 2 12Z` (two semicircle arcs).
2. Symbol subpath: a **single continuous closed polygon** traced around the entire cutout shape.

**The critical gotcha:** if the cutout symbol is built from multiple overlapping subpaths (e.g. a "+" as a horizontal rectangle + a vertical rectangle), the overlap region gets winding count 3 (1 from disc + 1 from horizontal + 1 from vertical), which is odd → **re-fills opaque at the center, ruining the cutout**. Trace plus, X, check, etc. as ONE continuous closed polygon so the winding inside stays at 2 (even = transparent).

**Plus (12-vertex cross polygon):**
```
M10.5 6 13.5 6 13.5 10.5 18 10.5 18 13.5 13.5 13.5 13.5 18 10.5 18 10.5 13.5 6 13.5 6 10.5 10.5 10.5Z
```
Trace around the perimeter: top-left of vertical → top-right of vertical → right-top of horizontal → right-bottom of horizontal → bottom-right of vertical → bottom-left of vertical → left-bottom of horizontal → left-top of horizontal → close.

**X (12-vertex octagonal polygon):**
```
M8.29 9.71 10.59 12 8.29 14.29 9.71 15.71 12 13.41 14.29 15.71 15.71 14.29 13.41 12 15.71 9.71 14.29 8.29 12 10.59 9.71 8.29Z
```
Outer corner of arm → inner notch → outer corner of next arm → … around all 4 arms.

**Check (6-vertex L-shaped stripe polygon):** for a V apex at (10.5, 15) with arms to (7.5, 12) and (16.5, 9), stripe width 3:
```
M6.44 13.06 10.5 17.12 17.56 10.06 15.44 7.94 10.5 12.88 8.56 10.94Z
```
Outer tail-left → outer V apex → outer tail-right → inner tail-right → inner V apex → inner tail-left → close.

**Sizing the cutouts to match each other:** at 1.5× scale (the current set), all cutouts use stripe width 3 and span ~12 units across, so disc + cutout reads as a consistent family. The check's stripe is sized differently from X/+ because the V's outer/inner corners derive from the sagitta of the V angle (90° apex → sagitta = stripe_width / sin(45°) = 1.5 / 0.707 = 2.12), not just an offset.

**Simple symbols cut cleanly; curvy glyphs don't.** A single continuous polygon works for `+`, `−`, `×`, the check, `!` (a tapered bar + a separate dot), and `i` (a dot + a stem). Separate **non-overlapping** subpaths are fine — the overlap-winding gotcha only bites *overlapping* subpaths. But a curvy glyph like `?` can't be cut by hand: a cutout can't hold both a bold-enough stroke and a visible interior counter at icon size — thick enough to read closes the counter; thin enough to show the counter looks broken.

**Fix for curvy glyphs — convert a stroked centerline to a filled outline.** Take a known-good stroked path (e.g. from Lucide) and offset it: a circular arc of centerline radius `r` and stroke width `w` becomes an **annular sector** — outer arc `r + w/2`, inner arc `r − w/2`, same center. The `circle-question-mark` bowl converted exactly this way from Lucide's stroked hook (centerline r=3, w=2 → outer 4, inner 2). Straight stroke segments offset `±w/2` perpendicular; curved tails need cubic-Bézier offsets.

**Crook/tangent rule when outlining a stroke:** where the outline turns (e.g. bowl → tail), leave the joint **tangent to the stroke's travel direction** — curve out (go down first, then sweep), don't cut a straight chord between the two offset points. A chord visibly kinks.

## Common techniques

### Compensating for stroke when sizing matters

To make a filled-with-stroke polygon match the visible dimensions of a filled-no-stroke polygon:
- **Inset the polygon by 1 unit** on every edge (perpendicular to each edge).
- The 1px outward stroke extension fills back to the original visible dimensions.

For sharp acute corners (arrow tips), the inset moves the vertex inward by more than 1 unit (factor `1/sin(angle/2)`), but the round-join stroke extends back by exactly 1 unit along the bisector — so corners end up slightly blunter than the geometry, but long edges hit their target exactly. This is what the `file-import`/`file-export` arrows do.

### Symmetry: rotate for directions, mirror for opposites

For 4-way directional icons (up/down/left/right), design ONE direction and rotate around the viewBox center (12, 12):
- **90° CCW visually (math CW with Y-down):** `(x, y) → (y, 24-x)`
- **180°:** `(x, y) → (24-x, 24-y)`
- **270° CCW (= 90° CW visually):** `(x, y) → (24-y, x)`

This guarantees identical geometry across all four orientations.

**Mirror for semantic opposites — build one, reflect the other:** vertical flip `(x, y) → (x, 24-y)`, horizontal `(x, y) → (24-x, y)`, point `(x, y) → (24-x, 24-y)`. Pairs built this way: `merge`↔`branch` (vertical flip), `cloud-download`↔`cloud-upload` (mirror about y=12), `resize-full`↔`resize-small`, `fast-forward`↔`fast-backward`, `sort-asc`↔`sort-desc`.

### Sharing base paths across a family

For file/folder families where multiple icons share a base shape (e.g. `file`, `file-import`, `file-export` all use the same page-with-folded-corner), put the shared paths first verbatim and append the variant-specific paths after:

```scss
  file:           "<path d='[page]'/><path d='[fold]'/>",
  file-import:    "<path d='[page]'/><path d='[fold]'/><polygon points='[arrow-in]'/>",
  file-export:    "<path d='[page]'/><path d='[fold]'/><polygon points='[arrow-out]'/>",
```

Confirm byte-for-byte identity of the base across variants.

### Optical centering for asymmetric shapes

A right-pointing triangle's geometric centroid is at the 1/3 mark from base to apex. Centered geometrically (centroid at x=12) makes the triangle LOOK left-shifted because the apex carries less visual mass than the broad base. **Push the geometric centroid slightly LEFT of true center** so it reads as visually centered. The play-button triangle uses centroid at x≈10.83 with apex at x=17.5.

### Arc path tricks

**Drawing a full circle as a path:** `M (cx-r) cy A r r 0 1 0 (cx+r) cy A r r 0 1 0 (cx-r) cy Z` — two semicircle arcs. Required when you need the circle as a subpath inside an evenodd compound path (circle elements can't be subpaths).

**SVG arc auto-scaling:** if you specify a radius smaller than chord/2, the renderer scales the radius UP to chord/2 (semicircle). Used in the moon to force a maximally curved inner arc: `A6 6 …` for a chord of ~15.6 produces a radius-7.78 semicircle.

**Sweep flag semantics:** sweep=1 = clockwise visually; sweep=0 = counterclockwise. For a crescent, outer and inner arcs need OPPOSITE sweep flags (curve in opposite directions across the chord). For a lens/eye shape, they use the SAME sweep flag.

### Fat polygon arrows

Build directional arrows as 7-vertex polygons going around the perimeter: tail-top, shaft-top-at-head, top-wing, tip, bottom-wing, shaft-bottom-at-head, tail-bottom. Dimensions:
```
length     = tip_x - tail_x
shaft      = inner_thickness
wing       = outer_span
head       = tip_x - shaft_head_x
shaft_len  = shaft_head_x - tail_x
```
Wing extension per side = `(wing - shaft) / 2`.

### Filled swooshes / curved arrows

Two parallel Bézier paths plus an arrowhead, closed into a single shape: `M[tail] Q[outer-curve] L[arrowhead-vertices] Q[inner-curve-back] Z`. The tail can be a single point (both Q curves share start/end) for a tapered comma-shape tail, or a flat edge (different start/end Y at the tail X) for a chunky tail.

### Composite icons (combine two icons)

Place two icons in **separate, non-overlapping regions** with a clear gap (mind constraint #7 — leave geometric room). Examples: `user-lock` (filled `user` left + outlined padlock lower-right), `disk-export`/`disk-save` (drive + arrow), `folder-plus` (`folder` + plus), `cloud-download`/`cloud-upload` (cloud + arrow). **Mixing fill styles is fine when the parts don't overlap** — a filled silhouette next to an outlined lock reads cleanly because they're spatially separate (they'd merge into a blob if overlapped — constraint #6).

### Reuse a cutout symbol as a standalone

The symbol polygon from a `circle-*` cutout works **verbatim** as a standalone filled icon: drop the disc subpath and keep the symbol with `fill='black' stroke='none'`. `remove` is the `circle-remove` X, `plus` is the `circle-plus` cross, `minus` is the `circle-minus` bar — same coordinates, no disc.

### Per-element stroke-width override

The wrapper sets `stroke-width='2'` globally. Override it on one element with `stroke-width='N'`, or wrap several in `<g stroke-width='N'>…</g>`. Used for `ban` (2.5), `search` (3), `bold` (4), the `file` family (1.5), the `more`/`more-vertical` dots (1.5), the `compass` inner rhombus (1), and filled-polygon arrows (1, so the fill barely puffs past the geometry).

### Tiny-segment dot trick

A near-zero-length segment with the inherited round linecap renders a filled dot of diameter = `stroke-width`: `M12 17h.01` (or `v.01`). Cheaper than a `<circle>` for `!`/`i` dots and signal dots (`alert`, `wifi`).

### Filled control / media family

`play` (triangle), `pause` (two bars), `stop` (square), and the `step-*` / `fast-*` controls (triangles + bars) all use `fill='black' stroke='none'` so their solid weight matches across the playback row. Pair opposites by mirroring.

## Specific icon-by-icon notes

### Crescent moon (`mode-dark`)

```scss
  mode-dark:      "<path fill='black' stroke='none' d='M21 14A9 9 0 1 1 10 3 6 6 0 0 0 21 14z'/>",
```

Two arcs sharing endpoints (21, 14) and (10, 3). Outer arc r=9, large=1, sweep=1. Inner arc r=6 (auto-scales to ~7.78, the chord-bisector min, producing a semicircle bite). The chord stretches diagonally to make the bite as deep as possible — Lucide's default uses closer endpoints, keeping the inner arc less curved.

- Thinner crescent: stretch endpoints further apart (limited by viewBox).
- Sharper horns: increase inner radius past the autoscale min (e.g. `8 8`), but this also widens the crescent because the bite gets shallower.
- Remove stroke-join rounding at horns: add `stroke='none'` (already present).

### Gear (`gear`)

Filled body + cutout center hole. Trapezoidal teeth at compass positions (every 45°).

| dimension | value |
|---|---|
| outer tooth tip radius | 10 |
| body / tooth base radius | 8 |
| gap floor radius | 7.5 (U depth 0.5) |
| center hole radius | 5.5 |
| tooth angular half-width | 7.5° (tooth = 15° wide, gap = 30°) |
| tooth tip corner fillet | 0.5 (via Q with sharp corner as control point) |

Pattern per tooth+gap: (1) up the radial side (L), (2) rounded `Q` corner at outer-left, (3) across tooth top (L), (4) rounded `Q` corner at outer-right, (5) down the radial side (L) to body, (6) straight radial into gap floor (L), (7) arc along R_floor to next tooth (A), (8) straight radial out to next tooth (L).

### Fat directional arrows

Identical geometry rotated 90° per direction. Current "short/fat" proportions:

| dimension | value |
|---|---|
| total length | 14 |
| shaft thickness | 6 |
| wing span | 12 |
| head length | 7 |
| shaft length | 7 |

Tail and tip each 5 units from their viewBox edge.

### File-family arrows

7-vertex polygon arrows passing through the file boundary. **Use the template stroke** (no `stroke='none'`) for visible outline weight. **Inset the polygon by 1 unit** on every edge so the 2px stroke brings visible dimensions back to target. Both `file-import` and `file-export` use identical polygon dimensions (mirror images around x=12).

### Share swoosh

Closed Bézier path forming a tapered comma shape: starts at a single point (tail), curves up and right with a sharp upward initial tangent, ends in a wide arrowhead. Single point at the tail (both outer and inner Q curves share that start/end) gives a clean tapered tail.

## Reference samples (style anchors)

A hand-picked sample per pattern family and technique — the concrete style anchor for new icons. Each entry is **inner geometry only**; it renders inside the wrapper from the **Outer template** in `../SKILL.md`. For the full, current inventory, read the source files (`cerb-icons.scss` and `reference_icons.php`) — they are the source of truth for *which* icons exist.

```scss
// Line icon (inherits fill:none, stroke 2). stroke-width override via <g>.
  mail:             "<rect x='2' y='4' width='20' height='16' rx='2'/><path d='m22 7-10 6L2 7'/>",
  search:           "<g stroke-width='3'><circle cx='11' cy='11' r='6'/><path d='m21 21-4.35-4.35'/></g>",

// Filled solid (fill='black' stroke='none' for crisp edges / sharp corners)
  chevron-down:     "<path fill='black' stroke='none' d='M12 15.5l-7-7 2-2 5 5 5-5 2 2z'/>",
  play:             "<polygon fill='black' points='7 5 19 12 7 19'/>",

// Compass / ring with a filled inner element
  compass:          "<circle cx='12' cy='12' r='10'/><polygon stroke-width='1' points='16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88'/><circle fill='black' stroke='none' cx='12' cy='12' r='1.5'/>",

// Cutout disc: filled r=10 disc, symbol punched via evenodd, stroke='none'
  circle-plus:      "<path stroke='none' fill='black' fill-rule='evenodd' d='M2 12A10 10 0 1 0 22 12A10 10 0 1 0 2 12ZM10.5 6 13.5 6 13.5 10.5 18 10.5 18 13.5 13.5 13.5 13.5 18 10.5 18 10.5 13.5 6 13.5 6 10.5 10.5 10.5Z'/>",
  circle-exclamation-mark: "<path stroke='none' fill='black' fill-rule='evenodd' d='M2 12A10 10 0 1 0 22 12A10 10 0 1 0 2 12ZM10.5 6 13.5 6 13 13.5 11 13.5ZM10.5 17.5A1.5 1.5 0 1 0 13.5 17.5A1.5 1.5 0 1 0 10.5 17.5Z'/>",

// Cutout of a CURVY glyph: stroked centerline → annular-sector outline
  circle-question-mark: "<path stroke='none' fill='black' fill-rule='evenodd' d='M2 12A10 10 0 1 0 22 12A10 10 0 1 0 2 12ZM8.15 8.67A4 4 0 0 1 15.92 10C15.92 12 13.5 13.7 12.24 13.95A1 1 0 0 1 11.6 12.05C12.5 12 13.8 11 13.92 10A2 2 0 0 0 10.03 9.33ZM10.7 17A1.3 1.3 0 1 0 13.3 17A1.3 1.3 0 1 0 10.7 17Z'/>",

// Standalone reuse of a cutout symbol (drop the disc subpath)
  remove:           "<path fill='black' stroke='none' d='M6.44 8.56 9.88 12 6.44 15.44 8.56 17.56 12 14.12 15.44 17.56 17.56 15.44 14.12 12 17.56 8.56 15.44 6.44 12 9.88 8.56 6.44Z'/>",

// Composite (two icons, separate regions, mixed fill is OK when not overlapping)
  user-lock:        "<circle fill='black' stroke='none' cx='6.5' cy='7' r='3.5'/><path fill='black' stroke='none' d='M2 21v-5a4.5 4.5 0 0 1 9 0v5z'/><rect x='14' y='15' width='7' height='6' rx='1'/><path d='M15.5 15v-2a2 2 0 0 1 4 0v2'/>",

// Mirror pair (build one, reflect for the opposite — here a vertical flip)
  merge:            "<path d='M8 9V15'/><path d='M8 10 13 13 15 13'/><rect x='5' y='3' width='6' height='6' rx='2'/><rect x='5' y='15' width='6' height='6' rx='2'/><rect x='15' y='10' width='6' height='6' rx='2'/>",
  branch:           "<path d='M8 9V15'/><path d='M8 14 13 11 15 11'/><rect x='5' y='3' width='6' height='6' rx='2'/><rect x='5' y='15' width='6' height='6' rx='2'/><rect x='15' y='8' width='6' height='6' rx='2'/>",

// Per-element stroke-width + the tiny-segment dot trick (M..h.01)
  ban:              "<g stroke-width='2.5'><circle cx='12' cy='12' r='10'/><line x1='4.93' y1='4.93' x2='19.07' y2='19.07'/></g>",
  alert:            "<path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3'/><path d='M12 9v4'/><path d='M12 17h.01'/>",
```
