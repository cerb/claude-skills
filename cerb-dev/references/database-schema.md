# Database Schema Reference

The canonical schema for all Cerb tables is stored in:

```
features/cerberusweb.core/assets/cerb.schema.kata
```

This KATA file is the authoritative source for column names, types, nullability, indexes, and foreign key references. **Always consult it before writing SQL** — never guess column names from context.

## Format

Each table is a top-level key. Columns and indexes are nested under it:

```yaml
message:
  columns:
    created_date:
      field: created_date
      type: int unsigned
      nullable: NULL
      key: MUL
    worker_id:
      field: worker_id
      type: int unsigned
      nullable: NULL
      key: MUL
      references: worker.id
  indexes:
    PRIMARY:
      columns:
        id:
          column_name: id
          index_type: BTREE
          unique: 1
```

## Key fields to look for

| Field | Meaning |
|---|---|
| `field` | Actual column name in MySQL |
| `type` | MySQL data type |
| `nullable` | `NOT NULL` or `NULL` |
| `key` | `PRI` (primary), `MUL` (index), `UNI` (unique), blank (none) |
| `default` | Default value (absent means no default) |
| `extra` | e.g. `auto_increment` |
| `references` | Foreign key target (`table.column`) |

## Common tables and their timestamp columns

| Table | Created column | Updated column |
|---|---|---|
| `worker` | `created_at` | `updated` |
| `message` | `created_date` | — |
| `context_activity_log` | `created` | — |
| `automation` | `created_at` | `updated_at` |
| `service_token` | `created_at` | `updated_at` |

## Usage in patches

When writing ALTER TABLE migrations, always verify the column names in `cerb.schema.kata` before referencing them in subqueries or joins. For example, the backfill for `worker.created_at` used:

```sql
SELECT MIN(cal.created) FROM context_activity_log cal ...  -- "created", not "created_at"
SELECT MIN(m.created_date) FROM message m ...              -- "created_date", not "created"
```
