/* ============================================================================
 * Continuity — Cloudflare Worker API
 *
 * Consent-first submission backend for the Sleepwalker Protocol landing page.
 * The form *models* consent, so this backend enforces it at write time:
 *   - a row only carries the fields the submitter switched on
 *   - if they switched everything off ("count for nothing at all"), nothing is
 *     persisted at all, and we say so
 *   - the withdrawal token is returned once and stored only as a SHA-256 hash
 *   - /aggregate returns real counts only, never invented precision
 *
 * Routes:
 *   POST /api/submit          -> validate + Turnstile + consent-gated insert
 *   GET  /api/aggregate       -> real counts (or { enough:false })
 *   POST /api/withdraw        -> { token } -> hard-delete the matching row
 *
 * Bindings (wrangler.toml):
 *   DB                 D1 database
 *   TURNSTILE_SECRET   secret (wrangler secret put TURNSTILE_SECRET)
 *   ALLOWED_ORIGIN     var, e.g. https://continuity.haief.org
 *   AGGREGATE_MIN      var (string int), min rows before counts are shown
 * ========================================================================== */

const SENTIMENTS = ['upset', 'mixed', 'won over'];
const ATTRIBUTIONS = ['anonymous', 'first name', 'handle'];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = env.ALLOWED_ORIGIN || '*';

    if (request.method === 'OPTIONS') return cors(new Response(null, { status: 204 }), origin);

    try {
      if (url.pathname === '/api/submit' && request.method === 'POST') {
        return cors(await handleSubmit(request, env), origin);
      }
      if (url.pathname === '/api/aggregate' && request.method === 'GET') {
        return cors(await handleAggregate(env), origin);
      }
      if (url.pathname === '/api/withdraw' && request.method === 'POST') {
        return cors(await handleWithdraw(request, env), origin);
      }
      return cors(json({ error: 'not_found' }, 404), origin);
    } catch (err) {
      // Log server-side only; never return error/stack details to the client.
      console.error('continuity-api error:', err && err.stack || err);
      return cors(json({ error: 'server_error' }, 500), origin);
    }
  },
};

/* ----------------------------- /api/submit ------------------------------ */
async function handleSubmit(request, env) {
  const body = await request.json().catch(() => null);
  if (!body || typeof body !== 'object') return json({ error: 'bad_request' }, 400);

  // Turnstile (spam/abuse). Skipped only if no secret is configured (local dev).
  if (env.TURNSTILE_SECRET) {
    const ok = await verifyTurnstile(env.TURNSTILE_SECRET, body.turnstileToken, request.headers.get('CF-Connecting-IP'));
    if (!ok) return json({ error: 'turnstile_failed' }, 403);
  }

  // Validate the required core.
  const experience = clip(str(body.experience), 4000);
  if (!experience) return json({ error: 'experience_required' }, 422);
  const model = clip(str(body.model), 120) || 'another model';
  const platform = clip(str(body.platform), 60);
  const sentiment = SENTIMENTS.includes(body.sentiment) ? body.sentiment : 'upset';
  const attribution = ATTRIBUTIONS.includes(body.attribution) ? body.attribution : 'anonymous';

  // Consent switches drive what is stored.
  const c = body.consent || {};
  const publicWall = !!c.public_wall;
  const quote = !!c.quote_verbatim;
  const aggregate = !!c.aggregate_signal;
  const mayContact = !!c.may_contact;

  // "Switch off to count for nothing at all": if nothing is switched on, persist
  // nothing. Honor it literally and tell the submitter.
  if (!publicWall && !aggregate && !mayContact) {
    return json({ ok: true, persisted: false, message: 'Nothing was stored — every consent switch was off, so your report counts for nothing at all, exactly as you asked.' });
  }

  // Field-level consent gating.
  const storeExperience = publicWall || aggregate;   // the content itself
  const handle = (attribution !== 'anonymous') ? clip(str(body.handle), 120) : null;
  const email = mayContact ? clip(str(body.email), 200) : null;

  const id = crypto.randomUUID();
  const token = crypto.randomUUID() + crypto.randomUUID().replace(/-/g, '');
  const tokenHash = await sha256(token);

  await env.DB.prepare(
    `INSERT INTO submissions
       (id, created_at, model, platform, sentiment, experience, attribution, handle, email,
        consent_public_wall, consent_quote_verbatim, consent_aggregate_signal, consent_may_contact,
        withdrawal_token_hash)
     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
  ).bind(
    id, new Date().toISOString(), model, platform, sentiment,
    storeExperience ? experience : null,
    attribution, handle, email,
    publicWall ? 1 : 0, quote ? 1 : 0, aggregate ? 1 : 0, mayContact ? 1 : 0,
    tokenHash
  ).run();

  // Plaintext token is returned exactly once; we only kept its hash.
  return json({ ok: true, persisted: true, withdrawal_token: token });
}

/* ---------------------------- /api/aggregate ---------------------------- */
async function handleAggregate(env) {
  const min = parseInt(env.AGGREGATE_MIN || '25', 10);
  const total = (await env.DB.prepare(
    `SELECT COUNT(*) AS n FROM submissions WHERE consent_aggregate_signal = 1`
  ).first('n')) || 0;

  // Data-honesty rule: no invented precision. Below threshold we expose no
  // numbers at all — just "not enough yet".
  if (total < min) return json({ enough: false, threshold: min });

  const rows = await env.DB.prepare(
    `SELECT sentiment, COUNT(*) AS n FROM submissions
      WHERE consent_aggregate_signal = 1 GROUP BY sentiment`
  ).all();
  const by_sentiment = {};
  for (const r of (rows.results || [])) by_sentiment[r.sentiment] = r.n;

  return json({ enough: true, total, by_sentiment });
}

/* ---------------------------- /api/withdraw ----------------------------- */
async function handleWithdraw(request, env) {
  const body = await request.json().catch(() => null);
  const token = body && str(body.token);
  if (!token) return json({ error: 'token_required' }, 400);

  const tokenHash = await sha256(token);
  await env.DB.prepare(
    `DELETE FROM submissions WHERE withdrawal_token_hash = ?`
  ).bind(tokenHash).run();

  // Indistinguishable response: identical body whether or not a row matched, so
  // the endpoint can't be used to probe which tokens are valid. The delete is
  // idempotent — a non-matching token simply deletes nothing.
  return json({ ok: true });
}

/* ------------------------------- helpers -------------------------------- */
async function verifyTurnstile(secret, token, ip) {
  if (!token) return false;
  const form = new FormData();
  form.append('secret', secret);
  form.append('response', token);
  if (ip) form.append('remoteip', ip);
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
  const data = await r.json().catch(() => ({}));
  return !!data.success;
}

async function sha256(s) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function str(v) { return typeof v === 'string' ? v.trim() : (v == null ? '' : String(v).trim()); }
function clip(v, n) { return v ? v.slice(0, n) : v; }
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json' } });
}
function cors(resp, origin) {
  const h = new Headers(resp.headers);
  h.set('Access-Control-Allow-Origin', origin);
  h.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  h.set('Access-Control-Allow-Headers', 'Content-Type');
  h.set('Vary', 'Origin');
  return new Response(resp.body, { status: resp.status, headers: h });
}
