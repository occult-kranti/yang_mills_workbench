# Root implementation audit and corrections

The complete initial finite_scalar.py and gravity_sim.py were read in bounded sections. Their equations were compared with the advisor contract and separately derived skeptical identities. Initial implementations are preserved under initial_implementations. Root validation is not attributed to the agents whose final reviews were interrupted by a usage limit.

| Finding | Why it matters | Correction and verification |
|---|---|---|
| Baseline import omitted sys.modules registration and caught all errors | Dataclass import failure could silently skip the historical comparator | Register the module, surface import failures, require `status=compared` and a passed comparison |
| nu=0 was rejected | A massless scalar and zero-frequency affine solution are legitimate limits | Admit nu>=0; implement the Omega=0 branch and test it |
| phi0=y0=0 was rejected for g>0 | A valid invariant subspace was confused with a nondiscriminating experiment | Admit it; test invariance separately from nonzero-exchange cases |
| Probe amplitude could be silently ignored in the wrong mode | A comparison might test a different source than its labels claim | Reject unused nonzero probe; validate mode and Boolean wrong-model switch |
| Several numeric inputs accepted strings or Booleans | Python's numeric coercion could hide malformed parameters | Reject these types explicitly; retain finite-value checks |
| Finite-difference gate only detected a nonzero signal | It did not check response resolution or pre-source behavior | Compare three centered perturbation sizes and the pre-source derivative; no claim of a demonstrated asymptotic order |
| Gravity analytic fixtures were defined but never called | A passing summary did not imply the fixtures ran | Execute both fixtures and include their results as acceptance gates |
| Empty default description prevented fixture creation | A documentation field blocked valid mathematical inputs | Require a string but allow an empty description |
| Small negative initial Friedmann radicands were clipped to zero | An inconsistent initial constraint could be silently altered | Reject every negative radicand; explicitly test a small negative value |
| Wrong-model gravity diagnostic clipped exponential arguments | Clipping could conceal an out-of-domain trajectory | Use an explicit checked exponential and fail outside the domain |
| Auxiliary Radau trajectories were computed but not compared | Integrator coverage was overstated | Check full, reduced and wrong-model method differences |
| Selecting a gravity case without coupled_mixed raised StopIteration | A supported command-line selection could fail for an unrelated gate | Apply that discrimination gate only when its case is selected and report absence explicitly |
| Flux reduction reused the gravitational RHS | It is a separately integrated formulation but not wholly independent source code | State this limitation; retain the separately written skeptic system and symbolic identities |

`validate_simulations.py` supplies an independent complex-spinor RK45 reference for the finite model, sharing only its specified regulator, constants and preparation. It does not call production RHS, energy or term functions. It also tests gauge translation, malformed inputs, zero-frequency and invariant preparations, negative coupling, equal initial fields, source/result consistency and before/after hashes.

Normal and optimized Python both passed the 47 root checks and 42 independent skeptical checks. Counts group heterogeneous checks and do not imply confidence percentages. Production finite and gravity suites have separate recorded gates. The gravity case selector was checked with the Minkowski-only command; its output was then replaced by a fresh complete eight-case run.

The code audit covers the two new scientific implementations and their root integration checks. It does not claim exhaustive branch coverage, a formal proof of floating-point code, a line-by-line audit of SciPy, or browser execution. Initial files are historical evidence and must not be run as current validated solvers.
