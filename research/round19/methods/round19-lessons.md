# Round19 lessons for later paired loops

These are operational lessons from the actual A1/A2/B1 feedback, supplementing the frozen creation-time method snapshots. They do not change any accepted scientific premise.

- **Count physical states, not just assignments.** At a fixed spin-network energy, sum the product of vertex invariant multiplicities over admissible edge-label assignments. At B1's excluded threshold, 99 assignments give 107 states. The strict below-threshold projector remains 48-dimensional.
- **Compare matrix entries before their quadratic form.** Combine ordered coupling monomials within each ordered matrix entry; check transpose or adjoint symmetry explicitly; only then compare a canonical matrix triangle. A perturbation with opposite signs in transposed entries must fail. Do not double a monomial that an independent implementation already stores in commutative form.
- **Normalize geometry before indices.** Match links by endpoint coordinates, validate ordered closed face words, and match basis and coefficient indices by their actual supports. A different enumeration order is not a different model. A permuted noncommuting word can be a different model even if its sorted signed edge set is unchanged.
- **The physical reference is a premise.** Check the declared positive energy reference itself as well as alpha/E_star and cutoff/E_star. A zero, static-kappa, tolerance or Fibonacci reference cannot be repaired by attaching numerically correct ratios.
- **Missing evidence must fail.** A source manifest is incomplete when a required source entry, output entry or file is absent. Conditional checks that run only when the missing object exists do not establish provenance. Reproduce fresh outputs from the reviewed source, then compare their actual semantics.
- **A larger projector changes the complement.** For P_new=P_old+R, the old principal block of the new cross Gram equals W_old*W_old-P_old V R V P_old. Reuse of the older Gram requires this subtraction; equality of the two complement Grams is not expected.
- **Bounded perturbations preserve the operator domain.** For the A2 bounded self-adjoint V, D(H_ref+V)=D(H_ref). The written closure and spectral argument is separate from exact coefficient arithmetic; JSON premise flags are not formal proofs.
- **Preserve the full target when using an exception.** A2's summable product representation does not establish finite clipped-restriction convergence or homogeneous dense stability. A correct static integral does not establish physical time-generator matching. Fibonacci geometry remains untested as physics.

A failed comparison and its repair are feedback within the same research loop. Ordinary, optimized and mutation runs do not add research loops or independent scientific roles.
