---
id: "docs-plugins"
title: "Plugins"
url: "https://cerb.ai/docs/plugins/"
summary: "This page provides a comprehensive guide on using plugins in Cerb to enhance and customize its functionality without conflicting with the core platform updates. It explains the structure and components of plugins, including IDs, manifests, extensions, events, patches, classloader, permissions, translations, resources, templates, and activity points. The page details how plugins can integrate with third-party services, add new record types, augment automations, and expand workspaces and dashboards. It also covers the requirements and dependencies for plugins, how to register extensions, and the use of the Smarty template engine for plugin templates. Additionally, it outlines the library of features, authentication, integration, legacy components, localization, record types, and storage options available through plugins. The guide emphasizes the importance of using plugins to maintain simplicity and efficiency in Cerb while allowing for extensive customization and functionality expansion."
tags: ["docs"]
---
While Cerb's source code is 100% public, any customizations you make to the platform itself will likely _"conflict"_ with ongoing improvements made by the official developers. This makes it more difficult for you to upgrade.

You can avoid these issues by using **plugins** – optional bundles of files that seamlessly contribute new functionality to Cerb.

Even the built-in functionality in Cerb is contributed by plugins. This way, as we continue to improve Cerb, we're also automatically expanding the ability for other people to build their own customizations too.

Common uses for plugins are:

- Integration with third-party services
- Adding new record types
- Augmenting automations with new events and commands
- Expanding workspaces and dashboards with new widgets and data sources
- …and much more

Plugins also allow unused functionality to be removed to keep everything simpler and more efficient.

- IDs
- Structure
- Manifests
  - Plugin metadata
  - Requirements
  - Dependencies
  - Everything else

- Extensions
  - Extension points

- Events
- Patches
- Classloader
- Permissions
- Translations
- Resources
- Templates
- Activity Points
- Library
  - Features
  - Authentication
  - Integration
  - Legacy
  - Localization
  - Record Types
  - Storage

### IDs

Every plugin must have a unique ID comprised of lowercase letters (`a-z`), numbers (`0-9`), underscores (`_`), and dots (`.`).

By convention, the first segment of a plugin's ID is a namespace unique to its author. One way to ensure uniqueness is to base your namespace on a domain name you own.

For instance: `com.example.plugin_name`

### Structure

Every plugin is a directory with the same name as its ID, using the following filesystem structure:

| Path | Description |
| --- | --- |
| **`api/`** | Extensions |
| **`patches/`** | Patches |
| **`resources/`** | Resources (images, scripts, stylesheets) |
| **`templates/`** | Templates |
| `plugin.xml` | Manifest |
| `strings.xml` | Translations |

The minimal set of plugins required for Cerb to work properly are called **features**. You'll find them in the `features/` directory.

Third-party plugins are found in the `storage/plugins/` directory. These plugins are installed and automatically updated from the Plugin Library.

# Manifests

Each plugin must have a **manifest** file named `plugin.xml` that describes its contents. This tells Cerb what kinds of new functionality the plugin is contributing.

Here's a minimal manifest:

```
<?xml version="1.0" encoding="UTF-8"?> <plugin xmlns:xsi= "http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation= "http://www.devblocks.com/schema/plugin.xsd" > <id>example.plugin</id> <name>Plugin Name</name> <description>This explains what your plugin does.</description> <author>Webgroup Media, LLC.</author> <version>0.0.0</version> <link>https://cerb.example/path/to/docs</link> <image>plugin.png</image> <requires> <app_version min= "11.0" max= "11.0.99" /> <!--<php_extension name="curl" />--> </requires> <dependencies> <require plugin_id= "cerberusweb.core" version= "11.0.0" /> </dependencies> <patches/> <class_loader/> <event_points/> <acl/> <activity_points/> <extensions/> </plugin>
```

### Plugin metadata

- **`<id>`** is the globally unique ID of the plugin, prefixed with the author's namespace. This should only contain lowercase letters (`a-z`), numbers (`0-9`), underscore (`_`), and dots (`.`).

- **`<name>`** is the human-friendly name of the plugin.

- **`<description>`** is a brief description of the purpose and contributions of the plugin.

- **`<author>`** is the name used for attribution of the plugin's author.

- **`<version>`** is the semantic version of the plugin in `<generation>.<major>.<minor>` format. This should start with `0.0.0` and be incremented for each update.

- **`<link>`** is a URL to the plugin's documentation page.

- **`<image>`** is a path to the plugin's icon. This is relative to the plugin's `resources/` directory.

### Requirements

The **`<requires>`** block specifies the requirements for installing and enabling this plugin.

This block must contain one **`<app_version>`** element specifying the minimum and maximum version of Cerb that are verified compatible with this build of the plugin.

The block may contain any number of **`<php_extension>`** elements if specific PHP extensions are required for the plugin to operate (e.g. `ldap`, `oauth`, `zip`).

### Dependencies

The optional **`<dependencies>`** block specifies if this plugin depends on another plugin.

This block may contain any number of **`<require>`** elements specifying a required `plugin_id` and its minimum compatible `version`.

### Everything else

The other elements will be covered in more detail in the subsequent sections:

- **`<extensions>`**
- **`<event_points>`**
- **`<patches>`**
- **`<class_loader>`**
- **`<acl>`**

# Extensions

Plugins contribute new functionality by registering **extensions** on **extension points**.

Extensions are defined in a plugin's manifest within the **`<extensions>`** block.

Each extension entry looks like:

```
<extension point= "com.example.extension_point" > <id>com.example.extension_name</id> <name>Extension name</name> <class> <file>relative/path/to/file.php</file> <name>Class_Name</name> </class> <params/> </extension>
```

- **`<extension point="...">`** specifies the extension point of the extension.

- **`<id>`** is the globally unique ID of the extension. Like plugins, this should only contain lowercase letters (`a-z`), numbers (`0-9`), underscores (`_`), and dots (`.`). The extension ID should always start with the ID of the plugin.

- **`<name>`** is the human-friendly name of the extension.

- **`<class>`** assigns code from the plugin to the extension. Each extension point provides a parent _class_ which must be _extended_ by the plugin's extension. The **`<name>`** element in this block specifies the class name of this implementation, and **`<file>`** is the path to a source code file, relative to the plugin's directory. This almost always starts with `api/`.

- **`<params>`** is where each extension manifest can set configuration details based on the extension point.

## Extension points

| Name | Extension Point |
| --- | --- |
| Automation Trigger | `devblocks.event.action` |
| Bot Action | `devblocks.event.action` |
| Bot Event | `devblocks.event` |
| Cache Engine | `devblocks.cache.engine` |
| Calendar Datasource | `cerberusweb.calendar.datasource` |
| Card Widget Type | `cerb.card.widget` |
| Community Portal | `cerb.portal` |
| Connected Service Provider | `cerb.connected_service.provider` |
| Controller | `devblocks.controller` |
| Custom Field Type | `cerb.custom_field` |
| Event Listener | `devblocks.listener.event` |
| Http Request Listener | `devblocks.listener.http` |
| Mail Transport Type | `cerberusweb.mail.transport` |
| Page Menu Item | `cerberusweb.ui.page.menu.item` |
| Page Section | `cerberusweb.ui.page.section` |
| Page Type | `cerberusweb.page` |
| Prebody Renderer | `cerberusweb.renderer.prebody` |
| Profile Tab Type | `cerb.profile.tab` |
| Profile Widget Type | `cerb.profile.tab.widget` |
| Record Type | `devblocks.context` |
| Resource Type | `cerb.resource.type` |
| Rest API Controller | `cerberusweb.rest.controller` |
| Scheduled Job | `cerberusweb.cron` |
| Search Engine | `devblocks.search.engine` |
| Search Schema | `devblocks.search.schema` |
| Sensor Type | `cerberusweb.datacenter.sensor` |
| Storage Engine | `devblocks.storage.engine` |
| Storage Schema | `devblocks.storage.schema` |
| Support Center Controller | `usermeet.sc.controller` |
| Support Center Login Authenticator | `usermeet.login.authenticator` |
| Support Center RSS Feed | `usermeet.sc.rss.controller` |
| Workspace Page Type | `cerberusweb.ui.workspace.page` |
| Workspace Tab Type | `cerberusweb.ui.workspace.tab` |
| Workspace Widget Datasource | `cerberusweb.ui.workspace.widget.datasource` |
| Workspace Widget Type | `cerberusweb.ui.workspace.widget` |

# Events

Plugins can add new **events** to Cerb based on the contributed functionality. The activity log will record the new events on records, automations can listen for them, etc.

```
<event_points> <event id= "example.event" > <name>Example Event</name> <param key= "field_name" /> </event> </event_points>
```

- **`<event id="...">`** specifies the ID of the event.

- **`<name>`** is the human-friendly name of the event.

- **`<param key="...">`** is a list of available parameters on the event.

If you create a Bot Event extension you do not need to add a separate event here.

# Patches

Plugins that need to maintain a _schema_ in the database can do so with **patches**. A patch is a collection of changes used to migrate data between versions during an upgrade.

When you skip several versions of a plugin to upgrade to the latest version, Cerb will automatically handle the migration of your data through the intervening versions. This is the same thing that happens when you upgrade Cerb itself.

```
<patches> <patch version= "9.0.0" revision= "1" file= "patches/9.0.0.php" /> </patches>
```

# Classloader

The **class loader** is a map of source code classes and their filesystem paths. This enables Cerb to efficiently only load the files necessary to serve a specific request.

If your plugin introduces classes that will be referenced by code outside of the plugin, you should register them here. Class loader entries are automatically created for any extensions you register.

```
<class_loader> <file path= "api/dao/example.php" > <class name= "Context_Example" /> <class name= "DAO_Example" /> <class name= "Model_Example" /> <class name= "Plugin_Example" /> <class name= "SearchFields_Example" /> <class name= "View_Example" /> </file> </class_loader>
```

# Permissions

Plugins can introduce new privileges into roles.

```
<acl> <priv id= "example.permission" label= "acl.example.permission" /> </acl>
```

- **`id="..."`** is the ID of the new privilege. This uses dot-notation like plugins and extensions. It should also use your plugin ID as a namespace prefix.

- **`label="..."`** is the translation ID of the human-readable label for the privilege.

# Translations

Most of the text you see in Cerb is provided by the **translation** system using _American English_ defaults. All of this text is able to be translated into any other language using our built-in Translation Editor plugin.

Plugins can add new text to the translation system with a `strings.xml` file in TMX format, which can then be translated into any language by anyone, as well as shared in our official translation packs.

```
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE tmx PUBLIC "-//LISA OSCAR:1998//DTD for Translation Memory eXchange//EN" "tmx14.dtd"> <tmx version= "1.4" > <header creationtool= "Cerb" creationtoolversion= "11.1.0" srclang= "en_US" adminlang= "en" datatype= "unknown" o-tmf= "unknown" segtype= "sentence" creationid= "" creationdate= "" /> <body> <tu tuid= 'example.plugin.string_name' > <tuv xml:lang= "en_US" ><seg>Replace this with your own text.</seg></tuv> </tu> </body> </tmx>
```

# Resources

Plugins can add new sharable resources like:

- Images

- Scripts (Javascript)

- Stylesheets

These must be stored in the `resources/` directory within the plugin.

Resources can then be accessed by URL with the format:

`/resource/` **`<plugin-id>`** `/path/to/resource/file.ext`

In templates:

```
{ devblocks_url }c=resource&plugin=example.plugin&f=path/to/resource/file.ext{/ devblocks_url }
```

From bot scripting:

```
{{ cerb_url ( 'c=resource&plugin=example.plugin&f=path/to/resource/file.ext' ) }}
```

All plugin resources are public (world readable) and do not require a valid session to access. Do not store private content in this directory.

# Templates

Cerb plugins use the Smarty template engine.

Templates are stored in the plugin's `templates/` directory.

They are referenced from plugin code like:

```
$tpl = DevblocksPlatform :: services () -> template (); $tpl -> assign ( 'name' , 'Kina Halpue' ); $tpl -> display ( 'devblocks:example.plugin::path/to/template.tpl' );
```

In `->display()`, `example.plugin` should be your plugin's ID. The `path/to/` is relative to the plugin's `templates/` directory.

Here's an example template:

```
<div>
	Hello, <b> { $name } </b>!
</div>
```

# Activity Points

We previously mentioned **events** when discussing automations and the activity log. Plugins can add new events to Cerb based on the contributed functionality. The activity log will record the new events on records, automations can listen for them, etc.

```
<activity_points> <activity point= "example.event" > <param key= "label_key" value= "Example Event" /> <param key= "string_key" value= "activities.example_event" /> <param key= "options" value= "api_create, notifications" /> </activity> </activity_points>
```

# Library

### Features

| Devblocks | `devblocks.core` |
| Cerb Core | `cerberusweb.core` |
| Chat Bots | `cerb.bots.portal.widget` |
| Knowledgebase | `cerberusweb.kb` |
| Project Boards | `cerb.project_boards` |
| Support Center | `cerberusweb.support_center` |
| Web Services API (JSON/XML) | `cerberusweb.restapi` |
| Webhooks | `cerb.webhooks` |

### Authentication

| LDAP Integration | `wgm.ldap` |

### Integration

| JIRA Integration | `wgm.jira` |

### Legacy

| Legacy Printing | `cerb.legacy.print` |
| Legacy Profile Attachments Download | `cerb.legacy.profile.attachments` |
| Ticket Profile "Move To" Shortcut | `cerb.profile.ticket.moveto` |
| Notifications Emailer | `wgm.notifications.emailer` |
| Record Simulator | `cerberusweb.simulator` |

### Localization

| Translation Editor | `cerberusweb.translators` |

### Record Types

| Call Logging | `cerberusweb.calls` |
| Collaborative Feed Reader | `cerberusweb.feed_reader` |
| Domains | `cerberusweb.datacenter.domains` |
| Feedback Capture | `cerberusweb.feedback` |
| Opportunity Tracking | `cerberusweb.crm` |
| Sensors | `cerberusweb.datacenter.sensors` |
| Servers | `cerberusweb.datacenter.servers` |
| Time Tracking | `cerberusweb.timetracking` |

### Storage

| S3 Gatekeeper Storage Engine | `wgm.storage.s3.gatekeeper` |

