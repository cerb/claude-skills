---
id: "docs-automations-triggers-interaction-website"
title: "interaction.website"
url: "https://cerb.ai/docs/automations/triggers/interaction.website/"
summary: "This webpage provides a detailed overview of interaction.website automations, which facilitate interactions with visitors on third-party websites through multi-step workflows that can pause and resume. These interactions are applicable for various purposes such as surveys, sign-up forms, contact forms, troubleshooters, and customer service bots. The page outlines the inputs and outputs of these interactions, including the use of forms and delegate interactions to enhance modularity and reusability. It also explains the process of initiating interactions through website elements or shared links and concludes with instructions on installation and implementation on websites."
tags: ["docs", "docs-automations"]
---
https://www.youtube.com/embed/dkpaBooNNGc

**interaction.website** automations are interactions with visitors on third-party websites that use continuations to pause and resume a multi-step workflow.

On websites, this can be used for surveys, sign-up forms, contact forms, troubleshooters, customer service bots, and much more.

- Inputs
- Outputs
  - await:form:
  - await:interaction:
  - return:

- Deploy interactions on websites

 

Website interactions are usually started on any website when a page element is interacted with – a link, button, image, etc.

A website interaction can also be started with a shared link.

At its conclusion, an interaction returns a dictionary and exit state to the caller, which is then responsible for acting on the results.

# Inputs

An interaction automation dictionary starts with the following input values:

| Key | Type | Notes |
| --- | --- | --- |
| `interaction` | string | The name of the interaction. |
| `interaction_params` | dictionary | Arbitrary interaction parameters. |
| `inputs` | dictionary | Custom input values from the caller. |
| `client_browser_name` | string | The client browser name (e.g. Safari). |
| `client_browser_platform` | string | The client browser platform (e.g. Macintosh). |
| `client_browser_version` | string | The client browser version. |
| `client_ip` | string | The client IP address. |
| `portal` | record | The community portal. |

# Outputs

## await:form:

When suspending in the `await` state, the interaction displays a web form with the desired elements. The form may prompt for user input, validate it, and set dictionary keys (placeholders) with the responses.

```
await: form: title: Your form title elements: # ...
```

### title:

The title of this form to be displayed in the interaction popup. This is usually a summary of the current step.

### elements:

Form elements are defined with a key in the format `type/name:`.

The `name` must be unique within the form. When an element prompts for user input, a placeholder with the same name will be created with their response. For instance, `text/prompt_name:` will create a placeholder of `{{prompt_name}}` with the value of that text element.

A form can be created with any combination of the following element types:

| Element | &nbsp; |
| --- | --- |
| **fileUpload:** | File upload prompt |
| **llmTranscript:** | AI agent chat transcript |
| **say:** | Block of text or Markdown |
| **sheet:** | Sheet with row selection |
| **submit:** | Continue to next step |
| **text:** | Text input with data types |
| **textarea:** | Multiple lines of text |

When the interaction suspends in the `await` state, a `submit:` element is automatically appended to the form if one doesn't already exist.

```
start: await/who: form: title: Introduction elements: text/prompt_name: label: What is your name? required@bool: yes   
   await/hello: form: title: Hello! elements: say/hello: content: Hello, {{ prompt_name }} !   
   return: user: name@key: prompt_name
```

## await:interaction:

When suspending in the `await:interaction:` state, the interaction temporarily hands control to another delegate interaction. The interaction resumes at the current point when the delegate exits.

Delegates can be nested to any depth. For instance, a reusable delegate could handle email or SMS validation, and be shared by many other interactions.

This makes interactions much more modular and reusable.

### uri:

The `uri:` parameter specifies the delegate automation. This must use the interaction.website trigger.

### inputs:

An optional dictionary of `inputs:` for the given `uri:` interaction.

### output:

An `output:` key specifies the placeholder that should receive the results from the delegate.

```
start: while: if@bool: yes do: await/menu: form: title: Menu elements: say: message: How can we help? sheet/prompt_menu: required@bool: yes data: 0: key: map label: Map 1: key: echo label: Echo schema: layout: style: buttons headings@bool: no paging@bool: no title_column: label columns: selection/key: params: mode: single text/label: submit: continue@bool: no reset@bool: no await/do: interaction: output: results uri@text: cerb:automation:{{{ 'map': 'wgm.interaction.locationByIP', 'echo': 'wgm.interaction.echo', }[prompt_menu]}}
```

## return:

When the interaction concludes in the `return` state, it returns any number of key/value pairs to the caller. Keys may be nested to return dictionaries.

# Deploy interactions on websites

See the Add a conversational bot to any website guide for instructions on deploying interactions on any website.

