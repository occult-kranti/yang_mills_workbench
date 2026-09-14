# F2 reverse reconstruction: the observable required by shared-variable derivatives

Use unit quaternions U,V,W and write `r=U dot W=Tr(UW†)/2` in addition to
C1's x,y,z,w,t. This r is a derived observable needed to close the gradient
algebra; it is absent from the static action and does not add an interaction.

With the Casimir metric fixed so a coordinate has eigenvalue 3/4,

\[
\Delta S=-{3\over4}(3x+y+z+2w+2t),
\]

\[
\Gamma(S)=|\nabla S|^2={1\over4}\left[
15+8y+2x+2z+2r-(3x+w)^2-(y+w+t)^2-(z+t)^2\right].
\]

The first derivation uses ambient gradients `3e0+V`, `e0+U+W`, `e0+V`
and projects each onto its unit quaternion tangent space. The second uses the
three left-invariant directional derivatives `D_i U=(e_i U)/2` on each factor.
Their squared derivatives sum to Gamma and their second derivatives sum to
Delta. Exact rational quaternion fixtures compare the two formulations.

Multiplication by `sqrt(rho_k)` is unitary from weighted L2 to Haar L2. Applying
the product rule to that map yields

\[
\widetilde H_{k,c}=c[-\Delta+{k\over2}\Delta S+{k^2\over4}\Gamma(S)],
\qquad\psi_0={e^{kS/2}\over\sqrt{Z_k}}.
\]

The positive ground function is annihilated exactly. This is a ground-state
transform of the added F1 dynamics, not identification with the original
Yang-Mills Hamiltonian. In particular the resulting potential contains derived
quadratic observables and shared-variable terms.

For fixed V with y=V0, minimizing over U and W independently gives
`m(y)=y-sqrt(10+6y)-sqrt(2+2y)`. For -1<=y<=1 the positive tangent bounds

\[
\sqrt{10+6y}\le(13+3y)/4,\qquad
\sqrt{2+2y}\le(3+y)/2
\]

follow by squaring: the differences are `9(1-y)^2/16` and `(1-y)^2/4`.
Therefore `m(y)>=-5+(1-y)/4>=-5`. Equality is attained at V=I,U=W=-I.
The upper bound S<=7 is attained at all three identities. Hence the exact range
is `[-5,7]`, with oscillation12, although the absolute bound7 remains needed for
the original Taylor remainder.

For m<=rho<=M, `Var_rho(f)<=M Var_Haar(f)` and
`q_rho[f]>=m q_Haar[f]`. The Haar Poincare inequality then gives

\[
\operatorname{gap}(H_{k,c})\ge{3c\over4}e^{-12|k|}.
\]

An independently constructed exact rational Taylor-plus-geometric upper bound
E for exp(3/2) satisfies `E<9/2`. Thus for every `|k|<=1/8`,
`gap>=3c/(4E)>c/6`; the weaker closed certificate `gap>=c/6` is admitted.
This step requires an upper exponential bound because it appears in the lower
bound's denominator. It neither infers c nor calibrates it from alpha.

A sufficient added dynamic observation is the stationary centered correlation
`C_f(t)=<f,exp(-tcA_k/hbar)f>_rho` for nonconstant form-domain f. Its right
initial derivative is `C_f'(0)=-c*q_k[f]/hbar`. If that derivative is measured
in declared physical time units and q_k[f]>0, it identifies

\[
c=-\hbar C_f'(0)/q_k[f].
\]

No such measurement is supplied here. The executable numerical recovery is
explicitly a synthetic algebra test, not empirical calibration.

Dropping r, or deleting the shared-V cross derivative `(r-wt)/2`, changes the
ground-state residual at explicit fixtures. Flipping the DeltaS potential sign
also changes it. The checker retains these failures, the metric factor1/4,
signed k, inward exponential bounds, c=0, zero E_star and unsupported matching
claims. The identities and range are model-specific derivations; no literature
priority or continuum theorem is asserted.
