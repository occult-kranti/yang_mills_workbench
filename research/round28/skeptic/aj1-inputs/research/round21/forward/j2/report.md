# J2 forward: the physical cyclic space and its energy generator

Frozen before reverse-J2 comparison. Retain J1's dyadic summable model, fixed positive `alpha/E_star`, fixed spacing and `|tau|<=1/64`. Let `Psi` be its unique invariant ground vector, `H Psi=e Psi`, and let `A_phys` be the norm closure of bounded gauge-invariant local operators. J1 proves a nonzero centered physical Wilson vector; G2 proves that Psi is cyclic for the full bounded local algebra.

## 1. Finite gauge averaging proves the reverse inclusion

J1 already gives `H_cyc=closure(A_phys Psi) subset H_inv`. Take any `xi in H_inv`. Full-algebra cyclicity gives bounded finite-support operators `A_n` with `A_n Psi -> xi`. Let `F_n` be the link support and `V_n` its finite set of endpoints. Define the compact-group average

\[
\mathcal E_n(A_n)=\int_{SU(2)^{V_n}}
 \Gamma(g) A_n\Gamma(g)^*\,dg.
\tag{J2.1}
\]

This is a **weak operator integral**. Its matrix elements are continuous bounded functions; the resulting bounded sesquilinear form defines an operator of norm at most `||A_n||`. No operator-norm continuity of gauge conjugation is assumed. Gauge transformations factor over links, so conjugation and the average preserve the finite link support. Haar invariance makes the average invariant under the endpoint groups; every other vertex acts trivially on its support. Thus `E_n(A_n)` belongs to `A_phys,loc`.

On Psi the integral is also the strong vector integral: the integrand is `Gamma(g) A_n Psi`, which is norm-continuous. Since both Psi and xi are invariant,

\[
\|\mathcal E_n(A_n)\Psi-\xi\|
\le\int\|\Gamma(g)(A_n\Psi-\xi)\|\,dg
=\|A_n\Psi-\xi\|\longrightarrow0.
\]

Consequently

\[
\boxed{\mathcal H_{\rm cyc}=\mathcal H_{\rm inv}.}
\tag{J2.2}
\]

This depends on the specified full bounded-local algebra and cyclic invariant vacuum. It is not a general statement for arbitrary gauge theories or arbitrary smaller observable algebras. The common space is proper in `H_full`: the charged free-z-link vector from J1 lies outside it. Full-space irreducibility was used only to supply full-algebra cyclicity, not asserted for the restricted algebra.

## 2. The physical GNS completion

For `omega(A)=<Psi,A Psi>` restricted to `A_phys`, the null left ideal is

\[
\mathcal N_\omega=\{A:\omega(A^*A)=0\}
=\{A:A\Psi=0\}.
\]

The map `W_phys:[A]->A Psi` is well defined on the quotient, preserves its inner product, and has dense range in `H_cyc`. It extends to a unitary from the physical GNS completion onto `H_inv`. Left multiplication by a physical observable is intertwined with its actual restriction. J1's positive Wilson variance proves this completion has a nonvacuum vector.

## 3. Restricting the unbounded energy operator

Gauge unitaries commute with H on the invariant core and hence with its spectral projections, as established in J1. Therefore `H_inv` reduces the unitary group and the spectral measure. The restricted self-adjoint operator has domain `D(H) intersect H_inv`; spectral cutoffs commuting with the gauge action show this domain is dense in `H_inv`. The corresponding form domain is the intersection with `Q(H)`.

The correctly normalized physical energy generator is

\[
K_{\rm phys}=(H-e)|_{\mathcal H_{\rm inv}},\qquad
K_{\rm phys}\Psi=0.
\tag{J2.3}
\]

Indeed, J1's invariant dynamics and the eigenvector equation give

\[
W_{\rm phys}[\alpha_t(A)]
=e^{it(H-e)/\hbar}A\Psi.
\]

Thus the GNS implementation is strongly continuous even though point-norm continuity on every bounded local operator is unavailable. The generator domain in the abstract GNS space is `W_phys^{-1}(D(H) intersect H_inv)`. The ground-energy subtraction is needed to fix the cyclic vector; it does not change observable conjugation.

A2/J1's threshold restricts to this reducing subspace:

\[
\operatorname{spec}(K_{\rm phys})
\subseteq\{0\}\cup[973\alpha/8640,\infty).
\tag{J2.4}
\]

The zero eigenspace is one-dimensional. The stronger threshold `g-e` may apply, but neither threshold is asserted to equal the first physical excitation or a measured glueball mass. This is the same specified summable representation, not a homogeneous or continuum identification.

## 4. A nonzero imaginary-time Wilson correlator

Use J1's xz Wilson operator and set `chi=(W-omega(W))Psi`. Its norm square is `Var_Psi(W)>=5321/22500`, and it is perpendicular to Psi in `H_inv`. The spectral measure `mu_chi` of `K_phys` is a nonzero positive finite measure supported at energies at least `g_min=973alpha/8640`. For finite `t>=0`, define

\[
C_W(t)=\langle\chi,e^{-tK_{\rm phys}/\hbar}\chi\rangle
=\int_{g_{\min}}^\infty e^{-tE/\hbar}\,d\mu_\chi(E).
\]

The integrand is strictly positive at every finite energy. Hence

\[
\boxed{0<C_W(t)\le\operatorname{Var}_\Psi(W)
       e^{-973\alpha t/(8640\hbar)}.}
\tag{J2.5}
\]

A lower spectral bound supplies this **upper** decay bound; it supplies no lower exponential bound on the correlator. In real time the spectral kernel is a complex phase, so the conclusion does not transfer. A single excited eigenstate retains a constant correlation magnitude forever.

## 5. Exact finite controls and provenance

The checker uses a separate three-dimensional symmetry model with `G=diag(1,1,-1)`, vacuum e0 and `H=diag(-2,1,5)`. Twirling removes the charged matrix blocks. The physical GNS orbit has dimension two, while the full orbit has dimension three. A noninvariant vacuum rejects the inclusion premise. Subtracting `e=-2` produces the physical spectrum `{0,3}`; retaining the raw ground energy fails vacuum invariance.

At imaginary time `t=log(2)` and hbar one, a normalized physical excited vector has correlation `2^-3=1/8`, an exact rational fixture. A spectral-energy-6 control gives `1/64`, disproving a lower bound inferred from gap 3. An exact unit-modulus nontrivial phase rejects real-time magnitude decay. These fixtures test the logical implications; the infinite-dimensional identification is proved above, not inferred from their ranks.

The inputs are the admitted J1 gate, [J1 forward proof](../j1/report.md), [G2's full GNS result](../../../round20/forward/g2/report.md), and [A2's operator theorem](../../../round19/forward/a2/report.md). The project contribution is this explicit physical-subspace identification and its instantiated spectral-correlator consequence. The GNS, compact-group averaging and spectral tools are established mathematics; scientific priority is unverified. No K loop was executed.

```bash
python -B research/round21/forward/j2/check.py --output /tmp/ym21-forward-j2-replay
```
