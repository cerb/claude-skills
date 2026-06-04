# Cerb Skills for Claude Code

Claude Code skills for working with [Cerb](https://cerb.ai/), the automation and workflow platform for teams.

## Installation

Skills are installed by placing them in the `.claude/skills/` directory of your project.

### Claude Code (CLI / Web)

Clone the repository once to a shared location, then symlink the skills you want into each project. This lets multiple projects share the same set of skills — pull once and every project is up to date.

```bash
# Clone the repository once to a shared location
git clone https://github.com/cerb/claude-skills.git ~/claude-skills

# From your project root, symlink the skill directories you want
mkdir -p .claude/skills
ln -s ~/claude-skills/cerb-automations .claude/skills/cerb-automations
ln -s ~/claude-skills/cerb-dev .claude/skills/cerb-dev
ln -s ~/claude-skills/cerb-search .claude/skills/cerb-search
ln -s ~/claude-skills/cerb-docs .claude/skills/cerb-docs
ln -s ~/claude-skills/cerb-icons .claude/skills/cerb-icons
```

Restart Claude Code or start a new session. The skills will be automatically discovered.

Verify the skill is available by typing `/cerb-automations` or checking:

```bash
ls .claude/skills/cerb-automations/SKILL.md
```

### Claude Desktop

1. Click **Customize** in the left sidebar.
2. Select **Skills** from the menu.
3. Click the **+** button.
4. Upload the skill as a ZIP file (download from [releases](https://github.com/cerb/claude-skills/releases) or create from the repository).

### Optional: Cerb Docs MCP Server

For live access to Cerb documentation, add the MCP server in your Claude Code or Claude Desktop settings:

- **URL:** `https://api.cerb.cloud/docs/mcp`
- No authentication required

## Skills

### cerb-automations

Create and modify Cerb automations, workflows, and event listeners using KATA syntax.

**Trigger:** `/cerb-automations` or when the user asks to create/update an automation.

**Capabilities:**

- Write automations with any trigger type (`automation.function`, `interaction.worker`, `webhook.respond`, etc.)
- React to events (`record.changed`, `mail.received`, `mail.route`, etc.)
- Use all automation commands: `set:`, `decision:`, `repeat:`, `while:`, `http.request:`, `record.create/get/search/update/delete:`, `llm.chat/agent:`, `queue.push/pop:`, `metric.increment:`, and more
- Build workflows that package automations, event listeners, and configuration together
- Create and send email via draft records (transactional, compose, reply, forward)
- Work with all Cerb record types and their field schemas
- Construct search queries with filters, deep search, and boolean groups
- Configure toolbar interactions and form elements
- Apply automation policies (callers, commands, time limits)

**Reference files included:**

- `kata.md` — KATA language syntax, annotations, Twig scripting functions and filters
- `automations.md` — all commands, triggers, events, policies, and structure
- `record-types.md` — record type field schemas
- `search-queries.md` — search query syntax and per-record-type filter fields
- `toolbars.md` — toolbar and form element configuration
- `workflows.md` — workflow KATA schema
- `icons.md` — available icon names

**Guides included:**

- `guide-record-dictionaries.md` — record dictionaries and key expansion
- `guide-drafts.md` — creating draft records to send email
- `guide-record-changed.md` — building `record.changed` event automations
- `guide-custom-fields.md` — working with custom fields in automations

---

### cerb-dev

Work on Cerb core and plugin code using the Devblocks PHP framework.

**Trigger:** `/cerb-dev` or when the user asks to add record types, write migrations, create extensions, or debug platform internals.

**Capabilities:**

- Add new record types with full DAO/Model/Context/View/SearchFields boilerplate (via code generator)
- Write database migration patches
- Add fields to existing DAOs and models
- Implement card widgets, cron jobs, and search index backends
- Register extensions in `plugin.xml` and translations in `strings.xml`
- Work with worklist subtotals, peek/edit templates, and form handling patterns
- Register and increment platform metrics

**Reference files included:**

- `architecture.md` — directory layout, plugin structure, naming conventions, context system, extension points, template paths
- `dao-pattern.md` — DAO class structure, database operations, events/deltas, form handling, migration patch authoring
- `extensions.md` — card widget, cron job, and search index extension patterns
- `plugin-xml.md` — plugin.xml manifest structure, extension points, class loaders
- `new-record-type.md` — complete step-by-step guide for creating a new record type
- `adding-dao-fields.md` — adding fields to an existing DAO/model/context
- `peek-edit-patterns.md` — Smarty gotchas, checkbox groups, dynamic rows, flat lookup sets
- `worklist-subtotals.md` — adding subtotals to View_ classes
- `metrics.md` — registering and incrementing metrics
- `rerun-patch.md` — forcing a database patch to re-run in development

**Tools included:**

- `tools/gen-dao.py` — Python generator that writes all PHP and Smarty boilerplate for a new record type from a table name and field list

---

### cerb-search

Construct Cerb search queries for any record type.

**Trigger:** `/cerb-search` or when the user asks to filter records by field values in a search bar, worklist, automation, or saved search.

**Capabilities:**

- Build search queries for any Cerb record type (tickets, messages, workers, orgs, contacts, tasks, etc.)
- All filter types: text, fulltext, numeric, boolean, date, chooser, record/deep search, links, watchers, null
- Deep search across related records to any depth
- Boolean groups (AND, OR, NOT with parentheses)
- Sorting and result limiting
- Safe query parameter injection for automation use (`record_query_params:`)

**Reference files included:**

- `search-queries.md` — complete search query syntax, all operators, and filter fields for every record type

> **Note:** `cerb-search` shares its reference data with `cerb-automations`. If installing skills individually rather than cloning the full repo, install both together to avoid duplication drift.

### cerb-icons

Design SVG icons for Cerb's custom SCSS icon set.

**Trigger:** `/cerb-icons` or when the user asks to create, edit, or add icons to the Cerb icon map.

**Capabilities:**

- Author icon geometry for Cerb's `mask-image`-based icon system, where geometry (opaque shape vs. transparent gap) carries all visual distinction — color comes from the button's CSS text color
- Match Cerb's icon style families (line, filled-solid, compass, punched-disc) and the 24×24 viewBox / stroke conventions
- Add icons to both `cerb-icons.scss` and `reference_icons.php` (kept alphabetized) and rebuild the CSS

**Reference files included:**

- `icon-design.md` — design reference: common techniques, icon-by-icon notes, and style-anchor samples

## Cerb Documentation

The official Cerb documentation is at https://cerb.ai/docs/.

An MCP server is available at `https://api.cerb.cloud/docs/mcp` for searching and fetching docs from Claude Desktop or Claude Code.

A public docs API is also available (no auth required):

```bash
# Semantic search
curl --silent -X POST "https://api.cerb.cloud/docs/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"your search query here"}'

# Fetch pages as LLM-friendly Markdown (comma-separated doc IDs from search results)
curl --silent "https://api.cerb.cloud/docs/fetch/index,pricing"
```
