---
name: cerb-automations
description: Create Cerb automations and modify existing automations. Use when users want to create an automation from scratch, or update an existing automation. 
---

# Cerb Automations

Automations are self-contained state machines written in KATA that transform an input dictionary into an output dictionary.

## KATA Syntax

See `references/kata.md` for the complete KATA language reference including:
- Syntax rules (indentation, keys, identifiers, values, comments, text blocks, references)
- All annotations (`@bool`, `@int`, `@csv`, `@json`, `@list`, `@text`, `@key`, `@raw`, etc.)
- Scripting (Twig-based): variables, operators, conditionals, loops, string/array/date handling
- All functions (~50) and filters (79)

## Automations

See `references/automations.md` for the complete automations reference including:
- Structure (inputs, exit states, error handling, simulation, continuations, timers)
- All commands: `set:`, `decision:`, `repeat:`, `while:`, `return:`, `error:`, `await:`, `http.request:`, `record.create/get/search/update/upsert/delete:`, `function:`, `data.query:`, `storage.get/set/delete:`, `file.read/write:`, `llm.chat/agent/embed:`, `queue.push/pop:`, `metric.increment:`, `email.parse:`, `encrypt.pgp/decrypt.pgp:`, `api.command:`, `log:`
- All 18 triggers (`automation.function`, `interaction.worker`, `webhook.respond`, etc.)
- All 16 events (`mail.received`, `record.changed`, `mail.route`, etc.)
- Policies (callers, commands, time limits)

## Record Types

See `references/record-types.md` for the full list of record types and their field schemas.

The **Type** field is used to refer to a record type in automation commands like `record.create`.

Fields marked with a `*` are required when creating a new record.

## Search Queries

For search query construction, invoke the `/cerb-search` skill if installed — it is a dedicated specialist with the full field reference for every record type.

If `/cerb-search` is not available, fall back to `references/search-queries.md` for filter types, operators, deep search syntax, boolean groups, sorting, query parameters, and per-record-type field listings.

## Toolbars

See `references/toolbars.md` for toolbar configuration including:
- `record.card` and `record.profile` toolbar KATA (placeholders, caller params, return values)
- Form elements for `interaction.worker` (`fileDownload`, `say`, `text`, `textarea`, `chooser`, `sheet`, `editor`, `fileUpload`, `submit`)

## Workflows

See `references/workflows.md` for the workflow KATA schema including:
- Template structure (name, version, description, requirements)
- Config types (chooser, picklist, text)
- Extensions (activity, permission, translation)
- Records (deletionPolicy, fields, updatePolicy)
- Placeholders (static template-time, dynamic runtime with `cerb_workflow_config()` and `cerb_workflow_resources()`)

**Important:** When a workflow record field contains `{{placeholders}}` that must be preserved literally and not evaluated at template-time, use the `@raw` annotation. This is critical for fields like `script@raw:`, `policy_kata@raw:`, and `event_kata@raw:` which contain automation code with runtime placeholders.

## Cerb Documentation

The official Cerb documentation is at `https://cerb.ai/docs/`. You can fetch individual pages with WebFetch (e.g. `https://cerb.ai/docs/records/types/draft`).

Search and fetch Cerb docs using one of these methods (in order of preference):

1. **MCP tools** (`mcp__claude_ai_Cerb__search_documents`, `mcp__claude_ai_Cerb__fetch_documents`): Use when available. Users can add the MCP server URL `https://api.cerb.cloud/docs/mcp` in Claude Desktop or Claude Code settings.

2. **Docs API** (no auth required, fallback when MCP is unavailable):
   ```bash
   # Semantic search
   curl --silent -X POST "https://api.cerb.cloud/docs/search" -H "Content-Type: application/json" -d '{"query":"your search query here"}'

   # Fetch pages as LLM-friendly Markdown (comma-separated doc IDs from search results)
   curl --silent "https://api.cerb.cloud/docs/fetch/index,pricing"
   ```

3. **WebFetch**: Fetch individual HTML pages directly (e.g. `https://cerb.ai/docs/records/types/draft`).

Use these when the local reference files don't cover a topic or you need to verify current behavior.

## Reference Files

- `references/kata.md` -- KATA syntax, annotations, scripting, functions, and filters
- `references/automations.md` -- automation commands, triggers, events, and policies
- `references/record-types.md` -- record types, field schemas
- `references/toolbars.md` -- toolbar configuration, form elements
- `references/workflows.md` -- workflow KATA schema, config, extensions, records, placeholders
- `references/search-queries.md` -- search query syntax, operators, filters, and fields by record type
- `references/icons.md` -- icon names for toolbar interactions and widgets

## Guides

- `references/guide-record-dictionaries.md` -- record dictionaries, key expansion, event placeholders vs command output, profile URLs, record type checking
- `references/guide-drafts.md` -- creating draft records to send email (transactional, compose, reply, forward)
- `references/guide-record-changed.md` -- record.changed event automations (filtering, detecting field changes, complete workflow example)
- `references/guide-custom-fields.md` -- setting and reading custom field values in automations