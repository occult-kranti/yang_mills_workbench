# Driven-error, volume and closure study

This research round continues the existing two-plaquette Yang–Mills workbench. It adds a rigorous dynamic representation-error theorem, an exact-rational computed-state fixture, an explicit growing-graph bound and counterbenchmark, and a primary-source/compact-hierarchy critique. It does not solve four-dimensional continuum Yang–Mills theory.

## Read the results

- `advisor/advisor.md`: full proof, initial-state and domain assumptions, common action/time variables, independent objections and roadmap.
- `solver/`: rational action certificates, four smooth-drive comparisons, and an exact polynomial evolution certificate for a separate two-step drive.
- `volume/volume-bridge.md`: graph-volume dependence, tensor counterbenchmark, Gibbs/Hamiltonian distinction, current rigorous literature and continuum obligations.
- `closure/closure-audit.md`: exact compact identities, variance, a failed defined closure, and version-specific article formula tests.
- `skeptic/`: independently implemented checks, original failures, mutations and final source-bound acceptance.
- `proof_results.json.gz`: losslessly compressed actual two-front search and separate arithmetic replay. Reviewed Horn implications are not a formal proof kernel.

The public site is [Yang–Mills Workbench](https://occult-kranti.github.io/yang_mills_workbench/#research). From the repository root, `python3 start.py` launches the same research and existing tools at `http://127.0.0.1:8001/#research`.

## Reproduce from the repository root

Install the root `requirements.txt` first. Python 3.11+ is supported; the exact computations use rational arithmetic, with NumPy/SciPy imported by the retained common model module. Exact rational coefficients do not mean the whole project uses no external dependencies.

```bash
# Exact drive-action bounds, protocol edge cases and independent-method diagnostics
python research/round12/solver/test_solver.py
python research/round12/solver/run_study.py

# Separate exact-rational two-step computed state
python research/round12/solver/exact_stepper.py

# Volume and compact hierarchy checks
python research/round12/volume/volume_checks.py
python research/round12/closure/closure_audit.py

# Frozen-source arithmetic replay and actual bidirectional search
python research/round12/proof_routes.py
```

Read `skeptic/README.md` for independent audit commands and isolated mutation testing. Use a separate checkout or copy when rerunning scripts that rewrite evidence. A source or certificate change deliberately invalidates the published hash manifest; do not delete missing hashes or accept unknown premises to force a pass.

## Exact dynamic result

For the unchanged finite spatial graph, the physical Hilbert space still has an infinite representation tower. If the initial normalized state lies in polynomial degree at most `d0`, the electric operator preserves the degree flag, and trace multiplication crosses at most one degree shell, then

\[
\|\psi(T)-\psi_D(T)\|\le
\min\left(2,\frac{A(T)^{D-d_0+1}}{(D-d_0+1)!}\right),
\qquad A(T)=\int_0^T(|\lambda_1|+|\lambda_2|)\,dt.
\]

This bound compares exact full and exact Galerkin states in normalized-product-Haar L². It follows from unitary high-degree block evolution and one-sided Duhamel forcing. For the reduced cosine ramp with duration 2, scales 1/10 and 3/20, vacuum start and degree 4, the endpoint bound is exactly **1/3840**. Its floating numerical trajectory still has uncertified time-integration and coefficient-rounding error. The original stronger ramp has action 5 and only the trivial bound 2 at degree 3/4.

For the separate exact fixture, use two duration-one segments `(lambda1,lambda2)=(1/20,1/10)` and `(1/10,1/20)`, with alpha=rho=1, initial constant electric vacuum and degree 3. Each finite Hamiltonian is applied with a degree 100 Taylor polynomial using exact complex rational coordinates. The physical operator norm is bounded by 114/5. Set

\[
e=\frac{(114/5)^{101}}{101!}.
\]

The stored unnormalized rational vector has a total full-space state-error bound

\[
\frac{27}{80000}+2e+e^2.
\]

Exact rational arithmetic removes floating coefficient and stepping roundoff for this specific algorithm. The Taylor remainder still needs its explicit bound. The vector is not renormalized. The state is initially the electric vacuum, not the interacting ground state of a nonzero magnetic Hamiltonian. The result controls this finite graph and specified endpoint, not infinite time, volume or continuum limits. A state-norm bound controls bounded observables; it does not alone bound unbounded electric energy.

## Research interpretation

The volume theorem is positive on each admitted open graph but explicitly worsens with link count and total coupling. Independent tensor copies retain their exact one-copy gap while the global comparison estimate vanishes. This rejects an inference about the estimate, not a theorem about the actual connected-volume gap.

The compact closure benchmark introduces variance as an existing observable. At finite coupling it has an analytic positive lower bound, so the defined point-concentration closure fails. A variance definition does not supply the rest of its moment hierarchy. The article critique names a fixed version and specific formulas; it is not a general dismissal of scalar ansätze or Haar integration by parts.

All sources state reading depth and limitations. Reviews are agent reviews of conventional arguments, not credentialed peer review. The remaining current experiments are listed with explicit acceptance conditions; no route proves the four-dimensional target from the present premises.

## Large traces and website rebuild

The full planner trace is about 143 MB before compression. Git stores its byte-identical gzip form, with original and compressed SHA-256 values in `trace-archives.json`. The site dialog retains proof certificates, assumptions and route outcomes; the complete search states and frontiers are a separate gzip download. The portable ZIP includes these compressed traces and their inventory. Replaying `proof_routes.py` recreates the raw JSON; it is ignored by Git.

After regenerating research outputs, rebuild from the repository root:

```bash
python research/round12/trace_archive.py
python research/round12/build_site_data.py
python research/round12/package_review.py
node tests/test_bridges_ui.mjs
python research/round12/package_review.py
python scripts/build_pages.py
node tests/test_workbench.mjs
```

`trace_archive.py` verifies original bytes against their compressed counterparts. A copied or altered trace must not be silently substituted for a reviewed run. Original failure records remain separate from the current acceptance.

The retained producer PNG/SVG applies a 10^-16 display floor to two very early numerical-difference points. The website uses the positive raw CSV values without that floor and omits exact zeros on logarithmic axes. Read the CSV for the numerical values; a floored pixel is not an accuracy certificate.

`skeptic/packaging_review.json` records a separate 33-gate independent archive review. Its historical bundle hash precedes addition of the review itself; the delivered ZIP includes an inventory verifying every final member. Scientific acceptance remains independently bound to the mathematical source files.
