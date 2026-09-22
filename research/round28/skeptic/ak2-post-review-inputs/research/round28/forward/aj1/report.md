# AJ1 forward: physical GNS space for the actual homogeneous orthant model

**Forward conclusion, pending independent review:** the actual I1 state is
locally normal, its finite endpoint gauge groups have strongly continuous GNS
implementers, and its full bounded local invariant algebra generates exactly
the joint fixed-vector space. That space reduces the inherited, ground-centered
closed generator. The new regularity estimate is

\[
 \omega_\Lambda(H_{0,F})\le2M N_{F,\Lambda}\le8M|F|=56|\tau||F|,
 \qquad M=7|\tau|.                                      \tag{1}
\]

Here every incoming and outgoing **complete** retained star meeting `F` is
counted in `N`. Compact resolvent makes this an actual energy-tightness and
local-normality argument. No numerical nonzero value of `tau` is certified.
The physical threshold `alpha/16` is inherited from I1 and restricts to the
physical sector; this is not a nonzero physical-excitation construction.

This is investigation 7, goal AJ loop 1. The frozen contract is
`a9660ab26b0116958c11721e5461eab3391d50149306e06a0ec2476cdbc21571`.
The input pack `a18b36cecf48204d5946ae6233a5228adf43a9750a6f05c55d5730d2cc0fc8ac`
was frozen before production and explicitly passed the advisor's manual and
standard preflights. No current reverse AJ1 or independent skeptic science
was read. All arguments and the checker here were written independently;
historical checkers were neither imported nor executed. The reset route was
an explicitly shared contract proposal, not a previously proved premise.

## 1. Model, source topology and inherited scope

For an original positive oriented link `(a,i)`, its coarse owner is
`(floor(a_x/4),floor(a_y/2),a_z)`. Each coarse site owns all 24 outgoing
link Haar factors. The three selected xy faces have anchors with local
remainders `(0,0,0),(1,0,0),(2,0,0)` and use ten links; fourteen further
links remain in the same site space. Thus `K_b=L2(SU(2)^24)` is an
unreduced tensor factor. No tensor factorization of the Gauss-constrained
space is assumed. In particular outgoing links and their head vertices are
not clipped from these factors.

Keep the inherited fixed real selected coefficients within
`|lambda_L|,|lambda_R|<=alpha/2`, `|mu|<=alpha/8`. With
`delta=alpha/8`, define

\[
 h_b=\delta^{-1}\left(H_{\mathrm{strip},b}-E_{\mathrm{strip},b}
                   +\alpha\sum_{e\text{ free at }b}C_e\right),
 \quad h_b\ge1-P_b,\quad h_b\Omega_b^0=0.                 \tag{2}
\]

The onsite vacuum is unique by the admitted strip result and the free-rotor
vacua. For finite positive-orthant coarse cuboids,

\[
 H_{0,\Lambda}=\sum_{b\in\Lambda}h_b,\quad
 \widehat H_\Lambda=H_{0,\Lambda}
      +\sum_{b+S\subset\Lambda}\phi_b,\quad
 \phi_b=-\frac\tau3\sum_{21\text{ omitted faces anchored at }b}W_f,
 \quad S=\{0,e_x,e_y,e_z\}.                              \tag{3}
\]

Every complete group has norm `M=7|tau|`: the upper bound uses `||W_f||=1`,
and the lower bound follows from positive-Haar-measure neighborhoods of the
identity link configuration. All 21 faces and their actual supports are
retained whenever the *whole* star lies in the volume. An individual-face
contained-boundary Hamiltonian is a different finite boundary prescription.

The sole homogeneous smallness premise is the already admitted I1 condition

\[
 |\tau|<\tau_*:=\tfrac17\min(c_1(S),1/(2c_2(S))),          \tag{4}
\]

where both source constants are positive and unevaluated. I1 gives the
unique finite ground vectors `Omega_Lambda`, the specified whole-star
orthant state `omega`, and its GNS triple `(pi,H_omega,Omega)` with unique
ground and nonnegative ground-centered self-adjoint generator `G` satisfying
`spec(G) subset {0} union [1/2,infinity)`.

The primary source is D.A. Yarotsky,
[math-ph/0411042v1, 11 November 2004](https://arxiv.org/pdf/math-ph/0411042).
Definitions and Theorems 1–3 are on printed pp.2–4; the creation/core and
limiting-generator passages are on pp.6–10. The frozen source note and
ledger record the actual prior reading depth. The full external cluster
expansion is inherited, not re-proved here. Its applicable topology is

\[
 \langle\Omega_\Lambda,A\Omega_\Lambda\rangle\longrightarrow\omega(A),
 \quad A\in\bigcup_{F\text{ finite}}B(K_F),               \tag{5}
\]

and, for bounded local `A,B` and nonreal `z`, the tested resolvent limit

\[
 \langle(\widehat H_\Lambda-E_\Lambda-z)^{-1}A\Omega_\Lambda,
 B\Omega_\Lambda\rangle
 \longrightarrow
 \langle(G-z)^{-1}\pi(A)\Omega,\pi(B)\Omega\rangle .       \tag{6}
\]

There is no identification of these finite Hilbert spaces with the J2
summable representation and no asserted same-representation strong
resolvent limit.

For clarity, the I1 orthant transfer used in (5)–(6) works by extending the
coarse lattice to `Z^3`, placing independent reference sites outside the
orthant, and setting every outside anchor interaction to zero. Inside
positive stars never reach outside. Every symmetric finite exhaustion
therefore factors into the desired positive-orthant Hamiltonian and free
spectators. Its ground is a tensor product, and its full limiting state is
the orthant state times the spectator vacuum. On the spectator-vacuum
subspace the finite centered resolvent is exactly the orthant centered
resolvent. Mixed matrix elements against vectors orthogonal to that
spectator vacuum vanish. Equation (6), tested on dense local product
vectors, makes that subspace reducing for the limiting resolvent. Its
restriction is precisely the specified orthant `G`. This transfers the
source boundary and topology; it supplies no equality with other boundary
limits or a homogeneous full-integer-lattice gauge model.

The source's creation vector uses
`u_I in H'_I intersect D(H_{0,I})`, where `H'_I` is the finite tensor of
onsite vacuum-orthogonal spaces, and the bounded local creation operator is
`hat u_I=|u_I><Omega_I^0|` on `I`. The span of the corresponding GNS vectors
is the source core; its density and essential self-adjointness follow from
the source expansion. Indeed `[H_{0,I},hat u_I]` is bounded for precisely
these domain-qualified vectors, and only finitely many bounded interaction
commutators meet `I`. In the spectator extension, projection onto the
spectator vacuum preserves this core: terms with an excited outside site
are killed, while terms wholly in the orthant remain. Thus its projected
span is a core of the reducing orthant restriction. An arbitrary bounded
local `A` need not have `pi(A)Omega in D(G)`. Section 6 below uses (6) for
gauge covariance and does not need to strengthen the source core claim.

## 2. Compact resolvent and the reset estimate

Each SU(2) Casimir has eigenvalues `j(j+1)` for nonnegative half-integer
`j`, with finite multiplicity `(2j+1)^2`. A finite sum of 24 such operators
has only finitely many eigenvectors below each fixed energy, because each
individual nonnegative eigenvalue is then bounded. It has compact
resolvent. The selected Wilson terms and the scalar ground subtraction are
bounded self-adjoint perturbations. The resolvent identity preserves
compactness under such a perturbation. Consequently each actual `h_b` has
compact resolvent on the electric-sum domain, with the same form domain as
that electric sum. Since `h_b>=0`, the finite-region sum
`H_{0,F}=sum_(b in F)h_b` also has compact resolvent. Its spectral projections

\[
 Q_{F,L}=1_{[0,L]}(H_{0,F}),\quad L>0,                    \tag{7}
\]

are finite rank and increase strongly to the identity. This concerns
finite regions only, not compact resolvent of an infinite-volume operator.

Fix a finite volume containing `F`. The finite perturbation in (3) is
bounded, so its ground is in `D(H_{0,Lambda})`, and all the following
reference form expectations are finite. Write
`rho_Lambda=|Omega_Lambda><Omega_Lambda|` and reset **only** `F`:

\[
 \sigma=|\Omega_F^0\rangle\langle\Omega_F^0|
             \otimes\operatorname{Tr}_F\rho_\Lambda .    \tag{8}
\]

It is a positive trace-one density. By positivity and monotone spectral
truncation of the reference sums, its expectation of `H_{0,Lambda\F}` is
the unchanged finite expectation in `rho_Lambda`; its `H_{0,F}` expectation
is zero. Thus it has finite total reference form energy. This justifies
using the variational principle for the possibly mixed state `sigma`:
the lower bound `Hhat_Lambda>=E_Lambda` extends to its closed quadratic
form and hence to any such density by monotone spectral integration. We
have not assumed that every vector in the reset density's support belongs
to the operator domain.

Let

\[
 \mathcal I_{F,\Lambda}=
 \{b:b+S\subset\Lambda,\ (b+S)\cap F\ne\varnothing\},
 \quad N_{F,\Lambda}=|\mathcal I_{F,\Lambda}|.             \tag{9}
\]

Terms outside this set act wholly in the complementary factors and have
unchanged expectations. Subtract the exact finite ground expectation
from the reset variational inequality. Scalar ground energies and all
unchanged terms cancel, giving

\[
 0\le \operatorname{Tr}\sigma\widehat H_\Lambda-E_\Lambda
 =-\operatorname{Tr}\rho_\Lambda H_{0,F}
  +\sum_{b\in\mathcal I_{F,\Lambda}}
                  \operatorname{Tr}(\sigma-\rho_\Lambda)\phi_b.
                                                               \tag{10}
\]

Each difference in the sum is at most `2||phi_b||=2M` in absolute value.
Each site `x` belongs only to anchors `x,x-e_x,x-e_y,x-e_z`, subject to
nonnegative coordinates and the retained-star condition. Taking their
union, rather than merely counting anchors in `F`, gives
`N_(F,Lambda)<=4|F|`. This proves (1) at every volume containing `F`,
with no global sum of interaction norms and no density normalization by
volume. For a fixed finite `F`, its sharper all-volume coefficient uses
the finite set `(F-S) intersect Z_+^3`; the uniform `8M|F|` suffices here.

In particular,

\[
 \operatorname{Tr}\rho_{\Lambda,F}(1-Q_{F,L})
       \le \frac{8M|F|}{L}=:\varepsilon_L.                \tag{11}
\]

The bound may be replaced by its minimum with one. Constants need not be
small for this tightness argument; finiteness and `epsilon_L -> 0` are
enough. When `tau=0` the estimate forces the local reference vacuum, as it
should. It does not enlarge the existence regime (4).

## 3. Local normality and the representation property actually used

Pointwise convergence (5) applies to each fixed finite-rank `Q_(F,L)` and
its complement, so `omega_F(1-Q_(F,L))<=epsilon_L`. This is an additional
uniform-energy conclusion, not a consequence of weak-star convergence
alone. For any state `eta` on `B(K_F)` and projection `Q`, Cauchy–Schwarz
gives, for `||A||<=1`,

\[
 |\eta(A)-\eta(QAQ)|
 \le |\eta((1-Q)A)|+|\eta(QA(1-Q))|
 \le2\sqrt{\eta(1-Q)}.                                  \tag{12}
\]

The functional `omega_F(Q_(F,L) A Q_(F,L))` is finite rank and normal.
Equation (12) makes it converge in functional norm to `omega_F`. Normal
functionals form the trace-class predual, a norm-closed subspace of
`B(K_F)^*`; hence `omega_F` is represented by an actual positive
trace-one density `rho_F`. Monotone bounded spectral truncations of
`H_(0,F)` further give
`Tr rho_F H_(0,F)<=8M|F|`.

One can also derive local density convergence, which is stronger than the
inherited topology. For positive trace-one `rho`, Schatten Cauchy–Schwarz
in `rho-QrhoQ=(1-Q)rho+Qrho(1-Q)` gives
`||rho-QrhoQ||_1<=2 sqrt(Tr rho(1-Q))`. For a fixed cutoff the finite
matrix entries of `Q rho_(Lambda,F) Q` converge by (5), hence converge in
trace norm to those of `Q rho_F Q`. Therefore

\[
 \limsup_\Lambda\|\rho_{\Lambda,F}-\rho_F\|_1
 \le4\sqrt{\varepsilon_L}\ \longrightarrow\ 0.          \tag{13}
\]

This is specific to each fixed finite region and this energy-tight family;
it is not global trace-norm convergence on an infinite tensor product.

The local representation property can now be proved without guessing that
an arbitrary GNS representation preserves weak operator integrals. For
local `B` supported in `K`, the positive functional

\[
 A\in B(K_F)\ \longmapsto\
 \langle\pi(B)\Omega,\pi(A)\pi(B)\Omega\rangle
 =\omega_{F\cup K}(B^*AB)                                \tag{14}
\]

is normal, because the state on the larger finite factor is normal and
the embedding and multiplication maps are normal. These local cyclic
vectors are dense. Approximating any vector by them makes its positive
vector functional on `B(K_F)` a norm limit of normal functionals, hence
normal. Polarization gives the same for every matrix-element functional.
Thus `pi` is normal on every original local factor. In particular all
the matrix-element functionals used below can be passed through a local
weak operator Haar average. No statement about normality on a global
infinite tensor-product von Neumann algebra is needed.

## 4. Gauge invariance and strong continuous implementation

On the original finite link Hilbert space a gauge element at a vertex acts
by left multiplication on outgoing links and right inverse multiplication
on incoming links. Include **every** endpoint, even heads outside a coarse
volume's tail set. Left/right SU(2) translations are strongly continuous
on each `L2(SU(2))`: continuity holds on the dense finite Peter–Weyl span
and extends by unitarity. Finite tensor products give a strongly
continuous representation for each finite endpoint group.

The local automorphism `beta_g` preserves each coarse support `F`: it
conjugates within the owned link factors without adding a link. It fixes
each electric term, and the vertex factors cancel around every complete
Wilson face. The onsite shifted Hamiltonians and the retained-star finite
Hamiltonians therefore commute with the appropriate endpoint gauge
products on their actual domains. The bounded perturbations do not
change those domains. Incomplete head-only or tail-only actions would
not have this property.

Their unique ground vectors can initially acquire a continuous phase
character. That phase is trivial for a finite product of SU(2): every
element of SU(2) is conjugate to its inverse, so a one-dimensional
character has value equal to its inverse and hence lies in `{+1,-1}`;
connectedness and its value at the identity force `+1`. Apply the same
argument componentwise to the product. Both the reference onsite vacua
and the finite interacting ground vectors are therefore fixed, not just
fixed up to an unspecified phase. The finite states are invariant, and
(5) gives `omega(beta_g A)=omega(A)` for every local `A`. Norm continuity
of states and the isometric automorphisms extend invariance to the
quasilocal C*-algebra `A=closure_norm union_F B(K_F)`.

Consequently the prescription

\[
 U_\omega(g)\pi(A)\Omega=\pi(\beta_g A)\Omega              \tag{15}
\]

respects the GNS null ideal, preserves inner products and has the inverse
defined by `g^-1`. It extends to a unitary representation with fixed
vacuum. For local `A`, the map `g -> beta_g A` is strong-* continuous
and uniformly bounded in its original local factor. Local normality gives

\[
 \|[U_\omega(g)-U_\omega(g_0)]\pi(A)\Omega\|^2
 =\omega((\beta_g A-\beta_{g_0}A)^*
              (\beta_g A-\beta_{g_0}A))\longrightarrow0. \tag{16}
\]

For example, diagonalize the trace-class local density and apply bounded
dominated convergence to its vector-state sum. Density and unitarity
extend (16) to every vector for each finite endpoint group. This is
strong unitary continuity. Conjugation on *all* bounded local operators
need not be point-norm continuous; no such claim is used.

## 5. Compatible Haar averages and the physical GNS identification

Let `V(F)` be the finite set of endpoints of all links owned by `F`, and
`K_(V(F))=product_(v in V(F)) SU(2)`. Define in the original local factor

\[
 E_F(A)=\int_{K_{V(F)}}\beta_g(A)\,dg                     \tag{17}
\]

by its weak operator matrix elements with normalized Haar measure.
The integrands are bounded and strong-* continuous, so this defines a
bounded operator of norm at most `||A||`. It remains in `B(K_F)`; positivity,
unitality and Haar translation invariance show it is a contractive local
conditional expectation onto the invariants. Gauge transformations at
vertices outside `V(F)` act trivially on this factor, so `E_F(A)` is
invariant under **every** local gauge transformation. Enlarging the
declared coarse support introduces only endpoint actions already trivial
on `A` or spectator link factors, so the embedded average is compatible
with that enlargement.

Strong continuity of (15) gives the strong vector integral on the right
of the following identity:

\[
 \pi(E_F(A))\Omega
       =\int_{K_{V(F)}}U_\omega(g)\pi(A)\Omega\,dg .      \tag{18}
\]

To prove it, pair both sides with `pi(B)Omega` for arbitrary bounded
local `B`. In the larger finite factor containing `A,B`, (14) supplies
the normal linear functional `X -> omega(B^*X)`. It passes through (17)
and gives exactly the matrix element of the vector integral. Equality
on a dense set of testing vectors proves (18). This explicitly uses the
regularity proved above, not a formal passage of WOT through an arbitrary
representation.

Define `A_phys` as the norm closure of the full bounded local algebra
invariant under every local gauge transformation, and set

\[
 H_{\rm cyc}=\overline{\pi(A_{\rm phys})\Omega},\qquad
 H_{\rm fix}=\{\psi:U_\omega(g)\psi=\psi
                       \text{ for every local }g\}.      \tag{19}
\]

The first is contained in the second by (15). Conversely, take
`psi in H_fix` and a local `A` with `||pi(A)Omega-psi||<epsilon`.
The Haar integral of `U_omega` over `K_(V(F))` is the orthogonal fixed
projection `P_(V(F))`; it fixes `psi` and has norm one. Using (18),

\[
 \|\pi(E_F(A))\Omega-\psi\|
 =\|P_{V(F)}(\pi(A)\Omega-\psi)\|<\varepsilon.             \tag{20}
\]

Its first vector belongs to the physical cyclic space. Hence
`H_cyc=H_fix`. Only finite groups were averaged; no Haar measure or
global infinite-product unitary conjugation was introduced. Replacing
`A_phys` by a Wilson-only algebra would require a separate density proof
and is not done here.

For completeness let `omega_phys=omega|_(A_phys)` and
`N_phys={A in A_phys: omega(A^*A)=0}`. This is the usual GNS left null
ideal. On its quotient the inner product is
`<[A],[B]>=omega(A^*B)`. The map

\[
 J:[A]\longmapsto\pi(A)\Omega                            \tag{21}
\]

is well-defined and isometric, with dense range in `H_cyc`. Its extension
is a unitary from the physical GNS Hilbert space onto (19), intertwining
the left multiplication representation and taking `[1]` to `Omega`.
Faithfulness of the state is not assumed or needed.

## 6. The actual closed generator and physical units

Fix a finite endpoint gauge element `g`. Each finite centered resolvent
commutes with its full endpoint implementer, and its ground is fixed.
For sufficiently large volumes containing the bounded local `A,B`,

\[
 \langle R_\Lambda(z)\beta_g(A)\Omega_\Lambda,
                      \beta_g(B)\Omega_\Lambda\rangle
 =\langle R_\Lambda(z)A\Omega_\Lambda,B\Omega_\Lambda\rangle,
 \quad R_\Lambda(z)=(\widehat H_\Lambda-E_\Lambda-z)^{-1}.
                                                               \tag{22}
\]

No support enlargement of `A,B` is required by the local gauge action.
Pass to the *tested* limit (6). Equation (15), density, and boundedness
of the resolvent give

\[
 U_\omega(g)^*(G-z)^{-1}U_\omega(g)=(G-z)^{-1}.            \tag{23}
\]

This proves commutation with the actual self-adjoint closed generator,
including its domain, without claiming that every bounded-local vector
is in that domain. It is also consistent with the inherited creation
core: gauge transformations preserve each `Omega_b^0`, each
`D(H_(0,I))` and `H'_I`, hence its specified domain-qualified vectors.

Both `(G-z)^-1` and its adjoint preserve the joint fixed space by (23).
Thus `H_cyc=H_fix` reduces the resolvent, and consequently reduces all
spectral projections of `G`. Its orthogonal projection `P_phys` strongly
commutes with `G`. The physical GNS generator transported by (21) is the
self-adjoint restriction

\[
 G_{\rm phys}=G|_{H_{\rm cyc}},\qquad
 D(G_{\rm phys})=D(G)\cap H_{\rm cyc},\qquad
 D(G_{\rm phys}^{1/2})=D(G^{1/2})\cap H_{\rm cyc}.          \tag{24}
\]

The inherited centered vacuum remains the unique ground. Its quadratic
form obeys the inherited inequality
`G_phys >= (1/2)(I_phys-|Omega><Omega|)` on the stated form domain.
In physical units the energy generator is

\[
 H_{\rm phys}=\delta G_{\rm phys},\quad
 \delta=\alpha/8,\qquad
 \text{frequency generator}=\delta G_{\rm phys}/\hbar.    \tag{25}
\]

Thus its spectrum is contained in `{0} union [alpha/16,infinity)` and
the dimensionless threshold in units `E_star` is
`(alpha/E_star)/16`. This is a reducing restriction, not a formal
compression, and no scalar ground energy has been reintroduced. A
vacuum-only physical Hilbert space would also satisfy this inequality;
AJ1 has not established a nonzero homogeneous Wilson fluctuation. In
particular (25) is not an evaluated mass, a continuum construction, or a
new quantitative stability theorem.

## 7. Exact fixtures, controls and reproducibility

The independently written standard-library checker enumerates all owned
links, every selected and omitted face with four oriented edges, actual
coarse supports, complete-star retention and all endpoint gauge supports.
The one-block omitted support multiplicities are `1,3,1,10,2,4` for
`{0,ex}`, `{0,ey}`, `{0,ex,ey}`, `{0,ez}`, `{0,ex,ez}`, `{0,ey,ez}`.
Their union is the entire star. Remainder arithmetic in Section 1 and
the inverse-incidence formula in Section 2 prove the corresponding
all-volume facts; the finite enumerations audit those formulas.

| Coarse side counts | Owned links | All endpoints | Retained complete stars | Retained omitted faces | Individually contained omitted faces, different boundary |
|---|---:|---:|---:|---:|---:|
| `(2,2,2)` | 192 | 120 | 1 | 21 | 70 |
| `(3,2,2)` | 288 | 176 | 2 | 42 | 110 |
| `(3,3,3)` | 648 | 342 | 8 | 168 | 336 |

The singleton coarse region has 24 links and 22 endpoint vertices; the
specified pair has 48 links and 42 endpoints. For the interior singleton
`(1,1,1)` in `(3,3,3)`, the four incident anchors are itself and
`(0,1,1),(1,0,1),(1,1,0)`. Counting only its outgoing anchor loses three
groups. The reset bound keeps all `4*21=84` group faces even though only
49 individual faces actually touch this singleton. In the two smaller
fixtures this same coordinate has zero retained incident stars; the
checker preserves that finite-boundary fact instead of pretending it is
already a bulk interaction environment.

Rational unit quaternions implement genuine SU(2) gauge transformations
on an omitted xz square. Its normalized Wilson trace stays `808/1105`;
dropping head actions changes it to `44181/93925`. An open-link quaternion
changes. The exact eight-element quaternion group closes under
multiplication; its finite averages kill the tested fundamental charged
first moment and preserve the closed trace at every endpoint. These
finite first moments agree with the corresponding SU(2) first moments,
but the finite group is not a replacement for SU(2) Haar on all operators
or for the connected SU(2) character argument.

The checker also executes these discriminating diagnostics, whose
infinite extensions or limitations are explicit:

* **Reset cancellation:** in an abstract two-factor four-dimensional
  system, `rho` is the Bell projector, `H=I-rho`, and
  `H0=diag(0,1,1,2)`. Resetting only the first factor to its vacuum keeps
  the complementary energy `1/2`, removes local energy `1/2`, changes the
  interaction expectation by `5/4`, and raises total energy by `3/4`.
  The self-adjoint interaction has the certified row-sum norm ceiling 2.
  Adding scalar `7I` leaves the energy difference unchanged. This checks
  (10)'s algebra; the unbounded-domain and all-volume proof is Section 2.
* **Summable substitution:** finite prefixes have constant-coupling norm
  budgets `N M`, whereas an explicitly abstract dyadic series has budget
  `1-2^-N`. The actual same-sign Wilson potential attains its finite norm
  budget near the identity, so its homogeneous total does not define a
  uniformly bounded global perturbation. The checker labels I1's
  normalized `1/2` and the different J2 `973/1080` as distinct model
  data; J2's stronger number is not transferred.
* **Automatic normality and unjustified WOT passage:** on `B(ell2)`, let
  `rho_n=|e_n><e_n|`. Any weak-star subnet limit gives every fixed finite
  rank projection `P_m` value zero but gives `I` value one. It is singular.
  Its GNS representation annihilates all finite-rank operators (test
  `omega(A^*P_m A)=0`) while preserving `I`; it therefore does not
  preserve `P_m -> I` strongly/WOT. Exact finite prefixes detect the
  escape. This rejects the generic continuity principle that would be
  needed for an unjustified integral interchange; it is not advertised
  as a special counterexample to (18), whose regularity is proved.
* **Strong versus norm continuity:** on `ell2(N)`, use
  `U(t)e_n=e^(int)e_n` and the isometry `S e_n=e_(2n)`. The unitary group
  is strongly continuous, but at `t_k=pi/k`, the vector `e_k` gives
  `||(U(t_k) S U(t_k)^*-S)e_k||=2`. Thus the conjugation norm difference
  equals 2 along a sequence tending to zero. Integer phase witnesses are
  checked exactly, with no floating-point trigonometry.
* **Arbitrary bounded-local domain membership:** take a vacuum `e_0`,
  `G e_n=n e_n`, and `psi=sum_(n>=1)n^-1 e_n`. Its squared norm is
  bounded by 2, but its squared generator norm has prefix `N` and
  diverges. The bounded rank-one operator `|psi><e_0|` takes the vacuum
  out of `D(G)`. Exact prefix sums verify the discriminating behavior;
  no finite truncation alone establishes the infinite divergence.
* **Compression:** `H=[[1,1],[1,1]]` has spectrum `{0,2}` while its
  compression to the first coordinate is 1. The corresponding projection
  fails to commute with `H`. This prevents replacing (23) by a bare
  compression assertion.
* **Ground center, physical scale and excitation:** an abstract units
  fixture with `alpha=24`, `delta=3`, `hbar=2` and raw normalized
  energies 7 and 9 has centered normalized excitation 2, energy 6 and
  frequency 3. Separately, `G=diag(0,1)` with the reducing physical
  projection onto its vacuum has no excited physical vector and zero
  scalar-observable variance, despite satisfying every positive
  restricted-gap lower inequality. Neither diagnostic chooses an
  actual positive homogeneous `tau` or claims a Wilson witness.

All pass/fail checks use explicit exceptions, so optimized Python cannot
remove them. There were no failed scientific attempts. The first successful
fixture pass was followed by additive Q8 closure and finite reset checks;
its code and outputs are preserved in `development/first-fixture-pass/`.
The final normal and optimized fresh replays must produce byte-identical
`results.json` and `source-manifest.json`, whose source hashes include the
frozen input pack and the actual checker. Exact commands and their observed
hashes are recorded in `validation.json`. To reproduce independently:

```bash
python -B research/round28/forward/aj1/check.py --output /tmp/ym28-forward-aj1-normal
python -B -O research/round28/forward/aj1/check.py --output /tmp/ym28-forward-aj1-optimized
```

Both output paths must be absolute and nonexistent. Finite checks are
support, arithmetic and countermodel audits, not substitutes for Sections
2–6 or new physical observations. The final freeze binds the complete owned
file closure, including nested historical `freeze.json` source snapshots;
only its own exact top-level `freeze.json` is excluded.

The frozen current draft/network are used with their six-loop model scopes
intact: AG's spent support-weight estimates provide no numerical I1 gap,
AI's candidate-indexed probes provide no representation premise, and AH's
finite heat certificates provide no infinite homogeneous state. I1's
qualitative construction and J2's distinct summable representation retain
their existing attribution. No AJ2 question, new cell, numerical coupling
threshold, Wilson variance or later-goal investigation was executed here.
