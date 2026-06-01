# Continuity API — Cloudflare Worker

Consent-first submission backend for the Continuity landing page. **D1** (SQLite)
for storage, **Turnstile** for abuse protection, **withdrawal tokens** for the
"withdraw any time" promise. No third-party analytics, no big-cloud dependency.

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

## Consent enforcement (the point of the whole thing)

Storage is gated on the four switches at write time:

- **All switches off** → *nothing is persisted at all* (the form's "count for nothing at all"). The response says so.
- `aggregate_signal` or `public_wall` on → the experience text is stored; otherwise it is not.
- `may_contact` on → email stored; otherwise dropped.
- `attribution = anonymous` → handle is not stored.
- The withdrawal token is returned to the submitter **once** and kept only as a `SHA-256` hash, so a DB leak can neither reveal nor delete-by-token.

`/api/aggregate` counts only rows with `consent_aggregate_signal = 1`.

## Deploy (human, one time)

```bash
npm i -g wrangler            # or: npx wrangler ...
cd web/continuity/worker

wrangler d1 create continuity
#   → paste the returned database_id into wrangler.toml ([[d1_databases]].database_id)
wrangler d1 execute continuity --file=./schema.sql

wrangler secret put TURNSTILE_SECRET     # from the Cloudflare Turnstile dashboard

# edit wrangler.toml: set ALLOWED_ORIGIN, and bind the route
#   continuity.haief.org/api/*  (zone haief.org)
wrangler deploy
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
verification is skipped so you can exercise submit/withdraw against a local D1
(`wrangler d1 execute continuity --local --file=./schema.sql`).
