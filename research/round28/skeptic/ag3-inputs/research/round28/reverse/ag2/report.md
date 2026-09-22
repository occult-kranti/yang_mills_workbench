# AG2 reverse: complete original remainder and its transport

The complete original remainder can be inventoried and transported uniformly on
the frozen interval `0<=M=7|tau|<=1/1000`. It includes a nonzero actual quadratic
vacuum coefficient in every fixed cuboid with a retained star. It is not a
fourth-order error. This report proves a positive form bound for the newly
extracted **reference diagonal alone**. It does not prove contraction of the
complete mixing source or a gap for the original Hamiltonian.

This is independent reverse production under `contracts/ag2.json`, with no
current forward production read. The pre-existing input snapshots were verified
and adopted before this production; `inputs/adoption-record.json` records their
unresolved creation provenance without assigning authorship. No existing input
bytes were changed. Shared inherited AG1 results are premises, not a second
independent derivation of AG1. Scientific priority is unverified.

## 1. Actual original model, operators and domain

Return to the homogeneous O1 complete-block model. Every coarse site is the
actual separable 24-link factor. Its possibly unbounded reference `h_x` is
nonnegative, has unique vacuum `Omega_x`, and satisfies `h_x>=I-P_x`. Retain
exactly complete stars `Z_b=b+{0,e1,e2,e3} subset Lambda` in finite cuboids in
the positive octant. All 21 omitted anchored faces are in `phi_b`, with
`||phi_b||<=M`. No finite spin cutoff replaces these operators. Physical
Hamiltonians multiply the dimensionless expressions by `delta=alpha/8`;
`a,E_star,alpha/E_star,hbar` remain fixed and positive. M is a dimensionless
coupling budget; rho and T below are proof parameters, not model deformations.

Define the original linear families

```
v_b=phi_b Omega_b, u_b=(H0,Z_b restricted to Q_b)^(-1)v_b,
L_b=|u_b><Omega_b|-|Omega_b><u_b|,
A1_b=|v_b><Omega_b|+|Omega_b><v_b|,
D_b=Q_b phi_b Q_b,
X=sum_b L_b, Phi=sum_b phi_b, A1=sum_b A1_b,
H0=sum_x h_x, D=sum_b D_b, G=H0+D.
```

Inherited actual Haar orthogonality gives `||v_b||^2=7tau^2/12=M^2/84`.
Consequently `||L_b||<=||v_b||` and `||A1_b||=||v_b||`. For exact rational
upper estimates set `s=a1=M/9`; these bound both norms because `1/84<1/81`.
They are not evaluations of the actual norms.

The identity `H0,Z_b u_b=v_b` implies bounded extensions
`H0,Z_b L_b=|v_b><Omega_b|` and
`L_b H0,Z_b=-|Omega_b><v_b|`. Local L_b preserves the local operator domain.
It commutes with the exterior spectral resolution and preserves that domain
as well; the joint spectral calculus for nonnegative local and exterior
Hamiltonians identifies the full domain as their intersection. Hence
`[X,H0]=-A1` on `D(H0)`. In a fixed cuboid X is bounded and skew-adjoint, and
this bounded commutator makes X bounded on the H0 graph space. Its exponential
and inverse preserve that space.

Integrating the bounded first commutator on this domain, then expanding only
bounded conjugations, proves

```
Hbar=exp(X)(H0+Phi)exp(-X)=G+R_O1,
R_O1=sum_(n>=1) [ad_X^n(Phi)/n! - ad_X^n(A1)/(n+1)!].        (1)
```

The series is norm convergent in each fixed cuboid. The interaction bounds below
also control its infinite ordered-word index set uniformly in volume. Finite
volume does not make that index set finite. No bounded extensive X or global
unitary in an infinite-volume representation is constructed.

## 2. Exact inventory and same-anchor compression

The selected cubic term is

```
C_b=(1/2)ad_(L_b)^2(phi_b)-(1/6)ad_(L_b)^2(A1_b),
w_b=Q_b C_b Omega_b=-<u_b,v_b>u_b-(||u_b||^2/3)v_b,
A3_b=|w_b><Omega_b|+|Omega_b><w_b|, A3=sum_b A3_b.
```

This is the S1 actual source, not its cubic upper estimate
`rbar=(4/3)a1^3`. For tau nonzero its actual homogeneous norm r is positive,
but this loop never divides by rbar as if rbar were r.

With `c_b=<Omega_b,C_b Omega_b>=<u_b,phi_b u_b>` and
`D3_b=Q_b(C_b-c_b I)Q_b`, exactly

```
C_b-A3_b=P_b C_b P_b+Q_b C_b Q_b=c_b I+D3_b.                (2)
```

Pinching by `P_b,Q_b` is contractive in operator norm: the result is a block
direct sum of two compressions. Thus
`||C_b-A3_b||<=||C_b||<=2s^2(M+a1/3)`. This avoids adding an artificial
extra A3 norm to the same-anchor inventory. Equation (2) has no omitted mixing
part. The scalar and centered diagonal are retained separately, with bounds
`|c_b|<=||C_b||` and `||D3_b||<=2||C_b||`; their separately summed budgets need
not equal the tighter pinched-operator budget.

The exact definition `E=R_O1-A3` has the disjoint indexed partition

| Part | Retained expression | Declared union |
|---|---|---|
| E2 | `[X,Phi]-(1/2)[X,A1]` | Two stars, at most seven factors |
| E3same | `sum_b(C_b-A3_b)` | Original four-factor stars |
| E3other | Every n=2 ordered word except `(b,b,b)` | At most ten factors |
| E4plus | Every n>=3 term of (1), with both factorials | At most `4+3n` factors |

All ordered anchors, repeated anchors, cross terms and roots are kept. A term
may cancel after a different grouping; none is removed on that assumption.

## 3. Complete rho-norm bounds

Use `||K||_rho=sup_x sum_(indexed Y contains x) rho^|Y| ||K_Y||`, with
`rho=9/4` and the indicated full union even when an operator admits a smaller
minimal support. Begin a word at a base star. At depth j a new star must meet
one of the j old stars. There are thirteen meeting relative displacements per
star, so there are at most `13j` choices. At order n this gives at most
`13^n n!` relative words, including repeats. Each union has at most `4+3n`
sites and at most that many translates containing a fixed root. Boundaries
delete complete stars only. Each commutator contributes `2s`.

Writing `z=26s rho^3`, the complete order-n budget is therefore

```
B_n=rho^4 (4+3n) z^n [M+a1/(n+1)], n>=1.                 (3)
```

This argument is all-order and includes incoming root placements. It is not an
inference from the finite enumeration in the checker. At order two the crude
relative count is `13^2*2!=338`, of which the one all-equal tuple is present.
Removing it leaves at most 337 relative tuples. Bounding each remaining union
by ten sites yields the valid, deliberately conservative factor `337/338`.
The exceptional tuple is instead counted on its true assigned four-site star,
with at most four root placements, using (2).

The four separate bounds are

```
e2       = rho^4 * 7z * (M+a1/2),
e3same   = 8rho^4 s^2 (M+a1/3),
e3other  = (337/338)rho^4 * 10z^2 * (M+a1/3),
e4plus   = rho^4 (M+a1/4) z^3(13-10z)/(1-z)^2,
e        = e2+e3same+e3other+e4plus.                         (4)
```

The last line uses `1/(n+1)<=1/4` for n>=3 and the exact positive-series
identity `sum_(n>=3)(4+3n)z^n=z^3(13-10z)/(1-z)^2`. It controls the complete
tail and every retained finite cuboid. The looser full-R-plus-A3 comparison is

```
e_triangle=rho^4(M+a1/2) z(7-4z)/(1-z)^2+4rho^4 rbar.     (5)
```

The direct inventory is no larger than (5): its n=1 term agrees, higher
coefficient envelopes improve, and its special cubic tuple is counted more
economically. The endpoint checks use exact fractions. Continuous coverage
follows from positive power series and increasing positive coupling monomials;
at M=1/1000, z<1. Both signs are covered by M, while zero is handled without
division. These upper budgets do not imply a lower bound on E or E/A3.

## 4. Actual AG1 correction and complete E transport

Use exactly the already admitted AG1 generator S: the odd compact triangular
filter of the actual A3 orbit under G, with T=3. Its residual R_A3 obeys
`[S,G]=-A3+R_A3`. The inherited graph-domain proof gives preservation of
`D(G)=D(H0)`. Its bounded first commutator can be integrated on that domain.
All the other terms here are bounded in each finite cuboid. Therefore

```
exp(S)Hbar exp(-S)=G+R_A3+N+exp(ad_S)E,
N=sum_(n>=1)ad_S^n(n A3+R_A3)/(n+1)!.                     (6)
```

The transformed E includes its n=0 term and all higher commutators. It is not
replaced by a declared free error.

For the inherited rooted AG1 estimate put

```
Abar_rho=4rho^4 rbar,
F_rho=(1-72rho^3 M)^(-3), F_2=(1-576M)^(-3),
theta=18 Abar_rho F_rho.
```

The actual bounds `||S||_rho,||R_A3||_rho<=Abar_rho F_rho` follow from the
admitted rooted recurrence; this imported refinement is attributed to the
Round27 forward producer and its post-freeze reviewers. At M=1/1000 the
filter radius is `72rho^3 M=6561/8000<1` and theta<1.

For arbitrary rho-summable E, split `d=log(rho/2)` equally over n commutators.
The support-weight estimate is `||[U,V]||_b<=2/(e log(a/b))||U||_a||V||_a`.
Using `n!>=(n/e)^n` and `log(9/8)>=1/9` gives

```
||ad_S^n E||_2/n! <=theta^n ||E||_rho,
||exp(ad_S)E||_2 <= e/(1-theta),
||N||_2 <= nbar=theta/(1-theta)*Abar_rho*(1+F_rho/2).      (7)
```

Every term pays its own rho-to-2 loss. This is one conjugation estimate; it
does not grant a fresh rho-to-2 margin for the next correction.

For the selected residual alone use

```
rsel=64 rbar F_2                            (main interval),
rsel=64 rbar[4/9+F_2-1]                    (M<=1/10000).
W=rsel+nbar+e/(1-theta).                                  (8)
```

The narrower line uses the admitted source-specific free-filter bound and full
positive interaction tail. It is a sufficient upper estimate; no evaluation
of the actual source norm is made. The complete output K in (6) satisfies
`||K||_2<=W`. Exact output contains every component of (4)-(8). Conservative
rational consequences are

| Interval | Complete output W | New reference-only dimensionless gap lower bound |
|---|---|---|
| `0<=M<=1/1000` | `<7/1000` | `>995/1000` |
| `0<=M<=1/10000` | `<7/100000` | Positive, from `1-4M-W/8` |

The exact budgets, not rounded decimal comparisons, support these statements.
The discontinuous choice of the narrower residual estimate affects only the
chosen upper bound, not the Hamiltonian or its actual dynamics.

## 5. Full generated split and a reference-only consequence

For every self-adjoint indexed K_Y in the complete K, define

```
P_Y=|Omega_Y><Omega_Y|, Q_Y=I-P_Y,
c_Y=<Omega_Y,K_Y Omega_Y>,
Anew_Y=P_Y K_Y Q_Y+Q_Y K_Y P_Y,
Dnew_Y=Q_Y(K_Y-c_Y I)Q_Y.
K_Y=c_Y I+Anew_Y+Dnew_Y.                                  (9)
```

Every full assigned support Y is retained, including for the scalar. The
weighted costs are at most W, W and 2W respectively; summing separate budgets
costs at most 4W. The first is an intensive scalar bound, not a bound on a
volume-independent extensive scalar operator. All declared Y have at least
four factors. Hence the unweighted scalar incidence density is at most W/16,
and `|sum_Y c_Y|/|Lambda|<=W/64`; the extra factor four follows by counting
each indexed support once instead of once per site.

Each Dnew_Y annihilates its local vacuum and obeys

```
|<psi,Dnew_Y psi>|<=||Dnew_Y|| <psi,Q_Y psi>,
Q_Y<=sum_(x in Y)(I-P_x).
```

Thus `|<psi,sum_Y Dnew_Y psi>|<=(W/8)<psi,H0 psi>`, since
`sup_x sum_(Y contains x)||Dnew_Y||<=2W/16`. The inherited original D has
relative bound 4M. The updated reference

```
Gnew=H0+D+sum_Y Dnew_Y
```

is self-adjoint on D(H0) in every finite cuboid: the full bounded interaction
series sums in norm there. Its form obeys

```
Gnew >= (1-4M-W/8) H0.                                   (10)
```

It annihilates the product vacuum, and for a nonempty site cuboid H0 has gap
at least one off that unique vacuum. Equation (10) proves the indicated
reference-only gap, or delta times it in physical units. A scalar added to
Gnew shifts this reference spectrum without changing its gap. Cuboids with
no retained star have E=S=K=0 and keep the original onsite reference.

The full corrected Hamiltonian is `Gnew+sum_Y c_Y I+sum_Y Anew_Y`. The
last sum has not been eliminated, so (10) is not its gap estimate. Moreover,
the new diagonal has generated supports, not just four-site stars. Positivity
of this reference is only one needed hypothesis for a further homological
step; its locality, inverse, source and remaining weight conditions still need
proof.

## 6. Actual quadratic obstruction and controls

Fix a finite cuboid with N>=1 retained stars. Inherited O1 Haar orthogonality
across all omitted faces gives `V1=Phi Omega/tau`, `||V1||^2=7N/12>0`.
Set `U1=sum_b u_b/tau`; then `H0 U1=V1` and
`a_Lambda=<U1,H0 U1>>0`. Both commutators in E2 have vacuum expectation
`-2tau^2 a_Lambda`. Therefore

```
<Omega,E Omega>=-tau^2 a_Lambda+O_Lambda(|tau|^3),          (11)
```

because A3 has zero vacuum mean. Analyticity follows from the bounded
finite-volume series. This actual model statement excludes `E=O(tau^4)` in
fixed-volume operator norm. It proves neither an actual nonzero quadratic
mixing matrix element in this model nor a volume-independent lower coefficient.
It also does not prove failure of a full correction or of a physical gap.

The executable has no third-party imports. Exact rational diagnostics include
a three-level rank-source fixture, a separate overlapping-pair fixture, and
an independent product-of-exponentials expansion through degree six. They
reject wrong n=1/n=2 coefficients, omitted ordered cross terms, scalar double
counting and omission of E or its transport commutator. Both coupling signs,
zero, empty-star, one-star and bulk boundary families are checked. Actual
four-site geometry is independently enumerated through depth three, including
repeats, all thirteen displacements and all four root incidences. These finite
examples check algebra and bookkeeping; (1)-(11) and their all-order estimates
supply the actual Hilbert-space argument.

A domain countercontrol uses `H e_j=j e_j` and `v_j=1/j`: v belongs to l2 but
not D(H). A bounded rank generator made from v need not preserve D(H), since
it sends a vacuum vector to v. The checker confirms bounded partial vector
norms and divergent graph components. Thus boundedness of S alone cannot
license differentiation of an unbounded conjugation; the actual bounded
commutator and graph-domain proofs above are required. Finite matrix
differentiability alone supplies no such full-space conclusion.

Reproduce with

```
python3 -B research/round28/reverse/ag2/check.py --output /absolute/fresh/ag2-reverse
python3 -B -O research/round28/reverse/ag2/check.py --output /absolute/fresh/ag2-reverse-opt
```

Each run verifies all bound source and instruction bytes, writes deterministic
results and refuses an existing or relative output directory. The normal and
optimized results must agree byte-for-byte. No AG3 or later investigation is
executed here. The next decision should address the actual generated source
relative to Gnew with its complete support class and already spent weights.
The known local Lie-Schwinger and SW literature motivates this requirement;
no unmatched external theorem threshold or continuum claim is imported.
