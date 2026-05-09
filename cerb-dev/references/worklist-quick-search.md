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
