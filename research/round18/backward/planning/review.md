# Round18 independent planning review

Status: planning only. No Round18 scientific code, simulation, experiment or acceptance gate has been executed. This review uses the accepted Round17 roadmap and the six-loop lattice contract. The advisor still selects each second loop after its first loop is independently accepted.

## Goal A1: a genuine three-face bridge

Use three coplanar consecutive xy squares with x-anchors 0,1,2 and common y-anchor 0. Their minimal support graph has eight vertices, ten links and three faces. The two end squares have disjoint four-link supports; the middle square shares one vertical link with each end and has two horizontal links absent from both. An embedding must retain all original electric links and give every omitted magnetic coefficient an explicit zero value.

On the full unprojected link Hilbert space, let H_ref contain the two end interactions and all electric terms. With α>0 and |λ_L|,|λ_R|≤αρ, ρ<3/4, the accepted four-link result gives a unique reference ground Ω_ref and gap δ₀≥α(3/4−ρ). The two untouched bridge links are exact constant Haar factors of that ground, even though the end-block grounds are dressed and need not be computed.

Conditioning on every other link and integrating one untouched link gives

\[
\langle\Omega_{ref},x_m\Omega_{ref}\rangle=0,
\qquad \|x_m\Omega_{ref}\|^2=1/4.
\]

Thus, for P_ref=|Ω_ref⟩⟨Ω_ref|, P_ref x_m P_ref=0 and \(\|(1-P_{ref})x_mP_{ref}\|=1/2\). Parity alone would not establish the second identity; normalized Haar integration of the squared trace is needed. These are statements about the actual dressed reference state, not the original free vacuum.

Adding V=−μx_m has norm at most |μ|. The min–max bound and the reference-state trial yield

\[
E_1(H)\ge E_0(H_{ref})+\delta_0-|\mu|,
\quad E_0(H)\le E_0(H_{ref}),
\quad\Delta(H)\ge\alpha(3/4-\rho)-|\mu|.
\]

The generic bound δ₀−2|μ| remains a valid fallback when the zero reference expectation is unproved. The sharper term must not be transplanted to a bridge with no untouched reference-Haar link.

The compact-group Laplacian has compact resolvent; real bounded plaquette multiplication preserves self-adjointness on its operator domain and its form domain. A strictly positive displayed gap proves uniqueness of the full cluster ground. The Hamiltonian commutes with the full vertex SU(2) action; the unique ground transforms by a continuous character, and SU(2)^V has no nontrivial such characters. Therefore the full ground is gauge invariant. Only then may one restrict to the Gauss subspace, which retains that ground and cannot lower its excitation threshold. No factorization of the physical Hilbert space is asserted. The unprojected reference scale is 3α/4, not the physical isolated-loop scale 3α.

**Proposed frozen acceptance:** ρ≤1/2 and |μ|/α≤1/8 give Δ≥α/8. With ρ=1/2, |μ|/α=1/4 is a valid zero sufficient bound, not evidence of gap closure. Verify the full bridge graph and signed words; both untouched links; both conditional Haar identities; zero/signed end couplings and bridge; α scaling; zero bridge; and the threshold endpoint. A negative control must add an active interaction touching the supposedly free link and reject the *sharpened argument*, while retaining any valid generic estimate. For the selected nonzero bridge the generic estimate reaches zero while the sharper one stays positive, so the fixture discriminates the improvement.

## Candidate A2, not preauthorized

Repeat entire ten-link clusters with pairwise disjoint link supports, permitting shared vertices only where no edge is shared. One possible coordinate mask uses xy strips anchored at x=4i,y=2j on each z layer, with three consecutive x-faces per strip. In an n-vertex open box the proposed count is n floor(n/4) floor(n/2); it requires a separate all-n incidence proof before use. The full-space tensor decomposition, unique cluster grounds and gauge-invariance argument could then give the uniform finite-family bound α_min(3/4−ρ−σ), where σ bounds |μ|/α and α_N≥α_min>0.

The advisor's further candidate is a remaining-face perturbation with a volume-independent absolutely summable energy budget Σ|ν_f|≤β. The generic extension is Δ≥δ_cluster−2β. It can have nonzero coefficients on every remaining face, but it is a decaying inhomogeneous family, not the homogeneous dense Yang–Mills family. A sharper −β term would require an additional actual-mask proof that every remaining face has an untouched reference-Haar link. Neither a favorable finite-cluster spectrum nor a total norm growing with volume supplies the original dense stability theorem. Applicable rotor stability, uniform smallness, domains and common units remain separate missing premises.

## Goal B: complete physical complement before spectral improvement

For the original dense two-cube graph, P spanning Ω and all eleven fundamental face characters reduces H₀. The candidate exact complement threshold is QH₀Q≥(9α/2)Q. To prove it, every active spin-network link contributes at least 3α/4. Energy below 9α/2 therefore permits at most five active edges. Gauss law excludes degree-one support; bipartiteness excludes odd cycles. On this graph the only possible nonempty support of that size is a four-cycle. Its degree-two intertwiners force a common spin around the loop; only spin1/2 has energy below 9α/2. Every actual four-cycle must be checked to be one of the eleven included faces. An actual six-edge fundamental loop attains 9α/2 and prevents an unjustified larger complement threshold. Adding the shared adjoint trial at energy8α does not eliminate this six-edge channel.

The proposed cross-block Gram W*W, W=QVP, has a zero vacuum row/column and face entries

\[
(W^*W)_{pp}=\tfrac14\sum_f\lambda_f^2,
\qquad(W^*W)_{ps}=\lambda_p\lambda_s/4\quad(p\ne s).
\]

This preliminary derivation requires every repeated fourth moment: single-face fourth moment1/8, two-face squared moment1/16 by exclusive-link integration, and no four-distinct-face closed mod-two surface on the actual graph. The last claim is a graph obligation, not an arbitrary-factorization assumption. At common λ=αr the face matrix is α²r²(10I+J)/4 and its norm is21α²r²/4.

If those premises pass, QHQ/α≥cQ with c=9/2−11r. On the codimension-one subspace orthogonal to Ω, a scalar block bound suggests

\[
E_1/\alpha\ge\frac{3+c-\sqrt{(3-c)^2+21r^2}}2.
\]

Using c≥3/8 and the cross-norm maximum throughout 0≤r≤3/8 would give the planned constant (27−3√70)/16>0. Combine a *full* E₁ lower bound with an actual Rayleigh E₀ upper bound; do not promote a Ritz gap. Exact cross-Gram positivity, the full complement proof and radical enclosure/sign controls are necessary before this is an accepted result. B remains unexecuted until the post-A decision.

## Goal C: valid joint Gram data and one real surrounding variable

For the declared dot-product integrands, equal joint Gram matrices of b,a₁,…,a₄ suggest a conventional isometry-of-spans proof: equality of Gram matrices makes the map well-defined even with linear dependence, and it extends to an orthogonal map of R⁴ preserving normalized S³ measure. Admission requires positive semidefiniteness, rank≤4, unit aᵢ and the exact relation b=Σκᵢaᵢ. Rank-deficient and b=0 cases need no inverse of a singular Gram matrix. This coordinate statement does not transform the surrounding link measure or cover unspecified orientation-sensitive insertions.

For a nontrivial next surrounding integration, the path link (1,0,0)→(1,0,1) belongs to one central incident face and two other faces. Integrating it together with the central link affects six distinct face weights; fourteen are constant under those two variables. All six weights and the induced joint observable must remain. Once this link varies, b(V) is generally off the scalar axis: the old restricted C2 routine cannot simply be reused. The new computation needs a valid general joint-Gram reduction or a direct two-link integral with complete numerator and partition errors. This is a conditional two-link milestone, not a twenty-face bulk result.
