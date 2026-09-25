/* Additive Round33 reader. Scientific wording comes from reviewed source data. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND33_DATA;
  if (!prior || !D) return;
  const IDS = ['ba1','ba2','bb1','bb2','bc1','bc2','bd1','bd2'];
  const REQUESTED = 8;
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
  const loops = arr(D.loops);
  const reviewed = loop => loop?.stage === 'reviewed' && IDS.includes(loop.id) &&
    /^[a-f0-9]{64}$/.test(String(loop.gate_sha256)) &&
    loop.gate_path === `research/round33/advisor/${loop.id}-gate.json` &&
    typeof loop.accepted === 'string' && !!loop.accepted.trim() &&
    typeof loop.title === 'string' && !!loop.title.trim() &&
    arr(loop.limitations).length > 0 &&
    /^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])/.test(String(loop.verdict));
  const counts = () => ({requested:REQUESTED, completed:loops.filter(reviewed).length});
  const complete = () => D.schema === 'hnm-round33-presentation-v1' && D.placeholder !== true && loops.length === REQUESTED &&
    loops.every((loop,index) => reviewed(loop) && loop.id === IDS[index] && loop.sequence === index + 1) &&
    D.progress?.completed === REQUESTED && D.progress?.requested === REQUESTED && D.progress?.cycle_complete === true;
  const byRoute = new Map(loops.filter(loop => IDS.includes(loop.id)).map(loop => ['round33-' + loop.id,loop]));
  const own = new Set(['home','round33','round33-results','round33-subrounds','round33-roadmap','round33-sources','round33-panel','round33-calculators','round33-figures','round33-applications','drafts','research-network','hnm-findings',...IDS.map(id => 'round33-' + id)]);
  function normalizeRoute(value='home') {
    let route=String(value||'home').split('?')[0];
    if(route==='round33' && location.hash.startsWith('#research/round33/')) route=location.hash.slice('#research/'.length).split('?')[0];
    if(route.startsWith('round33/')) {
      const tail=route.slice('round33/'.length);
      route={home:'home',results:'round33-results',loops:'round33-results',subrounds:'round33-subrounds',roadmap:'round33-roadmap',sources:'round33-sources',panel:'round33-panel',calculators:'round33-calculators',figures:'round33-figures',applications:'round33-applications'}[tail] ?? 'round33-'+tail;
    }
    return route==='round33' ? 'home' : route;
  }
  function nav(route) {
    const entries=[['home','Home'],['round33-results','Latest results'],['round33-subrounds','Sub-rounds'],['round33-applications','Applications'],['round33-panel','Panel'],['round33-calculators','Calculators'],['round33-figures','Figures'],['hnm-findings','HNM catalog'],['research-network','Research network'],['drafts','Drafts'],['round33-roadmap','Next questions'],['round33-sources','Sources'],['round32-results','Round32 archive']];
    return `<nav class="rc-nav r31-nav r32-nav r33-nav" aria-label="Research navigation">${entries.map(([target,title])=>`<a href="#research/${target}"${target===route?' aria-current="page"':''}>${esc(title)}</a>`).join('')}</nav>`;
  }
  function badge(loop) {
    const limited=/limited|insufficient|reject|fail/.test(loop.verdict);
    return `<span class="r29-badge r29-badge-${limited?'limited':'accepted'}">${esc(String(loop.verdict).replaceAll('_',' '))}</span>`;
  }
  function scope() {
    return `<aside class="r29-scope r32-scope r33-scope"><p class="rc-kicker">Applicability</p><p>${esc(D.scope_statement)}</p><p>Each result below names its model, coupling, state and exclusions. A fixed-lattice family must be distinguished from other families, from finite graphs and from the four-dimensional continuum problem; a transfer recorded in the applications stage applies only to its named model. Hruday / HNM aliases identify project records; established mathematics retains its attribution and scientific priority is unverified.</p></aside>`;
  }
  function incomplete() {
    return `<header class="r22-page-head"><p class="rc-kicker">Round33 · Review unavailable</p><h1>The complete review is not available.</h1><p>The eight required source-bound reviews across three research sub-rounds and the applications stage are incomplete in this reader. No Round33 scientific findings are displayed.</p><p>${link('round32-results','Read the preserved Round32 results →')}</p></header>`;
  }
  function card(loop) {
    return `<article class="rc-result r32-card r33-card"><div class="r29-card-top"><p class="rc-kicker">Sub-round ${esc(loop.subround)} · Investigation ${esc(loop.sequence)} · ${esc(loop.id.toUpperCase())}</p>${badge(loop)}</div><h2>${esc(loop.title)}</h2><p>${esc(loop.summary)}</p><p class="r29-card-limit"><strong>Limit:</strong> ${esc(loop.limitations[0])}</p><p>${link('round33-'+loop.id,'Derivation, scope and review →')}</p></article>`;
  }
  function subroundGroups() {
    const known=arr(D.subrounds).slice().sort((a,b)=>a.id-b.id);
    if(known.length) return known;
    const ids=[...new Set(loops.map(loop=>loop.subround))].sort((a,b)=>a-b);
    return ids.map(id=>({id,title:'Sub-round '+id}));
  }
  function home() {
    return `<header class="r29-home-hero"><div><p class="rc-kicker">Hruday N M (BUNZEEY) · Round33</p><h1>Read the result.<br>Check the conditions.</h1><p class="r29-home-lede">${esc(D.summary)}</p><div class="r29-home-actions">${link('round33-results','Read the latest results →')}${link('round33-applications','See the applications →')}${link('drafts','Read the manuscript →')}</div></div><aside class="r29-home-status"><p class="rc-kicker">This research cycle</p><p class="r29-home-count">${loops.filter(reviewed).length}<span> / ${REQUESTED}</span></p><h2>Investigations reviewed across three research sub-rounds and an applications stage</h2><p>A count of completed investigations, not a percentage of the Yang–Mills proof.</p>${link('round33-roadmap','Next questions →')}</aside></header>${scope()}<section aria-labelledby="r33-results-title"><h2 id="r33-results-title">Results with explicit limits</h2><div class="r29-grid">${loops.map(card).join('')}</div></section><section class="r29-reader-paths r33-reader-paths" aria-label="Reading paths"><a href="#research/round33-subrounds"><p class="rc-kicker">Trace</p><h2>Sub-rounds and panel direction</h2><p>See how the panel selected each pair of investigations and what changed after review.</p></a><a href="#research/round33-applications"><p class="rc-kicker">Apply</p><h2>Transfers and obstructions</h2><p>See where an admitted equation applies to a related problem, and where it does not.</p></a><a href="#research/research-network"><p class="rc-kicker">Trace</p><h2>Claims and dependencies</h2><p>Separate proved dependencies, proposed transfers and source comparisons.</p></a><a href="#research/round33-sources"><p class="rc-kicker">Inspect</p><h2>What was actually read</h2><p>Check selected passages, provenance and inaccessible leads.</p></a></section>`;
  }
  function results() {
    const groups=subroundGroups();
    return `<header class="r22-page-head"><p class="rc-kicker">Round33 · Eight reviewed investigations</p><h1>Latest results</h1><p>Every conclusion belongs to its stated model and error budget. A limited or insufficient outcome remains part of the record. Results are grouped by the sub-round in which the panel selected them; the fourth sub-round is the applications stage.</p></header>${groups.map(sub=>`<section aria-labelledby="r33-sub-${esc(sub.id)}-title"><h2 id="r33-sub-${esc(sub.id)}-title">Sub-round ${esc(sub.id)}${sub.title?' · '+esc(sub.title):''}</h2><div class="r29-grid">${loops.filter(loop=>loop.subround===sub.id).map(card).join('')}</div></section>`).join('')}${scope()}`;
  }
  function loopPage(loop) {
    return `<header class="r22-page-head"><p class="rc-kicker">Round33 · Sub-round ${esc(loop.subround)} · ${esc(loop.contribution_id)}</p><h1>${esc(loop.title)}</h1>${badge(loop)}<p>${esc(loop.summary)}</p></header><section class="r31-conclusion r32-conclusion r33-conclusion"><h2>Reviewed conclusion</h2><p>${esc(loop.accepted)}</p><p><strong>Model:</strong> ${esc(loop.model)}</p><p><strong>Producers:</strong> ${esc(arr(loop.producers).join(' + '))} · <strong>Direction:</strong> ${esc(loop.direction)}</p></section><section class="r31-section r32-section r33-section"><h2>How the result follows</h2><ol>${arr(loop.derivation_steps).map(step=>`<li>${esc(step)}</li>`).join('')}</ol></section><section class="r31-section r32-section r33-section"><h2>What this enables</h2>${list(loop.applications)}${arr(D.applications).some(row=>row.loop_id===loop.id)?`<p>${link('round33-applications','Recorded transfers and obstructions →')}</p>`:''}</section><section class="r31-section r32-section r33-section r31-limitations r32-limitations"><h2>Limitations</h2>${list(loop.limitations)}</section><section class="r31-section r32-section r33-section"><h2>Evidence and skeptical review</h2>${evidence(loop.sources)}<details class="r31-source-inventory r32-source-inventory"><summary>Full source inventory · ${arr(loop.all_sources).length} files</summary>${evidence(loop.all_sources)}</details><details><summary>Review binding</summary><p class="r31-hash r32-hash">${esc(loop.gate_sha256)}</p></details></section>${scope()}`;
  }
  function subroundCards() {
    const groups=subroundGroups();
    return groups.length ? groups.map(sub=>{
      const raw=arr(D.subrounds).find(row=>row.id===sub.id) ?? sub;
      const rows=loops.filter(loop=>loop.subround===sub.id);
      return `<article class="rc-result r32-card r32-subround-card r33-card"><p class="rc-kicker">Sub-round ${esc(sub.id)}${sub.id===4?' · Applications stage':''}</p><h2>${esc(sub.title||('Sub-round '+sub.id))}</h2>${raw.goal_id?`<p><strong>Goal:</strong> ${esc(raw.goal_id)}</p>`:''}<p>${rows.length} of 2 investigations reviewed.</p><ul>${rows.map(loop=>`<li>${link('round33-'+loop.id, loop.id.toUpperCase()+': '+loop.title)}</li>`).join('')}</ul>${raw.selection_note_path?`<p>${source(raw.selection_note_path,'Selection note →')}</p>`:'<p class="r29-muted">Selection note not yet recorded.</p>'}${raw.panel_update_path?`<p>${source(raw.panel_update_path,'Panel update after this sub-round →')}</p>`:'<p class="r29-muted">Panel update not yet recorded.</p>'}</article>`;
    }).join('') : '<p class="r29-empty">No sub-round records are available.</p>';
  }
  function subroundsPage() {
    return `<header class="r22-page-head"><p class="rc-kicker">Panel selection across the cycle</p><h1>Sub-rounds</h1><p>Each sub-round pairs two investigations: three research sub-rounds, then an applications stage. After each pair the panel may revise goals, direction and skills; see its selection note and panel update below.</p></header><div class="r29-grid">${subroundCards()}</div>${scope()}`;
  }
  const applicationKinds={transfer:['accepted','Transfer'],obstruction:['limited','Recorded obstruction'],partial:['limited','Partial transfer'],not_attempted:['pending','Not attempted']};
  function applicationCards() {
    const rows=arr(D.applications);
    return rows.length ? rows.map(row=>{
      const loopId=String(row.loop_id ?? ''), kind=applicationKinds[row.kind];
      return `<article class="rc-result r32-card r33-card r33-application-card"><div class="r29-card-top"><p class="rc-kicker">${esc(loopId.toUpperCase())} · Application</p>${kind?`<span class="r29-badge r29-badge-${kind[0]}">${esc(kind[1])}</span>`:''}</div><h2>${esc(row.problem)}</h2><p><strong>Outcome:</strong> ${esc(row.outcome)}</p><p><strong>Model:</strong> ${esc(row.model)}</p><pre class="r33-equation"><code>${esc(row.equation)}</code></pre>${row.detail?`<p>${esc(row.detail)}</p>`:''}${arr(row.sources).length?evidence(row.sources):''}<p>${IDS.includes(loopId)?link('round33-'+loopId,'Derivation, scope and review →'):''}</p></article>`;
    }).join('') : '<p class="r29-empty">No applications are recorded.</p>';
  }
  function applicationsPage() {
    return `<header class="r22-page-head"><p class="rc-kicker">Applications stage · sub-round 4</p><h1>Applications, transfers and obstructions</h1><p>Each entry applies an admitted equation to a named related problem. A transfer holds only in its stated model and is checked there by its own exact controls; where an equation does not transfer, the obstruction is recorded as a result. Entries marked not attempted are candidates named in planning that no investigation ran; nothing is claimed for them.</p></header><div class="r29-grid">${applicationCards()}</div>${scope()}`;
  }
  function drafts() {
    const add=D.addendum ?? {}, r32=D.round32_addendum ?? {}, r31=D.round31_addendum ?? {}, old=D.previous_draft ?? {}, url=safePath(add.url);
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday N M (BUNZEEY)</p><h1>Research draft and continuation</h1><p>Read each statement alongside its derivation, fixed model, error budget and limitations.</p></header><section class="r29-draft-feature"><div><p class="rc-kicker">Round33 addendum</p><h2>${esc(add.title)}</h2>${add.available===false?'<p class="r29-empty">The Round33 addendum has not been published yet.</p>':`<div class="r29-home-actions">${url?download(add.url,'Download the Round33 addendum ↓'):source(add.path,'Read the Round33 addendum')}${source(add.path,'Addendum source record')}</div>`}</div><aside><strong>Hruday N M</strong><span>BUNZEEY</span><hr><p>Human author and project direction. AI-assisted derivation and model-agent review; no external human peer review is claimed.</p></aside></section><section class="r31-section r32-section r33-section"><h2>Preserved Round32 addendum</h2><p>The preceding continuation retains its original Round32 scope and bytes.</p><p>${download(r32.url,'Download the Round32 addendum ↓')} · ${source(r32.path,'Round32 addendum source')}</p><p>${link('round32-results','Read the Round32 results →')}</p></section><section class="r31-section r32-section r33-section"><h2>Preserved Round31 addendum</h2><p>The Round31 continuation retains its original scope and bytes.</p><p>${download(r31.url,'Download the Round31 addendum ↓')} · ${source(r31.path,'Round31 addendum source')}</p><p>${link('round31-results','Read the Round31 checkpoint →')}</p></section><section class="r31-section r32-section r33-section"><h2>Preserved Draft03</h2><p>The original manuscript retains its Round30 scope and bytes.</p><p>${download(old.url,'Download Draft03 · through Round30 ↓')} · ${source(old.path,'Draft03 source')}</p></section>${url&&/\.pdf$/i.test(url)?`<details class="drafts-reader"><summary>Read the addendum in this page</summary><iframe title="Round33 research addendum" src="${esc(url)}" loading="lazy"></iframe></details>`:''}${scope()}`;
  }
  function roadmap() {
    return `<header class="r22-page-head"><p class="rc-kicker">Planning after the eight reviews</p><h1>Next research questions</h1><p>${esc(D.roadmap?.summary ?? D.roadmap?.ranking_basis ?? '')}</p></header><p class="r31-plan-notice r32-plan-notice r33-plan-notice">These follow-ups are planning records, separate from the eight investigations in this cycle.</p><div class="r29-grid">${arr(D.roadmap?.goals).map((goal,index)=>`<article class="rc-result r32-card r33-card"><p class="rc-kicker">Priority ${esc(goal.rank ?? index+1)} · ${esc(goal.id)}</p><h2>${esc(goal.title ?? goal.target)}</h2><p><strong>${esc(String(goal.status ?? 'planned_not_executed').replaceAll('_',' '))}</strong></p><p>${esc(goal.target ?? '')}</p>${goal.missing_premise?`<p><strong>Missing step:</strong> ${esc(goal.missing_premise)}</p>`:''}${goal.proposed_first_loop_test?`<details><summary>Proposed first test</summary><p>${esc(goal.proposed_first_loop_test)}</p></details>`:''}${list(goal.limitations)}</article>`).join('')}</div><p>${source('research/round33/advisor/roadmap.json','Complete roadmap')}</p>`;
  }
  function filterSources(query='',area='all') {
    const needle=String(query).trim().toLowerCase();
    return arr(D.survey).filter(row=>(area==='all'||row.area===area)&&[row.id,row.title,row.authors,row.author,row.provenance,row.reading_depth,row.use,row.limits,row.section,...arr(row.passages)].join(' ').toLowerCase().includes(needle));
  }
  function sourceCards(query='',area='all') {
    const rows=filterSources(query,area);
    return rows.length ? rows.map(row=>`<article class="rc-result r32-source r33-source"><p class="rc-kicker">${esc(row.area)} · ${esc(row.id)}</p><h2>${source(row,row.title)}</h2><p class="r29-muted">${esc(row.provenance)}${row.date?' · '+esc(row.date):''}</p><p><strong>Reading depth:</strong> ${esc(row.reading_depth || 'See the source ledger for the recorded depth.')}</p>${row.use?`<p><strong>Use here:</strong> ${esc(row.use)}</p>`:''}${row.limits?`<p><strong>Limits:</strong> ${esc(row.limits)}</p>`:''}<details><summary>Passages and access record</summary>${list(row.passages)}${row.date_note?`<p>${esc(row.date_note)}</p>`:''}${row.overlap?`<p>${esc(row.overlap)}</p>`:''}${list(row.access_failures)}${row.validation_status?`<p>${esc(row.validation_status)}</p>`:''}<p>${source(row.ledger,'Complete source ledger')}</p></details></article>`).join('') : '<p class="r29-empty">No source records match.</p>';
  }
  function survey() {
    const areas=[...new Set(arr(D.survey).map(row=>row.area))];
    return `<header class="r22-page-head"><p class="rc-kicker">Selected sources and reading limits</p><h1>Sources behind the work</h1><p>Historical and mystical material can motivate questions. A patent records a proposal; government custody records provenance. Neither replaces a tested model or a mathematical premise.</p></header><section class="r29-source-controls" aria-label="Filter source records"><label>Search sources<input id="r33-source-search" type="search" placeholder="Search title, passage or reading depth"></label><label>Research lens<select id="r33-source-area"><option value="all">All lenses</option>${areas.map(area=>`<option value="${esc(area)}">${esc(area)}</option>`).join('')}</select></label><button id="r33-source-reset" type="button">Reset</button></section><p id="r33-source-count" role="status">${arr(D.survey).length} source records.</p><section class="r29-grid" id="r33-source-cards">${sourceCards()}</section>`;
  }
  function filterFindings(query='',round='all') {
    const needle=String(query).trim().toLowerCase();
    return arr(D.registry?.contributions).filter(row=>(round==='all'||String(row.round)===String(round))&&[row.id,row.legacy_id,row.display_name,row.title,row.summary,row.application,row.limitation,row.model].join(' ').toLowerCase().includes(needle));
  }
  function findingCards(query='',round='all') {
    const rows=filterFindings(query,round);
    return rows.length?rows.map(row=>`<article class="rc-result r32-card r33-card"><p class="rc-kicker">${esc(row.id)} · Round ${esc(row.round)}</p><h2>${esc(row.display_name ?? row.title)}</h2><p><strong>${esc(String(row.status ?? 'Recorded').replaceAll('_',' '))}</strong></p><p>${esc(row.summary)}</p>${row.model?`<p><strong>Model:</strong> ${esc(row.model)}</p>`:''}${row.limitation?`<p><strong>Limits:</strong> ${esc(row.limitation)}</p>`:''}<details><summary>Application and original sources</summary><p>${esc(row.application)}</p>${evidence(row.source_paths)}<p>${esc(row.priority_status ?? 'Scientific priority is unverified.')}</p></details>${row.route?`<p>${link(row.route,'Read the complete result →')}</p>`:''}</article>`).join(''):'<p>No HNM records match.</p>';
  }
  function catalog() {
    const rounds=[...new Set(arr(D.registry?.contributions).map(row=>row.round))].sort((a,b)=>b-a);
    return `<header class="r22-page-head"><p class="rc-kicker">Hruday / HNM project records</p><h1>Contributions and their limits</h1><p>The current catalog adds the Round31, Round32 and Round33 records to the preserved Draft03 entries. Names locate work; they do not establish scientific priority or rename prior theorems.</p></header><section class="r29-source-controls" aria-label="Search the HNM catalog"><label>Search contributions<input id="r33-finding-search" type="search" placeholder="Try HNM-C-BA1, a model, or a limitation"></label><label>Round<select id="r33-finding-round"><option value="all">All rounds</option>${rounds.map(round=>`<option value="${esc(round)}">Round ${esc(round)}</option>`).join('')}</select></label><button id="r33-finding-reset" type="button">Reset</button></section><p role="status" id="r33-finding-count">${arr(D.registry?.contributions).length} records.</p><section class="r29-grid" id="r33-finding-cards">${findingCards()}</section>`;
  }
  function panelDeliberationCards() {
    const rows=arr(D.panel?.deliberation).slice().sort((a,b)=>a.loop-b.loop);
    return rows.length ? rows.map(row=>`<article class="rc-result r32-card r33-card"><p class="rc-kicker">Deliberation loop ${esc(row.loop)}</p><h2>${esc(row.summary)}</h2><p>${source(row.path,'Read the deliberation record →')}</p></article>`).join('') : '<p class="r29-empty">No deliberation records are available.</p>';
  }
  function panelUpdateCards() {
    const rows=arr(D.panel?.updates).slice().sort((a,b)=>a.subround-b.subround || String(a.lens).localeCompare(String(b.lens)));
    return rows.length ? rows.map(row=>`<article class="rc-result r32-card r33-card"><p class="rc-kicker">Sub-round ${esc(row.subround)} · ${esc(row.lens)}</p><h2>Panel update</h2>${row.goal_changes?`<p>${esc(row.goal_changes)}</p>`:''}<p>${source(row.path,'Read the panel update →')}</p>${arr(row.lenses).length?`<p>${arr(row.lenses).map(x=>source(x,'Lens update')).join(' · ')}</p>`:''}${arr(row.assistants).length?`<p>${arr(row.assistants).map(x=>source(x,'Assistant package')).join(' · ')}</p>`:''}</article>`).join('') : '<p class="r29-empty">No panel updates are recorded yet.</p>';
  }
  function panelPage() {
    return `<header class="r22-page-head"><p class="rc-kicker">Newton/Tesla, Jung/Pauli, Penrose/Feynman and occult-lens deliberation</p><h1>Panel deliberation and updates</h1><p>The deliberation loops fixed the initial goals and strategy. After every sub-round each lens may revise goals, direction and skills; those updates are recorded here, separate from the reviewed investigations.</p></header><section aria-labelledby="r33-deliberation-title"><h2 id="r33-deliberation-title">Deliberation loops</h2><div class="r29-grid">${panelDeliberationCards()}</div></section><section aria-labelledby="r33-updates-title"><h2 id="r33-updates-title">Per-sub-round panel updates</h2><div class="r29-grid">${panelUpdateCards()}</div></section>${scope()}`;
  }
  function flattenRecord(value, prefix='') {
    if (Array.isArray(value)) return [[prefix, value.map(item => item && typeof item === 'object' ? JSON.stringify(item) : String(item)).join(', ')]];
    if (value !== null && typeof value === 'object') return Object.entries(value).flatMap(([key,val]) => flattenRecord(val, prefix ? prefix+'.'+key : key));
    return [[prefix, value]];
  }
  function calculatorCards() {
    const rows=arr(D.calculators);
    return rows.length ? rows.map(row=>{
      const entries=flattenRecord(row.record ?? {});
      return `<article class="rc-result r32-card r33-card r32-calculator-card r33-calculator-card"><p class="rc-kicker">${esc(String(row.loop_id ?? '').toUpperCase())} · ${esc(row.formula_id)}</p><h2>${esc(row.title)}</h2><p class="r31-preview-notice r32-preview-label r33-preview-label"><strong>Recorded exact values; not a live computation.</strong></p><div class="r31-table-wrap r32-table-wrap"><table><thead><tr><th scope="col">Field</th><th scope="col">Recorded value</th></tr></thead><tbody>${entries.map(([key,value])=>`<tr><th scope="row">${esc(key)}</th><td>${esc(value)}</td></tr>`).join('')}</tbody></table></div><p>${source(row.source,'Exact calculator source')} · ${source(row.result_path,'Recorded result record')} · ${link('round33-'+row.loop_id,'Derivation and review →')}</p></article>`;
    }).join('') : '<p class="r29-empty">No recorded calculator results are available.</p>';
  }
  function calculatorsPage() {
    return `<header class="r22-page-head"><p class="rc-kicker">Recorded exact values from reviewed investigations</p><h1>Calculators</h1><p class="r31-preview-notice r32-preview-label r33-preview-label"><strong>Recorded exact values; not a live computation.</strong></p><p>Each record below was already bound by its investigation's admitted gate. No parameter is adjustable here and no browser floating-point preview is computed.</p></header><div class="r29-grid">${calculatorCards()}</div>${scope()}`;
  }
  function figureCards() {
    const rows=arr(D.figures);
    return rows.length ? rows.map(row=>{
      const path=safePath(row.path);
      return `<figure class="r32-figure r33-figure">${path?`<img src="${esc(path)}" alt="${esc(row.title)}" loading="lazy">`:'<p class="r29-empty">Figure file unavailable.</p>'}<figcaption><h2>${esc(row.title)}</h2><p>${esc(row.caption)}</p>${row.source_path?`<p>${source(row.source_path,'Figure source')}</p>`:''}</figcaption></figure>`;
    }).join('') : '<p class="r29-empty">No experiment-setup figures are recorded yet.</p>';
  }
  function figuresPage() {
    return `<header class="r22-page-head"><p class="rc-kicker">Experiment-setup images</p><h1>Figures</h1><p>Each figure illustrates a recorded model or setup; it is not itself a certificate.</p></header><div class="r32-figure-grid r33-figure-grid">${figureCards()}</div>${scope()}`;
  }
  const nodes=arr(D.network?.nodes), nodeById=new Map(nodes.map(node=>[String(node.id),node]));
  const relationNames={'proven-dependency':'Proved dependency','proposed-transfer':'Proposed transfer','review-selection':'Selected after review','source-dependency':'Source comparison','scope-boundary':'Scope boundary','recorded-equation':'Recorded equation'};
  const validEdges=()=>arr(D.network?.edges).filter(edge=>nodeById.has(String(edge.from))&&nodeById.has(String(edge.to))&&Object.hasOwn(relationNames,edge.type));
  const filterNodes=(query='')=>{const needle=String(query).toLowerCase().trim();return nodes.filter(node=>[node.id,node.title,node.kind,node.status,node.summary,node.model,node.hnm_alias,...arr(node.hnm_aliases)].join(' ').toLowerCase().includes(needle));};
  const networkInitial=()=>String([...nodes].reverse().find(node=>node.route==='round33-'+IDS[IDS.length-1])?.id ?? nodes[0]?.id ?? '');
  function networkCatalog(query='',selected=networkInitial()) {
    const found=filterNodes(query);
    return found.length?`<ul>${found.map(node=>`<li><button type="button" data-r33-node="${esc(node.id)}" aria-pressed="${String(node.id)===String(selected)}"><span>${esc(node.title)}</span><small>${esc(node.kind)} · ${esc(node.status)}</small></button></li>`).join('')}</ul>`:'<p>No entries match this search.</p>';
  }
  function networkDetails(selected=networkInitial()) {
    const node=nodeById.get(String(selected));
    if(!node)return '<p>Select a research or source entry.</p>';
    const edges=validEdges().filter(edge=>String(edge.from)===String(selected)||String(edge.to)===String(selected));
    return `<header><p class="rc-kicker">${esc(node.kind)} · ${esc(node.id)}</p><h2 id="r33-network-selected">${esc(node.title)}</h2><p><strong>${esc(node.status)}</strong></p></header>${node.model?`<p><strong>Model:</strong> ${esc(node.model)}</p>`:''}<p>${esc(node.summary)}</p>${node.detail?`<p>${esc(node.detail)}</p>`:''}${node.equation?`<pre><code>${esc(node.equation)}</code></pre>`:''}${evidence(node.sources)}${node.route?`<p>${link(node.route,'Read this record →')}</p>`:''}<h3>Direct relations · ${edges.length}</h3>${edges.length?`<ul class="r31-relations r32-relations r33-relations">${edges.map(edge=>{const outgoing=String(edge.from)===String(selected),other=nodeById.get(String(outgoing?edge.to:edge.from));return `<li><span class="r29-edge-label r29-edge-label-${edge.type}">${esc(relationNames[edge.type])}</span><p>${outgoing?'Outgoing to':'Incoming from'} <button type="button" data-r33-node="${esc(other.id)}">${esc(other.title)}</button></p>${edge.label?`<p>${esc(edge.label)}</p>`:''}${edge.detail?`<p>${esc(edge.detail)}</p>`:''}</li>`;}).join('')}</ul>`:'<p>No direct relations are recorded.</p>'}`;
  }
  function network() {
    return `<header class="r22-page-head"><p class="rc-kicker">${nodes.length} catalog entries · ${validEdges().length} relations</p><h1>Trace the research network</h1><p>Select a result or source to inspect its direct dependencies. Proposed transfers and source comparisons remain distinct from proved dependencies. Counts describe this index, not physical gauge links or the fraction of a proof completed.</p></header><section class="r29-source-controls" aria-label="Search the research network"><label>Search entries<input type="search" id="r33-network-search" placeholder="Try BA1, boundary, Hruday or a source"></label><button type="button" id="r33-network-reset">Reset</button></section><p role="status" id="r33-network-count">${nodes.length} entries.</p><div class="r29-network-layout"><aside class="r29-network-catalog"><h2>Research catalog</h2><div id="r33-network-catalog">${networkCatalog()}</div></aside><section class="r29-network-details" id="r33-network-details" aria-labelledby="r33-network-selected">${networkDetails()}</section></div>`;
  }
  function render(value='home') {
    const route=normalizeRoute(value);
    if(!own.has(route)) {
      const archived=prior.render(value).replace(/<aside class="r32-current-banner">[\s\S]*?<\/aside>/g,'');
      return `<aside class="r33-current-banner"><strong>Archived research view.</strong> ${link('round33-results','Current Round33 results')}<span>This page retains its earlier scope and navigation.</span></aside>`+archived;
    }
    const loop=byRoute.get(route);
    const body=!complete()?incomplete():loop?loopPage(loop):route==='round33-results'?results():route==='round33-subrounds'?subroundsPage():route==='round33-applications'?applicationsPage():route==='drafts'?drafts():route==='round33-roadmap'?roadmap():route==='round33-sources'?survey():route==='round33-panel'?panelPage():route==='round33-calculators'?calculatorsPage():route==='round33-figures'?figuresPage():route==='research-network'?network():route==='hnm-findings'?catalog():home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r29 r30 r31 r32 r33">${nav(route)}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · ${esc(D.author)}</strong>${link('round33-sources','Source ledger')}${link('round33-roadmap','Open questions')}${link('round32-results','Round32 archive')}</footer></div>`;
  }
  function afterRender() {
    const route=normalizeRoute(location.hash.replace(/^#research\/?/,'')||'home');
    if(!own.has(route))return prior.afterRender?.();
    window.ResearchJourney?.cleanup?.();
    document.title=`${complete()?(byRoute.get(route)?.title ?? ({home:'Hruday research home',drafts:'Draft and addendum','research-network':'Research network','hnm-findings':'HNM catalog','round33-results':'Round33 results','round33-subrounds':'Round33 sub-rounds','round33-applications':'Round33 applications','round33-sources':'Round33 sources','round33-panel':'Round33 panel','round33-calculators':'Round33 calculators','round33-figures':'Round33 figures','round33-roadmap':'Next research questions'}[route]??'Round33')):'Round33 review unavailable'} · Yang–Mills Workbench`;
    if(!complete())return;
    const get=name=>document.getElementById(name);
    if(route==='hnm-findings') {
      const search=get('r33-finding-search'),round=get('r33-finding-round'),cards=get('r33-finding-cards'),count=get('r33-finding-count'),reset=get('r33-finding-reset');
      if(!search||!round||!cards||!count||!reset)return;
      const query=location.hash.match(/(?:\?|&)finding=([^&]*)/);
      if(query){try{search.value=decodeURIComponent(query[1]);}catch{}}
      const update=()=>{cards.innerHTML=findingCards(search.value,round.value);count.textContent=`${filterFindings(search.value,round.value).length} of ${arr(D.registry?.contributions).length} HNM records shown.`;};
      search.addEventListener('input',update);round.addEventListener('change',update);reset.addEventListener('click',()=>{search.value='';round.value='all';update();search.focus();});update();
    }
    if(route==='round33-sources') {
      const search=get('r33-source-search'),area=get('r33-source-area'),cards=get('r33-source-cards'),count=get('r33-source-count'),reset=get('r33-source-reset');
      if(!search||!area||!cards||!count||!reset)return;
      const update=()=>{cards.innerHTML=sourceCards(search.value,area.value);count.textContent=`${filterSources(search.value,area.value).length} of ${arr(D.survey).length} source records shown.`;};
      search.addEventListener('input',update);area.addEventListener('change',update);reset.addEventListener('click',()=>{search.value='';area.value='all';update();search.focus();});update();
    }
    if(route==='research-network') {
      const search=get('r33-network-search'),catalog=get('r33-network-catalog'),details=get('r33-network-details'),count=get('r33-network-count'),reset=get('r33-network-reset');
      if(!search||!catalog||!details||!count||!reset)return;
      let selected=networkInitial();
      const query=location.hash.match(/(?:\?|&)node=([^&]*)/);
      if(query){try{const value=decodeURIComponent(query[1]);if(nodeById.has(value))selected=value;}catch{}}
      const draw=()=>{catalog.innerHTML=networkCatalog(search.value,selected);details.innerHTML=networkDetails(selected);count.textContent=`${filterNodes(search.value).length} of ${nodes.length} entries match. Direct relations retain their full context.`;};
      const choose=event=>{const button=event.target.closest?.('[data-r33-node]'),value=button?.getAttribute('data-r33-node');if(!nodeById.has(value))return;selected=value;draw();const heading=get('r33-network-selected');heading?.setAttribute?.('tabindex','-1');heading?.focus?.({preventScroll:true});};
      search.addEventListener('input',draw);catalog.addEventListener('click',choose);details.addEventListener('click',choose);reset.addEventListener('click',()=>{search.value='';selected=networkInitial();draw();search.focus();});draw();
    }
  }
  window.ResearchRound33={render,afterRender,normalizeRoute,reviewed,complete,counts,safePath,safeURL,source,filterSources,sourceCards,filterFindings,findingCards,filterNodes,networkCatalog,networkDetails,validEdges,subroundCards,figureCards,calculatorCards,applicationCards,data:D};
  window.ResearchObservatory={...prior,render,afterRender};
})();
