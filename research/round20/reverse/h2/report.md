# H2 reverse reconstruction: exact variance, constant operator norm, converging ground

Fix `0<eta<1`, fixed positive alpha/E_star, and
`|tau(q)|B(q)<=eta/8`. Write `g_bar=alpha(1-eta)/8`. H1 implies
`|tau(q)|=O((1-q)^3)` as q approaches1. The canonical positive ray is
`tau(q)=eta/[8B(q)]`; its total perturbation norm budget remains nonzero.

A conservative general reference-factor argument first gives a covariance
bound. A face has four links and touches at most four factors. Each reference
factor has at most ten links, and an elementary lattice link lies in at most
four faces. Thus a face overlaps at most160 other face factor supports, counting
itself. If factor supports are disjoint, the product reference and individual
zero means make the covariance zero. Symmetry and `2ab<=a^2+b^2` then imply

\[
\|V_q\Omega\|^2\le160\alpha^2\tau^2\sum_f w_f(q)^2
\le{5\over6}{\alpha^2\tau^2\over(1-q^2)^3}.
\]

A model-specific improvement is exact and does not require pretending that
faces with overlapping complete factors are independent. Every omitted face
has **two** free Haar links: the two z links for xz/yz, the two odd-y y links
for odd-y xy, and the two separator x links for even-y x=3 mod4 xy. Two distinct
elementary faces share at most one link. A free link of f absent from g can
therefore be integrated first, giving `<x_f x_g>=0` for f!=g. For f=g,
conditional Haar invariance and `integral(Tr(U)/2)^2=1/4` give the diagonal.
Absolute summability justifies passage from finite sums. Consequently

\[
\boxed{\sigma_q^2:=\|V_q\Omega\|^2
={\alpha^2\tau(q)^2\over96}B(q^2)}.
\]

The implementation verifies two free witnesses for every fixture face, every
pairwise link-intersection bound, the exact finite diagonal variance and the
factor-overlap bound. It also exhibits disjoint-link faces that share a complete
reference factor: link disjointness alone is not a product-independence theorem.
The zero covariance instead uses the free-link conditional integral.

Let P_q be the actual rank-one ground projection of H_q. Its excited spectrum
has absolute threshold at least g_bar. Since `H_q Omega=V_q Omega`, applying
the inverse on the actual excited spectral subspace gives

\[
\|P_q-P_\Omega\|\le\min(1,\sigma_q/g_{bar}).
\]

For energy, use Q=1-P_Omega. The compression `QH_qQ>=g_bar Q`, ground energy
e_q<=0, and nonzero vacuum overlap give the Schur equation
`e_q=-<v,(QH_qQ-e_q)^(-1)v>`, where `v=QV_q Omega=V_q Omega`.
Hence `-sigma_q^2/g_bar<=e_q<=0`. The nonzero overlap follows because a ground
orthogonal to Omega would contradict the positive compression threshold.

A provisional remote-ground shortcut is explicitly rejected: `e_full<=0` does
not imply `e_full<=e_remote` when e_remote is negative. Any remote-decoupling
proof would need to establish its absolute excited threshold separately.
The present argument uses the original reference vacuum and the established
absolute threshold directly; it never drops a remote scalar energy shift.

On the canonical ray, the exact endpoint rates are

\[
{\tau(q)\over(1-q)^3}\to{8\eta\over7},\quad
{\sigma_q^2\over\alpha^2\eta^2(1-q)^3}\to{1\over5376},\quad
{(\sigma_q/g_{bar})^2\over(1-q)^3}\to
{\eta^2\over84(1-\eta)^2}.
\]

Thus P_q converges in operator norm to P_Omega at least at the indicated
`O((1-q)^(3/2))` bound, and the corresponding vector states converge in dual
norm, since their trace-norm difference is `2||P_q-P_Omega||`. The energy
converges to zero with `O((1-q)^3)` bound. These are upper-bound rates, not
claims that the actual errors have nonzero leading asymptotic coefficients.

Despite this, the canonical perturbation norm is exactly

\[
\|V_q\|=\alpha\eta/8.
\]

The upper bound is its absolute coefficient sum. For the lower bound, fix a
finite face set and choose a normalized finite-factor smooth wavefunction
supported near identity for all its links. Every retained Wilson trace is then
arbitrarily close to1. The remaining operator is bounded by its absolute tail.
Taking the retained set to exhaust the faces and then the localization error
to zero reaches the full coefficient sum. This is a norm computation in the
full A2 factor representation; no restricted-sector equality is assumed.
It demonstrates why constant perturbation norm does not obstruct ground-state
convergence. A finite diagonal counterexample executes the same topology
warning without serving as the lattice proof.

The endpoint state is the selected-strip reference, which still contains its
selected interactions. A fixed nonzero homogeneous omitted coupling falls
outside this global bounded-perturbation certificate, but its physics is not
disproved. Fixed spacing, representation and physical alpha/E_star are retained.
The q=1 endpoint is not admitted as a member of this finite-budget construction,
and no continuum, physical c calibration or Gauss-only GNS claim follows.
