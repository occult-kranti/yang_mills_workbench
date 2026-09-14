# H1 reverse reconstruction: separate the spatial profile from the cutoff

Change only omitted-face coefficients to `w_f(q)=q^(x+y+z)/24`, with `0<q<1`.
The selected-strip coefficients, reference vectors, alpha and lattice spacing
stay fixed. The continuous parameter q is an explicit action deformation, not
an identified physical law or an energy scale. At q=1/2 it returns to A2.

Partition omitted faces into xz/yz, odd-y xy, and separator xy. Their sums give

\[
B(q)={1\over24}\left[{2\over(1-q)^3}
+{q\over(1-q)^2(1-q^2)}
+{q^3\over(1-q)(1-q^2)(1-q^4)}\right].
\]

As a cross-check, all faces sum to `3/[24(1-q)^3]`; selected faces sum to
`(1+q+q^2)/[24(1-q^4)(1-q^2)(1-q)]`. Clearing denominators shows exact
rational-function agreement, with common normalized numerator
`2+5q+5q^2+6q^3+3q^4` over `24(1+q)^2(1+q^2)`.

For the independent coordinate regulator L, define

\[
S={1-q^{L+1}\over1-q},\quad
Y={1-q^{2(\lfloor L/2\rfloor+1)}\over1-q^2},\quad
X={q^3(1-q^{4\lfloor(L+1)/4\rfloor})\over1-q^4}.
\]

Then the retained weight is `W_L=[2S^3+S(S-Y)S+XYS]/24` and the exact
positive tail is `t_L(q)=B(q)-W_L(q)`. The checker compares this expression
with direct coordinates at q=1/4,1/2,3/4,7/8 and L=0,1,2,4,8.
For fixed q<1, the geometric tails decrease to zero. For fixed L, the tail
increases as q increases and is not uniformly small near q=1.

B(q) is strictly increasing: it is a convergent power series of nonnegative
coefficients with at least one strictly positive nonconstant coefficient.
Its normalized endpoint is exactly

\[
\lim_{q\uparrow1}(1-q)^3B(q)=7/64.
\]

This proves divergence at the homogeneous endpoint. In particular q=1 cannot
be admitted by substituting a finite coordinate sum for the infinite norm
budget. For fixed L, W_L stays finite as q approaches1, so the retained
fraction W_L/B tends to zero. L and q limits cannot be silently exchanged.

The A2 operator construction applies at every q<1 for finite tau, while the
same gap certificate requires `|tau|B(q)<1/8` and yields
`gap>=alpha[1/8-|tau|B(q)]`. E_star and alpha/E_star remain fixed and positive.
At the default tau=1/64, this certificate is positive exactly on B(q)<8. The
checker constructs an exact rational bracket for its unique root using strict
monotonicity and exact rational inequalities; endpoint values and the bracket
are recorded in results.json. This is a boundary of the sufficient norm
estimate, not evidence that the physical spectral gap closes.

The prior dyadic budget107/135 fails when q changes. Signed cancellations also
cannot reduce this absolute norm budget. The code retains these wrong models
and the distinction between failure of a proof route and a closed physical gap.
No dense homogeneous or continuum conclusion is admitted.
