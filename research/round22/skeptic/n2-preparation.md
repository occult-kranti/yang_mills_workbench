# N2 independent preparation

Prepared from the frozen N2 contract before either current producer was read.
This is a private skeptical derivation/checklist, not an admission or a second
selection. The N1 strong-integral sources and domain proof remain applicable.

## Boundary reconstruction

Let `R_L={0,...,4L-1} x {0,...,2L-1} x {0,...,L-1}` be the set of owned
tails. E_L consists of all three positive links at each tail, hence has
`3(4L)(2L)L=24L^3` links. Euclidean division into x periods four and y periods
two gives unique block ownership. Each block contains its whole ten-link
selected strip and fourteen free singleton factors, so reference evolution
preserves this complete factor support for every time.

A positive elementary face at p in axes a,b has tails `p,p,p+e_a,p+e_b`.
If p lies in R_L, two of its links lie in E_L. Conversely, if one face link
lies in E_L, its tail is p or p+e_a or p+e_b. Since R_L is a coordinatewise
initial rectangle in the nonnegative octant, that tail lying in R_L forces
p in R_L. Thus the faces incident to E_L are exactly those with anchor in
R_L. Some other tails or endpoints may leave the rectangle and must remain
in the face. This converse specifically uses the origin-aligned initial
rectangle; it must not be reused for an arbitrarily translated region.

Write `G_L(u)=sum_(j=0)^(L-1) u^j`. Within one primitive block the omitted
anchor numerator is

`p(q)=3(1+q+q^2+q^3)(1+q)-(1+q+q^2)`
`=2+5q+5q^2+6q^3+3q^4`.

Therefore the exact finite incident weight candidate reconstructed here is

`D_L(q)=p(q) G_L(q^4) G_L(q^2) G_L(q)/24`
`=B(q)(1-q^(4L))(1-q^(2L))(1-q^L)`.

This follows from the boundary proof and geometric sums; finite enumerations
must only test it. At q=1 in this finite polynomial, `D_L(1)=21L^3/24`.
It does not define the forbidden infinite q=1 perturbation.

## Joint certificate reconstruction

For `sup_q ||A_q||||B_q|| <= M < infinity`, N1 applies separately at each q,
with no uniform domain-preservation requirement. Its state comparison is
already uniform in bounded operators. Defining
`R(q,L)=(1-q^(4L))(1-q^(2L))(1-q^L)`, its normalized certificate is

`K_q=6 sigma_q/gbar+(2alpha T_q/hbar) tau_q D_L(q)`
`=6 sigma_q/gbar+(eta/4)(alpha T_q/hbar) R(q,L)`.

Then the correlation error is bounded by `M K_q`. The state term vanishes,
so vanishing of K_q is equivalent to `(alpha T_q/hbar) R(q,L)->0`.
This equivalence concerns this nonnegative certificate. It is not necessary
for the actual correlations, especially if either observable is scalar or
their norm product itself tends to zero. A bound using M also avoids division
by a possibly zero norm product.

For epsilon=1-q, use `-log q / epsilon ->1`. For beta>0 the floor satisfies
`L/(ell epsilon^-beta)->1`. Thus:

| Support protocol | R(q,L) behavior | Fixed power-window certificate |
| --- | --- | --- |
| beta=0; actual fixed integer L | `R~8L^3 epsilon^3` | Vanishes exactly when gamma<3. |
| 0<beta<1 | `R~8ell^3 epsilon^(3-3beta)` | Vanishes exactly when gamma<3(1-beta). |
| beta=1 | `R->(1-exp(-4ell))(1-exp(-2ell))(1-exp(-ell))>0` | No vanishing certificate for gamma>=0. |
| beta>1 | `R->1` | No vanishing certificate for gamma>=0. |

At the equality gamma boundary in the first two rows, the dynamical certificate
has positive limit `2eta C L^3` or `2eta C ell^3`, respectively. At beta=1
or beta>1 with gamma=0 the limit is the corresponding positive R limit times
eta C/4. For positive gamma there it diverges before any trivial norm cap.
These conclusions use positivity of eta,C and L or ell. They do not imply
actual correlation nonconvergence.

For fixed L and `T=(hbar/alpha) C epsilon^-3/[log(1/epsilon)]^k`, k>0,
the dynamic term is asymptotic to `2eta C L^3/[log(1/epsilon)]^k` and vanishes.
The unshortened endpoint remains uncertified. This substitution is a check
within N2, not a separate research loop or actual endpoint resolution.

## Review checklist

* Check ownership and the exact initial-rectangle converse for all L, retaining
  outgoing links and faces with other links outside the region.
* Independently enumerate at least L=1 and a larger L; distinguish 24L^3 owned
  links from a clipped vertex graph and distinguish incidence from containment.
* Check finite D_L against direct sums at exact q. The infinite B(q) is strictly
  larger for every finite L and q in (0,1); it must fail as an equality control.
* Prove every factor asymptotic using epsilon L and the logarithm of q; keep
  beta=0 separate because floor(ell) need not equal ell, with the maximum at one.
* Require uniform boundedness and pointwise application of the already proved
  N1 estimate, without claiming strong convergence uniformly over moving vectors.
* Use the certificate-only meaning of necessity and critical boundaries. Add
  scalar/commuting or vanishing-norm witnesses to reject stronger inference.
* Preserve fixed physical scales; region sides are 4aL,2aL,aL. A growing observed
  region changes neither spacing nor the infinite Hamiltonian.
* Review both frozen manifests and fresh ordinary/optimized outputs after root
  opens review; temporary replay outputs should remain outside the repository.

No N2 producer has been inspected and no formula in this note is admitted by
the skeptic. Root must wait for both independent submissions and open review.
