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
composer build-css            # Rebuild cerb.css from SCSS sources
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
- `references/dao-pattern.md` — DAO class structure, standard `getContext()` tokens (`_label`, `_image_url`, `record_url`), database operations, events/deltas, form handling, migration patches
- `references/extensions.md` — card widget, cron job, and search index extension patterns
- `references/automation-triggers.md` — registering a new automation trigger/event (4 spots: trigger class, plugin.xml, patch INSERT, base_rows.sql) and the per-record-type `record.bulkUpdate` bulk-popup wiring via `Cerb\Records\BulkUpdate` (getMenuItems / handleBulkPost / createJob + `bulk_automations.tpl` include)
- `references/automation-commands.md` — adding a new top-level automation command/action (8 spots: Action class, ActionNode registry, grammar list, `cerberus.js` ×2, the two `_CerbApplication_KataSchemas` schemas `automation()`/`automationPolicy()`, `Extension_AutomationTrigger::getAutocompleteSuggestionsArray()`, +optional asset-automation build interaction) and the simpler `api.command:` sub-command pattern (`Extension_AutomationApiCommand` + plugin.xml, no framework edits)
- `references/plugin-xml.md` — plugin.xml manifest, extension points, class loaders, **options block** (`avatars`, `cards`, `comments`, etc.), and the **`/update` requirement** after edits
- `references/new-record-type.md` — complete guide for creating a new record type
- `references/adding-dao-fields.md` — adding fields to an existing DAO/model/context
- `references/peek-edit-patterns.md` — Smarty gotchas, checkbox groups, dynamic rows, flat lookup sets, avatar save via `upsertWithImage`
- `references/avatars.md` — context avatars: plugin.xml `avatars` option, `_image_url` token, `DAO_ContextAvatar::upsertWithImage`, `Controller_Avatars::renderMonogram` for fallbacks, anonymous endpoints
- `references/login-flow.md` — `Page_Login` state machine, `clearAllAssign()` gotcha, forced dark mode for login, CSRF fail-closed pattern, `getErrorMessage` codes
- `references/scss-build.md` — `cerb.css` is generated from SCSS; build command (`sass --no-source-map cerb.scss …`); inline-SVG mixin pattern; custom-button native-chrome reset
- `references/ui-conventions.md` — JS/UI rules: AJAX helpers (`genericAjaxGet/Post/Popup`), confirmation dialogs (`confirmPopup()`, never `confirm()`), custom-button reset pattern
- `references/cerb-ui.md` — the `cerb-ui-*` design system (CSS + plain-JS `CerbUI.*` components): build/loading (dev raw source vs prod minified `cerb-ui.js`, `composer build-js`/`dist`), naming + token conventions, chart `data-value*`/`data-text*` namespaces + palettes, component inventory (Page/Header/Panel/Chip/Toggle/Distbar/Legend); **live examples = the UI Reference gallery**, not this doc
- `references/worklist-subtotals.md` — adding IAbstractView_Subtotals to View_ classes; correct value_key routing for subtotal click-to-filter
- `references/worklist-quick-search.md` — IAbstractView_QuickSearch: TYPE_VIRTUAL deep-search for linked records, renderVirtualCriteria, renderCriteriaParam label display
- `references/worklist-internals.md` — getSearchQueryComponents/getPrimaryKey/getParamsQuery for building batch SQL against a worklist filter without paging
- `references/view-marquee.md` — marqueeAppend (visit-bound), setMarqueeContextCreated/Imported helpers, the cerb-peek-trigger binding gotcha
- `references/queue-system.md` — Extension_QueueConsumer, publish() shutdown semantics, GET_LOCK exactly-once completion hook, INSERT...SELECT bulk producer pattern, queue_job_chunk staging
- `references/migration-patch.md` — patch conventions: platform vs feature patches, idempotency, **prefer raw `$db` SQL over `DAO_` CRUD** (events/validation/drift) with the import-helper exceptions, **writing blobs to storage from a patch**, reimporting automations/packages
- `references/record-changeset.md` — `record_changeset` field version history: `DAO_RecordChangeset::create`, the **superuser-only diff viewer** (usable as an admin-only blob store), and the **database storage engine table format** (`storage_<namespace>`, raw chunked blobs) incl. hand-writing a changeset in pure SQL from a patch
- `references/support-center.md` — Support Center portal: **no-browser-editable-Smarty policy** (Twig=untrusted, Smarty=chrome), `DAO_CommunityToolProperty` per-portal settings, config-tab render/save, `usermeet.sc.controller` endpoints, `parseMarkdown`, and the portal-readable-by-all-workers ACL gotcha
- `references/rerun-patch.md` — how to force a database patch to re-run in development
- `references/metrics.md` — registering and incrementing metrics; the two metric **data queries** (`metrics.timeseries` for charts, `metrics.subtotals` for flat range aggregates / threshold filters / tables); the **dimension storage gotcha** (`dimN_value_id` = literal id for record/number dims, `metric_dimension.id` for text/extension dims)
- `references/database-schema.md` — canonical schema reference (`cerb.schema.kata`), column name lookups, common table timestamp columns
- `references/security.md` — security conventions: never use $_REQUEST, always enforce POST method before reading $_POST, CSRF protection, input sanitization via importGPC()
- `references/validation.md` — field validation: types, string modifiers, `->addValidator()`, `->addFormatter()`, available validators (`email`, `url`, `contextId`, etc.), surfacing errors in JSON responses
- `references/bot-behaviors.md` — deprecated bot behavior system (still widely used by large clients): package JSON format, all 42 event types, all conditions (universal + event-specific) with exact param keys, all actions with exact param keys, decision tree node types, behavior variables
- `references/baseline-sql.md` — rebuild `install/sql/cerb_base_tables.sql` and `cerb_base_rows.sql` from a fresh Docker install; the timestamp/charset/AUTO_INCREMENT normalization passes

## Tools

- `tools/gen-dao.py` — Python generator for new record type boilerplate. Key options: `--table`, `--fields` (SQL column definitions), `--plugin-id`, `--acl-write all|admin`, `--output-dir`. Fields are alphabetized automatically.
- `tools/dump-baseline-tables.sh <container_id>` — dump + normalize the schema DDL for `install/sql/cerb_base_tables.sql`. Optional `--user`/`--pass`/`--db` (default `cerb`/`s3cr3t`/`cerb`).
- `tools/dump-baseline-rows.sh <container_id>` — dump + normalize seed rows for `install/sql/cerb_base_rows.sql`, rewriting hard-coded Unix timestamps to `UNIX_TIMESTAMP()`. Same optional flags as above.
