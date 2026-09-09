# Advisor review of round 4

Review status: accepted for the specified finite-regulator response calculation. The selected record is `production_nk1024_baseline`. Its source, corrected diagnostics, independent comparisons and targeted fixed-window momentum refinement have been inspected. This is not a continuum, quantum-fluctuation or gravitational-validity certificate.

## The errors found are specific and reproducible

The first audit compared the delivered round-3 source with its claimed change. The reported per-mode current-cancellation fix was absent: `_grid_terms` still formed `j0=jrz+jkin` after separately summing the two contributions. Root confirmed that the delivered ZIP, current source and recorded run share SHA-256 `32008bfc4fc3f731ac7ed968006fd58642820e0f421766a1ace022a2d7f08e88`. This is a report/source mismatch. It does not establish that the field reversal is false. Round 3 is preserved; the new implementation evaluates `sum(w*(rz+p/omega))` and compares its actual numerical effect with the unchanged legacy code.

The next audit found a fresh diagnostic error before accepting round 4. The directly evaluated current variation used the electric-field variation \(u=\delta x\) where the subtraction and matching require its time derivative \(u'=\delta x'\). The corresponding displayed Maxwell residual made the same confusion. The principal coupled tangent RHS was correct; the diagnostic formula was not. The independent spinor implementation used the correct derivative, providing a genuine comparator.

More seriously, four production diagnostic arrays had been initialized to zero and never populated. Those zeros made the current-variation and tangent-orthogonality gates appear to pass. This is a false diagnostic pass, not a measured zero. The accepted repair populates every sample and rejects missing/nonfinite diagnostics; a named gate cannot certify its own uncomputed input. The selected record contains finite, nontrivial current, energy and tangency diagnostics.

The optional `unrenormalized` branch also switched \(Z\) to one while retaining subtraction terms from the matched branch. The accepted solver explicitly rejects that unimplemented option. It also rejects nonfinite parameters, invalid pulse durations and invalid integer grid settings before integration.

Finally, the initially suggested production momentum grid was insufficient. At fixed \(b=10,N=4,K=20,s_f=20\), the amplitude derivative endpoint changed from approximately 0.0545948 to 0.0400582 between 128 and 256 longitudinal nodes. Small work residuals did not diagnose that integration error. This is the reason for a focused fixed-window refinement; repeating independent symbolic checks or asking more agents to agree would not resolve it.

## Accepted theory contract

The advisor and independent verifier agree on the complete first variation in `response_contract.md`. In particular, the quotient contribution is \(+e^2\delta C\,x'/Z\); the variation of \(D\) contains \(M^2-6p^2\); the matter current requires \(-Cu'+\chi_bu'/e^2\); and the differentiated work identity is \((\delta W)'=uF+xf\). Each quantity uses one fixed canonical regulator and one magnetic matching coefficient.

The initial source-amplitude tangent is zero because the magnetic vacuum is identical for all amplitudes before the smooth pump starts. A delayed probe has no earlier perturbation. A constant gauge change translates the retained canonical momenta along with the potential. These are different physical/regulated families, and mixing them would spoil the interpretation.

The Bloch tangent also has an exact finite-regulator retarded rotation-kernel representation. Evolving it computes the response kernel's action without storing a dense two-time tensor. This is not a covariantly renormalized continuum current/stress kernel and does not calculate the symmetrized connected quantum noise.

## Accepted independent evidence

The verifier uses complex spinors and their tangents without importing the production differential equations or subtraction routines. It separately solves the nonlinear family at shifted amplitudes. The fixed quadrature and physical assumptions are shared intentionally; this isolates implementation error and is not an independent validation of those assumptions.

| Evidence | Measured result | Accepted scope |
|---|---:|---|
| Central differences, baseline | Maximum full-history field-derivative discrepancy falls from \(3.55\times10^{-6}\) to \(3.45\times10^{-9}\) | Second-order response check on \(b=10,N=2,K=6,N_k=32,s_f=8\) |
| Central differences, held-out | Discrepancy falls from \(8.01\times10^{-5}\) to \(7.86\times10^{-8}\) | Changed magnetic field, source amplitude and duration, same small regulator |
| Differentiated work | Maximum absolute residuals \(4.05\times10^{-11}\), \(1.00\times10^{-10}\) | Exact identity respected by the independently integrated finite model |
| Delete quotient contribution | Response changes by \(2.03\times10^{-4}\), work defect \(1.95\times10^{-4}\) | The test detects the missing term |
| Freeze coherent mode response | Response change 1.51 and work defect 1.53 | The test detects an inconsistent response closure |
| Translate gauge and grid | Field tangent changes by \(4.11\times10^{-15}\) | Correct residual gauge transformation on the tested regulator |
| Fixed-window potential shift | Field tangent changes by 0.0382 | This is a changed regulator, not a gauge violation |
| Delayed source | No resolvable response before the probe | Retarded temporal support |
| Zero base amplitude | Finite absolute tangent; essentially zero base field | Relative gain against the base field is undefined |

The originally planned finite-difference step \(\epsilon=5\times10^{-4}\) failed the preselected \(2\times10^{-7}\) field-derivative comparison target. The sequence was extended to \(6.25\times10^{-5}\), where both cases pass. The clean second-order trend identified finite-difference truncation as the limiting error. The failed record remains `response_verification_initial.json`; the threshold was not relaxed.

The direct physical-current derivative is also independently evaluated. Its full-history central-difference discrepancy shows the expected second-order trend, reaching about \(5.21\times10^{-7}\) and \(9.57\times10^{-6}\) in the baseline and held-out cases at the smallest step. These are diagnostic comparisons; no retrospective tighter current-accuracy gate is invented.

## Independent comparison of repaired production outputs

The frozen production source `0a197f5b46de8114d790c937059018d21df3f55a436c76067b91c09277035867` matches the regenerated result and per-record hashes. The independent comparison reads numerical arrays without importing production code. All 19 comparison gates pass. On the baseline small fixture, maximum full-history differences in the field tangent, potential tangent and directly evaluated matter-current tangent are respectively \(1.07\times10^{-11}\), \(1.15\times10^{-11}\) and \(4.00\times10^{-11}\). On the held-out small fixture they are \(3.76\times10^{-11}\), \(8.06\times10^{-11}\) and \(9.28\times10^{-11}\). The comparison target was \(2\times10^{-8}\). These results validate the repaired diagnostics and implementation within these finite models.

The old false-zero array output was overwritten before a byte-for-byte archive was captured. `advisor_errata.json` records that limitation explicitly. The retained post-fix snapshot must not be described as an archived original failure.

## Final production decision and resolved numerical risk

The selected case uses \(b=10,\lambda=1,T=4,s_f=20\), Landau indices \(n=0,\ldots,4\), longitudinal interval \([-20,20]\), 1024 Gauss–Legendre nodes and 401 reported times. The matched model is integrated with relative tolerance \(2\times10^{-10}\), absolute tolerance \(2\times10^{-12}\) and maximum time step 0.05.

The advisor froze a maximum sampled full-history field-tangent change below \(10^{-6}\) before inspecting the targeted refinements. These are differences between successive quadratures at the same finite window and Landau cutoff:

| Node comparison | Maximum \(|\Delta x|\) | Maximum \(|\Delta u|\) | Maximum direct \(|\Delta(\delta J)|\) | Decision |
|---|---:|---:|---:|---|
| 128 to 256 | \(2.87135\times10^{-4}\) | 0.0504254 | 9.21273 | Coarse response unresolved |
| 256 to 512 | \(7.15008\times10^{-5}\) | 0.0130291 | 3.25983 | Coarse response unresolved |
| 512 to 1024 | \(9.19598\times10^{-13}\) | \(2.15725\times10^{-10}\) | \(8.43000\times10^{-8}\) | Frozen field-tangent target passes |

The dramatic improvement is measured, not inferred from an energy residual. The current difference is reported separately because it differentiates an observable with faster mode oscillations. It is not an independently preselected current-accuracy threshold. Additional 2048-node runs are unnecessary to resolve the specific observed quadrature failure. Cutoff removal and control between reported time samples remain separate claims.

At the selected endpoint, \(x(20)=0.7284246832122947\) and \(u(20)=0.047336333923474944\). Across the reported interval the field tangent is finite, ranging from zero to about 0.986892. This is an absolute derivative with respect to the preparation impulse. It does not establish an all-time stability bound or small quantum fluctuations.

The minimum \(Z\) is 0.9965117049606924. The maximum background and differentiated-work residuals are respectively \(9.46\times10^{-13}\) and \(3.71\times10^{-12}\). The direct-current Maxwell residual is \(2.22\times10^{-16}\); the raw Bloch-norm error is \(1.23\times10^{-9}\), and the maximum raw tangent orthogonality error is \(5.72\times10^{-9}\). No tangent projection or normalization is used to manufacture these values. At identical sampled states, changing from separately aggregated current sums to per-mode subtraction changes \(S\) by at most \(1.85\times10^{-14}\) in this selected run; this narrow numerical observation does not repair the historical report/source mismatch retroactively.

Exact hashes, parameters and gate decisions are recorded in `physics_acceptance.json`; the independent comparator binds its final output to the accepted production source and result bytes. Failed coarse grids and the initial failed finite-difference threshold remain available.

## Interpretation limits and the next decision

Passing tangent and finite-difference comparisons means that the derivative of the specified finite nonlinear model is correctly computed on the tested cases. It does not mean that the continuum regulator has been removed, that electromagnetic quantum fluctuations are small, or that all inhomogeneous perturbations are stable. The homogeneous longitudinal response cannot be substituted for a finite-momentum transverse photon refractive index.

No quantum Einstein evolution is approved at this stage. The next dependency is a common covariant current/energy/two-pressure subtraction satisfying the electromagnetic-force Ward identity in an anisotropic metric, followed by response/noise and initial-constraint checks. A real electron-scale stress budget must support any proposed curvature. The other three original fronts remain active in `physics_completion_roadmap.md` with separate state, geometry and observable contracts.

The finite-model P3 deliverable is complete and accepted within these boundaries. The next solver handoff is `targeted_solver_prompt.md`. Initial false-zero diagnostic flags remain superseded evidence, and no approval to evolve gravity follows from this acceptance.
