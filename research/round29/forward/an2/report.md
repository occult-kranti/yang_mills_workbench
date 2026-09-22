# AN2 forward: HNM ordered bulk-state identification

Human project author: **Hruday N M (BUNZEEY)**. Independent forward execution under the frozen AN2 contract. Current reverse and skeptic results were not read. This is a source-theorem application and project boundary dictionary, with scientific priority unverified.

**Result:** under the inherited `|tau|<tau_*` and additional `7|tau|<=c_HTW(1,1)`, deep-bulk translates of the actual I1 orthant state converge locally in state norm to the compatible normal state obtained from centered whole-star boxes. This identifies these specified local-state routes. It is not a generator, dynamics or continuum identification.

## 1. Independent outer cutoffs

Fix a nonempty finite complete-factor region F in `[-r,r]^3` and n>=r+2. Let `b_n=n(1,1,1)`, and compare the translated orthant cutoff

`O_(n,L)=[-n,L-n]^3`, for every integer L>=2n,

with the centered cutoff `C_M=[-M,M]^3`, for every integer M>=n. Both contain the same inner cube `A_n=[-n,n]^3`. Extend each finite normal ground state by the onsite vacuum product to their common finite union (or a containing rectangle). These are grounds of their respective actual Hamiltonians plus decoupled exterior onsite terms.

Use exactly AN1's canonical reference on A_n, retaining star anchors `[-n+1,n-1]^3`, with twice-eroded bulk `D_n=[-n+2,n-2]^3`. Every difference term between either extended Hamiltonian and this canonical Hamiltonian is supported outside D_n. For an excluded anchor, some coordinate is <=-n or >=n; its star cannot reach D_n. Exterior onsite terms are disjoint too. The tensor-domain proof of AN1 therefore gives equality of bounded local commutators and the source ground-in-the-common-bulk condition for **every** allowed L,M.

HTW Theorem7 now gives

\[
\|\rho_{O_{n,L},F}-\rho_{C_M,F}\|_1
\le \varepsilon_n(F):=
\min\{2,\exp(C_1|F|-C_2(n-r-1))\}.
\tag{HNM-AN2.1}
\]

Indeed the exact distance from F to the complement of D_n is at least n-r-1. The norm is the trace norm, equal to the supremum over norm-one bounded operators on this same F. The constants do not depend on L,M,n or local Hilbert dimensions. The added smallness and positive source constants are unevaluated; AM2 did not supply them.

## 2. Centered marginals are Cauchy, not just a chosen subsequence

For any M,M'>=n, repeat the same common-bulk argument directly for C_M and C_M'. It gives

`||rho_(C_M,F)-rho_(C_M',F)||_1 <= epsilon_n(F)`.

For fixed F, epsilon_n tends to zero because C2>0. This is the Cauchy criterion for **all sufficiently large pairs**, rather than convergence along a diagonal. Completeness of the trace-class space gives a positive trace-one limit rho_F. Positivity and trace are preserved by trace-norm convergence.

For F subset F', finite marginals satisfy `Tr_(F'\F) rho_(C_M,F')=rho_(C_M,F)`. Partial trace is trace-norm contractive on trace-class operators, so the limits have the same compatibility. Define `omega_Z(A)=Tr(rho_F A)` for a bounded observable in F. Compatibility makes this independent of its chosen containing factor. It is positive, normalized and bounded by the operator norm on the local algebra; it uniquely extends to its norm closure. Each local restriction is normal by construction. One marginal alone would not define this state; the compatibility step is essential.

## 3. Ordered identification with the actual inherited orthant state

For **fixed n** and any fixed M>=n, take L to infinity in (HNM-AN2.1). Before translation this is the inherited I1 orthant exhaustion `[0,L]^3`, tested on the fixed observable translated into `F+b_n`. I1's local-state convergence applies because n is fixed during this passage. Coarse homogeneity identifies the translated finite state exactly; all endpoint gauge actions move with the original links. The result is, for every bounded A in F,

`|omega_+(T_(b_n) A)-rho_(C_M,F)(A)| <= epsilon_n(F)||A||`.

Now take M to infinity using Section2. Finally let n tend to infinity:

\[
\sup_{\|A\|\le1,\ A\in B(\mathcal H_F)}
|\omega_+(T_{b_n}A)-\omega_Z(A)|
\le\varepsilon_n(F)\longrightarrow0.
\tag{HNM-AN2.2}
\]

The order is L->infinity at fixed n, then the independent centered limit, then n->infinity. Uniformity in the outer cutoffs supplies this result; bare pointwise thermodynamic convergence on fixed observables would not justify a growing translation. The rate is a symbolic enclosure rather than a numerically evaluated convergence rate.

## 4. Gauge and coarse translations

Every finite ground is fixed by all its original endpoint gauge actions. On a bounded local factor those actions are the original left/right link actions, including outgoing heads outside the tail set, and preserve that factor. Local trace-norm convergence passes gauge invariance to omega_Z. No gauge-factor tensor decomposition or Wilson-only observable completion is substituted.

For a fixed coarse vector k, homogeneity gives

`rho_(C_M)(T_k A)=rho_(C_M-k)(A)`.

When M>=n+||k||_infinity, both C_M and C_M-k contain A_n. Applying the same common-bulk comparison and then passing M->infinity bounds `|omega_Z(T_k A)-omega_Z(A)|` by epsilon_n(F). Let n->infinity to obtain equality. Thus omega_Z is coarse-translation invariant. This needs the same selected triple at every cell, not merely arbitrary coefficients inside common ranges. The fine-coordinate translation associated with coarse k is `(4k_x,2k_y,k_z)`.

The result does not assert that a fixed-origin orthant observable already has its bulk expectation. Near-boundary translates whose distance from the missing coordinate half-spaces stays bounded are outside the proved vanishing-distance hypothesis. Nor does local-state equality by itself identify closed generators or their domains, all possible boundary limits, physical energy calibration, or a four-dimensional field theory.

## 5. Exact controls

The checker varies L and M independently, reconstructs all retained stars and the common interior, and verifies the n-r-1 distance and containment. It checks a translated centered box as required in the invariance proof. An abstract triangular array `a_(n,L)=1_{L>=n²}` has `lim_n a_(n,2n)=0` but `lim_n lim_L a_(n,L)=1`; all its diagonal points satisfy L>=2n. This discriminates the illegal diagonal substitution. The control is not an actual ground-state example.

An exact two-bit density fixture verifies marginal compatibility and rejects an inconsistent proposed singleton marginal. Near-boundary support has zero source-bulk distance; altered selected coefficients and absent HTW smallness fail the declared dictionary. These are geometric/logical controls, not computed SU(2) expectation values. The prior source-domain proof remains required for the actual states.

Reproduce: `python -B research/round29/forward/an2/check.py --output /absolute/new/output`.
