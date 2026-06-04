# Migration Patches

Patch files live in `features/cerberusweb.core/patches/` (e.g. `11.x/11.2.0.php`). They run once per version on `/update`. All operations should be idempotent (check before altering).

## Prefer raw `$db` SQL over `DAO_` CRUD

In patches, do row reads/writes with straight SQL through `$db = DevblocksPlatform::services()->database()` (`ExecuteMaster`, `GetOneMaster`/`GetArrayMaster`, `metaTables`/`metaTable`, `qstr`, `LastInsertId`) — **not** `DAO_*::create/update/delete/get`.

Why:
- `DAO_` methods fire validation, context change-events, and `checkpointChanges`/`markContextChanged` deltas that are inappropriate (and slow) during an upgrade, and can cascade into code paths that assume a *fully migrated* schema the patch hasn't finished applying.
- DAO behavior drifts across releases. A patch is historical — it must keep producing the same result years later. Calling today's DAO from a 2-year-old patch is how upgrades silently break. Raw SQL is self-contained and stable.

Look up workers/admins, settings, etc. directly: `SELECT id FROM worker WHERE is_superuser=1 AND is_disabled=0`, `REPLACE INTO devblocks_setting (...)`, etc. Compute hashes/sizes inline in PHP (`sha1()`, `strlen()`).

**The exception** is purpose-built import/reconcile helpers that are *designed* to be called from patches and replace-by-key (they don't do per-record event churn) — `DAO_Automation::importFromJson()`, `CerberusApplication::packages()->importToLibraryFromFiles()` (see below). Those are fine; general-purpose `DAO_Foo::create()` is not.

## Platform (devblocks.core) vs feature (cerberusweb.core) patches

Schema changes to **platform-owned tables** — anything created/owned under `libs/devblocks`, e.g.
`cerb_plugin` — must go in a **devblocks.core** patch at `libs/devblocks/patches/<ver>.php` (registered in
`libs/devblocks/plugin.xml`), **not** in a `cerberusweb.core` patch.

Platform patches run **before** all feature/plugin patches, so features can assume the platform schema is
already current. If you `ALTER` a platform table from a `cerberusweb.core` patch, feature/plugin code that
runs earlier (DAO `SELECT`s, the Engine's manifest persistence) will reference a column the platform hasn't
added yet and break. We hit exactly this adding a `status` column to `cerb_plugin` — it had to move to
`libs/devblocks/patches/2.6.0.php`.

```php
// libs/devblocks/patches/2.6.0.php  (devblocks.core)
$db = DevblocksPlatform::services()->database();
list($columns,) = $db->metaTable('cerb_plugin');

if(!array_key_exists('status', $columns)) {
    $db->ExecuteMaster("ALTER TABLE cerb_plugin ADD COLUMN status VARCHAR(32) NOT NULL DEFAULT ''");
}

return TRUE;
```

The column-existence guard (`$db->metaTable(...)`) is the idempotency pattern for the `ALTER`.

### `/update` re-reads plugin manifests automatically

Do **not** call `DevblocksPlatform::readPlugins()` from inside a patch to refresh manifest-derived columns
(plugin `name`, `description`, `status`, `manifest_cache_json`). The `/update` flow re-reads every
`plugin.xml` as part of its normal operation — in fact the patches are running *because* plugins are being
read — so that data is repopulated for you. A patch only needs to make the schema change (the `ALTER`); the
re-read backfills the values from the manifests.

## Writing a blob to storage from a patch

Patches may write blobs through the storage layer — established precedent: `features/cerberusweb.core/patches/10.x/10.2.0.php:619-641` migrates the logo into storage. To stay pure-SQL (preferred), write directly into the **database storage engine's** namespace table instead of calling the storage service. The engine (`DevblocksStorageEngineDatabase`, `libs/devblocks/api/services/storage.php`) stores each namespace in `storage_<namespace>`:

```sql
CREATE TABLE IF NOT EXISTS storage_<namespace> (
  id INT UNSIGNED NOT NULL DEFAULT 0,
  data BLOB,
  chunk SMALLINT UNSIGNED DEFAULT 1,
  INDEX id_and_chunk (id, chunk)
) ENGINE=InnoDB
```

- `data` is stored **raw** — no gzip, no base64. Split content into ≤65535-byte chunks: `str_split($content, 65535)`, one row per chunk with `chunk` starting at `1`. `get()` reassembles `ORDER BY chunk ASC`.
- The owning record's `storage_key` is the `id` used here; also set its `storage_extension = 'devblocks.storage.engine.database'` and `storage_size = strlen($content)`. Escape the blob with `$db->qstr()`.
- The `storage_<namespace>` tables ship in `cerb_base_tables.sql`; `CREATE TABLE IF NOT EXISTS` for safety. See `record-changeset.md` for a worked example (backing up data as a record changeset).

## Reimporting Built-in Automations

`DAO_Automation::importFromJson()` **replaces** the existing automation script in the database — no separate `UPDATE` query needed:

```php
$automation_files = [
    'cerb.reply.isBannedDefunct.json',
];

foreach($automation_files as $automation_file) {
    $path = realpath(APP_PATH . '/features/cerberusweb.core/assets/automations/') . '/' . $automation_file;

    if(!file_exists($path) || false === ($automation_data = json_decode(file_get_contents($path), true)))
        continue;

    DAO_Automation::importFromJson($automation_data);

    unset($automation_data);
}
```

## Reimporting Packages

```php
$packages = [
    'cerb_workspace_page_home.json',
];

CerberusApplication::packages()->importToLibraryFromFiles($packages, APP_PATH . '/features/cerberusweb.core/packages/library/');
```

See `patches/11.x/11.0.0.php` for a full example of both patterns.
