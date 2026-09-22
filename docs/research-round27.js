/* Round27 renders reviewed records; earlier research and manuscript renderers remain intact. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory, D = window.ROUND27_DATA;
  if (!prior || !D) return;
  const array = value => Array.isArray(value) ? value : [];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const loops = array(D.loops), experts = array(D.experts);
  const idOf = loop => String(loop.id ?? loop.loop ?? '').toLowerCase();
  const validId = id => /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(String(id));
  const loopByRoute = new Map(loops.filter(x => validId(idOf(x))).map(x => ['round27-' + idOf(x), x]));
  const ownRoutes = new Set(['home', 'round27', 'round27-results', 'round27-experts', 'round27-proof', 'round27-roadmap', ...loopByRoute.keys()]);
  const splitRoute = value => String(value ?? 'home').split('?')[0] || 'home';
  const routeLink = (route, label) => validId(route) ? `<a href="#research/${esc(route)}">${esc(label)}</a>` : esc(label);
  function safePath(value) {
    const raw = String(value ?? '');
    if (!raw || /[\s\\:#?<>"'\u0000-\u001f\u007f]/.test(raw) || raw.startsWith('/')) return '';
    const parts = raw.split('/');
    if (parts.some(part => !part || part === '.' || part === '..' || /%/.test(part))) return '';
    return parts.map(part => encodeURIComponent(part)).join('/');
  }
  function safeURL(value, local = false) {
    const raw = String(value ?? '');
    if (/^https:\/\/[^\s\\<>"'\u0000-\u001f\u007f]+$/i.test(raw)) {
      try {
        const url = new URL(raw);
        if (url.protocol === 'https:' && url.hostname && !url.username && !url.password) return url.href;
      } catch {}
    }
    return local ? safePath(raw) : '';
  }
  function safeSource(source) {
    const item = typeof source === 'string' ? {path:source} : source ?? {};
    const path = safePath(item.path);
    const url = item.url ? safeURL(item.url) : path ? `https://github.com/occult-kranti/yang_mills_workbench/blob/main/${path}` : '';
    const label = item.title ?? item.label ?? item.path ?? item.url ?? 'Source unavailable';
    return url ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} <span aria-hidden="true">↗</span></a>` : `<span class="r27-unlinked">${esc(label)}</span>`;
  }
  const textOf = value => typeof value === 'string' ? value : value?.text ?? value?.summary ?? value?.title ?? '';
  const list = values => array(values).length ? `<ul>${array(values).map(value => `<li>${esc(textOf(value))}</li>`).join('')}</ul>` : '';
  const sources = values => array(values).length ? `<ul class="r27-evidence">${array(values).map(value => `<li>${safeSource(value)}</li>`).join('')}</ul>` : '<p class="r27-muted">No source is attached to this record.</p>';
  const verdictText = loop => String(loop.verdict ?? loop.status ?? 'Review not recorded');
  function verdictClass(loop) {
    const verdict = verdictText(loop).toLowerCase();
    if (/limited|insufficient|reject|fail|counterexample/.test(verdict)) return 'limited';
    if (/conditional/.test(verdict)) return 'conditional';
    if (/pending|planned|unexecuted|not recorded|in.progress/.test(verdict)) return 'planned';
    if (/accepted|proved|pass|complete/.test(verdict)) return 'accepted';
    return 'neutral';
  }
  const badge = loop => `<span class="r27-badge r27-badge-${verdictClass(loop)}">${esc(verdictText(loop).replaceAll('_', ' '))}</span>`;
  const count = value => Number.isInteger(value) && value >= 0 ? value : null;
  function executionCounts() {
    return {
      completed: count(D.progress?.completed),
      requested: count(D.progress?.requested)
    };
  }
  function nav(current) {
    const entries = [['home','Current findings'],['round27-results','Three-loop record'],['round27-experts','Expert sources'],['round27-proof','Proof obligations'],['research-network','Research network'],['drafts','Drafts'],['round27-roadmap','Next goals']];
    return `<nav class="rc-nav" aria-label="Research navigation">${entries.map(([route,label]) => `<a href="#research/${route}"${current === route || current === 'round27' && route === 'home' ? ' aria-current="page"' : ''}>${label}</a>`).join('')}</nav>`;
  }
  function progressStatement() {
    return `<section class="r27-scope" aria-labelledby="r27-progress-title"><p class="rc-kicker">The panel’s assessment</p><h2 id="r27-progress-title">How much of Yang–Mills is solved?</h2><p>${esc(D.progress?.percentage_statement ?? 'No percentage assessment has been recorded.')}</p><p class="r27-muted">Executed loops count completed investigations, including limited outcomes. They are not a percentage of the mathematical problem solved.</p>${routeLink('round27-proof','Inspect each proof obligation →')}</section>`;
  }
  function loopCard(loop, index) {
    return `<article class="rc-result r27-loop-card"><div class="r27-card-top"><p class="rc-kicker">Loop ${index + 1} · ${esc(idOf(loop).toUpperCase())}</p>${badge(loop)}</div><h2>${esc(loop.title ?? idOf(loop))}</h2><p>${esc(loop.accepted ?? loop.summary ?? '')}</p>${array(loop.limitations).length ? `<p class="r27-card-limit"><strong>Limit:</strong> ${esc(textOf(loop.limitations[0]))}</p>` : ''}<p>${routeLink('round27-' + idOf(loop),'Read derivation, review and evidence →')}</p></article>`;
  }
  function addendumNotice() {
    const url = safeURL(D.addendum?.url, true);
    if (!url) return '';
    return `<aside class="r27-addendum" aria-label="Round27 manuscript addendum"><p class="rc-kicker">After Draft 01</p><h2>${esc(D.addendum.title ?? 'Round27 addendum')}</h2><p>The original draft remains available below. The addendum records the later investigations and their accepted scope.</p><a href="${esc(url)}">Read the addendum ↗</a> · ${routeLink('round27-results','Inspect the three-loop evidence →')}</aside>`;
  }
  function home() {
    const counts = executionCounts();
    return `<header class="rc-hero r27-hero"><div><p class="rc-kicker">Round27 · historical methods, modern checks</p><h1>${esc(D.title ?? 'Three investigations. Each result with its evidence.')}</h1><p>${esc(D.summary ?? '')}</p><div class="rc-hero-actions">${routeLink('round27-results','Read the current results →')}${routeLink('round27-experts','Explore the source corpus →')}${routeLink('research-network','Trace research dependencies →')}</div></div><aside class="rc-score r27-count"><span class="rc-score-number">${counts.completed ?? '—'}${counts.requested === null ? '' : `<small> / ${counts.requested}</small>`}</span><strong>Research loops executed</strong><small>${counts.completed === null ? 'Execution count has not been recorded.' : 'An execution count, including limited outcomes.'}</small></aside></header><section class="r27-method-note"><h2>A panel of research methods</h2><p>Model agents use documented ideas associated with Newton, Tesla, Jung, Penrose and Feynman. Their source records distinguish historical material, modern physics and speculative leads. These are model-agent reviews, not statements or endorsements by those people.</p>${routeLink('round27-experts','Read the experts’ sources and limits →')}</section><section class="r27-results" aria-labelledby="r27-results-title"><div class="r27-section-head"><h2 id="r27-results-title">What changed in this round</h2><span>${loops.length} recorded investigations</span></div><div class="r27-grid">${loops.map(loopCard).join('')}</div></section>${progressStatement()}${D.addendum ? addendumNotice() : ''}<section class="r27-next"><h2>Continue from the remaining premises</h2><p>Inspect the selected next targets and the evidence inherited from earlier rounds.</p>${routeLink('round27-roadmap','Read the revised roadmap →')} · ${routeLink('round26-home','Round26 checkpoint →')} · ${routeLink('all-results','All recorded rounds →')}</section>`;
  }
  function equations(values) {
    if (!array(values).length) return '';
    return `<section class="r27-equations"><h2>Equations and stated conditions</h2>${values.map(value => `<figure>${value.label ? `<figcaption>${esc(value.label)}</figcaption>` : ''}<pre><code>${esc(typeof value === 'string' ? value : value.expression ?? '')}</code></pre>${value.scope ? `<p>${esc(value.scope)}</p>` : ''}</figure>`).join('')}</section>`;
  }
  function loopPage(loop) {
    return `<header class="r22-page-head"><p class="rc-kicker">Round27 · ${esc(idOf(loop).toUpperCase())}</p><h1>${esc(loop.title ?? idOf(loop))}</h1>${badge(loop)}<p>${esc(loop.accepted ?? loop.summary ?? '')}</p></header><section class="rc-section"><h2>What this investigation establishes</h2>${list(loop.bullets)}${loop.review ? `<p>${esc(loop.review)}</p>` : ''}</section>${equations(loop.equations)}<section class="r27-scope"><h2>Scope and limitations</h2>${array(loop.limitations).length ? list(loop.limitations) : '<p>No limitation statement is attached. Consult the review record before interpreting the result.</p>'}</section><section class="rc-section"><h2>Derivation and verification records</h2>${sources(loop.sources)}</section><p>${routeLink('round27-results','Back to the three-loop record →')} · ${routeLink('research-network','Explore the dependency network →')}</p>`;
  }
  function results() {
    return `<header class="r22-page-head"><p class="rc-kicker">Round27 · execution and review record</p><h1>Results with their limits attached.</h1><p>Each verdict belongs to its stated model and premises. Source records provide the derivations and executable checks.</p></header><div class="r27-grid">${loops.map(loopCard).join('')}</div>${progressStatement()}`;
  }
  function expertSources(expert) {
    return array(expert.sources).length ? `<ul class="r27-source-cards">${expert.sources.map(source => `<li><div>${safeSource(source)}</div><dl>${source.depth ? `<div><dt>Reading depth</dt><dd>${esc(source.depth)}</dd></div>` : ''}${source.status ? `<div><dt>Evidence status</dt><dd>${esc(source.status)}</dd></div>` : ''}</dl></li>`).join('')}</ul>` : '<p class="r27-muted">No sources are attached to this expert record.</p>';
  }
  function expertPage() {
    return `<header class="r22-page-head"><p class="rc-kicker">Historical inspiration · source provenance</p><h1>What the experts read, and what it supports.</h1><p>Historical notes, occult interpretations, patents, conversations and current research have different evidential roles. Each source retains the reading depth and status recorded by the panel.</p></header><section class="r27-method-note"><p>The names identify research perspectives used by model agents. Historical material can motivate a question; a modern derivation and its tests determine the mathematical claim.</p></section><div class="r27-experts">${experts.map(expert => `<article class="r27-expert"><p class="rc-kicker">${esc(expert.id ?? 'Research perspective')}</p><h2>${esc(expert.name ?? '')}</h2><p>${esc(expert.summary ?? '')}</p>${expertSources(expert)}${expert.report ? `<p>${safeSource({path:expert.report,title:'Read this research review'})}</p>` : ''}${expert.final_review ? `<p>${safeSource({path:expert.final_review,title:'Read the final three-loop assessment'})}</p>` : ''}</article>`).join('')}</div>`;
  }
  function proofPage() {
    const obligations = array(D.progress?.obligations);
    return `<header class="r22-page-head"><p class="rc-kicker">Progress assessment · explicit obligations</p><h1>The proof still has to cross these steps.</h1><p>${esc(D.progress?.percentage_statement ?? 'No percentage assessment has been recorded.')}</p></header><section class="r27-proof-note"><p>A count of simulations, equations or completed research loops does not measure the fraction of a Yang–Mills existence and mass-gap proof completed. The table reports each obligation at the panel’s stated scope.</p></section>${obligations.length ? `<div class="r27-table-wrap" role="region" aria-label="Yang–Mills proof obligations" tabindex="0"><table class="r27-table"><caption>Proof obligations and missing inputs recorded in Round27</caption><thead><tr><th scope="col">Obligation</th><th scope="col">Current status</th><th scope="col">Still required</th></tr></thead><tbody>${obligations.map(obligation => `<tr><th scope="row">${esc(obligation.name)}</th><td>${esc(obligation.status)}</td><td>${Array.isArray(obligation.missing) ? list(obligation.missing) : esc(obligation.missing)}</td></tr>`).join('')}</tbody></table></div>` : '<p class="r27-muted">No obligation inventory is attached to the current record.</p>'}<p>${routeLink('round27-roadmap','See the targets selected from these gaps →')}</p>`;
  }
  function roadmap() {
    return `<header class="r22-page-head"><p class="rc-kicker">Panel-selected continuation · planning only</p><h1>The next goals start from the missing inputs.</h1><p>${esc(D.roadmap?.summary ?? 'The following targets are proposed work. They are not counted as executed investigations.')}</p></header><div class="r27-grid">${array(D.roadmap?.next_goals).map(goal => `<article class="rc-result"><p class="rc-kicker">${esc(goal.id ?? '')} · planned</p><h2>${esc(goal.title ?? '')}</h2><p>${esc(goal.target ?? goal.first_target ?? '')}</p></article>`).join('')}</div><p>${routeLink('round27-proof','Review the proof obligations →')} · ${routeLink('research-network','Trace the current research network →')}</p>`;
  }
  function render(value = 'home') {
    const route = splitRoute(value);
    if (route === 'research-network') {
      return prior.render(value)
        .replace(/<nav class="rc-nav"[^>]*>[\s\S]*?<\/nav>/, nav(route))
        .replace(/<footer class="rc-footer">[\s\S]*?<\/footer>/, `<footer class="rc-footer"><strong>Yang–Mills Workbench · Round27</strong>${routeLink('round27-results','Current results')}${routeLink('round27-proof','Proof obligations')}${routeLink('round27-roadmap','Current roadmap')}</footer>`);
    }
    if (route === 'round26-home') return `<div class="rc-history-notice">Archived Round26 checkpoint. ${routeLink('home','Current findings →')}</div>` + prior.render('home');
    if (route === 'drafts') return `<div class="r27 r27-draft-notice">${addendumNotice()}</div>` + prior.render(value);
    if (route === 'all-results' || route === 'contributions') return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27"><section class="r27-archive-note"><p class="rc-kicker">Current continuation</p><h2>Round27 research record</h2><p>${loops.length} investigations with source records, verdicts and limitations.</p>${routeLink('round27-results','Read the Round27 results →')}</section></div>` + prior.render(value);
    if (!ownRoutes.has(route)) return prior.render(value);
    const loop = loopByRoute.get(route);
    const body = loop ? loopPage(loop) : route === 'round27-results' ? results() : route === 'round27-experts' ? expertPage() : route === 'round27-proof' ? proofPage() : route === 'round27-roadmap' ? roadmap() : home();
    return `<div class="rc20 r21 r22 r23 r24 r25 r26 r27">${nav(route)}${body}<footer class="rc-footer"><strong>Yang–Mills Workbench · Round27</strong>${routeLink('round27-experts','Source corpus')}${routeLink('round27-proof','Proof obligations')}${routeLink('round26-home','Round26 archive')}${routeLink('all-results','All recorded rounds')}</footer></div>`;
  }
  function afterRender() {
    const route = splitRoute(location.hash.replace(/^#research\/?/, '') || 'home');
    if (route === 'round26-home') {
      window.ResearchJourney?.cleanup?.();
      document.title = 'Round26 archive · Yang–Mills Workbench';
      return;
    }
    if (!ownRoutes.has(route)) return prior.afterRender();
    window.ResearchJourney?.cleanup?.();
    const names = {'round27-experts':'Expert sources','round27-proof':'Proof obligations','round27-roadmap':'Next research goals','round27-results':'Three-loop record'};
    document.title = `${loopByRoute.get(route)?.title ?? names[route] ?? 'Round27'} · Yang–Mills Workbench`;
  }
  window.ResearchRound27 = {render, afterRender, safeURL, safeSource, safePath, executionCounts, verdictClass, data:D};
  window.ResearchObservatory = {...prior, render, afterRender};
})();
