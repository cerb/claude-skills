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
