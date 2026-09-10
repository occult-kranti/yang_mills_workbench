# Round18: six loops on three Yang–Mills roadmap goals

This release continues Round17 with the same three scientific roles: an advisor–skeptic, a forward researcher and an independent backward researcher. Each goal has two sequential loops, with a second advisor decision after Goal A. Accepted results are conditional mathematical bounds or controlled static integrals. They do not solve the four-dimensional Yang–Mills existence and mass-gap problem.

## Local launch

From the repository root:

```bash
python3 start.py
```

Open http://127.0.0.1:8001/#research. The published version is [GitHub Pages](https://occult-kranti.github.io/yang_mills_workbench/#research). The static site displays recorded exact results and their data; it does not run the Python research in your browser.

## Reproduce the research

Use Python 3.10 or newer. The six scientific modules use standard-library exact rational arithmetic. Plot generation additionally uses NumPy and Matplotlib. Select a new output directory outside the accepted `research/round18` directory:

```bash
python3 research/round18/reproduce.py --output /tmp/ym18-fresh
python3 research/round18/reproduce.py --optimized --output /tmp/ym18-optimized
python3 research/round18/proof_routes.py --output /tmp/ym18-proof.json
```

A destination that already exists is rejected. On Windows, use `py -3` and an appropriate absolute directory. The reproduction command verifies frozen source inventories, copies the accepted sources, executes each forward and independent implementation, reruns each independent producer comparison, and compares the resulting records with the accepted release. Normal and optimized execution repeat the same scientific checks and are counted once.

Individual loops can be run using their `check.py --output` interface. The backward modules additionally provide `compare.py --producer SOURCE --evidence OUTPUT --output NEW_DIRECTORY`. They reconstruct the required quantities independently instead of treating the producer's passed JSON as proof authority.

## Read the evidence

Start with the six summaries on the homepage. Each detailed page links its frozen contract, both derivations, accepting gate, rejecting controls and plotted CSV where applicable. `advisor/feedback-log.md` records the decisions between loops. `advisor/post-a-roadmap.md` records how the first goal changed the remaining work. `next-roadmap.md` lists the next unresolved obligations.

The dependency planner searches a finite library of reviewed conventional implications in both directions. It reruns independent arithmetic before admitting execution gates and checks an ordered proof certificate separately from the forward/backward meeting. It is not a theorem prover for unrestricted mathematics. Withdrawing a physical assumption must block any route that needs it. Open dense-uniform, full-bulk and continuum bridges are never starting facts.

The Hamiltonian convention is `H = alpha sum C_e - sum lambda_p x_p`, with `C_e = j(j+1)` and `x_p = Tr(U_p)/2`. Growing-volume claims require `alpha >= alpha_min > 0` in one energy unit. The static Euclidean coefficient `kappa` is a separate variable; no matched physical time generator is supplied by an integral alone.

## Build and publish

```bash
python3 research/round18/build_report.py
python3 research/round18/build_site_data.py
python3 research/round18/draw_network.py
python3 research/round18/draw_two_links.py
python3 research/round18/draw_figures.py
python3 research/round18/package_review.py
python3 scripts/build_pages.py
```

The page-data build requires the accepted six gates, the reviewed proof result and independent integration review already supplied in this release. It rejects stale reviewed source bytes. Regenerating figures changes presentation files, not frozen scientific evidence.

The source site is `dist/`; `docs/` is its GitHub Pages mirror. Commit both along with the reproducible research. No access token belongs in the repository or its public archive.

## Limits

A finite-cluster or finite-graph gap estimate is not a homogeneous volume-uniform gap. A spatially decaying, fully supported family is a specified inhomogeneous exception. A two-link conditional integral leaves the other link variables fixed. None alone constructs the required continuum quantum field theory. Agent review is not credentialed human peer review. Browser layout and keyboard review are recorded separately from source and static interface checks.

Final planning feedback: [next-roadmap-supplement.md](advisor/next-roadmap-supplement.md) clarifies fixed local coefficients, nonplanar cycles and valid discriminators. The reviewed base roadmap is preserved.

Final integration evidence: [independent report](backward/integration/report.md), [99-check record](backward/integration/results.json), [16-check author presentation review](forward/final-review/results.json), [site checks](site-validation.json), and [scientific figure review](visual-review.json). These scopes and counts are separate from the six loop gates.
