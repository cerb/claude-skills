# Code-editor KATA autocompletion (+ validation)

How to give a KATA `<textarea>` (Ace editor) live autocompletion, and validate the KATA on save. Two
independent pieces:

1. **Client suggestion map** — a static JS object describing what to suggest at each KATA path, wired onto
   the editor with `cerbCodeEditorAutocompleteKata`. Suggestions are either static or pull from the server.
2. **Server validation schema** (optional but recommended) — a `_CerbApplication_KataSchemas` method that
   `kata()->validate()` checks the saved KATA against. Validation and autocomplete are **authored
   separately** — the schema is *not* auto-converted into suggestions.

Worked reference implementation: the **Metrics Explorer** "Default series" editor — search
`kataSchemaMetricsExplorerSeries` (JS), `metricsExplorerSeries()` (PHP schema),
`metric-names` / `metric-dimensions-series` (dynamic types), and `CardWidget_MetricsExplorer::saveConfig`.

---

## 1. The suggestion map

Live in `features/cerberusweb.core/resources/js/cerberus.js` as keys of the global
`var cerbAutocompleteSuggestions = { … }` object (e.g. `kataSchemaDashboardFilters`,
`kataSchemaMetricDimension`, `kataSchemaMetricsExplorerSeries`). `cerberus.js` is loaded raw — **no build
step**, just edit it.

**Keyed by KATA path.** A path key is the chain of KATA keys from the root to the current cursor, each
ending in `:`, with the **segment before any `/` dropped**. So a document like:

```
series/s0:          ← key `series/s0:`  → path key  "series:"
  metric: …         ← path key  "series:metric:"
  function: …       ← path key  "series:function:"
  filters:
    group_id: …     ← path key  "series:filters:"
```

`''` is the root (top-level keys). The value at each path key is **either**:

- a **static array** — entries are bare strings (`'label:'`) or objects
  `{caption, snippet, docHTML?, score?}`. `snippet` uses Ace tab-stops `${1:placeholder}` and `\n` for
  multi-line block snippets. Example:
  ```js
  'series:': [
      { caption: 'metric:',   snippet: 'metric: ${1}' },
      { caption: 'function:', snippet: 'function: ${1:count}' },
      'label:',
      { caption: 'color:',    snippet: 'color: ${1:#1f77b4}' },
      'filters:'
  ],
  'series:function:': ['count','sum','avg','min','max'],   // value suggestions after `function: `
  ```
- a **dynamic object** `{ type: '<type>', params?: {…} }` — fetched from the server (see below). A path key
  pointing at a *value* (e.g. `'series:metric:'`) suggests the value typed after `metric: `.

**Regex paths.** A `'*'` key may hold a map of regex→suggestions for variable paths (see `kataToolbar`):
`'(.*):?interaction:icon:': { type: 'icon' }`. Use only when the path has variable middle segments.

### Wiring it onto an editor (a `.tpl`)

The textarea needs `data-editor-mode="ace/mode/cerb_kata"`; then chain in a `<script>`:

```smarty
<textarea name="params[series_kata]" data-editor-mode="ace/mode/cerb_kata" class="placeholders">…</textarea>
…
$config.find('textarea.placeholders')
    .cerbCodeEditor()
    .cerbCodeEditorAutocompleteKata({
        autocomplete_suggestions: cerbAutocompleteSuggestions.kataSchemaMetricsExplorerSeries
    });
```

Precedents: `templates/internal/workspaces/tabs/dashboard/config.tpl` (dashboard filters),
`templates/records/types/metric/peek_edit.tpl` (metric dimensions).

---

## 2. Dynamic (server-backed) suggestions

`$.fn.cerbCodeEditorAutocompleteKata` is in `cerberus.js`; its `parseCompletions` (~line 3568) dispatches
each `{type}` to a server action. **Built-in types:** `cerb-uri`, `record-field`, `record-fields`,
`record-fields-value`, `record-type`, `icon`, `automation-inputs`, `automation-command-params`,
`metric-dimensions`, `metric-names`, `metric-dimensions-series`.

Each dynamic branch builds a `FormData` posting `c=ui` + `a=kataSuggestions<Foo>Json` (+ `prefix` = what
the user has typed, + any `params[…]`), then `genericAjaxPost` expects the response to be a **JSON array of
`{caption, snippet, docHTML}`** objects.

### Reading a sibling value (the path helpers)

Dynamic types often need a *sibling* field's value (e.g. dimensions need the metric name). Use
`Devblocks.cerbCodeEditor.getKataTokenPath(null, editor)` (returns the ancestor key chain, each with `:`)
and `getKataRowByPath(editor, path.join(''))` (→ the editor row for that path), then read the value with
`line.match(/[^:]*:\s*(.*)/)`. Example — `metric-dimensions-series` walks up to the enclosing `series/…`
node and reads its `metric:` child:

```js
} else if('metric-dimensions-series' === completions['type']) {
    var key_path = Devblocks.cerbCodeEditor.getKataTokenPath(null, editor);
    while(key_path.length && !/^series\//.test(key_path[key_path.length - 1])) key_path.pop();
    if(key_path.length) {
        key_path.push('metric:');
        var key_row  = Devblocks.cerbCodeEditor.getKataRowByPath(editor, key_path.join(''));
        var matches  = editor.session.getLine(key_row).match(/[^:]*:\s*(.*)/i);
        if(Array.isArray(matches) && 2 === matches.length && -1 === matches[1].indexOf('{{')) {
            formData = new FormData();
            formData.set('c', 'ui');
            formData.set('a', 'kataSuggestionsMetricDimensionJson');
            formData.set('prefix', prefix);
            formData.set('params[metric]', matches[1].trim());
        }
    }
}
```

(`{{…}}` placeholders can't be enumerated — there's no record in the editor's scope — so skip them.)

### Adding a new dynamic type

1. **JS** — add an `else if('<type>' === completions['type']) { … }` branch in `parseCompletions`
   (`cerberus.js`) building the `FormData` (set `c=ui`, `a=kataSuggestions<Foo>Json`, `prefix`, params).
2. **PHP** — add a route `case 'kataSuggestions<Foo>Json': return $this->_uiAction_kataSuggestions<Foo>Json();`
   to `Controller_UI::handleControllerAction` and the method in `features/cerberusweb.core/api/uri/ui.php`.
   Set the JSON content-type and `echo json_encode([...])` of `{caption, snippet, docHTML}` rows, honoring
   `$_POST['prefix']`. Model on `_uiAction_kataSuggestionsMetricNamesJson` /
   `_uiAction_kataSuggestionsMetricDimensionJson`.

---

## 3. Server-side validation schema

`class _CerbApplication_KataSchemas` (`api/Application.class.php`) returns KATA `schema:` documents as
heredocs (`metricDimensions()`, `metricsExplorerSeries()`, `automation()`, …). Accessor:
`CerberusApplication::kataSchemas()->yourSchema()`. Validate in a save path:

```php
$kata = DevblocksPlatform::services()->kata();
if(false === $kata->validate($value, CerberusApplication::kataSchemas()->metricsExplorerSeries(), $error)) {
    $error = 'Default series: ' . $error;
    return false;
}
```

Call sites: `DAO_Metric::onBeforeUpdateByActor` (dimensions_kata), and card widgets via
`Extension_CardWidget::saveConfig(array $fields, $id, &$error)` (decode `EXTENSION_PARAMS_JSON`, validate
the relevant field). The `build` branch of `profiles/card_widget.php::_profileAction_savePeekJson` calls
`saveConfig` before persisting, so a `false` return surfaces inline in the config peek.

### Schema format

```
schema:
  attributes:
    series:                        # a key named `series` (matches `series/<id>:`)
      multiple@bool: yes           # allow many (slash-suffixed) instances
      types:
        object:
          attributes:
            metric:
              required@bool: yes
              types: { string: }
            function:  { types: { string: } }
            label:     { types: { string: } }
            color:     { types: { string: } }
            filters:                       # an OPEN map (arbitrary dimension keys)
              types:
                object:
                  attributePatterns:       # <-- allow unknown keys
                    pattern/dimension:
                      match: *             # glob (`*`) or `/regex/`
                      attributes:
                        types: { string: }
```

Types: `string`, `number`, `bool`, `list`, `object`. Key modifiers: `multiple@bool`, `required@bool`. A
key may list **several alternative types** (e.g. `types: { number: , string: }` to accept an id or a uri).
**Open maps:** an empty `attributes:` means *no children allowed* — to accept arbitrary keys (like
dimension names under `filters:`) you **must** use `attributePatterns: pattern/<id>: { match: *, attributes:
{ types: { string: } } }`. Reuse a sub-schema with `attributes@ref: <name>` + a top-level `definitions:`,
and the same `ref` can be pointed at from multiple places — including recursively (e.g. a `menu` definition
whose `items:` references `menu`, `interaction`, and `behavior`).

---

## Gotchas

- **Spaces only** in KATA indentation — tabs are a parse error. `_buildSeriesKata`-style emitters must use
  spaces.
- `#` starts a comment **only at the start of a (trimmed) line** — inline `color: #1f77b4` is a value, safe.
- Empty `attributes:` ≠ "any keys" — it's "no keys." Use `attributePatterns` for open maps.
- **Validation schema and autocomplete are independent — and may intentionally diverge.** A key the runtime
  emits/accepts but that's missing from the validation schema makes hand-saving the KATA fail with
  `Key \`x:\` is unknown` — a feature can stay broken for years until someone hand-edits that KATA (e.g.
  legacy `behavior/` toolbar items, auto-injected at render, were never in `interactionToolbar()`). Fix =
  add the key to the **schema**; add it to **autocomplete** only if you want it suggested (a legacy /
  auto-injected key is often deliberately schema-valid but *not* offered as a completion).
- Dynamic suggestion responses must be a **flat JSON array** of `{caption, snippet, docHTML}` (not an
  object); anything else yields no suggestions.
- A value-context path key (e.g. `series:metric:`) fires when typing the value *after* the colon, not the
  key. Don't confuse it with the key-context (`series:`).

See also: `metrics.md` (the metric data queries the Explorer series target).
