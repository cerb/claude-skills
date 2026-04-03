# Cerb Skills for Claude Code

Claude Code skills for working with [Cerb](https://cerb.ai/), the automation and workflow platform for teams.

## Installation

Skills are installed by placing them in the `.claude/skills/` directory of your project.

### Claude Code (CLI / Web)

From your project root:

```bash
# Clone into your project's skills directory
git clone https://github.com/cerb/claude-skills.git .claude/skills

# Or, if .claude/skills/ already exists, clone and copy the skill directories
git clone https://github.com/cerb/claude-skills.git /tmp/cerb-skills
cp -r /tmp/cerb-skills/cerb-automations .claude/skills/cerb-automations
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

- Write automations with any trigger type (automation.function, interaction.worker, webhook.respond, etc.)
- React to events (record.changed, mail.received, mail.route, etc.)
- Build workflows that package automations, event listeners, and configuration together
- Create and send email via draft records (transactional, compose, reply, forward)
- Work with all Cerb record types and their field schemas
- Construct search queries with filters, deep search, and boolean groups
- Configure toolbar interactions and form elements
- Apply automation policies (callers, commands)

**Reference files included:**

- KATA language syntax, annotations, scripting functions, and filters
- All automation commands, triggers, and events
- Record type field schemas and search query fields
- Toolbar and form element configuration
- Workflow KATA schema

**Guides included:**

- Record dictionaries and key expansion
- Creating draft records to send email
- Building record.changed event automations

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
