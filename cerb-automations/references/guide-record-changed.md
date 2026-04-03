# Guide: record.changed Event Automations

The `record.changed` event fires whenever any record is created, updated, or deleted. Automations listening to this event should always filter by record type.

## Placeholders

| Placeholder | Description |
|-|-|
| `actor_*` | Who made the change |
| `change_type` | `created`, `updated`, or `deleted` |
| `is_new` | Boolean, true if record was just created |
| `record_*` | Current record field values (e.g. `record_owner_id`) |
| `record__type` | The record type alias (e.g. `ticket`, `task`) |
| `record__context` | The record type extension ID (e.g. `cerberusweb.contexts.ticket`), but sometimes an alias |
| `was_record_*` | Previous field values before the change (e.g. `was_record_owner_id`) |

## Filtering by Record Type

Filter in **two places** for defense in depth:

### 1. Event Listener (`disabled@bool:`)

Prevent the automation from being invoked at all for irrelevant record types.

Use the `is record type` test for reliable comparison — it works regardless of whether the value is an alias (`ticket`) or a fully-qualified extension ID (`cerberusweb.contexts.ticket`):

```kata
automation_event_listener/listener:
  fields:
    name: example.listener
    event_name: record.changed
    event_kata@raw:
      automation/myAutomation:
        uri: cerb:automation:example.myAutomation
        disabled@bool: {{record__type is not record type ('ticket')}}
```

### 2. Automation Early Exit

Guard at the top of the automation script as a safety check:

```kata
start:
  decision/isTicket:
    outcome/no:
      if@bool: {{record__type is not record type ('ticket')}}
      then:
        return:
    outcome/yes:
      then:
        # ... main logic here
```

## Key Expansion

See `guide-record-dictionaries.md` for the full reference on key expansion, event placeholders vs command output dictionaries, profile URLs, and record type checking.

## Detecting Field Changes

Compare `was_record_<field>` with `record_<field>`:

```kata
decision/isOwnerChanged:
  outcome/yes:
    if@bool: {{record_owner_id and was_record_owner_id != record_owner_id}}
    then:
      # Owner was assigned or changed
```

## Complete Example: Notify on Ticket Assignment

### Workflow

```kata
workflow:
  name: example.ticket.ownerNotify
  version@date: 2026-04-03T00:00:00Z
  description: Emails a worker when they are assigned to a ticket.
  requirements:
    cerb_version: >=11.0

records:
  automation/notifyOwner:
    fields:
      name: example.ticket.ownerNotify.changed
      extension_id: cerb.trigger.record.changed
      script@raw:
        start:
          decision/isTicket:
            outcome/no:
              if@bool: {{record__type is not record type ('ticket')}}
              then:
                return:
            outcome/yes:
              then:
                decision/isOwnerChanged:
                  outcome/yes:
                    if@bool: {{record_owner_id and was_record_owner_id != record_owner_id}}
                    then:
                      record.create:
                        output: draft
                        inputs:
                          record_type: draft
                          fields:
                            type: mail.transactional
                            to: {{record_owner_address_email}}
                            name: You've been assigned: [{{record_mask}}] {{record_subject}}
                            params:
                              to: {{record_owner_address_email}}
                              subject: You've been assigned: [{{record_mask}}] {{record_subject}}
                              content@text:
                                Hi {{record_owner_first_name}},

                                You've been assigned to ticket [{{record_mask}}] {{record_subject}}.

                                {{record_record_url}}
                            is_queued@int: 1
                        on_error:
                          log.error: Failed to send notification: {{draft._errors}}
                  outcome/skip:
                    then:
                      return:
      policy_kata@raw:
        commands:
          record.create:
            deny/type@bool: {{inputs.record_type is not record type ('draft')}}
            allow@bool: yes

  automation_event_listener/listener:
    fields:
      name: example.ticket.ownerNotify.listener
      event_name: record.changed
      event_kata@raw:
        automation/notifyOwner:
          uri: cerb:automation:example.ticket.ownerNotify.changed
          disabled@bool: {{record__type is not record type ('ticket')}}
```
