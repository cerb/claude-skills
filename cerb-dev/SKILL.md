---
name: cerb-dev
description: Work on Cerb core and plugin code. Use when making changes to the Cerb PHP/MySQL codebase, adding new record types, creating extensions, writing migrations, or debugging platform internals.
---

# Cerb Core Development

Cerb is a 24-year-old PHP/MySQL helpdesk and workflow automation platform built on the **Devblocks** framework (not Laravel/Symfony). The codebase is mature and follows consistent patterns throughout.

For directory layout, plugin structure, naming conventions, context system, extension points, template paths, and CSS/SCSS: see `references/architecture.md`.

## Creating a New Record Type

See `references/new-record-type.md` for the complete step-by-step guide.

Quick summary:
1. Add `CREATE TABLE` migration in `patches/11.x/11.2.0.php`
2. Run the generator — writes PHP + template files directly, prints only XML snippets:
   ```bash
   python3 .claude/skills/cerb-dev/tools/gen-dao.py \
       --plugin-id cerberusweb.core \
       --table my_record \
       --fields "id bigint unsigned NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL DEFAULT '', created_at int unsigned NOT NULL DEFAULT 0, updated_at int unsigned NOT NULL DEFAULT 0" \
       --acl-write all \
       --output-dir features/cerberusweb.core
   ```
   `--acl-write` accepts `all` (default, anyone) or `admin` (admins only).
3. Insert the printed `plugin.xml` snippets (class loader + two extensions)
4. Insert the printed `strings.xml` i18n entries
5. Customize `// [TODO]` sections in the generated PHP for non-standard fields

## Common Commands

```bash
composer cache-clear          # Clear template/cache files
composer test                 # Run platform tests
cd install/docker && docker compose up   # Start local dev environment
docker exec -it cerb-mysql-1 mysql -u root -p cerb   # Connect to MySQL (password: s3cr3t)
```

## Related Skills

These skills are always installed alongside this one:

- `/cerb-docs` — look up Cerb documentation, features, configuration, integrations
- `/cerb-automations` — write or modify Cerb automations (KATA, commands, triggers, events)
- `/cerb-search` — build search queries for any record type

## Reference Files

- `references/architecture.md` — directory layout, plugin structure, naming conventions, context system, extension points, template paths, CSS/SCSS
- `references/dao-pattern.md` — DAO class structure, database operations, events/deltas, form handling pattern, migration patch authoring
- `references/extensions.md` — card widget, cron job, and search index extension patterns
- `references/plugin-xml.md` — plugin.xml manifest structure, extension points, class loaders
- `references/new-record-type.md` — complete guide for creating a new record type
- `references/adding-dao-fields.md` — adding fields to an existing DAO/model/context
- `references/peek-edit-patterns.md` — Smarty gotchas, checkbox groups, dynamic rows, flat lookup sets
- `references/ui-conventions.md` — JS/UI rules: AJAX helpers (`genericAjaxGet/Post/Popup`), confirmation dialogs (`confirmPopup()`, never `confirm()`)
- `references/worklist-subtotals.md` — adding IAbstractView_Subtotals to View_ classes
- `references/rerun-patch.md` — how to force a database patch to re-run in development
- `references/metrics.md` — registering and incrementing metrics
- `references/database-schema.md` — canonical schema reference (`cerb.schema.kata`), column name lookups, common table timestamp columns
- `references/security.md` — security conventions: never use $_REQUEST, always enforce POST method before reading $_POST, CSRF protection, input sanitization via importGPC()
- `references/validation.md` — field validation: types, string modifiers, `->addValidator()`, `->addFormatter()`, available validators (`email`, `url`, `contextId`, etc.), surfacing errors in JSON responses

## Tools

- `tools/gen-dao.py` — Python generator for new record type boilerplate. Key options: `--table`, `--fields` (SQL column definitions), `--plugin-id`, `--acl-write all|admin`, `--output-dir`. Fields are alphabetized automatically.
