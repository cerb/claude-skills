# Record changesets (field version history) + the DB storage engine

`record_changeset` versions one or more **fields** of a record over time, storing each version's content as a blob through the storage layer. Used today by automations, workflows, groups, metrics, mail routing rules, toolbar sections, etc. — anywhere you see "version history" / a diff popup on a profile.

DAO + model: `features/cerberusweb.core/api/dao/record_changeset.php`
(`DAO_RecordChangeset`, `Model_RecordChangeset`, `Storage_RecordChangeset`).

## Writing a changeset

```php
// returns ['<record_key>' => <changeset_id>, ...]
DAO_RecordChangeset::create(
    'automation',      // record_type — the context URI alias, NOT the full context id
    $id,               // record_id — the owning record's PK
    [
        'script' => $script_kata,   // record_key => content (any string)
        'policy' => $policy_kata,
    ],
    $active_worker->id ?? 0         // worker_id (0 = system, e.g. from a patch)
);
```

- `record_type` is the lowercase **context URI** (`'automation'`, `'group'`, `'metric'`, `'workflow'`, `'community_portal'` for portals — see `Context_*::URI`), not `cerberusweb.contexts.*`.
- `create()` JSON-encodes `{record_key: content}`, `sha1`s it, and **dedupes**: if the last changeset for that `(record_type, record_id, record_key)` has an identical hash, it returns the existing id and writes nothing. So calling it on every save is cheap and only stores real changes.
- It writes the blob via `Storage_RecordChangeset::put()` onto the configured storage profile.
- Real example: `features/cerberusweb.core/api/uri/profiles/automation.php:209-224` (wrapped in try/catch + `logError`, since versioning must never block the save).

Read content back: `Model_RecordChangeset::getContent()` → `['<record_key>' => '<content>']` (decodes the stored JSON via `Storage_RecordChangeset::get()`).

## The diff viewer is superuser-only

History/diff is rendered by `PageSection_InternalRecords` (`features/cerberusweb.core/api/uri/internal/records.php`) actions `showChangesetsPopup` / `refreshChangesets` / `getChangesetJson`, template `internal/record_changesets/diff_popup.tpl`.

**Access is hard-gated to admins** — every action begins with `if(!$active_worker->is_superuser) → 403` (lines ~649-650, ~708-711). There is **no** fallback to the owning record's `isReadableByActor()`. Practical consequence: a changeset attached to a *world-readable* record (e.g. a portal, whose `Context_CommunityTool::isReadableByActor()` returns `allowEverything`) is still only viewable by superusers. This makes a changeset a handy **admin-only blob store** when you need to stash something recoverable but not worker-visible (a migration backup, an audit snapshot) — unlike a file attachment, whose download permission *does* inherit the parent record's readability.

## The database storage engine format

`Storage_RecordChangeset` (and storage generally) dispatches to a pluggable engine. The **database** engine (`DevblocksStorageEngineDatabase`, `libs/devblocks/api/services/storage.php`) keeps each namespace in its own table `storage_<namespace>` (here `storage_record_changeset`):

```sql
CREATE TABLE storage_record_changeset (
  id INT UNSIGNED NOT NULL DEFAULT 0,   -- == the owning row's storage_key
  data BLOB,                            -- raw bytes, NO gzip / NO base64
  chunk SMALLINT UNSIGNED DEFAULT 1,    -- 1-based; content split at 65535 bytes/row
  INDEX id_and_chunk (id, chunk)
) ENGINE=InnoDB
```

- `put()` returns the row `id` as the `storage_key`; `get()` reassembles chunks `ORDER BY chunk ASC`. Tables auto-create on demand and also ship in `cerb_base_tables.sql`.
- This is why a **patch can hand-write a changeset entirely in raw SQL** (no DAO, no storage service — see `migration-patch.md`):
  1. `INSERT INTO record_changeset (record_type, record_id, record_key, worker_id, created_at, storage_sha1hash, storage_size, storage_extension, storage_profile_id) VALUES (...,'devblocks.storage.engine.database',0)` → `$cid = $db->LastInsertId()`.
  2. `UPDATE record_changeset SET storage_key='$cid' WHERE id=$cid`.
  3. For each `str_split($json, 65535)` chunk: `INSERT INTO storage_record_changeset (id, data, chunk) VALUES ($cid, <qstr chunk>, <n>)`.

Note: deleting a record does **not** currently purge its `record_changeset` rows or their `storage_*` blobs — orphans are harmless but persist.
