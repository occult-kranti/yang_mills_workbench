# A certified single-plaquette SU(2) study

This executable result concerns one spatial square with four SU(2) links and its gauge-invariant class-function Hilbert space. The representation tower is infinite; the spatial graph is fixed. It is not a construction of continuum four-dimensional Yang–Mills.

## What the variables mean

The Hamiltonian in normalized characters `chi_(n/2)`, n=0,1,..., is

\[
 H_{nm}=[\alpha n(n+2)+\lambda]\delta_{nm}
       -\frac{\lambda}{2}(\delta_{n,m+1}+\delta_{n,m-1}).
\]

Here alpha>0 is the electric energy coefficient after summing four link Casimirs, and lambda>=0 multiplies the plaquette potential `1-(Tr U)/2`. Thus lambda changes an existing gauge-invariant magnetic interaction. It is not a fitted mass term. `N` is the number of retained characters, n=0,...,N-1. It is neither lattice spacing nor spatial volume.

The normalized radial map sends a class wavefunction to a multiple of `sin(theta) f(theta)`, with Dirichlet endpoints on (0,pi). The same operator becomes

\[
 -\alpha\frac{d^2}{d\theta^2}-\alpha+\lambda(1-\cos\theta).
\]

This supplies a genuinely separate finite-difference implementation. Its numerical errors are measured, not certified by interval arithmetic.

## Exact infinite-tail enclosure

Let A be the N-character compression. The discarded tail begins at n=N and has quadratic-form lower bound `tau=alpha*N*(N+2)` because the compressed magnetic potential is nonnegative. Only the last retained character couples to the tail, with strength c=lambda/2.

Choose a rational U with `upper_eig1(A)<U<tau` and put

\[
 d=\frac{c^2}{\tau-U},\qquad B=A-d|N-1\rangle\langle N-1|.
\]

Completing the square in the cross coupling proves the form inequality

\[
 B\oplus UI\ \le H.
\]

Rayleigh–Ritz gives the opposite eigenvalue comparison from A. For k=0,1, since `eig1(B)<U`,

\[
 \lambda_k(B)\le E_k(H)\le\lambda_k(A).
\]

Exact Fraction Sturm determinant sign counts and rational bisection enclose the two eigenvalues of both finite matrices. The resulting gap interval is

\[
 [\underline\lambda_1(B)-\overline\lambda_0(A),
   \overline\lambda_1(A)-\underline\lambda_0(B)].
\]

`verify_certificate` reconstructs the matrices, replays the endpoint counts and checks every tail, energy, gap, scope, precision and positivity field. It is an arithmetic verifier conditional on the proved operator reduction and inequalities, not a general formal proof kernel. The local float eigensolver never supplies a certificate endpoint.

## A complete continuous coupling interval

The bounded potential obeys `0<=V<=2`. Min–max therefore gives, for h>=0, `0<=E_k(lambda+h)-E_k(lambda)<=2h`. Subtracting the two energy shifts gives the gap Lipschitz bound

\[
 |\Delta(\lambda+h)-\Delta(\lambda)|\le2|h|.
\]

Exact point certificates at lambda=0,2,4,6,8,10 and closed radius-one cells cover the whole interval [0,10]. Subtracting two from the smallest certified point lower bound proves, at alpha=1,

\[
 \boxed{\Delta(\lambda)\ge999999/1000000>0\quad(0\le\lambda\le10).}
\]

`verify_continuous_range` checks the coverage and point-certificate dependencies using rational arithmetic, including exact centers, per-cell radii and alpha. By the exact identity `H(alpha,lambda)=alpha H(1,lambda/alpha)`, the bound scales to `Delta>=0.999999*alpha` when `0<=lambda<=10*alpha`. This does not retain a positive constant when alpha tends to zero, and does not define a Yang–Mills continuum trajectory.

The separate lambda=100 study contracts the certified gap width from about 6.057 at N=8 to 1.29e-12 at N=24. A converged matrix eigenvalue by itself would not supply the infinite-tail bound.

## A changing continuous coupling and its energy cost

The driven numerical protocol is alpha=1, `lambda(t)=5[1-cos(pi*t/2)]`, 0<=t<=2, initial character chi_0. Its exact finite-Galerkin work identity is

\[
 \frac{d}{dt}\langle H(t)\rangle
 =\dot\lambda(t)\langle1-\cos\theta\rangle.
\]

DOP853 integrates both the state and external work. A separate unitary midpoint exponential scheme integrates work by Simpson quadrature using actual state expectations and the imposed lambda derivative. Neither implementation defines work by subtracting endpoint energies.

The final N=24 energy change is approximately 6.07229637263, equal to integrated external work within the recorded numerical tolerance. Omitting the work term leaves a defect of that size. DOP853 tolerance refinement and N=16 to 24 refinement are distinct axes. The independent midpoint final state discrepancy is approximately 7.74e-7, with observed second-order convergence. Small last-character occupancy is recorded as a diagnostic, not an a posteriori bound on the exact infinite-dimensional evolution. Stationary tail certificates do not certify driven evolution.

## Reproduce and inspect

Python dependencies: NumPy, SciPy and Matplotlib. No symbolic-computation package or network access is needed.

```bash
python run_study.py
python test_solver.py
python -O test_solver.py
```

`output/stationary_certificates.json` retains full rational strings. `continuous_range_certificate.json` binds the interval-wide theorem to these exact records. `stationary_intervals.csv` and plots use float display conversions; the exact JSON remains authoritative. `radial_comparison.csv` gives four grid resolutions and independent Mathieu characteristic-value comparisons. Raw driven histories, integrated work and comparisons are saved separately.

The special-function oracle is `E_k=lambda-alpha+(alpha/4)*b_(2k+2)(-2lambda/alpha)`, where b is the odd Mathieu characteristic value. The advisor cross-checked the reduction against [Bauer et al., Appendix B](https://arxiv.org/abs/2307.11829). This oracle is independent floating arithmetic, not a rigorous enclosure.

## Acceptance and retained corrections

The original study contract set stationary enclosure width below `1e-8*max(1,gap)`, finest radial mixed relative error below 1e-4, radial order in (1.8,2.2), DOP853 norm/work defects below 1e-8, tolerance and character-refinement state discrepancies below 1e-7, and independent midpoint state error below 1e-4 with order in (1.7,2.3).

Independent review then found two real evaluator defects. First, certificate replay accepted changed scope/precision/Boolean metadata while the numerical endpoints were unchanged. Second, midpoint work defects were recorded but not gated, allowing a deliberately omitted-work implementation to pass the existing dynamics checks. Both were repaired. Review-added midpoint work and norm gates use 1e-4 and 1e-8 respectively, plus a resolved work-refinement order. These extra gates were added after inspecting the original run; they are not described as preregistered.

All gates use explicit exceptions and run under `python -O`. The producer clears its gate list, marks validation as running before computation, marks failed reruns as failed, and requires frozen source hashes to agree before reporting success. The separate skeptic directory retains the original failing versions and independent checks. These repairs strengthen result integrity; they do not establish a four-dimensional physical mass gap.
