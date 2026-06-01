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
| `continuity.js` | Dual-arc SVG comparison, sentiment-wall filter, live `.toi` record preview, submit handler. |

No build step, no bundler, no raster assets — just static files plus CDN fonts.

## Preview locally

```bash
cd web/continuity
python3 -m http.server 8000   # then open http://localhost:8000
```

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

- **No backend yet.** The submit button does **not** send or store anything. Its confirmation
  state says so explicitly ("Preview — no server yet, so nothing was sent or stored. This is the
  `.toi` record your submission would create."). Do not swap in a "Recorded / kept" message until
  a real, consented backend exists — on a live public URL a false confirmation is actively harmful.
- **No fabricated aggregate numbers.** No report counts, sentiment percentages, or signature
  totals as invented precision. Every qualitative section works with zero aggregate stats, so the
  page can launch without them. Counters ship only when backed by real consented submissions or by
  figures cited from public reporting on the two events. This is a Transparency + Data Dignity
  requirement, not deferred polish.
- **Quotes are paraphrased and representative**, not verbatim transcription; platform attribution
  is illustrative. Keep them labeled as such.

## Open decisions (Josh's calls — see the handoff brief §7)

1. Does the form write to a real backend at launch (enabling real counts), or is v1
   collection-only / manual review?
2. Any sourced stats wanted at launch, or qualitative-only first?
3. Single micro-site (`continuity.haief.org`) vs. splitting report/act onto subpaths?

Out of scope for v1: the editorial essay page, the developer-docs surface, and the
pledge-counter / activist framing (deferred until real signature data exists).
