# AG2 forward: the complete original remainder and its transported reference

The original O1 remainder can be inventoried completely at weight `rho=9/4`
and transported through the actual admitted AG1 correction. The resulting
scalar, mixing and centered reference-diagonal interactions have uniform
finite-cuboid bounds. The new reference alone has normalized gap greater than
`99/100` on `0<=M<=1/1000`, and greater than `999/1000` on the inherited narrow
interval `0<=M<=1/10000`. Its remaining mixing is retained. No gap of the full
corrected Hamiltonian, complete-mixing contraction or second correction follows.

This is an independent forward derivation under the frozen AG2 contract. The
current reverse AG2 solution has not been read. Existing instruction/source
snapshots were verified and adopted without replacement before production;
`adoption.json` records that provenance. No prior scientific producer output was
present. The historical/source triage is separate from this executed loop.

## 1. Original transformation, notation and domain

Keep the homogeneous complete24-link coarse blocks, all21 omitted faces on each
retained complete star `Z_b=b+{0,e1,e2,e3}`, and the original finite cuboid
boundary. Work in the fixed physical energy unit `delta=alpha/8`. The positive
spacing and `E_star,alpha/E_star,hbar` remain fixed. `tau` is the original
homogeneous interaction coefficient, `M=7|tau|`; support weights and the AG1
filter duration `T=3` are dimensionless proof parameters.

The actual onsite reference satisfies `H0=sum h_x`, `h_x>=I-P_x`, with product
vacuum Omega and its finite-sum unbounded operator domain. On each star write

```
v_b=phi_b Omega_b, u_b=(H0,Z_b|Q_b)^(-1)v_b,
S1_b=|u_b><Omega_b|-adjoint,
A1_b=|v_b><Omega_b|+adjoint,
D_b=Q_b phi_b Q_b, X=sum_b S1_b,
Phi=sum_b phi_b, A1=sum_b A1_b, D=sum_b D_b, G=H0+D.
```

The inherited actual Haar variance gives `||v_b||=sqrt(7/12)|tau|`.
For rational budgets set

```
s=sigma=4M/35=(4/5)|tau|,
||S1_b||<=s, ||A1_b||<=sigma, ||phi_b||<=M.
```

These are upper certificates, not operator-norm equalities. In particular
`sqrt(7/12)<4/5` supplies the rational relaxation without changing the model.

Because `u_b,Omega_b` are in the local reference domain and `H0,Z_b u_b=v_b`,
`[S1_b,H0]=-A1_b` on `D(H0)`, with bounded extension. Strong commutation with
the exterior energy proves preservation of this domain, not regularization of
arbitrary exterior vectors. The finite sum X is bounded in its graph norm, so
`exp(+-X)` preserves `D(H0)`. First integrate this bounded commutator; only then
expand the bounded interactions. The exact inherited identity is

```
Hbar=exp(X)(H0+Phi)exp(-X)=G+R_O1,
R_O1=sum_(n>=1) [ad_X^n(Phi)/n! - ad_X^n(A1)/(n+1)!].             (1)
```

Each finite volume has a bounded perturbation and the same operator domain.
The series is a norm-convergent bounded-operator series there. The following
support estimates establish its stronger volume-independent local summability;
they do not construct a bounded infinite global X or a new representation.

## 2. Exact four-part E inventory

At depth n pair the two terms in (1) with the same ordered anchor history
`(b0;b1,...,bn)` and declare their support to be the complete union of the
stars. This pairing is an explicit indexed decomposition. Repeated anchors
and different orderings remain distinct. A new star disjoint from the current
union gives zero; every remaining union has at most `4+3n` sites. No additional
cancellation is assumed.

For a repeated-anchor depth-two history let

```
C_b=(1/2)ad_(S1_b)^2(phi_b)-(1/6)ad_(S1_b)^2(A1_b),
A3_b=P_b C_b Q_b+Q_b C_b P_b, A3=sum_b A3_b.
```

This is precisely the S1/AG1 selected cubic source, with
`w_b=-<u_b,v_b>u_b-||u_b||^2 v_b/3` and `A3_b=|w_b><Omega_b|+adjoint`.
It is not the original A1, total cubic coefficient or full remainder. Define

```
E=R_O1-A3=E2+E3,same+E3,other+E>=4,                           (2)
E2=[X,Phi]-(1/2)[X,A1]=[X,D]+(1/2)[X,A1],
E3,same=sum_b(C_b-A3_b),
E3,other=all other depth-two ordered histories,
E>=4=all histories of depths n>=3 with their original factorials.
```

The support maxima of the first three components are respectively7,4,10;
the tail has arbitrary finite connected unions. Their algebraic lowest degrees
are2,3,3,4. This does not assert that each component is nonzero in the actual
model. In particular no premise makes E2 purely scalar or reference diagonal.

There is no additional omitted mixing charge on a same-anchor cubic history:

```
C_b-A3_b=P_b C_b P_b+Q_b C_b Q_b,
||C_b-A3_b||<=||C_b||<=4s^2(M/2+sigma/6).                     (3)
```

The first norm inequality follows from orthogonal block compression. Its
scalar and centered complement remain
`c_b I+Q_b(C_b-c_b I)Q_b`, `c_b=<Omega_b,C_b Omega_b>`.
Adding `c_b I+Q_b C_b Q_b` would double-count `c_b Q_b`.
Absolute support convergence below justifies this regrouping of (1).

## 3. Complete geometry and all-order bound at the actual input weight

Use `||B||_a=sup_x sum_(Y contains x) a^|Y| ||B_Y||`, with all indexed
multiplicities retained and `a>=2`. For a fixed ordered relative history with
union Y, there are exactly `|Y|` translations whose union contains a fixed root
on the full integer lattice. Positive-octant complete-cuboid restrictions only
delete histories. Thus relative geometry supplies a uniform root majorant
without adding physical interactions outside the frozen boundary.

An incoming anchor meeting Y is exactly an element of
`{y-z:y in Y,z in Z_0}`. This identity makes the finite depth-one/two inventory
exhaustive, not a spatial sampling rule. Let `c_(n,m)` count relative histories
of depth n and union size m, starting at anchor0, and set

```
Q_n(a)=sum_m m c_(n,m) a^m.
Q_0(a)=4a^4, Q_1(a)=4a^4+84a^7.                             (4)
```

The only size-four depth-two history is `(0;0,0)`. The checker enumerates the
entire finite sets of incoming anchors at these two depths, records the exact
`c_(2,m)` table and Q2, and checks empty, one-star and interior finite boundaries.
It finds `(c_(2,4),c_(2,7),c_(2,9),c_(2,10))=(1,36,24,192)`, hence
`Q2(a)=4a^4+252a^7+216a^9+1920a^10`. This supplies an explicit rational
polynomial for the low order. It is not the proof of the infinite tail.

For that tail, a new commutator costs at most `2s a^3`. If the old union has
`k_n<=4+3n` sites, at most `4k_n` incoming stars meet it. Counting roots in the
incoming star as well costs at most another16 root incidences. Therefore the
unfactorialized depth-n root sum for a seed bound b obeys

```
N0(a)<=4a^4 b,
N_(n+1)(a)<=8s a^3(8+3n)N_n(a),
N_n(a)<=4a^4 b (24s a^3)^n (8/3)_n.                         (5)
```

The two root locations can overlap; this harmless overcount includes them both.
The argument applies at every n with repeated histories retained. With
`x=24s a^3`, the factorialized coefficient is bounded by `(8/3)_n/n!`.
For every n, factorwise comparison with `(3)_n/n!` bounds this by
`(n+1)(n+2)/2`. Its generating function is `(1-x)^(-3)` for `0<=x<1`.
At depths n>=3, the A1 coefficient is at most sigma/4 relative to the Phi
coefficient. Consequently a complete four-part majorant is

```
e2(a)=2s(M+sigma/2)Q1(a),
u3=4s^2(M/2+sigma/6),
e3,same(a)=u3*4a^4,
e3,other(a)=u3*(Q2(a)-4a^4),
e>=4(a)=4a^4(M+sigma/4)[(1-x)^(-3)-1-3x-6x^2],
e(a)=e2(a)+e3,same(a)+e3,other(a)+e>=4(a),  ||E||_a<=e(a).    (6)
```

This counts the compressed same-anchor word once, instead of adding its
selected mixing norm to an already complete cubic budget. For comparison an
independently valid, looser triangle estimate is

```
e_triangle(a)=4a^4(M+sigma/2)[(1-x)^(-3)-1]+4a^4 M^3/567.     (7)
```

Here the last term bounds the selected A3 and uses the inherited rational
`r=||A3_b||<=M^3/567`. Formula(7) is a full-R-plus-A3 upper budget; neither
formula is a measured norm. At `a=rho=9/4`, `x=(2187/70)M`, so the entire
continuous main interval has `x<=2187/70000<1`. All factors in (6) have
nonnegative power series in M; the tail begins at M^4. Endpoint evaluation
therefore bounds the full continuous interval. Q2 is a finite exact geometry
polynomial and (5) proves the all-order completion.

## 4. Actual AG1 transport, with every original term retained

Use the admitted AG1 generator S, constructed from the actual A3 by the
triangular strong filter under G at T=3. This is distinct from X. Its bounded
weak commutator identity is `[S,G]=-A3+R_A3`; the adjoint-domain argument proves
graph preservation, and its finite-volume exponential preserves `D(G)=D(H0)`.
E is bounded in finite volume. Its conjugation needs no extra assertion that
E itself preserves this domain. The exact full identity is

```
exp(S)Hbar exp(-S)=G+K,
K=R_A3+N+exp(ad_S)E,
N=sum_(n>=1) ad_S^n(n A3+R_A3)/(n+1)!.                      (8)
```

In particular E is neither deleted nor replaced by a quartic-only tail.
The first nonlinear term is `[S,A3+R_A3]/2`; a G-only BCH formula is incomplete.

For self-contained rational evaluation of the inherited AG1 budgets define

```
rbd=M^3/567, A3rho_bd=4rho^4 rbd, A3two_bd=64rbd,
Fag=(1-72rho^3 M)^(-3), theta=18 A3rho_bd Fag,
n2=theta/(1-theta)*A3rho_bd*(1+Fag/2),
r2_main=A3two_bd*(1-576M)^(-3),
r2_narrow=A3two_bd*[4/9+(1-576M)^(-3)-1].                   (9)
```

The narrow residual estimate is used only for M<=1/10000, where AG1 proved it
from the free source gap and the positive interaction tail. On the main interval
`72rho^3 M<=6561/8000<1` and theta<1. The weight-loss commutator estimate,
allocated equally across n nested commutators, gives
`||ad_S^n B||_2/n!<=theta^n ||B||rho`. Thus

```
||exp(ad_S)E||_2<=e(rho)/(1-theta),
||K||_2<=k(M):=r2+n2+e(rho)/(1-theta).                     (10)
```

Every displayed factor increases with M in the stated interval; the narrow
factor has nonnegative constant4/9 and positive higher coefficients. These
facts justify continuous bounds from the exact rational endpoint outputs.
The direct inventory and the triangle bound are both reported there. Comparing
their endpoint upper budgets is not a lower bound on actual E or its mixing.

The entire `rho -> 2` margin has been spent. No operation in (8)-(10) gives
the same next source a new rho-bound by renaming the weight.

## 5. Complete output split and a reference-only gap

For every self-adjoint indexed support term K_Y in (8), including each transported
E term, let `P_Y=|Omega_Y><Omega_Y|`, `Q_Y=I-P_Y`, and set

```
c_Y=<Omega_Y,K_Y Omega_Y>, B_Y=P_Y K_Y Q_Y+Q_Y K_Y P_Y,
Z_Y=Q_Y(K_Y-c_Y I)Q_Y,
K_Y=c_Y I+B_Y+Z_Y,
|c_Y|<=||K_Y||, ||B_Y||<=||K_Y||, ||Z_Y||<=2||K_Y||.         (11)
```

Declare all scalar supports to be their original indexed unions. Every union
has at least four sites, even if a term simplifies to a scalar operator. These
actual support costs give stronger intensive bounds than treating supports as
single sites. By double-counting scalar terms over their sites,

```
|sum c_Y|/|Lambda| <= k(M)/64,
||B||_2<=k(M), ||Z||_2<=2k(M), ||D+Z||_2<=64M+2k(M).        (12)
```

Indeed `1/(|Y|2^|Y|)<=1/64` for |Y|>=4. Since each Z_Y annihilates its local
vacuum, `|<psi,Z_Y psi>|<=||Z_Y||<psi,Q_Y psi>` and
`Q_Y<=sum_(x in Y)(I-P_x)`. Therefore

```
|<psi,Z psi>|<= [2*2^(-4) k(M)] <psi,H0 psi>
             =k(M)/8 <psi,H0 psi>,
|<psi,(D+Z)psi>|<=[4M+k(M)/8]<psi,H0 psi>.                 (13)
```

The initial coefficient4M counts all four incoming stars. In each finite
volume the absolutely convergent interaction sum Z is bounded, so
`G_next=H0+D+Z` is self-adjoint on `D(H0)`, separately from the form argument.
It annihilates Omega, and

```
G_next >= (1-kappa) H0 >= (1-kappa)(I-P_Omega),
kappa=4M+k(M)/8.                                          (14)
```

Exact endpoint tests establish `1-kappa>99/100` on the main interval and
`>999/1000` on the narrow interval. These are finite-volume reference gaps,
uniform in containing cuboids, multiplied by delta in physical energy units.
Including the scalar C shifts the reference ground energy to C without changing
that gap. C is a reference expectation sum, not the full interacting ground
energy while B is present. Equation(8) is `C I+G_next+B`, and the term B is
retained with its complete bound. A stability theorem for this last Hamiltonian
is not a consequence of (14).

The following rounded values are outward bounds checked against the exact
fractions in `output/results.json`. Each endpoint upper bound covers its
continuous interval by the monotonicity arguments above.

| Quantity | Main M<=1/1000 | Narrow M<=1/10000 |
|---|---:|---:|
| Direct complete E at rho | <0.006168 | <0.000059689 |
| Complete output K at weight2 | <0.006168 | <0.000059689 |
| Scalar density | <0.00009637 | <0.0000009327 |
| Reference-only normalized gap | >0.995229 | >0.9995925 |

The looser triangle E endpoint budgets are approximately0.01082710 and
0.000102216, respectively; they are additional sufficient upper bounds and
are not estimates of exact E. The full rational values are retained.

## 6. What is disproved, what remains missing, and controls

For every fixed nonempty finite cuboid, inherited O1 analyticity and actual
Wilson-face orthogonality give
`<Omega,R_O1 Omega>=-a_Lambda tau^2+O_Lambda(|tau|^3)` with
`a_Lambda=<U1,H0 U1>>0`. Every A3_b has zero vacuum expectation, so the same
leading coefficient holds for E. Thus the actual E cannot be O(tau^4) in
operator norm in that fixed volume. This actual-model argument is distinct
from the checker’s rational matrix diagnostic. It does not calculate the
full quadratic mixing or a volume-uniform lower coefficient.

No contraction of full B is inferred from a ratio of upper certificates.
The selected-source AG1 denominator is valid for its own source and does not
become an actual full-input denominator after E is restored. A large
E-budget/A3-budget ratio proves neither physical dominance nor failure of the
actual correction. The new reference has a proved local vacuum gap, but an
identity-extended full source inverse still needs its own all-sector/domain
and boundary analysis. AG3 must be selected after review with the generated
support class and an available weight budget; it has not been executed here.

The checker uses only standard-library exact rational arithmetic. Independent
matrix multiplication of the two exponential series reconstructs O1 through
degree6, for positive, negative and zero signs. A separate overlapping
three-qubit fixture retains exterior identities and rejects deleting cross
quadratic/cubic words. Wrong n1/n2 coefficients, scalar double counting,
missing E transport and a quartic-only E assignment are discriminating
controls. A second formal-parameter reconstruction of (8) tests the complete
nonlinear coefficients and E transport through degree6. These matrices are
algebra controls, not physical SU(2) discretizations or gap simulations.

The unbounded-domain counterexample `v_j=1/j`, `H e_j=j e_j` distinguishes a
bounded rank-two map from a domain-preserving one: v is square-summable while
Hv is not. The sequence `sin(nt)/n` converges uniformly to0 but has derivative1
at0, rejecting differentiation of a value estimate. Their finite arithmetic
prefixes corroborate the explicit series/derivative statements, not an
infinite-dimensional proof by sampling. No such shortcut is used above.

The mathematical source premises are the contract-bound O1/O2/S1 and AG1
reports and scope instructions. The external historical/modern reading is
documented in the expert triage; no external theorem threshold is imported.
Scientific priority is unverified. Infinite-volume representation transfer,
physical matching and the four-dimensional continuum Yang–Mills construction
and mass gap remain open.

Reproduce with fresh absolute directories:

```
python3 -B research/round28/forward/ag2/check.py --output /absolute/new/ag2-forward
python3 -B -O research/round28/forward/ag2/check.py --output /absolute/new/ag2-forward-O
```

The checker binds every contract source, retained instruction snapshot and
executed producer file. Normal and optimized outputs must agree byte-for-byte.
