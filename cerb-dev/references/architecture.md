# Architecture Reference

## Directory Structure

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

## Plugin/Feature Structure

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

## Context System

Records are identified by context strings (e.g., `cerb.contexts.ticket`). The context class:
- Implements `IDevblocksContextProfile`, `IDevblocksContextPeek`
- Defines `::ID` constant for the context string
- Controls permissions: `isReadableByActor()`, `isWriteableByActor()`, `isDeletableByActor()`
- Generates profile URLs and card popup rendering
- Provides token labels/values for placeholder expansion

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

## Extension Points (plugin.xml)

```xml
<extension point="devblocks.context">           <!-- Record types -->
<extension point="cerberusweb.page">            <!-- UI pages -->
<extension point="cerberusweb.ui.page.section"> <!-- Page sections -->
<extension point="cerb.automation.api_command"> <!-- Automation commands -->
<extension point="cerberusweb.cron">            <!-- Scheduled jobs -->
<extension point="cerberusweb.cards.widget">    <!-- Card widgets -->
<extension point="cerb.search.index">           <!-- Search index backends -->
```

## Template Locations

Uses Smarty 4.x. Common paths under `features/cerberusweb.core/templates/`:
- `records/types/{record_type}/view.tpl` — worklist view
- `records/types/{record_type}/peek_edit.tpl` — edit popup
- `internal/cards/widgets/{name}/render.tpl` — card widget render
- `internal/cards/widgets/{name}/config.tpl` — card widget config

## CSS/SCSS

- Source: `install/extras/developers/css/cerb.css/cerb.scss`
- Partials: `install/extras/developers/css/cerb.css/layout/*.scss`
- Output: `features/cerberusweb.core/resources/css/cerb.css`

Compile: `composer cache-clear` rebuilds assets, or run the SCSS compiler directly.

## Common PHP Utilities

### Random password / token generation

```php
CerberusApplication::generatePassword($length=8, $chars="ABCDEFGHJKLMNPQRSTUVWXYZ123456789")
```

Defined in `api/Application.class.php`. Generates a random string from the given charset.  
Default charset already excludes ambiguous chars (0/O, I). Use this instead of writing custom random-string loops.

```php
// 8-char uppercase alphanumeric token (default)
$token = CerberusApplication::generatePassword(8);

// 10-char lowercase hex
$token = CerberusApplication::generatePassword(10, "abcdef0123456789");
```
