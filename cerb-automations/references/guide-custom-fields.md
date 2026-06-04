# Custom Fields in Automations

## Setting custom field values

When setting custom field values in `record.create`, `record.update`, or `record.upsert`, use the custom field's **URI** directly as the field key — no prefix needed.

```
record.upsert:
  output: record
  inputs:
    record_type: agent_memory
    record_query: name:"INDEX" limit:1
    fields:
      name: INDEX
      memory_content: This is the content
      memory_summary: A brief summary
```

## Reading custom field values

When reading custom field values from record dictionaries, expand with `customfields` (not `custom_`). Custom field URIs are first-class keys — access them directly on the record, not under a `customfields` sub-key:

```
record.search:
  output: results
  inputs:
    record_type: agent_memory
    record_query: name:"INDEX" limit:1
    record_expand: customfields
  on_success:
    set:
      content: {{results.memory_content}}
```

The `customfields` expansion makes values available as URI-keyed first-class keys on the record dictionary, while `custom_` only returns numeric IDs.

## Custom field params

The `params` field on a custom_field record is a JSON-encoded object with type-specific options.

| Type | Param | Description |
|---|---|---|
| `T` (multi-line text) | `format` | `markdown` to enable Markdown rendering |

## List custom fields (type `M`)

List CFs hold multiple string values per record. A few important properties to keep in mind:

**Read shape**: With `record_expand: customfields`, a list CF appears as a flat array of strings under its URI:

```
{{ssl_cert.letsEncrypt_challengeTokens}}  → ["example.com:abc", "www.example.com:def"]
```

Iterate or `|filter` directly.

**Write shape**: Accept either an array (preferred for full replacement) or a single string. Delta updates prefix entries with `-` to remove:

```
record.update:
  inputs:
    fields:
      colors:
        - red
        - blue
      # ...or to delta-edit:
      # colors: ['-red', 'green']  → remove red, add green
```

**Gotchas — list CFs are sets, not sequences:**

1. **Order is not preserved.** The DAO reads values from `custom_field_stringvalue` with no `ORDER BY` clause. Order on read happens to often match insertion in practice but is not guaranteed across UI re-saves, replication, index rebuilds, or server restarts. **Do not rely on list CF order matching some parallel ordered field** (e.g. you cannot store challenge tokens in the same order as `name` + `alternativeNames` and index by position).

2. **Duplicate values collapse.** Internal storage uses the value itself as the array key (`$ptr[$field_id][$field_value] = $field_value`), so two identical entries silently merge into one. If you need to allow duplicate underlying data, encode something distinguishing into each entry (e.g. `domain:token` instead of bare `token`).

3. **Lookups are by content, not position.** Match entries by filtering on a prefix or substring rather than indexing. Idiomatic pattern:

   ```
   set:
     matches@list: {{my_list_cf|filter(v => v starts with key ~ ':')|join("\n")}}
   ```

If you genuinely need an ordered collection of records, use linked records (a separate record type with a `pos` field) rather than a list CF.
