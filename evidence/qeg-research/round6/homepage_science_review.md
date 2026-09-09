# Bounded claim-to-web-copy science review

Reviewed: `round6/homepage_claims.json`, all 11 claim pages, against the frozen mathematical verdicts, response contract, extension proofs and executed check records. The following are concrete copy defects; no new research or Site edits were performed.

## HSR-01 — The response objection incorrectly denies the finite-model commutator connection

**Location:** `R4-R1.objection`.

**Current text:** “Tangent sensitivity is not the quantum current commutator or a current-noise correlator.”

**Defect:** The blanket first denial contradicts `round4/response_contract.md` P24–P26, which explicitly derives a finite-model retarded commutator kernel and the differentiated instantaneous-vacuum contact term. The coupled source-amplitude tangent is a restricted response, not an unrelated classical construction. Its inability to provide symmetrized noise remains correct.

**Replace with:** “This source-amplitude tangent is a restricted projection of the finite-model retarded current response, including its required contact terms. It does not reconstruct the full spacetime QED kernel or the symmetrized quantum current-noise correlator. A signed first variation of energy is not a norm. Some comparisons used the wrong nonzero probe history.”

## HSR-02 — The stationary counterexample silently changes the tested coefficient set

**Location:** `R6-L4.tests`, third item.

**Current text:** `M=1` implicitly through `h=(1,0,0)`, `w=e²=Z0=1`, and energy `5/4`.

**Defect:** The energy `5/4` is algebraically correct for that alternate toy coefficient choice. It is not the frozen executed secular example or the matrix-propagator fixture, both of which use `M=w=e²=1`, `p=0`, `chi=0`, `Z0=3/4` and energy `1`. Moreover, within the defined model `Z0=1` requires `chi=1/4` because `C0=1/4`; leaving chi unstated hides that change. `extensions.md` and `skeptic_checks_results.json` agree on the original `3/4` fixture.

**Preferred replacement:** “Explicit checked counterexample: one mode M=w=e²=1, p=0, chi=0, Z0=3/4, u=1, q=s, eta=(0,−1/2,−s). Then E2=1 stays constant while |eta| grows.”

If the alternate `Z0=1` example is retained, label it a separate illustrative toy model with `chi=1/4`, not the executed matrix fixture. Do not imply either toy coupling is the frozen physical alpha used in the production run.

## HSR-03 — Kinetic momentum is incorrectly labeled fixed, and constant parameters are incomplete

**Location:** `R5-T1.definitions` and theorem assumptions.

**Current text:** “Fixed p_i=k_i−a”.

**Defect:** p_i evolves with `p_i'=x`; it is the canonical momentum k_i that is fixed. The work identity also requires fixed masses, weights, positive e² and constant chi. Time-dependent matching produces extra work terms, so those constants should not be left implicit on the theorem page.

**Replace the start of the definition with:** “In natural units hbar=c=1, s=m_e t, a=eA_z/m_e, x=eE_z/m_e² and b=|eB|/m_e². Fix k_i, M_i>0, w_i>0, e²>0 and finite real chi. The time-dependent kinetic momentum is p_i(s)=k_i−a(s).”

Also use `b=|eB|/m_e²` in `R3-M1.definitions`, or explicitly restrict the chosen orientation to eB>0. The existing contract defines the nonnegative magnetic parameter with an absolute value; allowing signed b would invalidate positive Landau masses/weights. Natural units must be visible when calling `m_e t` dimensionless.

## HSR-04 — The tangent page weakens the regularity hypothesis too far

**Location:** `R4-R1.assumptions`, first item.

**Current text:** “A differentiable source/data family and a finite interval where the base denominator is positive.”

**Defect:** Pointwise source parameter differentiability alone does not justify exchanging time integration and parameter differentiation. The frozen critique gives a moving-pulse counterexample. The theorem requires a common parameter neighborhood and joint/local-uniform regularity on compact time intervals.

**Replace with:** “A common parameter neighborhood with differentiable admissible initial data and source parameter derivatives jointly continuous on compact time/parameter sets, on a finite interval where the base denominator stays separated from zero.”

The existing separate zero-initial-tangent and unchanged-pre-probe-source assumptions should remain.

## HSR-05 — The symbolic check count is mislabeled as an identity count

**Location:** `R5-T1.tests`, first item.

**Current text:** “Sixteen exact symbolic identities”.

**Defect:** The historical suite has 16 symbolic **checks**, including two deliberately incorrect expressions whose nonzero residuals are detected. Those two controls are not valid identities. The total check count is correct; its description is not.

**Replace with:** “Sixteen symbolic checks, including fourteen exact identities and two deliberate-defect controls, repeated in the corrected runner.”

## HSR-06 — The joint-cutoff derivation describes the susceptibility sign incorrectly

**Location:** `R6-L3.steps`, “Use an exact recurrence”.

**Current text:** “Subtract the same chi ... to obtain the displayed Z.”

**Defect:** The model is `Z=1+chi−e²C`: chi is added, while the coefficient contribution is subtracted. The displayed final formula is correct, but the procedural sentence reverses the matching sign.

**Replace with:** “Use the digamma recurrence to sum the finite harmonic terms, then combine them in Z=1+chi_b−e²C with the unchanged susceptibility. The finite b-dependent pieces cancel, giving the displayed Z.”

These corrections preserve the accepted equations and their scopes. They change misleading text or fixture provenance rather than the underlying proofs.
