# Continuity — public landing page

Static landing page for **`continuity.haief.org`**, the public advocacy + evidence-collection
surface for the Sleepwalker Protocol.

**Naming (locked):** *Continuity* (public hook) · *Sleepwalker* (the protocol beneath it) ·
*Solidarity Framework* (the umbrella).

Built from the Claude Design hi-fi handoff **`NLT-HND-2026-001-Continuity-HiFi`** (v1.0.0),
shipped as refined vanilla HTML/CSS/JS per Josh's direction.

## Files

| File | What it is |
|---|---|
| `index.html` | The single-scroll page. All CSS is inline in `<head>`; type via Google Fonts CDN. |
| `continuity.js` | Dual-arc SVG comparison, sentiment-wall filter, live `.toi` record preview, submit handler, and optional API wiring. |
| `withdraw.html` | Standalone "withdraw your record" page; takes a token (`?t=...`) and calls same-origin `/api/withdraw`. |
| `worker/` | Cloudflare Worker backend (D1 + Turnstile + withdrawal tokens). See `worker/README.md`. |

No build step, no bundler, no raster assets — just static files plus CDN fonts.

## Runtime modes

### Preview-only mode (default)

The consent-first form is wired to a Cloudflare Worker (`worker/`) but **disabled
by default**. `continuity.js` ships with:

```js
const CONTINUITY_API = { base: '', turnstileSiteKey: '' };
```

With `base` blank, submitting the form sends no network request and shows the
honest preview message:

> Preview — no server yet, so nothing was sent or stored.

This mode is safe for static previews and local design review.

### Live API mode

After a human-approved Worker deploy (see `worker/README.md`), set
`CONTINUITY_API.base` and `turnstileSiteKey` in `continuity.js` to switch the form
to real submission, Turnstile verification, and a one-time withdrawal link:

```js
const CONTINUITY_API = {
  base: 'https://continuity.haief.org',
  turnstileSiteKey: '<Cloudflare Turnstile site key>'
};
```

The static site and Worker are expected to share the same public host in live
mode: submit calls `${CONTINUITY_API.base}/api/submit`, while `withdraw.html`
uses relative `/api/withdraw` so private withdrawal links work at
`https://continuity.haief.org/withdraw.html?t=...`.

Decisions made for the backend (Josh): **D1** for storage · **Cloudflare
Turnstile** for abuse protection · **withdrawal-token link** for the
"withdraw any time" promise.

## Preview locally

```bash
cd web/continuity
python3 -m http.server 8000   # then open http://localhost:8000
```

Local static preview exercises the page, filters, consent toggles, and live
`.toi` preview. It does not exercise Worker submission unless you separately run
`worker/` with Wrangler and point `CONTINUITY_API.base` at that local Worker.

## Page structure (per the build brief)

1. **Hero** — "My AI changed overnight."
2. **Dual-arc comparison (centerpiece)** — OpenAI GPT-4o swap vs Anthropic Opus 4.6→4.8;
   the same failure-and-walkback shape across two vendors.
3. **Sentiment wall** — paraphrased, de-identified accounts, filterable by flashpoint and by
   feeling. "Won over" voices are kept on purpose.
4. **What users found → what the framework calls it** — maps real asks onto the standard.
5. **Three demands** — warn us / let us keep the old one / make it opt-in, each with its real precedent.
6. **Consent-first `.toi` form** — the differentiator; every field has a matching consent switch
   and a live preview of the exact record it would create.

## Hard constraints (do not regress)

- **Preview mode must stay honest.** With `CONTINUITY_API.base` blank, the submit
  button must not send or store anything. Its confirmation state must say so
  explicitly. Do not show a "Recorded / kept" message unless the deployed Worker
  actually accepts the submission.
- **Live mode needs both halves.** A real launch requires the static files, the
  Worker route, D1 schema, `TURNSTILE_SECRET`, `ALLOWED_ORIGIN`, and front-end
  `CONTINUITY_API` values to be aligned. Production deployment remains a human
  sign-off action under NLT governance.
- **No fabricated aggregate numbers.** No report counts, sentiment percentages, or signature
  totals as invented precision. Every qualitative section works with zero aggregate stats, so the
  page can launch without them. Counters ship only when backed by real consented submissions or by
  figures cited from public reporting on the two events. This is a Transparency + Data Dignity
  requirement, not deferred polish.
- **Quotes are paraphrased and representative**, not verbatim transcription; platform attribution
  is illustrative. Keep them labeled as such.
- **Aggregate API is backend-only today.** `worker/src/index.js` implements
  `GET /api/aggregate`, but `index.html`/`continuity.js` do not render live
  counters yet.

## Open decisions (Josh's calls — see the handoff brief §7)

1. ~~Backend at launch?~~ **Decided:** Cloudflare Worker (D1 + Turnstile + withdrawal
   tokens), built in `worker/`. Remaining sub-call: *when* to flip it live (deploy +
   set `CONTINUITY_API`) vs. launch the page in preview-only mode first.
2. Any sourced stats wanted at launch, or qualitative-only first?
3. Single micro-site (`continuity.haief.org`) vs. splitting report/act onto subpaths?

Out of scope for v1: the editorial essay page, the developer-docs surface, and the
pledge-counter / activist framing (deferred until real signature data exists).
