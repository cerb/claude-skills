---
name: cerb-dev
description: Work on Cerb core and plugin code. Use when making changes to the Cerb PHP/MySQL codebase, adding new record types, creating extensions, writing migrations, or debugging platform internals.
---

# Cerb Core Development

Cerb is a 24-year-old PHP/MySQL helpdesk and workflow automation platform built on the **Devblocks** framework (not Laravel/Symfony). The codebase is mature and follows consistent patterns throughout.

## Architecture

### Directory Structure

```
api/                        # Application-level code
libs/devblocks/             # The Devblocks framework core
features/                   # Built-in plugins/features
  cerberusweb.core/         # Main plugin (DAOs, contexts, extensions)
    api/
      dao/                  # Data access objects
      cards/widgets/        # Card widget handlers
      crons/                # Scheduled job handlers
      Extensions/           # Extension base classes
      uri/                  # URL/controller handlers
    patches/11.x/           # Database migration patches
    plugin.xml              # Manifest: extensions, class loaders
    templates/              # Smarty templates
plugins/                    # Third-party plugins
install/
  docker/                   # docker-compose.yml for local dev
  extras/
    developers/css/         # SCSS source for cerb.css
    sdk/devblocks-dao.php   # Code generator for new record types
storage/                    # Runtime: cache, compiled templates
```

### Plugin/Feature Structure

```
features/plugin.name/
├── plugin.xml          # Manifest: class loaders, extension points, dependencies
├── strings.xml         # i18n translations
├── api/
│   ├── App.php         # Extension implementations
│   ├── dao/            # DAO classes
│   └── profiles/       # Profile page handlers
└── templates/          # Smarty templates
```

## Key Framework Services

Access via `DevblocksPlatform::services()`:

```php
$db = DevblocksPlatform::services()->database();   // DB connection (master/reader)
$cache = DevblocksPlatform::services()->cache();    // Disk, memcached, or redis
$tpl = DevblocksPlatform::services()->template();  // Smarty 4.x
$validation = DevblocksPlatform::services()->validation();
```

## DAO Pattern

All Data Access Objects extend `Cerb_ORMHelper`. Standard structure:

```php
class DAO_RecordType extends Cerb_ORMHelper {
    const ID = 'id';
    const NAME = 'name';
    // Field constants map to DB column names

    static function getFields(): array      // Validation schema
    static function create(array $fields): int   // INSERT, returns ID
    static function update($ids, array $fields)  // UPDATE, fires events
    static function get($id): ?Model_RecordType  // Fetch by ID
    static function getAll(): array              // Fetch all
    static function delete($ids)                 // DELETE with cleanup
    static function search(array $columns, DevblocksSearchCriteria $params, $limit, $page, $sortBy, $sortAsc, $withCounts): array
    static function maint(): void                // Maintenance/cleanup
}
```

Associated classes per record type:
- `Model_RecordType` — data model (plain object with public properties)
- `SearchFields_RecordType` — search field definitions (`IDevblocksSearchFields`)
- `View_RecordType` — worklist view (`C4_AbstractView`)
- `Context_RecordType` — record type context (permissions, cards, URLs)

## Naming Conventions

| Pattern | Example |
|---|---|
| `DAO_{RecordType}` | `DAO_Ticket`, `DAO_Queue` |
| `Model_{RecordType}` | `Model_Ticket` |
| `Context_{RecordType}` | `Context_Ticket` |
| `SearchFields_{RecordType}` | `SearchFields_Ticket` |
| `View_{RecordType}` | `View_Ticket` |
| `Controller_{Name}` | `Controller_Config` |
| `PageSection_Profiles{RecordType}` | `PageSection_ProfilesTicket` |

## Context System

Records are identified by context strings (e.g., `cerb.contexts.ticket`). The context class:
- Implements `IDevblocksContextProfile`, `IDevblocksContextPeek`
- Defines `::ID` constant for the context string
- Controls permissions: `isReadableByActor()`, `isWriteableByActor()`, `isDeletableByActor()`
- Generates profile URLs and card popup rendering
- Provides token labels/values for placeholder expansion

## Extension Points (plugin.xml)

```xml
<extension point="devblocks.context">     <!-- Record types -->
<extension point="cerberusweb.page">      <!-- UI pages -->
<extension point="cerberusweb.ui.page.section"> <!-- Page sections -->
<extension point="cerb.automation.api_command"> <!-- Automation commands -->
<extension point="cerberusweb.cron">      <!-- Scheduled jobs -->
<extension point="cerberusweb.cards.widget"> <!-- Card widgets -->
<extension point="cerb.search.index">     <!-- Search index backends -->
```

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

## Database Migration Patches

Patches live in `features/cerberusweb.core/patches/11.x/11.2.0.php` (version-specific file).

```php
// Add a new patch function at the bottom of the patch file:
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

Register new patch functions in the patch file's dispatch array.

## Templates

Uses Smarty 4.x. Templates stored in `templates/` subdirectories.

Common locations:
- `templates/records/types/{record_type}/view.tpl` — worklist view
- `templates/records/types/{record_type}/peek_edit.tpl` — edit popup
- `templates/internal/cards/widgets/{name}/render.tpl` — card widget render
- `templates/internal/cards/widgets/{name}/config.tpl` — card widget config

## Creating a New Record Type

1. Add table schema in a migration patch (`patches/11.x/11.2.0.php`)
2. Generate boilerplate with SDK: `php install/extras/sdk/devblocks-dao.php`
3. Create DAO class with standard methods in `api/dao/`
4. Create Context class implementing `IDevblocksContextProfile`, `IDevblocksContextPeek`
5. Register in `plugin.xml` under `devblocks.context`
6. Create templates for view and peek_edit
7. Add profile section class if a profile page is needed

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

## Events and Deltas

Updates trigger events automatically:
- `CerberusContexts::checkpointChanges($context, $ids)` — before update
- `DevblocksPlatform::markContextChanged($context, $ids)` — after update
- Event: `dao.{table_name}.update`

## Card Widgets

Card widgets extend `Extension_CardWidget` and implement:
- `renderConfig(Model_CardWidget $widget)` — render config form
- `saveConfig(Model_CardWidget $widget)` — save config from POST
- `render(Model_CardWidget $widget, $dict)` — render the widget

Register in `plugin.xml`:
```xml
<extension point="cerberusweb.cards.widget">
    <id>cerb.card.widget.my_widget</id>
    <name>My Widget</name>
    <class><file>api/App.php</file><name>CardWidget_MyWidget</name></class>
</extension>
```

## Search Index Extensions

Search index backends extend `Extension_SearchIndex` and implement:
- `index(array $records)` — index records
- `search($query, $options)` — run a search
- `delete($ids)` — remove records from index
- `purge()` — clear the index

Register in `plugin.xml`:
```xml
<extension point="cerb.search.index">
    <id>cerb.search.index.my_backend</id>
    <name>My Search Backend</name>
    <class><file>api/App.php</file><name>SearchIndex_MyBackend</name></class>
</extension>
```

## Cron Jobs

Cron job handlers extend `CerberusCronPageExtension` and implement `run()`.

```php
class Cron_MyJob extends CerberusCronPageExtension {
    function run() {
        $logger = DevblocksPlatform::services()->log('My Job');
        // Do work...
    }
}
```

Register in `plugin.xml`:
```xml
<extension point="cerberusweb.cron">
    <id>cerb.cron.my_job</id>
    <name>My Job</name>
    <class><file>api/App.php</file><name>Cron_MyJob</name></class>
    <params><param key="locked" value="0"/></params>
</extension>
```

## CSS/SCSS

Cerb's stylesheet is compiled from SCSS:
- Source: `install/extras/developers/css/cerb.css/cerb.scss`
- Partials: `install/extras/developers/css/cerb.css/layout/*.scss`
- Output: `features/cerberusweb.core/resources/css/cerb.css`

Compile: `composer cache-clear` rebuilds assets, or run the SCSS compiler directly.

## Common Commands

```bash
# Clear template and cache files
composer cache-clear

# Run platform tests
composer test

# Start local dev environment
cd install/docker && docker compose up

# Connect to MySQL
docker exec -it cerb-mysql-1 mysql -u root -p cerb
# password: s3cr3t
```

## Cerb Documentation

The official Cerb documentation is at `https://cerb.ai/docs/`. You can fetch individual pages with WebFetch (e.g. `https://cerb.ai/docs/records/types/ticket`).

Search and fetch Cerb docs using one of these methods (in order of preference):

1. **MCP tools** (`mcp__claude_ai_Cerb__search_documents`, `mcp__claude_ai_Cerb__fetch_documents`): Use when available. Users can add the MCP server URL `https://api.cerb.cloud/docs/mcp` in Claude Desktop or Claude Code settings.

2. **Docs API** (no auth required, fallback when MCP is unavailable):
   ```bash
   # Semantic search
   curl --silent -X POST "https://api.cerb.cloud/docs/search" -H "Content-Type: application/json" -d '{"query":"your search query here"}'

   # Fetch pages as LLM-friendly Markdown (comma-separated doc IDs from search results)
   curl --silent "https://api.cerb.cloud/docs/fetch/index,pricing"
   ```

3. **WebFetch**: Fetch individual HTML pages directly (e.g. `https://cerb.ai/docs/records/types/ticket`).

Use these when the local reference files don't cover a topic or you need to verify current behavior.

## Reference Files

- `references/plugin-xml.md` — plugin.xml manifest structure, extension points, class loaders
