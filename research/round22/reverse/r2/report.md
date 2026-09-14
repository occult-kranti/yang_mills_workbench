# R2 reverse: boundary-complete vacuum response and its limits

The proposed sandwiched Neumann series is valid for the actual initial
diagonal on the specified product-reference space. It has explicit spatial,
half-energy and response operator-graph tails, and converges from finite
volumes with explicit collar errors. The resulting vacuum rank-two
homological identity cancels `A_Y tensor P_ext`, leaving
`A_Y tensor Q_ext` when compared with the local source extended by identity.
That remainder has norm one on the frozen actual exterior-character test.
The specified positive **volume-weight upper certificate** diverges for
every fixed nonzero tau, although the unweighted response converges.
No all-stage or full homogeneous gap follows. This is the tenth and final
research loop; no subsequent research is selected or executed here.

## 1. Construct the initial form on the actual representation

Write H=H0 and `a=28|tau|`, `g=1-a`. Each onsite space is the actual
24-link I1 factor, with its ten-link selected-strip ground and fourteen free
Haar rotors. The inherited `h_x>=I-P_x` has a unique zero vacuum. Its free
Casimir coefficient is eight in energy unit `delta=alpha/8`. All selected
coupling restrictions and the homogeneous omitted-face coefficient remain
those of R1. The reference is neither a Gauss quotient nor Q2's physical
electric model.

An explicit construction of H on the incomplete product is useful. Split
each factor into its vacuum and its orthogonal complement. The product
space is the orthogonal sum over finite excitation sets Gamma. On the
Gamma summand use the nonnegative finite tensor sum H_Gamma; H is their
self-adjoint direct sum, with domain
`sum_Gamma ||H_Gamma psi_Gamma||^2<infinity`. Its form domain F has
`sum_Gamma ||H_Gamma^(1/2)psi_Gamma||^2<infinity`. Finite-support vectors
from the factor operator domains form an operator and form core. In
particular `H>=sum_x(I-P_x)>=Q`. Its inverse powers on Q are bounded and
preserve every spatial subspace `H(Z) tensor Omega_(Z^c)`; they do not
spread a vector that has vacuum exterior.

Keep every positive-octant star `B_b=b+{0,e_x,e_y,e_z}` and its actual
`D_b=Q_b phi_b Q_b`, `phi_b=-(tau/3)sum_(21 f)W_f`.
The R1 norm bound is `||D_b||<=7|tau|`, and `D_b Omega=0`. For phi,psi in F,

\[
 \sum_b|\langle\phi,D_b\psi\rangle|
 \le7|\tau|\Big(\sum_b\|Q_b\phi\|^2\Big)^{1/2}
                 \Big(\sum_b\|Q_b\psi\|^2\Big)^{1/2}
 \le a\|H^{1/2}\phi\|\|H^{1/2}\psi\|.                 \tag{1}
\]

The last step uses `Q_b<=sum_(x in B_b)(I-P_x)` and four-star incidence.
Thus the infinite sum defines a Hermitian form d, with absolute scalar
convergence; no infinite bounded operator sum D is presumed. Its sum with
the H form is closed on F, since its graph-form norm is equivalent to the
H form norm when a<1. The closed-form representation gives a unique
nonnegative self-adjoint G, with

`D(G^(1/2))=F`, `gH<=G<= (1+a)H`, `G Omega=0`, `G|Q>=g`.

Its operator domain is precisely the vectors psi in F for which
`h(phi,psi)+d(phi,psi)=<phi,f>` for some f and every phi in F; then Gpsi=f.
This statement does **not** identify D(G) with D(H) globally. It proves the
initial G ground and gap on this fixed product representation, not for
the omitted full `H+D+R` model.

On Q, (1) defines the bounded self-adjoint operator K by

`<xi,K eta>=d(H^(-1/2)xi,H^(-1/2)eta)`, `||K||<=a`.

When psi has finite spatial support, only stars meeting that support act
in `D psi=sum_b D_b psi`; this is a finite vector sum. On such vectors the
sandwiched notation `K=H^(-1/2)D H^(-1/2)` has its literal meaning. For
general vectors it denotes the bounded form extension just constructed.

## 2. Prove the proposed inverse and coefficient locality

For `v=v_Y tensor Omega_ext`, `r=||v||`, define

\[
 u=H^{-1/2}(I+K)^{-1}H^{-1/2}v
   =\sum_{n\ge0}u_n,\qquad
 u_n=H^{-1/2}(-K)^nH^{-1/2}v.                         \tag{2}
\]

All inverse powers here are on Q. Since a<1, the bounded Neumann series
converges. For every phi in F intersect Q, substituting (2) into the form
gives `h(phi,u)+d(phi,u)=<phi,v>`. The vacuum component also vanishes.
The domain characterization therefore proves `u in D(G)` and `Gu=v`.
This derives both the plus sign in I+K and the inverse equation, without
assuming that an unsandwiched `D H^(-1)` is globally bounded.

Let `Z_n=Y^(n)` be the frozen octant infinity-norm collars. A star meeting
Z_n is contained in Z_(n+1); a star disjoint from Z_n annihilates a vector
with vacuum exterior. H inverse powers preserve that exterior. Consequently
each u_n is supported in Z_n in this vector sense, is orthogonal to Omega,
and

`||u_n|| <= r a^n`, `||H^(1/2)u_n|| <= r a^n`.             (3)

There is more regularity for these particular coefficients. Initially
`u_0=H^(-1)v in D(H)`. On finite-support vectors the sandwich can be
multiplied as a finite vector sum, giving recursively

`u_n=-H^(-1)D u_(n-1)`, `H u_n=-D u_(n-1)` for n>=1.     (4)

Thus u_n lies in D(H), even when R_Y does not preserve an energy domain.
At most `4|Z|` stars can meet a finite Z, so

`||D w|| <= a |Z| ||w||`

for vectors w supported in Z. Since `|Z_j|<=|Y|(2j+1)^3`, (4) yields

`||H u_0||=r`,
`||H u_n|| <= r |Y| (2n-1)^3 a^n` for n>=1.             (5)

These estimates include every star meeting the previous support, not just
its interior. They hold with the same constants for every finite retained
whole-star volume.

## 3. Explicit tails and response domains

For integer N>=0 define c=2N+1 and

\[
 E_N(a)={a^{N+1}\over g},\qquad
 T_N(a)=a^{N+1}\left\{
 {c^3\over g}+{6c^2a\over g^2}
 +{12ca(1+a)\over g^3}
 +{8a(1+4a+a^2)\over g^4}\right\}.                 \tag{6}
\]

They are zero at a=0. Expanding `(2(N+1+k)-1)^3` and differentiating the
geometric series proves

`T_N(a)=sum_(n>N)(2n-1)^3 a^n
       =a sum_(n>=N)(2n+1)^3 a^n`.

In particular these explicit functions tend to zero for every a<1. With
`U_N=sum_(n=0)^N u_n`, equations (3)–(5) prove

\[
 \|u-U_N\|,\ \|H^{1/2}(u-U_N)\|\le rE_N(a),\qquad
 \|H(u-U_N)\|\le r|Y|T_N(a).                         \tag{7}
\]

The last claim uses completeness of the graph of the closed H: the series
converges in that graph, so the same u from (2) lies in D(H). Also
`sum_n ||D u_n||<infinity` by the second form of T_0. Its vector sum
represents d on this response and equals `v-Hu`. This establishes its
operator equation without claiming global operator-domain equality.

Every U_N is in D(G), because it is in D(H) and has finite spatial support.
Telescoping (4) gives `G U_N=v+D u_N`, and hence the additional G-graph tail

`||G(u-U_N)|| <= r |Y| (2N+1)^3 a^(N+1)`.             (8)

The full graph norm is bounded by the sum of the displayed Hilbert bound
and the corresponding H or G bound. For the required interval
`a<=35/416`, `g>=381/416`; substituting these rational values in (6) gives
uniform constants. The same proofs permit the enlarged initial-model
interval `|tau|<1/28`. At r=0 all coefficients vanish; at tau=0 only
`u_0=H^(-1)v` remains.

## 4. Finite-volume comparison, including boundaries

For a finite cuboid Lambda containing Y, let D_Lambda contain precisely its
retained whole stars. On the full product space use the bounded perturbation
`H+D_Lambda`; its subspace with vacuum outside Lambda reduces it. Its inverse
response is exactly the contract's embedded u_Lambda. The same sandwiched
construction with K_Lambda produces coefficients u_(Lambda,n), obeying
(3)–(5), with vector support in `Lambda intersect Z_n`.

If `Z_N subset Lambda`, then

`u_(Lambda,n)=u_n` for 0<=n<=N.                       (9)

Inductively, all stars meeting Z_(n-1) lie in Z_n and therefore are retained
when n<=N; inverse powers agree after vacuum embedding. Summing the two
tails proves, uniformly over all such containing cuboids,

\[
 \|u-u_\Lambda\|,\ \|H^{1/2}(u-u_\Lambda)\|
   \le2rE_N(a),\qquad
 \|H(u-u_\Lambda)\|\le2r|Y|T_N(a).                 \tag{10}
\]

The embedded u_Lambda is in D(G): it is an H-domain vector with finite
spatial support. Write `D_out=D-D_Lambda` as its finite action on such
vectors. For n<N it annihilates u_(Lambda,n), since all stars that can act
are contained in Lambda. For n>=N its norm on that coefficient is at most
`a r |Y|(2n+1)^3 a^n`. The series is absolutely convergent; for fixed Lambda
D_out is bounded on its spatial subspace. Therefore

`G(u-u_Lambda)=-D_out u_Lambda`,
`||G(u-u_Lambda)|| <= r |Y| T_N(a)`.                 (11)

Any cuboid exhaustion contains each fixed collar eventually. Equations
(10)–(11) establish exhaustion-independent Hilbert, half-energy, H-graph
and G-graph response convergence. They are response estimates, not a
global operator-norm resolvent convergence claim.

## 5. Actual source-sector and omitted-boundary controls

In a finite containing Lambda define the specified global vacuum rank-two
operators. Since `G_Lambda u_Lambda=v_Lambda`, direct domain multiplication
gives

`[S_vac,G_Lambda]=-A_vac`,
`A_vac=A_Y tensor P_(Lambda\Y)`.

The rank-two range lies in D(G_Lambda), so S_vac and its exponential preserve
that domain; the first commutator is bounded. The infinite version likewise
holds on D(G), since u and Omega are in that domain. Against the actual
local source the exact remainder is

`[S_vac,G_Lambda]+A_Y tensor I=A_Y tensor Q_(Lambda\Y)`. (12)

For the frozen origin source `v_Y=chi_e Omega_Y`, use the exterior free
z-character `chi_f` at physical tail `(4,0,0)`, coarse site e_x, and put
`eta=Omega_Y tensor chi_f Omega_ext`. Independent normalized Haar factors
give `||eta||=||v_Y||=1`, `<chi_f>=<chi_e>=0`. Then

`A_vac eta=0`, `(A_Y tensor I)eta=chi_e chi_f Omega`,
`||(A_Y tensor Q_ext)eta||^2=1`.                    (13)

These are actual SU(2) states, preserving the selected-strip ground, not
states from a finite-spin replacement. Their reference energies are 6,
6 and 12 in delta units. Equation (13) holds for both coupling signs and
tau=0; only the response changes with tau. Thus even perfect global vacuum
cancellation does not cancel the local source on an excited exterior.

The origin bare truncation gives another actual control. Only the anchor
zero star can act on `u_0=v/6`, and the R1 conditional free-Haar calculation
retains all 21 faces and their 210 vanishing distinct-face cross moments.
It gives

`||G u_0-v||^2=||D_0 v/6||^2=7 tau^2/432`,
`||H u_1||^2=7 tau^2/432`.                           (14)

Therefore omitting boundary action or truncating to u_0 fails for every
nonzero tau. The opposite first Neumann sign violates (4), with squared
H-image discrepancy `7 tau^2/108`. An inverse norm bound alone would not
detect these wrong constructions. The exact checker reuses only the
hash-bound admitted reverse R1 Haar helper for (14), and independently
checks (13), collars, tail formulas and noncommuting inverse algebra.

## 6. Local operators and the specified volume-weight obstruction

The truncations of the **global** rank-two generator formed from U_N
converge in operator norm with error at most rE_N, but still contain the
global vacuum projector. They are not local operators. One can instead
define a local rank-two skew operator L_n on Z_n, extended by identity,
whose action on Omega is u_n. It has norm `||u_n||<=r a^n`; hence
`L=sum_n L_n` is a norm limit of local bounded operators with
`L Omega=u` and tail at most rE_N. This proves a bounded local-operator
realization of the response, while **not** identifying L with S_vac or
asserting that its commutator cancels the local A on the full Hilbert space.

For the prescribed collar-indexed interaction representation keep support
Z_n. At the origin singleton `|Z_n|=(n+1)^3`. For any fixed mu>0, r>0 and
`0<a<1`, the upper-certificate summand is

`w_n=r exp(mu(n+1)^3) a^n`,
`w_(n+1)/w_n=a exp(mu(3n^2+9n+7)) -> infinity`.

In fact `log(w_n/r)=mu(n+1)^3+n log(a) -> infinity`; the summands do not
tend to zero. Thus this specified upper certificate diverges for every
fixed nonzero tau in the allowed interval. At r=0 it is zero; at tau=0 it
has just its finite n=0 term. For the exact test `mu=log 2`, `tau=1/10000`,
the unweighted majorants decrease at each step, while the weighted terms
first decrease and then increase sharply. Replacing `(n+1)^3` by `1+3n`
changes the declared representation and gives a different certificate.

This is failure of a particular positive upper sum, not divergence of the
actual response norms, impossibility of every connected-support regrouping,
or an all-stage no-go theorem. O2's positive volume weight cannot be
certified by these collar bounds alone. The vacuum-sector identity,
initial-diagonal restriction and remaining excited-exterior operator also
prevent an automatic transfer to its iterative full-source problem.

## Source depth, units and final scope

The primary form reference is Gerald Teschl,
[Mathematical Methods in Quantum Mechanics](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf),
GSM 99, online version 12 February 2009. Theorem 2.13 and its proof
(pp.71–72), Theorem 2.23 (p.79), and Theorems 6.24–6.25 with their proofs
(pp.150–151) were read. Closed semibounded forms and relative form bound
below one are the matched hypotheses. Its displayed inverse signs are
inconsistent with the proof's plus sign; (2) is independently derived by
testing the form equation. Only the closed-form representation and direct
sum results are imported; no locality or quantitative lattice theorem is.
The exact version and reading limits are bound in source-review.json.

All energies above are dimensionless until multiplication by delta=alpha/8.
Keep a_lattice,E_star,alpha/E_star and hbar positive and fixed; the symbol
a in the estimates is only the dimensionless form bound. Physical evolution
uses t/hbar. There is no fitted clock, Q2 transfer, new interacting-ground
representation, full homogeneous stability claim or continuum conclusion.
Scientific priority is unverified. The arbitrary diagnostic class is not
identified with an O1-generated residual.

Normal and optimized Python runs use explicit exceptions and fresh output
directories; their hashes agree. Executable checks supplement the written
infinite-dimensional proof. Current opposite R2 results were not read.
Run `python3 -B research/round22/reverse/r2/check.py --output NEW_DIR` and
the same command with `-O -B` for the optimized replay.
