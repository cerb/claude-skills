# Guide: Record Dictionaries and Key Expansion

Record dictionaries are the primary way to access record data in automations. They appear in two contexts with different syntax.

## Event Placeholders (Top-Level Scope)

Events like `record.changed`, `mail.received`, etc. set record placeholders in top-level scope with underscore-separated keys:

```kata
# Direct fields
{{record_id}}
{{record_subject}}
{{record_owner_id}}
{{record_status}}
```

### Key Expansion

Event placeholders support key expansion to any depth on the record graph. You can traverse linked records without a separate `record.get` call:

```kata
# ticket -> owner (worker) -> first name
{{record_owner_first_name}}

# ticket -> owner (worker) -> email address
{{record_owner_address_email}}

# ticket -> group -> name
{{record_group_name}}

# ticket -> org -> name
{{record_org_name}}
```

This works to arbitrary depth — follow the relationship chain with underscores.

### Profile URLs

Every record has a `record_url` key for its profile URL. Use `{{prefix_record_url}}` instead of building URLs with `cerb_url()`:

```kata
# In a record.changed event (prefix is "record")
{{record_record_url}}

# On a linked record (prefix varies by context)
{{ticket_record_url}}
{{worker_record_url}}
```

### Record Type Checking

Use the `is record type` test, which handles both aliases and fully-qualified extension IDs:

```kata
# Correct — works with aliases and extension IDs
{{record__type is record type ('ticket')}}
{{record__type is not record type ('ticket','task')}}

# Avoid — fragile, won't match extension IDs
{{record__type == 'ticket'}}
```

The `record__type` placeholder is always the alias (e.g. `ticket`). The `record__context` placeholder is usually the fully-qualified extension ID (e.g. `cerberusweb.contexts.ticket`) but can sometimes be an alias too. The `is record type` test handles both.

## Command Output Dictionaries (Dot Notation)

Automation commands like `record.get`, `record.search`, and `record.create` store results in a named output dictionary. Access fields with dot notation:

```kata
record.get:
  output: worker
  inputs:
    record_type: worker
    record_id: 123
  on_success:
    # Dot notation for command output
    set:
      name: {{worker.first_name}} {{worker.last_name}}
      email: {{worker.address_email}}
```

```kata
record.search:
  output: results
  inputs:
    record_type: ticket
    record_query: status:o owner.id:me
  on_success:
    repeat:
      each@key: results
      as: ticket
      do:
        log: {{ticket.subject}} - {{ticket.owner_first_name}}
```

Command output dictionaries do **not** overwrite the outer scope — they are isolated in their named variable.

## Key Differences

| | Event Placeholders | Command Output |
|-|-|-|
| **Syntax** | `{{record_field_name}}` (underscores) | `{{output.field_name}}` (dot then underscores) |
| **Scope** | Top-level, set by the event | Named dictionary, isolated |
| **Key expansion** | Supported to any depth | Supported with `record_expand` input |
| **Example** | `{{record_owner_first_name}}` | `{{worker.first_name}}` |

## When to Use record.get vs Key Expansion

Prefer key expansion on event placeholders when the data is reachable on the record graph. Only use `record.get` when you need a record that isn't linked to the event's record.

```kata
# Good — use key expansion (no extra command needed)
{{record_owner_first_name}}
{{record_group_name}}

# Only when needed — record not on the event's graph
record.get:
  output: other_ticket
  inputs:
    record_type: ticket
    record_id: {{some_other_ticket_id}}
```
