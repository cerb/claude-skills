# Extension Patterns Reference

## Card Widgets

Extend `Extension_CardWidget` and implement:
- `renderConfig(Model_CardWidget $widget)` — render config form
- `saveConfig(Model_CardWidget $widget)` — save config from POST
- `render(Model_CardWidget $widget, $dict)` — render the widget

```php
class CardWidget_MyWidget extends Extension_CardWidget {
    function render(Model_CardWidget $widget, $dict) {
        $tpl = DevblocksPlatform::services()->template();
        $tpl->assign('widget', $widget);
        $tpl->display('...');
    }
}
```

`plugin.xml` registration:
```xml
<extension point="cerberusweb.cards.widget">
    <id>cerb.card.widget.my_widget</id>
    <name>My Widget</name>
    <class><file>api/App.php</file><name>CardWidget_MyWidget</name></class>
</extension>
```

## Cron Jobs

Extend `CerberusCronPageExtension` and implement `run()`:

```php
class Cron_MyJob extends CerberusCronPageExtension {
    function run() {
        $logger = DevblocksPlatform::services()->log('My Job');
        // Do work...
    }
}
```

`plugin.xml` registration:
```xml
<extension point="cerberusweb.cron">
    <id>cerb.cron.my_job</id>
    <name>My Job</name>
    <class><file>api/App.php</file><name>Cron_MyJob</name></class>
    <params><param key="locked" value="0"/></params>
</extension>
```

## Search Index Backends

Extend `Extension_SearchIndex` and implement:
- `index(array $records)` — index records
- `search($query, $options)` — run a search
- `delete($ids)` — remove records from index
- `purge()` — clear the index

`plugin.xml` registration:
```xml
<extension point="cerb.search.index">
    <id>cerb.search.index.my_backend</id>
    <name>My Search Backend</name>
    <class><file>api/App.php</file><name>SearchIndex_MyBackend</name></class>
</extension>
```
