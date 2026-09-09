# Independent skeptical review — Yang–Mills round 9

**Verdict:** accept the stated finite-lattice identities, the complete-family finite Gibbs characterization, the auxiliary SU(2) convolution spectrum, and the conditional transfer-stability lemma within their explicit assumptions. Accept the corrected implementation on the executed fixtures. The review supplies no continuum four-dimensional Yang–Mills construction or physical mass-gap theorem.

The independent verifier completed **234 gates** in three reproducible scripts: 82 matrix/Haar/edge-case checks, 125 finite-theorem/raw-data checks, and 27 acceptance/proof-route checks. A gate is an executed diagnostic, not a new theorem. The conventional mathematical arguments were reviewed by an agent; there was no formal proof-kernel verification or credentialed human peer review.

## Accepted results and their strongest remaining objections

| Result | Independent evidence | What it establishes | What it does not establish |
|---|---|---|---|
| Wilson action and oriented staples | Complex 2×2 matrix oracle on 2×2×2×2 and 2×3×2×2 lattices; full-action link changes; all 64 link Ward terms reconstructed from global actions | Correct production quaternion orientation, six-staple normalization and tested local action changes | Every lattice geometry or every code branch |
| Link Haar identity | Independent Lie derivatives and 80-digit Haar integration; a wrong factor and an omitted reverse dagger produce resolved failures | Exact finite-measure identity and correct implementation on tested configurations | Correct sampling distribution from one satisfied residual |
| Complete SD family characterizes Gibbs law | Reviewed the weighted-measure argument, invariance under every generator flow, connectedness and Haar uniqueness | An exact characterization on a finite compact connected group product when every smooth test insertion is imposed | Closure of a finite truncation or a continuum measure |
| SU(2) convolution spectrum | Independently coded Decimal cosine, Gauss–Chebyshev Haar quadrature and character recurrence; node refinement; extreme-log checks | Eigenvalues I_n(β)/I_1(β), full multiplicity n², appropriate zero and underflow handling | The interacting gauge-invariant four-dimensional transfer spectrum or glueball masses |
| Product-L1/operator-norm counterexample | Independent SVD/eigenvalue calculations at held-out N=3,7,19,77 | Symmetric PSD positive Markov kernels can have product-L1 differences tending to zero while their operator difference stays fixed | A verdict on every assumption or argument of a 593-page claimed construction |
| Transfer stability | Independent 260-digit Decimal calculation, including a down to 10⁻²⁰⁰; independent scalar semigroup calculations | A sufficient gap bound on one common Hilbert space with the same vacuum and the specified operator error | An actual Yang–Mills renormalization comparison or a supplied physical scale |
| Bidirectional routes | Corrected metadata; routes of costs 8,7,5; withheld quantifier, vacuum, operator error, domain, reference bound and margin controls | Conditional reviewed Horn implications replay as intended | Semantic proof checking of natural-language mathematics |

The decisive false-measure example is exact: the equal mixture of the center elements ±I satisfies the scalar Ward residual, but the insertion f=u₀uₐ gives a nonzero SD residual 1/2. The full-family quantifier is therefore substantive. The Markov counterexample similarly blocks a specific erroneous operator-norm inference rather than merely expressing doubt.

## Retained failures and corrections

1. **Nonfinite derived statistics.** Finite samples of magnitude 10³⁰⁸ returned NaN or infinite means/uncertainties; a NaN supplied mean became a NaN statistical flag. These cases did not falsely pass, but were mislabeled as insufficient/disagreeing statistics. The fixed source rejects the invalid arithmetic. The original source and raw failure records are retained here.
2. **Empty prerequisite evidence.** The initial sampling runner accepted `successful: true` with zero executed tests and proceeded to the experiment stage. A safe sentinel reproduced this without sampling. The runner now requires all 12 named groups, no skipped/failed/errored groups and current producer hashes. The actual recorded experiment had 12 tests; its producer sources are preserved under `lattice/results/executed_sources`, and the Monte Carlo data were not rerun.
3. **Optimization-disabled exact checks.** Advisor fixture checks originally used `assert`; Python optimization removes those checks. Explicit recorded failure gates now survive both ordinary Python and `python -O`. Independently injected failures exit unsuccessfully and produce no false success artifact in either mode.
4. **Proof metadata mismatch.** The initial generic route builder assigned every starting assumption to every intermediate theorem. The existing guard correctly rejected legitimate early rules. Per-node inherited dependencies repair this without weakening the guard. The original exception text and code fragment are retained; the original full-file hash was not captured before the correction, and is explicitly marked unavailable.
5. **Transfer normalization precision and omitted acceptance field.** The transfer implementer retained a real tiny-β normalization cancellation and a deliberately perturbed diagnostic demonstrating an omitted gate. The corrected normalization preserves log Z at β=10⁻¹⁰⁰, retains its Decimal value when the positive result lies below float range, and rejects an unrepresentable scalar request. Independent checks confirm those repairs. These two issues were first identified by the implementer, not by the skeptic.

No acceptance threshold, chain seed, chain length or stochastic warmup was relaxed to obtain agreement.

## Sampling evidence and the unresolved flag

The raw data contain the six predeclared chains: hot and cold starts at β=0,0.5,2.2, each with 512 warmup sweeps and 2,048 recorded sweeps. Independent recomputation reproduced every recorded batch mean and standard error at batch sizes 16,32,64 and the direct autocorrelation estimates using a separate correlation implementation. Raw CSV hashes agree with the frozen experiment manifest.

Both β=2.2 plaquette autocorrelation estimates exceed the predeclared 64/5=12.8-sweep threshold (approximately 16.95 and 17.69). Their hot/cold comparison therefore remains **insufficient**. The Ward observables have shorter measured correlation times and their declared comparisons are statistically consistent. That does not promote the plaquette comparison or certify equilibration.

The β=0 Ward residual is identically zero and carries no sampling evidence. The tested β values do not include a positive value inside the translated rigorous strong-coupling interval 0<β_W<1/12. An experiment there remains a proposed follow-up; β=0 is its trivial endpoint.

## Source and execution scope

`source_audit_scope.json` records actual file hashes, line counts and function ranges for the reviewed lattice, transfer, advisor-fixture, stability and route sources. Source inspection is distinct from executed branch coverage. The prior general proof-search engine was reused: the verifier inspected selected assumption guards and the certificate replay function, then executed decisive new route controls. Its complete search implementation was not re-audited line by line in this round.

The primary physics sources and preprint passage were investigated by the advisor. This skeptic independently checked the supplied mathematical arguments and normalization algebra, rather than claiming a separate full literature survey. The source-context interpretation of the preprint objection remains bounded to the quoted norm-inference step.

The matrix oracle uses a different state representation from production. The main convolution reference uses Haar quadrature, not the production Bessel functions. Decimal precision is explicitly declared; these are high-precision numerical comparisons, not interval enclosures. Missing mpmath was detected before any claimed run and the reference was implemented using the standard library instead.

## Next obligation

The next mathematically substantive target is an actual gauge-invariant transfer comparison with a defined common Hilbert-space identification, vacuum matching and uniform row/column or operator-norm control. A common positive physical gap requires errors controlled relative to the temporal spacing and uniformity in the relevant volume/regulator limits. Neither finite-group rotor positivity nor finite-lattice Ward agreement supplies these premises. The earlier finite U(1)/Einstein–QED work supplies useful verification methods, but no implication that closes this nonabelian continuum problem.
