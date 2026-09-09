# Mass-gap inference audit: two reproducible counterexamples

These are exact free-scalar and positive-spectral-mixture diagnostics. **They are not Yang–Mills simulations, a new physical theory, or a solution of the Millennium Prize problem.** The purpose is to falsify two proposed inference rules before investing in a more difficult calculation:

1. “A positive finite-volume frequency that converges as the mesh is refined proves a positive infinite-volume mass gap.”
2. “A positive, apparently stable effective-mass plateau certifies a positive lower bound on the true gap.”

Both inference rules fail. The formulas below explain why; the executable arithmetic and plots make the failures reproducible.

## Run and artifacts

```bash
python3 gap_diagnostics.py --output .
python3 test_gap_diagnostics.py
```

Python, NumPy and Matplotlib are required. The scripts write three CSV files, `experiment_summary.json`, `test_results.json`, two PNG/SVG figure pairs, and a SHA-256 `manifest.json`. All computations use declared natural units and arbitrary common mass/length scales. The test file uses a separate circulant-matrix eigenvalue calculation and 100-digit Decimal exponential arithmetic; these references do not call the production formula being checked.

The original run passed **57 checks**. Some checks contain multiple reference cases (eight Decimal comparisons and 80 deterministic random spectra); those are not inflated into additional named checks. Input checks reject NaN, infinities, invalid indices, negative masses or amplitudes, all-zero weights, nonpositive spacings and nonpositive intervals. Explicitly requested frequency overflow raises an error. Underflowing correlators are handled using their logarithms and a stable divided difference rather than reporting a spurious zero mass.

## 1. A finite box can create a false mass-gap impression

For canonical coordinates on a periodic chain, consider the positive quadratic Hamiltonian

\[
H=\frac12\sum_{j=0}^{N-1}\left[p_j^2+m^2q_j^2+
\frac{(q_{j+1}-q_j)^2}{a^2}\right],\qquad q_N=q_0.
\]

This is a one-spatial-dimensional **free scalar toy model**. Its discrete Fourier modes diagonalize the Hamiltonian:

\[
\omega_k^2=m^2+\frac{4}{a^2}\sin^2\left(\frac{\pi k}{N}\right),
\qquad L=Na,\quad k=0,\ldots,N-1.
\]

The reported quantity is the lowest **nonzero-mode** frequency, \(\omega_1\). In the massless case the zero mode has frequency zero and is explicitly excluded from that diagnostic. The unconstrained massless zero mode is a free particle, not an oscillator with a normalizable oscillator ground state. It would be incorrect to label \(\omega_1\) the positive gap of that full finite-volume massless theory.

At fixed physical length \(L\), mesh refinement gives

\[
\omega_1(a,L)\longrightarrow\sqrt{m^2+(2\pi/L)^2}
\quad(a\to0,;N=L/a).
\]

For \(m=0\), this positive fixed-volume limit is \(2\pi/L\). Increasing the physical box then gives

\[
\lim_{L\to\infty}\lim_{a\to0}\omega_1(a,L)=0.
\]

The separate volume experiment holds \(a=0.125\) fixed and increases \(N\), so its lattice infrared frequency also tends to zero. These are two distinct trajectories in parameter space; a mesh-refinement test at fixed \(L\) cannot substitute for a volume test. The comparison model \(m=0.7\) tends instead to 0.7. Its full free-theory lowest oscillator excitation is already \(m\) at \(k=0\); the plotted nonzero mode is an explicitly defined diagnostic.

Actual massless values:

| Diagnostic | Computed frequency |
|---|---:|
| Fixed \(L=10\), \(N=1024\) | 0.6283175450554319 |
| Fixed-\(L\) continuum target \(2\pi/10\) | 0.6283185307179586 |
| Fixed \(a=0.125\), \(L=4\) | 1.5682742452729697 |
| Fixed \(a=0.125\), \(L=1024\) | 0.006135923001142329 |

At fixed \(L\), the expansion

\[
\frac{2}{a}\sin(\pi a/L)=\frac{2\pi}{L}
-\frac{\pi^3 a^2}{3L^3}+O(a^4)
\]

predicts second-order discretization error. The measured error ratios on successive doubling of \(N\) lie between 3.99 and 4.01. This confirms convergence of the toy formula to its finite-box target; it does not establish a volume-uniform lower bound.

## 2. A positive early plateau is not a lower-gap certificate

Let

\[
C(t)=\sum_i A_i e^{-m_i t},\qquad A_i\ge0,
\]

with at least one strictly positive amplitude, finite nonnegative masses, and \(t\ge0\). Define the supported minimum \(m_*=\min\{m_i:A_i>0\}\). The effective mass at interval \(\delta>0\) is

\[
m_{\rm eff}(t;\delta)=\frac{\log C(t)-\log C(t+\delta)}{\delta}.
\]

**Exact finite-mixture theorem.** Under these assumptions:

\[
m_*\le m_{\rm eff}(t;\delta)\le m^*,\qquad
m^*=\max\{m_i:A_i>0\},
\]

\(m_{\rm eff}\) is nonincreasing with \(t\), and tends to \(m_*\) as \(t\to\infty\). It is identically a constant when the positive-weight support contains one mass, including several terms at that same mass. For at least two distinct supported masses, it decreases strictly at finite times in exact arithmetic.

**Bound proof.** With \(w_i(t)=A_i e^{-m_i t}/C(t)\), the weights are nonnegative and sum to one. Thus

\[
\frac{C(t+\delta)}{C(t)}=\sum_iw_i(t)e^{-m_i\delta}
\in[e^{-m^*\delta},e^{-m_*\delta}].
\]

Apply \(-\log(\cdot)/\delta\). Therefore a measured effective mass is an **upper bound on the lowest mass in that operator's spectral support**. It is not a positive lower bound on that mass.

**Monotonicity proof.** Direct differentiation gives

\[
\frac{d^2}{dt^2}\log C(t)
=\sum_iw_i(t)m_i^2-\left(\sum_iw_i(t)m_i\right)^2
=\operatorname{Var}_{w(t)}(m)\ge0.
\]

Since \(\log C\) is convex, its secant slope over a fixed positive interval increases with \(t\); its negative is \(m_{\rm eff}\), which decreases. Equivalently, Cauchy–Schwarz gives

\[
C(t)C(t+2\delta)\ge C(t+\delta)^2,
\]

and hence \(m_{\rm eff}(t;\delta)\ge m_{\rm eff}(t+\delta;\delta)\). Factoring out \(e^{-m_*t}\) proves the stated late-time limit for a finite mixture. The inequality and monotonicity extend to positive spectral measures where the Laplace transforms are finite; that extension is not needed by the code.

**Hidden-state experiment.** We use

\[
C(t)=10^{-12}e^{-0.1t}+e^{-t},\qquad\delta=0.5.
\]

The terms become equal at \(t=\log(10^{12})/0.9\approx30.70113457\). Before then, a state with very small operator overlap is easy to miss.

| \(t\) | Computed \(m_{\rm eff}\) |
|---:|---:|
| 0 | 0.9999999999988635 |
| 10 | 0.9999999907898376 |
| 20 | 0.9999253755710283 |
| 30 | 0.6397568735140449 |
| 40 | 0.10016807403357479 |
| 60 | 0.10000000000256025 |
| 80 | 0.1 |

The early plateau near 1 coexists with a lowest supported mass 0.1. More generally, for any finite observation window, positive tolerance, and proposed lighter mass below 1, a sufficiently small positive amplitude hides that lighter contribution within the tolerance. A disconnected constant contribution or a zero-energy atom would drive the long-time effective mass toward zero; masses of zero are intentionally supported by the numerical function. For a physical connected vacuum correlator one must separately subtract the vacuum expectation value and prove the remaining spectral representation.

## 3. What these results do and do not connect

Positive kinetic coefficients, finite-model energy bounds, continuation theorems and conserved norms control particular classical or regulated evolutions. They do not alone construct a quantum gauge theory's Hilbert space, prove positivity after gauge constraints, identify the vacuum, or show a uniform positive energy separation above it. The positive free massless Hamiltonian is already a counterexample to the inference “positive Hamiltonian implies positive infinite-volume mass gap.”

Even if an operator's lowest supported mass were known exactly, selection rules or zero overlaps could omit lighter states elsewhere in the theory. Therefore the observed supported mass does not by itself identify the global gap. Conversely, the toy examples do **not** show that Yang–Mills has no gap, or that numerical lattice evidence is useless. They isolate missing logical requirements: a properly constructed physical theory, controlled regulator and physical-volume limits, and an appropriate positive lower bound over the relevant spectrum.

The spectral theorem above is a proof for its stated finite positive measure. The 57 passing software checks verify implementation and edge cases. Neither category turns these toy models into four-dimensional interacting nonabelian Yang–Mills theory.

## 4. Numerical implementation and audit boundaries

`effective_mass` factors out the lowest supported exponential before evaluating a ratio, uses log-sum-exp for very different amplitudes and large times, and uses `expm1`/`log1p` with a divided difference for tiny intervals. This avoids both an underflowed direct correlator and cancellation from subtracting two very large negative logarithms. For example, the direct floating-point correlator at \(t=10000\) underflows to zero, while the stable effective mass remains 0.1. A smallest-subnormal interval test also agrees with the correct limiting weighted mean.

The tests deliberately avoid interpreting a passing residual as a physics validation. The independent references validate finite arithmetic; no continuum error bound, renormalization calculation, gauge-field Monte Carlo, reflection-positivity reconstruction, or Yang–Mills spectrum was computed here. Plot axes and CSVs use the same saved finite experiment arrays. Raw source hashes identify the scripts and outputs actually delivered.

## Proposed next falsification tasks

1. Require any candidate lower-bound theorem to state its quantified domain, units, regulator dependence, physical volume and assumptions about the vacuum and spectral support.
2. Apply it to this massless toy model: if it proves a uniform positive infinite-volume gap here, its hypotheses or inference rule are wrong.
3. Apply any plateau-based inference to the hidden-state family while sweeping the lighter-state overlap, observation window and noise level.
4. If proposing a gauge-theory calculation, add genuinely gauge-theoretic construction and control of limits as explicit proof obligations. A successful ODE energy test or discrete proof-search route cannot supply those premises automatically.
