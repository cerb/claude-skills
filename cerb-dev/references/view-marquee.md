# View Marquee Reference

Worklist marquees are the inline notification banner above a worklist (e.g. "New ticket created: …" after a profile save, "Imported 250 records" after a CSV upload). Used 80+ times across the codebase.

## API

`C4_AbstractView::marqueeAppend($view_id, $string)` — appends an HTML message to the marquee for a worklist. Multiple appends accumulate; all flush on next render.

`C4_AbstractView::_marqueeFlush($view_id)` — pops and returns the queued messages (called automatically by `view_marquee.tpl` when the view renders).

**Visit-bound.** Storage is the worker's session (`$visit->append($view_id . '_marquee', $string)`). If `getVisit()` returns null — CLI, cron, queue consumers running stateless in `Devblocks::shutdown()` — the call returns `false` and the message is dropped silently.

For background work that needs to surface a result on the worker's next view render, don't use the marquee. Use a `DAO_Notification`, surface state in a card widget that re-queries on render, or store output as an `attachment_link` to the parent record.

## Rendering

The marquee renders via `internal/views/view_marquee.tpl`. Each per-record-type worklist template (`tickets/view.tpl`, `tasks/view.tpl`, etc.) includes it explicitly. New custom record types should follow that convention.

## Helpers

Two helpers wrap common patterns and call `marqueeAppend` for you:

### `setMarqueeContextCreated($view_id, $context, $context_id)`

For "New X created" after a profile save. Renders one of three forms by capability:

- Context implements `IDevblocksContextPeek` → `<a class='cerb-peek-trigger' data-context='X' data-context-id='Y' data-profile-url='Z'><b>Name</b></a>`
- Context has a `permalink` only → `<a href='url'><b>Name</b></a>`
- Bare → `New X created: <b>Name</b>`

Pattern after a profile save:

```php
$view_id = DevblocksPlatform::importGPC($_POST['view_id'] ?? null, 'string', '');
// ... save record, get $id ...
C4_AbstractView::setMarqueeContextCreated($view_id, CerberusContexts::CONTEXT_MY_RECORD, $id);
```

### `setMarqueeContextImported($view_id, $context, $count)`

For batch outcomes. Renders `Imported <b>N type</b> records.` Plain text, no link.

## Gotcha: `cerb-peek-trigger` requires explicit binding

Marquee anchors emitted with `class="cerb-peek-trigger"` (including those from `setMarqueeContextCreated`) **don't auto-bind** click handlers. `view_marquee.tpl` only wires the close button. There's no global event-delegation handler in `cerberus.js`.

Where this matters: a custom marquee call that renders a peek-trigger anchor will appear visually but clicking it does nothing — unless the host template (or downstream code) calls `$container.find('.cerb-peek-trigger').cerbPeekTrigger()`.

(This is an existing latent bug for the `setMarqueeContextCreated` callers across the codebase. Worth knowing when you're trying to make a marquee link clickable.)

For new code that needs a clickable marquee, prefer `<a href='url'>` (a real navigable link) over `<a class='cerb-peek-trigger'>` unless you're also going to wire the binding.

## XSS

All values must pass through `DevblocksPlatform::strEscapeHtml()`. The helpers do it for you. Direct `marqueeAppend` callers are responsible for their own escaping.
