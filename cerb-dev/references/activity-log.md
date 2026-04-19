# Activity Log Reference

## Overview

The activity log (`cerberusweb.contexts.activity_log`) maintains an auditable history of events affecting records. Two helpers on `CerberusContexts` cover the most common cases.

## Logging Record Creation

```php
// Call after DAO::create() and onUpdateByActor(), before marquee/view update
CerberusContexts::logActivityRecordCreate(CerberusContexts::CONTEXT_FOO, [$id]);
```

Emits the `record.created` activity point against the new record. If no label is provided, it is lazy-loaded via the context dictionary.

## Logging Record Deletion

```php
// Call before DAO::delete() so the model is still fetchable if needed
CerberusContexts::logActivityRecordDelete(CerberusContexts::CONTEXT_FOO, $model->id, $model->name);
```

Emits the `record.deleted` activity point. Skips `Context_Draft::ID` automatically. The third argument (label) is optional — omit it to have the method load it from the model.

## Signatures

```php
CerberusContexts::logActivityRecordCreate(
    string|Extension_DevblocksContext $context,
    int|array $record_ids,
    string|array|null $record_labels = null
): void

CerberusContexts::logActivityRecordDelete(
    string|Extension_DevblocksContext $context,
    int|array $record_ids,
    string|array|null $record_labels = null
): void
```

Both methods accept a context string, a single ID or array of IDs, and an optional label or array of labels. Defined in `api/Application.class.php`.

## Where to Place Calls in savePeekJson

```php
if(empty($id)) { // Create
    $id = DAO_Foo::create($fields);
    DAO_Foo::onUpdateByActor($active_worker, $fields, $id);
    CerberusContexts::logActivityRecordCreate(CerberusContexts::CONTEXT_FOO, [$id]);
    // ... marquee update

} else if(!empty($do_delete)) { // Delete
    CerberusContexts::logActivityRecordDelete(CerberusContexts::CONTEXT_FOO, $model->id, $model->name);
    DAO_Foo::delete($id);
}
```

## Coverage Notes

- `logActivityRecordCreate` is used for: `worker`, `mailbox` (added 11.2)
- `logActivityRecordDelete` is used broadly across most record types
- When adding a new record type, add both calls to `_profileAction_savePeekJson()`
