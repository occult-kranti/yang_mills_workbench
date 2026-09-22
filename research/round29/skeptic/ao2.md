# AO2 independent skeptical review

**Decision: accept the actual first-moment equality and Wilson operator-domain result for the inherited state; no blocking issue.** Both reports were frozen before review. The conclusion is

`chi in D(H_phys)`, `||H_phys chi||² <= alpha²(36+28|tau|)`, and `〈chi,H_phys chi〉=alpha omega(1−W²)`.

Both original coupling restrictions, the actual I1/AJ1/AK2 orthant representation, complete physical cover and fixed scales remain attached. No new AQ-state identity or second-moment equality is admitted.

AK2 Section 4 supplies convergence of nonreal resolvent tests, its Stone–Weierstrass passage to C0 tests and the correction for moving finite means. The argument therefore starts with the actual limiting spectral measure; it does not postulate common-Hilbert-space strong-resolvent convergence. AO1 supplies the new uniform finite second-moment ceiling B2.

A technical clarification preserves the frozen reverse report: its f_R and g_R formulas are defined on the nonnegative spectral half-line. Extend them by zero on E<0 to obtain the C0(R) functions used in the source-qualified passage. Their factors E and E² make these extensions continuous at zero. The forward report already states this convention explicitly. This is a harmless domain specification, not a changed estimate.

These nonnegative compact tests increase to E and E². Passing the E² tests and then using monotone convergence gives the actual limiting second-moment upper bound. The tail inequality `integral_(E>R) E dnu_Lambda <= B2/R` is uniform integrability of the first moment, with energy units. At fixed R, the finite first moments also converge to the bounded-local expression alpha omega(1−W²). Passing the truncated equality and then R to infinity identifies that expression with the actual limiting first moment. All limit orders and remainder controls are explicit.

The spectral theorem converts finite integral E² dnu directly into membership of chi in D(H_phys) and the claimed norm bound. This is stronger than AK2's earlier form-domain conclusion, while requiring no informal differentiated correlation. Bounded second moments do not ensure convergence of second moments. Both reports preserve this limitation with valid escaping-second-moment countermeasures. Their different atom locations are immaterial.

`ao2_check.py` independently checks compact-test zero extension and monotonicity, uniform first-tail bounds and a bounded-second-moment family that loses a unit of second moment in the weak limit. It makes 33 exact checks and replays both producers normally and with optimization; all four result files match. Centering removes a zero-energy atom and changes total spectral mass; it need not change positive moments. Ground-energy shifts and physical rescalings have different effects and remain correctly separated.

**AQ1 advice:** start a separate numerical-cap centered-box construction. Reprove local reset bounds and compactness in that geometry, then use the source-qualified finite-range dynamics theorem with unbounded onsite terms. Local normality must establish strong continuity of the GNS unitary group; norm convergence as volume grows does not imply norm continuity in time on all B(H) observables. Nonnegative energy and later physical gap transfer require bounded spectral-test arguments on the complete local algebra. None of the old-state identifications may be imported at all numerical couplings without its original hypotheses.

## Pre-admission evidence-label repair

The strict admission gate rejected two duplicated forward check identifiers: at n=2, the diagnostic cutoffs 1 and n/2 coincide. The producer preserved its original frozen tree and changed only labels to include the cutoff index. I inspected the source diff, verified that every results field except the label list is unchanged, and confirmed all 67 current labels are unique. The scientific derivation and verdict are unchanged. The initial reviewer files and four replay outputs are preserved in `history/ao2-review-before-label-repair/`. Fresh execution of the unchanged independent reviewer checker again passes all 33 checks and both normal/optimized producer replays. This is an administrative repair, not another research investigation.
