# G1 forward: fixed-time literal-box dynamics without false norm continuity

Return to the actual A1/A2 lattice Hamiltonian and its complete-reference-factor
representation. The F diffusion coefficient c is absent. α and E_star are
fixed positive energies, hbar has action units, t is physical time, and the
spacing is fixed. Here τ may be any fixed finite real number: the dynamical
construction uses bounded summability, not the earlier smallness needed for
ground isolation.

Let A_loc be the norm closure of all bounded operators on finitely many
complete reference factors, embedded by exterior identities. A literal finite
box operator is embedded canonically as an operator on its original links,
then on the finitely many complete factors touching those links. This defines
its local-algebra meaning without selecting an exterior boundary ground vector.

## Domain-safe bounded-difference dynamics

For self-adjoint K and H=K+W with bounded self-adjoint W, both operators have
the same operator domain. Differentiate the product of the two unitary groups
on this common domain and integrate strongly; extension by density gives

\[
e^{-itH/\hbar}-e^{-itK/\hbar}
=-\frac{i}{\hbar}\int_0^t
e^{-i(t-s)H/\hbar}W e^{-isK/\hbar}\,ds.
\]

The integral is a strong-operator integral with a uniform norm bound; no
operator-norm derivative of the unbounded generator is assumed. Thus

\[
\|e^{-itH/\hbar}-e^{-itK/\hbar}\|
\le |t|\|W\|/\hbar,
\]

and for `α_t^H(A)=e^(itH/hbar)Ae^(−itH/hbar)`,

\[
\|\alpha_t^H(A)-\alpha_t^K(A)\|
\le2\|A\||t|\|W\|/\hbar.
\]

These hold for positive and negative times and require no spectral gap.

## Central completion and every boundary phase

Fix the D1 interior perturbation V_M and complete its support together with
the support of A. E2 proves that, beyond a finite geometric margin, this
central factor set is identical in each literal rectangular box and in the
infinite product. The reference and V_M then split into the same central
Hamiltonian K_J plus a disjoint exterior reference. Every exterior term
commutes with A and its central evolution, so the truncated finite and
infinite evolutions are exactly the same local operator.

Apply Duhamel once in the finite box, where
`||V_box−V_M||≤ε_M`, and once in the infinite product, where
`||V−V_M||≤ε_M`, with `ε_M=α|τ|t_M`. The two comparisons each stay
on their own single Hilbert space; the common central observable identifies
the resulting local operators. Therefore uniformly in all sufficiently large
box boundary phases,

\[
\|\alpha_t^{box}(A)-\alpha_t^H(A)\|
\le4\|A\||t|\epsilon_M/\hbar\longrightarrow0.
\]

The convergence is uniform on any fixed compact time interval by the same
bound. Component energy subtractions affect neither side: the scalar phases
`exp(±it c_box/hbar)` cancel exactly in conjugation. Absolute unitary or
ground-energy comparisons would not permit that cancellation.

For each fixed t, the infinite evolution of local A is a norm limit of
central finite-factor operators, hence is in A_loc. Isometry extends this
invariance to its norm closure. The actual H-conjugations preserve products
and adjoints, satisfy the group law and have inverses at −t. They consequently
give a group of automorphisms of A_loc. Their Hilbert-space implementing
unitaries are strongly continuous by self-adjointness of H.

## Why this does not imply a point-norm continuous C*-flow

On one actual free z-link, let χ_n be the normalized SU2 character with
Casimir energy `E_n=αn(n+2)/4`. The bounded unilateral shift B sends
χ_n to χ_(n+1) on the closed character subspace and is zero on its
orthogonal complement. Its norm is one. Under the free dynamics,

\[
\alpha_t(B)\chi_n
=e^{it\alpha(2n+3)/(4\hbar)}\chi_{n+1}.
\]

Take `t_n=4πhbar/[α(2n+3)]`. Then t_n tends to zero but the displayed
phase is −1, giving `||α_(t_n)(B)−B||=2` exactly. The checker executes
the rational phase multipliers rather than a floating approximation to π.
This is an actual local bounded operator of the lattice model at τ=0.
Even adding the bounded summable V changes this discrepancy by at most
`2|t_n|β/hbar`, which tends to zero, so strong unitary continuity does not
repair point-norm continuity on the full stated algebra.

Controls retain this distinction and reject a missing hbar, substituting the
unmatched F coefficient c for α, omitting A's central factor, and treating an
uncanceled scalar phase as an observable effect. The exact ledger uses both
time signs and the previously accepted eight geometric phases. This is a
fixed-spacing summable lattice result, without a finite propagation-speed,
relativistic, homogeneous or continuum claim.
