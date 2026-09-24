# Round32 lessons: linear local state bounds and window kernels

Written from admitted Round32 evidence only; extended after each gate. Read this before any continuation that compares an interacting fixed-lattice state with a product reference or transfers a real-time comparison to Euclidean time.

## Admitted after AV1 (gate `research/round32/advisor/av1-gate.json`)

- A variational energy (reset) bound yields amplitudes of order sqrt(tau); it can never certify a local expectation to first order. The AM2 commuting nilpotent creation expansion gives the finite-volume ground vector explicitly; ordering the product so that creations meeting the cover act last separates an R-vacuum component from an R-excited one that are exactly orthogonal, so the outside normalization cancels without any adjoint exponential or inverse of e^{-C}. Two routes: the explicit reduced density (forward) and the vacuum overlap with the pure-state-mixture inequality (reverse).
- The normalization trap: outside creations appear in both numerator and denominator; restricting the numerator alone to supports meeting R gives a volume-dependent wrong value. Require a finite fixture that exhibits it.
- Two tiers, never mixed: the crude AM2 majorant (about 2.4e-5 at tau=1e-8) and the exact first-order coefficient with the self-consistent remainder (about 1.4e-8). Every constant names its tier. Derive face counts from the I1 table by translation covariance (49 omitted faces per factor, 15 owner sets, 82 meeting the cover, 10 inside it); 84 is only a bound.
- Cutoff removal must be proved for the ground vector, not only for eigenvalues (AM2 section 6 covers eigenvalues); the uniform gap and a Rayleigh/Eckart-type overlap argument suffice. Passage to the AQ state uses local trace-norm convergence only and yields a statement about every subsequential limit: uniform local closeness, never uniqueness, whole-sequence convergence or a rate in N.
- Pre-registration: the target and reference are read by the checker from the frozen contract; the pre-registration control mirror must equal the contract control list (the freeze tool now enforces it); the reverse producer's premise inventory is isolated by contract and validated.

## Admitted after AV2 (gate `research/round32/advisor/av2-gate.json`)

- The Poisson kernel's absolute first moment diverges, which is the whole source of the cutoff-and-tail floor (about 1.27e-6 at s=1, tau=1e-8). Any bounded continuous window equal to e^{-sx} on the nonnegative spectral support with an L^1 transform and finite first moment removes the cutoff: |C(s)-C_0(s)|<=||ghat||_1(D+m^2)+k int|theta||ghat|. The C^2 window g=e^{sx}(1-2sx+2s^2x^2) on x<0 has ||ghat||_1=2 and first moment 4s/pi. Freeze the transform sign convention (the mirrored convention reads the free atom as 25e^{-3}/4) and keep a negative-atom fixture (nonnegativity of the centered generator is essential). A kernel switch after the state bound is known is a post-hoc choice and is rejected.

## Admitted after AW1 (gate `research/round32/advisor/aw1-gate.json`)

- Before charging any first-order budget, compute the first-order coefficient exactly. In the zero-selected family SU(2) center grading (an odd number of j=1/2 factors on some link) kills every first-order term of the centered correlation and of omega(W^2); the only first-order Wilson effect is the uncentered mean +tau/144 under I1.5. A "resolved shift" target for the centered correlation at first order is therefore empty by representation theory; re-target rather than renegotiate.
- An exact center sign flip on the link set E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even} meets every plaquette oddly and maps H(tau,kappa) to H(-tau,-kappa). Use it as an exact tau-parity control; antisymmetry in tau holds via U_E only at the zero selected triple; AQ statements are about whole sets of subsequential limits; oddness alone gives no third-order remainder. A modified flip set that reaches nonzero triples is recorded, not admitted.
- Freeze the coupling rule for a later sign certificate inside the earlier contract and evaluate it in the checker from the admitted constant; never choose a coupling after the constant is seen. Bind the largest of several valid exact-tier upper bounds when producers' term counts differ; require every term to name its tier. Write contract shorthand formulas with the convention stated (the AV1 c^(1) is minus the ground-vector correction).
- Shared scratch directories are not isolation: require producers to disclose scratchpad reads and keep private subfolders.

## Admitted after AW2 (gate `research/round32/advisor/aw2-gate.json`)

- A single-direction certificate is admissible only with the skeptic's independent replay written from the contract alone and committed before the producer's package; the review then shows one admitted formula replayed correctly, not independent physical confirmation. Say so in the gate.
- A "resolved interaction shift" is always scoped to the observable and the order at which it is first order: here the static equal-time Wilson mean at the zero triple, with the sub-label static_not_dynamic; never the centered correlation, a mass shift or a susceptibility.
- Report the exclusion margin (distance of the enclosure from the reference divided by its half-width) and the sign margin separately; freeze which one the target uses. A preview file that the checker reads must be labelled veto-only if it can abort a run but never supplies an admitted value.
