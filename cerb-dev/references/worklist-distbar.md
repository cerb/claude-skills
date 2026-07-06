# Adding an inline distbar column to a worklist

A "distbar" is a mini horizontal **stacked bar** per worklist row — a live distribution of counts across
a few status buckets (e.g. queue-job messages `done/failed/inflight/...`, task-project tasks
`done/stashed/todo/inprogress`). Loaded async from a profile action so the worklist paints first, then the
bars fill in. Built on the shared loader + `CerbUI.Distbar`. Sibling of the sparkline column — same shape,
simpler (no metrics; just a row→counts endpoint). Live examples: `records/types/queue_job/view.tpl`,
`records/types/task_project/view.tpl`.

## Shared pieces (already exist — don't re-create)

- **Loader:** `templates/internal/views/distbar_loader.tpl` — finds the cells, POSTs their ids to a profile
  action, renders one `CerbUI.Distbar` per row, wires the hover legend tooltip, and (optionally) a scope
  switcher. Fully parameterized via Smarty include params (all but the first three default to the queue_job
  set, so queue_job passes only module/action/view):
  - `distbar_module`, `distbar_action`, `distbar_view_id` — the `c=profiles&a=invoke` endpoint + form ref.
  - `distbar_cell_attr` (default `data-cerb-messages`) — the per-row cell hook attribute.
  - `distbar_keys` / `distbar_labels` / `distbar_palette` — **comma-joined** strings, 1:1, in segment order.
    (Comma-joined, not JSON, to dodge the Smarty `{`-brace trap. No commas allowed inside a label.)
  - `distbar_scope_keys` (optional) / `distbar_scope_attr` — the scope switcher; see below.
- **Component:** `CerbUI.Distbar` (`resources/js/cerb-ui/distbar.js`) — segments are `> span` children carrying
  `data-value` / `data-label` / `data-text`; it computes each segment's `% = value/sum` → width, **colors by
  palette index**, hides zero-valued segments, and can clone the segments into a `CerbUI.Legend`.
- **Field-chooser icon:** the virtual column's type drives the customize-view tile. `TYPE_VIRTUAL_DISTBAR`
  (`DevblocksSearchCriteria` in `libs/devblocks/api/Model.php`) maps to `['chart-bar-stacked','purple',…]`
  in `C4_AbstractView::getColumnDisplayMeta()` (`api/dao/abstract_view.php`) — mirrors `TYPE_VIRTUAL_SPARKLINES`.

## Per-worklist checklist

1. **DAO:** a batched `getXCountsForRows(array $ids): array<int,array{bucketA:int,…,total:int}>` — ONE
   grouped query (`SUM(IF(status_id=…,1,0))` per bucket + `COUNT(*) AS total`), keyed by row id, omitting
   empty rows. Model it on `DAO_QueueJob::getLiveCountsForJobs()`. `total` is what the loader uses to decide
   an empty cell, so always include it. The JSON keys must equal `distbar_keys` 1:1.
2. **SearchFields_X:** a virtual display field — `db_table='*'`, **empty db_column** (suppresses the sort
   link), a label, type `DevblocksSearchCriteria::TYPE_VIRTUAL_DISTBAR`, not sortable. It never touches SQL
   (the `getSearchQueryComponents` SELECT is fixed), so no `getWhereSQL` case is needed.
3. **View_X constructor:** add the virtual field to `$this->view_columns` (default-on).
4. **Profile controller** (`api/uri/profiles/<type>.php`): a `profileAction` case + method that reads `ids[]`,
   ACL-filters to readable rows if the record type has per-row ACL (projects can be private — filter via
   `Context_X::isReadableByActor` before counting), calls the DAO, and `echo json_encode((object) $out)`
   (`(object)` → always `{}` when empty). Mirror `_profileAction_viewMessagesJson` in `profiles/queue_job.php`.
5. **view.tpl:** a cell branch → `<td data-column="*_x"><div class="cerb-ui-distbar cerb-ui-distbar--mini"
   data-<attr>="{$result.<pk>}"></div></td>`; and the loader include gated by the column, inside a
   `<script nonce>` block (see queue_job/task_project for the exact include call).

## Scope switcher (optional — `Open | All` style)

A header toggle that shows a **subset** of segments (e.g. hide `done` so it can't dominate a long-running
project). Unlike the sparkline window switcher (which re-queries), the distbar already fetched **all** buckets,
so the toggle is a **pure client-side re-render of cached rows — no server round-trip**. Reuses `CerbUI.Switcher`.

- **Loader param** `distbar_scope_keys='open=todo|inprogress|waiting;all=todo|inprogress|waiting|done'` —
  `value=key|key;value=key|key`. Empty (default) ⇒ no switcher (queue_job). The loader caches the last
  rows, filters `DISTBAR_SEGMENTS` to the active scope's key Set, and re-renders; the chosen scope persists
  per view in `localStorage` (`cerb.distbar.<module>:<viewId>`) and applies to the first paint.
- **Header markup** is worklist-specific (scopes/labels vary), so **inline** a `<th>` with a
  `<span class="cerb-ui-switcher cerb-ui-switcher--xs" data-cerb-distbar-switcher>` of
  `<button data-value="…">` (mark the default `cerb-ui-switcher--active`) — don't build a shared header
  partial. Special-case `{if $header == "*_x"}` in the header `{foreach}`. See task_project/view.tpl.

## Gotchas

- **Colors must travel with the series, not the index.** `CerbUI.Distbar` colors segments by their palette
  **position**. If a scope hides a segment, the remaining ones shift down and inherit the hidden segment's
  color (hiding `done` made `stashed` turn green). Fix in the loader: stash each segment's color on it
  (`DISTBAR_SEGMENTS[i].color = DISTBAR_PALETTE[i]`) and pass a palette built from only the **visible**
  segments (`segs.map(s => s.color)`) into `new CerbUI.Distbar(...)`. This also makes any non-prefix scope
  (hiding a *middle* segment) correct. (Alternative: pass a `scale` and `data-color-key` for color-by-key.)
- **Palette is positional, 1:1 with `distbar_keys`.** To recolor/reorder, reorder `distbar_keys`,
  `distbar_labels`, and `distbar_palette` **together**. Reorder for *reading* (e.g. progress order
  `done,stashed,todo,inprogress`) independent of the DB bucket order — only keys↔JSON must match.
- **Smarty `{`-brace traps in the loader JS** (the loader is plain JS, not wrapped in `{literal}`): bare
  `{}` and `{`+non-space parse as Smarty tags. Use `Object.create(null)` for empty-object inits; arrow
  object returns need the `=> ({ … })` space form; keep `{` after a space everywhere. See smarty-conventions.
- **`(object)` cast the JSON** so an empty result is `{}` not `[]` (the loader keys by row id).
- **Reuse the cell attribute name across worklists is fine** but pass a semantic one (`data-cerb-tasks`) via
  `distbar_cell_attr` for clarity; the loader keys everything off that one attribute.

## Verify

`Search → <Type>` shows the column; bars sum/scale correctly; a row with zero rows shows an empty cell; hover
shows the legend; add/remove in Customize (purple stacked-bar icon). With a scope switcher: default scope hides
the excluded segment and the bar re-scales; toggling re-colors correctly (each series keeps its color) with **no
network request**; the choice persists per view on reload. Regression-check any other distbar worklist
(defaults unchanged).
