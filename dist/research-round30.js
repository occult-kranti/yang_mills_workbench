/* Additive reader layer. Scientific conclusions enter only through reviewed data. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND30_DATA;
  if (!prior || !D) return;
  const arr = value => Array.isArray(value) ? value : [];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const validId = value => /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(String(value));
  const safePath = value => {
    const raw = String(value ?? '');
    if (!raw || /[\s\\:#?<>"'\u0000-\u001f\u007f%]/.test(raw) || raw.startsWith('/')) return '';
    return raw.split('/').some(part => !part || part === '.' || part === '..') ? '' : raw.split('/').map(encodeURIComponent).join('/');
  };
  const safeURL = value => {
    const raw = String(value ?? '');
    if (!/^https:\/\/[^\s\\<>"'\u0000-\u001f\u007f]+$/i.test(raw)) return '';
    try { const url = new URL(raw); return url.hostname && !url.username && !url.password ? url.href : ''; } catch { return ''; }
  };
  const link = (route, label) => validId(route) ? `<a href="#research/${route}">${esc(label)}</a>` : esc(label);
  const source = (value, label) => {
    const row = typeof value === 'string' ? {path: value} : value ?? {};
    const raw = row.url ?? row.path ?? '', remote = safeURL(raw), path = safePath(raw);
    const href = remote || (path ? 'https://github.com/occult-kranti/yang_mills_workbench/blob/main/' + path : '');
    const text = label ?? row.title ?? row.label ?? raw ?? 'Source';
    return href ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(text)} <span aria-hidden="true">↗</span></a>` : esc(text);
  };
  const download = (value, label) => { const path = safePath(value); return path ? `<a href="${esc(path)}" download>${esc(label)}</a>` : esc(label); };
  const list = values => arr(values).length ? `<ul>${values.map(value => `<li>${esc(value)}</li>`).join('')}</ul>` : '';
  const sources = values => `<ul class="r29-evidence">${arr(values).map(value => `<li>${source(value)}</li>`).join('')}</ul>`;
  const reviewed = loop => loop?.stage === 'reviewed' && /^[a-f0-9]{64}$/.test(String(loop.gate_sha256)) && typeof loop.accepted === 'string' && !!loop.accepted.trim() && arr(loop.limitations).length > 0 && /^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])/.test(String(loop.verdict));
  const loops = arr(D.loops), byRoute = new Map(loops.filter(loop => validId(loop.id)).map(loop => ['round30-' + loop.id, loop]));
  const counts = () => ({requested: 3, completed: loops.filter(reviewed).length});
  const own = new Set(['home', 'drafts', 'round30', 'round30-results', 'round30-roadmap', 'round30-sources', 'round30-proof', 'round30-calculator', ...byRoute.keys()]);
  const delegatedCurrent = new Set(['hnm-findings', 'hnm-priorities', 'research-network', 'contributions']);
  function normalizeRoute(value = 'home') {
    let route = String(value || 'home').split('?')[0];
    if (route === 'round30' && location.hash.startsWith('#research/round30/')) route = location.hash.slice('#research/'.length).split('?')[0];
    if (route.startsWith('round30/')) {
      const tail = route.slice('round30/'.length);
      route = {home:'home', results:'round30-results', loops:'round30-results', roadmap:'round30-roadmap', sources:'round30-sources', proof:'round30-proof',calculator:'round30-calculator'}[tail] ?? 'round30-' + tail;
    }
    return route === 'round30' ? 'home' : route;
  }
  function nav(route) {
    const entries = [['home','Home'], ['round30-results','Latest results'], ['round30-calculator','Certificate calculator'], ['hnm-priorities','Ranked findings'], ['hnm-findings','HNM catalog'], ['research-network','Network'], ['drafts','Complete draft'], ['round30-roadmap','Next goals'], ['round30-sources','Sources']];
    return `<nav class="rc-nav r30-nav" aria-label="Research navigation">${entries.map(([target,label]) => `<a href="#research/${target}"${route === target ? ' aria-current="page"' : ''}>${label}</a>`).join('')}</nav>`;
  }
  function badge(loop) {
    const ok = reviewed(loop), limited = /limited|insufficient|reject|fail/.test(loop?.verdict ?? '');
    return `<span class="r29-badge r29-badge-${!ok ? 'pending' : limited ? 'limited' : 'accepted'}">${esc(ok ? String(loop.verdict).replaceAll('_',' ') : 'Review not verified')}</span>`;
  }
  function card(loop) {
    return `<article class="rc-result r30-card"><div class="r29-card-top"><p class="rc-kicker">Investigation ${esc(loop.sequence)} · ${esc(String(loop.id).toUpperCase())}</p>${badge(loop)}</div><h2>${esc(loop.title)}</h2><p>${esc(reviewed(loop) ? loop.summary || loop.accepted : 'The review binding is incomplete. No finding is presented.')}</p>${reviewed(loop) ? `<p class="r29-card-limit"><strong>Limit:</strong> ${esc(loop.limitations[0])}</p>` : ''}<p>${link('round30-' + loop.id, 'Read the derivation and evidence →')}</p></article>`;
  }
  function scope() {
    return `<aside class="r29-scope r30-scope"><p class="rc-kicker">Scope of the work</p><p>${esc(D.scope_statement)}</p><p>Hruday / HNM names identify project records and derivations. Established methods retain their authors; scientific priority is unverified. Historical lenses do not imply participation or endorsement.</p>${link('round30-proof','Read the open proof obligations →')}</aside>`;
  }
  function home() {
    const count = counts();
    return `<header class="r29-home-hero"><div><p class="rc-kicker">Hruday N M (BUNZEEY) · Round30</p><h1>Follow the evidence.<br>Keep the open questions.</h1><p class="r29-home-lede">${esc(D.summary)}</p><div class="r29-home-actions">${link('round30-results','Read the latest results →')}${download(D.draft?.url,'Download Draft03 ↓')}</div></div><aside class="r29-home-status"><p class="rc-kicker">This research cycle</p><p class="r29-home-count" data-r30-completed>${count.completed}<span> / ${count.requested}</span></p><h2>Investigations reviewed</h2><p>Each investigation follows the preceding review. This counts completed work, not a percentage of the Yang–Mills proof.</p>${link('round30-roadmap','What remains open →')}</aside></header>${scope()}<section aria-labelledby="r30-latest"><div class="r29-section-head"><h2 id="r30-latest">Three investigations, with their limits.</h2>${link('hnm-priorities','All ranked findings →')}</div><div class="r29-grid r30-results-grid">${loops.map(card).join('')}</div></section><section class="r29-reader-paths" aria-label="Choose a reading path"><a href="#research/drafts"><p class="rc-kicker">Read</p><h2>The complete argument</h2><p>Draft03 connects the earlier work to this cycle. Draft02 remains available.</p></a><a href="#research/research-network"><p class="rc-kicker">Trace</p><h2>Claims and dependencies</h2><p>Follow each result to its premises, equations and source record.</p></a><a href="#research/round30-sources"><p class="rc-kicker">Check</p><h2>What was actually read</h2><p>Modern research, historical passages and access limitations.</p></a></section><p class="r29-muted">Author and project direction: ${esc(D.author)}. Model-assisted derivation and review; no external human peer review is claimed.</p>`;
  }
  function results() {
    return `<header class="r22-page-head"><p class="rc-kicker">Round30 · ${counts().completed} of 3 reviewed</p><h1>Latest research results</h1><p>Read the accepted scope before applying a result. A limited investigation remains part of the record.</p></header><div class="r29-grid r30-results-grid">${loops.map(card).join('')}</div>${scope()}`;
  }
  function loopPage(loop) {
    if (!reviewed(loop)) return `<header class="r22-page-head"><h1>${esc(loop.title)}</h1></header><p>The source-bound review is incomplete. No accepted result is displayed.</p>`;
    const statements = arr(D.registry?.statements).filter(row => arr(loop.statement_ids).includes(row.id));
    const equations = arr(loop.equations);
    return `<header class="r22-page-head"><p class="rc-kicker">Round30 · Investigation ${esc(loop.sequence)} · ${esc(loop.contribution_id)}</p><h1>${esc(loop.title)}</h1>${badge(loop)}<p>${esc(loop.summary || loop.target)}</p></header><section class="r30-conclusion"><h2>Reviewed conclusion</h2><p>${esc(loop.accepted)}</p>${loop.model ? `<p class="r29-model"><strong>Model:</strong> ${esc(loop.model)}</p>` : ''}</section>${arr(loop.derivation_steps).length ? `<section class="r30-section"><h2>How the result follows</h2><ol>${loop.derivation_steps.map(step => `<li>${esc(typeof step === 'string' ? step : step.text ?? step.detail ?? step.title ?? '')}</li>`).join('')}</ol></section>` : ''}${equations.length ? `<section class="r30-section"><h2>Recorded equations</h2>${equations.map(eq => `<figure class="r30-equation"><figcaption>${esc(eq.label ?? eq.id ?? 'Equation')}</figcaption><pre><code>${esc(eq.expression ?? eq.formula ?? '')}</code></pre>${eq.scope ? `<p>${esc(eq.scope)}</p>` : ''}</figure>`).join('')}</section>` : ''}${statements.length ? `<section class="r30-section"><h2>Named statements</h2><ul>${statements.map(row => `<li>${link('hnm-findings',row.id + ' · ' + (row.display_name ?? row.title ?? 'Statement'))}</li>`).join('')}</ul></section>` : ''}${arr(loop.applications).length ? `<section class="r30-section"><h2>What this enables</h2>${list(loop.applications)}</section>` : ''}<section class="r30-section r30-limitations"><h2>Limits and open questions</h2>${list(loop.limitations)}</section><section class="r30-section"><h2>Proof and review record</h2><p>The conclusion is bound to its contract, both derivations and the skeptical review.</p>${sources(loop.sources)}<details><summary>Review identifier</summary><p class="r30-hash">${esc(loop.gate_sha256)}</p></details></section>`;
  }
  function drafts() {
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday N M (BUNZEEY)</p><h1>The complete research draft</h1><p>Read the model, derivations and limitations together. HNM labels provide traceable names; they are not claims of established scientific priority.</p></header><section class="r29-draft-feature"><div><p class="rc-kicker">Current edition · Draft03</p><h2>Earlier results and the Round30 continuation.</h2><p>${esc(D.draft?.title)}</p><div class="r29-home-actions">${download(D.draft?.url,'Download Draft03 PDF ↓')}${source(D.draft?.path,'Manuscript source record')}</div><p>${download('hnm-registry-r30.json','Download the current HNM registry ↓')}</p></div><aside><strong>Hruday N M</strong><span>BUNZEEY</span><hr><p>Human author and project direction. AI-assisted mathematical work and review are disclosed in the manuscript.</p></aside></section><section class="r30-section"><h2>Preserved previous edition</h2><p>${download(D.previous_draft?.url,'Download Draft02 · through Round29 ↓')}</p><p>${link('round29','Read the Round29 checkpoint →')}</p></section><details class="drafts-reader"><summary>Read Draft03 in this page</summary>${safePath(D.draft?.url) ? `<iframe title="Complete Hruday research manuscript, Draft03" src="${esc(safePath(D.draft.url))}" loading="lazy"></iframe>` : '<p>The PDF address is unavailable.</p>'}</details>${scope()}`;
  }
  function roadmap() {
    const goals = arr(D.roadmap?.goals);
    return `<header class="r22-page-head"><p class="rc-kicker">Selected after this cycle's reviews</p><h1>Next questions</h1><p>${esc(D.roadmap?.summary ?? D.roadmap?.ranking_basis ?? 'These are planned follow-ups. They were not executed as extra investigations in this three-loop cycle.')}</p></header><p class="r30-plan-notice">Planned work is separate from the three reviewed investigations above.</p><div class="r29-grid">${goals.map((goal,index) => `<article class="rc-result r30-card"><p class="rc-kicker">Priority ${esc(goal.rank ?? index + 1)} · ${esc(goal.id)}</p><h2>${esc(goal.title ?? goal.target)}</h2><span class="r29-badge r29-badge-pending">${esc(String(goal.status ?? 'planned_not_executed').replaceAll('_',' '))}</span><p>${esc(goal.target ?? '')}</p>${goal.missing_premise ? `<p><strong>Missing step:</strong> ${esc(goal.missing_premise)}</p>` : ''}${goal.proposed_first_loop_test ? `<details><summary>Proposed test</summary><p>${esc(goal.proposed_first_loop_test)}</p></details>` : ''}${list(goal.limitations)}</article>`).join('')}</div><p>${source('research/round30/advisor/roadmap.json','Read the full roadmap and dependencies')}</p>`;
  }
  function filterSources(query = '', area = 'all') {
    const needle = String(query).trim().toLowerCase();
    return arr(D.survey).filter(row => (area === 'all' || row.area === area) && [row.id,row.title,row.authors,row.provenance,row.use,row.reading_depth,row.limits].join(' ').toLowerCase().includes(needle));
  }
  function sourceCards(query = '', area = 'all') {
    const rows = filterSources(query, area);
    if (!rows.length) return '<p class="r29-empty">No source records match these filters.</p>';
    return rows.map(row => `<article class="rc-result r30-source"><p class="rc-kicker">${esc(row.area)} · ${esc(row.id)}</p><h2>${row.url ? source({url:row.url},row.title) : esc(row.title)}</h2><p class="r29-muted">${esc(row.provenance ?? '')}${row.date ? ' · ' + esc(row.date) : ''}</p><p><strong>Reading depth:</strong> ${esc(row.reading_depth || 'See the source ledger.')}</p>${row.use ? `<p><strong>Use here:</strong> ${esc(row.use)}</p>` : ''}${row.limits ? `<p><strong>Unresolved:</strong> ${esc(row.limits)}</p>` : ''}${row.validation_status ? `<p><strong>Evidence status:</strong> ${esc(row.validation_status)}</p>` : ''}<details><summary>Passages and provenance</summary>${list(row.passages)}${row.overlap ? `<p>${esc(row.overlap)}</p>` : ''}${list(row.access_failures)}<p>${source(row.ledger,'Complete source ledger')}</p></details></article>`).join('');
  }
  function survey() {
    return `<header class="r22-page-head"><p class="rc-kicker">Selected reading · explicit limits</p><h1>Sources behind the research</h1><p>Primary research supports mathematical comparisons. Historical and esoteric material suggests questions; a patent records a proposal, and a forum post records discourse. Neither supplies an unproved physical premise.</p></header><section class="r29-source-controls" aria-label="Filter source records"><label>Search sources<input type="search" id="r30-source-search" placeholder="Try Newton, Wilson, Jung…"></label><label>Source collection<select id="r30-source-area"><option value="all">All sources</option><option value="historical">Historical and cultural</option><option value="modern">Modern technical research</option></select></label><button type="button" id="r30-source-reset">Reset</button></section><p role="status" id="r30-source-count">${arr(D.survey).length} reading records.</p><section id="r30-source-cards" class="r29-grid">${sourceCards()}</section>`;
  }
  function proof() {
    return `<header class="r22-page-head"><p class="rc-kicker">No defensible proof-completion percentage</p><h1>What remains to be established</h1><p>${esc(D.scope_statement)}</p></header>${arr(D.obligations).length ? `<div class="r29-grid">${D.obligations.map(row => `<article class="rc-result r30-card"><h2>${esc(row.name ?? row.title)}</h2><p><strong>${esc(row.status)}</strong></p><p>${esc(row.missing ?? row.detail ?? '')}</p></article>`).join('')}</div>` : `<p>Read the current roadmap for the outstanding state, scaling and continuum obligations.</p>`}<p>${link('round30-roadmap','Inspect the next planned tests →')}</p><p>Three reviewed investigations are a count of this cycle's work. They cannot be converted into a fraction of the continuum existence and mass-gap proof.</p>`;
  }
  // Exact rational arithmetic renders the admitted AT2 certificate, not a spectrum.
  const gcd = (a,b) => { a=a<0n?-a:a; b=b<0n?-b:b; while(b){[a,b]=[b,a%b];} return a; };
  function rational(n,d=1n) {
    n=BigInt(n); d=BigInt(d); if(!d)throw new Error('A fraction denominator cannot be zero.');
    if(d<0n){n=-n;d=-d;} const g=gcd(n,d); return {n:n/g,d:d/g};
  }
  const add=(a,b)=>rational(a.n*b.d+b.n*a.d,a.d*b.d), sub=(a,b)=>rational(a.n*b.d-b.n*a.d,a.d*b.d), mul=(a,b)=>rational(a.n*b.n,a.d*b.d), div=(a,b)=>rational(a.n*b.d,a.d*b.n);
  const less=(a,b)=>a.n*b.d<b.n*a.d, abs=a=>rational(a.n<0n?-a.n:a.n,a.d), str=a=>a.d===1n?String(a.n):`${a.n}/${a.d}`;
  function parseRational(value) {
    const raw=String(value).trim(); if(!raw||raw.length>120)throw new Error('Enter a decimal, scientific notation, or a short fraction.');
    const pieces=raw.split('/'); if(pieces.length===2)return div(parseRational(pieces[0]),parseRational(pieces[1]));
    if(pieces.length!==1)throw new Error('Use one slash for a fraction.');
    const normalized=raw.replace(/^([+-]?)\./,'$10.');
    const match=normalized.match(/^([+-]?)(\d+)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/);
    if(!match)throw new Error('Enter a valid decimal, scientific notation, or fraction.');
    const exponent=Number(match[4]||0)-(match[3]||'').length;
    if(!Number.isInteger(exponent)||Math.abs(exponent)>200)throw new Error('The display supports decimal exponents between -200 and 200.');
    let n=BigInt(match[2]+(match[3]||'')); if(match[1]==='-')n=-n;
    return exponent>=0?rational(n*10n**BigInt(exponent)):rational(n,10n**BigInt(-exponent));
  }
  function spectralCertificate(alphaValue='1',tauValue='1e-8') {
    const alpha=parseRational(alphaValue),tau=parseRational(tauValue),zero=rational(0);
    if(!less(zero,alpha))throw new Error('Alpha must be a positive physical energy coefficient.');
    if(less(rational(1,100000000),abs(tau)))throw new Error('Tau is outside the reviewed interval: |tau| ≤ 10⁻⁸.');
    const a=rational(1,16),L=rational(8),c=rational(3),b=rational(49),slo=rational(61999,250000),shi=rational(63,250),ulo=rational(187,250),uhi=rational(94,125);
    const B=add(rational(36),mul(rational(98),abs(tau)));
    const window=div(sub(mul(L,slo),uhi),sub(L,a));
    const tangent=sub(div(mul(rational(2),slo),c),div(uhi,mul(c,c))),cauchy=div(mul(slo,slo),uhi);
    const lower=less(tangent,cauchy)?cauchy:tangent;
    const upper=div(add(sub(B,mul(add(mul(rational(2),b),a),ulo)),mul(add(mul(b,b),mul(rational(2),mul(a,b))),shi)),mul(a,mul(b,b)));
    return {alpha:str(alpha),tau:str(tau),window_physical_energy:[str(mul(alpha,a)),str(mul(alpha,L))],unnormalized_window_mass_lower:str(window),inverse_energy_form_interval:[str(div(lower,alpha)),str(div(upper,alpha))],dimensionless_inverse_interval:[str(lower),str(upper)],tangent_lower_dimensionless:str(tangent),second_energy_moment_upper:str(mul(mul(alpha,alpha),B)),actual_response_evaluated:false,physical_susceptibility_claim:false};
  }
  function calculatorAdmitted() {
    const loop=loops.find(row=>row.id===D.calculator?.loop_id);
    return reviewed(loop)&&loop.gate_sha256===D.calculator?.gate_sha256;
  }
  function approximation(value) {
    const q=parseRational(value),number=Number(q.n)/Number(q.d);
    return Number.isFinite(number)?number.toPrecision(9):'outside decimal display range';
  }
  function calculatorOutput(alpha='1',tau='1e-8') {
    const out=spectralCertificate(alpha,tau), row=(name,exact,approx,unit)=>`<tr><th scope="row">${esc(name)}</th><td>${esc(exact)}</td><td>${esc(approx)}</td><td>${esc(unit)}</td></tr>`;
    return `<p>α = <strong>${esc(out.alpha)}</strong>; τ = <strong>${esc(out.tau)}</strong>. Fractions below are exact for these entered values. Decimal displays are rounded, not additional interval endpoints.</p><div class="r30-table-wrap" tabindex="0" role="region" aria-label="Exact spectral certificate values"><table class="r30-certificate-table"><thead><tr><th scope="col">Certified quantity</th><th scope="col">Exact bound</th><th scope="col">Decimal display ≈</th><th scope="col">Units</th></tr></thead><tbody>${row('Spectral energy window',out.window_physical_energy.join(' to '),out.window_physical_energy.map(approximation).join(' to '),'chosen energy unit')}${row('Unnormalized mass in the window ≥',out.unnormalized_window_mass_lower,approximation(out.unnormalized_window_mass_lower),'dimensionless mass')}${row('Reduced inverse-energy form ≥',out.inverse_energy_form_interval[0],approximation(out.inverse_energy_form_interval[0]),'inverse energy')}${row('Reduced inverse-energy form ≤',out.inverse_energy_form_interval[1],approximation(out.inverse_energy_form_interval[1]),'inverse energy')}${row('Second energy moment ≤',out.second_energy_moment_upper,approximation(out.second_energy_moment_upper),'energy squared')}</tbody></table></div><p class="r29-muted">The window mass is not normalized probability. The inverse-energy form is ⟨χ, H<sub>phys</sub><sup>−1</sup>χ⟩ on the physical vacuum-orthogonal sector; it is not an established static susceptibility.</p>`;
  }
  function calculator() {
    if(!calculatorAdmitted())return '<header class="r22-page-head"><h1>Certificate unavailable</h1><p>The calculator requires the matching AT2 review.</p></header>';
    const figure=D.figure?.gate_sha256===D.calculator.gate_sha256&&safePath(D.figure?.url);
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday spectral-window certificate · AT2</p><h1>Explore the certified bounds.</h1><p>Change the positive energy coefficient α and the signed coupling τ inside the reviewed numerical cap. This calculator evaluates bounds; it does not compute the AQ spectrum or its actual response.</p></header><section class="r30-calculator" aria-labelledby="r30-calculator-input-title"><h2 id="r30-calculator-input-title">Physical scale and coupling</h2><form id="r30-certificate-form"><div class="r30-calc-inputs"><label>α · positive energy coefficient<input id="r30-alpha" type="text" inputmode="decimal" value="1" aria-describedby="r30-alpha-help" required><small id="r30-alpha-help">In your chosen energy unit. Decimal, scientific notation or fraction.</small></label><label>τ · signed dimensionless coupling<input id="r30-tau" type="text" inputmode="decimal" value="1e-8" aria-describedby="r30-tau-help" required><small id="r30-tau-help">−10⁻⁸ ≤ τ ≤ 10⁻⁸. Both signs are covered.</small></label></div><div class="r30-calc-actions"><button type="submit">Calculate bounds</button><button type="button" data-r30-preset="1e-8">Positive cap</button><button type="button" data-r30-preset="-1e-8">Negative cap</button><button type="button" data-r30-preset="0">Zero coupling</button></div></form><p id="r30-calc-error" role="alert"></p><div id="r30-calc-output" aria-live="polite">${calculatorOutput()}</div><details><summary>Fixed choices and proof source</summary><p>The reviewed choices are L = 8, c = 3 and b = 49. The gap threshold is α/16. The fixed conservative moment bounds are used throughout; changing τ changes the second-moment and inverse-form upper certificates through 36 + 98|τ|.</p>${sources([D.calculator.source,D.calculator.gate_path])}<p>${link('round30-at2','Read the complete AT2 result →')}</p></details></section>${figure?`<figure class="r30-fixture-figure"><img src="${esc(figure)}" alt="Three equal-moment control measures and their different Euclidean correlations" loading="lazy"><figcaption>${esc(D.figure.caption)}<p>${esc(D.figure.accuracy)}</p></figcaption></figure>`:''}${scope()}`;
  }
  function render(value = 'home') {
    const route = normalizeRoute(value);
    if (delegatedCurrent.has(route)) {
      return prior.render(value).replace(/<nav class="rc-nav"[^>]*>[\s\S]*?<\/nav>/, nav(route));
    }
    if (!own.has(route)) return `<aside class="r30-current-banner"><strong>Current research: Round30.</strong> ${link('round30-results','Latest reviewed results')} · ${link('hnm-findings','Current Hruday / HNM catalog')}<span>This earlier view retains its original scope.</span></aside>` + prior.render(value);
    const loop = byRoute.get(route);
    const body = loop ? loopPage(loop) : route === 'drafts' ? drafts() : route === 'round30-results' ? results() : route === 'round30-roadmap' ? roadmap() : route === 'round30-sources' ? survey() : route === 'round30-proof' ? proof() : route === 'round30-calculator' ? calculator() : home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r29 r30">${nav(route)}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · ${esc(D.author)}</strong>${link('round30-proof','Proof obligations')}${link('round30-sources','Source ledger')}${link('round29','Round29 archive')}${link('all-results','Earlier rounds')}</footer></div>`;
  }
  let networkObserver;
  function afterRender() {
    networkObserver?.disconnect();
    const route = normalizeRoute(location.hash.replace(/^#research\/?/, '') || 'home');
    if(route === 'research-network') {
      prior.afterRender();
      const map=document.getElementById('r29-network-map');
      if(!map)return;
      const center=()=>{const scroller=map.querySelector('.r29-map-scroll'),selected=map.querySelector('.r29-map-node[aria-pressed="true"]');if(scroller&&selected){scroller.scrollLeft=Math.max(0,selected.offsetLeft+selected.offsetWidth/2-scroller.clientWidth/2);scroller.scrollTop=Math.max(0,selected.offsetTop+selected.offsetHeight/2-scroller.clientHeight/2);}};
      if(!/(?:\?|&)node=/.test(location.hash)) {
        const latest=[...loops].reverse().find(reviewed),node=arr(D.network?.nodes).find(row=>row.route==='round30-'+latest?.id);
        if(node)Array.from(document.querySelectorAll('[data-r29-node]')).find(button=>button.getAttribute('data-r29-node')===String(node.id))?.click();
      }
      center();
      if(window.MutationObserver){networkObserver=new window.MutationObserver(center);networkObserver.observe(map,{childList:true});}
      return;
    }
    if (!own.has(route)) return prior.afterRender();
    window.ResearchJourney?.cleanup?.();
    const titles = {home:'Hruday research home',drafts:'Complete Hruday draft', 'round30-results':'Round30 results','round30-roadmap':'Next research questions','round30-sources':'Round30 source ledger','round30-proof':'Open proof obligations','round30-calculator':'Hruday spectral certificate calculator'};
    document.title = `${byRoute.get(route)?.title ?? titles[route] ?? 'Hruday Research'} · Yang–Mills Workbench`;
    if(route === 'round30-calculator') {
      const get=name=>document.getElementById(name),form=get('r30-certificate-form'),alpha=get('r30-alpha'),tau=get('r30-tau'),output=get('r30-calc-output'),error=get('r30-calc-error');
      if(!form||!alpha||!tau||!output||!error)return;
      const update=()=>{try{output.innerHTML=calculatorOutput(alpha.value,tau.value);error.textContent='';}catch(problem){output.innerHTML='';error.textContent=problem.message;}};
      form.addEventListener('submit',event=>{event.preventDefault();update();});
      form.addEventListener('click',event=>{const button=event.target.closest?.('[data-r30-preset]');if(button){tau.value=button.getAttribute('data-r30-preset');update();}});
      return;
    }
    if (route !== 'round30-sources') return;
    const get = name => document.getElementById(name), search = get('r30-source-search'), area = get('r30-source-area'), cards = get('r30-source-cards'), count = get('r30-source-count'), reset = get('r30-source-reset');
    if (!search || !area || !cards || !count || !reset) return;
    const update = () => { cards.innerHTML = sourceCards(search.value,area.value); count.textContent = `${filterSources(search.value,area.value).length} of ${arr(D.survey).length} reading records shown.`; };
    search.addEventListener('input',update); area.addEventListener('change',update);
    reset.addEventListener('click',() => { search.value = ''; area.value = 'all'; update(); search.focus(); });
    update();
  }
  window.ResearchRound30 = {render,afterRender,normalizeRoute,counts,reviewed,safePath,safeURL,source,filterSources,sourceCards,spectralCertificate,calculatorOutput,calculatorAdmitted,data:D};
  window.ResearchObservatory = {...prior,render,afterRender};
})();
