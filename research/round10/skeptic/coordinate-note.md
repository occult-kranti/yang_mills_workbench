# A legitimate next continuous variable: relative loop orientation

This is a finite-dimensional gauge-orbit result, separate from the 119 round-10 verification gates and the one-square gap theorem. It identifies information needed for a two-loop model; it does not derive that model's kinetic operator or extend a mass-gap bound.

After tree gauge reduction of two independent loops, the holonomies transform by **simultaneous conjugation**: (U,V) -> (gUg^-1,gVg^-1). Write

    U = x I + i a·sigma,    V = y I + i b·sigma,
    x²+|a|² = y²+|b|² = 1.

The three real trace coordinates are

    x = Tr(U)/2,    y = Tr(V)/2,    z = Tr(UV)/2 = xy - a·b.

Therefore their exact admissible domain is

    -1 <= x,y <= 1,
    (z-xy)² <= (1-x²)(1-y²).

Equivalently, 1-x²-y²-z²+2xyz >= 0, together with the bounds on x and y. These conditions also imply -1<=z<=1.

**Necessity.** The scalar part of (xI+i a·sigma)(yI+i b·sigma) is xy-a·b. Apply the ordinary Cauchy–Schwarz inequality to the two real vectors a and b.

**Sufficiency.** If |x|<1 and |y|<1, choose vectors of lengths sqrt(1-x²) and sqrt(1-y²), with dot product xy-z. The displayed inequality says exactly that the required dot product lies within its possible range. These vectors construct SU(2) matrices realizing the coordinates. If x=+1 or -1, then a=0 and the inequality forces z=xy; take U=xI and any V with trace 2y. The y=+1 or -1 cases work the same way. This construction never divides by a vanishing length.

**Completeness for this pair of loops.** Simultaneous conjugation rotates a and b by a common element of SO(3). Their lengths and mutual dot product form their Gram matrix. Two ordered pairs of vectors with the same Gram matrix are related by an orthogonal transformation. If that transformation has determinant -1, composing it with a reflection fixing the target pair's span changes its determinant without changing either vector; the span has dimension at most two. Thus a common proper rotation exists. Every such rotation lifts to SU(2). The three trace coordinates consequently determine the simultaneous-conjugation orbit, including collinear and central degeneracies.

In the interior, the relative orientation is the bounded continuous variable

    t = (xy-z)/sqrt[(1-x²)(1-y²)] = a_hat·b_hat,  -1<=t<=1.

It is undefined when either vector vanishes. At those degenerate points the relative orientation is irrelevant and z=xy is the correct constraint. A program should retain (x,y,z) or explicitly mark the relative angle undefined, rather than inventing a zero angle or dividing by zero.

**Exact counterexample to independent loop traces.** Take U=i sigma_3. For V=i sigma_3, x=y=0 and z=-1. For V=i sigma_1, x=y=0 and z=0. The separate loop traces agree, but the joint trace differs, so these configurations cannot be related by simultaneous conjugation. Treating two interacting loops as only two independent conjugacy angles would discard a genuine gauge-invariant degree of freedom.

The accompanying `coordinate_check.py` uses exact Gaussian-rational 2x2 matrices. It checks determinant one and unitarity, independently extracts traces, verifies the domain and its polynomial form, exercises central degeneracies, and retains the trace counterexample. The checks are separate from the earlier 119 gates. Shared-link electric cross terms, the physical measure in these coordinates, operator domains and a two-loop cutoff theorem remain work to derive.
