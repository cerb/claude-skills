# Re-running a Database Patch (Development)

To repeat the latest patch for a plugin, decrement its revision in the MySQL console:

```sql
-- Repeat the latest patch (safe for dev):
UPDATE cerb_patch_history SET revision=revision-1 WHERE plugin_id='cerberusweb.core';

-- Or set an explicit revision (use with caution):
UPDATE cerb_patch_history SET revision=42 WHERE plugin_id='cerberusweb.core';
```

Then reload `/update` to re-run the patch.
