# O2 forward: arbitrary-support elimination and a quantified certificate obstruction

The homological map and a complete weight-loss iteration majorant are proved.
The specified bare-reference route does not close through this majorant: a
retained linear diagonal/residual term eventually defeats every positive-limit
weight schedule of the stated type. At the explicit coupling `tau=2^(-22)`,
the controlled recurrence first loses its series condition at step 42, after
an initial decrease. This is failure of this certificate, not proof that the
actual iteration or the homogeneous spectral gap fails. The numerical-gap
target remains limited.

This is an independent forward O2 derivation before any current reverse O2
solution was read. O1 and its review are inherited. No next loop is selected.

## Fixed model and initial bounds

Keep the homogeneous full-link I1/I2/O1 model with the same complete-star
finite-cuboid boundary. The underlying site spaces are separable and may be
infinite dimensional; `H_0=sum_x h_x`, `h_x>=I-P_x`, and the product ground
is Omega. All generated supports are arbitrary finite unions of these sites.
They are never reset to four-site stars. The actual finite-volume operator
domain is D(H_0). There is no canonical q profile here.

Normalized energies, D,R,S and tau are dimensionless. Physical Hamiltonians
are multiplied by `delta=alpha/8`, with fixed positive E_star, alpha/E_star,
hbar and spacing. Exponential support weights are proof choices, not changes
to the action, geometry or clock. Let

\[
\|B\|_\mu=\sup_x\sum_{Y\ni x}e^{\mu|Y|}\|B_Y\|,
\quad K=25460736/25,
\quad r_0=K\tau^2,\ d_0=448|\tau|,\ \kappa_0=28|\tau|.
\tag{1}
\]

The admitted common O1 interval is `|tau|<=5/1664`. It gives
`H_1=H_0+D_0+R_0`, `||R_0||_(log2)<=r_0`,
`||D_0||_(log2)<=d_0`, and relative form bound kappa_0 for D_0. Every
local D_0 term annihilates its local vacuum. These d and r values are
upper certificates, not equalities for the physical interaction norms.

## Arbitrary-support splitting and the domain-safe inverse

For any bounded self-adjoint local R_Y, with nonempty finite Y, set
P=|Omega_Y><Omega_Y|, Q=I-P, `c=<Omega_Y,R_Y Omega_Y>`,
`v=Q R_Y Omega_Y`, and

\[
A_Y=|v\rangle\langle\Omega_Y|+|\Omega_Y\rangle\langle v|,
\quad Z_Y=Q(R_Y-cI)Q,
\quad u=(H_{0,Y}|_Q)^{-1}v,
\quad S_Y=|u\rangle\langle\Omega_Y|-|\Omega_Y\rangle\langle u|.
\]

Because `H_(0,Y)|Q>=1`, the bare inverse exists, has norm at most one,
and maps v into D(H_(0,Y)). There is no assumption about a gap of the
already perturbed Hamiltonian in this inverse. Direct block multiplication
proves

\[
R_Y=cI+A_Y+Z_Y,\quad Z_Y\Omega_Y=0,\quad[S_Y,H_0]=-A_Y,
\]
\[
|c|\le\|R_Y\|,\quad\|A_Y\|=\|v\|\le\|R_Y\|,
\quad\|S_Y\|\le\|R_Y\|,\quad\|Z_Y\|\le2\|R_Y\|.
\tag{2}
\]

In finite volume, norm-summable indexed terms may first be grouped by their
finitely many possible support sets; all maps in (2) are linear in R_Y and
triangle bounds retain the original multiplicities. As in O1, the bounded
local products with H_(0,Y) and strong commutation with the exterior energy
give `S_Y D(H_0) subset D(H_0)` and
`H_0 S_Y=S_Y H_0+A_Y` there. The sum X of the local generators is bounded
in the H_0 graph norm. Indeed in a finite volume,
`sum_Y ||R_Y|| <= |Lambda| e^(-mu) ||R||_mu`, so both X and its first
commutator converge absolutely. Thus `exp(plus/minus X)` preserves D(H_0).
No arbitrary bounded local operator is asserted to preserve this domain.

The scalar `C=sum_Y c_Y` is retained as a finite-volume energy shift.
It satisfies `|C|/|Lambda|<=e^(-mu) r`. It need not be the true ground
energy while a residual remains. Defining `D'=D+sum_Y Z_Y`, direct
bounded-commutator integration, before expansion, gives

\[
e^X(H_0+D+R)e^{-X}=H_0+D'+CI+R',
\]
\[
R'=\sum_{k\ge1}\left\{
 \frac{\operatorname{ad}_X^k(D+R)}{k!}
 -\frac{\operatorname{ad}_X^k A}{(k+1)!}\right\}.
\tag{3}
\]

The first term includes `[X,D]`. Omitting it is not the frozen algorithm.
No unbounded H_0 is inserted into an operator-norm series.

## Why equal weight fails, and an all-support loss estimate

A universal estimate `||[S,B]||_mu<=C_mu||S||_mu||B||_mu` at one fixed
weight is false even for onsite homological generators and a vacuum-annihilating
diagonal B. On m qubits let `J=|1><0|-|0><1|`, `X=sum_i J_i`,
`P=product_i Z_i`, and `B_Y=e^(-mu m)(P-I)/2`. Each J_i is the bare
homological generator of `|1><0|+|0><1|` for `h_i=|1><1|`. Then
`||X||_mu=e^mu`, `||B||_mu=1`, and

\[
[X,B_Y]=e^{-\mu m}XP,\qquad\|XP\|=m,
\qquad\|[X,B]\|_\mu=m.
\tag{4}
\]

The norm equality follows because the commuting J_i have a common vector
with eigenvalue i for each site. Hence the ratio is `m/e^mu`, unbounded
as m grows. B annihilates the all-zero vacuum. This is a general-class
counterexample, not a claimed SU(2) matrix element.

For `mu'=mu-delta_w>0`, a valid bound is

\[
\boxed{\|[S,B]\|_{\mu'}\le
 \frac4{\delta_w}\|S\|_\mu\|B\|_\mu.}
\tag{5}
\]

To prove it, retain every indexed pair of intersecting supports Y,Z and
declare their union as the commutator support. Split the root condition into
x in Y and x in Z. The first sum is bounded by
`2 ||B||_(mu') sup_x sum_(Y contains x) |Y| exp(mu'|Y|)||S_Y||`,
and the second is its interchanged analogue. The inequality
`m exp(-delta_w m)<=1/delta_w` gives (5), with harmless double counting.
There is no cardinality restriction or hidden bounded-support reset.

Allocate a total loss delta_w equally among k nested commutators and apply
(5) repeatedly. If `s=||S||_mu` and `b=||B||_mu`,

\[
\frac{\|\operatorname{ad}_X^k B\|_{\mu-\delta_w}}{k!}
\le\frac{k^k}{k!}(4s/\delta_w)^k b
\le(12s/\delta_w)^k b.
\tag{6}
\]

The last conservative constant follows from
`log(k!)>=integral_1^k log x dx`, giving `k^k/k!<=e^(k-1)<3^k`.
The indexed expansion includes each ordered overlapping history and its
union; disjoint commutators vanish and all others retain their multiplicities.

Put `rho=12r/delta_w`, using s<=r from (2). Summing (3) and bounding
`1/(k+1)<=1/2` proves the complete one-step majorant

\[
\boxed{r'\le(d+3r/2)\frac{\rho}{1-\rho},\quad
 d'\le d+2r,\quad\kappa'\le\kappa+2r,\quad\rho<1.}
\tag{7}
\]

Here d' and r' are measured at the new weight. The relative update uses
`Q_Y<=sum_(x in Y)(I-P_x)` and the root sum of `||Z_Y||`, bounded by
`2e^(-mu)r<=2r`. In particular all updated D terms still annihilate their
local vacuum. The estimate requires only the bare reference inverse gap one;
`kappa<1` is the separate sufficient gap condition for H_0+D, not for H_0+D+R.

## Frozen schedule, recurrence, and its precise obstruction

The prescribed weights satisfy

\[
\mu_n=\frac{\log2}{2}+\frac{\log2}{2(n+1)},\quad
\delta_n=\frac{\log2}{2(n+1)(n+2)},\quad
\sum_{n\ge0}\delta_n=\frac{\log2}{2},\quad
\mu_\infty=\frac{\log2}{2}>0.
\tag{8}
\]

Taking equality on the right of (7), with rho_n=12r_n/delta_n,
defines the real-valued scalar certificate to test. It cannot hold forever
with rho_n<1 for any d_0>0,r_0>0. In fact d_n>=d_0 and

\[
\frac{r_{n+1}}{r_n}\ge\frac{12d_0}{\delta_n}
=\frac{24d_0(n+1)(n+2)}{\log2}\longrightarrow\infty.
\tag{9}
\]

If rho_n<1 held for all n, eventually the ratio would be at least two.
Since every finite preceding r_n is positive, the subsequent sequence would
grow geometrically while delta_n tends to zero, contradicting rho_n<1.
Thus this majorant necessarily exits its admissibility region. This argument
also covers any other positive summable loss schedule in this same majorant,
since delta_n tends to zero. It says nothing about a sharper estimate that
removes or controls the retained linear term differently. At tau=0 the
residual vanishes identically and this obstruction does not apply.

The linear source is genuine in the general operator class. In one qubit,
take `D=d|1><1|`, `R=r X`, and the bare generator rJ. Then
`[rJ,D]=-dr X`. The exact transformed offdiagonal entry is
`r cos(2r)-(1+d)sin(2r)/2=-dr+O(r^3)` at fixed d>0. It cannot obey a
uniform purely quadratic bound in r. A scalar subtraction does not change
that entry. Replacing the inverse with the gap 1+d repairs this toy's
first-order cancellation, but doing so on overlapping generated supports
requires a new full domain/inverse/commutator proof; it is not silently
substituted here.

## A controlled numerical example

For computation use the weaker rational loss
`delta_hat_n=1/[3(n+1)(n+2)]<delta_n`. The strict inequality follows from
`log2>2/3`, for example from the strict midpoint bound for the convex
function 1/x on [1,2]. The allocated weights remain exactly (8); using a
smaller allowed loss only makes the bound more conservative. Therefore the
fully rational recurrence

\[
\lambda_n=36(n+1)(n+2),\quad\widehat\rho_n=\lambda_n\widehat r_n,
\quad\widehat r_{n+1}=(\widehat d_n+3\widehat r_n/2)
 \widehat\rho_n/(1-\widehat\rho_n),
\quad\widehat d_{n+1}=\widehat d_n+2\widehat r_n
\tag{10}
\]

is also valid while its rho is below one. Initialize with the exact O1
upper values at `tau=2^(-22)`. Directed rational rounding on the grid
`2^(-256)` encloses (10), without floating-point or sampled-limit claims:

* Step 0 has `4.1681528e-6 < rho_hat_0 < 4.1681529e-6`.
* The smallest residual before stopping occurs at step 15, enclosed between
  `9.56163e-19` and `9.56165e-19`.
* Step 41 still has `0.184436 < rho_hat_41 < 0.184437`.
* Step 42 has `1.727758 < rho_hat_42 < 1.727759`, so (10) no longer
  permits another step. Its tracked relative coefficient remains below
  `1/1000`; the loss-series condition fails first.

The checker verifies each stated rational enclosure and the earlier rho<1
conditions. This is the first failure index of the conservative rational
recurrence, not necessarily of the less conservative exact-log recurrence.
Equation (9) separately proves eventual failure for the exact-log recurrence.
The norm r_n in these computations is an upper certificate, never a measured
physical remainder. Directed rounding error is bounded by the displayed
enclosures and does not cause the conclusion rho_hat_42>1.

Scalar increments are retained at every finite step with intensive bound
`|C_n|/|Lambda|<=e^(-mu_n)r_n`. If a different valid majorant achieved
`sum_n r_n<infinity`, all rho_n<1, and
`kappa_0+2sum_n r_n<1`, then the finite-volume transformations would
converge in norm and graph norm, the scalar and diagonal series would
converge, and the final product-vacuum Hamiltonian would have gap at least
`1-kappa_infinity`. This conditional finite-volume argument follows by
summing the bounds in (2) and (7). The present recurrence fails its premises.
Even that conditional construction would not be an infinite global unitary
or a summable-ITP representation transfer.

## Evidence, sources, and remaining scope

The checker supplies exact scalar/splitting/commutator matrices, the growing
support rejection of an equal-weight constant, a retained-D control, and the
directed rational recurrence above. It explicitly retains scalar energies
and both diagonal/mixing blocks. These lemma controls do not simulate SU(2)
or prove a physical gap failure.

Closest checked prior work is the accepted O1 operator-domain and all-order
rotation argument. Its `source-notes.md` records targeted primary reading
of Yarotsky's relative/bounded split and polymer proof, and the
multidimensional unbounded Lie-Schwinger domain lemma. That reading did not
evaluate the required full iterative constants, and no such theorem is
imported now. Equations (2)–(10) are proved directly from block algebra,
rooted support sums and elementary series estimates. No new specialized
source result is needed to assert the certificate obstruction. Scientific
priority is unverified; this is a scoped estimate and obstruction in a
declared iteration, not an exhaustive impossibility result.

The missing premise is a valid treatment of the retained diagonal interaction
in the homological step, or a support/inverse estimate that avoids the
accumulating linear loss. Numerical homogeneous stability, actual algorithm
failure, actual gap failure, physical matching and continuum Yang–Mills
claims remain unproved. Ordinary and optimized fresh runs are compared;
only the ordinary output and a compact optimized hash summary are retained.

```bash
python3 -B research/round22/forward/o2/check.py --output /absolute/new/o2-forward
python3 -B -O research/round22/forward/o2/check.py --output /absolute/new/o2-forward-optimized
```
