'use strict';

/*
 * The patent room is deliberately a pure view.  The host application owns
 * routing, persistence, and event delegation; this file only turns a data
 * snapshot into escaped HTML and supplies the two filter functions.
 */
(function (root) {
  const esc = value => String(value == null ? '' : value).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));

  const text = value => Array.isArray(value) ? value.filter(v => v != null).join(' ') : String(value == null ? '' : value);
  const validURL = value => /^https?:\/\//i.test(String(value || '').trim()) ? String(value).trim() : '';
  const href = value => esc(validURL(value));
  const sourceLink = (url, label) => {
    const u = validURL(url);
    return u ? `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(label || u)} ↗</a>` : '';
  };
  const list = (values, empty = 'Not supplied.') => {
    const a = Array.isArray(values) ? values.filter(v => v != null && String(v).trim()) : [];
    return a.length ? `<ul>${a.map(v => `<li>${esc(v)}</li>`).join('')}</ul>` : `<p class="muted">${esc(empty)}</p>`;
  };
  const labelValue = (label, value, fallback = 'Not supplied.') => `<p><strong>${esc(label)}:</strong> ${esc(value == null || value === '' ? fallback : value)}</p>`;

  function formatDate(value) {
    const s = String(value == null ? '' : value).trim();
    if (!s) return 'Not listed';
    const iso = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
    if (iso) return `${iso[3].padStart(2, '0')}.${iso[2].padStart(2, '0')}.${iso[1]}`;
    return s;
  }

  function patentData(data) {
    return (data && data.patents) || data || {};
  }

  function valuesForSearch(record) {
    const fields = ['id', 'serial', 'section', 'page', 'country', 'title', 'filed', 'granted', 'number', 'application', 'amendments', 'priority', 'notes', 'url', 'sourceUrl', 'correction', 'owner', 'theme', 'themes', 'relation', 'group', 'type', 'connectionType', 'claim', 'catalogueId', 'role', 'shelfmark', 'workDate', 'editionDate', 'boundary', 'task'];
    return fields.map(k => text(record && record[k])).join(' ').toLowerCase();
  }

  function matches(record, filters, kind) {
    const f = filters || {};
    const query = String(f.search || '').trim().toLowerCase();
    if (query && !valuesForSearch(record).includes(query)) return false;
    if (f.country && kind === 'inventory' && String(record.country || '') !== String(f.country)) return false;
    if (f.section && kind === 'inventory' && String(record.section || '') !== String(f.section)) return false;
    if (f.group && kind === 'case' && String(record.group || '') !== String(f.group)) return false;
    const themes = Array.isArray(record.themes) ? record.themes : [record.theme];
    if (f.theme && kind === 'case' && !themes.some(v => String(v || '') === String(f.theme))) return false;
    return true;
  }

  function filterInventory(inventory, filters) {
    return (Array.isArray(inventory) ? inventory : []).filter(r => matches(r, filters, 'inventory'));
  }

  function filterCases(cases, filters) {
    return (Array.isArray(cases) ? cases : []).filter(r => matches(r, filters, 'case'));
  }

  function resourceMap(data) {
    return Object.fromEntries((Array.isArray(data && data.resources) ? data.resources : []).map(r => [r.id, r]));
  }

  function resourceLinks(ids, resources) {
    const map = resources || {};
    const a = (Array.isArray(ids) ? ids : []).map(id => map[id]).filter(Boolean);
    return a.length ? a.map(r => sourceLink(r.url, r.title || r.id)).join(' · ') : '<span class="muted">No linked resource supplied.</span>';
  }

  function hasResourceLink(ids, resources) {
    const map = resources || {};
    return (Array.isArray(ids) ? ids : []).some(id => map[id] && validURL(map[id].url));
  }

  function recordLink(id, label, tab = 'dossiers') {
    if (!id) return esc(label || 'Unidentified record');
    if (tab === 'dossiers' && /^N\d+$/i.test(String(id))) tab = 'newton';
    return `<button class="patent-record-link" type="button" data-patent-find="${esc(id)}" data-patent-tab="${esc(tab)}">${esc(label || id)} →</button>`;
  }

  function chapterLinks(ids, chapters) {
    const map = Object.fromEntries((Array.isArray(chapters) ? chapters : []).map(c => [c.id, c]));
    const a = (Array.isArray(ids) ? ids : []).map(id => map[id] || { id, title: id });
    return a.length ? a.map(c => `<button type="button" data-chapter="${esc(c.id)}">${esc(c.title || c.id)}</button>`).join(' ') : '<span class="muted">No chapter prerequisite supplied.</span>';
  }

  function toolLinks(ids, tools) {
    const map = Object.fromEntries((Array.isArray(tools) ? tools : []).map(t => [t.id, t]));
    const a = (Array.isArray(ids) ? ids : []).map(id => map[id] || { id });
    return a.length ? a.map(t => `<button type="button" data-tool="${esc(t.id)}">${esc(t.name || t.title || t.id)}</button>`).join(' ') : '<span class="muted">No lab tool supplied.</span>';
  }

  function tabs(current) {
    const names = [['dossiers', 'Dossiers'], ['catalogue', 'Catalogue'], ['newton', 'Newton'], ['plan', 'Research plan'], ['evidence', 'Evidence']];
    return `<nav class="patent-tabs" aria-label="Patent room sections">${names.map(([id, label]) => `<a href="#patents/${id}" class="${current === id ? 'active' : ''}"${current === id ? ' aria-current="page"' : ''}>${esc(label)}</a>`).join('')}</nav>`;
  }

  function controls(p, filters, tab) {
    if (!['dossiers', 'catalogue', 'newton'].includes(tab)) return '';
    const inventory = Array.isArray(p.inventory) ? p.inventory : [];
    const cases = Array.isArray(p.cases) ? p.cases : [];
    const countries = [...new Set(inventory.map(x => x.country).filter(Boolean))].sort();
    const groups = [...new Set(cases.map(x => x.group).filter(Boolean))].sort();
    const themes = [...new Set(cases.flatMap(x => Array.isArray(x.themes) ? x.themes : (x.theme ? [x.theme] : [])))].sort();
    const selected = (key, value) => String(filters && filters[key] || '') === String(value);
    const optionList = (values, key) => values.map(v => `<option value="${esc(v)}"${selected(key, v) ? ' selected' : ''}>${esc(v)}</option>`).join('');
    const filtersForTab = tab === 'newton' ? '' : tab === 'catalogue' ? `<label>Historical jurisdiction <select id="patent-country"><option value="">All jurisdictions</option>${optionList(countries, 'country')}</select></label>
      <label>Section <select id="patent-section"><option value="">All sections</option><option value="US"${selected('section', 'US') ? ' selected' : ''}>US</option><option value="Foreign"${selected('section', 'Foreign') ? ' selected' : ''}>Foreign</option></select></label>` : `<label>Group <select id="patent-group"><option value="">All groups</option>${optionList(groups, 'group')}</select></label>
      <label>Theme <select id="patent-theme"><option value="">All themes</option>${optionList(themes, 'theme')}</select></label>`;
    return `<form class="patent-controls" aria-label="Filter patent records" data-patent-filters>
      <label>Search <input id="patent-search" type="search" value="${esc(filters && filters.search || '')}" placeholder="ID, title, owner, number, theme…" autocomplete="off"></label>
      ${filtersForTab}
      <button type="button" data-patent-reset>Reset filters</button>
    </form>`;
  }

  function intro(p, tab) {
    const inventory = Array.isArray(p.inventory) ? p.inventory : [];
    const cases = Array.isArray(p.cases) ? p.cases : [];
    const records = p.newton && Array.isArray(p.newton.records) ? p.newton.records : [];
    return `<div class="patent-intro"><div class="page-title"><div><span class="eyebrow">SOURCE ROOM · PATENTS, CLAIMS, AND CONTEXT</span><h1>Patent research room</h1><p>${esc(p.scope || 'A bounded research desk for reading patent records as dated, claim-bearing sources.')}</p><p class="small">Review date: ${esc(formatDate(p.date))}. Worksheets and module gates save in this browser; use Export backup.</p></div></div><div class="patent-stats" aria-label="Research room counts"><div><strong>${inventory.length}</strong><span>catalogue records</span></div><div><strong>${cases.length}</strong><span>case dossiers</span></div><div><strong>${records.length}</strong><span>Newton records</span></div></div>${tabs(tab)}<p class="small">Related rooms: <a href="#newton-esoteric">Newton · alchemy &amp; sacred history</a> · <a href="#tesla-esoteric">Tesla · philosophy &amp; unusual claims</a> · <a href="#sacred-geometry">Sacred geometry</a></p></div>`;
  }

  function caseCard(c, resources, chapters, first, state) {
    const themes = Array.isArray(c.themes) ? c.themes : (c.theme ? [c.theme] : []);
    const links = hasResourceLink(c.resources, resources) ? resourceLinks(c.resources, resources) : sourceLink(c.url, 'Case source');
    const notes = state && state.patentNotes && typeof state.patentNotes === 'object' ? state.patentNotes : {};
    return `<article class="card patent-case"><div class="patent-card-head"><div><span class="eyebrow">${esc(c.type || 'Case dossier')} · ${esc(c.group || 'Unassigned')}</span><h2>${esc(c.title || c.id || 'Untitled case')}</h2><p class="small">${esc(c.id || '')}${c.owner ? ` · Inventor / record attribution: ${esc(c.owner)}` : ''}${c.date ? ` · ${esc(formatDate(c.date))}` : ''}</p></div><div class="patent-tags">${themes.map(t => `<span class="pill blue">${esc(t)}</span>`).join('')}</div></div>${c.relation || c.connectionType ? `<p class="patent-relation"><strong>Relation:</strong> ${esc(c.relation || '')}${c.connectionType ? ` · ${esc(c.connectionType)}` : ''}</p>` : ''}<details${first ? ' open' : ''}><summary>Claims, inputs, assessment, and source worksheet</summary><div class="patent-detail-grid"><div>${labelValue('Claim', c.claim)}${labelValue('Inputs', c.inputs)}${labelValue('Assessment', c.assessment)}${labelValue('Test', c.test)}</div><div><p><strong>Prerequisite chapters:</strong></p><div class="patent-links">${chapterLinks(c.chapters, chapters)}</div><p><strong>Sources:</strong> ${links || '<span class="muted">No source links supplied.</span>'}</p></div></div><label class="patent-note"><strong>Worksheet</strong><textarea data-patent-note="${esc(c.id || '')}" placeholder="Question / claim:\nControls or inputs:\nUncertainty:\nConclusion:">${esc(notes[c.id] || c.note || '')}</textarea></label></details></article>`;
  }

  function dossiers(p, data, state, filters) {
    const cases = filterCases(p.cases, filters);
    const resources = resourceMap(data);
    const chapters = data.chapters;
    return `${controls(p, filters, 'dossiers')}<section class="patent-section"><div class="section-heading"><div><span class="eyebrow">CLAIM LEDGER</span><h2>Substantive case dossiers</h2></div><p class="muted">${cases.length} matched of ${(p.cases || []).length} cases</p></div>${cases.length ? `<div class="patent-case-list">${cases.map((c, i) => caseCard(c, resources, chapters, i === 0, state)).join('')}</div>` : `<div class="empty">No case dossiers match these filters.<br><button type="button" data-patent-reset>Reset filters</button></div>`}</section>`;
  }

  function inventoryURL(row) {
    return validURL(row && (row.url || row.sourceUrl));
  }

  function catalogue(p, filters) {
    const all = Array.isArray(p.inventory) ? p.inventory : [];
    const rows = filterInventory(all, filters);
    const perPage = 25;
    const pages = Math.max(1, Math.ceil(rows.length / perPage));
    const page = Math.min(pages, Math.max(1, Number(filters && filters.page) || 1));
    const visible = rows.slice((page - 1) * perPage, page * perPage);
    const table = visible.length ? `<div class="table-wrap patent-table-wrap"><table class="data-table patent-table"><caption>Matched catalogue records, page ${page} of ${pages}</caption><thead><tr><th scope="col">Source row</th><th scope="col">Historical jurisdiction</th><th scope="col">Title</th><th scope="col">Filing / grant</th><th scope="col">Number</th><th scope="col">Source PDF page</th></tr></thead><tbody>${visible.map(row => { const u = inventoryURL(row); return `<tr><th scope="row">${esc(row.id || '—')}${row.correction ? `<br><span class="correction">Correction: ${esc(row.correction)}</span>` : ''}</th><td>${esc(row.country || '—')}<br><span class="small">${esc(row.section || '—')}</span></td><td>${esc(row.title || '—')}${row.application ? `<br><span class="small">Application: ${esc(row.application)}</span>` : ''}${row.amendments ? `<br><span class="small">Amendments: ${esc(row.amendments)}</span>` : ''}${row.priority ? `<br><span class="small">Priority: ${esc(row.priority)}</span>` : ''}${row.notes ? `<br><span class="small">${esc(row.notes)}</span>` : ''}</td><td>Filed: ${esc(formatDate(row.filed))}<br>Granted: ${esc(formatDate(row.granted))}</td><td>${u ? sourceLink(u, row.number || row.id || 'Open patent') : esc(row.number || '—')}</td><td>${esc(row.page == null || row.page === '' ? '—' : `p. ${row.page}`)}${row.sourceUrl && validURL(row.url) && row.sourceUrl !== row.url ? `<br>${sourceLink(row.sourceUrl, 'Source')}` : ''}</td></tr>`; }).join('')}</tbody></table></div>` : `<div class="empty">No catalogue records match these filters.<br><button type="button" data-patent-reset>Reset filters</button></div>`;
    return `${controls(p, filters, 'catalogue')}<section class="patent-section"><div class="section-heading"><div><span class="eyebrow">SOURCE TRANSCRIPTION</span><h2>Catalogue</h2><p>Complete numbered rows from the museum’s 2019 list: 112 US and 199 foreign entries. Dates retain day.month.year source format. These are catalogue entries, including equivalents and a reissue; detailed specification review covers the 12 Tesla dossiers. <a href="#patents/evidence">Coverage and corrections →</a></p></div><p class="muted">${rows.length} matched of ${all.length} records · page ${page} of ${pages}</p></div>${table}<div class="patent-pagination" role="navigation" aria-label="Catalogue pages"><button type="button" data-patent-page="${page - 1}"${page <= 1 ? ' disabled' : ''}>Previous</button><span>Page ${page} / ${pages}</span><button type="button" data-patent-page="${page + 1}"${page >= pages ? ' disabled' : ''}>Next</button></div></section>`;
  }

  function newton(p, data, state, filters) {
    const n = p.newton || {};
    const records = Array.isArray(n.records) ? n.records : [];
    const matched = records.filter(r => matches(r, filters, 'newton'));
    const resources = resourceMap(data);
    return `${controls(p, filters, 'newton')}<section class="patent-section"><div class="section-heading"><div><span class="eyebrow">NEWTON RECORDS</span><h2>Manuscripts, editions, and catalogue boundaries</h2></div><p class="muted">${matched.length} matched of ${records.length} records</p></div>${n.scope ? `<p class="patent-scope">${esc(n.scope)}</p>` : ''}<div class="grid two">${matched.length ? matched.map(r => `<article class="card newton-card"><p class="small"><strong>Role:</strong> ${esc(r.role || 'Not listed')} · <strong>Document type:</strong> ${esc(r.type || 'Not listed')}</p><h2>${esc(r.title || r.id || 'Untitled record')}</h2><dl class="record-meta"><dt>Work date</dt><dd>${esc(formatDate(r.workDate))}</dd><dt>Edition date</dt><dd>${esc(formatDate(r.editionDate))}</dd><dt>Shelfmark</dt><dd>${esc(r.shelfmark || 'Not listed')}</dd><dt>Catalogue ID</dt><dd>${esc(r.catalogueId || 'Not listed')}</dd></dl>${labelValue('Claim', r.claim)}${labelValue('Boundary', r.boundary)}${labelValue('Task', r.task)}<p><strong>Chapters:</strong> <span class="patent-links">${chapterLinks(r.chapters, data.chapters)}</span></p><p><strong>Resources:</strong> ${resourceLinks(r.resources, resources)}</p>${validURL(r.url) ? `<p>${sourceLink(r.url, 'Open source record')}</p>` : ''}<label class="patent-note"><strong>Notes</strong><textarea data-patent-note="${esc(r.id || '')}" placeholder="Question / claim:\nControls or evidence:\nUncertainty:\nConclusion:">${esc((state && state.patentNotes && state.patentNotes[r.id]) || r.note || '')}</textarea></label></article>`).join('') : `<div class="empty">${records.length ? 'No Newton records match this search.' : 'No Newton records supplied.'}<br><button type="button" data-patent-reset>Reset filters</button></div>`}</div></section>`;
  }

  function plan(p, data, state) {
    const modules = Array.isArray(p.modules) ? p.modules : [];
    const done = new Set(state && Array.isArray(state.patentDone) ? state.patentDone : []);
    const projects = Array.isArray(p.projects) ? p.projects : [];
    const resources = resourceMap(data);
    const complete = modules.filter(m => done.has(m.id)).length;
    return `<section class="patent-section"><div class="section-heading"><div><span class="eyebrow">RESEARCH ROUTE</span><h2>Plan the reading and evidence work</h2><p>Begin with module 01. Modules 02–06 develop the physics; 07 is the historical branch and 08 the measurement branch. Take advanced module 09 when its prerequisites are secure, then use 10 to complete a research dossier. Open linked chapters to fill gaps and demonstrate each gate before moving on.</p></div><p id="patent-progress" class="muted" role="status">${complete} of ${modules.length} module gates complete</p></div><div class="patent-module-list">${modules.length ? modules.map((m, i) => `<article class="card patent-module"><span class="eyebrow">Module ${i + 1}</span><h2>${esc(m.title || m.id || 'Untitled module')}</h2><p><strong>Prerequisites:</strong> <span class="patent-links">${chapterLinks(m.prereqs, data.chapters)}</span></p><div class="lesson-list">${(Array.isArray(m.lessons) ? m.lessons : []).map((l, j) => `<details class="lesson"${i === 0 && j === 0 ? ' open' : ''}><summary>${esc(l.title || `Lesson ${j + 1}`)}</summary><div><p><strong>Topics:</strong></p>${list(l.topics)}${labelValue('Practice', l.practice)}</div></details>`).join('')}</div><div class="module-gate"><p><strong>Gate:</strong> ${esc(m.gate || 'Not supplied.')}</p><label><input type="checkbox" data-patent-done="${esc(m.id || '')}"${done.has(m.id) ? ' checked' : ''}> I can demonstrate this gate</label></div><p><strong>Resources:</strong> ${resourceLinks(m.resources, resources)}</p><p><strong>Cases:</strong> ${(m.cases || []).map(id => recordLink(id, id, 'dossiers')).join(' ') || '<span class="muted">None supplied.</span>'}</p><p><strong>Lab tools:</strong> ${toolLinks(m.tools, data.tools)}</p></article>`).join('') : '<div class="empty">No research modules supplied.</div>'}</div><div class="section-heading patent-project-heading"><div><span class="eyebrow">PROJECTS</span><h2>Make inspectable outputs</h2></div></div><div class="grid two">${projects.length ? projects.map((x, i) => `<article class="card patent-project"><span class="pill">Project ${i + 1}</span><h3>${esc(x.title || x.id || 'Untitled project')}</h3>${labelValue('Question', x.question)}${labelValue('Software', x.software)}<ol>${(Array.isArray(x.steps) ? x.steps : []).map(step => `<li>${esc(step)}</li>`).join('')}</ol>${labelValue('Gate', x.gate)}${labelValue('Deliverable', x.deliver)}<p><strong>Resources:</strong> ${resourceLinks(x.resources, resources)}</p><p><strong>Chapters:</strong> <span class="patent-links">${chapterLinks(x.chapters, data.chapters)}</span></p><p><strong>Cases:</strong> ${(x.cases || []).map(id => recordLink(id, id, 'dossiers')).join(' ') || '<span class="muted">None supplied.</span>'}</p></article>`).join('') : '<div class="empty">No research projects supplied.</div>'}</div></section>`;
  }

  function evidence(p, data) {
    const allResources = Array.isArray(data.resources) ? data.resources : [];
    const map = resourceMap(data);
    const used = new Set(allResources.filter(r => /^patent-/i.test(String(r.id || ''))).map(r => r.id));
    const collectResources = item => (Array.isArray(item && item.resources) ? item.resources : []).forEach(id => used.add(id));
    (Array.isArray(p.cases) ? p.cases : []).forEach(collectResources);
    (p.newton && Array.isArray(p.newton.records) ? p.newton.records : []).forEach(collectResources);
    (Array.isArray(p.modules) ? p.modules : []).forEach(collectResources);
    (Array.isArray(p.projects) ? p.projects : []).forEach(collectResources);
    const conns = Array.isArray(p.connections) ? p.connections : [];
    const glossary = Array.isArray(p.glossary) ? p.glossary : [];
    const resources = allResources.filter(r => used.has(r.id));
    return `<section class="patent-section evidence-room"><div class="section-heading"><div><span class="eyebrow">EVIDENCE LEDGER</span><h2>Sources, coverage, and boundaries</h2></div></div><div class="grid two evidence-lists"><article class="card"><h3>Coverage</h3>${list(p.coverage)}</article><article class="card"><h3>Protocol</h3>${list(p.protocol)}</article><article class="card"><h3>Gaps</h3>${list(p.gaps)}</article></div><div class="card connections"><h3>Connections</h3>${conns.length ? `<div class="table-wrap"><table class="data-table"><caption>Related record connections</caption><thead><tr><th scope="col">From</th><th scope="col">To</th><th scope="col">Relation</th><th scope="col">Source</th></tr></thead><tbody>${conns.map(c => `<tr><td>${esc(c.from || '—')}</td><td>${esc(c.to || '—')}</td><td>${esc(c.relation || '—')}</td><td>${sourceLink(c.url, 'Open source') || '<span class="muted">Not supplied.</span>'}</td></tr>`).join('')}</tbody></table></div>` : '<p class="muted">No connections supplied.</p>'}</div><details><summary>Patent sources (${resources.length})</summary><div class="resource-list">${resources.length ? resources.map(r => `<article class="resource-row"><div><h3>${sourceLink(r.url, r.title || r.id) || esc(r.title || r.id || 'Untitled source')}</h3><p class="small">${esc(r.publisher || 'Publisher not listed')} · ${esc(formatDate(r.date))}</p><p>${esc(r.use || r.description || '')}</p>${r.note ? `<p class="source-note">${esc(r.note)}</p>` : ''}</div><span class="pill">${esc(r.type || r.access || 'source')}</span></article>`).join('') : '<p class="muted">No linked patent sources supplied.</p>'}</div></details><article class="card glossary"><h3>Glossary</h3>${glossary.length ? glossary.map(g => `<details><summary>${esc(g.term || 'Term')}</summary><p>${esc(g.meaning || '')}</p>${labelValue('Boundary', g.boundary)}<p><strong>Resources:</strong> ${resourceLinks(g.resources, map)}</p></details>`).join('') : '<p class="muted">No glossary entries supplied.</p>'}</article></section>`;
  }

  function render(data, state, filters, tab) {
    const d = data || {};
    const p = patentData(d);
    const f = filters || { search: '', country: '', section: '', group: '', theme: '', page: 1 };
    const current = ['dossiers', 'catalogue', 'newton', 'plan', 'evidence'].includes(tab) ? tab : 'dossiers';
    const body = current === 'catalogue' ? catalogue(p, f) : current === 'newton' ? newton(p, d, state || {}, f) : current === 'plan' ? plan(p, d, state || {}) : current === 'evidence' ? evidence(p, d) : dossiers(p, d, state || {}, f);
    return `<div class="patent-room">${intro(p, current)}${body}</div>`;
  }

  const api = { render, filterInventory, filterCases };
  if (root) root.PatentRoom = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
