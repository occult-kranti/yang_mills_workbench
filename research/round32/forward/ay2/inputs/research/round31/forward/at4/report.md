# Hruday actual-sample provenance and local reference comparison — AT4 forward

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted independent forward production. The shared prospective proposal (local reset, free-reference Duhamel comparison and positive Poisson integration) came from the advisor/modern panel before the contract was frozen. This report reconstructs its constants and proof independently; no current reverse or skeptic solution was read. HNM labels are project aliases. Duhamel's formula, the Poisson kernel, trace-distance inequalities and moment-information arguments are established methods; scientific priority is unverified.

**Verdict.** There is a rigorous direct interval for the actual AQ centered Wilson Euclidean correlation at the specified nonzero coupling, selected triple and time. The interval's midpoint error allowance exceeds the frozen `10^-6` target, so that target is **insufficient under this certificate**. This is not a proof that the actual correlation differs from the free value by that allowance. The abstract inherited A/B equal-moment controls also give an explicit nonzero-time information obstruction, separate from any assertion about multiple AQ states.

## 1. Frozen state, complete model and units

Use AQ1's chosen locally normal centered-box subsequential state on the full coarse Z³ complete-factor algebra, its actual strongly continuous GNS dynamics, and AQ2's physical reducing generator. The frozen selected coefficients are exactly `(lambda_L,mu_M,lambda_R)=(0,0,0)`, which is included in the inherited closed ranges `|lambda_L|,|lambda_R|<=alpha/2`, `|mu_M|<=alpha/8`. Freeze `tau=+10^-8`; it is not zero. Thus there are omitted magnetic interactions but no selected magnetic interactions. This is a patterned interacting subfamily of AQ, not uniform Wilson magnetic theory.

Each factor b owns the 24 original positive links whose tails are `(4b_x+r,2b_y+q,b_z)`, `r=0,...,3`, `q=0,1`. All original endpoint gauge actions are retained. The normalized complete-factor reference is now exactly

\[
 h_b=8\sum_{e\text{ owned by }b}C_e,
 \qquad C_e=-\sum_{a=1}^3X_{ea}^2,
 \qquad P_b=|1_b\rangle\langle1_b|.
 \tag{HNM-AT4-F01}
\]

The constant Haar vector is the unique reference ground and its ground scalar is zero, because **the selected triple is zero**. For one nonzero selected plaquette the trial `1+tW`, with `t=lambda/(3alpha)`, has energy numerator `3alpha t²/4-lambda t/2=-lambda²/(12alpha)<0`. Hence Haar could not be its ground; (F01) must not be silently extended to other selected triples.

The first positive Casimir eigenvalue in the `i sigma_a/2` convention is `j(j+1)=3/4`, at `j=1/2`. The tensor sum (F01) has first positive normalized energy 6. For every finite region R,

\[
 h_R=\sum_{b\in R}h_b\ge6(I-P_R),
 \qquad P_R=\bigotimes_{b\in R}P_b.
 \tag{HNM-AT4-F02}
\]

This is a local full-Hilbert reference statement, not a new claim for the interacting spectral gap.

With `delta=alpha/8`, the actual dimensionless physical-time generator is

\[
 G_N:=H_N^{raw}/\alpha
 =\sum_{e\text{ owned in }\Lambda_N}C_e
 +\sum_{b+S\subset\Lambda_N}V_b,
 \quad V_b=\phi_b/8,
 \quad\|V_b\|\le7|\tau|/8,
 \quad S=\{0,e_x,e_y,e_z\}.
 \tag{HNM-AT4-F03}
\]

Actual finite ground subtraction remains `K_N=H_N^{raw}-E_N^{raw}`. It cancels in Heisenberg conjugation, not in arbitrary unitary matrix elements. The centered GNS operator is the actual nonnegative `H_phys`; set `G=H_phys/alpha`. Real-time `theta=alpha*t_real/hbar`, Euclidean `s=alpha*t_E/hbar=1`, and the older AQ normalized clock is `u=delta*t_real/hbar=theta/8`. The positive reference `E_star`, `alpha`, `hbar` and lattice spacing remain fixed. L=10000 is a dimensionless integration cutoff, not a coupling or physical deformation.

## 2. Original Wilson, free heat and seven whole stars

The observable is the original fine-lattice xz Wilson loop

\[
 W=\frac12\operatorname{Tr}
 [U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}].
 \tag{HNM-AT4-F04}
\]

Its four distinct stored links have owners `0,0,e_z,0`, so its complete cover is `R={0,e_z}`. This cover contains 48 links and 36 distinct original endpoints. The exact full-lattice incident-anchor set is

\[
 R-S=\{0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y\}.
 \tag{HNM-AT4-F05}
\]

All seven whole stars occur for every centered box `N>=2`. The two positive-orthant anchors `0,e_z` would omit five actual interactions. Counting only W's displayed links is not sufficient for a general bounded operator evolved on its complete reference factors.

The Haar distribution of the product holonomy yields `omega_0(W)=0`, `omega_0(W²)=1/4`. Each of the four original link Casimirs contributes `(3/4)W` (the inverse orientation has the same eigenvalue), so

\[
 G_{0,R}(W1_R)=3W1_R,
 \quad c_0(\theta)=\omega_0(W\alpha^0_\theta(W))
 =\tfrac14e^{3i\theta},
 \quad C_0(s)=\tfrac14e^{-3s}.
 \tag{HNM-AT4-F06}
\]

The corresponding energy is `3alpha`, frequency `3alpha/hbar`, and normalized AQ energy 24. Using exponent `-24s` when s is defined with alpha would be an eightfold clock error. Free factor evolution preserves R for every theta, although it is not asserted to be norm continuous in time on the entire local B(H_R) algebra.

## 3. State comparison in the actual interacting AQ state

Reset a finite actual ground density on R to P_R and retain its exterior marginal. The mixed full-Hilbert trial has finite reference form energy. Each incident retained star changes expectation by at most twice its normalized norm; all other interaction expectations are unchanged. The finite ground variational principle gives

\[
 \operatorname{Tr}(\rho_{N,R}h_R)\le2(7)(7|\tau|)=98|\tau|.
 \tag{HNM-AT4-F07}
\]

Unbounded exterior reference expectations cancel after bounded positive spectral truncation and monotone convergence; the finite ground and reset trial have finite form energies since the finite interactions are bounded. A gauge-invariant restriction on the trial is unnecessary because the admitted AQ finite ground is the full-Hilbert minimum.

Along the **actual AQ subsequence**, every local density converges in trace norm. First pass each bounded positive truncation of h_R and then take its monotone supremum. Equation (F07) holds for the actual limiting density rho_R. Together with (F02),

\[
 \epsilon_R:=1-\operatorname{Tr}(\rho_RP_R)
 \le\frac{98|\tau|}{6}=\frac{49|\tau|}{3},
 \qquad
 \|\rho_R-P_R\|_1\le D:=2\sqrt{49|\tau|/3}.
 \tag{HNM-AT4-F08}
\]

The trace inequality follows by expressing rho_R as a mixture of pure states, using the exact pure-state distance `2sqrt(1-overlap)`, then convexity and Cauchy-Schwarz. No thermodynamic convergence rate is used. Equation (F08) applies to every AQ subsequential state having the inherited construction; it does not identify or equate them.

Let `m=omega(W)`, `q=omega(W²)` and `v=q-m²`. Trace duality gives `|m|<=D`. The trace-zero difference rho_R-P_R satisfies the sharper effect bound `|Tr[(rho_R-P_R)A]|<=D/2` for `0<=A<=I`, by its positive/negative parts. Since `0<=W²<=I`,

\[
 |q-\tfrac14|\le D/2,
 \qquad 0\le v\le\tfrac14+D/2.
 \tag{HNM-AT4-F09}
\]

This is a refinement available in this zero-selected corner; it is not a claim that the interacting values equal their Haar values.

## 4. Local Duhamel estimate with unbounded onsite energies

For a finite centered box containing R, separate the physical-dimensionless Hamiltonian into

\[
 G_N=A_N+B_N,
 \quad A_N=G_{0,R}+G_{outside,N},
 \quad B_N=\sum_{b:(b+S)\cap R\ne\varnothing}V_b,
 \quad\|B_N\|\le49|\tau|/8.
 \tag{HNM-AT4-F10}
\]

Here `G_outside,N` contains every outside onsite term and every retained interaction disjoint from R. All star groups meeting R are assigned in full to B_N, even if some constituent faces act only outside. Therefore A_N evolves W exactly as the free R generator. Both A_N and G_N are self-adjoint on the same domain: finite compact-product Casimir sums plus bounded potentials. Outside and R operators commute strongly as tensor operators.

For completeness, bounded-perturbation Duhamel is justified without differentiating `G_N W`. On the common operator domain differentiate the relative unitary product `e^{itG_N}e^{-itA_N}`. Its derivative is the bounded strongly continuous operator `i e^{itG_N}B_N e^{-itA_N}`. Integration vectorwise extends the identity by density to every vector and yields `||e^{itG_N}e^{-itA_N}-I||<=|t| ||B_N||`. Insert the bounded W only **after** this relative-unitary estimate. Conjugation then gives

\[
 \|\alpha^N_\theta(W)-\alpha^0_\theta(W)\|
 \le2|\theta|\|B_N\|\|W\|
 \le k|\theta|,
 \qquad k=49|\tau|/4.
 \tag{HNM-AT4-F11}
\]

The integral need only exist strongly; the resulting norm bound does not assert a norm-Bochner derivative on arbitrary bounded local operators. This estimate is local and independent of box size. Replacing B_N by the extensive total magnetic norm destroys that property and is unnecessary.

AQ1's norm convergence of the actual bounded-local finite-volume dynamics on compact theta intervals allows N to tend along the actual exhaustion in (F11). The free reference evolution is already the same local operator in all these volumes. Thus (F11) holds for the actual infinite AQ evolution at each real theta. This passage uses the admitted unbounded-onsite dynamics theorem in its already matched model; no finite numerical matrix is substituted for it.

## 5. State, dynamics and centering are separate costs

Let `chi=(pi(W)-m)Omega` in the actual physical GNS space and

\[
 c(\theta)=\langle\chi,e^{i\theta G}\chi\rangle
 =\omega(W\alpha_\theta(W))-m^2.
\]

Add and subtract the free evolution inside the actual state, then the local reference state. Since `W alpha^0_theta(W)` stays in B(H_R) and has norm at most one,

\[
 \begin{split}
 |c(\theta)-c_0(\theta)|
 &\le|\omega(W[\alpha_\theta(W)-\alpha^0_\theta(W)])|
  +|\operatorname{Tr}[(\rho_R-P_R)W\alpha^0_\theta(W)]|+m^2\\
 &\le k|\theta|+D+D^2.
 \end{split}
 \tag{HNM-AT4-F12}
\]

The complex operator in the state term is not an effect, so the D/2 effect refinement from (F09) is not assigned to it. Spectral positivity and Cauchy-Schwarz also give the all-time bound

\[
 |c(\theta)-c_0(\theta)|\le v+1/4\le1/2+D/2=:B.
 \tag{HNM-AT4-F13}
\]

Centering a **vector** with a numerical mean `m_hat=m+d` gives `chi_hat=chi-d Omega`. Since the centered chi is orthogonal to the zero-energy vacuum, its heat correlation is `C(s)+d²`. By contrast scalar subtraction of `m_hat²` from the true uncentered correlation gives `C(s)-2md-d²`. These are different operations and have different errors. For the exact control `m=1/4,d=1/100`, they are respectively `+1/10000` and `-51/10000`. An entirely uncentered correlation retains the vacuum residue `m²=1/16` in that control for all time. These finite controls expose the algebra; they are not AQ data.

## 6. Positive Poisson integration and its full tail

The actual AQ physical GNS generator is nonnegative, and chi has finite squared norm. Its centered spectral measure eta is supported in `[1/16,infinity)` by AQ2; only nonnegativity is needed here. The standard Poisson/Cauchy Fourier identity is

\[
 \int_{\mathbb R}\frac{s}{\pi(s^2+\theta^2)}e^{i\theta x}\,d\theta
 =e^{-s|x|},\qquad s>0.
 \tag{HNM-AT4-F14}
\]

One proof for x>0 closes the contour of `e^{izx}/(s²+z²)` in the upper half-plane and takes the residue at `is`; the semicircle contribution tends to zero, first away from the real endpoints and then by the elementary endpoint bound. For x<0 close below; x=0 follows from the arctangent integral. Thus the identity is all-real x, not only a sampled quadrature rule. Since the kernel is positive with integral one and eta is finite, Fubini is justified by absolute integrability after taking the spectral measure. Functional calculus gives

\[
 C(s):=\langle\chi,e^{-sG}\chi\rangle
 =\int_{\mathbb R}\frac{s\,c(\theta)}{\pi(s^2+\theta^2)}d\theta.
 \tag{HNM-AT4-F15}
\]

The same identity applies to the free reference. It would give `e^{-s|G|}`, not `e^{-sG}`, for a generator of unrestricted sign. Actual nonnegative ground-centered spectrum is essential.

On `|theta|<=L` use (F12). The kernel integrates to at most one, and direct elementary integration gives

\[
 \int_{-L}^L\frac{s|\theta|}{\pi(s^2+\theta^2)}d\theta
 =\frac{s}{\pi}\log(1+L^2/s^2).
\]

On the entire complement use (F13). Its kernel mass is `(2/pi) arctan(s/L)<=2s/(pi L)`. Hence

\[
 \boxed{|C(s)-\tfrac14e^{-3s}|
 \le\mathcal E(D,k,s,L):=
 D+D^2+\frac{ks}{\pi}\log(1+L^2/s^2)
 +(1/2+D/2)\frac{2s}{\pi L}.}
 \tag{HNM-AT4-F16}
\]

All terms have correlation units (dimensionless), and every theta outside the cutoff is included. L is an integration resource, not a statement that real-time response ceases beyond L. Increasing L decreases the tail but increases the logarithmic bulk term; neither can simply be deleted. The constant term is conservatively charged over total kernel mass one rather than only the bulk mass.

At the frozen values, the certificate has `D^+≈0.000808290376865476`, state-centering cost `D^2≈0.000000653333333333`, integrated dynamical cost `≈0.000000718276887292`, and whole-tail cost `≈0.0000318567173001654`. Their sum is `mathcal E^+≈0.000841518704386267`. The resulting interval is approximately `[0.0116052483875797, 0.0132882857963523]`, with midpoint `≈0.0124467670919660`. These decimal summaries are for readability; the exact rational outward enclosure in `output/results.json` yields the final **actual AQ interval**

\[
 C(1)\in[\max(0,C_0^- -\mathcal E^+),
           \min(1/4+D^+/2,C_0^+ +\mathcal E^+)].
 \tag{HNM-AT4-F17}
\]

The two clipping bounds follow from positivity of the heat operator and `C(1)<=v`. They do not become active in this cap-level calculation. The returned midpoint requires half the interval width as its absolute point-error certificate. That half-width exceeds `10^-6`; the original target remains unmet. The code explicitly requires this **insufficient** outcome rather than silently replacing tau, s or the tolerance.

This establishes actual-state analytic information in a specified interacting corner, as opposed to evaluating abstract A/B controls. It does not compute an AQ sample at the inherited AT3 epsilon premise, an exact AQ value or a certified finite-volume numerical solution.

## 7. Equal moments still leave nonzero-time information missing

The inherited controls are

\[
 \eta_A=(\delta_2+\delta_4)/8,
 \qquad\eta_B=\delta_1/32+3\delta_3/16+\delta_5/32.
\]

Both have exactly `(mass,first moment,second moment)=(1/4,3/4,5/2)` and positive support above 1/16. At s=1 put `r=e^-1`. Their Laplace transforms differ by

\[
 C_B(1)-C_A(1)
 =\frac{r+6r^3+r^5-4r^2-4r^4}{32}
 =\frac{r(1-r)^4}{32}>0.
 \tag{HNM-AT4-F18}
\]

Any deterministic estimator seeing only these three common moments returns the same scalar z on A and B. The triangle inequality gives

\[
 \max(|z-C_A(1)|,|z-C_B(1)|)
 \ge\frac{|C_B(1)-C_A(1)|}{2}
 >\frac9{10000}=0.0009.
 \tag{HNM-AT4-F19}
\]

Directed rational exponential enclosures prove the last strict inequality; the half-separation is about 0.000917751717. The exact interval is emitted. This applies to estimators for the abstract moment-compatible class. These measures are not asserted to be realizations of the AQ Hamiltonian. Equation (F19) proves neither actual AQ-state nonuniqueness nor an impossibility result for estimators using the richer AQ Hamiltonian and local-state information in (F08).

## 8. Arithmetic, controls, provenance and remaining obligations

`check.py` uses only Python standard-library integer/Fraction arithmetic for decisions. For `0<=z<=1/2`, the alternating exponential series bounds `P_41(z)<=e^-z<=P_40(z)`; reduce larger positive arguments by halving, then square positive intervals with outward rounding to denominator `10^30`. Logarithms use `log y=2sum_{k>=0}z^(2k+1)/(2k+1)`, `z=(y-1)/(y+1)`, after reducing y into [1,2]; the omitted series is bounded by its geometric majorant. Pi uses Machin's identity and alternating arctangent enclosures. Integer-square-root brackets are checked after squaring. All final errors/endpoints remain exact rational numbers. Binary floating values are unnecessary for admission.

The executed controls retain the seven incoming stars, 48-link cover and 36 endpoints; reject the wrong clock; distinguish selected reference from generic Haar; separate vector centering from scalar subtraction and vacuum residue; prove the exact equal-moment mismatch; expose omission of positive Poisson tail mass; and contrast the seven local star budget with an extensive-volume norm. The finite-prefix control compares two convergent scalar sequences identical through any chosen finite observation count and different thereafter. It demonstrates that finite observed agreement supplies no abstract convergence rate. It is not offered as two actual AQ ground sequences.

The direct route bypasses a **quantitative state/boundary convergence rate** only because a uniform local-state reset estimate and a uniform local dynamics comparison are proved and passed to the already constructed actual state. It does not prove boundary independence or a canonical choice of subsequence. A future finite-volume numerical route must still specify the exact whole-star boundary and selected parameters; certify that its finite state approximates the chosen AQ state at a quantified rate; control the complete infinite-rank onsite representation truncation and omitted channels; bound actual ground projection/energy and solver residual errors; center the observable with its true mean (including mean uncertainty); and match the physical clock. A finite-matrix gap, stable digits or several box sizes do not discharge those obligations.

Nearest checked source placement is the inherited AQ dictionary: Gauvin arXiv:2503.15539v3 Supplement A.10 for the compactness/GNS/Fourier strategy, and Nachtergaele–Sims arXiv:1410.8174v1 Section 3/Theorem 4.1 for unbounded-onsite thermodynamic dynamics. Those hypotheses and model bindings were read from the copied AQ reports/source dictionary in this loop; no new full-paper reading by this producer is claimed. The local bounded-perturbation and Poisson arguments are proved explicitly above. Generic perturbation/Poisson/moment methods retain established attribution. The proposed contribution is the evaluated specified-corner AQ certificate and the precise unmet tolerance, with priority unverified.

Newton's analysis/synthesis and Tesla's full mechanism/clock accounting are modern methodological lenses; the historical panel's occult and symbolic material supplies no mathematical premise. No historical figure participates in or endorses this analysis. No actual response at `10^-6`, uniform Wilson result, state uniqueness, particle pole, physical susceptibility or continuum construction is claimed.

Reproduce with `python -B research/round31/forward/at4/check.py --output /absolute/fresh-directory`; optimized Python must produce identical output bytes. Every source input and generated output is bound in the manifest and freeze. AT4 is one investigation; no second loop has been executed by this producer.
