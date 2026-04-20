# Security Conventions

## HTTP Superglobals — Never Use $_REQUEST

Always use `$_POST` or `$_GET` explicitly. **Never use `$_REQUEST`.**

`$_REQUEST` merges GET, POST, and cookie data, so a crafted query string can silently override expected POST values. This bypasses CSRF protection and can subvert form handling logic.

**Pattern for state-changing (POST) endpoints:**

```php
// 1. Enforce POST method
if('POST' != DevblocksPlatform::getHttpMethod())
    DevblocksPlatform::dieWithHttpError('', 405);

// 2. Read inputs exclusively from $_POST via importGPC
$name = DevblocksPlatform::importGPC($_POST['name'] ?? null, 'string', '');
$id   = DevblocksPlatform::importGPC($_POST['id']   ?? null, 'integer', 0);
```

**Pattern for read-only (GET) endpoints:**

```php
$id = DevblocksPlatform::importGPC($_GET['id'] ?? null, 'integer', 0);
```

Always pass input through `DevblocksPlatform::importGPC()` — it coerces type and sanitizes the value.

## CSRF Protection

Cerb generates a per-session CSRF token stored in `$_SESSION['csrf_token']`. State-changing forms must include a hidden `csrf_token` field. The framework validates it automatically on form submissions when the correct HTTP method is enforced.

Never use `--no-verify` workarounds or skip the method check. If a form action needs a `GET` link, it should only read state, never write it.

On the JavaScript side, popup dialogs that trigger data-modifying actions must also use POST. Pass a `FormData` object to `genericAjaxPopup()` instead of a URL string — a plain URL string always produces a GET. See `ui-conventions.md` for the pattern.

## Input Sanitization

Use `DevblocksPlatform::importGPC()` for all user input:

```php
// Types: 'string', 'integer', 'float', 'bit', 'array'
$value = DevblocksPlatform::importGPC($_POST['field'] ?? null, 'string', '');
```

For database queries, always use parameterized values via `self::qstr()` or framework query helpers — never interpolate raw user input into SQL strings.
