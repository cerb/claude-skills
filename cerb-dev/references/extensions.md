# Extension Patterns Reference

## Automation API Commands

Extend `Extension_AutomationApiCommand` and implement `run()` and `getAutocompleteSuggestions()`.
Registered under `cerb.automation.api_command` in `plugin.xml`. Invoked from KATA via `api.command:` with `inputs.name` and `inputs.params`.

```php
class ApiCommand_Example extends Extension_AutomationApiCommand {
    const ID = 'cerb.commands.example';

    function run(array $params=[], &$error=null) : array|false {
        $value = $params['some_param'] ?? '';
        if(!$value) {
            $error = 'example: `some_param` is required.';
            return false;
        }
        return ['result' => $value];
    }

    public function getAutocompleteSuggestions($key_path, $prefix, $key_fullpath, $script) : array {
        return match($key_path) {
            // Root: list param keys available at this level
            '' => [
                'some_param:',
                'connected_account_id@int:',
                'domains@csv:',
                'key_bits@int: 2048',
            ],
            // Typed suggestions — cerb-uri opens a connected account chooser
            'connected_account_id:' => [
                'type'   => 'cerb-uri',
                'params' => ['connected_account' => null],
            ],
            default => [],
        };
    }
}
```

The `cerb-uri` type for a key path triggers the KATA editor to show a live record chooser popup. This works in **any** PHP autocomplete suggestion array — `getAutocompleteSuggestions()` on API commands, automation triggers, connected service providers, or anywhere else suggestions are returned. Use `'params' => ['connected_account' => null]` for connected accounts. Other supported `params` keys (from `cerberus.js` `kataSuggestionsCerbUriJson` call): `automation`, `automation_resource`, `resource`. Set the value to `null` to include all, or pass filter params to restrict results.

`plugin.xml` registration:
```xml
<extension point="cerb.automation.api_command">
    <id>cerb.commands.example</id>
    <name>cerb.commands.example</name>
    <class>
        <file>api/automations/api_commands/cerb.commands.example.php</file>
        <name>ApiCommand_Example</name>
    </class>
    <params />
</extension>
```

KATA usage (automation function):
```yaml
api.command/example:
  output: result
  inputs:
    name: cerb.commands.example
    params:
      some_param: hello
      connected_account_id@int: {{inputs.connected_account_id}}
  on_error:
    error: {{__return.error}}
```

---

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
