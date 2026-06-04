# Login Flow

`features/cerberusweb.core/api/uri/login.php` (`Page_Login`) drives the entire signed-out experience: router → authenticate → MFA → MOTD → consent → recover, plus the OAuth invite flow. The state machine lives in `CerbLoginWorkerAuthState` (`api/Application.class.php`), serialized into `$_SESSION['login.state']` with a 20-minute self-expiration on `getInstance()`.

## Route Dispatch

`Page_Login::render()` reads `$response->path` and dispatches to one of:

| Path | Method | Renders |
|---|---|---|
| `/login` | `_routeLogin()` | `login/login_router.tpl` |
| `/login/authenticate` (POST) | `_routeAuthenticate()` | redirect on success/failure |
| `/login/authenticated` | `_routeAuthenticated()` | redirects through MFA/MOTD/consent chain |
| `/login/mfa` | `_routeMultiFactorAuth()` | `login/auth/mfa/totp.tpl` or `totp_setup.tpl` |
| `/login/motd` | `_routeMotd()` | `login/auth/motd/motd.tpl` |
| `/login/consent` | `_routeConsent()` | `login/auth/consent/oauth_consent.tpl` |
| `/login/recover/...` | `_routeRecover()` | `login/recover/*.tpl` |

All sub-templates render *inside* `border.tpl`, which wraps with `header.tpl`. They share one shell of classes (`.cerb-login-bg`, `.cerb-login-card`, `.cerb-login-field`, `.cerb-login-submit`, etc.) defined in `install/extras/developers/css/cerb.css/layout/cerb-login.scss`.

## `clearAllAssign()` Wipes Globals

`render()` calls `$tpl->clearAllAssign()` before dispatching. That nukes every template variable normally provided by `controllers/default.php` — including `$settings`, `$session`, and `$visit`. Any template under `login/` that references `$settings->get(...)` will fatal with *"Call to a member function get() on null"*.

**Pattern:** resolve the value in PHP and assign it explicitly:

```php
// Page_Login::render(), after $tpl->clearAllAssign() and csrf_token assign
$settings = DevblocksPlatform::services()->pluginSettings();
$tpl->assign('helpdesk_title', $settings->get('cerberusweb.core', 'helpdesk_title', 'Cerb'));
```

Then in templates: `{$helpdesk_title}` not `{$settings->get(...)}`.

## Forcing Dark Mode for the Login Flow

`header.tpl:2` emits `<html class="dark">` based on `$pref_dark_mode`. The standard path in `features/cerberusweb.core/api/controllers/default.php:171–180` reads that flag from the active worker's prefs. For signed-out pages there's no worker — add an `elseif` next to it keyed off the URL:

```php
if(!empty($visit) && !is_null($active_worker)) {
    // ... existing worker pref read ...
    $tpl->assign('pref_dark_mode', $dark_mode);
} elseif(($response->path[0] ?? null) === 'login') {
    $tpl->assign('pref_dark_mode', true);
}
```

Doing it in `default.php` (not `Page_Login::render()`) keeps the chrome decision with the chrome controller, and runs before `header.tpl` emits the `<html>` tag.

## Border Logo: Hide for Pages with Their Own

`border.tpl` renders a centered `#cerb-logo` for unauthenticated visitors. If your page renders its own logo inside a card (as the login pages do), suppress the border one by checking the path — `$response_path` is assigned globally in `default.php:191`:

```smarty
{elseif $response_path[0] != 'login'}
<div style="text-align:center;">
    <a href="{devblocks_url}{/devblocks_url}"><div id="cerb-logo" style="background-position:center;"></div></a>
</div>
{/if}
```

## Stale CSRF Must Fail Closed

When a login form sits open longer than the session lifetime, the submitted `_csrf_token` no longer matches `$_SESSION['csrf_token']`. Engine.php special-cases this at `libs/devblocks/api/Engine.php:715–727`. Originally it called `respondWithErrorReason(SessionExpired)` and rendered a dead-end error page — **but residual `$_SESSION['login.state']` could still authenticate the user on the next request**. The correct handling is fail-closed:

```php
// libs/devblocks/api/Engine.php — CSRF mismatch branch for /login/authenticate
unset($_SESSION['login.state']);
$_SESSION = [];
session_regenerate_id(true);
DevblocksPlatform::redirect(new DevblocksHttpRequest(['login'], ['error' => 'session.expired']));
```

Order matters: clear `login.state`, wipe `$_SESSION`, regenerate the session ID (which invalidates the old cookie server-side), then bounce back to `/login` with an inline error. `session.php:66–68` re-creates the `csrf_token` on the next request, the email pre-fills from the 30-day `cerb_login_email` cookie set by `CerbLoginWorkerAuthState::setEmail()`, and the user gets a friendly "Your session timed out" instead of a wall.

## Error Messages

`Page_Login::getErrorMessage($code)` (~line 31) maps short error codes to user-facing strings. Redirects pass `?error=<code>` and the templates render `{Page_Login::getErrorMessage($error)}` inside `.error-box`. To add a new code:

```php
// In the $error_messages array (alphabetical order)
'session.expired' => "Your session timed out. Please sign in again.",
```

Codes used by the platform: `auth.failed`, `auth.expired`, `account.disabled`, `account.locked`, `confirm.failed`, `confirm.invalid`, `email.invalid`, `email.unavailable`, `mfa.failed`, `password.invalid`, `password.mismatch`, `seats.limit`, `session.expired`. Unknown codes fall back to `$_SESSION['worker.auth.failed.error']` if set, else "An unexpected error occurred."

## JS Click Handler — Visual Feedback Before Submit

The login form's Sign-in JS calls `$submit.attr('disabled', 'disabled')` immediately, then `$frm.submit()`. If the button's default state is mostly invisible (e.g. transparent with hover-only orange), the user sees no flash to confirm Enter triggered submit. Focus the button first, defer the click one tick so the focus state paints:

```js
if(13 === keycode) {
    $submit.focus();
    setTimeout(function() { $submit.click(); }, 100);
}
```

Synchronous `focus(); click();` doesn't allow the browser a paint window — the user sees nothing before navigation.
