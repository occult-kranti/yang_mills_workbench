# H2 forward: exact vacuum variance and a return to the selected-strip state

Keep the A2 reference vacuum Ω, fixed selected interactions, fixed spacing,
and fixed positive finite α/E_star. For 0<q<1 assume
`|τ(q)|B(q)≤η/8`, where 0<η<1 is fixed. Write
`g_bar=α(1−η)/8>0`. H1 gives `B(q)~7/[64(1−q)³]`, so
`|τ(q)|=O((1−q)³)`. This forces every fixed omitted face coefficient
to zero at this physical scale. The canonical nonzero-budget ray is
`τ(q)=η/[8B(q)]~(8η/7)(1−q)³`.

## General complete-factor covariance bound

Each face touches at most four complete reference factors. Each factor has
at most ten links, and each orthant link lies in at most four elementary
faces. Thus the symmetric factor-overlap graph on omitted faces has row
degree at most 160, including the face itself. Product-reference expectations
factorize for disjoint factor supports; each face also has zero mean by its
free Haar witness. Only overlapping supports can contribute covariance.
Using `2|a_f a_g|≤a_f²+a_g²`, `|x_f|≤1`, and the symmetric row bound,

\[
\|V_q\Omega\|^2\le160\alpha^2\tau^2\sum_f w_f(q)^2
\le\frac{5\alpha^2\tau^2}{6(1-q^2)^3}.
\]

The last sum uses all three face orientations. First prove the estimate
for finite sums, then pass to their operator-norm convergent infinite series.
The checker enumerates the full factor-neighbor sets of a finite set of
faces, including neighbors beyond that set; its observed maximum is never
substituted for the all-geometry bound 160.

## A sharper identity specific to the actual omitted faces

The same model has more structure than the generic dependency bound needs:
**each omitted face has two free Haar links**. Non-xy faces have their two
z-links; odd-y xy faces have their two odd-row y-links; separator xy faces
have their two x-residue-3 x-links. Every pair is free in the complete-strip
reference and consists of distinct links.

Two distinct elementary square faces share at most one link. Therefore, for
f≠g, at least one free link of f is absent from g. Integrate that link
first: x_f is a normalized fundamental character linear in that Haar
quaternion, while x_g and the remaining reference density do not depend
on it. Its conditional first moment vanishes, giving
`<x_f x_g>_ref=0`. For f=g, integrating one free Haar link instead yields
`<x_f²>_ref=1/4`, independently of every remaining SU2 matrix. The
identity follows from `E[u_i u_j]=δ_ij/4` and the unit norm of the
remaining quaternion coefficient. No independence of whole faces is assumed.

Since `sum_f w_f(q)²=B(q²)/24`, the orthogonal vectors x_fΩ give
the exact variance

\[
\boxed{\sigma_q^2:=\|V_q\Omega\|^2
=\frac{\alpha^2\tau(q)^2}{96}B(q^2).}
\]

Finite pair checks verify the two free witnesses and common-link cardinality;
the preceding conditional Haar argument proves the infinite identity.
Disjoint link supports alone would not justify general factor independence:
two disjoint link sets can still touch the same entangled strip factor.

## Projection and energy bounds use the reference vacuum

Let H_q=H_ref+V_q, with ground e_q≤0 and rank-one projection P_q.
The original zero-mean reference and compression proof gives excited H_q
spectrum at or above g_bar. On Q_q=1−P_q, its inverse therefore has
norm at most 1/g_bar. Because `H_qΩ=V_qΩ`,

\[
\|P_q-P_\Omega\|=\|Q_q\Omega\|
\le\min(1,\sigma_q/g_{bar}).
\]

For the energy estimate use instead `Q_Ω=1−P_Ω`. Its compression
`D=Q_Ω H_q Q_Ω` is at least g_bar. A ground vector cannot be
orthogonal to Ω; block elimination is consequently legitimate and gives

\[
e_q=-\langle V_q\Omega,(D-e_q)^{-1}V_q\Omega\rangle,
\qquad -\sigma_q^2/g_{bar}\le e_q\le0.
\]

These reference-vacuum statements must not be replaced by an unproved
zero-mean claim in some already perturbed remote ground state.

The uniform budget and exact variance imply σ_q²=O((1−q)³), hence
global projector error O((1−q)^(3/2)) and energy error O((1−q)³).
The trace-norm distance of the pure states is twice the projector distance,
so every bounded observable in this Hilbert representation converges in
expectation to its selected-strip reference value. On the canonical ray,

\[
\frac{\sigma_q^2}{\alpha^2(1-q)^3}\to\frac{\eta^2}{5376},
\qquad
\frac{(\sigma_q/g_{bar})^2}{(1-q)^3}
\to\frac{\eta^2}{84(1-\eta)^2}.
\]

## The operator norm nevertheless stays nonzero on that ray

The upper bound is `||V_q||≤α|τ|B(q)`. For a finite subset of faces,
choose a unit vector supported on the finitely many full factors touching
their links and localized with every such link near the identity. Every
retained trace is then arbitrarily close to one. The omitted remainder
has norm at most its absolute coefficient tail. Increasing the finite set
and then shrinking the localization neighborhoods attains the upper bound
as a supremum. This proves

\[
\|V_q\|=\alpha|\tau|B(q)=\alpha\eta/8
\]

on the canonical ray. No illegal delta-function state or positive probability
of infinitely many identity links is required. A nonvanishing perturbation
norm therefore coexists here with proved global ground-state convergence;
neither norm-resolvent convergence nor its failure follows from that norm
fact alone.

## Endpoint and controls

Exact controls include shared factors despite disjoint links, both free
witnesses, a finite-neighbor maximum masquerading as a universal degree,
a perturbed-ground nonzero expectation of a reference-zero-mean operator,
constant perturbation norm with unchanged ground state, and attempts to
vary α to hide the diverging budget. q=1 itself is excluded from the
summable operator family. The endpoint Ω retains its selected-strip
interactions and need not be the free Haar product. This route loses fixed
nonzero homogeneous **omitted** couplings; it does not disprove a gap in
the homogeneous or continuum Yang–Mills theories. No Gauss-only GNS
equivalence or missing physical matching is supplied by this result.
