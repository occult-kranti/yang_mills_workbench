# Jung/Pauli lens, Round33 sub-round 1 update

Status: bounded advisory input after BA1/BA2 admission, before BB1/BB2 freeze. Contemporary methodological lens grounded in the documented texts in this lens's `sources.json`; not participation, endorsement, recreated private thought or human peer review. No research loop, simulation or production calculation was executed by this agent. Human project author: Hruday N M (BUNZEEY). Read this update: `advisor/ba1-gate.json`, `advisor/ba2-gate.json`, `skeptic/ba1.md`, `skeptic/ba2.md`, `advisor/plan.json`, `advisor/deliberation-2.md`, `experts/modern/bb-targets-proposal.md`, own `loop2-response.md`. `experts/jung/assistant-1/README.md` is not yet present; the advisor records it in panel update 1.

## 1. Observation-map assessment of sub-round 1

Pre-registration was honoured. BA1's twelve frozen gate fields hold exactly as prefrozen: `coefficient_cauchy_claimed=true` with the scope "AM2 creation coefficients of F1 and F2 on supports meeting R"; `state_decay_claimed`, `whole_sequence_claimed`, `common_limit_claimed`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `translation_invariance_claimed` all false. BA2 exports `whole_sequence_claimed=true` but with the scope pinned to "dynamics only, no state," `dynamics_limit_identified_claimed=true`, and `gns_dynamics_equality_claimed`, `state_convergence_claimed`, `common_limit_claimed`, `uniform_in_time_claimed`, `uniqueness_of_ground_state_claimed` all false — the F2-limit-equals-AQ1 identification is exported as a dynamics fact, never smuggled into a state fact. Both mandatory sentence templates appear once as one unbroken span in each of the four producer reports, both phrase scans (`phrase_scan.py` and the skeptic's own negation-aware scan) are clean, and both sub-label sets (`boundary_decay_rate_only`+`static_not_dynamic` for BA1; `dynamics_on_compact_windows` for BA2) are exactly the vocabulary this lens proposed in loop 1 and audited in loop 2. R6/R7 (the phrase-scanner and template-quoting checks I asked to be moved into `record_gate.py`) evidently held: no gate text carries an affirmative forbidden phrase, and both templates quote correctly.

**One item still open from my loop-2 dissent.** `deliberation-2.md`'s sign-offs record my narrowed ask verbatim: the future BB selection note must record why no separate Dobrushin/HTW loop runs, with the answer already drafted ("the weighted contraction of BA1 is the stronger form of the same smallness, and uniqueness of every ground state stays excluded in any case"). `advisor/selection-bb1.md` does not exist yet. This is not a new dissent; it is the same one, still unresolved on the record, and it binds the coming BB1 selection note.

## 2. Goals for sub-round 2

**Keep BB1 (`polymer_kp` forward / `iterated_split` reverse) and BB2 (`nested_telescoping` / `union_comparison`).** `plan.json`'s sub-round-2 loop titles already carry the vocabulary I audited in loop 2 word for word (`sub_labels_allowed` includes `convergence_of_named_constructions`, `common_limit_of_named_constructions`; the `rate_in_N`/`rate_in_a` split is preserved). No change is needed to the shape.

**The modern proposal's targets, vocabulary-audited.** `q=1/64` headline and the "floor not reachable for reduced densities" claim: both routes are said to need weight beyond `q_min`, for stated (not yet machine-checked) reasons — acceptable as a target, provided the required derivations actually carry the proof rather than the assertion. `q2=4 q_min` labelled as an "optional secondary pair": correctly scoped as a labelled, non-headline value, matching this lens's own T-A1/T-A2 discipline of never letting a secondary reading substitute for the frozen headline. `C<=4e-6`: the proposal's own §7 shows the naive `2e-6` reading has margin only ~1.14 against the admitted (not the loop-1 preview) BA1 reverse `K`, and explicitly says "do not freeze it" — correct, and the `4e-6` figure restores the margin-of-2 discipline. The correlation bound's three separate constants (`C_dyn`, `c_site`, `C'`): correct under this lens's own rule against merging distinct error channels into one number, and the proposal's item-5 table shows why — at `N=5` the state term exceeds the dynamics term, so a single lumped constant would hide which channel actually governs the bound.

**One vocabulary gap to close before BB2 freezes.** `bb-targets-proposal.md` §3 itself flags that `dynamics_level: correlation_functions_compact_window` "is a new value; add it to plan.json before freeze." `plan.json#/vocabulary/gate_fields` does not yet list it. This must be added the same way `sub_labels_allowed` was extended twice in loop 1/2, with a dated entry, before BB2's contract can export it.

## 3. Concrete requirements for the BB1/BB2 contracts

- **Gate-field pairing, taken directly from the proposal.** BB1: `state_decay_claimed:true` with a named scope, `rate_in_N_claimed:true`; false: `whole_sequence_claimed`, `common_limit_claimed`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `translation_invariance_claimed`, `weak_coupling_claim`. BB2: `whole_sequence_claimed:true` with `whole_sequence_scope` naming F1 and F2 on every finite region; `common_limit_claimed:true`; `state_convergence_claimed:true`; `translation_invariance_claimed:true` only with the scope "coarse translations; the limit of the named constructions"; `dynamics_level:correlation_functions_compact_window` (pending the vocabulary addition above); false: `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `weak_coupling_claim`.
- **P7 isolation, as an inventory check, not a promise.** The BB1 reverse producer's `inputs/` must be checked the way BA1's `reverse_premise_isolation` control was checked: no file under `experts/modern/memo.md`, `experts/modern/bb-targets-proposal.md`, or `skeptic/triage.md` present, by byte-identical inventory comparison against the contract's declared premise list — a machine check, mirroring the BA1/BA2 precedent, not disclosure alone.
- **The historical lens's fixed-N boundary-condition item.** Its own update flags this; this lens's role is to require it appear as a distinct contract item with its own required field, never folded into the Cauchy-chain requirement by silence.

## 4. What this lens's research assistant should test after sub-round 1

1. A template/phrase dry run: run `tools/phrase_scan.py` against the BB1/BB2 draft contracts once frozen, exactly as `record_gate.py` will, before either loop's production begins.
2. Grep every contract and, once written, every report for `dynamics_level` values, confirming `correlation_functions_compact_window` is a registered member of `plan.json`'s vocabulary before it is used — testing the gap named in Section 2.
3. A P7 isolation script: diff the BB1 reverse producer's declared `inputs/` inventory against the three named files (`experts/modern/memo.md`, `experts/modern/bb-targets-proposal.md`, `skeptic/triage.md`), failing loudly if any is present, writing the result rather than trusting disclosure text alone.
4. A one-loop pilot of the R9 field-mirror sweep between `plan.json#/vocabulary/forbidden` and `tools/phrase_scan.py#/ROUND_FORBIDDEN`, since this is still outstanding from loop 2 and BB1/BB2 will add new phrase surface.

## 5. Occult/mystical sources

None read this sub-round. A dated addendum with no new entries and the required sentence is appended to `../occult/reading-ledger.md`; `sources.json` is unchanged.

**No occult proposition became a physical premise.**

## 6. Closing line

This lens admits nothing and counts zero research loops.
