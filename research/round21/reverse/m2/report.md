# M2 reverse reconstruction: connected physical correlations on growing windows

The proposed coefficient-six estimate is valid under the admitted canonical
summable-profile premises. It is sufficient for real-time windows with exponent
`0 <= gamma < 3/2`. The endpoint is not established by this estimate, and its
failure to vanish does not prove endpoint nonconvergence. This is the tenth
Round21 loop; no additional research loop is selected or executed here.

No forward M2 report, source or result was read before this report and checker
were frozen. The shared contract and admitted M1/H2/J2 results are shared
mathematical premises, not independent observations. The project contribution
is this scoped quantitative application; scientific priority is unverified.

## 1. Reconstruct the target and its sufficient premises

Work in exactly the A2 full-link incomplete tensor product with its
selected-strip/free reference vacuum `Omega` and Hamiltonian `H0=H_ref`.
Spacing, `E_star>0`, `alpha/E_star>0`, `hbar>0` and `0<eta<1` are fixed.
The continuous parameter `0<q<1`, the budget fraction eta and the canonical
coupling tau are dimensionless action-profile parameters. They are not a
measured clock, a new physical field or parameters of the K/L diffusion.

Put

\[
p(q)=2+5q+5q^2+6q^3+3q^4,\quad
B(q)=\frac{p(q)}{24(1-q)^3(1+q)^2(1+q^2)},\quad
\tau_q=\frac{\eta}{8B(q)},\quad \bar g=\frac{\alpha(1-\eta)}8.
\]

The omitted-face perturbation is
`V_q=-alpha tau_q sum_f q^(x+y+z)x_f/24`. In this representation the admitted
premises are

\[
H_q=H_0+V_q,\quad \|V_q\|=\alpha\eta/8,\quad
\sigma_q^2=\|V_q\Omega\|^2
=\alpha^2\tau_q^2B(q^2)/96,
\]
\[
-\sigma_q^2/\bar g\le e_q\le0,\qquad
d_q:=\|P_q-P_0\|\le\sigma_q/\bar g,
\qquad P_0=|\Omega\rangle\langle\Omega|.
\]

For fixed bounded local invariant A and B, the desired quantity is

\[
C_q^{A,B}(t)=\langle\Psi_q,A^*U_q(t)B\Psi_q\rangle
-\omega_q(A^*)\omega_q(B),\qquad
U_q(t)=e^{-it(H_q-e_q)/\hbar}.
\]

Use `U_0(t)=exp(-itH0/hbar)` and the analogous reference expression.
Complex A and B are allowed: `omega_q(A*)` is the complex conjugate of
`omega_q(A)`, and generally the two mean factors differ. Equivalently,
`C_q=< (A-omega_q(A))Psi_q, U_q(t)(B-omega_q(B))Psi_q >`.
This equality uses `U_q(t)Psi_q=Psi_q`. At `t=0` it gives the actual connected
covariance. For `A=B` it gives variance at zero time.

Reverse reconstruction isolates three sufficient ingredients: a trace-distance
bound for the two states, a quantitative dynamical estimate on the *fixed*
vector `B Omega`, and the actual ground-energy subtraction. Strong convergence
on arbitrary fixed vectors alone supplies no growing-time rate.

## 2. Re-establish the physical sector for this profile

A2 supplies `H0>=0`, a simple zero ground and reference excitation threshold
`alpha/8`. Bounded self-adjoint `V_q` has norm `alpha eta/8`; hence
`D(H_q)=D(H0)` and the closed form domain is unchanged. The zero reference
mean of every omitted Wilson face gives `<Omega,H_q Omega>=0`. On the
codimension-one reference complement,
`Q0 H_q Q0 >= gbar Q0`. Its spectral subspace below gbar has rank at most
one: a two-dimensional subspace would contain a nonzero vector perpendicular
to Omega, contradicting this form inequality. The reference trial vector
ensures that this spectral subspace is nonzero. Thus `H_q` has a unique ground
`e_q<=0`, and the rest of its spectrum is at least gbar in absolute energy.
Consequently `H_q-e_q` has gap at least gbar. This is its own profile-wide
floor, not J2's dyadic constant `973alpha/8640`.

A finite-support assignment of vertex SU(2) elements acts by endpoint left
and right multiplication on links. It touches finitely many complete factors
and defines a strongly continuous unitary in this representation. Each unique
strip ground carries a continuous one-dimensional character of a finite
product of SU(2); such a character is trivial. Free Haar vectors are invariant,
so Omega is invariant. Electric Casimirs and closed Wilson traces commute with
this action. Commutation holds on the local smooth tensor core and extends to
the closed reference form/operator domains. Boundedness of V_q and its
norm-convergent gauge-invariant face sum preserve commutation for H_q. Its
unique ground is again invariant by the same trivial-character argument.

Let A_loc contain all bounded operators on finite complete reference factors,
let A be its norm closure, and let A_phys be the norm closure of its invariant
local elements. Reference evolution acts independently on complete factors,
so it preserves A_loc. For a finite face truncation V_N, `H0+V_N` evolves any
local observable on the union of finitely many complete factors. Since
`||V_N-V_q|| -> 0`, the two Heisenberg evolutions differ by at most
`2|t| ||V_N-V_q|| ||A||/hbar`. Thus the full evolution preserves A. Each
finite truncation and the reference evolution commute with gauge actions, so
the same approximants show preservation of A_phys. This argument needs no
point-norm continuity of reference evolution on all of B(H).

The full bounded-factor algebra is irreducible by the admitted G2 finite
reference-projection argument, independent of q; every nonzero vector,
including Psi_q, is cyclic for it. Define
`K_phys,q=closure(A_phys Psi_q)` and let H_inv be the vectors fixed by all
finite-support gauges. Invariance gives `K_phys,q subset H_inv`. For the
reverse inclusion, approximate any xi in H_inv by `A Psi_q` with A bounded
and local. Average A over the compact product of SU(2) groups at all endpoints
of its complete link support E. The bounded weak/strong operator integral
remains supported in E and is invariant under every gauge transformation.
Its error on Psi_q is at most `||A Psi_q-xi||`, since xi and Psi_q are fixed.
Therefore

\[
\mathcal K_{\rm phys,q}=\mathcal H_{\rm inv}.
\]

This equality uses the full bounded invariant local algebra, not an arbitrarily
smaller selected-Wilson algebra. A fundamental matrix coefficient on one free
link changes sign under a center transformation at one endpoint and gives a
nonzero charged vector, so H_inv is a proper subspace of the full Hilbert space.
The variance estimate below makes it larger than the vacuum line eventually.

Gauge commutation makes H_inv reducing for the full unitary group. The map
`[A] -> A Psi_q` identifies the restricted-state GNS completion with K_phys,q.
Its canonical energy generator is the self-adjoint restriction

\[
K_q=(H_q-e_q)|_{\mathcal H_{\rm inv}},\qquad
D(K_q)=D(H_q)\cap\mathcal H_{\rm inv},\qquad
\operatorname{spec}K_q\subset\{0\}\cup[\bar g,\infty).
\]

Its Stone frequency generator is K_q/hbar. Arbitrary bounded local observables
are not assumed to preserve this unbounded operator's domain. No exponential
real-time decay follows from this spectral gap.

## 3. Retain complete factor support at every reference time

Let F_B be a finite set of complete factors supporting B, and let E(F_B)
contain every link of those factors. The nonnegative reference form sum splits
as the finite-factor Hamiltonian plus its exterior sum; their spectral
resolutions commute. Thus its unitary factors across this decomposition, and

\[
U_0(s)B\Omega=B_s\Omega,\qquad
B_s=U_{0,F_B}(s)B U_{0,F_B}(-s),\qquad \|B_s\|=\|B\|.
\]

For all real s the support of B_s is still F_B. This can enlarge B's displayed
link support *within* a dressed strip; its complete factor support is unchanged.
No differentiability of B_s or domain invariance of B is needed for this
bounded-operator identity.

With N(F_B) the omitted faces meeting E(F_B), put
`D_FB(q)=sum_(f in N(F_B)) q^(x+y+z)/24`. M1 proves

\[
D_{F_B}(q)\le |E(F_B)|/6,\quad
\|V_q B_s\Omega\|\le
\|B\|[\sigma_q+2\alpha\tau_qD_{F_B}(q)]
\]

uniformly for all s, since each link is incident to at most four elementary
faces. The origin-xz loop has four displayed links but its complete cover has
22 links and 28 incident omitted faces, versus five for the displayed links.
The larger support is what is valid for an arbitrary bounded operator after
complete-factor reference evolution.

Bounded-perturbation Duhamel, first on D(H0) and then extended by density to
all vectors, now gives for either sign of t

\[
\|(U_q(t)-U_0(t))B\Omega\|
\le\frac{|t|}{\hbar}\|B\|
[|e_q|+\sigma_q+2\alpha\tau_qD_{F_B}(q)].
\]

The scalar shift can be included in the perturbation `V_q-e_q I` or estimated
using `|exp(ite_q/hbar)-1|<=|te_q|/hbar`. Omitting it would fail even for a
constant observable with otherwise identical dynamics.

## 4. Derive the coefficient-six bound without self-adjointness assumptions

For rank-one states `||P_q-P_0||_1=2d_q`. This follows by restricting their
difference to the span of the two vectors: its nonzero eigenvalues are
`+d_q,-d_q`. Hence for every bounded, possibly non-self-adjoint X,
`|omega_q(X)-omega_0(X)|<=2d_q||X||`.

First hold the bounded operator `X=A*U_q(t)B` fixed while changing its state.
This costs at most `2d_q||A||||B||`. The remaining uncentered reference-state
change is at most `||A|| ||(U_q-U_0)B Omega||`. For the product of means,

\[
\begin{split}
|\omega_q(A^*)\omega_q(B)-\omega_0(A^*)\omega_0(B)|
&\le |\omega_q(A^*)-\omega_0(A^*)|\,|\omega_q(B)|\\
&\quad+|\omega_0(A^*)|\,|\omega_q(B)-\omega_0(B)|\\
&\le4d_q\|A\|\|B\|.
\end{split}
\]

Adding the three state costs and the dynamical cost proves

\[
\boxed{|C_q^{A,B}(t)-C_0^{A,B}(t)|\le\|A\|\|B\|
\left[6d_q+\frac{|t|}{\hbar}
(|e_q|+\sigma_q+2\alpha\tau_qD_{F_B}(q))\right].}
\]

The coefficient six is sufficient, not claimed optimal. At t=0 the dynamical
term vanishes and the covariance comparison remains valid. Substituting the
admitted residual/energy bounds and the complete-link count gives

\[
\boxed{\sup_{|t|\le T}|C_q^{A,B}(t)-C_0^{A,B}(t)|
\le\|A\|\|B\|\left[
\frac{6\sigma_q}{\bar g}+\frac T\hbar
\left(\frac{\sigma_q^2}{\bar g}+\sigma_q
+\frac{\alpha\tau_q|E(F_B)|}{3}\right)\right].}
\]

## 5. Determine exactly what this rate establishes

Write epsilon=1-q. Exact profile identities yield

\[
\frac{\tau_q}{\epsilon^3}\to\frac{8\eta}{7},\qquad
\frac{\sigma_q^2}{\alpha^2\eta^2\epsilon^3}\to\frac1{5376},
\qquad
\frac{\sigma_q}{\alpha\epsilon^{3/2}}\to\frac{\eta}{\sqrt{5376}}.
\]

For `T_q=(hbar/alpha) C epsilon^(-gamma)`, with fixed C>0, fixed A,B and
`0<=gamma<3/2`, the bound is
`O(epsilon^(3/2-gamma))`. Its state term has exponent 3/2, its T sigma term
has exponent `3/2-gamma`, and its energy and local-interaction terms have
exponent `3-gamma`. This establishes uniform convergence on the declared
growing windows; the fixed-time upper rate is 3/2. It is not uniform over
moving observables, growing supports, eta approaching one or varying units.

At gamma=3/2 the displayed sufficient upper bound has a positive limit
`||A||||B|| C eta/sqrt(5376)` when both norms are nonzero, due to its residual
term. Thus this bound supplies no vanishing-error certificate there. It does
not supply a lower bound on the actual correlation error. Endpoint convergence,
larger admissible windows and optimality remain unresolved for this family.
No rapid oscillation or real-time decay assumption is used.

## 6. Transfer a concrete physical fluctuation

Choose the actual origin-xz Wilson loop `W=Tr(U_square)/2`. It is self-adjoint,
gauge invariant, local and has norm one. Integrating one of its free Haar z
links conditionally gives `omega_0(W)=0` and `omega_0(W^2)=1/4`. The exact
reference moments remain those of the same selected-strip vacuum for all q.
Trace distance controls both actual perturbed moments:

\[
\operatorname{Var}_{\Psi_q}W
\ge\frac14-2d_q-4d_q^2.
\]

The right side decreases for nonnegative d. In particular

\[
\boxed{\sigma_q/\bar g\le1/16
\quad\Longrightarrow\quad
\operatorname{Var}_{\Psi_q}W\ge7/64>0.}
\]

A concrete sufficient profile condition can be written without sigma:

\[
\left(\frac{\sigma_q}{\bar g}\right)^2
=\frac{\eta^2\epsilon^3}{(1-\eta)^2}
\frac{p(q^2)(1+q)}{4p(q)^2(1+q^4)}
\le\frac{\eta^2\epsilon^3}{4(1-\eta)^2}.
\]

Here `p(q^2)<=p(q)`, `p(q)>=2`, `1+q<=2` and `1+q^4>=1` prove the last
inequality. Thus `(1-q)^3 <= (1-eta)^2/(64 eta^2)` suffices. For example,
eta=1/2 and every q in `[3/4,1)` satisfy it. Any fixed eta strictly between
zero and one satisfies it eventually. The centered Wilson vector is therefore
nonzero, physical and perpendicular to Psi_q. Smooth Wilson multiplication
preserves the form domain by its bounded first derivatives, so this particular
vector also has finite energy. The general bounded-observable proof did not
need that stronger property.

## 7. Evidence, source boundary and unresolved questions

The standard-library checker computes rational profile identities, exact
Gaussian-rational complex covariances, phase controls, complete support,
time-exponent bookkeeping, a finite symmetry reduction and the variance floor.
Controls expose absent conjugation, uncentered means, an omitted energy shift,
displayed-link support, an endpoint promoted from a sufficient bound and a
dyadic gap transplanted to a different profile. They discriminate errors;
they do not machine-formalize the infinite-dimensional proof or represent
measured data. Runs use explicit checks that survive `python -O`.

For the established operator framework, see
[Teschl, Mathematical Methods in Quantum Mechanics](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf),
sections 4.2, 5.1, 6.1 and 6.6. The model-specific support, gauge averaging,
centering and growing-window arguments are given above. No source is claimed
to establish this workbench's numerical profile constants or scientific
priority.

The limit remains the fixed-spacing selected-strip reference: each fixed
omitted coefficient tends to zero, although the global perturbation norm is
constant. No nonzero homogeneous interaction, K/L clock matching, continuum
four-dimensional Yang-Mills construction or Clay mass gap is established.
Norm-resolvent and propagator-norm limits, optimal time windows, and unrelated
finite-clipped-restriction limits are not resolved here.

```bash
python3 -B research/round21/reverse/m2/check.py --output FRESH_DIRECTORY
python3 -O -B research/round21/reverse/m2/check.py --output OTHER_FRESH_DIRECTORY
```
