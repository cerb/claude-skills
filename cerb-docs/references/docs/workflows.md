---
id: "docs-workflows"
title: "Workflows"
url: "https://cerb.ai/docs/workflows/"
summary: "This page provides an overview of Cerb's Workflow KATA, a feature introduced in version 11.0, which allows users to create and manage workflows as templates with versioned updates. These workflows help synchronize related records across different environments like development, staging, and production. The page includes a sample workflow template for creating tasks with configurable names and owners, and explains the schema components such as config, extensions, and records. It details how to use placeholders and scripting functions like cerb_workflow_config() and cerb_workflow_resources() to dynamically manage workflow configurations and resources. The page also outlines the deletion and update policies for records within workflows, and provides guidance on using automation scripting filters with workflow placeholders."
tags: ["docs"]
---
https://www.youtube.com/embed/F0p2INrtq1U

**Workflows** are text-based templates that define a set of records and configuration values. They enable anyone to create and share new features in Cerb, and synchronize ongoing changes between multiple environments (e.g. dev, staging, production).

When a workflow is updated, its changes are automatically recorded in a versioned history. For instance, improvements to a workflow can be made by developers and tested on their own machines in a free, clean copy of Cerb.

A new version of a workflow can be confidently deployed to a staging or production environment and its records will be automatically synchronized. Changes with unexpected consequences can be easily rolled back to the last stable version.

We provide a [library](/resources/workflows/) of pre-built workflows for common requirements; like email auto-replies, capturing user feedback, customer satisfaction surveys, service level agreements, and more.

| **Since version:** | [11.0](/releases/11.0/) |
| **Found at:** | Search&nbsp;» Workflows |

Here's a simple workflow KATA template that creates a new task using a configurable name and owner.

```
workflow: name: example.newTask version@date: 2025-12-31T00:00:00Z description: This example workflow manages a task record requirements: cerb_version: >=11.0 <11.2 cerb_plugins: cerberusweb.core, config: text/taskName: label: Task name: default: New task from a workflow chooser/taskOwner: label: Task owner: multiple@bool: no record_type: worker record_query: isDisabled:n 
 records: task/newTask: deletionPolicy: retain fields: owner_id: {{ config.taskOwner_id|default(0) }} title: {{ config.taskName }}
```

When you make a changes to a workflow template, any records that were previously created by the workflow are automatically updated to match. The workflow manages the mapping between template "keys" and local record IDs.

- [Workflow KATA](#workflow-kata)
  - [Schema](#schema)
    - [config:](#config)
    - [extensions:](#extensions)
    - [records:](#records)

  - [Placeholders](#placeholders)
  - [Next Steps](#next-steps)

# Workflow KATA

## Schema

```
config: chooser: default: label: multiple@bool: record_query: record_type: text: default: label: extensions: activity: id: label: message: permission: id: label: translation: id: langs: __lang_code__: records: __record_type__: deletionPolicy: fields: updatePolicy:
```

### config:

| **chooser:** | An interactive record chooser. |
| **picklist:** | A single-selection dropdown or multiple-selection set of checkboxes. |
| **text:** | A text input. |

### extensions:

| **activity:** | Add new activity log events. |
| **permission:** | Add new custom role permissions. |
| **translation:** | Add new translation phrases. |

### records:

Each record is defined with a [record type](/docs/records/types/) and unique key.

For example: `task/newTask:`

| **deletionPolicy:** | If `retain` the record won't be deleted when removed from the workflow template. |
| **fields:** | A list of record [fields](/docs/records/#fields) to update. |
| **updatePolicy:** | An optional comma-separated list of `fields` to update on subsequent changes after a record is created. If omitted, all fields are set on creation and changes. If included and blank, fields are created but not updated (e.g. persist user-level changes to snippet content). |

## Placeholders

To avoid conflicts with the usual `{{placeholder}}` syntax found in records like automations and snippets, Workflow KATA provides two special scripting functions: [cerb\_workflow\_config()](/docs/scripting/functions/#cerb_workflow_config) and [cerb\_workflow\_resources()](/docs/scripting/functions/#cerb_workflow_resources).

From any feature that supports automation scripting (e.g. automations, workflows, snippets) you can use `{{cerb_workflow_config('workflow_name')}}` to dynamically read workflow configuration values at runtime. For instance, you can create a workflow just for sharing values (e.g. API keys) between multiple workflows.

Read a single key with a default value using: `{{cerb_workflow_config('workflow_name','hashSecret','default')}}`

The `{{cerb_workflow_resources('workflow_name')}}` function performs runtime lookups and returns a map of workflow resources and their local record IDs. This is useful from automations, event listeners, and toolbars.

Statically replace configuration values in the template with: `{{config.keyName}}`

If the configuration value is a `chooser:`, you can expand its dictionary keys like: `{{config.keyName__label}}`

Workflow placeholders also support automation scripting [filters](/docs/scripting/filters/), such as: `{{config.keyName|lower|sha1}}`

## Next Steps

- [Workflow Library](/resources/workflows/)

