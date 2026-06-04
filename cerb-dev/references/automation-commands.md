# Automation commands & `api.command:` sub-commands

Two distinct extension mechanisms:

- **Part 1** — a new **top-level automation command/action** (a first-class node like `llm.chat:`, `record.update:`, `records.update:`). Hardcoded in the framework; **8 spots** (+1 optional). Only the first 3 affect execution; the other 5 are all editor UX (autocomplete + KATA validation) that fail silently if missed.
- **Part 2** — a new **`api.command:` sub-command** (e.g. `cerb.commands.worklist.query.debug`) invoked through the generic `api.command:` action. Plugin-extensible; only 2 spots, no framework edits.

Reference commits: `721dcba441` (added the `llm.chat:` command) and `b22e895e85` (added the `cerb.commands.worklist.query.debug` api.command sub-command).

---

## Part 1 — New top-level automation command (action)

A command is a class under `Cerb\AutomationBuilder\Action`. **Spots 1–3 make it run; spots 4–8 make the automation editor understand it** (autocomplete + KATA schema validation). Missing any of 4–8 won't break execution — the command still works if hand-typed — but the editor will flag the KATA as invalid or fail to suggest it. The KATA-schema spots (6 & 7) are the most damaging to miss: a command absent from the schema makes the editor mark otherwise-valid automations (and policies) as errors.

### 1. Action class
`libs/devblocks/api/services/automation/Action/<Name>Action.php`, namespace `Cerb\AutomationBuilder\Action`, extends `AbstractAction`, with `const ID = '<command.name>'`.

Autoloads automatically via the directory→namespace mapping in `libs/devblocks/plugin.xml`
(`<dir path="api/services/automation/" namespace="Cerb\AutomationBuilder\" />`) — **no `plugin.xml` edit and no class-loader entry needed.**

`activate()` signature and conventional body (see `LlmChatAction.php`, `RecordUpdateAction.php`):
```php
function activate(Model_Automation $automation, DevblocksDictionaryDelegate $dict, array &$node_memory, ?string &$error=null) : string|false {
    $validation = DevblocksPlatform::services()->validation();
    $params  = $automation->getParams($this->node, $dict);
    $policy  = $automation->getPolicy();
    $inputs  = $params['inputs'] ?? [];
    $output  = $params['output'] ?? null;

    try {
        // 1) validate params (`inputs` array, `output` string)
        // 2) $validation->reset(); validate the individual `inputs:` fields
        // 3) policy gate — REQUIRED on every mutating/external command:
        $action_dict = DevblocksDictionaryDelegate::instance([
            'node' => ['id' => $this->node->getId(), 'type' => self::ID],
            'inputs' => $inputs, 'output' => $output,
        ]);
        if(!$policy->isCommandAllowed(self::ID, $action_dict)) {
            $error = sprintf("The automation policy does not allow this command (%s).", self::ID);
            throw new Exception_DevblocksAutomationError($error);
        }
        // 4) do the work; if($output) $dict->set($output, ...);
    } catch (Exception_DevblocksAutomationError $e) {
        $error = sprintf("[%s] %s", $this->node->getId(), $e->getMessage());
        if(null != ($event_error = $this->node->getChildBySuffix(':on_error'))) {
            if($output) $dict->set($output, ['error' => $error]);
            return $event_error->getId();
        }
        return false;
    }
    // success / continue
    if(null != ($event_success = $this->node->getChild($this->node->getId() . ':on_success')))
        return $event_success->getId();
    return $this->node->getParent()->getId();
}
```
Return value is the **next node id** (string) or `false` to halt. Honor the `:on_error` / `:on_success` child events. Commands that toggle the event listener (`disable_events`) must restore it in a `finally` block (see `RecordUpdateAction`).

### 2. Dispatch registry — `ActionNode::getActionClasses()`
`libs/devblocks/api/services/automation/Node/ActionNode.php`, add the alphabetized entry:
```php
'llm.chat' => '\Cerb\AutomationBuilder\Action\LlmChatAction',
```

### 3. Grammar list — `_getNodeGrammar()`
`libs/devblocks/api/services/automation.php`, add the name to the `$actions` array (alphabetized):
```php
'llm.chat',
```

### 4 & 5. Editor autocomplete — `cerberus.js` (easy to miss; editor-only)
`features/cerberusweb.core/resources/js/cerberus.js`, in `cerbAutocompleteSuggestions`:

- **Command list** — add `'<command>:'` to the top-level action suggestions array:
  ```js
  'llm.chat:',
  ```
- **Policy autocomplete** — add a `commands:<command>:` key so policy blocks autocomplete allow/deny:
  ```js
  'commands:llm.chat:': [
      'deny@bool: yes',
      'allow@bool: yes'
  ],
  ```
Both are alphabetized alongside the siblings. (`cerberus.js` is the static client-side fallback list; the richer server-side autocomplete is spot 8.)

### 6. KATA schema for the command — `_CerbApplication_KataSchemas::automation()`
`api/Application.class.php`. The automation editor validates the script against this schema; **a command missing here makes the editor mark valid automations that use it as errors.** Add a block for the command under the `commands:` attributes, declaring its `inputs:` attributes, `output:`, and the three event refs. Mirror the sibling `record.update:` entry:
```yaml
              records.update:
                multiple@bool: yes
                types:
                  object:
                    attributes:
                      inputs:
                        types:
                          object:
                            attributes:
                              disable_events:
                                types:
                                  bool:
                              fields:
                                types:
                                  list:
                              record_ids:
                                types:
                                  list:
                              record_type:
                                types:
                                  string:
                      output:
                        types:
                          string:
                      on_error:
                        ref: commands
                      on_success:
                        ref: commands
                      on_simulate:
                        ref: commands
```

### 7. KATA schema for the policy — `_CerbApplication_KataSchemas::automationPolicy()`
`api/Application.class.php`. Add one line under the `commands:` attributes so `commands:<name>:` validates in **automation policy** KATA (the `&policyRule` anchor supplies allow/deny):
```yaml
                records.update@ref: policyRule
```
Omitting this makes the editor reject any policy that grants/denies your command.

### 8. Server-side autocomplete — `Extension_AutomationTrigger::getAutocompleteSuggestionsArray()`
`api/Extension.class.php`. This is the rich, server-driven editor autocomplete shared by all triggers. Two parts:

- **Top-level command snippet** — add a caption/snippet/description entry to the actions list (alongside `record.update:`, `llm.chat:`). The optional `'interaction'` key launches a build-assistant interaction (spot 9):
  ```php
  [
      'caption' => 'records.update:',
      'snippet' => "records.update:\n\tinputs:\n\t\t\${1:}\n\toutput: results\n\t#on_simulate:\n\t#on_success:\n\t#on_error:\n",
      'description' => "Update many records of one type in a batch",
      'interaction' => 'ai.cerb.automationBuilder.action.recordsUpdate', // optional; see spot 9
  ],
  ```
- **Child-key autocomplete map** — add key-path entries so the editor completes the command's `inputs:` (and nested values). Keys are regex-anchored with a `(.*):` prefix; reuse the special `'type' => 'record-type'` / `'record-fields'` / `'record-fields-value'` resolvers where applicable. Mirror the `record.update` block:
  ```php
  '(.*):records.update:' => $action_base,
  '(.*):records.update:inputs:' => [
      ['caption' => 'record_type:', 'snippet' => 'record_type:', 'score' => 2000, 'description' => "The record type to update"],
      ['caption' => 'record_ids:',  'snippet' => "record_ids:\n\t\${1:}", 'score' => 1999, 'description' => "The record IDs to update"],
      ['caption' => 'fields:',      'snippet' => "fields:\n\t\${1:}", 'score' => 1998, 'description' => "The record fields to update"],
      ['caption' => 'disable_events:', 'snippet' => "disable_events@bool: \${1:yes}", 'score' => 900, 'description' => "Don't trigger automations or behaviors"],
  ],
  '(.*):records.update:inputs:fields:' => ['type' => 'record-fields'],
  '(.*):records.update:inputs:fields:(.*?):' => ['type' => 'record-fields-value'],
  '(.*):records.update:inputs:record_type:' => ['type' => 'record-type'],
  ```
There are plenty of sibling examples in this method to copy (`record.update`, `record.search`, `llm.chat`).

### 9. (Optional) build-assistant interaction — asset automation JSON
`features/cerberusweb.core/assets/automations/`. When a worker autocompletes the command (via the `'interaction'` key in spot 8), Cerb can launch a guided interaction (a prompt form) that builds the command snippet for them. To add one:

1. Copy an existing example — `ai.cerb.automationBuilder.action.recordUpdate.json` is the closest template. It prompts for a record type and fields via sheets, then `return:`s a templated `record.update/...:` snippet inserted into the script.
2. Name the file `ai.cerb.automationBuilder.action.<yourCommand>.json` and set its `"name"` to match; reference that name from spot 8's `'interaction'` key (without the `.json`).
3. Register it for import in a migration patch's **"Update built-in automations"** list (see `features/cerberusweb.core/patches/11.x/11.0.0.php` lines ~160–183) — add the filename to the `$automation_files` array, which loops `DAO_Automation::importFromJson(...)`. Fresh installs pick it up via the baseline import; existing installs get it when the patch runs.

This step is purely a convenience UX; the command is fully usable without it.

> Note: command-specific *backing logic* (e.g. `llm.chat:` added LLM provider plumbing elsewhere in `api/Application.class.php` and `api/Extension.class.php`) is separate from this checklist — that belongs to whatever the command does.

---

## Part 2 — New `api.command:` sub-command

`api.command:` is a single generic action that dispatches to a registered command by URI
(`cerb.commands.*`). Adding one is plugin-extensible — **only two spots, no framework edits, no `cerberus.js` edit, no grammar edit.** (See the `api.command:` wrapper convention: `cerb.commands.*` URIs go inside `api.command:` with `inputs.name:` + `inputs.params:`.)

### 1. Command class
`features/<plugin>/api/automations/api_commands/<id>.php`, extends `Extension_AutomationApiCommand`, `const ID = 'cerb.commands.<dotted.name>'`:
```php
class ApiCommand_CerbWorklistQueryDebug extends Extension_AutomationApiCommand {
    const ID = 'cerb.commands.worklist.query.debug';

    function run(array $params=[], &$error=null) : array|false {
        $record_type = $params['record_type'] ?? null;
        if(!$record_type) { $error = '`params:record_type:` is required'; return false; }
        // ... do work ...
        return $results;   // associative array surfaced to the automation, or false + $error
    }

    // Editor autocomplete for `params:` keys — keyed by the key_path under the command
    public function getAutocompleteSuggestions($key_path, $prefix, $key_fullpath, $script) : array {
        return match ($key_path) {
            '' => ['record_type:', 'query:'],
            default => [],
        };
    }
}
```
`run()` receives the resolved `params:` map and returns an associative array (surfaced back to the automation) or `false` with `$error` set. Autocomplete is provided by the command's own `getAutocompleteSuggestions()` — there is **no** central JS list to edit for sub-commands.

### 2. `plugin.xml` extension (point `cerb.automation.api_command`)
```xml
<extension point="cerb.automation.api_command">
    <id>cerb.commands.worklist.query.debug</id>
    <name>cerb.commands.worklist.query.debug</name>
    <class>
        <file>api/automations/api_commands/cerb.worklist.query.debug.php</file>
        <name>ApiCommand_CerbWorklistQueryDebug</name>
    </class>
    <params />
</extension>
```
Run `/update` after editing `plugin.xml`.

### Choosing between Part 1 and Part 2
- Use an **api.command sub-command** when the capability is plugin-specific, niche, or you want it shippable without patching the framework grammar — most new capabilities should go here.
- Use a **top-level command** only for broadly-applicable primitives that deserve first-class syntax and their own `:on_success`/`:on_error` flow control.
