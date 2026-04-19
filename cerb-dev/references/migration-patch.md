# Migration Patches

Patch files live in `features/cerberusweb.core/patches/` (e.g. `11.x/11.2.0.php`). They run once per version on `/update`. All operations should be idempotent (check before altering).

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
