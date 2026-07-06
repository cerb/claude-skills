# plugin.xml Reference

Every Cerb plugin/feature declares its manifest in `plugin.xml`. This file registers class loaders, declares extension points contributed to the platform, and specifies dependencies.

## Top-Level Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plugin xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.devblocks.com/schema/plugin.xsd">
    <id>plugin.id.here</id>
    <name>Human-Readable Plugin Name</name>
    <description>Brief description of the plugin.</description>
    <author>Author Name</author>
    <version>0.0.1</version>
    <link>https://cerb.ai/</link>
    <image>resources/plugin.png</image>

    <!-- PHP class loader paths -->
    <class_loader>
        <file path="api/App.php">
            <class name="MyClass"/>
            <class name="AnotherClass"/>
        </file>
    </class_loader>

    <!-- Declared extensions -->
    <extensions>
        <!-- ... -->
    </extensions>
</plugin>
```

## Class Loader

Maps PHP class names to source files. Classes are autoloaded on demand.

```xml
<class_loader>
    <file path="api/App.php">
        <class name="Controller_MyPlugin"/>
        <class name="DAO_MyRecord"/>
        <class name="Model_MyRecord"/>
        <class name="SearchFields_MyRecord"/>
        <class name="View_MyRecord"/>
        <class name="Context_MyRecord"/>
    </file>
    <file path="api/dao/my_record.php">
        <class name="DAO_MyRecord"/>
    </file>
</class_loader>
```

## Extension Points

### devblocks.context — Record Types

```xml
<extension point="devblocks.context">
    <id>cerb.contexts.my.record</id>
    <name>My Record</name>
    <class>
        <file>api/App.php</file>
        <name>Context_MyRecord</name>
    </class>
    <params>
        <param key="alias" value="my_record"/>
        <param key="icon" value="collection"/>
        <param key="dao_class" value="DAO_MyRecord"/>
        <!-- Optional: show in search, worklist, etc. -->
        <param key="show_in_setup" value="1"/>
        <param key="options">
            <value>
                <data key="avatars" />
                <data key="cards" />
                <data key="comments" />
                <data key="custom_fields" />
                <data key="links" />
                <data key="records" />
                <data key="search" />
                <data key="watchers" />
                <data key="workspace" />
            </value>
        </param>
    </params>
</extension>
```

**Options** are feature toggles read by core templates via `$context_ext->hasOption('foo')`. Common keys: `avatars` (gates the 75×75 image header in `card.tpl`/`profile.tpl`), `cards` (record peek cards), `comments`, `custom_fields`, `links`, `records`, `search`, `watchers`, `va_variable`, `workspace`. Omit options your record type doesn't support — extra options can light up dead UI.

**Icon** (`<param key="icon" value="<cerb-icons name>"/>`) gives the record type a canonical glyph, read via `Extension_DevblocksContext::getIcon()` (`params['icon'] ?? 'circle'`; instance method, so `getByAlias($alias, true)`). Every built-in context carries one; consumers: the KATA `record_type:` autocomplete, Setup → Records (sidebar + section headers), and the global search menu. Custom record types are dynamic contexts built in `Extension_DevblocksContext::getAll()` — they default to `collection` and read a per-record override from `params['icon']` (picked with `CerbUI.IconPicker` in the custom-record peek, sanitized against `getCerbIcons()` on save). The name list + SVG geometry live in `getCerbIcons()` (`libs/devblocks/api/services/ui.php`) + `cerb-icons.scss` (`composer build-css`) — see the `cerb-icons` skill.

> **After any plugin.xml edit, hit `/update` in the browser** (or run the Devblocks update CLI) to reload the manifest cache. `composer cache-clear` alone clears Smarty/compiled-template caches but does *not* reload plugin manifests, so newly added options / class loader entries / extensions won't be visible until `/update`.

### cerberusweb.page — UI Pages

```xml
<extension point="cerberusweb.page">
    <id>cerb.page.my_page</id>
    <name>My Page</name>
    <class>
        <file>api/App.php</file>
        <name>Controller_MyPage</name>
    </class>
    <params>
        <param key="uri" value="my_page"/>
    </params>
</extension>
```

### cerberusweb.ui.page.section — Page Sections

```xml
<extension point="cerberusweb.ui.page.section">
    <id>cerb.page.section.profiles.my_record</id>
    <name>My Record Profile</name>
    <class>
        <file>api/App.php</file>
        <name>PageSection_ProfilesMyRecord</name>
    </class>
    <params>
        <param key="uri" value="my_record"/>
        <param key="page_id" value="cerberusweb.pages.profiles"/>
    </params>
</extension>
```

### cerberusweb.cron — Scheduled Jobs

```xml
<extension point="cerberusweb.cron">
    <id>cerb.cron.my_job</id>
    <name>My Job</name>
    <class>
        <file>api/App.php</file>
        <name>Cron_MyJob</name>
    </class>
    <params>
        <param key="locked" value="0"/>
    </params>
</extension>
```

### cerberusweb.cards.widget — Card Widgets

```xml
<extension point="cerberusweb.cards.widget">
    <id>cerb.card.widget.my_widget</id>
    <name>My Widget</name>
    <class>
        <file>api/App.php</file>
        <name>CardWidget_MyWidget</name>
    </class>
    <params/>
</extension>
```

### cerb.search.index — Search Index Backends

```xml
<extension point="cerb.search.index">
    <id>cerb.search.index.my_backend</id>
    <name>My Search Backend</name>
    <class>
        <file>api/App.php</file>
        <name>SearchIndex_MyBackend</name>
    </class>
    <params/>
</extension>
```

### cerb.automation.api_command — Automation Commands

```xml
<extension point="cerb.automation.api_command">
    <id>cerb.automation.api_command.my_command</id>
    <name>my.command</name>
    <class>
        <file>api/App.php</file>
        <name>AutomationApiCommand_MyCommand</name>
    </class>
    <params/>
</extension>
```

### cerb.portal — Community Portals

```xml
<extension point="cerb.portal">
    <id>cerb.portal.my_portal</id>
    <name>My Portal</name>
    <class>
        <file>api/App.php</file>
        <name>Portal_MyPortal</name>
    </class>
    <params>
        <param key="template_set" value="portal/my_portal"/>
    </params>
</extension>
```

## Dependency Declaration

Plugins can declare dependencies on other plugins:

```xml
<requires>
    <api_version>3.0.0</api_version>
    <plugin id="cerberusweb.core" version="11.0"/>
</requires>
```

## Tips

- The `<id>` for extensions must be globally unique across all plugins.
- `<class><file>` paths are relative to the plugin root.
- Extension point IDs in `<extension point="...">` must match a declared extension point somewhere in the platform.
- Changes to `plugin.xml` require a cache clear to take effect: `composer cache-clear`.
