# Adding an inline sparkline column to a worklist

A reusable, async, multi-series sparkline column ("Activity"/"Trend") for any record type that has metric
data. One `metrics.timeseries` query per page (no N+1); the worklist paints first, charts fill in. Built on
the shared helper + frontend loader — each new worklist is ~5 small edits.

## Shared pieces (already exist — don't re-create)

- **Backend:** `DAO_MetricValue::getSparklines($row_series, $window, $tz)` in
  `features/cerberusweb.core/api/dao/metric_value.php`. One query for all rows; returns
  `[rowId => ['categories'=>[...], 'series'=>[ ['type','label','values','text'], ... ]]]`.
- **Header partial:** `templates/internal/views/view_header_sparkline.tpl` — the `<th>` label + the window
  switcher, shared by every worklist. Presets (currently **2h / 1d / 30d**) live here only — change them
  once. Params: `header`, `view_fields`.
- **Frontend:** `templates/internal/views/sparkline_loader.tpl` — the switcher loader + async fetch +
  render (destroy-then-redraw, request-generation guard, localStorage window). Params: `spark_module`,
  `spark_action`, `spark_view_id`. Persists the chosen window in `localStorage` (`cerb.spark.*`), default
  `1d`.
- **Window map:** `DAO_MetricValue::getSparklines()`'s `$windows` array is the single window-key →
  `[period, range]` source: `2h`→`minute` (5-min bins, near-real-time), `1d`→`hour`, `1w`→`day`,
  `1mo`→`day`, plus legacy `24h`/`7d`/`30d` aliases (the scheduler dashboard still uses the old keys).
- **Component:** `CerbUI.Sparkchart` (`resources/js/cerb-ui/sparkchart.js`) — bars are 0-based (bars sharing
  a `stack` key stack + share one 0→max scale), lines range over their own min→max (or a shared `scaleGroup`);
  later series render in front. `CerbUI.colorScale()` colors by series **order** (1st = category10 blue,
  2nd = orange), shared per worklist via the loader.

## The series spec (what each endpoint builds)

`$row_series = [rowId => [ spec, ... ]]`, each `spec`:
```php
[
  'metric'   => 'cerb.automation.invocations', // metric name (required)
  'function' => 'count',                        // count|sum|avg|min|max|faceted_average|faceted_min|faceted_max
  'type'     => 'bar',                          // 'bar' (magnitude, behind) | 'line' (measure, in front)
  'label'    => 'runs',                         // shown in tooltip when >1 series; also the color key
  'query'    => ['automation_id' => $rowId],    // optional metric-dimension filter
  'stack'    => 'msgs',                          // bars sharing a key stack + share one 0→max scale
  'missing'  => 'zero',                          // counters: 'zero'; gauges: usually 'zero' too (see below)
  'suffix'   => 'ms',                            // optional text suffix (e.g. durations)
]
```
**Conventions:** counter → `count` + `missing:zero`. **Gauge** = point-in-time snapshot sampled sparsely by
a cron, so choose the aggregate by intent: `faceted_max` for a depth/backlog ("did it back up this bin?"),
`faceted_average` for an average level. The `faceted_*` functions sum each facet's per-bin aggregate
(`SUM(max)`, `SUM(sum/samples)`, …) so a multi-facet metric reads as a total. Prefer `missing:zero` over
`carry` for a gauge — see the gauge gotcha. For a runs+duration pair use **invocations bar first (blue),
duration line second (orange, ms)** — matches the scheduler.

**Two shapes:**
- *Row IS the metric* (Metric worklist): one spec, `metric` = the row's name, no `query`.
- *Fixed metric, filtered by dimension* (Automation = `automation_id`, Automation Event = `trigger`):
  one+ specs with `query => [dimension => rowId-or-value]`.

## Per-worklist checklist

1. **SearchFields_X** (`api/dao/<type>.php`): add the virtual field — `db_table='*'`, **empty db_column**
   (suppresses the sort link), label, the `TYPE_VIRTUAL_SPARKLINES` type (drives the chart-line/purple
   tile in the customize-view column picker), not sortable.
   ```php
   const VIRTUAL_SPARKLINE = '*_sparkline';
   // in _getFields():
   self::VIRTUAL_SPARKLINE => new DevblocksSearchField(self::VIRTUAL_SPARKLINE, '*', '', 'Activity', DevblocksSearchCriteria::TYPE_VIRTUAL_SPARKLINES, false),
   ```
2. **View_X constructor:** add `SearchFields_X::VIRTUAL_SPARKLINE` to `$this->view_columns` (default-on).
3. **view.tpl** (find the real path — some are `records/types/<type>/view.tpl`, others
   `internal/<type>/view.tpl`; `View_X::render()` assigns `view_template`):
   - Header `{foreach view_columns}`: special-case the column → include the shared header partial (label +
     switcher). One line; the presets live in the partial, not here:
     ```smarty
     {if $header == "*_sparkline"}
       {include file="devblocks:cerberusweb.core::internal/views/view_header_sparkline.tpl" header=$header view_fields=$view_fields}
     {else} ...existing header... {/if}
     ```
   - Body `{foreach view_columns}`: add `{elseif $column == "*_sparkline"}` →
     `<td data-column="{$column}" style="width:160px;"><div class="cerb-ui-sparkchart" data-cerb-spark="{$result.<pk>}" style="min-width:140px;"></div></td>`
   - Inside the bottom `<script nonce>` `$(function(){ ... })`, gated by the column:
     ```smarty
     {if in_array('*_sparkline', $view->view_columns)}
     {include file="devblocks:cerberusweb.core::internal/views/sparkline_loader.tpl" spark_module='<type>' spark_action='viewSparklinesJson' spark_view_id=$view->id}
     {/if}
     ```
4. **Profile controller** (`api/uri/profiles/<type>.php`): add a `profileAction` case + method that builds
   `$row_series` and returns JSON (mirror `_profileAction_viewSparklinesJson` in `metric.php`/`automation.php`):
   ```php
   DevblocksPlatform::services()->http()->setHeader('Content-Type', 'application/json; charset=utf-8');
   $ids = array_filter(array_map('intval', DevblocksPlatform::importGPC($_REQUEST['ids'] ?? [], 'array', [])));
   $window = DevblocksPlatform::importGPC($_REQUEST['window'] ?? '1d', 'string', '1d'); // 2h|1d|1w|1mo (+legacy 24h/7d/30d)
   $row_series = [];
   if($active_worker && $ids) foreach($ids as $id) { $row_series[$id] = [ /* specs */ ]; }
   $out = $row_series ? DAO_MetricValue::getSparklines($row_series, $window, $active_worker->timezone ?: null) : [];
   echo json_encode((object) $out); // (object) => always {} when empty
   ```
5. **Migration** (current patch, e.g. `patches/11.x/11.2.0.php`): add the view class to the reset so saved
   worklists reload with the new default column — `DELETE FROM worker_view_model WHERE class_name IN
   ('View_Metric','View_Automation', ...)` guarded by `if($revision < N)`. Dev: re-test by decrementing
   `cerb_patch_history.revision` (see `rerun-patch.md`).

## Gotchas (all hit during the metric/automation builds)

- **Virtual column is SQL-safe:** worklist `getSearchQueryComponents` SELECTs fixed columns, so a `*`-table
  column in `view_columns` never touches SQL. `getColumnsAvailable()` includes it (shows in Customize);
  the picker needs only a token + db_label, not a db_column.
- **No `gmdate`, no hand-rolled binning** — the `metrics.timeseries` query does lerp/timezone/gap-fill. See
  `metrics.md` and the auto-period idea in the metrics-quicksearch roadmap.
- **Smarty brace trap:** a `{` + non-space in a JS comment (e.g. `{type:...}`) compiles as a tag. The shared
  loader is pure JS (no `{literal}` needed) because it avoids them — keep new JS comments brace-free.
- **Build:** edited `sparkchart.js`/`menu.js` etc. need `composer build-js`; SCSS needs `composer build-css`;
  then `composer cache-clear`. Dev mode loads the raw component files; prod uses the bundle.
- **Duration metric is milliseconds** (`increment('cerb.automation.duration', $elapsed_ms, ...)`) → `suffix:'ms'`.
- **Gauge sampling is sparse & ambiguous.** A heartbeat-sampled gauge (e.g. `cerb.queue.messages.open`) only
  emits rows for non-empty facets, so "empty" and "not sampled yet" look identical (both missing). `missing:zero`
  reads empties correctly but sawtooths between samples on the `2h`/5-min view; `missing:carry` smooths but
  would freeze a drained queue at its last non-zero depth and never read 0. Narrow gaps by sampling more often
  (tighten the cron throttle), not with `carry`. The truly gap-free depth is a derived counter (enqueued − done
  − failed); deferred. The `2h` window exists for exactly this near-real-time monitoring.
- **Removing a metric dimension shifts positions.** `dimN_value_id` storage is positional, so dropping a
  *middle* dimension scrambles every dim after it. Unreleased: just edit the patch `INSERT` (+ clear old
  `metric_value`; `INSERT IGNORE` won't update an existing row). Released: leave a `number/reserved:`
  placeholder in the slot — a dimension you never write to stays `0` (increment fills unprovided dims with 0
  via `array_fill_keys`), so later dims keep their column. Protobuf-style. See `metrics.md`.
- **Header switcher is one shared partial.** Change `view_header_sparkline.tpl` once to re-skin every
  worklist's presets; the `getSparklines` `$windows` map is the matching key→period source (keep keys in sync,
  legacy `24h/7d/30d` aliased for the scheduler).

## Verify

`Search → <Type>` shows the column; toggle 2h/1d/30d (persists per view); hover shows tooltip
(labels appear only for multi-series); add/remove in Customize; one `metric_value`-backed query per page.
Headless check: bootstrap + `DAO_MetricValue::getSparklines([...], '1mo', 'America/New_York')`.

---

# The matching metric quick-search filter

Constrain the worklist by the **same metrics** the sparkline shows — "automations that ran >100×",
"events slower than 2000ms avg in the past 2h". This is now a fully-shared pattern; **the authoritative
recipe lives in `worklist-quick-search.md` → "Parameterized metric filter"** (the series map via
`DAO_MetricValue::metricFilterSeries()`, the shared resolver, the marquee hint, and the `field:()`
autocomplete). Below is only what's specific to the sparkline relationship.

- **Same metrics, two providers.** The sparkline column uses `metrics.timeseries` (binned, with the
  `faceted_*` functions); the filter uses `metrics.subtotals` (one flat range aggregate, functions
  `sum/count/avg/min/max`). `avg` in subtotals = `SUM(sum)/SUM(samples)` is the weighted/faceted average
  for the grouped dimension and matches the sparkline's short `avg` legend label.
- **Counter vs gauge.** `metricFilterSeries($metric, 'counter'|'gauge', $extra)` mirrors the sparkline's
  per-type series choice (counters → `sum` bar; gauges → `faceted_*` band). The filter map and the
  sparkline series specs are *separate* (different provider/function vocab) but describe the same metrics —
  keep them in sync by intent.

## Sparkline-specific gotchas

- **Dimension storage differs by type** (the bug that killed the first hand-rolled version): `record`/`number`
  dims store the **literal id** in `dimN_value_id`; `string`/`extension`/`text` dims store a `metric_dimension.id`
  (look up `.name`). `metrics.subtotals` and `metrics.timeseries` both handle this — never resolve dims yourself.
- **Filter range is independent of the sparkline switcher.** The filter's `since`/`until` default to all-time
  (`'big bang'`/`'now'`); the column's 2h/1d/30d switcher is a separate localStorage window.
- **`since`/`until` are reserved** range sub-keys, so a series can't be named that. We control `cerb.*`
  metrics, so fine.
- **Threshold compared in PHP** after the subtotal (one row per dim value = a small set). Push a SQL `HAVING`
  into the provider later only if a high-cardinality dimension needs it.

## Verify (headless)

`DAO_MetricValue::validateMetricQuery('runs:>50 duration.avg:>2s', SearchFields_X::getMetricFilterMap(), $err)`
→ `true`; a typo or bad function (`duration.bogus:>1`) → `false` + a hint in `$err`. End-to-end:
`SearchFields_X::getWhereSQL(getVirtualQuickSearchParamFromTokens('usage', $tokens, …VIRTUAL_USAGE))` from
`CerbQuickSearchLexer::getFieldsFromQuery('usage:(runs:>50)')` → `<table>.id IN (…)`; `runs:>99999999` →
`0=1`; `typo:>1` → `0=1`. (Set an active worker first in CLI: `getActiveWorker()` hits the session.)
