# S2 reverse — connected control for the full-source triangular filter

The frozen filter supplies a bounded full-source map with an exact retained residual on every finite containing volume. Its generator and residual have explicitly summable connected-support interactions at weight `2^{|Y|}`, uniformly in volume throughout the prescribed parameter range. The generator preserves the actual graph domain. This is a **regulated inverse identity**, not an exact unregularized inverse: the residual keeps every equal-energy source block. Regulator removal, the infinite-volume identification, later-diagonal iteration and the homogeneous numerical gap remain unproved.

## 1. Reconstruct the intended inverse and its residual

Keep the actual S1 cubic source on each retained star. With `v=phi_b Omega`, `u=(H0|Q)^(-1)v`, `c=<u,v>` and `beta=||u||^2`, its vector is `w=-c u-beta v/3`; S1 proves it is nonzero at nonzero tau using actual SU(2) Haar moments. Set `A=A_b^gen tensor I_ext`, with

`||A||=||w||<=r_*`, `r_*=(4/3)(7/12)^(3/2)|tau|^3`

as one possible common bound. Do not replace the exterior identity by a global vacuum projection. Let `G=G_Lambda=H0_Lambda+sum D_b` be the **full** initial retained diagonal, including crossing stars. It is self-adjoint on `D(H0_Lambda)` in every finite cuboid, since the finite sum D is bounded self-adjoint. Define `alpha_s(A)=exp(isG)A exp(-isG)`.

For `0<Theta<=1/16`, put `f_Theta(s)=sign(s)(1-|s|/Theta)` on `[-Theta,Theta]`, and zero elsewhere. The contract's map is

\[
L_\Theta(A)=-\frac i2\int_{-\Theta}^{\Theta}f_\Theta(s)\alpha_s(A)\,ds.\tag{1}
\]

The integral is taken vectorwise strongly. For every vector, its integrand is norm-continuous on each half interval, and uniformly bounded by `||A||`; the jump at zero causes no difficulty. It defines a bounded skew-adjoint operator, with

`||L_Theta||<=Theta||A||/2`.

No operator-norm continuity of the orbit is assumed.

For domain vectors phi,psi the scalar matrix element of alpha_s(A) is differentiable by moving the unitary factors onto the domain vectors. This does **not** require A to preserve D(G). The distributional derivative of f is

`f_Theta'=2 delta_0-(1/Theta)1_(-Theta,Theta)`.

Integration by parts, with the vanishing endpoint values, proves the bounded commutator identity

\[
\boxed{[L_\Theta,G]=-A+R_\Theta(A),\qquad
R_\Theta(A)=\frac1{2\Theta}\int_{-\Theta}^{\Theta}\alpha_s(A)\,ds.}\tag{2}
\]

The residual is a self-adjoint bounded operator with `||R_Theta(A)||<=||A||`. The scalar weak identity implies that for every psi in D(G), the functional `phi -> <G phi,L_Theta psi>` is represented by the vector `L_Theta G psi+(A-R_Theta)psi`. Self-adjointness of G therefore proves `L_Theta psi in D(G)` and the same operator identity there. Thus

`||G L_Theta psi||<=||L_Theta||||G psi||+2||A||||psi||`.

L_Theta is bounded on the Banach graph space. Its exponential power series and that of its inverse converge there, so `exp(+-L_Theta)D(G)=D(G)`. This establishes graph preservation from the integrated commutator, without assuming the source's graph regularity or formally expanding unbounded G.

Equation (2) is a full-operator identity against the actual identity-extended source, on all exterior sectors. Its residual is an essential part of that identity.

## 2. Spectral meaning, exceptions and inverse limitations

On a matrix element of Bohr frequency `omega=E_m-E_n`, equation (1) has the scalar multiplier

\[
\ell_\Theta(\omega)
=\int_0^\Theta(1-s/\Theta)\sin(\omega s)\,ds
=\frac{1-\operatorname{sinc}(\Theta\omega)}\omega,\tag{3}
\]

with its continuous value zero at omega zero. Here `sinc(x)=sin(x)/x`, `sinc(0)=1`. The commutator multiplies this by `-omega`, so the residual multiplier is precisely

`r_Theta(omega)=sinc(Theta omega)`.

Every exact equal-energy block is retained: `P_E R_Theta(A)P_E=P_E A P_E`. The small-frequency expansions are

`ell_Theta(omega)=Theta^2 omega/6+O(Theta^4 omega^3)`,
`r_Theta(omega)=1-Theta^2 omega^2/6+O(Theta^4 omega^4)`.

Consequently shortening this filter approaches zero generator and the full source residual; it does not improve the inverse. A zero residual on an isolated frequency with `Theta omega` a nonzero integer multiple of pi is a valid special case, not a uniform spectral statement. Scalar bounds such as `|sinc(Theta omega)|<=min(1,1/|Theta omega|)` do not alone provide an operator-norm bound for an arbitrary spectral multiplier acting on every source.

Sending Theta to infinity would be a different limit, outside the declared proof regime below. Equal-energy blocks would survive it, and positive ground energy separation does not control excited Bohr frequencies. Even pointwise convergence of the scalar inverse coefficient away from zero would not establish a bounded full inverse or the required support norm. This loop proves no nonzero equal-energy block for the actual SU(2) source. The generic S1 resonance fixture remains only an inference falsifier.

Tau zero and source zero are exact zero solutions of (1)–(2). The contract excludes Theta zero; the limiting construction there has `L=0,R=A`. Negative Theta is not used to change the filter's sign. Reversing time while changing only one sign reverses the homological cancellation and is rejected by the scalar checks.

## 3. Actual connected expansion, including its time factors

The operator proof above is independent of a locality expansion. To obtain locality, use the interaction picture with respect to the onsite H0. Let

`D_b(s)=exp(isH0)D_b exp(-isH0)`, `W(s)=exp(isH0)exp(-isG)`.

Each D_b(s) remains supported on its original star and has norm at most `M=7|tau|`; onsite evolution preserves complete factor support. Bounded perturbation theory in each fixed finite volume gives `W'=-i(sum_b D_b(s))W` in the strong sense. For fixed final s,

`alpha_s(A_b)=W(s)^* alpha_s^0(A_b) W(s)`.

Iterating this identity gives ordered nested commutators of D_b(t), integrated over a time simplex of volume `|s|^n/n!`. These are strong integrals of bounded operators. The fixed-volume Dyson series converges, and the following absolute estimate permits its connected regrouping uniformly in volume for the stated times.

A possibly nonzero word must attach every next star to the accumulated union. With j stars already present, at most `13j` candidate anchors meet that union, because `|G_star-G_star|=13`. Retain repeated anchors and terms that meet an earlier generated star while missing the base. Thus at order n there are at most `13^n n!` relative ordered words. Each union has at most `4+3n` sites. For every relative word, at most `4+3n` translations put a specified site in that union. Restriction to the positive octant and retained finite-volume stars removes terms but never creates additional ones. This also retains incoming crossings where they exist.

For a whole family of source anchors with uniform norm bound r_*, the order-n rooted weighted contribution is therefore bounded by

\[
\begin{aligned}
& (4+3n)\,2^{4+3n}\,(13^n n!)\,(2M)^n r_*\frac{|s|^n}{n!}\\
&\hspace{15mm}=16r_*(4+3n)(208M|s|)^n.\tag{4}
\end{aligned}
\]

The factors are, in order, rooted translations, declared support weight, candidate words, commutator norm, and time-simplex volume. Omitting any of the word factorial, simplex factorial, or root factor changes the certificate. The weight is exactly the required cardinality weight; no cubic collar has replaced these connected unions. Different indexed words with identical unions remain in the decomposition, so cancellations are not presumed.

## 4. Sum every order and give explicit tails

Let `z=208MTheta=1456|tau|Theta`. For `z<1`, define

\[
F(z)=\sum_{n\ge0}(4+3n)z^n=\frac{4-z}{(1-z)^2}.\tag{5}
\]

Equation (4) proves, for the declared interaction family,

`||alpha_s(A_family)||_w<=16r_*F(z)` for `|s|<=Theta`.

Integrating the coefficients with the actual filter weights gives the sharper series

\[
\|L_\Theta\|_w\le16r_*\Theta
 \sum_{n\ge0}\frac{(4+3n)z^n}{(n+1)(n+2)},\tag{6}
\]
\[
\|R_\Theta\|_w\le16r_*
 \sum_{n\ge0}\frac{(4+3n)z^n}{n+1}.\tag{7}
\]

In particular the following rational bounds suffice, including z zero:

\[
\boxed{\|L_\Theta\|_w\le8r_*\Theta F(z),\qquad
\|R_\Theta\|_w\le16r_*F(z).}\tag{8}
\]

These are local interaction norms, not volume-independent norms of extensive global sums. In a fixed finite cuboid the global sums have the corresponding finite-volume norm bounds. The regulated identity also holds term by term for each original source, so finite family summation is legitimate.

For a truncation after n=N, the unintegrated positive tail is exactly

\[
F_{>N}(z)=\frac{z^{N+1}[(3N+7)-(3N+4)z]}{(1-z)^2}.\tag{9}
\]

Thus the weighted truncation errors of L and R are respectively at most `8r_*Theta F_>N(z)` and `16r_*F_>N(z)`. They tend to zero uniformly on any fixed compact subinterval of z<1. A truncated filter is not the full filter; its additional truncation error must remain in any commutator or evolution use.

At the frozen endpoints,

`z<=208*(35/1664)*(1/16)=35/128<1`,

and `F(35/128)=6784/961`. Hence the fully uniform rational certificate is

`||L_Theta||_w<=(54272/961)r_*Theta`,
`||R_Theta||_w<=(108544/961)r_*`.

This is a useful positive cardinality-weight certificate for the regulated map. It does not show that R is smaller than A or supply a contraction. For small Theta, the exact spectral calculation says the low-frequency residual is almost unchanged.

An infinite-time Laplace integral of this same positive local-series majorant would instead introduce `int_0^infty exp(-eta s)s^n ds=n!/eta^(n+1)`. The resulting positive terms have eventually growing ratio for every nonzero M, regardless of eta>0. Therefore that interchange cannot be justified by this certificate. This is failure of a particular majorant integration, not divergence of the actual bounded filtered operator or a no-go theorem for other locality methods.

## 5. Scope, checks and next missing premise

The checker independently integrates the sine power coefficients with rational polynomial integrals, checks the exact commutator sign and sinc coefficients including frequency zero, and encloses a nonzero-frequency example with alternating-series errors. It verifies the required root multiplicity, connected-word recurrence, simplex coefficients, endpoint radius, positive-series tail identities and the failed all-time coefficient ratio. The actual source's nonzero proof and units are inherited from admitted S1 and bound in the manifest. Generic scalar frequency controls do not establish the actual source's full spectral distribution. Explicit runtime exceptions preserve the checks in optimized Python.

No infinite-volume identification with R2 G is claimed. Such an identification would need an actual strong-resolvent/unitary or direct form-limit argument for these finite-volume constructions, followed by identification of the resulting local interaction map with that operator. The present result already gives finite-volume full-source identities and uniform weighted bounds; those bounds alone do not prove that missing operator limit. There is also no later-diagonal induction here.

The closest primary methods are the inherited O1 connected Lie/Dyson estimates and R2's form-domain construction, whose reading scopes remain those recorded in the bound reports: [Yarotsky](https://arxiv.org/pdf/math-ph/0411042), [unbounded-interaction Lie-Schwinger methods](https://arxiv.org/pdf/2108.13907), and [Teschl](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf). This loop did not claim a new reading of those complete proofs or import a numerical stability threshold. The triangular filter identity and the displayed connected constants are directly derived here. Their scientific priority remains unverified.

Theta is a dimensionless proof duration with energy-resolution scale `delta/Theta`, where `delta=alpha/8`. Its real-time parameter obeys `s=delta*t_physical/hbar`. It changes neither the action nor the measured clock. Fixed lattice spacing a, E_star, alpha/E_star and hbar remain positive. A zero physical reference is rejected, not regularized by a numerical tolerance.

The next missing S premise is control of the retained actual low/zero-frequency residual in a norm compatible with an all-stage construction, or a proof that a modified retained equation suffices. This pair does not execute that next investigation. T and U require their own models and frozen contracts; none of these homogeneous-filter constants transfers to them. Physical calibration and the four-dimensional continuum construction remain open.

Reproduce with `python3 -B research/round23/reverse/s2/check.py --output /tmp/ym23-reverse-s2-fresh` and a separate fresh `python3 -O -B` run.
