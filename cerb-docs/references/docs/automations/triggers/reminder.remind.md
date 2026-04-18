---
id: "docs-automations-triggers-reminder-remind"
title: "reminder.remind"
url: "https://cerb.ai/docs/automations/triggers/reminder.remind/"
summary: "This page provides information about the 'reminder.remind' automation trigger in Cerb, which is activated by a reminder alarm. It explains that this trigger utilizes event handler KATA, executing all enabled automations. The page details the inputs available in the automation dictionary, including custom input values from the caller and the reminder record, which supports key expansion. There are no outputs specified for this trigger."
tags: ["docs", "docs-automations"]
---
**reminder.remind** automations are triggered by a reminder alarm.

This trigger uses event handler KATA, and all enabled automations are executed.

- Inputs
- Outputs

# Inputs

The automation dictionary starts with the following values:

| Key | Type | Notes |
| --- | --- | --- |
| `inputs` | dictionary | Custom input values from the caller |
| `reminder_*` | record | The reminder record (supports key expansion) |

# Outputs

(none)

