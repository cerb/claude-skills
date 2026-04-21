# Field Validation

## Basic Pattern

```php
$validation = DevblocksPlatform::services()->validation();

$validation
    ->addField('field_name', 'Human Label')
    ->string()
    ->setRequired(true)
;

if(false === $validation->validateAll($edit_params, $error))
    return false;
```

`validateAll()` returns `false` and populates `$error` on the first failure. Use `===` to check the return value — it returns `true` on success, `false` on failure.

**Every key present in `$edit_params` must have a rule.** Unknown fields cause a validation error. Add rules for all fields the form can submit — including hidden inputs, checkboxes, and radio buttons — even if they're optional.

## Field Types

| Method | Use for |
|--------|---------|
| `->string()` | Text fields; chainable with string modifiers below |
| `->url()` | URL fields; built-in format check |
| `->id()` | Record ID (positive integer) |
| `->idArray()` | Array of record IDs |
| `->bit()` | Boolean 0/1 |
| `->boolean()` | Boolean true/false |
| `->number()` | Arbitrary number |
| `->uint($bytes=4)` | Unsigned integer |
| `->float()` | Float; chainable with `->setMin()` / `->setMax()` |
| `->timestamp()` | Unix timestamp integer |
| `->context()` | Context string (e.g. `cerb.contexts.ticket`) |
| `->array()` | Arbitrary array |
| `->stringOrArray()` | Accepts either |

## String Modifiers

Chain these after `->string()`:

**`->string()` defaults to 255-char max with truncation enabled.** Any value longer than 255 chars is silently truncated to 252 + `'...'` before validators or your code see it. Always call `->setMaxLength()` explicitly for fields that accept long content.

```php
->string()
->setRequired(true)
->setNotEmpty(true)          // must not be empty string (separate from required)
->setMaxLength(16_777_215)   // MEDIUMTEXT; use a real byte count, not named aliases
->setMinLength(8)
->setPossibleValues(['a','b','c'])
->setUnique(DAO_Example::class) // reject duplicates in that table
```

## Adding Validators

`addValidator()` accepts any callable returned by `$validation->validators()->...()`. Validators run after the type check passes.

```php
// Optional email (allow blank)
->string()
->addValidator($validation->validators()->email(allow_empty: true))

// Required email
->string()
->setRequired(true)
->addValidator($validation->validators()->email())

// Valid context string
->string()
->addValidator($validation->validators()->context())

// Record must exist
->id()
->addValidator($validation->validators()->contextId(CerberusContexts::CONTEXT_WORKER))

// URI slug (alphanumeric + underscores/dashes, unique)
->string()
->addValidator($validation->validators()->uri())
```

### Available Validators

| Validator | Description |
|-----------|-------------|
| `->email($allow_empty)` | Valid email address |
| `->emails($allow_empty)` | Newline-delimited list of email addresses |
| `->url()` | Valid URL |
| `->uri()` | Valid URI slug |
| `->context($allow_empty)` | Valid context string |
| `->contextId($context, $allow_empty)` | Record ID that exists for that context |
| `->contextIds($context, $allow_empty)` | Array of record IDs for that context |
| `->colorHex()` | Hex color string (`#rrggbb`) |
| `->colorsHex()` | Newline-delimited list of hex colors |
| `->date()` | Parseable date string |
| `->timezone()` | Valid PHP timezone name |
| `->language()` | Valid language code |
| `->extension($class)` | Valid extension ID for that class |
| `->yaml()` | Valid YAML string |

## Adding Formatters

`addFormatter()` mutates the value before validation. Chain after the type:

```php
->string()
->addFormatter($validation->formatters()->stringUpper())   // uppercase
->addFormatter($validation->formatters()->stringWithoutEmoji())
->addFormatter($validation->formatters()->context())       // normalize context string
```

## Surfacing Errors in JSON Responses

```php
try {
    if(false === $validation->validateAll($edit_params, $error))
        throw new Exception_DevblocksAjaxValidationError($error);

    // ... save logic ...

} catch(Exception_DevblocksAjaxValidationError $e) {
    echo json_encode(['status' => false, 'error' => $e->getMessage()]);
    return;
}
```

For field-level error highlighting, pass the field name as the second argument:
```php
throw new Exception_DevblocksAjaxValidationError('Bad value', 'field_name');
```
