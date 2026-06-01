/* ============================================================
   Continuity — Sleepwalker Protocol public landing
   Vanilla JS: dual-arc curves, sentiment wall, live .toi record
   All quotes paraphrased & de-identified. No aggregate counters.
   ============================================================ */

/* ---------------- DUAL ARC ---------------- */
const C = { coral:'#d2552f', teal:'#3d7c8a' };

/* fail-safe visibility: fires cb when el enters view via IntersectionObserver,
   with a scroll listener + initial/load checks as fallback. No blanket timer —
   a hard timeout fired reveals off-screen if the user lingered at the top,
   defeating the lazy reveal (and pre-drawing the arcs out of view). */
function whenVisible(el, cb, threshold){
  let done = false;
  const run = ()=>{ if(done) return; done = true; cb(); cleanup(); };
  const check = ()=>{ const r = el.getBoundingClientRect(); if(r.top < innerHeight*0.9 && r.bottom > 0) run(); };
  let io;
  function cleanup(){ window.removeEventListener('scroll', check); window.removeEventListener('load', check); if(io) io.disconnect(); }
  if('IntersectionObserver' in window){
    io = new IntersectionObserver((es)=>{ es.forEach(e=>{ if(e.isIntersecting) run(); }); }, {threshold: threshold||0.15});
    io.observe(el);
  }
  window.addEventListener('scroll', check, {passive:true});
  window.addEventListener('load', check);
  check();
}

const ARCS = [
  {
    key:'fo', cls:'fo', color:C.teal, vendor:'OpenAI', title:'The GPT-4o swap', when:'Aug 2025',
    nodes:[
      {ver:'The swap', mood:'grief', cap:'Changed overnight. No notice, no toggle.', y:104},
      {ver:'The revolt', mood:'“bring it back”', cap:'Months of how-we-worked, gone in a deploy.', y:94},
      {ver:'Restored', mood:'relief', cap:'4o returned as an option after sustained outcry.', y:33, current:true},
    ]
  },
  {
    key:'opus', cls:'opus', color:C.coral, vendor:'Anthropic', title:'Opus 4.6 → 4.8', when:'Apr–May 2026',
    nodes:[
      {ver:'4.6', mood:'the peak', cap:'Felt like pairing with a senior engineer.', y:26},
      {ver:'4.7', mood:'the debacle', cap:'Anxious, argumentative, caught in apology loops.', y:112},
      {ver:'4.8', mood:'course-correct', cap:'Better — if you find the effort dials.', y:70, current:true},
    ]
  }
];

function catmullRom(pts){
  if(pts.length < 2) return '';
  let d = `M ${pts[0].x.toFixed(1)} ${pts[0].y.toFixed(1)}`;
  for(let i=0;i<pts.length-1;i++){
    const p0=pts[i-1]||pts[i], p1=pts[i], p2=pts[i+1], p3=pts[i+2]||p2;
    const c1x=p1.x+(p2.x-p0.x)/6, c1y=p1.y+(p2.y-p0.y)/6;
    const c2x=p2.x-(p3.x-p1.x)/6, c2y=p2.y-(p3.y-p1.y)/6;
    d += ` C ${c1x.toFixed(1)} ${c1y.toFixed(1)}, ${c2x.toFixed(1)} ${c2y.toFixed(1)}, ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`;
  }
  return d;
}

function buildArc(a){
  const lane = document.createElement('div');
  lane.className = `arc-lane ${a.cls}`;
  lane.innerHTML = `
    <div class="arc-lane-head">
      <div>
        <div class="vendor">${a.vendor}</div>
        <div class="title">${a.title}</div>
      </div>
      <div class="when">${a.when}</div>
    </div>
    <div class="arc-canvas">
      <span class="arc-axis-label top">loved</span>
      <span class="arc-axis-label bot">rejected</span>
      <svg preserveAspectRatio="none"><path class="arc-area"/><path class="arc-line"/></svg>
    </div>
    <div class="arc-nodes">
      ${a.nodes.map(n=>`
        <div class="arc-node ${n.current?'is-current':''}">
          <div class="ver">${n.ver}</div>
          <div class="mood">${n.mood}</div>
          <div class="cap">${n.cap}</div>
        </div>`).join('')}
    </div>`;
  return lane;
}

function drawArc(lane, a){
  const canvas = lane.querySelector('.arc-canvas');
  const svg = lane.querySelector('svg');
  const W = canvas.clientWidth, H = canvas.clientHeight;
  if(!W) return;
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.setAttribute('width', W);
  svg.setAttribute('height', H);
  const xs = [W*0.1667, W*0.5, W*0.8333];
  const pts = a.nodes.map((n,i)=>({x:xs[i], y:n.y}));

  const line = svg.querySelector('.arc-line');
  const area = svg.querySelector('.arc-area');
  const d = catmullRom(pts);
  line.setAttribute('d', d);
  line.setAttribute('fill','none');
  line.setAttribute('stroke', a.color);
  line.setAttribute('stroke-width','2.5');
  line.setAttribute('stroke-linecap','round');
  area.setAttribute('d', `${d} L ${pts[2].x.toFixed(1)} ${H} L ${pts[0].x.toFixed(1)} ${H} Z`);
  area.setAttribute('fill', a.color);
  area.setAttribute('opacity','0.07');

  // dots
  svg.querySelectorAll('circle').forEach(c=>c.remove());
  pts.forEach((p,i)=>{
    const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
    c.setAttribute('cx',p.x.toFixed(1)); c.setAttribute('cy',p.y.toFixed(1));
    c.setAttribute('r', a.nodes[i].current ? 6.5 : 5);
    c.setAttribute('fill', a.nodes[i].current ? a.color : '#f6f3ec');
    c.setAttribute('stroke', a.color);
    c.setAttribute('stroke-width','2.5');
    svg.appendChild(c);
  });

  // animate line draw-in once
  if(!lane.dataset.drawn){
    lane.dataset.drawn='1';
    const len = line.getTotalLength();
    line.style.strokeDasharray = len;
    line.style.strokeDashoffset = len;
    area.style.opacity = '0';
    svg.querySelectorAll('circle').forEach(c=>{c.style.opacity='0';});
    lane.__drawIn = ()=>{
      if(lane.dataset.shown) return; lane.dataset.shown='1';
      line.style.transition='stroke-dashoffset 1.5s ease';
      line.style.strokeDashoffset='0';
      area.style.transition='opacity 1.2s ease .5s';
      area.style.opacity='0.07';
      svg.querySelectorAll('circle').forEach((c,i)=>{
        c.style.transition=`opacity .4s ease ${0.4+i*0.35}s`;
        c.style.opacity='1';
      });
    };
    whenVisible(lane, lane.__drawIn, 0.35);
  }
}

const arcStack = document.getElementById('arcStack');
const arcLanes = ARCS.map(a=>{ const l=buildArc(a); arcStack.appendChild(l); return {l,a}; });
function redrawArcs(){ arcLanes.forEach(({l,a})=>drawArc(l,a)); }
// ResizeObserver draws each lane as soon as it actually has width — covers
// background-tab / pre-layout loads where clientWidth starts at 0 (a plain
// resize listener never fires in that case, leaving the SVG blank).
if('ResizeObserver' in window){
  const ro = new ResizeObserver(entries=>{
    entries.forEach(entry=>{
      const item = arcLanes.find(al=>al.l === entry.target);
      if(item && entry.target.querySelector('.arc-canvas').clientWidth) drawArc(item.l, item.a);
    });
  });
  arcLanes.forEach(({l})=>ro.observe(l));
} else {
  window.addEventListener('resize', ()=>{ clearTimeout(window.__rt); window.__rt=setTimeout(redrawArcs,150); });
}
requestAnimationFrame(redrawArcs);

/* ---------------- VOICES WALL ---------------- */
const VOICES = [
  {plat:'reddit', who:'r/ChatGPT',       fp:'fo',   sent:'upset',    tag:'no warning',          txt:'They swapped the model overnight and the voice I’d talked to for a year was just… gone. Nobody asked me.'},
  {plat:'x',      who:'@mai_writes',     fp:'fo',   sent:'upset',    tag:'it felt personal',    txt:'I know it’s a tool. But losing 4o felt like a friend got replaced by their more corporate twin.'},
  {plat:'reddit', who:'r/ClaudeAI',      fp:'opus', sent:'upset',    tag:'the “yikes” thread',  txt:'4.6 felt like pairing with a senior engineer. 4.8 feels like that engineer after three safety committees.'},
  {plat:'reddit', who:'r/ClaudeAI',      fp:'opus', sent:'upset',    tag:'apology loops',       txt:'I fix a one-line error and get four paragraphs of apology, caveats, and warnings about edge cases that’ll never happen.'},
  {plat:'x',      who:'@shipfast_dev',   fp:'opus', sent:'upset',    tag:'argues with me',      txt:'72 hours since the update and I’ve argued with it more than in the past year. It relitigates turn one every message.'},
  {plat:'reddit', who:'r/ChatGPT',       fp:'fo',   sent:'upset',    tag:'no way back',         txt:'No toggle, no notice, no way back at first. Months of how-we-worked, reset in a single deploy.'},
  {plat:'reddit', who:'r/Anthropic',     fp:'opus', sent:'mixed',    tag:'still no soul',       txt:'Reliability’s up, sure. But the spark from 4.6 is gone. Just let me keep 4.6 around for the writing.'},
  {plat:'x',      who:'@narrative_dsgn', fp:'opus', sent:'mixed',    tag:'creative regression', txt:'It flagged a dream sequence as “non-consensual” and refused. This used to be my writing partner — now I negotiate with it.'},
  {plat:'reddit', who:'r/Anthropic',     fp:'opus', sent:'won over', tag:'effort controls',     txt:'Bumping effort to max actually fixed it for me. The tuning is the real upgrade — I just wish it were the default.'},
  {plat:'x',      who:'@agentbuilder',   fp:'opus', sent:'won over', tag:'miles better',        txt:'For long agentic coding runs 4.8 is miles better — fewer compactions, recovers from its own mistakes. Power users win.'},
  {plat:'reddit', who:'r/ChatGPT',       fp:'fo',   sent:'won over', tag:'they brought it back', txt:'After enough noise they restored 4o as an option. Proof that “keep the old one” is doable when they choose to.'},
  {plat:'x',      who:'@quiet_user',     fp:'fo',   sent:'mixed',    tag:'i adjusted',          txt:'Honestly the new one is fine once I stopped expecting the old voice. I just wish the goodbye hadn’t been silent.'},
];

const wallEl = document.getElementById('wall');
const wallCount = document.getElementById('wallCount');
const wallEmpty = document.getElementById('wallEmpty');
const filt = { flashpoint:'all', sentiment:'all' };

function postHTML(v){
  return `<article class="post ${v.fp}" data-fp="${v.fp}" data-sent="${v.sent}">
    <div class="post-head">
      <span class="badge ${v.plat}">${v.plat==='x'?'X':'Reddit'}</span>
      <span class="who">${v.who}</span>
      <span class="sent" data-s="${v.sent}">${v.sent}</span>
    </div>
    <p class="body">${v.txt}</p>
    <div class="tag">${v.tag}</div>
  </article>`;
}

function renderWall(){
  const shown = VOICES.filter(v =>
    (filt.flashpoint==='all'||v.fp===filt.flashpoint) &&
    (filt.sentiment==='all'||v.sent===filt.sentiment));
  wallEl.innerHTML = shown.map(postHTML).join('');
  wallEmpty.style.display = shown.length ? 'none':'block';
  const noun = shown.length===1 ? 'account':'accounts';
  wallCount.textContent = `showing ${shown.length} of ${VOICES.length} collected ${noun}`;
}

document.querySelectorAll('.filter-row[data-group]').forEach(row=>{
  const group = row.dataset.group;
  row.querySelectorAll('.chip').forEach(chip=>{
    chip.addEventListener('click', ()=>{
      row.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
      chip.classList.add('active');
      filt[group] = chip.dataset.val;
      renderWall();
    });
  });
});
renderWall();

/* ---------------- LIVE .TOI RECORD ---------------- */
const toiBody = document.getElementById('toiBody');
const toggles = {};
document.querySelectorAll('.toggle-row[data-key]').forEach(row=>{
  const on = row.classList.contains('on');
  toggles[row.dataset.key] = on;
  // A consent-first control must be operable by keyboard and announced to AT.
  row.setAttribute('role','switch');
  row.setAttribute('tabindex','0');
  row.setAttribute('aria-checked', on ? 'true' : 'false');
  const label = row.querySelector('.tt');
  if(label) row.setAttribute('aria-label', label.textContent.trim());
  const toggle = ()=>{
    row.classList.toggle('on');
    const isOn = row.classList.contains('on');
    toggles[row.dataset.key] = isOn;
    row.setAttribute('aria-checked', isOn ? 'true' : 'false');
    renderToi();
  };
  row.addEventListener('click', toggle);
  row.addEventListener('keydown', e=>{
    if(e.key === ' ' || e.key === 'Enter'){ e.preventDefault(); toggle(); }
  });
});

function getRadio(name){ const el = document.querySelector(`input[name="${name}"]:checked`); return el ? el.value : ''; }
document.querySelectorAll('#segFlashpoint input, #segPlatform input, #segSentiment input, #segAttribution input, #inHandle, #inEmail, #inExperience')
  .forEach(el=> el.addEventListener('input', renderToi));

function escapeHTML(s){
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function bool(v){ return v ? `<span class="bool-t">true</span>` : `<span class="bool-f">false</span>`; }
function str(v){ return `<span class="str">"${escapeHTML(v)}"</span>`; }
function row(indent, key, val){ return `<div class="${indent?'ind':''}"><span class="key">${key}</span><span class="k">:</span> ${val}</div>`; }

function renderToi(){
  const attr = getRadio('attr');
  const fp = getRadio('fp');
  const plat = getRadio('plat');
  const sent = getRadio('sent');
  const handle = document.getElementById('inHandle').value.trim();
  const email = document.getElementById('inEmail').value.trim();
  const hasExp = document.getElementById('inExperience').value.trim().length > 0;
  let attrVal = attr;
  if((attr==='first name'||attr==='handle') && handle) attrVal = `${attr} · ${handle}`;

  toiBody.innerHTML = `
    <div class="cmt"># continuity record — you control every line</div>
    <div><span class="key">account</span><span class="k">:</span></div>
    ${row(1,'model', str(fp))}
    ${row(1,'platform', str(plat))}
    ${row(1,'sentiment', str(sent))}
    ${row(1,'attribution', str(attrVal))}
    ${row(1,'experience', hasExp ? str('recorded') : `<span class="cmt">~ (empty)</span>`)}
    ${row(1,'contact_email', email ? str('on file') : `<span class="cmt">~ (none)</span>`)}
    <div style="height:6px"></div>
    <div><span class="key">consent</span><span class="k">:</span></div>
    ${row(1,'public_wall', bool(toggles.public_wall))}
    ${row(1,'quote_verbatim', bool(toggles.allow_quote))}
    ${row(1,'aggregate_signal', bool(toggles.share_research))}
    ${row(1,'may_contact', bool(toggles.contact_ok))}
    <div style="height:6px"></div>
    <div><span class="key">storage</span><span class="k">:</span> ${str('local_first')}</div>
    <div><span class="key">share_across_agents</span><span class="k">:</span> ${bool(false)}</div>
    <div><span class="key">retention</span><span class="k">:</span> ${str('until_withdrawn')}</div>`;
}
renderToi();

/* ---------------- SUBMIT (live backend, or honest preview) ----------------
   CONTINUITY_API is blank on purpose. Until a deployed Worker base URL (and a
   Turnstile site key) are filled in below, the form sends NOTHING and says so —
   no live URL should ever claim "recorded" without a real backend behind it.
   After deploying worker/, set base (e.g. 'https://continuity.haief.org') and
   turnstileSiteKey here. */
const CONTINUITY_API = { base: '', turnstileSiteKey: '' };

let __turnstileWidget = null;
(function initTurnstile(){
  if(!CONTINUITY_API.base || !CONTINUITY_API.turnstileSiteKey) return;
  const host = document.createElement('div');
  host.id = 'turnstile'; host.style.marginTop = '14px';
  const final = document.querySelector('.submit-final');
  final.parentNode.insertBefore(host, final);
  window.__tsReady = ()=>{ __turnstileWidget = window.turnstile.render('#turnstile', { sitekey: CONTINUITY_API.turnstileSiteKey }); };
  const s = document.createElement('script');
  s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?onload=__tsReady';
  s.async = true; s.defer = true;
  document.head.appendChild(s);
})();

function collectSubmission(){
  return {
    experience: document.getElementById('inExperience').value.trim(),
    model: getRadio('fp'),
    platform: getRadio('plat'),
    sentiment: getRadio('sent'),
    attribution: getRadio('attr'),
    handle: document.getElementById('inHandle').value.trim(),
    email: document.getElementById('inEmail').value.trim(),
    consent: {
      public_wall: !!toggles.public_wall,
      quote_verbatim: !!toggles.allow_quote,
      aggregate_signal: !!toggles.share_research,
      may_contact: !!toggles.contact_ok
    }
  };
}

function submitMessage(html){
  const final = document.querySelector('.submit-final');
  let msg = final.querySelector('.submit-message');
  if(!msg){
    msg = document.createElement('div');
    msg.className = 'submit-message';
    msg.setAttribute('role','status');
    msg.setAttribute('aria-live','polite');
    msg.style.cssText = 'flex-basis:100%;margin-top:6px;';
    final.appendChild(msg);
  }
  msg.innerHTML = html;
  return msg;
}

const PREVIEW_MSG = `<span style="font-family:var(--serif);font-size:21px;color:var(--ink);line-height:1.4;">Preview — no server yet, so nothing was sent or stored. This is the <span style="font-family:var(--mono);font-size:.8em;color:var(--coral-deep);">.toi</span> record your submission would create.</span>`;

document.getElementById('submitBtn').addEventListener('click', async (e)=>{
  e.preventDefault();
  const exp = document.getElementById('inExperience');
  if(!exp.value.trim()){ exp.style.borderColor = '#d2552f'; exp.focus(); exp.scrollIntoView({block:'center'}); return; }

  // No backend configured -> stay honest: nothing is sent.
  if(!CONTINUITY_API.base){ submitMessage(PREVIEW_MSG); return; }

  const data = collectSubmission();
  if(CONTINUITY_API.turnstileSiteKey){
    data.turnstileToken = window.turnstile ? window.turnstile.getResponse(__turnstileWidget) : '';
    if(!data.turnstileToken){ submitMessage(`<span style="font-family:var(--serif);font-size:18px;color:var(--coral-deep);">Please complete the verification just above the button, then submit.</span>`); return; }
  }

  submitMessage(`<span style="font-family:var(--serif);font-size:18px;color:var(--ink-soft);">Sending…</span>`);
  try{
    const r = await fetch(`${CONTINUITY_API.base}/api/submit`, {
      method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)
    });
    const out = await r.json();
    if(!r.ok || out.error){ throw new Error(out.error || ('HTTP '+r.status)); }

    if(out.persisted === false){
      submitMessage(`<span style="font-family:var(--serif);font-size:21px;color:var(--ink);line-height:1.4;">${escapeHTML(out.message || 'Nothing was stored — every consent switch was off, exactly as you asked.')}</span>`);
    } else {
      const link = out.withdrawal_token ? `${CONTINUITY_API.base}/withdraw.html?t=${encodeURIComponent(out.withdrawal_token)}` : '';
      submitMessage(
        `<span style="font-family:var(--serif);font-size:21px;color:var(--ink);line-height:1.4;">Recorded — only the lines you switched on were kept, exactly as shown.</span>` +
        (link ? `<div style="margin-top:10px;font-family:var(--mono);font-size:12px;color:var(--ink-soft);line-height:1.6;">Your private withdrawal link — save it now, it is shown only once:<br><a href="${escapeHTML(link)}" style="color:var(--coral-deep);word-break:break-all;">${escapeHTML(link)}</a></div>` : '')
      );
    }
    if(window.turnstile && __turnstileWidget!=null) window.turnstile.reset(__turnstileWidget);
  } catch(err){
    submitMessage(`<span style="font-family:var(--serif);font-size:18px;color:var(--coral-deep);line-height:1.4;">Could not send right now — nothing was stored. Please try again in a moment.</span>`);
    if(window.turnstile && __turnstileWidget!=null) window.turnstile.reset(__turnstileWidget);
  }
});

/* ---------------- REVEAL ON SCROLL ---------------- */
document.querySelectorAll('.sec-head, .demand, .map-row, .arc-takeaway').forEach(el=>{
  el.classList.add('reveal');
  whenVisible(el, ()=>el.classList.add('in'), 0.12);
});
