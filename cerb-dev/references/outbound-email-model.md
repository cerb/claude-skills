# Outbound Email Model (`Model_DevblocksOutboundEmail`)

The email model is created via `DevblocksPlatform::services()->mail()->createComposeModelFromProperties()` or `createReplyModelFromProperties()` and sent with `$email_model->send($error)`.

## Key Methods

- `isDeliverable()` — returns `true` if `getTo()` is non-empty and `dont_send` is not set
- `getTo()` / `getCc()` / `getBcc()` — call `CerberusMail::parseRfcAddresses()` on the stored raw string; invalid addresses are silently dropped
- `send(?string &$error)` — validates, delivers, and returns `true` on success (including intentional no-send); returns `false` with `$error` set on hard failures

## Silent Drop vs. Error

`parseRfcAddresses()` silently drops any address that:
- Has no `@` (local/hostless like `hildy`)
- Fails Egulias `RFCValidation`

`send()` will error (return `false` + set `$error`) if a To/Cc/Bcc field has a non-empty raw value that produces **zero** valid addresses after parsing. Empty fields are allowed (phone-call tickets, `dont_send` flag).

## `is_not_sent` Flag

Set on the saved `DAO_Message` record:

| Code path | Condition for `is_not_sent = 1` |
|---|---|
| `CerberusMail::compose()` | `!$email_model->isDeliverable()` |
| `CerberusMail::sendTicketReply()` | `$email_model->getProperty('dont_send')` only |

The reply path does **not** check `isDeliverable()` for `is_not_sent` — it relies on `dont_send` being explicitly set. Intentionally no-To replies (rare) will therefore be marked Sent.

## `dont_send` Property

Set to skip delivery while still saving the message record (e.g., automations that compose but hold). Bypasses the invalid-address validation check in `send()`.
