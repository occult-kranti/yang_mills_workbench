# Round30 website layer

The additive layer uses the current Draft03 registry and Round30 network with the inherited searchable catalog and interactive graph. Round29 routes and its frozen data remain available. The new reader pages show exactly the three source-bound investigations, their limitations, complete draft, source reading records and unexecuted roadmap.

The data builder refuses incomplete research releases. It requires three sequential gates, current gate-input hashes, the Draft03 registry, a network containing all three loop routes, both expert ledgers, the next roadmap and both PDF editions. It does not fabricate pending results or validate mathematics by presentation checks.

Build after final sources exist:

```bash
python3 research/round30/presentation/build_site.py --require-complete
node tests/round30_site.mjs
```

The builder writes only `dist/research-round30-data.js` and `dist/hnm-registry-r30.json`. The root release integration copies the reviewed manuscript to `dist/ym-draft-03.pdf` and performs the final deterministic `docs/` build. The previous registry download remains unchanged.

Render the real final data:

```bash
node tests/round30_browser.mjs
```

Set `YM_SITE_FOLDER=docs` to test the published build. `YM_PLAYWRIGHT_MODULE`, `YM_CHROMIUM_EXECUTABLE`, `YM_SITE_PORT` and `YM_QA_OUTPUT` can override local runtime paths. Screenshots require a separate visual inspection; merely writing them is not visual verification.

Current routes are `#research/home`, `#research/round30-results`, `#research/round30-<loop>`, `#research/round30-roadmap`, `#research/round30-sources`, `#research/round30-proof` and `#research/drafts`. The catalog, ranked table and graph retain their established routes. `#research/round29` opens the previous checkpoint.

Source text is escaped, external links require HTTPS without user credentials, relative paths reject traversal, and unreviewed loop data cannot render an accepted conclusion. The three-investigation count is never presented as proof-completion percentage.

The `#research/round30-calculator` page uses the admitted AT2 certificate. JavaScript BigInt fractions preserve exact input arithmetic; displayed decimals are explicitly rounded. Positive alpha and signed tau inside the numerical cap are adjustable, while L=8, c=3 and b=49 remain fixed. It reports unnormalized spectral mass and a reduced inverse-energy form, without claiming a susceptibility or an evaluated AQ spectrum. Tests compare the browser arithmetic with the supplied Python evaluator at both coupling signs, zero and changed scales. The fixture figure is bound to its AT2 gate and retains the exact source caption.
