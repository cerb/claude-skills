# Worklist Internals Reference

For batch processing or background work that needs to operate on a worklist's filtered result set without paging through it. See also `worklist-quick-search.md` (search syntax) and `worklist-subtotals.md` (subtotal grouping).

## Reaching the Underlying SQL

Every DAO that backs a worklist exposes the search query in parts:

```php
$query_parts = $dao_class::getSearchQueryComponents(
    $columns,           // column names (often [])
    $view->getParams(), // current view filter as DevblocksSearchCriteria[]
    $sortBy,            // optional sort field key (or null)
    $sortAsc            // optional bool
);
```

Returns:

```php
[
    'primary_table' => 'ticket',                                // base table name
    'select'        => 'SELECT ticket.id AS t_id, ... ',        // column projection
    'join'          => 'FROM ticket LEFT JOIN ... ',            // FROM + JOINs
    'where'         => 'WHERE 1 AND ... ',                      // always begins with WHERE
    'sort'          => 'ORDER BY t_id DESC ',                   // includes ORDER BY keyword
]
```

Use these to build batch SQL against the worklist's filter without paging:

```php
// Count
$total = intval($db->GetOneReader("SELECT COUNT(1) " . $query_parts['join'] . $query_parts['where']));

// Fetch all matching IDs (e.g. as the inner subquery for INSERT...SELECT)
$primary_key = $search_class::getPrimaryKey();   // "ticket.id"
$inner = "SELECT $primary_key AS id " . $query_parts['join'] . $query_parts['where'];
```

`$context_ext->getDaoClass()` and `$context_ext->getSearchClass()` get you the right class names from a context extension.

## Join-Multiplication Caveat

`_searchWithTimeout` (the engine behind `DAO_X::search`) assumes 1:1 row results. Most worklists are written so joins don't multiply rows — many-to-many filters use `WHERE id IN (SELECT …)` subqueries rather than joins. But this is a convention, not enforced.

When building batch SQL from `getSearchQueryComponents` output, defensively add `GROUP BY $primary_key` to the inner select to dedupe in case a join did multiply rows. This was the approach taken by `_internalAction_saveExport`'s producer SQL.

## Capturing the Filter as Audit

`$view->getParamsQuery()` returns the raw quick-search query string used to build the current params (e.g. `"status:open created:[-7 days to now]"`). This is set by `addParamsWithQuickSearch()` and persisted on saved worklists.

For background jobs that process a filtered set, store this string in the job's metadata at submission time. The view's saved filter can change after the job is queued, but the audit trail stays accurate. The worklist's `view_id` alone isn't enough — capture the query separately.

## Captured Order vs ID Order

The simplest deterministic order for batch processing is `ORDER BY <primary_key>` — matches what most worklists default to. Preserving the worker's selected sort (`$view->renderSortBy`) requires more plumbing because the sort SQL references column aliases (`t_subject`) that exist only in the SELECT projection, not the inner subquery. For most batch-processing use cases ID order is fine; if you need display-order fidelity, expose the relevant column directly in the inner SELECT.

## Worklist View Loading

`C4_AbstractViewLoader::getView($view_id)` returns a hydrated `C4_AbstractView` for any view ID — built-in worklists, custom (`cust_*`), saved searches, etc.

`Extension_DevblocksContext::getByViewClass(get_class($view), true)` resolves the context extension from a view class. Use it to bridge from the JS-supplied `view_id` to the context's DAO/Search/UI classes.

## Forms That Reference a View

When a peek/popup is launched from a worklist row, the form should carry `view_id` so a successful save can refresh that worklist via:

```js
genericAjaxGet('view' + view_id,
    'c=internal&a=invoke&module=worklists&action=refresh&id=' + view_id);
```

This is the standard close-handler pattern (see `popup_mapping.tpl`, `view_export.tpl` for examples).
