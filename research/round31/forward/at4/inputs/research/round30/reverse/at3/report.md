# Hruday finite Euclidean readout certificate — independent reverse AT3

Human author: **Hruday N M (BUNZEEY)**. AI-assisted independent reverse reconstruction; scientific priority unverified. HNM identifiers are project aliases, not claims to invent quadrature. The contract and shared prospective Peano-kernel suggestion were fixed before fixture production. No current forward or skeptic AT3 results were read. This is the third and final authorized investigation.

## 1. Reverse target: a finite readout of a specified spectral functional

AT2 produced a broad interval for an inverse-energy form and demonstrated that moments do not identify a spectrum. This loop asks whether a finite, explicitly accurate Euclidean sample set could certify that same scalar. Reconstructing backward from the desired integral requires four controlled errors: quadrature on a finite interval, the unobserved infinite-time tail, deterministic sample errors, and arithmetic enclosures. The actual AQ premises establish a conditional theorem. The executed inputs below are only AT2's declared abstract A/B controls.

Let eta be AQ's centered Wilson spectral measure in x=E/alpha, supported on x>=a=1/16, with mass <=s_up=63/250, first moment <=u_up=94/125, and second moment <=B=36+98|tau|. Use the dimensionless Euclidean time s=alpha t_E/hbar; it is distinct from the mass notation used in AT2. Define

\[
 C(s)=\int_a^\infty e^{-sx}\,d\eta(x),\qquad
 I=\int_0^\infty C(s)\,ds=\int_a^\infty\frac1x\,d\eta(x)=\alpha R.
 \tag{HNM-AT3-R01}
\]

Tonelli applies to the nonnegative integrand, and the support bound gives I<=s_up/a<infinity. Thus the desired scalar is dimensionless I; physical R=I/alpha has inverse-energy units. An integral in physical time would instead equal hbar R. No static susceptibility is identified.

The frozen sample design is

\[
 T=128,\quad h=1/32,\quad N=4096,\quad s_j=jh\ (0\le j\le N),\quad
 \epsilon=10^{-6},\quad \text{target width}=1/500.
 \tag{HNM-AT3-R02}
\]

There are 4097 nodes. Physically these correspond to t_E,j=(hbar/alpha)jh and total duration 128hbar/alpha. The error premise is |d_j-C(s_j)|<=epsilon separately at every node. It is a deterministic absolute-error contract; neither independence nor a probability distribution is assumed. Feasibility or cost of producing actual AQ data at this precision is not established.

## 2. Differentiability, integrated curvature and the exact Peano kernel

The finite second moment permits differentiating twice under the measure integral for every s>=0, including right derivatives and continuity at zero. The majorants x and x^2 are integrable; dominated convergence also gives continuity of the derivatives. Consequently C is C2 on every closed finite nonnegative time interval, with

\[
 C'(s)=-\int x e^{-sx}\,d\eta(x),\qquad
 C''(s)=\int x^2e^{-sx}\,d\eta(x)\ge0.
 \tag{HNM-AT3-R03}
\]

Tonelli supplies a stronger integrated budget than a supremum estimate:

\[
 \int_0^T C''(s)\,ds
 =\int x(1-e^{-Tx})\,d\eta(x)\le\int x\,d\eta(x)\le u_{up}.
 \tag{HNM-AT3-R04}
\]

The second moment supplies regularity at the first node; the first moment supplies this global quadrature budget.

On a cell [jh,(j+1)h], put r=s-jh and k_j(s)=r(h-r)/2. Twice integrating by parts, with k=0 at both endpoints, k'(jh)=h/2, k'((j+1)h)=-h/2 and k''=-1, gives

\[
 \frac h2\{C(jh)+C((j+1)h)\}-\int_{jh}^{(j+1)h}C(s)\,ds
 =\int_{jh}^{(j+1)h}k_j(s)C''(s)\,ds,
 \quad 0\le k_j(s)\le h^2/8.
 \tag{HNM-AT3-R05}
\]

This proves the excess sign as well as the bound. Summing all cells defines the usual composite trapezoid and yields

\[
 Q_h(C)=h\left[\tfrac12C(0)+\sum_{j=1}^{N-1}C(jh)+\tfrac12C(T)\right],\qquad
 0\le Q_h(C)-\int_0^T C(s)\,ds
 \le q_{err}:=\frac{h^2u_{up}}8=\frac{47}{512000}.
 \tag{HNM-AT3-R06}
\]

The proof holds on the full time interval and retains all N cells. It is not an inference from observed grid convergence, nor N times a sampled second derivative.

## 3. Tail, deterministic errors and interval arithmetic

For all s>=T the gap gives C(s)<=s_up exp(-as). Therefore

\[
 0\le\int_T^\infty C(s)\,ds
 \le t_{err}:=\frac{s_{up}}a e^{-aT}=\frac{504}{125}e^{-8}.
 \tag{HNM-AT3-R07}
\]

Every trapezoid weight is positive and the weights sum to Nh=T. If |d_j-C(s_j)|<=epsilon, the triangle inequality gives

\[
 |Q_h(d)-Q_h(C)|\le T\epsilon=:n_{err}=\frac{16}{125000}.
 \tag{HNM-AT3-R08}
\]

The two constant-sign error vectors attain the positive and negative extremes. A root-N estimate is unjustified for this premise.

The implementation permits a rational interval [d_j^-,d_j^+] enclosing each observed real d_j; these are arithmetic representation intervals, separate from the sample error. Positive weights produce Q_h(d) in [Q^-,Q^+]. A rigorous upper exponential enclosure t_err^+ then gives the conditional certificate

\[
 \boxed{I\in[Q^- -q_{err}-n_{err},\ Q^+ +t_{err}^+ +n_{err}].}
 \tag{HNM-AT3-R09}
\]

Its width is Q^+-Q^-+q_err+t_err^++2n_err. Exact rational arithmetic supplies the endpoints, so no later floating-point rounding is hidden in them.

For the reusable API, each observed-sample arithmetic interval may have width at most 10^-12. Exact decimal or rational observed values can be supplied with equal endpoints. Positivity of weights bounds Q^+-Q^- by T times that width. Our rigorous rational exp(-8) enclosure gives

\[
 t_{err}^+=\frac{10567072778929122922873757469}
 {7812500000000000000000000000000},\qquad
 \operatorname{width}\le
 \frac{13284236864866622922873757469}
 {7812500000000000000000000000000}<\frac1{500}.
 \tag{HNM-AT3-R10}
\]

The upper width is approximately 0.001700382319, including the full API arithmetic allowance 128 times 10^-12. This is a conditional guarantee for every permitted sample-error vector and arithmetic interval; it is not an actual AQ response estimate.

## 4. Rigorous exponentials and all 4097 sample nodes

Every synthetic exponential is enclosed by a rational computation. For 0<=z<=1/2, let P_m(z)=sum_(k=0)^m(-z)^k/k!. Alternating-series monotonicity gives

\[
 P_{33}(z)\le e^{-z}\le P_{32}(z).
 \tag{HNM-AT3-R11}
\]

The terms decrease in absolute value, so the signed tail has the claimed bracket. We round the lower endpoint down and the upper up to denominator D=10^30. For larger decay arguments, halve the argument until it is <=1/2, obtain that interval and repeatedly square it, always outward rounding; exp(-2z)=(exp(-z))^2 and nonnegativity justify the procedure. In particular exp(-8) is enclosed by this method. No floating exponential value is used for admission.

For a fixture atom x, enclose r=exp(-hx) once. Begin at the exact interval [1,1]. If integer pairs (l_j,u_j) and (l_r,u_r) represent positive intervals divided by D, update

\[
 l_{j+1}=\left\lfloor\frac{l_jl_r}{D}\right\rfloor,\qquad
 u_{j+1}=\left\lceil\frac{u_ju_r}{D}\right\rceil,
 \quad r^{j+1}\in[l_{j+1}/D,u_{j+1}/D].
 \tag{HNM-AT3-R12}
\]

Induction proves enclosure of every node through j=4096, including very small values whose lower endpoint rounds to zero. A zero lower bound does not assert that the exponential itself vanishes. Weighted interval sums give the fixture correlation enclosures. All 4097 nodes are actually emitted to CSV and read by the same trapezoid evaluator; no geometric-series shortcut or implicit subsampling is used.

The API takes those bins as enclosures of the observed d_j. For the exact-noise stress cases d_j=C(jh)+epsilon or C(jh)-epsilon, the whole computed interval is shifted by the exact rational epsilon. Its bin encloses that real observation, while the separate observation error remains exactly epsilon. This avoids miscounting synthetic rounding as an uncharged extra sample error.

## 5. Executed A/B controls and separation under every allowed error

The only executed benchmark measures are

\[
 \eta_A=(\delta_2+\delta_4)/8,\qquad
 \eta_B=\delta_1/32+3\delta_3/16+\delta_5/32,\qquad
 I_A=3/32,\ I_B=1/10.
 \tag{HNM-AT3-R13}
\]

They have the equal moments checked in AT2. They are abstract positive-measure controls, not AQ ground-state calculations. For each fixture the program generates the 4097 exact-enclosure nodes and evaluates three cases: zero sample error, all +epsilon, and all -epsilon. Every interval contains its exact I and satisfies the target width. The following decimal displays are for readability; the JSON contains exact rational endpoints.

| Input case | Lower endpoint | Upper endpoint | Exact benchmark |
|---|---:|---:|---:|
| A, zero error | 0.09359122636 | 0.09529160856 | 0.09375 |
| B, zero error | 0.09984122636 | 0.10154160856 | 0.1 |
| Envelope of all admissible A errors | 0.09346322636 | 0.09541960856 | 0.09375 |
| Envelope of all admissible B errors | 0.09971322636 | 0.10166960856 | 0.1 |

The envelopes include two distinct noise effects. When d varies, its observed trapezoid itself shifts by at most T epsilon; each returned certificate also has its own allowance T epsilon. Let [Q_A^-,Q_A^+] and [Q_B^-,Q_B^+] enclose the true noise-free trapezoids. The largest possible A upper endpoint and smallest possible B lower endpoint are bounded by

\[
 U_A=Q_A^+ +t_{err}^+ +2T\epsilon,\qquad
 L_B=Q_B^- -q_{err}-2T\epsilon,\qquad
 L_B-U_A>\frac4{1000}.
 \tag{HNM-AT3-R14}
\]

The exact computed margin is approximately 0.00429361781. The checker independently executes A with all-positive observations and B with all-negative observations, each passed through the full output-interval evaluator. Positive weights prove these are the damaging extremes among all allowed error vectors, even when A and B errors are unrelated. This establishes discrimination of these two abstract controls by the frozen protocol. It does not identify the AQ spectrum, its poles or its actual inverse-energy value.

## 6. Reusable input contract

`check.py` provides deterministic functions `evaluate(samples, *, T_value=128, h_value=Fraction(1,32), N_value=4096, epsilon=Fraction(1,1000000))` and `evaluate_csv(path)`. Each sample is a lower/upper pair of exact rational numbers. Allowed numeric values are Python `Fraction`, integers, exact decimal strings or rational strings; binary floats are rejected. The CSV has exactly this header:

`index,s,value_lower,value_upper`

It must have 4097 data rows, consecutive indices 0 through 4096, and exact times j/32. Both sample-bin endpoints may be equal. Sample values may be slightly negative under the allowed observation error near the tail; the evaluator does not clip them and bias the sum. Intervals wholly incompatible with the mass/error envelope are rejected. Inverted intervals, excessive arithmetic width, wrong sample count, time grid, design, error level, nonfinite text and malformed rational fields are rejected.

For actual future observations, the caller must independently certify centering, AQ model/state provenance and the epsilon absolute-error premise. Parsing data and producing an interval cannot establish these scientific conditions. Even the output flag stating `actual_aq_samples_computed: false` remains false in external-input mode: this program does not compute those samples itself.

Run the benchmark and its exact controls with:

`python -B research/round30/reverse/at3/check.py --output /absolute/fresh-directory`

Evaluate a CSV meeting the declared design with:

`python -B research/round30/reverse/at3/check.py --csv /absolute/input.csv --output /absolute/fresh-directory`

The program writes exact rational certificates and a file manifest. Division of its I endpoints by a specified alpha gives physical R endpoints; no implicit choice of alpha or hbar is made.

## 7. Damaging controls and limitations

The executed controls reject the following inferences:

- **Wrong trapezoid sign.** For fixture A, the rigorous lower bound for its trapezoid exceeds the exact I_A. Reversing the convex-quadrature correction would exclude the truth.
- **Omitted tail.** A further diagnostic with mass 1/10 at x=1/16 and 3/20 at x=119/24 preserves total mass 1/4 and first moment 3/4. Its no-tail upper endpoint lies strictly below its exact inverse integral, even including the sample allowance. It is a damaging abstract kernel control, not another AQ computation.
- **Root-N deterministic noise.** All-positive errors shift the sum by exactly T epsilon. The proposed root-N replacement T epsilon/64 is smaller by 64 and fails this explicit allowed error vector.
- **Missing centering.** Adding a positive zero-energy atom leaves a nondecaying constant in C. Its time integral diverges and it violates the positive-gap tail estimate; inversion on the vacuum-orthogonal subspace cannot be replaced by integrating that uncentered correlation.
- **Wrong time/energy conversion.** An exact alpha=4,hbar=3 fixture distinguishes physical time from dimensionless duration and I from R.
- **Insufficient settings.** With T=16 the allowed tail budget alone exceeds the target; with h=1/4 the quadrature budget alone exceeds it. These outcomes concern the uniform certificate and do not prove actual reconstruction failure for every measure.
- **Uncontrolled floating exponentials and malformed input.** The API rejects these rather than treating a point float or invalid grid as a rigorous enclosure. Source snapshots, report, code, CSVs and output bytes are frozen and replayed normally and with optimized Python.

NIST DLMF Section 3.5(i), equations 3.5.1–3.5.3, is the primary source for standard trapezoidal quadrature and its sign. The positive kernel and integrated-moment application are derived explicitly above. Abbott et al., arXiv:2605.20509v1, supplies established spectral-functional certification from finite Euclidean information. Neither general technique is attributed as a new Hruday invention. No actual AQ correlation data, AQ response value, physical susceptibility, optimal sampling design, spectral pole, experimental apparatus or continuum theory has been produced. After this freeze only review, repairs, integration and publication remain; no fourth scientific investigation is started.
