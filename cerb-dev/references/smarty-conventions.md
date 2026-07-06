# Smarty template conventions

Cerb runs **Smarty 4.x**. House-style rules for `.tpl` files.

## Never use the `@` modifier prefix (`|@func`)

`{$arr|@count}` is a **Smarty 2 relic**. Back then modifiers auto-mapped over each array element, and the
`@` forced the modifier onto the array *as a whole*. Smarty 3+ dropped that mapping — modifiers always
apply to the variable as-is — so the `@` is a **no-op** kept only for back-compat. `{$arr|@count}` and
`{$arr|count}` are identical.

- **Always write the bare modifier:** `{$arr|count}`, never `{$arr|@count}`. The repo is swept clean of
  `|@` — keep it that way (`grep -rn '|@' --include='*.tpl' features plugins` should stay empty).
- `count` works as a modifier because Cerb's Smarty allows PHP-function modifiers (used 12+ places). If you
  want array-counting out of the view entirely, precompute in the controller `render()` and assign it
  (e.g. `$board['counts']['done']`), then `{$board.counts.done}`.

## Other established Smarty house-style (checklist)

- **No *unregistered* `Foo::method()` / `Foo::CONST` in templates** — triggers the `[16384]` deprecation.
  Resolve in the section's PHP `render()` and `$tpl->assign(...)`; instance calls (`$obj->method()`) are
  fine. A `registerClass` whitelist (`DevblocksPlatform`, `Extension_DevblocksContext`, `Page_Profiles`,
  many `DAO_*`) IS sanctioned in-template — don't over-resolve those into PHP.
- **Wrap JS/JSON `{` in `{literal}`** — a `{` immediately followed by a non-space (`{key:1}`, `{}`,
  `=> {…}`) parses as a Smarty tag and breaks compilation. Keep real Smarty tags outside the `{literal}`.
  This **also bites JS comments** — `// e.g. {code: 'x'}` or `// echoes {{token}}` compile-500 the file; reword
  the braces out of the comment (or `{literal}`-wrap it). A common offender is an inline **options object** —
  `new Event('change', {bubbles:true})` 500s (the `{bubbles:` is a bare `{`+non-space). When the listener is
  bound **directly on the element** (not delegated), bubbling is irrelevant, so drop the object:
  `new Event('change')`. Likewise prefer a space after `{` in unavoidable object literals (`{ key: 1 }`) so
  Smarty treats it as literal.
- **`{literal}` can't live inside an `{include}` attribute value.** `{include … placeholder="e.g. {literal}{{x}}{/literal}"}`
  fails — the `{{x}}` parses as a tag before `{literal}` takes effect. Pre-build the string first:
  `{capture assign="ph"}e.g. {literal}{{x}}{/literal}{/capture}` then `{include … placeholder=$ph}`. (The `\"`
  escape for literal double-quotes *inside* an `{include "..."}` arg does work, e.g. `placeholder="say \"hi\""`.)
- **`{$x|default:true}` overrides an explicit `false`.** Smarty's `default` modifier fires on *any* empty/falsy
  value, so a deliberately-`false` include param (e.g. `gutter=false`) comes back `true`. To honor an explicit
  boolean, branch on presence: `{$g = true}{if isset($gutter)}{$g = $gutter}{/if}`.
- **Output is auto-escaped** by the registered `devblocks_autoescape` variable filter — `{$x}` is already
  `htmlspecialchars`'d. So don't add `|escape` (double-encodes), and a `value="{$x}"` / textarea body is safe by
  default; reach for `{$x nofilter}` only for known-safe pre-built HTML (see the sanitize-in-PHP rule below).
- **Smarty expression limits (each is a hard compile 500):** Cerb's Smarty rejects (a) a **ternary inside an
  array literal** — `{$row = ['role' => ($a ? 2 : 1)]}`; (b) a ternary with an **unparenthesized condition** —
  `{$x = $obj->prop ? 2 : 1}` (every working ternary parenthesizes: `{$x = ($obj->prop) ? 2 : 1}`); (c)
  **appending an array literal** — `{$arr[] = ['k'=>v]}`. Safe pattern: compute with `{if}/{else}` + scalar
  assigns, build the row as a keyed array literal of plain vars, then append a **variable**
  (`{$arr[] = $row}`). Keyed literals with `=>` and property/var values are fine (`['url' => $x->name]`).
- **Diagnose template 500s in the php-fpm log, NOT the browser.** A Smarty compile error is an uncaught
  exception → bare 500 (no body, because `display_errors` is off) → logged to the **FPM/Apache error log**
  (`docker logs <php-fpm>`), not `storage/logs/` or the console. To verify a template compiles without a
  browser/auth, fetch it in-container: bootstrap Devblocks + `services()->template()->fetch('devblocks:cerberusweb.core::<path>.tpl')`
  in a try/catch — a `Smarty Compiler: Syntax error` = real bug; a `getX() on null`-style runtime stop = the
  template compiled (your dataless harness just hit a null model). See `references/peek-edit-patterns.md`.
- **Sanitize in PHP, emit `{$x nofilter}`** — don't lean on Smarty auto-escape (it double-escapes JSON
  quotes, etc.). Sanitize/encode via `DevblocksPlatform` / `json_encode` in PHP, then `{$x nofilter}` in
  the template.
- **No 4-byte UTF-8 emoji** in templates — most DB columns aren't `utf8mb4`.
- **`const`/`let`, never `var`** in `<script>` blocks; every inline `<script>`/`<style>` carries
  `nonce="{DevblocksPlatform::getRequestNonce()}"`.
- **`<pre data-cerb-uiref-source>` code samples must entity-escape `<tags>` even inside `{literal}`** —
  `{literal}` only stops *Smarty* parsing, not HTML; write `&lt;span&gt;`.
- Keep existing inline comments; prefer terse single-line `{* … *}`.

Related: `references/css-utilities.md` (the `cerb-u-*` utility layer + the reduce-ad-hoc-CSS methodology),
`references/peek-edit-patterns.md` (peek/checkbox Smarty gotchas), `references/security.md` (POST/CSRF/
`importGPC`).
