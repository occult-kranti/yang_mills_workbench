# AG3 forward: one correction of the complete mixing source

For the complete AG2 mixing family B, one bare-reference correction satisfies

```
||R_next||_(3/2) <= (3060/3623) ||B||_2 < (17/20)||B||_2
```

when `0<M=7|tau|<=1/1000` and B is nonzero. The narrow interval
`M<=1/10000` gives the stronger factor `5949/96812<1/16`. At B=0 the
correction and remainder vanish. These compare different support weights.
Every retained diagonal and scalar term is included; the new centered reference
alone has a positive gap. No same-weight contraction, all-stage convergence or
gap of the full Hamiltonian is established.

The advisor's pre-freeze interpretation check supplies an essential comparison:
doing no correction and merely lowering the weight already gives
`||B||_(3/2)<=(81/256)||B||_2`. The main factor is weaker than this passive
upper bound. The narrow factor is stronger than this common passive upper
bound, but it is still not a comparison to the actual old `||B||_(3/2)`.
Thus the main result certifies the complete controlled step; its factor alone
does not establish a benefit over leaving B unchanged at the lower weight.

This forward derivation was executed after the AG3 contract freeze and before
reading current reverse AG3 work. The bare-inverse route was proposed in the
Newton post-AG2 review. The advisor proposed the overlap refinement and numerical
target, which both workers and skeptic discussed prospectively. That shared
contract context is attributed here rather than called independent discovery.
The proof and executable below independently verify its required implications.

## 1. Actual source, decomposition and domain

The admitted complete finite-cuboid operator is

```
H_full=C I+H0+D_next+B, D_next=D+Z,
B_Y=P_Y K_Y Q_Y+Q_Y K_Y P_Y,
c_Y=<Omega_Y,K_Y Omega_Y>, Z_Y=Q_Y(K_Y-c_Y I)Q_Y.             (1)
```

Here K is the complete AG2 output, including the transported original E. Use its
declared paired O1 histories, compressed same-anchor cubic histories, remaining
ordered histories, AG1 filtered source histories and nonlinear/transported union
histories. Split each such self-adjoint K_Y as in (1); retain every index and
assigned union. Coincident supports are not canceled or assigned smaller support
to change the denominator. All assigned supports are finite connected unions
of complete coarse blocks, of size at least four, with no uniform upper size.
The sum is the complete original transformed Hamiltonian, not selected G+A3.

For `||V||_a=sup_x sum_(indexed Y contains x) a^|Y| ||V_Y||`, define

```
r=||B||_2, d=||D_next||_2, k=an admitted upper bound on ||K||_2.
r<=k, d<=64M+2k,
|C|/|Lambda|<=k/64,
|<psi,D_next psi>|<=(4M+k/8)<psi,H0 psi>.                  (2)
```

Common conservative caps are `k<=7/1000` on the main interval and
`k<=7/100000` on the narrow interval. The actual r, not k, is the final
multiplicative input in every reduction claim. The indexed interaction norm is
not the norm of the extensive total operator.

Write `H0,Y=sum_(x in Y)h_x`; its product vacuum is unique and
`H0,Y>=Q_Y`. For each actual B_Y set

```
v_Y=B_Y Omega_Y, u_Y=(H0,Y|Q_Y)^(-1)v_Y,
X_Y=|u_Y><Omega_Y|-|Omega_Y><u_Y|.                          (3)
```

Because B_Y is exactly a local vacuum/complement block, v_Y is orthogonal to
Omega_Y and `||B_Y||=||v_Y||`. Spectral calculus on the reduced positive
operator gives `u_Y in D(H0,Y)`, `H0,Y u_Y=v_Y`, and
`||X_Y||=||u_Y||<=||v_Y||`. Its local products with H0,Y have bounded
extensions, and `[X_Y,H0,Y]=-B_Y` on the local operator domain.

Identity extension commutes with the exterior spectral resolution. For the
finite nonnegative tensor sum, `D(H0)=D(H0,Y) intersect D(H0,exterior)`.
Thus X_Y preserves this full domain and `[X_Y,H0]=-B_Y` there. It does not
regularize an arbitrary exterior vector. A global vacuum projector would give
a different operator and would not cancel the identity-extended source on an
excited exterior sector.

Let X be the sum of every indexed X_Y. In finite Lambda,
`sum_Y ||B_Y||<=|Lambda|r/64`: distribute each term over its sites and use
`1/(|Y|2^|Y|)<=1/64`. The same bound holds for the X_Y sum. Their commutators
also converge absolutely. The relation `H0 X_Y=X_Y H0+B_Y` bounds each map
on the graph norm; summability therefore gives a bounded skew X on that graph
space, `[X,H0]=-B`, and `||X||_2<=r`. The graph-space exponential and its
inverse imply `exp(+-X)D(H0)=D(H0)`. All other full finite-volume interactions
are bounded, so their Hamiltonians have the same operator domain. No bounded
infinite extensive generator or infinite global unitary is inferred.

## 2. Root counting below weight two

For `a>b>1`, keep every ordered pair of intersecting indexed supports U,V and
declare the commutator support to be their full union. Nonempty intersection
gives `b^|U union V|<=b^|U| b^|V|/b`. The operator commutator costs factor2.
For a fixed root x in U, summing all V meeting U costs at most
`|U| ||V_family||_b`. With `ell=log(a/b)>0`,
`m exp(-ell m)<=1/(e ell)`. Hence this root assignment costs at most

```
2/[b e log(a/b)] ||U_family||_a ||V_family||_a.
```

Roots in V have an equal upper bound. Counting roots in both supports twice
only increases the positive sum. Therefore

```
||[U_family,V_family]||_b
 <=4/[b e log(a/b)] ||U_family||_a ||V_family||_a.          (4)
```

This is a new proof for the stated range, not reuse of the old lemma restricted
to output weight at least two. No finite support-size restriction appears.
Repeated supports and a new support meeting only an already generated union
are retained. The two root assignments and the overlap factor are both needed.

Let `ell=log(4/3)` and allocate ell/n at each of n brackets from weight2 to
weight3/2. Every intermediate output weight is at least3/2. Applying (4) and
using monotonicity of the X norm as weights decrease gives

```
||ad_X^n V||_(3/2)/n! <= [(8/3)r/ell]^n ||V||_2.          (5)
```

Indeed the iterated constant before division by n! is
`[(8/3)n r/(e ell)]^n`. The elementary integral estimate
`log(n!)>=integral_1^n log t dt=n log n-n+1` yields
`n!>=(n/e)^n`, canceling the factors n and e.

The logarithm constant is also explicit. On `0<=t<=1/3`,
`1/(1+t)=1-t+t^2-t^3+t^4/(1+t)`. Integration gives

```
ell>=1/3-1/18+1/81-1/324=31/108,
c=(8/3)/ell<=cbar=288/31.                                (6)
```

The rational upper bound cbar will be used below. Equations(4)-(6) account for
the whole support loss at each order of the infinite series.

## 3. Full conjugation and actual-input estimate

First integrate the established bounded commutator on D(H0):

```
exp(X)H0 exp(-X)=H0-integral_0^1 exp(t ad_X)B dt.
```

Expand only B and D_next afterward. Their terms combine to give exactly

```
exp(X)(C I+H0+D_next+B)exp(-X)=C I+H0+D_next+R_next,
R_next=sum_(n>=1) [ad_X^n D_next/n! + n ad_X^n B/(n+1)!].  (7)
```

The scalar remains unchanged. In particular the first remainder is
`[X,D_next]+[X,B]/2`. The bare inverse does not remove the retained-D
commutator; no inverse involving excited gaps of D_next is assumed.

Set `theta=cbar r`. For theta<1, (5) and `n/(n+1)<=1` imply

```
||R_next||_(3/2) <= (d+r) sum_(n>=1)theta^n
                  =r cbar(d+r)/(1-cbar r).                (8)
```

The tail after order N is bounded by
`(d+r)theta^(N+1)/(1-theta)`. This proves the entire infinite completion;
finite matrix Taylor checks are not substituted for it. In each finite volume
the support-norm convergence also implies bounded operator convergence, so it
identifies the bounded-domain expression (7).

The coefficient multiplying r in (8) increases with nonnegative r and d.
Use (2) only inside this coefficient, preserving the actual r outside. For any
M in the main interval, `r<=7/1000`, `d<=78/1000`, hence

```
theta<=252/3875<1,
||R_next||_(3/2) <= q_main r,
q_main=3060/3623<17/20.                                  (9)
```

On the narrow interval, `r<=7/100000`, `d<=654/100000`, giving

```
q_narrow=5949/96812<1/16.                                 (10)
```

These constants hold over each whole continuous interval: the coefficient is
increasing and the inherited uniform k cap and maximum M bound it everywhere.
No interpolation or sign symmetry of an unknown operator is needed; the actual
inputs for both signs are covered by `M=7|tau|`. If r=0, every B_Y vanishes in
the positive indexed norm, X=0 and R_next=0. No division occurs. At tau=0, or
in a volume with no retained original stars, AG2 already gives zero B and K;
the original onsite reference is retained. An empty volume is trivial.

For the passive comparison, every input support has |Y|>=4, so termwise
`(3/2)^|Y| <= (3/4)^4 2^|Y|`. Summing the same positive indexed family gives
the coefficient `81/256`. Exact comparisons show
`q_main>81/256` and `q_narrow<81/256`. The latter compares sufficient budgets
against the same actual r; no lower bound on the actual old lower-weight norm
has been proved. This does not promote the narrow result to same-weight
contraction either.

## 4. All scalar and diagonal updates

For each generated self-adjoint indexed term R_J of R_next, keep its full
connected support J, still of size at least four, and write

```
gamma_J=<Omega_J,R_J Omega_J>,
Bnext_J=P_J R_J Q_J+Q_J R_J P_J,
Znext_J=Q_J(R_J-gamma_J I)Q_J,
R_J=gamma_J I+Bnext_J+Znext_J.                             (11)
```

The norm costs are respectively1,1,2 times ||R_J||. Let `L=q k` be the
appropriate endpoint bound on `||R_next||_(3/2)` and b=3/2. Then

```
||Bnext||_b<=q r<=L, ||Znext||_b<=2L,
|sum gamma_J|/|Lambda|<=L/(4b^4)=4L/81,
|C+sum gamma_J|/|Lambda|<=k/64+4L/81.                      (12)
```

The scalar sums retain their declared supports and can be extensive. Their
sum is not claimed to be the full interacting ground energy. Centering in
(11) prevents double-counting gamma_J Q_J.

Since Znext_J annihilates the local vacuum, its quadratic form is bounded by
`2||R_J||Q_J`, and `Q_J<=sum_(x in J)(I-P_x)`. Minimum support size gives

```
|<psi,Znext psi>|<=(2b^-4 L)<psi,H0 psi>
                    =(32L/81)<psi,H0 psi>.
```

Thus the new reference `G2=H0+D_next+Znext` has domain D(H0) by finite-volume
bounded perturbation and obeys

```
G2>=(1-kappa2)H0,
kappa2=4M+k/8+32L/81.                                    (13)
```

It annihilates the product vacuum and has normalized reference-only gap at
least `1-kappa2`. Exact rational endpoint checks give a gap greater than
`124/125` on the main interval and `1999/2000` on the narrow interval. The
full corrected Hamiltonian is
`(C+sum gamma_J)I+G2+Bnext`; Bnext has not been discarded. The complete
diagonal norm may also be bounded by `d+2L` at b. All finite-volume bounds
are uniform in the retained complete-star cuboids.

The physical energy multiplier remains `delta=alpha/8`, with unchanged positive
spacing, E_star, alpha/E_star and hbar. Neither the support weight nor the
inverse gap is a fitted physical clock, coupling or action deformation.

## 5. Tests and scope

The standard-library checker computes the exact logarithm lower polynomial,
rational radii, both interval coefficients, scalar budgets and reference-only
gaps. It compares full matrix multiplication of the exponential products with
(7) through sixth degree, retaining the mixed coefficient dependence on B.
Local inverse/splitting tests retain scalar, centered complement and exterior
identity; overlapping-pair matrices reject removing cross and retained-D
commutators. Sign and zero cases are explicit. Separate exact support tests
exercise both root placements, nonempty overlap and unions larger than four.

An actual-input control keeps r variable below a fixed budget and verifies
that the coefficient bound multiplies r. A distinct admissible scalar example
rejects dividing two upper budgets. A family normalized at weight3/2 on growing
supports has weight-two norm `(4/3)^|J|`, rejecting conversion of this result
to same-weight contraction or a free weight reset. These are logical/finite
algebra controls, not assertions that the diagnostic interactions occur along
the actual SU(2) trajectory, not physical cutoff simulations and not observations.

The actual model proof is (1)-(13), using the source-bound AG2 premises. The
new scalar and diagonal class is controlled for one more step, but an iteration
requires a remaining positive weight schedule, complete retained-diagonal
estimates, new radius conditions and convergence in the required topology.
The earlier O2 obstruction for its own complete majorant is unchanged. The
previous9/4-to2 margin and this2-to3/2 margin are both spent. A bare inverse is
adequate for this single step precisely because its diagonal defect is retained.
It is not a proof that this unchanged inverse schedule converges indefinitely.

No full homogeneous gap, infinite global unitary, physical model matching,
four-dimensional continuum construction or Yang–Mills mass gap is claimed.
Scientific priority is unverified. No new external theorem constant was imported;
the advisor's shared proposed constant was derived under the frozen contract.

Reproduce into fresh absolute directories:

```
python3 -B research/round28/forward/ag3/check.py --output /absolute/new/ag3-forward
python3 -B -O research/round28/forward/ag3/check.py --output /absolute/new/ag3-forward-O
```

Every source/instruction snapshot and executed producer file is bound. The
normal and optimized deterministic outputs must agree byte-for-byte.
