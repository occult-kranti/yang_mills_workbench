# Newton method lens: audit, selected reading, and proposed continuation

Prepared 2026-09-22 from repository checkpoint `9b5a41d`, Round26 HANDOFF, AG/AH/AI roadmap, Draft 01 roadmap/recent sections, and the AE2 forward report. This is a modern researcher using selected documented methods. It is not Newton speaking, historical endorsement, exhaustive knowledge of Newton, or external peer review. The source inventory records the actual reading depth.

## Decision supplied to the advisor

Prefer **AG: one actual nonlinear homogeneous update**, because the largest immediate logical gap is the passage from a contracting individual source to a controlled collective interaction. AE2 already says its rooted weight-2 estimate proves finiteness, not contraction. Another accurate small-graph simulation does not repair that inference. If the contract cannot produce a useful nonlinear bound, report the obstruction and select a narrower mathematical question after review. AI's identifiability test is the strongest alternate: it can distinguish observable information from a fitted physical clock.

The proposed mathematical device below is a candidate for a frozen contract, not an admitted new result or a production run. No scientific production simulation was executed for this literature/planning report.

## Historical source distinctions that change the work

| Primary record read | What the record supports | Modern use, explicitly our interpretation |
|---|---|---|
| `De motu`, Theorem 2 corollaries and Theorem 3 [N1] | Newton reconstructs force dependence from orbital geometry and limiting quantities. | Write the identifying map and its hypotheses before inferring a cause from an observed scalar. |
| `Opticks`, Query 31 closing paragraphs [N2] | Analysis moves from observed effects toward causes; synthesis checks consequences. Newton explicitly treats the remaining hints as requiring further examination. | Couple inverse reconstruction to a forward prediction with a rejection test. |
| `General Scholium`, closing paragraphs [N3] | Its speculative subtle-spirit passage ends by acknowledging inadequate experiments for a demonstrated law. Its theological discussion is separately explicit. | A hidden-cause proposal is not an extra term in the Hamiltonian until it has units, operational meaning, and discriminating evidence. |
| `Of Natures obvious laws & processes in vegetation`, opening outline [N4] | A historical attempt to organize mineral, plant, and animal processes around a latent principle. | Ask whether a single map connects two model descriptions, then require measure, state, domain, and generator control. |
| `Experiments`, 10–15 December 1678 entries [N5] | Dated operations and recorded masses/residues, including material left after operations. | Keep complete residual/error accounting and unsuccessful cases. These notes do not establish transmutation. |
| Keynes MS.28, English Emerald Tablet passage, ff.2r–2v [N6] | Newton's translation/transcription of a prior Hermetic text uses correspondence and separation/recombination language. | Propose a correspondence test; do not assume correspondence is a theorem or Newton's original physical discovery. Latin commentary was not fully translated. |
| `Observations upon the Prophecies of Daniel`, I.II [N7] | An explicit dictionary from natural imagery to political/theological interpretation. | Publish the dictionary between a metaphor and its proposed mathematical variable. This is a transparency practice, not physical evidence. |

The occult/mystical material is retained as historical material and a source of questions. The word “spirit” cannot silently mean a quantum field, dark energy, a new particle, or a measured frequency. A public Reddit discussion [D1] contains competing interpretations of this passage, including a participant correcting an earlier overstatement. That is useful evidence of interpretive disagreement; it is not evidence that either physical mechanism is true. We returned to the primary passage rather than choosing the comment that fit the desired theory.

## Current research examined

This is a targeted search current to 2026-09-22, not a complete SOTA review or a novelty search.

- **Local Krylov truncation** [M1]: Ciavarella, Burbano, and Bauer construct local plaquette-generated truncations with explicit plaquette/link restrictions. Their retained finite representation is a computational lead for AH. Their large-N expansion and truncation cannot certify this workbench's exact SU(2) omitted channels by citation. The paper also explains why the strictly leading large-N theory's vanishing correlation length is inadequate for a continuum limit.
- **Area-law progress** [M2]: Cao, Nissim, and Sheffield's version 3 treats a master-loop equation and controls comparison between a truncated model and the original one. Theorem 1.2 and its surrounding discussion were read; the full 35-page proof was not audited. The useful methodological connection is that simplification is followed by a proved comparison defect. Its U(N), coupling, and observable hypotheses are not interchangeable with AG's homogeneous Hamiltonian family.
- **Dynamical area-law route** [M3]: the abstract reports a route through a mass-gap condition for selected groups with nontrivial center. This is a follow-up lead only, not an imported theorem. Its physical/stochastic generator and gap notion must be reconciled with ours before using it.
- **A 2026 negative control** [M4]: Nissim's SO(3) preprint abstract states failure of Wilson's confinement criterion in a strong-coupling regime. This is sufficient to flag that a blanket identification of “mass gap,” “area law,” and “every non-Abelian group” is unsafe; we have not audited its proof.
- **Formalization** [M5]: Douglas and collaborators discuss formal methods and AI-assisted backward chaining. Treat this as a route to making hidden premises explicit, not evidence that passing Python checks proves an operator theorem. Selected overview passages only were read.
- **Target definition** [M6]: Jaffe–Witten requires a nontrivial four-dimensional theory with the required axiomatic properties and a positive physical mass gap, for every compact simple gauge group. A finite-graph gap or a controlled truncated evolution does not establish that target.

## Proposed AG contract ingredient: pay for growing supports

For bounded interactions on finite nonempty supports, define, for `a > b >= 1`,

\[
 \|\Phi\|_a=\sup_x\sum_{X\ni x} a^{|X|}\|\Phi_X\|,
 \qquad \delta=\log(a/b)>0.
\]

The parameter `a` is dimensionless proof bookkeeping; it changes neither the action nor the physical energy scale. Define the interaction commutator by summing `[Phi_X,Psi_Y]` on `X union Y` for overlapping supports. Splitting the rooted sum according to whether the root belongs to X or Y gives

\[
 \|[\Phi,\Psi]\|_b
 \le 2K_{a,b}\left(\|\Phi\|_a\|\Psi\|_b+
                         \|\Psi\|_a\|\Phi\|_b\right)
 \le\frac{4}{e\delta}\|\Phi\|_a\|\Psi\|_a,
 \quad K_{a,b}=\sup_{n\ge1}n(b/a)^n\le\frac1{e\delta}.
\]

Reason: after choosing X, the sum over overlapping Y costs at most `|X| ||Psi||_b`. The factor `|X|` is absorbed by the strict weight loss; `b^{|X union Y|} <= b^{|X|}b^{|Y|}`. This derivation explains exactly why retaining only a fixed weight without a support factor does not close the same estimate.

Allocate the total loss `delta` equally over n nested commutators. If `S` and `Phi` have finite a-norm, this suggests the explicit bounded-interaction estimate

\[
 \frac{\|\operatorname{ad}_S^n\Phi\|_b}{n!}
 \le\left(\frac{4\|S\|_a}{\delta}\right)^n\|\Phi\|_a,
 \qquad \eta=\frac{4\|S\|_a}{\delta}<1.
\]

Here `n! >= (n/e)^n` removes the factorial cost. A resulting BCH tail after order N is at most `||Phi||_a eta^{N+1}/(1-eta)`. This is a proposed analytic bound for review; it is not a bound on an unbounded onsite Hamiltonian without an additional domain argument. In the actual AG step, first use the bounded commutator identity `[S,G]=-A+R(A)` to handle the unbounded G term, preserve its graph domain, and keep scalar/diagonal/off-diagonal terms separate.

**Acceptance tests proposed for the advisor**:

1. Re-derive AE2's full translated source count at the chosen `a>2`. At weight a the same counting argument should replace `192 M` by `24 a^3 M`; this must be proved from the complete supports, not copied as a new constant. Require `24 a^3 M T<1` and the actual `eta<1` before invoking the tail.
2. Compute the exact first conjugation, including the residual and all twelve translated crossings. Compare its degree-N expansion and a complete remainder against a finite-volume direct calculation only as a consistency test.
3. Include zero source, both coupling signs, overlapping and disjoint supports, a large-support family, and a control deliberately deleting a crossing. Test the original rooted weight-2 output, not a replacement diameter norm.
4. State whether the upper bound is smaller than the original collective source budget. If it is not, the verdict is a proved bounded update or failed contraction certificate. Do not infer actual divergence from the failed certificate.
5. Treat the consumed weight margin as a resource. A first step with `a>2` does not prove infinitely many steps: later support growth, diagonal change, and the sum of norm losses need a new induction.

The proposed benefit is a precise place to test whether an extra proof variable repairs a genuine missing estimate. It is not a new physical field. Scientific priority of this elementary norm-loss device and of the project's particular constants remains unverified.

## Alternate AI test and progress estimate

If the panel chooses AI first, freeze real laboratory time and independent parameters rather than defining time by the desired endpoint phase. Compute the Jacobian of complete readouts; exhibit any parameter family in its kernel; retain the elementary Wilson null probe and add a genuinely discriminating readout. A scale fit cannot identify two independent parameters when all measurements depend on one combination.

There is no defensible scalar **percentage of the Yang–Mills problem solved** from this research inventory. A percentage requires a complete finite proof-dependency list and meaningful weights, neither of which is available. The workbench has admitted controlled model results, while homogeneous induction, a volume/cutoff-uniform matched continuum trajectory, nontrivial reconstruction, and the continuum physical gap remain open. The panel can report a disclosed checklist completion fraction, but it must label that fraction as workbench bookkeeping rather than mathematical distance to the theorem. This lens's numerical completion estimate is therefore **not estimable**, not an invented percentage.

See `sources.json` for canonical URLs, retrieval date, claim role, and reading depth.
