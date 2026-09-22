/* Manuscript shelf. Research claims and original artifact bytes stay frozen. */
(() => {
  'use strict';
  const prior = window.ResearchObservatory;
  const draft = window.YM_DRAFTS?.drafts?.find(d => d.id === window.YM_DRAFTS.latest);
  if (!prior || !draft) return;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const source = 'https://github.com/occult-kranti/yang_mills_workbench/tree/main/papers/draft-01';
  function render(route) {
    if (String(route).split('?')[0] !== 'drafts') return prior.render(route);
    return `<div class="drafts-page">
      <nav class="rc-nav" aria-label="Research navigation"><a href="#research">Current findings</a><a href="#research/drafts" aria-current="page">Drafts</a><a href="#research/research-network">Research network</a><a href="#research/all-results">Every round</a><a href="#research/round26-roadmap">Next goals</a></nav>
      <header class="drafts-heading"><p class="rc-kicker">Research manuscripts · Draft 01 · 22 September 2026</p><h1>From the first model<br>to the next question.</h1><p>The research record in one paper: what we started with, what changed, the equations and derivations, and the work still ahead.</p></header>
      <article class="drafts-feature" aria-labelledby="draft-title">
        <a class="drafts-cover" href="ym-draft-01.pdf" aria-label="Read Draft 01 PDF"><img src="ym-draft-01-cover.png" alt="Title page of Certified finite-model gauge calculations" width="596" height="842"></a>
        <div class="drafts-copy"><span class="drafts-status">${esc(draft.status)}</span><h2 id="draft-title">${esc(draft.title)}</h2><p class="drafts-subtitle">${esc(draft.subtitle)}</p><p>Follow the surviving record from the early Maxwell–Dirac calculations through Round26’s source corrections, Wilson observables, and computed heat evolution. Each contribution connects its derivation to possible applications, earlier understanding, limitations, and next steps.</p>
          <dl class="drafts-stats"><div><dt>Pages</dt><dd>${draft.pages}</dd></div><div><dt>Contribution rows</dt><dd>${draft.contributions}</dd></div><div><dt>Historical entries</dt><dd>${draft.history_entries}</dd></div><div><dt>Figures</dt><dd>${draft.figures}</dd></div></dl>
          <div class="drafts-actions"><a class="drafts-primary" href="ym-draft-01.pdf">Read the paper ↗</a><a href="ym-draft-01.pdf" download="yang_mills_first_draft.pdf">Download PDF</a><a href="ym-draft-01-source.zip" download="yang_mills_reproducibility_bundle.zip">LaTeX &amp; reproducibility ZIP · 3.1 MB</a></div>
          <p class="drafts-note">The <strong>**</strong> markers identify workbench contributions. Scientific priority remains unverified. Author names and affiliations are pending; this draft has not been submitted to arXiv.</p>
        </div>
      </article>
      <section class="drafts-section" aria-labelledby="draft-reading"><h2 id="draft-reading">Choose where to start</h2><div class="drafts-reading">
        <a href="ym-draft-01.pdf#page=7"><span>01 / Origins</span><strong>The initial problem</strong><small>Regulated mean fields, consistency checks, and the move toward finite gauge theory. Page 7 →</small></a>
        <a href="ym-draft-01.pdf#page=30"><span>02 / Recent results</span><strong>Sources, observables, heat</strong><small>Rounds 23–26, with brief derivations and the conditions each result needs. Page 30 →</small></a>
        <a href="ym-draft-01.pdf#page=60"><span>03 / Contribution catalog</span><strong>Applications and limits</strong><small>Grouped contributions, equations, changes from earlier understanding, and next obligations. Page 60 →</small></a>
        <a href="ym-draft-01.pdf#page=57"><span>04 / Next steps</span><strong>The planned goals</strong><small>AG, AH, and AI are planned. Two later goals remain unselected. Page 57 →</small></a>
      </div></section>
      <details class="drafts-reader"><summary>Read the PDF on this page</summary><p><a href="ym-draft-01.pdf">Open the PDF directly</a> if your browser does not display the reader.</p><iframe title="Draft 01 research manuscript, 92 pages" src="ym-draft-01.pdf#view=FitH" loading="lazy"></iframe></details>
      <section class="drafts-section" aria-labelledby="draft-companions"><h2 id="draft-companions">Work alongside the paper</h2><div class="drafts-companions">
        <article><p class="rc-kicker">Interactive companion</p><h3>Calculate within the stated ranges</h3><p>Explore the Gaussian correction, compact filter, Wilson endpoints, and physical heat error budget. The interface shows rounded numerical values; the Python package includes exact rational checks.</p><a class="drafts-primary" href="ym-draft-01-calculators.html">Open calculators →</a><p><a href="ym-draft-01-calculators.html" download="calculators.html">Download for offline use</a></p></article>
        <article><p class="rc-kicker">Review and reproduction</p><h3>Inspect the evidence</h3><p>The recorded suites passed ${draft.checks.calculator} calculator checks, ${draft.checks.skeptic} skeptic checks, and ${draft.checks.html} HTML checks. These are programmed checks with declared scopes. The full historical production archive was not rerun for this manuscript.</p><ul><li><a href="${source}/audit/skeptic-review.md">Read the skeptic review</a></li><li><a href="${source}/audit/contribution-catalog.json">Inspect the contribution catalog</a></li><li><a href="${source}">Browse LaTeX, figures, calculators, and audit files</a></li></ul></article>
      </div></section>
      <section class="drafts-section" aria-labelledby="draft-figures"><h2 id="draft-figures">Figures from the draft</h2><div class="drafts-figures"><figure><a href="ym-draft-01-network.png"><img src="ym-draft-01-network.png" alt="Evidence network grouped by historical round, current equations, premises, and planned goals" loading="lazy"></a><figcaption>158 nodes and 260 directed relations. The layout organizes recorded dependencies and proposed transfers; distance has no physical meaning. <a href="#research/research-network">Explore the interactive network →</a></figcaption></figure><figure><a href="ym-draft-01-wilson.png"><img src="ym-draft-01-wilson.png" alt="Wilson endpoint plots comparing real and imaginary responses, spectral weights, and operator moments" loading="lazy"></a><figcaption>Wilson endpoint functions within the stated small-parameter range. The source bundle includes vector figures and plot data.</figcaption></figure></div></section>
      <section class="drafts-section drafts-boundary"><h2>What this draft establishes</h2><p>The paper collects finite-model identities, conditional bounds, certified arithmetic, numerical diagnostics, and failed approaches. Model-agent review is documented alongside its limits. The homogeneous all-stage construction, physical scale calibration, and continuum Yang–Mills mass gap remain open.</p></section>
      <section class="drafts-section"><h2>Draft history</h2><div class="drafts-table"><table><caption>Published workbench drafts</caption><thead><tr><th>Version</th><th>Coverage</th><th>Status</th><th>Files</th></tr></thead><tbody><tr><th scope="row">Draft 01<br><small>22 Sep 2026</small></th><td>Surviving Rounds 3–26 and next planned goals</td><td>First draft for author review</td><td><a href="ym-draft-01.pdf">PDF</a> · <a href="ym-draft-01-source.zip">Source ZIP</a></td></tr></tbody></table></div><details class="drafts-integrity"><summary>Source checkpoint and file integrity</summary><p>Research commit: <a href="https://github.com/occult-kranti/yang_mills_workbench/tree/${draft.source_commit}"><code>${draft.source_commit}</code></a></p><p>PDF SHA-256: <code>${draft.assets['ym-draft-01.pdf'].sha256}</code></p><p>The source ZIP contains its own file manifest. This publication adds no new physics loops.</p></details></section>
    </div>`;
  }
  function afterRender() {
    if (location.hash.split('/')[1]?.split('?')[0] !== 'drafts') return prior.afterRender();
    window.ResearchJourney?.cleanup?.();
    document.title = 'Research drafts · Yang–Mills Workbench';
  }
  window.ResearchDrafts = {render, afterRender};
  window.ResearchObservatory = {...prior, render, afterRender};
})();
