# Loop 2 independent review and backward handoff

**Acceptance:** all 23 finite Euclidean covariance certificates replay through an independent exact character oracle. The selected all-nonzero triple (k1,k2,eta)=(1,1,1/4) has strictly positive covariance. The degree-24 enclosure has width approximately 1.1072984240×10^(-16), smaller than the requested 10^(-12). Exact rational endpoints, rather than these rounded displays, are the proof evidence.

This loop follows the advisor's frozen acceptance of loop 1. No loop-1 source, output or narrative was rewritten. The owned `loop1_manifest.json` still binds those files.

## 1. What the feedback changed

The initial local sign argument at k1=k2=1 used a rigorous baseline variance interval and the improved fourth-cumulant bound7. It certifies the sign at eta=±1/1024. At eta=1/4 its interval is approximately [−0.20646,0.23104], which is inconclusive. That interval is correct; it does not claim the covariance vanishes.

The second loop therefore changed the method of estimation while retaining the exact same finite action, measure and observable. Instead of truncating the coupling response at first order, the forward member integrated a polynomial approximation to exp(k1 x+k2 y+eta z) and enclosed its full remainder. The backward member rebuilt every coefficient using the independently derived SU(2) character formula. The two representations agree exactly.

| Taylor degree | Status for (1,1,1/4) | Covariance enclosure width, rounded display |
|---|---|---:|
| 4 | Inconclusive | 4.8656040522 |
| 8 | Strictly positive | 0.0129310726 |
| 12 | Strictly positive | 1.7832829634×10^(-5) |
| 16 | Strictly positive | 7.6747442749×10^(-9) |
| 24 | Strictly positive; requested accuracy passed | 1.1072984240×10^(-16) |
| 32 | Strictly positive; further exact refinement | 1.2708967584×10^(-25) |

The degree-24 endpoint displays are approximately 0.012037131325864906 and 0.012037131325865015. Ordinary floating displays of the degree-32 endpoints coincide, even though the exact rational interval has positive width. The website must use the stored exact width, not subtract rounded endpoint displays. The degree-4 interval exceeds the elementary physical covariance range; it remains a valid, loose enclosure and must not be described as measured covariance outside that range.

## 2. Independent certificate review

`verify_certificate.py` implements `verify(certificate, producer_source_sha256=...)`. It imports no producer mathematics or interval routines. Its source-pinned dependency is the unchanged loop-1 character oracle. It independently computes all four exact Taylor integrals, the rational tail, the Jensen intersection for Z, all signed product corners, the numerator, positive denominator, covariance interval and width. A canonical semantic replay rejects a status supplied without matching arithmetic.

The accepted source's implementation domain is exact rational couplings with |each|≤8 and total absolute sum≤12, and Taylor degrees0 through48 satisfying the strict tail-ratio condition N+2>M. These limits bound the current implementation; the underlying compact-integral identity is not restricted to this box. A rational string is required inside serialized certificates, with no floating proof coefficients.

The complete collection schema, its producer hash, nonempty unique fixture IDs and individual certificate schemas are checked. The 23 fixtures cover the selected convergence sequence, zero action/degree0, signed eta=0 factorization controls, special eta-only families, small signed deformations, signed mixed couplings and supported boundary values. They do not establish a universal covariance-sign theorem outside the proved special family and local interval.

The exact audit has **59 registered checks**. A further **17 boundary checks** challenge changed source/oracle bytes after a warmed cache, mutable cached expected data, incomplete or duplicate collections, source substitutions and invalid metadata. Both suites pass ordinary and optimized Python; the two execution modes are not counted twice.

## 3. Defects identified and preserved

The independent reviewer found a producer metadata bug: Python equality identifies True and1. The original verifier therefore accepted `tail.first_omitted_degree=True` in a degree-0 certificate whose correct value was1. The forward member reproduced it, retained the failing source/fixture and repaired replay with strict recursive type checking. This was a semantic certificate defect; the recorded numerical values were not changed by it.

The independent reviewer also found two proof-adapter admission defects:

1. A caller could supply an empty frozen-source collection and fabricate a matching passed-record fingerprint. The draft library constructor trusted that record and admitted all arithmetic gates. Its ordered replay then accepted a ten-rule finite proof without any actual scientific replay.
2. The mutable in-memory rule list could be extended by a fabricated `measure -> yang_mills_gap` rule while file hashes remained unchanged. The draft library admitted an unsupported one-step outer proof.

Both failures were executed in isolation and retained in `loop2_history/proof_adapter_admission_failures.json` with the original draft bytes. Root repaired the constructor to perform fresh independent exact replay before admitting facts, froze the rule declarations and rechecks their serialized semantics, bound the reviewed adapter bytes in the second-loop gate, and corrected the outer nodes' physical-continuum domain label. The repaired adapter rejects both original attempts and a covariance mutation even when its certificate hash is updated consistently.

## 4. Advisor algebra and evidence transfer

`review_advisor.py` compares the advisor's twice-differentiated covariance polynomial with an independent construction of the fourth cumulant from all fifteen labelled set partitions. A nonzero fixture on four admissible center-element triples checks the contraction signs. This independently verifies the formal identity used in the improved constant7 argument.

The sharper analytic inequality itself uses the reviewed centered-variable proof: |dz|≤2, E|dx dy|≤sqrt(Var(x)Var(y))≤1 and every covariance has magnitude at most one. The three fourth-cumulant terms are bounded by4,1,2. Merely adding those integers is not the entire analytic proof.

The review also executes the advisor's frozen source with the pinned round13 variance checker and certificate collection. It independently reconstructs outward rounding to denominator10^15 by `divmod`, checks exact containment and sub-unit rounding slack, and recomputes each signed perturbative interval. The compact endpoints are rational outward enclosures; no floating roundoff is used to claim containment. **23 independent advisor-review checks pass** in both execution modes.

## 5. Actual forward/backward meeting and its outer boundary

The root adapter contains eleven reviewed conventional rules. Rules r01–r10 connect the declared compact Haar/action premises and independently replayed arithmetic gates to the positive finite covariance. The backward prerequisites are a strictly positive normalizer, a rigorous connected-numerator interval and the requested sign/width. The forward construction supplies those same objects from exact polynomial moments and a uniform exponential remainder.

The unchanged search core executes two fronts. The independent adapter harness confirms eleven routes: two positive finite conclusions and nine rejected routes with required gates/premises removed or an unmatched physical target requested. Both positive routes have recorded meetings and separate ordered proof replay. An independent saturation calculation checks all128 subsets of the seven primitive hypothesis/gate facts. This checks the small Horn dependency library, not the completeness of research approaches to Yang–Mills.

Rule r11 is a conditional outer implication: a matched physical generator, common physical decay on the required dense sector, continuum construction and nontrivial pure theory would imply the physical gap target. None of those outer premises is admitted by a covariance certificate. The adapter keeps them in a physical-continuum domain, distinct from the finite Euclidean integral.

The repaired adapter passes **36 independent checks** in both execution modes. The reviewed adapter SHA256 is `da671529e9c0c520dbf82a4ae4afe41ebc8ca4caf27ca4fd6ad9a791b38575f7`, and the reviewed rule IDs are r01 through r11. The harness uses a clearly labelled synthetic gate to test the code before the advisor issues the real second-loop acceptance; that synthetic gate is not external review authority. Root must publish its actual acceptance gate and rerun against the frozen integrated files.

## 6. Further conventional implications and the next roadmap

There is a simple controlled removal theorem **within this same finite model**. For any fixed real observable with ||O||_infinity≤1,

\[
 \frac{d}{d\eta}E_\eta[O]=\operatorname{Cov}_\eta(O,z),
 \qquad |E_\eta[O]-E_0[O]|\le|\eta|.
\]

The derivative follows by differentiating the bounded integral; Cauchy–Schwarz and the variance bound for variables in [−1,1] bound its magnitude by one. Integrate along the real coupling segment. Thus removal of this bounded single mixed-loop deformation returns the declared observables to the exactly factorized eta=0 baseline. It does not yield a uniform bound for a growing sum of deformations, identify a Hamiltonian vacuum, or supply a four-dimensional continuum return theorem.

At each fixed finite rational triple, the unbounded-order mathematical version of the Taylor enclosure converges: R_N→0 factorially once N+2>M; exact raw intervals contract to the true integrals; Z≥1 makes the normalization map continuous. Consequently any truly nonzero covariance at that fixed point is eventually sign-certified by some sufficiently high order. This is a conditional algorithmic completeness statement when arbitrary successful orders are allowed. The implemented cap48 does not execute that infinite sequence, and an exactly zero covariance can remain inconclusive without a separate analytic identity.

The next useful finite experiments are to obtain a quantitative many-loop return estimate or derive the actual moment geometry of a genuinely interacting higher-dimensional pure Wilson complex. These require new action/graph proofs and should not silently inherit the two-holonomy product-Haar action. In parallel, the actual fixed-spacing Hamiltonian roadmap still needs explicit stability constants and a controlled route beyond the electric-dominated regime. The continuum reconstruction and common physical spectral decay remain separate unresolved prerequisites.

## 7. Reproduction

From the workbench root after integration, with this directory copied to `research/round14/backward`:

```bash
python research/round14/backward/oracle.py
python research/round14/backward/verify_certificate.py research/round14/forward/loop2_output/certificates.json research/round14/forward/loop2_certificate.py research/round14/backward/loop2_output
python research/round14/backward/test_verifier_boundary.py research/round14/forward/loop2_output/certificates.json research/round14/forward/loop2_certificate.py research/round14/backward/loop2_output
python research/round14/backward/review_advisor.py research/round14/advisor/advisor_checks.py research/round14/backward/loop2_output/advisor
python research/round14/backward/review_proof_adapter.py research/round14 research/round14/forward research/round14/backward/loop2_output/proof
```

Use `python -O` with separate output directories to reproduce optimized-mode checks. Root owns final source freezing, actual acceptance gates, public route execution and publishing.
