# Context Avatars

Cerb stores per-record avatar images in `context_avatar`, indexed by `(context, context_id)`. Bytes live in storage (`Storage_ContextAvatar`). The framework serves them, falls back to defaults (silhouettes, building, conversation icon), and ultimately to a deterministic-color monogram.

## Enabling Avatars on a Context

In `plugin.xml`, add `avatars` to the context's options block:

```xml
<param key="options">
    <value>
        <data key="avatars" />
        <data key="cards" />
        <data key="comments" />
        <!-- ... -->
    </value>
</param>
```

This is what `card.tpl:7` and `profile.tpl:16` check via `$context_ext->hasOption('avatars')` before rendering the 75×75 header image. **After editing `plugin.xml` you must hit `/update`** — manifests are cached and the new option won't take effect from cache-clear alone.

## Standard Token Values

In `Context_X::getContext()`, set `_image_url` alongside `_label` and `record_url`:

```php
$url_writer = DevblocksPlatform::services()->url();

$token_values['_loaded'] = true;
$token_values['_label'] = $record->name;
$token_values['_image_url'] = $url_writer->writeNoProxy(
    sprintf('c=avatars&ctx=%s&id=%d', 'my_record', $record->id), true
) . '?v=' . $record->updated_at;
// ...
$token_values['record_url'] = $url_writer->writeNoProxy(
    sprintf("c=profiles&type=my_record&id=%d-%s", $record->id, DevblocksPlatform::strToPermalink($record->name)), true
);
```

`_image_url` surfaces in mention chips, profile cards, placeholders, and anywhere the framework asks "give me this record's image." Mirror the group/contact/worker pattern in `api/dao/group.php:2061`.

## Saving an Avatar from peek_edit

The `peek_edit.tpl` wires up the avatar chooser like this:

```smarty
<img class="cerb-avatar" src="{devblocks_url}c=avatars&context=my_record&context_id={$model->id}{/devblocks_url}?v={$model->updated_at}" style="height:50px;width:50px;">
<button type="button" class="cerb-avatar-chooser" data-context="{CerberusContexts::CONTEXT_MY_RECORD}" data-context-id="{$model->id}">{'common.edit'|devblocks_translate|capitalize}</button>
<input type="hidden" name="avatar_image">
```

The chooser script (`ajax.chooserAvatar`) writes the chosen image data into the hidden `avatar_image` field. The profile action *must* read and persist it — peek-template wiring alone doesn't save anything:

```php
// In _profileAction_savePeekJson, after the record save
$avatar_image = DevblocksPlatform::importGPC($_POST['avatar_image'] ?? null, 'string', '');
DAO_ContextAvatar::upsertWithImage(CerberusContexts::CONTEXT_MY_RECORD, $id, $avatar_image);
```

Empty string means "no change"; a data URL replaces; an explicit removal sentinel deletes. The cascade in `_handleContextDelete` already cleans up `context_avatar` rows when the record itself is deleted — see `references/dao-pattern.md` for the full table list.

## Reusable Monogram Generation

`Controller_Avatars::renderMonogram(string $text, ?string $hash = null)` (public static, `features/cerberusweb.core/api/uri/avatars.php`) renders a 100×100 PNG with white text on a color-hashed background and exits. It auto-truncates to 3 chars, uppercases, picks an optimal font size, and uses `crc32($hash ?: $text)` so the same input always gets the same color.

```php
// First letter, color hashed off a stable identifier (URI not name)
Controller_Avatars::renderMonogram(mb_substr($service->name, 0, 1), $service->uri);
exit;
```

Wire it into your context's default-avatar branch in `Controller_Avatars::_renderDefaultAvatar()`:

```php
case CerberusContexts::CONTEXT_MY_RECORD:
    if($context_id && ($record = DAO_MyRecord::get($context_id))) {
        self::renderMonogram(mb_substr($record->name, 0, 1), $record->uri ?: (string)$record->id);
        return;
    }
    $this->_renderFilePng(APP_PATH . '/features/cerberusweb.core/resources/images/avatars/va.png');
    break;
```

Hash on a stable identifier — URI, opaque token, ID — *not* the name, so the color doesn't drift if an admin renames the record.

## Serving Avatars to Signed-Out Pages

`/avatars` requires an active worker (`Controller_Avatars::handleRequest` at line 32). For anonymous endpoints (the login form's SSO buttons), don't bypass the auth check in `/avatars` — add a narrow, validated endpoint on a controller that's already anonymous. The login flow uses `/sso/_avatar/{uri}` (see `features/cerberusweb.core/api/controllers/sso.php`):

```php
if('_avatar' == $provider_uri) {
    $this->_renderServiceAvatar(array_shift($stack));
    return;
}

private function _renderServiceAvatar($uri) : void {
    if(empty($uri) || !($service = DAO_ConnectedService::getByUri($uri)))
        DevblocksPlatform::dieWithHttpError(null, 404);

    // Only expose avatars for services already exposed elsewhere on this controller
    $service_ids = explode(',', DevblocksPlatform::getPluginSetting('cerberusweb.core', CerberusSettings::AUTH_SSO_SERVICE_IDS, ''));
    if(!in_array($service->id, $service_ids))
        DevblocksPlatform::dieWithHttpError(null, 404);

    if(
        ($avatar = DAO_ContextAvatar::getByContext(CerberusContexts::CONTEXT_CONNECTED_SERVICE, $service->id))
        && !empty($avatar->storage_key)
        && !empty($avatar->content_type)
        && false !== ($contents = Storage_ContextAvatar::get($avatar))
    ) {
        // ... write headers, echo $contents, exit ...
    }

    // Fall through to monogram
    Controller_Avatars::renderMonogram(mb_substr($service->name, 0, 1), $service->uri);
    exit;
}
```

Gate the lookup against an explicit allow-list (here, the SSO services exposed on the login form) so the endpoint can't enumerate every connected service's avatar by URI. Then the login template fetches `{devblocks_url}c=sso&a=_avatar&uri={$sso_service->uri}{/devblocks_url}?v={$sso_service->updated_at}` — no auth needed.

## URL Patterns

`Controller_Avatars::handleRequest` accepts both the full context ID and the alias, so either form works:

```
c=avatars&context=cerberusweb.contexts.my_record&context_id=42
c=avatars&context=my_record&context_id=42
c=avatars&ctx=my_record&id=42         <!-- shorter, used by _image_url -->
c=avatars&type=my_record&id=42        <!-- legacy autocomplete pattern -->
```

All resolve to the same path-based dispatch via `array_values($args)` concat in `url.php`. Always append `?v={$record->updated_at}` (or equivalent) as a cache-bust — the controller sets `Cache-Control: max-age=86400`.
