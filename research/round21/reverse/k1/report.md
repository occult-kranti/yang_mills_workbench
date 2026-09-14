# Reverse K1: a shared density does not fix the reversible dynamics

The mobility operator, transformed potential, gap factor, and two-rate inverse are verified for the declared conditional model. The deformation `m_zeta=1+zeta x` preserves its static density and changes its dynamics. No supplied measurement or reduction identifies this model with the J2 physical lattice generator.

## 1. Recover the operator from reversibility

On compact connected `SU(2)^3`, use the F2 Casimir metric, `S=3x+y+z+w+t`, density `rho=e^(kappa S)/Z`, known `|kappa|<=1/8`, and positive `m=1+zeta x`, `|zeta|<1`. The closed nonnegative weighted form is

\[
q_m[f]=\int \rho m|\nabla f|^2\,dU\,dV\,dW.
\]

Smooth functions form a core; bounded positive smooth coefficients on the compact manifold give the self-adjoint Friedrichs realization of

\[
A_m=-\rho^{-1}\operatorname{div}(\rho m\nabla)
=-m\Delta-\nabla m\cdot\nabla-\kappa m\nabla S\cdot\nabla.
\]

The form vanishes precisely on constants, because `m>=1-|zeta|>0` and the manifold is connected. Thus the zero mode is unique. The energy generator is `c A_m`, with `c>0` in energy units; its imaginary-time exponent is `-tcA_m/hbar`. Changing `c` or `zeta` leaves `rho` unchanged, so static expectations cannot identify either parameter.

## 2. Transform the ground state without dropping mobility derivatives

Multiplication by `sqrt(rho)` is a unitary to the unweighted Haar space. Applying the product rule gives

\[
\boxed{\widetilde H=c\left[-\operatorname{div}(m\nabla)
+\frac\kappa2\operatorname{div}(m\nabla S)
+\frac{\kappa^2}{4}m\Gamma(S)\right],}
\]

with ground function `sqrt(rho)`. The divergence terms mean

\[
-\operatorname{div}(m\nabla)=-m\Delta-\nabla m\cdot\nabla,
\quad
\operatorname{div}(m\nabla S)=m\Delta S+\zeta\Gamma(x,S).
\]

Using the ambient U-gradient `3e0+V` and projection onto the unit-quaternion tangent space,

\[
\Gamma(x,S)=\frac{3+y-x(3x+w)}4.
\]

Retain the F2 shared-middle observable `r=Tr(UW^dagger)/2`:

\[
\Gamma(S)=\frac{15+8y+2x+2z+2r-(3x+w)^2-(y+w+t)^2-(z+t)^2}{4},
\]

and `Delta S=-3(3x+y+z+2w+2t)/4`. The new `grad(m)` contributions cannot be absorbed into a constant clock. At `U=W=(0,1,0,0)`, `V=(1,0,0,0)`, exact tangent projection gives `Gamma(S)=6` and `Gamma(x,S)=1`. Omitting the mobility term in the potential produces residual `-c*kappa*zeta/2` times the ground function, equal to `-1/32` for the checker fixture.

## 3. Preserve the mobility factor in the gap estimate

F2 proves `osc(S)=12`. Comparing the weighted measure with Haar and using the Haar gap `3/4` gives

\[
\Delta\ge\frac{3c}{4}(1-|\zeta|)e^{-12|\kappa|}
\ge\frac{c(1-|\zeta|)}6.
\]

The checker independently encloses `exp(3/2)` from above by a rational Taylor sum plus geometric tail and verifies that it is less than `9/2`. At `|zeta|=1`, the uniform ellipticity premise degenerates; this bound becoming zero does not prove the actual gap vanishes. For `|zeta|>1`, mobility is negative on an open set and the nonnegative form construction fails. The physical ratio `c/E_star` is distinct from `alpha/E_star`; no identification is supplied by equal units.

## 4. Use dynamic observations that discriminate the new variable

For a centered nonconstant form-domain observable, the right derivative of its stationary imaginary-time correlation is

\[
r_f:=-\hbar C_f'(0)=c\int\rho m\Gamma(f).
\]

At `kappa=0`, Haar symmetry gives `E x^(2n+1)=0` and the recurrence `E x^(2n)=[(2n-1)/(2n+2)] E x^(2n-2)`. In particular `E x^2=1/4`, `E x^4=1/8`, and `Gamma(x)=(1-x^2)/4`.

For `f=x` and `g=x+x^2`, centering does not change the gradients. Exact polynomial integration yields

\[
\boxed{r_f=\frac{3c}{16},\qquad
r_g=c\left(\frac5{16}+\frac\zeta8\right).}
\]

In the linear parameters `(p,q)=(c,c*zeta)`, the rate matrix is

\[
\begin{pmatrix}3/16&0\\5/16&1/8\end{pmatrix},
\qquad \det=3/128.
\]

The Jacobian in the original variables `(c,zeta)` instead has determinant `3c/128`. Thus, for valid measured rates with known `kappa=0`,

\[
\boxed{c=\frac{16r_f}{3},\qquad
\zeta=\frac{8r_g}{c}-\frac52.}
\]

The admissible rate region is `r_f>0` and `1<r_g/r_f<7/3`. In contrast, `h=x^2` gives `r_h=c/8`, independent of `zeta`; pairing `x` with `x^2` has rank one. Parity can hide a dynamics deformation even from two observables. A constant observable has zero Dirichlet form and cannot calibrate a clock.

All recovery fixtures here are synthetic exact values. No physical correlation slopes were supplied. For nonzero known `kappa`, the analogous moment matrix must be reconstructed and its determinant/conditioning checked; the Haar inverse must not simply be reused.

## 5. A necessary obstruction to an overly simple physical matching

Multiplication conjugacy by a smooth nonvanishing function changes lower-order coefficients of a differential operator but not its second-order principal symbol. In the same declared coordinates and metric, the transformed diffusion has symbol `c*m_zeta*g^(ij)`, while a constant-mobility rotor has `alpha*g^(ij)`. Equality throughout the coordinate domain requires `c(1+zeta x)=alpha` for all `x`, hence `zeta=0` and the corresponding constant scale equality. The checker rejects an explicit nonzero-zeta fixture by comparing `x=-1` and `x=1`.

This is only a necessary test for **same-coordinate multiplication conjugacy**. It neither proves the infinite gauge lattice reduces to three conditional SU(2) links nor excludes every other coordinate transformation or representation relation. Even `zeta=0` does not complete physical matching.

The checker additionally rejects the nondivergence shortcut: at `kappa=0`, the correct operator gives `A_m x=3x/4+zeta(x^2-1/4)`, with Haar mean zero, whereas dropping `grad(m)` gives mean `3zeta/16`. These exact falsifiers distinguish the claimed operator from an operator with the same static formula written beside it. The contribution is a model-specific rate design and inverse built from established reversible diffusion methods; scientific priority remains unverified.

```bash
python -B research/round21/reverse/k1/check.py --output /tmp/ym21-reverse-k1
```
