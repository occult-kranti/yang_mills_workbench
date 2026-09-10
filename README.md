# Yang–Mills Workbench

A reproducible research workbench for nonabelian gauge theory: explicit finite-model proofs, exact arithmetic certificates, numerical experiments, skeptical audits and a navigable Physics Observatory.

**Research website:** [Open Yang–Mills Workbench on GitHub Pages](https://occult-kranti.github.io/yang_mills_workbench/#research)

**Repository:** [occult-kranti/yang_mills_workbench](https://github.com/occult-kranti/yang_mills_workbench)

The four-dimensional Yang–Mills existence and mass-gap problem remains open. This project separates established mathematics, reviewed finite-model derivations, certified calculations, numerical evidence, failed claims and unproved continuum obligations. It does not claim a Millennium Prize solution or mathematical novelty for known one-plaquette results.

**Current milestone:** the next shared-face subproblem is complete in its finite scope after **two sequential loops with three scientific roles**. The actual two-cube complex has12 vertices,20 links and11 faces. Independent Haar-projector and polynomial calculations certify the shared interaction’s effect on the same all-eleven trace observable, with exact total interval width about4.173e−22. A separate scale audit proves why a common dimensionless gap bound needs a common energy convention. The **numerical volume-uniform interacting threshold and continuum problem remain open**. [Graph and contractions](https://occult-kranti.github.io/yang_mills_workbench/#research/shared-haar), [exact experiment](https://occult-kranti.github.io/yang_mills_workbench/#research/shared-integral), [energy scale](https://occult-kranti.github.io/yang_mills_workbench/#research/physical-scale), [two-loop collaboration](https://occult-kranti.github.io/yang_mills_workbench/#research/shared-team), [updated roadmap](https://occult-kranti.github.io/yang_mills_workbench/#research/shared-roadmap). Detailed code and reproduction instructions: [Round16 guide](research/round16/README.md).

Round15 remains available: a complete21-cell covariance cover over `eta in [1/8,1/4]`, a closed-cube integral rejecting independent-face factorization, and an improved finite physical spectral bound. [Previous dashboard](https://occult-kranti.github.io/yang_mills_workbench/#research/review15-home).

The previous23 point certificates and exact positive covariance at `(1,1,1/4)` remain available in round14, with their original finite Euclidean assumptions.

The earlier two-step drive certificate remains available with total physical Haar L² state error **below 0.000337501** on its finite graph. Historical results are preserved with their original assumptions.

## Launch locally

Install Python 3.11 or newer and Git. The website and calculators need no Python packages, API key, account or JavaScript build step.

```bash
git clone https://github.com/occult-kranti/yang_mills_workbench.git
cd yang_mills_workbench
python3 start.py
```

Open **http://127.0.0.1:8001/#research**. The launcher opens a browser unless `--no-browser` is supplied. Keep the terminal running; press Ctrl+C to stop.

```bash
python3 start.py --no-browser --port 8002
```

On Windows, use `py -3 start.py`. The server binds only to `127.0.0.1`. If the port is occupied, choose another port. Use one address consistently: `localhost`, `127.0.0.1`, GitHub Pages and the earlier private Observatory have separate browser storage. Export and import a backup to transfer notes or progress.

## What works where

| Feature | GitHub Pages | Local Python server |
|---|---|---|
| Research pages, equations, recorded plots and documents | Yes | Yes |
| Exact certificate inspection and CSV/ZIP downloads | Yes | Yes |
| Physics calculators, curriculum and patent archive | Yes | Yes |
| Notes, worksheets and progress | Browser-local | Browser-local |
| Curated sources and direct arXiv category links | Yes | Yes |
| Live arXiv metadata refresh | Use the direct category link | Optional server endpoint; depends on arXiv availability |
| Python simulations and exact proof replays | Download/clone and run locally | Run in a terminal; not executed inside the browser |

GitHub Pages is static hosting. It does not run Python, the previous Worker, a database or a private API proxy. No GitHub token is needed by the website or scientific programs.

## Read the research

Begin at the [research home](https://occult-kranti.github.io/yang_mills_workbench/#research). Each detailed result distinguishes the physical state space, equations, assumptions, derivation, tested cases, skeptic objections and missing implications.

| Research layer | Location | Status and interpretation |
|---|---|---|
| Shared-face subproblem, two loops and three roles | `research/round16/` | Current eleven-face Haar contractions, exact changed-action comparison, physical energy-scale audit and independent checks |
| Three revised goals, six research loops | `research/round15/` | Preserved interval cover, cube integral, finite physical spectral bounds, independent reviews and retained original uniform-threshold gap |
| Three-role, two-loop finite correlation study | `research/round14/` | Preserved exact point covariance, independent rational replay and earlier feedback roadmap |
| Exceptions, locality, compact hierarchy and restricted gap | `research/round13/` | Preserved exact moment certificates, scalar response, fixed-spacing local limit and qualitative uniform-gap theorem application; continuum remains open |
| Driven error, volume and closure bridges | `research/round12/` | Preserved exact dynamic theorem, rational endpoint certificate, source critique and historical roadmap |
| Two adjacent plaquettes | `research/round11/` | Reviewed coupled operator, stationary certificates and finite-graph analytic gap proof |
| One physical SU(2) square | `research/round10/` | Infinite-character spectral tail controlled; exact continuous-coupling gap certificate |
| Four-dimensional finite lattice and SU(2) transfer benchmark | `research/round9/` | Deterministic identities and finite benchmarks; beta=2.2 sampling uncertainty remains insufficient |
| Spectral connection and free-field counterexamples | `research/round8/` | Checks that block invalid finite-volume-to-continuum inferences |
| Earlier Einstein–QED work | `evidence/qeg-research/round3` through `round7` | Retained model-specific evidence; common renormalized current and directional stress remain unresolved |
| Learning and source archive | `dist/`, `curriculum/`, `guides/physics-observatory.md` | Physics curriculum, 29 calculators, subject rooms and patent research |

### Certified one-square result

For four distinct links on one square, after independent vertex Gauss constraints,

\[
H=\alpha\sum_e C_e+\lambda(1-\tfrac12\operatorname{Re}\operatorname{Tr}U_\square),
\qquad \alpha>0,\quad\lambda\ge0.
\]

The physical Hilbert space is the SU(2) class functions. In the character basis indexed by `n=2j`,

\[
H_{nn}=\alpha n(n+2)+\lambda,\qquad H_{n,n+1}=-\lambda/2.
\]

An analytic omitted-tail bound and exact rational Sturm calculations establish

\[
\Delta(\alpha,\lambda)\ge0.999999\,\alpha
\quad\text{for every }0\le\lambda/\alpha\le10.
\]

The representation tower is infinite; the spatial graph is finite. A 2-Lipschitz bound and complete interval coverage extend point certificates to every real coupling in the stated interval. Floating-point Mathieu and radial-grid results are independent comparisons, not the exact proof premises. The one-plaquette/Mathieu solution is established prior work.

### Variables need mathematical obligations

`alpha` is an electric-energy coefficient; `lambda` is a magnetic coefficient; `kappa=lambda/alpha` is a dimensionless physical ratio. `N` or polynomial degree `D` is a numerical regulator. A prescribed `lambda(t)` changes the Hamiltonian and requires its independently integrated work term. A lattice spacing and matched bare coupling require an explicitly stated normalization and scale trajectory.

For two loop holonomies modulo simultaneous conjugation, the physical invariants are

\[
x=\tfrac12\operatorname{Tr}U,\quad y=\tfrac12\operatorname{Tr}V,\quad z=\tfrac12\operatorname{Tr}(UV),
\quad (z-xy)^2\le(1-x^2)(1-y^2),\quad |x|,|y|\le1.
\]

The third trace retains relative orientation lost by two separate loop traces. At a central element (`|x|=1` or `|y|=1`), `z=xy`; a relative-angle formula must not divide by a vanishing sine. Adding coordinates records existing configurations. Inserting an arbitrary mass or scalar would change the theory and cannot establish the pure Yang–Mills target.

## Reproduce the current shared-face study

The [Round16 guide](research/round16/README.md) contains both loop contracts, exact outputs, retained failures and the updated physical roadmap. From the repository root:

```bash
python3 research/round16/reproduce.py --output /absolute/path/to/new-results
python3 research/round16/proof_routes.py --output /absolute/path/to/proof-results.json
```

These run the five research programs and the actual bidirectional proof routes. NumPy supports the matrix diagnostics; Matplotlib is optional for figures. The exact integral code uses standard-library rational arithmetic. No API key is required.

## Reproduce the previous three-goal study

The [round15 guide](research/round15/README.md) records the six-loop commands, exact evidence, dependencies and boundaries. From the repository root:

```bash
python3 research/round15/reproduce.py --output /absolute/path/to/new-results
python3 research/round15/proof_routes.py --output /absolute/path/to/proof-results.json
```

The exact arithmetic uses the standard library. NumPy is needed for B1's floating matrix comparison; Matplotlib is needed only to regenerate the standalone scientific figures. The runner preserves accepted evidence and refuses to overwrite an existing output directory.

The six-face Euclidean coupling `k` is an action coefficient. It is not identified with the physical Hamiltonian energy ratio `lambda/alpha`. Full trial-state and generator assumptions are recorded on the spectral page.

## Reproduce the previous two-loop study

[Round14 instructions](research/round14/README.md) contain the complete model, commands for both simulations, exact certificate generation, independent verification and bidirectional proof replay. Run scientific commands in a terminal; the site displays recorded results. The earlier fixed-spacing Hamiltonian gap theorem remains available with its qualitative small-coupling threshold explicitly unevaluated.

## Install scientific dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell activation is `.venv\Scripts\Activate.ps1`; direct invocation with `.venv\Scripts\python.exe` also works. NumPy, SciPy and Matplotlib are used for numerical evolution, comparisons and plots. Exact certificates use Python rational arithmetic. Node.js 22 or newer is needed only for interface tests; no npm packages are required.

## Reproduce the one-square proof and experiments

Run from the repository root:

```bash
cd research/round10
python solver/test_solver.py
python solver/run_study.py
python proof_routes.py
python skeptic/audit_independent.py
python skeptic/audit_artifacts.py
python skeptic/audit_acceptance.py
python skeptic/audit_proof.py
python skeptic/coordinate_check.py
cd ../..
```

The stored study contains 16 stationary certificates, an exact continuous-range certificate, independent radial and Mathieu comparisons, and a smooth coupling ramp `lambda(t)=5[1-cos(pi*t/2)]`. Numerical evolution integrates external work separately and compares representation dimensions, tolerances and an independent unitary method. Stationary certificates do not certify the entire driven state.

Outputs are in `research/round10/solver/output/`. Scripts may rewrite output records. Preserve a clean checkout or copy before reproducing. Hash manifests deliberately reject modified mathematical sources or changed certificate bytes. Do not remove a hash or promote a missing test to an assumed premise to make a replay pass.

The repository's `.gitattributes` preserves exact file bytes across operating systems, including Windows checkouts. This prevents automatic line-ending conversion from invalidating the reviewed source hashes.

## Other experiments

### Reproduce the preserved round13 exceptions and hierarchy study

```bash
python research/round13/moments/test_moments.py
python research/round13/moments/run_study.py
python research/round13/locality/locality_checks.py
python research/round13/response/response_checks.py
python research/round13/proof_routes.py
python research/round13/test_proof_routes.py
```

The study contains 28 exact rational moment certificates, including negative, near-zero and zero couplings; a proved complete compact-hierarchy uniqueness result; a scalar response derived from the same normalized measure; and separate boundary-locality and static vacuum-stability arguments. **532 distinct independent scientific checks pass**, repeated under optimized Python without counting the repetitions twice. Read [the full round13 guide](research/round13/README.md), [independent review](research/round13/skeptic/REVIEW.md), [next experiment contracts](research/round13/next-experiments.md) and [source ledger](research/round13/advisor/sources.json).

The exact scalar identity is `kappa u' + 3u = kappa(1-u^2)`, with `u(0)=0` and `u'(0)=1/4`. Its derivative is variance with respect to a Euclidean coupling, not physical time. The round13 numerical trajectory comparisons are diagnostics; the rigorous initial series error is a separate bound. Twenty-four actual bidirectional routes retain 11 conditional successes and 13 rejection controls, including withheld smallness and blocked finite-to-continuum transfers.

### Reproduce the earlier dynamic and volume bridges

```bash
python research/round12/solver/test_solver.py
python research/round12/solver/run_study.py
python research/round12/solver/exact_stepper.py
python research/round12/volume/volume_checks.py
python research/round12/closure/closure_audit.py
python research/round12/proof_routes.py
```

The exact dynamic theorem gives `min(2, A^(D-d0+1)/(D-d0+1)!)`, where `A` is the integral of the absolute magnetic coefficients. A reduced cosine drive at degree 4 has exact representation bound 1/3840. Floating time evolution is still separately labeled numerical.

The distinct exact fixture uses two duration-one nonnegative coefficient pairs `(1/20,1/10)` and `(1/10,1/20)`, alpha=rho=1, degree 3, and the initial constant electric vacuum. Exact complex-rational Taylor polynomials of order 100 produce a stored 20-coefficient vector and exact Gram norm. Its representation error is 27/80000; the algorithm error is about 3.01×10⁻²³. The complete rational upper bound is strictly below 0.000337501. The computed vector is not renormalized.

The volume report proves an explicitly volume-dependent gap comparison and tests it against independent tensor copies whose exact gap stays fixed. The hierarchy report derives the missing variance term and audits named equations of a fixed primary-source version. [Round12 README](research/round12/README.md), [advisor proof](research/round12/advisor/advisor.md), [independent review](research/round12/skeptic/REVIEW.md), and [historical roadmap](research/round12/current_roadmap.json) give the precise assumptions and retained failures. Round13 adds a different, qualitative uniform-gap theorem in a restricted regime.

### Reproduce the coupled two-square extension

```bash
cd research/round11
python solver/test_solver.py
python solver/run_study.py
python proof_routes.py
python skeptic/audit_solver.py solver/two_plaquette.py --label local_replay
python skeptic/audit_dynamics.py solver
cd ../..
```

The coupled operator now includes the shared-link derivative and uses the correct three-coordinate Haar measure. Its complete free spectrum proves an exact omitted-polynomial threshold. The resulting full-space interacting certificate gives **Delta >=0.96 alpha throughout 0<=lambda_i/alpha<=2**, at shared-link weight rho=1. A separate analytic proof gives the positive bound `(243/625)*alpha*exp[-16*(lambda1+lambda2)/(3*alpha)]` for every finite nonnegative coupling pair on this fixed graph.

The advisor inventory contains 37 claims. The actual two-front planner replays 17 rules for the rectangle result and 13 for the analytic finite-coupling result; withholding required premises blocks the routes. See [the full round11 README](research/round11/README.md), [advisor proof](research/round11/advisor/advisor.md) and [independent review](research/round11/skeptic/REVIEW.md).

The historical dynamic degree 3→4 state difference is about 0.00409; energy-work consistency is substantially tighter. Round11 did not bound its dynamic representation error. Round12 now supplies a general analytic bound, but it is only the trivial 2 for that original strong drive at degree 3/4. Its useful weaker-drive and exact rational-fixture certificates are separate results; none establishes a continuum limit.

### Earlier benchmark commands

```bash
# Optional textbook checks: diffusion, oscillator and quantum well
python examples/reproduce.py --experiment all --output workbench-results/textbook

# Finite-lattice deterministic geometry/action checks
python research/round9/lattice/test_lattice.py

# All deterministic round9 benchmarks and selected independent audits
python research/round9/reproduce.py
```

For stochastic sampling commands, seeds, warmup, retained starts and failure thresholds, read `research/round9/lattice/README.md` and `PREDECLARED_CONTRACT.md`. Sampling is intentionally separate from deterministic replay. Do not rerun until a favorable statistical result appears. The retained beta=2.2 uncertainty failure remains part of the evidence.

Earlier QED rounds retain their own README and requirements files. Their models have different geometry, normalization and regulators; sharing notation does not identify their physical fields. The historical artifacts are preserved rather than silently rewritten to match the latest result.

## Verify the website and server

```bash
python -m unittest -v test_server.py
python -m unittest -v tests/test_local_launch.py
node dist/test_calculators.mjs
node tests/test_ui.mjs
node tests/test_research_plaquette.mjs
node tests/test_two_plaquette_ui.mjs
node tests/test_bridges_ui.mjs
node tests/test_exceptions_ui.mjs
node tests/test_workbench.mjs
python scripts/build_pages.py
```

Interface checks use a Node VM and a DOM stand-in. They test routes, events, escaped documents, certificate selection and data bindings; they do not constitute a real-browser layout or keyboard audit. The server tests mock upstream metadata responses and failures.

## Build and publish GitHub Pages

`dist/` is the local site source; `docs/` is the generated GitHub Pages tree. The build rewrites only known local asset URLs for the project prefix, preserves external source links, omits server code and marks live metadata refresh as local-only.

```bash
python research/round14/build_site_data.py
python research/round14/package_review.py
node tests/test_team_ui.mjs
python research/round14/package_review.py
python scripts/build_pages.py
node tests/test_workbench.mjs
git add dist docs research guides scripts tests README.md .codex/skills
git commit -m "Update research and Pages site"
git push origin main
```

GitHub Pages is configured to deploy from branch **main**, folder **/docs**, with `.nojekyll`. The published address is [https://occult-kranti.github.io/yang_mills_workbench/](https://occult-kranti.github.io/yang_mills_workbench/). Check repository Settings → Pages and the Pages deployment status after pushing. If publishing a fork, pass its project prefix to `python scripts/build_pages.py --base /your_repository/` and update these links.

For a local preview of exactly the static Pages behavior, run `python scripts/preview_pages.py`. Open `http://127.0.0.1:8002/yang_mills_workbench/`. This preserves the real project prefix, so recorded downloads work. The normal `start.py` launch additionally provides the optional metadata endpoint.

Official setup and permission details: [GitHub Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [Pages REST API](https://docs.github.com/en/rest/pages/pages).

## Research protocol and complete-problem roadmap

1. Define graph, gauge group, Gauss constraints, Hilbert measure, operator domain, coefficients, state and observable.
2. Derive forward from those premises; search backward from the proposed theorem for its missing obligations.
3. Independently check the meeting equations. A bidirectional search locates a derivation through admitted rules; it cannot prove those rules by choosing a route.
4. Separate exact arithmetic and analytic inequalities from numerical trends. Preserve failed controls, stale manifests and inconclusive lower bounds.
5. Add one controlled coupling or geometry extension, derive its energy and constraint terms, then repeat the skeptic review.
6. For the prize target, prove bounds uniform in spatial volume and along a matched continuum trajectory, construct a nontrivial continuum theory and establish its required axioms and positive physical mass gap.

The last step is unresolved. Finite-graph compactness, a positive matrix gap, a fitted exponential, or a coordinate change cannot supply the required uniform limits. The advisor and validator instructions are versioned under `.codex/skills/`; their reviews are agent reviews, not credentialed human peer review or formal proof-kernel verification.

## Project layout and provenance

| Path | Purpose |
|---|---|
| `start.py` | Loopback website and optional arXiv endpoint |
| `dist/`, `docs/` | Local source assets and generated public Pages assets |
| `research/round8`–`round12` | Yang–Mills/spectral studies, scripts, certificates, plots and reviews |
| `evidence/qeg-research/` | Earlier QED/gravity reproducibility evidence |
| `scripts/`, `tests/` | Pages build and interface/transport checks |
| `examples/` | Independent textbook numerical exercises |
| `guides/`, `provenance/` | Full Observatory guide, import record and historical hosting reference |
| `.codex/skills/` | Reusable advisor and numerical-validation protocols |

The import record names the exact Physics Observatory source commit. Host-specific connection metadata and compiled Worker output are excluded from this independent GitHub repository. Mathematical source/data files, original failed implementations and their hash records remain traceable. No private browser notes or credentials are included.

Third-party sources retain their original terms; see `THIRD_PARTY.md` and source ledgers. Linked books and papers are not a claim of unrestricted redistribution rights. The official problem statement and status are available from the [Clay Mathematics Institute](https://www.claymath.org/millennium/yang-mills-the-maths-gap/).
