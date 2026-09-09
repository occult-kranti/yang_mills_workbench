# Local dynamics on growing Yang–Mills lattices

**Status:** a conditional finite-spacing locality theorem, with explicit arithmetic and graph checks. Independent review is separate. This is an application of the Lieb–Robinson method; no mathematical novelty, ground-state gap, Lorentz invariance or continuum Yang–Mills construction is claimed.

The useful workaround for the previous extensive volume bound is to ask a different, local question: how much can changing a distant boundary change the evolution of one bounded observable during a fixed time interval? The total potential norm grows with volume, but a chain of local interactions must reach the boundary before it can affect that observable. This avoids the total-volume factor for this dynamical question.

## 1. Exact contract and introduced quantities

Fix an open hypercubic spatial lattice with dimension `d_s >= 2`. Each geometric link is counted once with a chosen orientation; no periodic identifications, repeated links or nonlocal added interactions are allowed. Let `Lambda` and `Lambda_prime` be finite nested link sets, and include every elementary four-link plaquette fully contained in the corresponding set. Connected open boxes are the intended application. The estimate also allows disconnected finite sets and missing plaquettes when their incidence is declared explicitly.

Before imposing Gauss constraints, use

\[
\mathcal H_{\Lambda'}=\bigotimes_{e\in\Lambda'}L^2(SU(2),d\mu_H),\qquad
C_e=-\sum_{a=1}^3(L_e^a)^2,\qquad T_a=\sigma_a/2.
\]

Thus `C_e` is the unbounded nonnegative self-adjoint link Casimir with eigenvalues `j(j+1)`. The Hamiltonian is

\[
H_{\Lambda'}(u)=\sum_{e\in\Lambda'}\alpha_e(u)C_e
 +\sum_{p\subset\Lambda'}\lambda_p(u)(1-x_p),
\qquad x_p=\tfrac12\operatorname{Tr}U_p,\quad \|x_p\|=1.
\tag{L1}
\]

All coefficients are real and locally integrable in physical time. Positive `alpha_e` and nonnegative `lambda_p` recover the usual electric and magnetic sign convention. Positivity is unnecessary for this finite-time norm estimate. No differentiability of a drive is required. A volume-independent nonnegative envelope must exist:

\[
|\lambda_p(u)|\le j(u)\quad\text{a.e. for every plaquette},\qquad
J_{s,t}=\int_{\min(s,t)}^{\max(s,t)}j(u)\,du<\infty.
\tag{L2}
\]

The comparison Hamiltonian has exactly the same electric terms on `Lambda_prime`, and retains only plaquettes entirely in `Lambda`. Its extra exterior free dynamics does not affect an observable initially in `Lambda`; this supplies the common-Hilbert-space embedding. Shared coefficients must agree. The removed scalar `sum lambda_p` creates only a phase and drops out of every Heisenberg observable.

Let `A` be a bounded operator supported on a finite nonempty link set `X subset Lambda`. For physical claims, `A` is gauge invariant, such as a normalized Wilson trace around a loop. The estimate is first established on the full tensor product. All Casimirs and plaquette terms commute with vertex gauge transformations, so restriction to the common larger physical sector cannot increase its norm. This argument does not assert that physical Hilbert spaces themselves tensor-factor across the boundary.

| Quantity | Definition | What changes |
|---|---|---|
| `q = 2(d_s-1)` | Maximum plaquettes incident on one link | Fixed by spatial dimension |
| `J` | Absolute time-integrated uniform plaquette envelope | Driver and physical time |
| `R` | Smallest number of overlapping plaquettes from `X` to a removed plaquette | Boundary distance in the interaction graph |
| `z = 8 q J` | Dimensionless conservative propagation budget | Derived, not a new field or fitted mass |
| `F_R(z) = sum_{k=R}^infinity z^k/k!` | Positive factorial tail | Calculated observable-error bound |

More explicitly, `R` is the smallest `k >= 1` admitting plaquettes `p_1,...,p_k` with `p_1 intersect X` nonempty, consecutive plaquettes sharing a link, and `p_k` removed. A shortest such chain has all earlier plaquettes retained. Put `R = infinity` if none exists. Equivalently, make each link a vertex and connect two links when they belong to a common plaquette; `R` is the distance from `X` to a link outside `Lambda`, for the induced-volume comparison. Vertex proximity alone is not this distance. Inactive plaquettes may be removed from this graph only if their coefficient vanishes almost everywhere on the whole time interval.

## 2. Conditional theorem L: volume-independent finite-time comparison

Under the above contract, for either time ordering,

\[
\boxed{\quad
\|\tau_{\Lambda'}^{t,s}(A)-\tau_\Lambda^{t,s}(A)\|
\le \|A\|\min\!\left\{2,\frac{|X|}{4}
 F_R(8qJ_{s,t})\right\}.
\quad}
\tag{L3}
\]

Use `F_infinity = 0`. For zero drive, zero time, empty support or no connecting plaquette chain, the difference is exactly zero. The bound needs no representation cutoff and no bound on the electric Casimirs. A bounded observable error also bounds the expectation difference in any one common normalized state. It does not compare two separately chosen ground states or thermal states.

### Step 1: remove the unbounded onsite dynamics without expanding it

Set

\[
U_0(u,s)=\bigotimes_e
\exp\!\left[-iC_e\int_s^u\alpha_e(v)\,dv\right].
\tag{L4}
\]

Spectral calculus defines each factor as a strongly continuous unitary. A tensor of onsite unitaries leaves support unchanged. In the interaction picture the nonconstant terms are

\[
\Phi_p^I(u)=-\lambda_p(u)U_0(u,s)^*x_pU_0(u,s),
\qquad\operatorname{supp}\Phi_p^I\subseteq p,
\qquad\|\Phi_p^I(u)\|\le j(u).
\tag{L5}
\]

For finite volume their sum is strongly measurable with an integrable norm envelope. Its Dyson series is defined by strong integrals: the `n`th term is norm-bounded by the `n`th scalar exponential term. The interaction-picture series produces a unitary absolutely continuous propagator on vectors and justifies the integral identities below. For merely integrable coefficients, (L1) is interpreted through this mild interaction-picture construction; it does not assert that an arbitrary state lies in the instantaneous unbounded Hamiltonian domain. The full propagator is strongly continuous; absolute continuity on every vector is asserted here only for its bounded interaction-picture factor. This does **not** require norm continuity of `U_0^* x_p U_0` or of every bounded local observable. It also does not expand an unbounded commutator `[C_e,A]` in operator norm. Both compared evolutions use the same `U_0`; undoing it preserves support and norm of their common input.

### Step 2: a commutator recursion with unitary resummation

For a bounded interaction evolution and a fixed bounded `B`, define

\[
C_B(S;t,s)=\sup_{0\ne O\in\mathcal A_S}
\frac{\|[\tau^{t,s}(O),B]\|}{\|O\|}.
\]

Separating all interaction terms inside `S` gives a support-preserving internal unitary. Apply the Jacobi identity to the remaining commutator equation and remove its homogeneous commutator by another unitary conjugation. The resulting integral inequality is

\[
C_B(S;t,s)\le C_B(S;s,s)
 +2\sum_{p:p\cap S\ne\varnothing}
 \int_s^t\|\Phi_p^I(u)\| C_B(p;u,s)\,du
\tag{L6}
\]

for `s <= t`; a reversal of the time parameter covers the opposite order. One may first sum only terms crossing `S`; including all intersecting plaquettes enlarges the nonnegative bound. The initial term vanishes if `S` misses `supp B` and is at most `2||B||` otherwise. For measurable coefficients, the same integral argument holds almost everywhere, or follows by integrable coefficient approximation with finite-volume Duhamel control.

Iterating (L6), the nonzero terms are overlapping plaquette chains from `S` to `supp B`, carrying a factor `2` for each recursion. The remainder tends to zero: after its first step each support has four links, at most `4q` next plaquettes, and `C_B <= 2||B||`. Unitary resummation is essential here. A raw nested-commutator expansion with the union of all visited supports would have growing branching counts and would not justify this chain estimate.

### Step 3: compare the two volumes by Duhamel

Write the interaction-picture difference as the integral of

\[
i\,\tau_{\Lambda'}^{u,s}
\bigl([\Phi_{\rm removed}^I(u),
                 \tau_\Lambda^{t,u}(A)]\bigr).
\tag{L7}
\]

Conjugations disappear in norm. Apply (L6), with reversed time on `[u,t]`, to each removed plaquette in (L7). Each resulting term is a chain whose last plaquette is removed; its previous plaquettes are retained. A chain with `k` plaquettes has `k` ordered time integrals, an overall factor `2^k ||A||`, and an integrand at most `product j(u_i)`. The first factor `2` is the terminal commutator in Duhamel; there is no additional factor `2` outside this count.

At most `|X| q` choices touch `X`. Any four-link plaquette intersects at most `4q` plaquettes, including itself and harmless overcounting. Thus the number of length-`k` chains is bounded by

\[
N_k\le |X|q(4q)^{k-1}.
\tag{L8}
\]

No chain has `k < R`. Symmetry of the scalar product integrand gives the ordered-integral identity

\[
\int_{s\le u_k\le\cdots\le u_1\le t}
\prod_{i=1}^k j(u_i)\,du_1\cdots du_k=\frac{J^k}{k!}.
\tag{L9}
\]

Consequently the un-capped difference is at most

\[
\|A\|\sum_{k\ge R}2^k|X|q(4q)^{k-1}\frac{J^k}{k!}
=\frac{\|A\||X|}{4}\sum_{k\ge R}\frac{(8qJ)^k}{k!}.
\tag{L10}
\]

The two exact observable evolutions each have norm `||A||`, giving the cap `2||A||` and proving (L3).

### Step 4: what survives a growing connected lattice

For fixed finite `X`, fixed spacing, a common local coefficient family and bounded `J` on each compact time interval, nested exhaustive open boxes have `R -> infinity`. At fixed `z`, the exponential-series tail tends to zero. The local observable evolutions are therefore Cauchy in operator norm, uniformly on compact time intervals. This constructs their thermodynamic-limit dynamics by compatible finite-volume embeddings. It is a limit in volume, at fixed regulator spacing.

One should not conclude that the time action is norm-continuous on **all** of `B(L^2(SU(2)))`. The onsite automorphisms generated by an unbounded operator may be only strongly continuous on vectors for some bounded observables. A norm-continuous observable subalgebra requires its own specification. This issue does not invalidate norm convergence **between volumes at a fixed time**.

## 3. Exact computable enclosures and conditional scaling

If `R+1 > z`, the ratio between successive tail terms is at most `z/(R+1)`, so

\[
F_R(z)\le \frac{z^R}{R!}\frac1{1-z/(R+1)}.
\tag{L11}
\]

For arbitrary rational `z >= 0`, sum positive rational terms through any `N >= R` with `N+2 > z`; enclose the remaining terms geometrically starting at `N+1`. This provides a strict rational upper endpoint and a lower endpoint without cancellation. The accompanying script implements this enclosure using only Python standard-library integer and rational arithmetic. Decimal columns are display approximations to those endpoints, not interval computations performed in binary floating point.

For fixed `z` the ratio test proves the boundary limit. A growing time window or spacing-dependent coupling changes the question. A sufficient, conservative simultaneous regime follows from `R! >= (R/e)^R`: if `z/R <= c < 1/e` eventually, the tail bound tends to zero exponentially, up to its finite geometric prefactor. This is only a sufficient condition on this estimate. Failure of it does not prove physical instantaneous propagation.

In the workbench's declared Hamiltonian normalization,

\[
\lambda(a)=\frac{2}{g_H^2(a)a},\qquad
J=T\lambda(a),\qquad R\sim b/a,
\qquad \frac zR\sim\frac{16qT}{g_H^2(a)b}.
\tag{L12}
\]

Here `b` is a fixed physical separation from the boundary. This conservative estimate is not uniform along a trajectory with `g_H(a) -> 0`. The ratio itself worsens even when the boundary distance in lattice links increases. Physical time calibration, operator renormalization, a sharper velocity estimate and nonperturbative scale matching remain open obligations. Choosing a coupling that keeps `z` small changes the trajectory; it cannot be passed off as the missing continuum proof.

## 4. Exceptions, rejected shortcuts and tests

1. **Disconnected or inactive barrier:** `R = infinity` gives exactly zero boundary influence. This checks the component contract; it cannot replace connected interacting lattices in a mass-gap argument.
2. **Zero coupling or time:** `J = 0` gives exactly zero. A signed-integral cancellation is insufficient: a drive with two opposite pulses can have signed integral zero while `J > 0`.
3. **Changed onsite coefficient inside the support:** at `lambda = 0`, changing `alpha` can change `tau(A)` immediately. On one physical square, `K` has eigenvalues `r(r+2)` and `x` couples the vacuum to `r=1`; the matrix element of evolved `x` is `(1/2) exp(i 3 alpha t)` up to the Heisenberg sign convention. Comparing `alpha=1` with `alpha=2` is generally nonzero although the locality formula has `J=0`. Such a comparison violates the shared-onsite premise.
4. **Nonlocal interactions or wrong incidence:** an added interaction directly joining distant supports invalidates the old `R` and `q`. The script measures actual incidence and checks both `d_s=2` and `d_s=3` boxes. Vertex distance and plaquette-link distance are not interchangeable.
5. **Unbounded observable:** `A=C_e` has no finite operator norm. This estimate cannot certify electric-energy accuracy, and finite-state norm bounds do not repair that omission.
6. **Growing support:** the factor `|X|` matters. A whole-volume observable is not a fixed local Wilson loop.
7. **Ground states:** locality controls one dynamics in common states; it neither constructs a vacuum nor proves decay of connected ground-state correlations. A free product family `sum_e epsilon_e C_e` has strictly onsite dynamics even if positive `epsilon_e` tend to zero and its infimum excitation energy is zero. In the gauge-invariant sector of a connected open lattice, choose the coefficients to tend to zero on all links of distant elementary squares. A fundamental closed flux loop on such a square has excitation energy `(3/4) sum_{e in p} epsilon_e -> 0`, while locality remains exact. This inhomogeneous family is a logical counterexample to locality implying a gap; it is not a claim that homogeneous interacting Yang–Mills is gapless.
8. **Gauge restriction:** a physical support is declared in the unreduced link algebra. Gauge fixing can turn a local link term into a nonlocal reduced-coordinate expression; counting quotient variables instead of link support can give a false radius.
9. **Long time or continuum coupling growth:** the cap may become `2`; that is an inconclusive bound, not an instability, gap closure or observed error of size `2`.

The exact diagnostics check these assumptions and conservative bounds. They do not solve the full connected-lattice time evolution and must not be described as simulated measurement of the actual boundary error.

## 5. Bidirectional dependency route and next experiment

Forward route: tensor link Hilbert space and Casimir spectral calculus → onsite support-preserving interaction picture → bounded four-link interactions → commutator recursion → overlap-chain count → Duhamel comparison → boundary-distance tail → fixed-spacing local thermodynamic dynamics.

Backward route: a local volume-independent dynamics limit needs a Cauchy estimate → distant-boundary effects must vanish → the factorial tail needs `R -> infinity` at a common bounded drive budget → a uniform incidence bound and shared local coefficient family are required → the unreduced gauge-invariant support and correct Hamiltonian define those data. The backward route asks for those premises; it does not manufacture them.

The next bounded experiment is to derive the exact operator of three connected squares and compare a central bounded Wilson observable in two and three connected blocks against a declared `R,J` bound, using separate representation and time-error certificates. That would test implementation and sharpen constants; the present analytic locality theorem already covers every finite open-box size under its assumptions. A ground-state clustering route must additionally establish appropriate ground states and spectral or correlation hypotheses. Neither step supplies the continuum target automatically.

## 6. Primary-source audit

The operator-topology issue was explicitly repaired in Nachtergaele and Sims, **On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian**, arXiv:1410.8174v1. Read selected passages in Sections 1–3, Proposition 2.1, Lemma 2.2 and Theorems 3.1–3.2, especially the interaction-picture and finite-volume comparison formulas. Its result supplies the established framework; constants (L8)–(L10) here are separately derived for four-link plaquettes. [Primary paper](https://arxiv.org/pdf/1410.8174)

Nachtergaele, Sims and Young, **Quasi-Locality Bounds for Quantum Lattice Systems. Part I**, arXiv:1810.02428v2, treats time-dependent interactions and unbounded onsite terms. Read selected passages in Sections 3.1–3.3, particularly Lemma 3.2 and Theorems 3.1, 3.3, 3.4 and 3.5; the bounded local comparison and strong-topology distinctions guided this derivation. The 106-page paper was not read cover to cover. The locally integrable scalar-drive extension above is justified directly by the finite-volume strong Dyson construction, rather than asserted as a verbatim theorem from that paper. [Primary paper](https://arxiv.org/pdf/1810.02428)
