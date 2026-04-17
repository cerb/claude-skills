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
<a data-cerb-worklist-icon-customize title="{'common.customize'|devblocks_translate|capitalize}" class="minimal"><span class="glyphicons glyphicons-cogwheel"></span></a>
<a data-cerb-worklist-icon-subtotals title="{'common.subtotals'|devblocks_translate|capitalize}" class="minimal"><span class="glyphicons glyphicons-signal"></span></a>
<a data-cerb-worklist-icon-refresh title="{'common.refresh'|devblocks_translate|capitalize}" class="minimal"><span class="glyphicons glyphicons-refresh"></span></a>
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
    $context = CerberusContexts::CONTEXT_MY_RECORD;

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

        // String column with a label map — translate IDs/codes to display names
        case SearchFields_MyRecord::STATUS:
            $label_map = function(array $values) use ($column) {
                return SearchFields_MyRecord::getLabelsForKeyValues($column, $values);
            };
            $counts = $this->_getSubtotalCountForStringColumn($context, $column, $label_map, 'in', 'options[]');
            break;

        // Worker foreign key — use DictionaryDelegate for display labels, handle 0 (nobody)
        case SearchFields_MyRecord::OWNER_ID:
            $label_map = function(array $values) {
                $models = DAO_Worker::getIds($values);
                $dicts = DevblocksDictionaryDelegate::getDictionariesFromModels($models, CerberusContexts::CONTEXT_WORKER);
                $map = array_column(DevblocksPlatform::objectsToArrays($dicts), '_label', 'id');
                if(in_array(0, $values))
                    $map[0] = DevblocksPlatform::translate('common.nobody');
                return $map;
            };
            $counts = $this->_getSubtotalCountForStringColumn($context, $column, $label_map, 'in', 'worker_id');
            break;

        // Numeric foreign key (non-worker record)
        case SearchFields_MyRecord::ORG_ID:
            $label_map = function(array $values) use ($column) {
                return SearchFields_MyRecord::getLabelsForKeyValues($column, $values);
            };
            $counts = $this->_getSubtotalCountForNumberColumn($context, $column, $label_map, 'in', 'context_id[]');
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
| `_getSubtotalCountForStringColumn($context, $column)` | Plain strings where the value is also the label (IP, user agent, etc.) |
| `_getSubtotalCountForStringColumn($context, $column, $label_map, 'in', 'param[]')` | String/VARCHAR columns that need label lookup |
| `_getSubtotalCountForNumberColumn($context, $column, $label_map, 'in', 'param[]')` | Numeric foreign keys |
| `_getSubtotalCountForCustomColumn($context, $column)` | Custom fields (`cf_*`) |
| `_getSubtotalCountForVirtualField($context, $column)` | Virtual search fields (`*_`) |

**`param` name conventions** (4th arg to string/number helpers):
- `worker_id` — worker foreign key
- `context_id[]` — generic record foreign key
- `options` — enum/status codes
- `value[]` — generic values

## Label Map Patterns

**Via `getLabelsForKeyValues`** (when `SearchFields_` already implements the key):
```php
$label_map = function(array $values) use ($column) {
    return SearchFields_MyRecord::getLabelsForKeyValues($column, $values);
};
```

**Worker inline** (preferred for worker fields — uses `DevblocksDictionaryDelegate` for display labels, handles 0/"nobody"):
```php
$label_map = function(array $values) {
    $models = DAO_Worker::getIds($values);
    $dicts = DevblocksDictionaryDelegate::getDictionariesFromModels($models, CerberusContexts::CONTEXT_WORKER);
    $map = array_column(DevblocksPlatform::objectsToArrays($dicts), '_label', 'id');
    if(in_array(0, $values))
        $map[0] = DevblocksPlatform::translate('common.nobody');
    return $map;
};
$counts = $this->_getSubtotalCountForStringColumn($context, $column, $label_map, 'in', 'worker_id');
```

**Other record inline** (when `getLabelsForKeyValues` doesn't cover it):
```php
$label_map = function($ids) {
    $rows = DAO_Address::getIds($ids);
    return array_column(DevblocksPlatform::objectsToArrays($rows), 'email', 'id');
};
```

## Records Without a Context Extension

System records like `devblocks_session` have no registered `Extension_DevblocksContext`, so the standard `_getSubtotalDataForColumn` (which uses `Extension_DevblocksContext::get($context)` to find the DAO class) returns `[]` and all subtotals silently produce empty results.

**Fix:** Override `_getSubtotalDataForColumn` in the `View_` class to call the DAO directly, then pass `null` as `$context` to the count helpers (they only pass it through to the data method, which you've already overridden).

```php
// devblocks_session has no context extension, so bypass the context lookup
protected function _getSubtotalDataForColumn($context, $field_key) {
    $db = DevblocksPlatform::services()->database();

    $fields = $this->getFields();
    $columns = $this->view_columns;
    $params = $this->getParams();

    if(!isset($columns[$field_key]))
        $columns[] = $field_key;

    $query_parts = DAO_MyRecord::getSearchQueryComponents(
        $columns,
        $params,
        $this->renderSortBy,
        $this->renderSortAsc
    );

    $join_sql = $query_parts['join'];
    $where_sql = $query_parts['where'];

    $sql = sprintf("SELECT %s.%s as label, count(*) as hits ",
            $db->escape($fields[$field_key]->db_table),
            $db->escape($fields[$field_key]->db_column)
        ).
        $join_sql.
        $where_sql.
        sprintf("GROUP BY %s.%s ",
            $db->escape($fields[$field_key]->db_table),
            $db->escape($fields[$field_key]->db_column)
        ).
        "ORDER BY hits DESC ".
        "LIMIT 0,250 ";

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
$counts = $this->_getSubtotalCountForStringColumn(null, $column, $label_map, 'in', 'worker_id[]');
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
