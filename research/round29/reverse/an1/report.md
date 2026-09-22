# HNM common-bulk comparison — independent reverse AN1

Project author: Hruday N M (BUNZEEY). This is an application of Henheik–Teufel–Wessel (HTW), arXiv:2106.13780v3, Theorem 7, attributed there to Yarotsky (2005). HNM labels this workbench's geometry and dictionary; scientific priority is unverified. No current forward/skeptic AN1 outputs were read.

## Model and source hypotheses

Fix one coarse-translation-invariant selected coefficient triple within I1's endpoint/bridge ranges. Every coarse site retains its 24 original SU(2) links and actual onsite ground, with h_x>=Q_x after normalization by alpha/8. The original omitted anchor group has norm 7|tau| and support S={0,ex,ey,ez}, contained in the l1 ball of radius R=1. The diameter two does not make its radius zero or two. All original endpoint gauge actions remain. Require the new source premise 7|tau|<=c_HTW(1,1), with positive unevaluated c_HTW. If the inherited orthant state is subsequently invoked, also require |tau|<tau_*; AM2 evaluates neither threshold.

HTW allows infinite-dimensional onsite spaces and unbounded onsite operators with unique gapped ground states. Its bounded-commutator condition includes domain preservation. Two normal states that are ground states in the common twice-eroded bulk satisfy its exponentially decaying local comparison. We use Definitions 1,2,6, Theorem 7 and Lemma 8, including the latter's domain argument. This source theorem, not sample state agreement, supplies the uniform bounded-algebra estimate.

## Common Hilbert space and explicit boundary mismatch

After the frozen translation by -n(1,1,1), the orthant restriction is B_n=[-n,n]^3 in coarse coordinates; the centered restriction is Gamma_n=[-2n,2n]^3. Use n>=3 and Y={0,ez}. The selected coefficient triple is repeated identically, so the translation identifies the actual local link/gauge/energy data. It is not valid if the translated coefficients vary with n.

Embed both states in H_(Gamma_n). Extend the B_n actual ground density by the product of onsite vacuum densities on Gamma_n\B_n. This is a normal ground state of H_(B_n)+sum_(outside B_n)h_x. The other density is the actual Gamma_n ground. These finite ground states exist by compact resolvent and bounded perturbation; positivity makes them gauge invariant, and the comparison will hold on the full local algebra before its gauge-invariant restriction.

Let the common source Hamiltonian on B_n contain all onsite h_x and only anchor groups at

\[
D_n=\{x\in B_n:\operatorname{dist}(x,\mathbb Z^3\setminus B_n)>1\}
=[-n+1,n-1]^3.
\]

This is HTW's canonical anchor restriction. In contrast, the actual whole-star B_n Hamiltonian retains anchors [-n,n-1]^3. Their difference includes the negative faces of the anchor box. Therefore they are not equal finite Hamiltonians. Both extended actual Hamiltonians have the same canonical restriction, and all interaction differences lie outside

\[
B_n^\circ=\{x:\operatorname{dist}(x,\mathbb Z^3\setminus B_n)>2\}
=[-n+2,n-2]^3.
\]

To see this for every n, an anchor within distance one of the complement can reach at most one further lattice step, so its star misses the strictly twice-eroded bulk. Anchors outside B_n have the same property. The extra onsite terms are outside B_n itself. This proves the support separation, rather than assuming the boundary prescriptions coincide.

## Domain and ground-condition transfer

Take A supported in B_n^circ from HTW's bounded-commutator class for H0. Such A preserves the appropriate local onsite-sum domain. Its exterior identity extension preserves the full domain of the nonnegative tensor-sum H0: local and exterior energy spectral projections commute, and the domain is the intersection of the two sum domains. Bounded interaction sums leave this domain unchanged.

The difference between either actual extended Hamiltonian and the common canonical restriction consists of bounded boundary interactions plus unbounded onsite terms on disjoint exterior factors. Those operators strongly commute with A on the product spectral core, and closure gives zero commutator on the domain. Consequently [H_i,A]=[H_*,A] is bounded with domain preservation. The actual ground inequality Tr rho_i A* [H_i,A]>=0 thus proves Tr rho_i A*[H_*,A]>=0. Both states meet the same HTW bulk ground condition. This is the content of Lemma 8 specialized to the actual boundaries; no arbitrary bounded local observable is incorrectly assumed to preserve the unbounded domain. The theorem's conclusion itself covers every bounded local observable.

## Explicit estimate on the complete local algebra

The two complete factors of Y own 48 links and 36 distinct endpoints. Since |Y|=2 and its nearest point to the upper z boundary of B_n^circ is ez,

\[
\operatorname{dist}(Y,\mathbb Z^3\setminus B_n^\circ)=n-2.
\]

Thus, writing the two extended finite states as rho_n and sigma_n,

\[
\sup_{A\in B(H_Y),\ \|A\|\le1}
|\operatorname{Tr}[(\rho_n-\sigma_n)A]|
\le \min\{2,\exp[2c_1-c_2(n-2)]\}. \tag{HNM-AN1}
\]

The positive constants c1,c2 belong to the external theorem and are not evaluated here. This bound is uniform over the norm-one bounded local algebra, so also holds for the local gauge-invariant algebra, with all endpoints retained. This loop claims only the specified finite comparison.

## Controls and scope

An observation at (n-2,0,0) has distance one from the eroded-bulk complement, so the same estimate does not decay with n. A changed bulk interaction at anchor zero changes the common Hamiltonian and invalidates this application. Each interior site has four incoming anchor stars; Y meets seven distinct anchors. Deleting incoming terms, using R=0, dropping the new HTW smallness premise or varying translated selected coefficients fails an explicit control.

Run `python research/round29/reverse/an1/check.py --output /absolute/new-directory`. Exact enumeration checks n=3,4,6 as corroboration for the all-n geometry proof, plus the 48-link/36-endpoint cover and controls. It does not simulate ground expectations or evaluate source constants. Normal/optimized results agree and source/code/output hashes are bound. A common spectral gap alone would not imply this estimate; it depends on the separately matched source theorem.
