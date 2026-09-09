# Independent verification of the causal response

The new computation differentiates an already coupled Maxwell–Dirac initial-value problem with respect to the amplitude of its smooth external-current pump. It measures sensitivity **inside a specified finite semiclassical model**. The mode variation implicitly evolves the action of the finite-regulator retarded kernel derived in contract P24–P26. It is not a calculation of quantum current noise, a covariantly renormalized continuum current-commutator tensor, or proof that the mean-field approximation is valid.

## Independent representation and derivation

The candidate uses three real Bloch components per Landau block. The verifier evolves two complex spinor components under

\[
i y'=H y,\qquad H=M\sigma_1+p\sigma_3,\qquad p=k-a.
\]

No production differential equation or subtraction routine is imported. The quadrature and physical assumptions are intentionally shared; this isolates implementation error and does not provide independent evidence for those shared assumptions. The verification also solves the full nonlinear spinor problem at pump amplitudes \(A+\epsilon\) and \(A-\epsilon\), without tangent variables, and compares their centered difference with the independently evolved tangent.

Let \(v=\partial_Aa\), \(u=\partial_Ax\), \(z=\partial_Ay\), and \(q=\partial_Ak-v\). Ordinary amplitude variation holds the regulator fixed, so \(\partial_Ak=0\). Differentiating the spinor equation gives

\[
i z'=H z+q\sigma_3y,\qquad
\eta_i=2\operatorname{Re}(y^\dagger\sigma_i z),\qquad
v'=-u.
\]

The initial state is the exact magnetic vacuum, before the compact pump begins. It is unchanged by pump-amplitude variation: \(v(0)=u(0)=z(0)=0\). A prepared initial electric field is a different physical problem and cannot be substituted for this preparation.

The three derivatives needed by the constitutive law are

\[
\partial_p(p/\omega)=M^2/\omega^3,\qquad
\partial_p\frac{M^2}{4\omega^5}=-\frac{5M^2p}{4\omega^7},\qquad
\partial_p\frac{5M^2p}{8\omega^7}
=\frac{5M^2(M^2-6p^2)}{8\omega^9}.
\]

Using \(S=\sum w(r_3+p/\omega)\), \(C=\sum wM^2/(4\omega^5)\), \(D=\sum w5M^2p/(8\omega^7)\), and \(Z=1+\chi_B-e^2C\), the quotient derivative is

\[
u'=\frac{\delta F-e^2(\delta S+\delta D x^2+2Dxu)
                    +e^2\delta C x'}{Z}.
\]

The final term has a **positive** sign because \(\delta Z=-e^2\delta C\). Omitting it leaves an apparently reasonable response system that fails an independently evaluated identity.

The tangent energy follows by differentiating the same matched energy as the baseline:

\[
\delta U=\sum w\,[M\eta_1+p\eta_3+q(r_3+p/\omega)],
\]

\[
\delta W=Zxu-\tfrac12e^2\delta C x^2+e^2\delta U,
\qquad (\delta W)'=uF+x\delta F.
\]

The work variation is integrated as a separate ODE. It is not estimated by coarse integration of stored samples. Norm preservation supplies two additional identities, \(2\operatorname{Re}(y^\dagger z)=0\) and \(\boldsymbol r\cdot\boldsymbol\eta=0\). Neither identity by itself certifies response accuracy.

The full dimensionless matter current is \(J=S-Cx'+Dx^2+\chi_Bx'/e^2\). The verifier records this current and its derivative explicitly. It does not label the numerator \(S+Dx^2\) as the physical current.

## Finite test configurations

Both tests retain Landau levels 0 through 2 and 32-point Gauss–Legendre quadrature on \([-6,6]\). They use DOP853, relative tolerance \(2\times10^{-11}\), absolute tolerance \(2\times10^{-13}\), and maximum step 0.02. The first test uses \(b=10\), amplitude 1, pump duration 4, and final time 8 with 81 samples. The independently selected second test uses \(b=3\), amplitude 0.5, pump duration 6, and final time 18 with 181 samples. These small regulators are implementation fixtures, not production continuum approximations.

Centered differences used \(\epsilon=0.002,0.001,0.0005,0.00025,0.000125,0.0000625\). The whole-history field derivative discrepancy decreases by approximately a factor of four at each halving. It reaches \(3.45\times10^{-9}\) in the first case and \(7.86\times10^{-8}\) in the second. These discrepancies are empirical comparisons; no interval-arithmetic enclosure is claimed.

The initially planned smallest difference \(\epsilon=0.0005\) failed the preselected \(2\times10^{-7}\) acceptance target: its discrepancies were \(2.22\times10^{-7}\) and \(5.03\times10^{-6}\). The original failed record remains in `response_verification_initial.json`. The step was refined because the observed second-order trend identified finite-difference truncation as the limiting error; the gate was not relaxed.

The directly evaluated full-current variation supplies a separate diagnostic. Its whole-history centered-difference discrepancy decreases from \(5.33\times10^{-4}\) to \(5.21\times10^{-7}\) in the first case, and from \(9.73\times10^{-3}\) to \(9.57\times10^{-6}\) in the second, across the same six steps. This is also a second-order sequence. These current discrepancies are reported directly; no extra precision threshold was selected after observing them. In particular, P12 contains \(u'\), not \(u\), in the two terms proportional to \(C\) and \(\chi_B\).

The exact finite-model tangent energy/work relation has maximum absolute residual \(4.05\times10^{-11}\) and \(1.00\times10^{-10}\), respectively. Dividing by the explicitly reported global tangent energy scales gives relative residuals \(4.07\times10^{-11}\) and \(2.00\times10^{-10}\). These are conservation diagnostics, not total physical error estimates.

## Deliberate falsifiers and boundary cases

| Test | Measured result | Interpretation |
|---|---:|---|
| Delete only the \(\delta Z\) quotient contribution | Field response changes by \(2.03\times10^{-4}\); differentiated work defect \(1.95\times10^{-4}\) | The evaluator detects an easily missed coupling term. |
| Freeze the dynamical mode contribution to the current response | Field response changes by 1.51; work defect 1.53 | A response built only from a changing vacuum subtraction is inconsistent. This is a deliberately wrong control, not a competing physical model. |
| Shift \(a_0\) and every canonical momentum together by 7.3 | Field tangent changes by \(4.11\times10^{-15}\) | Correct residual gauge transformation preserves the tested response. |
| Shift \(a_0\) while holding the finite canonical window fixed | Field tangent changes by 0.0382 | This is a different regulated problem, not evidence against gauge invariance. |
| Pure gauge tangent \(\delta a=\delta k=1\) | Electric-field tangent remains exactly zero in the recorded arithmetic | The kinetic momentum and initial magnetic vacuum are unchanged. |
| Delay the compact tangent source until time 9 | Maximum prior response \(2.91\times10^{-77}\) | No resolvable acausal response; values below meaningful arithmetic scale are reported rather than clipped. |
| Exactly zero base pump | Maximum absolute response 0.9969; base field only \(6.25\times10^{-16}\) numerical residual | Linear response is well defined. Relative amplification against the zero base field is not. |

The two broken controls preserve the baseline and alter only the tangent system. Their large defects cannot be attributed to comparing different background trajectories. For field-zero crossings, the response should be normalized by one declared nonzero global field or energy scale, never by the instantaneous field. A zero-field baseline requires absolute response and an undefined relative gain; inserting a convenient denominator would invent an observable.

## Frozen production comparison

The final array comparison reads the production results without importing production code. It checks the source hash, per-record hashes, physical preparation, regulator, output times and observed discrepancies. At production source `0a197f5b46de8114d790c937059018d21df3f55a436c76067b91c09277035867`, all 19 comparison and provenance gates pass.

| Whole-history absolute discrepancy | First finite fixture | Independently selected second fixture |
|---|---:|---:|
| Electric-field tangent \(u\) | \(1.07\times10^{-11}\) | \(3.76\times10^{-11}\) |
| Potential tangent \(v\) | \(1.15\times10^{-11}\) | \(8.06\times10^{-11}\) |
| Direct matched-current tangent \(\delta J\) | \(4.00\times10^{-11}\) | \(9.28\times10^{-11}\) |
| Baseline electric field \(x\) | \(3.62\times10^{-12}\) | \(4.29\times10^{-12}\) |

The direct-current check mattered: an intermediate production expression used \(u\) where P12 requires \(u'\). Comparing a Maxwell-rearranged current alone would have missed that direct-output error, because the field tangent was already accurate. The current expression was corrected before the accepted comparison. The separate script `compare_response_production.py` and result `response_production_comparison.json` preserve the final comparison and all hashes.

## Acceptance boundary

The independently generated result file records every acceptance gate, configuration, trajectory, finite-difference step and code hash. The comparison establishes that the two implementations differentiate the same tested finite problem. The 13 independent verification gates, 19 production-comparison gates and six advisor-skill evidence checks are different tests; their counts must not be interpreted as independent probabilities or a percentage of the full physical problem solved.

Further momentum, window and Landau refinement are needed for a regulator-controlled response observable. Source-off amplification over one finite interval is not an all-time stability result. Connection to renormalized causal quantum kernels, metric perturbations, anisotropic stress and quantum fluctuations remains a separate derivation and validation task.
