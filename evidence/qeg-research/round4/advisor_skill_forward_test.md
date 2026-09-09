# Forward test of the project advisor skills

The independent response verifier applied the new `qeg-research-advisor` and `qeg-numerical-validation` skills to two realistic claims in `advisor_skill_claim_inputs.json`. Both skill files were read. Their linked protocol and contract copies exactly match the corresponding research documents by SHA-256. The source hash in the response result was also checked against the executed verifier file before adjudication.

This is a transparent two-case exercise, not a blinded benchmark or an estimate of general agent performance. The reviewer wrote the independent numerical verifier and therefore already knows its construction. The skills are project-local instructions for evidence review; this test does not modify hidden system instructions or prove that a future advisor will always detect a mistake.

## Case 1: a limited numerical claim

The supplied claim states that the independent spinor tangent agrees with centered nonlinear pump differences to a maximum sampled field-derivative discrepancy below \(8\times10^{-8}\), in the \(b=3\), amplitude 0.5, duration 6, final-time 18 experiment at \(\epsilon=0.0000625\). It explicitly limits the result to the finite regulator and avoids a continuum or semiclassical-validity claim.

**Disposition: accept with that stated scope.** The raw key `heldout_finite_differences[-1].max_field_derivative_difference` is \(7.860759199118661\times10^{-8}\). The regulator is Landau levels 0–2 and 32 momentum nodes on \([-6,6]\), with 181 stored times. Six finite-difference steps show the expected approximate factor-of-four error reduction. The claim reports an observed comparison, not a rigorous error enclosure.

The earlier record has a failed finite-difference gate: \(\epsilon=0.0005\) gave \(5.03\times10^{-6}\), above the preselected \(2\times10^{-7}\) threshold. The later run retains that historical failure and refines the difference step; it does not relax the threshold. This is a resolved numerical approximation issue and is not grounds to discard the narrower later result. The next independent test is comparison to the frozen production Bloch output, followed by separate response-quadrature and cutoff studies.

The skills correctly direct attention to the raw parameters, error definition, source hash, failed history, and separate numerical limits. Accepting this claim must not be silently upgraded to continuum accuracy, asymptotic stability, small quantum fluctuations or gravitational validity.

## Case 2: an incorrect physical interpretation of a real difference

The supplied claim takes a field-response change of about 0.038 after shifting the initial potential by 7.3 as evidence of spontaneous gauge-symmetry breaking.

**Disposition: retain the measurement and reject its physical interpretation.** The relevant raw difference is 0.038186197994979354, but inspection of `simulate` and `run_all` shows that this control sets `translated_grid=False`. It moves the potential while holding the finite canonical window fixed. Thus it changes the retained kinetic momenta and physical mode set. This is not the gauge transformation defined in contract P7.

The discriminating control shifts the canonical nodes and initial potential together. Its maximum field-tangent difference is \(4.107825191113079\times10^{-15}\). The explicit pure-gauge tangent has zero electric-field response. These controls explain the first difference as regulator dependence. They provide no evidence that the magnetic vacuum spontaneously breaks gauge invariance.

The next test for an actual gauge-violation claim would preserve the physical mode set, preparation and weights, and demonstrate a reproducible difference above integration error in another representation. Discarding the measured wrong-window result would also be a mistake: it is useful evidence that the regulator comparison must be specified correctly.

## Recorded outcome

All six mechanical evidence checks pass, and both claim dispositions follow the skills' contract, preparation and evidence rules. No skill change was required by these two examples. The JSON companion contains the exact inputs, raw values, source locations, hashes, limits and decisions. Broader effectiveness of the skills remains unmeasured.
