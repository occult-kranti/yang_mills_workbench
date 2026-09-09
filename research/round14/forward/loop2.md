# Loop 2 forward result: exact covariance certificates

The second loop closes the numerical-certification gap selected after the first loop. For the same declared finite SU(2) measure, exact rational arithmetic now certifies that

\[
\operatorname{Cov}_{1,1,1/4}(x,y)>0.
\]

The degree-24 certificate has exact width approximately \(1.1073\times10^{-16}\), satisfying the requested \(10^{-12}\) target. At degree 32, an outward-rounded decimal rendering of the exact rational enclosure is

\[
0.012037131325864960269805503
\;<\operatorname{Cov}_{1,1,1/4}(x,y)<\;
0.012037131325864960269805631.
\tag{16}
\]

The full rational endpoints, rather than these rounded decimal strings, are in `loop2_output/certificates.json`. The exact degree-32 width is approximately \(1.27090\times10^{-25}\). This is an interacting finite Euclidean covariance result. It does not identify a Hamiltonian ground state or establish a Yang–Mills mass gap.

## 1. The feedback that changed the calculation

Loop 1 proved \(C'(0)=v_1v_2\) and the uniform curvature estimate \(|C''|\le7\). The advisor selected two types of point. At \(\kappa_1=\kappa_2=1,\eta=\pm1/1024\), previous exact variance bounds make the local sign inequality useful. At \(\eta=1/4\), the same sufficient inequality straddles zero. Its failure does not imply that the true covariance vanishes.

The second loop therefore changes the proof method, preserving the action and observable: use exact Haar moments and a certified exponential remainder to enclose the full normalized expectation. The backward researcher computes the same Haar moments using characters. The forward researcher independently computes them using quaternion angular coordinates. Neither exact computation depends on the first loop's Bessel functions, quadrature grid or floating covariance subtraction.

## 2. Exact angular Haar moment formula

Under independent normalized Haar holonomies, \(x\) and \(y\) have density \((2/\pi)\sqrt{1-x^2}\), and the relative orientation \(c\) is uniform on \([-1,1]\). Thus

\[
z=xy-\sqrt{1-x^2}\sqrt{1-y^2}\,c.
\]

For nonnegative integers \(a,b,d\), expand the \(d\)-th power and integrate \(c\). Odd powers vanish; even powers integrate to \(1/(j+1)\). Consequently

\[
H(a,b,d):=E_0[x^ay^bz^d]
=\sum_{\substack{0\le j\le d\\ j\;\mathrm{even}}}
\frac{\binom dj}{j+1}
Q(a+d-j,j/2)Q(b+d-j,j/2),
\tag{17}
\]

where

\[
Q(n,s)=E_0[x^n(1-x^2)^s].
\]

For odd \(n\), \(Q(n,s)=0\). For \(n=2r\), substituting \(u=x^2\) gives

\[
Q(2r,s)=\frac2\pi B(r+\tfrac12,s+\tfrac32)
=\frac{2(2r)!(2s+2)!}
{4^{r+s+1}r!(s+1)!(r+s+1)!}.
\tag{18}
\]

Every term in (17) is an exact nonnegative rational. Nonzero moments require the exponents \(a,b,d\) to have matching parity. Reference values include \(H(0,0,0)=1\), \(H(2,0,0)=1/4\), \(H(4,0,0)=1/8\), and \(H(1,1,1)=1/16\). Formula (17) is separate from the character-coefficient sum used by the independent backward verifier; matching outputs therefore tests a meaningful algebraic difference rather than duplicate implementation.

## 3. Rational polynomial expectations and a uniform remainder

For rational \(\kappa_1,\kappa_2,\eta\), let

\[
S=\kappa_1x+\kappa_2y+\eta z,\quad
M=|\kappa_1|+|\kappa_2|+|\eta|,
\quad P_N(S)=\sum_{n=0}^{N}S^n/n!.
\]

For each numerator insertion \(F\in\{1,x,y,xy\}\), the exact polynomial integral is

\[
\widehat A_F=E_0[FP_N(S)]
=\sum_{i+j+k\le N}
\frac{\kappa_1^i\kappa_2^j\eta^k}{i!j!k!}
E_0[Fx^iy^jz^k].
\tag{19}
\]

Negative coefficients produce signed rational sums; the implementation never replaces them by absolute coefficients in the polynomial itself. The absolute bound is used only for the remainder. For \(N+2>M\),

\[
R_N=\frac{M^{N+1}}{(N+1)!}\frac{1}{1-M/(N+2)}
\]

controls \(|e^S-P_N(S)|\) uniformly. This follows by bounding the absolute exponential tail and observing that successive terms have ratio at most \(M/(N+2)<1\). Since each insertion has magnitude at most one,

\[
A_F=E_0[Fe^S]\in[\widehat A_F-R_N,\widehat A_F+R_N].
\tag{20}
\]

This proof handles signed couplings and does not invoke a floating exponential. At \(M=0,N=0\), the remainder is exactly zero. At \(M=N+2\), the bound's denominator vanishes; the API rejects that request instead of assigning a misleading finite error.

The normalized partition function is \(Z=A_1\). Product Haar has \(E_0[S]=0\), so convexity of the exponential supplies \(Z\ge e^{E_0[S]}=1\). The Taylor interval for \(Z\) is intersected with \([1,\infty)\). The result cannot have a zero or negative denominator.

## 4. Covariance without uncertified floating cancellation

The exact covariance is

\[
C=\frac{ZA_{xy}-A_xA_y}{Z^2}.
\tag{21}
\]

The implementation encloses the numerator with signed interval products, then divides by the strictly positive interval for \(Z^2\). An interval product takes the minimum and maximum of all four endpoint products; it does not assume that the numerator insertions have positive expectation. Rational arithmetic retains all cancellations in polynomial centers.

The interval can be wider than the true range of covariance. That is allowed: it is a sufficient enclosure, not an optimal bound. The degree-4 central interval is approximately \([-2.5872,2.2784]\), so it is explicitly inconclusive. Its upper and lower endpoints do not mean that a covariance outside \([-1,1]\) is physically possible. The algorithm simply did not intersect that coarse enclosure with the independent trivial bound.

The central refinement is:

| Degree | Covariance interval width | Sign conclusion | Requested width met? |
|---:|---:|---|---|
| 4 | 4.8656 | Inconclusive | No |
| 8 | \(1.2931\times10^{-2}\) | Positive | No |
| 12 | \(1.7833\times10^{-5}\) | Positive | No |
| 16 | \(7.6747\times10^{-9}\) | Positive | No |
| 24 | \(1.1073\times10^{-16}\) | Positive | Yes |
| 32 | \(1.2709\times10^{-25}\) | Positive | Yes |

Only the central fixture was assigned a \(10^{-12}\) width acceptance target. Other fixture intervals are valid as stored even when wider. For example the signed mixed point \((2,-1,1/2)\) at degree 24 has width about \(5.76\times10^{-12}\); the report does not claim every fixture meets the central precision target.

## 5. Certificate contract and actual failures

The certificate binds its exact action and observable scope, three rational parameters, Taylor degree, absolute exponent bound, omitted-tail index and ratio, four polynomial integrals, all interval endpoints, interval width, status and producer source hash. The verifier reconstructs every field from the parameters; equality to an arbitrary supplied hash is not the acceptance test.

Statuses have exact semantics. `certified-positive` requires a strictly positive lower endpoint; `certified-negative` requires a strictly negative upper endpoint. `certified-zero` requires the computed interval to be exactly \([0,0]\). A positive-degree factorized baseline generally has a nonzero generic Taylor remainder and is reported as an enclosure containing zero, without silently replacing the arithmetic by an analytic factorization branch. The exact \(\eta=0\) factorization theorem remains available separately.

The public exact API accepts integer, Fraction or rational-string couplings, with \(|\text{each coupling}|\le8\), total \(M\le12\), and integer degree \(0\le N\le48\). It additionally requires \(N+2>M\). Floats, Booleans, nonfinite strings, zero denominators and requests outside these implementation limits are rejected. Certificate strings must use canonical rational syntax. Exact helper intervals convert integer endpoints to Fractions before reciprocal division.

Two real validation failures were caught and repaired:

1. A public cached Haar-moment function originally validated arguments after a cache lookup. Since Python treats `True` as numerically equal to `1`, a warmed integer cache could return a result for an invalid Boolean request. Validation now occurs before dispatching to the private cached calculation. The failing source and fixture remain in `history/`.
2. Ordinary Python dictionary equality allowed `tail.first_omitted_degree=True` to match the integer value 1 in the zero-action degree-0 certificate. The backward reviewer independently identified this same weakness. Complete replay now checks recursive types as well as values, rejecting Boolean and float substitutions for integer metadata. The accepted bad certificate and original source are retained.

These are repaired software acceptance defects. They do not invalidate the conventional moment or remainder proofs. They would have weakened the claim that the delivered verifier enforces its declared input contract if left unfixed.

## 6. Executed evidence and interpretation

The producer delivers **23 exact certificates** and **136 passing producer gates**. The gates include zero degree at zero action, signed factorized baselines, the special families \(\eta=\pm1,\pm5\), all six central degrees, small signed perturbations, center transformations, a signed mixed action, a parameter family with the removable conditional \(h=0\) endpoint, and the declared parameter-domain endpoints. Mutation tests challenge missing fields, changed scope or action, wrong rational integrals, false tail bounds, zero/negative denominators, reversed intervals, false zero claims and inappropriate success labels.

The first-loop numerical code is retained unchanged. Its 1D covariance for the degree-32 central fixture is about \(2.15\times10^{-17}\) away from the exact interval midpoint and therefore lies outside the far narrower exact interval. That is expected: numerical agreement at roughly machine precision does not certify a \(10^{-25}\) enclosure. Floating containment is recorded as a diagnostic and is never used as an exact proof gate. A similar effect occurs for the narrow conditional-zero-field-family certificate.

The independent backward verifier reconstructs the Haar integrals using characters and all interval arithmetic separately. Its results and the advisor's acceptance are distinct artifacts; this producer report does not count them as its own checks. The exact proofs here are conventional mathematics with executable rational replay, not a formal proof-assistant derivation.

## 7. What the two loops achieved and what remains

The first loop proposed and tested a common observable, derived its response, and located a regime where a simple sufficient sign bound is inconclusive. The second loop used feedback to change the proof method and certify the same point with exact arithmetic. The action, measure and target observable stayed fixed across that change. This is a genuine forward/backward meeting for a finite compact subproblem.

The next useful finite task is to use these exact values as independently known fixtures for a multivariate Schwinger–Dyson/localizing-matrix hierarchy, or to add a carefully declared additional loop and derive its exact Haar geometry before scaling the certificate. The coupling deformations do not by themselves remove the separate open obligations of pure four-dimensional Yang–Mills: the intended action and dimensions, uniform volume control, continuum construction, reconstruction hypotheses and a nonzero physical spectral threshold. Adding an arbitrary coefficient cannot stand in for any of those proofs.

## Reproduce

```bash
python test_loop2.py
python -O test_loop2.py --output loop2_output_optimized
python plot_loop2.py
```

`loop2_output/certificates.json` contains replayable rational evidence. `certificate_summary.csv` includes exact endpoints and separate rounded display columns; `floating_diagnostics.csv` preserves the floating comparisons without promoting them to proof. The source ledger is the first-loop primary-source ledger plus the explicitly derived angular/Beta and exponential-tail arguments above. This loop does not claim an additional exhaustive literature survey.
