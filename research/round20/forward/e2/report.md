# E2 forward: all boundary phases converge on bounded local observables

Keep the full inherited coefficient family: each fixed selected strip obeys
`|λ_L|,|λ_R|≤α/2`, `|μ|≤α/8`, with arbitrary permitted signs and zeros;
omitted coefficients are `ατw_f`. Require α>0, a fixed positive physical
reference E_star, fixed spacing a, and `β=α|τ|107/135<δ=α/8`.
Consider literal rectangular boxes with vertices `[0,Nx]×[0,Ny]×[0,Nz]`.
The minimum side tends to infinity; the lower boundary stays at zero.

## Every finite reference, including clipped boundaries

Group selected faces actually contained in the box by their infinite strip
anchor. Each nonempty group is a complete or proper clipped strip; its links
are disjoint from the other groups. All other box links are free factors.
A1 supplies the same gap δ for every such component, with exactly the fixed
inherited coefficients. Subtract the scalar
`c_box=sum_S E_S` of **actual clipped-component** ground energies, not the
energies of completed strips outside the box. The resulting reference is a
nonnegative product operator with unique vacuum and gap at least δ.

Every omitted contained face still has an actual unused link: non-xy faces
have a z-link, odd-y xy faces have a y-link on an odd row, and separator
xy faces have an x-link at x=3 modulo 4. Clipping cannot make these links
selected. Their Haar means vanish even though other links can lie in
entangled clipped strip factors. Thus every truncated or full finite
perturbation has zero reference mean and norm at most β. A2's codimension-one
argument gives each shifted finite operator a unique ground of energy≤0,
and the excited spectrum starts at least at δ minus its absolute budget.
Adding back c_box leaves its state and gap unchanged.

## A common interior state

Fix an interior anchor cutoff M and a bounded local operator A. Complete the
supports of both V_M **and A** under the full infinite reference factors,
producing a finite central set J. If A's links have coordinates≤R, the
sufficient margin `min(Nx,Ny,Nz)≥max(M+4,R+3)` places every central strip
entirely inside the box. The factor rule gives this bound directly: face
links extend at most one beyond their anchors; completing an x strip extends
at most three further coordinates. No interaction reaches a remote factor
once only V_M is retained.

The shifted finite operator with perturbation V_M is consequently a central
operator on J plus a disjoint remote clipped reference. The corresponding
infinite truncated operator has exactly the same central operator plus its
disjoint full exterior reference. Their simple ground states have the same
central marginal, call it ω_M. A is an operator on J, so its expectation is
identical in these two truncated states. This statement would fail to follow
if A's support had been omitted from J.

## Uniform errors, followed by the limit

Let `s_M,t_M` be D1's exact retained weight and tail, put
`g_M=δ−α|τ|s_M>0`, and `ε_M=α|τ|t_M`. The norm differences between
the finite full and finite truncated perturbations satisfy

\[
\eta_{M,box}=\alpha|\tau|
\sum_{f\in O_{box}\setminus O_M}w_f\le\epsilon_M.
\]

These are absolute budgets, independent of the outer phase or size. D2's
residual argument applies in each respective finite or infinite Hilbert
space. The truncated excited spectral threshold is at least g_M, and each
full ground has nonpositive energy. Therefore

\[
|\omega_{box}(A)-\omega_M(A)|
\le2\|A\|\min(1,\eta_{M,box}/g_M),
\]

\[
|\omega_\infty(A)-\omega_M(A)|
\le2\|A\|\min(1,\epsilon_M/g_M).
\]

Combining on the common local algebra gives the requested uniform bound

\[
|\omega_{box}(A)-\omega_\infty(A)|
\le4\|A\|\min(1,\epsilon_M/g_M)\longrightarrow0.
\]

First choose M large enough to make the tail small, then choose every side
large enough for the central support. This proves all-phase local-state
convergence for every bounded local A. Since states have norm one and local
operators are norm dense in the quasi-local C*-algebra, approximation extends
the conclusion to that algebra's weak-star topology. Fixed M alone leaves a
fixed error; a small finite fixture does not by itself establish convergence.

## Topology and controls

A moving tensor factor can be in `(3/5,4/5)` instead of its vacuum `(1,0)`.
Every fixed local marginal eventually equals the vacuum marginal, while its
global projector distance from the vacuum stays 4/5. The executed rational
fixture therefore forbids inferring vector norm or global norm-resolvent
convergence from the local conclusion; it is a topology counterexample,
not a claimed calculation of the actual clipped ground state.

Eight rectangular fixtures cover all four x residues and both y parities.
They enumerate the actual clipped factors, every omitted-face Haar witness,
and an A supported outside V_0. Other controls remove A's support, use
unshifted component energies, remove the uniform A1 gap, or replace summable
tails by a homogeneous nondecaying face count. The report's infinite proof
supplies the theorem; exact fixtures audit the geometry and inequalities.
No global boundary-vector, arbitrary-phase norm-resolvent, homogeneous, or
continuum claim is made.
