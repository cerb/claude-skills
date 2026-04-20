---
id: "docs-automations-commands-queue-push"
title: "Automations: queue.push"
url: "https://cerb.ai/docs/automations/commands/queue.push/"
summary: "This page provides detailed information on the 'queue.push' command used in Cerb automations to add new messages to a queue. It outlines the syntax and parameters required for the command, including inputs like `queue_name` and `messages`, and optional settings such as `available_at@date`. The page also explains how to handle outputs, simulate the command, and manage success and error scenarios. It includes examples and descriptions of how to use placeholders for results and error handling, ensuring users can effectively implement and troubleshoot the queue.push command in their automation workflows."
tags: ["docs", "docs-automations"]
---
The **queue.push:** command adds new messages to a [queue](/docs/queues/).

```
start:
  queue.push:
    inputs:
      queue_name: example.queue.name
      messages:
        0:
          id: message0
          priority: high
        1:
          id: message1
          priority: low
    output: results
```

- [Syntax](#syntax)
  - [inputs:](#inputs)
  - [output:](#output)
  - [on\_simulate:](#on_simulate)
  - [on\_success:](#on_success)
  - [on\_error:](#on_error)

# Syntax

## inputs:

| Key | &nbsp; |
| --- | --- |
| `available_at@date:` | The optional future date to process the message |
| `queue_name:` | The [queue](/docs/queues/) name to add messages to |
| `messages:` | An array of messages to add. These can be strings or objects |

## output:

Save the queue push result to this placeholder.

## on\_simulate:

The [commands](/docs/automations/#commands) to run during simulation instead of pushing messages to the queue.

If omitted, messages are pushed to the queue during simulation.

## on\_success:

The [commands](/docs/automations/#commands) to run on success.

The `output:` placeholder contains an array of unique queue message IDs. These can be reused to look up eventual message processing success or failure.

## on\_error:

The [commands](/docs/automations/#commands) to run on failure. If omitted, the automation exits in the `error` [state](/docs/automations/#exit-states).

The `output:` placeholder receives a dictionary with these keys:

| Key | &nbsp; |
| --- | --- |
| `error` | The error message. |

