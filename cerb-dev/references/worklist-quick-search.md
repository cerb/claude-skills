# Worklist Quick Search & Virtual Deep-Search Fields

Quick search provides the search bar above a worklist. Fields are registered with type, operator, and example hints. For linked records (queue, worker, group, org), use **virtual deep-search fields** so the user can type a name rather than a raw ID.

## Quick Search Field Types

| `type` constant | Behavior |
|---|---|
| `TYPE_TEXT` | Free-text match (use `OPTION_TEXT_PARTIAL` for `LIKE %value%`) |
| `TYPE_NUMBER` | Numeric equality / range |
| `TYPE_DATE` | Date / date-range |
| `TYPE_VIRTUAL` | Delegates to a context-aware nested search (use for linked records) |
| `TYPE_CONTEXT` | Chooser-style ID filter |

## Virtual Deep-Search Fields for Linked Records

When a field holds a foreign key (e.g., `queue_id`, `worker_id`), expose it as `TYPE_VIRTUAL` so the user can type `queue:(name contains foo)` instead of a raw ID. This powers both the search bar and the filter chip display.

### Step 1 — Add constants to `SearchFields_`

```php
const VIRTUAL_QUEUE_SEARCH  = '*_queue_search';
const VIRTUAL_WORKER_SEARCH = '*_worker_search';
```

Naming rule: `*_<table_alias>_search` where `<table_alias>` matches what you'd call the field in quick search (e.g., `queue`, `worker`, `group`, `org`).

### Step 2 — Register in `_getFields()`

Add non-sortable, non-visible entries with `'*'` as the table and `false` for visibility:

```php
self::VIRTUAL_QUEUE_SEARCH  => new DevblocksSearchField(self::VIRTUAL_QUEUE_SEARCH,  '*', 'queue_search',  null, null, false),
self::VIRTUAL_WORKER_SEARCH => new DevblocksSearchField(self::VIRTUAL_WORKER_SEARCH, '*', 'worker_search', null, null, false),
```

### Step 3 — Handle in `getWhereSQL()`

```php
static function getWhereSQL(DevblocksSearchCriteria $param) {
    switch($param->field) {
        case self::VIRTUAL_QUEUE_SEARCH:
            return self::_getWhereSQLFromVirtualSearchField($param, CerberusContexts::CONTEXT_QUEUE, 'my_record.queue_id');

        case self::VIRTUAL_WORKER_SEARCH:
            return self::_getWhereSQLFromVirtualSearchField($param, CerberusContexts::CONTEXT_WORKER, 'my_record.worker_id');

        default:
            // ... cf_ and common virtual handling
    }
}
```

The third argument is the fully-qualified column (`table.column`) that holds the foreign key.

### Step 4 — Register in `getQuickSearchFields()`

Use `TYPE_VIRTUAL` with `'type' => 'search'` examples (opens a nested search popup, not a chooser):

```php
'queue' => [
    'type' => DevblocksSearchCriteria::TYPE_VIRTUAL,
    'options' => ['param_key' => SearchFields_MyRecord::VIRTUAL_QUEUE_SEARCH],
    'examples' => [
        ['type' => 'search', 'context' => CerberusContexts::CONTEXT_QUEUE, 'q' => ''],
    ],
],
'worker' => [
    'type' => DevblocksSearchCriteria::TYPE_VIRTUAL,
    'options' => ['param_key' => SearchFields_MyRecord::VIRTUAL_WORKER_SEARCH],
    'examples' => [
        ['type' => 'search', 'context' => CerberusContexts::CONTEXT_WORKER, 'q' => ''],
    ],
],
```

### Step 5 — Handle in `getParamFromQuickSearchFieldTokens()`

```php
function getParamFromQuickSearchFieldTokens($field, $tokens) {
    switch($field) {
        case 'fieldset':
            return DevblocksSearchCriteria::getVirtualQuickSearchParamFromTokens($field, $tokens, '*_has_fieldset');

        case 'queue':
            return DevblocksSearchCriteria::getVirtualQuickSearchParamFromTokens($field, $tokens, SearchFields_MyRecord::VIRTUAL_QUEUE_SEARCH);

        case 'worker':
            return DevblocksSearchCriteria::getVirtualQuickSearchParamFromTokens($field, $tokens, SearchFields_MyRecord::VIRTUAL_WORKER_SEARCH);

        default:
            if($field == 'links' || str_starts_with($field, 'links.'))
                return DevblocksSearchCriteria::getContextLinksParamFromTokens($field, $tokens);

            $search_fields = $this->getQuickSearchFields();
            return DevblocksSearchCriteria::getParamFromQueryFieldTokens($field, $tokens, $search_fields);
    }
}
```

### Step 6 — Implement `renderVirtualCriteria()`

Renders the human-readable filter chip when a virtual search param is active:

```php
function renderVirtualCriteria($param) : void {
    switch($param->field) {
        case SearchFields_MyRecord::VIRTUAL_QUEUE_SEARCH:
            echo sprintf('%s matches <b>%s</b>',
                DevblocksPlatform::strEscapeHtml(DevblocksPlatform::translateCapitalized('dao.my_record.queue_id')),
                DevblocksPlatform::strEscapeHtml($param->value)
            );
            break;

        case SearchFields_MyRecord::VIRTUAL_WORKER_SEARCH:
            echo sprintf('%s matches <b>%s</b>',
                DevblocksPlatform::strEscapeHtml(DevblocksPlatform::translateCapitalized('common.worker')),
                DevblocksPlatform::strEscapeHtml($param->value)
            );
            break;

        default:
            $this->_renderVirtualCriteria($param);
            break;
    }
}
```

## `renderCriteriaParam()` for Linked Record Labels

When the raw filter chip would display a numeric ID, override `renderCriteriaParam()` to show the record name instead:

```php
function renderCriteriaParam($param) {
    $field = $param->field;
    $values = !is_array($param->value) ? [$param->value] : $param->value;

    switch($field) {
        // Linked records — look up display names from IDs
        case SearchFields_MyRecord::QUEUE_ID:
        case SearchFields_MyRecord::WORKER_ID:
            $label_map = SearchFields_MyRecord::getLabelsForKeyValues($field, $values);
            parent::_renderCriteriaParamString($param, $label_map);
            break;

        // Status enum — all labels known upfront, $values doesn't matter
        case SearchFields_MyRecord::STATUS_ID:
            $label_map = SearchFields_MyRecord::getLabelsForKeyValues($field, $values);
            $this->_renderCriteriaParamString($param, $label_map);
            break;

        default:
            parent::renderCriteriaParam($param);
            break;
    }
}
```

`getLabelsForKeyValues()` must handle these field keys — see `SearchFields_::getLabelsForKeyValues()` pattern in `worklist-subtotals.md`.

## String-Based Status Filter (VIRTUAL_STATUS pattern)

When a field holds a small fixed set of status values (like running/paused/done or open/waiting/closed), expose it as a `VIRTUAL_STATUS`-style field so users can type `status:r` or `status:[p,d]` instead of raw integers.

### 1 — Constant and field registration

```php
const VIRTUAL_STATUS = '*_status';

// in _getFields():
self::VIRTUAL_STATUS => new DevblocksSearchField(self::VIRTUAL_STATUS, '*', 'status', $translate->_('common.status'), null, false),
```

### 2 — `getWhereSQL()` — translate string aliases to integers

Match on the first letter only so `'r'`, `'running'`, `'Running'` all work:

```php
case self::VIRTUAL_STATUS:
    $values = is_array($param->value) ? $param->value : [$param->value];
    $statuses = [];

    $oper = match($param->operator) {
        DevblocksSearchCriteria::OPER_NIN,
        DevblocksSearchCriteria::OPER_NIN_OR_NULL => 'NOT ',
        default => '',
    };

    foreach($values as $value) {
        switch(substr(DevblocksPlatform::strLower($value), 0, 1)) {
            case 'r': $statuses[] = MyStatus::RUNNING->value; break;
            case 'p': $statuses[] = MyStatus::PAUSED->value;  break;
            case 'd': $statuses[] = MyStatus::DONE->value;    break;
        }
    }

    if(empty($statuses))
        return null;

    return sprintf('my_record.status_id %sIN (%s) ', $oper, implode(', ', $statuses));
```

### 3 — `getQuickSearchFields()` — both string and ID filters

```php
'status' => [
    'type' => DevblocksSearchCriteria::TYPE_VIRTUAL,
    'options' => ['param_key' => SearchFields_MyRecord::VIRTUAL_STATUS],
    'examples' => ['running', 'paused', 'done', '[r,p]', '![d]'],
],
'status.id' => [
    'type' => DevblocksSearchCriteria::TYPE_NUMBER,
    'options' => ['param_key' => SearchFields_MyRecord::STATUS_ID],
],
```

### 4 — `getParamFromQuickSearchFieldTokens()` — normalize tokens

```php
case 'status':
    $oper = null;
    $value = null;
    CerbQuickSearchLexer::getOperArrayFromTokens($tokens, $oper, $value);

    $statuses = [];
    foreach($value as $v) {
        switch(substr(DevblocksPlatform::strLower($v), 0, 1)) {
            case 'r': $statuses['running'] = true; break;
            case 'p': $statuses['paused']  = true; break;
            case 'd': $statuses['done']    = true; break;
        }
    }

    return new DevblocksSearchCriteria(SearchFields_MyRecord::VIRTUAL_STATUS, $oper, array_keys($statuses));
```

### 5 — `renderVirtualCriteria()` — human-readable chip

```php
case SearchFields_MyRecord::VIRTUAL_STATUS:
    $values = is_array($param->value) ? $param->value : [$param->value];
    $labels = [];
    foreach($values as $v) {
        $labels[] = '<b>' . DevblocksPlatform::strEscapeHtml(match(substr(DevblocksPlatform::strLower($v), 0, 1)) {
            'r' => 'Running',
            'p' => 'Paused',
            'd' => 'Done',
            default => $v,
        }) . '</b>';
    }
    echo sprintf('Status is %s', implode(' or ', $labels));
    break;
```

### 6 — `doSetCriteria()` — sidebar filter path

```php
case SearchFields_MyRecord::VIRTUAL_STATUS:
    $options = DevblocksPlatform::importGPC($_POST['options'] ?? null, 'array', []);
    $criteria = new DevblocksSearchCriteria($field, $oper, $options);
    break;
```

## Standard vs. Virtual Quick Search Comparison

| Scenario | Use |
|---|---|
| Filter by exact numeric ID (`queue.id:42`) | `TYPE_NUMBER` on the raw FK field |
| Filter by name/search across linked record (`queue:(name:foo)`) | `TYPE_VIRTUAL` with `VIRTUAL_*_SEARCH` |
| Boolean or timestamp field | `TYPE_CHECKBOX` / `TYPE_DATE` on the real column |
| Fieldset membership | `TYPE_VIRTUAL` with `VIRTUAL_HAS_FIELDSET` (standard; included by generator) |
| Parameterized metric/aggregate group (`activity:(runs:>100 duration.avg:>2s since:..)`) | `TYPE_VIRTUAL` + custom `case` parser + a `getMetricFilterMap()` series map (see "Parameterized metric filter" below) |

For linked records that users interact with by name (queues, workers, groups, orgs), always expose **both**:
- The ID field as `TYPE_NUMBER` with a chooser example (for programmatic / precise filtering)
- A virtual search field as `TYPE_VIRTUAL` with a search example (for interactive use)

Example — expose both for queue:
```php
'queue' => [
    'type' => DevblocksSearchCriteria::TYPE_VIRTUAL,
    'options' => ['param_key' => SearchFields_MyRecord::VIRTUAL_QUEUE_SEARCH],
    'examples' => [['type' => 'search', 'context' => CerberusContexts::CONTEXT_QUEUE, 'q' => '']],
],
'queue.id' => [
    'type' => DevblocksSearchCriteria::TYPE_NUMBER,
    'options' => ['param_key' => SearchFields_MyRecord::QUEUE_ID],
    'examples' => [['type' => 'chooser', 'context' => CerberusContexts::CONTEXT_QUEUE, 'q' => '']],
],
```

## Parameterized metric filter (`usage:`/`activity:`/`records:`)

A field that takes a **self-parsed `(...)` group** of metric thresholds + a date range, e.g.
`usage:(runs:>100 duration.avg:>2s since:"-2 weeks")` — filter a worklist by its metric data. **The filter
key is each worklist's own choice** (automations `usage:`, queues `activity:`, search indexes `records:`,
…); the backend resolver in `DAO_MetricValue` is name-neutral and shared across **11 worklists** today.
Resolution runs through the `metrics.subtotals` data query (one range aggregate per threshold → PHP compare
→ AND-intersect → matching raw dimension values). See `metrics.md` and `worklist-sparklines.md`.

### The series map — `SearchFields_X::getMetricFilterMap()` (single source of truth)

One static method per worklist returns the threshold vocabulary; it is the **single source** consumed by
the SQL filter, the parse-time validator, AND the autocomplete. Build each row with the helper
`DAO_MetricValue::metricFilterSeries($metric, $type, $extra)` — **one row per series**, never per function:

```php
static function getMetricFilterMap() : array {
    return [
        'runs'     => DAO_MetricValue::metricFilterSeries('cerb.automation.invocations', 'counter'),
        'errors'   => DAO_MetricValue::metricFilterSeries('cerb.automation.invocations', 'counter', ['query' => ['exit_state' => 'error']]),
        'duration' => DAO_MetricValue::metricFilterSeries('cerb.automation.duration', 'counter', ['unit' => 'ms', 'default' => 'avg']),
    ];
}
```

- **`$type` (`counter`|`gauge`)** picks the valid aggregate set + default (`METRIC_FILTER_FUNCTIONS`):
  counter → `[sum,count,avg,max,min]` (default **sum**); gauge → `[avg,max,min,count]` (default **avg**, no
  `sum` — summing snapshots is meaningless). A bare `runs:` uses `functions[0]`; `runs.max:` selects another.
- **`$extra['query']`** pins a *second* dimension while still grouping by the anchor dimension — this is how
  `errors` slices `cerb.automation.invocations` by `exit_state=error`, and how queue `done`/`failed` slice by
  `status_id`. The whole filter stays anchored to one grouping dimension.
- **`$extra['unit'=>'ms']`** makes values parse as **durations** (`500ms`/`2s`/`5m`/`1h`/`1000d` → ms; a
  bare number stays ms). A *timer counter* like `duration` (stored as a counter: `sum`=total runtime,
  `avg`=mean) keeps the counter set but adds `'default'=>'avg'` so bare `duration:`=mean while `duration.sum:`
  (total) survives.
- **Function names are the `metrics.subtotals` ones** (`sum/count/avg/min/max`). There, `avg` =
  `SUM(sum)/SUM(samples)` — the weighted/faceted average for the grouped dimension, and it matches the
  sparkline's short legend labels. The verbose `faceted_average/faceted_min/faceted_max` exist **only** in
  `metrics.timeseries` (sparklines), not subtotals — don't use them here.

### The shared resolver (`DAO_MetricValue`)

| method | when | returns |
|---|---|---|
| `getDimensionValuesByMetricQuery($inner, $map, $dimension, $tz?)` | SQL time (`getWhereSQL`) | `?array`: **null** = invalid filter, `[]` = matched nothing, `array` = matching raw dim values |
| `validateMetricQuery($inner, $map, &$error)` | parse time (DB-free) | `bool`; on false sets `$error` with a human hint |
| `getMetricFilterSubkeySuggestions($map)` | autocomplete | the in-parens `()` sub-key suggestions |

All three delegate to the private `_parseMetricQuery` so SQL/validation/autocomplete can never disagree.
**Invalid input fails loud, not silent**: any unknown series, stray/keyless token, unparseable value, or
unknown `series.function` → `null` → `getWhereSQL` emits **`0=1`** (match nothing). Empty group / range-only
is valid ("ran in range" = primary series `count > 0`); a legitimately-empty result (`errors:>0`, no errors)
returns `[]` → `0=1` with **no** warning. Range defaults to all-time when no `since`/`until`.

### Per-worklist wiring (the ~6 edits)

1. **`SearchFields_X`**: `const VIRTUAL_USAGE='*_usage';` + a hidden `_getFields()` entry; `getMetricFilterMap()`; a `_getWhereSQLFrom…Filter` that calls the resolver.
   ```php
   // getWhereSQL() case — BOTH invalid paths return 0=1 (fail loud), not 1=1
   case self::VIRTUAL_USAGE:
       if($param->operator != DevblocksSearchCriteria::OPER_CUSTOM || !is_string($param->value)) return '0=1';
       $matches = DAO_MetricValue::getDimensionValuesByMetricQuery($param->value, self::getMetricFilterMap(),
           'automation_id', CerberusApplication::getActiveWorker()?->timezone ?: null);
       if(is_null($matches)) return '0=1';                       // invalid criteria
       $ids = array_filter(array_map('intval', $matches));
       return $ids ? sprintf('%s IN (%s)', self::getPrimaryKey(), implode(',', $ids)) : '0=1';
   ```
2. **View `getParamFromQuickSearchFieldTokens`**: `case 'usage': return DevblocksSearchCriteria::getVirtualQuickSearchParamFromTokens($field, $tokens, SearchFields_X::VIRTUAL_USAGE);` (captures the `(...)` group as one `OPER_CUSTOM` raw string).
3. **View `getQuickSearchMetricFilterMap($field_key)`** — override the base no-op to return the map for this field's key. **This one hook drives both the marquee hint and the autocomplete** (below), so no other autocomplete/validation code is needed:
   ```php
   function getQuickSearchMetricFilterMap(string $field_key) : ?array {
       return $field_key == 'usage' ? SearchFields_X::getMetricFilterMap() : null;
   }
   ```
4. **View `getQuickSearchFields`**: declare the field `TYPE_VIRTUAL` with `options.param_key` only — **no `examples`** (the `()` autocomplete supersedes them).
5. **View ctor**: `addColumnsHidden([SearchFields_X::VIRTUAL_USAGE])` (search-only, never a column).
6. **`renderVirtualCriteria`**: echo a chip label for `VIRTUAL_USAGE`.

When the dimension ≠ the row record, map the matched values in `getWhereSQL`: Automation filters
`automation.id IN (dimValues)` (values ARE automation ids); Automation Event maps `trigger` extension_ids
via `automation_event.id IN (SELECT id FROM automation_event WHERE extension_id IN (…))`.

### User-facing hint (marquee) — already wired centrally

`C4_AbstractView::getParamsFromQuickSearch()`'s parse walk calls `validateMetricQuery` for any field whose
`getQuickSearchMetricFilterMap($key)` is non-null; on failure it sets `$error`, and the existing
`addParamsWithQuickSearch` path does `addParams([false])` (match nothing) **and**
`C4_AbstractView::marqueeAppend($this->id, $error)` → a dismissible banner via `view_marquee.tpl`. Messages
come from the resolver (`_parseMetricQuery`): unknown series lists the valid keys; `duration.bogus` →
"`duration` has no `bogus` function. Try: avg, sum, …"; bad duration/number values get a format hint.

### In-parens autocomplete — the `field:()` group-scope feature

Driven generically off the same `getQuickSearchMetricFilterMap` hook in
`C4_AbstractView::getQueryAutocompleteSuggestions()`: it sets the top-level snippet `usage:(${1})` (open the
group), populates `$suggestions['usage:()']` from `getMetricFilterSubkeySuggestions($map)` (each series +
every `series.function` + `since:`/`until:`), and drops the flat value bucket. The client
(`resources/js/cerb-ui/searchquery.js`) computes `scopeKey = path.join('')` from the cursor — inside
`usage:(` that's `'usage:()'` — and the tokenizer (`/[A-Za-z0-9_.]+:/`) treats dotted keys like
`duration.avg:` as one field, so it re-scopes cleanly after each pick. The `date` filter (`case 'date'` in
`getQueryAutocompleteSuggestions`, ~line 2387) is the precedent for the `'<field>:()'` sub-key bucket;
nested paren scopes (`field:subkey:()`) also work but aren't used here (functions are dotted, listed flat).

> Don't reach for `TYPE_DATE` for these — it's only for real date columns. (`created:`'s
> `getDateParamFromTokens` in `libs/devblocks/api/Model.php` is still a fine model for *parsing* a
> `(since: until: …)` group, and the metric filter reuses `since`/`until` as reserved range keys.)
