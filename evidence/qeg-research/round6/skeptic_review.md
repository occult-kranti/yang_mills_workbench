# Skeptical physics review: accepted results, obstructions and new restricted lemmas

Review date: 9 September 2026. This review treats round 4's equations and round 5's proof as a specified finite mathematical model. A derivation of that model's consequences is not automatically a derivation from continuum QED. The review used the actual theorem, critique, gravity bridge, theory map, response contract and acceptance record. The code reviewer is separately inspecting implementation behavior. No historical file was changed.

The important new outcome is two-sided. The denominator certificate is stronger than previously stated when the longitudinal window is fixed: it survives every finite Landau cutoff. But the same positive-gap proof cannot survive the unmodified joint removal of the longitudinal and Landau cutoffs at fixed susceptibility. Both statements follow from exact equations. Neither depends on which agent prefers a result.

## 1. What survives skeptical review

| Result | Verdict | Objection retained |
|---|---|---|
| Finite-model global forward existence and uniqueness | Accepted under the explicit finite-model, state, drive and global-gap hypotheses | This is a standard ODE continuation argument for a specified closure, not a continuum or gravitational existence theorem |
| Selected exact quadrature certificate Z(a)>3/4 | Accepted, for b=10, K=20 and the prescribed coupling/matching | A sampled minimum is not the proof; exact quadrature, rounded coefficient lists and floating trajectories remain distinct |
| Vacuum-start field envelope | Accepted: absolute field <= 4|lambda|/3 for a normalized nonnegative pulse | lambda is external-current impulse; the envelope does not predict a waveform or its derivative at a pumped baseline |
| Finite-time differentiable retarded response | Accepted with regular source/data families and identical pre-probe preparation | Parameter differentiation needs joint/local uniform regularity; no all-time full-tangent stability follows |
| Bianchi-I constraint propagation | Accepted for the displayed off-constraint Einstein evolution and a regular positive-volume interval | The source must include apparatus work and both directional pressures; a propagated constraint does not establish the physical correctness of a guessed source |
| Finite-rule bidirectional planner | Accepted only as dependency replay and finite-library cost search | Human-entered implication validity is external to the checker; its `conditional:false` metadata must not be displayed as an assumption-free theorem |
| Archived default numerical response | Accepted within the frozen acceptance record | Only 401 output times, one fixed window/cutoff and small independent spinor fixtures were accepted; numerical source setup outside the default is under separate audit |

The energy proof correctly preserves the zero-energy case with sqrt(W+epsilon), bounds every finite state coordinate before invoking continuation, and distinguishes all-time field bounds from finite-time potential bounds. I did not find a counterexample satisfying every stated hypothesis. That is not a claim that this proves all possible numerical runs: an approximate Bloch vector outside the unit ball need not satisfy the exact energy inequality.

The forced-field theorem also requires the global coefficient margin, not just an initial positive value. The existing example reaching Z=0 with finite fields remains a valid falsifier of that shortcut. For the smooth-response theorem, r dot eta is constant but need not vanish for a varying mixed-state purity. The existing signed first-variation energy counterexample remains valid; section 5 below obtains a different, positive quadratic result at a stationary vacuum.

The original response acceptance explicitly retains failed coarse momentum comparisons: 128 to 256 and 256 to 512 nodes fail the field-tangent gate. Only the 512 to 1024 comparison passes it. The direct-current difference is a diagnostic, not a previously frozen accuracy gate. A graph must distinguish that field-tangent threshold from current error, ODE tolerance and continuum error. Reusing a tiny work residual as an error bar for all plotted observables would be invalid.

## 2. Exact coefficient analysis exposes the cutoff issue

Fix b>0, e^2>0, N>=0 and K>0. Let M_n^2=1+2bn, d_0=1 and d_n=2 for n>0. This section uses an **exact longitudinal integral**, not a finite node rule:

\[
C_{K,N}(a)=\frac{b}{4\pi^2}\sum_{n=0}^N d_n
\int_{-K}^K\frac{M_n^2\,dk}{4[M_n^2+(k-a)^2]^{5/2}}.
\tag{S1}
\]

A primitive of the integrand is

\[
A_M(p)=\frac{1}{4M^2}\left(u-\frac{u^3}{3}\right),
\qquad u=\frac{p}{\sqrt{M^2+p^2}}.
\tag{S2}
\]

Consequently the integral is A_M(K-a)+A_M(K+a). Its derivative with respect to a is g_M(K+a)-g_M(K-a), where g_M(p)=M^2/[4(M^2+p^2)^(5/2)]. Since g_M is even and strictly decreases with |p|, C is even and strictly decreases for a>0. Therefore its global maximum is exactly at a=0. This proves an exact-integral denominator test Z_min=1+chi_b-e^2 C_{K,N}(0). Positivity is a condition to check; it is not automatic for arbitrary parameters.

The primitive and whole-line integral have independent symbolic checks, and four shifted-window cases agree with a separate 65-digit numerical integration. In particular,

\[
\int_{\mathbb R}\frac{M^2\,dp}{4(M^2+p^2)^{5/2}}
=\frac1{3M^2}.
\tag{S3}
\]

Using z=1/(2b) and the digamma recurrence gives

\[
e^2 C_{\infty,N}
=\frac{e^2}{12\pi^2}
\left[b+\psi(N+1+z)-\psi(1+z)\right].
\tag{S4}
\]

Combining this with the **unchanged** round-4 susceptibility cancels its finite b-dependent pieces:

\[
Z_{\infty,N}
=1-\frac{e^2}{12\pi^2}
\left[\log(2b)+\psi(N+1+z)\right].
\tag{S5}
\]

Since psi(x)=log(x)+O(1/x), Z tends to minus infinity as N tends to infinity at fixed b,e and matching. These are derivations from our coefficient definitions; the mathematical inputs are the [digamma recurrence](https://dlmf.nist.gov/5.5.E2) and its [positive-real asymptotic expansion](https://dlmf.nist.gov/5.11.E2). The asymptotic formula is not being treated as an exact finite-N identity.

### The obstruction is not merely an order-of-limits observation

Positivity makes C_{K,N}(0) increase with K and N. For any threshold L, first choose a finite N_0 so C_{infinity,N_0}>L. Then choose a finite K_0 so C_{K_0,N_0}>L. Every K>=K_0 and N>=N_0 exceeds it. Thus any cofinal joint limit K,N to infinity has C_{K,N}(0) to infinity. Monotonicity of a particular sequence is unnecessary if both cutoffs eventually exceed every fixed threshold.

An explicit quantitative route takes K>=sqrt(1+2bN), so K>=M_n for every retained level. Then u=K/sqrt(M_n^2+K^2)>=1/sqrt(2), and

\[
\int_{-K}^K g_{M_n}(k)\,dk
\ge \frac{5}{12\sqrt2 M_n^2}.
\tag{S6}
\]

The resulting sum over d_n/M_n^2 diverges harmonically. This provides a finite-window lower bound, independent of invoking the whole-line limit first.

**What is disproved:** a uniform positive denominator bound for this unchanged explicitly divided closure as both cutoffs are removed with fixed coupling and susceptibility.

**What is not disproved:** continuum QED, every alternative renormalized formulation, finite-time physical observables, or an alternative existence proof. The unrenormalized modal current S and local subtraction C may contain divergences that cancel only when a common renormalized combination is formed. One must analyze that combination before exchanging limit, subtraction and algebraic division. Tuning chi alone to restore positivity is a different model unless justified by a shared matching/renormalization prescription.

The affordable numerical sequence in the checks only shows the coefficient increasing and Z still positive, from about 0.99658 to 0.99238 over the displayed joint-cutoff cases. It does **not** numerically reach a zero. The divergence result is analytic. Do not turn an asymptotic extrapolation into an observed physical pole or an experimental prediction.

## 3. A positive result in the opposite cutoff direction

At fixed b=10 and K=20, any positive exact longitudinal quadrature with total longitudinal weight 40 obeys the individual-mode bound used in round 5. For the new Landau tail, monotonicity gives

\[
\sum_{n=5}^{\infty}(1+20n)^{-3/2}
\le\int_4^{\infty}(1+20y)^{-3/2}dy=\frac1{90}.
\tag{S7}
\]

Adding this conservative tail to the original rational certificate yields, for **every finite N** and every real a,

\[
e^2C_N(a)
<\frac{100}{137(314/100)}
\left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}+\frac1{90}\right)\right]
=\frac{67743204500}{274510827927}<\frac14.
\tag{S8}
\]

The strict margin below one quarter is exactly 3538009927/1098043311708. With the already proved positive matched susceptibility, Z_N(a)>3/4. Thus the old N=4 certificate was unnecessarily narrow: denominator control survives all finite Landau cutoffs at the fixed window. This does not contradict section 2; the longitudinal window has not been removed.

For a nested coefficient family at fixed K and b, the same argument gives the uniform-a tail bound

\[
e^2\sup_a|C_{\infty,K}(a)-C_{N,K}(a)|
\le\frac{\alpha K}{\pi\sqrt{1+2bN}}.
\tag{S9}
\]

Here already retained weights/nodes stay fixed as N increases; otherwise the sequence changes its old coefficients too. This proves uniform convergence of this coefficient series alone. It supplies neither a convergent quantum-state sequence nor a bound on the renormalized current, energy, tangent, pressure or noise. For a finite pure vacuum start and normalized impulse, the same field envelope holds uniformly over this fixed-window family; passing the dynamical trajectories to an infinite-state solution requires separate compactness and limit-identification arguments.

## 4. A discrete counterexample blocks careless reuse of the exact integral

Positive quadrature weights and polynomial exactness do not imply that the discrete sum is maximized at a=0. Retaining only N=0, take b=10, K=200 and the exact two-node Gauss–Legendre rule. Its nodes are +/-K/sqrt(3), each longitudinal weight K. At a=K/sqrt(3), one mode has p=0 and contributes

\[
e^2 C_{\rm quad}(a)\ge\frac{\alpha bK}{4\pi}.
\tag{S10}
\]

Using the frozen coupling and matching, the independently evaluated values are:

| Quantity | Value |
|---|---:|
| Discrete Z at a=0 | 1.00580868437 |
| Discrete Z at a=K/sqrt(3) | -0.15560104840 |
| Exact-integral minimum Z for the same K,N,b | 0.99806595293 |

The margins are large; nevertheless these displayed decimals are high-precision evaluations, not interval enclosures. The exact node construction and lower-bound formula expose the mechanism. A coarse node can land on the sharp kernel maximum with a large weight while most of the true integration interval contributes little.

This is a deliberately underresolved regulator and a falsifier of transferring the integral certificate to arbitrary quadrature. It does not claim the selected K=20, 1024-node run is defective. Its denominator already has a different all-node-count rational certificate. A new integral-based certificate for larger windows needs either quadrature error bounds uniform in a or a separate exact/rational discrete bound.

## 5. A restricted positive tangent energy, and its own counterexample

The advisor proposed a stationary-vacuum extension. I checked it directly, without assuming that a C^2 nonlinear family exists uniformly for all time. Fix the finite coefficients, set the background F=x=0 and r_i=-h_i/omega_i, with constant a, and assume Z_0>0. For tangents with h_i dot eta_i=0 initially, set

\[
t_i=\partial_p(h_i/\omega_i)
=\hat z/\omega_i-p_i h_i/\omega_i^3,
\qquad q=-v,\qquad s_i=\eta_i+q t_i.
\tag{S11}
\]

Tangency is preserved. The stationary linear equations become

\[
s_i'=2h_i\times s_i+u t_i,\qquad
u'=\frac{f-e^2\sum_iw_i s_{iz}}{Z_0},\qquad q'=u.
\tag{S12}
\]

Because h_i dot s_i=0, omega_i s_i dot t_i=s_iz. Therefore the positive semidefinite quadratic form

\[
\mathcal E=Z_0u^2+e^2\sum_iw_i\omega_i|s_i|^2
\tag{S13}
\]

obeys the exact identity Ecal'=2uf. For f=0 it is conserved, and |u|<=sqrt(Ecal(0)/Z_0) for all time. For an integrable tangent drive, the same epsilon-regularized energy argument gives

\[
|u(t)|\le\sqrt{\mathcal E(0)/Z_0}
+\frac1{Z_0}\int_0^t|f(s)|ds.
\tag{S14}
\]

This is an all-time electric-tangent statement about a **stationary vacuum**, rather than the already pumped production background. It uses a quadratic energy; the earlier signed first variation delta W remains insufficient.

The tangency hypothesis cannot disappear: off that tangent plane the computed derivative has an extra term -2e^2 u sum_i w_i p_i(h_i dot eta_i)/omega_i^2. For genuine differentiable two-sided pure-state initial families, tangency is automatic. An arbitrary array of perturbations need not satisfy it.

Nor does Ecal control the full raw tangent. An exact one-mode secular solution has M=w=e^2=1, p=0, Z_0=3/4 and

\[
u=1,\quad q=t,\quad v=-t,\quad
\eta=(0,-1/2,-t),\quad s=(0,-1/2,0),\quad
\mathcal E=1.
\tag{S15}
\]

Every linearized equation holds, the electric tangent stays bounded and the positive energy is constant, while |eta| grows linearly. This directly disproves full-tangent boundedness even for this stationary example. The vacuum-manifold zero direction must not be called a residual gauge transformation at fixed canonical grid: the simultaneous grid shift required by the contract is a different variation.

A separate small matrix check uses y=(u,s_y,s_z), A=[[0,0,-4/3],[0,0,-2],[1,2,0]] and G=diag(3/4,1,1). Exact algebra verifies A^T G+GA=0. Numerical matrix exponentials at t=0,0.3,1,10 check conservation for generic data; the executed result and fixed tolerance are recorded in `skeptic_checks_results.json`. This is a representation check of the restricted linear model, not a new production ODE run.

## 6. Gravity and original four fronts remain separate obligations

The Bianchi-I identity Cdot=-theta C-kappa Q is accepted for the displayed spatial evolution equations. In an expanding regular volume it damps homogeneous constraint errors; in contraction it can amplify them. No statement survives a zero volume automatically. An external current with omitted apparatus stress leaves Q=-E J_ext and drives a constraint defect even from zero initial constraint. Setting the pump to zero later does not retroactively repair that defect. Keeping B constant in transversely expanding space also needs a support mechanism.

Zahn's current construction and his stress argument have different scopes. Section 4.2 restricts the stated nonperturbative stress treatment to constant mass and vanishing gauge curvature, discussing a perturbative alternative. It cannot be used as an already evaluated strong-field Bianchi-I quantum closure. [Zahn, sections 4.1–4.3](https://arxiv.org/html/1210.4031v3).

The original four research fronts are context and targets, not consequences of S8 or S14:

- **WGC and Festina Lente:** light scalar forces distinguish repulsive-force and charge-to-mass versions; the de-Sitter discharge assumptions of FL are not premises proved by a flat finite model. A generic q/m>=1 sentence lacks normalized charge and Planck conventions. [Heidenreich, Reece and Rudelius](https://arxiv.org/abs/1906.02206), [Montero and collaborators](https://arxiv.org/abs/2106.07650).
- **Magnetized curved pair creation:** static matching and homogeneous retarded current do not provide an in-in current and both directional stresses in curved geometry. Field strength alone does not set the gravitational curvature. A low-order Euler–Heisenberg polynomial cannot be silently extended to every strong-field, high-curvature frequency regime.
- **Cauchy-horizon fate:** a spherically symmetric Einstein–Maxwell–scalar mass-inflation theorem has specific data regularity and decay assumptions. It is not charged-Dirac quantum backreaction or a proof of the quantum endpoint. The recent rough-data result explicitly states its regularity class and a conditional Price-law component. [Rossetti](https://arxiv.org/abs/2506.08075).
- **Photon–graviton conversion:** longitudinal static susceptibility cannot replace the full transverse, frequency-dependent polarization and mixing blocks. The 2026 one-loop analysis includes diagrams and a gravitational Ward test that a naive two-level scalar susceptibility insertion omits. This round checked the abstract and version record, not every integral in the paper. [Ahmadiniaz and collaborators](https://arxiv.org/abs/2601.23279).

Nothing in this review tests or validates metaphysical claims. Historical topics elsewhere in the observatory do not supply mathematical premises for the proof graph.

## 7. Experiments that can actually distinguish hypotheses

| Hypothesis or bridge | Decisive next test | Stopping condition |
|---|---|---|
| An exact-integral gap predicts discrete conditioning after controlled refinement | Compare coefficient curves at fixed K,N over a including every node and boundary; use a uniform quadrature bound or explicit discrete certificate | Do not promote integral positivity when any discrete gap fails |
| Fixed-window Landau coefficient convergence helps an infinite-mode dynamics construction | First use S9 for C only; then separately derive high-mode current/energy tails for a fixed admissible state and source | Stop at the first observable without a uniform tail; no limit of C proves convergence of S |
| Renormalized joint-cutoff current has a finite limit despite divergent pieces | Derive the common subtraction before splitting; track S, C x' and their combination with one scheme and physical preparation | A cancellation observed at one time is not a uniform-in-time theorem or a numerical accuracy guarantee |
| Stationary positive quadratic energy extends to a pumped background | Differentiate a candidate time-dependent quadratic form including all extra background-work terms; test its sign on adversarial perturbations | Indefinite or uncontrolled terms block an all-time bound; keep the stationary theorem |
| A covariant pressure closure can source Einstein equations | Compute current, energy and both pressures independently from one state/counterterm action; evaluate total Ward defect and G8 | Reject a source manufactured to satisfy conservation by defining the missing pressure from it |
| A causal numerical probe is the derivative of the actually executed background | Exercise nonzero baseline probe amplitude, zero/negative pulse amplitudes, support endpoints and source-free cases | Any mismatch between nominal and executed source requires new metadata and corrected reruns before promotion |

The planner should treat failed sufficient routes as blocked routes, not impossibility proofs. In particular, failure of uniform Z coercivity blocks our current continuation strategy in the joint limit; it does not prove that no other mathematical representation can work. Every new edge must carry its regulator, state, time interval and approximation assumptions.

## 8. Executed evidence and limits

`skeptic_checks.py` imports no production solver. It contains exact SymPy identities, exact Fraction inequalities, independent high-precision integrals, a deliberately failing integral-to-quadrature inference, monotone cutoff examples, the stationary tangent energy and its secular counterexample, and a small matrix-propagator check. Full counts, hashes, settings, tolerances and outcomes are in `skeptic_checks_results.json`.

The check suite is evidence for those identities and falsifiers. It is not a formal proof assistant, exhaustive physical-model validation or an interval enclosure of floating time evolution. The review is complete at the stated scope; remaining obligations are explicitly retained in `claim_verdicts.json`.
