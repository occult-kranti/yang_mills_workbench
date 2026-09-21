# S2 independent frozen preparation

Prepared against contract `a339228a20375c197f01901e34806fd827cc22fd1e930b740475c15262cd21c2`, without reading current forward/reverse S2 work. The earlier prospective filter note was planning; this is contract-specific skeptical derivation, not producer evidence or an additional loop.

## Full-source filter, sign and graph domain

For bounded self-adjoint A and self-adjoint G, alpha_s(A)=exp(isG)Aexp(-isG) is strongly continuous. The compact filter is a legitimate vectorwise integral and is skew-adjoint, with `||L_Theta||<=Theta||A||/2`. The candidate residual is

`R_Theta=(1/(2Theta)) integral_{-Theta}^{Theta} alpha_s(A) ds`,
`[L_Theta,G]=-A+R_Theta`, `||R_Theta||<=||A||`.

For phi,psi in D(G), differentiate the scalar pairing of alpha_s(A). Only the two unitary vector orbits are differentiated; A need not map D(G) to itself. Piecewise integration by parts uses the jump2 of sign(s)(1-|s|/Theta) at0, derivative -1/Theta off0, and zero values at +/-Theta. This supplies the weak commutator and correct sign. Self-adjointness characterizes D(G): the resulting identity

`<G phi,L psi>=<phi,L G psi+(A-R)psi>`

places L psi in D(G) and gives `G L psi=L G psi+(A-R)psi`. Thus L is graph bounded by `Theta||A||/2+2||A||`, and its exponential and inverse preserve the domain. A proof differentiating G A psi instead would be circular.

For Bohr frequency omega=E_m-E_n, the exact multipliers are

`R_mn=sinc(omega Theta) A_mn`,
`L_mn=(1-sinc(omega Theta))/omega A_mn`,

with sinc(0)=1 and L's continuous zero-frequency value0. Since `[L,G]_mn=-omega L_mn`, the residual sign is fixed. At zero frequency the entire A block remains. R is self-adjoint but not generally positive: sinc has negative intervals. At a fixed nonzero frequency R tends to zero as Theta grows, but that does not justify norm convergence over arbitrarily small frequencies or removal of the actual all-sector residual. The frozen small-Theta regime has no Theta->infinity limit.

## Connected Dyson coefficient sum

In finite volume factor out the full onsite dynamics. With `W(s)=exp(-isH0)exp(isG)`, `W'=i D_I(s)W`, where `D_I(s)=exp(-isH0)Dexp(isH0)`. Each actual D_b(s) keeps its four-site star and norm at most M. Picard expansion of W A W* gives time-ordered nested commutators. No unbounded H0 belongs inside the bounded commutator series. Strong continuity suffices for the vector integrals.

For the family of source stars with norm bound r_*, let N_n denote the root-summed positive 2^|Y| coefficient before its time-simplex factor. Initially `N_0<=64 r_*`. A surviving word attaches each new star to the accumulated union and has at most4+3n sites. Every added commutator costs norm2M and weight at most2^3, hence16M. Splitting the new root between old union and new star gives

`N_(n+1)<=64 M(8+3n)N_n`,
`N_n<=64 r_* (192M)^n (8/3)_n`.

The time simplex contributes exactly |s|^n/n!, yielding the all-order family majorant `64r_*(1-192M|s|)^(-8/3)`. The frozen radius is safe:

`192MTheta<=192*(35/1664)*(1/16)=105/416<1`.

For a declared source family and all indexed connected words, convenient sufficient bounds are

`||L_Theta||_w<=32 Theta r_* (1-192MTheta)^(-8/3)`,
`||R_Theta||_w<=64 r_* (1-192MTheta)^(-8/3)`.

Sharper integrated coefficients divide the evolution coefficients by `(n+1)(n+2)` for L and `(n+1)` for R, with the appropriate Theta powers. An ordinary physical Hilbert norm bound alone would not prove these weighted statements. Repeated anchors, incoming anchors and outer generators meeting only newly generated support remain in this count. Full alpha_G(A) and alpha_H0(A) cannot be interchanged.

The generalized binomial sum follows directly from its coefficient recurrence; it is not a lattice-gap theorem. The same positive series cannot be integrated over all times when its radius condition fails. A finite support bound4+3n without the above root-summed multiplicity is insufficient. Source tau=0 implies A=0; M=0 itself gives the n=0 evolution contribution and does not require dividing by M.

## Infinite-volume identification: additional obligations

Norm stabilization of local Dyson coefficients within the certified radius can define a quasi-local limit. It is not automatically evolution by R2's form-defined G. A possible proof route is to embed finite-volume generators as `G_Lambda'=H0+D_Lambda` on the same product-reference space. Local finite-excitation form-domain vectors have only finitely many interacting stars, so the sandwiched bounded perturbations using (H0+1)^(-1/2) stabilize on a dense set; their uniform norm bound kappa<1 extends this to strong convergence. Neumann inversion then gives strong resolvent convergence. Strong convergence of the unitary groups on compact time intervals identifies the filter and local norm limit with the actual G filter. Each asserted step must be supplied; merely citing pointwise form convergence or interchanging infinite integrals is insufficient. The graph-domain argument for the actual G can then be repeated directly, without claiming D(G)=D(H0).

## Acceptance boundary

The regulated identity is all-sector but retains its explicit residual. It need not reduce the source norm or initiate a contraction. A generic resonant matrix does not show the actual SU2 residual has a nonzero spectral block. The parameter Theta is a dimensionless proof duration; physical time is hbar Theta/delta and resolution is delta/Theta, with delta=alpha/8 fixed. Calibration, later diagonal control, homogeneous gap and continuum construction remain separate.
