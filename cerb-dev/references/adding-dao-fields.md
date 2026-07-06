# Adding Fields to an Existing Record Type

When adding a new column to an existing DAO, touch every location below in order. Missing any one will cause silent bugs or runtime errors.

## Checklist

### 1. Database migration (`patches/11.x/11.2.0.php`)
Add an `ALTER TABLE` in a new dated patch function. Register it in the dispatch array.

### 2. `DAO_{RecordType}` — constants
Add the new constant(s) alphabetically. The constant value **is** the DB column name.

```php
const EXPIRES_AT = 'expires_at';
const LAST_ACCESSED_AT = 'last_accessed_at';
```

### 3. `DAO_{RecordType}::getFields()` — validation
Add a validation entry. Use `->timestamp()` for Unix timestamps, `->string()` for text.

```php
$validation->addField(self::EXPIRES_AT)->timestamp();
$validation->addField(self::LAST_ACCESSED_AT)->timestamp();
```

### 4. `DAO_{RecordType}::getWhere()` — SELECT clause
Add the column to the SELECT string (keep alphabetical).

```sql
SELECT created_at, expires_at, id, last_accessed_at, name, token_hint, updated_at
```

### 5. `DAO_{RecordType}::_getObjectsFromResult()` — row mapping
Map the new column to the model property.

```php
$object->expires_at = intval($row['expires_at']);
$object->last_accessed_at = intval($row['last_accessed_at']);
```

### 6. `DAO_{RecordType}::getSearchQueryComponents()` — search SELECT
Add the column and its `SearchFields_*` alias (keep parallel with the constants).

```php
$select_sql = sprintf("SELECT ".
    "service_token.expires_at as %s, ".
    ...
    SearchFields_ServiceToken::EXPIRES_AT,
```

Note: internal-only fields (e.g. `token_hash` used only for lookup) can be **omitted** from the search SELECT — they don't need to appear in worklist results.

### 6b. `DAO_{RecordType}::search()` — model-overlay merge loop (if present)
Some DAOs (e.g. `DAO_Task`) re-load full models after the search query and **overlay** select
display fields onto each result row before handing off to the worklist template:

```php
$models = CerberusContexts::getModels(CerberusContexts::CONTEXT_TASK, array_column($results[0], SearchFields_Task::ID));
foreach($results[0] as $id => $result) {
    if(null != ($model = $models[$id] ?? null)) {
        $result[SearchFields_Task::OWNER_ID]   = $model->owner_id;
        $result[SearchFields_Task::PROJECT_ID] = $model->project_id;  // <-- easy to forget
        ...
    }
}
```

If this loop exists, add your field to it too. **Symptom of missing it:** the worklist column
renders blank even though the SELECT, SearchField, and template cell are all correct — because the
overlay rebuilds the row and the template reads the overlaid value, not the raw SELECT column.
Not every DAO has this loop; grep `search()` for a `foreach($results[0]` overlay before assuming.

### 7. `SearchFields_{RecordType}` — constants
Add constants alphabetically. Values are prefixed shorthand (e.g. `s_expires_at`).

```php
const EXPIRES_AT = 's_expires_at';
const LAST_ACCESSED_AT = 's_last_accessed_at';
```

### 8. `SearchFields_{RecordType}::_getFields()` — field definitions
Add a `DevblocksSearchField` entry. Fourth argument is the i18n label key; **fifth argument is the column type**.

```php
self::EXPIRES_AT => new DevblocksSearchField(self::EXPIRES_AT, 'service_token', 'expires_at', $translate->_('common.expires'), Model_CustomField::TYPE_DATE, true),
```

**Always set the 5th arg (`$type`) — never leave it `null`.** It's a `Model_CustomField::TYPE_*` (or `DevblocksSearchCriteria::TYPE_*`) constant that drives the **type-hint icon + label** on each column tile in the worklist Customize UI (`internal/views/customize_view.tpl`), routed through `C4_AbstractView::getColumnDisplayMeta()` (`abstract_view.php`). A `null` type falls through to a meaningless gray `tag` icon with no hint. Keep it consistent with the type the same field already declares in `Context_*::getContext()`'s `$token_types`. `SearchFields_Notification::_getFields()` is a clean exemplar.

| Column kind                          | 5th arg                               |
|--------------------------------------|---------------------------------------|
| id / numeric (priority, counts)      | `Model_CustomField::TYPE_NUMBER`      |
| name / varchar / `*_context` string  | `Model_CustomField::TYPE_SINGLE_LINE` |
| `*_context_id`                       | `Model_CustomField::TYPE_NUMBER`      |
| created / updated timestamp          | `Model_CustomField::TYPE_DATE`        |
| 0/1 boolean (`is_disabled`)          | `Model_CustomField::TYPE_CHECKBOX`    |
| JSON / kata blob (`entry_json`)      | `Model_CustomField::TYPE_MULTI_LINE`  |

**i18n for field labels:** Reuse an existing `common.*` key if one fits. For field-specific labels, add a `dao.{record_type}.{field_name}` key to `strings.xml` (alphabetically under a `<!-- RecordType -->` comment in the `dao.*` section) and reference it with `$translate->_('dao.record_type.field_name')`. Never hard-code English strings as the fourth argument.

```xml
<!-- Group -->
<tu tuid="dao.group.subject_has_mask">
    <tuv xml:lang="en_US">
        <seg>Subject Has Mask</seg>
    </tuv>
</tu>
```

```php
self::SUBJECT_HAS_MASK => new DevblocksSearchField(self::SUBJECT_HAS_MASK, 'worker_group', 'subject_has_mask', $translate->_('dao.group.subject_has_mask'), Model_CustomField::TYPE_CHECKBOX, true),
```

### 9. `Model_{RecordType}` — public properties
Add properties alphabetically.

```php
public $expires_at;
public $last_accessed_at;
```

### 10. `View_{RecordType}::getQuickSearchFields()` — quick search
Add date/text entries. **Keys use camelCaps** (not underscores).

```php
'expires' => [
    'type' => DevblocksSearchCriteria::TYPE_DATE,
    'options' => ['param_key' => SearchFields_ServiceToken::EXPIRES_AT],
],
'lastAccessed' => [
    'type' => DevblocksSearchCriteria::TYPE_DATE,
    'options' => ['param_key' => SearchFields_ServiceToken::LAST_ACCESSED_AT],
],
```

### 11. `View_{RecordType}::doSetCriteria()` — criteria dispatch
Add date fields to the date case; string fields to the string case.

```php
case SearchFields_ServiceToken::EXPIRES_AT:
case SearchFields_ServiceToken::LAST_ACCESSED_AT:
    $criteria = $this->_doSetCriteriaDate($field, $oper);
    break;
```

### 12. `Context_{RecordType}::profileGetFields()` — profile card
Add a property entry. Use `TYPE_DATE` for timestamps.

```php
$properties['expires_at'] = [
    'label' => DevblocksPlatform::translateCapitalized('common.expires'),
    'type' => Model_CustomField::TYPE_DATE,
    'value' => $model->expires_at,
];
```

For a field that **references another record** (a `*_id` foreign key), use `TYPE_LINK` and pass the
target context in `params.context`. The value is the linked record's id:

```php
$properties['project_id'] = [
    'label' => mb_ucfirst($translate->_('common.project')),
    'type' => Model_CustomField::TYPE_LINK,
    'value' => $model->project_id,
    'params' => ['context' => Context_TaskProject::ID],
];
```

**Symptom of missing it:** the field is absent from the profile / not available as a
`profileGetFields` entry, even though the DAO column and SearchField exist.

### 13. `Context_{RecordType}::getContext()` — placeholder tokens
Add to both `$token_labels` and `$token_types`, then assign in the `if($record)` block.

```php
// labels
'expires_at' => $prefix.$translate->_('common.expires'),

// types
'expires_at' => Model_CustomField::TYPE_DATE,

// values
$token_values['expires_at'] = $service_token->expires_at;
```

### 14. `templates/{record_type}/view.tpl` — worklist cell renderer
For timestamp fields, add the search field constant value (e.g. `w_created_at`) to the existing date `in_array` check so it renders with `devblocks_prettytime`:

```smarty
{elseif in_array($column, ['w_created_at', 'w_updated'])}
    {if !empty($result.$column)}
    <td data-column="{$column}" title="{$result.$column|devblocks_date}">{$result.$column|devblocks_prettytime}</td>
    {else}
    <td data-column="{$column}">{'common.never'|devblocks_translate|lower}</td>
    {/if}
```

Without this, the raw Unix timestamp integer is displayed instead of a human-readable relative time.

### 15. `Context_{RecordType}::getKeyToDaoFieldMap()` — API key mapping
Add entries so the record API and automations can set the field by key.

```php
'expires_at' => DAO_ServiceToken::EXPIRES_AT,
'last_accessed_at' => DAO_ServiceToken::LAST_ACCESSED_AT,
```

## Notes

- **Quick search keys**: use camelCaps (`lastAccessed`, not `last_accessed`).
- **Internal-only fields** (e.g. a hash used only for lookup): add to DAO constants + `getFields()` validation, but omit from `getWhere()` SELECT, `_getObjectsFromResult()`, `SearchFields`, and `Context` — they don't surface to users.
- **i18n keys**: reuse existing `common.*` keys where possible; otherwise add `dao.{record_type}.{field_name}` entries to `strings.xml`. Never pass a bare English string as the label argument to `DevblocksSearchField`.
- **`TEXT` columns in MySQL cannot have a `DEFAULT` value.** Use `text NOT NULL` — never `text NOT NULL DEFAULT ''`. The DB engine rejects a default on any `TEXT`/`BLOB` type. Use `varchar(255)` instead if a default is needed.
