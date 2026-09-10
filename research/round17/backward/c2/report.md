# Independent C2: one action vector does not determine the joint observable

This sixth scientific loop retains C1's actual four-cube graph and signed boundary paths. It compares two fixed boundaries in a normalized conditional integral over the central link alone. It does not integrate the surrounding links or infer a Hamiltonian gap.

For unit quaternion q and boundary Hᵢ, write xᵢ(q)=Tr(qHᵢ)/2=q·aᵢ, where aᵢ=(Hᵢ₀,−Hᵢ,vec). The action is q·b, b=Σᵢκᵢaᵢ. This is a derived action variable, not an additional physical field. An orthogonal rotation may simplify b but must also rotate every observable direction. The implemented exact domain is scalar-axis b or b=0; other directions raise an explicit unsupported-domain error rather than receiving a silent rotation.

The tetrahedral boundary T is the four accepted Hadamard unit quaternions. The commuting boundary C is (I,I,i,−i). Both are realized on the same actual four three-edge paths by the C1 link-assignment construction. With every κᵢ=κ, both give b=(2κ,0,0,0) and the identical partition

\[
Z(\kappa)=\mathbb E_{S^3}\exp(2\kappa q_0).
\]

The common functional is O=∏ᵢ(4xᵢ²−1)/81, evaluated on different boundaries. The central-link integrands are therefore different functions despite their equal actions. C gives (4q₀²−1)²(4q₁²−1)²/81≥0. T has orthogonal direction vectors, whereas C has repeated and opposite directions. This relative-direction information is not encoded by b.

## Independent angular and scalar integrations

The verifier does not import the producer's four-dimensional sphere-moment oracle. Put q=(t,√(1−t²)n), with n uniform on S² and independent of t. The scalar density is the normalized semicircle density 2√(1−t²)/π on [−1,1]. For spatial exponents 2kⱼ,

\[
\mathbb E_{S^2}\prod_{j=1}^3n_j^{2k_j}
=\frac{\prod_j(2k_j-1)!!}{3\cdot5\cdots(2K+1)},\qquad K=\sum k_j.
\]

Odd spatial powers vanish. Each four-variable monomial becomes a scalar polynomial tᵖ(1−t²)ᴷ times this angular moment. Expanding the latter factor exactly produces radial polynomials f_T and f_C. Scalar moments then follow from

\[
\mathbb E t^{2m}=\frac{C_m}{4^m},\qquad
C_m=\frac1{m+1}\binom{2m}{m},\qquad \mathbb E t^{2m+1}=0.
\]

The resulting normalized observable polynomials are

\[
f_T(t)=\frac{1024t^8-2752t^6+2448t^4-736t^2+16}{8505},
\]
\[
f_C(t)=\frac{768t^8-1280t^6+864t^4-240t^2+23}{1215}.
\]

For T, each individual normalized adjoint insertion reduces to the identically zero radial polynomial. Equivalently its conditional square mean is t²/4+(1−t²)/4=1/4. Thus all four individual means vanish for every scalar-axis action, while their joint need not vanish. This is an exact symmetry calculation, not a missing-value placeholder.

At κ=0 the scalar integration gives E[O_T]=−1/405, E[O_C]=13/1215 and contrast C−T=16/1215. These anchor the independent implementation to C1 and to an additional commuting-boundary calculation.

## Complete truncation enclosures

Let M=|2κ| and expand exp(2κt) to degree N. The exact rational coefficients are

\[
A_{X,n}=\frac{(2\kappa)^n}{n!}\mathbb E[t^n f_X(t)],\qquad
Z_n=\frac{(2\kappa)^n}{n!}\mathbb E[t^n].
\]

If M<N+2, a uniform bound on the omitted exponential terms is

\[
R_N=\frac{M^{N+1}}{(N+1)!}\frac1{1-M/(N+2)}.
\]

Every normalized adjoint insertion lies in [−1/3,1], so |O_X|≤1. Each numerator and Z have absolute remainder at most R_N; the contrast numerator has remainder at most 2R_N. Jensen's inequality and the zero Haar mean of q·b give Z≥1. The denominator interval therefore has lower endpoint max(1,Z_N−R_N). All four corners of signed numerator/positive-denominator interval division are considered. The contrast uses its numerator difference and the same denominator, not an equality of two approximate partition values.

The fixed degree sequence is 0,4,8,12,16 at κ=1/8. Degrees 0,4,8 are retained as insufficient for the requested 10⁻¹² width. Degree 8 already establishes a positive contrast but still has width about 4.3075×10⁻¹¹. Degrees 12 and 16 meet the target. At degree 16,

\[
E[O_T]\approx-0.002469114394235138,\quad
E[O_C]\approx0.01073813525633129,
\]
\[
E[O_C]-E[O_T]\approx0.013207249650566428,
\]

with a rigorous contrast enclosure width about 6.6301×10⁻²⁵. Exact fractions in the evidence files are authoritative. These are quadrature-free rational enclosures of a finite conditional integral, not floating-point simulations or a continuum result.

## Exceptions and validation boundaries

Zero and negative common couplings and κ=1/16 are evaluated explicitly. Negative common coupling gives the same even-observable expectation and enclosure. Boundary C with coefficients (1/8,−1/8,1/8,1/8) has nonzero individual coefficients but exactly b=0; it uses the original Haar branch with tail zero and Z=1, with no normalization by |b|. The all-zero case agrees. Input validation precedes every cached angular or scalar moment, including warm Boolean aliases, negative indices, malformed tuples and nonunit boundary data.

The other sixteen face terms do not contain the central link. At fixed surrounding links they multiply numerator and denominator by the same positive constant and cancel from this conditional expectation. They still affect the distribution of surrounding links in the full bulk theory. The action variable b and the Hamiltonian energy scale α have distinct roles and are not equated here.

The wrong action-only closure is decisively contradicted: T and C have the same b and Z but different exact numerator coefficients and a strictly positive contrast. This does not rule out using b together with the full observable-direction data. The accepted result is an obstruction to discarding that data, not a closure of the dense volume-uniform or continuum Yang–Mills problem.

The focused helper review found an input-validation omission in the independent `scalar_coefficients` helper: although the main `data` entry point already validated the degree, directly calling the helper with `False` silently meant degree zero, and degree −1 returned an empty coefficient array. The actual accepted inputs, initial source and initial 34-check report are retained under `history/`. The helper now checks an exact integer degree in 0..16 and a Fraction action coefficient before any iteration. Two direct helper controls supplement the original entry-point tests. This correction does not change the scientific coefficient arrays or enclosures. A corresponding unchecked scalar-index issue was also reported to the forward author for its separate source review; producer failure evidence is owned by that implementation.

The corrected independent suite passes **36 named checks**, with a separate **22-check complete producer comparison**. Normal and optimized Python outputs are byte-identical and are counted once. The producer independently reproduced its direct `integrate` helper's Boolean/negative-index acceptance, retained the old source and observations, and added strict scalar-index and polynomial validation before arithmetic. Both corrected algorithms agree exactly on all five complete refinement records, all seven additional producer fixtures, boundary assignments, observable polynomials, coefficient arrays, common partition and full numerator/denominator remainders. No material scientific discrepancy remains.

The focused source review covered the S³ versus S²/semicircle arithmetic, exact parameter and cache boundaries, helper validation, actual path realizations, geometric tail condition, signed division, source guards, complete fixed fixture inventory and the retained action-only cache counterexample. It does not claim a new whole-repository audit. Run `python check.py --output ../c2-reproduced` from this source folder. For the separate comparison run `python compare.py --producer <forward-c2-source> --evidence <forward-c2-output> --output ../c2-comparison-reproduced`. Output destinations must be new directories outside the frozen source folder. The next authorized work is integration review, not another scientific experiment.
