# AG3 independent derivation before producer exchange

The frozen advisor proposal is supported: one bare-reference correction of the actual complete AG2 mixing family has output at weight `3/2` bounded by `3060/3623` times its actual input norm at weight two on the main interval. The narrow audit factor is `5949/96812`. This derivation and checker were produced without reading either current AG3 producer. The inequality, overlap refinement and proposed main target were shared advisor-origin contract context; the following reconstruction and executed controls are independent validation, not claims of independent discovery.

## Actual entry family and domain

The admitted complete transformed homogeneous Hamiltonian is

```
H_entry=C I+H0+D_next+B,
B_Y=P_Y K_Y Q_Y+Q_Y K_Y P_Y,
Z_Y=Q_Y(K_Y-c_Y I)Q_Y,
D_next=D+sum_Y Z_Y,  C=sum_Y c_Y.
```

The AG2 indexed decomposition is kept exactly. Every assigned support is a finite connected union of at least four complete blocks, including when an operator simplifies on that support. All original terms now enter this family, rather than only the earlier selected cubic source. Write the actual chosen indexed interaction norm as `r=||B||_2` and the actual diagonal norm as `d=||D_next||_2`. AG2 supplies upper certificates `r<=K`, `d<=64M+2K`, with `K=7/1000` on the main interval and `K=7/100000` on the narrow interval. These constants are not actual norm evaluations. The original scales and physical energy unit `delta=alpha/8` stay fixed.

For each local mixing term, `v_Y=B_Y Omega_Y` is orthogonal to the local vacuum and `B_Y=|v_Y><Omega_Y|+adjoint`. The unchanged bare reference satisfies `H0,Y|Q_Y>=1`. Consequently

```
u_Y=(H0,Y|Q_Y)^(-1)v_Y,
X_Y=|u_Y><Omega_Y|-|Omega_Y><u_Y|,
||X_Y||=||u_Y||<=||v_Y||=||B_Y||,
[X_Y,H0,Y]=-B_Y.
```

Here `u_Y` lies in the actual local operator domain. Both local products with `H0,Y` have bounded extensions. Identity extension commutes with the exterior spectral projections; joint nonnegative spectral calculus identifies `D(H0)` with the intersection of the local and exterior domains. Thus the extension preserves `D(H0)` and has the same bounded commutator there. It does not regularize an arbitrary exterior vector.

The finite cuboid still has infinitely many indexed words. Absolute convergence is supplied by the input norm: because `|Y|>=4`,

```
sum_Y ||B_Y|| <= |Lambda| r/64,
sum_Y ||X_Y|| <= |Lambda| r/64.
```

The first inequality follows by counting each support over its sites and using `|Y|2^|Y|>=64`. The bounded-commutator estimates similarly sum on the graph space. Hence `X=sum_Y X_Y` is bounded and skew-adjoint in finite volume, preserves the graph domain, and satisfies `[X,H0]=-B`. Its graph-space exponential and inverse preserve `D(H0)`. No bounded infinite-volume extensive generator is constructed. This uses a bare inverse and does not assert an all-sector commutator inverse for the changed reference `H0+D_next`.

## All-support commutator estimate below weight two

For arbitrary indexed interactions with complete supports define

```
||U||_a=sup_x sum_(Y contains x) a^|Y| ||U_Y||.
```

Let `a>b>=3/2` and `L=log(a/b)>0`. Define the commutator by every ordered intersecting pair and its full union. Nonempty overlap gives

```
b^|Y union Z| <= b^|Y| b^|Z|/b.
```

The operator commutator costs two. Split the root between `x in Y` and `x in Z`; including both may overcount a root in their intersection and is safe. For the first assignment, sum the `Z` family over its possible intersection sites in `Y`, costing `|Y|`. The resulting cardinality is absorbed by

```
|Y| (b/a)^|Y| <= sup_(t>=0) t exp(-Lt)=1/(e L).
```

The first assignment therefore costs `2/(b e L)||U||_a||V||_a`, and the other assignment has the same bound. This proves, without using an inherited lemma outside its range,

```
||[U,V]||_b <= 4/[b e log(a/b)] ||U||_a||V||_a.
```

It applies to arbitrary generated support sizes, repeated indices and every incoming overlap. A nonzero commutator's union stays connected and has at least four assigned blocks. No finite support cutoff is introduced.

For `n` nested commutators allocate the total `L0=log(4/3)` equally between weights two and `3/2`. Every intermediate output weight is at least `3/2`, and every intermediate generator norm is at most `r`. Thus

```
||ad_X^n V||_(3/2)/n!
 <= [(8n)/(3eL0)]^n r^n ||V||_2/n!
 <= [8r/(3L0)]^n ||V||_2.
```

The last inequality uses `n!>=(n/e)^n`, obtained by integrating `log` on `[1,n]`. All nested orders are covered. The elementary identity

```
1/(1+t) - (1-t+t^2-t^3) = t^4/(1+t) >= 0
```

integrated from zero to `1/3` proves `log(4/3)>=31/108`. Therefore the rational constant `c=288/31` is a valid upper bound for `8/(3L0)`. The prior `9/4 -> 2` loss remains spent; this step spends the additional `2 -> 3/2` loss.

## Full operator identity and actual-norm multiplier

Integrating the bounded first commutator on `D(H0)` gives

```
exp(X)H0 exp(-X)=H0-integral_0^1 exp(t ad_X)B dt.
```

Expand the bounded integrand and the bounded `D_next+B` conjugation. The scalar commutes and is retained. Combining coefficients gives the exact identity

```
exp(X)H_entry exp(-X)=C I+H0+D_next+R_next,
R_next=sum_(n>=1) ad_X^n[D_next/n!+n B/(n+1)!].
```

In particular `[X,D_next]` is present at first order. The inverse did not remove it. The leading source contribution is `[X,B]/2`, and every later factorial is retained. Arbitrary ordered overlapping supports are present through all orders.

If `cr<1`, the complete positive majorant gives

```
||R_next||_(3/2)
 <= sum_(n>=1)(cr)^n[d+n r/(n+1)]
 <= r * c(d+r)/(1-cr).
```

The final multiplier is the actual `r=||B||_2` of the declared indexed family. The coefficient is increasing in each of `d` and `r` below its pole. Only inside that coefficient substitute the AG2 ceilings:

```
gamma(M,K)=c(64M+3K)/(1-cK),
||R_next||_(3/2) <= gamma(M,K) ||B||_2.
```

At the main endpoint, `cK=252/3875<1` and `gamma=3060/3623<17/20`. At the narrow endpoint `gamma=5949/96812<1/16`. With the fixed respective interval ceiling `K`, the coefficient increases with `M`, so these endpoint inequalities hold continuously on the entire frozen intervals. Both signs are covered by `M=7|tau|`; no pure parity of the full resummed `B(tau)` is assumed. If `r=0`, each term of the nonempty-support norm vanishes, hence `X=0` and `R_next=0` even with nonzero `D_next`, before any ratio. Zero coupling and no-retained-star volumes give this case directly.

This is a reduction between different support norms, not contraction in a single fixed norm. It cannot be relabeled as an unchanged-weight estimate or an all-stage induction. The bound concerns the actual declared interaction norm and is not a measured global operator-norm ratio.

## Scalar and reference-diagonal update

Split every self-adjoint generated residual term on its full assigned support:

```
R_Y=c'_Y I+B'_Y+Z'_Y,
B'_Y=P_Y R_Y Q_Y+Q_Y R_Y P_Y,
Z'_Y=Q_Y(R_Y-c'_Y I)Q_Y.
```

The individual costs are `|c'_Y|<=||R_Y||`, `||B'_Y||<=||R_Y||`, `||Z'_Y||<=2||R_Y||`. The old scalar is still present and the new reference is `H0+D_next+sum Z'_Y`. For `W=gamma(M,K)K` and `b=3/2`, complete support counting gives

```
||B'||_b <= gamma ||B||_2 <= W,
||D_next+Z'||_b <= 64M+2K+2W,
|C+sum c'_Y|/|Lambda| <= K/64 + 4W/81,
|<psi,sum Z'_Y psi>| <= (32W/81)<psi,H0 psi>.
```

The scalar factor is `1/(4b^4)=4/81`, from counting each support over its at least four sites. The relative factor is `2/b^4=32/81`; each centered term annihilates its local vacuum and `Q_Y<=sum_(x in Y)(I-P_x)`. All incoming root incidences are counted in the norm. Old AG2 diagonal relative cost is at most `4M+K/8`. The new centered reference therefore has gap at least

```
g_ref=1-4M-K/8-32W/81.
```

Its finite-volume domain is `D(H0)` because the diagonal interaction sums absolutely to a bounded perturbation there. It annihilates the product vacuum and its lower form bound is `g_ref H0`, proving reference-only positivity. The full transformed Hamiltonian still contains `B'`; the reference gap is not its gap. The scalar is an explicit reference energy shift, not the known full interacting ground energy.

| Endpoint | Factor multiplying actual `||B||_2` | Full residual upper ceiling `W` | Total scalar energy-density ceiling | Centered-reference-only gap lower bound |
|---|---:|---:|---:|---:|
| Main `M=1/1000` | `3060/3623 < .85` | about `.005912227436` | about `.000401336849` | about `.992789305211` |
| Narrow `M=1/10000` | `5949/96812 < 1/16` | about `.000004301430` | about `.000001306167` | about `.999589550670` |

The exact fractions in the output are the certificates; these decimals are descriptions. In particular the new reference gap is greater than `.99` throughout the main interval. No homogeneous gap for the complete original Hamiltonian, infinite global unitary, physical model/scale matching, or continuum Yang–Mills construction follows.

## Independent controls and remaining limits

The standard-library checker passes **152 exact checks**, with identical normal and optimized output. It verifies its 22 input-source snapshots, independently multiplies exponential series through degree six, keeps the retained diagonal term, checks both diagnostic signs and zero source with nonzero diagonal, rejects wrong source factorials and missing old/new scalars, and reconstructs the centered complement. A nonvacuum exterior vector separates identity extension from a global-vacuum projector; a separate overlapping operator has a nonzero retained diagonal commutator.

Support controls retain both exclusive root placements, nonempty-overlap weight gain, a growing chain whose outer support misses the seed, repeated words, and the minimum assigned support costs. The exact geometric tail is checked with a remainder. Rational actual-input examples reject division by an upper input budget. The exterior sequence `1/j` has bounded Hilbert norm and unbounded energy graph norm, diagnosing the domain shortcut. These finite checks corroborate the written all-order/domain arguments; they do not discretize the physical SU(2) Hilbert space or prove the infinite statements by sampling.

A generic fixed-weight countercontrol uses `X=sum_i J_i` on `m` qubits and `D_Y=a^(-m)(product_i Z_i-I)/2`. The vacuum-annihilating diagonal has norm one at weight `a`, the onsite generator family has norm `a`, and the commutator has norm `m` at the same weight. Thus a generic same-weight bilinear bound cannot have a universal constant. This does not prove that every specially structured homological pair needs the same loss. Separately, a single assigned support with norm `b^(-m)` has lower-weight norm one but weight-two norm `(2/b)^m`; this rejects restoring the spent weight without a new hypothesis. Neither control proves actual algorithm divergence or excludes a sharper future treatment of the retained diagonal. O2's earlier failed all-stage positive majorant remains an inherited limitation.

The shared proposal is now independently substantiated within this frozen single-step scope. Scientific priority remains unverified. Current producer reports are still unread at this independent freeze.
