# Candidate only: tetrahedral conditional boundary

This is an unexecuted candidate for selection after C1, not an accepted result.

The general candidate common variable is the four-component sum b=Σκ_i a_i, where x_i(U)=q·a_i in unit-quaternion coordinates. The conditional action is q·b. For b≠0, a Haar-preserving rotation aligns b with the scalar axis; the individual observable directions a_i must rotate with it. For b=0 the central action is constant and the correct branch is the original Haar integral, with no division by‖b‖. This change of coordinates cannot erase the relative directions needed by a joint observable. It supplies a conditional integration simplification, not a spectral or continuum closure.

On the central link of the four-cube complex, orient the four incident face characters as x_i(U)=Tr(UH_i)/2. Select unit quaternions

H₁=(1,1,1,1)/2, H₂=(1,1,−1,−1)/2,
H₃=(1,−1,1,−1)/2, H₄=(1,−1,−1,1)/2.

They are individually noncommuting boundary holonomies. Their vector parts sum to zero. For U=(q₀,q⃗), the equal-coefficient central action becomes Σκx_i(U)=2κq₀. All four incident coefficients can remain nonzero, for example κ=1/8. The surrounding three-edge paths must actually realize the four specified H_i on the signed graph. The other sixteen face terms of a full action are constant under the central conditional integral and cancel from its normalized expectation; their effect on the surrounding marginal remains necessary for the bulk calculation.

A channel-sensitive bounded observable is O=∏ᵢχ₂(UH_i)/3⁴, with χ₂=4x²−1. Compare its complete central expectation to the product of four individual normalized adjoint expectations. Under the central class weight exp(2κq₀), the tentative symmetry calculation gives each individual mean zero: H_i has scalar component1/2, and rotational symmetry implies E[4(q·a_i)²−1]=E[q₀²+q⃗²]−1=0. A nonzero joint expectation would therefore be an exact obstruction to an independent-channel shortcut.

The proposed verification uses the rank-three Haar projector atκ=0, exact polynomial moments on S³ for a finite Taylor expansion, and a complete numerator/partition remainder. The independent implementation should use a different representation or conditional radial integration. An arbitrary degree cap is not success; insufficient width/sign must be retained. The numerical value, sign, nonzero channel contrast, finite-action precision and realizability have not been checked in this candidate note.

## Additional candidate selected for scrutiny, still unexecuted

A matched common-variable control could use commuting boundary quaternions (1,0,0,0), (1,0,0,0), (0,1,0,0), (0,−1,0,0). Their sum is also(2,0,0,0). Thus the equal-κ conditional action and normalization agree exactly with the tetrahedral case, while the same four-face adjoint functional has a different boundary-dependent integrand. In the commuting case it is (4q₀²−1)²(4q₁²−1)²/81≥0. The tentative Haar values are13/1215 for this case and−1/405 for the tetrahedral case, giving contrast16/1215. These are hypotheses awaiting independent checks, not accepted numbers.

If verified, C2 can compare both expectations atκ=1/8 with one common exact normalization and a complete rational remainder. This directly tests whether the common action vector b alone can replace the boundary tensor: it cannot do so if the joint observable differs at fixed b. A result cache keyed only by b would be invalid for such observables. The correct reduced variables must retain the required relative boundary directions or equivalent tensor data. This matched contrast would be stronger than comparing two unrelated actions; the surrounding bulk integral would still remain open.
