# CerbUI chart family (successor to c3.js / d3.js / the legacy canvas plugin)

All charting is now in-house SVG, no external lib. **c3.js, d3.v5/v7, topojson, and
`jquery.devblocksCharts.js` are deleted.** Components live in `features/cerberusweb.core/resources/js/cerb-ui/`,
styles in `install/extras/developers/css/cerb.css/layout/cerb-ui/_chart.scss` (build with `composer build-css`),
JS bundled by `composer build-js` into `cerb-ui.js` (registered in the `build-js` terser list + the dev loader
`templates/cerb_ui_scripts.tpl` — **2 spots per new component**). Live examples = the UI Reference gallery
(`configuration/section/developers/ui_reference/components/*.tpl`), not this doc.

## Components

`CartesianChart`, `PieChart`, `ScatterChart`, `Gauge`, **and `Sparkchart`** all `extend CerbUI.Chart`.
**`Timeblocks` is the lone standalone class** (no `extends`) — which is why it loads *before* `chart.js` in
both build lists, while every subclass must load *after* it.

| Component | File | Use |
|---|---|---|
| `CerbUI.Chart` | `chart.js` | **base class** — lifecycle (`_instances`/`from`/`destroy`), palette+`ColorScale`+`_color(i,item)` (keyed `item.key ?? item.label`), lazy shared point-mode tooltip (`CerbUI.Chart._sharedTooltip`, one across ALL subclasses), `cerb-ui-chart:{hover,leave,click}` events (`_emit`), `_search(context,query)` drill-through, ResizeObserver, and **it creates the `<svg>` itself**. **Subclasses call `render()` at the END of their ctor; the base does NOT** (avoids base-renders-before-subclass-parsed) |
| `CerbUI.CartesianChart` | `cartesian-chart.js` | bar/line/spline/area over a **band (category)** OR **continuous (time/linear)** x-axis. `orientation` vertical\|horizontal only swaps screen placement. Per-series `type`, `axis:'y'\|'y2'`, `stack` (mark-agnostic — stacked bars AND lines/areas), unstacked bars **dodge**. Grouped tooltip (`tooltip.sum`/`ratios`), `_search` drill, y2, gridlines. **ONE shared value scale** (or two w/ y2) |
| `CerbUI.PieChart` | `piechart.js` | pie/donut; slices `[{label,value,text?,color?,click?}]`; ratio tooltip; component-owned legend sharing one `ColorScale`; full-circle guard (single 100% slice = evenodd ring, since an `A` arc can't draw start==end) |
| `CerbUI.ScatterChart` | `scatter-chart.js` | XY point clouds — its OWN class (each series is independent (x,y), not the shared-x model). Two linear axes, 5%-padded domains, nearest-point-within-40px tooltip, `axesIndependent` (per-series scales) |
| `CerbUI.Gauge` | `gauge.js` | single-value radial; `[min,max]`→arc; `thresholds:[{value,color}]` recolor the fill (highest crossed wins); `valueText`; optional `minLabel`/`maxLabel` end labels; `arc` deg (270 default, 180=semicircle) |
| `CerbUI.Sparkchart` | `sparkchart.js` | compact, categorical, axis-less multi-series (bar+line) — worklist sparkline columns, scheduler dashboard. **Independent per-series scaling** (each bar 0→own-max, each line own-min→max, `scaleGroup` nests min/avg/max bands) and renders backend-**preformatted `text[]`** (never formats). Stretches (`preserveAspectRatio:none`), baseline ticks + caption extents. Keeps its bespoke `render()`; inherits only the base plumbing. Data contract locked by `DAO_MetricValue::getSparklines()` (12+ worklists) — **do not touch** `{categories, series:[{type,label,color,stack,scaleGroup,values,text}]}`. Events stay `cerb-ui-sparkchart:*` (not the base `_emit` namespace) |
| `CerbUI.Timeblocks` | `timeblocks.js` | GitHub-style day×hour heatmap `[{date,value}]`; 12-step bg→green ramp. **Standalone** (not a `CerbUI.Chart` subclass) |

Shared foundation (functional helpers, not classes):
- `chart-core.js` — `CerbUI.scale.linear/band/time` (band has `.center()`), `CerbUI.ticks.linear` (d3 tickIncrement: **√-based 1/2/5 step boundaries, NOT integer**).
- `CerbUI.num.format(pattern)` (subset of d3-format: `,`/`.Nf`/`.N%`), `num.percent`, `num.duration(value,unit)` (shortEn largest-2, ported off humanize-duration.js), `num.compact`.
- `CerbUI.date.strftime(pattern)` (subset `%Y%y%m%d%e%H%M%S%I%p%a%A%b%B`, hardcoded en-US names, replaces `d3.timeFormat`). Honors the GNU **`-` no-pad flag** (`%-I`→`3`, `%-d`, `%-m`, `%-H`…) — the token regex is `/%(-?)([…])/`; without the `-` handling `%-I` leaked as literal `%-I`. **Unknown tokens (`%Q`, `%j`, `%L`) intentionally render verbatim** so an unsupported pattern is visible, not silently dropped. Drives BOTH axis ticks and tooltips (one shared formatter).
- `palettes.js` — `CerbUI.resolvePalette`, `ColorScale`/`colorScale` (ordinal, stable per key — share ONE across a chart+legend so colors match).

## The chart-KATA engine (`type:cerb.workspace.widget.chart.kata` + the `await:…:chart` interaction)

Server: `libs/devblocks/api/services/chart.php` `_DevblocksChartService::parse($chart_kata, $datasets_kata,
$chart_options, &$error)` keeps ALL its input parsing (x-normalization, stacking, color/dark-mode) building a
**c3-shaped intermediate**, then `_toChartConfig()` transforms it into the **CerbUI config that is the public
return** (c3 never leaves chart.php — this is a server re-target, NOT a client adapter):
```
{ kind:'cartesian'|'pie'|'gauge'|'scatter', height, palette,
  x:{scale,categories?|values?,label?,format?,rotate?}, y:{label?,format?,grid}, y2?,
  series:[{key,name,type,axis,stack?,color,values,x?,click?}],  // pie→slices[]; gauge→value/min/max
  legend:{show,style:'compact'|'table',stats?,data?}, tooltip:{show,grouped,ratios} }
```
- **`format`** = the `{as:'date'|'number'|'duration', params}` descriptor (already CerbUI-friendly; client resolves).
- Per-series `dataset__key` join id maps c3 `types/axes/colors/names/groups/click_search` → `series[]`.
- **pie/donut have NO `x` column** — each dataset key IS a slice (label = series name, value = column total). Handle both: `x` present → zip(labels, values); absent → each column = a slice.
- The KATA **dialect (input) is unchanged** — no user migration.

Client: ALL 5 render sites (3 widget hosts `api/{cards,profiles,workspaces}/widgets/chart_kata.php`, the config
preview `Charts/ChartKataWidgetTester::previewChart`, and `Awaits/ChartAwait.php` which `{include}`s it) share ONE
template `internal/chart_kata/render.tpl`, contract = `chart_json` (required) + optional `chart_id`. It: resolves
formatters (`fmtFor` for values, **`xFmtFor` for the x-axis** — category → NO formatter), instantiates by `kind`,
renders `legend:false` on the component + a **custom jQuery stats-table legend** (per-series total + per-x data
grid + sum/avg/min/max/count + y2 split + drill) for `style:'table'` (compact uses the component's built-in).
Workspace CSV/JSON export reconstructs rows from `series[]` via `_configToColumns`.

## GOTCHAs (each cost a debug cycle — all durable)

1. **SVG `fill: var(--cerb-color-background-contrast-140)` renders BLACK.** The grayscale ramp is defined only in
   steps of 10 **starting at 150** — 140 is undefined → the `var()` is invalid → SVG text `fill` falls back to the
   initial **black** (unlike CSS `color:`, which inherits). **Use ≥150 for any SVG `fill`**, or `--cerb-color-text`.
2. **A category axis must NOT run labels through a number formatter** — `Number("Demo")` → `NaN`. The x-axis
   formatter defaults to a value formatter, which is wrong for string category labels. Gate it by scale: category
   → `null` (raw labels), time → date, linear → number. (Bit the chart-KATA renderer; the fixed widgets already
   returned `null` for no-format.)
3. **`render()` stacks event listeners** — the `<svg>` is created ONCE (base ctor) and reused, but `_bindEvents`/
   `_bindSlices` run every `render()`. `ResizeObserver` fires an initial render right after the ctor's render →
   **two click handlers → the drill-through popup opens twice** (more on each resize). **Bind must remove the
   prior handlers before re-adding** (store refs on `this`, `removeEventListener` first). Applies to Cartesian/
   Scatter/Pie (all bind in render); Timeblocks/Sparkchart bind once in the ctor and are immune.
4. **Point-mode `CerbUI.Tooltip` lingers on scroll** — it's `position:fixed` at the cursor's viewport coords and
   only repositions on mousemove. `show()` now registers a **capture-phase `scroll` listener that hides it**
   (fresh hover re-shows); `hide()` unregisters. Fixes charts, sparkchart, timeblocks at once.
5. **Rotated axis labels overflow onto whatever's below** (the legend, the axis title). The svg is
   `overflow:visible`, so a rotated `-90°` date/duration label (~110px) escapes a fixed bottom margin. **Size the
   bottom margin from the longest tick label** (`min(cap, 24 + maxChars*6.2)`, + extra for an axis label),
   computed from the axis DOMAIN before the pixel scales. Done in both CartesianChart + ScatterChart.
6. **A component legend must color its swatch from the chart's own `_seriesColor`**, not `CerbUI.Legend`'s
   scale-by-order — else an explicit-colored series (metrics explorer sets per-series colors) shows a mismatched
   swatch, and hiding a series reshuffles the scale ("blue = Sum"). After `new CerbUI.Legend(...)`, overwrite each
   swatch's `backgroundColor = _seriesColor(si, series[si])`.
7. **Smarty brace-parsing eats chart JS.** Dense object-literal chart code (`{key:1}`) is misread as a Smarty tag.
   Either put a space after every `{` (`{ key: 1 }`) or — cleaner for big blocks — **inject the Smarty values
   first (`var CERB_CHART_CONFIG = {$chart_json nofilter};`) then wrap the rest in `{literal}`**. See
   `chart_kata/render.tpl`.
8. **Sparse bars on a CONTINUOUS (time/linear) axis need TWO guards, or they render as giant edge-pinned bars.**
   The chart is handed only the points it's given (e.g. subtotals returns 2 populated months, not a gap-filled
   year) — that's correct, don't invent a timeline. But `CartesianChart` (a) sized each bar to the full
   inter-point gap (`_minGap`) → huge/clipped bars, and (b) fit the domain to `[min,max]` with a flat 3% pad →
   `min` pinned hard-left, `max` hard-right, giant void between. Fixes in `cartesian-chart.js`: **cap bars at 64px
   centered on the point** (`_drawBar`: `groupW = min(_fullBandwidth(), 64/0.86 * _barCols)`); and **when the
   chart has any bar series, pad the continuous domain by HALF a data-step each side** (`[lo-step/2, hi+step/2]`,
   `range` unpadded) so edge buckets sit inside with room for a full bar — two consecutive months land at ~25%/75%.
   Line/area series keep the 3% proportional pad (they *should* span edge-to-edge; half-step padding is a bar
   convention only). A BAND (category) axis is immune — it already slots evenly.
9. **Reparenting a standalone chart onto `CerbUI.Chart` — the friction checklist.** Sparkchart was reparented
   (`class extends CerbUI.Chart`) to delete ~50 lines of re-inlined plumbing (`_instances`/`from`, palette/scale,
   `NS`, `<svg>` creation, ResizeObserver, `_color`, `_tooltip`). What bites: **(a) load order** — a subclass must
   load AFTER `chart.js` in BOTH `composer.json` build-js and `cerb_ui_scripts.tpl` (else `extends` sees an
   undefined base at eval time); move it, don't just add it. **(b)** The base sets `preserveAspectRatio:'xMidYMid
   meet'`, `<svg>` class `cerb-ui-chart--plot`, and `height:320` — re-assert your own (`none` / `cerb-ui-<x>--plot`
   / your default) AFTER `super()`. **(c)** The base creates the svg; drop your own creation (base appends it before
   your ctor's post-super code, so a caption appended after still lands below). **(d)** `render()` must still size
   the svg (base sets no width/height/viewBox). **(e)** Keep a `destroy()` OVERRIDE if you bind listeners on
   `this.el` (base's `destroy` only knows the svg/RO/tooltip): remove them, then `super.destroy()`. **(f)** `from()`
   is inherited and reads the SHARED `CerbUI.Chart._instances`, so `CerbUI.Sub.from(el)` works — fine since no two
   chart types share an el. **(g)** To preserve a documented event namespace (`cerb-ui-sparkchart:*`), keep your own
   `dispatchEvent`, do NOT switch to the base `_emit` (which hardcodes `cerb-ui-chart:`). CSS needs no change if the
   base `.cerb-ui-chart`/`--plot` rules match yours (both `display:block; width:100%; overflow:visible`) and your
   element classes are flat BEM set by JS.

## Extending
- **New mark type** (area/step/spline/scatter marks): add a `_drawX` renderer + a case in CartesianChart's
  per-series `type` dispatch; stacking is free (consumes `_base/_top`).
- **New chart kind** in chart-KATA: extend `_toChartConfig`'s `kind` switch (PHP) + the `render.tpl` `if(kind…)`.
- **New format pattern**: grow the `CerbUI.num.format` subset or `date.strftime` tokens (port only what's used).

## Testing — headless DOM-stub harness
Each chart has a Node pure-logic test (see the scratchpad `test-{cartesian,piechart,scatter,gauge,timeseries,
timeblocks,spark}.js` pattern): stub a minimal `document.createElementNS`/`createElement` (FakeNode with `attrs`,
`children`, `dataset`, `style`, `classList`, `append`), `global.window={}` (so the base skips ResizeObserver),
`CustomEvent`, `CerbUI={}` + `valueAttr`/`textAttr`, then `eval` the component sources in dependency order and
assert geometry/scales/colors/listener-count from the built SVG tree. No browser needed; catches the math + the
listener-stacking regression (#3). PHP `chart.php` can't be headless-tested standalone (needs the platform
bootstrap) — verify it live.
