# Automation Dictionary (Dict) Architecture

## Lazy expansion

Automations use a `DevblocksDictionaryDelegate` that lazy-loads and expands dict paths only when they are actually dereferenced during execution. Bot behaviors by contrast call `setEvent()` upfront, which eagerly loads and expands the full context chain (message → ticket → group → worker, plus all TYPE_LINK/TYPE_WORKER custom field recursion) before any condition or action runs — paying that cost regardless of what the behavior actually touches.

## Shared context across executions on the same event

When multiple automations are triggered by the same event (e.g., a webhook fires three automations), they share the same dict context. The first automation to dereference a path expands it; subsequent automations get the already-expanded value for free. Bot behaviors have no equivalent sharing — each behavior execution rebuilds its own context from scratch.

## Why this matters

These two properties (lazy + shared) are why automations scale well on instances with many custom fields and complex record schemas, while bot behavior execution time grows with schema complexity even when the behavior itself is simple. This is a core architectural reason behaviors are being removed (target: 12.0) in favor of automations.
