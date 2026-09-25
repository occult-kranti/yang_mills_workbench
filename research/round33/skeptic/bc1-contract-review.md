# BC1 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/bc1.json` (sha256 `3fb84ed3…79bd`, frozen 2026-09-25T04:21:44Z) before reading anything of the BC1 producer. I am a model-agent skeptic with correlated ancestry. This is not human review. My pre-freeze review (`bc-contract-review.md` / `.json`) wrote the 6 blocking and 13 non-blocking BC1 edits that the frozen text carries, so this review also checks my own wording. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written. Nothing blocks production.** `bc1_check.py` establishes the following:
- 55 checks pass, byte-identical under `-B` and `-B -O` (and without `-B`; no cache is written);
- every restated value can be read by hash from a declared gate, and `N_sign` follows from declared gate values by exact arithmetic;
- all 25 controls execute as damaging mutations: 86 mutations, each rejected for the expected reason, plus 5 positive cases accepted;
- 6 source-edit mutations of the program all abort (§5).

Three readings will matter at the post-comparison:
- **R2:** the `-10^-8` restatements need no pointwise pairing of states.
- **R4:** the finite-box node stays open, although the F1 route to it looks short.
- **R1:** `N_sign` does not depend on which BB2 value is read, but only the bound value may be used.

## 1. Frozen bytes against the pre-freeze edits; producer inputs

**Edits.** All 19 BC1 replacement texts of `bc-contract-review.json` are in the frozen bytes verbatim at their paths (6 blocking, 13 non-blocking; check `prefreeze_edits_verbatim_in_frozen_bytes`). The removal of `gate_fields_required.resolved_interaction_shift` is in force. I did not diff the draft further.

**Plan record.** The plan history entry "BC1 and BC2 frozen after the skeptic's pre-freeze review" records the BC1 hash `3fb84ed3…79bd` and `plan_sha256_at_freeze` `347f3cb1…c2f2`. The plan as committed with the freeze (e4ffdf5) has sha256 `f69d4503…b264` and holds every BC1 gate field in `vocabulary.gate_fields` (check `plan_vocabulary_covers_gate_fields`, from a recorded copy; the program does not read `plan.json` at run time, because a later BD drafting commit, 1833023, edited it during BC production).

**Producer inputs.** I ran `find` on `forward/bc1/inputs/` (names only) and hashed each file against the repository.
- The folder holds 40 files: `AGENTS.md`, the contract and its 38 shared premises.
- Every file is byte-identical to its source, and the inventory equals the contract-derived list.
- No `experts/` file, plan, panel update, deliberation or skeptic contract review is among them.

The program checks the recorded inventory against the contract and the repository hashes; it never opens `forward/bc1/`.

## 2. Executability, item by item

1. **Item 1 (AV2 node).** The AV2 gate gives `d = 497870683678639429793424156500617766317/(4·10^40)`, `R = 1831967503411879425147166810021607/10^40` and the interval, which is exactly `[d−R, d+R]` (checked). The free reference `e^{-3}/4` is inside. Executable by reading.
2. **Item 2 (AW2 enclosure).** The AW2 endpoints are exactly `tau/144 ∓ K_2^+ tau^2` at `tau = 10^-8`, with `K_2^+` read from the same gate, and the mirror is `[−hi, −lo]`. The gate margins are reproduced exactly. Executable by reading.
3. **Item 3 (finite-box sign).** Provable from the declared premises. The chain is BB2 item 1 at fixed `N` for the untruncated F2 vector, `M → ∞` through the closed trace-norm ball, BB2 items 2–3, AW2, and trace duality with `||W|| ≤ 1`. `N_sign = 4`, computed exactly (derivation §4).
4. **Item 4 (finite-box node).** The determination is frozen, and the record supports it as stated. I checked the cited labels in the hash-pinned AV2 reports, the AV2 gate wording ("each chosen state separately"), the AV2 reverse control row with "finite-box provenance", and the AW1 gate's "tau^2 constant explicitly unbounded (not uniform in N" (check `finite_box_node_record_determination`).
5. **Item 5 (common GNS item).** Within scope of BB2 items 2, 3 and 5, BA2 item 4 and the AQ1 gate. Nothing new is claimed.
6. **Item 6 (obligations).** The AY2 rows O1–O6 are in the hash-pinned AY2 forward report, and the BA2 gate itself records "AY2 row O6 closed within scope". All the rows the contract lists as a minimum can be written from the gates. My table is in the derivation, §7.
7. **Item 7.** The template is one literal span, scans clean with the round, contract, plan and my extra lists, and contains no placeholder.

## 3. Readings and residual defects (numbered)

1. **R1. Which `C'`.** The frozen `finite_box_sign` pins the BB2 **bound value** `C' = 4/984375 = C_h/(1−q)`, the nested-telescoping value at the hypothesis `C_h = 1/250000`. The gate also lists the union value `1/250000` and a re-evaluated value of about `9.0465e-7`, both labelled. `N_sign = 4` for every `C'` in `[lo·64^2, lo·64^3) ≈ [2.831e-7, 1.812e-5)`, so all three give the same `N_sign`. That makes a wrong choice undetectable by the integer, so the constant string must be read. My validator rejects the union value as `C'`.
2. **R2. The `-10^-8` restatements need no pointwise pairing.** BB2 holds at both signs, so the `-tau` limit of the named constructions is itself an AQ1 subsequential limit at `-tau`. The AV2 and AW2 whole-set statements at `-tau` therefore apply to it directly. The AW2 limitation that pairs individual states only along a common subsequence is not lifted by BC1 and is not needed. A producer that derives the `-tau` enclosure through `U_E` and a pointwise pairing is not wrong (the AW1 flip lemma at the zero triple plus whole-sequence convergence would give it), but it goes beyond the declared chain and must be labelled a replay.
3. **R3. The state in item 3.** `omega^{F2,N}` is the untruncated F2 ground state at fixed `N`. BB2 item 1 holds for it at fixed `N`, and `M → ∞` passes the bound to `omega_inf`. A cutoff-L F2 state is not claimed; its `M → ∞` limit would be a cutoff-L state, not `omega_inf`.
4. **R4. The finite-box node (item 4).** The F1 route looks short: F13–F14 are per box, `G_N − E_N ≥ 0` in each box, and AV1's `D` bounds each box density. But the window lemma for the finite-box vector is a new derivation, not a restatement, and BC1 correctly restates none. The two open rows must name the missing premises as the contract does.
5. **R5. `correlation_shift_resolved: false`** refers to `C(s)`. The static Wilson mean is carried by `sign_certificate_restated_for_limit` and `finite_box_sign_claimed` in the AW2 meaning. No `resolved_interaction_shift` field may be exported (it was removed at freeze).
6. **R6. `N_sign` below the cap.** At `tau/100` the same `C'` gives `N_sign = 5` (information only). AW2 admits the enclosure at the cap only, so nothing below the cap is claimed, and no bracket applies.
7. **D1 (residual, non-blocking). No limited-outcome frame for the template.** My pre-freeze review said BC1 should add the frame that BC2 got ("The frozen template, which this verdict meets only in part, reads:"). The frozen `gate_fields_rule` does not carry it. This is moot at `accepted_within_scope`. At `limited`, the gate would have to quote the template inside a frame the contract does not name.
8. **D2 (residual, non-blocking). Inherited `parameters_declare_metric_weights_window`** (BA2 text) asks for `d_X`, `N_0` and the weights `w=e^mu, e^beta`. BC1 has no decay estimate. Its parameters declare the metric, weights ("not applicable" with a reason), window, clock, node and `N_min`. I read the control as satisfied by those fields.
9. **D3 (residual, non-blocking). Inherited `wrong_delta_alpha_hbar_clock`** is about a real-time window in `u`. For BC1 the substantive case is the Euclidean free energy 3 at the clock `s` (24 in `u`). My checker executes both.
10. **R7. The obligations row for route B** must read "pending": the BC2 gate is recorded after the BC1 gate (BC2 `selected_after_note`), so the BC1 gate cannot cite a BC2 outcome.

## 4. Control mirror

- `controls` equals `preregistration.controls_required.ids`: 25 = 25, same order, no duplicates.
- 12 ids carry BC1 semantics. The other 13 are defined in the frozen BA1, BA2, BB1 or BB2 contracts, which are declared premises (latest definition used; check `control_semantics_coverage`).
- The program implements all 25 as damaging mutations against a packet validator: 86 mutations, 5 positives. The finite-box-sign control is decided against the exact `N_sign` recomputed from the gate values, not against a flag. The certificate-values control is decided against the gate rationals, including a one-unit change at `10^-40`.
- Deferred parts are scope notes only: the inventory is recorded, not re-listed at run time; the phrase scan and placeholder detector mirror the tools; tampering is checked at packet level.

## 5. What the gates give (exact values in `bc1-independent/results.json`)

| quantity | value | source |
|---|---|---|
| AV2 datum `d` | `497870683678639429793424156500617766317/(4·10^40)` ≈ 0.012446767092 | AV2 gate |
| AV2 radius `R` | `1831967503411879425147166810021607/10^40` ≈ 1.83196750e-7 | AV2 gate |
| AV2 interval | `[d−R, d+R]` exactly; `e^{-3}/4` inside | AV2 gate |
| AW2 `[lo, hi]` at `+10^-8` | `tau/144 ∓ K_2^+ tau^2` ≈ `[6.91089641e-11, 6.97799248e-11]` | AW2 gate |
| AW2 mirror | `[−hi, −lo]` | AW2 gate (replay) |
| `C'` | `4/984375` ≈ 4.0635e-6 = `C_h/(1−q)` | BB2 gate bound value |
| `N_sign` | **4** | this program |

**Source-edit mutations** (scratch copies; each aborts): `C'` replaced by the union value (the control mutation is then accepted and the run aborts); the strict comparator replaced; `K_2^+ tau^2` dropped from the AW2 endpoints; `q = 1/32`; the AV2 radius shifted by `10^-40`; obligation O6 set to open.
