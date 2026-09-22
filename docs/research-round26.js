/* Current continuation and a source-bound dependency explorer. Historical renderers remain intact. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND26_DATA;
  if (!D) return;
  const esc = x => String(x ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const array = x => Array.isArray(x) ? x : [];
  const loops = array(D.loops);
  const nodes = array(D.network?.nodes ?? D.nodes);
  const edges = array(D.network?.edges ?? D.edges);
  const nodeById = new Map(nodes.map(x => [String(x.id), x]));
  const statuses = ['proved-in-model', 'conditional', 'limited', 'planned'];
  const kinds = ['history', 'premise', 'equation', 'loop', 'open'];
  const kindNames = {history:'Earlier findings', premise:'Required premises', equation:'Equations', loop:'Current loops', open:'Open targets'};
  const statusNames = {'proved-in-model':'Proved in model', conditional:'Conditional', limited:'Limited', planned:'Planned / open'};
  const edgeNames = {'proven-dependency':'Verified source dependency', 'proposed-transfer':'Proposed transfer', 'review-selection':'Review selection'};
  const edgeTypes = Object.keys(edgeNames);
  function status(x) {
    const value = String(x.status ?? x.verdict ?? 'planned').toLowerCase();
    if (value.includes('limited') || value.includes('insufficient') || value.includes('fail') || value.includes('rejected')) return 'limited';
    if (value.includes('conditional')) return 'conditional';
    if (value.includes('planned') || value.includes('open') || value.includes('unexecuted')) return 'planned';
    if (value.includes('proved') || value.includes('accepted') || value.includes('pass')) return 'proved-in-model';
    return 'limited';
  }
  const badge = x => `<span class="r26-status r26-status-${status(x)}">${statusNames[status(x)]}</span>`;
  const routeLink = (id, label) => /^[a-z0-9-]+$/i.test(String(id)) ? `<a href="#research/${esc(id)}">${esc(label)}</a>` : esc(label);
  function safeSource(s) {
    const item = typeof s === 'string' ? {path:s, label:s} : s ?? {};
    const path = String(item.path ?? '');
    const raw = item.url ? String(item.url) : path && !/^[a-z][a-z\d+.-]*:/i.test(path) && !path.startsWith('//') ? `https://github.com/occult-kranti/yang_mills_workbench/blob/main/${path}` : '';
    if (!/^https:\/\/[^\s"<>]+$/i.test(raw)) return `<span>${esc(item.label ?? item.title ?? (path || 'Source unavailable'))}</span>`;
    return `<a href="${esc(raw)}" target="_blank" rel="noopener noreferrer">${esc(item.label ?? item.title ?? (path || raw))} <span aria-hidden="true">↗</span></a>`;
  }
  const sources = items => array(items).length ? `<div class="r22-evidence r26-sources">${array(items).map(safeSource).join('')}</div>` : '<p class="r26-muted">No direct source attached to this entry.</p>';
  const nav = () => `<nav class="rc-nav" aria-label="Research navigation">${routeLink('home','Current findings')}${routeLink('drafts','Drafts')}${routeLink('research-network','Research network')}${routeLink('round26-results','Ten-loop results')}${routeLink('all-results','Every round')}${routeLink('round26-roadmap','Next goals')}${routeLink('resonance-methods','Newton & Tesla')}</nav>`;
  const list = items => array(items).length ? `<ul>${array(items).map(x => `<li>${esc(typeof x === 'string' ? x : x.text ?? x.summary ?? x.title ?? '')}</li>`).join('')}</ul>` : '';
  const completed = () => loops.filter(x => status(x) !== 'planned');
  const loopId = x => String(x.loop ?? x.id ?? '');
  const loopLink = x => routeLink('round26-' + loopId(x), 'Read result and evidence →');
  const goals = () => array(D.roadmap?.next_goals ?? D.roadmap?.goals);
  function loopCard(x) {
    return `<article class="rc-result r26-loop-card"><div class="r26-card-top"><p class="rc-kicker">${esc(loopId(x).toUpperCase())}${x.goal ? ' · ' + esc(x.goal) : ''}</p>${badge(x)}</div><h2>${esc(x.title ?? loopId(x))}</h2>${x.model ? `<p class="r26-model">Model: ${esc(x.model)}</p>` : ''}<p>${esc(x.accepted ?? x.summary ?? '')}</p>${list(x.bullets)}${loopLink(x)}</article>`;
  }
  function home() {
    return `<section class="rc-hero r26-hero"><div><p class="rc-kicker">Round26 · paired derivation and reconstruction</p><h1>${esc(D.title ?? 'Follow the result. Trace every premise.')}</h1><p>${esc(D.summary ?? 'Five research goals, two evidence-gated loops each. Explore what each calculation establishes and the dependencies still missing.')}</p><div class="rc-hero-actions">${routeLink('research-network','Explore the research network →')}${routeLink('round26-results','Read this round’s results →')}${routeLink('drafts','Read the research draft →')}</div></div><aside class="rc-score"><span class="rc-score-number">${completed().length}<small> / ${Math.max(10, loops.length)}</small></span><strong>Research loops executed</strong><small>Execution counts include limited outcomes. They do not measure progress toward a continuum proof.</small></aside></section><section class="r23-disclosure"><strong>The scope travels with the result.</strong><p>${esc(D.scope ?? 'Accepted model calculations do not establish the homogeneous Yang–Mills mass gap or the four-dimensional continuum construction.')}</p><p>${esc(D.review ?? 'Forward and reverse reports, skeptical review, and advisor gates are linked from each result. Shared premises remain shared assumptions.')}</p></section><section class="r26-network-callout"><div><p class="rc-kicker">An inspectable chain of evidence</p><h2>What depends on what?</h2><p>Trace earlier results, equations, the ten current loops and open targets. Verified source dependencies, proposed transfers and review decisions carry separate labels.</p></div>${routeLink('research-network','Open the connected map →')}</section><section><div class="r26-section-head"><h2>Current investigations</h2><p>${completed().length} executed · ${Math.max(10, loops.length) - completed().length} remaining</p></div><div class="rc-results rc-results-all">${loops.map(loopCard).join('')}</div></section><section class="r22-limit"><h2>Keep the remaining problem visible</h2><p>${esc(D.open_summary ?? 'A restricted endpoint or a numerical certificate does not provide a volume-uniform homogeneous gap, physical scale matching, or a nontrivial continuum quantum field theory.')}</p>${routeLink('round26-roadmap','Review the next goals →')} · ${routeLink('all-results','Inspect the complete history →')}</section>`;
  }
  function results() {
    return `<header class="r22-page-head"><p class="rc-kicker">Round26 · ${completed().length} / ${loops.length} executed loops</p><h1>Results with their limits attached.</h1><p>Each contribution is local to the stated model and premises. Scientific priority is unverified; “new” means new in this workbench.</p></header><div class="r26-result-list">${loops.map(x => `<section class="rc-section"><div class="r26-card-top"><p class="rc-kicker">${esc(loopId(x).toUpperCase())} · ${esc(x.goal ?? '')}</p>${badge(x)}</div><h2>${esc(x.title ?? '')}</h2><p>${esc(x.accepted ?? x.summary ?? '')}</p>${x.model ? `<p class="r26-model">Model: ${esc(x.model)}</p>` : ''}${list(x.bullets)}${array(x.limitations).length ? `<div class="r26-boundary"><h3>Limit of this result</h3>${list(x.limitations)}</div>` : ''}<p>${loopLink(x)}</p>${sources(x.sources)}</section>`).join('')}</div>`;
  }
  function equations(items) {
    return array(items).length ? `<section class="r26-equations"><h2>Equations used in this loop</h2>${array(items).map(x => `<figure>${typeof x === 'object' && x.label ? `<figcaption>${esc(x.label)}</figcaption>` : ''}<pre><code>${esc(typeof x === 'string' ? x : x.expression ?? x.equation ?? '')}</code></pre>${typeof x === 'object' && x.scope ? `<p>${esc(x.scope)}</p>` : ''}</figure>`).join('')}</section>` : '';
  }
  function loopPage(x) {
    const related = nodes.find(n => n.route === 'round26-' + loopId(x) || n.id === loopId(x) || n.id === 'round26-' + loopId(x));
    return `<header class="r22-page-head"><p class="rc-kicker">Round26 · ${esc(loopId(x).toUpperCase())}</p><h1>${esc(x.title ?? loopId(x))}</h1><div class="r26-card-top">${badge(x)}${x.model ? `<span class="r26-model">Model: ${esc(x.model)}</span>` : ''}</div><p>${esc(x.accepted ?? x.summary ?? '')}</p></header><section class="rc-section"><h2>What this loop contributes</h2>${list(x.bullets)}${x.review ? `<p>${esc(x.review)}</p>` : ''}${sources(x.sources)}${x.gate_sha256 ? `<code class="r22-hash">Gate SHA-256: ${esc(x.gate_sha256)}</code>` : ''}</section>${equations(x.equations)}${array(x.derivation_steps).length ? `<section class="rc-section"><h2>Derivation and reverse checks</h2>${list(x.derivation_steps)}</section>` : ''}<section class="r26-boundary"><h2>Scope and remaining conditions</h2>${array(x.limitations).length ? list(x.limitations) : '<p>Use the linked evidence gate for the exact accepted scope. This loop does not by itself establish the continuum Yang–Mills problem.</p>'}</section><p>${related ? `<a href="#research/research-network?node=${encodeURIComponent(related.id)}">Inspect this loop’s dependencies →</a> · ` : ''}${routeLink('round26-results','Back to all ten loops')}</p>`;
  }
  function roadmap() {
    return `<header class="r22-page-head"><p class="rc-kicker">Evidence-selected continuation · planning only</p><h1>The next goals follow the missing premises.</h1><p>${esc(D.roadmap?.summary ?? 'These are future targets selected from this round’s accepted results and unresolved objections. A planned goal is not an executed result.')}</p></header><div class="rc-results rc-results-all">${goals().map(x => `<article class="rc-result"><div class="r26-card-top"><p class="rc-kicker">${esc(x.id ?? '')}</p>${badge({status:x.status ?? 'planned'})}</div><h2>${esc(x.title)}</h2>${x.model ? `<p class="r26-model">Model: ${esc(x.model)}</p>` : ''}<p>${esc(x.first_target ?? x.target ?? '')}</p>${x.second_loop ? `<h3>Second-loop selection</h3><p>${esc(x.second_loop)}</p>` : ''}${list(x.dependencies)}${sources(x.sources)}</article>`).join('')}</div><section class="r22-limit"><h2>Separate the model result from the intended theory</h2><p>Homogeneous stability, uniform volume control, physical observable and clock matching, and continuum reconstruction require their own premises. A graph connection marked “proposed transfer” records an open task.</p>${routeLink('research-network','Inspect the open dependencies →')}</section>`;
  }
  function validEdges() { return edges.filter(e => nodeById.has(String(e.from)) && nodeById.has(String(e.to)) && edgeTypes.includes(e.type)); }
  function filteredNodes(query = '', filterStatus = 'all', filterKind = 'all') {
    const q = String(query).trim().toLowerCase();
    return nodes.filter(n => (filterStatus === 'all' || status(n) === filterStatus) && (filterKind === 'all' || n.kind === filterKind) && [n.id, n.title, n.summary, n.detail, n.model, n.equation].join(' ').toLowerCase().includes(q));
  }
  function neighborhood(id, type = 'all') {
    const selected = nodeById.get(String(id));
    if (!selected) return {nodes:[], edges:[]};
    const localEdges = validEdges().filter(e => (type === 'all' || e.type === type) && (String(e.from) === String(id) || String(e.to) === String(id)));
    const ids = new Set([String(id)]);
    for (const e of localEdges) { ids.add(String(e.from)); ids.add(String(e.to)); }
    return {nodes:nodes.filter(n => ids.has(String(n.id))), edges:localEdges};
  }
  function initialNode() {
    return [...nodes].reverse().find(n => n.kind === 'loop' && status(n) !== 'planned') ?? nodes.find(n => n.kind === 'loop') ?? nodes[0];
  }
  function catalog(query = '', filterStatus = 'all', filterKind = 'all', selected = '') {
    const found = filteredNodes(query, filterStatus, filterKind);
    if (!found.length) return '<p class="r26-empty" role="status">No entries match. Clear the search or change a filter.</p>';
    return kinds.map(kind => {
      const group = found.filter(n => n.kind === kind);
      if (!group.length) return '';
      return `<section class="r26-catalog-group"><h3>${kindNames[kind]} <span>${group.length}</span></h3><ul>${group.map(n => `<li><button type="button" data-r26-node="${esc(n.id)}" aria-pressed="${String(n.id) === String(selected)}"><span class="r26-entry-title">${esc(n.title)}</span><span class="r26-entry-meta">${esc(n.id)} · ${statusNames[status(n)]}</span></button></li>`).join('')}</ul></section>`;
    }).join('');
  }
  function graphMap(id, type = 'all') {
    const local = neighborhood(id, type);
    if (!local.nodes.length) return '<p class="r26-empty">Select an entry to inspect its connections.</p>';
    const positions = new Map(), laneWidth = 218, width = laneWidth * 5 + 96, step = 112;
    let rows = 1;
    for (const [column, kind] of kinds.entries()) {
      const members = local.nodes.filter(n => n.kind === kind);
      rows = Math.max(rows, members.length);
      members.forEach((n, row) => positions.set(String(n.id), {x:24 + column * laneWidth, y:56 + row * step}));
    }
    const height = Math.max(220, rows * step + 65);
    const paths = local.edges.map((e, i) => {
      const a = positions.get(String(e.from)), b = positions.get(String(e.to));
      if (!a || !b) return '';
      let d;
      if (a.x === b.x) { const side = a.x + 205 + (i % 3) * 7; d = `M ${a.x+196} ${a.y+43} C ${side+35} ${a.y+43}, ${side+35} ${b.y+43}, ${b.x+196} ${b.y+43}`; }
      else { const forward = a.x < b.x, ax = a.x+(forward?196:0), bx = b.x+(forward?0:196), middle = (ax+bx)/2; d = `M ${ax} ${a.y+43} C ${middle} ${a.y+43}, ${middle} ${b.y+43}, ${bx} ${b.y+43}`; }
      return `<path class="r26-edge r26-edge-${e.type}" d="${d}" marker-end="url(#r26-arrow-${e.type})"><title>${esc(nodeById.get(String(e.from)).title)} → ${esc(nodeById.get(String(e.to)).title)}: ${esc(edgeNames[e.type])}${e.label ? ' — ' + esc(e.label) : ''}</title></path>`;
    }).join('');
    return `<div class="r26-map-scroll" tabindex="0" role="region" aria-label="Dependency map; scroll horizontally if needed"><div class="r26-map-canvas" style="width:${width}px;height:${height}px"><svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" aria-hidden="true" focusable="false"><defs>${edgeTypes.map(t => `<marker id="r26-arrow-${t}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker>`).join('')}</defs>${paths}</svg>${kinds.map((k,i) => `<div class="r26-lane-label" style="left:${24+i*laneWidth}px">${kindNames[k]}</div>`).join('')}${local.nodes.map(n => {const p=positions.get(String(n.id)); if(!p)return ''; return `<button type="button" class="r26-map-node r26-map-node-${status(n)}${String(n.id)===String(id)?' is-selected':''}" data-r26-node="${esc(n.id)}" aria-pressed="${String(n.id)===String(id)}" style="left:${p.x}px;top:${p.y}px"><span>${esc(n.title)}</span><small>${statusNames[status(n)]}</small></button>`;}).join('')}</div></div>`;
  }
  function nodeDetails(id, type = 'all') {
    const n = nodeById.get(String(id));
    if (!n) return '<p>Select an entry from the catalog.</p>';
    const local = neighborhood(id, type);
    return `<header><p class="rc-kicker">${esc(kindNames[n.kind] ?? n.kind)} · ${esc(n.id)}</p><h2 id="r26-selected-title">${esc(n.title)}</h2>${badge(n)}</header>${n.model ? `<p class="r26-model">Model: ${esc(n.model)}</p>` : ''}<p>${esc(n.summary ?? '')}</p>${n.detail ? `<p>${esc(n.detail)}</p>` : ''}${n.equation ? `<pre><code>${esc(n.equation)}</code></pre>` : ''}${sources(n.sources)}${n.route ? `<p>${routeLink(n.route,'Open the full result →')}</p>` : ''}<h3>Direct connections <span class="r26-count">${local.edges.length}</span></h3>${local.edges.length ? `<ul class="r26-connections">${local.edges.map(e => {const outgoing=String(e.from)===String(id), other=nodeById.get(String(outgoing?e.to:e.from));return `<li><span class="r26-edge-label r26-edge-label-${e.type}">${edgeNames[e.type]}</span><span>${e.type==='proven-dependency'?(outgoing?'Supports':'Requires'):e.type==='proposed-transfer'?(outgoing?'Proposed transfer to':'Proposed input from'):(outgoing?'Selected next':'Selected after')}</span><button type="button" data-r26-node="${esc(other.id)}">${esc(other.title)}</button>${e.label?`<p>${esc(e.label)}</p>`:''}${e.detail?`<p>${esc(e.detail)}</p>`:''}</li>`;}).join('')}</ul>` : '<p>No direct connections match this edge filter.</p>'}`;
  }
  function network() {
    const selected = initialNode()?.id ?? '';
    return `<header class="r22-page-head"><p class="rc-kicker">${nodes.length} source-bound entries · ${validEdges().length} recorded links</p><h1>A network of results and remaining premises.</h1><p>Choose a result to see one step of its incoming and outgoing connections. Search the full catalog to reach every indexed historical entry.</p></header><section class="r26-legend" aria-label="Evidence and edge legend"><div>${statuses.map(s => badge({status:s})).join('')}</div><div>${edgeTypes.map(t=>`<span class="r26-edge-label r26-edge-label-${t}">${edgeNames[t]}</span>`).join('')}</div><p>Arrows follow the recorded dependency direction. Proposed transfers remain open; review selection records research order. Layout has no physical meaning.</p></section><section class="r26-controls" aria-label="Filter the research network"><label>Search all entries<input id="r26-search" type="search" placeholder="Try homogeneous, AB1, memory…"></label><label>Evidence status<select id="r26-status"><option value="all">All statuses</option>${statuses.map(s=>`<option value="${s}">${statusNames[s]}</option>`).join('')}</select></label><label>Entry kind<select id="r26-kind"><option value="all">All kinds</option>${kinds.map(k=>`<option value="${k}">${kindNames[k]}</option>`).join('')}</select></label><label>Connection type<select id="r26-edge-type"><option value="all">All connections</option>${edgeTypes.map(t=>`<option value="${t}">${edgeNames[t]}</option>`).join('')}</select></label><button id="r26-reset" type="button">Reset filters</button></section><p class="r26-muted" id="r26-match-count" role="status">${nodes.length} entries in the catalog. The map shows the selected entry and its direct neighbors.</p><section class="r26-map-section" aria-label="Selected dependency neighborhood"><div class="r26-section-head"><h2>One step around the selected entry</h2><button id="r26-map-toggle" type="button" aria-expanded="true" aria-controls="r26-map">Hide visual map</button></div><div id="r26-map">${graphMap(selected)}</div></section><div class="r26-network-layout"><aside class="r26-catalog" aria-label="All matching entries"><h2>Research catalog</h2><p class="r26-muted">Select any entry. The connection list provides the same relationships as the visual map.</p><div id="r26-catalog">${catalog('','all','all',selected)}</div></aside><section class="r26-node-details" id="r26-details" aria-labelledby="r26-selected-title">${nodeDetails(selected)}</section></div>`;
  }
  const ownRoutes = new Set(['home','round26-results','research-network','round26-roadmap',...loops.map(x=>'round26-'+loopId(x))]);
  function splitRoute(value) { const [route,query=''] = String(value ?? 'home').split('?'); return {route:route || 'home', query}; }
  function render(value = 'home') {
    const {route:r} = splitRoute(value);
    if (r === 'round25-home') return `<div class="rc-history-notice">Archived Round25 checkpoint. ${routeLink('home','Current findings →')}</div>` + prior.render('home');
    if (r === 'all-results' || r === 'contributions') return `<div class="rc20 r21 r22 r23 r24 r25 r26">${nav()}<section class="r26-archive-addition"><p class="rc-kicker">Current continuation</p><h1>Round26 results</h1><p>${completed().length} executed loops are available with their evidence and limitations. The complete earlier ledger is preserved below.</p>${routeLink('round26-results','Read every Round26 contribution →')} · ${routeLink('research-network','Explore linked evidence →')}</section></div>` + prior.render(r);
    if (!ownRoutes.has(r)) return prior.render(r);
    const loop = loops.find(x => r === 'round26-' + loopId(x));
    const body = loop ? loopPage(loop) : r === 'research-network' ? network() : r === 'round26-results' ? results() : r === 'round26-roadmap' ? roadmap() : home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26">${nav()}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · Round26</strong>${safeSource({path:'research/round26/HANDOFF.md',label:'Current handoff'})}${safeSource({path:'research/round26/NOVELTY.md',label:'Contribution scope'})}${safeSource({path:'research/round26/methods/prospective-updates.json',label:'Updated research methods'})}${routeLink('round25-home','Round25 archive')}${routeLink('all-results','All recorded rounds')}</footer></div>`;
  }
  function afterRender() {
    const value = location.hash.replace(/^#research\/?/, '') || 'home';
    const {route:r, query} = splitRoute(value);
    if (r === 'round25-home') {
      window.ResearchJourney?.cleanup?.();
      document.title='Round25 archive · Yang–Mills Workbench';
      const slider=document.getElementById('r25-z'), endpoint=window.ResearchRound25?.endpoint;
      if(slider && endpoint){
        const update=()=>{const scale=Number(slider.value),a=endpoint(scale*1e-6);document.getElementById('r25-z-value').textContent=scale.toFixed(2);document.getElementById('r25-endpoint').innerHTML=`<dl class="r25-values"><div><dt>Re(F∞) − 1</dt><dd>${a.realMinusOne.toExponential(5)}</dd></div><div><dt>Im(F∞)</dt><dd>${a.imag.toExponential(5)}</dd></div><div><dt>Linear-approximation radius</dt><dd>≤ ${a.linearRadius.toExponential(5)}</dd></div></dl>`;};
        slider.addEventListener('input',update);update();
      }
      return;
    }
    if (!ownRoutes.has(r)) { prior.afterRender(); return; }
    window.ResearchJourney?.cleanup?.();
    document.title = r === 'research-network' ? 'Research network · Yang–Mills Workbench' : 'Round26 · Yang–Mills Workbench';
    if (r !== 'research-network') return;
    const byId = id => document.getElementById(id);
    if (!byId('r26-search')) return;
    let selected = initialNode()?.id ?? '';
    const match = query.match(/(?:^|&)node=([^&]*)/);
    if (match) { try { const target=decodeURIComponent(match[1]); if(nodeById.has(target)) selected=target; } catch {} }
    const queryValue = () => byId('r26-search').value;
    const statusValue = () => byId('r26-status').value;
    const kindValue = () => byId('r26-kind').value;
    const edgeValue = () => byId('r26-edge-type').value;
    function drawSelection() {
      byId('r26-map').innerHTML = graphMap(selected, edgeValue());
      byId('r26-details').innerHTML = nodeDetails(selected, edgeValue());
      byId('r26-catalog').innerHTML = catalog(queryValue(), statusValue(), kindValue(), selected);
    }
    function updateFilters() {
      const found = filteredNodes(queryValue(), statusValue(), kindValue());
      if (found.length && !found.some(n=>String(n.id)===String(selected))) selected=found[0].id;
      byId('r26-match-count').textContent = `${found.length} of ${nodes.length} entries match. ${found.length ? 'The map includes direct neighbors, including context outside the catalog filters.' : 'The last selected neighborhood stays visible; clear filters to choose another entry.'}`;
      drawSelection();
    }
    function selectFromEvent(event) {
      const button = event.target.closest?.('button[data-r26-node]');
      const id = button?.getAttribute('data-r26-node');
      if (!id || !nodeById.has(String(id))) return;
      selected=id; drawSelection();
      const title=byId('r26-selected-title');
      if(title){ title.setAttribute('tabindex','-1'); title.focus({preventScroll:true}); }
    }
    for (const id of ['r26-catalog','r26-map','r26-details']) byId(id).addEventListener('click',selectFromEvent);
    byId('r26-search').addEventListener('input',updateFilters);
    for (const id of ['r26-status','r26-kind']) byId(id).addEventListener('change',updateFilters);
    byId('r26-edge-type').addEventListener('change',drawSelection);
    byId('r26-reset').addEventListener('click',()=>{byId('r26-search').value='';byId('r26-status').value='all';byId('r26-kind').value='all';byId('r26-edge-type').value='all';selected=initialNode()?.id??'';updateFilters();});
    byId('r26-map-toggle').addEventListener('click',()=>{const map=byId('r26-map'),button=byId('r26-map-toggle');map.hidden=!map.hidden;button.setAttribute('aria-expanded',String(!map.hidden));button.textContent=map.hidden?'Show visual map':'Hide visual map';});
    drawSelection();
  }
  window.ResearchRound26 = {render, afterRender, filteredNodes, neighborhood, graphMap, nodeDetails, catalog, status, safeSource, validEdges, data:D};
  window.ResearchObservatory = {...prior, render, afterRender};
})();
