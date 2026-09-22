# O1 forward: simultaneous homogeneous rotation with all supports retained

The finite-volume simultaneous rotation is well defined on the unbounded
reference domain and admits the explicit volume-independent bound

\[
\boxed{\|R_\Lambda\|_w\le\frac{25460736}{25}\tau^2
 \quad\text{for }|\tau|\le\frac5{1536}.}
\tag{1}
\]

The first-order retained diagonal part has relative form bound `28|tau|`.
These are proved operator/interaction estimates. They do not yet prove a
numerical homogeneous spectral-gap interval or an iterative contraction:
the remainder is not purely relative, and its generated supports leave the
initial four-site class. The numerical-stability target is therefore limited.
This forward derivation precedes current O1 reverse/skeptic exchange; O2 is
not selected or executed.

## Frozen model and inherited ingredients

Use the homogeneous I1/I2 model, not the canonical summable N model.
The coarse positive-octant sites each own the complete 24 physical links
with tails `(4i+r,2j+s,k)`, `0<=r<4,0<=s<2`. These comprise one whole
ten-link selected strip and fourteen free-link factors. In a finite cuboid
Lambda retain exactly anchors b whose full star
`S_b=b+{0,e_x,e_y,e_z}` lies in Lambda. All 21 omitted anchored faces enter
`phi_b=-(tau/3) sum_f W_f`, with the same real homogeneous tau. Outgoing
owned links and the exact whole-star boundary remain part of the model.

The normalized onsite Hamiltonians obey `h_x>=I-P_x`, `h_x Omega_x=0`,
and are self-adjoint, generally unbounded, on the actual separable block
spaces. Let `H_0=sum_(x in Lambda) h_x`, with its finite-sum operator
domain and product ground Omega. The normalized energy unit is
`delta=alpha/8`. E_star>0, alpha/E_star>0, hbar>0 and spacing a>0 remain
fixed. Multiply a Hamiltonian or remainder below by delta for physical
energies; no time or coupling is fitted. The weight 2 in the requested
interaction norm is a fixed dimensionless proof device, not a physical
parameter.

I2 supplies, on each retained complete star,

\[
v_b=\phi_b\Omega_{S_b},\quad\|v_b\|^2=7\tau^2/12,\quad
u_b=(H_{0,S_b}|_Q)^{-1}v_b,
\]
\[
S_b=|u_b\rangle\langle\Omega_{S_b}|-
 |\Omega_{S_b}\rangle\langle u_b|,\quad
A_b=|v_b\rangle\langle\Omega_{S_b}|+
 |\Omega_{S_b}\rangle\langle v_b|.
\]

All act as identity on complementary tensor factors where appropriate.
Write `X=sum_b S_b`, `Phi=sum_b phi_b`, `A=sum_b A_b`, and
`D=sum_b Q_(S_b) phi_b Q_(S_b)=Phi-A`. The star-vacuum mean is zero.
The bounds used below are

\[
\|\phi_b\|\le M:=7|\tau|,\quad
\|A_b\|\le a_0:=\sqrt{7/12}|\tau|,\quad
\|S_b\|\le s:=\sqrt{7/12}|\tau|\le\frac45|\tau|.
\tag{2}
\]

The rational relaxation follows from `7/12<16/25`. The symbols s and a_0
are proof bounds on constructed operators; they introduce no new coupling.

## Domain preservation before any series expansion

For a given b, split the nonnegative reference sum into the star and its
complement. I2 has `u_b,Omega_(S_b) in D(H_(0,S_b))`, and both
`H_(0,S_b) S_b` and `S_b H_(0,S_b)` extend boundedly. The complement
strongly commutes with the bounded local S_b. Thus S_b maps D(H_0) into
D(H_0) and, on that domain,

\[
[S_b,H_0]=-A_b,\quad
H_0S_b\psi=S_bH_0\psi+A_b\psi.
\tag{3}
\]

This is not a claim that the global extension of S_b maps every Hilbert
vector into D(H_0); a rough vector in the complementary factors would
invalidate that claim. Instead (3) bounds S_b in the H_0 graph norm.
Finite sums give the same property for X, with `[X,H_0]=-A`. Since X is
bounded in that Banach graph norm, its exponential series converges there.
The inverse exponentials show `exp(plus/minus X) D(H_0)=D(H_0)`.
Also X*=-X, so U=exp(X) is unitary. Phi is bounded in each finite volume,
hence H_0+Phi has exactly D(H_0).

Differentiate the graph-domain conjugation only after establishing (3):

\[
e^XH_0e^{-X}=H_0-\int_0^1 e^{tX}Ae^{-tX}\,dt.
\tag{4}
\]

The correction in (4) is an operator-norm integral of bounded operators.
Combining with bounded conjugation of Phi gives the exact identity

\[
\boxed{e^X(H_0+\Phi)e^{-X}=H_0+D+R_\Lambda,}
\]
\[
R_\Lambda=\sum_{n\ge1}\left\{
 \frac{\operatorname{ad}_X^n\Phi}{n!}
 -\frac{\operatorname{ad}_X^n A}{(n+1)!}\right\}.
\tag{5}
\]

For each fixed finite volume this bounded series converges in operator norm
for every finite tau. It comes from expanding only A and Phi in (4), not
from putting the unbounded H_0 into an operator-norm BCH series. The local
volume-uniform summability established next has its own smallness range.

## Every ordered word, enlarged support, and multiplicity

For a seed family B_b equal to phi_b or A_b, expand `ad_X^n sum_b B_b`
into the indexed ordered words

\[
T_{b_0;\,b_1,\ldots,b_n}
=[S_{b_n},[S_{b_{n-1}},\ldots,[S_{b_1},B_{b_0}]\ldots]].
\tag{6}
\]

Declare its support to be `Y=union_(j=0)^n S_(b_j)`. Repetitions of
anchors and different orderings remain distinct terms, with the factorial
coefficients in (5); coincident support sets are added by triangle summation.
If at any stage the next star is disjoint from the preceding union, the
nested commutator is zero. Every retained word therefore has an ordered
connected support history. Its union contains at most `4+3n` sites, since
each new intersecting four-site star adds at most three. There is no fixed
four-site support bound after the first commutator. This criterion includes
all possible nonzero words; further cancellations need not be detected.

Let N_n(B) be the supremum over x of the sum
`sum_(words with x in Y) 2^|Y| ||T_word||` at depth n, with no factorial.
Each site is contained in at most four retained stars, hence
`N_0(B)<=64 b` if `sup_b ||B_b||<=b`. Suppose Y is a depth-n support
of size at most k_n=4+3n and a new star Z intersects Y. Then

\[
2^{|Y\cup Z|}\|[S_Z,T_Y]\|
\le16s\,2^{|Y|}\|T_Y\|.
\tag{7}
\]

For a fixed x in the new union, split the sum into x in Y and x in Z.
For the first case, at most `4|Y|` anchors have stars meeting Y. Its
contribution is at most `64s k_n N_n`. For the second case, at most four
stars contain x; for each such star the sum over Y meeting it is at most
four times N_n. This contributes at most `256s N_n`. The cases can
overlap; that only increases this positive upper bound. Therefore

\[
\boxed{N_{n+1}(B)\le64s(8+3n)N_n(B),\qquad N_0(B)\le64b.}
\tag{8}
\]

This proof sums over every actual term occurrence and permits repeated
anchors. It bounds all orders without relying on a finite-order count or
replacing intersecting unions by isolated stars. Deleting anchors at the
cuboid boundary can only reduce the sums.

With r=192s, induction yields
`N_n(B)<=64b r^n (8/3)_n`. The generalized-binomial sum can be checked
without importing a cluster theorem: the power series with coefficients
`(8/3)_n/n!` has value 1 at zero and satisfies
`(1-r) f'(r)=(8/3)f(r)`, hence f(r)=(1-r)^(-8/3) for 0<=r<1.
Using `1/(n+1)<=1/2` for n>=1 in the A contribution of (5), we obtain

\[
\boxed{\|R_\Lambda\|_w\le
64(M+a_0/2)\{(1-192s)^{-8/3}-1\},\qquad192s<1.}
\tag{9}
\]

This proves a convergent scalar majorant for the specified indexed-support
decomposition, independent of cuboid size. Absolute convergence in this
weighted interaction norm also defines the corresponding infinite
homogeneous interaction coefficients as limits of the words. It does not
construct a bounded infinite X or a unitary exp(X) in the summable ITP.

## Evaluated interval and constants

By (2), `r<=768|tau|/5`. If `|tau|<=5/1536`, then r<=1/2. On this interval

\[
(1-r)^{-8/3}-1\le(1-r)^{-3}-1\le14r.
\]

For the last inequality, expand `(1-r)^(-3)` into its positive-coefficient
series: its difference quotient by r increases up to its value 14 at r=1/2.
Moreover `M+a_0/2 <=37|tau|/5`. Substitution in (9) proves (1), since
`64*14*37*768/25=25460736/25`. For the explicit interior value
`|tau|=1/4096`,

\[
\|R_\Lambda\|_w\le777/12800,\qquad28|\tau|=7/1024.
\tag{10}
\]

For `|tau|<=2^(-22)`, the same arithmetic even gives
`||R||_w <=(777/3200)|tau| < |tau|/4`. This is smallness of the new
remainder alone, not a contraction of the full Hamiltonian or a gap theorem.
The first-order D remains, and an iteration would need a changed class and
new inverse/domain estimates. The numerical constants are deliberately
conservative and are not claimed optimal.

## Relative diagonal part and the precise stability obstruction

The commuting onsite ground projections obey
`Q_(S_b)<=sum_(x in S_b) (I-P_x)`. Thus for every reference form-domain psi,

\[
|\langle\psi,D\psi\rangle|
\le M\sum_b\langle\psi,Q_{S_b}\psi\rangle
\le4M\langle\psi,H_0\psi\rangle
=28|\tau|\langle\psi,H_0\psi\rangle.
\tag{11}
\]

All four-site overlap multiplicities have been retained. D Omega=0, so
H_0+D by itself has the product ground and gap at least 1-28|tau| when
that quantity is positive. Equation (11) is not a gap estimate for (5)
after adding R.

In fact the actual remainder is not generally vacuum annihilating. Fix any
finite cuboid with at least one retained anchor. Let `U_1=sum_b u_b/tau`
and `V_1=Phi Omega/tau`, understood at nonzero tau and extended by their
linear definitions. On the product vacuum, `X Omega=tau U_1` and
`H_0 U_1=V_1`. The distinct omitted Wilson faces have the same two-free-link
orthogonality used in I2, now across all retained anchors. For N anchors,
`||V_1||^2=7N/12>0`; hence `a_Lambda=<U_1,H_0 U_1>>0`.
Taking the vacuum mean of the second-order term in (5) gives

\[
\langle\Omega,R_\Lambda\Omega\rangle
=-\tau^2 a_\Lambda+O_\Lambda(|\tau|^3).
\tag{12}
\]

Indeed both `[X,Phi]` and `[X,A]` have vacuum mean
`-2tau^2 a_Lambda`, and their coefficients are 1 and -1/2.
The bounded series makes the remainder analytic for fixed volume.
Consequently the displayed mean is strictly negative for all sufficiently
small nonzero tau in that fixed volume. A pure relative form bound for R
against H_0 would instead force its vacuum mean to be zero. This disproves
that attempted route in the actual model; it does not assert a volume-uniform
negative lower coefficient or gap failure.

Subtracting a scalar is a legitimate possible reorganization, but it does
not generally eliminate the remaining vacuum off-diagonal terms. The exact
small spin control described below demonstrates that further obstruction to
a universal one-step argument. A successful further method must control
the generated supports, remove their vacuum mixing, retain a relative
diagonal bound and bound the inverse used for each new dressing.

Nor does (1) give a volume-uniform global operator norm for R_Lambda. Even
the elementary local family `epsilon sum_x I_x` has weighted local norm
2epsilon and global norm `epsilon |Lambda|`. Its spectral gap is unchanged,
which also shows why this norm obstruction proves no physical gap failure.
A global bounded-perturbation gap test based only on summing local norms
therefore loses uniformity. One needs a genuine many-site stability or
closed block-diagonalization argument, with evaluated constants.

## Checks, sources, and limits

The checker uses exact rational support counting and matrices. A finite
retained-anchor fixture counts every ordered connected word through depth
three, including repeated anchors and enlarged supports, and verifies (8)
with the triangle majorants. This corroborates, but does not prove, its
all-order derivation. A separate overlapping three-qubit fixture has actual
rank-two vacuum-rotation generators on neighboring pairs: it rejects
deletion of cross commutators and confirms support outside either seed.
An exact one-spin fourth-order commutator calculation shows nonzero vacuum
offdiagonal remainder; omitting the full remainder also changes the
determinant already in the elementary one-spin case. These are lemma
controls, not SU(2) physical simulations or finite evidence for a lattice gap.

Targeted primary-source reading is recorded in `source-notes.md`. Yarotsky's
qualitative hypotheses allow the relevant unbounded sites, but the checked
source proof leaves cluster constants unevaluated. The multidimensional
unbounded-interaction block-diagonalization paper also requires its full
induction, inverse-gap and domain estimates; its threshold is not imported.
O1 instead proves the bounded simultaneous rotation and its local majorant
directly. The source framework is established mathematics; the explicit
instantiated constant and overlap calculation are model-specific derivations.
Scientific priority is unverified.

The numerical homogeneous stability interval, a convergent iteration,
thermodynamic representation transfer, physical dynamics matching and
continuum Yang–Mills mass gap remain open. The justified next candidate is
an iteration with an explicit class of enlarged interactions and a uniform
vacuum-mixing elimination estimate. This report does not select O2.

```bash
python3 -B research/round22/forward/o1/check.py --output /absolute/new/o1-forward
python3 -B -O research/round22/forward/o1/check.py --output /absolute/new/o1-forward-optimized
```
