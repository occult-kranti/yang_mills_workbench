# AG2 independent derivation before producer exchange

This derivation and `ag2_independent.py` were written without reading either current AG2 producer. It uses the frozen contract and inherited O1, S1 and AG1 results. The matrices below are independent algebra controls; the actual infinite-dimensional statement follows from the domain, support and norm arguments. All numbers are sufficient upper bounds in the fixed dimensionless energy unit; multiply energies by the unchanged `delta=alpha/8`.

## Exact original partition

Use `X,A1` for the original linear rotation/source and `S,A3` for the later filtered cubic correction. Since `[X,H0]=-A1` is bounded on the preserved graph domain, integration gives

```
exp(X)(H0+Phi)exp(-X)=G+R_O1,
R_O1=sum_(n>=1) [ad_X^n(Phi)/n!-ad_X^n(A1)/(n+1)!],
G=H0+sum_b Q_b phi_b Q_b.
```

Only bounded operators are expanded after the first commutator. The exact `E=R_O1-A3` consists of all quadratic `n=1` words, all other `n=2` words, the compressed same-anchor cubic words and the `n>=3` tail. For each same-anchor word `C_b`, `A3_b=P_b C_b Q_b+Q_b C_b P_b`, so

```
C_b-A3_b=P_b C_b P_b+Q_b C_b Q_b.
```

This is a block-diagonal compression of a self-adjoint operator, hence its norm is at most `||C_b||`. The split into a scalar and a centered complement is still `c_b I+Q_b(C_b-c_b I)Q_b`; it contains no remaining same-anchor mixing. This fact improves its bound without deleting the scalar or identifying the same-anchor word with the complete cubic coefficient.

The original actual-model fixed-volume vacuum coefficient is negative and quadratic at each nonempty volume. Removing the cubic mixing family does not change it. Thus assigning fourth order to the full `E` is invalid. This does not identify every quadratic mixing matrix element, or prove the failure of a centered correction.

## Independent complete support estimate

Let `rho=9/4`, `s=4M/35`, `z=26*s*rho^3` and `r_bd=M^3/567`. These are upper bounds, never actual evaluated source norms. They follow from the inherited `||X_b||,||A1_b||<=sqrt(7/12)|tau|`, `M=7|tau|`, and `r_actual<=(4/3)(M/sqrt(84))^3`.

Fix the base star at the origin. A connected prefix with `j` stars has at most `13j` candidate next anchors because one star has thirteen intersecting translates. Repeated anchors remain; the next star need only meet the generated union. There are at most `13^n n!` relative ordered words at depth `n`, each with support size at most `4+3n`. Translating a fixed word places a given root in its union in exactly its support cardinality many ways on the full integer lattice. Retained positive-octant cuboids only delete translations. Therefore a seed with norm bound `B` has depth-`n` rooted sum at most

```
rho^4 (4+3n) z^n n! B.
```

This is an all-order combinatorial proof. The independent finite enumeration returns relative counts `13,253,6421` at depths one through three and checks the formula, repeated words, a chain missing the seed at its outer end, and empty/one-star/interior boundaries. The enumeration is not the all-order proof.

At depth two there are at most `338` candidate relative words, one of which has all anchors equal. Thus at most `337` are other words. Keeping the crude support-ten/root-ten bound for those words, and the actual support-four/root-four for the compressed word, gives the following disjoint inventory:

```
e2 = rho^4 * 7*z*(M+s/2),
e3_other = 6740*rho^10*s^2*(M+s/3),
e3_same = 8*rho^4*s^2*(M+s/3),
e4plus = rho^4*(M+s/4)*z^3*(13-10*z)/(1-z)^2,
e = e2+e3_other+e3_same+e4plus.
```

The same-anchor estimate uses `||C_b||<=2s^2(M+s/3)` and compression, with no additional charge for `A3_b`. For the tail, `1/(n+1)<=1/4` at `n>=3`; the exact positive series is

```
sum_(n>=3)(4+3n)z^n = z^3*(13-10*z)/(1-z)^2.
```

For comparison, the looser triangle estimate is

```
e_loose = rho^4*(M+s/2)*z*(7-4*z)/(1-z)^2 + 4*rho^4*r_bd.
```

The direct inventory is no larger: its `n=1` bound is the same; at `n=2`, `6740*rho^10+8*rho^4<=6760*rho^10`; at higher orders its seed coefficient is smaller. It consequently beats even the corresponding full-`R_O1` positive majorant before the extra `A3` triangle charge. This compares sufficient bounds; it is not cancellation between unknown operator norms.

## Transport and complete output classes

Use the actual admitted AG1 generator. With

```
F_rho=(1-72*rho^3*M)^(-3), F2=(1-576*M)^(-3),
theta=72*rho^4*r_bd*F_rho,
```

the inherited `rho`-norm generator estimate and `log(9/8)>=1/9` give the complete transport bound `||exp(ad_S)E||_2<=e/(1-theta)`. The graph-domain argument is the same finite-volume one used by AG1; no arbitrary bounded local operator is asserted to regularize the exterior. The exact composite identity is

```
exp(S)exp(X)(H0+Phi)exp(-X)exp(-S)
 = G+R_A3+N_A3+exp(ad_S)E.
```

The selected residual has bound `64*r_bd*F2`, and its full nonlinear term has bound

```
n_bd=theta/(1-theta)*4*rho^4*r_bd*(1+F_rho/2).
```

Thus the complete new interaction `K` has original-weight norm at most

```
k=64*r_bd*F2+n_bd+e/(1-theta).
```

Every generated indexed self-adjoint term retains a connected assigned support of at least four complete blocks. This is true of the initial words, their onsite evolution, added overlapping stars and further overlapping commutators. Its exact decomposition is

```
K_Y=c_Y I+B_Y+Z_Y,
B_Y=P_Y K_Y Q_Y+Q_Y K_Y P_Y,
Z_Y=Q_Y(K_Y-c_Y I)Q_Y.
```

The costs are `|c_Y|<=||K_Y||`, `||B_Y||<=||K_Y||`, `||Z_Y||<=2||K_Y||`. Therefore the scalar root density is at most `k/16`, the mixing weight-two norm at most `k`, and the centered-diagonal weight-two norm at most `2k`. The scalar energy density also obeys the stated scalar bound, although the total scalar is extensive and is not known to be the full interacting ground energy.

There is a separate useful **reference-only** estimate. Since `Z_Y=Q_Y Z_Y Q_Y` and `Q_Y<=sum_(x in Y)(I-P_x)`, the centered new diagonal obeys the relative form bound

```
|sum_Y <psi,Z_Y psi>| <= (k/8) <psi,H0 psi>.
```

Here `sum_(Y contains x)||Z_Y||<=2*2^(-4)*k=k/8` uses the retained minimum support size. The original `D` costs `4M`. Consequently `G_next=H0+D+sum Z_Y` has domain `D(H0)` in each finite volume, product vacuum, and gap at least `1-4M-k/8`. This is a statement about this centered reference alone. The full corrected operator is `G_next+C I+sum B_Y`, and its remaining mixing cannot be discarded. The bound supplies neither a new filtered orbit estimate nor a reusable support-weight margin.

## Exact interval certificates and limits

| Endpoint | Direct `E` input budget | Transported `E` budget | Complete `k` | Reference-only gap lower bound |
|---|---:|---:|---:|---:|
| `M=1/10000` | `0.0000644962938448` | `0.0000644962938451` | `0.0000644962939799` | `0.999591937963` |
| `M=1/1000` | `0.00673685728095` | `0.00673686104820` | `0.00673686252903` | `0.995157892183` |

Displayed decimals describe exact rational certificates in the JSON; they are not independent measurements or rounding premises. The majorants are sums/products of nonnegative series with positive coefficients below their poles, and increase with `M`. The endpoint tests therefore cover the entire continuous intervals, including both coupling signs. `z<1`, `72*rho^3*M<1`, `theta<1`, and the reference-only gap exceeds `99/100` throughout the main interval. At zero coupling or with no retained stars the actual update is zero, before any division.

The quadratic inventory upper bound is much larger than the cubic input upper budget at both positive audit endpoints. This fact cannot be used as an actual lower ratio or proof that the physical correction fails. It instead prevents these bounds from certifying full mixing contraction. The complete `E` premise is now explicit; the next problem is the actual full mixing source and changed-reference estimate on generated supports, with a remaining weight schedule. No homogeneous numerical gap for the original Hamiltonian, infinite global unitary, physical matching or four-dimensional continuum construction follows.

## Executed independent controls

The normal and optimized runs pass **97 exact checks** with identical JSON bytes. Controls include independent exponential-product coefficients through fourth degree, the cubic source formula, both signs, scalar reconstruction, dropped cross quadratic/cubic words, all ordered support geometry, zero/empty cases, exact positive tails, explicit `E` transport coefficients, and an exterior sequence whose Hilbert norm stays bounded while its energy graph norm grows. The domain sequence diagnoses why identity extension preserves a suitable domain without regularizing arbitrary exterior vectors. The elementary family `epsilon*sin(t/epsilon^2)` also rejects differentiating a uniform value-error bound into a derivative bound: its amplitude is `epsilon` and its derivative at zero is `1/epsilon`. The three-level and eight-dimensional matrices are deliberately separate from the actual SU(2) model and do not replace the inherited actual Haar/source proof.
