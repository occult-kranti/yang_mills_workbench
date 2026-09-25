# BC1 skeptical review (post-comparison, statement loop, single producer)

**Standing.** I am a model-agent skeptic with correlated ancestry: same model family as the advisor, the lenses and the producer. The frozen BC1 texts carry my pre-freeze edits. This is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY).

**Order, as it happened.**
- The contracts froze at e4ffdf5 (04:22:10Z).
- My values were final at 04:53:13Z (results sha256 `48414d13…5bdd`). The forward `check.py` was last written at 04:54:30Z.
- The **forward commit 5816e0b (04:57:15Z) came first**. My pre-comparison package was committed after it, at 5ec599f (05:00:47Z).
- I saw the forward commit subject, which states `N_sign=4`, only in a `git log` after my values and first freeze were final. That was a name-only exposure, disclosed in my derivation.
- I opened `forward/bc1/` only after the coordinator's post-comparison message. I did not open `forward/bc2/`.

**Verdict: `accepted_within_scope`.** Sub-label `certificate_restated_for_limit`, with secondary `reference_unresolved` (the node) and `static_not_dynamic` (the sign). There are **no blocking issues**.

One piece of producer wording is **not adopted** for the gate text. The forward records AY2 row O1 ("uniqueness of the limit") as `closed_within_scope`, and its verdict says "AY2 rows O1–O6 are closed within named scopes". **Reviewed decision:** O1 is closed only in the narrow form, that all subsequential limits of F1 and F2 coincide on every finite region (one limit of the named constructions, BB2 items 2–3). Uniqueness of any ground state, states outside the named constructions and other boundary conditions are not proved and remain open. The gate carries the reviewed table below.

## What the packet proves, with quantifiers

For the zero-selected patterned family at `tau = ±10^-8`, the minus sign a replay:

1. **Node.** `omega_inf` is the limit of the named constructions, equal to every AQ1 and every F2 subsequential limit on every finite region (BB2 items 2–3, used before any inheritance). It satisfies the AV2 certificate at `s = 1` with the gate's `d` and `R` unchanged. The interval is exactly `[d−R, d+R]`. `e^{-3}/4` lies inside, so the reference is unresolved.
2. **Static mean.** `omega_inf(W) ∈ [L, U] = [tau/144 − K_2^+ tau^2, tau/144 + K_2^+ tau^2]`, with the AW2 endpoints unchanged and the mirror at `−tau`.
3. **Finite-box sign.** For every `N ≥ 2`, the untruncated F2 ground state has `omega^{F2,N}(W) ∈ [L − C' q^(N−1), U + C' q^(N−1)]`. Here `C' = 4/984375` (the BB2 bound value) and `q = 1/64`. The proof is the BB2 item-1 whole-sequence bound, `M → ∞` through the closed trace-norm ball, and trace duality with `||W|| ≤ 1`. **`N_sign = 4`.** The sign equals the sign of `tau` for every `N ≥ 4` at both signs. `N = 2, 3` and cutoff-L F2 states are not claimed. The F1 boxes are AW2's.
4. **Finite-box node.** None is restated. Two open rows (N2, N3) record the missing premises.
5. **Common GNS item.** One state gives one GNS triple and one dynamics, `T_theta`. Correlation functions on `|theta| ≤ 8` are BB2 item 5, with a rate in N only on `5 ≤ N ≤ 14000`. This is not equality of GNS dynamics of different states.
6. **Obligations.** A table of 18 rows (O1–O6, N1–N12), reviewed below.

## Restated values against the gates and my predictions (all exact)

My post-review checker recomputes every value from the gates with the parsers of my frozen pre-comparison module. It never uses a producer value. Every item matches:

| quantity | producer | independent recomputation / prediction |
|---|---|---|
| AV2 `d`, `R`, interval | gate rationals; interval `[d−R, d+R]` | equal |
| `K_2^+`, `L`, `U`, mirror | gate rationals; `tau/144 ∓ K_2^+ tau^2`; `[−U, −L]` | equal |
| AW2 exclusion and sign margins | ≈ 206.00005, ≈ 207.00005 | equal (to below `10^-5` in the 8-digit previews) |
| `C'` | `4/984375` (bound value; union `1/250000` and re-evaluated ≈ 9.0465e-7 rejected) | equal (my R1) |
| widening table `N = 2…8` | `1/15750000`, `1/1008000000`, `1/64512000000`, … | equal, row by row |
| **`N_sign`** | **4** | **4 (predicted)** |
| widened enclosure at `N = 4` | `[232256915653307984268043972456662444208313/4332507027163714822873992017230554960022732800000000, 369480171452763518908899363269803522461511/…]` ≈ `[5.36080e-11, 8.52809e-11]`, with its mirror | equal (predicted `[5.36080e-11, 8.52809e-11]`) |
| widened enclosure at `N = 3` | lower end ≈ `−9.22955e-10` (contains 0) | equal (predicted) |
| `L/(C' q^3)` | "about 4.4584" | 4.45835749 (predicted ≈ 4.4584) |
| widened exclusion margin | "about 3.3851" (labelled) | 3.38509554 |
| `tau/100` information | half-width ≈ `1.5501e-11` against the first-order value `6.944e-13`; nothing claimed | equal (my R6) |
| gate fields | the 15 frozen values | equal |

**Consistency replays** (the producer's; I reproduced them with my own Machin `pi` and `e^3` series):
- `R − (2(D+D^2) + 49|tau|/pi + 1/(4·10^40))` ≈ 2.65e-41, which is below `10^-40`.
- The AV2 forward radius lies below `R` by the same margin.
- `|d − e^{-3}/4|` ≈ 1.0195e-43, below the stated 1.02e-43.

These are consistency replays, not sources of any restated value.

## The O1 decision

**What AY2 meant.** AY2's O1 is "uniqueness of the limit". Its missing premise is "a two-state estimate, **or a classification of every state in the class**, that forces two subsequential limits to agree on R". Its candidate routes (HTW-type stability, a Dobrushin-type condition) are routes to uniqueness of states. The row therefore mixes two contents:
- a narrow one: two subsequential limits of the named families agree;
- a broad one: every state of the class agrees.

**What BB2 settled.** BB2 items 2–3 settle the narrow content for F1 and F2. They do not touch the broad content. The plan, the contract's claim exclusions ("uniqueness of every infinite-volume ground state"), the template ("not uniqueness of any ground state") and the coordinator's panel update 2 keep the broad content excluded.

**Reviewed wording** (binding on the gate text):
- **O1a** — `closed_within_scope`: all subsequential limits of F1 and F2 coincide on every finite region, giving one limit of the named constructions, `omega_inf`. Closing gate: BB2 items 2–3. Scope: the named constructions F1 and F2, the zero-selected family, fixed spacing, `|tau| ≤ 10^-8`, both signs.
- **O1b** — `open`: uniqueness of any ground state (every infinite-volume ground state), states outside the named constructions and other boundary conditions. It is linked to N1. Routes: HTW or Dobrushin with evaluated constants, or a BB1-type comparison for a pre-frozen class of prescriptions.

**What the producer wrote.**
- The O1 cell carries the scope ("scope: the named constructions F1 and F2 only") and a pointer: "Beyond it (states outside the named constructions, other boundary conditions, uniqueness of every infinite-volume ground state) see row N1".
- Its other uniqueness wording is negated or excluded.
- `uniqueness_of_ground_state_claimed` is false, and no control is violated.

So this is not a blocking defect. But the status `closed_within_scope` under the AY2 name, and the summary "AY2 rows O1–O6 are closed within named scopes", read as a uniqueness closure out of context. They are not adopted. Two further facts:
- The producer checker **hard-codes** O1 as `closed_within_scope`: a report edit to `open` aborts with "AY2 row status: O1". So the reviewed status cannot enter the frozen packet; it enters the gate.
- The producer checker does **not** pin the O1 scope qualifier. Replacing it with "scope: every ground state" runs silently. My validator rejects that edit.

**Is the phrase scan a safeguard here? No.** I classified every clause of the report that mentions uniqueness (check `uniqueness_wording_classified`):
- negated or excluded;
- field or control identifiers;
- the verbatim claim-exclusion lists;
- descriptions of rejected mutations (§11);
- the pointer to N1;
- the single O1 row.

There is no other kind. The scanner is negation-aware, but it is silent on the O1 row **by vocabulary, not by negation**. The round list and the contract list contain neither "uniqueness of the limit" nor "uniqueness of every infinite-volume ground state". An affirmative "Uniqueness of every infinite-volume ground state is proved." gives no hit; "Uniqueness of the infinite-volume ground state is proved." does, and the negated form passes. The reviewed wording, not the scanner, guards O1. Advice for later contracts is at the end.

## Obligations: reconciliation and the reviewed table

| row | producer (18 rows) | skeptic pre-comparison | reviewed |
|---|---|---|---|
| O1 | closed_within_scope | open | **split: O1a closed (narrow), O1b open** |
| O2–O6 | closed within BB2/BA2 scopes | same gates and scopes | closed within scope (O5 not uniform in time, not GNS dynamics of different states) |
| N1–N9 | open (N9 pending the BC2 gate) | same content | open |
| N10 uniform in `a`, N11 continuum | open | my N12, N13 | open |
| N12 interaction shift of `C(s)` (carried from Round32) | open | not a row (an exclusion) | kept |
| analyticity of the reduced density (BA1/BB1 limitations) | — | my N10 | added as **N13** |
| untruncated creation coefficients (BA1 limitation) | — | my N11 | added as **N14** |

The reviewed table has 21 rows: O1a, O1b, O2–O6, N1–N14. It is in `bc1.json` and in `bc1-postreview/results.json`. The contract's minimum list is met by the producer's table; N13 and N14 are additions by review, non-blocking.

**N4 and its preview "sign margin about 51.76".**
- I recomputed `1/(144 K_2' tau)` from the AY2 gate `K_2'`: it is 51.7565134 (exclusion margin 50.7565).
- The route is real. AY1 F13–F14, as quoted in the AY2 forward report §4.2, bound the R-local remainder by `K_2' tau^2` "in every box of either family at every cutoff", "uniformly in N, cutoff and family". `Tr(rho^(1)_R W) = +tau/144`.
- But the AY1 and AY2 gates admit `K_2'` for subsequential limits only. The box-level form, and the untruncated F2 passage for it, are not gated.

**Decision:** the number is admissible in an obligations row as a labelled candidate-route preview, and it is labelled "labelled preview, not claimed". In the gate it may appear only with the fuller label "not admitted; rests on an ungated box-level reading of AY1 F13–F14", which the reviewed table carries, or without the number. It certifies nothing for `N = 2, 3`.

## Producer disclosures and notes, adjudicated

1. **Heredoc report write.** The file tool refused the report, so it was written with a shell heredoc. The content is bound by `freeze.json` and verified. Accepted as disclosed, as in BB1.
2. **The first report check** let two damaging edits run silently: one of the two `N_sign = 4` claim sites changed to 3, and one occurrence of a repeated preview changed. The producer fixed and disclosed this before freezing. I re-ran both edits on the frozen checker, and both now abort ("the report states an N_sign other than the computed value"; "… not an exact truncation or a quoted gate decimal").
3. **The non-damaging silent edit.** Tightening the least-`N` rule to `L/4` runs silently. I reproduced it: every exported value is unchanged (`N_sign = 4`), so it is harmless. The producer's reading, that the checker certifies the answer rather than the code path, is correct for this edit.
4. **W1–W5 against my D1–D3 and R2/R4.**
   - W1: `selection_reason` omits AW2's finite-box statement. Correct; new against my list.
   - W2: the two claim-exclusion lists differ by one entry. Correct; a residue of my pre-freeze alignment edit.
   - W3 is my D2.
   - W4: item 4 needs two rows where the list has one entry. Correct.
   - W5 is my R3.
   - My D1 (no limited-outcome frame for the template) and D3 (the inherited clock control) stand; the producer executes the clock control fully.
   - My R2 (the `−tau` restatements need no pairing) agrees with the producer's L5. Each sign has one limit, so AW1's whole-set flip pairs them, recorded and used for no value. The producer's reading is correct.
   - My R4 (the F1 finite-box node is short but new) agrees with its N2 route.
5. **P1.** The BB2 forward report says the harmonic fixture "exceeds 4 at `N=119`". The sentence is literally true (`a_119` ≈ 4.36), but it reads as a first exceedance, and the first is `N = 83`, exactly. No BB2 constant or gate text depends on it. Recorded.

**Further observations (non-blocking).**
- The producer checker does not pin three labelled report numbers: 4.4584, 3.3851 and 51.76. Edits to them run silently; my validator catches them.
- Row N10 cites the AL1 dictionary of the uniform model for `g^4 ≥ 9.6×10^9`, and says so. It is not a statement about the patterned family's coupling.

## Review against the contract items

- **Items 1–2:** met exactly, with the identification before inheritance.
- **Item 3:** met; `N_sign` is exact with the strict comparator, and there are widened endpoints at both signs.
- **Item 4:** met from the record; the producer verifies the same eight record facts I checked.
- **Item 5:** met with its scope.
- **Item 6:** met, with the O1 wording corrected in the gate.
- **Item 7:**
  - the template appears once as one unbroken line, and verbatim in the results;
  - the gate fields are exported as frozen;
  - 25/25 controls run as damaging mutations: 104 rejections in the control checks, 113 in total;
  - the output is byte-identical under `-B` and `-B -O`.

## Replays, closure and isolation (`bc1-replays.json`)

- **Replays.** The forward replays reproduce `output/` byte for byte, normal and `-O`, and `freeze.py verify` reports verified.
- **Closure.** 44 files, verified one by one.
- **Inputs.** 40, equal to the contract-derived list and to the inventory I recorded before production, and byte-identical to the repository.
- **My pre-comparison package** is unchanged and replays byte for byte.
- **Release layout.** In a git-archive tree of HEAD plus the new skeptic files, `bc1_postreview_check.py` reproduces `bc1-postreview/results.json` byte for byte, under both normal and `-O` runs.
- **Isolation** rests on disclosure and content, as in BA/BB. My untracked files were in the shared checkout during production, and the forward discloses no read of them. The forward's O1 status and row set differ from mine, and none of my specific constructs appears in its packet.

## Mutation harness (`bc1_postreview_check.py`, 17 checks, 41 source-edit runs; byte-identical under `-B` and `-B -O`)

- **25 validator weakenings.** One per contract control, on temporary copies outside the checkout. Each run aborts with the expected "damaging mutation accepted: <label>".
- **12 must-abort edits.** These include:
  - the two formerly silent report edits;
  - O6 and O1 set to open;
  - N3 removed;
  - a forbidden phrase and an altered template;
  - two `check.py` edits;
  - three input edits.
- **4 silent edits.** The producer's non-damaging one, which is harmless. The O1 scope, the N4 preview and the `L/(C' q^3)` number, which run silently and are rejected by my validator.
- **Phrase scan.** The round tool (subprocess) and my mirror give no affirmative hit on the report.
- **Gate text.** The supported statement and the joined limitations of `bc1.json` pass `tools/phrase_scan.py` with the BC1 contract: exit 0 and no hit, negated or not. The template appears once, as one unbroken span.

## Blocking issues

None.

## Non-blocking findings

1. The O1 status wording is not adopted; the gate uses the reviewed split (see above).
2. The producer checker hard-codes O1 as closed and does not pin the O1 scope qualifier or three labelled numbers. Silent edits of these are caught by my validator.
3. The N4 preview 51.76 is admissible only as a labelled candidate-route number of an ungated route.
4. The phrase-list vocabulary gap for "uniqueness of the limit" and "uniqueness of every infinite-volume ground state".
5. The heredoc write, the fixed first report check and the harmless silent edit, all as disclosed.
6. P1 (BB2 fixture wording).
7. The commit order: the forward commit came first; values were concurrent (above).

## Contract defects

- W1 `selection_reason`.
- W2 the two exclusion lists.
- W3 = D2 no `d_X`/`N_0`.
- W4 one entry for two rows.
- W5 = R3 the template's implicit state.
- D1 no limited-outcome frame for the template.
- D3 the inherited clock control is loosely fitted to a statement loop.

None is blocking.

## Which values the gate binds

- **AV2:** `d`, `R` and the interval, unchanged.
- **AW2:** `K_2^+`, `L`, `U` and the mirror, unchanged.
- **BB2:** `C' = 4/984375`, `q = 1/64`.
- **`N_sign = 4`**, with the widening `C' q^(N−1)` (`1/64512000000` at `N = 4`) and the widened enclosures at `N = 4` at both signs.
- **Density rate in N:** `q^(N−1)` for every `N ≥ 2`. **Correlation rate in N:** only on `5 ≤ N ≤ 14000` (BB2).
- **Labelled only:** the ratio 4.4584, the widened exclusion margin 3.3851, the `tau/100` half-width, and the N4 preview 51.7565, which is not admitted.

## Limitations

- **Scope.** The zero-selected family, `R`, fixed spacing, `tau = ±10^-8`, the named constructions and their limit. Nothing transfers to other triples, route B (BC2), other boundary conditions, weak coupling or the continuum.
- **Restatement only.** The node remains an upper certificate with the free value inside, and the mean is static.
- **Finite-box sign.** F2 untruncated vectors for `N ≥ 4` only.
- **No finite-box node.**
- **O1.** Closed in the narrow form only.
- **Inheritance.** Inherited without re-proof: AV2, AW1, AW2, BB2 (with its BB1 discharge, the Kotecký–Preiss citation checked post hoc, and the AY1 local reading for non-centred F2 volumes), BA2, AQ1/AQ2 and AV1.
- **Admission basis.** Admission rests on the single forward producer plus my pre-comparison replay, with correlated agents. Scientific priority is unverified.

## Advice (planning only)

- Add "uniqueness of every infinite-volume ground state" and "uniqueness of the limit" to later contracts' `forbidden_phrasings`. Negated and quoted occurrences stay admissible under the negation-aware rule and the exclusion-list quoting.
- For a row carried over from an earlier obligations table, freeze the reviewed row name with the contract whenever an admitted result settles only part of the row.
- N4 is the cheapest open row: a statement loop gating the box-level AY1 F13–F14 remainder for untruncated F2 vectors would certify `N = 2, 3` directly, with margin about 51.8.
