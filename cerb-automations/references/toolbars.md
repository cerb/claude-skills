# Toolbars

Toolbars display interaction buttons in various contexts. Each toolbar is configured with KATA that defines which interactions appear and when.

Configure toolbars at: **Search » Toolbars**

---

## record.card

Displayed when viewing a record's card popup.

### Configuration

```
interaction/trackTime:
  uri: cerb:automation:example.trackTime
  tooltip: Track time
  icon: stopwatch
  hidden@bool:
    {{record__type is not pattern("task","ticket")}}
  inputs:
    record: {{record_id}}
```

### Placeholders

| Key | Description |
|-|-|
| `record_*` | The record being viewed. Supports key expansion. `record__type` is the type (e.g. `ticket`) |
| `worker_*` | The active worker record. Supports key expansion |

### Interaction

Caller: `cerb.toolbar.record.card`

**Caller params:**

| Key | Type | Description |
|-|-|-|
| `record_` | record | The record dictionary |

**Return:**

| Key | Type | Description |
|-|-|-|
| `close@bool:` | boolean | `yes` to close the card popup |

**After:**

| Key | Type | Description |
|-|-|-|
| `refresh_widgets@list:` | records | One or more card widget names to refresh |

---

## record.profile

Displayed when viewing a record's profile page.

### Configuration

```
interaction/exportTicket:
  uri: cerb:automation:example.exportTicket
  tooltip: Export ticket
  icon: download
  hidden@bool:
    {{record__type is not pattern("ticket")}}
  inputs:
    ticket: {{record_id}}
```

### Placeholders

| Key | Description |
|-|-|
| `record_*` | The record being viewed. Supports key expansion. `record__type` is the type (e.g. `ticket`) |
| `worker_*` | The active worker record. Supports key expansion |

### Interaction

Caller: `cerb.toolbar.record.profile`

**Caller params:**

| Key | Type | Description |
|-|-|-|
| `record_` | record | The record dictionary |

**Return:** No expected outputs.

**After:**

| Key | Type | Description |
|-|-|-|
| `refresh_widgets@list:` | records | One or more profile widget names to refresh |

---

## Form Elements

These elements are available in `await:form:` for `interaction.worker` triggers.

### fileDownload

Displays a button that downloads an attachment or automation resource file. Useful for interactions that generate large or binary output (dynamic images, CSV/JSON exports, ZIP archives).

```
await:
  form:
    title: Download
    elements:
      fileDownload/prompt_file:
        label: Download:
        uri: cerb:automation_resource:TOKEN
        filename: export.json
```

| Key | Description |
|-|-|
| `uri:` | URI for an attachment, automation resource, or resource to download |
| `data:` | Raw content to download (alternative to `uri:`) |
| `label:` | Optional label above the form element |
| `filename:` | Filename shown on the download button |
| `hidden:` | Conditionally hide this element |

### say

Displays formatted text (Markdown supported).

```
say/intro:
  content@text:
    **Bold text** and other Markdown.
```

| Key | Description |
|-|-|
| `content:` | Text content to display (supports Markdown) |
| `hidden:`  | Conditionally hide this element |

### text

Text input field.

```
text/prompt_name:
  label: Name:
  required@bool: yes
  type: freeform
  placeholder: Enter a name...
```

| Key | Description |
|-|-|
| `label:` | Label above the input |
| `required@bool:`  | Whether input is required |
| `type:` | Input format (freeform, date, decimal, email, uri, etc.) |
| `placeholder:` | Placeholder text |
| `default:` | Default value |
| `max_length:` | Maximum character length |
| `hidden:` | Conditionally hide this element |
| `validation@raw:` | Custom validation script |

### textarea

Multi-line text input.

```
textarea/prompt_description:
  label: Description:
  required@bool: yes
```

### chooser

Record chooser input.

```
chooser/prompt_ticket:
  label: Ticket:
  record_type: ticket
  required@bool: yes
```

| Key | Description |
|-|-|
| `label:` | Label above the input |
| `record_type:` | Record type to choose |
| `required@bool:` | Whether input is required |
| `single@bool:` | Only allow one selection |
| `default:` | Default record ID(s) |
| `hidden:` | Conditionally hide this element |

### submit

Continue/Reset buttons. Automatically added when an interaction enters `await` state.

```
submit/prompt_submit:
  continue_label: Save
  reset_label: Start Over
```

### sheet

Displays tabular data.

```
sheet/results:
  data@key: results
  schema:
    layout:
      paging@bool: yes
    columns:
      text/name:
        label: Name
      text/status:
        label: Status
```

### editor

Code/text editor with syntax highlighting.

```
editor/prompt_code:
  label: Code:
  syntax: yaml
```

### fileUpload

File upload input that creates an attachment or automation resource.

```
fileUpload/prompt_file:
  label: Upload:
  record_type: automation_resource
  required@bool: yes
```
