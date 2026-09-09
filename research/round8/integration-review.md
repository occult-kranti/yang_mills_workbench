# Review 8 scientific integration verdict

**Verdict: accept the current mathematics and computed examples within their explicit scope. No blocking scientific defect was found.** This review inspected the diagnostic source, test source, saved results, CSV files, manifest, README and the scientific text in `physics-observatory/dist/research-millennium.js`. It did not rerun the writing test harness or edit the diagnostic/site files. Fresh independent checks were read-only.

## Periodic diagnostic: accepted with its stated boundary

The implementation uses the periodic one-dimensional free-scalar dispersion

\[
\omega_k^2=m^2+\frac4{a^2}\sin^2(\pi k/N),\qquad L=Na.
\]

This differs from the advisor's earlier proposed Dirichlet benchmark, but is a valid alternative because the UI and README explicitly call the plotted quantity the **lowest nonzero-momentum frequency**, with the homogeneous massless mode excluded from that diagnostic. They do not call it the full finite-volume theory's gap. The README also correctly notes that the unconstrained massless homogeneous mode is a free particle, without a normalizable oscillator vacuum.

At fixed L, the massless frequency tends to \(2\pi/L\) on mesh refinement; on increasing L it tends to zero. The CSV volume sweep actually holds a=0.125 fixed while increasing N. That is a separate path from first taking the continuum limit at every L, and the README correctly distinguishes these paths. Both the exact formula and that fixed-spacing path show the intended infrared frequency vanishing. The massive m=0.7 control tends to m; its plotted k=1 frequency is not the full theory's k=0 excitation gap.

Fresh checks compared every stored frequency with the separately evaluated cosine form of the dispersion: 18 volume rows and 16 fixed-volume rows agreed within 1.60e-13 and 5.61e-13, respectively. The cosine reference itself loses some precision at small angle; these discrepancies do not indicate a defect in the stable sine implementation.

## Spectral example and theorem: accepted

The executed model is

\[
C(t)=10^{-12}e^{-0.1t}+e^{-t},\qquad\delta=0.5,
\]

not the earlier advisor's illustrative parameters. The data and explanations are consistent with the executed model. Equal contributions occur at t=30.7011345733. The early effective mass is nearly 1 and its late limit is 0.1. Fresh independent 80-digit Decimal calculations checked **all 321 CSV effective-mass values**, with largest absolute difference 6.67e-16.

The exact inequality \(m_{\rm eff}\ge\inf\operatorname{supp}\mu\) and nonincreasing behavior follow from positivity and log-convexity as stated. They bound the supported threshold from above, not below. They do not identify the full theory's gap when an operator misses lighter sectors. Finite-temperature wraparound and signed correlators are correctly excluded from the displayed argument.

The uniform exponential-bound implication is also correct. For a positive diagonal semigroup correlator, weight below a proposed common rate contradicts an upper exponential bound at arbitrarily large physical time. With a densely spanning family of vacuum-subtracted states, the bounded spectral projection below that rate vanishes on the physical vacuum-orthogonal space. The UI correctly keeps reconstruction, continuum convergence, positivity, dense channel coverage, nontriviality and regulator-independent bounds as unproved Yang–Mills premises. A measured finite-window plateau supplies none of these premises by itself.

## Yang–Mills convention: accepted

With Hermitian generators satisfying \([T^a,T^b]=if^{abc}T^c\) and \(\operatorname{Tr}T^aT^b=\delta^{ab}/2\), the UI convention

\[
F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu-ig[A_\mu,A_\nu],
\qquad S_E=\frac12\int\operatorname{Tr}F_{\mu\nu}F_{\mu\nu}
\]

is consistent: it gives \(S_E=\frac14\int F^a_{\mu\nu}F^a_{\mu\nu}\), with g inside the curvature. An additional prefactor 1/g² would mix conventions. For a general compact simple group, “Tr” should be read as the chosen normalized invariant quadratic form; the displayed fundamental matrix trace is directly standard for the SU(2)/SU(3) examples. The one-loop QED and pure Yang–Mills coefficients in the UI have the correct sign and \(\mu\,d/d\mu\) convention.

## Evidence and minor copy notes

- The stored test report contains **57 passing named checks**. This review inspected that report and its harness, but does not count those as 57 fresh reruns. All 12 manifest file hashes matched when independently checked.
- Nonblocking copy precision: where the README says a “measured effective mass” is an upper bound, “the exact effective mass of this positive correlator” is more precise. Noise, fits and subtraction errors can violate the mathematical premises; the displayed theorem itself is correct.
- Nonblocking test-comment defect: the comment above the 80 randomized spectra says they include a zero-energy atom, but the sampled masses come from a continuous uniform distribution and no atom at zero is deliberately inserted. Separate explicit reference/control cases do include zero masses, so this does not invalidate the reported checks. Remove that phrase from the random-loop comment or add the advertised case.
- No claim of exhaustive branch coverage, a new physical discovery, a formally checked theorem, or a Yang–Mills solution is warranted. The current UI appropriately distinguishes these limits.

