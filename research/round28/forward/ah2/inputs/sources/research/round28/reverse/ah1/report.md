# AH1 reverse: complete new-graph enrichment and a uniform heat certificate

Independent reverse derivation under the frozen AH1 contract, sequence 5,
goal AH loop 1. Current forward AH1 and current skeptic science remained unread
through this producer's derivation and freeze. Shared mathematical ancestors
are acknowledged; agreement is not an independent physical observation.

The open 3×2×1-cell graph has **24 vertices, 46 links, 29 faces**, including
seven internal faces, and cycle rank 23. Its complete strict electric subspace
has rank 30. The specified individually resolved enrichment has **561**
linearly independent physical vectors. Its exact Gram, electric operator and
all 2,124 nonzero magnetic entries are exported, with every remaining entry
proved zero. For the declared normalized complex preparation ball the exact
separately ground-centered heat evolutions satisfy, at every sigma≥0,

\[
 \frac{\|E(\sigma)x-E_+(\sigma)x\|}{\|E(\sigma)x\|}
 \le \frac{3037671524521}{1418412601938100}
 <\frac{43}{20000}=0.00215. \tag{R1}
\]

This is a conservative analytic certificate for the exact retained semigroup.
It is not a numerical matrix-exponential evaluator, an evaluated full outside
Gram, or a graph-size/continuum theorem. The older graph's accuracy constants
are not reused. Scientific priority is unverified.

## 1. Reverse target, model and full domains

To prove a true-output-relative all-time statement, it suffices to construct
the actual retained space, a simultaneous full outside bound, both ground
projector comparisons to the original Ritz ground, a positive true output
floor, and independently valid increasing/decaying time estimates. Sections
2–6 provide these premises in this exact model.

Vertices are lexicographic integer triples in `{0,…,3}×{0,…,2}×{0,1}`.
Links are ordered by tail coordinate, then axis, and point in the positive
coordinate direction. Faces are ordered by base coordinate and increasing
axis pair a<b; their word follows +a,+b,−a,−b. The coordinate bounds determine
all links and faces, including faces internal to the cell complex.
There are 12 xy faces, 9 xz faces and 8 yz faces. The seven internal faces are
not discarded. The graph is connected, so its cycle rank is 46−24+1=23.

Work on the actual Hilbert space

\[
 \mathcal H_{\rm phys}=L^2(SU(2)^{46},dU)^{SU(2)^{24}},\quad
 K=\sum_e C_e,\quad W_p=\tfrac12\operatorname{Tr}U_{\partial p},\quad
 S=\sum_{p=0}^{28}W_p,\quad L=K+\lambda(29-S).
\]

The gauge action on link variables is `U_e → g_tail U_e g_head^{-1}`.
Every vertex acts on every incident link; `graph.json` gives all signed
incidences, and every oriented face word transforms by conjugation at its
base. No maximal-tree deletion or independent-cycle electric replacement is
made. The checker also verifies all 29 face traces under exact noncommuting
rational SU(2) link and gauge assignments.

The full product Casimir is positive and self-adjoint. Its Peter–Weyl spin
blocks have finite multiplicities and eigenvalues tending to infinity as any
link spin grows. Thus it has compact resolvent. Gauge averaging commutes with
every link Casimir and their spectral sums; restriction to the closed physical
sector preserves self-adjointness and compact resolvent. Finite invariant
Peter–Weyl polynomials form an operator core, and smooth invariant functions
contain that core. The operator domain is the physical spectral sum with
square-summable electric-energy-weighted coefficients; the form domain uses
one energy weight. This keeps all original link derivatives.

Each W_p is a real smooth invariant bounded multiplication operator, with
|W_p|≤1. Thus S is bounded, self-adjoint, gauge invariant, and ||S||≤29.
Bounded perturbation gives `D(L)=D(K)` and the same form domain; the smooth
invariant core remains a core. For 0≤lambda≤1/100, each 1−W_p≥0, so **L≥K**.
Negative lambda would invalidate this positivity argument and is excluded.

The fixed physical Hamiltonian is H=alpha L, with fixed positive
a,E_star,alpha/E_star,hbar and sigma=alpha t/hbar. All displayed energy
and residual bounds are dimensionless; multiply them by alpha for physical
energies. Preparation radius and joining time are proof/preparation choices,
not action parameters or fitted clocks. This is a new finite uniform-coupling
graph, distinct from the homogeneous and canonical profile models.

## 2. Strict electric cutoff and the unique vacuum

In a nontrivial invariant spin network, an active edge has spin j≥1/2 and
costs at least 3/4. A vertex incident to exactly one active edge cannot have an
invariant intertwiner. Below electric energy 9/2 there are therefore at most
five active edges, with active-support minimum degree at least two.

The graph is simple, bipartite and has girth four. Such a nonempty support
with at most five edges must contain a four-cycle. A fifth edge cannot attach
a new vertex without a degree-one vertex; it cannot join opposite cycle
vertices because that creates an odd cycle, or join adjacent cycle vertices
because the graph is simple. Equivalently, a five-edge minimum-degree-two
bipartite graph would have at most five vertices: four vertices permit at
most four edges, while a five-edge subgraph of K_(2,3) has a degree-one
vertex. The checker verifies this finite combinatorial exclusion separately.

Every four-cycle in the cubical graph is a single elementary square: its
four unit steps use two axes, once in each sign. An independent common-neighbor
enumeration recovers exactly the 29 exported face edge sets. At every
degree-two cycle vertex, invariance forces equal adjacent spins and a unique
intertwiner. All four edge spins are thus equal. The strict bound selects
j=1/2, because its energy is 3 while j≥1 has energy at least 8.

Consequently

\[
 P_0=1_{[0,9/2)}(K)
 =\operatorname{span}\{\Omega=1,\ \phi_p=2W_p:0\le p<29\},\qquad
 \operatorname{rank}P_0=30. \tag{R2}
\]

The physical Gram is the identity: a simple square holonomy is Haar and
distinct squares have exclusive links. The same support argument proves that
the full physical electric gap is exactly 3 and that the constant vacuum is
unique. States on six fundamental edges cost **exactly 9/2**; in particular
the shared-edge singlet channels below are excluded from P0. Replacing the
strict endpoint by an inclusive one changes the problem. No spin-degree cutoff
family is identified with this spectral interval.

## 3. Actual generated vectors, Haar Gram and complete K reduction

For each unordered pair p<q, write X_pq=W_p W_q. Distinct faces share at most
one link. There are 96 shared-edge pairs and 310 edge-disjoint pairs, of which
64 touch only at vertices. For a shared edge e, let E_e be Haar integration
over that link, acting on the actual full-link function. This is the spin-zero
Casimir projection and commutes with the physical gauge action. Define
X_s=E_e X_pq and X_t=X_pq−X_s. The product of two fundamental matrix factors
contains only link spin zero and one, so these exhaust the shared-link
spectral components of the generated vector.

The following rational-coordinate basis fixes the actual functions; no
arbitrary ambient intertwiner is substituted:

| Vector | Count | Squared norm | Electric energy |
|---|---:|---:|---:|
| Omega | 1 | 1 | 0 |
| phi_p=2W_p | 29 | 1 | 3 |
| chi_p=4W_p²−1 | 29 | 1 | 8 |
| d_pq=4W_pW_q, no common edge | 310 | 1 | 6 |
| s_pq=8X_s, common edge | 96 | 1 | 9/2 |
| t_pq=8X_t, common edge | 96 | 3 | 13/2 |

For disjoint edges, including a vertex-only meeting, the actual product is an
electric eigenvector: each of eight links carries spin 1/2. Extra ambient
intertwiners at a meeting vertex do not need to be included for this chosen
product to be an eigenvector. For shared-edge pairs the six exterior links
cost 9/2, and the common triplet adds 2. Same-face chi_p is the normalized
spin-one character on a square and costs 8.

To verify the shared norms with the phases/orientations retained, reverse a
face trace when necessary and cyclically order it to write
X=t(GA)t(G^{-1}B), where t=Tr/2 and A,B are products along the two exterior
three-link paths. SU(2) trace reversal does not change the function. The paths
use disjoint Haar links, so their products are independent Haar variables,
even if the paths meet at vertices. The exact link integral is

\[
 E_G X=\tfrac14t(AB),\quad \|X\|^2=\tfrac1{16},\quad
 \|X_s\|^2=\tfrac1{64},\quad \|X_t\|^2=\tfrac3{64}. \tag{R3}
\]

The new checker derives these identities again by quaternion polynomial
integration on three unit 3-spheres; it integrates the common variable
coefficientwise and checks the orthogonal decomposition. It uses the exact
even-monomial sphere moment formula, not a Monte Carlo estimate or an imported
historical implementation.

Distinct pair masks (symmetric differences of their original face edge sets)
are nonzero and all 406 are distinct. None is a fundamental face mask. These
facts are exhaustively checked on the actual graph; equivalently there are
no three-face or four-distinct-face zero XOR relations. Independent link
center flips therefore make different pair vectors orthogonal, and separate
them from the old and spin-one sectors. Within a shared pair, different
electric energies give orthogonality. The chi_p have distinct nonzero integer
spin supports; these Peter–Weyl labels make them mutually orthogonal and
orthogonal to Omega. All vectors have the strictly positive norms above.

Hence the **actual Gram is diagonal, its kernel is empty, and its quotient
rank is 561**. This conclusion is proved, not assumed from the old graph.
Every basis vector is a finite smooth invariant polynomial. Their K eigenvector
span reduces K, its operator domain and its form domain.

This is the span of each individually resolved product and its K spectral
components. It is not a claim to fill whole electric shells. Nor may one
replace it by the K-cyclic closure of only summed columns `(I−P0)SP0`: K does
not resolve distinct vectors at one repeated eigenvalue. A two-coordinate
exact control illustrates this loss. A separate duplicate-coordinate Gram
control checks its nullspace and quotient action; no synthetic null relation
is incorrectly attributed to this actual independent basis.

## 4. Every magnetic column, structural zero and full outside map

For a link with integer tail (x,y,z), assign central signs +1 on x links,
(−1)^x on y links, and (−1)^(x+y) on z links. Each actual face acquires sign −1,
as checked independently on every exported word. This product-Haar-preserving
gauge-compatible transformation commutes with K and sends S to −S.
Omega and all new vectors are even, and the 29 phi_p are odd. Therefore all
within-parity matrix elements of S vanish. Uniform reversal of every link
would instead give a square sign +1 and is a rejected control. This one
global oddness argument does **not** prove pair-mask independence; Section 3
provides the separate mask/representation argument.

The complete odd columns and vacuum column follow from multiplication:

\[
 \begin{aligned}
 S\Omega&=\tfrac12\sum_p\phi_p,\\
 S\phi_p&=\tfrac12\Omega+\tfrac12\chi_p
 +\tfrac12\sum_{q:\,e(p)\cap e(q)=\varnothing}d_{pq}
 +\tfrac14\sum_{q:\,|e(p)\cap e(q)|=1}(s_{pq}+t_{pq}).
 \end{aligned} \tag{R4}
\]

Metric self-adjointness gives all remaining even-to-odd entries. If g_i is the
diagonal Gram, the coordinate matrix satisfies g_i S_ij=g_j S_ji. In
particular the retained triplet-to-face coefficients are **3/4**, whereas the
face-to-triplet coefficients are **1/4**. Treating t_pq as norm one or blindly
transposing coordinate coefficients is wrong. There are 2,124 directed nonzero
entries and 312,597 exact zeros. Every possible parity-crossing entry is
determined by (R4) and this metric identity, so the sparse export describes
the entire operator P+SP+, including all nonvacuum inputs.

Let A+=P+LP+, Q+=I−P+, and

\[
 B=Q_+LP_+=-\lambda Q_+SP_+.
 \quad BP_0=0,\qquad \|B\|\le29\lambda. \tag{R5}
\]

K reduction justifies the first equality on every retained vector. Equation
(R4) proves BP0=0. Orthogonal projection in the physical Gram norm and the
actual pointwise bound |S|≤29 prove the simultaneous last inequality for
every complex linear combination of all 561 inputs. All 531 new input columns
and all unretained intertwiners are charged; it is not a collection of
single-column estimates or a complete outside Gram evaluation.

More explicitly, each omitted column is
`B b_j=−lambda [S b_j−sum_i b_i S_ij]`. This exact function formula specifies
every column without claiming a cubic outside basis has been assembled.
The full map is nonzero for lambda>0: on chi_p, the W_p term contains the
normalized spin-3/2 character of face p with coefficient 1/2. That character
is outside P+, while every q≠p term is excluded from that coefficient by its
different center mask. Thus ||B||≥lambda/2 for this particular normalized input.
BP0=0 therefore gives neither B=0 nor autonomous retained evolution.

## 5. Complete original residual and both nested ground comparisons

Set N=29, c=N lambda, Dlambda=sqrt(9+N lambda²),
w=(Dlambda−3)/2, h=lambda/[2(3+w)], and Z=1+N h². The exact P0 ground is

\[
 \mu_0=c-w,\qquad
 f_0=\frac{\Omega+h\sum_p\phi_p}{\sqrt Z}. \tag{R6}
\]

The other P0 eigenvalues are c+3 (multiplicity 28) and c+(3+Dlambda)/2.
These formulas follow from its complete star matrix: diagonal entries c on
Omega and c+3 on faces, couplings −lambda/2, no other entries.

Before residual inference, positivity and min-max establish on the full
operator and both compressions

\[
 0\le\epsilon\le\mu_+\le\mu_0\le29\lambda<3,
 \qquad E_1(L),E_1(A_+),E_1(A_0)\ge3. \tag{R7}
\]

The vacuum trial vector gives the upper bound; compactness and the full
electric gap establish existence and simplicity of the separated ground
states. Define their actual rank-one projections G,G+,G0. No exact enlarged
ground vector is numerically guessed or evaluated in this loop.

Let F_source=S²−N/4. Conditional Haar integration gives E W_p²=1/4,
E W_p⁴=1/8 and E W_p²W_q²=1/16. The separate mask checks exclude all remaining
fourth-moment terms. Equivalently, the complete basis expansion is

\[
 F_{\rm source}=\tfrac14\sum_p\chi_p
 +\tfrac12\sum_{\rm disjoint}d_{pq}
 +\tfrac14\sum_{\rm shared}(s_{pq}+t_{pq}),
 \quad \|F_{\rm source}\|^2=\frac{N(2N-1)}{16}=\frac{1653}{16}. \tag{R8}
\]

The electric first moment from all four nonvacuum channel types is 1247/2,
also equal to 4 E S⁴. Keeping only spin-one faces would underestimate the
squared residual norm by a factor of 57. The whole full-Hilbert residual is

\[
 (L-\mu_0)f_0=-\frac{2\lambda h}{\sqrt Z}F_{\rm source},\qquad
 \rho_0^2=\frac{N(2N-1)\lambda^2h^2}{4Z}. \tag{R9}
\]

For Lambda=1/100 use uniform rational envelopes

\[
 g=3-N\Lambda=\frac{271}{100},\quad
 \bar r_0=\frac{41}{12}\Lambda^2,\quad
 \bar p_0=\bar r_0/g.
\]

Indeed h≤lambda/6, Z≥1 and sqrt(1653)<41. Spectral expansion using (R7)
gives the **two separate comparisons**

\[
 \|G-G_0\|\le\bar p_0,\qquad
 \|G_+-G_0\|\le\bar p_0. \tag{R10}
\]

For the first, the full excited spectral distance from mu0 is at least
3−mu0≥g. For the second, BP0=0 gives Lf0 in P+, hence
`(A+−mu0)f0=(L−mu0)f0`; the same residual has the same separation in the
nested compression. These are different spectral arguments, not a
substitution of a compressed residual for an uncomputed full residual.

For the actual normalized enriched ground f+, Bf0=0 yields

\[
 \rho_+=\|(L-\mu_+)f_+\|=\|Bf_+\|
 =\|B(I-G_0)f_+\|
 \le N\Lambda\bar p_0=:\bar r_+.
\]

The full spectral measure then gives

\[
 \|G-G_+\|\le\bar p_+:=\bar r_+/g,\qquad
 0\le\mu_+-\epsilon\le\bar d_+:=\bar r_+^2/g. \tag{R11}
\]

For the energy estimate, `(L−epsilon)(L−3)` is nonnegative on the full
spectrum, so `rho_+²−(mu_+−epsilon)(3−mu_+)≥0`. Smoothness of f+ provides
the required second moment. These quantities are uniform envelopes, not
evaluated actual errors:

| Envelope | Exact value |
|---|---:|
| r0 | 41/120000 |
| p0, for both comparisons | 41/325200 |
| r+ | 1189/32520000 |
| p+ | 1189/88129200 |
| d+ | 1413721/2865961584000000 |

All inequalities cover the continuous coupling interval directly; the
checker's rational parameterized Ritz examples are algebra controls only.

## 6. True denominator, strong Duhamel and all-time join

Let x be any normalized complex vector in P0 with ||x−Omega||≤eta=1/100.
From (R6), `(1+u)^(-1/2)≥1−u/2`, h≤Lambda/6 and sqrt(29)<27/5, set

\[
 z=1-\frac{29\Lambda^2}{72},\qquad q_0=\frac9{10}\Lambda,
 \qquad b=q_0+\bar p_0+\eta,\quad D_*=z-\eta-\bar p_0>0.
\]

Here z≤|<f0,Omega>|, q0≥||(I−G0)Omega||. The two comparisons (R10)
imply both `||(I−G)x||≤b` and `||(I−G+)x||≤b`. Also

\[
 \|E(\sigma)x\|\ge\|Gx\|
 \ge|\langle f_0,x\rangle|-\bar p_0\ge D_*
 =\frac{193136341}{195120000}>0.9898. \tag{R12}
\]

This is the **actual full output denominator**, and triangle/Cauchy bounds
are valid for complex x. It is not the retained output norm or a regularizer.

Use the exact independently centered heats
`E(sigma)=exp[−sigma(L−epsilon)]` and
`E+(sigma)=exp[−sigma(A+−mu+)]P+`. They are contractions. The finite retained
span lies in D(L), so differentiation on it followed by strong vector
integration gives

\[
 (E-E_+)(\sigma)x=-\int_0^\sigma E(\sigma-u)
 [B+(\mu_+-\epsilon)P_+]E_+(u)x\,du. \tag{R13}
\]

The defect has the displayed **plus** centering term. Decompose E+(u)x into
its ground piece and an excited piece of norm at most b exp(−gu). Equations
(R5),(R11) give the early absolute bound

\[
 V(\sigma)=(\bar r_++\bar d_+)\sigma
 +\frac{29\Lambda b}{g}(1-e^{-g\sigma}). \tag{R14}
\]

Independently, the full and retained spectral decompositions give
`||(E−E+)x||≤p+ +2b exp(−g sigma)`. The contract template's slightly looser
decaying envelope is therefore valid:

\[
 J(\sigma)=\bar p_++(2b+\bar p_+)e^{-g\sigma}. \tag{R15}
\]

V is increasing and J is decreasing. Use V on [0,2] and J on [2,infinity),
with the predeclared join 2. A positive rational Taylor sum proves
exp(2g)>225; also 1−exp(−2g)≤1. Thus exact upper join values are

\[
 \bar V_2=\frac{3037671524521}{1432980792000000},\qquad
 \bar J_2=\frac{4549807}{24786337500}<\bar V_2.
\]

Dividing their maximum by (R12) proves (R1). No time grid establishes the
all-time conclusion, and no old numerical target is imported. This positive
upper bound measures certified scope; it is not observed approximation error.

At sigma=0 both exact evolutions equal x on this preparation class. At
lambda=0, P+ reduces K and both centers vanish, so they agree on every
retained input at every time. These exact identities supersede coarse
positive envelopes. Zero-extension still has full-input operator norm error
one at sigma=0; no full-Hilbert initial accuracy is claimed.

The scalar reference 29lambda cannot replace epsilon: already the P0 ground
has mu0<29lambda for lambda>0. Centering full heat by that reference gives
a growing true-ground coefficient. Any independently rounded ground center
also changes that coefficient and its derivative; it can destroy the
all-time limit. BP0=0 cancels neither the actual center difference nor later
loading of retained channels. No real-time relative conclusion follows.

## 7. Execution, controls and limits

The standard-library `check.py` constructs this graph afresh, integrates the
local Haar polynomial identities, enumerates masks, builds the complete
physical-coordinate matrices and checks all rational inequalities. It does
not import, execute or use the output of a historical checker as its new
algorithm. The authoritative output fractions accompany the sparse data in
`output/{graph,basis,magnetic,results}.json`.

Controls include missing internal faces; all oriented Gauss identities;
the strict endpoint; five-edge support exclusion; missing singlet/triplet
branches; incorrect triplet metric and metric-blind transposition; duplicate
Gram/null quotient; the distinction between individual and summed cyclic
channels; incorrect global sign and pair-mask inference; all-input outside
loading versus BP0=0; negative coupling; old graph constants; scalar or
rounded centers; and normalized real and imaginary face preparations.

One initially chosen wrong-orientation trace fixture was nondiscriminating:
its endpoint gauge elements agreed. Applying that same orientation mutation
to horizontal links across the graph remained blind for that assignment.
The retained diagnostic records the failure, and a replacement scans the four
positions in each face word; vertical-link reversals produce exact unequal
traces. Both the blind original and discriminating replacements are reported
in `graph.json`. This repair is a control refinement, not another research
loop or independent observation.

The contract's 42 sources plus the contract itself were hash-verified and
snapshotted before science, along with 26 used instruction snapshots. The
initial input-manifest formatting was adapted to the advisor's existing schema
before science; the initial format is preserved. Main inherited reconstruction
reading is X1/X2 physical cutoff and Haar/residual arguments, AC1 closure and
heat bounds, Z2 strong-domain/centering arguments, and the frozen AH1 proposal
and source clarifications. AC2/AF2 and the other declared sources are retained
as scoped mathematical/provenance context. No claim of new historical or
external literature reading is made in this loop. Newton/Tesla methods guide
reconstruction, full loading and attempted falsification; they supply no
historical-person endorsement or additional physical premise.

Reproduce into a fresh absolute directory:

```
python3 -B research/round28/reverse/ah1/check.py --output /absolute/fresh/ah1
python3 -B -O research/round28/reverse/ah1/check.py --output /absolute/fresh/ah1-O
```

The final checker executes 320 exact checks. Explicit exceptions keep controls
active under optimized Python. The freeze records final normal/optimized byte
equality and every current file hash.
There is no full outside Gram, numerical exponentiation, complete ambient
representation cutoff, graph-size uniformity, homogeneous/canonical matching,
physical calibration or continuum construction here. AH2 and later goals
remain unselected by this producer.
