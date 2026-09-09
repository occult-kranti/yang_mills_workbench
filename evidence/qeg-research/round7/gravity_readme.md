# Round7 bounded scalar–Einstein–Maxwell Bianchi-I benchmark

This directory contains a finite classical benchmark for the natural-unit system specified in the round7 task. It is a new-sector ODE calculation; it does not compute Dirac quantum stress tensors and makes no cutoff-removal claim.

`gravity_sim.py` integrates the full eight-variable state `(lA,lC,phi,v,hp,hl,E,B)` with both DOP853 and Radau. It separately integrates a six-variable reduced system (sharing the gravitational RHS) in which E and B are reconstructed from the conserved fluxes `exp(2*lA) f E` and `exp(2*lA) B`. The trajectories, constraints, fluxes, and wrong-model Ward data are emitted as CSV files.

The true constraint is `C=hp^2+2*hp*hl-rho-lambda` and propagates as `C'=-theta*C`. The control removes only the scalar electromagnetic force from `v'`, computes `Q` analytically from all state derivatives, and integrates `I'=exp(2*lA+lC)Q`; therefore `exp(2*lA+lC)C+I` remains constant while C itself drifts.

Cases: coupled mixed fields, pure electric, pure magnetic, c=0, Minkowski, pure de Sitter, nonzero scalar, and a short early-contraction branch. Inputs and time grids reject malformed, non-finite, non-monotone, and unsafe bounded runs with explicit exceptions.

Generated `2026-09-09T17:00:32.878448+00:00` with Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. Source SHA-256: `7b811ae535a46b3cf34c0b1b1c25d955f4751bda97aa89196b73399e1df65707`.

Gate results: {"all_finite_trajectories": true, "analytic_fixtures": true, "auxiliary_methods_agree": true, "fluxes_preserved": true, "full_reduced_agree": true, "methods_agree": true, "true_constraint_small": true, "wrong_constraint_fails_for_coupled_mixed": true, "wrong_invariant_small": true}
