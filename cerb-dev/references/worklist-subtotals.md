# Worklist Subtotals

Subtotals let users group worklist results by a field (e.g., "count tickets by status"). Only add fields with **low cardinality** — a handful of distinct values across many rows. Skip high-cardinality fields like unique IDs, masks, or free-text subjects. Date fields are not subtotaled.

## 1. Add the Interface

```php
class View_MyRecord extends C4_AbstractView implements IAbstractView_Subtotals, IAbstractView_QuickSearch {
```

Remove the commented-out `/* IAbstractView_Subtotals */` placeholder if present.

## 2. Add the Subtotals Icon to the View Template

In the worklist `view.tpl`, add the subtotals icon to the title toolbar — after the customize (cogwheel) icon and before refresh:

```smarty
<a data-cerb-worklist-icon-customize title="{'common.customize'|devblocks_translate|capitalize}" class="minimal"><span class="cerb-icons cerb-icon-gear"></span></a>
<a data-cerb-worklist-icon-subtotals title="{'common.subtotals'|devblocks_translate|capitalize}" class="minimal"><span class="cerb-icons cerb-icon-signal"></span></a>
<a data-cerb-worklist-icon-refresh title="{'common.refresh'|devblocks_translate|capitalize}" class="minimal"><span class="cerb-icons cerb-icon-refresh"></span></a>
```

The `data-cerb-worklist-icon-subtotals` attribute is what wires the icon to the subtotals panel — the label and glyph are standard across all worklists.

## 3. Implement `getSubtotalFields()`

Whitelist the specific fields that are useful to subtotal. Custom and virtual fields are handled generically in the `default` branch.

```php
function getSubtotalFields() {
    $all_fields = $this->getParamsAvailable(true);
    
    $fields = [];

    if(is_array($all_fields))
    foreach($all_fields as $field_key => $field_model) {
        $pass = false;
        
        switch($field_key) {
            case SearchFields_MyRecord::STATUS:
            case SearchFields_MyRecord::OWNER_ID:
                $pass = true;
                break;
                
            default:
                if(DevblocksPlatform::strStartsWith($field_key, 'cf_')) {
                    $pass = $this->_canSubtotalCustomField($field_key);
                } else if(str_starts_with($field_key, '*_')) {
                    $pass = $this->_canSubtotalVirtualField($field_key);
                }
                break;
        }
        
        if($pass)
            $fields[$field_key] = $field_model;
    }
    
    return $fields;
}
```

## 4. Implement `getSubtotalCounts($column)`

Dispatch to the appropriate count helper per field type.

```php
function getSubtotalCounts($column) {
    $counts = [];
    $fields = $this->getFields();
    $context = Context_MyRecord::ID;

    if(!array_key_exists($column, $fields))
        return [];
    
    switch($column) {
        // Boolean field (0/1)
        case SearchFields_MyRecord::IS_CLOSED:
            $counts = $this->_getSubtotalCountForBooleanColumn($context, $column);
            break;

        // Plain string — value IS the label (e.g., IP address, user agent)
        case SearchFields_MyRecord::USER_IP:
        case SearchFields_MyRecord::USER_AGENT:
            $counts = $this->_getSubtotalCountForStringColumn($context, $column);
            break;

        // String/numeric column with a label map (status enum, foreign key, etc.)
        // The 5th arg ('value') is the default — omit it unless doSetCriteria reads a different $_POST key
        case SearchFields_MyRecord::STATUS:
        case SearchFields_MyRecord::QUEUE_ID:
        case SearchFields_MyRecord::WORKER_ID:
            $label_map = function(array $values) use ($column) {
                return SearchFields_MyRecord::getLabelsForKeyValues($column, $values);
            };
            $counts = $this->_getSubtotalCountForStringColumn($context, $column, $label_map, 'in');
            break;

        default:
            if(DevblocksPlatform::strStartsWith($column, 'cf_')) {
                $counts = $this->_getSubtotalCountForCustomColumn($context, $column);
            } else if(DevblocksPlatform::strStartsWith($column, '*_')) {
                $counts = $this->_getSubtotalCountForVirtualField($context, $column);
            }
            break;
    }
    
    return $counts;
}
```

## Count Helper Reference

| Method | Use when |
|---|---|
| `_getSubtotalCountForBooleanColumn($context, $column)` | Boolean 0/1 fields |
| `_getSubtotalCountForStringColumn($context, $column)` | Plain strings where the value is also the label |
| `_getSubtotalCountForStringColumn($context, $column, $label_map, 'in')` | String/numeric columns needing label lookup |
| `_getSubtotalCountForCustomColumn($context, $column)` | Custom fields (`cf_*`) |
| `_getSubtotalCountForVirtualField($context, $column)` | Standard virtual fields (`*_`) |

## The 5th Argument: POST key routing

**Critical:** The 5th arg to `_getSubtotalCountForStringColumn` / `_getSubtotalCountForNumberColumn` is the `$_POST` key name that `doSetCriteria` reads when a subtotal item is clicked. Get it wrong and clicking a subtotal silently sets a null filter.

The default is `'value'`, which is what `_internalAction_addFilter` reads: `$value = DevblocksPlatform::importGPC($_POST['value'] ?? null)`. This is correct for **all simple fields** that call `new DevblocksSearchCriteria($field, $oper, $value)` in `doSetCriteria`.

Only use a different key when `doSetCriteria` explicitly reads a different `$_POST` field:

| 5th arg | When to use |
|---|---|
| *(omit / default `'value'`)* | `doSetCriteria` uses `new DevblocksSearchCriteria($field, $oper, $value)` — covers status enums, foreign key IDs, plain strings |
| `'worker_id[]'` | `doSetCriteria` calls `_doSetCriteriaWorker($field, $oper)`, which reads `$_POST['worker_id']` |
| `'options[]'` | `doSetCriteria` reads `$_POST['options']` (used for `VIRTUAL_HAS_FIELDSET`) |
| `'context_link[]'` | Context link filters |

In practice, for a record with status, queue, and worker fields where all three cases just do `new DevblocksSearchCriteria(...)`, all three should omit the 5th arg (use default `'value'`).

## Label Map Patterns

**Via `getLabelsForKeyValues`** (when `SearchFields_` already implements the key):
```php
$label_map = function(array $values) use ($column) {
    return SearchFields_MyRecord::getLabelsForKeyValues($column, $values);
};
```

**Status enum** (all labels known upfront — `getLabelsForKeyValues` ignores `$values`):
```php
case self::STATUS_ID:
    return [
        MyStatus::RUNNING->value => 'Running',
        MyStatus::PAUSED->value  => 'Paused',
        MyStatus::DONE->value    => 'Done',
    ];
```

**Worker inline** (uses `DevblocksDictionaryDelegate` for display name, handles 0/"nobody"):
```php
$label_map = function(array $values) {
    $models = DAO_Worker::getIds($values);
    $dicts = DevblocksDictionaryDelegate::getDictionariesFromModels($models, CerberusContexts::CONTEXT_WORKER);
    $map = array_column(DevblocksPlatform::objectsToArrays($dicts), '_label', 'id');
    if(in_array(0, $values))
        $map[0] = DevblocksPlatform::translate('common.nobody');
    return $map;
};
```

## Records Without a Context Extension

System records like `devblocks_session` have no registered `Extension_DevblocksContext`, so the standard `_getSubtotalDataForColumn` returns `[]` and all subtotals silently produce empty results.

**Fix:** Override `_getSubtotalDataForColumn` in the `View_` class to call the DAO directly, then pass `null` as `$context` to the count helpers.

```php
protected function _getSubtotalDataForColumn($context, $field_key) {
    $db = DevblocksPlatform::services()->database();
    $fields = $this->getFields();
    $columns = $this->view_columns;
    $params = $this->getParams();

    if(!isset($columns[$field_key]))
        $columns[] = $field_key;

    $query_parts = DAO_MyRecord::getSearchQueryComponents(
        $columns, $params, $this->renderSortBy, $this->renderSortAsc
    );

    $sql = sprintf("SELECT %s.%s as label, count(*) as hits ",
            $db->escape($fields[$field_key]->db_table),
            $db->escape($fields[$field_key]->db_column)
        ).
        $query_parts['join'].
        $query_parts['where'].
        sprintf("GROUP BY %s.%s ",
            $db->escape($fields[$field_key]->db_table),
            $db->escape($fields[$field_key]->db_column)
        ).
        "ORDER BY hits DESC LIMIT 0,250 ";

    try {
        $results = $db->GetArrayReader($sql, 15000);
    } catch(Exception_DevblocksDatabaseQueryTimeout $e) {
        $results = false;
    }

    return $results;
}
```

In `getSubtotalCounts`, pass `null` for `$context`:
```php
$counts = $this->_getSubtotalCountForStringColumn(null, $column, $label_map, 'in');
```

## Field Selection Guidelines

Good subtotal candidates:
- Status / state enums (open, waiting, closed)
- Worker owner/assignee
- Group, bucket, category
- Boolean flags
- Low-cardinality string fields (IP address for session worklists)

Poor candidates (skip these):
- Unique IDs, masks, tokens
- Free-text subject/body/name fields with high uniqueness
- Timestamps / date fields (not currently supported)
