# Profile Widget Reference

## Registering a Profile Widget (`cerb.profile.tab.widget`)

```xml
<extension point="cerb.profile.tab.widget">
    <id>cerb.profile.tab.widget.my_widget</id>
    <name>My Widget</name>
    <class>
        <file>api/profiles/widgets/my_widget.php</file>
        <name>ProfileWidget_MyWidget</name>
    </class>
    <params>
    </params>
</extension>
```

## `contexts` param — restricting which profile types can use the widget

Add a `<param key="contexts">` block to limit the widget to specific profile record types. The UI will only offer the widget when adding/editing a tab on a matching profile.

```xml
<params>
    <param key="contexts">
        <value>
            <data key="cerberusweb.contexts.ticket" />
            <data key="cerberusweb.contexts.message" />
            <data key="cerberusweb.contexts.mail.draft" />
        </value>
    </param>
</params>
```

**Omit the `contexts` param entirely** (leave `<params>` empty) to allow the widget on any profile type.

## Config template — ticket/record chooser

When a widget can appear on profiles other than the record it naturally displays, provide a chooser in the config template so the admin can pin a specific record:

```smarty
<fieldset class="peek black">
    <legend>Ticket (when used outside a ticket profile)</legend>
    <b><a class="cerb-chooser-ticket" data-context="{CerberusContexts::CONTEXT_TICKET}" data-single="true">Ticket</a>:</b>
    <div style="margin-left:10px;">
        <input type="text" name="params[ticket_id]" value="{$widget->extension_params.ticket_id}"
            class="placeholders" style="width:95%;padding:5px;border-radius:5px;" autocomplete="off" spellcheck="false">
    </div>
</fieldset>

<script nonce="{DevblocksPlatform::getRequestNonce()}" type="text/javascript">
$(function() {
    var $config = $('#widget{$widget->id}Config');
    var $input = $config.find('input[name="params[ticket_id]"]');
    $config.find('.cerb-chooser-ticket').cerbChooserTrigger()
        .on('cerb-chooser-selected', function(e) {
            {literal}$input.val(e.values[0] + '{# ' + e.labels[0] + ' #}');{/literal}
        });
});
</script>
```

The chooser stores the value as `"123{# Subject #}"`. `intval()` on the result of `$tpl_builder->build()` extracts the numeric ID after placeholder resolution.

## PHP — override with placeholder resolution vs. auto-detect pattern

When the widget supports both a configured ID (with optional placeholders) and auto-detection from the current profile context, resolve the override through `templateBuilder` first, then fall back to context-based detection.

The param value may be a literal ID (`"123"`) or a placeholder expression (`"{{record_ticket_id}}"`) referencing the current profile record's tokens.

Use `DevblocksDictionaryDelegate::instance()` with lazy-loading keys (`record__context`/`record_id`, `widget__context`/`widget_id`) — the dict resolves tokens on demand without pre-loading via `CerberusContexts::getContext`.

```php
$target_ticket_id = $model->extension_params['ticket_id'] ?? null;

if($target_ticket_id) {
    $tpl_builder = DevblocksPlatform::services()->templateBuilder();

    $dict = DevblocksDictionaryDelegate::instance([
        'record__context' => $context,
        'record_id' => $context_id,
        'widget__context' => CerberusContexts::CONTEXT_PROFILE_WIDGET,
        'widget_id' => $model->id,
    ]);

    $ticket_id = intval($tpl_builder->build($target_ticket_id, $dict));

    if($ticket_id)
        $this->_showTicketConversation($ticket_id, $display_options);

} else if($context == CerberusContexts::CONTEXT_TICKET) {
    $this->_showTicketConversation($context_id, $display_options);
} else if($context == CerberusContexts::CONTEXT_MESSAGE) {
    $this->_showMessageConversation($context_id, $display_options);
}
// etc.
```

The `__context`/`_id` suffix convention tells the dict delegate which context to lazy-load tokens from. This is simpler and more efficient than calling `CerberusContexts::getContext` + `merge` manually.

This allows the widget to work on any profile (with a fixed or placeholder-derived ID) while still auto-detecting when placed on its native profile type.
