# Rebuilding the installer baseline SQL

The guided installer at `install/index.php` reads three SQL files from `install/sql/`:

| File | What it is | Origin |
|------|------------|--------|
| `cerb_base_tables.sql` | `CREATE TABLE` DDL, one statement per line, no `AUTO_INCREMENT=N` counters, no per-column `CHARACTER SET utf8mb3` (utf8mb4 columns are preserved). | Regenerated from `mysqldump -d` after running all patches. |
| `cerb_base_rows.sql` | Seed `INSERT` rows for automation events, listeners, workflows, default workspace pages, etc. Timestamps use `UNIX_TIMESTAMP()` so values land at install time. | Regenerated from `mysqldump -t` with a curated `--ignore-table` list. |
| `cerb_setup.sql` | Admin worker + first-run workspace seed. Run when the installer prompts for the admin account. | **Hand-maintained.** Don't regenerate. |

The baseline drifts out of sync as patches in `features/cerberusweb.core/patches/11.x/` add columns, tables, and seed rows. Periodically (before a major release, or after a notable schema change) rebuild it as described below.

## End-to-end workflow

### 1. Spin up a clean release-branch worktree

From the main checkout:

```bash
git worktree add ../worktrees/cerb-11.2-baseline-sql -b 11.2-baseline-sql 11.2
cd ../worktrees/cerb-11.2-baseline-sql
composer install --ignore-platform-req=ext-mailparse --ignore-platform-req=ext-yaml
```

### 2. Configure Docker

```bash
cd install/docker
cp .env.template .env
# edit .env:
#   CERB_ENV=11-2-baseline-sql
#   CERB_PORT=8888    # only if 80 is already taken
docker compose up --build
```

### 3. Run the guided installer through the DB step

Open `http://localhost[:PORT]/` in a browser. Walk the installer up to and including the "install database" step — this is what runs all the patches. **Stop before you fill in the admin account.** That step seeds via `cerb_setup.sql`, which we don't want to capture.

### 4. Find the MySQL container

```bash
docker container list
# note the cerb-mysql-1 container id (e.g. 0ca616ae3a29)
```

### 5. Dump and normalize the schema (tables)

```bash
./.claude/skills/cerb-dev/tools/dump-baseline-tables.sh <container_id> \
    > install/sql/cerb_base_tables.sql
```

Optional flags (defaults match `install/docker/.env.template`): `--user cerb`, `--pass s3cr3t`, `--db cerb`.

The script:
- runs `mysqldump --compact --skip-opt -d` against the patched DB (`-d` = no rows),
- strips MySQL conditional comments,
- removes table-level `AUTO_INCREMENT=N` counters (column-level `AUTO_INCREMENT` is preserved),
- removes redundant per-column ` CHARACTER SET utf8mb3` while preserving ` CHARACTER SET utf8mb4` on columns that intentionally use it,
- collapses each `CREATE TABLE` onto a single line.

### 6. Dump and normalize the rows

```bash
./.claude/skills/cerb-dev/tools/dump-baseline-rows.sh <container_id> \
    > install/sql/cerb_base_rows.sql
```

Same optional flags as the tables script: `--user`, `--pass`, `--db`.

The script:
- runs `mysqldump --compact --skip-opt -t` (no DDL),
- skips tables that are populated elsewhere or hold transient runtime state (`automation`, `cerb_class_loader`, `cerb_event_point`, `cerb_extension`, `context_avatar`, `resource`, `storage_resources`, `package_library`, `devblocks_session`, `translation`),
- rewrites Unix timestamps to `UNIX_TIMESTAMP()` so the installer plants "now" values.

The timestamp rewrite is two ordered passes:

1. `s/'(?:1[7-9]\d{8}|2\d{9})'/UNIX_TIMESTAMP()/g` — quoted form first. Strips the surrounding `'…'` so a `text`-column timestamp (e.g. `cerb_property_store.value`) ends up as an unquoted function call rather than the literal string `'UNIX_TIMESTAMP()'`.
2. `s/\b(?:1[7-9]\d{8}|2\d{9})\b/UNIX_TIMESTAMP()/g` — bare form for top-level numeric columns.

The prefix alternation `1[7-9]\d{8}|2\d{9}` covers ~Nov 2023 → ~Jan 2065. This avoids the fragility of the old `17\d{8}` rule, which would silently fail to match `18…` timestamps starting in 2025.

### 7. Review the diff

```bash
git diff install/sql/cerb_base_tables.sql
git diff install/sql/cerb_base_rows.sql
```

Every changed line should map to a real schema or seed-row change introduced by patches since the last rebuild. No spurious whitespace/formatting noise.

## Verification checks

**Tables file:**

```bash
# One CREATE per line
[[ $(grep -c '^CREATE TABLE ' install/sql/cerb_base_tables.sql) -eq $(wc -l < install/sql/cerb_base_tables.sql) ]]
# No table-level AUTO_INCREMENT counters
! grep -F 'AUTO_INCREMENT=' install/sql/cerb_base_tables.sql
# No per-column utf8mb3 charset (table default covers it)
! grep -F 'CHARACTER SET utf8mb3' install/sql/cerb_base_tables.sql
# utf8mb4 columns preserved
grep -F 'CHARACTER SET utf8mb4' install/sql/cerb_base_tables.sql   # >0 hits expected
```

**Rows file:**

```bash
# No bare numeric timestamps left
! grep -E '\b1[7-9][0-9]{8}\b|\b2[0-9]{9}\b' install/sql/cerb_base_rows.sql
# No quoted numeric timestamps left
! grep -E "'1[7-9][0-9]{8}'|'2[0-9]{9}'" install/sql/cerb_base_rows.sql
# Most importantly: no literal-string'd function calls
! grep -F "'UNIX_TIMESTAMP()'" install/sql/cerb_base_rows.sql
# And the function call IS present
grep -F 'UNIX_TIMESTAMP()' install/sql/cerb_base_rows.sql   # >0 hits expected
```

**Round-trip import.** Wipe the DB and rerun the baseline + setup, then confirm timestamps actually resolved as function calls rather than literal text:

```bash
docker exec <container_id> mysql -u root -ps3cr3t -e \
    'DROP DATABASE cerb; CREATE DATABASE cerb CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;'
docker exec -i <container_id> mysql -u cerb -ps3cr3t cerb < install/sql/cerb_base_tables.sql
docker exec -i <container_id> mysql -u cerb -ps3cr3t cerb < install/sql/cerb_base_rows.sql
docker exec <container_id> mysql -u cerb -ps3cr3t cerb -e \
    'SELECT name, updated_at FROM automation_event LIMIT 3;'
# updated_at should be the current epoch, close to `date +%s`
```

## Edge case: timestamps inside JSON-in-string

If a seed `INSERT` ever contains a Unix-epoch-shaped integer **inside** a JSON value (e.g. `'{"created_at":1730000000}'`), pass 2 of the rewrite would replace the bare number with `UNIX_TIMESTAMP()` *inside* the single-quoted SQL string literal — producing literal text in the JSON column rather than a resolved timestamp. No 10-digit numbers currently appear in any JSON seed value, so this is a latent risk only. The verification grep checks would catch the symptom indirectly; the diff review in step 7 is the primary safeguard. If it ever happens, the fix is to `--ignore-table` the offending table and add the rows by hand to `cerb_setup.sql`.
