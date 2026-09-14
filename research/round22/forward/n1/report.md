# N1 forward: stationary local comparison in the canonical summable model

The frozen proposed bound is valid for all real physical times and the stated
bounded complex local gauge-invariant observables. The resulting sufficient
growing-window range is `0 <= gamma < 3`. Its endpoint is unresolved. This is
an independent forward derivation, completed before reading any current N1
reverse or skeptic solution. It does not select or execute N2.

## Fixed premises and scope

The model is the M1/M2 canonical summable full-link SU(2) Hamiltonian in the
selected-strip/free incomplete tensor product on the nonnegative cubic orthant.
Use exactly the inherited partition and representation, with reference ground
Omega, `H_0=H_ref >= 0`, `H_0 Omega=0`, and normalized perturbed ground Psi_q.
Spacing, `E_star > 0`, `alpha/E_star > 0`, `hbar > 0`, and `0 < eta < 1` stay
fixed. The action-profile parameters q, eta and tau are dimensionless; q lies
strictly in `(0,1)`. For the profile-generating function, distinct from the
observable B,

\[
\mathcal B(q)=\frac{2+5q+5q^2+6q^3+3q^4}
 {24(1-q)^3(1+q)^2(1+q^2)},\quad
\tau_q=\frac{\eta}{8\mathcal B(q)},\quad
V_q=-\alpha\tau_q\sum_{f\in O}\frac{q^{|a_f|_1}}{24}x_f,
\quad x_f=\tfrac12\operatorname{Tr}U_f.
\tag{1}
\]

Here O is the exact inherited omitted-face set. Each x_f is a bounded
self-adjoint multiplication operator of norm at most one. Absolute summability
gives norm convergence of V_q. Thus `H_q=H_0+V_q` is self-adjoint on precisely
`D(H_0)`. The admitted M1/M2 quantities are

\[
H_q\Psi_q=e_q\Psi_q,\quad
\bar g=\alpha(1-\eta)/8,\quad
\sigma_q^2=\alpha^2\tau_q^2\mathcal B(q^2)/96,
\quad d_q=\|P_q-P_0\|\le\sigma_q/\bar g,
\quad -\sigma_q^2/\bar g\le e_q\le0.
\tag{2}
\]

Alpha, e_q, sigma_q and gbar are energies. hbar has energy-times-time units.
The following argument uses the admitted stationary physical ground and the
same gauge-invariant reducing sector; it introduces no changed generator or
homogeneous representation. A and B are fixed bounded complex local
gauge-invariant operators. No domain-preservation assumption on either is
made. Their complete finite reference-factor covers are fixed before q tends
to one. The q=1 coefficient series itself is outside the model.

## Stationarity removes the scalar phase legitimately

Let `U_j(t)=exp(-it H_j/hbar)` and
`beta_j^t(X)=U_j(t) X U_j(-t)`. This choice of sign matches the correlation
in the contract; it is the negative-time Heisenberg convention. Since
`U_q(-t) Psi_q=exp(it e_q/hbar) Psi_q`,

\[
\beta_q^t(B)\Psi_q
=e^{it e_q/\hbar}U_q(t)B\Psi_q
=e^{-it(H_q-e_q)/\hbar}B\Psi_q.
\]

Consequently, with the inner product linear in its second entry,

\[
C_q(t)=\omega_q(A^*\beta_q^t(B))
       -\omega_q(A^*)\omega_q(B),\qquad
\omega_q(A^*)=\overline{\omega_q(A)}.
\tag{3}
\]

Equation (3) uses stationarity, not an omission of e_q from the original
matrix element. Conjugation by `H_q-e_q` equals conjugation by H_q because
the two scalar phases cancel. Independent scalar shifts of A or B leave
(3) unchanged: `omega_q(beta_q^t(B))=omega_q(B)`, while conjugation fixes
the identity. A=B=I gives exactly zero. These identities hold for every
real t, including negative t and zero.

## A strong integral that never differentiates an arbitrary observable

Fix q. For a general bounded self-adjoint V=V_q with H=H_0+V, define

\[
W(s)=U_q(s)U_0(-s).
\]

First take a vector in the common dense domain D(H_0)=D(H_q). Each of its
unitary orbits stays in that common domain. The product difference quotient,
using the generators on this vector only, gives

\[
W'(s)\psi=-\frac{i}{\hbar}U_q(s)V U_0(-s)\psi.
\]

The cancellation uses H_q-H_0=V on the common domain; neither A nor B appears.
Integrating and extending by density yields, on every Hilbert-space vector,

\[
W(s)=I-\frac{i}{\hbar}\int_0^s U_q(r)V U_0(-r)\,dr.
\tag{4}
\]

The integral is defined vectorwise in Hilbert norm. Its integrand is strongly
continuous and bounded by `||V||`, so it defines a bounded operator of norm
at most `|s| ||V||/hbar`. Therefore (4) proves that W is strongly C1 on
every vector, with the displayed bounded strongly continuous derivative.
The adjoint product has the analogous strong derivative
`(W(s)^*)'=i U_0(s)V U_q(-s)/hbar`. Both derivatives have uniform norm bound
`||V||/hbar`. In particular, strong product differentiation with any fixed
bounded operator between W and W* is legitimate. This conclusion does not
require operator-norm continuity of the conjugated perturbation.

Now fix a real terminal time t and the bounded operator `B_t=beta_0^t(B)`.
Keep B_t fixed while differentiating only W and W*. By the strong product
rule,

\[
\frac{d}{ds}\{W(s)B_tW(s)^*\}
=-\frac{i}{\hbar}U_q(s)
 [V,\beta_0^{t-s}(B)]U_q(-s).
\]

For completeness, the product rule follows by splitting its difference
quotient into the two W differences and using their uniform boundedness;
a strongly convergent bounded family can be applied to a norm-convergent
vector. Thus it also applies when B sends domain vectors outside the domain.
At s=0 the product is beta_0^t(B); at s=t it is beta_q^t(B). Integration gives
the bounded-operator identity in the strong sense

\[
\boxed{\beta_q^t(B)-\beta_0^t(B)
=-\frac{i}{\hbar}\int_0^t
 U_q(s)[V_q,\beta_0^{t-s}(B)]U_q(-s)\,ds.}
\tag{5}
\]

The integrand is strongly continuous. For t<0 the integral has its usual
orientation. Applying (5) to every unit vector and using a uniform integrand
bound proves its operator-norm inequality; an operator-norm Bochner integral
is neither claimed nor needed. This is the domain-safe step absent from a
formal differentiation of `U_q(s) beta_0^{t-s}(B) U_q(-s)` through H_0 B.

## Complete support holds for every reference time

A strip anchored at `(4i,2j,z)` owns the six x-links with tails x equal to
`4i,4i+1,4i+2` and y equal to `2j,2j+1`, and the four y-links at x equal to
`4i,...,4i+3`, y=`2j`. Every z-link, odd-row y-link, and x-link whose tail
x is 3 modulo 4 is a free one-link factor. The selected xy faces have even
y and x residue 0, 1 or 2 modulo 4; every other face is omitted.

For the complete finite factor set F_B, let E(F_B) be all of its links.
Grouping the nonnegative reference sum gives
`H_0=H_F tensor I+I tensor H_complement`. In the product spectral
representation its exponential factorizes. Hence

\[
\beta_0^r(B)=
 (e^{-irH_F/\hbar}B_F e^{irH_F/\hbar})\otimes I
\]

for every real r; it has the same complete factor cover and norm ||B||.
This identity is valid for arbitrary bounded B_F. Define the finite set

\[
\mathcal I_F=\{f\in O:\operatorname{links}(f)\cap E(F_B)\ne\varnothing\},
\qquad D_F(q)=\sum_{f\in\mathcal I_F}q^{|a_f|_1}/24.
\tag{6}
\]

Each link can be on two faces per transverse axis, with the backward anchor
excluded on the boundary. Thus it meets at most four faces. Deduplicating
faces gives `m_F=|I_F| <=4|E(F_B)|` and `D_F(q)<=|E(F_B)|/6`.
Every omitted x_f outside I_F acts only on factors disjoint from F_B and
commutes with every beta_0^r(B). Taking the commutator of the norm-convergent
series (1) consequently leaves exactly the finite intersecting sum. Therefore

\[
\|[V_q,\beta_0^r(B)]\|
\le2\alpha\tau_q\|B\|D_F(q),\qquad r\in\mathbb R.
\]

Substitution into (5), followed by the supremum over unit vectors, proves

\[
\boxed{\|\beta_q^t(B)-\beta_0^t(B)\|
\le\frac{2\alpha\tau_q|t|}{\hbar}\|B\|D_F(q).}
\tag{7}
\]

There is no support assertion about the *perturbed* evolution in this step.
The unitary conjugations outside the commutator preserve its norm. It is the
reference evolution inside the commutator that must retain the full support.

## State distance and both mean products

The two rank-one projections have difference with nonzero eigenvalues
`+d_q,-d_q`, giving `||P_q-P_0||_1=2d_q`. Trace duality therefore gives
`|omega_q(X)-omega_0(X)|<=2d_q||X||` for complex bounded X. Apply this first
to `X=A* beta_q^t(B)`. Changing the state in the raw expectation costs
`2d_q||A||||B||`. Then (7) changes the dynamics in the reference expectation
at cost `||A|| ||beta_q^t(B)-beta_0^t(B)||`. Finally split the mean product:

\[
\omega_q(A^*)\omega_q(B)-\omega_0(A^*)\omega_0(B)
=[\omega_q(A^*)-\omega_0(A^*)]\omega_q(B)
+\omega_0(A^*)[\omega_q(B)-\omega_0(B)].
\]

Each term costs `2d_q||A||||B||`. Together with (7), this proves precisely
the frozen target:

\[
\boxed{|C_q(t)-C_0(t)|\le\|A\|\|B\|
 \left[6d_q+\frac{2\alpha\tau_q|t|}{\hbar}D_F(q)\right].}
\tag{8}
\]

Coefficient six is sufficient; no optimality is claimed. The bounds on e_q
and the vacuum residual sigma_q remain valid inherited facts. Their
time-dependent costs are not needed in (8); sigma_q still bounds d_q.

## Growing windows, explicit constants, and the endpoint

Put epsilon=1-q. Direct substitution in the exact rational profile yields

\[
\epsilon^3\mathcal B(q)\to7/64,\quad
\tau_q/\epsilon^3\to8\eta/7,\quad
\frac{\sigma_q^2}{\alpha^2\epsilon^3}\to\eta^2/5376,
\quad
\frac{\sigma_q/\bar g}{\epsilon^{3/2}}
\to\frac{\eta}{(1-\eta)\sqrt{84}}.
\tag{9}
\]

The support sum is a finite polynomial: `D_F(q)->D_F(1)=m_F/24`.
For fixed dimensionless C>0 and exponent gamma>=0, the window
`T_q=(hbar/alpha) C epsilon^(-gamma)` is an observation protocol; it is
neither an action deformation nor a fitted physical clock. Equations (8)-(9)
give the explicit sufficient certificate

\[
\frac{\sup_{|t|\le T_q}|C_q(t)-C_0(t)|}{\|A\|\|B\|}
\le 6\sigma_q/\bar g+2C\tau_q\epsilon^{-\gamma}D_F(q),
\tag{10}
\]

where (10) is read without division when an observable is zero. Its two
terms have the respective asymptotics

\[
\frac{6\eta}{(1-\eta)\sqrt{84}}\epsilon^{3/2}(1+o(1)),
\qquad
\frac{2\eta C m_F}{21}\epsilon^{3-\gamma}(1+o(1))
\tag{11}
\]

when m_F>0; if m_F=0 the second term is identically zero. Thus for all
`0<=gamma<3` there is uniform correlation convergence, with sufficient rate
`O(epsilon^min(3/2,3-gamma))`. In particular gamma=3/2 is now included.
For `gamma<3/2` the state term dominates the certificate; at `gamma=3/2`
both displayed constants add; for `3/2<gamma<3` the dynamical term dominates.

At gamma=3 and m_F>0 the right side of (10) tends to the strictly positive
constant `2 eta C m_F/21`; for gamma>3 it diverges. This is failure of this
vanishing-error certificate, not a lower bound on the actual difference.
The actual difference is bounded, and may vanish even when this estimate
does not. For example constant observables have identically zero connected
correlations and may be assigned an unnecessarily large cover with m_F>0.
This exact exception directly rejects an inference from a positive upper
bound to nonconvergence. The actual nonconstant endpoint requires another
argument and remains the next missing premise; N2 is not preselected here.

## Executed checks and failure controls

`check.py` is an independent standard-library implementation. It uses exact
Fractions and exact Gaussian-rational matrices, with a rational alternating
Taylor enclosure only for the sine control. It checks the rational profile
identity and constants; reconstructs factor closure and face incidence;
and executes complex centering, independent scalar shifts, missing
conjugation, missed mean factor, omitted ground-phase, commutator coefficient,
domain, and endpoint controls. Finite matrices are algebraic controls, not
physical replacements for the lattice or proofs of the infinite theorem.

The domain control is analytic: on ell2(N), `H e_n=n e_n` and
`v=sum_n n^(-1)e_n` give a bounded rank-one `B=|v><e_1|`, with
`||v||^2<=2`, but `B e_1=v` is outside D(H), since every term of
`sum_n n^2 |v_n|^2` equals one. Exact partial sums corroborate this
counterexample; the infinite conclusion follows from that displayed series.
Teschl's Theorem 5.1 makes the failed derivative consequence explicit.

The full-support control closes the origin xz loop's four displayed links to
22 complete-factor links. The omitted xz face anchored at `(2,1,0)` meets
that closure but no displayed link. A two-qubit entangled-factor fixture
also shows actual support spreading inside a reference factor: conjugation
of X tensor I by `exp(-it Z tensor Z)` at t=pi/4 gives Y tensor Z, whose
commutator with I tensor X is nonzero although the initial commutator is zero.
The abstract fixture is only a rejection of the edge-support inference;
the actual lattice bound is proved by (6).

The scalar-phase failure uses a stationary two-level model with energies
3 and 4 at t=pi/2, hbar=1: retaining the unshifted unitary in a constant
correlation gives i-1 instead of zero. Correct Heisenberg conjugation and
the ground-subtracted unitary give the same complex covariance. Both signs
of time are checked exactly. The factor-two control uses V=Z, B=X, H_0=0,
so the dynamic difference is `2|sin t|`; at t=1/2 a certified sine lower
bound disproves a coefficient-one commutator estimate.

The source manifest binds the executed code, this report, primary-source
record, frozen contract and instruction snapshots, consulted inherited
reports/gates, and every generated scientific output. Normal and optimized
Python execute into different fresh directories. Explicit exceptions guard
every check; neither asserts nor current other-producer imports are used.
These are repeat validations of one research loop.

```bash
python3 -B research/round22/forward/n1/check.py --output /absolute/new/n1-forward
python3 -B -O research/round22/forward/n1/check.py --output /absolute/new/n1-forward-optimized
```

## Attribution and remaining limits

The primary-source reading record is in `source-notes.md`. Teschl's checked
Theorems 4.14, 5.1 and 6.4 supply established tensor, unitary and bounded
perturbation tools; the report supplies the strong interpolation identity
and its canonical-profile application. This is a model-specific derivation,
not an established scientific-priority claim. The closest checked internal
result is M2, whose weaker time-dependent residual estimate is sharpened.

No actual endpoint nonconvergence, optimal coefficient, growing-support
theorem, exponential real-time decay, homogeneous interaction threshold,
conditional-mobility clock matching, continuum Yang–Mills construction or
Clay mass-gap solution follows. The accepted model remains at fixed spacing
and returns to its selected-strip reference as q increases to one.
