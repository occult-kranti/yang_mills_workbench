# H1 forward: continuous decay exposes the bounded-budget boundary

Deform only the omitted coefficients to `ν_f=ατq^(x+y+z)/24`, with
0<q<1. The fixed selected-strip coefficient family, α/E_star (positive
and finite), and spatial lattice spacing stay fixed. q is a dimensionless
continuous action-profile parameter; it is not an inferred physical law.
The old omitted coefficients are recovered exactly at q=1/2.

## Two infinite ledgers agree as rational functions

Summing all orientations and subtracting selected xy strips gives

\[
B(q)=\frac1{8(1-q)^3}
-\frac{1+q+q^2}{24(1-q^4)(1-q^2)(1-q)}.
\]

Independently classify the omitted faces into non-xy, odd-y xy, and
even-y x-separator xy classes. They give

\[
B(q)=\frac2{24(1-q)^3}
+\frac{q}{24(1-q)^2(1-q^2)}
+\frac{q^3}{24(1-q^4)(1-q^2)(1-q)}.
\]

Both reduce algebraically to

\[
B(q)=\frac{2+5q+5q^2+6q^3+3q^4}
{24(1-q)^3(1+q)^2(1+q^2)}.
\]

The checker independently expands the two common-denominator numerators,
so agreement is an exact polynomial identity, not four matching samples.
At q=1/2 it recovers 107/135. Every series term is nonnegative, and
the omitted set includes faces with positive coordinate exponent. Hence B
is strictly increasing on (0,1). The rational form gives

\[
\lim_{q\uparrow1}(1-q)^3B(q)=\frac7{64},
\qquad B(q)\longrightarrow\infty.
\]

## Distinct coordinate and profile limits

For anchors 0≤x,y,z≤L, put m=L+1 and

\[
g_m(q)=\frac{1-q^m}{1-q},\quad
a_m(q)=\sum_{r=0}^2q^r\frac{1-q^{4n_r}}{1-q^4},\quad
n_r=\max(0,1+\lfloor(L-r)/4\rfloor),
\]

and `b_m(q)=(1−q^(2 ceil(m/2)))/(1−q²)`. The retained omitted weight is

\[
s_L(q)=\frac{3g_m(q)^3-a_m(q)b_m(q)g_m(q)}{24},
\qquad t_L(q)=B(q)-s_L(q)>0.
\]

For every fixed q<1, positivity and exhaustion prove `t_L(q)↓0` as
L→∞. At q=1 each finite retained sum remains finite, but the infinite
omitted set has infinitely many weight-1/24 faces and diverges. Fixing L
while taking q→1 therefore cannot establish a bounded infinite operator.

## Admitted operators and the default certificate boundary

For each fixed q<1, the perturbation is a bounded self-adjoint multiplication
operator in the A2 representation with `||V(q)||≤α|τ|B(q)`. All omitted
free-Haar witnesses remain valid, because only coefficients changed. The
same-domain and codimension-one proofs therefore apply if
`|τ|B(q)<1/8`, yielding the inherited lower bound

\[
\operatorname{gap}(H(q))\ge\alpha[1/8-|\tau|B(q)].
\]

At the original τ=1/64 the sufficient condition is B(q)<8. Since B
increases continuously from 1/12 to infinity, there is exactly one root
q_crit of B(q)=8. Exact rational endpoint checks give
`764003/1000000 < q_crit < 764004/1000000`, a width of 10^(−6).
The endpoint budgets are recorded in `results.json`. This is the boundary
of this sufficient certificate, not a measured or proved physical critical
coupling. At or beyond it, the bound ceases to establish a positive gap;
the actual gap has not been computed there.

The divergence also has an immediate implication at fixed physical α:
maintaining any fixed strict budget `|τ(q)|B(q)≤η/8`, with 0<η<1,
requires `|τ(q)|≤η/[8B(q)]→0`. Thus the bounded-budget argument cannot
reach a nonzero homogeneous omitted coupling simply by increasing q to one.
The local-state consequence of this requirement is reserved for H2.

## Executed failures and remaining scope

The checker verifies q=1/4,1/2,3/4,7/8 and five coordinate cutoffs per q.
It rejects reuse of 107/135 after changing q, a signed coefficient sum as
an absolute norm budget, finite-sum promotion at q=1, a zero common energy
ratio, and interpreting a nonpositive certificate as a gap-closure result.
The common physical scale is fixed throughout, and τ's sign never reduces
its absolute norm budget. Normal and optimized exact runs count once.

The new rational ledger describes a family of fixed-spacing summable
actions. It provides neither a homogeneous stability theorem nor a continuum
limit, and its certificate failure supplies no proof that either target is
impossible or ungapped.
