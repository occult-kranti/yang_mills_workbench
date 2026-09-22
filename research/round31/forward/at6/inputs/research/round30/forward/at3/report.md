# Hruday finite Euclidean readout certificate — AT3 forward

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted independent forward execution, without reading current AT3 reverse or skeptic solutions. HNM tags are project aliases for this application of established quadrature and spectral methods. Scientific priority is unverified.

**Outcome:** the frozen design certifies a conditional AQ inverse-form readout with interval width below 1/500 for exact rational reported data meeting its error contract. Its two executed abstract fixtures pass, including all-positive/all-negative sample errors; their worst-case output envelopes are disjoint. **No actual AQ correlation samples or actual AQ inverse value have been produced.**

## 1. Actual-state conditional theorem and physical clock

Use exactly AT1/AT2's actual AQ centered Wilson spectral measure eta in dimensionless energy x=E/alpha. Its inherited hypotheses are support x>=a=1/16, mass `m<=M=63/250`, first moment `u<=U=94/125`, and finite second moment `v<=B=36+98|tau|`. To avoid confusing Euclidean duration with mass, denote mass by m in this report and duration by s. Define

\[
C(s)=\int e^{-sx}\,d\eta(x),\qquad
I=\int_0^\infty C(s)\,ds=\int x^{-1}d\eta(x)=\alpha R.
\tag{HNM-AT3-F01}
\]

Positivity permits Tonelli, and x>=a>0 gives I<=M/a<infinity. Here R is precisely AT2's reduced inverse-energy quadratic form, not a thermodynamic susceptibility. In physical Euclidean time,

\[
s=\alpha t_E/\hbar,\quad C_{phys}(t_E)=C(\alpha t_E/\hbar),\quad
R=\hbar^{-1}\int_0^\infty C_{phys}(t_E)\,dt_E.
\tag{HNM-AT3-F02}
\]

The frozen design is

\[
T=128,\quad h=1/32,\quad N=4096,\quad Nh=T,\quad
\epsilon=10^{-6},\quad N+1=4097.
\tag{HNM-AT3-F03}
\]

Thus the physical endpoint is `128 hbar/alpha` and the physical sample spacing is `hbar/(32alpha)`. Sample errors are deterministic absolute errors on dimensionless C(s), not Gaussian noise, independent random errors or confidence intervals. This protocol supplies no claim that obtaining those data is experimentally or computationally feasible.

## 2. Differentiability and integrated curvature from actual moments

Since m,u,v are finite, dominated convergence on each compact nonnegative duration interval yields right derivatives at zero and ordinary derivatives thereafter:

\[
C'(s)=-\int x e^{-sx}d\eta(x),\qquad
C''(s)=\int x^2e^{-sx}d\eta(x)\ge0.
\tag{HNM-AT3-F04}
\]

Continuity of C'' at zero follows from domination by the integrable x^2. There is no third-moment assumption. More usefully than a pointwise supremum, Tonelli gives

\[
\int_0^T C''(s)\,ds=\int x(1-e^{-Tx})d\eta(x)\le u\le U.
\tag{HNM-AT3-F05}
\]

Only nonnegative integrands are interchanged. The second moment justifies C^2 regularity; the final quadrature constant uses the smaller integrated first moment U.

## 3. Exact Peano identity and quadrature sign

On cell `[jh,(j+1)h]`, take `k_j(s)=(s-jh)((j+1)h-s)/2`. It vanishes at both endpoints, with derivatives h/2 and -h/2 there and second derivative -1. Two integrations by parts yield

\[
\frac h2[C(jh)+C((j+1)h)]-\int_{jh}^{(j+1)h}C(s)ds
=\int_{jh}^{(j+1)h}k_j(s)C''(s)ds.
\tag{HNM-AT3-F06}
\]

The kernel satisfies `0<=k_j<=h^2/8` throughout the continuous cell. Summing and using (F05), with `Trap(C)=h(C(0)/2+sum_(j=1)^(N-1) C(jh)+C(T)/2)`, proves

\[
0\le\operatorname{Trap}(C)-\int_0^T C(s)ds
\le Q:=h^2U/8=47/512000.
\tag{HNM-AT3-F07}
\]

The trapezoid rule overestimates the finite integral because C is convex. Treating Q as an amount to add to a lower endpoint gives the wrong sign. No observed mesh convergence or finite positivity grid supplies this theorem.

## 4. Infinite-time tail and deterministic sample budget

Support above a gives

\[
0\le\int_T^\infty C(s)ds
=\int e^{-Tx}x^{-1}d\eta(x)
\le D:=\frac{M}{a}e^{-aT}=\frac{504}{125}e^{-8}.
\tag{HNM-AT3-F08}
\]

For reported real samples y_j satisfying `|y_j-C(jh)|<=epsilon`, all trapezoid weights are positive and sum hN=T. Therefore

\[
|\operatorname{Trap}(y)-\operatorname{Trap}(C)|\le T\epsilon
=2/15625=:J.
\tag{HNM-AT3-F09}
\]

The vectors with every error +epsilon and every error -epsilon attain +J and -J. A root-N allowance would be invalid for this deterministic model. Combining (F07)-(F09) yields the conditional interval

\[
I\in[\operatorname{Trap}(y)-Q-J,\ \operatorname{Trap}(y)+D+J].
\tag{HNM-AT3-F10}
\]

For arithmetic enclosures `y_j in [l_j,r_j]`, use the corresponding positive-weight lower and upper sums P_-,P_+. With a proved rational upper D_+ for D,

\[
I\in[P_--Q-J,\ P_++D_++J],\quad
\text{width}=(P_+-P_-)+Q+D_++2J.
\tag{HNM-AT3-F11}
\]

The arithmetic width is separate from the physical/sample error budget. The API never treats unknown exponential roundoff as free. For exact rational y_j the arithmetic width is zero. The certified error calculation gives `Q+D_++2J<170039/100000000<1/500`. For the executed enclosures their extra width is below 10^-24, so the frozen width target also passes.

## 5. Directed rational exponential arithmetic and complete node semantics

The arithmetic scale `G=10^30` was fixed in evaluator.py before generating any fixture outcome. To enclose exp(-y) for rational y>=0, choose k so r=y/2^k<=1/2. The alternating exponential Taylor terms decrease in absolute magnitude. Consequently the odd partial sum at degree39 and even partial sum at degree40 give

\[
\sum_{n=0}^{39}\frac{(-r)^n}{n!}
\le e^{-r}\le
\sum_{n=0}^{40}\frac{(-r)^n}{n!}.
\tag{HNM-AT3-F12}
\]

Both sums are exact Fractions. Since r<=1/2, the odd lower sum is at least 1-r>=1/2 by grouping consecutive positive/negative terms. Round the lower sum down to the G grid and the upper sum up. Repeatedly square the nonnegative interval k times, rounding every lower product down and every upper product up. Monotonicity of squaring on nonnegative numbers preserves enclosure. This produces rational bounds for the needed exp(-8) tail and each fixture ratio exp(-h x). No floating exponential, library transcendental value or uncontrolled arbitrary precision number is used in a claimed bound.

For a fixture atom of energy x, let `[q_-,q_+]` enclose exp(-hx), and start `[p_0^-,p_0^+]=[1,1]`. At every step compute

\[
p_{j+1}^-=\lfloor Gp_j^-q_-\rfloor/G,
\quad p_{j+1}^+=\lceil Gp_j^+q_+\rceil/G.
\tag{HNM-AT3-F13}
\]

Induction using positive multiplication proves `p_j^-<=exp(-jhx)<=p_j^+` for every j=0,...,4096. Positive weighted summation over atoms encloses each C(jh). **Every one of the 4097 nodes is generated and included with its actual trapezoid weight.** No geometric closed-sum substitution is used. The saved CSVs contain exactly those node enclosures, explicitly marked as synthetic in the result metadata. The total arithmetic trapezoid widths are computed exactly and both are below 10^-24.

## 6. Executed equal-moment benchmarks and all-error separation

Only AT2's abstract atomic fixtures are evaluated:

\[
\eta_A=(\delta_2+\delta_4)/8,\quad
\eta_B=\delta_1/32+3\delta_3/16+\delta_5/32,
\quad I_A=3/32,\quad I_B=1/10.
\tag{HNM-AT3-F14}
\]

For each fixture and each sign sigma=-1,0,+1, shift every exact node enclosure by sigma*epsilon. These enclose the real observations `C(jh)+sigma*epsilon`, so the extreme errors are exactly the contracted epsilon, not epsilon plus an unrecorded midpoint error. Feed all 4097 shifted enclosures through the same reusable evaluator.

The following decimal intervals are widened outward to nine decimal places; exact rational results are saved:

| Fixture and sample error | Certified I interval |
|---|---|
| A, every error -epsilon | [0.093463226, 0.095163609] |
| A, zero error | [0.093591226, 0.095291609] |
| A, every error +epsilon | [0.093719226, 0.095419609] |
| B, every error -epsilon | [0.099713226, 0.101413609] |
| B, zero error | [0.099841226, 0.101541609] |
| B, every error +epsilon | [0.099969226, 0.101669609] |

Each interval contains its known exact inverse integral and has width less than 0.001701, passing the requested 0.002 target. For every possible error vector, not merely the two tested constant vectors, positive weights place its trapezoid result between those extremal sums. Hence compare **A-plus's upper output endpoint against B-minus's lower output endpoint**. This includes both the shift J in the observed sum and the already-present allowance J inside the reported interval. The independently executed rational comparison gives

\[
\operatorname{Lower}(B,-\epsilon)
-\operatorname{Upper}(A,+\epsilon)
>4293/1000000>0.
\tag{HNM-AT3-F15}
\]

Thus the whole permitted output envelopes are disjoint. Merely comparing the two noiseless intervals would not prove worst-error separation. The result discriminates these abstract controls using this finite protocol. It does not identify the true AQ spectral type, response, particle mass or pole.

## 7. Reusable deterministic API and rejected inputs

`evaluator.py` exposes `evaluate(samples, *, T='128', h='1/32', N=4096, epsilon='1/1000000')`. Supply a list/tuple of exactly4097 entries. Each entry is an exact rational string, integer or Fraction, or a two-element lower/upper enclosure of those types. Decimal strings denote exact rationals. Floats, NaN, infinities, reversed enclosures, wrong sample count, changed design, and changed error contract are rejected. The output contains rational lower/upper endpoints, width, trapezoid arithmetic width, all three physical allowances, and the target-width verdict.

The caller must independently establish that each enclosure contains its actual reported sample and that the actual reported sample is within epsilon of the relevant AQ correlation. The API cannot verify that physical premise from numbers alone; it labels its output conditional and never claims to have supplied AQ samples. Wider arithmetic enclosures remain mathematically valid but can fail the target-width verdict. Divide a returned I interval by positive alpha to obtain R with inverse-energy units.

Reproduce all declared tests with `python -B research/round30/forward/at3/check.py --output /absolute/new/directory`. Normal and optimized Python semantic outputs and manifests must match. Saved fixture CSVs are optional inspection data, not measurement records.

## 8. Damaging controls, ancestry and final stop

The checker tests the quadrature sign against exactly enclosed finite fixture integrals; deleting the tail fails by an analytic finite-integral/curvature bound for a slow abstract atom at the gap. No samples from that control are generated. That atom satisfies the gap/mass/first-moment hypotheses used by the quadrature theorem, and is not called an AQ realization. Root-N error scaling is rejected by the exact constant-sign vector. Adding a zero-energy atom creates a constant correlation and divergent full inverse integral, exposing missing centering and violation of the gap support assumption. Energy/time rescaling, float inputs, malformed designs, and absent source provenance are distinguished explicitly. Coarsening h to1/2 gives Q>1/500; truncating at T=16 gives a tail bound>1/500. These failed alternatives are controls, not retuning or additional investigations.

NIST DLMF §3.5(i), Eqs.3.5.1-3.5.3, supplies the standard trapezoidal rule and sign. The Peano-kernel integrated-moment argument is derived fully above for this model's moment information. Abbott et al., arXiv:2605.20509v1, supplies current context for spectral bounds from finite Euclidean data; no new generic quadrature, bootstrap or Laplace-inversion method is claimed. This selected source comparison does not establish scientific priority.

This is investigation3 of3. Production stops after its review. Only repair, validation, integration, prospective planning and publication follow. No actual AQ sample acquisition, susceptibility proof, spectral-pole inference, continuum construction or fourth scientific investigation is included.
