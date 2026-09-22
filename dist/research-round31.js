/* Additive Round31 reader. Scientific wording comes from reviewed source data. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND31_DATA;
  if (!prior || !D) return;
  const arr = value => Array.isArray(value) ? value : [];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const idOK = value => /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(String(value));
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
  const link = (route, label) => idOK(route) ? `<a href="#research/${route}">${esc(label)}</a>` : esc(label);
  const source = (item, label) => {
    const row = typeof item === 'string' ? {path:item} : item ?? {};
    const raw = row.url ?? row.path ?? '', remote = safeURL(raw), path = safePath(raw);
    const href = remote || (path ? 'https://github.com/occult-kranti/yang_mills_workbench/blob/main/' + path : '');
    const text = label ?? row.title ?? row.label ?? raw;
    return href ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(text)} <span aria-hidden="true">↗</span></a>` : esc(text);
  };
  const download = (path, label) => safePath(path) ? `<a href="${esc(safePath(path))}" download>${esc(label)}</a>` : esc(label);
  const list = values => arr(values).length ? `<ul>${values.map(value => `<li>${esc(value)}</li>`).join('')}</ul>` : '';
  const evidence = values => `<ul class="r29-evidence">${arr(values).map(value => `<li>${source(value)}</li>`).join('')}</ul>`;
  const loops = arr(D.loops), ids = ['at4','at5','at6'];
  const reviewed = loop => loop?.stage === 'reviewed' && ids.includes(loop.id) &&
    /^[a-f0-9]{64}$/.test(String(loop.gate_sha256)) &&
    loop.gate_path === `research/round31/advisor/${loop.id}-gate.json` &&
    typeof loop.accepted === 'string' && !!loop.accepted.trim() &&
    typeof loop.title === 'string' && !!loop.title.trim() &&
    arr(loop.limitations).length > 0 &&
    /^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])/.test(String(loop.verdict));
  const counts = () => ({requested:3, completed:loops.filter(reviewed).length});
  const complete = () => D.schema === 'hnm-round31-presentation-v1' && loops.length === 3 &&
    loops.every((loop,index) => reviewed(loop) && loop.id === ids[index] && loop.sequence === index + 1) &&
    D.progress?.completed === 3 && D.progress?.requested === 3 && D.progress?.cycle_complete === true;
  const byRoute = new Map(loops.filter(loop => ids.includes(loop.id)).map(loop => ['round31-' + loop.id,loop]));
  const own = new Set(['home','round31','round31-results','round31-roadmap','round31-sources','round31-calculator','drafts','research-network','hnm-findings',...ids.map(id => 'round31-' + id)]);
  function normalizeRoute(value='home') {
    let route=String(value||'home').split('?')[0];
    if(route==='round31' && location.hash.startsWith('#research/round31/')) route=location.hash.slice('#research/'.length).split('?')[0];
    if(route.startsWith('round31/')) {
      const tail=route.slice('round31/'.length);
      route={home:'home',results:'round31-results',loops:'round31-results',roadmap:'round31-roadmap',sources:'round31-sources',calculator:'round31-calculator'}[tail] ?? 'round31-'+tail;
    }
    return route==='round31' ? 'home' : route;
  }
  function nav(route) {
    const entries=[['home','Home'],['round31-results','Latest results'],['round31-calculator','Error calculator'],['hnm-findings','HNM catalog'],['research-network','Research network'],['drafts','Draft and addendum'],['round31-roadmap','Next questions'],['round31-sources','Sources'],['round30-results','Round30 archive']];
    return `<nav class="rc-nav r31-nav" aria-label="Research navigation">${entries.map(([target,title])=>`<a href="#research/${target}"${target===route?' aria-current="page"':''}>${title}</a>`).join('')}</nav>`;
  }
  function badge(loop) {
    const limited=/limited|insufficient|reject|fail/.test(loop.verdict);
    return `<span class="r29-badge r29-badge-${limited?'limited':'accepted'}">${esc(String(loop.verdict).replaceAll('_',' '))}</span>`;
  }
  function scope() {
    return `<aside class="r29-scope r31-scope"><p class="rc-kicker">Applicability</p><p>${esc(D.scope_statement)}</p><p>A fixed-lattice patterned subfamily must be distinguished from the general selected reference and from the four-dimensional continuum problem. Each result below names its model. Hruday / HNM aliases identify project records; established mathematics retains its attribution and scientific priority is unverified.</p></aside>`;
  }
  function incomplete() {
    return `<header class="r22-page-head"><p class="rc-kicker">Round31 · Review unavailable</p><h1>The complete review is not available.</h1><p>The three required source-bound reviews are incomplete in this reader. No Round31 scientific findings are displayed.</p><p>${link('round30-results','Read the preserved Round30 results →')}</p></header>`;
  }
  function card(loop) {
    return `<article class="rc-result r31-card"><div class="r29-card-top"><p class="rc-kicker">Investigation ${loop.sequence} · ${esc(loop.id.toUpperCase())}</p>${badge(loop)}</div><h2>${esc(loop.title)}</h2><p>${esc(loop.summary)}</p><p class="r29-card-limit"><strong>Limit:</strong> ${esc(loop.limitations[0])}</p><p>${link('round31-'+loop.id,'Derivation, scope and review →')}</p></article>`;
  }
  function home() {
    return `<header class="r29-home-hero"><div><p class="rc-kicker">Hruday N M (BUNZEEY) · Round31</p><h1>Read the result.<br>Check the conditions.</h1><p class="r29-home-lede">${esc(D.summary)}</p><div class="r29-home-actions">${link('round31-results','Read the latest results →')}${link('drafts','Read the manuscript →')}</div></div><aside class="r29-home-status"><p class="rc-kicker">This research cycle</p><p class="r29-home-count">3<span> / 3</span></p><h2>Investigations reviewed</h2><p>A count of completed investigations, not a percentage of the Yang–Mills proof.</p>${link('round31-roadmap','Next questions →')}</aside></header>${scope()}<section aria-labelledby="r31-results-title"><h2 id="r31-results-title">Results with explicit limits</h2><div class="r29-grid">${loops.map(card).join('')}</div></section><section class="r29-reader-paths" aria-label="Reading paths"><a href="#research/research-network"><p class="rc-kicker">Trace</p><h2>Claims and dependencies</h2><p>Separate proved dependencies, proposed transfers and source comparisons.</p></a><a href="#research/round31-sources"><p class="rc-kicker">Inspect</p><h2>What was actually read</h2><p>Check selected passages, provenance and inaccessible leads.</p></a><a href="#research/drafts"><p class="rc-kicker">Read</p><h2>Draft and addendum</h2><p>The new continuation and the preserved Draft03 remain separately available.</p></a></section>`;
  }
  function results() {
    return `<header class="r22-page-head"><p class="rc-kicker">Round31 · Three reviewed investigations</p><h1>Latest results</h1><p>Every conclusion belongs to its stated model and error budget. A limited or insufficient outcome remains part of the record.</p></header><div class="r29-grid">${loops.map(card).join('')}</div>${scope()}`;
  }
  function loopPage(loop) {
    return `<header class="r22-page-head"><p class="rc-kicker">Round31 · ${esc(loop.contribution_id)}</p><h1>${esc(loop.title)}</h1>${badge(loop)}<p>${esc(loop.summary)}</p></header><section class="r31-conclusion"><h2>Reviewed conclusion</h2><p>${esc(loop.accepted)}</p><p><strong>Model:</strong> ${esc(loop.model)}</p></section><section class="r31-section"><h2>How the result follows</h2><ol>${arr(loop.derivation_steps).map(step=>`<li>${esc(step)}</li>`).join('')}</ol></section><section class="r31-section"><h2>What this enables</h2>${list(loop.applications)}</section><section class="r31-section r31-limitations"><h2>Limitations</h2>${list(loop.limitations)}</section><section class="r31-section"><h2>Evidence and skeptical review</h2>${evidence(loop.sources)}<details class="r31-source-inventory"><summary>Full source inventory · ${arr(loop.all_sources).length} files</summary>${evidence(loop.all_sources)}</details><details><summary>Review binding</summary><p class="r31-hash">${esc(loop.gate_sha256)}</p></details></section>${scope()}`;
  }
  function drafts() {
    const add=D.addendum ?? {}, old=D.previous_draft ?? {}, url=safePath(add.url);
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday N M (BUNZEEY)</p><h1>Research draft and continuation</h1><p>Read each statement alongside its derivation, fixed model, error budget and limitations.</p></header><section class="r29-draft-feature"><div><p class="rc-kicker">Round31 addendum</p><h2>${esc(add.title)}</h2><div class="r29-home-actions">${url?download(add.url,'Download the Round31 addendum ↓'):source(add.path,'Read the Round31 addendum')}${source(add.path,'Addendum source record')}</div></div><aside><strong>Hruday N M</strong><span>BUNZEEY</span><hr><p>Human author and project direction. AI-assisted derivation and model-agent review; no external human peer review is claimed.</p></aside></section><section class="r31-section"><h2>Preserved Draft03</h2><p>The preceding manuscript retains its original Round30 scope and bytes.</p><p>${download(old.url,'Download Draft03 · through Round30 ↓')} · ${source(old.path,'Draft03 source')}</p><p>${link('round30-results','Read the Round30 checkpoint →')}</p></section>${url&&/\.pdf$/i.test(url)?`<details class="drafts-reader"><summary>Read the addendum in this page</summary><iframe title="Round31 research addendum" src="${esc(url)}" loading="lazy"></iframe></details>`:''}${scope()}`;
  }
  function roadmap() {
    return `<header class="r22-page-head"><p class="rc-kicker">Planning after the three reviews</p><h1>Next research questions</h1><p>${esc(D.roadmap?.summary ?? D.roadmap?.ranking_basis ?? '')}</p></header><p class="r31-plan-notice">These follow-ups are planning records, separate from the three investigations in this cycle.</p><div class="r29-grid">${arr(D.roadmap?.goals).map((goal,index)=>`<article class="rc-result r31-card"><p class="rc-kicker">Priority ${esc(goal.rank ?? index+1)} · ${esc(goal.id)}</p><h2>${esc(goal.title ?? goal.target)}</h2><p><strong>${esc(String(goal.status ?? 'planned_not_executed').replaceAll('_',' '))}</strong></p><p>${esc(goal.target ?? '')}</p>${goal.missing_premise?`<p><strong>Missing step:</strong> ${esc(goal.missing_premise)}</p>`:''}${goal.proposed_first_loop_test?`<details><summary>Proposed first test</summary><p>${esc(goal.proposed_first_loop_test)}</p></details>`:''}${list(goal.limitations)}</article>`).join('')}</div><p>${source('research/round31/advisor/roadmap.json','Complete roadmap')}</p>`;
  }
  function filterSources(query='',area='all') {
    const needle=String(query).trim().toLowerCase();
    return arr(D.survey).filter(row=>(area==='all'||row.area===area)&&[row.id,row.title,row.authors,row.author,row.provenance,row.reading_depth,row.use,row.limits,row.section,...arr(row.passages)].join(' ').toLowerCase().includes(needle));
  }
  function sourceCards(query='',area='all') {
    const rows=filterSources(query,area);
    return rows.length ? rows.map(row=>`<article class="rc-result r31-source"><p class="rc-kicker">${esc(row.area)} · ${esc(row.id)}</p><h2>${source(row,row.title)}</h2><p class="r29-muted">${esc(row.provenance)}${row.date?' · '+esc(row.date):''}</p><p><strong>Reading depth:</strong> ${esc(row.reading_depth || 'See the source ledger for the recorded depth.')}</p>${row.use?`<p><strong>Use here:</strong> ${esc(row.use)}</p>`:''}${row.limits?`<p><strong>Limits:</strong> ${esc(row.limits)}</p>`:''}<details><summary>Passages and access record</summary>${list(row.passages)}${row.date_note?`<p>${esc(row.date_note)}</p>`:''}${row.overlap?`<p>${esc(row.overlap)}</p>`:''}${list(row.access_failures)}${row.validation_status?`<p>${esc(row.validation_status)}</p>`:''}<p>${source(row.ledger,'Complete source ledger')}</p></details></article>`).join('') : '<p class="r29-empty">No source records match.</p>';
  }
  function survey() {
    const areas=[...new Set(arr(D.survey).map(row=>row.area))];
    return `<header class="r22-page-head"><p class="rc-kicker">Selected sources and reading limits</p><h1>Sources behind the work</h1><p>Historical and mystical material can motivate questions. A patent records a proposal; government custody records provenance. Neither replaces a tested model or a mathematical premise.</p></header><section class="r29-source-controls" aria-label="Filter source records"><label>Search sources<input id="r31-source-search" type="search" placeholder="Search title, passage or reading depth"></label><label>Research lens<select id="r31-source-area"><option value="all">All lenses</option>${areas.map(area=>`<option value="${esc(area)}">${esc(area)}</option>`).join('')}</select></label><button id="r31-source-reset" type="button">Reset</button></section><p id="r31-source-count" role="status">${arr(D.survey).length} source records.</p><section class="r29-grid" id="r31-source-cards">${sourceCards()}</section>`;
  }
  function filterFindings(query='',round='all') {
    const needle=String(query).trim().toLowerCase();
    return arr(D.registry?.contributions).filter(row=>(round==='all'||String(row.round)===String(round))&&[row.id,row.legacy_id,row.display_name,row.title,row.summary,row.application,row.limitation,row.model].join(' ').toLowerCase().includes(needle));
  }
  function findingCards(query='',round='all') {
    const rows=filterFindings(query,round);
    return rows.length?rows.map(row=>`<article class="rc-result r31-card"><p class="rc-kicker">${esc(row.id)} · Round ${esc(row.round)}</p><h2>${esc(row.display_name ?? row.title)}</h2><p><strong>${esc(String(row.status ?? 'Recorded').replaceAll('_',' '))}</strong></p><p>${esc(row.summary)}</p>${row.model?`<p><strong>Model:</strong> ${esc(row.model)}</p>`:''}${row.limitation?`<p><strong>Limits:</strong> ${esc(row.limitation)}</p>`:''}<details><summary>Application and original sources</summary><p>${esc(row.application)}</p>${evidence(row.source_paths)}<p>${esc(row.priority_status ?? 'Scientific priority is unverified.')}</p></details>${row.route?`<p>${link(row.route,'Read the complete result →')}</p>`:''}</article>`).join(''):'<p>No HNM records match.</p>';
  }
  function catalog() {
    const rounds=[...new Set(arr(D.registry?.contributions).map(row=>row.round))].sort((a,b)=>b-a);
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday / HNM project records</p><h1>Contributions and their limits</h1><p>The current catalog adds this cycle's records to the preserved Draft03 entries. Names locate work; they do not establish scientific priority or rename prior theorems.</p></header><section class="r29-source-controls" aria-label="Search the HNM catalog"><label>Search contributions<input id="r31-finding-search" type="search" placeholder="Try HNM-C-AT4, a model, or a limitation"></label><label>Round<select id="r31-finding-round"><option value="all">All rounds</option>${rounds.map(round=>`<option value="${esc(round)}">Round ${esc(round)}</option>`).join('')}</select></label><button id="r31-finding-reset" type="button">Reset</button></section><p role="status" id="r31-finding-count">${arr(D.registry?.contributions).length} records.</p><section class="r29-grid" id="r31-finding-cards">${findingCards()}</section>`;
  }
  function calculatorAdmitted() {
    const loop=loops.find(row=>row.id==='at5'),config=D.calculator;
    return complete() && reviewed(loop) && /^accepted(?:$|[_ -])/.test(loop.verdict) &&
      config?.loop_id==='at5' && config.formula_id==='zero-selected-reference-comparison-gap-six' &&
      config.gate_sha256===loop.gate_sha256 && config.gate_path===loop.gate_path &&
      config.record?.actual_aq_enclosure===true && config.record?.target_met===true;
  }
  function previewNumber(value,name) {
    if(typeof value!=='string'&&typeof value!=='number')throw new Error(`${name}: enter a finite number or fraction.`);
    const raw=String(value).trim();
    if(!raw||raw.length>120)throw new Error(`${name}: enter a short finite number.`);
    const part='[+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+-]?\\d+)?';
    if(!new RegExp(`^${part}(?:/${part})?$`).test(raw))throw new Error(`${name}: invalid number or fraction.`);
    const pieces=raw.split('/'),numerator=Number(pieces[0]),denominator=pieces.length===2?Number(pieces[1]):1;
    if(!Number.isFinite(numerator)||!Number.isFinite(denominator)||denominator===0)throw new Error(`${name}: a finite value and nonzero denominator are required.`);
    const number=numerator/denominator;
    if(!Number.isFinite(number))throw new Error(`${name}: outside the browser's finite numerical range.`);
    const mantissa=pieces[0].split(/[eE]/)[0];
    if(number===0&&/[1-9]/.test(mantissa))throw new Error(`${name}: underflow is outside this preview's numerical range.`);
    return number;
  }
  function referencePreview({tau='1e-14',s='1',L='1e9',alpha='1',hbar='1',E_star='1',lattice_spacing='1',selected=['0','0','0']}={}) {
    if(!Array.isArray(selected)||selected.length!==3||selected.some(value=>previewNumber(value,'Selected coefficient')!==0))throw new Error('Only selected coefficients (0, 0, 0) belong to this calculator model.');
    const p=Object.fromEntries(Object.entries({tau,s,L,alpha,hbar,E_star,lattice_spacing}).map(([key,value])=>[key,previewNumber(value,key)]));
    if(Math.abs(p.tau)>1e-8)throw new Error('The reviewed comparison domain requires |tau| ≤ 10⁻⁸.');
    for(const key of ['s','L','alpha','hbar','E_star','lattice_spacing'])if(!(p[key]>0))throw new Error(`${key} must be positive.`);
    const D=2*Math.sqrt(49*Math.abs(p.tau)/3),k=49*Math.abs(p.tau)/4;
    const logRatio=Math.log(p.L)-Math.log(p.s);
    const logTerm=logRatio>0?2*logRatio+Math.log1p(Math.exp(-2*logRatio)):Math.log1p(Math.exp(2*logRatio));
    const costs={state:D,centering:D*D,real_time_comparison:k*p.s/Math.PI*logTerm,Poisson_tail:(.5+D/2)*2*p.s/(Math.PI*p.L)};
    // At tau=0 the model is exactly the free reference; the comparison filter is unnecessary.
    if(p.tau===0)for(const key of Object.keys(costs))costs[key]=0;
    const model_error=Object.values(costs).reduce((sum,value)=>sum+value,0),reference=Math.exp(-3*p.s)/4;
    const physical_Euclidean_time=p.hbar*p.s/p.alpha,physical_real_time_cutoff=p.hbar*p.L/p.alpha;
    if(![D,k,model_error,reference,physical_Euclidean_time,physical_real_time_cutoff,...Object.values(costs)].every(Number.isFinite))throw new Error('These parameters exceed the browser preview numerical range.');
    if(physical_Euclidean_time<=0||physical_real_time_cutoff<=0)throw new Error('The physical time underflows the browser preview numerical range.');
    return {parameters:p,D,k,costs,model_error,reference,approximate_interval:[Math.max(0,reference-model_error),reference+model_error],physical_Euclidean_time,physical_real_time_cutoff,normalized_time:p.s/8,zero_reference:p.tau===0,rigorous:false,arithmetic_error_certified:false};
  }
  const decimal=value=>{
    const raw=String(value ?? '');
    if(!/^[+-]?\d+(?:\/\d+)?$/.test(raw)||raw.length>2000)return 'See the exact rational record';
    const parts=raw.split('/'),number=Number(parts[0])/Number(parts[1]??'1');
    return Number.isFinite(number)?number.toPrecision(12):'See the exact rational record';
  };
  function recordedCertificate() {
    const record=D.calculator.record;
    const labels={state:'State comparison',centering:'Ground centering',real_time_comparison:'Real-time comparison',Poisson_tail:'Poisson tail',arithmetic:'Arithmetic'};
    return `<section class="r31-conclusion" aria-labelledby="r31-recorded-title"><p class="rc-kicker">Frozen reviewed output · AT5</p><h2 id="r31-recorded-title">Recorded datum and certified absolute error</h2><p>Datum <strong data-r31-recorded-datum>${esc(decimal(record.certified_datum))}</strong> with error radius <strong data-r31-recorded-radius>${esc(decimal(record.certified_absolute_error))}</strong>. These decimals are rounded displays of the exact rational record below.</p><p>The radius bounds the absolute error of the exported point value. The full interval width is twice the radius; it is not the point-error tolerance.</p><p>Fixed record: τ = ${esc(record.parameters.tau)}, s = ${esc(record.parameters.s)}, L = ${esc(record.parameters.L)}; selected coefficients = (0, 0, 0).</p><div class="r31-table-wrap"><table><thead><tr><th scope="col">Error contribution</th><th scope="col">Rounded display</th></tr></thead><tbody>${Object.entries(record.costs).map(([key,value])=>`<tr><th scope="row">${esc(labels[key]??key)}</th><td>${esc(decimal(value))}</td></tr>`).join('')}</tbody></table></div><details><summary>Exact rational datum, error and enclosure</summary><dl class="r31-exact"><dt>Datum</dt><dd>${esc(record.certified_datum)}</dd><dt>Certified absolute error radius</dt><dd>${esc(record.certified_absolute_error)}</dd><dt>Interval width</dt><dd>${esc(record.interval_width)}</dd><dt>Actual correlation enclosure</dt><dd>[${esc(record.actual_C_interval?.lower)}, ${esc(record.actual_C_interval?.upper)}]</dd></dl></details><p>The free reference remains inside this enclosure. This certifies an actual correlation bound in the specified patterned subfamily; it does not resolve an interaction-induced shift, establish uniqueness, evaluate an inverse response, or solve the continuum problem.</p>${evidence([D.calculator.result_path,D.calculator.source,D.calculator.gate_path])}</section>`;
  }
  function previewOutput(parameters={}) {
    const out=referencePreview(parameters),fmt=value=>value.toPrecision(9);
    return `<p class="r31-preview-notice"><strong>Floating-point preview only.</strong> These calculations do not include a certified arithmetic error. They do not replace the recorded rational certificate.</p><p>${out.zero_reference?'At exactly τ = 0 the model is the free reference. Its model-comparison error is zero; displayed exponentials still have ordinary browser rounding.':'The comparison applies only to the zero-selected patterned subfamily.'}</p><div class="r31-table-wrap"><table><thead><tr><th scope="col">Preview quantity</th><th scope="col">Approximate value</th></tr></thead><tbody><tr><th scope="row">Free reference exp(−3s)/4</th><td>${fmt(out.reference)}</td></tr>${Object.entries(out.costs).map(([key,value])=>`<tr><th scope="row">${esc(key.replaceAll('_',' '))}</th><td>${fmt(value)}</td></tr>`).join('')}<tr><th scope="row">Sum of model-error terms</th><td>${fmt(out.model_error)}</td></tr></tbody></table></div><p>Approximate enclosure: [${fmt(out.approximate_interval[0])}, ${fmt(out.approximate_interval[1])}]. Physical Euclidean time t<sub>E</sub> = ℏs/α ≈ ${fmt(out.physical_Euclidean_time)}; normalized AQ time u = s/8 ≈ ${fmt(out.normalized_time)}.</p><p>The ${out.model_error<=1e-6?'model-error sum is below':'model-error sum exceeds'} 10⁻⁶ in this floating preview. Only the separately recorded preset has its full error certified here.</p>`;
  }
  function calculator() {
    if(!calculatorAdmitted())return `<header class="r22-page-head"><h1>Calculator review is unavailable.</h1><p>The AT5 calculator has no matching admitted source binding in this reader. No certified datum or explorer is displayed.</p></header>`;
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday reference-comparison calculator · AT5</p><h1>Inspect the error budget.</h1><p>The recorded certificate and the adjustable floating preview are shown separately. Selected coefficients remain fixed at (0, 0, 0); general selected references and uniform Wilson theory are outside this calculator.</p></header>${recordedCertificate()}<section class="r31-calculator" aria-labelledby="r31-preview-title"><h2 id="r31-preview-title">Explore a numerical preview</h2><form id="r31-preview-form"><div class="r31-calc-inputs"><label>τ · dimensionless coupling<input id="r31-tau" type="text" inputmode="decimal" value="1e-14" required><small>|τ| ≤ 10⁻⁸; selected coefficients fixed at zero.</small></label><label>s · dimensionless Euclidean time<input id="r31-s" type="text" inputmode="decimal" value="1" required><small>s = αt<sub>E</sub>/ℏ, strictly positive.</small></label><label>L · dimensionless real-time cutoff<input id="r31-L" type="text" inputmode="decimal" value="1e9" required><small>Proof-filter cutoff, strictly positive.</small></label></div><details><summary>Physical scale convention</summary><div class="r31-calc-inputs"><label>α · energy unit<input id="r31-alpha" type="text" inputmode="decimal" value="1" required></label><label>ℏ · action unit<input id="r31-hbar" type="text" inputmode="decimal" value="1" required></label><label>E* · comparison energy<input id="r31-E-star" type="text" inputmode="decimal" value="1" required></label><label>a · lattice spacing<input id="r31-lattice-spacing" type="text" inputmode="decimal" value="1" required></label></div><p>All scales must be positive. Changing units does not change the dimensionless coupling or establish a continuum limit.</p></details><div class="r31-calc-actions"><button type="submit">Update preview</button><button type="button" data-r31-preset="certified">Recorded design</button><button type="button" data-r31-preset="cap">Original coupling cap</button><button type="button" data-r31-preset="old-cutoff">Cutoff L = 10,000</button><button type="button" data-r31-preset="zero">Exact free reference</button></div></form><p id="r31-preview-error" role="alert"></p><div id="r31-preview-output" aria-live="polite">${previewOutput()}</div><details><summary>Formula and scope</summary><pre class="r31-formula">D = 2 sqrt(49 |τ| / 3)\nk = 49 |τ| / 4\nE = D + D² + (k s / π) log(1 + L²/s²)\n    + (1/2 + D/2) 2s/(π L)\nC₀(s) = exp(−3s)/4</pre><p>The five certified recorded costs include arithmetic separately. The explorer shows four model-comparison terms only. At exactly zero coupling it uses the exact free-reference branch.</p><p>${source(D.calculator.source,'Exact rational Python calculator')} · ${link('round31-at5','Derivation and skeptical review')}</p></details></section>${scope()}`;
  }
  const nodes=arr(D.network?.nodes), nodeById=new Map(nodes.map(node=>[String(node.id),node]));
  const relationNames={'proven-dependency':'Proved dependency','proposed-transfer':'Proposed transfer','review-selection':'Selected after review','source-dependency':'Source comparison','scope-boundary':'Scope boundary','recorded-equation':'Recorded equation'};
  const validEdges=()=>arr(D.network?.edges).filter(edge=>nodeById.has(String(edge.from))&&nodeById.has(String(edge.to))&&Object.hasOwn(relationNames,edge.type));
  const filterNodes=(query='')=>{const needle=String(query).toLowerCase().trim();return nodes.filter(node=>[node.id,node.title,node.kind,node.status,node.summary,node.model,...arr(node.hnm_aliases)].join(' ').toLowerCase().includes(needle));};
  const networkInitial=()=>String([...nodes].reverse().find(node=>node.route==='round31-at6')?.id ?? nodes[0]?.id ?? '');
  function networkCatalog(query='',selected=networkInitial()) {
    const found=filterNodes(query);
    return found.length?`<ul>${found.map(node=>`<li><button type="button" data-r31-node="${esc(node.id)}" aria-pressed="${String(node.id)===String(selected)}"><span>${esc(node.title)}</span><small>${esc(node.kind)} · ${esc(node.status)}</small></button></li>`).join('')}</ul>`:'<p>No entries match this search.</p>';
  }
  function networkDetails(selected=networkInitial()) {
    const node=nodeById.get(String(selected));
    if(!node)return '<p>Select a research or source entry.</p>';
    const edges=validEdges().filter(edge=>String(edge.from)===String(selected)||String(edge.to)===String(selected));
    return `<header><p class="rc-kicker">${esc(node.kind)} · ${esc(node.id)}</p><h2 id="r31-network-selected">${esc(node.title)}</h2><p><strong>${esc(node.status)}</strong></p></header>${node.model?`<p><strong>Model:</strong> ${esc(node.model)}</p>`:''}<p>${esc(node.summary)}</p>${node.detail?`<p>${esc(node.detail)}</p>`:''}${node.equation?`<pre><code>${esc(node.equation)}</code></pre>`:''}${evidence(node.sources)}${node.route?`<p>${link(node.route,'Read this record →')}</p>`:''}<h3>Direct relations · ${edges.length}</h3>${edges.length?`<ul class="r31-relations">${edges.map(edge=>{const outgoing=String(edge.from)===String(selected),other=nodeById.get(String(outgoing?edge.to:edge.from));return `<li><span class="r29-edge-label r29-edge-label-${edge.type}">${esc(relationNames[edge.type])}</span><p>${outgoing?'Outgoing to':'Incoming from'} <button type="button" data-r31-node="${esc(other.id)}">${esc(other.title)}</button></p>${edge.label?`<p>${esc(edge.label)}</p>`:''}${edge.detail?`<p>${esc(edge.detail)}</p>`:''}</li>`;}).join('')}</ul>`:'<p>No direct relations are recorded.</p>'}`;
  }
  function network() {
    return `<header class="r22-page-head"><p class="rc-kicker">${nodes.length} catalog entries · ${validEdges().length} relations</p><h1>Trace the research network</h1><p>Select a result or source to inspect its direct dependencies. Proposed transfers and source comparisons remain distinct from proved dependencies. Counts describe this index, not physical gauge links or the fraction of a proof completed.</p></header><section class="r29-source-controls" aria-label="Search the research network"><label>Search entries<input type="search" id="r31-network-search" placeholder="Try AT4, boundary, Hruday or a source"></label><button type="button" id="r31-network-reset">Reset</button></section><p role="status" id="r31-network-count">${nodes.length} entries.</p><div class="r29-network-layout"><aside class="r29-network-catalog"><h2>Research catalog</h2><div id="r31-network-catalog">${networkCatalog()}</div></aside><section class="r29-network-details" id="r31-network-details" aria-labelledby="r31-network-selected">${networkDetails()}</section></div>`;
  }
  function render(value='home') {
    const route=normalizeRoute(value);
    if(!own.has(route)) {
      const archived=prior.render(value).replace(/<aside class="r30-current-banner">[\s\S]*?<\/aside>/g,'').replace(/<div class="r29 r29-history-banner">[\s\S]*?<\/div>/g,'');
      return `<aside class="r31-current-banner"><strong>Archived research view.</strong> ${link('round31-results','Current Round31 results')}<span>This page retains its earlier scope and navigation.</span></aside>`+archived;
    }
    const loop=byRoute.get(route);
    const body=!complete()?incomplete():loop?loopPage(loop):route==='round31-results'?results():route==='drafts'?drafts():route==='round31-roadmap'?roadmap():route==='round31-sources'?survey():route==='round31-calculator'?calculator():route==='research-network'?network():route==='hnm-findings'?catalog():home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r29 r30 r31">${nav(route)}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · ${esc(D.author)}</strong>${link('round31-sources','Source ledger')}${link('round31-roadmap','Open questions')}${link('round30-results','Round30 archive')}</footer></div>`;
  }
  function afterRender() {
    const route=normalizeRoute(location.hash.replace(/^#research\/?/,'')||'home');
    if(!own.has(route))return prior.afterRender?.();
    window.ResearchJourney?.cleanup?.();
    document.title=`${complete()?(byRoute.get(route)?.title ?? ({home:'Hruday research home',drafts:'Draft and addendum','research-network':'Research network','hnm-findings':'HNM catalog','round31-results':'Round31 results','round31-sources':'Round31 sources','round31-calculator':'Hruday error calculator','round31-roadmap':'Next research questions'}[route]??'Round31')):'Round31 review unavailable'} · Yang–Mills Workbench`;
    if(!complete())return;
    const get=name=>document.getElementById(name);
    if(route==='round31-calculator'&&calculatorAdmitted()) {
      const form=get('r31-preview-form'),output=get('r31-preview-output'),error=get('r31-preview-error');
      const fields={tau:get('r31-tau'),s:get('r31-s'),L:get('r31-L'),alpha:get('r31-alpha'),hbar:get('r31-hbar'),E_star:get('r31-E-star'),lattice_spacing:get('r31-lattice-spacing')};
      if(!form||!output||!error||Object.values(fields).some(field=>!field))return;
      const update=()=>{try{output.innerHTML=previewOutput(Object.fromEntries(Object.entries(fields).map(([key,field])=>[key,field.value])));error.textContent='';}catch(problem){output.innerHTML='';error.textContent=problem.message;}};
      form.addEventListener('submit',event=>{event.preventDefault();update();});
      form.addEventListener('click',event=>{const preset=event.target.closest?.('[data-r31-preset]')?.getAttribute('data-r31-preset');if(!['certified','cap','old-cutoff','zero'].includes(preset))return;for(const field of Object.values(fields))field.value='1';fields.tau.value=preset==='cap'?'1e-8':preset==='zero'?'0':'1e-14';fields.L.value=preset==='old-cutoff'?'10000':'1e9';update();});
      return;
    }
    if(route==='hnm-findings') {
      const search=get('r31-finding-search'),round=get('r31-finding-round'),cards=get('r31-finding-cards'),count=get('r31-finding-count'),reset=get('r31-finding-reset');
      if(!search||!round||!cards||!count||!reset)return;
      const query=location.hash.match(/(?:\?|&)finding=([^&]*)/);
      if(query){try{search.value=decodeURIComponent(query[1]);}catch{}}
      const update=()=>{cards.innerHTML=findingCards(search.value,round.value);count.textContent=`${filterFindings(search.value,round.value).length} of ${arr(D.registry?.contributions).length} HNM records shown.`;};
      search.addEventListener('input',update);round.addEventListener('change',update);reset.addEventListener('click',()=>{search.value='';round.value='all';update();search.focus();});update();
    }
    if(route==='round31-sources') {
      const search=get('r31-source-search'),area=get('r31-source-area'),cards=get('r31-source-cards'),count=get('r31-source-count'),reset=get('r31-source-reset');
      if(!search||!area||!cards||!count||!reset)return;
      const update=()=>{cards.innerHTML=sourceCards(search.value,area.value);count.textContent=`${filterSources(search.value,area.value).length} of ${arr(D.survey).length} source records shown.`;};
      search.addEventListener('input',update);area.addEventListener('change',update);reset.addEventListener('click',()=>{search.value='';area.value='all';update();search.focus();});update();
    }
    if(route==='research-network') {
      const search=get('r31-network-search'),catalog=get('r31-network-catalog'),details=get('r31-network-details'),count=get('r31-network-count'),reset=get('r31-network-reset');
      if(!search||!catalog||!details||!count||!reset)return;
      let selected=networkInitial();
      const query=location.hash.match(/(?:\?|&)node=([^&]*)/);
      if(query){try{const value=decodeURIComponent(query[1]);if(nodeById.has(value))selected=value;}catch{}}
      const draw=()=>{catalog.innerHTML=networkCatalog(search.value,selected);details.innerHTML=networkDetails(selected);count.textContent=`${filterNodes(search.value).length} of ${nodes.length} entries match. Direct relations retain their full context.`;};
      const choose=event=>{const button=event.target.closest?.('[data-r31-node]'),value=button?.getAttribute('data-r31-node');if(!nodeById.has(value))return;selected=value;draw();const heading=get('r31-network-selected');heading?.setAttribute?.('tabindex','-1');heading?.focus?.({preventScroll:true});};
      search.addEventListener('input',draw);catalog.addEventListener('click',choose);details.addEventListener('click',choose);reset.addEventListener('click',()=>{search.value='';selected=networkInitial();draw();search.focus();});draw();
    }
  }
  window.ResearchRound31={render,afterRender,normalizeRoute,reviewed,complete,counts,safePath,safeURL,source,filterSources,sourceCards,filterFindings,findingCards,filterNodes,networkCatalog,networkDetails,validEdges,calculatorAdmitted,referencePreview,previewOutput,data:D};
  window.ResearchObservatory={...prior,render,afterRender};
})();
