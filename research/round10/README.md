# Continuous coupling and a certified SU(2) plaquette gap

This round closes a specific approximation gap: an explicit tail theorem connects exact finite-matrix calculations to the full, infinite-character Hamiltonian on a single gauge-invariant square. A continuity theorem then extends point certificates to every coupling in a declared interval.

For H=alpha sum of four link Casimirs + lambda(1-ReTr U_loop/2), alpha>0 and 0<=lambda/alpha<=10, the certified result is

    Delta(alpha,lambda) >= (999999/1000000)*alpha.

The graph remains one finite square. This does not establish an infinite-volume or four-dimensional continuum Yang–Mills gap. The exact one-plaquette/Mathieu solution is established prior work; this package makes the derivation, error contract, exact certificates and independent checks inspectable without a novelty claim.

Read `advisor/advisor.md` for the mathematical derivation and 24-node theory map, `solver/README.md` for the numerical and exact-arithmetic contract, and `skeptic/REVIEW.md` for independent findings and retained defects. `proof_results.json` contains the actual bidirectional search and separate rule replay. A Horn route is not a proof-assistant formalization of the analytic theorems.

## Reproduce

Python 3.11+ with NumPy, SciPy and Matplotlib is required. Exact stationary certificates use standard-library Fraction arithmetic. No SymPy, mpmath or external proof service is required.

```bash
python solver/test_solver.py
python solver/run_study.py
python proof_routes.py
python skeptic/audit_independent.py
python skeptic/audit_artifacts.py
python skeptic/audit_acceptance.py
python skeptic/audit_proof.py
python skeptic/coordinate_check.py
```

Reproducing the study rewrites its output. Preserve an original copy when comparing provenance; the stored proof manifest requires byte-identical reviewed mathematical and certificate inputs. The same deterministic run settings regenerate the certified inputs. Scripts reject changed or missing required proof references rather than silently relaxing that check.

The time-dependent test ramps lambda(t)=5[1-cos(pi t/2)] from 0 to10 over t in[0,2], with alpha=1 and initial chi_0. It independently integrates source work and compares representation dimensions, time tolerance and a unitary midpoint method. These checks do not provide a rigorous dynamic-tail error enclosure.

`skeptic/coordinate-note.md` proves the next two-loop coordinate contract: x=Tr(U)/2, y=Tr(V)/2 and z=Tr(UV)/2 classify pairs up to simultaneous conjugation, with (z-xy)^2 <= (1-x^2)(1-y^2) and |x|,|y|<=1. Fifteen separate exact-matrix checks include degenerate endpoints and a counterexample to using x,y alone. The Site adds this as a 25th theory node. The coupled two-plaquette electric operator and its spectral certificates remain open work.

The full artifact includes raw histories, certificate endpoints, original failing source/probes and rendered figures. The compact Site download omits PNG/SVG figures and bulky temporary failure-probe directories while retaining the failure records and executable audit source. Replaying a retained defect may regenerate its probe output. The live Observatory also keeps the previous Yang–Mills, Einstein–QED, literature and learning branches.
