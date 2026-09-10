# C1: actual four-cube graph and the complete central Haar tensor

Executable after B2 acceptance. This follows the post-A roadmap and does not use the sparse physical theorem for a dense graph. The static conditional calculation remains separate from Hamiltonian spectral statements.

Construct the full2×2×1-cell cubical complex, with vertices x,y∈{0,1,2}, z∈{0,1}. Independently verify every signed link/face word, eighteen vertices, thirty-three links and twenty faces. Four faces are internal. The central link from(1,1,0) to(1,1,1) has incidence four. The outer-boundary-only complex has eighteen vertices, thirty-two links and sixteen faces: it omits that central link. Verify these from actual incidence; do not reuse a single-cube sphere formula for the full complex.

Place four adjoint representation factors on the four incident face insertions and integrate the central link with normalized SU(2) Haar. In the real spin-one representation this is P=∫R(U)^⊗4 dU on an81-dimensional tensor space. The proposed invariant basis consists of B₁=δ_abδ_cd, B₂=δ_acδ_bd, B₃=δ_adδ_bc. Rebuild its Gram matrix (diagonal9, offdiagonal3), inverse (diagonal2/15, offdiagonal−1/30), and P=B G⁻¹ Bᵀ. Prove the invariant dimension is three, with intermediate pair spins0,1,2, rather than merely checking three independent vectors.

Independently compare the full tensor with quaternion/S³ Haar integration or another nonshared construction. Check self-adjointness, idempotence, trace/rank, group invariance, and a decisive failure when the offdiagonal coefficients or channels are dropped. A positive scalar or rank count does not replace the tensor.

The boundary test must be realizable on the actual three-edge paths surrounding the central link. Reorient whole face words if needed so their real SU(2) characters contain U H_i; do not change only one dagger. At zero central coupling, contract a noncommuting set of H_i and show a channel-sensitive difference from an invalid shortcut. The tetrahedral choice in `candidate-c2.md` is an optional zero-coupling probe for selecting C2. Normalized adjoint insertions useχ₂/3, so their fourfold product has normalization3⁴.

This is the central conditional Haar tensor and an actual boundary fixture, not the fully integrated twenty-face bulk amplitude. C2's nonzero-coupling calculation remains unexecuted until C1 is accepted; its observable, boundary data, error target and precision cap will be selected using the actual C1 result.
