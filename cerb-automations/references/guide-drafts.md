# Guide: Creating Draft Records

Drafts are used to send outgoing email from automations. The `type` field determines the behavior.

## Draft Types

| Type | Purpose |
|-|-|
| `mail.compose` | New outgoing message (creates a new ticket) |
| `mail.transactional` | Notification/system email (sent without creating a ticket from the reply) |
| `ticket.reply` | Reply to an existing ticket (requires `ticket_id`) |
| `ticket.forward` | Forward an existing ticket (requires `ticket_id`) |

## Fields vs Params

Draft records have top-level `fields` and a nested `params` object. The `params` control the actual sent message. The top-level `fields:to:` and `fields:name:` are display hints (e.g. `name` could say "Weekly Newsletter" while `params:subject:` is the actual subject the recipient sees). Currently both need to be set — this quirk may be fixed in a future version.

## Params by Type

### mail.transactional

| Param | Description |
|-|-|
| `to` | Recipient email address(es) |
| `subject` | Email subject line |
| `content` | Plain text message body |
| `cc` | CC recipients |
| `bcc` | BCC recipients |
| `from` | Sender address |
| `from_personal` | Sender display name |
| `reply_to` | Reply-to address |
| `return_path` | Return path address |
| `format` | `parsedown` or `plaintext` |
| `file_ids` | Attachment file IDs |
| `headers` | Custom email headers |
| `html_template_id` | HTML template to wrap content |
| `options_gpg_encrypt` | GPG encrypt the message |
| `options_gpg_sign` | GPG sign the message |

### mail.compose

| Param | Description |
|-|-|
| `to` | Recipient email address(es) |
| `subject` | Email subject line |
| `content` | Plain text message body |
| `cc` | CC recipients |
| `bcc` | BCC recipients |
| `format` | `parsedown` or `plaintext` |
| `file_ids` | Attachment file IDs |
| `headers` | Custom email headers |
| `group_id` | **Required.** Group to create the ticket in |
| `bucket_id` | Bucket within the group |
| `org_id` | Organization to link |
| `org_name` | Organization name (alternative to `org_id`) |
| `owner_id` | Worker to assign |
| `status_id` | Initial ticket status |
| `ticket_reopen` | Reopen date if status is waiting |
| `custom_fields` | Ticket custom fields |
| `message_custom_fields` | Message custom fields |
| `html_template_id` | HTML template to wrap content |
| `send_at` | Scheduled send timestamp |
| `options_gpg_encrypt` | GPG encrypt the message |
| `options_gpg_sign` | GPG sign the message |

### ticket.reply / ticket.forward

Inherits `to` (existing participants) and `subject` from the ticket. Only set these in `params` if overriding.

| Param | Description |
|-|-|
| `to` | Override recipients |
| `subject` | Override subject |
| `content` | Plain text message body |
| `cc` | CC recipients |
| `bcc` | BCC recipients |
| `format` | `parsedown` or `plaintext` |
| `file_ids` | Attachment file IDs |
| `headers` | Custom email headers |
| `group_id` | Move ticket to group |
| `bucket_id` | Move ticket to bucket |
| `status_id` | Set ticket status after send |
| `owner_id` | Set ticket owner after send |
| `custom_fields` | Ticket custom fields |
| `message_custom_fields` | Message custom fields |
| `html_template_id` | HTML template to wrap content |
| `in_reply_message_id` | Specific message ID to reply to |
| `is_autoreply` | Mark as auto-reply |
| `send_at` | Scheduled send timestamp |
| `ticket_reopen` | Reopen date if status is waiting |
| `options_gpg_encrypt` | GPG encrypt the message |
| `options_gpg_sign` | GPG sign the message |

## Examples

### Sending a Transactional Email

```kata
record.create:
  output: draft
  inputs:
    record_type: draft
    fields:
      type: mail.transactional
      to: recipient@example.com
      name: Subject line here
      params:
        to: recipient@example.com
        subject: Subject line here
        content@text:
          The plain text body of the email.
      is_queued@int: 1
  on_success:
    return:
  on_error:
    log.error: Failed to send: {{draft._errors}}
```

**Important:** Without `is_queued@int: 1`, the draft is saved but never sent. Note: `is_queued` is a bit field, so use `@int: 1` (not `@bool: yes`).

### Replying to a Ticket

```kata
record.create:
  output: draft
  inputs:
    record_type: draft
    fields:
      type: ticket.reply
      ticket_id: {{ticket_id}}
      params:
        content@text:
          Reply body here.
      is_queued@int: 1
```

### Composing a New Ticket

```kata
record.create:
  output: draft
  inputs:
    record_type: draft
    fields:
      type: mail.compose
      to: recipient@example.com
      name: Subject line here
      params:
        to: recipient@example.com
        subject: Subject line here
        group_id: {{group_id}}
        content@text:
          Message body here.
      is_queued@int: 1
```

## Policy

Restrict `record.create` to only `draft` records using principle of least privilege:

```kata
policy:
  commands:
    record.create:
      deny/type@bool: {{inputs.record_type is not record type ('draft')}}
      allow@bool: yes
```

---

## Modifying Drafts Before the Editor Opens (mail.draft trigger)

The `cerb.trigger.mail.draft` trigger fires when a worker opens a new or resumed draft. Use it to pre-populate or modify draft content before the editor is shown.

### Inputs

| Key | Description |
|-|-|
| `draft_*` | The draft record (supports key expansion). Includes `draft_type`, `draft_ticket_id`, `draft_ticket_*`, `draft_params.*`, etc. |
| `is_resumed` | `true` if the draft was resumed from a saved state, `false` if newly created |

### Return

Return a `draft: params:` dict with any fields to override. Only the keys you return are modified; omitted keys are unchanged.

```
return:
  draft:
    params:
      content: {{modified_content}}
```

### Accessing ticket and group context

From within a `mail.draft` automation, use the `draft_ticket_` prefix to access the ticket record, and `draft_ticket_group_` to access the ticket's group (including its custom fields):

```
draft_ticket_id                               # ticket ID
draft_ticket_group_reply_snippet_enabled      # group custom field (checkbox)
draft_ticket_group_reply_snippet_id           # group custom field (record link ID)
draft_ticket_group_reply_snippet_content      # linked snippet's content field
```

### Injecting content above #signature

Use `|replace` to insert text above the `#signature` marker in the draft content:

```
return:
  draft:
    params:
      content: {{draft_params.content|replace({"#signature": rendered_snippet ~ "\n\n#signature"})}}
```

If no `#signature` is present in the content, `|replace` is a no-op.

### Full example: group-configured snippet injection

```
start:
  outcome/skip:
    if@bool:
      {{
        is_resumed
        or draft_type != 'ticket.reply'
        or not draft_ticket_group_reply_snippet_enabled
        or not draft_ticket_group_reply_snippet_id
      }}
    then:
      return:

  kata.parse:
    output: results
    inputs:
      kata:
        template: {{draft_ticket_group_reply_snippet_content}}
      dict@json:
        {% do draft_ticket_ %}
        {{cerb_placeholders_list('draft_ticket_', '')|json_encode}}

  return:
    draft:
      params:
        content: {{draft_params.content|replace({"#signature": results.template ~ "\n\n#signature"})}}
```

### Event listener guard

Use the `disabled@bool` condition on the event listener to skip the automation entirely when prerequisites aren't met (avoids loading the automation at all):

```
event_kata@raw:
  automation/replySnippet:
    uri: cerb:automation:cerb.replySnippet.mailDraft
    disabled@bool:
      {{
        is_resumed
        or draft_type != 'ticket.reply'
        or not draft_ticket_group_reply_snippet_enabled
        or not draft_ticket_group_reply_snippet_id
      }}
```

Mirror this same condition as the first `outcome/skip:` inside the automation itself as a safety net.
