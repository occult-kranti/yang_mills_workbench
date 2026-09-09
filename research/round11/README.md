# The coupled two-plaquette study

This round derives the physical seven-link SU(2) operator on two adjacent open squares, including all six local Gauss constraints and the shared-link interaction. The physical quotient uses three traces x,y,z, with constant normalized Haar density on its constrained body. The Hilbert space is infinite dimensional; the spatial graph remains finite.

## Read the evidence

- `advisor/advisor.md`: complete equations, measure/domain, polynomial spectrum, tail comparison, heat-kernel gap proof, common/difference variables, alpha limit and remaining continuum obligations.
- `advisor/theorem_inventory.json`: 37 claims with dependencies and source locations; `inference_rules.json` and `experiments.json` define the roadmap.
- `solver/README.md`: implementation contract, parameters, CLI and numerical limitations.
- `skeptic/REVIEW.md`: independent source-level critique, original failures, mathematical review and exact acceptance scope.
- `proof_results.json`: actual bidirectional search, separate rule replay, source hashes and negative controls. The planner is not a formal proof kernel.

For rho=1, alpha>0 and finite lambda1,lambda2>=0, the conventional proof gives

    Delta >= (243/625)*alpha*exp[-16*(lambda1+lambda2)/(3*alpha)].

Exact rational arithmetic plus a tail and continuity theorem further gives a useful bound over the whole closed parameter square:

    Delta >= 0.96*alpha,  0 <= lambda1/alpha,lambda2/alpha <= 2.

The exact computed normalized lower is `963936567779819/1000000000000000`. For the matched point `(alpha,lambda1,lambda2,rho)=(1,2,3,1)`, the degree-4 certificate gives `[3.362386061099721,3.362408390681595]`. These are full finite-graph Hilbert-space enclosures, not just differences between finite-matrix Ritz upper bounds.

The earlier one-square result has different topology and a different exact spectrum. The complete four-dimensional Yang–Mills existence and mass-gap problem remains open.

## Execute from this directory

Install the repository's root `requirements.txt`, then:

```bash
python solver/test_solver.py
python solver/run_study.py
python proof_routes.py
python skeptic/audit_solver.py solver/two_plaquette.py --label local_replay
python skeptic/audit_dynamics.py solver
```

These commands rewrite output records. Preserve a clean clone or copied directory for provenance comparisons. The rational certificate inputs are deterministic under the recorded settings; changed source bytes or stale inputs fail the proof manifest. Do not edit a hash set to hide a missing premise. Source, dependency, solver tolerance and representation changes require a new reviewed run.

For the independent proof-wrapper mutation suite, follow `skeptic/README.md`: it creates an isolated copy before deliberately changing mathematical files and metadata. Do not run mutation probes against the sole evidence copy. Scripts use `python -O` as a separate acceptance check; repeated normal/optimized outcomes are not counted as new independent tests.

To inspect a single case:

```bash
python solver/two_plaquette.py --degree 3 --alpha 1 --lambda1 1 --lambda2 2 --rho 1 --certificate
```

Without `--certificate`, the CLI returns numerical Ritz estimates and explicitly labels them as such. The numeric API selects alpha,rho>0 and lambda_i>=0. Rho weights the existing shared-link electric term; it is not a new field. The analytic rho=0 endpoint is discussed separately in the advisor report.

## Simulations and their limits

`solver/output/` contains exact certificates, the complete rectangle cover, fixed-parameter degree refinement, one-coefficient sweeps, exact low-degree fixtures, raw histories for every reported evolution, and PNG/SVG plots. The drive uses alpha=rho=1, lambda1(t)=1-cos(pi*t/2), lambda2(t)=1.5*(1-cos(pi*t/2)), t in [0,2], starting from the constant Haar wavefunction.

Degree-4 energy is 4.137719528396125; separately integrated work is 4.137719528400475. The independent raw-monomial RK45 calculation agrees with degree-3 orthonormal DOP853 to about 1.11e-11 in Haar state norm. Degree3→4 still changes the state by about0.00409082. This distinction is preserved: a good integrator and correct work identity do not certify infinite-state dynamics. No dynamic truncation-error bound is reported.

The 199 solver edge/mutation tests and 25 study gates pass. Independent review reports 495 exact/core gates, 16 dynamic checks and 30 proof-wrapper checks. Their fixtures and source scope are available, and original failures remain executable. Agent review is not credentialed human peer review.

`build_site_data.py` is an integration script for the full repository: it binds the recorded source hashes, rejects incomplete reviews, and writes the site's data and CSV assets. It is not needed to reproduce the mathematical study in a standalone extracted package. The full repository's `scripts/build_pages.py` then builds the static public website.
