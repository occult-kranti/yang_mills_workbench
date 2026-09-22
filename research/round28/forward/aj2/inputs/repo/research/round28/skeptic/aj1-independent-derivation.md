# AJ1 independent pre-exchange derivation

The proposed regularity route closes within the actual I1 model. A local vacuum reset proves, for every finite coarse region R and every finite whole-star volume containing it,

\[
 \operatorname{Tr}(\rho_{\Lambda,R}H_{0,R})
 \leq 2M\,n_\Lambda(R)\leq8M|R|=56|\tau||R|,
 \qquad M=7|\tau|.
\]

This supplies spectral tightness and trace-norm convergence of the local densities to the restriction of the already admitted I1 state. Local normality then justifies strong gauge implementation and compatible local Haar averaging. The physical bounded-local observable cyclic space equals the joint gauge-fixed vector space and reduces the actual centered I1 GNS generator. Its self-adjoint physical energy restriction inherits the threshold `alpha/16`; no nonzero physical excitation or numerical coupling interval is established.

This is an independent pre-exchange derivation. The contract, all48 declared sources, used instructions and a fresh primary retrieval were snapshotted before science; the advisor verified the65-file pack. Current AJ1 producer science remains unread. The finite diagnostics below verify geometry, arithmetic and counterexamples, not the infinite-dimensional analytic implications.

## Actual model, domains and compact energy cutoffs

Keep the positive coarse orthant and I1 whole-star empty-boundary exhaustion. Site b owns every positive original link with tail `(4b_x+r,2b_y+s,b_z)`, `0<=r<4`, `0<=s<2`: exactly24 links, including outgoing links and their external head endpoints. Ten links form the complete selected xy strip and14 are free. This factorization is on the full link Hilbert space; no gauge-constrained tensor factorization is assumed.

The inherited selected coefficients remain fixed, with endpoint bounds `alpha/2` and bridge bound `alpha/8`. On one strip the bounded potential has norm at most `9alpha/8`. The constant Haar trial has zero electric and Wilson expectations, while positivity of the electric part bounds the strip ground energy between `-9alpha/8` and0. With `delta=alpha/8`,

\[
 h_b=8\sum_{e\text{ owned by }b} C_e+B_b,
 \quad\|B_b\|\leq18,
 \quad h_b\geq8\sum_e C_e-9.
\]

The inherited strip theorem and free-link gap give the stronger nonnegativity, unique onsite vacuum Omega_b, and `h_b>=I-P_b`. Its actual operator/form domains are the full product-group H2/H1 domains, preserved by bounded smooth multiplication. The positive Casimir sum has compact resolvent: its Peter–Weyl labels have finite multiplicities, and only finitely many labels lie below a finite energy. Bounded perturbation preserves compact resolvent. Finite sums `H0,R=sum_(b in R)h_b` therefore have compact resolvent and finite-rank spectral cutoffs `P_(R,T)=1_[0,T](H0,R)`. The form lower bound also gives a spectral **counting** upper comparison to `8 sum C-9|R|`; it does not identify its spectral projection with a bare-electric cutoff.

At each retained whole star `b+S`, `S={0,ex,ey,ez}`, include all21 omitted faces exactly once:

\[
 \widehat H_\Lambda=H_{0,\Lambda}+\Phi_\Lambda,
 \quad \Phi_\Lambda=\sum_{b+S\subset\Lambda}\phi_b,
 \quad \phi_b=-\frac\tau3\sum_{f\in O_b}W_f,
 \quad\|\phi_b\|=M=7|\tau|.
\]

All incoming and outgoing complete stars count when they meet a region. The finite potential is bounded, so finite-volume operator/form domains are the reference domains and finite ground vectors have finite reference form energy. The homogeneous sum is not a bounded global perturbation: its absolute interaction budget grows with the number of stars.

Only I1's symbolic range is used: `|tau|<tau_*=min(c1(S),1/(2c2(S)))/7`. Its specified orthant state omega, unique ground, centered normalized generator G and spectral gap at least1/2 are inherited. No positive numerical tau is chosen. These are not J2's summable representation or AH's finite uniform-coupling model.

## Vacuum reset with the unbounded form costs retained

Fix finite R contained in Lambda, and let rho be the actual normalized finite ground density. On the full tensor product define the trace-preserving completely positive reset

\[
 \mathcal R_R(\rho)=|\Omega_{R,0}\rangle\langle\Omega_{R,0}|
                    \otimes\operatorname{Tr}_R\rho,
 \qquad\Omega_{R,0}=\bigotimes_{b\in R}\Omega_b.
\]

This is a mixed trial density, not necessarily a vector trial. Its regional reference energy is exactly zero, and its complementary reference energy equals the original one. These unbounded statements follow first for bounded positive spectral truncations of the complementary reference and then by monotone convergence. The original total reference form expectation is finite; hence the reset has finite reference form expectation and is an admissible trial for the semibounded finite-volume form. One need not assert that arbitrary reset maps preserve the full operator domain or that every individual Kraus image lies there. The chosen reset vacuum belongs to the reference kernel; replacing it by an arbitrary vector of infinite form energy would invalidate this argument.

Let `I_Lambda(R)={b:b+S subset Lambda,(b+S) intersect R nonempty}`, with cardinality n_Lambda(R). Disjoint-star and complementary reference expectations agree before and after reset. The ground variational principle for finite-energy densities and exact scalar-energy cancellation give

\[
 0\leq\operatorname{Tr}[\mathcal R_R(\rho)\widehat H_\Lambda]-E_\Lambda
 =-\operatorname{Tr}(\rho H_{0,R})
   +\sum_{b\in I_\Lambda(R)}
       \operatorname{Tr}[(\mathcal R_R(\rho)-\rho)\phi_b].
\]

Each difference costs at most `2||phi_b||<=2M`. Every incident anchor belongs to `{r-s:r in R,s in S}`, so `n_Lambda(R)<=4|R|`, including the boundary and every incoming anchor. This proves the displayed estimate for all volumes and regions, independent of the finite fixtures. No uncancelled extensive ground scalar or reference cost is suppressed.

## Tightness, normality and the actual local representation

Let `K_R=8M|R|`. Spectral calculus gives

\[
 \operatorname{Tr}(\rho_{\Lambda,R}(I-P_{R,T}))\leq K_R/T,
 \qquad
 \|\rho_{\Lambda,R}-P_{R,T}\rho_{\Lambda,R}P_{R,T}\|_1
 \leq2\sqrt{K_R/T}.
\]

For the second inequality, write the difference as `(I-P)rho+P rho(I-P)` and apply Hilbert–Schmidt factorization to each term. The bound uses positivity and trace one. The compressed density matrices live in a fixed finite-dimensional trace-norm bounded set. Uniform tails therefore make the entire local family trace-norm precompact.

I1 already supplies convergence of expectations for every bounded local operator. Any trace-norm cluster point must give that same limiting functional. Precompactness and uniqueness imply trace-norm convergence of the local densities to a positive trace-one density rho_R. Consequently omega restricted to `B(H_R)` is normal. This is a new deduction from the reset estimate and compactness, not an inference from weak-star convergence alone. It applies to every finite union of supports, not merely the selected diagnostic regions. The same energy bound passes to rho_R by bounded spectral truncation.

The represented local algebra is normal as well. For a dense vector `pi(B)Omega` with B bounded local, its positive functional on `B(H_R)` is `omega(B* A B)`, evaluated inside the larger finite factor containing both supports. That functional is normal because its density there is trace class. Approximating arbitrary vectors by these cyclic vectors gives uniform norm convergence of their vector functionals; positive normal functionals are norm closed. Thus pi restricted to each local type-I factor is normal. This stronger conclusion is not assumed for an arbitrary GNS representation.

## Gauge invariance and the required topology

On all original owned links, a finite product of endpoint SU(2) transformations acts by `U_(v,w)->g_v U_(v,w)g_w^-1`. It is a strongly continuous unitary group on the original finite link Hilbert space. Closed selected and omitted Wilson multipliers and every original Casimir are invariant; domains are preserved. Each unique finite-volume ground transforms in a continuous one-dimensional character of the complete finite endpoint product. Such a character is trivial: its Lie algebra derivative vanishes on the perfect algebra su(2), and each SU(2) factor is connected. The same argument fixes every onsite vacuum. Projector/state invariance and pointwise limiting expectations give invariance of omega under every finite gauge product.

For each g define the norm-isometric local automorphism beta_g, extended to the quasilocal norm closure, and

\[
 U_\omega(g)\pi(A)\Omega=\pi(\beta_g(A))\Omega.
\]

State invariance makes this independent of representatives and isometric; g inverse makes it unitary, and the vacuum is fixed. For A supported in R, concrete `beta_g(A)` is bounded strongly-star continuous as g varies in a finite endpoint group, even though its orbit need not be norm continuous. Local normality implies

\[
 \|\pi(\beta_g(A)-A)\Omega\|^2
 =\operatorname{Tr}\rho_R(\beta_g(A)-A)^*(\beta_g(A)-A)\longrightarrow0.
\]

Bounded strong convergence is tested by a trace-class density using finite-rank approximation. Density of bounded-local cyclic vectors then proves strong continuity on the entire GNS Hilbert space for each finite endpoint group. No point-norm continuity of conjugation on all bounded local operators is claimed.

## Compatible Haar averaging and cyclic equality

For A in a local factor on R, let V_R contain **all** endpoints of its24|R| owned links, including outgoing heads. The original weak-operator Haar average

\[
 E_R(A)=\int_{SU(2)^{V_R}}\beta_g(A)\,dg
\]

exists in that same finite-region von Neumann factor. It is a unital positive contraction, has the same site support, and is invariant under every local gauge transformation. Haar invariance gives the expectation/idempotence property. Gauge transformations outside V_R act trivially on A, so this is full local gauge invariance, not merely invariance at internal vertices.

Its compatibility with GNS is proved rather than assumed. For any bounded local B, the functional `A -> omega(B* A)` is normal on the finite factor containing both supports. It therefore passes through this bounded weak-operator integral. Testing against the dense vectors pi(B)Omega gives

\[
 \pi(E_R(A))\Omega
 =\int_{SU(2)^{V_R}}U_\omega(g)\pi(A)\Omega\,dg.
\]

The right side is a strong vector integral by the previously established continuity. This reasoning does not pass a weak operator integral through an arbitrary representation.

Define A_phys as the norm closure of the entire bounded local gauge-invariant algebra and H_cyc as its cyclic closure. Every vector in H_cyc is jointly fixed by all finite gauge products. Conversely, if psi is jointly fixed, approximate it by pi(A)Omega with A local. Averaging over V_R fixes psi and contracts the approximation error, and the identity above replaces the approximant by pi(E_R(A))Omega in H_cyc. Therefore

\[
 H_{\rm cyc}=\{\psi:U_\omega(g)\psi=\psi\text{ for every finite local }g\}.
\]

No Haar measure or continuity on an infinite global gauge product is needed. No Wilson-only algebra is substituted, and no nonzero Wilson fluctuation or strict dimension comparison is deduced here.

## Source-correct generator and closure

The primary text was checked directly: its state limit is pointwise on the full bounded local algebra, and its resolvent limit is a matrix-element limit between finite-volume excitation vectors and their GNS counterparts. The source's creation core uses `u_I in H'_I intersect D(H0,I)` and bounded rank-one operators `hat u_I=|u_I><Omega_(I,0)|`. The bounded local commutator definition and essential self-adjointness are attributed to that source, not independently reconstructed from its cluster expansions. See [Yarotsky, arXiv:math-ph/0411042v1](https://arxiv.org/html/math-ph/0411042v1), Theorems2–3 and Section2 ending.

The orthant transfer used here keeps I1's decoupled negative-site spectators. The limiting state of the extended model is the product of the orthant state and spectator reference vacua. Its GNS product representation has the orthant cyclic subspace obtained by projecting spectators to their vacuum. On the source creation core this projection kills every term exciting a negative site and leaves the positive-site creation terms. It commutes with the core generator: the negative Hamiltonian is decoupled and no positive star reaches a negative site. Both the projection and its complement preserve the source core. Commuting on an essentially self-adjoint core passes to the closure; graph-norm projection of approximants shows that the positive-site creation vectors form a core of the reducing orthant restriction. This restriction is the actual I1 orthant generator, consistently with the source's tested resolvent limit. It is not a same-Hilbert-space strong resolvent assertion about the summable model.

For a positive-site creation operator, `u_I in D(H0,I)` ensures

\[
 [H_{0},\widehat u_I]=\widehat{H_{0,I}u_I}
\]

is bounded and local. Only incident complete stars contribute to the interaction commutator, with total norm at most `2M n(I)||u_I||<=8M|I|||u_I||`. This is a finite local sum, not a bounded infinite global Hamiltonian. Endpoint gauge transformations factor over owned sites, fix onsite vacua and commute with their self-adjoint references. They preserve H'_I and D(H0,I), hence send this core to itself. Covariance of the finite commutator gives `G U_omega(g)=U_omega(g) G` there. Applying the same statement to g inverse and taking graph closures proves commutation with the actual closed G and its resolvents.

The jointly fixed space therefore reduces G. Its restriction is self-adjoint with domain `D(G) intersect H_cyc`; its form domain is `D(G^(1/2)) intersect H_cyc`. The physical GNS quotient has null left ideal `N_omega={A in A_phys:omega(A* A)=0}` and inner product `omega(A* B)`. The map `[A] -> pi(A)Omega` is an isometry onto the physical cyclic completion and identifies its centered generator with that restriction.

Physical energy is `delta G|H_cyc` and frequency is `(delta/hbar)G|H_cyc`. Thus the inherited spectral exclusion becomes `{0} union [alpha/16,infinity)` in energy and threshold `alpha/(16hbar)` in frequency. The ground remains at zero and unique. A restricted spectral inequality alone does not ensure any nonzero physical excitation. No numerical tau, mass measurement, different boundary-state limit, global infinite-volume conjugating unitary or continuum conclusion is supplied.

## Exact diagnostics and their limits

The new checker reconstructs complete tail-owned links, selected10/free14 splits, all21 omitted face words, whole-star incidences and every regional gauge endpoint for the three prescribed cuboids and regions. The interior singleton in the3x3x3 cuboid has three incoming anchors in addition to its own; an anchor-only count is rejected. Finite rational quaternion transformations check closed Wilson covariance, charged endpoints and complete support. Finite fundamental-representation Haar controls are explicitly representation-limited.

The analytic countermodels are spelled out so their finite checks are not mistaken for proofs of infinite statements:

- Normal states `<e_n,Ae_n>` on B(l2) have weak-star cluster states annihilating every finite-rank projection but taking I to1. The clusters are singular; their unbounded reference energy escapes. A finite projection test diagnoses the missing tightness premise.
- A strongly continuous diagonal circle subgroup with weights n has a bounded magnetic-index reversal whose conjugation orbit has norm distance2 at angles tending to0. Each fixed vector is strongly continuous. This subgroup occurs among the growing SU(2) Peter–Weyl representations, so strong and point-norm continuity are genuinely different assumptions.
- Weak operator averages do not pass through an arbitrary representation. On l2 of positive integers let V(t)e_n=exp(int)e_n; its original weak Haar average is0. There is a singular state f with f(V(t))=1 for every t: choose a net n tending to infinity with all finitely prescribed phases tending to1, then take a weak-star cluster of the vector states. Such n exist by simultaneous pigeonhole approximation applied to multiples of an arbitrarily large integer. In its GNS representation pi(V(t))Omega=Omega, so the vector average is Omega while pi of the original average is0. This is an abstract weak-integral diagnostic, not the actual model's gauge orbit. The local-normality proof above excludes the missing premise in the actual application.
- A bounded rank-one operator can create a vector outside D(G). For h e_n=n^2 e_n, the coefficients1/n^2 define an l2 vector whose h-image is not l2. Resetting to a vector of infinite form energy is likewise inadmissible; the actual vacuum reset avoids that problem.
- A finite positive matrix and a noncommuting projection distinguish a compression from a reducing restriction. A one-dimensional vacuum restriction also satisfies a positive spectral-exclusion statement while having no nonzero excitation.
- The actual selected reference shift, physical factor delta=alpha/8, and centered energy units are kept. The dyadic numerical gap and globally summable perturbation bound fail the current model dictionary.

All fixture and countermodel arithmetic is subordinate to the displayed proofs. No AJ2 question is selected or executed by this derivation.
