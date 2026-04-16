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

### 7. `SearchFields_{RecordType}` — constants
Add constants alphabetically. Values are prefixed shorthand (e.g. `s_expires_at`).

```php
const EXPIRES_AT = 's_expires_at';
const LAST_ACCESSED_AT = 's_last_accessed_at';
```

### 8. `SearchFields_{RecordType}::_getFields()` — field definitions
Add a `DevblocksSearchField` entry. Fourth argument is the i18n label key.

```php
self::EXPIRES_AT => new DevblocksSearchField(self::EXPIRES_AT, 'service_token', 'expires_at', $translate->_('common.expires'), null, true),
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

### 14. `Context_{RecordType}::getKeyToDaoFieldMap()` — API key mapping
Add entries so the record API and automations can set the field by key.

```php
'expires_at' => DAO_ServiceToken::EXPIRES_AT,
'last_accessed_at' => DAO_ServiceToken::LAST_ACCESSED_AT,
```

## Notes

- **Quick search keys**: use camelCaps (`lastAccessed`, not `last_accessed`).
- **Internal-only fields** (e.g. a hash used only for lookup): add to DAO constants + `getFields()` validation, but omit from `getWhere()` SELECT, `_getObjectsFromResult()`, `SearchFields`, and `Context` — they don't surface to users.
- **i18n keys**: reuse existing `common.*` keys where possible; add new ones to `strings.xml` when needed.
- **`TEXT` columns in MySQL cannot have a `DEFAULT` value.** Use `text NOT NULL` — never `text NOT NULL DEFAULT ''`. The DB engine rejects a default on any `TEXT`/`BLOB` type. Use `varchar(255)` instead if a default is needed.
