---
id: "docs-toolbars-interactions-draft-read"
title: "draft.read"
url: "https://cerb.ai/docs/toolbars/interactions/draft.read/"
summary: "This page provides detailed information on configuring and using the `draft.read` toolbar in Cerb when reading a mail draft. It guides users on how to navigate to the toolbar settings, edit the `draft.read` record, and add interactions using toolbar KATA. The page outlines available placeholders for draft and worker records, and describes the interactions, including the caller parameters and expected outputs. It also specifies how to refresh widgets after interactions."
tags: ["docs"]
---
The `draft.read` toolbar is displayed when reading a mail draft.

 

# Configuration

Navigate to **Search&nbsp;» Toolbars**.

Edit the record for `draft.read`.

Add interactions using toolbar KATA.

```
interaction/example: uri: cerb:automation:example.draft.delete label: Delete icon: circle-remove
```

The following **placeholders** are available in KATA:

| Key | &nbsp; |
| --- | --- |
| `draft_*` | The draft record being viewed. Supports key expansion. |
| `worker_*` | The active worker record. Supports key expansion. |

# Interactions

Caller: `cerb.toolbar.draft.read`

### Inputs

The following `caller_params` are passed interactions:

| Key | Type | &nbsp; |
| --- | --- | --- |
| **`selected_text`** | string | The currently selected editor text |

### Output

(none)

### after:

| Key | Type | &nbsp; |
| --- | --- | --- |
| **`refresh_widgets@list:`** | records | One or more profile widget names to refresh |

