# Contributions after ten paired research loops

Round20 completed D1,D2,E1,E2,F1,F2,G1,G2,H1,H2, in that order, with separate forward and reverse reports, exact checks, executed objections and source-bound advisor gates. Closing the inherited C2 certificate was additional work and is not counted among those ten loops. Ordinary and optimized repetitions do not increase the loop count.

The strongest advances are a literal finite-box state limit for the specified summable model, an exact shared-middle differential identity for a declared conditional diffusion, and an exact vacuum-variance identity showing where a uniform global perturbation budget leads as the spatial profile becomes flatter. These are mathematical results within their stated models. No literature-priority search or human peer review establishes them as discoveries new to science.

## What is new in this workbench

| Result | Classification | Exact scope and evidence |
|---|---|---|
| D1 finite-factor support completion and exact tails | Model-specific construction using established spectral tools | Norm-resolvent approximation in the A2 incomplete tensor product; retain the exterior reference generator. [Gate](d1-gate.json) |
| D2 energies, rank-one projectors and bounded observables | Quantitative model corollary | Zero reference trial mean and a positive absolute excited threshold justify the residual denominator. [Gate](d2-gate.json) |
| E1 aligned literal boxes | Model-specific boundary dictionary | Subtract actual reference energies; states and gaps survive that subtraction, fixed-z resolvents change. [Gate](e1-gate.json) |
| **E2 all upper-boundary phases** | **A previously missing premise is closed for this model** | Every bounded local observable has the same limiting expectation across anchored growing rectangular boxes. [Gate](e2-gate.json) |
| F1 static law versus physical clock | Identifiability obstruction and explicit auxiliary construction | The same conditional static density permits different positive energy coefficients c and different gaps. [Gate](f1-gate.json) |
| **F2 shared-middle gradient closure** | **Exact model-specific equation** | The extra trace r is a generated observable required by the derivative algebra; the conditional diffusion has a c/6 gap bound on the stated interval. [Gate](f2-gate.json) |
| G1 local dynamics | Quantitative convergence plus a proved topology exception | Fixed-time local Heisenberg convergence holds, but point-norm continuity fails on all bounded local operators. [Gate](g1-gate.json) |
| G2 limiting-state representation | Application of established GNS and spectral methods | The full-factor limiting-state GNS is the A2 representation with generator H−e and the inherited gap. [Gate](g2-gate.json) |
| H1 continuous profile | Exact model-specific coefficient ledger | B(q) and its endpoint divergence locate failure of a sufficient global norm certificate. [Gate](h1-gate.json) |
| **H2 exact variance and endpoint state** | **Exact model-specific equation and theorem within the budget family** | Actual global ground projections return to the selected-strip reference even while the perturbation operator norm remains nonzero. [Gate](h2-gate.json) |

No new universal axiom is asserted. A theorem proved under a declared action, representation and parameter range is not an axiom of underlying physics. The Fibonacci geometry remains a way to organize paired investigations; no observed physical law or golden-ratio action coefficient has been deduced.

## E2: the finite-box state limit

Let delta=alpha/8, s_M the retained omitted weight, t_M=107/135−s_M, epsilon_M=alpha|tau|t_M and g_M=delta−alpha|tau|s_M. Complete the reference factors touched by both a bounded local observable A and the retained interactions. For every sufficiently large anchored rectangular box, the central truncated Hamiltonian is then identical to the infinite one. Actual remote clipped components keep the inherited A1 gap. Two residual comparisons give

\[
|\omega_{\rm box}(A)-\omega_\infty(A)|
\le4\|A\|\min(1,\epsilon_M/g_M).
\]

Taking M large and then the outer box large proves the local-state limit for every upper-boundary phase. This closes the earlier finite-box **state** question for the fixed-spacing, fixed-coefficient, summable strip model. It does not claim global convergence of arbitrary moving boundary vectors. D1/D2 provide stronger operator/projector convergence for the explicitly completed factor approximants, and E1 for the aligned shifted literal boxes.

## F2: a shared variable generates an additional observable

This is the conditional link space SU(2)^3 with exterior links fixed. It is not proved equivalent to a gauge fixing of the original full graph; see the [scope clarification](f-conditional-space-clarification.md). Write x=Tr(U)/2, y=Tr(V)/2, z=Tr(W)/2, w=Tr(UV†)/2, t=Tr(VW†)/2 and S=3x+y+z+w+t. The shared V derivative generates r=Tr(UW†)/2:

\[
\Gamma(S)=\frac{15+8y+2x+2z+2r-(3x+w)^2-(y+w+t)^2-(z+t)^2}{4}.
\]

With the fundamental Casimir normalization3/4, the ground-state transform of the declared reversible diffusion is

\[
\widetilde H=c\left[-\Delta+\frac\kappa2\Delta S
+\frac{\kappa^2}{4}\Gamma(S)\right].
\]

The exact action range is [−5,7]. Weighted Poincare comparison then gives gap>=3c exp(−12|kappa|)/4>=c/6 for |kappa|<=1/8. The proof uses established reversible-generator and Dirichlet-form methods, checked against [Ledoux, section1.1](https://www.numdam.org/item/AFST_2000_6_9_2_305_0.pdf); the workbench contribution is the explicit shared-link identity, extrema and scoped bound.

The independent coefficient c has units of energy and is not alpha by definition. A dynamical correlation slope could calibrate it through c=−hbar C_f'(0)/q_kappa[f], when q_kappa[f]>0 and the measured dynamics belongs to this generator family. No measured physical slope or original-Hamiltonian matching is supplied. r is a derived observable, not a new interaction inserted into S.

## H2: exact variance separates state convergence from operator norm

Change only omitted coefficients to w_f(q)=q^(x+y+z)/24 with0<q<1. Keep alpha/E_star, spacing and all selected-strip coefficients fixed. H1 gives

\[
B(q)=\frac{2+5q+5q^2+6q^3+3q^4}
{24(1-q)^3(1+q)^2(1+q^2)},\qquad
(1-q)^3B(q)\longrightarrow\frac7{64}.
\]

Fix0<eta<1 and require |tau(q)|B(q)<=eta/8. The canonical ray is tau(q)=eta/[8B(q)]. Thus tau=O((1−q)^3), so every fixed omitted coupling vanishes in the endpoint.

Every omitted elementary face has two free Haar links. Distinct elementary faces share at most one link, so one free link can be integrated out to make their vacuum cross moment zero. Each diagonal second moment is1/4. This is pairwise orthogonality in the reference state, not independence of higher moments or of shared factors. It yields

\[
\boxed{\sigma_q^2=\|V_q\Omega\|^2
=\frac{\alpha^2\tau(q)^2}{96}B(q^2).}
\]

The actual excited spectral threshold is g_bar=alpha(1−eta)/8. The excited-space inverse and a separate reference-vacuum Schur complement give

\[
\|P_q-P_{\rm ref}\|\le\min(1,\sigma_q/g_{\rm bar}),
\qquad -\sigma_q^2/g_{\rm bar}\le e_q\le0.
\]

On the canonical ray, sigma_q²/[alpha²eta²(1−q)^3] tends to1/5376. The projector error therefore has an O((1−q)^(3/2)) upper bound; the energy error has an O((1−q)^3) bound. The selected-strip reference still contains its selected interactions.

At the same time finite-factor localization near identity proves ||V_q||=alpha eta/8. A constant perturbation norm coexists with actual global ground-state convergence. The variance identity was proposed by the separate auditor and independently reconstructed in both directions; its common proposal origin is explicit in the [team record](../methods/team-and-protocol.md).

## What remains established from earlier rounds

The work does not reset earlier successes. Round13 already matched a qualitative fixed-spacing homogeneous lattice stability result to sufficiently small local plaquette interactions, including permitted infinite-dimensional sites, appropriate boundary conventions and a scoped physical restriction. Its constants were existential, so it did not certify a numerical coupling interval. The relevant checked source is [Yarotsky, definitions and Theorems1–3](https://arxiv.org/pdf/math-ph/0411042), with the repository's application in [Round13](../../round13/advisor/weak-coupling-stability.md).

H2 obstructs the **global absolute-sum perturbation-budget route** to nonzero homogeneous omitted couplings. It does not disprove that local stability result, forbid unbounded onsite Hilbert spaces, or show that homogeneous lattice Yang–Mills is ungapped. The next quantitative task is to audit a suitable selected-strip blocking and extract applicable explicit local constants, not to claim that no homogeneous theorem exists.

## Scope of review and the remaining final target

Resolvent, bounded-perturbation, min-max and eigenspace methods are established tools; targeted primary-source checks used [Teschl, chapters4–6](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf). The exact supports, coefficient ledgers, exceptions and model equations are the workbench's applications. A separate AI-agent audit adds source-independent polynomial identities and geometry checks; it is not human peer review, full formal verification or an exhaustive priority search. See its [report](../external-audit/report.md).

The required nontrivial four-dimensional continuum theory and physical mass gap remain beyond these fixed-spacing and conditional results. That target includes the field-theory requirements stated by [Jaffe and Witten](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf). The [post-ten roadmap](post-ten-roadmap.md) identifies the next specific missing premises without treating a newly introduced symbol as their proof.
