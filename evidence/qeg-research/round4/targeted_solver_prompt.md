# Targeted GPT Astra solver specification

Use this prompt with `response_contract.md`, `response_advisor_review.md`, `physics_acceptance.json`, `advisor_errata.json`, the production code and the independent verification records. Read the attachments before proposing changes. These are explicit public task instructions, not a request for hidden reasoning. Return derivations, assumptions, alternatives rejected with reasons, executable artifacts and measured evidence.

## Role, objective and claim boundary

Act as an analytical physicist and numerical verification lead. Reproduce and audit the finite-regulator, longitudinal causal response of the homogeneous matched Maxwell–Dirac initial-value problem in contract equations P1–P26. Then specify the missing P27 covariant stress closure without pretending it is implemented. The four original research fronts remain hypotheses and research programs. Do not claim that reproducing this subproblem solves quantum gravity, establishes cosmic censorship, proves the WGC/Festina Lente conjectures, or demonstrates gravitational-wave conversion.

## Equation and preparation contract

Use $s=mt,a=eA_z/m,x=eE_z/m^2,b=|eB|/m^2$, signature $(-+++)$, natural Heaviside–Lorentz units and $e^2=4\pi\alpha$. Use exactly the fixed positive Gauss–Legendre weights and Landau factors in P1, with $n=0,\ldots,N$. P2–P6 define the background, subtraction and finite magnetic matching. P7–P12 define the complete first variation. In particular, retain the quotient term $+e^2\delta C\,x'/Z$, and use $u'=\delta x'$, not $u=\delta x$, in the derivative terms of the direct matter-current variation. Perform vacuum subtraction inside each weighted mode contribution. Never add the same QED loop again as an Euler–Heisenberg source.

The physical family is $F(s;\lambda)=\lambda g_T(s)$ with normalized compact pulse P14 and the common magnetic vacuum P13. Initial source tangents are zero. The amplitude is the integrated external-current impulse, not the realized peak electric field. A delayed perturbation and a gauge null are separate families. Gauge tests translate both the potential and the canonical grid. This temporal IVP has no radial origin, horizon or spatial-infinity boundary. Do not invent them.

## Required work products

1. Derive P8–P12 and P16–P20 algebraically, with a complete SymPy script that simplifies the derivative and work-identity residuals to zero. Independently explain why tangent magnitude need not be conserved. State the fixed-regulator retarded-kernel equivalence P24–P26 and its noise limitation.
2. Supply complete runnable Python using NumPy/SciPy, an environment/dependency record and a command-line entry point. Solve the background, tangent and integrated work variables together with an adaptive high-order method such as DOP853. State tolerances, maximum step, sample times, state layout, and how dense output is used. Diagnostics must be populated from actual arrays; reject missing or nonfinite values. Do not renormalize or clip the tangent to enforce constraints.
3. Reproduce the accepted $b=10,\lambda=1,T=4,s_f=20,N=4,K=20$ case at 512 and 1024 longitudinal nodes and 401 output samples. Use the recorded tolerances. The frozen acceptance target is maximum sampled full-history $|u_{1024}-u_{512}|<10^{-6}$; separately report direct-current and background-field sensitivity. Preserve the failed 128/256/512 comparisons. This checks quadrature at a fixed window and Landau cutoff, not removal of either cutoff.
4. Reproduce the two independent small fixtures in `response_production_comparison.json`, using complex spinors P22–P23 without importing the production tangent RHS. Compare complete sampled histories. Scan central-difference amplitudes from $0.002$ to $0.0000625$, retain failed steps and show truncation trends. Include the delayed, translated-gauge, pure-gauge and zero-amplitude cases. Deliberately omit the quotient term in a test-only mutant and confirm a resolvable diagnostic failure.
5. Write a report with an equation/change ledger, direct current residual, raw norm/tangency errors, work identities, per-axis refinement, source/result hashes, independent differences and a bounded claim. Preserve superseded evidence rather than overwrite it silently.

## Machine-readable output contract

Emit `solver_result.json` with this required schema shape (additional fields allowed):

```json
{
  "contract_version": "P3-v1",
  "status": "accepted_finite_model | failed | blocked",
  "source_sha256": "string",
  "parameters": {"b": 10, "lambda": 1, "T": 4, "s_final": 20, "N": 4, "K": 20, "nK": 1024},
  "preparation": "source_amplitude",
  "samples": {"s": [], "x": [], "u": [], "delta_J_direct": []},
  "diagnostics": {},
  "gates": [{"name": "field_tangent_refinement", "status": "blocked", "threshold": 0.000001, "measured": null, "passed": null}],
  "superseded_records": [],
  "scope_limits": [],
  "next_dependencies": []
}
```

Select one top-level status from `accepted_finite_model`, `failed`, or `blocked`; the pipe-separated text above describes the allowed values, not a literal status. Each gate has status `passed`, `failed`, or `blocked`. For a computed gate, `measured` is a finite number and `passed` is a Boolean consistent with the status. For an uncomputed gate, `measured` and `passed` are null and the status is `blocked`. All accepted sample arrays must have equal nonzero lengths and finite values. A missing computation is never represented by a numerical zero or a pass. If a result-file hash is recorded, compute it after the final write and place it in a separate manifest to avoid a self-referential hash.

## Stop rules and the P4 readiness decision

Stop on $Z\leq Z_{\rm floor}$, nonfinite state, inconsistent preparation, unexplained identity failure or a source/output mismatch. Diagnose the cause before changing equations or thresholds. Run further refinements only to resolve a specified remaining error. A finite-time response peak or division by a field zero is not proof of instability.

Before any gravitational evolution, specify a common covariant subtraction yielding $J_q,\rho_q,p_{\perp q},p_{\parallel q}$ in the P27 Bianchi-I geometry. Derive its electromagnetic-force Ward identity, list allowed finite counterterms and fix the renormalization conditions. Require consistent initial constraints, mixed current/stress retarded kernels, physically smeared noise, and a stress budget supporting the desired curvature. Until those dependencies are derived and verified, deliver a P4 readiness report with explicit missing terms, not an invented Einstein solver.
