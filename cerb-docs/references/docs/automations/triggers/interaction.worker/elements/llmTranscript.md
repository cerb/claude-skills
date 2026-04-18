---
id: "docs-automations-triggers-interaction-worker-elements-llmtranscript"
title: "LLM Transcript - Interaction Form Element"
url: "https://cerb.ai/docs/automations/triggers/interaction.worker/elements/llmTranscript/"
summary: "This page provides information on the 'llmTranscript' interaction form element used in Cerb's web forms."
tags: ["docs", "docs-automations"]
---
In worker interaction web forms, an **llmTranscript** element displays an llm.agent: chat transcript.

```
start: # ... Run llm.agent:
    await: form: title: Cerb Docs Q&A elements: llmTranscript/prompt_transcript: session_id: {{ results.session_id }} hidden@bool: {{ prompt_user is empty }} tool_labels: search_docs@raw: Searching documentation: {{ query }} fetch_doc@raw: Reading documentation
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
