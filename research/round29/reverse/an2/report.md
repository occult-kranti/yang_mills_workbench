# HNM ordered bulk-state identification — independent reverse AN2

Project author: Hruday N M (BUNZEEY). This extends the model dictionary for the existing HTW/Yarotsky local comparison theorem. It is not a new theorem of universal boundary independence or a scientific-priority claim. Current forward/skeptic AN2 outputs were not read.

## Fixed hypotheses and independent outer cutoffs

Retain AN1's actual untruncated 24-link factors, one fixed repeated selected coefficient triple, homogeneous omitted tau, all endpoint gauge actions and fixed positive scales. The two independent smallness requirements are |tau|<tau_* for the inherited orthant state and 7|tau|<=c_HTW(1,1) for the comparison theorem. Their constants remain unevaluated. AM2's numerical finite-volume gap is not substituted for either condition.

Let F be any fixed finite nonempty complete-factor region contained in [-r,r]^3. Take n>=r+2. Translate the orthant cutoff [0,L]^3 by -b_n, b_n=n(1,1,1), with **every L>=2n**, and independently take centered cutoff [-M,M]^3 with **every M>=n**. Both contain B_n=[-n,n]^3. Embed their normal ground densities by product onsite vacua into a common finite cube of radius K=max(L-n,M,n+1); the extra one-site collar ensures the canonical anchor restriction is the same even when L=2n and M=n.

AN1's domain proof applies unchanged: the two actual whole-star Hamiltonians have identical bounded commutators on B_n^circ=[-n+2,n-2]^3, since every difference is outside that region. Both extended densities are common-bulk ground states. For all such L,M,

\[
\sup_{\|A\|\le1,\ A\in B(H_F)}
|\omega_{L,+}(T_{b_n}A)-\omega_{M,0}(A)|
\le \varepsilon_{n,F}:=\min\{2,e^{C_1|F|-C_2(n-r-1)}\}. \tag{HNM-AN2.1}
\]

The distance lower bound follows coordinatewise: the complement of B_n^circ begins at coordinate magnitude n-1, while every coordinate in F has magnitude at most r. Hence the distance is at least n-r-1. The constants are independent of the two outer cutoffs. This independence is the new ingredient needed for ordered limits.

## Centered Cauchy property and a genuine local state

Apply the same argument to any pair of centered boxes with M,M'>=n. Their F marginal densities satisfy ||rho_(M,F)-rho_(M',F)||_1<=epsilon_(n,F), by trace-class/bounded-operator duality. For fixed F the right side tends to zero as n→infinity. This is a Cauchy estimate for all sufficiently large pairs, not a statement along one paired diagonal.

Trace class is complete, so rho_(M,F) converges in trace norm to rho_F. Positivity and trace one survive because the positive cone is closed and trace is continuous in this norm. If F is contained in G, finite marginals satisfy rho_(M,F)=Tr_(G\F)rho_(M,G). Partial trace is contractive in trace norm; passing to the limit gives rho_F=Tr_(G\F)rho_G. For arbitrary regions use their finite union. Thus the positive trace-one normal marginal family is compatible and defines a bounded positive normalized functional on the union of finite local algebras. It extends uniquely by norm continuity to their norm closure. Denote this locally normal state omega_bulk.

This argument constructs compatible limits on every finite complete-factor algebra; convergence of only one chosen marginal would not suffice.

## Ordered identification with the actual orthant state

For each fixed n and fixed local A, first take L→infinity in (HNM-AN2.1). The inherited I1 local convergence gives the **actual** orthant state omega_+(T_(b_n)A). The bound is independent of L, so it survives. Next take M→infinity using the centered trace-norm convergence just proved. We obtain

\[
\sup_{\|A\|\le1,\ A\in B(H_F)}
|\omega_+(T_{b_n}A)-\omega_{\rm bulk}(A)|
\le\varepsilon_{n,F}\longrightarrow0. \tag{HNM-AN2.2}
\]

Passing each inequality for arbitrary A and then taking the supremum is valid; no uniform-in-L strengthening of the inherited orthant limit is silently assumed. Only after this fixed-n outer-limit passage do we let n→infinity. The result identifies the deep-bulk translates of that orthant state with the centered local state. It does not identify an observable kept at the orthant boundary with the bulk.

## Symmetries and exact scope

Every sufficiently large original finite ground state is invariant under all original endpoint gauge transformations. On any fixed local A these transformations act within a finite set of owned links, including every endpoint action; finite-volume invariance passes to the local limit. Thus omega_bulk is gauge invariant.

For a fixed coarse translation z, compare centered boxes and their translates. The fixed repeated coefficient triple makes their local Hamiltonians translates of the same interaction. Once M>=n+||z||_infinity, both contain the same B_n, so the same estimate applies to A and its translated finite-box expectation. Taking the outer limits and then n→infinity gives omega_bulk(T_z A)=omega_bulk(A). This proves coarse translation invariance. It makes no claim of invariance under a finer translation that changes the selected-strip assignment.

Equality here is equality of local states along the two specified routes. It does not itself identify representations of time evolution, domains of generators, spectral gaps, all other boundary limits, or a continuum field theory. The new symbolic HTW premise remains attached to this result.

## Logical controls and execution

For n>=2 and L>=2n, the triangular array a_(n,L)=1 if L<=n² and zero otherwise has a_(n,2n)=1 for every n, but lim_(L→infinity)a_(n,L)=0 for every fixed n. Thus diagonal agreement can give the wrong iterated limit. This is a logical control, not a physical counterexample.

A moving observation at (n-2,0,0) has fixed distance one from the eroded-bulk complement, so the estimate supplies no decaying error. Distinct repeated selected triples define different bulk problems even if both satisfy the coefficient ranges. Removing HTW smallness removes the comparison hypothesis. Individually positive trace-one marginals can be incompatible: |0><0| on one factor and |11><11| on two factors have inconsistent reductions.

Run `python research/round29/reverse/an2/check.py --output /absolute/new-directory`. Exact geometry checks include minimal L=2n and M=n with the explicit ambient collar, larger independent outer cutoffs, the triangular array, and marginal compatibility control. Normal and optimized outputs agree and all input, source, report and execution bytes are bound in the manifest and freeze. The analytic completeness/ordering argument, not the finite checks, proves the limiting statement.
