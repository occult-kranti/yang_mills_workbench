# Separate mathematical audit of Round20

Audit status: all ten new research loops D1,D2,E1,E2,F1,F2,G1,G2,H1,H2
checked after their advisor gates. No unresolved mathematical implication error
was found within the narrowed claims described below. One conditional-state-space
ambiguity was corrected explicitly. This is a separately assigned agent review
within this project, not external human peer review.

## What was examined

The reviewer read all ten frozen contracts, both reports for each loop, the
production implementations, relevant advisor decisions, the inherited A1/A2 reports
and the Round18 dressed-bridge argument. The review checked mathematical implications,
state spaces, operator domains, energy units, infinite-limit premises and
independence of the two calculation paths. It did not treat an output field
named `passed`, an advisor decision or a content hash as mathematical proof.

An initial independent replay covered seven loops. The final replay covered
all ten loops in ordinary and optimized Python, for 40 producer executions
in fresh scratch directories. All generated result bytes agreed with their
admitted outputs, and the source inventories checked at replay. The separate
exact checker also reproduced identically in ordinary and optimized execution.
Replays establish reproducibility of the implementation; the arguments below
are the separate assessment of what its results imply.

## D: finite factors, resolvents and ground projections

The reference Hilbert space is the incomplete tensor product based on the
complete-strip ground vectors and free-link Haar vectors. Completing the
support of each retained omitted face under complete strip factors is finite.
The factor assignment is disjoint: selected x-links use their x residue and
paired y row; selected y-links use their even y row and four-position x block.
The opposite residue/y cases and all z-links are free. There is no second
completion propagation after a complete factor is included.

The omitted dyadic total is exactly `107/135`. Direct omitted-class summation
and all-minus-selected summation are algebraically equivalent, and every
coefficient tail is positive. The actual finite lift includes the entire
exterior reference generator. Consequently the difference from the limiting
operator is the bounded multiplication tail, of norm at most
`epsilon_L=alpha*abs(tau)*t_L`. Both operators have exactly `D(H_ref)` as
operator domain; the second resolvent identity then gives the stated
`epsilon_L/abs(Im z)^2` bound. A finite number of L2 factors does not make
the Hilbert space finite dimensional. Removing the exterior generator fails
in norm resolvent, as the escaping free-link excitation demonstrates.

The ground argument needs both `beta<delta` and zero trial expectation. The
reference-vacuum orthogonal compression is at least `delta-beta>0`, while
the trial energy is zero. The spectral subspace below that threshold is
nonempty and at most one dimensional; hence it is a simple isolated ground
eigenprojection. This is a valid spectral-subspace proof without a compact
resolvent premise. The exterior-excitation sector of each finite lift starts
above zero, so its nonpositive ground belongs to the exterior-vacuum sector
and gives an actual finite-factor ground.

For the exact limiting ground vector, the residual equation against the
truncated operator is valid on the common domain. Since the limiting energy
is nonpositive, inversion of the excited block has norm at most `1/g_L`.
Thus `||P-P_L||<=epsilon_L/g_L`. Rank one is essential for the projector
leakage identity and the trace norm factor two. Removing the nonpositive
energy premise or rank-one premise invalidates those sharp steps; the retained
two-dimensional controls demonstrate this. No gap persistence is inferred
from strong resolvent convergence alone.

## E: literal boxes and all upper boundary phases

For `N=4m+3`, all selected strips that meet the cube are complete. The strip
count `(N+1)^3/8` equals the forward expression, and the three different
orientation ranges are necessary for the omitted weight. The explicit sum
of strip ground energies is an energy-origin subtraction. It leaves states,
gaps and Heisenberg conjugation unchanged; it changes resolvents at fixed z
and absolute energies.

For arbitrary anchored rectangular upper boundaries, the selected-face
components remain actual disjoint clipped strips plus free links. An omitted
non-xy face has a free z-link, an odd-y xy face has a free odd-y y-link, and
a separator xy face has a free x-link with x residue3. These exhaust the
omitted faces. Clipping cannot turn such a link into a selected link, so the
zero-mean premise survives in the clipped reference vacuum.

For a fixed bounded local observable A, the common central factor set must
cover **both A and the retained perturbation**. Completing their support and
taking a sufficiently large geometric margin yields the same central
Hamiltonian in every sufficiently large box and the infinite representation.
The differing remote reference factors then have no effect on the truncated
central ground marginal. Two residual comparisons yield
`4||A||min(1,epsilon_M/g_M)`, uniformly in the sufficiently large outer
boundary phases. Taking M first and the box size second is legitimate.
Norm-one state bounds extend local convergence to weak-star convergence on
the norm closure of the local algebra. The result does not imply global
vector convergence or arbitrary-phase norm-resolvent convergence.

These arguments retain the anchored lower boundary, fixed lattice spacing,
uniform component gap, positive physical alpha and absolutely summable
omitted interactions. They do not establish translation invariance or a
homogeneous Yang–Mills limit.

## F: conditional diffusion, differential identities and normalization

The actual model is the conditional fixed-exterior link space `SU(2)^3`.
Some accepted forward wording calls it “gauge-fixed”; no equivalence of that
conditional model to a gauge fixing of the original graph was proved. This
scope ambiguity was reported to the advisor and resolved in the source-bound
[conditional-space clarification](../advisor/f-conditional-space-clarification.md).
The formulas are valid for that conditional model. The earlier report bytes
remain available for reproducibility; their shorthand cannot support an
unproved equivalence to an unfixed graph.

The metric has S3 radius 2, or equivalently a factor 1/4 relative to the unit
S3 Laplacian. Hence a fundamental coordinate has eigenvalue 3/4. A smooth
strictly positive bounded density on the connected compact product manifold
gives the stated closed H1 form, self-adjoint weighted operator, H2 operator
domain and unique constant zero mode. Scaling it by a positive external
energy c changes all excitation energies and the clock but no static law.
At kappa=0 the explicit character autocorrelation proves nonidentifiability.

The review independently rederived the full Gamma and Laplacian identities
from the ambient S3 Laplace-Beltrami formula. The accompanying checker uses
exact polynomial arithmetic in 12 coordinates, imports no production code,
and reduces the difference from the claimed identities identically modulo
the three unit-sphere constraints. This checks the identity globally, beyond
the production quaternion fixtures. Exact isotropic Haar moments give
`E[S^2]=13/4` and `E[Gamma(S)]=45/16`, independently checking the metric
and action normalization.

The shared-middle `r=U dot W` term is required by the V derivative. The
unitary transform has potential `kappa*DeltaS/2+kappa^2*GammaS/4`;
the kinetic action on `exp(kappa*S/2)` cancels it with the stated signs.
The conditional extrema proof gives the attained action range `[-5,7]`:
the minimum is at V=I,U=W=-I and the maximum at all identities. The
derivative and squared tangent-majorant proofs of the lower endpoint are
both valid.

The Poincare comparison is correctly normalized: take the Haar mean as a
trial constant in the weighted variance, apply the Haar gap 3/4, then use
the density lower bound in the Dirichlet form. The density ratio is
`exp(12*abs(kappa))`, not its square. An independent outward rational
Taylor-tail bound proves `exp(3/2)<9/2`, hence the conditional `c/6`
bound on `abs(kappa)<=1/8`. This is a chosen finite reversible generator;
it has not supplied a physical value of c or a Yang–Mills Hamiltonian.
The autocorrelation slope formula requires a measured physical-time slope
and nonzero Dirichlet form; the available synthetic slope is only algebra.

## G: fixed-time dynamics and the representation

The bounded-difference Duhamel estimate is valid as a strong-operator
integral on the common domain and then by density. No operator-norm
differentiability of the unbounded generator is assumed. Applying it in
the finite and infinite spaces separately, joined by the exact central
evolution, gives `4||A||abs(t)*epsilon_M/hbar`. This proves convergence
uniformly on compact time intervals and an automorphism at each fixed t.
The implemented Hilbert-space unitary group is strongly continuous.

The SU(2) character shift is an actual bounded local operator whose
energy spacings grow without bound. At the stated sequence of times
tending to zero, its norm displacement is exactly 2 for the free reference.
A bounded perturbation changes that displacement by a vanishing amount.
The failure of point-norm continuity on the full local B algebra is
therefore real and retained. No finite propagation speed follows.

Both G2 proofs have been checked: finite products of
reference vacuum projections tend strongly to the global rank-one vacuum
projection; a commuting operator is scalar on its cyclic vacuum orbit.
This proves irreducibility of the declared full factor representation.
Every nonzero vector is then cyclic. The GNS map `[A] -> A Psi` is
isometric on its null quotient and onto by cyclicity; the canonical group
fixing the ground vector is implemented by `exp[it(H-e)/hbar]`. This
does not identify the Gauss-only algebra GNS with the full algebra GNS.

## H: continuous profile, exact variance and global state return

The independent checker verified the generic positive-q omitted
weight by exact coordinate enumeration at four rational q values and six
cutoffs. Both H1 reports correctly derive the rational-function identity,
strict monotonicity of the nonnegative series, and leading coefficient
`7/64` after multiplication by `(1-q)^3` as q tends to 1. The exact
default-amplitude root bracket denotes failure of this sufficient positive
certificate, not closure of the actual gap. The fixed-L and fixed-q limits
are correctly separated.

The external review proposed a stronger final-loop target before its
contract was frozen: disjoint completed factor supports have zero covariance
in the product reference, and each face overlaps at most 160 other supports
including itself. Therefore
`||V_q Omega||^2 <= (5/6)alpha^2*tau(q)^2/(1-q^2)^3`.
A uniform absolute budget forces `tau(q)=O((1-q)^3)`; with a uniform
positive excited threshold, the residual then bounds the global ground
projector distance by `||V_q Omega||/g_bar`. Both H2 derivations preserve
this conservative estimate and validate the following stronger exact identity.

Every omitted face has two actual free Haar links. The two z-links cover
non-xy faces; the two odd-y y-links cover odd-y xy faces; and the two
separator x-links cover even-y separator faces. Two distinct elementary
plaquettes share at most one edge. Hence at least one free link of f is
absent from g for f different from g. Integrating that link first proves
`<x_f x_g>=0`, irrespective of any other entangled strip factors. For
the diagonal, conditional Haar integration gives `<x_f^2>=1/4`.
The infinite series is absolutely summable at each q<1, so passage from
finite variance sums is justified. Thus

`sigma_q^2=||V_q Omega||^2=alpha^2 tau(q)^2 B(q^2)/96`.

The external checker independently tests the two-witness geometry on 1,872
omitted faces, with minimum witness count 2 and maximum pair intersection 1.
These fixtures audit the general geometric argument; they do not replace it.
Its canonical-ray calculations agree with ten forward and fifteen reverse
rows, checking five exact quantities per row after converting the reverse
physical scale `alpha/E_star=2` explicitly.

For the actual ground projection P_q, the excited **absolute** H_q spectrum
lies above `g_bar=alpha(1-eta)/8>0`. Since `H_q Omega=V_q Omega`,
inverting on `1-P_q` yields the projector bound. For energy, a different
projection is needed: `Q_Omega H_q Q_Omega>=g_bar Q_Omega`, so eliminating
that block in the ground equation gives `-sigma_q^2/g_bar<=e_q<=0`.
The overlap with Omega is nonzero because a ground orthogonal to it would
contradict the positive compression. Both reports distinguish these two
projections and avoid an unproved zero-mean premise in a perturbed remote
ground state.

On `tau(q)=eta/[8B(q)]`, the exact variance has leading coefficient
`alpha^2 eta^2/5376` times `(1-q)^3`. Therefore the bounds yield global
ground-projector convergence at order `(1-q)^(3/2)` and ground-energy
return at order `(1-q)^3`. Pure-state trace norm gives convergence for
all bounded observables in this representation. These are rates of upper
bounds, not measured asymptotic equality of the actual errors.

Meanwhile `||V_q||=alpha eta/8` on that ray. The lower norm bound comes
from normalized wavefunctions on finitely many full factors localized near
identity, followed by the absolutely bounded omitted tail. No delta-function
state or positive probability of infinitely many identity links is invoked.
This correctly separates nonvanishing perturbation norm from converging
ground projectors. It alone proves neither norm-resolvent convergence nor
its failure.

The endpoint is the selected-strip reference, retaining selected interactions;
the omitted local amplitudes vanish. The obstruction applies to retaining a
nonzero homogeneous omitted coupling **inside this global absolute-sum proof
method**. It does not disprove homogeneous lattice stability, retract any
separate inherited qualitative local-stability theorem, or decide continuum
Yang–Mills. No simultaneous arbitrary-phase boundary-vector convergence is
inferred from this fixed-representation q limit.

## Independence and limits of this review

The forward implementation reuses its own D1 geometry in E/G. The reverse
implementation has a separate omitted-class derivation and separate
incidence/union-find construction of clipped components, and G1 reuses that
reverse geometry. Neither inspected direction imports the other's current
implementation. D2 reverse also supplies a separate Riesz-contour bound;
F2 reverse supplies an algebraic tangent-majorant proof of the action range.
H2 reconstructs the externally proposed variance identity independently in
two producer implementations; the proposal and frozen contract were shared,
so this is not a blind discovery comparison.
The implementations nevertheless share the contracts, inherited mathematical
premises and standard theorem routes. They are not independent experimental
observations, and matching outputs cannot exclude a shared premise error.

The audit's additional exact script is distinct from both producer paths;
ordinary and optimized execution produced identical result bytes.
It verifies finite identities and arithmetic, not a proof-assistant formalization
of self-adjointness, infinite tensor products, spectral calculus or GNS theory.
The reviewer read the relevant A1/A2 and dressed-bridge arguments but did not independently
rederive every earlier sparse-block input, audit every historical loop or
perform an exhaustive literature-priority search. No human peer review or
formal proof certification has occurred. Model-specific derivations should
retain “novelty unverified”; standard resolvent, GNS, diffusion and Poincare
arguments should be labeled as established tools applied here.

Primary-source spot checks, accessed 2026-09-14: Teschl,
[Mathematical Methods in Quantum Mechanics](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf),
Theorem 6.4 and Lemma 6.5 for bounded perturbations and the second resolvent
identity; Ledoux, [The geometry of Markov diffusion generators](https://www.numdam.org/item/AFST_2000_6_9_2_305_0.pdf),
section 1.1 for reversible generators and invariant measures. These were
targeted passages, not full-book/article reviews. The official
[Jaffe–Witten problem statement](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf)
requires a nontrivial four-dimensional continuum quantum field theory with
the required axiomatic properties. None of these lattice or conditional
finite diffusion results establishes that conclusion.

To reproduce the final executable audit from the repository root, use a new
scratch directory outside the repository:

```bash
python -B research/round20/external-audit/replay_audit.py --output /tmp/ym20-external-audit-new --evidence /tmp/ym20-external-audit-evidence-new.json
```

The saved [audit evidence](audit-evidence.json) binds this report, both audit
scripts, independent results, all ten accepted gates and the conditional-space
clarification. It includes the forty replay records and exact H2 comparison.
Presentation files and mutable site data are intentionally outside this
mathematical evidence inventory.
