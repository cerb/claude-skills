# Dark-mode flash-of-white (FoUC) on full-page templates

## Problem

Cerb full-page HTML templates (`<!DOCTYPE html><html {if $pref_dark_mode}class="dark">`)
paint the browser's default **white** canvas for a split second before `cerb.css`
loads and the `.dark` class applies its background (`--cerb-color-background`).
In dark mode this reads as a bright white flash. It's most visible on pages that
reload frequently — e.g. **explore mode**, where paging does a full page reload
on every next/prev submit.

Two distinct surfaces flash, with different fixes:

1. **The page's own canvas** (the document itself, incl. the navigation gap between
   full-page reloads).
2. **An `<iframe>`'s inner document** (explore mode loads record profiles into
   `#explorerFrame` via `header.tpl` → `border.tpl`). Styling the iframe *element*
   dark is not enough — once the inner document starts painting, its own canvas
   covers the element background.

Relevant files: `templates/header.tpl` (the app shell every full page renders
through), `templates/explorer/index.tpl`, `templates/explorer/automation/index.tpl`.
Dark background value = `rgb(32,32,32)` (`.dark` scope, `cerb.css` /
`cerb-theme.scss`). It must be **hardcoded inline** — `--cerb-color-background`
isn't defined until `cerb.css` loads, which is the exact gap being covered.

## Fix (three layers, apply what the surface needs)

### 1. `color-scheme` meta — kills the canvas / navigation-backdrop flash

Add to `<head>`, gated to emit the real value both ways so native controls +
scrollbars theme correctly:

```smarty
<meta name="color-scheme" content="{if $pref_dark_mode}dark{else}light{/if}">
```

Read during early HTML parsing (before the CSSOM is built), so the browser uses a
**dark canvas** for the pre-paint / navigation backdrop instead of white. This is
the primary cure for "flashes white before going dark" on a normal page load.
Added to `header.tpl` (fixes it app-wide, incl. the forced-dark login flow) and
both explorer chrome templates.

### 2. Inline dark `background-color` on the chrome

In the template's own `<style>` block, belt-and-suspenders for the chrome canvas:

```smarty
{if $pref_dark_mode}
HTML, BODY, IFRAME { background-color: rgb(32,32,32); }
{/if}
```

### 3. Hide an iframe until its `load` event — the decisive fix for iframe content

`color-scheme` + a dark element background still leave a residual flash inside an
iframe: at the very start of the iframe navigation the browser paints the incoming
document's default **white** canvas before its `color-scheme` meta is processed.
CSS alone can't win that race. Instead, hide the frame until it has painted, then
reveal it — the dark outer background shows through during load:

```smarty
{if $pref_dark_mode}
#explorerFrame { visibility: hidden; }
{/if}
```

```javascript
// in the existing iframe 'load' handler (funcOnLoad), before the try/focus:
$explorerFrame.css('visibility', 'visible');   // no-op in light mode
```

Notes:
- Gate the initial hide on `{if $pref_dark_mode}` so **light mode is unchanged**
  (white loading is expected there); the JS reveal runs unconditionally and is a
  harmless no-op when the frame was never hidden.
- The reveal must run **outside** the `try {}` that touches `.contents()`, so a
  cross-doc access error can't leave the frame permanently hidden.
- `visibility:hidden` (not `display:none`) keeps the frame laid out and still
  loads/executes its inner document normally.
- The `load` event waits on subresources; if the reveal feels laggy on heavy
  pages, switch to the inner frame's `DOMContentLoaded` for a snappier reveal.

## Gotchas

- **Recompile templates** after any `.tpl` edit: `composer cache-clear`. A stale
  compiled `header.tpl` will silently drop the meta and look like the fix "didn't
  work."
- There was no pre-existing inline-dark-background pattern in the codebase before
  this — `header.tpl`, `border.tpl`, and login all relied purely on `cerb.css`.
  These three layers are that pattern now; reuse them for any new full-page
  template.
- Only four templates emit their own `<html {if $pref_dark_mode}class="dark">`:
  `header.tpl`, `explorer/index.tpl`, `explorer/automation/index.tpl`,
  `error_page.tpl`. Everything else is a fragment wrapped by `border.tpl` →
  `header.tpl`, so fixing `header.tpl` covers the whole app.
