# D2 reverse reconstruction: the residual determines the state error

Let `delta=alpha/8`, `s_L=107/135-t_L`,
`beta_L=alpha*|tau|*s_L`, `beta=alpha*|tau|*107/135`, and
`g_L=delta-beta_L`. Require `beta<delta` and the exact A2 zero trial mean.

For each lift `H_L`, the reference-vector compression is at least `g_L`.
The trial mean is zero. Therefore its spectral projection below `g_L` is
nonzero and has rank one: a two-dimensional spectral subspace would contain a
nonzero vector orthogonal to the reference vacuum and contradict the compression
inequality. Its ground eigenvalue `e_L` lies in `[-beta_L,0]`. The same proof
applies to `H`, yielding `e in [-beta,0]`. This argument does not assume compact
resolvent.

There is also a genuine ground vector of the finite-factor operator `K_L`.
Since the exterior reference has ground zero, `inf spec K_L=inf spec H_L=e_L`.
On the subspace orthogonal to the exterior vacuum, the tensor-sum operator is
at least `e_L+delta`. Thus the rank-one ground of the lift lies entirely in
`H_I tensor Omega_out` and yields a unique `K_L` ground vector. Finite factor
count alone would not prove this statement.

The variational principle and `||H-H_L||<=epsilon_L` give
`|e-e_L|<=epsilon_L`. For a normalized exact limiting ground `psi`, put
`P_L=|psi_L><psi_L|` and `Q_L=1-P_L`. Since `Q_L` reduces `H_L` and `e<=0`,

\[
Q_L(H_L-e)Q_L\ge g_LQ_L,\qquad
(H_L-e)\psi=(H_L-H)\psi.
\]

Inverting on `Q_L` consequently gives

\[
\|P-P_L\|=\|Q_L\psi\|\le{\epsilon_L\over g_L},\qquad
|\langle A\rangle-\langle A\rangle_L|\le
2\|A\|{\epsilon_L\over g_L}.
\]

The equality of projector norm and vector leakage uses rank one. The observable
bound uses the exact trace norm `||P-P_L||_1=2||P-P_L||`; it holds for every
bounded operator. A phase choice can additionally give
`||psi-psi_L||<=sqrt(2)*epsilon_L/g_L`. No vector phase is physically identified.

As an independent, weaker route, enclose both ground spectra in the circle of
center `-beta/2` and radius `delta/2`. Its distance from either spectrum is at
least `(delta-beta)/2`. The resolvent identity gives
`||P-P_L||<=2*delta*epsilon_L/(delta-beta)^2`.
The coefficient-rational computation confirms the residual bound is sharper
for every retained cutoff in the specified example.

At fixed `alpha/E_star=2`, `tau=1/64`, all errors are generated for `L=0..8`
from the direct omitted-face class formulas. `epsilon_L` and the energy error
have energy units; projection and normalized observable errors are dimensionless.

The zero-mean premise matters for the sharper denominator. If a positive scalar
perturbation gives `e>0`, the compression of `H_L-e` is only `g_L-e`; the checker
exhibits this failure. Without zero mean, one must separately control e and use
that reduced denominator. A spectral threshold and an eigenvalue gap also differ:
if `e_L<0`, the gap from `e_L` is greater than the threshold measured from zero.
Rank-one identities fail for higher-rank projections. Finally strong-resolvent
convergence alone does not preserve ground projectors: on `ell^2`,
`I-|n><n|` converges strongly (and in strong resolvent) to I while its ground
vectors escape to infinity and its rank-one ground projections converge strongly
to zero. The admitted norm perturbation and isolation estimates exclude that
example.

This closes ground-state convergence for the exact D1 exterior-reference lifts
inside the A2 representation. Original clipped boxes, dense interactions and
continuum Yang-Mills remain outside this claim.
