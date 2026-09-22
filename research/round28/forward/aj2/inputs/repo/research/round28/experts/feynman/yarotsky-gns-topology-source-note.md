# Yarotsky source check for a possible homogeneous physical-GNS contract

Source verification only, 2026-09-22. Zero research loops; no theorem
application, energy/tightness estimate, fixture or goal selection. AH2 current
science was not read. This note preserves the earlier source and planning
files and is available for the advisor's selection after the sixth gate.

The primary text is D. A. Yarotsky,
[math-ph/0411042v1](https://arxiv.org/pdf/math-ph/0411042), submitted
11 November 2004, 17 pages. I inspected the PDF text and corresponding
[arXiv HTML](https://arxiv.org/html/math-ph/0411042v1), specifically definitions
and Theorems 1–3 on printed pp.2–4, the creation-operator definition on pp.6–7,
and the thermodynamic/generator passages on pp.9–10. The long source proof
and its cited earlier papers were not independently reconstructed. The ledger
records exact passages and access depth.

## What the inspected source states

The full local algebra is `A_infinity=union_F B(H_F)` for finite site sets.
Theorem 2 gives convergence of finite-ground-state expectations for each such
observable. Theorem 3 specifies a self-adjoint GNS Hamiltonian by convergence
of resolvent matrix elements tested on local excitation vectors, fixes its
vacuum at energy zero, and retains the stated spectral estimates. Section 2
defines its action using local bounded commutators. With
`u_I in H'_I intersect Dom(H_I,0)`, it describes the span of creation vectors
`pi(û_I)Omega`, asserts density and essential self-adjointness, and invokes
the resolvent expansion. Theorem proofs are attributed to earlier references.

No explicit local-normality, trace-norm convergence of local density matrices,
continuous gauge implementation or Haar-averaging compatibility statement was
located in these inspected passages. The unitary symmetries discussed after
Theorem 3 are lattice translations under an additional hypothesis. This
limited reading does not establish that local normality is false, unavailable
from the full theory, or requires one particular proof method.

## How those statements constrain a future contract

The following are prospective workbench obligations, not deductions executed
in this source pass.

| Item | Required distinction or proof obligation |
|---|---|
| Limit topology | Keep the source's pointwise state limit and tested resolvent limit as stated. Do not relabel them trace-norm convergence of local states, strong resolvent convergence on the earlier summable Hilbert space, or convergence of a bounded infinite-volume global unitary. |
| Local normality | If used, establish that the actual I1 limiting state restricted to each relevant `B(H_F)` is normal, and justify the local representation property needed for the subsequent averaging. Alternatively supply a direct regularity and averaging argument with equally explicit hypotheses. The words weak-star limit do not themselves serve as that argument. |
| Gauge implementation | Establish invariance of the actual homogeneous state, identify its gauge implementers and prove the continuity needed on finite products of endpoint groups. Specify the local automorphism and represented unitary, rather than assuming the concrete J2 implementation survives a change of representation. |
| Compatible Haar averages | Distinguish the weak operator average in the original finite link factor from vector integration in the homogeneous GNS representation. Justify that the represented local average acts on the cyclic vector as the desired averaged vector; an arbitrary representation cannot be silently treated as preserving the original weak operator integral. Retain every endpoint and the exact finite support. |
| Algebra | Use the full bounded local invariant algebra if the target is equality of invariant and physical cyclic spaces. A selected list of Wilson loops is a different algebra and has no inherited equality. |
| Generator domain | Match a valid source domain/core or prove a separate resolvent-commutation route to a reducing physical subspace. Do not declare every bounded-local cyclic vector to be in the unbounded generator's domain. The source's creation-vector restriction is material. |
| Physical restriction | Prove a reducing spectral restriction with its domain, rather than a formal compression. Keep the already centered homogeneous generator and the fixed physical energy units. No new quantitative gap is supplied by an abstract GNS identification. |

The advisor's suggested local vacuum-reset/energy-tightness route is **only a
prospective proof obligation** here. No reset map, variational inequality,
energy ceiling, spectral cutoff or tightness bound has been constructed or
checked in this note. Likewise, no gauge-cyclic equality is asserted for the
homogeneous model at this stage.

## Controlling project scope

Current I1 gate revision 2 and its skeptic already admit the complete
24-link/21-face homogeneous-omitted-coupling dictionary, the qualitative
fixed-spacing gap at symbolic small coupling, and the specified positive-orthant
full-algebra GNS state and generator. The theorem and boundary application
remain inherited results. I1's skeptical review explicitly leaves the
gauge-invariant observable GNS identification separate. This note adds no new
I1 admission or numerical interval.

Current J2 gate and skeptical review admit the physical cyclic/invariant
identification in the **dyadic summable** representation. Its proofs use
already strongly continuous concrete gauge unitaries, a weak operator local
Haar average and its compatible strong vector integral, full-algebra cyclicity,
and a reducing unbounded generator. They do not assume point-norm continuity
of conjugation on all bounded local operators. Those carefully scoped J2
premises explain what must be rebuilt or replaced for the actual homogeneous
representation; its numerical gap, vacuum and Wilson variance do not transfer.

The primary check therefore supports a bounded future question about
representation regularity and compatible gauge averaging, with an explicit
insufficient outcome if a needed transfer is not proved. It does not select
that question or turn it into an executed investigation. It also does not
reopen I1's qualitative gap as an unproved milestone.
