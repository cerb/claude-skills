# Workflows

Workflows are text-based templates that define a set of records and configuration values. They enable creating and sharing features in Cerb, and synchronizing changes between environments (dev, staging, production).

When updated, changes are recorded in versioned history. Records previously created by the workflow are automatically synchronized to match. Changes can be rolled back to the last stable version.

| Since version | 11.0 |
|-|-|
| Found at | Search » Workflows |

---

## KATA Schema

```
workflow:
  name: example.newTask
  version@date: 2025-12-31T00:00:00Z
  description: This example workflow manages a task record
  requirements:
    cerb_version: >=11.0 <11.2
    cerb_plugins: cerberusweb.core,
  config:
    text/taskName:
      label: Task name:
      default: New task from a workflow
    chooser/taskOwner:
      label: Task owner:
      multiple@bool: no
      record_type: worker
      record_query: isDisabled:n

records:
  task/newTask:
    deletionPolicy: retain
    fields:
      owner_id: {{config.taskOwner_id|default(0)}}
      title: {{config.taskName}}
```

### Schema Reference

```
config:
  chooser:
    default:
    label:
    multiple@bool:
    record_query:
    record_type:
  picklist:
    default:
    label:
    options@list:
  text:
    default:
    label:
extensions:
  activity:
    id:
    label:
    message:
  permission:
    id:
    label:
  translation:
    id:
    langs:
      __lang_code__:
records:
  __record_type__:
    deletionPolicy:
    fields:
    updatePolicy:
```

---

## config:

| Type | Description |
|-|-|
| `chooser/`  | An interactive record chooser |
| `picklist/` | A single-selection dropdown or multiple-selection checkboxes |
| `text/` | A text input |

## extensions:

| Type | Description |
|-|-|
| `activity/` | Add new activity log events |
| `permission/`  | Add new custom role permissions |
| `translation/` | Add new translation phrases |

## records:

Each record is defined with a record type and unique key (e.g. `task/newTask:`).

| Key | Description |
|-|-|
| `deletionPolicy:` | If `retain`, the record won't be deleted when removed from the workflow template |
| `fields:` | A list of record fields to update |
| `updatePolicy:` | Optional comma-separated list of `fields` to update on subsequent changes after creation. If omitted, all fields are set on creation and changes. If included and blank, fields are created but not updated (preserves user-level changes) |

---

## Placeholders

To avoid conflicts with `{{placeholder}}` syntax in records like automations and snippets, workflows provide two special scripting functions:

### Static (template-time)

Replace configuration values in the template:
```
{{config.keyName}}
```

For chooser configs, expand dictionary keys:
```
{{config.keyName__label}}
```

Supports automation scripting filters:
```
{{config.keyName|lower|sha1}}
```

### Dynamic (runtime)

Read workflow config at runtime from automations, snippets, etc:
```
{{cerb_workflow_config('workflow_name')}}
{{cerb_workflow_config('workflow_name','hashSecret','default')}}
```

Look up workflow resources and their local record IDs:
```
{{cerb_workflow_resources('workflow_name')}}
```

---

## Workflow Header

| Key | Description |
|-|-|
| `name:` | Unique workflow identifier (e.g. `wgm.example.myFeature`) |
| `version@date:` | Version timestamp in ISO 8601 format |
| `description:` | Human-readable description of the workflow |
| `requirements:` | Version and plugin requirements |
| `requirements:cerb_version:` | Semver constraint (e.g. `>=11.0 <11.2`) |
| `requirements:cerb_plugins:` | Comma-separated list of required plugin IDs |
| `config:` | Interactive configuration inputs |
