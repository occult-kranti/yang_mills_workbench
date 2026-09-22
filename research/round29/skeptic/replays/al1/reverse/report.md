# HNM full-interaction matching audit — reverse AL1

Project author: Hruday N M (BUNZEEY). This project label identifies this audit; it does not rename Yang–Mills theory, the Kogut–Susskind Hamiltonian, or Yarotsky's theorem. Scientific priority is unverified. No current forward or skeptic AL1 output was read.

## Reverse target and complete map

To use the actual I1 result for a uniform standard SU(2) lattice theory one must match every electric link and every magnetic face, retain the physical clock and meet all theorem hypotheses. The inherited R18-B2 convention, attributed there to Bauer, D'Andrea, Freytsis and Grabowska (arXiv:2307.11829, equations 55–56), is alpha=g²/(2a) and lambda=2/(g²a), in the inherited natural units. This report uses that inherited formula, not a new source-derived Hamiltonian.

There are 24 original outgoing links and 24 plaquette anchors per complete coarse cell. Three selected xy faces comprise two endpoints and one bridge; the other 21 faces include every remaining xy, xz and yz plaquette. Therefore the uniform coefficient dictionary is necessarily lambda_L=lambda_R=mu=nu=lambda. Since I1 defines nu=alpha*tau/24, the dimensionless project bookkeeping variable is

\[
r_{\rm HNM}=\lambda/\alpha=4/g^4,\qquad
\tau_{\rm HNM}=24r_{\rm HNM}=96/g^4,\qquad
\epsilon_{\rm HNM}=21\lambda/(\alpha/8)=672/g^4.
\]

These are reparameterizations, not new fields or tunable repair terms. The exact I1 local norm is 7|tau| because all 21 normalized Wilson traces approach one simultaneously on positive Haar-measure neighborhoods of the identity. The electric part remains alpha times every original link Casimir. No Casimir is counted twice or discarded by the block partition.

I1 requires endpoint r<=1/2, bridge r<=1/8, epsilon<c1(S), and c2(S)*epsilon<1/2. On the positive uniform branch these become

\[
g^4\ge32,\qquad 672/g^4<c_1(S),\qquad
672c_2(S)/g^4<1/2.
\]

The constants remain unevaluated. The bridge requirement implies the endpoint requirement. This is a complete membership test in the *inherited sufficient domain*; it is not a necessary condition for a spectral gap.

## Ground shift, boundary and clock

The standard magnetic expression is lambda sum_p(1-W_p), so its raw additive scalar is lambda times the number of retained faces. Adding this scalar shifts the true ground energy by the same amount and cancels from H-E0. It is not itself E0. I1 additionally subtracts each selected strip's true reference ground energy when defining onsite h_b. Reconstructing the raw I1 Hamiltonian therefore requires adding those reference scalars. For G centered by its own actual ground energy, the corresponding centered physical operator is K=(alpha/8)G. Physical evolution is exp[-it(alpha/8)G/hbar], hence the dimensionless time is u=alpha*t/(8hbar). Substituting t/hbar for u changes the clock.

The dictionary is exact for the bulk interaction assignment. It does not identify two different finite-boundary prescriptions. I1 retains an omitted anchor group only if its entire four-site star S={0,ex,ey,ez} is inside B. In B={0,ex}, the omitted xy face with base (3,0,0) has all its actual coarse support {0,ex} inside B and is retained by an actual-contained plaquette rule; the whole-star rule deletes it. Thus raw finite Hamiltonians under these two rules are different even after scalar shifts. To obtain equality one must impose the same declared whole-star rule on both. The previously inherited finite padding argument transfers a gap estimate; it does not assert equality of the raw Hamiltonians or all infinite-volume limits.

For interior star incidence there are four anchors whose declared stars contain a given site: its own and its three predecessor anchors. A local budget using only the site's own anchor deletes incoming terms. The checker distinguishes that error.

## All-path result

For the prospectively frozen a_n=a0/n and g_n²=1/n, n a positive integer, alpha_n=1/(2a0), lambda_n=2n²/a0, r_n=4n², tau_n=96n² and epsilon_n=672n². Since n>=1, r_n>=4>1/8. Every member fails the selected-bridge sufficient hypothesis, irrespective of c1,c2. This is an analytic argument for the entire path; exact sample computations are controls, not its proof. The fixed alpha_n/E_star is strictly positive when a0,E_star>0, so a vanishing energy reference is not the obstruction here. A positive global energy rescaling preserves lambda/alpha and cannot repair membership.

The old R18-B2 box required g^4>=32/3 for an eleven-face finite graph. That inequality is inherited and is not claimed as a new discovery. This audit adds the full I1 class dictionary, its stronger bridge restriction g^4>=32, both symbolic local inequalities, and an explicit finite-boundary mismatch. Neither certificate failure proves an absent Yang–Mills gap. This path is one declared weak-coupling candidate, not an independently derived renormalization trajectory.

## Executed evidence and limits

Run `python research/round29/reverse/al1/check.py`. Exact rational checks enumerate all original face classes, actual supports, the boundary witness and coefficient/clock controls. Outputs and immutable source snapshots are SHA-256 bound in output/manifest.json. Source reading depth: I1 reverse report and source dictionary, R18-B2 displayed matching section, frozen contract and roadmap; the external spectral theorem is inherited. No infinite-dimensional spectral simulation or continuum construction is performed. Numerical source constants, field reconstruction and a continuum physical mass remain unresolved.
