# Round33: continuation cycle, three research sub-rounds and an applications stage

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted research with the same expert panel as Round32 (Newton/Tesla, Jung/Pauli and Penrose/Feynman as documented methodological lenses), an advisor and an independent skeptic, all model agents with shared ancestry. This is not external human peer review; scientific priority is unverified; no historical figure participated or endorsed the work; no occult, mystical or governmental source becomes a premise.

The cycle starts from merged Round32 commit `519a9a2a26201422a8bfa9e3a83f9129b66b8c88`. The user asked to continue with the next three rounds and then apply the admitted solutions and new equations to their related problems. A panel deliberation fixes the plan (`advisor/brief.md`, `advisor/plan.json`); three research sub-rounds of two investigations follow (BA, BB, BC), each with prospectively frozen contracts, producers, skeptic packages, byte-identical replays, reviews and gates, lens updates and one research assistant per lens; the applications stage (BD) applies the admitted equations to related problems and records obstructions where they do not transfer. All earlier scientific records, Draft03 and the Round31 and Round32 addenda retain their bytes; the root `AGENTS.md` is hash-bound by the Round32 gates and is not edited.

| Sub-round | Loop | Result | Limitation |
|---|---|---|---|
| 1 | BA1 | accepted_within_scope (boundary_decay_rate_only; static_not_dynamic) | Boundary change moves the AM2 coefficients on supports meeting R by at most K q^(N-1): K about 4.38e-7 at q=1/64, about 2.43e-5 at q=37888\|tau\|; both routes, every comparison, both signs, uniform in the cutoff; coefficients only, not the state |
| 1 | BA2 | accepted_within_scope (dynamics_on_compact_windows) | F1 and F2 Heisenberg evolutions of observables A on R with \|\|A\|\|<=1 differ by at most about 2.55e-11 (5N+1)/N^3 for \|theta\| at most 8; Cauchy estimates at O(1/N) in N; the padded family's limit dynamics is AQ1's; algebraic dynamics only |
| 2 | BB1 | accepted_within_scope (boundary_decay_rate_only; static_not_dynamic) | Reduced densities of the named constructions on R differ by at most C q^(N-1), C about 8.91e-7 at q=1/64, and on regions Y by c_site\|Y\|e^{\|Y\|/10^8}q^{d_Y}, c_site about 8.77e-7; every comparison, both signs, each cutoff space and untruncated at fixed N; polymer expansion and recursive split; per comparison, not a limit |
| 2 | BB2 | accepted_within_scope (convergence_of_named_constructions; common_limit_of_named_constructions) | F1 and F2 reduced densities converge as whole sequences at rate q^(N-1) (C' about 4.06e-6 on the cover R; region form c'_site \|Y\| e^{\|Y\|/10^8} q^{d_Y} with c'_site about 2.03e-6) to one common limit on every finite region; equal to every AQ1/F2 subsequential limit; coarse-translation invariant; correlation functions on \|theta\| at most 8 converge (rate 1/N only on 5<=N<=14000); BB1 hypotheses discharged by the BB1 gate; not uniqueness of any ground state |
| 3 | BC1 | accepted_within_scope (certificate_restated_for_limit; reference_unresolved, static_not_dynamic) | At tau=10^-8 (tau=-10^-8 a mirror replay): AV2 node at s=1 (radius about 1.832e-7) and AW2 Wilson-mean enclosure restated unchanged for the limit of the named constructions; untruncated padded boxes have certified sign for N at least 4 at tau=+-10^-8 only; one GNS triple and dynamics for the two limits; obligations updated (O1 split: limits of F1/F2 coincide, closed; uniqueness of any ground state, open); no finite-box node |
| 3 | BC2 | accepted_within_scope (convergence_of_named_constructions; certificate_restated_for_limit, reference_unresolved, static_not_dynamic) | Route-B uniform model: K_B=13/27941256, C_B about 9.45e-7, c_site,B about 9.31e-7 at q=1/64; whole-sequence convergence of its one named construction, exhaustion, pointwise sign mirror, coarse translations, identification with every AQ1-type subsequential state; AX2 node at tau=10^-8, s=1 (radius about 1.912e-7) restated for the limit; no route-B dynamics |
| 4 | BD1 | accepted_within_scope (transfer_to_named_model; obstruction_recorded) | Link-flip lemma transfers to SU(2), SU(4), U(1), Z2; first-order parity to SU(2), SU(4), SU(5), U(1), Z2; first-order Wilson coefficients 1/1152 (SU(3)), 1/2880, 1/5760, 1/96, 1/48, 1/864 (SO(3)); SU(3), SO(3), SU(5) obstructions with exact nonzero coefficients; SU(2) area parity at kappa=0 in F1 boxes and for the limit; one-plaquette models and boxes only |
| 4 | BD2 | accepted_within_scope (sign_certified_finite_graph; transfer_to_named_model, obstruction_recorded, static_not_dynamic) | Two-plaquette graph with independent couplings: exact coefficients through total order 4, flip parities, 1x2 loop certified positive at l1=l2 in {+-1/10, +-1/100, +-1/1000}; zero-selected family at \|tau\| at most 10^-8: Z^3 1x2 mean zero at first order and at most about 1.34e-12 at \|tau\|=10^-8; electric energy band about [2.88e-19, 9.8e-7] at \|tau\|=10^-8; 2+1D AM2 cap about 1.58e-3 (constants only); no area law, no certified 1x2 sign |

Loop counts are never a fraction of the four-dimensional Yang–Mills problem, which remains open.

## Records

- Reviewed findings: [`advisor/findings.json`](advisor/findings.json) (eight rows, summary, scope statement, applications ledger); admission specification: [`advisor/admission-spec.json`](advisor/admission-spec.json); gates: `advisor/<loop>-gate.json`.
- Plan and panel: [`advisor/brief.md`](advisor/brief.md), [`advisor/plan.json`](advisor/plan.json) (plan v2, contract rules, vocabulary, history with the plan sha at every freeze), deliberations 1-2, panel updates 1-4, selection notes.
- Contracts: `contracts/<loop>.json` (frozen after the skeptic's pre-freeze reviews `skeptic/bb-contract-review.*`, `bc-contract-review.*`, `bd-contract-review.*`).
- Producers: `forward/<loop>/` and `reverse/<loop>/` (report, exact checker, snapshotted inputs, output, freeze).
- Skeptic: pre-comparison packages (`<loop>-contract-review.md`, `<loop>-independent-derivation.md`, `<loop>_check.py`, `<loop>-independent/`), post-comparison reviews (`<loop>.md`, `<loop>.json`, `<loop>-replays.json`, `<loop>_postreview_check.py`, `<loop>-postreview/`), the BB2 discharge record `bb2-bb1-admission.json` and the Kotecky-Preiss repair record `bb1-kp-repair.md`; `skeptic/programs.json` lists every program.
- Committed source excerpts: [`sources/`](sources/) (Nachtergaele-Sims arXiv:1410.8174v1; Ueltschi arXiv:math-ph/0304003v3, committed after the BB1 freeze as a repair source).
- Lenses and assistants: `experts/<lens>/` (memo, sources, loop-2 response, updates 1-4, assistant packages 1-4); the occult reading ledger `experts/occult/reading-ledger.md`.
- Roadmap (planning only): [`advisor/roadmap.json`](advisor/roadmap.json); handoff: [`HANDOFF.md`](HANDOFF.md); tools: [`tools/`](tools/).
- Addendum: [`papers/round33-addendum/main.pdf`](../../papers/round33-addendum/main.pdf) with its build receipt and page-image QA.

## Reproduce

```sh
python3 -B research/round33/reproduce.py --complete --validate-only
python3 -B research/round33/reproduce.py --complete --output /absolute/fresh/r33-normal
python3 -B -O research/round33/reproduce.py --complete --optimized --output /absolute/fresh/r33-optimized
python3 -B research/round33/test_admission.py
python3 -B research/round33/forward/bb1/check.py --output /absolute/fresh/one-producer
python3 -B research/round33/skeptic/bb2_postreview_check.py --output /absolute/fresh/one-review
node tests/round33_site.mjs --require-release
```

Replay outputs must be fresh absolute directories outside the checkout and reproduce `output/` byte for byte under normal and `-O` Python. Publication follows [`release/README.md`](release/README.md).
