# Reverse J1: a physical Wilson fluctuation in the perturbed vacuum

The exact positive bound `Var_Psi(W)>=5321/22500>1/5` passes for the frozen dyadic model and all `|tau|<=1/64`. This is a bound on a specified observable in the constructed vacuum, not a measured mass or a claim that the full and physical Hilbert spaces coincide.

## 1. Fix the model and define the required gauge action

We explicitly return to A2/E/G: fixed-spacing SU(2), positive `alpha/E_star`, the selected-strip reference, and omitted coefficients `alpha*tau/(24*2^(x+y+z))`. The perturbation is bounded and summable. I1's homogeneous model and its unevaluated coupling interval are not used.

For a finite-support assignment of vertex group elements `g_v`, an oriented link transforms as `U_(v,w) -> g_v U_(v,w) g_w^-1`. Pullback gives a unitary on the full Haar link space. A finite-support gauge transformation touches finitely many links and hence finitely many complete reference factors. Electric Casimirs commute with both endpoint actions; the group factors telescope around any closed Wilson loop, leaving its trace invariant.

Each unique selected-strip ground vector is invariant: its one-dimensional eigenspace carries a continuous character of a finite product of SU(2), and every such character is trivial. Each free Haar vector is invariant as well. Therefore the reference product vacuum and its incomplete tensor-product representation carry the finite-support gauge action. The same argument applies to the unique perturbed ground `Psi`: its Hamiltonian commutes with the gauge action and its ground eigenspace is one-dimensional, so `Psi` is invariant.

Let `C` be the algebraic finite-excitation tensors with smooth vectors on complete local factors and reference ground vectors outside. The finite compact rotor Hamiltonians have smooth ground functions; their smooth domains are cores. Finite spectral/tensor truncation gives a core for the nonnegative reference sum. The finite-support gauge action preserves `C`, the reference operator domain, and its form domain. Since `V` is bounded, `D(H)=D(H_ref)` and `Q(H)=Q(H_ref)`; `C` is a common core. Gauge commutation extends from `C` to these closed domains. This **does not** assert that `V` maps algebraic finite excitations into themselves: its infinite tail need not. Nor does every bounded local observable preserve an energy domain.

## 2. Keep the three Hilbert-space constructions distinct

Let `A_phys,loc` contain every bounded finite-reference-factor observable invariant under every finite-support vertex gauge transformation, and let `A_phys` be its norm closure. The reference/perturbed dynamics from G1/G2 maps the full quasilocal algebra into itself and commutes with the gauge action; hence it preserves `A_phys`.

Define

\[
\mathcal H_{\rm fix}=\{\xi:U_g\xi=\xi\text{ for every finite-support }g\},
\qquad
\mathcal K_{\rm phys}=\overline{\mathcal A_{\rm phys}\Psi}.
\]

Vacuum invariance and observable invariance give `K_phys subset H_fix subset H`. Equality is not assumed. G2's irreducibility proof concerns the **full** bounded factor algebra; restricting to invariant observables does not inherit that proof. The identity belongs to `A_phys`, so the physical cyclic space contains the vacuum; a nonzero fluctuation is still needed to prove that it contains an excitation.

## 3. Choose an actual closed loop and prove its reference moments

Choose the xz square with vertices `(0,0,0),(1,0,0),(1,0,1),(0,0,1)`, and write `W=Tr(U_square)/2`. It is omitted because it is not an xy selected face. It is a bounded self-adjoint gauge-invariant observable with `||W||=1`. Its two z links are free Haar factors of the reference product even though its x links can touch dressed strips.

Integrate one free z link conditionally on all other links. Haar invariance gives `omega_ref(W)=0`, while the four equal quaternion-coordinate second moments yield `omega_ref(W^2)=1/4`. Smooth bounded Wilson multiplication on finitely many links preserves the common form domain, using the product derivative rule and bounded first derivatives. Thus the forthcoming fluctuation can also be viewed as a finite-energy physical vector.

Reference variance alone would be insufficient: a different state could be an eigenstate of `W` and have zero variance. The following estimate controls the **actual perturbed** state.

## 4. Bound the actual ground projection using its residual

The inherited exact omitted ledger is

\[
B(q)=\frac{2+5q+5q^2+6q^3+3q^4}{24(1-q)^3(1+q)^2(1+q^2)}.
\]

H2's free-link cancellation mechanism gives `sigma^2=||V Omega_ref||^2=alpha^2 tau^2 B(1/4)/96`. Exact rational evaluation gives

\[
B(1/2)=107/135,\quad B(1/4)=2504/11475,
\quad {\sigma^2\over\alpha^2}\le{313\over564019200}.
\]

A2 places the entire excited spectrum above the **absolute** energy threshold

\[
g=\alpha\left(\frac18-\frac{107}{135}|\tau|\right)
\ge\frac{973\alpha}{8640}>0.
\]

Let `P` be the actual ground projection and `P_ref` the reference projection. On `ran(1-P)`, the operator `H` is invertible with inverse norm at most `1/g`. Since `H Omega_ref=V Omega_ref`,

\[
d:=\|P-P_{\rm ref}\|=\|(1-P)\Omega_{\rm ref}\|
\le\sigma/g,
\qquad
d^2\le{2817\over64377572}<\frac1{22500}.
\]

The right side is maximal at `|tau|=1/64`: the numerator increases with `|tau|` and the positive denominator decreases. This proves the continuous signed interval, rather than inferring it from samples. At zero coupling the residual and projector distance vanish.

## 5. Transfer both moments and subtract the perturbed mean

For rank-one projections, the trace distance is `||P-P_ref||_1=2d`. Thus for any bounded observable `A`, the expectation change is bounded by `2d||A||`. Apply this separately to `W` and `W^2`:

\[
\langle W^2\rangle_\Psi\ge\frac14-2d,
\qquad |\langle W\rangle_\Psi|\le2d.
\]

Subtracting the **actual** perturbed mean square and using `d<1/150` gives

\[
\boxed{\operatorname{Var}_\Psi(W)
\ge\frac14-2d-4d^2
\ge\frac{5321}{22500}>\frac15.}
\]

Consequently `(W-<W>_Psi)Psi` is a nonzero vector, invariant under finite-support gauge transformations, orthogonal to the vacuum, and in `K_phys`. This proves a nonvacuum physical fluctuation without asserting that the first full-space charged level is a glueball. The bound is dimensionless because `W` is dimensionless; the energy lower scale remains `973alpha/8640`.

## 6. Exact controls and scope

The checker evaluates every rational constant, all signed endpoint inequalities, the actual square's center-gauge cancellations, and four rejecting cases. An open-link trace flips sign under a center transformation at one endpoint and is excluded. A scalar-only algebra has zero variance. A two-state example has reference variance `1/4` but perturbed variance zero, rejecting reference-only inference. The diagonal subalgebra of `M2` has a nonscalar commutant and a one-dimensional orbit of a basis vector, rejecting transfer of full-algebra irreducibility to a subalgebra. These finite fixtures illustrate failures of premises; the proofs above cover the infinite model.

The physical cyclic GNS identification and its restricted energy generator are the next loop's task. No equality of full and physical spaces, representation-independent homogeneous conclusion, numerical mass measurement, or continuum result follows here. This is an application of established gauge and trace-distance arguments with a project-specific exact positive margin; scientific priority is unverified.

```bash
python -B research/round21/reverse/j1/check.py --output /tmp/ym21-reverse-j1
```
