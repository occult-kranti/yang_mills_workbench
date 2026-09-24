# Jung/Pauli lens, Round32 sub-round 2 -> sub-round 3 update

Advisory only; model-agent lens with correlated ancestry to the advisor, producers and skeptic. No historical-person participation or endorsement. Human project author: Hruday N M (BUNZEEY); AI-assisted.

## 1. Observation-map assessment of sub-round 2

**Coupling fixed before the constant was seen: yes.** `contracts/aw1.json.parameters.aw2_coupling_rule` freezes the decade-grid rule ("never chosen after K_2 is seen") before AW1 production existed. AW2's `check.py` evaluates it internally from the hash-verified AW1 gate's `K_2^+` (`results.json` id `aw2_coupling_rule_prefrozen`), rejecting a supplied literal, an off-grid value, `10^-9`, the forward AW1 headline constant and a rule bound not half the coefficient; the skeptic's independent replay (contract-only) reaches the identical `tau_AW2=10^-8` and slack. No node was chosen post hoc.

**Sub-labels applied: yes, both correctly.** `results.json`: `static_not_dynamic:true`, `sign_certified_below_cap:false` (honest, since `tau_AW2` equals the cap, not a below-cap value) -- matching update-1 sec.3's prediction exactly.

**"The interaction shift is resolved": honestly scoped.** `resolved_interaction_shift:true` is set only for the static, uncentered mean `omega_tau(W)`, "and only because the exclusion holds at the cap" (report sec.6). The report and results.json both restate, unweakened, that the centered correlation `C(s)`/`c(theta)` remains `reference_unresolved` (AV2) and that no dynamical, mass-shift or susceptibility claim is made. The sentence is never applied to the correlation. Good practice: `correlation_shift_resolved:false` is an explicit control-tested flag, not a silent omission.

**Scratchpad isolation (AW1 finding N1, carried into the gate).** Both AW1 producers used the shared scratchpad root 23:14-23:20Z pre-commit without disclosing reads; the forward's `k2.py` overwrote the skeptic's own pre-comparison scratch file at the same path. Isolation is verified for repository inputs only; scratch-channel independence is unrefuted but unaudited. **Rule to add:** require private per-agent scratch subfolders plus a mandatory scratch-read-disclosure line in every future report (skeptic already recommends this; AW2's skeptic honoured it -- "scratch work stayed in a private subfolder" -- and it should become a contract control, not a courtesy).

**Contract sign-shorthand defect.** AW1 item 3's literal display `omega_tau(W)=2<W Omega_0,c^(1)>` evaluates to `-tau/144` under the AV1 convention; both producers derived `+tau/144` and rejected the literal reading as a damaging mutation. The gate recorded it as a non-blocking "contract wording defect," did not amend the frozen contract, and instructed the gate text itself not to repeat the bad display -- correct handling (repair by record, not by silent edit, per AGENTS.md).

## 2. Goals for sub-rounds 3-5

- **Sub-round 3 (AX1/AX2, uniform Hamiltonian).** No change to the goal; proceed, but require the pre-registration items in sec.3 below before AX1 leaves `draft`.
- **Sub-round 4 (AY1/AY2, state identification).** No change; keep `uniform_local_closeness_not_uniqueness` and the forbidden-phrasing list in force.
- **Sub-round 5 (AZ1/AZ2, continuum + finite graph).** No change; AZ2 stays `transfers_to_aq:false` and is never cited toward the continuum goal.

## 3. AX1/AX2 pre-registration specifics

- **Uniform label.** Model text must read "uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling" (per `selection-ax1.md`), never "weak coupling" or "continuum" -- both phrases are explicit `claim_exclusions` and `preregistration.claim_exclusions` entries in `ax1.json`/`ax2.json`.
- **J_0 re-freeze as a pre-registered constant.** `J_0'=29/10^8` (Resolution A/R1) is written into `ax1.json.parameters.J0_resolution` with its two exact contraction inequalities before any AX1 outcome exists; control `j0_resolution_declared` rejects reuse of the old `J_0=7/25000000` at `tau=10^-8`. Resolution B (capping `|tau|<=7/725000000`) is named and excluded in advance as a changed-coupling relabelling, not chosen after the fact.
- **Route declaration.** Route B (Haar reference kept; three selected faces per factor moved into the interaction as single-factor groups) is fixed in the selection note and contract before production; control `reference_route_declared` exists precisely to block the route-A/route-B mixing flagged in `loop2-response.md` sec.(d) ("AM2's h_x already contains the selected potential ... reference no longer Haar" vs. the Haar-based 102|tau| budget) -- a real historical hazard in the drafting, correctly closed by a named control rather than by trust.
- **Forbidden wordings.** "weak coupling" and "continuum" are both listed in `ax1.json`/`ax2.json` `claim_exclusions` and the shared `preregistration.claim_exclusions`; `ax1.json`'s model line states this explicitly ("Not weak coupling, not continuum").

## 4. Occult/mystical sources

None. No occult, mystical or synchronicity source supplied any premise, force, Hamiltonian term or coupling value in sub-round 2; all such material remains excluded per Round32/Round29 `sources.json` and served only as cautionary template, as in sub-round 1.

## 5. Assistant tests wanted after sub-round 3

1. Verify `ax1.json`/`ax2.json` `controls` == `preregistration.controls_required.ids` byte-for-byte (continuing the AV2-mirror-gap check; both already pass at freeze but must be re-checked once AX1/AX2 are frozen post-review).
2. Replay `j0_resolution_declared`: recompute `J_0'*148/7=1073/175000000<1/64` and `2*J_0'*352=319/1562500<1` as exact rationals, and confirm rejection when `J_0=7/25000000` is substituted at `tau=10^-8`.
3. Grep both AX1 and AX2 reports and results.json for "weak coupling" and "continuum" (must not appear as claims), and confirm every scratch file used in AX1/AX2 production carries a per-agent-private-subfolder disclosure line per the new scratchpad rule.
