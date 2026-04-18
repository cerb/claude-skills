---
id: "docs-toolbars-interactions-automation-editor"
title: "automation.editor"
url: "https://cerb.ai/docs/toolbars/interactions/automation.editor/"
summary: "This page provides detailed instructions for configuring the toolbar in the Cerb automation editor. It guides users on how to navigate to the toolbar settings, specifically for `automation.editor`, and how to add interactions using the KATA scripting language. The page outlines the available placeholders in KATA, such as `trigger_id`, `trigger_name`, and `worker_*`, which can be used to customize the automation triggers. Additionally, it describes the expected output format for interactions, specifically the `return:` dictionary, which includes a `snippet` key for inserting text into the editor."
tags: ["docs"]
---
The toolbar displayed in the automation editor.

 

# Configuration

Navigate to **Search&nbsp;» Toolbars**.

Edit the record for `automation.editor`.

Add interactions using toolbar KATA.

```
interaction/magic: uri: cerb:automation:wgm.example.openai icon: magic tooltip: Add form elements with OpenAI hidden@bool: {{trigger_name not in ['interaction.website', 'interaction.worker',]}}
```

The following **placeholders** are available in KATA:

| Key | &nbsp; |
| --- | --- |
| `trigger_id` | The extension ID of the current automation trigger. |
| `trigger_name` | The name of the current automation trigger. |
| `worker_*` | The active worker record. Supports key expansion. |

# Interactions

### Output

The caller expects the following `return:` dictionary:

| Key | Type | &nbsp; |
| --- | --- | --- |
| **`snippet`** | string | A snippet of text to insert in the editor at the cursor |

