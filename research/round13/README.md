# Exceptions, compact moments and a restricted uniform gap

This round asks which apparent workarounds preserve a mathematical problem and which change it. It adds four compatible, carefully separated results: local finite-time dynamics on growing lattices, exact moment bounds for one compact Euclidean measure, an exact scalar coupling response, and an application of a known vacuum-stability theorem giving a qualitative volume-uniform Hamiltonian gap at fixed spacing and sufficiently small magnetic/electric ratio. **The four-dimensional continuum Yang–Mills existence and mass-gap problem remains open.**

[Open the current research home](https://occult-kranti.github.io/yang_mills_workbench/#research). The site preserves the earlier finite-graph certificates and Einstein–QED evidence, while giving each new result its own page. Results here are conventional mathematical arguments, exact arithmetic certificates, numerical diagnostics and independent agent critiques. They are not a formal proof-assistant verification or credentialed human peer review. Known one-plaquette identities and the cited stability theorem are not claimed as new mathematics.

## What was established

| Result | Precise scope | Evidence and limitation |
|---|---|---|
| Qualitative uniform Hamiltonian gap | Static bounded plaquette perturbation of the electric product vacuum, sufficiently small magnetic/electric ratio, fixed lattice spacing | Application of Yarotsky's theorem with infinite-dimensional link blocking, boundary padding and Gauss restriction. Gap at least `3 alpha / 8`; the admissible threshold is existential and has not been evaluated numerically. |
| Boundary locality | Bounded local observable; common electric terms and plaquette coefficients; locally integrable uniform absolute envelope; fixed spacing and finite time | Explicit factorial tail independent of total graph size. This constructs a local volume limit of dynamics, not by itself a vacuum or a mass gap. |
| Finite compact moment intervals | Normalized exponential tilt of the SU(2) Haar trace distribution | 28 exact rational certificates at specified parameters and levels; witnesses, feasible inner points and optimization slack are independently replayed. |
| Full compact hierarchy uniqueness | One normalized moment sequence, every recurrence and every support-positivity condition, one fixed finite real coupling | Distribution equation and endpoint-atom argument identify the unique measure. Nested full feasible intervals converge; no convergence rate is proved. Successful algorithmic orders must tend to infinity and their certified slack to zero. |
| Exact scalar coupling response | The same compact Euclidean measure | `u' = Var(x)` and `kappa u' + 3u = kappa(1-u^2)`. Regularity fixes the zero-coupling branch. It is not a physical-time equation. |

The uniform gap result is stronger than the previously deteriorating global comparison bound. It is a **known-theorem application in a restricted phase**, not a continuum solution. Read [the source](https://arxiv.org/abs/math-ph/0411042) and `advisor/weak-coupling-stability.md` for the exact hypotheses, boundary distinctions and theorem-specific reading depth.

## The new variables and equations

Keep the Euclidean tilt `kappa_E`, the Hamiltonian ratio `kappa_H=lambda/alpha`, and physical time distinct. Reusing a symbol cannot match their states or observables.

For a single trace `x` in `[-1,1]`,

\[
d\mu_\kappa=Z_\kappa^{-1}e^{\kappa x}\frac{2}{\pi}\sqrt{1-x^2}\,dx,
\quad m_n=\mathbb E[x^n],\quad u=m_1,\quad v=m_2-u^2.
\]

Integration by parts gives

\[
n m_{n-1}-(n+3)m_{n+1}+\kappa(m_n-m_{n+2})=0.
\]

The `n=0` term with negative index is absent. Differentiating this same normalized exponential family gives `u'=v>0`, so

\[
\kappa u'+3u=\kappa(1-u^2),\qquad u(0)=0,\quad u'(0)=1/4.
\]

Variance is an existing observable with a derived equation. It was not fitted to force closure. A scalar equation is legitimate here because its coupling derivatives retain the hierarchy. Changing `3u` to `2u` instead gives the analogous equation for a uniform prior: a useful controlled counterexample that changes the measure. An irregular Bessel branch introduces a singular mean near zero and fails the compact-observable range.

At finite hierarchy level `r`, rational positivity of

\[
H_r=(m_{i+j})_{i,j=0}^{r},\qquad
L_{r-1}=(m_{i+j}-m_{i+j+2})_{i,j=0}^{r-1}
\]

gives bounds without discarding fluctuations. At `kappa=1,r=6`, the certified mean lies approximately in `[0.24019372387000923, 0.24019372387014987]`, width `1.4063056031141083e-13`. The exact rational values in the certificate are authoritative; rounded decimal endpoints are displays. At `kappa=5,r=6`, the width is about `6.04e-8`: accuracy is parameter dependent. At zero coupling, the exact mean is zero and variance is `1/4`. Finite feasibility alone does not identify the full measure.

For a local bounded observable `A`, support `X`, incidence `q=2(d_s-1)`, absolute integrated envelope `J`, and actual plaquette-chain boundary distance `R`,

\[
\|\tau_{\Lambda'}(A)-\tau_\Lambda(A)\|
\le \|A\|\min\left\{2,\frac{|X|}{4}
\sum_{k\ge R}\frac{(8qJ)^k}{k!}\right\}.
\]

The bound uses a unitary interaction picture and a commutator recursion, not a naive count of all Dyson histories. The recorded `d_s=3, |X|=4, ||A||=1, J=1/4, R=48` example has an upper bound about `2.14535e-18`. **That is a bound calculation, not an observed simulation error.** It controls fixed-spacing finite-time dynamics, with no total-volume prefactor. Changing onsite terms or removing the common-envelope assumption invalidates the comparison.

For the separate static stability application, block outgoing link spaces at each site. The free block gap is `delta0=3 alpha/4`, and the dimensionless perturbation is bounded by

\[
\epsilon\le\frac{4}{3}{d_s\choose2}\frac{\lambda_{\max}}{\alpha}.
\]

Yarotsky's existential constants `c1(S),c2(S)>0` yield

\[
\kappa_* = \frac{3}{4{d_s\choose2}}
\min\{c_1(S),[2c_2(S)]^{-1}\}>0,
\quad \lambda_{\max}/\alpha<\kappa_*
\implies \Delta\ge3\alpha/8.
\]

The proof accounts for the source theorem's grouped empty boundary through a free halo and coefficient mask. Unique ground states are gauge invariant because finite products of SU(2) have no nontrivial continuous one-dimensional characters; restriction to the Gauss sector preserves the lower bound. The canonical infinite-volume construction and the finite-box padding argument have distinct boundary claims.

With the declared Hamiltonian normalization,

\[
\alpha=\frac{g_H^2}{2a},\quad \lambda=\frac{2}{g_H^2a},
\quad \kappa_H=\frac4{g_H^4}.
\]

The usual weak-bare-coupling continuum trajectory exits every fixed small-`kappa_H` regime. No chosen positive numerical coupling can be certified merely by naming an existential `kappa_*`.

## Reproduce from the repository root

Python 3.11+ is recommended. Install the root `requirements.txt` for the numerical comparisons and plotting. The website itself needs no scientific packages or credentials.

```bash
python3 start.py --no-browser
# Open http://127.0.0.1:8001/#research

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python research/round13/moments/test_moments.py
python research/round13/moments/run_study.py
python research/round13/locality/locality_checks.py
python research/round13/response/response_checks.py
python research/round13/proof_routes.py
python research/round13/test_proof_routes.py
```

On Windows use `py -3`, and `.venv\Scripts\activate` for the virtual environment. See the branch READMEs for exact output arguments and independent reviewer commands. Run regenerating experiments in a separate checkout or copy. Scientific manifests deliberately reject changed sources, missing evidence and stale outputs; changing a manifest is a reviewed packaging action, not a way to bypass a failed check.

`proof_results.json` retains the actual forward/backward meetings and separate certificate replay for 24 routes: 11 positive conditional routes and 13 rejection controls. The unchanged historical ground-Horn search core explores the complete backward dependency cone of each target. This preserves every rule capable of deriving that target while keeping traces compact. It does not turn a reviewed implication into a formal mathematical proof. Withholding smallness blocks the stability route; finite constraints cannot supply all-order hypotheses; the four-dimensional target remains unreachable.

For a portable archive, run the same commands relative to its `moments/`, `locality/` and `response/` directories. The archive carries a dependency list and all scientific source files, documents and original failures. It does not contain the entire historical website; clone the repository to launch every earlier tool.

## Audit findings that changed the implementation

1. A positive-definite exact congruence calculation fell through to a branch using an unbound witness variable. The missing terminal return is fixed; the reconstructed first draft and original failure are explicitly labelled.
2. The locality input accepted generators but consumed them twice. An exhausted iterator could erase the graph and report zero boundary influence. Inputs are now frozen once, and generator/list equivalence is tested.
3. A response-grid conversion could turn Boolean input into a numerical coupling. It now rejects Boolean grid values before conversion; the failure is retained.
4. The rule graph needed explicit normalization, a fixed finite coupling, common locality coefficients, exhaustive nested volumes and successful hierarchy orders tending to infinity. Those hypotheses now remain visible in both search directions.
5. Existential stability constants must not be converted into numerical acceptance. The retained smallness-withdrawal control makes this distinction executable.
6. The proof adapter could accept changed rule premises after an earlier successful replay. All 19 frozen input fingerprints and the scientific ledger are now rechecked at library construction. The saved standard-execution routes did not mutate their inputs and retain their outcomes. The repaired adapter passes 131 producer gates and 69 independently authored adapter gates, separately from the 532 scientific gates.

Every review records its source hashes. Producer tests and independently implemented tests are separate counts; normal and optimized runs repeat the same gates and are not added together. Sampled numerical agreement, exact arithmetic replay and conventional theorem review remain separate forms of evidence. Real-browser visual and keyboard review is not asserted by the Node VM or HTTP checks.

## Read the full documents

- `advisor/advisor.md`, `case_matrix.json`, `theorem_inventory.json`, `inference_rules.json`: 16 cases, 46 nodes and 21 reviewed implications, with assumptions and rejection conditions.
- `advisor/weak-coupling-stability.md`: known-theorem application, boundary padding, Gauss restriction, constants and continuum obstruction.
- `moments/README.md`: complete rational certification algorithm and domain, exact zero branch, variance images and optimization slack.
- `locality/locality.md`: complete local estimate, actual graph geometry and continuity scope.
- `response/response.md`: scalar equation, origin uniqueness, launch-error proof and numerical diagnostics.
- `skeptic/`: independent formulations, exact reference intervals, counterexamples, code mutations and source-bound acceptance.
- `proof-replay.md`: admission policy, full dependency search and negative route controls.
- `skeptic/proof_adapter_review.md`: independent exhaustive minimum-cost comparison, admission flaw and verified repair. Original adapter and test records remain in `history/`.
- `current_roadmap.json`, `next-experiments.md`: reconciled status and bounded next tasks. The advisor's original handoff is retained separately.

The primary-source ledger states reading depth and limitations. Its coverage is targeted, not exhaustive. All possible proof strategies cannot be enumerated or exhausted by a finite research run.

## Build the published snapshot

After an independent acceptance ledger matches the scientific files:

```bash
python research/round13/build_site_data.py
python research/round13/package_review.py
node tests/test_exceptions_ui.mjs
python research/round13/package_review.py
python scripts/build_pages.py
node tests/test_workbench.mjs
python tests/test_local_launch.py
```

The Pages snapshot is static. Charts show saved data and offer CSV downloads; simulations run locally in Python. The final archive inventory binds every packaged byte, and the Pages build manifest binds every deployed asset.
