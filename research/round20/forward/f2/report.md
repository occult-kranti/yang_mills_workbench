# F2 forward: derivative closure, a specified Hamiltonian, and its missing clock

Use the F1 diffusion family and its Casimir metric, without changing C1's
action or identifying this dynamics with Yang–Mills. Let u,v,q be unit
quaternions, e=(1,0,0,0), and retain x=u0, y=v0, z=q0, w=u·v,
t=v·q. Introduce the **derived observable** r=u·q; it is dimensionless
and is not a new action coefficient or an assumed physical constant.

## Exact differential closure on the shared-middle space

The ambient action gradients are `a=3e+v`, `b=e+u+q`, `d=e+v`.
Tangential projection on each S3, followed by the Casimir factor 1/4, gives

\[
\Gamma S=|\nabla S|^2
=\frac{15+8y+2x+2z+2r-(3x+w)^2-(y+w+t)^2-(z+t)^2}{4}.
\]

Each quaternion coordinate has Casimir Laplacian −3/4 times itself. A
bilinear dot product receives that contribution from both its factors:

\[
\Delta S=-\frac34(3x+y+z+2w+2t).
\]

The middle-factor square contains the mixed contribution `(r−wt)/2`.
It comes from differentiating w and t with respect to their actual common
V. Replacing V by independent copies loses this term and changes the
state space. A second route uses the three left SU2 generators:
their tangent vectors are half the quaternion products of an imaginary
unit with each quaternion. Summing their squared derivatives reproduces
the projected formula; their second derivatives give −3p/4. The checker
compares these two exact derivative routes on rational unit quaternions,
including a fixture with `r−wt=1`.

## Unitary ground-state transform

The map `Uf=sqrt(ρ_κ)f` is unitary from L2(μ_κ) to L2(Haar).
The chain and product rules give on smooth functions

\[
UH_{\kappa,c}U^{-1}
=c\left[-\Delta+\frac\kappa2\Delta S
+\frac{\kappa^2}{4}\Gamma S\right].
\]

The normalized ground is `ψ_κ=e^(κS/2)/sqrt(Z_κ)`. Its kinetic term
divided by ψ is `−κΔS/2−κ²ΓS/4`, canceling the displayed potential
exactly. The smooth potential is bounded on this compact manifold, so
the operator equality extends to the self-adjoint H2 domain. Unitarity
preserves the unique ground and every excitation energy established in F1.

At `u=q=(0,1,0,0)`, `v=(1,0,0,0)`, the exact ΓS is 6 and the
shared contribution is 1/2. Omitting it gives 11/2 and a residual
`−cκ²/8` after division by ψ. This is an executed nonzero failure for
κ≠0, not an undetectable change of notation. Reversing the sign of the
ΔS potential also produces a nonzero residual.

## Exact action range and a conditional energy gap

At fixed y=v0, independent optimization over u and q is legitimate for
the action (while differentiation still uses the shared V). Cauchy–Schwarz
gives the attained extrema

\[
S_{min}(y)=y-\sqrt{10+6y}-\sqrt{2+2y},\qquad
S_{max}(y)=y+\sqrt{10+6y}+\sqrt{2+2y}.
\]

The maximum function is increasing. On (−1,1], the minimum derivative
is `1−3/sqrt(10+6y)−1/sqrt(2+2y)≤−1/4`; continuity handles y=−1.
Both global extrema therefore occur at y=1. They are −5 at U=W=−I,
V=I and 7 at U=V=W=I. Hence **osc(S)=12**, improving the sufficient
oscillation 14 used in F1 without changing any static coefficient.

The same density-comparison proof now yields

\[
\operatorname{gap}(H_{\kappa,c})\ge\frac{3c}{4}e^{-12|\kappa|}.
\]

For `|κ|≤1/8`, the rational Taylor-plus-geometric-tail upper enclosure
in the checker proves `e^(3/2)<9/2`. Taking reciprocals in the correct
direction gives the convenient certified lower bound **gap≥c/6**.
It is a theorem for this chosen finite reversible generator at independently
supplied c>0; it neither measures c nor transfers to the original lattice
Hamiltonian by relabeling c as α.

## What would supply the missing energy coefficient

For a nonconstant real f in the form domain, let C_f(t) be its stationary
centered autocorrelation under `exp(−tcA_κ/hbar)`. Spectral calculus gives
the right derivative `C_f'(0)=−c q_κ[f]/hbar`; strict positive density
and connectedness give q_κ[f]>0. Thus within this fixed scalar family,

\[
c=-\frac{\hbar C_f'(0)}{q_\kappa[f]}.
\]

This requires an independently measured slope in physical time and the
declared metric. No slope has been measured in this project. The κ=0
fixture for f=x merely checks the identity symbolically: q[x]=3/16,
variance=1/4, and `C_x'(0)=−3c/(16hbar)`. Tests reject a missing slope,
q=0, c=0, zero reference energy, an inward exponential enclosure, and
energy assignments from κ/α notation. The added r identity and action
range are model-specific derivations; the ground transform and comparison
principles are standard methods, without a literature-priority claim.
