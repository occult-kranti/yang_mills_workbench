# Round16: the shared-face subproblem

[Open the research home](https://occult-kranti.github.io/yang_mills_workbench/#research) · [Source repository](https://github.com/occult-kranti/yang_mills_workbench)

This round uses two sequential research loops and three scientific roles: advisor–skeptic, forward researcher and backward researcher. It extends the single-cube calculation to the actual eleven-face complex of two adjacent cubes. The shared plaquette occurs exactly once. The ten-face outer boundary is a different action, even though it has the same link graph.

The exact Haar identities are:

- Either six-face cube product:1/1024.
- Outer ten-face product:1/262144.
- All eleven fundamental traces:0.
- Outer ten-face product times the shared trace squared:1/524288.

The independent shared-link calculation contracts256 fourth-Haar projector branches. A separate exhaustive graph check covers all2,048 distinct-face subsets. These calculations apply known SU(2) representation theory to a finite complex; no mathematical novelty or continuum solution is claimed.

Loop2 compares the SAME all-eleven observable under outer coefficients1/8, with shared coefficient1/8 versus0. The difference is approximately2.430327491597616e−7. The exact degree24 certificate has a total difference width about4.173e−22, including both numerator and normalization errors. The requested width is1e−12; degrees0,6,12 remain insufficient and18,24 pass. Exact fractions in `forward/loop2/output/collection.json` are authoritative. Rounded decimals and plotted lines are display aids.

The omitted-action observable is not zero. Its near-zero expansion begins41t^5/(81*2^18). The second-loop target therefore compares two fully bounded expectations instead of presuming a zero baseline.

## Launch the current website

From the repository root:

```bash
python3 start.py --no-browser
```

Visit `http://127.0.0.1:8001/#research`. Windows: `py -3 start.py`. The static website needs no API key or Python packages. GitHub Pages displays recorded research; Python programs execute locally. Choose another port with `--port 8002` if needed. Notes and progress stay in the browser.

## Reproduce the two loops

Python3.11+ is required. Exact arithmetic uses the standard library. The Loop1 floating matrix/quaternion diagnostics need NumPy; figure generation needs Matplotlib. From the repository root, an optional isolated environment is:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install numpy matplotlib
```

Run the recorded five-program sequence without overwriting accepted data:

```bash
python3 research/round16/reproduce.py --output /absolute/path/to/new-results
python3 research/round16/reproduce.py --optimized --output /absolute/path/to/another-new-results
```

The output folders must be new and outside `research/round16`. The runner checks source-bound gates, executes both producer programs, both independent verifiers and the scale audit, then compares semantic results and accepted bytes. Normal and optimized runs are the same gate set, counted once. Exact results should be portable; last-bit floating diagnostic differences on a different NumPy/platform must be classified separately from rational certificate failures.

Replay the actual finite bidirectional dependency search:

```bash
python3 research/round16/proof_routes.py --output /absolute/path/to/proof-results.json
```

This command freezes the reviewed source inventory, reconstructs scientific evidence in fresh processes, performs forward/backward search and separately replays the ordered rule certificate. Withdrawal tests remove required graph, projector, coefficient, tail, target and scale gates. Unproved local constants, time-generator and continuum premises cannot be initial facts. This is an auditable conventional proof planner, not a formal proof-assistant kernel.

## Files and review scope

`advisor/contract.md` contains the initial subproblem breakdown. `advisor/loop2-contract.md` fixes the second-loop target selected after the first gate. `advisor/feedback-log.md` preserves decisions and corrections. Each `advisor/loop*-gate.json` binds the complete accepted phase files. `forward/` contains derivations and code; `backward/` contains independent exact methods and adversarial checks. `proof_results.json` contains real search results, including failed routes. `next-roadmap.md` preserves the original physical target.

The cache-alias defect is retained under the first-loop history. It allowed a caller to modify cached character coefficients and change a later integral; defensive copies and strict public input types repair it. Wrong Haar projector, coefficient normalization, insertion, action and incomplete-evidence controls are documented. Review scope covers the new scientific files and affected integration paths; it is not a claim that every line of all historical rounds received a new audit.

## Physical energy scale remains separate

For the same self-adjoint domain, H_N=α_N K_N implies Δ(H_N)=α_N Δ(K_N), α_N>0. A common dimensionless lower bound and a common positive energy prefactor yield a common physical lower bound. The free-box example for n>=2, Δ(K_n)=3, α_n=1/n gives physical gaps3/n→0, despite zero coupling ratio at every volume.

This scale condition concerns the proposed inference from a common dimensionless LOWER bound; it is not universally necessary for arbitrary growing spectra. The static Euclidean κ_f is not identified with Hamiltonian λ_f/α. No matched state/time-generator theorem is supplied by the finite integral.

The numerical volume-uniform interacting threshold remains open. It still needs explicit local operator constants and a matched common physical family. The four-dimensional pure Yang–Mills continuum construction, reconstruction axioms and mass gap remain unresolved.

## Rebuild and inspect the research site

From the repository root, after scientific gates are accepted:

```bash
python3 research/round16/build_site_data.py
python3 research/round16/plot_figures.py
python3 research/round16/package_review.py
python3 scripts/build_pages.py
node tests/test_shared_ui.mjs
node tests/test_workbench.mjs
python3 tests/test_local_launch.py
```

The plot data are exact saved endpoints converted only for display. Every chart provides a CSV; standalone PNG/SVG figures and exact certificates are archived. The site includes historical routes and the local simulation tools. Node VM and HTTP checks cover code behavior, downloads and data binding. Real-browser visual layout and keyboard interaction remain unverified.

Primary sources and actual reading depth are recorded in `advisor/source-audit.md` and `advisor/sources.json`. The finite graph derivations and direct convention checks are part of the project evidence, not copied claims of a solved Millennium problem.
