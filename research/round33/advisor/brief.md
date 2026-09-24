# Round33 brief (advisor)

Date 2026-09-24. Human project author: Hruday N M (BUNZEEY). All panel members, the advisor, the skeptic, the producers and the research assistants are model agents with shared ancestry; this is not external human peer review; scientific priority is unverified; no historical figure participates or endorses anything.

## User instruction

After the merged Round32 (pull request #15), the user asked: "continue with the next 3 rounds - and then apply all these solutions and new equations to solve their related problems - if any". In the Round32 instruction a "round" was a sub-round of two investigations with the advisor, the skeptic and the expert panel, with one research assistant/coder per expert after each sub-round and goal changes allowed after each. Round33 therefore runs:

1. a panel deliberation (two loops: lens memos with source search plus the skeptic's triage; then responses and sign-off on the plan);
2. three research sub-rounds of two investigations each (BA1/BA2, BB1/BB2, BC1/BC2), each followed by lens updates, one assistant package per lens and a panel update;
3. an applications stage (sub-round 4: BD1/BD2) that applies every admitted Round32/Round33 solution and new equation to the related problems where it applies, and records an explicit obstruction where it does not ("if any");
4. integration, release verification, pull request and merge.

## Starting knowledge (read before writing)

- `research/round32/HANDOFF.md`, `research/round32/advisor/findings.json`, all ten gates `research/round32/advisor/*-gate.json`, `research/round32/advisor/roadmap.json` (ranked: uniqueness, dynamics, whole-sequence convergence, continuum statement, triggered second-order constant), `research/round32/advisor/panel-update-5.md`, the closing lens updates `research/round32/experts/*/update-5.md`, `research/round32/experts/modern/sota-closing.md`, `research/round32/experts/occult/reading-ledger.md`.
- The admitted equations and constants: AM2 creation expansion (J<=28|tau|, R=1/64, G(t)=16e^{8t}(1+10t), G(R)<148/7, G'(R)<352), the AV1 linear local state lemma (tiers; D about 1.36e-8), the C^2 window kernel (M_0=2, M_1=4s/pi), the center-grading parity theorem and link-flip set E, +tau/144, K_2^+ about 3354.80, route B for the uniform model (J'=29|tau|, 52 faces per factor), AY1 closeness 2D and the R-local K_2' about 13418, the AY2 two-sided distance tier and six obligations, the AZ1 dictionary identities and lattice-unit floor, the AZ2 finite-graph coefficients.
- Rules for this round: `research/round32/experts/jung/update-5.md` section 3 (ten rules; the contract freezer `research/round33/tools/freeze_contract.py` enforces R1-R5 and R8), `research/round32/advisor/panel-update-5.md`, the lessons file `.codex/skills/qeg-research-advisor/references/round32-state-lemma-and-window.md`. The root `AGENTS.md` is hash-bound by every Round32 gate and is not edited.

## Advisor's candidate directions (for triage, not decisions)

- **Boundary-influence decay (roadmap goals 1 and 3 together).** The AM2 fixed point is obtained by a contraction on local creation coefficients. If the contraction also controls how a change of the box boundary propagates through chains of overlapping supports, the R-marginal of the finite-box ground vector may form a Cauchy sequence in N with an explicit rate (each chain step costing a factor of order J G(R) < 1/64), giving whole-sequence convergence for each family and a common limit for both families. This would be convergence of the named constructions, never uniqueness of every infinite-volume ground state; it must be derived, with a pre-registered target and a retained failure if the chain argument does not close.
- **Dynamics (goal 2).** A Lieb-Robinson/Duhamel comparison of the Heisenberg dynamics of A in B(H_R) between the two families on compact time windows with the AQ1 Nachtergaele-Sims constants (F(r)=(1+r)^-4, C<=224, ||Phi||_F<=2268|tau|, ||Phi'||_F<=1323|tau|), and then the consequence for the correlation functions of a limit (if the first direction succeeds).
- **Consequences.** If a limit exists, the AV2/AX2 node certificates and the AW2 sign certificate become statements about that limit rather than about each subsequential limit.
- **Applications stage (candidates).** Gauge-group transfer of the parity theorem and the link-flip lemma (U(1), Z2, SU(N): the flip needs -1 central; SU(3) has center Z3); the state lemma and window kernel in two spatial dimensions (2+1D); other observables (larger Wilson loops, electric-flux or Casimir observables); the two-plaquette graph and the earlier finite-model rounds; the site calculators. Every application is a labelled transfer to a named model with its own exact checks; an equation that does not transfer is recorded with the obstruction.

## Panel tasks for deliberation loop 1

Each lens writes `research/round33/experts/<lens>/memo.md` and appends read sources to `research/round33/experts/<lens>/sources.json` (per-record: id, title, author, url, version_date, section, reading_depth, provenance, claim, relevance, unresolved; access failures recorded). Lenses may search current state-of-the-art research, patents, rumours and government programmes in any field; the Jung lens keeps the occult/mystical reading ledger `research/round33/experts/occult/reading-ledger.md`. No source becomes a premise; custody is not confirmation. The skeptic writes `research/round33/skeptic/triage.md` and `research/round33/skeptic/prospective-controls.json`. The advisor then writes `advisor/plan.json` and deliberation records; loop 2 collects responses and sign-offs before the first contract freezes.
