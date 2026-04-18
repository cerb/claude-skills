---
id: "docs-toolbars-interactions-mail-read"
title: "mail.read"
url: "https://cerb.ai/docs/toolbars/interactions/mail.read/"
summary: "This page provides detailed instructions on configuring the message toolbar for viewing email messages on a ticket profile page in Cerb. It guides users on how to navigate to the toolbar settings, edit the `mail.read` record, and add interactions using toolbar KATA. The page outlines available placeholders for KATA, such as message, widget, and worker records, and describes the interactions, inputs, and expected outputs for the `cerb.toolbar.mail.read` caller. It also explains how to handle outputs, including refreshing profile widgets."
tags: ["docs"]
---
The message toolbar is displayed when viewing email messages on a ticket profile page.

 

### Configuration

Navigate to **Search&nbsp;» Toolbars**.

Edit the record for `mail.read`.

Add interactions using toolbar KATA.

```
interaction/feedback: label: Capture Feedback icon: conversation uri: cerb:automation:example.captureFeedback # after:
```

The following **placeholders** are available in KATA:

| Key | &nbsp; |
| --- | --- |
| `message_*` | The message record. Supports key expansion. |
| `widget_*` | The widget record. Supports key expansion. `widget__type` will be one of: card\_widget, profile\_widget, or workspace\_widget. |
| `worker_*` | The active worker record. Supports key expansion. |

# Interactions

Caller: `cerb.toolbar.mail.read`

### Inputs

The following `caller_params` are passed to the interaction:

| Key | Type | &nbsp; |
| --- | --- | --- |
| **`message_id`** | record | The message record |
| **`selected_text`** | string | The currently selected text |

### Output

The caller expects the following `return:` dictionary:

| Key | Type | &nbsp; |
| --- | --- | --- |
| **`reply:draft_id:`** | record | The draft ID to resume |

### after:

| Key | Type | &nbsp; |
| --- | --- | --- |
| **`refresh_widgets@list:`** | records | One or more profile widget names to refresh |

