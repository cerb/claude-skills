---
id: "docs-automations-triggers-interaction-website-elements-llmtranscript"
title: "LLM Transcript - Interaction Form Element"
url: "https://cerb.ai/docs/automations/triggers/interaction.website/elements/llmTranscript/"
summary: "This page provides information on the 'llmTranscript' interaction form element used in Cerb's web forms."
tags: ["docs", "docs-automations"]
---
In website interactions web forms, an **llmTranscript** element displays an llm.agent: chat transcript.

```
start: # ... Run llm.agent:
    await: form: title: AI Agent elements: llmTranscript/prompt_transcript: session_id: {{ results.session_id }} hidden@bool: {{ prompt_user is empty }} tool_labels: docs_search@raw: Searching documentation: {{ query }} docs_fetch@raw: Reading documentation text/prompt_user: required@bool: yes placeholder: (ask a question about Cerb) submit: buttons: continue/send: label: Send icon: send value: send
```

 

# Syntax

### session\_id:

The transcript ID to display. This can be retrieved from llm.agent: output.

### tool\_labels:

A dictionary of tool names and the text to render in the transcript. This may include placeholders for the tool parameters.

```
tool_labels: example_tool@raw: Running tool: {{ param_name }}
```

### hidden:

This form element can be conditionally hidden.

```
hidden@bool: {{ not prompt_user }}
```
