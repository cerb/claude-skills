---
id: "docs-automations-events-mail-received"
title: "mail.received"
url: "https://cerb.ai/docs/automations/events/mail.received/"
summary: "This page provides information on the 'mail.received' automation events in Cerb, which are designed to respond to incoming messages once they are added to a ticket. It explains how these events can be used, such as sending an automatic reply confirmation for new tickets. The page details the placeholders available in the automation event dictionary, including keys like `is_new_ticket` to determine if a message is opening a new ticket or replying to an existing one, and `message_*` for accessing the message record with key expansion. There are no outputs specified for these events."
tags: ["docs", "docs-automations"]
---
**mail.received** automation events can react to received messages after they are appended to a ticket. For instance, sending an auto-reply confirmation to new tickets.

# Placeholders

The automation event dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `is_new_ticket` | bool | `true` if the message opened a new ticket, `false` if a reply to an existing ticket |
| `message_*` | record | The message record. Supports key expansion. |

# Outputs

(none)

# Examples

Send an autoresponder when a new ticket is created:

- automation
- policy
- event
- inputs

- 
```
start: record.create: output: new_draft inputs: record_type: draft fields: name: Auto-Response type: ticket.reply ticket_id: {{ message_ticket_id }} is_queued: 1 queue_delivery_date@date: 5 mins to: {{ message_sender_address }} params: to: {{ message_sender_address }} subject: [# {{ message_ticket_mask }}] {{ message_ticket_subject }} headers: In-Reply-To@optional: {{ message_headers['in-reply-to'] }} Auto-Submitted: auto-replied content: Thank you for contacting us. We will respond as soon as possible.
```
- 
```
commands: record.create: deny/type@bool: {{ inputs.record_type is not record type ('draft') }} allow@bool: yes
```
- 
```
automation/autoreply: uri: cerb:automation:example.newticket.autoresponder disabled@bool: {{ not is_new_ticket or not message_ticket_group_auto_responder_enabled or message_ticket_subject is pattern ( '*out of the office*', '*out of office*', '*auto response*', '*autoreply*', ) }}
```
- 
```
message__context: message message_id: 1
```

