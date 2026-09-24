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
| 4 | AY1 | accepted_within_scope (uniform_local_closeness_not_uniqueness) | 2D ≈ 2.72e-8 for any two subsequential limits of both families on R; common rho^(1)_R; R-local K_2' ≈ 13418 (about 4 × K_2^+) |
| 4 | AY2 | accepted_within_scope (uniform_local_closeness_not_uniqueness; static_not_dynamic) | Statement with six unproved obligations, falsifying scenario at second order, and the certified static two-sided distance ‖ρ_R−P_R‖₁ ∈ [4.3786e-10, 4.4055e-10] of every limit from the Haar product |
| 5 | AZ1 | accepted_within_scope | Dictionary identities exact; one volume-uniform estimate at fixed a (gap g²/(32a)); none uniform in a; toy-trajectory crossovers n*=2/132 (and 4/421); no fraction of the continuum problem |
| 5 | AZ2 | accepted_within_scope (sign_certified_finite_graph; static_not_dynamic) | Two-face two-plaquette graph, D∈{6,8}: derivative exactly 1/6 (↔ 1/144 under τ_FG=τ/24, consistency only), second-order coefficient exactly 0, ⟨W₁⟩ enclosed at six grid points with certified tails; never a transfer |

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
