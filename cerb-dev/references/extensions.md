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

Card widgets render inside the peek popup of a record. They're configurable per record-type by an admin and seeded via patches (`INSERT INTO card_widget (record_type, extension_id, ...)`).

Extend `Extension_CardWidget` and implement:
- `render(Model_CardWidget $widget, $context, $context_id)` — render the widget
- `invoke(string $action, Model_CardWidget $widget)` — handle AJAX actions from the rendered widget
- `renderConfig(Model_CardWidget $widget)` — render the admin config form
- `invokeConfig($action, Model_CardWidget $widget)` — handle config form actions

```php
class CardWidget_MyWidget extends Extension_CardWidget {
    const ID = 'cerb.card.widget.my_widget';

    function render(Model_CardWidget $widget, $context, $context_id) {
        $tpl = DevblocksPlatform::services()->template();
        $tpl->assign('widget', $widget);
        $tpl->display('devblocks:my.plugin::cards/my_widget/render.tpl');
    }
}
```

`plugin.xml` registration (point `cerb.card.widget`):
```xml
<extension point="cerb.card.widget">
    <id>cerb.card.widget.my_widget</id>
    <name>My Widget</name>
    <class><file>api/cards/widgets/my_widget.php</file><name>CardWidget_MyWidget</name></class>
</extension>
```

### Card vs Profile Widgets — same logic, two extensions

Most widgets ship as **both** a card widget and a profile widget so they work in both the peek popup and the full profile-page dashboard. They typically share a `Cerb\Records\MyWidget` helper class with the actual logic, plus paired template directories:

```
api/cards/widgets/my_widget.php          → CardWidget_MyWidget
api/profiles/widgets/my_widget.php       → ProfileWidget_MyWidget
api/Records/MyWidget.php                 → shared logic
templates/internal/cards/widgets/my_widget/render.tpl
templates/internal/profiles/widgets/my_widget/render.tpl
```

The two extensions are usually thin wrappers around the same render — the only template difference is `#cardWidget{$widget->getUniqueId(...)}` vs `#profileWidget{$widget->id}` for the container ID.

See `profile-widgets.md` for the profile-specific configuration pattern (`contexts` param, ticket/record chooser, placeholder resolution).

### Widget Self-Refresh Events

A widget can request a re-render of itself or of every other widget on the same card.

```js
// One widget — server re-renders the named widget into its content slot
$popup.triggerHandler($.Event('cerb-widget-refresh', { widget_id: {$widget->id} }));

// All widgets on the card
$popup.triggerHandler($.Event('cerb-widgets-refresh', { widget_ids: [] }));

// Specific list
$popup.triggerHandler($.Event('cerb-widgets-refresh', { widget_ids: [42, 43] }));
```

Listeners live in `templates/internal/cards/card.tpl` (`$popup.on('cerb-widget-refresh', …)` / `$popup.on('cerb-widgets-refresh', …)`).

From inside a widget render template, get `$popup` via:
```js
const $popup = genericAjaxPopupFind($widget);
```

Use this when widget state changes outside the widget itself — e.g. the Monitor widget polls a queue job and fires `cerb-widget-refresh` when the job transitions to DONE so the widget redraws (revealing a download list, removing controls, etc.).

### Render Lifecycle

When a widget refreshes, the framework swaps the widget's `.cerb-card-widget--content` HTML via `$widget.html(html)`. Per-render JS bindings (peek triggers, button handlers, listeners) must run inside the widget template's `$(function(){...})` block — they get re-attached every refresh because they reference newly-created DOM. Stash long-lived state on `$widget.data(...)` if you need to survive a refresh; see `queue_job_monitor/render.tpl` for the "generation guard" pattern that cancels stale callbacks across refreshes.

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
