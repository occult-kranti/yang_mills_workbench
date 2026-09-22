# AG3 reverse: a full-source correction with a spent weight margin

For the complete actual AG2 local mixing family, this one bare-reference
correction satisfies

```
||R_next||_(3/2) <= (3060/3623) ||B||_2 < (17/20)||B||_2
```

when `0<M<=1/1000` and `||B||_2>0`. Zero source gives zero correction directly.
The coefficient bound holds throughout the continuous interval, including
both signs of tau. It compares **different support weights**. It is not
same-weight contraction, an all-stage iteration, or a gap theorem for the
original Hamiltonian. The narrower frozen interval gives a coefficient below
1/16. All scalar and diagonal terms remain explicit.

The contract shares Newton's bare-inverse proposal and the advisor's prospective
overlap/logarithm refinement, with pre-contract feedback. These are attributed
shared premises for a proposed target, not independently invented discoveries.
The proof and checker here were produced without reading current forward AG3.
All 25 source/contract/instruction snapshots were created and verified before
production. No pre-existing AG3 directory or scientific artifact was present.

## 1. Reconstruct the actual full input

AG2 admits the exact transformed homogeneous complete24-link operator

```
H_in=C I+H0+D_next+B,
H0=sum_x h_x, D_next=D+Z,
c_Y=<Omega_Y,K_Y Omega_Y>,
B_Y=P_Y K_Y Q_Y+Q_Y K_Y P_Y,
Z_Y=Q_Y(K_Y-c_Y I)Q_Y,
C=sum_Y c_Y, B=sum_Y B_Y, Z=sum_Y Z_Y.
```

Here K contains every original O1 remainder and its actual AG1 transport. Each
indexed Y is the complete assigned connected union of at least four coarse
blocks, with repetitions retained. The family is not replaced by four-site
sources or the selected cubic A3. C is the sum of reference expectations, not
the exact full interacting ground energy.

For any indexed interaction U put
`||U||_a=sup_x sum_(Y contains x) a^|Y| ||U_Y||`. Keep this very same B family
when defining the actual denominator `r=||B||_2`. AG2 gives

```
r<=Kcap, d:=||D_next||_2<=64M+2Kcap,
|<psi,D_next psi>|<=(4M+Kcap/8)<psi,H0 psi>,
|C|/|Lambda|<=Kcap/64,
Kcap=7/1000       on 0<=M<=1/1000,
Kcap=7/100000     on 0<=M<=1/10000.
```

Non-strict caps are used safely although the admitted positive-coupling
certificates are strict. For tau=0 the actual interactions and C vanish.
If no complete original star is retained, all original interactions and
generated corrections vanish even at nonzero tau. These facts are handled
directly, not inferred from a nonzero upper cap.

The onsite factors are the actual separable link Hilbert spaces, with possibly
unbounded `h_x>=I-P_x` and a unique zero vacuum. All assertions below are first
on each finite cuboid. Dimensionless Hamiltonians multiply the unchanged
positive physical unit `delta=alpha/8`; spacing, E_star, alpha/E_star and hbar
stay fixed. Support weights are proof bookkeeping, not physical couplings.

## 2. Local inverse, exterior identity and the whole graph domain

Set `v_Y=B_Y Omega_Y`. The exact local mixing form is
`B_Y=|v_Y><Omega_Y|+|Omega_Y><v_Y|`, with v_Y orthogonal to Omega_Y and
`||B_Y||=||v_Y||`. The finite-support reference has
`H0,Y|Q_Y>=1`. By spectral calculus,

```
u_Y=(H0,Y|Q_Y)^(-1)v_Y belongs to D(H0,Y),
H0,Y u_Y=v_Y, ||u_Y||<=||v_Y||,
X_Y=|u_Y><Omega_Y|-|Omega_Y><u_Y|,
||X_Y||=||u_Y||<=||B_Y||.
```

Thus `||X||_2<=r`, with the original support Y assigned to X_Y. On the local
domain `H0,Y X_Y=|v_Y><Omega_Y|` and
`X_Y H0,Y=-|Omega_Y><v_Y|`, with bounded extensions. Tensor by the exterior
identity. X_Y strongly commutes with the exterior energy projections and
preserves its domain. Joint spectral calculus for nonnegative commuting
local/exterior energies gives `D(H0)=D(H0,Y) intersect D(H0,ext)`. Therefore

```
[X_Y,H0]=-B_Y on D(H0).
```

The identity extension preserves this domain; it does not turn every exterior
Hilbert vector into a domain vector. It also differs from a source formed
with the global vacuum projector, as the excited-exterior control demonstrates.

Although a finite cuboid has infinitely many indexed generated terms, their
norm sums converge absolutely: for example
`sum_Y||B_Y||<=|Lambda|r/64`, since |Y|>=4 and the input weight is two.
The same estimate holds for X. For finite partial sums the commutator is the
corresponding negative partial B. Taking norm limits in X and B and using
closedness of H0 shows `X D(H0) subset D(H0)` and `[X,H0]=-B`. Explicitly,
`H0 X_j psi=X_j H0 psi+B_j psi` converges for every domain vector.
The graph-norm bound `||H0 X psi||<=||X||||H0 psi||+||B||||psi||` then makes
the exponential series converge on the graph space. Both exp(X) and exp(-X)
preserve D(H0). X is bounded skew-adjoint in each fixed volume.

This inverse uses only H0. It is not a commutator inverse for D_next or the
changed reference, and no all-sector spectral inverse is assumed. No bounded
global extensive X or infinite-volume unitary is constructed.

## 3. Complete transformed identity

Integrate the bounded first commutator on D(H0):

```
exp(X)H0 exp(-X)=H0-int_0^1 exp(t ad_X)B dt.
```

Expand only the bounded conjugations of B and D_next. The zero-order B
cancels, while C commutes unchanged. Exactly

```
exp(X)H_in exp(-X)=C I+H0+D_next+R_next,
R_next=sum_(n>=1) ad_X^n[D_next/n!+n B/(n+1)!].             (1)
```

The first remainder is `[X,D_next]+[X,B]/2`. The retained diagonal is
essential. All higher coefficients and ordered histories remain. A history
can contribute only when its incoming support meets the accumulated union;
its full union, including repetitions and all previous factors, stays assigned.
Infinite norm convergence in fixed volume follows from bounded operators;
the following argument supplies the volume-independent weighted summability.

## 4. Prove the commutator constant below weight two

For arbitrary indexed U,V and `a>b>=3/2`, any nonzero term has intersecting
supports Y,Z. Consequently

```
b^|Y union Z| <= b^-1 b^|Y| b^|Z|.
```

The norm of a commutator costs factor two. Split the root between Y and Z,
allowing harmless double counting when it lies in both. For a root in Y, sum
the Z incidence over all sites of Y; the contribution is at most

```
(2/b) sup_x sum_(Y contains x) |Y| b^|Y| ||U_Y|| * ||V||_b.
```

The other root placement is the same expression with U and V exchanged.
Let `ell=log(a/b)`. Since `m exp(-ell m)<=1/(e ell)` for m>=0, both together
give the new, proved-range estimate

```
||[U,V]||_b <= 4/[b e log(a/b)] ||U||_a ||V||_a.            (2)
```

No finite maximum support size, star-only hypothesis, or omitted incoming root
is used. Absolute positive sums allow this proof first for finite index sets
and then by monotone bounds and norm convergence for the full families.

For an n-fold commutator allocate `ell0=log(4/3)` equally between intermediate
weights `a_j=2 exp(-j ell0/n)`, j=0,...,n. Every output is at least 3/2 and
every X norm at an intermediate input is at most r. Iterating (2) gives

```
||ad_X^n U||_(3/2) <= [8n/(3e ell0)]^n r^n ||U||_2.
```

The elementary factorial inequality `n!>=(n/e)^n` yields

```
||ad_X^n U||_(3/2)/n! <= (c r)^n ||U||_2,
c= (8/3)/log(4/3) <= cbar:=288/31.                         (3)
```

The rational logarithm bound is not a decimal approximation: on 0<=t<=1/3,
`1/(1+t)-(1-t+t^2-t^3)=t^4/(1+t)>=0`. Integration gives
`log(4/3)>=1/3-1/18+1/81-1/324=31/108`.

Each nested order spends the entire prescribed 2-to-3/2 loss across its
own brackets. This does not reuse the earlier 9/4-to-2 loss and does not create
another unused margin for the next iteration.

## 5. Keep the actual denominator through the infinite tail

The factor `n/(n+1)` in the B part of (1), after extracting n!, is at most one.
For `cbar r<1`, (3) therefore proves the complete infinite sum

```
||R_next||_(3/2) <= (d+r) sum_(n>=1)(cbar r)^n
                  = r*cbar(d+r)/(1-cbar r).                (4)
```

The final r in (4) is the **actual indexed input norm**, never its cap. Only
the coefficient may use the positive monotonicities in r and d. With
`dcap=64Mmax+2Kcap`, define

```
gamma=cbar(dcap+Kcap)/(1-cbar Kcap), W=gamma Kcap.
```

Then `||R_next||_(3/2)<=gamma*r` uniformly for every coupling in that frozen
interval. At the main cap, `cbar Kcap=252/3875<1` and

```
gamma=3060/3623<17/20.                                    (5)
```

The narrow interval has gamma<1/16. Exact fractions and denominator floors
are in the output; all coefficient factors are increasing for positive r,d
below their pole, which proves continuous coverage. Testing finitely many
interior values is only corroboration, not the coverage proof.

If r=0 every B_Y is zero because the norm is a sum of nonnegative local terms
on nonempty supports. Thus every X_Y and the entire R_next vanish. This holds
also when tau is nonzero. There is no division by zero, and no inference that
the actual source is nonzero because Kcap is positive.

## 6. Scalar and diagonal updates remain complete

Write `b=3/2`, and for each self-adjoint indexed J_Y of R_next retain its full
support and define

```
c'_Y=<Omega_Y,J_Y Omega_Y>,
B'_Y=P_Y J_Y Q_Y+Q_Y J_Y P_Y,
Z'_Y=Q_Y(J_Y-c'_Y I)Q_Y,
J_Y=c'_Y I+B'_Y+Z'_Y.
```

The respective weighted costs are at most `gamma r`, `gamma r` and
`2gamma r`. In particular the complete new mixing obeys the same
weight-changing bound (5). No term is reset to a four-site source; it merely
retains the inherited minimum assigned support size four.

For scalar densities and relative forms that minimum gives

```
|C'|/|Lambda| <= ||R_next||_b/(4b^4) <= (4/81)gamma r,
|C+C'|/|Lambda| <= Kcap/64+(4/81)W,
|<psi,Z' psi>| <= (2/b^4)||R_next||_b <psi,H0 psi>
               <= (32/81)gamma r <psi,H0 psi>.              (6)
```

The scalar estimate double-counts each support over its |Y| sites. The form
estimate uses local vacuum annihilation and
`Q_Y<=sum_(x in Y)(I-P_x)`. It is not a global norm estimate for an extensive
scalar. The old C is unchanged by conjugation and is included in (6).

The full centered diagonal at output weight b satisfies

```
||D_next+Z'||_b <= (b/2)^4 d+2gamma r,
G_after=H0+D_next+Z'
 >= [1-4M-Kcap/8-(32/81)gamma r]H0.                        (7)
```

The factor `(b/2)^4` follows from the minimum support size in the original
D_next decomposition. All indexed sums converge in operator norm in each
finite cuboid, so G_after is self-adjoint on D(H0); the separate form argument
proves (7). It annihilates the product vacuum. Its normalized reference-only
gap exceeds 99/100 on the main interval and 999/1000 on the narrow interval,
using r<=Kcap only in this additional upper budget. Physical reference gaps
are delta times these coefficients. The full transformed Hamiltonian remains

```
(C+C') I+G_after+B'.
```

B' is retained. Thus the displayed reference gap is not the gap of that full
Hamiltonian, and the scalar is not asserted to be its true ground energy.

## 7. Meaning of the controls and the remaining boundary

`check.py` independently reconstructs the exponential product through degree
six in rational matrices. It checks the complete D and B coefficients, rejects
omission of D, retains old/new scalars and centered complements, and tests
positive, negative and zero scaling. The nontrivial three-level rank inverse
has exact norms `||B||=5`, `||X||=17/10`. This is an algebra fixture, not the
physical AG2 source or an SU(2) truncation.

A separate overlapping-support fixture checks a commutator on a three-factor
union and shows why either root placement is needed. The exterior test acts on
an excited exterior factor and distinguishes local identity extension from a
global-vacuum source. An exterior sequence with coefficients 1/j has bounded
Hilbert norm and divergent energy graph norm, confirming that preservation of
the appropriate domain is not exterior regularization. Full finite support
enumeration includes repetitions and an incoming term meeting only generated
support. The analytic estimate (2), not this enumeration, proves completeness.

Two controls identify incorrect norm interpretations. An n-support rank mixing
operator normalized at weight 3/2 has weight-two norm `(4/3)^n`, so the
available output bound cannot be reset to input weight two. For arbitrary
interactions, `U=(3/2)^(-n) X_Pauli^tensor n` and singleton
`V_i=Z_i/(3/2)` have individual weight-3/2 norms one, while their commutator
has weight-3/2 norm `2n/(3/2)`. This rules out a universal fixed-weight
bilinear constant for that generic class; it is not a physical counterexample
to a stronger specially restricted theorem. A separate exact number example
shows that two upper budgets cannot supply an actual contraction denominator.

The method descends from known local bare-reference block diagonalization;
the overlap refinement was explicitly shared by the advisor before this
contract. Scientific priority is unverified. Nothing here resets O2's failed
particular all-stage majorant. The next problem would require a fresh complete
class and remaining weight schedule. No further correction, infinite global
unitary, original homogeneous numerical gap, physical matching or continuum
construction is executed or proved in this loop.

Reproduce with fresh absolute directories:

```
python3 -B research/round28/reverse/ag3/check.py --output /absolute/fresh/ag3-reverse
python3 -B -O research/round28/reverse/ag3/check.py --output /absolute/fresh/ag3-reverse-opt
```

Each run checks all source and instruction hashes and writes deterministic
results. Normal and optimized outputs must agree byte-for-byte. No current
forward AG3 report or checker was read before this producer freeze.
