# Round32: expert-panel adaptive cycle, five sub-rounds, ten investigations

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted research with an expert panel (Newton/Tesla, Jung/Pauli and Penrose/Feynman as documented methodological lenses), an advisor and an independent skeptic, all model agents with shared ancestry. This is not external human peer review; scientific priority is unverified; no historical figure participated or endorsed the work; no occult, mystical or governmental source became a premise.

The cycle starts from merged Round31 commit `1a686cdf9808aca9b5811dbf23e78bd2be1201f9`. Three deliberation loops fixed the plan (`advisor/deliberation-1.md`, `-2.md`, `-3.md`, `advisor/plan.json`); five sub-rounds of two investigations follow, each with a prospectively frozen contract, paired or single-direction production, a pre-comparison skeptic package, byte-identical replays, a post-comparison review and an advisor gate. After each sub-round one research assistant per lens runs tests and the panel may change goals (`advisor/panel-update-<n>.md`). All earlier scientific records, Draft03 and the Round31 addendum retain their bytes.

| Sub-round | Loop | Result | Limitation |
|---|---|---|---|
| 1 | AV1 | Volume-uniform local state bound linear in tau; exact tier about 1.36e-8 at the cap | Zero-selected patterned family and cover R only; closeness, not uniqueness |
| 1 | AV2 | Window-kernel certificate of the centered Wilson node at tau=10^-8, s=1: radius about 1.83e-7 (<10^-6) | Free reference inside (reference_unresolved); only s=1 |
| 2 | AW1 | Parity theorem, link-flip antisymmetry, first-order Wilson mean +tau/144, exact-tier second-order constant about 3354.8; AW2 coupling fixed at the cap | Static equal-time effect; finite-box parity; no third-order remainder |
| 2 | AW2 | Sign-certified Wilson mean at the cap: about [6.91e-11, 6.98e-11], zero excluded, exclusion margin about 206 | Static equal-time effect; not dynamical; centered shift unresolved |
| 3 | AX1 | Uniform Kogut-Susskind SU(2) at fixed spacing (route B): re-frozen contraction constant, itemized incidence, 52 faces per factor, exact-tier state bound about 1.44e-8; flip antisymmetry and +tau/144 transferred | Strong bare coupling g^4=9.6e9; never weak coupling or continuum |
| 3 | AX2 | Uniform-model Euclidean node at the cap: radius about 1.91e-7 (<10^-6), free reference inside | reference_unresolved; strong bare coupling; only s=1 |
| 4 | AY1 | Uniform local closeness of every pair of subsequential limits of two named construction families: 2D about 2.72e-8 on the cover R in trace norm; common first-order density rho^(1)_R (10 faces, trace norm sqrt(10)|tau|/72, mean +tau/144); second-order difference 2K_2' tau^2 about 2.7e-12 with R-local K_2' about 13418 (four times K_2^+) | Closeness, never uniqueness, whole-sequence convergence, translation invariance, a rate in N or dynamics; uniform_local_closeness_not_uniqueness |
| 4 | AY2 | Statement with the AY1 constants: six unproved obligations with missing premises and routes; explicit second-order falsifying scenario; certified static two-sided distance of every limit from the Haar product on R, about 4.3786e-10 to 4.4055e-10 (first_order_distance_from_product) | Static, not dynamical; excludes the product as any limit's marginal without identifying the limit; uniform_local_closeness_not_uniqueness, static_not_dynamic |
| 5 | AZ1 | Continuum-trajectory statement: dictionary identities exact (incl. alpha*lambda*a^2=1); the one uniform estimate supplied is the volume-uniform gap g^2/(32a) at fixed a for g^4>=9.6e9; nothing uniform along any trajectory with g->0; toy crossovers n*=2/132 (g_0^4=9.6e9) and 4/421 (g_0=1000); lattice-unit floor a*Delta>=g^2/32 | Strong bare coupling at fixed spacing only; no continuum, weak-coupling or uniform-in-a statement; no number is a fraction of the continuum problem |
| 5 | AZ2 | Exact finite-graph Wilson coefficients on the Round11 two-plaquette graph with both faces coupled (D=6, 8): derivative exactly 1/6 (consistent with 1/144 under tau_FG=tau/24, consistency only), second-order coefficient exactly 0, <W_1> enclosed at six grid points with certified five-part residual ledgers (half-widths down to 2.8e-39) | A different finite model; sign_certified_finite_graph, static_not_dynamic; never a transfer to any subsequential limit of the AQ construction, K_2 or the continuum |

The authoritative reviewed statements are in `advisor/findings.json` and the per-loop gates; `advisor/admission-spec.json` fixes the trusted reviewed semantics and required check ids. A `limited` or `insufficient` verdict is a retained outcome. Loop counts are not a fraction of the four-dimensional Yang–Mills problem, which remains open.

## Evidence and tools

- `contracts/`: frozen before production with a pre-registration block; `advisor/`: selection notes, gates, findings, plan, panel record, roadmap.
- `forward/`, `reverse/`: disjoint producer closures (`report.md`, `check.py`, `output/`, `inputs/` snapshots, `freeze.json`); the reverse producer's premises are isolated by contract.
- `skeptic/`: prospective triage and control catalogue, pre-comparison independent derivations and checkers, post-comparison reviews, replay receipts, the Gauvin version diff record.
- `experts/`: lens memos, source ledgers with reading depth and access failures, loop responses, per-sub-round updates and assistant test packages; `experts/occult/reading-ledger.md`.
- `methods/`: frozen skill snapshots including the Round32 rules; `tools/`: freeze/gate/contract helpers and the Arb/mpmath cross-check; `figures/`: deterministic presentation figures (no admission weight).

```sh
python3 -B research/round32/reproduce.py --validate-only
python3 -B research/round32/reproduce.py --complete --output /absolute/new/normal
python3 -B -O research/round32/reproduce.py --complete --optimized --output /absolute/new/optimized
python3 -B research/round32/test_admission.py
python3 -B research/round32/tools/freeze.py verify research/round32/forward/av1
node tests/round32_site.mjs --require-release
```

Hashes and exact fixtures establish provenance and executed checks, not mathematical truth by themselves. The written reports and the separate skeptical reviews remain necessary.
