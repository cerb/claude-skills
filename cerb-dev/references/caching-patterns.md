# Caching Patterns

## The `schema_records` tag

`DAO_CustomField`, `DAO_CustomFieldset`, and `DAO_CustomRecord` all call `$cache->removeByTags(['schema_records'])` on any write. Any cache entry whose content is derived from the custom field/fieldset schema should be saved with this tag and it will be automatically invalidated when schemas change:

```php
$cache->save($data, $cache_key, ['schema_records']);
```

No manual invalidation needed. This is the right tag for things like context placeholder label trees, which depend on which custom fields exist and their types.

## The `$cache_local = true` antipattern

Passing `local_only=true` to `$cache->load()` / `$cache->save()` looks like caching but only writes to the PHP process's in-request `_registry` array. The data is discarded at the end of the request — the persistent cache engine (disk/memcached/redis) is never touched.

```php
// ANTIPATTERN: rebuilt from scratch on every request
$cache->save($data, $cache_key, [], 0, true);

// Correct: persisted across requests, invalidated by tag
$cache->save($data, $cache_key, ['schema_records']);
```

This was the root cause of 3–5 second response times in the bot behavior action popup (`renderDecisionPopup`): `CerberusContexts::getContext()` with a null object was rebuilding the full context chain (message → ticket → group → worker, recursively expanding TYPE_LINK/TYPE_WORKER custom fields) on every single request. Fixed in `api/Application.class.php` by dropping `$cache_local` and tagging with `schema_records`.

When auditing for performance issues, grep for `local_only=true` or `$cache_local = true` — any hit that's not intentionally request-scoped is a candidate for this fix.
