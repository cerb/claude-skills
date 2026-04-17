# DAO Pattern Reference

## Class Structure

All Data Access Objects extend `Cerb_ORMHelper`:

```php
class DAO_RecordType extends Cerb_ORMHelper {
    const ID = 'id';
    const NAME = 'name';
    // Field constants map to DB column names

    static function getFields(): array                    // Validation schema
    static function create(array $fields): int            // INSERT, returns ID
    static function update($ids, array $fields)           // UPDATE, fires events
    static function get($id): ?Model_RecordType           // Fetch by ID
    static function getAll(): array                       // Fetch all
    static function delete($ids)                          // DELETE with cleanup
    static function search(array $columns, DevblocksSearchCriteria $params,
        $limit, $page, $sortBy, $sortAsc, $withCounts): array
    static function maint(): void                         // Maintenance/cleanup
}
```

Associated classes per record type:
- `Model_RecordType` — data model (plain object with public properties)
- `SearchFields_RecordType` — search field definitions (`IDevblocksSearchFields`)
- `View_RecordType` — worklist view (`C4_AbstractView`)
- `Context_RecordType` — record type context (permissions, cards, URLs)

## Database Operations

```php
// Writes go to master
$db->ExecuteMaster("INSERT INTO table ...");
$db->ExecuteMaster(sprintf("UPDATE table SET name=%s WHERE id=%d",
    $db->qstr($name), $id));

// Reads use replica if configured
$rs = $db->QueryReader("SELECT * FROM table WHERE id=%d", [$id]);
while($row = mysqli_fetch_assoc($rs)) { ... }
```

- Use `Cerb_ORMHelper::qstr($val)` for string escaping in class context
- Batch updates in chunks of 100 when firing events

## Events and Deltas

Updates trigger events automatically:
- `CerberusContexts::checkpointChanges($context, $ids)` — before update
- `DevblocksPlatform::markContextChanged($context, $ids)` — after update
- Event: `dao.{table_name}.update`

## Form Handling Pattern

```php
private function _profileAction_savePeekJson() {
    DevblocksPlatform::readHttpRequest();  // Validate method
    $active_worker = CerberusApplication::getActiveWorker();

    // Get form data
    $id = DevblocksPlatform::importGPC($_POST['id'] ?? null, 'integer', 0);
    $name = DevblocksPlatform::importGPC($_POST['name'] ?? null, 'string', '');

    // Build fields array
    $fields = [
        DAO_RecordType::NAME => $name,
    ];

    // Validate
    if(false == ($error = DAO_RecordType::validate($fields, $id))) {
        // Check actor permissions
        if($id) {
            $record = DAO_RecordType::get($id);
            Context_RecordType::isWriteableByActor($record, $active_worker);
            DAO_RecordType::update($id, $fields);
        } else {
            $id = DAO_RecordType::create($fields);
        }
    }

    echo json_encode(['status' => true, 'id' => $id]);
}
```

## Database Migration Patches

Patches live in `features/cerberusweb.core/patches/11.x/11.2.0.php`.

```php
function patch_11_2_0_YYYY_MM_DD_HHMMSS() {
    $db = DevblocksPlatform::services()->database();
    $logger = DevblocksPlatform::services()->log();
    $tables = $db->metaTables();

    if(!isset($tables['my_new_table'])) {
        $sql = "CREATE TABLE my_new_table (
            id INT UNSIGNED NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL DEFAULT '',
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";
        $db->ExecuteMaster($sql) or die("[PATCH] Failed to create table.");
        $logger->info("[Patch] Created 'my_new_table' table.");
    }
}
```

Register new patch functions in the patch file's dispatch array at the bottom.

To re-run a patch during development, see `references/rerun-patch.md`.
