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

## Standard `getContext()` Token Values

`Context_X::getContext()` populates `$token_values` for placeholder expansion, mention chips, card render, and the framework's general "give me this record" lookup. Always include these alongside whatever record-specific fields you add:

```php
$url_writer = DevblocksPlatform::services()->url();

$token_values['_loaded'] = true;
$token_values['_label'] = $record->name;
$token_values['_image_url'] = $url_writer->writeNoProxy(
    sprintf('c=avatars&ctx=%s&id=%d', 'my_record', $record->id), true
) . '?v=' . $record->updated_at;
$token_values['id'] = $record->id;
$token_values['name'] = $record->name;
$token_values['updated_at'] = $record->updated_at;
// ...record-specific fields...
$token_values['record_url'] = $url_writer->writeNoProxy(
    sprintf("c=profiles&type=my_record&id=%d-%s", $record->id, DevblocksPlatform::strToPermalink($record->name)), true
);
```

`_image_url` is the canonical handle for the record's avatar — without it, downstream UI that wants to show the record's image has nothing to render. See `references/avatars.md` for the full avatar system (plugin.xml `avatars` option, peek-save `upsertWithImage` call, monogram fallback).

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

## Delete Cascade — What Happens Automatically

A `DAO_X::delete()` should bracket its actual `DELETE FROM x_table` with:

```php
parent::_deleteAbstractBefore($context, $ids);
// ... your DELETE ...
parent::_deleteAbstractAfter($context, $ids);
```

`_deleteAbstractAfter` fires the `context.delete` event. The platform listener (`_handleContextDelete` in `features/cerberusweb.core/api/listeners.classes.php`) then **automatically** cleans up these cross-cutting tables for the deleted context+ids:

| Table | Purpose |
|---|---|
| `attachment_link` | File attachments linked to the record |
| `calendar` | Calendars owned by the record |
| `comment` | Comments on the record (and where it's the owner) |
| `context_activity_log` | Activity log entries about the record |
| `context_alias` | Aliases for the record |
| `context_avatar` | Avatar/image for the record |
| `context_link` | Manual record-to-record links |
| `context_merge_history` | Merge history rows |
| `custom_fieldset` | Custom fieldsets owned by, or referenced via, the record |
| `custom_field_value` | Custom field values on the record |
| `email_signature` | Signatures owned by the record |
| `mail_html_template` | HTML templates owned by the record |
| `notification` | Notifications about the record |
| `context_scheduled_behavior` | Scheduled behaviors on the record |
| `snippet` | Snippets owned by the record |
| `bot` | Bots owned by the record |
| `workspace_page` | Workspace pages owned by the record |

**Don't add explicit cleanup calls for any of these in your `delete()` method** — they'll run twice. The abstract handler covers them as long as you call `_deleteAbstractAfter`.

You only need explicit cleanup for tables that are **not** keyed by `(context, context_id)` or **not** universal — e.g. `queue_message.job_id`, `queue_job_chunk.job_id`, plugin-specific tables that reference your record by some other column. Those need their own `DAO_OtherThing::deleteByXIds($ids)` calls inside your `delete()`.

## Attachment Lifecycle

Linking an attachment to a record via:
```php
DAO_Attachment::addLinks($context, $context_id, $attachment_ids);
```
…grants download access to anyone who can `Context_X::isReadableByActor` the linked record. `Context_Attachment::isDownloadableByActor` walks every `attachment_link` row and approves if the worker can read **any** linked context. Use this instead of session hacks (e.g. the legacy `$_SESSION['view_export_file_id']`).

When deleting a parent record, the abstract delete cascade (above) removes the `attachment_link` rows automatically. The orphan-files maint job then purges attachments with no remaining links after 24h. So the right pattern is **never delete the attachment directly** — drop the link and let maint handle it.

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
