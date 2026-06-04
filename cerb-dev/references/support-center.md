# Support Center portal plumbing

The Support Center is a public-facing portal in `plugins/cerberusweb.support_center/`. Its server class is `UmScApp` (`api/UmScApp.php`); a portal record is a `community_tool` row (`Context_CommunityTool`, `const ID='cerberusweb.contexts.portal'`, `const URI='community_portal'`).

## Architectural policy: no browser-editable Smarty

Cerb runs **two** template engines on purpose:
- **Twig** — for user/portal-authored, untrusted content. Locked down (sandboxed, no arbitrary PHP/static calls).
- **Smarty** — for app/portal *chrome* (the base `.tpl` files shipped on disk).

The legacy "custom templates" feature (DB-stored Smarty overrides via `devblocks_template`) let portal admins edit base Smarty from the browser. It was **removed in 11.2** — it was an injection surface, blocked shipping security/template fixes, and silently broke portals on upgrade when base templates drifted (e.g. the glyphicons removal). **Do not reintroduce browser-editable Smarty anywhere.** When customers need to customize, give them: a **stylesheet** setting, **Markdown** content, or portal config fields — never editable templates.

## Per-portal settings: `DAO_CommunityToolProperty`

Portal config lives in `community_tool_property (tool_code, property_key, property_value)`, keyed by the portal **code** (not id). DAO in `features/cerberusweb.core/api/dao/community_portal.php`:

```php
DAO_CommunityToolProperty::get($tool_code, $key, $default=null, $json_decode=false);
DAO_CommunityToolProperty::set($tool_code, $key, $value, $json_encode=false);
DAO_CommunityToolProperty::getJson($tool_code, $key, $default=null);   // convenience
DAO_CommunityToolProperty::setJson($tool_code, $key, $value);
DAO_CommunityToolProperty::getAllByTool($tool_code);                   // cached
```

Cached under `um_comtoolprops_{code}`; `set()` invalidates it. In a **patch**, write the row directly (`REPLACE INTO community_tool_property ...`) and clear that cache key via the cache service rather than calling the DAO (see `migration-patch.md`). Define keys as `UmScApp::PARAM_*` constants (e.g. `PARAM_PAGE_TITLE`, `PARAM_LOGO_URL`, `PARAM_SECURITY_CSP_IMG_SRC`).

## Config tabs (render + save)

`UmScApp::renderConfiguration()` / `saveConfiguration()` dispatch on the `config_tab` request var:
- Built-in tabs (`website`) have dedicated `_profileRenderConfigTab*` / `_profileSaveConfigTab*` methods. The `website` tab template (`templates/portal/sc/profile/tabs/configuration/website.tpl`) is the canonical example of a config form: it POSTs to the `community_portal` profile action `saveConfigTabJson` with `config_tab=website`, loads values with `DAO_CommunityToolProperty::get`, saves them in `_profileSaveConfigTabWebsite`.
- **Module** tabs route through the `default` arm to the controller's `configure($portal)` (render) and `saveConfiguration($portal)` (save) — `Extension_UmScController`. To add a savable field to a module tab, implement `saveConfiguration()` on that controller and POST `config_tab=<uri>` from its config template.

## Portal endpoints (controllers)

Each portal URL segment is a `usermeet.sc.controller` extension with a `uri` param, class extends `Extension_UmScController` (files in `api/sc/uri/*.php`). `writeResponse()` emits the response; a controller can serve raw bytes (see `api/sc/uri/avatar.php` for a binary/`Content-Type` example — mirror it to serve CSS/JSON/etc.). Utility controllers that shouldn't appear as nav items are force-hidden (visibility `0`) via the hidden-module list in `website.tpl` (e.g. `sc.controller.ajax`, `sc.controller.avatar`).

## Markdown rendering

`DevblocksPlatform::parseMarkdown($text, $safeMode=false, $externalLinks=false)` (`libs/devblocks/Devblocks.class.php:1768`) — league/commonmark + GFM, filters dangerous HTML. Smarty modifier `|devblocks_markdown_to_html[:safeMode]`. Use this (not editable templates) for admin-authored portal content; render in PHP and pass the HTML to the template to avoid static-calls-in-Smarty.

## Portal ACL gotcha

`Context_CommunityTool::isReadableByActor()` and `isWriteableByActor()` both return `CerberusContexts::allowEverything()` — a portal is **readable by any worker** (write is effectively gated earlier by the portal `update` priv; there's no per-record delegate). So anything whose visibility *inherits portal readability* (e.g. a linked file attachment's download check) is exposed to all workers. For admin-only data tied to a portal, use a superuser-gated channel instead — see the changeset trick in `record-changeset.md`.
