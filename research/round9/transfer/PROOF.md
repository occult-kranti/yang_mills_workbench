# Exact SU(2) central convolution: a proved benchmark and a blocked bridge

Research round 9, 9 September 2026. This is a self-contained derivation for a specified compact-group operator. It is a replication of standard harmonic analysis, not a new proof of four-dimensional Yang–Mills existence or its mass gap. Numerical verification records are in `output/validation.json`; independent review is recorded separately by the skeptic.

## 1. Contract and distinctions

Let Haar measure on SU(2) be normalized to one and fix a real number β>0. Define

\[
(T_\beta f)(U)=\int_{SU(2)}k_\beta(UV^\dagger)f(V)\,dV,
\qquad
k_\beta(W)=\frac{\exp[\beta\operatorname{ReTr}(W)/2]}{Z_\beta},
\]
\[
Z_\beta=\int_{SU(2)}\exp[\beta\operatorname{ReTr}(W)/2]dW.
\]

The Hilbert space is the complete, infinite-dimensional \(L^2(SU(2),dU)\). A finite list of representations is used only for numerical display; the proof includes all spins. β is an abstract kernel parameter here; its identification with a Yang–Mills bare coupling has not been established. An independently chosen positive time step \(a_t\) defines \(H_{\beta,a_t}=-a_t^{-1}\log T_\beta\) by spectral calculus.

Four separate notions must be kept distinct: the pointwise sign of a kernel, positive semidefiniteness of its integral operator, the Markov gap \(1-r_1\), and the generator energy gap \(-\log r_1/a_t\). We will prove operator positivity for β>0 through its full spectrum. Pointwise positivity alone is insufficient, as the negative-β counterexample shows.

## 2. Haar measure, characters and normalization

Write a group element as \(W=\cos\theta\,I+i\sin\theta\,\widehat n\cdot\boldsymbol\sigma\), with \(0\leq\theta\leq\pi\). SU(2) is the unit three-sphere; integrating the angular direction on its two-sphere gives the class-function measure

\[
d\mu(\theta)=\frac{2}{\pi}\sin^2\theta\,d\theta,
\qquad \int_0^\pi d\mu=1.
\]

For spin \(j=0,\tfrac12,1,\ldots\), let \(n=2j+1\) be the representation dimension. The character is

\[
\chi_j(\theta)=\frac{\sin(n\theta)}{\sin\theta}.
\]

The endpoint values are removable limits; the integrated numerator is \(\sin\theta\sin(n\theta)\), so direct quadrature need not divide by \(\sin\theta\). The SU(2) character and dimension follow from the symmetric-power construction described by Woit. His integer label is the highest weight \(2j=n-1\), not our dimension n. [S1]

The integer-order Bessel integral and recurrence give [S2, S3]

\[
\begin{aligned}
c_j(\beta)&=\int_{SU(2)}e^{\beta\cos\theta}\chi_j(\theta)dU\\
&=\frac{2}{\pi}\int_0^\pi e^{\beta\cos\theta}\sin\theta\sin(n\theta)d\theta\\
&=I_{n-1}(\beta)-I_{n+1}(\beta)
=\frac{2n}{\beta}I_n(\beta).
\end{aligned}
\]

In particular \(Z_\beta=c_0(\beta)=2I_1(\beta)/\beta\). This step fixes both the factor two and Bessel order. Omitting the \(\sin^2\theta\) Haar weight gives a different problem.

## 3. Exact spectrum, including multiplicities

The kernel is a real central function satisfying \(k(W^{-1})=k(W)\). Its integral operator is compact and self-adjoint. Peter–Weyl decomposes \(L^2(SU(2))\) into the orthogonal blocks of matrix coefficients of the irreducible representations. A dimension-n block has dimension \(n^2\). A central convolution acts as a scalar on each such block, and Schur orthogonality gives that scalar as \(c_j/(nZ_\beta)\), not \(c_j/Z_\beta\). Thus

\[
\boxed{r_j(\beta)=\frac{I_{2j+1}(\beta)}{I_1(\beta)},\qquad
\mathrm{multiplicity}=(2j+1)^2.}
\]

One can see the division by n without assuming it: the matrix \(\int k(W)D^j(W^{-1})dW\) commutes with the irreducible representation, so it is scalar. Taking its trace gives n times the scalar, while the trace integral is \(c_j/Z_\beta\). Completeness of the matrix coefficients ensures no additional spectral sector has been omitted. [S4]

On the invariant subspace of class functions there is one character per spin, hence one eigenfunction per eigenvalue. This restriction is invariance under one simultaneous conjugation \(U\mapsto gUg^{-1}\). It is **not** invariance under the independent endpoint gauge actions on an open lattice link. Requiring \(f(g_LUg_R^{-1})=f(U)\) for arbitrary independent \(g_L,g_R\) forces f to be constant. Accordingly the rotor's j=1/2 excitation is not a glueball or a nontrivial physical excitation of a lone open link after local gauge projection.

## 4. Strict positivity and the first excited eigenvalue

The power series

\[
I_n(\beta)=\sum_{k=0}^\infty\frac{(\beta/2)^{n+2k}}{k!(n+k)!}
\]

has positive terms for β>0, so all \(r_j>0\). To identify the largest nonconstant eigenvalue for every β, a sampled order check is inadequate. Use the positive integral representation, valid for \(\nu>-1/2\), and its derivative recurrence: [S2, S3]

\[
I_\nu(\beta)=\frac{(\beta/2)^\nu}{\sqrt\pi\Gamma(\nu+1/2)}
\int_{-1}^1e^{\beta t}(1-t^2)^{\nu-1/2}dt,
\qquad I_\nu'=I_{\nu+1}+\frac\nu\beta I_\nu.
\]

Logarithmic differentiation, justified on this bounded integration interval, gives

\[
\frac{I_{\nu+1}(\beta)}{I_\nu(\beta)}
=\frac{\int_{-1}^1 t e^{\beta t}(1-t^2)^{\nu-1/2}dt}
{\int_{-1}^1 e^{\beta t}(1-t^2)^{\nu-1/2}dt}.
\]

This is the mean of t for a positive probability density supported on (-1,1), hence is strictly less than 1. Its numerator is strictly positive: pairing ±t changes it into \(\int_0^1t(e^{\beta t}-e^{-\beta t})(1-t^2)^{\nu-1/2}dt>0\). Therefore \(0<I_{\nu+1}/I_\nu<1\) and

\[
1=r_0>r_{1/2}>r_1>r_{3/2}>\cdots>0.
\]

For fixed β, \((n+k)!\geq n!(n+1)^k\) gives

\[
I_n(\beta)\leq\frac{(\beta/2)^n}{n!}
\exp\!\left(\frac{\beta^2}{4(n+1)}\right),
\]

so \(r_j\to0\) as \(j\to\infty\). Consequently zero is in the operator's spectrum as an accumulation point, but is not an eigenvalue when β>0. The operator is strictly positive on every nonzero vector but is not bounded below by a positive multiple of the identity. Its unique stationary state is the constant function.

The exact two gaps are

\[
\boxed{\gamma_\beta=1-\frac{I_2(\beta)}{I_1(\beta)}>0,\qquad
\Delta_{\beta,a_t}=-\frac1{a_t}\log\frac{I_2(\beta)}{I_1(\beta)}>0.}
\]

The generator is defined on the dense domain of coefficient sequences obeying \(\sum_{j,m,n}E_j^2|f^j_{mn}|^2<\infty\), with \(E_j=-\log r_j/a_t\). Its eigenvalues tend to infinity at fixed β. None of these statements is a four-dimensional quantum field construction.

## 5. An independent weaker bound

Since \(k_\beta(W)\geq\epsilon_\beta=e^{-\beta}/Z_\beta>0\), write

\[
T_\beta=\epsilon_\beta P+(1-\epsilon_\beta)R,
\]

where P averages to the constant function and R has a nonnegative normalized convolution kernel. Jensen's inequality and Haar invariance show \(\|R\|_{2\to2}\leq1\). On the orthogonal complement of constants, P vanishes, so \(\|T_\beta\|\leq1-\epsilon_\beta\). Thus

\[
\gamma_\beta\geq\epsilon_\beta=\frac{\beta e^{-\beta}}{2I_1(\beta)}\geq e^{-2\beta}.
\]

The last inequality uses \(Z_\beta\leq e^\beta\). This bound is rigorous but much weaker at large β: \(\epsilon_\beta\sim\sqrt{\pi/2}\,\beta^{3/2}e^{-2\beta}\), whereas \(\gamma_\beta\sim3/(2\beta)\). Its logarithm is stored to avoid underflow.

## 6. Limits and a concrete missing inference

At β=0 exactly, \(k=1\) and T=P; all nonconstant eigenvalues vanish. The code explicitly labels those zeros as the exact projection limit and supplies no finite excited generator energy. At small positive β and fixed n,

\[
r_j\sim\frac{(\beta/2)^{n-1}}{n!},
\qquad r_{1/2}\sim\beta/4,
\qquad -\log r_{1/2}\sim\log(4/\beta).
\]

At large β and fixed n, the standard Bessel large-argument expansion gives [S5]

\[
I_n(\beta)=\frac{e^\beta}{\sqrt{2\pi\beta}}
\left[1-\frac{4n^2-1}{8\beta}+O(\beta^{-2})\right],
\]
\[
-\log r_j=\frac{n^2-1}{2\beta}+O(\beta^{-2})
=\frac{2j(j+1)}\beta+O(\beta^{-2}).
\]

The O term is at fixed representation; no uniformity in j is claimed. The first energy gap therefore scales as \(\Delta\sim3/(2\beta a_t)\). Even requiring both \(\beta\to\infty\) and \(a_t\to0\) does not select a nonzero limiting gap. In chosen time units, let \(a_t=\beta^{-p}\):

| Path | First energy gap | Limit |
|---|---|---|
| p=1/2 | \(\Delta\sim(3/2)\beta^{-1/2}\) | zero |
| p=1 | \(\Delta\to3/2\) | finite positive |
| p=3/2 | \(\Delta\sim(3/2)\beta^{1/2}\) | infinite |

All finite-β operators in the three paths are identical before a time scale is assigned. This disproves the inference “a positive gap at each regulator implies a finite nonzero continuum gap.” It does not prove that Yang–Mills follows any of these arbitrary rotor scaling trajectories. A continuum Yang–Mills argument must identify its physical renormalization trajectory and establish the needed uniform control on that trajectory.

### A complete continuum-time link for this rotor

One can prove more than a finite list of coefficient limits. Suppose β→∞, a_t→0 and βa_t→c∈(0,∞). Let the nonnegative SU(2) Casimir operator \(\mathcal C\) have eigenvalue \(j(j+1)\) on the spin-j matrix coefficients. Then, for every fixed t≥0,

\[
T_\beta^{\lfloor t/a_t\rfloor}f\;\longrightarrow\;
e^{-(2t/c)\mathcal C}f
\quad\text{in }L^2(SU(2))\quad\text{for every }f\in L^2(SU(2)).
\]

Indeed, for each fixed spin, the preceding expansion implies \(\lfloor t/a_t\rfloor\log r_j\to-2t j(j+1)/c\). Both the approximate and limiting spectral multipliers lie in [0,1]. The squared difference on each coefficient is therefore bounded by four times that coefficient's squared modulus. Peter–Weyl square-summability and dominated convergence prove the strong operator limit on the whole Hilbert space. This argument needs no uniform large-spin asymptotic. It establishes strong convergence, not operator-norm convergence. The limiting rotor generator is \(2\mathcal C/c\) and has gap \(3/(2c)\). This is a proved continuum-time compact-group quantum-mechanical limit; spatial field degrees of freedom and the Yang–Mills continuum-space obligations remain absent. The independent skeptic checked this additional derivation; it requires no new production-code claim.

## 7. Pointwise positive kernel with a negative eigenvalue

As a disallowed-domain control, take β=−b<0. The kernel \(e^{-b\cos\theta}/Z_b\) is still strictly pointwise positive and normalized. Integer-order Bessel parity gives

\[
r_j(-b)=(-1)^{n-1}\frac{I_n(b)}{I_1(b)}.
\]

For j=1/2, n=2, this is negative. The same sign follows directly by changing \(\theta\mapsto\pi-\theta\) in the Haar/character integral. Taking the normalized character \(f=\chi_{1/2}\) yields \(\langle f,T_{-b}f\rangle=r_{1/2}(-b)<0\). It is therefore false that pointwise positivity of a Euclidean kernel alone proves positive semidefiniteness or reflection positivity. The counterexample is tested independently by direct quadrature; the positive-transfer API rejects negative β.

## 8. Bidirectional proof obligations

Forward route: normalized SU(2) Haar → exact character coefficients → Schur factor and full Peter–Weyl completeness → positive ordered spectrum → exact rotor gap.

Backward route from a desired four-dimensional Yang–Mills gap: a nontrivial continuum local quantum field theory and its physical Hilbert space → regulator-independent renormalization trajectory and spatial infinite-volume limit → physical transfer operator with gauge projection and spatial interactions → uniform spectral/decay estimates along that trajectory.

These routes do not meet in this benchmark. The missing edges are precise: spatial plaquette interaction, local gauge projection, continuum-field existence, infinite-volume control, and a uniform physical gap estimate. Adding an adjustable time step or a fitted mass term does not supply any of them. The exact rotor is useful for checking Fourier coefficients, normalization, positivity logic and numerical underflow before attacking those obligations.

## 9. Reproduction and test interpretation

Run `python run_benchmark.py` in this directory. Dependencies are NumPy, SciPy and Matplotlib; the standard-library Decimal supplies the independent high-precision series. The run also succeeds with `python -O run_benchmark.py` because acceptance uses explicit exceptions rather than removable assertions.

The delivered run evaluates 92 gates: exact limits, positivity/order samples, 80-digit series comparisons, independent Haar quadrature and refinement, asymptotics, normalization/order mutants, multiplicities, invalid domains, and underflow/overflow. These are distinct from mathematical proof and from independent skeptic review. Checks bind before/after SHA256 hashes of both Python files. Every promised case is evaluated before pass status is formed; failures create `output/failure.json` and stop execution.

The numerical API is intentionally bounded: 0≤β≤10⁶, integer 1≤n≤4096. A scaled-Bessel underflow or invalid ratio triggers the positive Decimal series for β≤1000 and explicit rejection beyond that fallback range. Subnormal Bessel values are not trusted. A positive eigenvalue smaller than floating range is returned as `ratio=None`, with a finite logarithm, Decimal string and explicit status; it is never converted to a mathematical zero. Likewise, if positive log Z is below floating range, the reference retains its Decimal value and an explicit status, while the float-only normalization API rejects it. The requested Decimal precision is 80 digits in the reference tests; actual working precision adds guard digits and enough digits to resolve Z−1 at tiny β, and is recorded. These are high-precision numerical references with an estimated positive-series truncation tail, not certified interval enclosures.

Two self-audited flaws were corrected before final source freeze. First, fixed working precision erased the normalization correction at β=10⁻¹⁰⁰ before taking log Z; adaptive precision fixes it. Second, the Haar gate recorded normalization error but initially omitted it from its acceptance condition. `retained_failures.py` reproduces the former and demonstrates the latter with an explicitly constructed perturbed diagnostic. The original run's actual normalization comparisons were accurate; this was a latent acceptance defect rather than evidence that those data were wrong. The independent skeptic requested an additional rejection/Decimal-retention test below the float range, which is included.

Direct Haar quadrature is a separate double-precision formulation, validated only on its stated cases and β range. It can suffer cancellation for tiny character coefficients and does not claim to establish their sign in that regime. Exact sign is supplied by the analytic theorem; the Decimal series provides a numerical reference when needed. The benchmark freezes the physical β while refining θ nodes. The joint-limit plot deliberately changes the model's time scaling and is labeled as a physical-path comparison, not numerical mesh convergence.

Both PNGs were opened and visually inspected: axes, legends, titles and CSV data labels are visible. The supplied plots are static artifacts, not fitted mass-gap evidence.

## 10. Source ledger and reading depth

Only the specific supporting sections were used; this ledger does not claim exhaustive reading of all Yang–Mills literature.

| ID | Source | Actual reading depth and use |
|---|---|---|
| S1 | [Woit, SU(2) Representations and Their Applications](https://www.math.columbia.edu/~woit/notes10.pdf) | Read extracted representation construction, dimensions, Casimir and character formula on pages 1–3. Notation converted from highest weight to dimension; no physics conclusions from its later survey were used. |
| S2 | [NIST DLMF 10.32](https://dlmf.nist.gov/10.32) | Read equations 10.32.2 and 10.32.3 and their domains. Used the real positive integral and integer-order Fourier integral; did not rely on later product-integral sections. |
| S3 | [NIST DLMF 10.29](https://dlmf.nist.gov/10.29) | Read equations 10.29.1 and 10.29.2, including both derivative forms; used recurrence and derivative only. |
| S4 | [Peter–Weyl lecture notes](https://www.math.ksu.edu/~dav/EFT-F23/PeterWeylLec%2023-24.pdf) | Read extracted convolution definition, compactness/self-adjointness result, and Peter–Weyl/class-function statements. Standard theorem is assumed and applied; not formalized in a proof assistant. |
| S5 | [NIST DLMF 10.40](https://dlmf.nist.gov/10.40) | Read fixed-order large-argument expansion and its stated sector. Only leading correction used; no uniform large-order remainder was asserted. |
| S6 | [SciPy ive documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.ive.html) | Read exponential-scaling definition, AMOS algorithm notes and overflow example. This motivates scaled evaluation but is not an error bound on every input. |
| S7 | [Woit, Weyl Integral and Character Formulas](https://www.math.columbia.edu/~woit/notes12.pdf) | Read normalized character orthogonality and conjugation-invariant Weyl integral formula, pages 1–2. Used to cross-check normalization and conjugation scope. |

The older Columbia course link to `repthynotes3.pdf` returned 404; it was not read and supplies no evidence. No new external skill was installed. The existing local numerical-validation skill was read and applied to completeness gates, independent formulations, precision, source hashes and separation of physical/numerical limits.
