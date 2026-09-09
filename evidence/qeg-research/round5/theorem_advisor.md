# Conditional theorem for the finite Maxwell–Dirac model

Advisor review, 9 September 2026. This is a conventional mathematical proof for the explicitly defined finite model from round 4. It is not a new theorem about continuum quantum electrodynamics or semiclassical Einstein equations, and it is not a machine-checked Lean proof. The exact identities below supply a useful forward chain from assumptions to consequences; the continuation criterion supplies the backward chain from the target to the estimates that must be proved.

**Decision:** accept global forward existence and uniqueness, an explicit electric-field energy bound, finite-time differentiability under the stated parameter regularity, and retarded support. Accept the analytic certificate \(Z(a)>3/4\) for every real potential \(a\) at the selected finite regulator. Reject the stronger inference that this proves all-time tangent stability, quantum fluctuation control, a continuum limit, or gravitational backreaction.

## 1. Model assumptions, rather than unqualified physical axioms

Let \(I=\{1,\ldots,L\}\) be a fixed finite nonempty mode list. For every mode fix \(w_i>0\), \(M_i>0\), and \(k_i\in\mathbb R\). Fix \(e^2>0\) and a finite real susceptibility \(\chi\). None of these quantities varies with time. Let the prescribed drive \(F\) be continuous on \([0,\infty)\). Set

\[
p_i=k_i-a,\qquad \omega_i=(M_i^2+p_i^2)^{1/2},\qquad
\mathbf h_i=(M_i,0,p_i),
\tag{T1}
\]

\[
S=\sum_iw_i\left(r_{iz}+\frac{p_i}{\omega_i}\right),\quad
C=\sum_iw_i\frac{M_i^2}{4\omega_i^5},\quad
D=\sum_iw_i\frac{5M_i^2p_i}{8\omega_i^7},\quad
Z(a)=1+\chi-e^2C(a).
\tag{T2}
\]

The exact real-arithmetic evolution under examination is

\[
a'=-x,\qquad
x'=\frac{F-e^2(S+Dx^2)}{Z},\qquad
\mathbf r_i'=2\mathbf h_i\times\mathbf r_i.
\tag{T3}
\]

Initial data are finite and obey \(|\mathbf r_i(0)|\le1\). Finally assume the **global coefficient bound**

\[
Z(a)\ge z_*>0\qquad\text{for every }a\in\mathbb R.
\tag{T4}
\]

These assumptions define a flat, homogeneous, fixed-magnetic-background mean-field model with a fixed finite regulator. The matching prescription in T2 is part of the assumed model. Proving consequences of that prescription does not independently derive its physical correctness. The proof is insensitive to the canonical momenta's spacing; it requires positivity and finiteness of the weights and masses.

The condition \(|\mathbf r|\le1\) is precisely positivity of the unit-trace two-dimensional density matrix \((I+\mathbf r\cdot\boldsymbol\sigma)/2\). Pure blocks have norm one; strictly mixed blocks have norm less than one. This mathematical extension does not assert that every such list is a continuum Hadamard state. The production preparation is the particular pure vacuum list \(\mathbf r_i(0)=-\mathbf h_i(0)/\omega_i(0)\), with \(x(0)=0\).

## 2. The target theorem

Under T1–T4, the initial-value problem has a unique classical solution for all \(t\ge0\). Define

\[
U=\sum_iw_i(\mathbf h_i\cdot\mathbf r_i+\omega_i),\qquad
W=\frac12Zx^2+e^2U,\qquad W_0=W(0).
\tag{T5}
\]

For every finite \(t\ge0\),

\[
U(t)\ge0,\quad W(t)\ge\frac{z_*}{2}x(t)^2,\quad
W'(t)=x(t)F(t),
\tag{T6}
\]

\[
\boxed{
|x(t)|\le \sqrt{\frac{2W_0}{z_*}}
+\frac1{z_*}\int_0^t|F(s)|\,ds.}
\tag{T7}
\]

If \(F\in L^1([0,\infty))\), T7 uniformly bounds the electric field, and T6 uniformly bounds \(W\) and \(U\). Every Bloch vector remains in its initial sphere. The proof gives a bound for \(a\) on every finite interval, and at most linear growth of \(|a|\) when \(F\in L^1\). It does **not**, for general pure-state data, establish a uniform bound on the entire state vector for all time.

## 3. Proof, with the zero-energy case retained

**Local existence and uniqueness.** Each \(\omega_i\ge M_i>0\), and T4 keeps the denominator away from zero. Consequently the right side of T3 is continuous in time and smooth in all state variables on an open finite-dimensional state space. It is locally Lipschitz in those variables uniformly on compact time intervals. The local theorem and the compact-set continuation criterion apply. Relevant reference locations are Teschl §2.2, Theorem 2.2; §2.6, Theorem 2.13, Lemma 2.14 and Corollary 2.15. Smooth dependence and first variations are treated in §2.4, Theorems 2.10–2.11. These are standard ODE inputs; the estimates that make them applicable here are derived next. [Teschl, author-hosted text](https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf).

**Invariant state positivity.** Antisymmetry of the cross product gives

\[
\frac{d}{dt}|\mathbf r_i|^2
=4\mathbf r_i\cdot(\mathbf h_i\times\mathbf r_i)=0.
\tag{T8}
\]

Thus the initial Bloch balls are invariant. Cauchy–Schwarz then yields, separately for every mode,

\[
\mathbf h_i\cdot\mathbf r_i+\omega_i
\ge\omega_i(1-|\mathbf r_i|)\ge0.
\tag{T9}
\]

The positive weights imply \(U\ge0\), and T4 gives the coercive field term in T6. There is no assumption that a signed, vacuum-subtracted continuum stress tensor is positive: T9 is a statement about this finite sum.

**Work identity.** Because \(p_i'=x\),

\[
\mathbf h_i'=(0,0,x),\qquad \omega_i'=p_ix/\omega_i,
\]

and the precession contribution to \((\mathbf h_i\cdot\mathbf r_i)'\) vanishes. Hence

\[
U'=xS,\qquad
C'=-\sum_iw_i\frac{5M_i^2p_ix}{4\omega_i^7}=-2Dx,
\qquad Z'=2e^2Dx.
\tag{T10}
\]

Direct differentiation, without an extra approximation, gives

\[
\begin{aligned}
W'&=\tfrac12Z'x^2+Zxx'+e^2U'\\
&=e^2Dx^3+x[F-e^2(S+Dx^2)]+e^2xS=xF.
\end{aligned}
\tag{T11}
\]

This cancellation would fail if the inertia correction, quadratic-current term and energy counterterm were chosen independently.

**Energy estimate at and away from \(W=0\).** A derivation that divides directly by \(\sqrt W\) is incomplete for the actual vacuum start, where \(W_0=0\). For \(\epsilon>0\), use T6 to obtain

\[
\frac{d}{dt}\sqrt{W+\epsilon}
=\frac{xF}{2\sqrt{W+\epsilon}}
\le\frac{|F|}{\sqrt{2z_*}}
\sqrt{\frac{W}{W+\epsilon}}
\le\frac{|F|}{\sqrt{2z_*}}.
\tag{T12}
\]

Integrate and send \(\epsilon\downarrow0\):

\[
\sqrt{W(t)}\le\sqrt{W_0}
+\frac{1}{\sqrt{2z_*}}\int_0^t|F(s)|\,ds.
\tag{T13}
\]

Combining \(|x|\le\sqrt{2W/z_*}\) with T13 proves T7. Negative or sign-changing drive is allowed because its absolute integral appears. A drive that removes energy does not invalidate the estimate. A field reversal does not produce a singularity.

**Continuation.** Suppose a maximal forward interval ended at a finite \(T_+\). Continuity of the drive makes \(\int_0^{T_+}|F|\) finite. T7 gives a finite constant \(X_{T_+}\) bounding \(|x|\), and

\[
|a(t)|\le|a(0)|+\int_0^t|x(s)|\,ds
\le|a(0)|+T_+X_{T_+}.
\tag{T14}
\]

Together with T8, this confines every state coordinate to a compact set. On that set T4 excludes a denominator boundary and T1 excludes a zero mass gap. Compact continuation extends the solution beyond \(T_+\), a contradiction. Therefore no finite forward endpoint exists. This proves the theorem.

**An extra mixed-state consequence.** If at least one retained block \(j\) is strictly mixed, write \(\delta_j=1-|\mathbf r_j(0)|>0\). Then

\[
U\ge w_j\delta_j\omega_j
\ge w_j\delta_j|k_j-a|.
\tag{T15}
\]

An \(L^1\) drive therefore gives the additional uniform bound
\(|a|\le|k_j|+\sup W/(e^2w_j\delta_j)\). This strengthens the theorem for that subclass. The positive gap \(\delta_j\) is essential to this estimate; it vanishes for the production pure-state preparation.

## 4. Proving the global denominator condition before running a trajectory

For any finite positive-weight model,

\[
0<C(a)\le C_*:=\sum_i\frac{w_i}{4M_i^3},\qquad
Z(a)\ge1+\chi-e^2C_*.
\tag{T16}
\]

This follows from \(\omega_i\ge M_i\). It is a sufficient bound, not a claim that all modes simultaneously attain their individual maxima at one potential. If the right side is nonpositive, the test is inconclusive; it does not prove that the actual \(Z(a)\) crosses zero. In contrast, a positive minimum sampled along one trajectory does not prove T4.

For the matched magnetic susceptibility, set \(z=1/(2b)>0\). The exact recurrence and Binet integral imply

\[
\begin{aligned}
b-\log(2b)-\psi(1+1/(2b))
&=\log z-\frac1{2z}-\psi(z)\\
&=2\int_0^\infty
\frac{t}{(t^2+z^2)(e^{2\pi t}-1)}\,dt>0.
\end{aligned}
\tag{T17}
\]

The integrand has a finite positive limit at the origin and decays at infinity, so the positivity claim does not depend on subtracting nearly equal floating-point digamma terms. Thus \(\chi_b>0\) for every \(b>0\). The two primary identities are [DLMF 5.5.2](https://dlmf.nist.gov/5.5.E2) and [DLMF 5.9.15](https://dlmf.nist.gov/5.9.E15). Only these identities, not a large-field asymptotic expansion, are used.

### Selected finite regulator: exact analytic certificate

Take \(b=10\), \(K=20\), and Landau indices \(n=0,1,2,3,4\) inclusive. For any exact Gauss–Legendre rule with a positive number of nodes, its longitudinal weights are positive and sum to \(2K=40\). Positivity and polynomial exactness are stated in [DLMF §3.5(v), equations 3.5.18–3.5.21](https://dlmf.nist.gov/3.5#v). Only exactness on the constant function is required here. With \(d_0=1\), \(d_{n>0}=2\),

\[
\sum_{i:n_i=n}w_i=\frac{b\,d_n(2K)}{4\pi^2},\qquad
M_n^3=(1+20n)^{3/2}.
\tag{T18}
\]

For \(n=1,2,3,4\), use the deliberately conservative exact bounds

\[
21\sqrt{21}>84,\quad41\sqrt{41}>246,\quad
61\sqrt{61}>427,\quad81\sqrt{81}=729.
\tag{T19}
\]

Since \(e^2=4\pi\alpha\),

\[
\begin{aligned}
e^2C_*
&=\frac{100\alpha}{\pi}
\left[1+2\sum_{n=1}^4(1+20n)^{-3/2}\right]\\
&<\frac{100}{137(314/100)}
\left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}\right)\right]\\
&=\frac{66325137500}{274510827927}<\frac14.
\end{aligned}
\tag{T20}
\]

The final strict comparison is exactly equivalent to
\(265300550000<274510827927\); the positive rational margin below \(1/4\) is \(9210277927/1098043311708\). Together with T17,

\[
\boxed{Z(a)>3/4\quad\text{for every real }a.}
\tag{T21}
\]

This certificate is independent of time, source amplitude, canonical-grid translation, and longitudinal node count for the stated exact quadrature family. It is much more conservative than the recorded trajectory minimum \(0.9965117049606924\), because it bounds every mode by its separate worst case. No numerical trajectory is an input to T20.

The assumptions \(\alpha<1/137\) and \(\pi>3.14\) are ample. The frozen production source defines \(\alpha=1/137.035999084\); its defining decimal already implies the first inequality. The current NIST table inspected in this review lists a slightly different recommended central value, \(7.2973525643\times10^{-3}\), which also satisfies it. The historical solver constant has been preserved; the proof does not silently update the experiment. [NIST 2022 CODATA table](https://physics.nist.gov/cuu/pdf/wallet_2022.pdf).

For a normalized nonnegative compact pump \(F=\lambda g_T\), \(\int g_T=1\), and the exact production vacuum preparation \(W_0=0\), T7 yields

\[
\boxed{|x(t)|\le4|\lambda|/3\qquad(t\ge0).}
\tag{T22}
\]

For \(\lambda=1\), this is an all-time electric-field amplitude bound \(4/3\). It neither predicts the detailed waveform nor bounds its amplitude derivative by \(4/3\). Differentiating an inequality between nonlinear solution families does not produce an inequality between their derivatives.

### Exact quadrature, rounded coefficients, and a computed trajectory are different claims

The selected code creates weights and masses in IEEE double precision. At 1,024 nodes the observed weight totals differ from the usual double-precision expression for T18 by approximately \(-1.78\times10^{-15}\) in level zero and \(-3.55\times10^{-15}\) in each other level. This is harmless as a diagnostic, but an approximate equality is not the exact Gauss–Legendre identity.

A separate check performed in this review interpreted every generated weight, mass, \(e^2\), and \(\chi\) as its exact binary rational. Grouping weights by their five repeated masses and using rational arithmetic in T16 produced the **exact comparison**

\[
1+\widehat\chi-\widehat{e^2}\sum_i
\frac{\widehat w_i}{4\widehat M_i^3}>3/4.
\tag{T23}
\]

Its decimal display is approximately \(0.7653173589206453\), with a margin approximately \(0.015317358920645334\). Every generated weight was positive and every mass positive. This certifies the real-arithmetic ODE using that rounded coefficient list, provided its initial vectors satisfy the exact norm condition. It does not certify accumulated floating-point time-stepping errors or an interval enclosure of the recorded trajectory. The saved trajectory has small nonzero norm defects, so it cannot itself be called an exact invariant-ball solution.

Reproduction recipe for T23: generate the frozen `response.Grid(response.Params(nK=1024))`; convert floats using `Fraction.from_float`; sum the weights in each Landau group exactly; divide by four times that group's exact rational mass cubed; multiply by the exact rational `response.E2`; compare `1 + Fraction.from_float(response._chi(10)) - E2*Cstar` with `Fraction(3,4)`. No floating transcendental function is being certified by that operation: the already evaluated coefficient is the rational model input. The original analytic susceptibility is certified separately by T17.

## 5. Tangent existence, causality, and the missing stability inference

Let \(Y=(a,x,\mathbf r_1,\ldots,\mathbf r_L)\). For a source family \(F(t;\lambda)\) with continuous first parameter derivative and an admissible continuously differentiable initial-data family, standard parameter dependence gives a first variation on each compact time interval. If the complete drive/data family is \(C^k\), the corresponding solution family is \(C^k\); a merely continuous drive does not imply unlimited differentiability with respect to time. The smooth compact production pulse meets the stronger hypothesis.

For the fixed canonical grid define \(v=\partial_\lambda a\), \(u=\partial_\lambda x\), \(\boldsymbol\eta_i=\partial_\lambda\mathbf r_i\), \(q_i=-v\) and \(f=\partial_\lambda F\). Direct differentiation gives

\[
\begin{gathered}
\delta S=\sum_iw_i(\eta_{iz}+M_i^2q_i/\omega_i^3),\\
\delta C=-\sum_iw_i\frac{5M_i^2p_iq_i}{4\omega_i^7},\quad
\delta D=\sum_iw_i\frac{5M_i^2(M_i^2-6p_i^2)q_i}{8\omega_i^9},\\
v'=-u,\qquad
u'=\frac{f-e^2(\delta S+\delta D x^2+2Dxu)+e^2\delta C x'}{Z},\\
\boldsymbol\eta_i'=2\mathbf h_i\times\boldsymbol\eta_i
+2(0,0,q_i)\times\mathbf r_i.
\end{gathered}
\tag{T24}
\]

Writing this as \(\delta Y'=A(t)\delta Y+B(t)f\), with \(B=\mathbf e_x/Z\), its continuous coefficients are bounded on each fixed finite interval. If \(\Phi(t,s)\) is the fundamental matrix,

\[
\delta Y(t)=\Phi(t,0)\delta Y(0)
+\int_0^t\Phi(t,s)B(s)f(s)\,ds.
\tag{T25}
\]

This proves retarded support: if initial variations vanish and the source variation vanishes before \(t_p\), every tangent is zero before \(t_p\). For a bound \(\|A(t)\|\le L_T\) on \([0,T]\),

\[
\|\delta Y(t)\|\le e^{L_Tt}
\left(\|\delta Y(0)\|+\frac1{z_*}\int_0^t|f(s)|\,ds\right).
\tag{T26}
\]

This finite-time estimate supplies existence and continuous dependence, not a useful uniform-in-time stability constant. Neither \(L_T\) nor its exponential has been bounded independently of \(T\).

Two exact tangent facts require especially careful wording:

* \((\mathbf r_i\cdot\boldsymbol\eta_i)'=0\), but this conserved value is zero only when the initial family has fixed norm to first order. A mixed family \(\mathbf r(\lambda)=(\lambda,0,0)\) at \(\lambda=1/2\) has \(\mathbf r\cdot\boldsymbol\eta=1/2\). The pure-state tangent constraint must not be imposed on every mixed-state variation.
* \(\delta W=Zxu-e^2\delta C\,x^2/2+e^2\delta U\) is signed and obeys \((\delta W)'=uF+xf\). It is not a positive quadratic norm of the tangent. Conservation of \(\delta W\) after source shutoff cannot prove tangent stability.

A concrete falsifier of the latter inference uses one mode, \(M=w=e^2=1\), \(k=a=x=0\), \(\chi=F=0\), and the admissible rotated initial family \(\mathbf r(\lambda)=(-\cos\lambda,0,\sin\lambda)\). At \(\lambda=0\), the baseline is stationary, \(Z=3/4\), \(\delta W=0\), but \(\eta_z=1\) and \(u'(0)=-4/3\). A nonzero response is compatible with zero first-variation energy. This example does not claim an instability; it invalidates that proposed stability diagnostic.

## 6. Assumptions that cannot be silently deleted

| Proposed shortcut | Why the proof fails or the interpretation changes |
|---|---|
| Only check \(Z>0\) at sampled times | There is no all-potential margin; denominator degeneracy can occur elsewhere or between samples. |
| Declare failure whenever T16 is nonpositive | T16 is sufficient, not necessary; its separate mode maxima may overestimate the actual maximum of \(C(a)\). |
| Allow \(M_i=0\) without a new analysis | \(p_i=0\) can make the square-root derivatives and counterterms undefined; smoothness and T16 no longer follow. |
| Allow negative weights | The sum of individually nonnegative modal energies need not be nonnegative. |
| Permit \(|\mathbf r_i|>1\) | State positivity and T9 fail. For \(M=1,p=0,\mathbf r=(-2,0,0)\), the modal energy is \(-1\). |
| Use arbitrary time-dependent weights, masses or matching | T10–T11 acquire extra work and parameter-derivative terms. |
| Replace the finite sum with an infinite limit | Uniform coercivity, renormalized-energy control, compactness and convergence have not been established. |
| Use a discontinuous or merely integrable drive but claim a classical smooth solution | One must instead state and prove an appropriate absolutely continuous/Carathéodory formulation. The present theorem uses a continuous drive. |
| Divide response by instantaneous \(x(t)\) | Ordinary field zeros make the ratio undefined; they are not evidence of an instability. |
| Differentiate the amplitude envelope T22 to bound \(u\) | Derivatives cannot be inferred from an inequality between function values. |
| Call the energy bound a quantum-noise estimate | No symmetrized current or stress fluctuation observable appears in the theorem. |
| Insert the energy alone into Einstein equations | A conserved covariant source also needs directional pressures, current/stress compatibility and gravitational constraints. |

## 7. Forward and backward proof connections

The forward chain is **finite admissible blocks → invariant Bloch balls → positive finite excitation energy → exact work balance → field envelope → compact finite-time state bounds**. The backward chain is **global solution target → continuation criterion → finite-time compactness and a nonsingular vector field → bounds on \(a,x,\mathbf r\) and a uniform \(Z\) margin**. They meet at T7, T8, T14 and T21. No edge is inverted simply because its forward implication is true.

The accepted theorem removes one concrete dependency: the selected finite dynamical model cannot develop a finite-time solution singularity from its own denominator or field amplitude under the stated continuous drive. It does not establish that its tangent stays uniformly small. The next proof obligations are distinct: a controlled infinite-regulator limit; a stronger stability norm or a discriminating instability result; fluctuation observables with physical smearing; and a common covariant current/stress closure. Those obligations must be added as open nodes rather than drawn as already proved consequences.

## 8. Review outcome and provenance

The round-4 acceptance file identifies the 1,024-node production run, source hash `0a197f5b46de8114d790c937059018d21df3f55a436c76067b91c09277035867`, fixed \(K=20\), and Landau indices zero through four. Its numerical response and finite-difference evidence remain numerical evidence. The theorem above is an additional analytic statement over the same declared model and a larger class of admissible initial data. It neither upgrades sampled errors into interval enclosures nor retrospectively erases underresolved runs.

The independent critic specifically challenged the zero-energy square-root step, all-time wording, mixed-state tangent normalization, and use of signed tangent work as a norm. Those challenges are addressed above. This advisor accepts T6–T7, T21–T22 and finite-time T24–T26 under their hypotheses. All-time tangent stability, continuum QED validity, quantum noise control and a gravitational solution remain **unproved**.
