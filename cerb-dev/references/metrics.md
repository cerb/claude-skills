# Metrics

## Getting the singleton

```php
$metrics = DevblocksPlatform::services()->metrics();
```

## Incrementing a counter

```php
$metrics->increment(
    'cerb.some.metric.name',
    1,
    [
        'dimension_key' => $dimension_value,
    ]
);
```

Dimensions are optional. Only pass dimensions that are defined on the metric.

## Registering a new metric

Add an `INSERT IGNORE` in the versioned patch file (`features/cerberusweb.core/patches/11.x/11.2.0.php`):

```php
$db->ExecuteWriter(sprintf("INSERT IGNORE INTO metric (name, description, type, dimensions_kata, created_at, updated_at) ".
    "VALUES (%s, %s, %s, %s, %d, %d)",
    $db->qstr('cerb.some.metric.name'),
    $db->qstr('Human-readable description of what this counts'),
    $db->qstr('counter'),
    $db->qstr("text/dimension_key:\n"),
    time(),
    time()
));
```

## Dimension types in `dimensions_kata`

| Prefix | Type | Example |
|---|---|---|
| `text/` | Free-form string | `text/scope:` |
| `record/` | Record ID (with `record_type` sub-key) | `record/rule_id:\n  record_type: mail_routing_rule` |

Multiple dimensions are newline-separated in the KATA string:

```php
$db->qstr("record/rule_id:\n  record_type: mail_routing_rule\ntext/rule_key:\ntext/node_key:\n")
```

## Metric types

- `counter` — monotonically increasing count (most common)

## Notes

- Use `INSERT IGNORE` so the patch is safe to re-run.
- If it's unclear whether a metric already exists in the database, confirm with the user before adding it to the patch.
