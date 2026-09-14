# J1 forward: an invariant local algebra with a surviving Wilson fluctuation

Frozen before reading reverse J1. This goal explicitly returns to the **dyadic summable model** of A2/E/G, at fixed spacing, `q=1/2`, `alpha>0`, `E_star>0`, and `|tau|<=1/64`. It is not I1's homogeneous interaction. No numerical homogeneous stability interval is borrowed from I.

## 1. Gauge action, core and vacuum

For a finite-support assignment of vertex matrices `g_v in SU(2)`, each oriented link transforms as

\[
U_{(v,w)}\longmapsto g_v U_{(v,w)}g_w^{-1}.
\]

Pullback defines a unitary `Gamma(g)` on the Haar link space. Only finitely many links, and therefore finitely many complete reference factors, are affected. Left/right Haar invariance preserves the measure. Every selected strip Hamiltonian and free Casimir commutes with its endpoint gauge action. The unique strip ground vector transforms by a continuous character of a finite product of SU(2) groups; this character is trivial because `su(2)=[su(2),su(2)]` and SU(2) is connected. Free Haar vacua are also invariant. Hence `Gamma(g) Omega=Omega` in the A2 reference representation.

Let `D_fin` be the finite span of tensors with finitely many factors in their individual operator domains and all other factors in their reference ground vectors. Finite spectral truncation and then finite-factor truncation give a core for the nonnegative sum `H_ref`. The analogous finite tensors in the factor form domains form its quadratic-form core. Gauge unitaries commute with each affected factor operator, preserve these cores, and preserve the closed operator and form domains.

The dyadic perturbation is an operator-norm convergent sum of bounded Wilson multiplications. Each Wilson loop is gauge invariant by cancellation of the successive endpoint transformations. Thus V commutes with every `Gamma(g)`. Bounded perturbation leaves `D(H)=D(H_ref)` and its form domain unchanged; `D_fin` remains an operator core. It follows that H commutes with the gauge action, including its spectral projections. A2's unique ground line therefore carries a trivial character by the same argument, giving `Gamma(g) Psi=Psi`.

These are applications of the inherited [A2 operator and gauge construction](../../../round19/forward/a2/report.md), now with the local algebra specified. No assertion that all bounded local operators preserve the unbounded operator domain is needed.

## 2. Local physical observables and the three Hilbert spaces

For a finite link set F, use bounded operators supported on F and invariant under every endpoint gauge transformation, extended by the identity. Their increasing union is `A_phys,loc`; its norm closure is `A_phys`. Finite link supports are contained in finite unions of complete reference factors, so this is a subalgebra of G1's quasilocal algebra.

Keep the following spaces distinct:

\[
\mathcal H_{\rm inv}=\{\xi:\Gamma(g)\xi=\xi\text{ for every finite-support }g\},
\quad
\mathcal H_{\rm cyc}=\overline{\mathcal A_{\rm phys}\Psi},
\quad
\mathcal H_{\rm cyc}\subseteq\mathcal H_{\rm inv}\subseteq\mathcal H_{\rm full}.
\]

No equality between the first two spaces is inferred. The invariant space is proper in the full representation: an open **free z-link** trace times the reference vacuum is nonzero, by its Haar second moment, but changes sign under the central gauge transformation `g_v=-I` at one endpoint. Thus it cannot be invariant. G2's full-algebra irreducibility cannot be copied to this restricted algebra: the nontrivial gauge unitaries commute with every invariant observable.

The dynamics of [G1/G2](../../../round20/forward/g2/report.md) commutes with the gauge action. A evolved invariant local operator is quasilocal and invariant. To see that it belongs to the stated norm closure, approximate it by bounded operators on finite link sets and Haar-average each approximation over the finitely many gauge groups at its endpoints. Averaging is contractive, preserves finite link support, and leaves the invariant target unchanged. This gives invariant local approximations with the same error. Consequently dynamics preserves `A_phys`. This argument does not assert point-norm continuity in time on every bounded observable; G1's contrary control remains in force.

## 3. A genuine omitted physical observable

Choose the xz face based at `(0,0,0)` and its normalized Wilson multiplication `W=Tr(U_f)/2`. It has norm one and is invariant under every local gauge transformation. Its two z links are free reference Haar factors. Integrating either one gives

\[
\langle\Omega,W\Omega\rangle=0,\qquad
\langle\Omega,W^2\Omega\rangle=1/4.
\]

The SU(2) identity is the quaternion second moment `E[u_i u_j]=delta_ij/4`; the remaining unit quaternion only rotates the linear coefficient. Internal entanglement of selected strips does not affect that conditional integral. The checker includes exact rational quaternion gauge transformations and a charged open-link rejection. The gauge-cancellation proof supplies the full group statement.

Reference variance alone is insufficient. The following calculation proves a nonzero fluctuation in the **perturbed** ground Psi.

## 4. Exact residual and projector estimates at the actual coupling range

The complete omitted coefficient sum is independently reconstructed by geometric series:

\[
B(q)={1\over8(1-q)^3}
-{1+q+q^2\over24(1-q^4)(1-q^2)(1-q)}.
\]

Hence `B(1/2)=107/135` and `B(1/4)=2504/11475`. The unused-link covariance proof of [H2](../../../round20/forward/h2/report.md) gives

\[
\sigma^2=\|V\Omega\|^2
={\alpha^2\tau^2\over96}B(1/4)
\le {313\alpha^2\over564019200}.
\]

A2 bounds every excited H energy above the absolute threshold

\[
g=\alpha\bigl(1/8-|\tau|B(1/2)\bigr)
\ge {973\alpha\over8640}>0.
\]

Let `P=|Psi><Psi|` and `P_ref=|Omega><Omega|`. On the complement of Psi, H has inverse norm at most `1/g`; using `H Omega=V Omega` gives

\[
d^2:=\|P-P_{\rm ref}\|^2=\|(1-P)\Omega\|^2
\le\sigma^2/g^2
\le {2817\over64377572}<{1\over22500}.
\]

The worst case is the endpoint `|tau|=1/64`: the function `t/(1/8-B(1/2)t)` increases on this positive-denominator interval. Both signs of tau and tau zero are covered. Alpha cancels in this dimensionless comparison; the energy threshold still refers to the fixed positive physical scale `alpha/E_star`.

## 5. A positive perturbed-vacuum variance

The trace-norm distance of these pure-state projections is `2d`. Therefore

\[
|\langle W\rangle_\Psi|\le2d,\qquad
\langle W^2\rangle_\Psi\ge1/4-2d.
\]

Combining the two independently necessary estimates gives

\[
\boxed{\operatorname{Var}_\Psi(W)
\ge1/4-2d-4d^2
\ge {5321\over22500}>{1\over5}.}
\]

The rational bound uses `d<1/150`. Thus `(W-<W>_Psi)Psi` is nonzero, perpendicular to Psi, belongs to `H_cyc`, and is gauge invariant. The physical cyclic space contains more than the vacuum. This is a certified lower bound, not a measured variance or a measured glueball mass. The stronger unrounded bound is not needed for this gate.

## 6. Controls and scope

An open-link trace transforms under independent endpoint gauges and is rejected as a physical observable. A scalar-only algebra has zero centered fluctuations and cannot contain the W just proved. A two-dimensional diagonal subalgebra with vacuum e0 has a one-dimensional cyclic orbit, whereas the full matrix algebra has a two-dimensional orbit; this exact control rejects the inference from full-algebra irreducibility to an arbitrary restricted algebra. A two-level rotation also exhibits nonzero perturbed expectation of an observable with zero reference expectation, rejecting substitution of reference moments for perturbed moments.

The project contribution is the explicit nonvacuous invariant algebra and rational perturbed Wilson-variance guarantee within the admitted summable model. The operator/gauge/GNS tools are established methods; scientific priority is unverified. Equality of `H_cyc` and `H_inv`, a physical-sector representation construction, homogeneous numerical stability and continuum Yang–Mills remain separate obligations. J2 has not been selected or executed here.

Reproduce from the repository root:

```bash
python -B research/round21/forward/j1/check.py --output /tmp/ym21-forward-j1-replay
```
