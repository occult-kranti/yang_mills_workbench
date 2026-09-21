# W2 independent skeptic review

Verdict: **accepted for fixed-G finite-step identities, actual vacuum-column
graph convergence and fixed-finite-volume full-source strong limits; the
full-source weighted and later-diagonal closure target remains limited**.
Both direction submissions were frozen before this comparison. This is
independent model-agent review, not external peer review.

## All-step identities and domain

Both reports keep `A_n=R^n(A)` and the accumulated filtered generator, whose
commutator is exactly `-A+A_n` on D(G). Every residual remains present. The
bounded strong-integral domain theorem applies to each bounded source at each
finite step. The resulting finite graph-norm bound allows both exponentials
to preserve D(G); it gives no uniform infinite-step generator bound.
The scalar multipliers correctly retain zero frequency and negative sinc
values. They are not used as an unproved full-operator Schur multiplier bound.
This is a fixed-G linear construction, not an executed nonlinear sequence of
diagonal updates.

## Actual column estimates

The initial form comparison and orthogonality place the actual vacuum-response
vector above `g>=381/416`. Both global absolute-sinc bounds are valid: forward
uses `rho=1-(Theta g)^2/10`, reverse uses the stronger sufficient
`rho=1-(Theta g)^2/8`. Their piecewise Taylor/envelope arguments control all
energies, including negative sinc lobes. Spectral calculus then gives the
actual residual-column norm decay and accumulated-column G-graph convergence
in finite volumes and the admitted infinite representation.

The iteration-count examples target different accuracies and use different
inequalities. Forward uses an exponential sufficient estimate for error below
one thousandth; reverse uses a conservative Bernoulli estimate for a tenth or
an extra coupling factor. Their counts cannot be presented as contradictory
or as optimal. Uniformity is at fixed positive Theta; it does not cover a
uniform contraction rate as Theta goes to zero. At fixed n a numerical factor
does not improve the asymptotic power of tau.

## Full-source topology

In a fixed finite complete-block volume, a finite product of SU(2) electric
Casimirs has compact resolvent. The selected potentials and finite retained
diagonal sum are bounded perturbations, so G retains compact resolvent.
For a vector in one eigenspace, orthogonality and dominated convergence give
the residual's limit in its equal-energy output block. Density and uniform
boundedness extend this to the full strong-operator limit
`sum_E P_E A P_E`. Both proofs are valid in that stated volume and topology.
Neither computes the actual excited diagonal blocks or shows that this limit
vanishes. No pure-point premise for the infinite G is silently imported.

Forward's compact-resolvent paired-level countermodel verifies that even a
zero strong limit and discrete spectrum can coexist with residual norm one
at every step. Reverse's simpler bounded-generator example also refutes
strong-to-norm inference, but is explicitly not a compact-resolvent model.
Neither is asserted to be the actual SU(2) spectrum. The identity-extended
source is not Hilbert-Schmidt when its exterior Hilbert space is infinite;
the optional Hilbert-Schmidt remark cannot close the actual source problem.

## Replay, controls and remaining premise

Normal and optimized runs reproduce frozen outputs exactly. All source hashes,
contract dependencies and method inputs verify; both producers contain at
least three true Boolean controls. `w2-replay.json` records the checks.
The telescoping, zero-frequency, negative-sinc, decaying-column/retained-block
and near-degenerate topology controls discriminate actual wrong inferences.
Finite rational spectral coefficients remain algebra fixtures.

The inherited weight-2 positive bounds cover only three composed time windows
at the cap. Their loss at the fourth composition is a limitation of those
upper bounds, not failure of R^4 or of every possible method. Applying a
single-star estimate again without tracking generated support would be invalid.
Full operator/weighted decay, actual excited-sector diagonal data and an
all-step support theorem remain missing. Later-diagonal closure additionally
needs actual updated scalar/diagonal/source terms, ground projection, form
constants and domains. No homogeneous numerical gap or continuum conclusion
is admitted by W2.
