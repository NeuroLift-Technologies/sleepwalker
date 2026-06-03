# Continuity API — Cloudflare Worker

Consent-first submission backend for the Continuity landing page. **D1** (SQLite)
stores consented records, **Turnstile** provides abuse protection, and hashed
**withdrawal tokens** support the "withdraw any time" promise. The Worker does
not include analytics or other tracking integrations.

> **Not deployed by this PR.** Deploying to production is a human action
> (governance: no production deploys without Josh's sign-off). The code + config
> live here ready to go; the live page stays in honest-preview mode until the
> steps below are done and the front-end is pointed at the deployed Worker.

## Endpoints

| Method + path | Purpose |
|---|---|
| `POST /api/submit` | Validate, verify Turnstile, store **only what consent allows**, return a one-time withdrawal token. |
| `GET /api/aggregate` | Real counts only (consented rows). Returns `{ enough:false }` until `AGGREGATE_MIN` rows exist — no invented precision. |
| `POST /api/withdraw` | `{ token }` → hard-delete the matching row. Same response whether or not it matched (can't probe tokens). |

All routes set CORS headers using `ALLOWED_ORIGIN`; `OPTIONS` returns a `204`
preflight response. Unknown paths return `{ "error": "not_found" }`.

## Front-end contract

`web/continuity/continuity.js` calls this Worker only after
`CONTINUITY_API.base` is configured. The submit body is:

```json
{
  "experience": "What changed, and how it landed",
  "model": "Opus (Anthropic)",
  "platform": "Reddit",
  "sentiment": "upset",
  "attribution": "anonymous",
  "handle": "",
  "email": "",
  "consent": {
    "public_wall": false,
    "quote_verbatim": false,
    "aggregate_signal": true,
    "may_contact": false
  },
  "turnstileToken": "<present only when Turnstile is enabled>"
}
```

The Worker returns one of these successful shapes:

```json
{ "ok": true, "persisted": false, "message": "Nothing was stored ..." }
```

```json
{ "ok": true, "persisted": true, "withdrawal_token": "<shown once>" }
```

The front end turns `withdrawal_token` into
`<CONTINUITY_API.base>/withdraw.html?t=<token>`. `withdraw.html` then posts the
token to same-origin `/api/withdraw`, so live hosting should put the static page
and `/api/*` Worker route on the same public host.

## Consent enforcement (the point of the whole thing)

Storage is gated on the four switches at write time:

- **All switches off** → *nothing is persisted at all* (the form's "count for nothing at all"). The response says so.
- `aggregate_signal` or `public_wall` on → the experience text is stored; otherwise it is not.
- `may_contact` on → email stored; otherwise dropped.
- `attribution = anonymous` → handle is not stored.
- `quote_verbatim` is stored as consent metadata; no current endpoint publishes
  quotes directly.
- The withdrawal token is returned to the submitter **once** and kept only as a
  `SHA-256` hash, so stored data does not reveal the plaintext token.

`/api/aggregate` counts only rows with `consent_aggregate_signal = 1`.

### Validation and limits

- `experience` is required and clipped to 4000 characters.
- `model` is clipped to 120 characters and defaults to `another model`.
- `platform` is clipped to 60 characters.
- `sentiment` must be `upset`, `mixed`, or `won over`; otherwise it defaults to
  `upset`.
- `attribution` must be `anonymous`, `first name`, or `handle`; otherwise it
  defaults to `anonymous`.
- `handle` is clipped to 120 characters; `email` is clipped to 200 characters.

Error responses are JSON:

| Error | When |
|---|---|
| `bad_request` | Body is not valid JSON/object for `/api/submit`. |
| `turnstile_failed` | `TURNSTILE_SECRET` is set and verification fails. |
| `experience_required` | Submission has no non-empty experience text. |
| `token_required` | `/api/withdraw` body has no token. |
| `not_found` | Route/method is not implemented. |
| `server_error` | Unhandled Worker error; stack details are logged server-side only. |

## Deploy (human, one time)

```bash
cd web/continuity/worker

npx wrangler@latest d1 create continuity
#   → paste the returned database_id into wrangler.toml ([[d1_databases]].database_id)
npx wrangler@latest d1 execute continuity --remote --file=./schema.sql

npx wrangler@latest secret put TURNSTILE_SECRET     # from the Cloudflare Turnstile dashboard

# edit wrangler.toml: set ALLOWED_ORIGIN, and bind the route
#   continuity.haief.org/api/*  (zone haief.org)
npx wrangler@latest deploy --dry-run
npx wrangler@latest deploy
```

Then go live on the page: in `web/continuity/continuity.js`, set
```js
const CONTINUITY_API = { base: 'https://continuity.haief.org', turnstileSiteKey: '<your Turnstile site key>' };
```
That flips the form from honest preview to real submission (with the withdrawal
link) and renders the Turnstile widget. Leave it blank and the page sends nothing.

## Config reference

| Binding / var | Where | Meaning |
|---|---|---|
| `DB` | `[[d1_databases]]` | D1 database binding |
| `TURNSTILE_SECRET` | `wrangler secret` | Turnstile server secret (verify) |
| `ALLOWED_ORIGIN` | `[vars]` | CORS origin, e.g. `https://continuity.haief.org` |
| `AGGREGATE_MIN` | `[vars]` | Min consented rows before `/api/aggregate` returns numbers |

## Local dev

`wrangler dev` runs the Worker locally. With no `TURNSTILE_SECRET` set, Turnstile
verification is skipped so you can exercise submit/withdraw against a local D1:

```bash
cd web/continuity/worker
npx wrangler@latest d1 execute continuity --local --file=./schema.sql
npx wrangler@latest dev --local --port 8787
```

For end-to-end local form testing, temporarily set
`CONTINUITY_API.base = 'http://localhost:8787'` in `../continuity.js`, serve the
static page from `web/continuity`, then revert the local edit before committing.

`GET /api/aggregate` is implemented for future counters and manual checks; the
current static page does not call it.
