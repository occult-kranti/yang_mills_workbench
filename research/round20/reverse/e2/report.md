# E2 reverse reconstruction: local states across arbitrary upper phases

Fix a bounded local observable A and an interior omitted-face cutoff M. Close
both its link support and every face in V_M under complete infinite reference
factors. The resulting central factor set J is finite. Every sufficiently large
rectangular box contains J completely, regardless of Nx modulo 4 or Ny parity.
This observable-dependent geometric margin is necessary even if M is small.

The remaining selected face components are literal A1 clipped strips; remaining
links are free. Subtract the exact scalar `c_box=sum E_S` over all selected
components, including clipped components. Each shifted component has a unique
vacuum and gap at least `delta=alpha/8`. The omitted potential has zero mean
in that product vacuum: xz/yz faces contain free z links, odd-y xy faces contain
free odd-y y links, and separator xy faces contain free x=3 mod 4 links. These
are exhaustive cases and remain free under clipping. Thus the full finite
Hamiltonian has a rank-one ground with shifted energy at most zero, by the A2
compression argument with beta_box<=beta_infty<delta.

After truncating the omitted perturbation to V_M, the central Hamiltonian
K_J is common to the box and the infinite representation. Every other factor
is an uncoupled reference component, so both truncated grounds have exactly the
same central marginal. The remote factors may have different ground vectors;
no equality of their boundary embeddings is used.

Write `beta_M=alpha*|tau|*s_M`, `g_M=delta-beta_M`, and
`epsilon_M=alpha*|tau|*t_M`. On the orthogonal complement of the truncated
ground, the truncated box Hamiltonian has threshold at least g_M. Central
excitations satisfy this bound by the compression theorem. Remote excitations
cost at least delta above central energy e_M>=-beta_M, so they too have absolute
threshold at least g_M. Since the full shifted ground energy is <=0, the
D2 residual argument bounds its projector distance from the truncated box
ground by `min(1,epsilon_M/g_M)`. The infinite comparison gives the same bound.
Consequently

\[
|\omega_{box}(A)-\omega_\infty(A)|
 \le4\|A\|\min(1,\epsilon_M/g_M).
\]

One may also cap the final answer by the trivial `2||A||`. The stated bound is
uniform in all sufficiently large anchored rectangular boxes. First choose M
large enough for the tail error, then choose the outer sides large enough for
the central support closure. This proves convergence on every bounded local
algebra. By density and norm-one states it extends to weak-star convergence on
the quasi-local C*-algebra. It does not prove convergence for arbitrary global
operators in B(H), global boundary vectors or arbitrary-phase norm resolvents.

The checker independently constructs literal selected components from face-link
incidence, rather than intersecting full-strip factors blindly. This distinction
matters at Ny even, where boundary-row x-links can be free even though their
infinite partners belong to a strip. Eight actual `Nx mod 4` by `Ny mod 2`
fixtures verify central completeness and the omitted-face free-Haar witness.
An observable placed outside the V_M support demonstrates why it must be
included separately in J. Exact error ledgers use the direct D1 omitted-class
sum for M=0..8. Scalar shifts, the uniform A1 gap and the summability premise
remain explicit. Fixed spacing and the anchored lower boundary are retained;
no dense homogeneous or continuum conclusion follows.
