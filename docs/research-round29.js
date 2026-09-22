/* Additive Round29 pages. Only reviewed, source-bound records render as findings. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND29_DATA;
  if (!prior || !D) return;
  const array = value => Array.isArray(value) ? value : [];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const id = value => String(value ?? '').toLowerCase();
  const validId = value => /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(String(value));
  const list = values => array(values).length ? `<ul>${values.map(value => `<li>${esc(value)}</li>`).join('')}</ul>` : '';
  const loops = array(D.loops), byRoute = new Map(loops.filter(loop => validId(loop.id)).map(loop => ['round29-' + loop.id, loop]));
  const own = new Set(['home','hnm-findings','hnm-priorities','drafts','sharing','round29','round29-results','round29-sources','round29-roadmap','round29-proof','round29-addendum', ...byRoute.keys()]);
  if (D.network) own.add('research-network');
  const networkNodes = array(D.network?.nodes), networkEdges = array(D.network?.edges);
  const nodeById = new Map(networkNodes.map(node => [String(node.id),node]));
  const kindNames = {history:'Earlier findings',premise:'Required premises',equation:'Equations',loop:'Research loops',open:'Open targets',literature:'Literature and historical sources',source:'External primary sources'};
  const edgeNames = {'proven-dependency':'Verified source dependency','proposed-transfer':'Proposed transfer or scope comparison','review-selection':'Review selection or methodological comparison','source-dependency':'Scoped source input','scope-boundary':'Open scope boundary','recorded-equation':'Equation recorded in derivation'};
  const lensNames = {newton:'Newton',tesla:'Tesla',jung:'Jung / Pauli',penrose:'Penrose',feynman:'Feynman',skeptic:'Skeptic'};
  const categoryNames = {historical_primary:'Historical primary source',technical_primary:'Modern primary research',patent_primary:'Patent',bibliographic_primary:'Bibliographic metadata',forum_discourse:'Forum discussion',official_problem_reference:'Official problem statement'};
  function normalizeRoute(value) {
    let route = String(value ?? 'home').split('?')[0] || 'home';
    if (route === 'round29' && location.hash.startsWith('#research/round29/')) route = location.hash.slice('#research/'.length).split('?')[0];
    if (route.startsWith('round29/')) {
      const tail = route.slice('round29/'.length);
      const aliases = {home:'round29',loops:'round29-results',results:'round29-results',sources:'round29-sources',roadmap:'round29-roadmap',proof:'round29-proof',addendum:'round29-addendum'};
      route = aliases[tail] ?? 'round29-' + tail;
    }
    return route === 'contributions' ? 'hnm-findings' : route;
  }
  const link = (route, label) => validId(route) ? `<a href="#research/${route}">${esc(label)}</a>` : esc(label);
  function safePath(value) {
    const raw = String(value ?? '');
    if (!raw || /[\s\\:#?<>"'\u0000-\u001f\u007f%]/.test(raw) || raw.startsWith('/')) return '';
    const parts = raw.split('/');
    return parts.some(part => !part || part === '.' || part === '..') ? '' : parts.map(encodeURIComponent).join('/');
  }
  function safeURL(value, local = false) {
    const raw = String(value ?? '');
    if (/^https:\/\/[^\s\\<>"'\u0000-\u001f\u007f]+$/i.test(raw)) {
      try { const url = new URL(raw); if (url.hostname && !url.username && !url.password) return url.href; } catch {}
    }
    return local ? safePath(raw) : '';
  }
  function source(value) {
    const item = typeof value === 'string' ? /^https:/i.test(value) ? {url:value} : {path:value} : value ?? {};
    const path = safePath(item.path), href = item.url ? safeURL(item.url) : path ? 'https://github.com/occult-kranti/yang_mills_workbench/blob/main/' + path : '';
    const title = item.title ?? item.label ?? item.path ?? item.url ?? 'Source unavailable';
    return href ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(title)} <span aria-hidden="true">↗</span></a>` : `<span>${esc(title)}</span>`;
  }
  const sourceList = values => array(values).length ? `<ul class="r29-evidence">${values.map(value => `<li>${source(value)}</li>`).join('')}</ul>` : '<p class="r29-muted">No sources are attached to this record.</p>';
  const reviewed = loop => loop.stage === 'reviewed' && /^[a-f0-9]{64}$/.test(String(loop.gate_sha256)) && typeof loop.accepted === 'string' && loop.accepted.length > 0 && /^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])/.test(String(loop.verdict));
  const reviewedLoops = () => loops.filter(reviewed);
  const requested = () => Number.isInteger(D.progress?.requested) && D.progress.requested > 0 ? D.progress.requested : null;
  function counts() { return {completed:reviewedLoops().length, selected:loops.length, requested:requested(), remaining:requested() === null ? null : Math.max(0, requested() - reviewedLoops().length)}; }
  function badge(loop) {
    const status = reviewed(loop) ? /limited|insufficient|reject|fail/.test(loop.verdict) ? 'limited' : /conditional/.test(loop.verdict) ? 'conditional' : 'accepted' : 'pending';
    const label = reviewed(loop) ? String(loop.verdict).replaceAll('_',' ') : loop.stage === 'in-progress' ? 'In progress · review pending' : 'Selected · review pending';
    return `<span class="r29-badge r29-badge-${status}">${esc(array(registry.equations).find(eq=>eq.legacy_label===label)?.id??label)}</span>`;
  }
  function nav(route) {
    return `<nav class="rc-nav" aria-label="Research navigation">${[['home','Home'],['hnm-priorities','Ranked findings'],['hnm-findings','HNM catalog'],['round29-results','New research'],['research-network','Network'],['drafts','Complete draft'],['round29-roadmap','Next goals'],['round29-sources','Sources']].map(([target,label]) => `<a href="#research/${target}"${target === route || target === 'home' && route === 'round29' ? ' aria-current="page"' : ''}>${label}</a>`).join('')}</nav>`;
  }
  function assessment(compact = false) {
    return `<section class="r29-scope"><p class="rc-kicker">Proof progress</p><h2>Research progress and proof completion are different counts.</h2><p>${esc(D.progress?.percentage_statement ?? 'No new proof-completion assessment is recorded.')}</p>${compact ? '' : '<p class="r29-muted">An executed investigation may have a limited or insufficient outcome. It does not represent a fixed fraction of a Yang–Mills existence and mass-gap proof.</p>'}<p>${link('round29-proof','Inspect the outstanding proof obligations →')}</p></section>`;
  }
  function loopCard(loop, number) {
    const complete = reviewed(loop);
    return `<article class="rc-result r29-loop-card"><div class="r29-card-top"><p class="rc-kicker">${number + 1} · ${esc(id(loop.id).toUpperCase())}${loop.goal ? ' · ' + esc(loop.goal) : ''}</p>${badge(loop)}</div><h2>${esc(loop.title ?? id(loop.id).toUpperCase())}</h2><p>${complete ? esc(loop.accepted) : 'This investigation has been selected. Its findings will appear after the review is complete.'}</p>${complete && array(loop.limitations).length ? `<p class="r29-card-limit"><strong>Limit:</strong> ${esc(loop.limitations[0])}</p>` : ''}<p>${link('round29-' + loop.id,complete ? 'Read result and evidence →' : 'View the selected investigation →')}</p></article>`;
  }
  function pairCards() {
    const pairs = array(D.goal_pairs), acceptedIds = new Set(reviewedLoops().map(loop => loop.id)), selectedIds = new Set(loops.map(loop => loop.id));
    return `<div class="r29-pairs">${pairs.map(pair => `<article><p class="rc-kicker">Goal ${esc(pair.id)}</p><h3>${esc(pair.target || pair.id)}</h3><ul>${array(pair.loops).map(loopId => `<li><span>${selectedIds.has(loopId) ? link('round29-' + loopId,String(loopId).toUpperCase()) : esc(String(loopId).toUpperCase())}</span><small>${acceptedIds.has(loopId) ? 'Reviewed' : selectedIds.has(loopId) ? 'Selected · review pending' : 'Not yet selected'}</small></li>`).join('')}</ul></article>`).join('')}</div>${pairs.length < 5 ? `<p class="r29-muted">${5 - pairs.length} later goal${5 - pairs.length === 1 ? '' : 's'} remain${5 - pairs.length === 1 ? 's' : ''} to be selected from the reviews.</p>` : ''}`;
  }
  function cycleHome() {
    const c = counts();
    return `<header class="rc-hero r29-hero"><div><p class="rc-kicker">Round29 · five paired research goals</p><h1>${esc(D.title ?? 'Follow each result to its remaining premise.')}</h1><p>${esc(D.summary ?? '')}</p><div class="rc-hero-actions">${link('round29-results','Read the reviewed findings →')}${link('round29-sources','Explore the source survey →')}${link('research-network','Trace the research network →')}</div></div><aside class="rc-score r29-count"><span class="rc-score-number">${c.completed}${c.requested === null ? '' : `<small> / ${c.requested}</small>`}</span><strong>Research loops reviewed</strong><small>${c.requested !== null && c.completed === c.requested ? 'This requested cycle is complete.' : `${c.selected} selected · ${c.remaining ?? '—'} investigations remain to be reviewed.`}</small><small>Execution count; not a percentage of Yang–Mills solved.</small></aside></header><section class="r29-pair-section"><div class="r29-section-head"><h2>Where each goal stands</h2><p>Second loops follow the first review.</p></div>${pairCards()}</section><section><div class="r29-section-head"><h2>Current investigations</h2><p>${c.completed} reviewed · ${c.selected - c.completed} awaiting review</p></div><div class="r29-grid">${loops.map(loopCard).join('')}</div></section>${assessment(true)}<section class="r29-reading-callout"><div><p class="rc-kicker">Historical ideas and modern research</p><h2>What was read, and how it was used.</h2><p>Newton, Tesla, Jung, Penrose and Feynman provide documented research perspectives. Reading records preserve the source category, passages inspected and limits on the claims they support.</p></div>${link('round29-sources','Open the source survey →')}</section><p>${link('round28-home','Previous Round28 checkpoint →')} · ${link('all-results','All recorded rounds →')}</p>`;
  }
  const registry = D.registry ?? {}, contributions = array(registry.contributions);
  const ranked = () => contributions.filter(item => Number.isFinite(item.priority) && item.priority > 0).sort((a,b) => a.priority-b.priority);
  const findingRoute = item => Number(item.round) === 29 && byRoute.has('round29-' + id(item.legacy_id)) ? 'round29-' + id(item.legacy_id) : 'hnm-findings?finding=' + encodeURIComponent(item.id);
  function findingLink(item, label) { return `<a href="#research/${esc(findingRoute(item))}">${esc(label ?? item.display_name)}</a>`; }
  function routeAliases(route) {
    const match=String(route).match(/^(?:round|review)(\d+)-([a-z]+\d+)$/);
    if(!match)return [];
    const prefix='research/round'+match[1]+'/',loop=match[2];
    return contributions.filter(item=>array(item.source_paths).some(path=>typeof path==='string'&&(path.startsWith(prefix+'forward/'+loop+'/')||path.startsWith(prefix+'reverse/'+loop+'/')||path===prefix+'contracts/'+loop+'.json'||path===prefix+'advisor/'+loop+'-gate.json')));
  }
  function namedStatements(item) {
    const ids=new Set(array(item?.statement_ids)), statements=array(registry.statements).filter(note=>ids.has(note.id)||note.contribution_id===item?.id);
    if(!statements.length)return '';
    return `<section class="r29-statements"><h3>Named statements</h3>${statements.map(note=>`<details><summary>${esc(note.id)} · ${esc(note.title)}</summary><p><strong>${esc(note.type)} · ${esc(String(note.status).replaceAll('_',' '))}</strong></p><p>${esc(note.summary)}</p><p class="r29-card-limit"><strong>Scope:</strong> ${esc(note.scope)}</p>${sourceList(note.source_paths)}<p class="r29-muted">${esc(note.priority_status)}</p></details>`).join('')}</section>`;
  }
  function extensionLinks(item) {
    const notes=array(item?.current_extensions);
    return notes.length?`<p class="r29-muted"><strong>Later reviewed extension:</strong> ${notes.map(note=>{const target=contributions.find(row=>row.id===note.id);return target?findingLink(target,note.title):esc(note.title??note.id);}).join(' · ')}</p>`:'';
  }
  function currentExtensions(item) {
    const extensions=array(item?.current_extensions);
    if(!extensions.length)return '';
    return `<aside class="r29-current-extensions"><p class="rc-kicker">Later reviewed extensions</p>${extensions.map(note=>{const target=contributions.find(row=>row.id===note.id);return `<article><h3>${target?findingLink(target,note.title):esc(note.title??note.id)}</h3><p class="r29-muted">${esc(note.id)}</p><p>${esc(note.summary)}</p>${sourceList(note.source_paths)}</article>`;}).join('')}<p class="r29-muted">These later findings extend the research record. The original result and its recorded scope follow their own gates.</p></aside>`;
  }
  function aliasNotice(route) {
    const rows=routeAliases(route);
    return rows.length ? `<section class="r29 r29-alias-notice"><p class="rc-kicker">Current HNM names for this historical record</p><ul>${rows.map(item=>`<li>${findingLink(item)} <small>${esc(item.id)}</small></li>`).join('')}</ul>${rows.map(currentExtensions).join('')}<p>The links are matched to this route's original evidence paths. The historical presentation follows below.</p></section>` : '';
  }
  function namingNote() { return `<p class="r29-naming-note"><strong>HNM / Hruday</strong> names are project identifiers. They do not establish scientific priority or rename established mathematics. Original symbols, theorem attributions, models and historical evidence remain traceable.</p>`; }
  function priorityTable(limit) {
    const rows=ranked().slice(0,limit ?? ranked().length);
    return rows.length ? `<div class="r29-table-wrap r29-priority-wrap" tabindex="0" role="region" aria-label="Ranked research findings"><table class="r29-table r29-priority-table"><caption>Research priority: relevance to the remaining problem and usefulness of the reviewed result. This is an editorial ranking, not a ranking of verified world novelty.</caption><thead><tr><th scope="col">Rank</th><th scope="col">HNM finding</th><th scope="col">What it establishes / possible use</th><th scope="col">Recorded scope / later extensions</th></tr></thead><tbody>${rows.map(item=>`<tr><td><strong>${esc(item.priority)}</strong></td><th scope="row">${findingLink(item)}<small>${esc(item.id)} · Round ${esc(item.round)}<br>${esc(item.classification)}</small></th><td data-label="Use">${esc(item.application || item.legacy_title)}</td><td data-label="Scope">${array(item.current_extensions).length?'<strong>Original checkpoint:</strong> ':''}${esc(item.limitation)}${extensionLinks(item)}</td></tr>`).join('')}</tbody></table></div>` : '<p>The ranked catalog is being updated from the reviewed research records.</p>';
  }
  function stateRoutes() {
    const ids=new Set(reviewedLoops().map(loop=>loop.id));
    if(!ids.has('ao2')||!ids.has('aq1'))return '';
    return `<section class="r29-state-routes"><h2>Two state routes, with separate conclusions.</h2><p>These constructions share a local selected-strip model dictionary. Equality of their limiting states has not been established.</p><div class="r29-grid"><article class="rc-result"><p class="rc-kicker">Inherited orthant state</p><h3>The conditional energy-identity route</h3><p>The original restrictions <code>|τ| &lt; τ*</code> and <code>|τ| ≤ 2<sup>−16</sup></code> remain. AO2 proves the actual Wilson first-energy identity and operator-domain membership for this state, with a second-moment upper bound.</p><p>${link('round29-ao2','Read AO2 and its retained hypotheses →')}</p></article><article class="rc-result"><p class="rc-kicker">Numerical full-lattice state</p><h3>The explicit-cap thermodynamic route</h3><p>At <code>|τ| ≤ 10<sup>−8</sup></code>, AQ1 constructs a locally normal stationary subsequential state on the full coarse lattice. No old symbolic stability or HTW smallness restriction is used. Uniqueness, whole-sequence convergence and identity with the inherited state remain separate questions.</p>${ids.has('aq2')?'<p>AQ2 establishes a physical energy gap of at least <code>α/16</code> and Wilson variance greater than <code>1/5</code> in this same chosen representation.</p>':''}<p>${link('round29-aq1','Read AQ1’s construction →')}${ids.has('aq2')?' · '+link('round29-aq2','Read the AQ2 physical-sector result →'):''}</p></article></div><p class="r29-muted">The AO2 energy identity applies to its specified orthant state. The numerical route requires its own observable and spectral arguments; a shared symbol does not identify states.</p></section>`;
  }
  function home() {
    const c=counts(), first=ranked()[0];
    return `<header class="r29-home-hero"><div class="r29-home-intro"><p class="rc-kicker">HNM Research · Yang–Mills Workbench</p><h1>Gauge theory.<br>Exact checks.<br>Open questions.</h1><p class="r29-home-lede">A research notebook tracing finite calculations and fixed-lattice constructions toward the Yang–Mills problem, with the assumptions still needed for a continuum theory.</p><p class="r29-byline">Human author <strong>${esc(D.author)}</strong><span>with disclosed AI-assisted research and review</span></p><div class="r29-home-actions"><a class="r29-primary" href="#research/drafts">Read the complete draft →</a><a href="#research/hnm-priorities">Explore the findings →</a></div></div><aside class="r29-home-status"><p class="rc-kicker">Current checkpoint · Round29</p><div class="r29-home-count">${c.completed}<span>/ ${c.requested ?? 10}</span></div><h2>investigations reviewed</h2><p>${c.completed === c.requested ? 'Five paired goals complete. Next goals are planned from their outcomes.' : 'The current cycle is in progress. Unreviewed proposals are not listed as findings.'}</p><div class="r29-open-status"><span>Clay problem</span><strong>Still open</strong></div><p class="r29-muted">Loop counts measure work completed, not how much of a proof is solved.</p></aside></header><section class="r29-reader-paths" aria-label="Choose a way into the research"><a href="#research/hnm-priorities"><span>01 / Understand</span><h2>What changed?</h2><p>Start with the ranked results and the limits attached to each.</p><strong>Read the priorities →</strong></a><a href="#research/research-network"><span>02 / Trace</span><h2>What depends on what?</h2><p>Follow proven dependencies, open transfers and source comparisons.</p><strong>Open the network →</strong></a><a href="https://github.com/occult-kranti/yang_mills_workbench/tree/main/research/round29" target="_blank" rel="noopener noreferrer"><span>03 / Reproduce</span><h2>Can I check it?</h2><p>Inspect source-bound reports, exact arithmetic and skeptical reviews.</p><strong>Browse the code ↗</strong></a></section>${first ? `<section class="r29-featured"><p class="rc-kicker">First reading · priority ${esc(first.priority)}</p><h2>${esc(first.display_name)}</h2><p>${esc(first.application)}</p><p class="r29-feature-limit"><strong>Scope:</strong> ${esc(first.limitation)}</p>${findingLink(first,'Follow this result →')}</section>` : ''}<section><div class="r29-section-head"><h2>Results worth starting with</h2><a href="#research/hnm-priorities">All ranked findings →</a></div>${priorityTable(5)}</section>${namingNote()}${stateRoutes()}<section><div class="r29-section-head"><h2>The latest research cycle</h2><a href="#research/round29-results">All ${c.completed} reviewed investigations →</a></div>${pairCards()}</section><section class="r29-reading-callout"><div><p class="rc-kicker">Share the work</p><h2>A public research draft, with the caveats intact.</h2><p>Read the prepared Substack and Reddit posts, the derivation behind the headline, and links to the paper and source code.</p></div><a href="#research/sharing">Open the share drafts →</a></section>${assessment(true)}`;
  }
  function priorities() { return `<header class="r22-page-head"><p class="rc-kicker">HNM contribution priorities</p><h1>What we have established—and what it is useful for.</h1><p>The table prioritizes model results, certificates, obstructions and conditional deductions. No row is a claim to have solved the four-dimensional continuum problem.</p></header>${priorityTable()}${namingNote()}<p><a href="#research/hnm-findings">Search all ${contributions.length} named contributions, equations and quantities →</a></p>`; }
  function matchesFinding(item, query='', round='all') { return (round === 'all' || String(item.round) === round) && [item.id,item.legacy_id,item.display_name,item.legacy_title,item.classification,item.application,item.limitation,...array(item.statement_ids)].join(' ').toLowerCase().includes(String(query).trim().toLowerCase()); }
  function findingCards(query='',round='all') {
    const rows=contributions.filter(item=>matchesFinding(item,query,round));
    return rows.length ? rows.map(item=>`<article class="r29-finding" id="${esc(item.id)}"><p class="rc-kicker">${esc(item.id)} · Round ${esc(item.round)} · ${esc(item.classification)}</p><h2>${esc(item.display_name)}</h2><p><strong>Original record:</strong> ${esc(item.legacy_id)} · ${esc(item.legacy_title)}</p>${item.proof_status||item.status?`<p><strong>Recorded status:</strong> ${esc(item.proof_status??item.status)}</p>`:''}<p><strong>Use:</strong> ${esc(item.application)}</p><p class="r29-card-limit"><strong>${array(item.current_extensions).length?'Original Limit:':'Limit:'}</strong> ${esc(item.limitation)}</p>${currentExtensions(item)}${namedStatements(item)}${item.next?`<p><strong>Next:</strong> ${esc(item.next)}</p>`:''}${array(item.equation_labels).length?`<p class="r29-equation-tags">${item.equation_labels.map(label=>`<span>${esc(array(registry.equations).find(eq=>eq.legacy_label===label)?.id??label)}</span>`).join('')}</p>`:''}<details><summary>Evidence and equation aliases</summary>${sourceList(item.source_paths)}${array(registry.equations).filter(eq=>array(eq.contribution_ids).includes(item.id)||eq.contribution_id===item.id||array(item.equation_labels).includes(eq.legacy_label)).map(eq=>`<p><strong>${esc(eq.id??eq.hnm_label)}</strong> ${esc(eq.display_name??eq.original_label??eq.legacy_label??'')}</p>${eq.expression?`<pre><code>${esc(eq.expression)}</code></pre>`:''}`).join('')}</details></article>`).join('') : '<p class="r29-empty" role="status">No named findings match. Clear the search or change the round.</p>';
  }
  function catalog() {
    const rounds=[...new Set(contributions.map(item=>String(item.round)))];
    const selected=location.hash.match(/[?&]finding=([^&]+)/);let query='';if(selected){try{query=decodeURIComponent(selected[1]);}catch{}}
    return `<header class="r22-page-head"><p class="rc-kicker">${contributions.length} contribution aliases · ${array(registry.equations).length} equation records · ${array(registry.quantities).length} named quantities · ${array(registry.statements).length} statement aliases</p><h1>The Hruday / HNM research catalog.</h1><p>Current project names sit beside the original labels. Search by either name, browse by round, and open the underlying derivation. These are overlapping documentation records, not a count of independent discoveries.</p></header>${namingNote()}${registry.statement_policy?`<p class="r29-muted">${esc(registry.statement_policy)}</p>`:''}<section class="r29-source-controls" aria-label="Filter HNM findings"><label>Find a contribution<input id="r29-finding-search" type="search" value="${esc(query)}" placeholder="Try Wilson, endpoint, HNM, AL1…"></label><label>Research round<select id="r29-finding-round"><option value="all">All rounds</option>${rounds.map(round=>`<option value="${esc(round)}">Round ${esc(round)}</option>`).join('')}</select></label><button id="r29-finding-reset" type="button">Reset</button></section><p id="r29-finding-count" class="r29-muted" role="status"></p><section id="r29-finding-cards" class="r29-source-grid">${findingCards(query)}</section><section class="rc-section"><h2>Quantities and variable aliases</h2><p>Aliases identify quantities used in this workbench. Standard mathematical symbols and physical dimensions retain their definitions.</p><div class="r29-table-wrap"><table class="r29-table"><thead><tr><th scope="col">HNM name</th><th scope="col">Symbol / definition</th><th scope="col">Scope</th></tr></thead><tbody>${array(registry.quantities).map(item=>`<tr><th scope="row">${esc(item.display_name??item.name??item.id)}</th><td><code>${esc(item.symbol??item.legacy_symbol??'')}</code><br>${esc(item.definition??'')}${item.units?`<small>Units: ${esc(item.units)}</small>`:''}</td><td>${esc(item.scope??item.limitation??'See the cited research definition.')}</td></tr>`).join('')}</tbody></table></div><p><a href="hnm-registry.json" download>Download the complete naming registry (JSON)</a> · ${source({path:D.registry_source,title:'Registry and naming policy'})}</p></section>`;
  }
  function drafts() {
    const ready=safeURL(D.addendum?.url,true);
    return `<header class="r22-page-head"><p class="rc-kicker">Complete manuscript · Draft02</p><h1>The whole research record.<br>With the new names and addenda.</h1><p>Human author: <strong>${esc(D.author)}</strong>. The current manuscript integrates the earlier work, Rounds 27–29, HNM contribution and equation aliases, derivations, applications, limitations and the next roadmap.</p></header><section class="r29-draft-feature"><div><p class="rc-kicker">Current edition</p><h2>HNM gauge research</h2><p>Begin with the scope statement, then use the ranked contributions and the appendix to follow an equation back to its source-bound review.</p>${ready?`<div class="r29-home-actions"><a class="r29-primary" href="${esc(ready)}">Read Draft02 PDF ↗</a><a href="${esc(ready)}" download>Download the draft</a></div>`:'<p>The full PDF is being assembled for this active checkpoint.</p>'}<p>${source({path:'papers/draft-02',title:'LaTeX, registry and derivation sources'})}</p></div><aside><strong>Hruday N M</strong><span>BUNZEEY</span><hr><p>Project contribution labels<br>Priority unverified<br>Continuum problem open</p></aside></section>${namingNote()}${ready?`<details class="drafts-reader"><summary>Read the current PDF on this page</summary><p><a href="${esc(ready)}">Open the PDF directly</a> if this browser does not show the reader.</p><iframe title="Complete HNM research manuscript Draft02" src="${esc(ready)}#view=FitH" loading="lazy"></iframe></details>`:''}<section class="rc-section"><h2>Preserved earlier editions</h2><p>Earlier files preserve the names, author placeholders and research scope recorded when they were produced. The current HNM registry provides the new aliases.</p><div class="r29-table-wrap"><table class="r29-table"><thead><tr><th scope="col">Edition</th><th scope="col">Coverage</th><th scope="col">Read</th></tr></thead><tbody><tr><th scope="row">Draft01</th><td>Rounds 3–26 · original 92-page snapshot</td><td><a href="ym-draft-01.pdf">PDF</a> · <a href="ym-draft-01-source.zip">Sources</a></td></tr><tr><th scope="row">Round27 addendum</th><td>Historical-source survey and three investigations</td><td><a href="ym-round27-addendum.pdf">PDF</a></td></tr><tr><th scope="row">Round28 addendum</th><td>Five paired goals · ten reviewed investigations</td><td><a href="ym-round28-addendum.pdf">PDF</a></td></tr></tbody></table></div></section><p><a href="#research/hnm-findings">Search the full HNM catalog →</a> · <a href="#research/sharing">Read the prepared share posts →</a></p>`;
  }
  function sharing() { return `<header class="r22-page-head"><p class="rc-kicker">Drafts to share · ${esc(D.author)}</p><h1>The result, the derivation, and the open question.</h1><p>Prepared posts link readers to the complete draft and reproducible research. They are drafts for you to publish.</p></header><div class="r29-reader-paths r29-share-paths"><a href="https://github.com/occult-kranti/yang_mills_workbench/blob/main/research/round29/sharing/substack.md"><span>Long form</span><h2>Substack draft</h2><p>The research story, a scoped result, its derivation and the next question.</p><strong>Read the post ↗</strong></a><a href="https://github.com/occult-kranti/yang_mills_workbench/blob/main/research/round29/sharing/reddit.md"><span>Discussion</span><h2>Reddit draft</h2><p>A concise technical account with code, draft and website links.</p><strong>Read the post ↗</strong></a></div>${namingNote()}`; }
  function equations(values) {
    return array(values).length ? `<section class="r29-equations"><h2>Equations from the reviewed derivation</h2>${values.map(item => `<figure>${item.label ? `<figcaption>${esc(item.label)}</figcaption>` : ''}<pre><code>${esc(typeof item === 'string' ? item : item.expression ?? '')}</code></pre>${item.scope ? `<p>${esc(item.scope)}</p>` : ''}</figure>`).join('')}</section>` : '';
  }
  function loopPage(loop) {
    const complete = reviewed(loop);
    return `<header class="r22-page-head"><p class="rc-kicker">Round29 · ${esc(id(loop.id).toUpperCase())}</p><h1>${esc(loop.title ?? loop.id)}</h1>${badge(loop)}${complete ? `<p>${esc(loop.accepted)}</p>` : '<p>No reviewed finding is recorded for this investigation yet.</p>'}</header>${complete ? `${loop.model ? `<p class="r29-model"><strong>Model:</strong> ${esc(loop.model)}</p>` : ''}${array(loop.bullets).length ? `<section class="rc-section"><h2>What this result establishes</h2>${list(loop.bullets)}</section>` : ''}${equations(loop.equations)}${array(loop.derivation_steps).length ? `<section class="rc-section"><h2>Derivation and checks</h2>${list(loop.derivation_steps)}</section>` : ''}${array(loop.applications).length ? `<section class="rc-section"><h2>Possible applications</h2>${list(loop.applications)}</section>` : ''}<section class="r29-scope"><h2>${array(loop.current_extensions).length?'Conditions and limits recorded for this investigation':'Limitations and remaining conditions'}</h2>${list(loop.limitations)}</section>${currentExtensions(loop)}${namedStatements(loop)}` : ''}<section class="rc-section"><h2>${complete ? 'Derivation and review records' : 'Selected question'}</h2>${sourceList(loop.sources)}</section><p>${link('round29-results','Back to all Round29 investigations →')} · ${link('research-network','Explore research dependencies →')}</p>`;
  }
  function results() {
    const c = counts();
    return `<header class="r22-page-head"><p class="rc-kicker">Round29 · ${c.completed} reviewed / ${c.requested ?? '—'} requested investigations</p><h1>The finding, the scope, the evidence.</h1><p>Each card keeps its review verdict and limitation beside its result. Selected investigations remain pending until a final review is recorded.</p></header><div class="r29-grid">${loops.map(loopCard).join('')}</div>${assessment(true)}`;
  }
  function filterSources(query = '', lens = 'all', category = 'all') {
    const needle = String(query).trim().toLowerCase();
    return array(D.survey?.records).filter(item => (lens === 'all' || item.lens === lens) && (category === 'all' || item.category === category) && [item.title,item.lens,item.category,item.depth,item.use,item.limits,item.change_status].join(' ').toLowerCase().includes(needle));
  }
  function sourceCards(query = '', lens = 'all', category = 'all') {
    const records = filterSources(query,lens,category);
    if (!records.length) return '<p class="r29-empty" role="status">No reading records match. Clear the search or change a filter.</p>';
    return records.map(item => `<article class="r29-source-card"><p class="rc-kicker">${esc(lensNames[item.lens] ?? item.lens)} · ${esc(categoryNames[item.category] ?? item.category)}</p><h2>${esc(item.title)}</h2><p class="r29-reading-depth"><strong>Reading depth:</strong> ${esc(item.depth)}</p><div class="r29-source-links">${array(item.urls).map((url, index) => source({url,title:array(item.urls).length === 1 ? 'Open source' : `Source link ${index + 1}`})).join('')}</div><details><summary>Use, limits and earlier reading</summary>${item.use ? `<p><strong>Use:</strong> ${esc(item.use)}</p>` : ''}${item.limits ? `<p><strong>Limit:</strong> ${esc(item.limits)}</p>` : ''}${item.change_status ? `<p><strong>Reading status:</strong> ${esc(item.change_status.replaceAll('_',' '))}</p>` : ''}${item.change_basis ? `<p>${esc(item.change_basis)}</p>` : ''}${item.ledger ? `<p>${source({path:item.ledger,title:'Attributed reading record'})}</p>` : ''}</details></article>`).join('');
  }
  function survey() {
    const s = D.survey ?? {}, records = array(s.records), lenses = [...new Set(records.map(item => item.lens))], categories = [...new Set(records.map(item => item.category))];
    const distinctURLs = new Set(records.flatMap(item => array(item.urls))).size;
    const allInspectedURLs = new Set([...records.flatMap(item => array(item.urls)), ...array(s.screening).map(item => item.url)]).size;
    return `<header class="r22-page-head"><p class="rc-kicker">Current primary research · source provenance</p><h1>Read the sources with their limits attached.</h1><p>This round checks the Clay problem statement, Gauvin v3 and selected primary research. Earlier historical, patent and conversation readings remain in the Round28 archive. This is a targeted comparison by model agents, not an exhaustive literature review or external human peer review.</p></header><dl class="r29-survey-counts"><div><dt>Reading records</dt><dd>${records.length}</dd></div><div><dt>Distinct recorded URLs</dt><dd>${distinctURLs}</dd></div><div><dt>Additional screening records</dt><dd>${array(s.screening).length}</dd></div><div><dt>URLs including screening</dt><dd>${allInspectedURLs}</dd></div></dl><p class="r29-muted">Reading records include repeated readings and bibliographic metadata checks. They are not a count of distinct studies. A record may cover only an abstract or selected passages; source counts do not count full books, proofs or research loops. Unopened leads stay outside these reading and screening totals.</p><section class="r29-source-controls" aria-label="Filter source readings"><label>Search readings<input id="r29-source-search" type="search" placeholder="Try noise, fluxions, spin networks…"></label><label>Research perspective<select id="r29-source-lens"><option value="all">All perspectives</option>${lenses.map(lens => `<option value="${esc(lens)}">${esc(lensNames[lens] ?? lens)}</option>`).join('')}</select></label><label>Source category<select id="r29-source-category"><option value="all">All categories</option>${categories.map(category => `<option value="${esc(category)}">${esc(categoryNames[category] ?? category)}</option>`).join('')}</select></label><button id="r29-source-reset" type="button">Reset filters</button></section><p id="r29-source-count" class="r29-muted" role="status">${records.length} reading records shown.</p><section id="r29-source-cards" class="r29-source-grid" aria-label="Matching reading records">${sourceCards()}</section>${array(s.screening).length ? `<details class="r29-survey-notes"><summary>Additional screening and reopened sources</summary><p>These records are separate from the formal reading count.</p>${array(s.screening).map(item => `<article><h3>${source({url:item.url,title:item.id ?? item.url})}</h3><p>${esc(item.reading_depth)}</p><p>${esc(item.use ?? item.status ?? '')}</p></article>`).join('')}</details>` : ''}${array(s.unread_leads).length ? `<details class="r29-survey-notes"><summary>Unopened leads · excluded from reading and screening counts</summary>${s.unread_leads.map(item => `<article><h3>${source({url:item.url,title:item.id ?? item.url})}</h3><p>${esc(item.reading_depth)}</p><p>${esc(item.context ?? '')}</p></article>`).join('')}</details>` : ''}${array(s.discrepancies).length ? `<details class="r29-survey-notes"><summary>Bibliographic discrepancies and corrections</summary>${s.discrepancies.map(item => `<article><p><strong>${esc(item.record_id ?? array(item.record_ids).join(', '))}:</strong> ${esc(item.issue)}</p><p>${esc(item.resolution)}</p></article>`).join('')}</details>` : ''}<section class="r29-scope"><h2>Scope recorded at the survey checkpoint</h2>${list(s.interpretation_limits)}${s.government_context?.scope ? `<p>${esc(s.government_context.scope)}</p>` : ''}${sourceList(s.sources)}<p><a href="#research/round28-sources">Historical and broader Round28 source survey →</a></p></section>`;
  }
  function proof() {
    const obligations = array(D.progress?.obligations);
    return `<header class="r22-page-head"><p class="rc-kicker">Proof obligations · panel assessment</p><h1>What the remaining proof requires.</h1><p>${esc(D.progress?.percentage_statement ?? 'No current assessment has been recorded.')}</p></header>${stateRoutes()}${obligations.length ? `<div class="r29-table-wrap" tabindex="0" role="region" aria-label="Outstanding proof obligations"><table class="r29-table"><caption>Round29 assessment at the stated model and scale</caption><thead><tr><th scope="col">Obligation</th><th scope="col">Current status</th><th scope="col">Missing input</th></tr></thead><tbody>${obligations.map(item => `<tr><th scope="row">${esc(item.name)}</th><td>${esc(item.status)}</td><td>${Array.isArray(item.missing) ? list(item.missing) : esc(item.missing)}</td></tr>`).join('')}</tbody></table></div>` : '<p>A revised obligation table has not been recorded for this active cycle.</p>'}<p>${link('round29-roadmap','Review the proposed next goals →')} · ${link('round27-proof','Read the previous panel assessment →')}</p>`;
  }
  function roadmap() {
    const goals = array(D.roadmap?.next_goals);
    return `<header class="r22-page-head"><p class="rc-kicker">Reviewed continuation · planned work</p><h1>The next question follows the remaining premise.</h1><p>${esc(D.roadmap?.summary ?? (goals.length ? 'These priorities follow the completed review. Future investigations have not started; each second loop will be selected after its first review.' : 'The current pairs and selected investigations are shown below. Later goals will be added after the required reviews.'))}</p></header>${goals.length ? `<div class="r29-grid">${goals.map(goal => `<article class="rc-result"><p class="rc-kicker">${esc(goal.id)} · planned</p><h2>${esc(goal.title)}</h2><p>${esc(goal.target ?? goal.first_target ?? '')}</p>${goal.missing_premise ? `<p><strong>Missing input:</strong> ${esc(goal.missing_premise)}</p>` : ''}${goal.proposed_first_loop_test ? `<details><summary>Proposed first investigation</summary><p>${esc(goal.proposed_first_loop_test)}</p>${goal.exact_model ? `<p><strong>Model:</strong> ${esc(goal.exact_model)}</p>` : ''}${goal.reason_for_rank ? `<p><strong>Priority:</strong> ${esc(goal.reason_for_rank)}</p>` : ''}</details>` : ''}${list(goal.limitations)}${sourceList(goal.sources)}</article>`).join('')}</div>` : '<p class="r29-muted">No post-cycle research goals have been recorded yet.</p>'}<section><h2>Current goal pairs</h2>${pairCards()}</section><p>${link('round29-proof','Inspect the remaining proof obligations →')}</p>`;
  }
  function addendumCard() {
    const a = D.addendum, url = safeURL(a?.url, true);
    if (!url) return '<p class="r29-muted">The Round29 addendum is not available in this checkpoint.</p>';
    return `<article class="r29-addendum-card"><p class="rc-kicker">Round29 manuscript addendum</p><h2>${esc(a.title ?? 'Round29 research addendum')}</h2>${a.summary ? `<p>${esc(a.summary)}</p>` : ''}<p><a href="${esc(url)}">Read the addendum ↗</a></p>${a.sources ? sourceList(a.sources) : ''}</article>`;
  }
  function addendum() {
    return `<header class="r22-page-head"><p class="rc-kicker">Research manuscripts</p><h1>The Round29 findings in the complete draft.</h1><p>Use the addendum with each result’s derivation and review. The complete Draft02 includes the latest addendum; earlier editions preserve their original scope.</p></header>${addendumCard()}<section class="rc-section"><h2>Earlier manuscripts</h2><p>${link('drafts','Read the complete current draft and earlier editions →')} · ${link('round29-results','Inspect the current findings →')}</p></section>`;
  }
  function nodeStatus(node) {
    if (node.kind === 'literature' || node.kind === 'source' || node.status === 'source-reviewed') return {name:'Source reviewed · not a physics premise',css:'source'};
    const status = String(node.status ?? 'planned').toLowerCase();
    if (/limited|insufficient|reject|fail/.test(status)) return {name:'Limited result',css:'limited'};
    if (/conditional/.test(status)) return {name:'Conditional',css:'conditional'};
    if (/proved|accepted/.test(status)) return {name:'Proved within stated model',css:'accepted'};
    if (/planned|open|unexecuted/.test(status)) return {name:'Planned / open',css:'pending'};
    return {name:String(node.status ?? 'Unclassified'),css:'pending'};
  }
  const nodeBadge = node => { const status=nodeStatus(node); return `<span class="r29-badge r29-badge-${status.css}">${esc(status.name)}</span>`; };
  function validEdges() { return networkEdges.filter(edge => nodeById.has(String(edge.from)) && nodeById.has(String(edge.to)) && edgeNames[edge.type]); }
  function filterNodes(query = '',kind = 'all') {
    const needle=String(query).trim().toLowerCase();
    return networkNodes.filter(node => (kind === 'all' || node.kind === kind) && [node.id,node.title,node.legacy_title,node.summary,node.detail,node.model,node.equation].join(' ').toLowerCase().includes(needle));
  }
  function neighborhood(selected, type = 'all') {
    if (!nodeById.has(String(selected))) return {nodes:[],edges:[]};
    const edges=validEdges().filter(edge => (type === 'all' || type === edge.type) && (String(edge.from) === String(selected) || String(edge.to) === String(selected)));
    const ids=new Set([String(selected)]);
    edges.forEach(edge => {ids.add(String(edge.from));ids.add(String(edge.to));});
    return {nodes:networkNodes.filter(node => ids.has(String(node.id))),edges};
  }
  function networkInitial() {
    const last=[...reviewedLoops()].reverse().map(loop => networkNodes.find(node => node.route === 'round29-' + loop.id)).find(Boolean);
    return String(last?.id ?? networkNodes[0]?.id ?? '');
  }
  function networkCatalog(query='',kind='all',selected='') {
    const nodes=filterNodes(query,kind);
    if (!nodes.length) return '<p class="r29-empty">No entries match the current search.</p>';
    const kinds=[...new Set(networkNodes.map(node=>node.kind))];
    return kinds.map(value=>{const group=nodes.filter(node=>node.kind===value);return group.length ? `<section><h3>${esc(kindNames[value] ?? value ?? 'Other entries')} <span>${group.length}</span></h3><ul>${group.map(node=>`<li><button type="button" data-r29-node="${esc(node.id)}" aria-pressed="${String(node.id)===String(selected)}"><span>${esc(node.title)}</span><small>${esc(nodeStatus(node).name)}</small></button></li>`).join('')}</ul></section>` : '';}).join('');
  }
  function networkMap(selected,type='all') {
    const local=neighborhood(selected,type);
    if (!local.nodes.length) return '<p class="r29-empty">Select an entry from the research catalog.</p>';
    const incoming=new Set(local.edges.filter(edge=>String(edge.to)===String(selected)).map(edge=>String(edge.from)));
    const left=local.nodes.filter(node=>String(node.id)!==String(selected)&&incoming.has(String(node.id)));
    const right=local.nodes.filter(node=>String(node.id)!==String(selected)&&!incoming.has(String(node.id)));
    const rows=Math.max(1,left.length,right.length),height=Math.max(245,rows*116+70),width=990;
    const positions=new Map([[String(selected),{x:366,y:Math.max(62,Math.floor((rows-1)/2)*116+62)}]]);
    left.forEach((node,index)=>positions.set(String(node.id),{x:24,y:62+index*116}));
    right.forEach((node,index)=>positions.set(String(node.id),{x:708,y:62+index*116}));
    const paths=local.edges.map(edge=>{
      const a=positions.get(String(edge.from)),b=positions.get(String(edge.to));
      if(String(edge.from)===String(edge.to))return '';
      const forward=a.x<b.x,ax=a.x+(forward?258:0),bx=b.x+(forward?0:258),middle=(ax+bx)/2;
      return `<path class="r29-net-edge r29-net-edge-${edge.type}" d="M ${ax} ${a.y+44} C ${middle} ${a.y+44}, ${middle} ${b.y+44}, ${bx} ${b.y+44}" marker-end="url(#r29-arrow-${edge.type})"><title>${esc(nodeById.get(String(edge.from)).title)} → ${esc(nodeById.get(String(edge.to)).title)}: ${esc(edge.label ?? edgeNames[edge.type])}</title></path>`;
    }).join('');
    return `<div class="r29-map-scroll" tabindex="0" role="region" aria-label="Selected entry and its direct incoming and outgoing relations"><div class="r29-map-canvas" style="width:${width}px;height:${height}px"><svg width="${width}" height="${height}" aria-hidden="true" focusable="false"><defs>${Object.keys(edgeNames).map(type=>`<marker id="r29-arrow-${type}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>`).join('')}</defs>${paths}</svg>${['Incoming relations','Selected entry','Outgoing relations'].map((name,i)=>`<span class="r29-map-label" style="left:${24+i*342}px">${name}</span>`).join('')}${local.nodes.map(node=>{const p=positions.get(String(node.id));return `<button type="button" class="r29-map-node r29-map-node-${nodeStatus(node).css}" data-r29-node="${esc(node.id)}" aria-pressed="${String(node.id)===String(selected)}" style="left:${p.x}px;top:${p.y}px"><span>${esc(node.title)}</span><small>${esc(['literature','source'].includes(node.kind)?'Literature · source reviewed':nodeStatus(node).name)}</small></button>`;}).join('')}</div></div>`;
  }
  function nodeAliases(node) {
    const ids=[...new Set([...array(node.hnm_aliases),node.hnm_alias].filter(value=>typeof value==='string'&&value))];
    return ids.length ? `<p class="r29-equation-tags r29-node-aliases"><strong>Current identifiers:</strong> ${ids.map(alias=>{const entry=contributions.find(item=>item.id===alias);return entry?`<a href="#research/hnm-findings?finding=${encodeURIComponent(alias)}">${esc(alias)}</a>`:`<span>${esc(alias)} · graph locator</span>`;}).join(' ')}</p>` : '';
  }
  function networkDetails(selected,type='all') {
    const node=nodeById.get(String(selected));
    if(!node)return '<p>Select an entry from the research catalog.</p>';
    const local=neighborhood(selected,type);
    return `<header><p class="rc-kicker">${esc(kindNames[node.kind]??node.kind)} · ${esc(node.id)}</p><h2 id="r29-network-selected">${esc(node.title)}</h2>${nodeBadge(node)}</header>${nodeAliases(node)}${node.legacy_title?`<p class="r29-muted"><strong>Original label:</strong> ${esc(node.legacy_title)}</p>`:''}${node.model?`<p class="r29-model">${esc(node.model)}</p>`:''}<p>${esc(node.summary??'')}</p>${node.detail?`<p class="r29-node-detail">${esc(node.detail)}</p>`:''}${node.equation?`<pre><code>${esc(node.equation)}</code></pre>`:''}${sourceList(node.sources)}${node.route?`<p>${link(node.route,'Read the complete record →')}</p>`:''}<h3>Direct relations · ${local.edges.length}</h3>${local.edges.length?`<ul class="r29-network-connections">${local.edges.map(edge=>{const outgoing=String(edge.from)===String(selected),other=nodeById.get(String(outgoing?edge.to:edge.from));return `<li><span class="r29-edge-label r29-edge-label-${edge.type}">${edgeNames[edge.type]}</span><p class="r29-relation-direction">${outgoing?'Outgoing relation to':'Incoming relation from'}</p><button type="button" data-r29-node="${esc(other.id)}">${esc(other.title)}</button>${edge.label?`<p>${esc(edge.label)}</p>`:''}${edge.detail?`<p>${esc(edge.detail)}</p>`:''}</li>`;}).join('')}</ul>`:'<p>No direct relations match this connection filter.</p>'}`;
  }
  function network() {
    const selected=networkInitial(),kinds=[...new Set(networkNodes.map(node=>node.kind))];
    return `<header class="r22-page-head"><p class="rc-kicker">${networkNodes.length} research and source entries · ${validEdges().length} recorded relations</p><h1>Trace the result. Inspect every relation.</h1><p>Choose a research result or source to inspect its direct relations. Literature comparisons and proposed transfers carry their own labels; a source-review entry is not a proved physical premise.</p></header><section class="r29-network-legend"><div>${Object.entries(edgeNames).map(([type,name])=>`<span class="r29-edge-label r29-edge-label-${type}">${name}</span>`).join('')}</div><p>The counts describe this research index, not vertices, links or states of a physical gauge graph. Position and distance in the map have no physical meaning. Read each relation label for its precise role.</p></section><section class="r29-source-controls" aria-label="Filter the research network"><label>Search all entries<input id="r29-network-search" type="search" placeholder="Try HNM, AL1, homogeneous, literature…"></label><label>Entry kind<select id="r29-network-kind"><option value="all">All kinds</option>${kinds.map(kind=>`<option value="${esc(kind)}">${esc(kindNames[kind]??kind)}</option>`).join('')}</select></label><label>Relation type<select id="r29-network-edge"><option value="all">All relations</option>${Object.entries(edgeNames).map(([type,name])=>`<option value="${type}">${name}</option>`).join('')}</select></label><button id="r29-network-reset" type="button">Reset filters</button></section><p class="r29-muted" id="r29-network-count" role="status">${networkNodes.length} entries in the catalog.</p><section class="r29-network-map-section"><div class="r29-section-head"><h2>One step around the selected entry</h2><button id="r29-network-map-toggle" type="button" aria-controls="r29-network-map" aria-expanded="true">Hide visual map</button></div><div id="r29-network-map">${networkMap(selected)}</div></section><div class="r29-network-layout"><aside class="r29-network-catalog" aria-label="All matching research and source entries"><h2>Research catalog</h2><div id="r29-network-catalog">${networkCatalog('','all',selected)}</div></aside><section id="r29-network-details" class="r29-network-details" aria-labelledby="r29-network-selected">${networkDetails(selected)}</section></div>`;
  }
  function render(value = 'home') {
    const route = normalizeRoute(value);
    if (route === 'round28-home') return `<div class="rc-history-notice">Archived Round27 checkpoint. ${link('home','Current findings →')}</div>` + prior.render('home');

    if (route === 'all-results' || route === 'contributions') return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r29"><section class="r29-reading-callout"><div><p class="rc-kicker">Current continuation</p><h2>Round29 · ${counts().completed} reviewed investigations</h2><p>Read the current results with their scope and limitations. Earlier round records remain below.</p></div>${link('round29-results','Read the Round29 results →')}</section></div>` + prior.render(value);
    if (!own.has(route)) return `<div class="r29 r29-history-banner"><p><strong>${esc(D.author)}</strong> · Earlier research view. <a href="#research/hnm-findings">Current HNM names and complete catalog →</a></p></div>` + aliasNotice(route) + prior.render(value);
    const loop = byRoute.get(route);
    const body = route === 'hnm-findings' ? catalog() : route === 'hnm-priorities' ? priorities() : route === 'drafts' ? drafts() : route === 'sharing' ? sharing() : loop ? loopPage(loop) : route === 'research-network' ? network() : route === 'round29-results' ? results() : route === 'round29-sources' ? survey() : route === 'round29-proof' ? proof() : route === 'round29-roadmap' ? roadmap() : route === 'round29-addendum' ? addendum() : home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r29">${nav(route)}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · ${esc(D.author)}</strong>${link('round29-proof','Proof obligations')}${link('round29-sources','Source survey')}${link('round28-home','Round28 archive')}${link('all-results','All recorded rounds')}</footer></div>`;
  }
  function afterRender() {
    const route = normalizeRoute(location.hash.replace(/^#research\/?/, '') || 'home');
    if (route === 'round28-home') { window.ResearchJourney?.cleanup?.(); document.title = 'Round28 archive · Yang–Mills Workbench'; return; }
    if (!own.has(route)) return prior.afterRender();
    window.ResearchJourney?.cleanup?.();
    const names = {'home':'HNM Research home','hnm-findings':'HNM research catalog','hnm-priorities':'Ranked HNM findings','drafts':'Complete HNM draft','sharing':'Substack and Reddit drafts','research-network':'Research and source network','round29-results':'Round29 results','round29-sources':'Round29 source survey','round29-proof':'Round29 proof obligations','round29-roadmap':'Round29 next goals','round29-addendum':'Round29 research addendum'};
    document.title = `${byRoute.get(route)?.title ?? names[route] ?? 'Round29'} · Yang–Mills Workbench`;
    if (route === 'hnm-findings') {
      const get=name=>document.getElementById(name); const search=get('r29-finding-search'),round=get('r29-finding-round'),cards=get('r29-finding-cards'),count=get('r29-finding-count'),reset=get('r29-finding-reset');
      if(!search||!round||!cards||!count||!reset)return;
      const update=()=>{cards.innerHTML=findingCards(search.value,round.value);count.textContent=`${contributions.filter(item=>matchesFinding(item,search.value,round.value)).length} of ${contributions.length} named contributions shown.`;};
      search.addEventListener('input',update);round.addEventListener('change',update);reset.addEventListener('click',()=>{search.value='';round.value='all';update();search.focus();});update();return;
    }
    if (route === 'research-network') {
      const get=name=>document.getElementById(name);
      const search=get('r29-network-search'),kind=get('r29-network-kind'),edge=get('r29-network-edge'),catalog=get('r29-network-catalog'),details=get('r29-network-details'),map=get('r29-network-map'),count=get('r29-network-count'),reset=get('r29-network-reset'),toggle=get('r29-network-map-toggle');
      if(!search||!kind||!edge||!catalog||!details||!map||!count||!reset||!toggle)return;
      let selected=networkInitial();
      const target=location.hash.match(/(?:\?|&)node=([^&]*)/);
      if(target){try{const decoded=decodeURIComponent(target[1]);if(nodeById.has(decoded))selected=decoded;}catch{}}
      const draw=()=>{catalog.innerHTML=networkCatalog(search.value,kind.value,selected);details.innerHTML=networkDetails(selected,edge.value);map.innerHTML=networkMap(selected,edge.value);};
      const filter=()=>{const found=filterNodes(search.value,kind.value);if(found.length&&!found.some(node=>String(node.id)===selected))selected=String(found[0].id);count.textContent=`${found.length} of ${networkNodes.length} catalog entries match. The map retains direct neighbors as context.`;draw();};
      const select=event=>{const button=event.target.closest?.('button[data-r29-node]'),target=button?.getAttribute('data-r29-node');if(!target||!nodeById.has(target))return;selected=target;draw();const heading=get('r29-network-selected');heading?.setAttribute?.('tabindex','-1');heading?.focus?.({preventScroll:true});};
      for(const host of [catalog,details,map])host.addEventListener('click',select);
      search.addEventListener('input',filter);kind.addEventListener('change',filter);edge.addEventListener('change',draw);
      reset.addEventListener('click',()=>{search.value='';kind.value='all';edge.value='all';selected=networkInitial();filter();});
      toggle.addEventListener('click',()=>{map.hidden=!map.hidden;toggle.setAttribute('aria-expanded',String(!map.hidden));toggle.textContent=map.hidden?'Show visual map':'Hide visual map';});
      draw();return;
    }
    if (route !== 'round29-sources') return;
    const get = name => document.getElementById(name);
    const search = get('r29-source-search'), lens = get('r29-source-lens'), category = get('r29-source-category'), reset = get('r29-source-reset'), cards = get('r29-source-cards'), count = get('r29-source-count');
    if (!search || !lens || !category || !reset || !cards || !count) return;
    const update = () => { const found = filterSources(search.value,lens.value,category.value); cards.innerHTML = sourceCards(search.value,lens.value,category.value); count.textContent = `${found.length} of ${array(D.survey?.records).length} reading records shown.`; };
    search.addEventListener('input',update); lens.addEventListener('change',update); category.addEventListener('change',update);
    reset.addEventListener('click',() => { search.value=''; lens.value='all'; category.value='all'; update(); search.focus(); });
    update();
  }
  window.ResearchRound29 = {render,afterRender,counts,reviewed,safePath,safeURL,source,normalizeRoute,routeAliases,aliasNotice,ranked,priorityTable,matchesFinding,findingCards,filterSources,sourceCards,filterNodes,neighborhood,networkCatalog,networkMap,nodeAliases,networkDetails,nodeStatus,validEdges,data:D};
  window.ResearchObservatory = {...prior,render,afterRender};
})();
