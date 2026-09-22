# Reverse J2: the physical cyclic space equals the invariant space here

For the J1 dyadic summable model and its **full bounded local invariant algebra**, `K_phys=H_inv`, while both are proper subspaces of the full Hilbert space. The physical vacuum GNS generator is the self-adjoint restriction of `H-e`. This result uses local averaging and full-algebra cyclicity, not a transfer of full-space irreducibility to the invariant algebra.

## 1. Reconstruct the missing reverse inclusion

J1 supplies an invariant vacuum `Psi`, the finite-support vertex SU(2) gauge action `U_g`, and `K_phys=closure(A_phys Psi) subset H_inv`. G2 supplies cyclicity of `Psi` for the full bounded reference-factor quasilocal algebra. Therefore, for any `xi in H_inv` and `epsilon>0`, there is a bounded local operator `A` with `||A Psi-xi||<epsilon`.

Let `E` be the finite union of all links in the complete reference factors supporting `A`, and let `V(E)` contain every endpoint of those links. Average over the compact finite product `G_E=product_(v in V(E)) SU(2)`:

\[
\mathbb E_E(A)=\int_{G_E}U_g A U_g^*\,dg.
\]

This is not assumed to be a norm-Bochner integral in the bounded-operator space. The representation is strongly continuous, so each vector-valued integrand is continuous and bounded; equivalently define the integral by its scalar matrix elements. It gives a bounded weak/strong-operator integral with `||E_E(A)||<=||A||`. Conjugating `A` leaves its operator support inside the same link union `E`: gauge actions on links outside `E` commute through `A`. The local algebra `B(H_E) tensor I_out` is strongly closed, so the average remains local.

Haar invariance makes the result commute with every endpoint gauge transformation. Vertices outside `V(E)` act trivially on this local operator. Hence `E_E(A)` belongs to the **full** gauge-invariant local algebra. Since both `xi` and `Psi` are invariant,

\[
\|\mathbb E_E(A)\Psi-\xi\|
=\left\|\int_{G_E}U_g(A\Psi-\xi)\,dg\right\|
\le\|A\Psi-\xi\|<\epsilon.
\]

Thus `xi in K_phys`, proving

\[
\boxed{\mathcal K_{\rm phys}=\mathcal H_{\rm inv}.}
\]

The premise concerning the observable algebra matters: a smaller scalar-only or selected-Wilson algebra need not contain these averaged approximants. We establish no analogous equality for every proposed gauge observable algebra.

## 2. The invariant space is still strictly smaller than the full space

Choose a free z link and multiply the reference vacuum by a nonzero fundamental matrix coefficient of that link. Its Haar norm is positive. A gauge-center element `-I` at one endpoint flips this vector's sign, while the reference vacuum remains invariant. Therefore a nonzero charged vector belongs to the full representation and is absent from `H_inv`. Consequently `K_phys=H_inv` is a proper subspace of `H`. J1's positive Wilson variance also ensures that `K_phys` is larger than the vacuum line.

## 3. Construct the physical GNS map and its generator

For the restricted state `omega(A)=<Psi,A Psi>` on `A_phys`, the GNS null left ideal is

\[
\mathcal N=\{A:\omega(A^*A)=0\}=\{A:A\Psi=0\}.
\]

The map `[A] -> A Psi` is well-defined and isometric from the null quotient. Its completion is onto `K_phys` by definition, and it intertwines the GNS representation with the restricted algebra action. No full-space cyclicity is asserted for this smaller algebra.

Let `e` be the actual ground energy. The full gauge-commuting unitary group fixes `Psi` after this subtraction and maps `A_phys` into itself. Thus

\[
e^{it(H-e)/\hbar}A\Psi=\alpha_t(A)\Psi\in\mathcal K_{\rm phys}.
\]

The same statement holds for negative time, so `K_phys` is reducing for this unitary group. Its orthogonal projection commutes with the group and hence with the spectral resolution of `H`. It follows that

\[
\boxed{K=(H-e)|_{\mathcal K_{\rm phys}},\qquad
D(K)=D(H)\cap\mathcal K_{\rm phys}}
\]

is self-adjoint. The GNS implementer is the strongly continuous group `exp(itK/hbar)`, and its Stone frequency generator is `K/hbar`. The cyclic ground vector is fixed, `K Psi=0`, and the inherited lower inequality restricts to this reducing space:

\[
\operatorname{spec}(K)\subset\{0\}\cup
\left[\frac{973\alpha}{8640},\infty\right).
\]

The zero eigenspace is one-dimensional. Arbitrary bounded local `A` need not put `A Psi` in `D(K)`; the null quotient is a Hilbert-space construction, not an unqualified operator-domain claim. Subtracting `e` is necessary for the canonical implementing vector to be fixed, even though scalar energy shifts cancel from Heisenberg conjugation.

## 4. Bound a connected imaginary-time correlator

Use the actual J1 Wilson loop and `chi=(W-omega(W))Psi`. J1 gives `chi in K_phys`, `chi perpendicular Psi`, and `||chi||^2=Var_Psi(W)>=5321/22500>0`. For finite `t>=0`, define

\[
C_W(t)=\langle\chi,e^{-tK/\hbar}\chi\rangle.
\]

Its spectral measure is positive, nonzero, and supported in `[g,infinity)`, where `g=973alpha/8640`. The function `exp(-tE/hbar)` is strictly positive at every finite spectral value and bounded above by `exp(-tg/hbar)` on this support. Therefore

\[
\boxed{0<C_W(t)\le\operatorname{Var}_\Psi(W)
\exp\!\left(-\frac{973\alpha t}{8640\hbar}\right)}
\]

for every finite `t>=0`. This is an upper decay estimate with a positive equal-time amplitude, not an identification of the lowest overlapping excitation or a measured glueball mass. In real time the spectral phase has unit magnitude; a positive gap does not imply exponential decay of the correlator's magnitude.

## 5. Exact finite controls

The checker uses a three-dimensional finite example with symmetry `diag(1,1,-1)` and vacuum `e0`. The invariant algebra is `M2 direct-sum C`; its vacuum GNS Gram matrix has rank two and nullity three, while the full Hilbert space has dimension three. Exact group averaging deletes the charged matrix entries.

For `H=diag(-2,1,0)`, the physical restriction of `H-e` is `diag(0,3)`. The unsubtracted operator fails to annihilate the ground vector. A projection onto `span{e0,e1+e2}` fails the exact commutator test and cannot be treated as a reducing spectral restriction. For `W=(E01+E10)/2`, the connected imaginary-time values at `t/hbar=n log 2` are exactly `(1/4)2^(-3n)`, bounded by `(1/4)2^(-2n)`. The real-time correlator returns to `1/4` at `t/hbar=2pi/3`, rejecting gap-implies-real-time-decay.

These are finite logical controls, not substitutes for the SU(2) Haar proof. The result is restricted to the established dyadic summable representation, fixed spacing, and positive physical energy scale. Homogeneous and continuum representation matching remain open. The averaging/GNS/spectral methods are established mathematics; the workbench contribution is their completed, explicitly bounded application here, with scientific priority unverified.

```bash
python -B research/round21/reverse/j2/check.py --output /tmp/ym21-reverse-j2
```
