# M2 forward: connected physical correlations on growing time windows

This is the tenth and final requested Round21 research loop. The derivation is independent of reverse M2 and the current skeptical M2. The proposed coefficient 6 is valid. The growing-window guarantee is sufficient for `0<=gamma<3/2`; this estimate does not establish convergence at its endpoint. An external process overwrote the initial shared-directory report, so this authored proof and its independent checker were restored in the isolated continuation checkout before admission. The imported source hashes are preserved separately. This repair counts no extra research loop.

## Fixed profile and units

Use precisely M1/H2's canonical full-link incomplete tensor product, with selected complete three-face strips fixed, reference ground Omega, `H_0=H_ref`, and reference ground energy zero. Keep spacing, positive `alpha/E_star`, E_star, hbar, and `0<eta<1` fixed. For `0<q<1`,

\[
 B(q)=\frac{2+5q+5q^2+6q^3+3q^4}{24(1-q)^3(1+q)^2(1+q^2)},
 \quad \tau_q=\frac{\eta}{8B(q)},
 \quad V_q=-\alpha\tau_q\sum_{f\in O}w_f(q)x_f,
 \quad w_f(q)=q^{|\operatorname{anchor}(f)|_1}/24.
\]

Let `H_q=H_0+V_q`, `H_q Psi_q=e_q Psi_q`, and `P_q=|Psi_q><Psi_q|`. H2 and M1 admit

\[
 \|V_q\|=\alpha\eta/8,\quad \bar g=\alpha(1-\eta)/8>0,
 \quad\sigma_q^2=\|V_q\Omega\|^2=\alpha^2\tau_q^2B(q^2)/96,
\]
\[
 d_q:=\|P_q-P_0\|\le\sigma_q/\bar g,
 \qquad -\sigma_q^2/\bar g\le e_q\le0.\tag{1}
\]

Here q and tau are dimensionless spatial-action deformations, eta is a dimensionless budget fraction, sigma and gbar have energy units, and hbar has energy-times-time units. They do not identify the conditional K/L diffusion clock with this Hamiltonian. The q=1 series is outside the summable family.

## Reconstructing the physical sector for this profile

A2 gives `H_0>=delta(1-P_0)`, `delta=alpha/8`, with unique ground Omega. V_q is an operator-norm convergent bounded self-adjoint Wilson series and has zero reference mean. Therefore `D(H_q)=D(H_0)` and the form domain is unchanged. On the form-domain vectors orthogonal to Omega its form is at least `delta-||V_q||=gbar`, whereas the form on Omega is zero. The codimension-one spectral argument of A2 gives one isolated eigenvalue `e_q<=0` and all remaining H_q spectrum at or above gbar. This reuses the argument with this profile's budget; it does not import the dyadic numerical threshold.

For every finite-support vertex assignment of SU(2) matrices, Haar pullback defines a unitary Gamma(g). Each selected-strip Hamiltonian and free-link Casimir commutes with it on the finite tensor core and on its closed domains. Every unique strip ground carries a continuous one-dimensional character of a finite product of SU(2); that character is trivial because SU(2) is connected with perfect Lie algebra. The free Haar grounds are invariant. Thus Gamma(g)Omega=Omega. Endpoint cancellation makes each Wilson multiplication invariant, so V_q, H_q and H_q's spectral projections commute with the gauge action. The unique ground line again has a trivial character, giving Gamma(g)Psi_q=Psi_q for every q in this profile.

Let A_phys be the norm closure of bounded finite-link-support operators invariant under every endpoint gauge group, and let H_inv be the vectors invariant under all finite-support gauge transformations. The full local-factor algebra in this fixed incomplete tensor product is irreducible: the finite-factor vacuum projections tend strongly to P_0; an operator commuting with the local algebra is consequently scalar on Omega and then on its dense local rank-one orbit. Every nonzero vector, including Psi_q, is therefore cyclic for the full local algebra. This is G2's representation argument, independent of its earlier dyadic coupling.

If xi is invariant, choose local A_n with A_n Psi_q tending to xi. Weak-operator Haar averaging over the finitely many endpoint groups produces a bounded invariant local E_n(A_n) supported on the same finite links. On the invariant vacuum,

\[
 \|E_n(A_n)\Psi_q-\xi\|
 \le\int\|\Gamma(g)(A_n\Psi_q-\xi)\|\,dg
 =\|A_n\Psi_q-\xi\|.
\]

Hence `closure(A_phys Psi_q)=H_inv`. The null-quotient map `[A] -> A Psi_q` is isometric and extends to a unitary from the physical GNS space onto H_inv. H_inv is proper in H_full: the trace of an open free z-link times Omega is nonzero and changes sign under the central gauge transformation at one endpoint.

Dynamics preserves A_phys. Approximate V_q in operator norm by finite-face partial sums V_q,N. For a local A, the conjugation by `H_0+V_q,N` remains supported on the finite union of complete factors meeting A and those faces. Strong bounded-perturbation Duhamel bounds its difference from the full conjugation by `2|t| ||A|| ||V_q-V_q,N||/hbar`, tending to zero at fixed time. Each approximant is invariant by gauge commutation. This establishes invariance of the stated norm closure without assuming point-norm continuity for every bounded reference-evolved operator.

H_inv reduces the spectral measure. Spectral cutoffs commuting with the gauge action prove that `D(H_0) intersect H_inv` is dense in H_inv. The restricted self-adjoint energy generator is

\[
 K_{q,\mathrm{phys}}=(H_q-e_q)|_{H_{\rm inv}},\qquad
 D(K_{q,\mathrm{phys}})=D(H_0)\cap H_{\rm inv},
\]
\[
 \operatorname{spec}K_{q,\mathrm{phys}}
 \subset\{0\}\cup[\bar g-e_q,\infty)
 \subset\{0\}\cup[\bar g,\infty).\tag{2}
\]

Its zero eigenspace is one-dimensional. The selected-strip reference has the analogous construction with e_0=0. No arbitrary bounded local operator is asserted to preserve this unbounded operator domain.

## Complex connected correlators and coefficient 6

Use an inner product linear in its second entry. For fixed bounded local gauge-invariant A,B, including nonselfadjoint operators, set `omega_q(X)=<Psi_q,X Psi_q>`, `U_q(t)=exp(-itH_q/hbar)`, and `U_tilde_q(t)=exp(-it(H_q-e_q)/hbar)`. Define

\[
 C_q^{A,B}(t)=\langle\Psi_q,A^*\widetilde U_q(t)B\Psi_q\rangle
             -\omega_q(A^*)\omega_q(B).\tag{3}
\]

The first subtracted mean equals the conjugate of omega_q(A). Because U_tilde fixes Psi_q, this is also the inner product of the centered A-vector with the evolved centered B-vector. At t=0 it is their complex covariance; for A=B=W selfadjoint it is the variance.

For normalized rank-one projections, `||P_q-P_0||_1=2d_q`: on the span of their vectors the nonzero eigenvalues of their difference are ±d_q. Therefore every bounded, possibly complex X satisfies

\[
 |\omega_q(X)-\omega_0(X)|\le2d_q\|X\|.\tag{4}
\]

Applying (4) to `X=A* U_tilde_q(t)B` changes the state in the uncentered term at cost at most `2d_q||A||||B||`. Next change the evolution in the reference expectation, at cost at most `||A|| ||(U_tilde_q-U_0)B Omega||`. Split the mean-product difference exactly as

\[
 [\omega_q(A^*)-\omega_0(A^*)]\omega_q(B)
 +\omega_0(A^*)[\omega_q(B)-\omega_0(B)].
\]

Each summand is bounded by `2d_q||A||||B||`. Thus the state and centering terms total `(2+2+2)d_q=6d_q`. This is a valid common upper coefficient; no optimality is asserted. Neither subtracted mean is omitted.

## Complete-factor support for all reference times

Let F_B be a finite set of complete reference factors supporting B. E(F_B) contains every link of those factors. The reference nonnegative sum splits as `H_0=H_F tensor I + I tensor H_Fc`, so its exponential factorizes by the spectral theorem. Consequently

\[
 B_s=U_0(s)B U_0(-s)
\]

acts on the same complete factors for every real s, has norm ||B||, and obeys `U_0(s)B Omega=B_s Omega`. These are bounded-operator/vector identities; B Omega need not lie in D(H_0).

M1's complete-support estimate applies uniformly in s:

\[
 \|V_qB_s\Omega\|\le\|B\|[\sigma_q+2\alpha\tau_qD_{F_B}(q)],
 \quad
 D_{F_B}(q)=\sum_{\substack{f\in O:\operatorname{links}(f)\cap E(F_B)\ne\varnothing}}w_f(q)
 \le |E(F_B)|/6.\tag{5}
\]

Strong bounded-perturbation Duhamel, extended from the common domain by density, gives

\[
 \|(U_q(t)-U_0(t))B\Omega\|
 \le\frac{|t|}{\hbar}\|B\|[\sigma_q+2\alpha\tau_qD_{F_B}(q)].\tag{6}
\]

The energy phase contributes at most `|t e_q| ||B||/hbar` by `|exp(it e_q/hbar)-1|<=|t e_q|/hbar`. Combining (3)–(6) proves the proposed estimate:

\[
 \boxed{|C_q^{A,B}(t)-C_0^{A,B}(t)|
 \le\|A\|\|B\|\left[6d_q+\frac{|t|}{\hbar}
 (|e_q|+\sigma_q+2\alpha\tau_qD_{F_B}(q))\right].}\tag{7}
\]

For |t|<=T an explicit sufficient upper bound is

\[
 \boxed{\sup_{|t|\le T}|C_q^{A,B}(t)-C_0^{A,B}(t)|
 \le\|A\|\|B\|\left[\frac{6\sigma_q}{\bar g}
 +\frac{T}{\hbar}\left(\frac{\sigma_q^2}{\bar g}+\sigma_q
 +\frac{\alpha\tau_q|E(F_B)|}{3}\right)\right].}\tag{8}
\]

It covers t=0 and negative times. A positive spectral gap does not imply real-time decay, and no such decay is claimed. The observables and their factor covers are fixed before taking the limit; growing supports require their own examination of (8).

## Growing windows and endpoint scope

Write epsilon=1-q. The exact rational profile gives

\[
 \epsilon^3B(q)\to7/64,\quad
 \tau_q/\epsilon^3\to8\eta/7,\quad
 \sigma_q^2/(\alpha^2\epsilon^3)\to\eta^2/5376.\tag{9}
\]

The four terms in (8) have orders `epsilon^(3/2)`, `(alpha T/hbar)epsilon^3`, `(alpha T/hbar)epsilon^(3/2)`, and `(alpha T/hbar)epsilon^3`. For fixed C>0 and

\[
 T_q=(\hbar/\alpha)C\epsilon^{-\gamma},\qquad0\le\gamma<3/2,
\]

all vanish, yielding

\[
 \sup_{|t|\le T_q}|C_q^{A,B}(t)-C_0^{A,B}(t)|
 =O(\epsilon^{3/2-\gamma}).\tag{10}
\]

At gamma=0 this includes every fixed compact time interval with sufficient error exponent 3/2. At gamma=3/2, the right side's term `T_q sigma_q/hbar` tends to `C eta/sqrt(5376)>0`; its square tends to the exact positive rational `C^2 eta^2/5376`. The sufficient estimate cannot guarantee endpoint convergence. Beyond the endpoint this term diverges. Neither statement proves failure of the actual correlator limit. Oscillatory cancellation or a sharper estimate could improve the range; no such improvement is examined here.

## An eventual nonzero physical Wilson fluctuation

Take the actual omitted origin-xz Wilson loop `W=Tr(U_f)/2`, of norm one and invariant under every local gauge. Its two z-links are free Haar factors. Integrating either one gives `omega_0(W)=0`, `omega_0(W^2)=1/4`, independently of internal strip entanglement. Equation (4) yields

\[
 \operatorname{Var}_{\Psi_q}W\ge1/4-2d_q-4d_q^2.
\]

This lower expression decreases on nonnegative d. Thus

\[
 \frac{\sigma_q^2}{\bar g^2}
 =\frac{\eta^2B(q^2)}{96(1-\eta)^2B(q)^2}\le\frac1{256}
 \quad\Longrightarrow\quad
 \boxed{\operatorname{Var}_{\Psi_q}W\ge7/64.}\tag{11}
\]

This holds eventually for every fixed eta in (0,1). A simpler explicit region uses `B(q)>=1/[12(1-q)^3]` from the two non-xy orientations and `B(q^2)<=1/[8(1-q^2)^3]` from all orientations:

\[
 \frac{\sigma_q^2}{\bar g^2}
 \le\frac{3\eta^2}{16(1-\eta)^2}
 \left(\frac{1-q}{1+q}\right)^3.
\]

Hence `((1-q)/(1+q))^3 <= (1-eta)^2/(48 eta^2)` suffices. In particular eta=1/2 and every q>=3/4 satisfy this condition, with upper bound `3/5488<1/256`. Equation (11) is a certified sufficient floor, not measured variance. It gives a nonzero physical vector `(W-omega_q(W))Psi_q` orthogonal to the vacuum. Equation (2) governs its spectral support, while (10) governs the convergence of the fixed-observable connected correlation.

## Executable checks and provenance

The checker imports no other research implementation. It uses exact fractions and Gaussian rationals, independently reconstructs the profile class-sum identity and complete strip geometry, and bounds square roots by rational intervals. The finite profile rows illustrate the certified error budget; equation (9), not sampled values, proves its asymptotic order.

The origin-xz displayed support has four links, but its complete factor cover has 22 links and 28 incident omitted faces. The omitted xz face at `(2,1,0)` meets that cover and misses the displayed links. Independent direct face enumeration checks the incidence construction. A two-link-factor controlled-phase matrix also shows why conjugation can spread within a factor while preserving its complete support.

Discriminating controls include complex adjoint centering at t=0, both mean-product differences, missing centering, the exact pure-projector factor 2, and the omitted energy shift: for `H=diag(-1,1)`, identity observables and `t=pi/2`, the raw connected expression is `i-1`, whereas the correctly shifted identity correlation is zero. A finite invariant-sector example illustrates a proper reducing subspace and shifted generator, without purporting to prove the infinite theorem. A gap-budget control rejects unsupported use of the dyadic threshold but does not infer an actual gap below that threshold. The endpoint test rejects only sufficiency. Input checks reject Booleans, floating coefficients, excluded parameter endpoints and nonpositive physical scales. Every acceptance check uses explicit exceptions, so optimized Python retains it.

The complete direct-input manifest binds code, this proof, the frozen M2 contract and M1 selection gate, immutable instruction snapshots, and each consulted inherited report with its admission gate. Each inherited report is checked against its accepted gate. Every source component is checked for symlinks and all sources are rehashed before writing fresh outputs. Mutable live AGENTS/skills are not producer inputs. Normal and optimized executions validate this one loop.

```bash
python3 -B research/round21/forward/m2/check.py --output /absolute/new/m2-forward-output
python3 -B -O research/round21/forward/m2/check.py --output /absolute/new/m2-forward-optimized
```

The project contribution is this explicit profile-dependent physical correlation estimate, its sufficient growing-time range, and its quantitative nonzero-fluctuation region. Trace distance, gauge averaging, GNS reconstruction, spectral restriction and Duhamel are established mathematics; scientific priority is unverified. The limit is the fixed selected-strip theory. No nonzero homogeneous omitted coupling, finite clipped-restriction convergence, conditional-diffusion matching, continuum construction, Clay mass gap or physical double-Fibonacci law follows. No further research loop is executed.
