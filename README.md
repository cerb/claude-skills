# Cerb Skills for Claude Code

Claude Code skills for working with [Cerb](https://cerb.ai/), the automation and workflow platform for teams.

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

A public search API is also available (no auth required):

```
curl --silent -X POST "https://api.cerb.cloud/docs/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"your search query here"}'
```
