# Final presentation evidence

The authoritative ten-loop browser and visual QA record is `site-qa-final.json`. It binds all rendered site assets, current research inputs, the final 232-page PDF and the five screenshots in `final-render/`. Earlier `site-qa-active.json` describes an explicitly earlier development checkpoint. Presentation and release checks add zero scientific investigations.

# Current HNM website presentation

The site reads `advisor/findings.json`, source-bound final gates, `network.json`, `experts/sources.json` and the canonical `papers/draft-02/registry/hnm-registry.json`. Only records with checked final gates become reviewed results. Exact tagged equations are copied from the bound forward reports and displayed with the gate's accepted scope and limitations.

Historical research and manuscript bytes remain unchanged. The current catalog maps Hruday/HNM project names to original records; it does not rename established mathematics or assert scientific priority. Current graph presentation preserves original node labels while distinguishing scoped source inputs, proven dependencies, proposed transfers, review relations and open scope boundaries.

After the complete manuscript and all ten reviewed loops exist:

```bash
python3 research/round29/build_site.py --require-complete
python3 scripts/build_pages.py
node tests/round29_site.mjs
```

The final build requires ten sequential source-bound gates, five completed pairs, all ten current aliases, each reviewed network route, the current primary-source review, next-goal assessment and Draft02 PDF. It copies the PDF and registry to static download assets.

Optional rendered checks require Playwright and Chromium:

```bash
node tests/round29_browser.mjs
```

`YM_PLAYWRIGHT_MODULE`, `YM_CHROMIUM_EXECUTABLE` and `YM_QA_OUTPUT` can select an existing local runtime and output folder. The browser check exercises desktop/mobile presentation, all current routes, the historical home, registry search, network search/reset/map visibility, and the downloaded PDF. Inspect the output screenshots separately; programmed route checks alone are not a visual review. `site-qa-active.json` records the inspected active-cycle checkpoint, not the final ten-loop release.

Current routes:

- `#research`: new research home and first reading paths.
- `#research/hnm-priorities`: ranked scoped results, with applications and limits.
- `#research/hnm-findings`: complete searchable naming registry; `contributions` is an alias.
- `#research/drafts`: full Draft02 and preserved earlier editions.
- `#research/round29-results`: every selected/current investigation.
- `#research/research-network`: current graph and labeled dependencies.
- `#research/round29-sources`: current primary-source comparison.
- `#research/round29-roadmap`: next goals planned from the reviewed cycle.
- `#research/sharing`: Substack and Reddit post drafts, not published posts.
