# Independent A1: a bridge between dressed end blocks

The calculation concerns a finite SU(2) rotor Hamiltonian on a three-square strip. It does not approximate the dressed reference ground numerically, repeat clusters or prove a homogeneous dense-family gap. All ten electric links are retained. The three xy squares have anchors x=0,1,2 at y=z=0, giving eight vertices, ten links and three faces. Every signed face word is independently reconstructed and checked.

Write x_p=Tr(U_p)/2 and

\[
H_s=\alpha\sum_{e=1}^{10}C_e-\lambda_Lx_L-\lambda_Rx_R,
\qquad H=H_s-\mu x_m,\qquad\alpha>0.
\]

The end plaquettes have disjoint four-link supports. The middle plaquette shares one link with each and has two horizontal links outside both supports. If an end coefficient is zero, its term is absent from the active reference support, so even more middle links can remain free. All-zero end support is a valid reference exception, not missing input.

## Full operator and reference ground

The full reference Hilbert space is L²(SU(2)¹⁰) with normalized Haar measure, before imposing Gauss law. It factors by its actual link partition into two four-link blocks and two free-link factors. The link Casimirs form a positive elliptic Laplacian on a compact manifold, with compact resolvent. The plaquette multipliers are real, bounded and smooth. Bounded self-adjoint perturbation preserves the operator domain and the quadratic form domain; the perturbed operators remain bounded below with compact resolvent. No truncation of a link representation or Sobolev domain is made.

Put ρ=max(|λ_L|,|λ_R|)/α<3/4. The accepted one-block argument gives a unique end-block ground and a gap at least 3α/4−|λ_p|. The constant free-link grounds are unique and have unprojected gap 3α/4. Hence H_s has a unique full-space product ground Ψ_s, some energy E_s, and

\[
g_s=E_1(H_s)-E_s\ge\alpha(3/4-\rho)>0.
\]

E_s and the dressed end-block wavefunctions need not be known. The 3α/4 scale is an unprojected link-space bound; substituting the physical isolated-loop scale 3α here would be invalid. The physical Hilbert space is not claimed to factor.

## Haar identity for arbitrary dressed end functions

Choose either untouched middle horizontal link U. Its factor in Ψ_s is the normalized constant function. With every other link fixed, the actual middle holonomy has the form A U^ε B, ε=±1, with A,B fixed unit quaternions. Thus x_m is a real linear function c·q of the four quaternion coordinates q of U. Left/right multiplication by unit quaternions and quaternion inversion are orthogonal maps of R⁴, so |c|²=1.

The independent code proves the two multiplication norm identities as exact symbolic quadratic polynomials: L(a)ᵀL(a)=R(a)ᵀR(a)=|a|²I. It also reconstructs c from the actual signed graph for noncommuting rational quaternion assignments. These latter fixtures check the connection to the graph; they do not replace the arbitrary-A,B identity.

Normalized Haar on SU(2) is uniform measure on S³. Reflection symmetry gives E q_i=0 and E q_iq_j=0 for i≠j. Coordinate symmetry and Σq_i²=1 give E q_i²=1/4. Therefore, pointwise in all other link variables,

\[
\int x_m\,dU=0,\qquad\int x_m^2\,dU=1/4.
\]

The reference density is independent of this U. Fubini/Tonelli and normalization of the arbitrary remaining dressed factors give

\[
\langle\Psi_s,x_m\Psi_s\rangle=0,
\qquad\|x_m\Psi_s\|=1/2.
\]

No bare-vacuum substitution or finite proxy for Ψ_s is used. For P_s=|Ψ_s⟩⟨Ψ_s| and Q_s=1−P_s, these equalities imply P_sx_mP_s=0 and \(\|Q_s(-\mu x_m)P_s\|=|\mu|/2\).

## Spectral transfer and Gauss restriction

Multiplication by −μx_m has norm at most |μ|. Min–max gives E₁(H)≥E_s+g_s−|μ|, while the actual reference-state Rayleigh quotient gives E₀(H)≤E_s because its bridge expectation vanishes. Consequently

\[
\Delta_{full}(H)\ge\alpha(3/4-\rho)-|\mu|.
\]

If the displayed lower bound is positive, E₁(H)>E₀(H) and the full ground is unique. H commutes with the continuous SU(2) action at all eight vertices: face traces are gauge invariant and link Casimirs commute with left/right translations. Its one-dimensional ground eigenspace therefore carries a continuous character of SU(2)⁸. Such a character is trivial, since its differential annihilates the perfect Lie algebra su(2)⁸ and the group is connected. The unique full ground is therefore gauge invariant. The closed Gauss subspace reduces H, contains that ground and cannot introduce an excitation below the full-space threshold. The same lower bound holds physically, without factorizing the physical Hilbert space.

For |λ_L|,|λ_R|≤α/2 and |μ|≤α/8,

\[
\Delta_{physical}\ge\alpha/8.
\]

A declared common α≥α_min>0 turns this into α_min/8 in common physical energy units. This is a parameter-family statement for the finite cluster; no volume repetition is executed in A1.

## Boundaries, fallback and a counterexample

At ρ=1/2, μ=0 recovers the reference lower bound α/4. Either sign of μ=α/8 gives the sharp α/8 bound while the generic two-norm estimate gives zero. At |μ|=α/4 the sharp sufficient bound is zero; beyond it the bound can be negative. Such cases remain explicitly insufficient. They do not demonstrate gap closure or nonuniqueness of the actual model.

Without a proved zero reference expectation, the general bounded-perturbation estimate is g_s−2|μ|. A two-dimensional counterexample prevents replacing it by g_s−|μ|: take H_s=diag(0,1) and V=diag(1/4,−1/4). The true perturbed eigenvalues are 1/4 and 3/4, so the true gap is 1/2, exactly the two-norm estimate; the unsupported one-norm estimate would be 3/4. The reference expectation of V is 1/4. This is a counterexample to the generic inference, not an asserted SU(2) cluster spectrum.

The actual support control includes the middle interaction in the reference inventory. Every middle link is then touched, and the sharpened Haar gate correctly blocks instead of producing a zero diagnostic. One cannot retain the old two-end reference gap for that changed reference without a new argument. The generic bounded-perturbation lemma is separate and requires whatever reference gap has actually been proved.

## Executed checks and limits

The standalone verifier checks the complete graph, symbolic quaternion norm identities, conditional moments on the signed words, noncommuting gauge transformations, eleven frozen parameter fixtures, signed/zero couplings, two nonunit energy scales, physical floors and malformed input/support controls. The exact 2×2 counterexample and all insufficient margins are retained. The quaternion fixtures illustrate an identity already proved for arbitrary dressed factors; they are not samples claimed to certify an unknown ground state.

Source review and producer comparison are separate from this independent derivation. A2 requires a new advisor decision. Dense overlap estimates, an applicable rotor stability theorem and the relevant uniform smallness conditions remain unresolved by this finite cluster calculation.

The final standalone run has 33 named checks. A separate complete comparison has 27 checks, reconstructing the author's entire signed graph, all eleven certificates and their exact parameter bindings, nine signed bridge scan rows, the blocked unused-link record and the generic counterexample. It independently recomputes the conditional moments and spectral bounds without importing an author module. The author's unequal signed-end fixture uses (−1/2,1/4), complementing our (−1/2,1/2) fixture; both are explicitly bound and give the same maximum-ratio estimate. Ordinary and optimized Python produce byte-identical scientific and comparison outputs. Counts describe separate checks, not independent proofs of every sentence.

The full author bridge implementation, its fixture/check driver and written proof were reviewed at function and file scope. No new material defect was found. Held-out comparison controls reject changed source digests, omitted scale fixtures, a fabricated dressed-ground calculation claim, a missing moment replaced by zero, unproved endpoint physical inclusion, a changed common physical floor, Boolean word-sign aliases, a relabelled signed coefficient and forged caller pass metadata. These are deliberate rejection tests, not newly discovered historical code failures. Source and output hashes are bound in the phase manifest.
