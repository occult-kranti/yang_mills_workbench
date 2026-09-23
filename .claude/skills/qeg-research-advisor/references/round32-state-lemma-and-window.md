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
