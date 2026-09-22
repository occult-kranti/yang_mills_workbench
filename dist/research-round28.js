/* Additive Round28 pages. Only reviewed, source-bound records render as findings. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND28_DATA;
  if (!prior || !D) return;
  const array = value => Array.isArray(value) ? value : [];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const id = value => String(value ?? '').toLowerCase();
  const validId = value => /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(String(value));
  const list = values => array(values).length ? `<ul>${values.map(value => `<li>${esc(value)}</li>`).join('')}</ul>` : '';
  const loops = array(D.loops), byRoute = new Map(loops.filter(loop => validId(loop.id)).map(loop => ['round28-' + loop.id, loop]));
  const own = new Set(['home','round28','round28-results','round28-sources','round28-roadmap','round28-proof','round28-addendum', ...byRoute.keys()]);
  if (D.network) own.add('research-network');
  const networkNodes = array(D.network?.nodes), networkEdges = array(D.network?.edges);
  const nodeById = new Map(networkNodes.map(node => [String(node.id),node]));
  const kindNames = {history:'Earlier findings',premise:'Required premises',equation:'Equations',loop:'Research loops',open:'Open targets',literature:'Literature and historical sources'};
  const edgeNames = {'proven-dependency':'Verified source dependency','proposed-transfer':'Proposed transfer or scope comparison','review-selection':'Review selection or methodological comparison'};
  const lensNames = {newton:'Newton',tesla:'Tesla',jung:'Jung / Pauli',penrose:'Penrose',feynman:'Feynman',skeptic:'Skeptic'};
  const categoryNames = {historical_primary:'Historical primary source',technical_primary:'Modern primary research',patent_primary:'Patent',bibliographic_primary:'Bibliographic metadata',forum_discourse:'Forum discussion',official_problem_reference:'Official problem statement'};
  function normalizeRoute(value) {
    let route = String(value ?? 'home').split('?')[0] || 'home';
    if (route === 'round28' && location.hash.startsWith('#research/round28/')) route = location.hash.slice('#research/'.length).split('?')[0];
    if (route.startsWith('round28/')) {
      const tail = route.slice('round28/'.length);
      const aliases = {home:'round28',loops:'round28-results',results:'round28-results',sources:'round28-sources',roadmap:'round28-roadmap',proof:'round28-proof',addendum:'round28-addendum'};
      route = aliases[tail] ?? 'round28-' + tail;
    }
    return route;
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
  const sourceList = values => array(values).length ? `<ul class="r28-evidence">${values.map(value => `<li>${source(value)}</li>`).join('')}</ul>` : '<p class="r28-muted">No sources are attached to this record.</p>';
  const reviewed = loop => loop.stage === 'reviewed' && /^[a-f0-9]{64}$/.test(String(loop.gate_sha256)) && typeof loop.accepted === 'string' && loop.accepted.length > 0 && /^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])/.test(String(loop.verdict));
  const reviewedLoops = () => loops.filter(reviewed);
  const requested = () => Number.isInteger(D.progress?.requested) && D.progress.requested > 0 ? D.progress.requested : null;
  function counts() { return {completed:reviewedLoops().length, selected:loops.length, requested:requested(), remaining:requested() === null ? null : Math.max(0, requested() - reviewedLoops().length)}; }
  function badge(loop) {
    const status = reviewed(loop) ? /limited|insufficient|reject|fail/.test(loop.verdict) ? 'limited' : /conditional/.test(loop.verdict) ? 'conditional' : 'accepted' : 'pending';
    const label = reviewed(loop) ? String(loop.verdict).replaceAll('_',' ') : loop.stage === 'in-progress' ? 'In progress · review pending' : 'Selected · review pending';
    return `<span class="r28-badge r28-badge-${status}">${esc(label)}</span>`;
  }
  function nav(route) {
    return `<nav class="rc-nav" aria-label="Research navigation">${[['home','Current findings'],['round28-results','Loop results'],['round28-sources','Source survey'],['research-network','Research network'],['round28-roadmap','Next goals'],['round28-addendum','Round28 addendum'],['drafts','Earlier drafts']].map(([target,label]) => `<a href="#research/${target}"${target === route || target === 'home' && route === 'round28' ? ' aria-current="page"' : ''}>${label}</a>`).join('')}</nav>`;
  }
  function assessment(compact = false) {
    return `<section class="r28-scope"><p class="rc-kicker">Proof progress</p><h2>Research progress and proof completion are different counts.</h2><p>${esc(D.progress?.percentage_statement ?? 'No new proof-completion assessment is recorded.')}</p>${compact ? '' : '<p class="r28-muted">An executed investigation may have a limited or insufficient outcome. It does not represent a fixed fraction of a Yang–Mills existence and mass-gap proof.</p>'}<p>${link('round28-proof','Inspect the outstanding proof obligations →')}</p></section>`;
  }
  function loopCard(loop, number) {
    const complete = reviewed(loop);
    return `<article class="rc-result r28-loop-card"><div class="r28-card-top"><p class="rc-kicker">${number + 1} · ${esc(id(loop.id).toUpperCase())}${loop.goal ? ' · ' + esc(loop.goal) : ''}</p>${badge(loop)}</div><h2>${esc(loop.title ?? id(loop.id).toUpperCase())}</h2><p>${complete ? esc(loop.accepted) : 'This investigation has been selected. Its findings will appear after the review is complete.'}</p>${complete && array(loop.limitations).length ? `<p class="r28-card-limit"><strong>Limit:</strong> ${esc(loop.limitations[0])}</p>` : ''}<p>${link('round28-' + loop.id,complete ? 'Read result and evidence →' : 'View the selected investigation →')}</p></article>`;
  }
  function pairCards() {
    const pairs = array(D.goal_pairs), acceptedIds = new Set(reviewedLoops().map(loop => loop.id)), selectedIds = new Set(loops.map(loop => loop.id));
    return `<div class="r28-pairs">${pairs.map(pair => `<article><p class="rc-kicker">Goal ${esc(pair.id)}</p><h3>${esc(pair.target || pair.id)}</h3><ul>${array(pair.loops).map(loopId => `<li><span>${selectedIds.has(loopId) ? link('round28-' + loopId,String(loopId).toUpperCase()) : esc(String(loopId).toUpperCase())}</span><small>${acceptedIds.has(loopId) ? 'Reviewed' : selectedIds.has(loopId) ? 'Selected · review pending' : 'Not yet selected'}</small></li>`).join('')}</ul></article>`).join('')}</div>${pairs.length < 5 ? `<p class="r28-muted">${5 - pairs.length} later goal${5 - pairs.length === 1 ? '' : 's'} remain${5 - pairs.length === 1 ? 's' : ''} to be selected from the reviews.</p>` : ''}`;
  }
  function home() {
    const c = counts();
    return `<header class="rc-hero r28-hero"><div><p class="rc-kicker">Round28 · five paired research goals</p><h1>${esc(D.title ?? 'Follow each result to its remaining premise.')}</h1><p>${esc(D.summary ?? '')}</p><div class="rc-hero-actions">${link('round28-results','Read the reviewed findings →')}${link('round28-sources','Explore the source survey →')}${link('research-network','Trace the research network →')}</div></div><aside class="rc-score r28-count"><span class="rc-score-number">${c.completed}${c.requested === null ? '' : `<small> / ${c.requested}</small>`}</span><strong>Research loops reviewed</strong><small>${c.requested !== null && c.completed === c.requested ? 'This requested cycle is complete.' : `${c.selected} selected · ${c.remaining ?? '—'} investigations remain to be reviewed.`}</small><small>Execution count; not a percentage of Yang–Mills solved.</small></aside></header><section class="r28-pair-section"><div class="r28-section-head"><h2>Where each goal stands</h2><p>Second loops follow the first review.</p></div>${pairCards()}</section><section><div class="r28-section-head"><h2>Current investigations</h2><p>${c.completed} reviewed · ${c.selected - c.completed} awaiting review</p></div><div class="r28-grid">${loops.map(loopCard).join('')}</div></section>${assessment(true)}<section class="r28-reading-callout"><div><p class="rc-kicker">Historical ideas and modern research</p><h2>What was read, and how it was used.</h2><p>Newton, Tesla, Jung, Penrose and Feynman provide documented research perspectives. Reading records preserve the source category, passages inspected and limits on the claims they support.</p></div>${link('round28-sources','Open the source survey →')}</section><p>${link('round27-home','Previous Round27 checkpoint →')} · ${link('all-results','All recorded rounds →')}</p>`;
  }
  function equations(values) {
    return array(values).length ? `<section class="r28-equations"><h2>Equations within the reviewed scope</h2>${values.map(item => `<figure>${item.label ? `<figcaption>${esc(item.label)}</figcaption>` : ''}<pre><code>${esc(typeof item === 'string' ? item : item.expression ?? '')}</code></pre>${item.scope ? `<p>${esc(item.scope)}</p>` : ''}</figure>`).join('')}</section>` : '';
  }
  function loopPage(loop) {
    const complete = reviewed(loop);
    return `<header class="r22-page-head"><p class="rc-kicker">Round28 · ${esc(id(loop.id).toUpperCase())}</p><h1>${esc(loop.title ?? loop.id)}</h1>${badge(loop)}${complete ? `<p>${esc(loop.accepted)}</p>` : '<p>No reviewed finding is recorded for this investigation yet.</p>'}</header>${complete ? `${loop.model ? `<p class="r28-model"><strong>Model:</strong> ${esc(loop.model)}</p>` : ''}<section class="rc-section"><h2>What this result establishes</h2>${list(loop.bullets)}</section>${equations(loop.equations)}${array(loop.derivation_steps).length ? `<section class="rc-section"><h2>Derivation and checks</h2>${list(loop.derivation_steps)}</section>` : ''}${array(loop.applications).length ? `<section class="rc-section"><h2>Possible applications</h2>${list(loop.applications)}</section>` : ''}<section class="r28-scope"><h2>Limitations and remaining conditions</h2>${list(loop.limitations)}</section>` : ''}<section class="rc-section"><h2>${complete ? 'Derivation and review records' : 'Selected question'}</h2>${sourceList(loop.sources)}</section><p>${link('round28-results','Back to all Round28 investigations →')} · ${link('research-network','Explore research dependencies →')}</p>`;
  }
  function results() {
    const c = counts();
    return `<header class="r22-page-head"><p class="rc-kicker">Round28 · ${c.completed} reviewed / ${c.requested ?? '—'} requested investigations</p><h1>The finding, the scope, the evidence.</h1><p>Each card keeps its review verdict and limitation beside its result. Selected investigations remain pending until a final review is recorded.</p></header><div class="r28-grid">${loops.map(loopCard).join('')}</div>${assessment(true)}`;
  }
  function filterSources(query = '', lens = 'all', category = 'all') {
    const needle = String(query).trim().toLowerCase();
    return array(D.survey?.records).filter(item => (lens === 'all' || item.lens === lens) && (category === 'all' || item.category === category) && [item.title,item.lens,item.category,item.depth,item.use,item.limits,item.change_status].join(' ').toLowerCase().includes(needle));
  }
  function sourceCards(query = '', lens = 'all', category = 'all') {
    const records = filterSources(query,lens,category);
    if (!records.length) return '<p class="r28-empty" role="status">No reading records match. Clear the search or change a filter.</p>';
    return records.map(item => `<article class="r28-source-card"><p class="rc-kicker">${esc(lensNames[item.lens] ?? item.lens)} · ${esc(categoryNames[item.category] ?? item.category)}</p><h2>${esc(item.title)}</h2><p class="r28-reading-depth"><strong>Reading depth:</strong> ${esc(item.depth)}</p><div class="r28-source-links">${array(item.urls).map((url, index) => source({url,title:array(item.urls).length === 1 ? 'Open source' : `Source link ${index + 1}`})).join('')}</div><details><summary>Use, limits and earlier reading</summary>${item.use ? `<p><strong>Use:</strong> ${esc(item.use)}</p>` : ''}${item.limits ? `<p><strong>Limit:</strong> ${esc(item.limits)}</p>` : ''}${item.change_status ? `<p><strong>Reading status:</strong> ${esc(item.change_status.replaceAll('_',' '))}</p>` : ''}${item.change_basis ? `<p>${esc(item.change_basis)}</p>` : ''}${item.ledger ? `<p>${source({path:item.ledger,title:'Attributed reading record'})}</p>` : ''}</details></article>`).join('');
  }
  function survey() {
    const s = D.survey ?? {}, records = array(s.records), lenses = [...new Set(records.map(item => item.lens))], categories = [...new Set(records.map(item => item.category))];
    const distinctURLs = new Set(records.flatMap(item => array(item.urls))).size;
    const allInspectedURLs = new Set([...records.flatMap(item => array(item.urls)), ...array(s.screening).map(item => item.url)]).size;
    return `<header class="r22-page-head"><p class="rc-kicker">Historical perspectives · current primary research · source provenance</p><h1>Read the sources with their limits attached.</h1><p>This targeted survey includes historical manuscripts, occult interpretations, modern research, patents and conversations. The panel uses them as distinct kinds of evidence; it does not claim an exhaustive literature search or historical-person endorsement.</p></header><dl class="r28-survey-counts"><div><dt>Reading records</dt><dd>${records.length}</dd></div><div><dt>Distinct recorded URLs</dt><dd>${distinctURLs}</dd></div><div><dt>Additional screening records</dt><dd>${array(s.screening).length}</dd></div><div><dt>URLs including screening</dt><dd>${allInspectedURLs}</dd></div></dl><p class="r28-muted">Reading records include repeated readings and bibliographic metadata checks. They are not a count of distinct studies. A record may cover only an abstract or selected passages; source counts do not count full books, proofs or research loops. Unopened leads stay outside these reading and screening totals.</p><section class="r28-source-controls" aria-label="Filter source readings"><label>Search readings<input id="r28-source-search" type="search" placeholder="Try noise, fluxions, spin networks…"></label><label>Research perspective<select id="r28-source-lens"><option value="all">All perspectives</option>${lenses.map(lens => `<option value="${esc(lens)}">${esc(lensNames[lens] ?? lens)}</option>`).join('')}</select></label><label>Source category<select id="r28-source-category"><option value="all">All categories</option>${categories.map(category => `<option value="${esc(category)}">${esc(categoryNames[category] ?? category)}</option>`).join('')}</select></label><button id="r28-source-reset" type="button">Reset filters</button></section><p id="r28-source-count" class="r28-muted" role="status">${records.length} reading records shown.</p><section id="r28-source-cards" class="r28-source-grid" aria-label="Matching reading records">${sourceCards()}</section>${array(s.screening).length ? `<details class="r28-survey-notes"><summary>Additional screening and reopened sources</summary><p>These records are separate from the formal reading count.</p>${array(s.screening).map(item => `<article><h3>${source({url:item.url,title:item.id ?? item.url})}</h3><p>${esc(item.reading_depth)}</p><p>${esc(item.use ?? item.status ?? '')}</p></article>`).join('')}</details>` : ''}${array(s.unread_leads).length ? `<details class="r28-survey-notes"><summary>Unopened leads · excluded from reading and screening counts</summary>${s.unread_leads.map(item => `<article><h3>${source({url:item.url,title:item.id ?? item.url})}</h3><p>${esc(item.reading_depth)}</p><p>${esc(item.context ?? '')}</p></article>`).join('')}</details>` : ''}${array(s.discrepancies).length ? `<details class="r28-survey-notes"><summary>Bibliographic discrepancies and corrections</summary>${s.discrepancies.map(item => `<article><p><strong>${esc(item.record_id ?? array(item.record_ids).join(', '))}:</strong> ${esc(item.issue)}</p><p>${esc(item.resolution)}</p></article>`).join('')}</details>` : ''}<section class="r28-scope"><h2>Scope recorded at the survey checkpoint</h2>${list(s.interpretation_limits)}${s.government_context?.scope ? `<p>${esc(s.government_context.scope)}</p>` : ''}${sourceList(s.sources)}</section>`;
  }
  function proof() {
    const obligations = array(D.progress?.obligations);
    return `<header class="r22-page-head"><p class="rc-kicker">Proof obligations · panel assessment</p><h1>What the remaining proof requires.</h1><p>${esc(D.progress?.percentage_statement ?? 'No current assessment has been recorded.')}</p></header>${obligations.length ? `<div class="r28-table-wrap" tabindex="0" role="region" aria-label="Outstanding proof obligations"><table class="r28-table"><caption>Round28 assessment at the stated model and scale</caption><thead><tr><th scope="col">Obligation</th><th scope="col">Current status</th><th scope="col">Missing input</th></tr></thead><tbody>${obligations.map(item => `<tr><th scope="row">${esc(item.name)}</th><td>${esc(item.status)}</td><td>${Array.isArray(item.missing) ? list(item.missing) : esc(item.missing)}</td></tr>`).join('')}</tbody></table></div>` : '<p>A revised obligation table has not been recorded for this active cycle.</p>'}<p>${link('round28-roadmap','Review the proposed next goals →')} · ${link('round27-proof','Read the previous panel assessment →')}</p>`;
  }
  function roadmap() {
    const goals = array(D.roadmap?.next_goals);
    return `<header class="r22-page-head"><p class="rc-kicker">Reviewed continuation · planned work</p><h1>The next question follows the remaining premise.</h1><p>${esc(D.roadmap?.summary ?? (goals.length ? 'These priorities follow the completed review. Future investigations have not started; each second loop will be selected after its first review.' : 'The current pairs and selected investigations are shown below. Later goals will be added after the required reviews.'))}</p></header>${goals.length ? `<div class="r28-grid">${goals.map(goal => `<article class="rc-result"><p class="rc-kicker">${esc(goal.id)} · planned</p><h2>${esc(goal.title)}</h2><p>${esc(goal.target ?? goal.first_target ?? '')}</p>${goal.missing_premise ? `<p><strong>Missing input:</strong> ${esc(goal.missing_premise)}</p>` : ''}${goal.proposed_first_loop_test ? `<details><summary>Proposed first investigation</summary><p>${esc(goal.proposed_first_loop_test)}</p>${goal.exact_model ? `<p><strong>Model:</strong> ${esc(goal.exact_model)}</p>` : ''}${goal.reason_for_rank ? `<p><strong>Priority:</strong> ${esc(goal.reason_for_rank)}</p>` : ''}</details>` : ''}${list(goal.limitations)}${sourceList(goal.sources)}</article>`).join('')}</div>` : '<p class="r28-muted">No post-cycle research goals have been recorded yet.</p>'}<section><h2>Current goal pairs</h2>${pairCards()}</section><p>${link('round28-proof','Inspect the remaining proof obligations →')}</p>`;
  }
  function addendumCard() {
    const a = D.addendum, url = safeURL(a?.url, true);
    if (!url) return '<p class="r28-muted">The Round28 addendum is not available in this checkpoint.</p>';
    return `<article class="r28-addendum-card"><p class="rc-kicker">Round28 manuscript addendum</p><h2>${esc(a.title ?? 'Round28 research addendum')}</h2>${a.summary ? `<p>${esc(a.summary)}</p>` : ''}<p><a href="${esc(url)}">Read the addendum ↗</a></p>${a.sources ? sourceList(a.sources) : ''}</article>`;
  }
  function addendum() {
    return `<header class="r22-page-head"><p class="rc-kicker">Research manuscripts</p><h1>The Round28 findings alongside the earlier draft.</h1><p>Use the addendum with each result’s derivation and review. The original draft and Round27 addendum preserve their earlier scope.</p></header>${addendumCard()}<section class="rc-section"><h2>Earlier manuscripts</h2><p>${link('drafts','Read Draft 01 and the Round27 addendum →')} · ${link('round28-results','Inspect the current findings →')}</p></section>`;
  }
  function nodeStatus(node) {
    if (node.kind === 'literature' || node.status === 'source-reviewed') return {name:'Source reviewed · not a physics premise',css:'source'};
    const status = String(node.status ?? 'planned').toLowerCase();
    if (/limited|insufficient|reject|fail/.test(status)) return {name:'Limited result',css:'limited'};
    if (/conditional/.test(status)) return {name:'Conditional',css:'conditional'};
    if (/proved|accepted/.test(status)) return {name:'Proved within stated model',css:'accepted'};
    if (/planned|open|unexecuted/.test(status)) return {name:'Planned / open',css:'pending'};
    return {name:String(node.status ?? 'Unclassified'),css:'pending'};
  }
  const nodeBadge = node => { const status=nodeStatus(node); return `<span class="r28-badge r28-badge-${status.css}">${esc(status.name)}</span>`; };
  function validEdges() { return networkEdges.filter(edge => nodeById.has(String(edge.from)) && nodeById.has(String(edge.to)) && edgeNames[edge.type]); }
  function filterNodes(query = '',kind = 'all') {
    const needle=String(query).trim().toLowerCase();
    return networkNodes.filter(node => (kind === 'all' || node.kind === kind) && [node.id,node.title,node.summary,node.detail,node.model,node.equation].join(' ').toLowerCase().includes(needle));
  }
  function neighborhood(selected, type = 'all') {
    if (!nodeById.has(String(selected))) return {nodes:[],edges:[]};
    const edges=validEdges().filter(edge => (type === 'all' || type === edge.type) && (String(edge.from) === String(selected) || String(edge.to) === String(selected)));
    const ids=new Set([String(selected)]);
    edges.forEach(edge => {ids.add(String(edge.from));ids.add(String(edge.to));});
    return {nodes:networkNodes.filter(node => ids.has(String(node.id))),edges};
  }
  function networkInitial() {
    const last=[...reviewedLoops()].reverse().map(loop => networkNodes.find(node => node.route === 'round28-' + loop.id)).find(Boolean);
    return String(last?.id ?? networkNodes[0]?.id ?? '');
  }
  function networkCatalog(query='',kind='all',selected='') {
    const nodes=filterNodes(query,kind);
    if (!nodes.length) return '<p class="r28-empty">No entries match the current search.</p>';
    const kinds=[...new Set(networkNodes.map(node=>node.kind))];
    return kinds.map(value=>{const group=nodes.filter(node=>node.kind===value);return group.length ? `<section><h3>${esc(kindNames[value] ?? value ?? 'Other entries')} <span>${group.length}</span></h3><ul>${group.map(node=>`<li><button type="button" data-r28-node="${esc(node.id)}" aria-pressed="${String(node.id)===String(selected)}"><span>${esc(node.title)}</span><small>${esc(nodeStatus(node).name)}</small></button></li>`).join('')}</ul></section>` : '';}).join('');
  }
  function networkMap(selected,type='all') {
    const local=neighborhood(selected,type);
    if (!local.nodes.length) return '<p class="r28-empty">Select an entry from the research catalog.</p>';
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
      return `<path class="r28-net-edge r28-net-edge-${edge.type}" d="M ${ax} ${a.y+44} C ${middle} ${a.y+44}, ${middle} ${b.y+44}, ${bx} ${b.y+44}" marker-end="url(#r28-arrow-${edge.type})"><title>${esc(nodeById.get(String(edge.from)).title)} → ${esc(nodeById.get(String(edge.to)).title)}: ${esc(edge.label ?? edgeNames[edge.type])}</title></path>`;
    }).join('');
    return `<div class="r28-map-scroll" tabindex="0" role="region" aria-label="Selected entry and its direct incoming and outgoing relations"><div class="r28-map-canvas" style="width:${width}px;height:${height}px"><svg width="${width}" height="${height}" aria-hidden="true" focusable="false"><defs>${Object.keys(edgeNames).map(type=>`<marker id="r28-arrow-${type}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>`).join('')}</defs>${paths}</svg>${['Incoming relations','Selected entry','Outgoing relations'].map((name,i)=>`<span class="r28-map-label" style="left:${24+i*342}px">${name}</span>`).join('')}${local.nodes.map(node=>{const p=positions.get(String(node.id));return `<button type="button" class="r28-map-node r28-map-node-${nodeStatus(node).css}" data-r28-node="${esc(node.id)}" aria-pressed="${String(node.id)===String(selected)}" style="left:${p.x}px;top:${p.y}px"><span>${esc(node.title)}</span><small>${esc(node.kind==='literature'?'Literature · source reviewed':nodeStatus(node).name)}</small></button>`;}).join('')}</div></div>`;
  }
  function networkDetails(selected,type='all') {
    const node=nodeById.get(String(selected));
    if(!node)return '<p>Select an entry from the research catalog.</p>';
    const local=neighborhood(selected,type);
    return `<header><p class="rc-kicker">${esc(kindNames[node.kind]??node.kind)} · ${esc(node.id)}</p><h2 id="r28-network-selected">${esc(node.title)}</h2>${nodeBadge(node)}</header>${node.model?`<p class="r28-model">${esc(node.model)}</p>`:''}<p>${esc(node.summary??'')}</p>${node.detail?`<p class="r28-node-detail">${esc(node.detail)}</p>`:''}${node.equation?`<pre><code>${esc(node.equation)}</code></pre>`:''}${sourceList(node.sources)}${node.route?`<p>${link(node.route,'Read the complete record →')}</p>`:''}<h3>Direct relations · ${local.edges.length}</h3>${local.edges.length?`<ul class="r28-network-connections">${local.edges.map(edge=>{const outgoing=String(edge.from)===String(selected),other=nodeById.get(String(outgoing?edge.to:edge.from));return `<li><span class="r28-edge-label r28-edge-label-${edge.type}">${edgeNames[edge.type]}</span><p class="r28-relation-direction">${outgoing?'Outgoing relation to':'Incoming relation from'}</p><button type="button" data-r28-node="${esc(other.id)}">${esc(other.title)}</button>${edge.label?`<p>${esc(edge.label)}</p>`:''}${edge.detail?`<p>${esc(edge.detail)}</p>`:''}</li>`;}).join('')}</ul>`:'<p>No direct relations match this connection filter.</p>'}`;
  }
  function network() {
    const selected=networkInitial(),kinds=[...new Set(networkNodes.map(node=>node.kind))];
    return `<header class="r22-page-head"><p class="rc-kicker">${networkNodes.length} research and source entries · ${validEdges().length} recorded relations</p><h1>Trace the result. Inspect every relation.</h1><p>Choose a research result or source to inspect its direct relations. Literature comparisons and proposed transfers carry their own labels; a source-review entry is not a proved physical premise.</p></header><section class="r28-network-legend"><div>${Object.entries(edgeNames).map(([type,name])=>`<span class="r28-edge-label r28-edge-label-${type}">${name}</span>`).join('')}</div><p>The counts describe this research index, not vertices, links or states of a physical gauge graph. Position and distance in the map have no physical meaning. Read each relation label for its precise role.</p></section><section class="r28-source-controls" aria-label="Filter the research network"><label>Search all entries<input id="r28-network-search" type="search" placeholder="Try AG2, homogeneous, literature…"></label><label>Entry kind<select id="r28-network-kind"><option value="all">All kinds</option>${kinds.map(kind=>`<option value="${esc(kind)}">${esc(kindNames[kind]??kind)}</option>`).join('')}</select></label><label>Relation type<select id="r28-network-edge"><option value="all">All relations</option>${Object.entries(edgeNames).map(([type,name])=>`<option value="${type}">${name}</option>`).join('')}</select></label><button id="r28-network-reset" type="button">Reset filters</button></section><p class="r28-muted" id="r28-network-count" role="status">${networkNodes.length} entries in the catalog.</p><section class="r28-network-map-section"><div class="r28-section-head"><h2>One step around the selected entry</h2><button id="r28-network-map-toggle" type="button" aria-controls="r28-network-map" aria-expanded="true">Hide visual map</button></div><div id="r28-network-map">${networkMap(selected)}</div></section><div class="r28-network-layout"><aside class="r28-network-catalog" aria-label="All matching research and source entries"><h2>Research catalog</h2><div id="r28-network-catalog">${networkCatalog('','all',selected)}</div></aside><section id="r28-network-details" class="r28-network-details" aria-labelledby="r28-network-selected">${networkDetails(selected)}</section></div>`;
  }
  function render(value = 'home') {
    const route = normalizeRoute(value);
    if (route === 'round27-home') return `<div class="rc-history-notice">Archived Round27 checkpoint. ${link('home','Current findings →')}</div>` + prior.render('home');
    if (route === 'drafts') return `<div class="r28 r28-draft-notice">${D.addendum ? addendumCard() : ''}</div>` + prior.render(value);
    if (route === 'all-results' || route === 'contributions') return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r28"><section class="r28-reading-callout"><div><p class="rc-kicker">Current continuation</p><h2>Round28 · ${counts().completed} reviewed investigations</h2><p>Read the current results with their scope and limitations. Earlier round records remain below.</p></div>${link('round28-results','Read the Round28 results →')}</section></div>` + prior.render(value);
    if (!own.has(route)) return prior.render(value);
    const loop = byRoute.get(route);
    const body = loop ? loopPage(loop) : route === 'research-network' ? network() : route === 'round28-results' ? results() : route === 'round28-sources' ? survey() : route === 'round28-proof' ? proof() : route === 'round28-roadmap' ? roadmap() : route === 'round28-addendum' ? addendum() : home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27 r28">${nav(route)}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · Round28</strong>${link('round28-proof','Proof obligations')}${link('round28-sources','Source survey')}${link('round27-home','Round27 archive')}${link('all-results','All recorded rounds')}</footer></div>`;
  }
  function afterRender() {
    const route = normalizeRoute(location.hash.replace(/^#research\/?/, '') || 'home');
    if (route === 'round27-home') { window.ResearchJourney?.cleanup?.(); document.title = 'Round27 archive · Yang–Mills Workbench'; return; }
    if (!own.has(route)) return prior.afterRender();
    window.ResearchJourney?.cleanup?.();
    const names = {'research-network':'Research and source network','round28-results':'Round28 results','round28-sources':'Round28 source survey','round28-proof':'Round28 proof obligations','round28-roadmap':'Round28 next goals','round28-addendum':'Round28 research addendum'};
    document.title = `${byRoute.get(route)?.title ?? names[route] ?? 'Round28'} · Yang–Mills Workbench`;
    if (route === 'research-network') {
      const get=name=>document.getElementById(name);
      const search=get('r28-network-search'),kind=get('r28-network-kind'),edge=get('r28-network-edge'),catalog=get('r28-network-catalog'),details=get('r28-network-details'),map=get('r28-network-map'),count=get('r28-network-count'),reset=get('r28-network-reset'),toggle=get('r28-network-map-toggle');
      if(!search||!kind||!edge||!catalog||!details||!map||!count||!reset||!toggle)return;
      let selected=networkInitial();
      const target=location.hash.match(/(?:\?|&)node=([^&]*)/);
      if(target){try{const decoded=decodeURIComponent(target[1]);if(nodeById.has(decoded))selected=decoded;}catch{}}
      const draw=()=>{catalog.innerHTML=networkCatalog(search.value,kind.value,selected);details.innerHTML=networkDetails(selected,edge.value);map.innerHTML=networkMap(selected,edge.value);};
      const filter=()=>{const found=filterNodes(search.value,kind.value);if(found.length&&!found.some(node=>String(node.id)===selected))selected=String(found[0].id);count.textContent=`${found.length} of ${networkNodes.length} catalog entries match. The map retains direct neighbors as context.`;draw();};
      const select=event=>{const button=event.target.closest?.('button[data-r28-node]'),target=button?.getAttribute('data-r28-node');if(!target||!nodeById.has(target))return;selected=target;draw();const heading=get('r28-network-selected');heading?.setAttribute?.('tabindex','-1');heading?.focus?.({preventScroll:true});};
      for(const host of [catalog,details,map])host.addEventListener('click',select);
      search.addEventListener('input',filter);kind.addEventListener('change',filter);edge.addEventListener('change',draw);
      reset.addEventListener('click',()=>{search.value='';kind.value='all';edge.value='all';selected=networkInitial();filter();});
      toggle.addEventListener('click',()=>{map.hidden=!map.hidden;toggle.setAttribute('aria-expanded',String(!map.hidden));toggle.textContent=map.hidden?'Show visual map':'Hide visual map';});
      draw();return;
    }
    if (route !== 'round28-sources') return;
    const get = name => document.getElementById(name);
    const search = get('r28-source-search'), lens = get('r28-source-lens'), category = get('r28-source-category'), reset = get('r28-source-reset'), cards = get('r28-source-cards'), count = get('r28-source-count');
    if (!search || !lens || !category || !reset || !cards || !count) return;
    const update = () => { const found = filterSources(search.value,lens.value,category.value); cards.innerHTML = sourceCards(search.value,lens.value,category.value); count.textContent = `${found.length} of ${array(D.survey?.records).length} reading records shown.`; };
    search.addEventListener('input',update); lens.addEventListener('change',update); category.addEventListener('change',update);
    reset.addEventListener('click',() => { search.value=''; lens.value='all'; category.value='all'; update(); search.focus(); });
    update();
  }
  window.ResearchRound28 = {render,afterRender,counts,reviewed,safePath,safeURL,source,normalizeRoute,filterSources,sourceCards,filterNodes,neighborhood,networkCatalog,networkMap,networkDetails,nodeStatus,validEdges,data:D};
  window.ResearchObservatory = {...prior,render,afterRender};
})();
