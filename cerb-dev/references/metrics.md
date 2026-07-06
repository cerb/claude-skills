# Metrics

## Getting the singleton

```php
$metrics = DevblocksPlatform::services()->metrics();
```

## Incrementing a counter

```php
$metrics->increment(
    'cerb.some.metric.name',
    1,
    [
        'dimension_key' => $dimension_value,
    ]
);
```

Dimensions are optional. Only pass dimensions that are defined on the metric.

## Registering a new metric

Add an `INSERT IGNORE` in the versioned patch file (`features/cerberusweb.core/patches/11.x/11.2.0.php`):

```php
$db->ExecuteWriter(sprintf("INSERT IGNORE INTO metric (name, description, type, dimensions_kata, created_at, updated_at) ".
    "VALUES (%s, %s, %s, %s, %d, %d)",
    $db->qstr('cerb.some.metric.name'),
    $db->qstr('Human-readable description of what this counts'),
    $db->qstr('counter'),
    $db->qstr("text/dimension_key:\n"),
    time(),
    time()
));
```

## Dimension types in `dimensions_kata`

| Prefix | Type | Example |
|---|---|---|
| `text/` | Free-form string | `text/scope:` |
| `record/` | Record ID (with `record_type` sub-key) | `record/rule_id:\n  record_type: mail_routing_rule` |
| `extension/` | Extension point ID | `extension/trigger:` (value is an `extension_id`) |

Multiple dimensions are newline-separated in the KATA string:

```php
$db->qstr("record/rule_id:\n  record_type: mail_routing_rule\ntext/rule_key:\ntext/node_key:\n")
```

### Dimension storage gotcha (load-bearing)

`metric_value.dimN_value_id` stores **different things per dimension type**:
- `record` / `number` dims → the **literal record id / number** (e.g. automation id `42`).
- `text` / `extension` dims → a **`metric_dimension.id`** that maps to the real value via
  `metric_dimension.name` (e.g. id `7` → `cerb.trigger.mail.received`).

So you cannot resolve every dimension through `metric_dimension` — that silently breaks record dims. Both
metric data queries below already handle this per-type; **never resolve dimensions by hand** for a chart or
filter — go through `metrics.timeseries` / `metrics.subtotals`.

## Metric types

- `counter` — monotonically increasing count (most common)

## Querying metrics

Two data queries read `metric_value` (run via `DevblocksPlatform::services()->data()->executeQuery($q, [], $error)`,
or the Data Query Tester). **Never hand-roll `metric_value` SQL/binning, and never `gmdate()`** (use date.php).

### `metrics.timeseries` — for charts/sparklines
Chart-shaped: time-binned, with bin lerp, gap-fill (`missing:zero|carry`), worker timezone, and **label-keyed
series** output (`format:timeseries`). `by:[dim]` splits into one series per dimension value (relabeled to a
human label — the raw id is discarded). `function:avg` is per-bin. Use this whenever you're drawing something.
`DAO_MetricValue::getSparklines()` (see `worklist-sparklines.md`) wraps it for inline worklist sparklines.

### `metrics.subtotals` — for filters/tables/sheets
The **inverse projection**: one **flat range aggregate per dimension tuple**, no binning/lerp/gap-fill, keeping
the **RAW dimension value** (+ a `__label`). Use it to answer "which dimension values cross a threshold over
this range?" (EXISTS/threshold filters) or to dump subtotals into a table/sheet/chart.

```
type:metrics.subtotals
range:"-2 weeks to now"        # auto-granularity by span: <=1d→5m, <=14d→1h, else 1d (override: period:minute|hour|day)
series.runs:(
  metric:cerb.automation.invocations
  function:count               # count(SUM samples) | sum | avg(=SUM(sum)/SUM(samples)) | min | max
  by:[automation_id]           # GROUP BY that dimension slot (raw record id back out)
  query:(...)                  # optional dimension-value filters, same semantics as metrics.timeseries
)
format:dictionaries            # dictionaries (flat dicts) | table ({columns,rows}) | categories (C3 columnar, series-keyed)
```
- `dictionaries`/`table` are flat (one row per series×dim, with a `series` field); `categories` is C3/billboard
  columnar `[['label',cat1,cat2…],['runs',v1,v2…],['dur',…]]` (series as keys, first `by:` dim = x-axis).
- `avg` here is the correct **sample-weighted range average** (`SUM(sum)/SUM(samples)`), unlike timeseries' per-bin avg.
- File: `libs/devblocks/api/services/data/metrics_subtotals.php` (`_DevblocksDataProviderMetricsSubtotals`).
  A new metric data query registers in **4 spots**: `libs/devblocks/plugin.xml` (classloader `<file>`) + `data.php`
  ×3 (getSuggestions, executeQuery dispatch, the `data.query.types` list). A new `<file>` needs a registry
  rebuild (`DevblocksPlatform::readPlugins()`), not just `composer cache-clear`.
- Drives the per-worklist metric filter (key is the worklist's choice, e.g. `usage:(...)` / `activity:(...)`)
  via the shared `DAO_MetricValue::getDimensionValuesByMetricQuery()` — see `worklist-quick-search.md`.

## Notes

- Use `INSERT IGNORE` so the patch is safe to re-run.
- If it's unclear whether a metric already exists in the database, confirm with the user before adding it to the patch.
