# Cerb Automations Reference

Automations are **self-contained state machines** written in KATA that transform an **input dictionary** into an **output dictionary**. They enable workflow customization throughout Cerb.

Automations use the KATA automation dialect — see `kata.md` for the base KATA syntax, annotations, scripting functions, and filters.

---

## Table of Contents

- [Structure](#structure)
  - [Inputs](#inputs)
  - [Start Block](#start-block)
  - [Exit States](#exit-states)
  - [Error Handling](#error-handling)
  - [Simulation](#simulation)
  - [Continuations](#continuations)
  - [Timers](#timers)
  - [Naming Repeated Commands](#naming-repeated-commands)
- [Commands](#commands)
  - [State Transitions](#state-transition-commands)
    - [return:](#return)
    - [error:](#error)
    - [await:](#await)
  - [Flow Control](#flow-control-commands)
    - [decision:](#decision)
    - [outcome:](#outcome)
    - [repeat:](#repeat)
    - [while:](#while)
  - [Variable Operations](#variable-commands)
    - [set:](#set)
    - [var.set:](#varset)
    - [var.push:](#varpush)
    - [var.unset:](#varunset)
    - [var.expand:](#varexpand)
  - [Record Operations](#record-commands)
    - [record.create:](#recordcreate)
    - [record.get:](#recordget)
    - [record.search:](#recordsearch)
    - [record.update:](#recordupdate)
    - [record.upsert:](#recordupsert)
    - [record.delete:](#recorddelete)
  - [HTTP](#http-commands)
    - [http.request:](#httprequest)
  - [Data Queries](#data-query-commands)
    - [data.query:](#dataquery)
  - [Functions](#function-commands)
    - [function:](#function)
  - [Storage](#storage-commands)
    - [storage.get:](#storageget)
    - [storage.set:](#storageset)
    - [storage.delete:](#storagedelete)
  - [File Operations](#file-commands)
    - [file.read:](#fileread)
    - [file.write:](#filewrite)
  - [KATA Parsing](#kata-parsing-commands)
    - [kata.parse:](#kataparse)
  - [LLM (AI)](#llm-commands)
    - [llm.chat:](#llmchat)
    - [llm.agent:](#llmagent)
    - [llm.embed:](#llmembed)
  - [Queues](#queue-commands)
    - [queue.push:](#queuepush)
    - [queue.pop:](#queuepop)
  - [Metrics](#metric-commands)
    - [metric.increment:](#metricincrement)
  - [Email](#email-commands)
    - [email.parse:](#emailparse)
  - [Encryption](#encryption-commands)
    - [encrypt.pgp:](#encryptpgp)
    - [decrypt.pgp:](#decryptpgp)
  - [API](#api-commands)
    - [api.command:](#apicommand)
  - [Logging](#logging-commands)
    - [log: / log.warn: / log.error: / log.alert:](#log)
  - [Simulation Commands](#simulation-commands)
    - [simulate.success:](#simulatesuccess)
    - [simulate.error:](#simulateerror)
- [Triggers](#triggers)
  - [automation.function](#automationfunction)
  - [automation.timer](#automationtimer)
  - [interaction.worker](#interactionworker)
  - [interaction.website](#interactionwebsite)
  - [webhook.respond](#webhookrespond)
  - [data.query (trigger)](#dataquery-trigger)
  - [scripting.function](#scriptingfunction)
  - [llm.tool](#llmtool)
  - [ui.widget](#uiwidget)
  - [ui.sheet.data](#uisheetdata)
  - [ui.chart.data](#uichartdata)
  - [resource.get](#resourceget)
  - [reminder.remind (trigger)](#reminderremind-trigger)
  - [map.clicked](#mapclicked)
  - [projectBoard.cardAction](#projectboardcardaction)
  - [projectBoard.renderCard](#projectboardrendercard)
  - [behavior.action](#behavioraction)
  - [interaction.worker.explore](#interactionworkerexplore)
- [Events](#events)
  - [mail.draft](#maildraft)
  - [mail.draft.validate](#maildraftvalidate)
  - [mail.filter](#mailfilter)
  - [mail.moved](#mailmoved)
  - [mail.received](#mailreceived)
  - [mail.reply.validate](#mailreplyvalidate)
  - [mail.route](#mailroute)
  - [mail.send](#mailsend)
  - [mail.sent](#mailsent)
  - [record.changed](#recordchanged)
  - [record.merge](#recordmerge)
  - [record.merged](#recordmerged)
  - [record.viewed](#recordviewed)
  - [reminder.remind (event)](#reminderremind-event)
  - [worker.authenticate.failed](#workerauthenticatefailed)
  - [worker.authenticated](#workerauthenticated)
- [Policies](#policies)
  - [Callers Scope](#callers-scope)
  - [Commands Scope](#commands-scope)
  - [Time Limits](#time-limits)

---

## Structure

### Inputs

Automations can define optional `inputs:` at the top level. Input types:

| Type | Description |
|-|-|
| `array:` | An array of values |
| `record:`  | A single record ID of a given type (converted to dictionary) |
| `records:` | Multiple record IDs (converted to array of dictionaries) |
| `text:` | Text with optional data type |

Each input can specify `required@bool: yes` and `snippet:` for editor insertion examples.

```
inputs:
  record/ticket:
    record_type: ticket
    required@bool: yes
  text/subject:
    type: freeform
    required@bool: yes
    snippet:
      subject: Example subject

start:
  return:
    result@text:
      Changed subject on {{inputs.ticket.mask}} to: {{inputs.subject}}
```

Input values are accessed via the `inputs` placeholder (e.g., `{{inputs.ticket.id}}`).

### Start Block

All automations begin execution at the `start:` command. The working memory dictionary starts as a copy of the automation inputs and is modified during execution.

### Exit States

| State | Description |
|-|-|
| `return` | Completed successfully; output in `__return:` |
| `await`  | Paused awaiting additional input; creates a continuation |
| `error`  | Failed; error message in `__return:error:` |
| `exit` | Exited without success or failure (default if no explicit exit) |

### Error Handling

Commands can include `on_success:` and `on_error:` handlers:

- **Without `on_error:`** — a command failure immediately exits the automation in the `error` state
- **With `on_error:`** — execution can recover and continue

```
start:
  http.request:
    output: http_response
    inputs:
      method: GET
      url: https://api.example/data
    on_success:
      return:
        data@key: http_response:body
    on_error:
      return:
        error: Request failed
```

The `on_error:` handler's output placeholder receives a dictionary containing `error` (the error message).

### Simulation

Commands can provide `on_simulate:` handlers with alternative execution for development testing. Two special commands are available inside `on_simulate:`:

- `simulate.success:` — sets mock output and executes `on_success:`
- `simulate.error:` — sets mock output and executes `on_error:`

```
start:
  http.request:
    output: http_response
    inputs:
      method: GET
      url: https://api.example/data
    on_simulate:
      simulate.success:
        status_code: 200
        content_type: application/json
        body: {"result": "simulated"}
    on_success:
      return:
        body@key: http_response:body
```

### Continuations

When an automation exits in `await:` state, a snapshot of its working dictionary is saved with a long random identifier. This **continuation** enables resuming from the exact suspension point later with new input. An automation can `await` multiple times before concluding.

### Timers

Automations can run at scheduled future times (once or recurring). Timer components:
- **name** — timer identifier
- **datetime** — future execution time
- **schedule** — optional Unix CRON expression for recurring
- **events** — KATA block selecting the automation

When an automation ends in `await`, a continuation saves the pause point and the timer reschedules for the specified datetime.

### Naming Repeated Commands

When the same command appears multiple times under the same parent, each must have a unique name via `/identifier`:

```
start:
  set/first:
    a: 5
  set/second:
    b: 4
  return:
    answer: {{a * b}}
```

---

## Commands

### State Transition Commands

#### return:

Successfully terminates the automation. Returns a dictionary whose expected keys depend on the trigger.

```
start:
  set:
    name: Kina
  return:
    output@text:
      Hello, {{name}}!
```

#### error:

Unsuccessfully terminates the automation with an error message.

```
start:
  error: An unexpected error occurred!
```

The text becomes the error message returned to the caller (`__return:error:`).

#### await:

Pauses the automation in the `await` state and yields a dictionary. Creates a continuation for resuming.

```
start:
  await:
    form:
      title: Intro
      elements:
        text/prompt_name:
          label: What is your name?
          required@bool: yes
  return:
    output@text:
      Hello, {{prompt_name}}!
```

Supported by triggers: `automation.timer`, `interaction.worker`, `interaction.website`, `mail.draft.validate`, `mail.reply.validate`.

The returned dictionary structure varies by trigger (e.g., `form:` for interactions, `until@date:` for timers).

---

### Flow Control Commands

#### decision:

Conditionally selects one of multiple potential outcomes. First matching outcome executes (first-match semantics).

```
start:
  decision:
    outcome/weekend:
      if@bool: {{'now'|date('l') in ['Saturday','Sunday'] ? 'yes'}}
      then:
        return:
          output: It is the weekend.
    outcome/weekday:
      then:
        return:
          output: It is a weekday.
```

An outcome without `if@bool:` acts as a default/catch-all.

#### outcome:

A conditional sequence of commands used inside `decision:`. Each outcome requires a unique `/identifier`.

| Parameter  | Description |
|-|-|
| `if@bool:` | Boolean condition. Expected: `yes` or `no` (empty/absent = no match) |
| `then:` | Command sequence to execute when condition matches |

#### repeat:

Iterates an array and executes commands for each value.

```
start:
  set:
    sum: 0
  repeat:
    each@json: [1,2,3,4,5,6,7,8,9,10]
    as: i
    do:
      set:
        sum@int: {{sum + i}}
  return:
    sum@key: sum
```

| Parameter | Required | Description |
|-|-|-|
| `each:` | Yes | Array to iterate. Supports `@csv`, `@json`, `@list` |
| `as:` | Yes | Placeholder name for current value. Format `key, value` for both key and value |
| `do:` | Yes | Commands to repeat |

#### while:

Conditionally loops a sequence of commands.

```
start:
  set:
    counter: 0
  while:
    if@bool: {{counter < 5 ? 'yes'}}
    do:
      set:
        counter: {{counter + 1}}
  return:
    counter@key: counter
```

| Parameter  | Required | Description |
|-|-|-|
| `if@bool:` | Yes | Loop continues while `true` |
| `do:` | Yes | Commands to execute each iteration |

---

### Variable Commands

#### set:

Sets one or more placeholders. Supports type annotations, nested dictionaries, and sequential references within the same block.

```
start:
  set:
    a@int: 2
    b@int: {{a * 2}}
    person:
      name: Kina
      role:
        title: Customer Support Manager
  return:
    output@text: {{person.name}} is a {{person.role.title}}
```

No `on_success`/`on_error`/`on_simulate` handlers — this is a simple assignment.

#### var.set:

Sets a value at a key path (colon-delimited).

```
start:
  set:
    person:
      name:
        first: Kina
  var.set:
    inputs:
      key: person:name:last
      value: Halpue
  return:
    output@text: {{person.name.first}} {{person.name.last}}
```

| Input | Required | Description |
|-|-|-|
| `key:` | Yes | Colon-delimited key path |
| `value:` | Yes | Value to set |
| `delimiter:` | No | Custom delimiter (default `:`) |

Handlers: `on_simulate:`, `on_success:` (output = new value), `on_error:` (output.error).

#### var.push:

Appends a value to an array.

```
start:
  set:
    numbers@csv: 1,2,3,4
  var.push:
    output: result
    inputs:
      key: numbers
      value: 5
  return:
    output: {{numbers|join(', ')}}
```

| Input | Required | Description |
|-|-|-|
| `key:` | Yes | Colon-delimited key path to array |
| `value:` | Yes | Value to append |

Handlers: `on_simulate:`, `on_success:` (output = new array), `on_error:`.

#### var.unset:

Removes a placeholder at a key path.

```
start:
  set:
    person:
      name:
        first: Kina
        last: Halpue
      phone: +15551234321
  var.unset:
    inputs:
      key: person:phone
  return:
    person@key: person
```

| Input  | Required | Description |
|-|-|-|
| `key:` | Yes | Colon-delimited key path(s) to unset |

Handlers: `on_simulate:`, `on_success:` (output = true if found, false otherwise), `on_error:`.

#### var.expand:

Expands nested keys at a given dictionary path (lazy-loads related data).

```
start:
  var.expand:
    inputs:
      key: inputs:tickets
      paths: owner_,customfields
  return:
    owners@json: {{array_column(inputs.tickets,'owner__label','_label')|json_encode}}
```

| Input | Required | Description |
|-|-|-|
| `key:` | No | Colon-delimited path to expand (root if omitted) |
| `paths:` | Yes | Which paths to expand at the dictionary keys |

Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### Record Commands

#### record.create:

Creates a new record.

```
start:
  record.create/newTask:
    output: new_task
    inputs:
      record_type: task
      fields:
        title: This is a new task
        status: open
        importance: 50
    on_success:
      return:
        task_id: {{new_task.id}}
```

| Input | Required | Description |
|-|-|-|
| `record_type:` | Yes | Record type to create |
| `fields:` | Yes | Fields to set (varies by record type) |
| `expand:` | No | Keys to expand in output dictionary |
| `disable_events@bool:` | No | Skip triggering events (useful for imports) |

Output: Record dictionary. Handlers: `on_simulate:`, `on_success:`, `on_error:`.

#### record.get:

Retrieves a single record by type and ID.

```
start:
  record.get:
    output: record
    inputs:
      record_type: task
      record_id: 123
    on_success:
      return:
        label: {{record._label}}
```

| Input | Required | Description |
|-|-|-|
| `record_type:` | Yes | Record type to load |
| `record_id:` | Yes | Record ID |

Output: Record dictionary. Handlers: `on_simulate:`, `on_success:`, `on_error:`.

#### record.search:

Searches records and returns matching dictionaries.

```
start:
  record.search:
    output: results
    inputs:
      record_type: ticket
      record_query: status:${status} limit:10
      record_query_params:
        status: o
      record_expand: group_,bucket_,owner_,customfields
    on_success:
      return:
        tickets@key: results
```

| Input | Required | Description |
|-|-|-|
| `record_type:` | Yes | Record type to search |
| `record_query:` | Yes | Search query. `limit:1` returns single dict instead of array |
| `record_query_params:` | No | Parameters referenced as `${param}` in queries (sanitizes user input) |
| `record_expand:` | No | Comma-separated keys to expand in each result dictionary (e.g. `content,sender_,worker_,attachments`). Use this instead of a separate `var.expand:` step |
| `validation@raw:` | No | Template where non-empty output triggers `on_error:` |

Output: Array of record dictionaries (or single dict with `limit:1`). Handlers: `on_simulate:`, `on_success:`, `on_error:`.

**Deep search filters:** Some search query filters like `on.*:` (for comments) perform deep searches into the target record type. These require nested query syntax: `on.ticket:(id:${id})`, not `on.ticket:${id}`.

**Key expansion preference:** Use `customfields` instead of `custom_` for expanding custom fields. The `customfields` key returns human-readable URIs as field keys, while `custom_` only returns numeric IDs.

#### record.update:

Updates an existing record.

```
start:
  record.update:
    output: updated_record
    inputs:
      record_type: task
      record_id: 123
      fields:
        importance: 90
```

| Input | Required | Description |
|-|-|-|
| `record_type:` | Yes | Record type |
| `record_id:` | Yes | Record ID |
| `fields:` | Yes | Fields to update |
| `disable_events@bool:` | No | Skip triggering events |

Output: Updated record dictionary. Handlers: `on_simulate:`, `on_success:`, `on_error:`.

#### record.upsert:

Creates or updates a record. Zero query matches = create; one match = update; multiple matches = error (unless `limit:1 sort:` used).

```
start:
  record.upsert:
    output: record
    inputs:
      record_type: task
      record_query: name:"My task" status:open
      fields:
        importance: 75
```

| Input | Required | Description |
|-|-|-|
| `record_type:` | Yes | Record type |
| `record_query:` | Yes | Search query for matching  |
| `record_query_params:` | No | Sanitized query parameters |
| `fields:` | Yes | Fields to set |
| `disable_events@bool:` | No | Skip triggering events |

Output: Record dictionary. Handlers: `on_simulate:`, `on_success:`, `on_error:`.

#### record.delete:

Deletes a record.

```
start:
  record.delete:
    output: results
    inputs:
      record_type: task
      record_id: 123
```

| Input | Required | Description |
|-|-|-|
| `record_type:` | Yes | Record type |
| `record_id:` | Yes | Record ID |

Output: Deleted record dictionary. Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### HTTP Commands

#### http.request:

Sends HTTP requests and returns responses. Supports streaming large uploads/downloads.

```
start:
  http.request/getData:
    output: http_response
    inputs:
      method: GET
      url: https://api.example/data
      headers@text:
        Authorization: Bearer {{api_token}}
        Accept: application/json
      timeout: 10
    on_success:
      set:
        body@json: {{http_response.body}}
      return:
        data@key: body
    on_error:
      error: HTTP request failed: {{http_response.error}}
```

**Inputs:**

| Input | Required | Description |
|-|-|-|
| `method:` | No | HTTP verb: GET (default), POST, PUT, PATCH, DELETE, HEAD, OPTIONS |
| `url:` | Yes | Endpoint URL |
| `headers:` | No | HTTP header key/value pairs. Use `headers@text:` for multi-line |
| `body:` | No | Request payload. Dictionaries auto-encode based on Content-Type. Use `body@text:` for raw text  |
| `timeout:` | No | Duration in seconds (decimal allowed, e.g., `0.5`) |
| `authentication:` | No | Connected account URI: `cerb:connected_account:<name>`. OAuth2 adds bearer tokens automatically |
| `response:` | No | Force automation resource output. Key: `expires` |

**Output dictionary:**

| Key | Type | Description |
|-|-|-|
| `status_code`  | int | HTTP response code |
| `url` | string | Endpoint URL |
| `content_type` | string | Response MIME type |
| `headers` | dict | Response headers (lowercase keys, dashes preserved) |
| `body` | string | Response payload |
| `is_data_uri`  | bool | True if base64-encoded (binary responses auto-converted) |
| `is_cerb_uri`  | bool | True if stored as automation resource (responses >1MB) |

**POST with JSON body:**
```
start:
  http.request/post:
    output: http_response
    inputs:
      method: POST
      url: https://api.example/employee
      headers@text:
        Content-Type: application/json
      body:
        name: Kina
        title: Support Manager
    on_simulate:
      simulate.success:
        status_code@int: 200
        content_type: application/json
        body: {"status": true, "id": 123}
    on_success:
      set:
        response@json: {{http_response.body}}
      return:
        id: {{response.id}}
```

**Streaming large file upload:**
```
start:
  http.request/upload:
    output: http_response
    inputs:
      method: POST
      url: https://api.example/upload
      headers@text:
        Content-Type: application/vnd.cerb.uri
      body@text:
        cerb:attachment:123
```

Handlers: `on_simulate:`, `on_success:`, `on_error:` (output includes `error` key plus response details).

---

### Data Query Commands

#### data.query:

Executes a data query and returns results.

```
start:
  data.query:
    output: results
    inputs:
      query@text:
        type:worklist.records
        of:ticket
        query:(status:open)
        format:dictionaries
      query_params:
        status: o
    on_success:
      return:
        records@key: results:data
```

| Input | Required | Description |
|-|-|-|
| `query@text:` | Yes | Data query to execute |
| `query_params:` | No | Sanitized parameters referenced as `${param}` |

**Output dictionary:**

| Key | Description |
|-|-|
| `data` | Query results  |
| `_` | Query metadata |

Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### Function Commands

#### function:

Executes an `automation.function` automation and returns its output.

```
start:
  function/sum:
    uri: cerb:automation:example.math.sum
    output: result
    inputs:
      numbers@csv: 2,4,8
    on_success:
      return:
        sum@key: result:sum
```

| Parameter | Required | Description |
|-|-|-|
| `uri:` | Yes | Automation URI: `cerb:automation:<name>` |
| `inputs:` | Varies | Inputs specific to the function |
| `output:` | Yes | Placeholder for results |

Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### Storage Commands

Long-term key/value storage shared between automations and invocations.

#### storage.get:

```
start:
  storage.get:
    output: result
    inputs:
      key: some.arbitrary.identifier
      default: fallback value
```

| Input | Required | Description |
|-|-|-|
| `key:` | Yes | Storage identifier |
| `default:` | No | Value when key doesn't exist |

#### storage.set:

```
start:
  storage.set:
    output: result
    inputs:
      key: some.arbitrary.identifier
      value: stored data
      expires: +15 mins
```

| Input | Required | Description |
|-|-|-|
| `key:` | Yes | Storage identifier |
| `value:` | Yes | Value to store |
| `expires:` | No | Expiration date/time (e.g., `+2 hours`). Omit for no expiration |

Output: dictionary with `key` and `expires`.

#### storage.delete:

```
start:
  storage.delete:
    inputs:
      key: some.arbitrary.identifier
```

| Input  | Required | Description |
|-|-|-|
| `key:` | Yes | Storage identifier to delete |

All storage commands support: `on_simulate:`, `on_success:`, `on_error:`.

---

### File Commands

#### file.read:

Reads bytes from attachments or automation resources.

```
start:
  file.read:
    output: results
    inputs:
      uri: cerb:attachment:123
      offset: 0
      length: 1024000
```

| Input | Required | Description |
|-|-|-|
| `uri:` | Yes | Record URI: `cerb:attachment:<id>`, `cerb:automation_resource:<guid>`, `cerb:resource:<name>` |
| `filters:` | No | E.g., `gzip.decompress:` |
| `offset:` | No | Byte position to start (default 0) |
| `length:` | No | Bytes to read (default 1024000 / 1MB) |
| `length_split:` | No | Sequence to split on (e.g., `length_split@json: "\n"` for JSONL) |
| `password:` | No | Password for encrypted ZIP archives |

**Output dictionary:**

| Key | Description |
|-|-|
| `bytes` | File bytes (base64 if binary) |
| `uri` | Record URI |
| `name` | Filename |
| `offset_from` | First byte of read range |
| `offset_to` | Last byte of read range |
| `mime_type` | MIME type |
| `size` | Total file size |

#### file.write:

Writes bytes to an automation resource record.

```
start:
  file.write:
    output: result
    inputs:
      content:
        text: File content here
      name: example.txt
      mime_type: text/plain
      expires@date: +15 mins
```

| Input | Required | Description |
|-|-|-|
| `content:` | Yes | Content to write: `bytes:`, `text:`, or `zip:` |
| `expires:` | No | Expiration (default +15 minutes) |
| `mime_type:` | No | MIME type (default application/octet-stream) |
| `name:` | No | Filename |
| `uri:` | No | Append to existing resource |

**ZIP content:**
```
content:
  zip:
    password: optional
    files:
      file/readme:
        path: /readme.txt
        bytes: File content
      file/data:
        uri: cerb:attachment:123
```

**Output dictionary:** `uri`, `id`, `name`, `mime_type`, `size`, `token`, `expires_at`.

Both file commands support: `on_simulate:`, `on_success:`, `on_error:`.

---

### KATA Parsing Commands

#### kata.parse:

Parses an arbitrary KATA document with placeholder substitution.

```
start:
  kata.parse:
    output: results
    inputs:
      kata@raw:
        greeting@text:
          Hello {{name}}! Welcome to {{company}}.
      dict:
        name: Janey
        company: Cerb
  return:
    output: {{results.greeting}}
```

| Input | Required | Description |
|-|-|-|
| `kata@raw:` | Yes | KATA document (use `@raw` to prevent premature substitution) |
| `dict:` | No | Dictionary for placeholder replacement |
| `schema:` | No | Validation schema |

**Schema keys:** `multiple@bool:`, `required@bool:`, `types:` (array, bool, list, object, text).

Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### LLM Commands

#### llm.chat:

Single-turn chat completions without transcripts, memory, or tools.

```
start:
  llm.chat:
    output: result
    inputs:
      llm:
        anthropic:
          model: claude-sonnet-4-20250514
          authentication: cerb:connected_account:anthropic
      system_prompt@text:
        You are a helpful assistant.
      messages:
        0:
          role: user
          content: What is the sentiment of this message?
    on_success:
      return:
        response: {{result.messages.0.content}}
```

| Input | Required | Description |
|-|-|-|
| `llm:` | Yes | Provider and model configuration |
| `messages:` | Yes | Message list with `role` and `content`. Final message must be `role: user` |
| `system_prompt:` | No | LLM instructions |

**Supported providers:** `anthropic:`, `aws_bedrock:`, `docker:`, `gemini:`, `groq:`, `huggingface:`, `ollama:`, `openai:`, `together:`

Each provider requires `model:` and `authentication:` (URI format: `cerb:connected_account:<name>`). Some (ollama, docker) need `api_endpoint_url:`.

**Output:** `messages` array, each with `type` ("text") and `content`.

#### llm.agent:

Conversational AI with tools and multi-turn transcripts.

```
start:
  llm.agent:
    output: result
    inputs:
      llm:
        anthropic:
          model: claude-sonnet-4-20250514
          authentication: cerb:connected_account:anthropic
      system_prompt@text:
        You are a helpful assistant.
      messages:
        0:
          role: user
          content: Search for docs about webhooks
      tools:
        automation/docs_search:
          uri: cerb:automation:docs.search
        tool/custom_action:
          description: Perform a custom action
          parameters:
            string/input_name:
              description: Parameter description
              required@bool: yes
    on_tool:
      decision:
        outcome/docs_search:
          if@bool: {{__tool.name == 'docs_search'}}
          then:
            # Tool is handled automatically by the linked automation
        outcome/custom_action:
          if@bool: {{__tool.name == 'custom_action'}}
          then:
            tool.return:
              content: Custom result here
    on_success:
      return:
        response: {{result.messages|last.content}}
```

**Tool types:**
- `automation/<id>:` — links to `llm.tool` automation via `uri:` (description/inputs auto-extracted)
- `tool/<id>:` — custom tool with `description:` and `parameters:` (string, number, boolean types)

**on_tool handler:** `__tool` dictionary has: `__tool.name`, `__tool.id`, `__tool.parameters`. Return results via `tool.return:`.

#### llm.embed:

Generate text vector embeddings.

```
start:
  llm.embed:
    output: results
    inputs:
      llm:
        openai:
          model: text-embedding-3-large
          authentication: cerb:connected_account:openai
      texts:
        0: What is Cerb?
        1: Cerb automates customer service workflows.
    on_success:
      return:
        embeddings@key: results:embeddings
```

**Embedding providers:** `aws_bedrock:`, `docker:`, `gemini:`, `huggingface:`, `ollama:`, `openai:`, `pinecone:`, `together:`, `voyage:`

**Output:** `embeddings` — list of float arrays.

All LLM commands support: `on_simulate:`, `on_success:`, `on_error:`.

---

### Queue Commands

#### queue.push:

Push messages to a queue.

```
start:
  queue.push:
    output: results
    inputs:
      queue_name: example.queue
      messages:
        0:
          id: msg0
          priority: high
      available_at@date: +5 mins
```

| Input | Required | Description |
|-|-|-|
| `queue_name:` | Yes | Queue name |
| `messages:` | Yes | Array of messages (strings or objects) |
| `available_at@date:` | No | Future date for message availability |

Output: Array of unique queue message IDs.

#### queue.pop:

Pop messages from a queue.

```
start:
  queue.pop:
    output: results
    inputs:
      queue_name: example.queue
      limit: 5
```

| Input | Required | Description |
|-|-|-|
| `queue_name:` | Yes | Queue name |
| `limit:` | Yes | Maximum messages to retrieve |

**Output dictionary:**

| Key | Description |
|-|-|
| `consumer_id` | Unique consumer ID for acknowledging messages |
| `messages` | Dictionary of messages (key = message ID, value = `{queue, data}`) |

Both queue commands support: `on_simulate:`, `on_success:`, `on_error:`.

---

### Metric Commands

#### metric.increment:

Add samples to a metric.

```
start:
  metric.increment:
    output: results
    inputs:
      metric_name: example.login.fails
      dimensions:
        worker@int: {{worker_id}}
        ip: {{client_ip}}
      values: 1
      is_realtime@bool: yes
```

| Input | Required | Description |
|-|-|-|
| `metric_name:` | Yes | Metric name |
| `dimensions:` | No | Key/value dimension pairs |
| `values:` | No | Number or array of numbers (default 1) |
| `is_realtime@bool:` | No | Update instantly vs. queued (default false) |
| `timestamp@date:` | No | Retroactive timestamp (default now) |

Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### Email Commands

#### email.parse:

Parse a MIME-encoded email message into a ticket.

```
start:
  email.parse:
    output: results
    inputs:
      message@text:
        From: sender@example.com
        To: support@example.com
        Subject: Test message
        Date: {{'now'|date('r')}}
        Content-Type: text/plain; charset=utf-8

        This is the message body.
    on_success:
      return:
        ticket_id: {{results.id}}
```

| Input | Required | Description |
|-|-|-|
| `message@text:` | Yes | MIME-encoded email (headers + blank line + body) |

**Policy required:** `commands: email.parse: allow@bool: yes`

Output: Ticket dictionary. Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### Encryption Commands

#### encrypt.pgp:

Encrypt text for PGP public keys.

```
start:
  encrypt.pgp:
    output: encrypted
    inputs:
      message@text:
        Secret message content.
      public_keys:
        uri: cerb:gpg_public_key:FINGERPRINT
```

| Input | Required | Description |
|-|-|-|
| `message@text:` | Yes | Message to encrypt |
| `public_keys:`  | Yes | `uri:` or `ids:` specifying recipient keys |

#### decrypt.pgp:

Decrypt PGP-encrypted messages. Automatically matches against available private key records.

```
start:
  decrypt.pgp:
    output: decrypted
    inputs:
      message@text:
        -----BEGIN PGP MESSAGE-----
        ...
        -----END PGP MESSAGE-----
```

| Input | Required | Description |
|-|-|-|
| `message@text:` | Yes | PGP-encrypted message |

Both encryption commands support: `on_simulate:`, `on_success:`, `on_error:`.

---

### API Commands

#### api.command:

Execute internal API commands.

```
start:
  api.command:
    output: results
    inputs:
      name: cerb.commands.worklist.explorer.create
      params:
        interaction: cerb:automation:wgm.explore.worklist
```

| Input | Required | Description |
|-|-|-|
| `name:` | Yes | API command name |
| `params:` | No | Command-specific parameters |

**Available commands:**

| Command | Purpose |
|-|-|
| `cerb.commands.activity.log` | Create activity log entries and send watcher notifications |
| `cerb.commands.dataset.vector_similarity` | Find similar vectors in JSONL dataset |
| `cerb.commands.email.relay` | Relay message to external email |
| `cerb.commands.email.relay.sign` | Generate signed Message-Id for relay |
| `cerb.commands.email.spam.train` | Train ticket as spam |
| `cerb.commands.oauth2.token.validate` | Validate OAuth2 tokens |
| `cerb.commands.worklist.explorer.create`  | Create dynamic explore set |
| `cerb.commands.worklist.search` | Worklist configuration and search |

Handlers: `on_simulate:`, `on_success:`, `on_error:`.

---

### Logging Commands

#### log:

Write messages to the automation log at various severity levels.

```
start:
  log: This is a notice
  log.warn: This is a warning
  log.error: This is an error
  log.alert: This is an alert
```

Each entry includes: automation name, node, created date, level, and message. Log entries are accessed via data queries. No handlers.

---

### Simulation Commands

#### simulate.success:

Used inside `on_simulate:` handlers to provide mock output and trigger `on_success:`.

#### simulate.error:

Used inside `on_simulate:` handlers to provide mock output and trigger `on_error:`.

```
on_simulate:
  simulate.success:
    status_code@int: 200
    body: {"mock": "data"}
```

---

## Triggers

Triggers define which automations respond to specific events or requests.

### automation.function

Reusable shared functions called by other automations via the `function:` command.

**Inputs:** `inputs` dictionary (custom values from caller).

**Return:** Any key/value pairs.

```
inputs:
  text/text:
    type: freeform
    required@bool: yes

start:
  return:
    length@int: {{inputs.text|length}}
```

### automation.timer

Scheduled automations with continuations. Run at future times (once or recurring).

**Inputs:** `timer_*` (timer record), `inputs` dictionary.

**Await output:** `until` (Unix timestamp for next resumption).

```
start:
  # Do work
  await:
    until@date: +5 mins
```

**Return output:** `delete` (bool, true to delete timer when complete).

### interaction.worker

Conversational processes with workers that pause between steps to collect input.

**Inputs:** `caller_name`, `caller_params`, `client_browser_*`, `client_ip`, `client_url`, `inputs`, `worker_*`.

**Await states:**

| Type | Description |
|-|-|
| `await:form:` | Web form with elements: audio, chart, chooser, editor, fileDownload, fileUpload, llmTranscript, map, query, say, sheet, submit, text, textarea |
| `await:draft:` | Email editor popup. Output: `status`, `record` |
| `await:duration:` | Wait until date/time |
| `await:interaction:` | Delegate to another interaction |
| `await:record:` | Record editor popup. Output: `event`, `record` |

**Return keys:** `alert:`, `callout:`, `clipboard:`, `open_link:`, `open_url:`, `search:`, `snippet:`, `timer:`.

**Callers (20):** `global.menu`, `mail.compose`, `mail.read`, `mail.reply`, `record.card`, `record.profile`, `cerb.toolbar.cardWidget.interactions`, `cerb.toolbar.profileWidget.interactions`, `cerb.toolbar.workspaceWidget.interactions`, `cerb.toolbar.projectBoardColumn`, sheet callers, editor callers.

### interaction.website

Interactions with visitors on third-party websites.

**Inputs:** `interaction`, `interaction_params`, `inputs`, `client_browser_*`, `client_ip`, `portal`.

**Await:form: elements:** fileUpload, llmTranscript, say, sheet, submit, text, textarea.

**Return:** Any key/value pairs.

### webhook.respond

Triggered by webhook listeners receiving HTTP requests.

**Inputs:**

| Key | Description |
|-|-|
| `request_body` | Request body text |
| `request_client_ip` | Client IP |
| `request_headers` | Headers (lowercase keys, underscores for dashes) |
| `request_method` | HTTP method (uppercase) |
| `request_params` | Query string parameters |
| `request_path` | Request path |

**Return:**

| Key | Description |
|-|-|
| `body:` | Response body. `body@base64:` for binary. Stream from URIs. |
| `headers:` | Response headers |
| `status_code:` | HTTP status (200, 403, 404, 500, etc.) |

### data.query (trigger)

Generate custom data query results for `automation.invoke` queries.

**Inputs:** `inputs`, `query_format`.

**Return:** `data:` dictionary (format depends on `query_format`).

### scripting.function

Invoked via `cerb_automation()` from scripting anywhere in Cerb (automations, behaviors, snippets, events, toolbars).

**Inputs:** `inputs` dictionary.

**Return:** Any key/value pairs.

### llm.tool

Reusable tools triggered by `llm.agent:` command. Description and inputs enable AI agents to understand usage.

**Inputs:** `inputs` dictionary (values from AI agent).

**Return:** `content` (text result of the tool).

```
inputs:
  text/query:
    type: freeform
    description: The search query
    required@bool: yes

start:
  # Perform search...
  return:
    content@text:
      Search results here.
```

### ui.widget

Custom output for card, profile, or workspace widgets.

**Inputs:** `inputs`, `record_*`, `widget_*`, `worker_*`.

**Return:** `html` (HTML to render).

### ui.sheet.data

Dynamic data source for sheet widgets.

**Inputs:** `inputs`, `sheet_filter`, `sheet_limit`, `sheet_page`.

**Return:** `data` (array of dictionaries), `total` (total record count).

### ui.chart.data

Data source for Chart KATA widgets.

**Inputs:** `inputs`, `widget_*`, `worker_*`.

**Return:** `data` dictionary (array of series with same length).

```
return:
  data:
    ts@csv: 2023-10, 2023-11, 2023-12
    series0@csv: 104, 77, 84
    series1@csv: 218, 335, 183
```

### resource.get

Dynamic resource content triggered by resource records.

**Inputs:** `actor_*`, `inputs`, `resource_*`.

**Return:** `file:` object with `content:` and `expires_at:`.

### reminder.remind (trigger)

Triggered by reminder alarms. All enabled automations execute.

**Inputs:** `inputs`, `reminder_*`.

**Return:** none.

### map.clicked

Triggered by clicks on map widget regions/points.

**Inputs:** `feature_type` (region/point), `feature_properties`, `inputs`, `widget_*`, `worker_*`.

**Return:** `sheet` (sheet schema for clicked feature).

### projectBoard.cardAction

Triggered when a card enters a new board column. All enabled automations execute.

**Inputs:** `board_*`, `card_*`, `column_*`, `inputs`, `worker_*`.

**Return:** none.

### projectBoard.renderCard

Triggered when displaying a card on a project board.

**Inputs:** `board_*`, `card_*`, `inputs`, `worker_*`.

**Return:** `sheet` (sheet schema for the card).

### behavior.action

Execute automations from legacy bot behaviors.

**Inputs:** `inputs` dictionary.

**Return:** Any key/value pairs.

### interaction.worker.explore

Custom logic for next record in dynamic explore sets.

**Inputs:** `explore_hash`, `explore_page`, `inputs`, `worker_*`.

**Await:explore: output:** `title`, `url`, `label`, `toolbar` (interaction definitions).

---

## Events

Event handlers trigger automations using KATA dialect. Single-handler events execute the first matching non-disabled automation; multi-handler events execute all in order.

Events are configured via **Search >> Automation Events** or on parent records.

**Event handler KATA format:**
```
automation/<name>:
  uri: cerb:automation:<automation_name>
  disabled@bool: {{condition to disable}}
  inputs:
    key: value
```

### mail.draft

Modify draft properties before editor opens. Multiple automations can cumulatively modify the same draft.

**Placeholders:** `draft_*`, `is_resumed` (bool).

**Return:** `draft:params:` dictionary.

### mail.draft.validate

Validate email drafts before sending. Interactive validators allow worker bypass; non-interactive reject with errors.

**Placeholders:** `caller_name`, `caller_params`, `draft_*`, `inputs`, `worker_*`.

**Return:** `reject:` (string — if set, sending aborted).

### mail.filter

Modify or reject inbound messages before acceptance.

**Placeholders:** `email_sender_*`, `email_subject`, `email_headers`, `email_body`, `email_body_html`, `email_recipients`, `parent_ticket_*`.

**Return:** `reject:` (bool), `set:` (object with `custom_fields:`, `email_body:`, `email_body_html:`, `email_sender_org_id:`, `email_subject:`, `headers:`).

### mail.moved

React after ticket moves to new group/bucket.

**Placeholders:** `actor_*`, `was_group_*`, `was_bucket_*`, `ticket_*`.

**Return:** none.

### mail.received

React after new email arrives and is appended to ticket.

**Placeholders:** `is_new_ticket` (bool), `message_*`.

**Return:** none.

### mail.reply.validate

Validate before worker starts replying. Runs sequentially.

**Placeholders:** `caller_name`, `caller_params`, `inputs`, `message_*`, `worker_*`.

**Return:** `reject:` (string — if set, aborts reply).

### mail.route

Determine destination group/bucket for incoming messages.

**Placeholders:** `email_sender_*`, `email_subject`, `email_headers`, `email_body`, `email_body_html`, `email_recipients`, `parent_ticket_*`.

**Return:** `group_id:` or `group_name:`, optionally `bucket_id:` or `bucket_name:`.

### mail.send

Modify sent message drafts before delivery.

**Placeholders:** `draft_*`.

**Return:** `content:` (append/prepend/replace modifications), `draft:params:`.

Content modifications: `append:`, `prepend:`, `replace:` — each with `on:` (html, text, saved, sent booleans), `text:`, and (for replace) `with:`.

### mail.sent

React after outgoing message is sent.

**Placeholders:** `message_*`.

**Return:** none.

### record.changed

React when fields change on a record.

**Placeholders:** `actor_*`, `change_type` (created/updated/deleted), `inputs`, `is_new` (bool), `record_*`, `was_record_*`.

**Return:** none.

### record.merge

Allow or reject record merge requests.

**Placeholders:** `record_type_*`, `records`, `source_ids`, `target_id`, `worker_*`.

**Return:** `deny:` (string — if set, merge rejected with this message).

### record.merged

React after records are consolidated (before source deletion).

**Placeholders:** `record_type_*`, `records`, `source_ids`, `target_id`, `worker_*`.

**Return:** none.

### record.viewed

React after worker views a record profile.

**Placeholders:** `record_*`, `worker_*`.

**Return:** none.

### reminder.remind (event)

Triggered when reminder reaches its alarm date.

**Placeholders:** `reminder_*`.

**Return:** none.

### worker.authenticate.failed

After failed worker login. All enabled automations execute.

**Placeholders:** `inputs`, `client_browser_*`, `client_ip`, `worker_*`.

**Return:** none.

### worker.authenticated

After successful worker login. All enabled automations execute.

**Placeholders:** `inputs`, `client_browser_*`, `client_ip`, `worker_*`.

**Return:** `deny:` (string), `motd:message:` (Markdown), `motd:button:` (label, default "Continue").

---

## Policies

Policies govern automation permissions with rules for allowing/denying actions.

### Callers Scope

Rules determining who can use an interaction and where. Currently only `interaction.worker` supports callers.

```
callers:
  cerb.toolbar.projectBoardColumn:
    allow/owners@bool:
      {{cerb_record_writeable('project_board', board_id, worker__context, worker_id) ? 'yes'}}
    deny: yes
```

Denied caller policies automatically hide interactions from toolbars.

### Commands Scope

Rules determining which commands are allowed or denied. For `interaction.worker` automations, the policy typically only needs `commands:` to allowlist the specific commands used. Only add `callers:` when you need to restrict which toolbars can invoke the interaction.

**Important:** Each command entry can ONLY contain `allow` or `deny` child keys (with optional `/name` identifiers). Generally use `allow@bool:` or `deny@bool:` with scripting expressions. All `inputs:` of the automation command being evaluated are available as policy placeholders.

**Permissive:**
```
commands:
  all:
    allow: yes
```

**Restrictive (principle of least privilege):**
```
commands:
  http.request:
    deny/url@bool: {{inputs.url is not prefixed ('https://api.example/')}}
    deny/method@bool: {{inputs.method != 'GET'}}
    allow@bool: yes
  record.create:
    allow/tasks@bool:
      {{inputs.record_type|context_alias == 'task' ? 'yes'}}
  record.get:
    allow: yes
  all:
    deny: yes
```

**Exception-based:**
```
commands:
  http.request:
    deny/url@bool: {{inputs.url is not prefixed ('https://')}}
    allow: yes
```

**Policy placeholders:**

| Key | Example |
|-|-|
| `node.id` | `start:record.create:` |
| `node.type` | `record.create` |
| `inputs.*`  | `inputs.record_type`, `inputs.url` |
| `output` | placeholder name |

**Rule processing:**
1. Each command entry can ONLY have `allow` and `deny` child keys (with optional `/name` identifiers)
2. A rule evaluating to `no` is skipped (failed allow ≠ deny)
3. Rules tested sequentially until explicit `allow: yes` or `deny: yes`
4. If no rules match, default is `deny: yes`
5. `all:` matches any unmatched command

### Time Limits

Default: 25,000ms (25 seconds). Configure via:

```
settings:
  time_limit_ms: 30000
```

Best practice: break long tasks into smaller pieces using timers and queues.
