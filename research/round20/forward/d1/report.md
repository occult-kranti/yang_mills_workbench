# D1 forward: finite-factor completion and a quantitative resolvent limit

This is conditional on Round19 A2's complete-strip incomplete tensor product and
its self-adjoint nonnegative reference operator. Fix one physical energy
`E_star>0`, `alpha>0`, and real dimensionless `tau`. The coordinate cutoff `L`
is an integer regulator, never an energy. No homogeneous or continuum limit is
claimed.

## Exact retained and tail coefficients

Put `m=L+1`, `g_m=sum_{j=0}^{m-1}2^{-j}=2(1-2^{-m})`, and

\[
a_m=\sum_{r=0}^2 2^{-r}\frac{1-16^{-n_r}}{1-1/16},\qquad
n_r=\max(0,1+\lfloor(L-r)/4\rfloor),
\]

\[
b_m=\frac{1-4^{-\lceil m/2\rceil}}{1-1/4}.
\]

The total face weight retained by **anchor** coordinates `0<=x,y,z<=L` is
`g_m^3/8`; its selected-strip part is `a_m b_m g_m/24`. Thus the omitted-face
weight retained in the perturbation and the positive discarded tail are

\[
s_L=\frac{g_m^3}{8}-\frac{a_m b_m g_m}{24},\qquad
t_L=\frac{107}{135}-s_L\downarrow0.
\]

The descent and limit follow from the positive-term exhaustion, not the nine
fixtures. The closed forms show `a_infty=28/15`, `b_infty=4/3`, `g_infty=2`,
so the infinite omitted total is `1-28/135=107/135`.
The face coefficient remains `alpha tau/(24*2^(x+y+z))` at every L.

## A genuine finite-factor construction

A selected strip anchored at `(4i,2j,z)` contains three xy plaquettes and ten
distinct links. Each horizontal x-link with `x mod4 in {0,1,2}` belongs to
the unique strip `(x-x mod4,y-y mod2,z)`. Each y-link with even y belongs
to `(x-x mod4,y,z)`. All remaining links, including every z-link, are free
reference factors. These rules prove disjointness and exhaust all link cases.

Take all four links of every retained omitted face, including links whose
coordinates exceed L. Replace each touched strip link by its whole ten-link
reference factor. Retain each touched free link as its own factor. This gives
`I_L`, a finite set with at most `4|O_L|` factors. Enlarging a factor requires
no further iteration: all its links belong to the same already selected
factor. Define on the finite tensor product of these factors

\[
K_L=\sum_{i\in I_L}h_i+V_L,\qquad
V_L=-\alpha\tau\sum_{f\in O_L}w_f x_f.
\]

There are finitely many factors, each an infinite-dimensional L2 space;
`K_L` is not a finite matrix. The finite nonnegative factor sum is
self-adjoint and the bounded multiplication perturbation preserves its
operator domain. The incomplete tensor product factors exactly into this
finite tensor product and its vacuum-based exterior. Its closed form sum
gives

\[
H_L=K_L\otimes I+I\otimes H_{ref,out}=H_{ref}+V_L.
\]

All completed strip links remain present with their original A2 reference
coefficients; completion does not add or change perturbing faces.

## Norm-resolvent bound with physical units

Absolute summability and `|x_f|<=1` imply the operator-norm convergent series
and bound

\[
\|V-V_L\|\le\epsilon_L:=\alpha|\tau|t_L.
\]

Both H and H_L are self-adjoint on exactly `D(H_ref)` because both added
operators are bounded self-adjoint. For every common nonreal physical energy z,
the resolvent identity on this common domain extends to bounded operators:

\[
(H-z)^{-1}-(H_L-z)^{-1}
=-(H-z)^{-1}(V-V_L)(H_L-z)^{-1}.
\]

Consequently

\[
\|(H-z)^{-1}-(H_L-z)^{-1}\|
\le\epsilon_L/|\operatorname{Im}z|^2\longrightarrow0.
\]

The bound has inverse-energy units. No isolated-ground-state assumption is
needed for this loop. The theorem is for the exact exterior-reference lift,
not the operator obtained by padding a finite Hamiltonian with zero exterior
energy, and not yet the original clipped boundary Hamiltonian.

## Discriminating controls and evidence

At tau=0, dropping the exterior reference term leaves any exterior excited
free link at energy zero. The correct reference puts a fundamental free-link
excitation at `3 alpha/4`. For alpha=E_star and z=i E_star, the resolvent
difference on this vector has modulus `3/(5 E_star)` for every L; its square
is exactly `9/(25 E_star^2)`. The excitation can always escape the finite
support. This disproves norm-resolvent convergence of that wrong embedding.

Executed controls also detect: dropping crossing-face links; dropping one
completed strip link; cancellation of equal opposite disjoint face
coefficients (a zero signed sum does not bound the nonzero multiplication
operator); invalid zero/static physical references; real resolvent parameters;
and the false assertion that finitely many L2 factors have finite dimension.

`check.py` independently enumerates all retained faces and completed factors
for L=0..8, compares their exact weights with the residue-class closed forms,
and emits the exact ledger, controls, and source-bound manifest. These finite
arithmetic checks verify implementation and fixtures; the infinite operator
argument is the proof above. Ordinary and optimized replays count once.

Bounded perturbation and resolvent methods are standard (Teschl,
*Mathematical Methods in Quantum Mechanics*, sections 6.1 and 6.6; see the
advisor source register). The contribution here is the stated model's explicit
support completion and dyadic error ledger; no literature-priority claim is made.
