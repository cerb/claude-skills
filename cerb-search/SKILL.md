---
name: cerb-search
description: Build Cerb search queries for filtering records. Use when users need help constructing search queries for any record type (tickets, messages, workers, orgs, etc.) — whether for the Cerb search bar, automations, saved searches, or data queries.
---

# Cerb Search Query Builder

Consult `references/search-queries.md` for the complete reference: filter types, operators, deep search syntax, boolean groups, sorting, and per-record-type field listings.

## Process

1. **Identify the record type** (ticket, message, worker, org, contact, task, etc.)
2. **Look up available fields** in `references/search-queries.md` under "Search Query Fields by Record Type"
3. **Only use fields that exist** for that record type — never invent field names
4. **Choose the correct filter syntax** based on field type
5. **Construct the query** using proper syntax

## Syntax Quick Reference

| Field Type | Example |
|---|---|
| text | `subject:Invoice*` `status:open` `name:[a,b,c]` `mask:!ABC*` |
| fulltext | `content:("exact phrase" other terms)` |
| numeric | `importance:>=75` `size:>100000` `id:123` `age:25...50` |
| boolean | `isAdmin:y` `isDisabled:no` |
| date | `created:today` `updated:"-1 week"` `closed:"2024-01-01 to 2024-06-30"` |
| chooser | `group.id:5` `owner.id:[1,2,3]` `bucket.id:0` |
| record (deep search) | `group:(name:Support)` `org:(country:Germany)` |
| links | `links:task` `links.ticket:(mask:ABC*)` |
| watchers | `watchers:me` `watchers:any` `watchers:none` |
| null | `org.id:null` `phone:!null` |

## Key Rules

**Deep search:** Use parentheses for nested queries: `group:(name:Support)`. Chain to any depth: `messages.first:(sender:(org:(name:"Acme Corp")))`. Negate with `!`: `group:!(name:Sales)`. The `on.<type>:` filter always takes a nested query: `on.ticket:(id:123)` — never `on.ticket:123`.

**Boolean logic:** Filters are AND-ed by default. Use `OR` between filters: `owner.id:me OR owner.id:0`. Group with parentheses: `(status:open group:(name:Sales)) OR (status:waiting group:(name:Support))`. Negate groups: `!(mimetype:image/png size:<100KB)`.

**Sorting/limiting:** `sort:-field` (desc), `sort:field` (asc), multiple: `sort:-importance,created`. `limit:N` to cap results.

**Query parameters (automations only):** When user input is involved, use `record_query_params:` for safe injection:
```kata
record_query: status:${status} group.id:${group_id}
record_query_params:
  status: o
  group_id: 5
```

## Output Format

- **Record type:** state the target record type
- **Query:** the complete query on a single line (all filters space-separated)
- For automations, show in `record.search:` context with proper KATA indentation
- For the Cerb UI or general use, always present as a single line
- Explain each filter if the query is non-trivial
