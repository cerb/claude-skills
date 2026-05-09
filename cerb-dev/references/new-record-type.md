# Creating a New Record Type

A new Cerb record type requires changes across several files. Use the generator tool (see below) to produce all the boilerplate, then customize it.

## Files to Create or Modify

| File | Action | Purpose |
|---|---|---|
| `features/cerberusweb.core/patches/11.x/11.2.0.php` | Modify | Add `CREATE TABLE` migration |
| `features/{plugin}/api/dao/{table}.php` | Create | DAO, Model, SearchFields, View, Context classes |
| `features/{plugin}/templates/records/types/{table}/peek_edit.tpl` | Create | Edit/create popup |
| `features/{plugin}/templates/records/types/{table}/view.tpl` | Create | Worklist view |
| `features/{plugin}/plugin.xml` | Modify | Register class loader + two extension blocks |
| `features/{plugin}/strings.xml` | Modify | i18n keys for field labels |

## Step 1: Generate the Boilerplate

Run the generator with `--output-dir` pointing to the plugin root. It writes PHP and template files directly and prints only a short manifest plus the XML snippets that still need manual insertion:

```bash
python3 .claude/skills/cerb-dev/tools/gen-dao.py \
    --plugin-id cerberusweb.core \
    --table my_record \
    --fields "id bigint unsigned NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL DEFAULT '', created_at int unsigned NOT NULL DEFAULT 0, updated_at int unsigned NOT NULL DEFAULT 0" \
    --output-dir features/cerberusweb.core
```

Output:
```
Cerb Record Type Generator
  Plugin:     cerberusweb.core
  Table:      my_record  |  Class: MyRecord
  Context ID: cerb.contexts.my.record

Writing files to: features/cerberusweb.core
  Created: api/dao/my_record.php          ← DAO + SearchFields + Model + View + Context
  Created: templates/records/types/my_record/peek_edit.tpl
  Created: templates/records/types/my_record/view.tpl

Manual edits still required in plugin.xml and strings.xml:
  [XML snippets printed here for copy-paste]
```

Omit `--output-dir` for a full dry-run that prints all content to stdout.

Files written by the generator:
- `api/dao/{table}.php` — all five PHP classes concatenated
- `templates/records/types/{table}/peek_edit.tpl`
- `templates/records/types/{table}/view.tpl`

Snippets printed (require manual insertion):
- `plugin.xml` class loader `<file>` block
- `plugin.xml` `<devblocks.context>` extension
- `plugin.xml` `<cerberusweb.ui.page.section>` extension
- `strings.xml` i18n entries

## Step 2: Add a Database Migration

Add a new patch function at the bottom of the active patch file. The function name must be unique (use a timestamp):

```php
// features/cerberusweb.core/patches/11.x/11.2.0.php

function patch_11_2_0_YYYY_MM_DD_HHMMSS() {
    $db = DevblocksPlatform::services()->database();
    $logger = DevblocksPlatform::services()->log();
    $tables = $db->metaTables();

    if(!isset($tables['my_record'])) {
        $sql = "
            CREATE TABLE `my_record` (
            `id` bigint unsigned NOT NULL AUTO_INCREMENT,
            `name` varchar(255) NOT NULL DEFAULT '',
            `created_at` int unsigned NOT NULL DEFAULT 0,
            `updated_at` int unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY (id),
            INDEX (updated_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ";
        $db->ExecuteMaster($sql) or die("[MySQL Error] " . $db->ErrorMsgMaster());
        $logger->info("[Patch] Created 'my_record' table.");
        $tables['my_record'] = 'my_record';
    }
}
```

Then register it in the patch file's dispatch array at the top.

## Step 3: Add plugin.xml Entries

**IMPORTANT: Never abbreviate the `options` or `acl` param blocks.** Copy the full list from the generator output. Omitting `workspace` silently breaks the Search nav popup for that record type. Only remove options that genuinely don't apply (e.g. `create` for programmatic-only records), and document why.

### In `<class_loader>`:

```xml
<file path="api/dao/my_record.php">
    <class name="Context_MyRecord" />
    <class name="DAO_MyRecord" />
    <class name="Model_MyRecord" />
    <class name="SearchFields_MyRecord" />
    <class name="View_MyRecord" />
</file>
```

### In `<extensions>`:

```xml
<extension point="devblocks.context">
    <id>cerb.contexts.my.record</id>
    <name>My Record</name>
    <class>
        <file>api/dao/my_record.php</file>
        <name>Context_MyRecord</name>
    </class>
    <params>
        <param key="names">
            <value>
                <data key="my_record" value="singular" />
                <data key="my_records" value="plural" />
            </value>
        </param>
        <param key="alias" value="my_record" />
        <param key="dao_class" value="DAO_MyRecord" />
        <param key="view_class" value="View_MyRecord" />
        <param key="options">
            <value>
                <data key="cards" />
                <data key="comments" />
                <data key="custom_fields" />
                <data key="links" />
                <data key="records" />
                <data key="search" />
                <data key="snippets" />
                <data key="va_variable" />
                <data key="watchers" />
                <data key="workspace" />
            </value>
        </param>
        <param key="acl">
            <value>
                <data key="broadcast" />
                <data key="comment" />
                <data key="create" />
                <data key="delete" />
                <data key="export" />
                <data key="import" />
                <data key="merge" />
                <data key="update" />
                <data key="update.bulk" />
            </value>
        </param>
    </params>
</extension>

<extension point="cerberusweb.ui.page.section">
    <id>cerb.page.profiles.my_record</id>
    <name>My Record Section</name>
    <class>
        <file>api/profiles/my_record.php</file>
        <name>PageSection_ProfilesMyRecord</name>
    </class>
    <params>
        <param key="page_id" value="core.page.profiles" />
        <param key="uri" value="my_record" />
    </params>
</extension>
```

## Step 4: Add strings.xml Entries

```xml
<!-- MyRecord -->

<tu tuid='dao.my_record.id'>
    <tuv xml:lang="en_US">
        <seg>Id</seg>
    </tuv>
</tu>
<tu tuid='dao.my_record.name'>
    <tuv xml:lang="en_US">
        <seg>Name</seg>
    </tuv>
</tu>
<tu tuid='dao.my_record.updated_at'>
    <tuv xml:lang="en_US">
        <seg>Updated At</seg>
    </tuv>
</tu>
```

## Step 5: Customize the Generated Code

After placing the generated code, review these `// [TODO]` areas:

### In `DAO_*::getFields()`:
Add validation rules for all non-standard fields:
```php
$validation
    ->addField(self::STATUS)
    ->string()
    ->setPossibleValues(['open', 'closed'])
    ;
```

### In `SearchFields_*`:
The `getWhereSQL()` switch may need custom cases for non-standard filter types.

### In `View_*::getQuickSearchFields()`:
Add entries for any extra fields beyond `id`, `name`, `updated`, `fieldset`, `watchers`.

### In `Context_*::getContext()`:
Add token labels, types, and values for any extra fields:
```php
$token_labels['status'] = $prefix . 'Status';
$token_types['status'] = Model_CustomField::TYPE_SINGLE_LINE;
// ...
$token_values['status'] = $my_record->status;
```

### In `Context_*::getKeyToDaoFieldMap()`:
Map automation key names to DAO constants for all fields:
```php
'status' => DAO_MyRecord::STATUS,
```

## Class Name Derivation

The naming follows a simple rule: `snake_case` → `PascalCase`

| Table | Class prefix | Context ID | Field prefix |
|---|---|---|---|
| `my_record` | `MyRecord` | `cerb.contexts.my.record` | `m` |
| `knowledge_source` | `KnowledgeSource` | `cerb.contexts.knowledge.source` | `k` |
| `queue` | `Queue` | `cerb.contexts.queue` | `q` |

The **field prefix** (first letter of table name) is used in SearchFields constants and view templates:
- `SearchFields_MyRecord::M_NAME` maps to `my_record.name`
- In view.tpl: `$result.m_name`, `$result.m_id`, `$result.m_updated_at`
