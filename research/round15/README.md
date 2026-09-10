# Round15: three revised goals, two loops each

Live workbench: [research home](https://occult-kranti.github.io/yang_mills_workbench/#research). Repository: [yang_mills_workbench](https://github.com/occult-kranti/yang_mills_workbench).

The advisor–skeptic first reviewed the next three roadmap goals with the same forward and backward researchers. Each goal then received two sequential evidence loops. Each second loop was selected after its first-loop gate. The research record separates completed execution, supported finite-model results and unresolved original targets. This is not a solution of the four-dimensional Yang–Mills Millennium problem.

## Roles, files and acceptance

`advisor/revised-plan.md` records the initial corrections. `advisor/loop-gates/` binds the accepted source and output bytes for A1,A2,B1,B2,C1,C2. `forward/` contains producer derivations and calculations. `backward/` contains independent constructions and rejection tests. `advisor/feedback-log.md` explains the first-to-second decisions; `next-roadmap.md` gives the next bounded contracts. Historical rounds remain preserved in the full repository.

Do not equate the number of passing checks with independent physical premises. Ordinary and optimized runs execute the same checks and are counted once. The planner organizes reviewed conventional mathematics; it is not a proof-assistant kernel.

## Launch the website

From the repository root:

```bash
python3 start.py --no-browser
```

Open `http://127.0.0.1:8001/#research`. On Windows use `py -3 start.py`. Python3.11+ suffices for the static server. No API key, cloud account, package installation or JavaScript build is required. Progress and notes remain in the browser. GitHub Pages displays recorded experiments; Python research programs run in a terminal.

## Reproduce exact science

The round15 exact arithmetic uses the Python standard library; the B1 floating matrix/quaternion comparison additionally needs NumPy. Scientific figure generation uses Matplotlib. Install optional plotting/diagnostic dependencies in a virtual environment if they are absent:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install numpy matplotlib
```

Run the reproduction runner from this directory:

```bash
python3 reproduce.py --output /absolute/path/to/new-results
```

The output directory must be outside the recorded round15 tree and must not already exist. The runner preserves a frozen input snapshot, invokes the actual programs, checks semantic outcomes and records commands and return codes. It does not overwrite accepted evidence. Use `--optimized` to rerun the same gate set under `python -O`. The supplied exact fractions are authoritative; decimal displays and plots are rounded. The strict reproduction runner compares accepted byte identities. Floating B1 diagnostic reports can vary across numerical platforms; `runtime.json` records the tested versions. Such a difference must be distinguished from failure of an exact rational certificate.

To replay the actual bidirectional dependency routes:

```bash
python3 proof_routes.py --output /absolute/path/to/proof-results.json
```

The replay validates the full expected source inventory and independently recomputes admitted finite evidence. Missing coverage, graph/tail, variational or uniform-continuum premises block the corresponding route. A forged serialized pass is not accepted as authority.

## Interpret the goals

A uses the fixed finite deformed measure `exp(x+y+eta*z)dU dV/Z`, with `k1=k2=1`. Exact point error and the proved derivative bound2 cover the entire requested interval. Neither Taylor degree nor cell radius is physical time.

B uses the actual cube boundary with12 oriented SU(2) links and6 normalized Wilson traces. Its coupling `k` is a dimensionless Euclidean action coefficient. The all-six character contraction differs from a product of independent face integrals. The finite Taylor certificate includes both normalization and numerator error.

C uses the physical gauge-invariant Hamiltonian `H=alpha*sum_e C_e-sum_p lambda_p*x_p`, with its irrelevant constant magnetic offset removed. `alpha` and `lambda_p` have energy units; `lambda_p/alpha` is a physical dimensionless ratio. These coefficients are not identified with B's Euclidean `k`. The original explicit volume-uniform threshold remains open unless its source-specific/local proof is completed. A finite variational matrix provides an upper bound on ground energy; it needs a separate lower bound on the full second eigenvalue to certify a gap.

## Rebuild the site and check integration

After scientific acceptance and source binding, from the repository root:

```bash
python3 research/round15/build_site_data.py
python3 research/round15/package_review.py
python3 scripts/build_pages.py
node tests/test_cycles_ui.mjs
node tests/test_workbench.mjs
python3 tests/test_local_launch.py
```

Recorded figures and downloadable CSVs use the same data. The actual-script tests exercise routes, documents, malformed data, escaping and evidence bindings. Loopback HTTP tests cover the localhost and GitHub-project-prefix launch modes. They do not establish real-browser visual layout or keyboard accessibility; those remain unverified.

The package preserves the coarse failures and the scope boundaries. Nothing in the static site starts an unattended research swarm or guarantees that an open mathematical problem will be solved.
