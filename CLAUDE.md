# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A Claude Code skills repository for [Cerb](https://cerb.ai/docs/) — a PHP/MySQL helpdesk and workflow automation platform. Skills are distributed by cloning into `.claude/skills/` and provide Claude with deep domain context about Cerb's automation scripting language (KATA) and its PHP plugin architecture (Devblocks).

## Skill Architecture

Each skill follows this layout:

```
{skill-name}/
├── SKILL.md              # YAML frontmatter + comprehensive guide (the skill entrypoint)
├── references/           # Detailed reference docs loaded on demand
│   ├── [topic].md
│   └── guide-[task].md   # Task-specific how-to guides
├── agents/               # (optional) Sub-agents for specialized sub-tasks
└── tools/                # (optional) Executable utilities (e.g., Python generators)
```

### SKILL.md Frontmatter

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: {skill-id}
description: {one-line description — used to determine when to activate this skill}
---
```

The `description` field is critical: it determines when Claude Code selects this skill automatically. Write it as a trigger condition ("Use when...").

## Existing Skills

### `cerb-automations`
Covers KATA syntax, all automation commands/triggers/events, record types and field schemas, search query syntax, toolbar configuration, workflows, and email draft creation. Reference files are comprehensive (700–1800 lines each) and meant to be read selectively based on the task.

### `cerb-dev`
Covers the Devblocks PHP framework architecture, plugin manifest structure (`plugin.xml`), DAO/Model/Context class patterns, database migrations, Smarty templates, and the step-by-step process for adding new record types. Includes `tools/gen-dao.py`, a Python generator that produces all boilerplate PHP/Smarty/XML files for a new record type from a table name and field list.

## Conventions When Adding or Modifying Skills

- **Reference files** should be comprehensive and self-contained — they are loaded directly into Claude's context.
- **Guides** (`guide-*.md`) address a single specific task and are shorter and more focused than general reference files.
- **Agents** define a specialist role within a skill, with a clear process, validation rules, and output format.
- **Tools** are standalone executables; document their CLI interface and expected input/output inside `SKILL.md`.
- Cross-reference related documents within `SKILL.md` so Claude knows which reference file to consult for which task.
- All documentation in this repo targets Claude as the reader, not human developers — write to maximize Claude's ability to perform tasks correctly on the first attempt.

## Cerb Documentation Access

Three methods are available for fetching up-to-date Cerb documentation, in priority order:

1. **MCP tools** (`mcp__claude_ai_Cerb__search_documents`, `mcp__claude_ai_Cerb__fetch_documents`) — semantic search and fetch from the Cerb Docs MCP Server
2. **Docs API** — `POST https://api.cerb.cloud/docs/search` with `{"query":"..."}` (search) / `GET https://api.cerb.cloud/docs/fetch/{ids}` with comma-separated doc IDs from search results (fetch)
3. **WebFetch** — fetch `https://cerb.ai/docs/{path}/` directly and parse the HTML
