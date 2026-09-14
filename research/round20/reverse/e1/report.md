# E1 reverse reconstruction: aligned literal boxes

Fix `Lambda_N={0,...,N}^3` with `N=4m+3`, `m>=0`. The selected xy strip
anchors have x=4i and even y=2j. Horizontal x-links have x<N and y<=N;
selected x-links therefore fill three consecutive x intervals `4i..4i+2`
inside each box. Vertical y-links at even y have x<=N and y<N; their four
x positions `4i..4i+3` are likewise all present. Odd N pairs every included
horizontal row with its partner. Thus every reference strip meeting the box is
included in full; all remaining included links are free factors. This is an
all-m factorization proof, not a numerical extrapolation.

The counts are `C_N=(N+1)^3/8` complete strips, `3N(N+1)^2` links,
`3N^2(N+1)` faces, `3C_N` selected faces and `3N^2(N+1)-3C_N` omitted faces.
Strip supports are disjoint and each has ten links, leaving
`3N(N+1)^2-10C_N` free factors. At N=4, a new strip is clipped, so promotion
of this factorization to arbitrary N is false.

To compute the retained omitted weight, put

\[
A=2(1-2^{-N}),\quad B=2(1-2^{-N-1}),\quad
Y={4\over3}(1-4^{-(N+1)/2}),\quad
X={2\over15}(1-16^{-m}).
\]

The orientation ranges are xy: `x,y<N,z<=N`; xz: `x,z<N,y<=N`;
yz: `y,z<N,x<=N`. Direct omitted-class summation gives

\[
W_N={2A^2B+A(A-Y)B+XYB\over24},\qquad t_N=107/135-W_N.
\]

The first class is xz/yz, the second odd-y xy, and the third separator xy.
The checker enumerates each orientation independently and matches the formula
for N=3,7,11,15. Replacing these orientation ranges by a common anchor cube
changes the retained measure and is explicitly rejected.

Let `H_box,N` be the literal Hamiltonian with the original Casimir and fixed
selected coefficients and the A2 omitted coefficients. Since complete strip
Hamiltonians have ground energies `E_C`, define the scalar energy origin

\[
c_N=\sum_{C\subset\Lambda_N}E_C.
\]

Then, exactly on the common product representation,

\[
(H_{box,N}-c_N)\otimes I+I\otimes H_{ref,out}
 =H_{ref}+V_{box,N}.
\]

No coupling changes in this identity. The scalar subtraction leaves eigenvectors
and spectral gaps unchanged but shifts every absolute energy; it does not leave
a resolvent at fixed z unchanged. The checker includes an exact scalar example
with nonzero resolvent difference. Omitting the exterior generator also spoils
the bounded-tail argument, since its free-link Casimir eigenvalues are unbounded.

D1 and D2 now apply to this literal aligned family. With
`epsilon_N=alpha*|tau|*t_N`, `beta_N=alpha*|tau|*W_N`, and
`g_N=alpha/8-beta_N`, one has the norm-resolvent error
`epsilon_N/|Im z|^2`, shifted-ground energy error `epsilon_N`, rank-one projector
error `epsilon_N/g_N`, and bounded-observable error
`2||A_obs||epsilon_N/g_N`. Fix `alpha/E_star=2`, `tau=1/64`,
`Im z/E_star=1/2` in the executed examples. Lattice spacing is an independently
fixed length and N is a volume regulator, never an energy scale.

This is convergence of the shifted, exterior-completed aligned subsequence.
It says nothing yet about arbitrary boundary phases. Dense homogeneous couplings
and continuum Yang-Mills remain outside the result.
