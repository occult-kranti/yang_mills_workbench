# AJ2 forward: an actual nonzero homogeneous Wilson fluctuation

**Independent forward conclusion, pending review:** throughout the inherited
symbolic I1/AJ1 coupling regime, the specified elementary xz Wilson observable
has strictly positive variance in the actual homogeneous state. Its centered
vector is a nonzero physical vector orthogonal to the ground. Its connected
imaginary-time correlation satisfies

\[
 0<C(t)\le v\exp\!\left(-\frac{\alpha t}{16\hbar}\right),
 \qquad 0\le t<\infty,\qquad
 v=\omega(W^2)-\omega(W)^2>0.                            \tag{1}
\]

The value `v` is not evaluated. The key new proof uses a Haar-null level-set
property of the **actual original-link multiplier**, followed by AJ1's
locally normal density. It does not assume that the density is faithful or
equals a reference state. Equation (1) uses only the bounded spectral
semigroup; it requires no energy moment or domain membership of the vector.

This is investigation 8, AJ loop 2. The frozen contract is
`0f71cc35d4e6fef93188cee740f9cdf90596f034193f3c9aee9455fb0411c154`.
The input pack was frozen before science as
`a8fbbe82d129b9108bf12b4920d0ead9e4cec3dc17761f4d271e9e4a457fcc5c`;
the advisor explicitly released production after standard input preflight.
The prospective level-set strategy was shared in the contract and advisor
selection. The proof and checker here were written independently, with no
current opposite or skeptic AJ2 science read. Historical methods guide
scrutiny; they supply no physical coefficients or historical endorsement.

## 1. The exact inherited model and the chosen operator

Keep the actual I1 nonsummable **homogeneous omitted interaction** in the
positive coarse orthant, the specified whole-star empty-boundary limit, and
fixed selected-strip coefficients satisfying
`|lambda_L|,|lambda_R|<=alpha/2`, `|mu|<=alpha/8`. The original positive
link with tail `a` is owned by

\[
 b(a)=(\lfloor a_x/4\rfloor,\lfloor a_y/2\rfloor,a_z).
                                                               \tag{2}
\]

Every coarse site owns all 24 outgoing Haar link factors: ten selected-strip
links and fourteen free links. Both endpoint actions remain, including
heads outside a tail-owned block. This is factorization of the unreduced
link space, not a presumed factorization of the physical subspace. The
onsite reference is
`h_b=(H_strip,b-E_strip,b+alpha sum_free C_e)/(alpha/8)`.
Each retained `b+S`, `S={0,e_x,e_y,e_z}`, carries all 21 omitted anchored
faces and has interaction norm `M=7|tau|`. The global interaction is not
replaced by a bounded summable operator.

The only actual-state coupling assumption is

\[
 |\tau|<\tau_*:=\frac{\min\{c_1(S),1/(2c_2(S))\}}7,       \tag{3}
\]

with unevaluated positive source constants. Zero and either sign of the
omitted coupling are covered. No chosen positive numerical `tau` follows.
The scales `alpha,hbar,E_star,a` remain fixed and positive.

Inherit precisely the admitted I1/AJ1 state `omega` on the full bounded
quasilocal factor algebra, its local positive trace-class densities, normal
represented local factors, and the physical algebra
`A_phys=closure_norm{bounded local operators invariant under every local
endpoint gauge transformation}`. AJ1 proves that
`H_cyc=closure pi(A_phys)Omega` equals the joint gauge-fixed space and
reduces the actual centered generator. Its physical restriction

\[
 H_{\rm phys}=\frac\alpha8G_{\rm phys},\quad
 \ker H_{\rm phys}=\mathbb C\Omega,\quad
 \operatorname{spec}(H_{\rm phys})\subset
                 \{0\}\cup[\Delta,\infty),\quad
 \Delta=\alpha/16                                       \tag{4}
\]

is inherited. The AJ1 gate and post-review include the source-correct
tested-resolvent topology, domain-qualified creation core and the
local-normality justification of spectator-product vector density. Those
admitted results are not re-proved by the finite diagnostics here.

Let `e_x=(1,0,0)` and `e_z=(0,0,1)` now denote original unit steps. The
ordered xz loop is
`0 -> e_x -> e_x+e_z -> e_z -> 0`, with

\[
 U_\partial=U_x(0)U_z(e_x)U_x(e_z)^{-1}U_z(0)^{-1},
 \qquad W=\tfrac12\operatorname{Tr}(U_\partial).           \tag{5}
\]

The four original links are distinct:

| Positive canonical link | Orientation in (5) | Coarse owner |
|---|---:|---|
| `U_x(0)` | `+1` | `(0,0,0)` |
| `U_z(e_x)` | `+1` | `(0,0,0)` |
| `U_x(e_z)` | `-1` | `(0,0,1)` |
| `U_z(0)` | `-1` | `(0,0,0)` |

The minimal complete coarse-factor region is therefore
`R={(0,0,0),(0,0,1)}`, containing 48 original links. Its tails are
`x=0,...,3`, `y=0,1`, `z=0,1`; all three positive directions are owned
at each tail. Its 36 endpoints are the disjoint union of those 16 tails,
four added x-heads `(4,y,z)`, eight added y-heads `(x,2,z)`, and eight
added z-heads `(x,y,2)`. The four loop vertices alone omit 32 endpoint
groups relevant to arbitrary operators on the complete local factor.
The full lists, not just these counts, appear in the output.

Under the original action `U_(v,w) -> g_v U_(v,w)g_w^-1`, the four
factors telescope to `g_0 U_partial g_0^-1`. Thus the trace is invariant
under every endpoint transformation. All other endpoint actions on `R`
act trivially on this particular multiplier. Each SU(2) matrix has real
trace in `[-2,2]`, so `W` is a real bounded self-adjoint multiplication
operator. Section 2 proves that its norm is exactly one. It is an actual
omitted xz face; its containing Hamiltonian anchor group uses the whole
four-site star, while the observable's minimal factor region has two
sites. These are distinct support statements.

## 2. Haar-null levels on the actual full configuration space

Work first on the original local Hilbert space
`K_R=L2(X,mu_H)`, where `X=SU(2)^48` and `mu_H` is the normalized product
Haar measure. This is the underlying multiplication representation, not
the actual interacting probability law of `W`.

Condition on all original link matrices except the single actual link
`u=U_z(0)`. Equation (5) becomes

\[
 U_\partial=A u^{-1},\qquad
 A=U_x(0)U_z(e_x)U_x(e_z)^{-1}\in SU(2).                  \tag{6}
\]

For every fixed choice of the other 47 matrices, inversion and left
multiplication preserve normalized Haar measure. Thus `A u^-1` is Haar
when this one original link is integrated. This conditional calculation
uses independent original link coordinates, never independent plaquette
variables. The 44 links outside the loop are genuine spectators, each
with normalized Haar mass one.

For explicit normalization, write a unit quaternion as
`q=cos(theta)+sin(theta)n`, `0<=theta<=pi`, with `n` uniform on `S^2`.
Normalized SU(2) Haar measure is uniform measure on `S^3`: left quaternion
multiplication is orthogonal and transitive, so normalized surface measure
is the Haar measure. In these coordinates its marginal angular measure is
`(2/pi)sin^2(theta)dtheta`; its integral is one. The scalar component
`x=cos(theta)=Tr(q)/2` therefore has probability measure

\[
 d\nu_H(x)=\frac2\pi\sqrt{1-x^2}\,1_{[-1,1]}(x)\,dx.
                                                               \tag{7}
\]

Indeed `dx=-sin(theta)dtheta` and
`integral_(-1)^1 sqrt(1-x^2) dx=pi/2`. In particular every singleton
has zero measure. At `x=+1` and `x=-1` the angular poles have zero
surface measure; at `x=0` the equatorial level also has zero measure.
Outside `[-1,1]` the level is empty. There is no exceptional zero or
endpoint atom hidden in the change of variables.

Conditional integration in (6) and Fubini/Tonelli now give, for every
Borel set `B` and every real `c`,

\[
 \mu_H\{W\in B\}=\nu_H(B),\qquad
 \mu_H\{W=c\}=0.                                      \tag{8}
\]

For the original local multiplication operator its spectral projection is

\[
 E_W(B)=M_{1_{\{W\in B\}}}.
                                                               \tag{9}
\]

Consequently `E_W(B)=0` **if and only if** `nu_H(B)=0`, and in
particular `E_W({c})=0` for every real `c`. If `nu_H(B)>0`, the indicator
of its preimage is a nonzero vector, so the converse in this statement
also holds on the full local Hilbert space. Every open subinterval meeting
`(-1,1)` has positive measure. Hence the multiplication spectrum is
`[-1,1]`, with norm one and no point eigenprojection, including at its
spectral endpoints. These are operator statements under the original
measure. A particular normal state may give additional sets zero weight;
state faithfulness is not being inferred.

## 3. Strict variance in the actual normal homogeneous state

AJ1 supplies a positive trace-class local density `rho_R` with trace one
such that `omega(A)=Tr(rho_R A)` for every bounded local `A` in this
complete factor. Write its spectral decomposition as
`rho_R=sum_j p_j |psi_j><psi_j|`, with `p_j>=0` and `sum p_j=1`.
Tonelli gives an integrable nonnegative function

\[
 r(q)=\sum_jp_j|\psi_j(q)|^2,\qquad
 \int_Xr(q)\,d\mu_H(q)=1.                              \tag{10}
\]

For bounded multiplication functions their expectation is integration
against this density. This construction does not assume a pointwise
diagonal kernel for an arbitrary trace-class operator. The state may
be rank one, `r` may vanish on large sets, and no full-support or
faithfulness assertion is required.

Let `m=omega(W)` and `v=omega(W^2)-m^2`. Self-adjointness makes `m`
real; boundedness makes both moments finite. Directly from (10),

\[
 v=\int_X(W(q)-m)^2r(q)\,d\mu_H(q)\ge0.                 \tag{11}
\]

If it were zero, the nonnegative integrand would vanish almost everywhere.
Thus `r` could have weight only on `{W=m}`. That set has Haar measure
zero by (8), which would force `integral r=0`, contradicting (10).
Therefore `v>0`. Equivalently,
`v=||(W-m)rho_R^(1/2)||_HS^2`; zero would force the range of the
nonzero `rho_R^(1/2)` into the zero kernel of `W-m`.

This proves positivity separately for each actual state throughout (3),
without a smaller perturbative radius. It gives no uniform positive
variance margin over all normal states, no numerical value in the
interacting state, and no identification of its moment law with (7).
Normality of the represented local factor is also available from AJ1;
it preserves the local spectral projections under representation. The
density argument above is already sufficient for the variance claim.

Let

\[
 \chi=(\pi(W)-m)\Omega.                                \tag{12}
\]

The operator `W-mI` belongs to the full bounded local physical algebra,
so `chi in H_cyc`. It obeys
`<Omega,chi>=0` and `||chi||^2=v>0`. On the physical null quotient
`N_phys={A:omega(A^*A)=0}`, the class `[W-mI]` is therefore nonzero.
The inherited isometry `[A] -> pi(A)Omega` identifies it with precisely
this physical vector. In particular the physical cyclic space contains
both the vacuum and a nonzero orthogonal vector. This is the nonvacuity
conclusion that the AJ1 gap inequality alone did not establish.

## 4. The positive imaginary-time spectral consequence

Use the spectral resolution of the **actual** self-adjoint centered
restriction (4), and define

\[
 \nu_\chi(B)=\langle\chi,E_{H_{\rm phys}}(B)\chi\rangle.
                                                               \tag{13}
\]

It is a finite positive measure with total mass `v`. Uniqueness of the
ground and (12) give `nu_chi({0})=0`; (4) excludes `(0,Delta)`.
Thus this nonzero measure is supported in `[Delta,infinity)`.

For all real finite `t>=0`, the bounded positive contraction
`exp(-t H_phys/hbar)` is defined on every Hilbert vector. Its spectral
formula gives the connected imaginary-time correlation

\[
 C(t)=\langle\chi,e^{-tH_{\rm phys}/\hbar}\chi\rangle
     =\int_{[\Delta,\infty)}e^{-tE/\hbar}\,d\nu_\chi(E).
                                                               \tag{14}
\]

The scalar kernel is strictly positive at every finite energy for each
finite `t`. The integral of a strictly positive measurable function
against a nonzero positive finite measure is strictly positive. For
example, its positive level sets form a countable cover of the measure
space, so an integral of zero would force the total measure to be zero.
There is no spectral mass at an added point called infinite energy.
This proves the strict lower inequality `C(t)>0`, including `C(0)=v`.
It does not evaluate a lower decay coefficient or rate.

On the actual spectral support,
`exp(-tE/hbar)<=exp(-tDelta/hbar)`, which gives exactly (1).
The physical factor is `Delta/hbar=alpha/(16hbar)`, not the normalized
source gap `1/2` inserted as a frequency. Bounded dominated convergence
also gives continuity at zero, with no differentiability assertion.
The upper bound tends to zero at large imaginary time.

The centering in (12) is essential. Since the semigroup fixes the vacuum,
the corresponding uncentered expression is

\[
 \langle\pi(W)\Omega,e^{-tH_{\rm phys}/\hbar}\pi(W)\Omega\rangle
      =m^2+C(t).                                       \tag{15}
\]

No unproved condition `m=0` is imposed on the actual state.

The lower support bound does not identify the infimum of the overlap
support, an atom at `alpha/16`, or an eigenvector there. In particular it
does not show that the upper exponential in (1) is sharp. No real-time
magnitude-decay theorem, lower exponential decay estimate, measured mass,
or threshold eigenvalue is inferred. A nonzero positive excited spectral
measure has now been established; its precise energies and weights have
not been determined.

Neither (13) nor (14) requires `chi in D(H_phys)` or in its form domain.
Those conditions would respectively require finite second or first
energy moments of (13), which have not been estimated here. Bounded
locality alone is not such a premise. The bounded-semigroup proof does
not differentiate at `t=0` and does not reopen an energy-moment goal.

## 5. Discriminating controls and what they test

All countermodels below are explicitly distinguished from the actual
homogeneous ground state. They test the inference, not the source theorem.

**Constant and step multipliers.** A constant `cI` has zero variance in
every state. Nonconstancy alone is also insufficient: multiplication by
`1_[1/2,1]` on `L2([0,1])` has positive-measure levels, and the normal
rank-one state of `sqrt(2)1_[0,1/2)` has variance zero. The exact
two-point diagnostic `diag(0,1)` with density `diag(1,0)` reproduces that
failure. What rules it out in Section 3 is specifically the null level
set, not mere nonconstancy.

**Normality without faithfulness.** On the original local Haar space the
normalized constant vector defines a normal rank-one density. It is
nonfaithful on the full infinite-dimensional `B(K_R)`. Nevertheless its
conditional moments for (5) are `0` and `1/4`, so its variance is positive.
These are reference diagnostics: the scalar of a uniform unit quaternion
has mean zero and component second moment `1/4`, because the four equal
component second moments sum to one. The fundamental character `2W`
therefore has second moment one. No actual interacting moment is assigned
these values. Rank-one normality is fully compatible with Section 3.

**Small normal variances and singular concentration.** As a control on
claims about *all normal states*, take the actual local event
`A_epsilon={|W|<epsilon}`, `0<epsilon<1`. Its original Haar measure is
positive by (7). The normalized indicator
`psi_epsilon=1_Aepsilon/sqrt(mu_H(A_epsilon))` defines a normal,
nonfaithful vector state, gauge invariant on this local factor. Symmetry
of (7) gives mean zero, while its non-atomic law gives positive variance
at most `epsilon^2`. Thus these variances can be arbitrarily small;
there is no uniform positive lower margin from normality alone. These
states are not claimed to be the actual ground for any parameter, and
no energy estimate on them is made.

At `epsilon=1/4` this normal-state variance is at most `1/16`, which
already discriminates against replacing every normal-state variance by
the Haar value `1/4`. As `epsilon -> 0`, a weak-star cluster state on
`B(K_R)` exists by compactness of the state space. It takes `W` and
`W^2` to zero and `I` to one. It cannot be normal by Section 3. This
shows why a singular state can have a zero-variance functional despite
the original point spectral projection `E_W({0})` being zero: singular
GNS representation does not preserve the needed Borel spectral calculus.
No sequential convergence of the entire normal-state family is asserted;
the argument uses a cluster subnet. Exact rational epsilon prefixes audit
the vanishing upper bounds, not the infinite weak-star construction.

**Gap exclusion versus a nonzero measure.** The self-adjoint two-level
model `diag(0,Delta)` restricted to its vacuum has a positive exclusion
threshold and no nonzero excited vector. It is the AJ1-only logical
possibility. Section 3 now eliminates it for the actual model by producing
`chi`, rather than by strengthening the gap number.

**Upper versus lower decay and a threshold eigenvalue.** An abstract
unit-mass spectral atom at energy `k Delta`, `k=2,3,8`, obeys the gap
bound but has no atom at `Delta`. At dimensionless imaginary time
`s=Delta t/hbar=log(2)`, its heat correlation is exactly `2^-k`, strictly
less than the gap ceiling `1/2`. Thus the same ceiling is not a lower
bound, and the lower support estimate does not determine the overlap
infimum. An abstract uniform measure on `[Delta,2Delta]` has support
endpoint `Delta` and zero atom there, so even identification of a support
endpoint would not itself prove an eigenatom. These probability measures
are admissible spectral-measure controls, not computed physical spectra.

**Real time and centering.** A single positive-energy atom has real-time
correlation of constant modulus. For energy `2Delta` and real
`s=Delta t/hbar=pi/4`, the phase is exactly `-i`; its modulus is one,
and at every real time it remains one. Separately, in the abstract
two-dimensional model with `Omega=e_0`, `H=diag(0,2Delta)` and
`W=(1/2)[[1,1],[1,1]]`, the mean is `1/2` and variance `1/4`.
At imaginary `s=log(2)`, centered heat is `1/16` whereas uncentered
heat is `5/16`. Its nondecaying vacuum component even violates the
naive uncentered norm-squared gap ceiling `1/4`. The checker retains
this exact distinction.

**Unproved domain membership.** Add a zero vacuum `e_0` to a Hilbert
space with `H e_n=n Delta e_n`, `n>=1`, and let
`xi=sum_(n>=1)n^-1 e_n`. This vector is orthogonal to the vacuum and has
finite squared norm `sum n^-2<2`. Its form moment has the divergent
harmonic series, and its operator-norm-squared energy moment has the
divergent series `sum 1`. The bounded self-adjoint rank-two operator
`|xi><e_0|+|e_0><xi|` creates it from the vacuum. Rescaling that operator
can make it a contraction without curing either divergence. This
abstract bounded-observable control rejects automatic domain membership;
it does not compute or assert divergence of any moment for the actual
Wilson vector. Its bounded positive semigroup correlation is still
well-defined. The finite exact prefixes and the dyadic harmonic-series
argument separate bounded vector norm from the required domains.

## 6. Exact implementation, sources and scope

The fresh standard-library checker independently walks (5), canonicalizes
the signed links, reconstructs their owners, and lists all 48 complete
links and all 36 endpoint vertices. Rational unit quaternions test the
original closed word and both endpoint actions. In the first tested
assignment the Wilson value is `12/17` before and after complete gauge
transformation; suppressing the head actions instead gives `10272/18785`.
The first candidate discriminates, so there is no hidden blind attempt.
A central transformation flips an open fundamental link but preserves
the closed trace. All attempted missing-head diagnostics are retained in
the output; none is overwritten if an attempt is blind.

The conditional dependence on the actual `U_z(0)` is also checked
algebraically: its four rational quaternion coefficients have squared
sum one. The exact fundamental reference identities then give mean zero,
second moment `1/4`, and character second moment one. This is not
Monte Carlo, a discretized group, independent plaquette coordinates,
or a numerical proof of Haar-null level sets. The analytic conditional
integration in Section 2 proves those sets are null. The actual-state
and infinite-volume conclusions use Sections 3–4 and the admitted
sources, not finite sampling.

The first diagnostic run passed with no failed or nondiscriminating
scientific attempt. The same unchanged checker is used for final fresh
normal and optimized replays; their exact commands and observed hashes
are recorded in `validation.json`. Explicit exceptions, not removable
`assert` statements, implement every check. From the repository root:

```bash
python -B research/round28/forward/aj2/check.py --output /tmp/ym28-forward-aj2-normal
python -B -O research/round28/forward/aj2/check.py --output /tmp/ym28-forward-aj2-optimized
```

Both output directories must be absolute and nonexistent. Runtime content
reads use only owned repository snapshots, the local manifest and the
checker itself. Installed resource locators and original repository paths
are provenance metadata; preflight verified the originals. The result's
`bindings` is one flat repository-relative hash map for the checker,
contract, all declared and actually consulted source originals, manifest
and all owned input snapshots. No historical checker is executed as the
new algorithm. The final producer freeze binds every owned file except
its own exact top-level `freeze.json`, including both nested historical
AJ1 source files named `freeze.json`.

The immutable 36-page seven-loop draft and network were read as current
project knowledge: all changed draft passages and five added network
nodes/eight edges were read, while unchanged passages reuse their earlier
full reading. AJ1's complete reports and admitted spectator-density
clarification are controlling premises. J1/J2's explicit dyadic
variance, numerical coupling and summable representation are context,
not transferred constants. The input reading record separates complete
proof readings, unchanged instruction reuse and large-JSON structural
inspection from any claimed full independent revalidation.

The contribution is an explicit qualitative nonzero original Wilson
vector and its positive imaginary-time spectral consequence in this
workbench's actual homogeneous model. The analytic tools are standard;
scientific priority is unverified. No uniform positive variance margin,
numerical stability constant, energy moment, global faithfulness,
alternative boundary-state equality, real-time decay or continuum/model
matching is claimed. No fifth-goal investigation was selected or executed.
