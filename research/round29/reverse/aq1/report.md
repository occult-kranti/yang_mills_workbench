# HNM numerical-cap thermodynamic construction — independent reverse AQ1

Project author: Hruday N M (BUNZEEY). The compactness/dynamics/GNS/Fourier strategy has direct prior overlap with Gauvin, arXiv:2503.15539v3 supplement A.10. Dynamics uses Nachtergaele–Sims arXiv:1410.8174v1, Section 3 and Theorem 4.1; NSY arXiv:1810.02428v2 provides the parallel formulation. This report's contribution is the actual SU(2) selected-strip dictionary and its numerical-cap application. It is not a new generic construction or an established priority claim. Current forward/skeptic AQ1 outputs were not read.

## Frozen numerical model and original links

Take full coarse Z³, centered boxes Lambda_N=[-N,N]³, a fixed repeated selected triple in the inherited ranges and all actual whole-star omitted groups. Only |tau|<=10^-8 is imposed; no old symbolic tau_* or HTW premise is used. Keep alpha,hbar,a,E_star>0 and delta=alpha/8. The full-Hilbert finite ground property has been admitted in AM2's reviewed strengthening; the finite physical rotor ground is also unique, positive and gauge invariant.

The factor b=(i,j,k) owns all positive-direction original links whose tails are (4i+r,2j+s,k), r=0,...,3 and s=0,1. Euclidean floor division gives unique ownership at negative coordinates too: tail(-1,-1,-1) belongs to(-1,-1,-1), with remainders(3,1). Truncation toward zero gives invalid remainders. Each factor retains ten selected-strip links and fourteen free links. Every link transforms with its two original endpoint variables; no boundary endpoint action is deleted.

## 1. Actual reference-energy compactness

Let rho_Lambda be the actual full ground density. For any fixed finite R contained in Lambda, reset its reduced state to the product of the actual onsite vacua, preserving the outside marginal. The reset is a legitimate full-Hilbert trial state, with zero onsite reference energy on R. Outside reference energy is unchanged; this follows first for bounded spectral truncations and then by monotone convergence. Both states have finite form energy because finite-volume V is bounded. Every interaction not meeting R is unchanged. Each incident anchor group changes its expectation by at most twice its norm. The variational principle therefore gives

\[
\operatorname{Tr}(\rho_{\Lambda,R}h_R)
\le2\sum_{b:(b+S)\cap R\ne\varnothing}\|\phi_b\|
\le56|R||\tau|=:C_R,\quad h_R=\sum_{b\in R}h_b. \tag{HNM-AQ1.1}
\]

There are at most four incident anchors per site, each of norm 7|tau|. This is the selected-reference energy, not an assumed pure-electric Haar bound. The two-factor Wilson region has seven incident bulk stars, yielding the sharper cap 98|tau|; the general bound remains valid.

h_R has compact resolvent: each actual finite rotor factor is elliptic on a compact group with bounded selected potential and the exact ground scalar, and finite tensor sums preserve discrete spectra with finite multiplicities. For P_L=1_[0,L](h_R),

\[
\operatorname{Tr}(\rho_{\Lambda,R}(1-P_L))\le C_R/L,
\qquad\|\rho_{\Lambda,R}-P_L\rho_{\Lambda,R}P_L\|_1
\le2\sqrt{C_R/L}. \tag{2}
\]

The latter follows by purification: if the omitted squared norm is p, the original rank-one density minus its projected density has trace norm sqrt(4p-3p²)<=2sqrt(p); partial trace contracts trace norm. The compressed densities lie in a bounded finite-dimensional set. Thus the local family is trace-norm precompact. Bounded spectral truncations also show the energy ball is closed.

Diagonal extraction over the countable collection of finite regions gives one subsequence with trace-norm convergent local densities everywhere. The limits are positive trace one and compatible, since partial trace is continuous. They define a locally normal state omega on the norm closure of the full bounded local algebras. Extend the finite states outside their boxes by product onsite states when comparing observables. Finite gauge invariance passes to omega. No whole-sequence convergence, translation invariance or identity with the old orthant state is inferred.

## 2. Place the actual interaction in the dynamics theorem

Use coarse l1 distance and F(r)=(1+r)^-4. The shell of radius n>=1 in Z³ has 4n²+2 points; therefore sum_z F(d(0,z))<=1+6sum_(n>=1)(n+1)^-2<=7. For D=d(x,y), either d(x,z)>=D/2 or d(z,y)>=D/2. In either case the corresponding F factor is at most16F(D). Splitting the sum gives

\[
\sum_z F(d(x,z))F(d(z,y))\le32\|F\|_1F(D)\le224F(D).
\]

The original declared star has diameter two, and the full site incidence norm is J<=28|tau|. Consequently the source interaction norm obeys

\[
\|\Phi\|_F=\sup_{x,y}F(d(x,y))^{-1}
\sum_{X\ni x,y}\|\Phi(X)\|\le81J.
\]

Repeated terms on a support are retained in the sum, and the numerator is zero at distances exceeding two. Onsite h_b is densely defined self-adjoint on the separable L²(SU(2)^24); no finite local Hilbert dimension is assumed. The whole-star finite restriction is exactly the source rule of retaining each declared interaction support contained in Lambda. Thus every assumption of the cited unbounded-onsite dynamics theorem is met. It yields norm convergence of each bounded local finite evolution as volume grows, uniformly on compact times, and isometric star automorphisms on the quasi-local algebra.

In physical time use onsite delta*h_b/hbar and interaction delta*phi_b/hbar, or normalized time s=delta*t/hbar. The F norm then scales by delta/hbar. No extra smallness hypothesis is needed for this existence theorem. Norm convergence as **volume** grows does not imply norm continuity as **time** varies on every B(H_R) operator.

## 3. Stationarity and GNS strong continuity

Write alpha_t(A) for the resulting physical Heisenberg automorphism. For local A, approximate it uniformly in compact time intervals by evolution inside one fixed sufficiently large finite region. Subsequential state convergence on that region is in trace norm. Finite ground-state invariance and these norm approximations give omega(alpha_t(A))=omega(A). Quasi-local norm approximation extends invariance to the full algebra.

Hence U_t pi(A)Omega=pi(alpha_t(A))Omega defines a unitary group in the GNS representation. Strong time continuity is a separate step. Fixed finite-region evolution of A is strongly and strong-star continuous, even with unbounded onsite energy. A normal local density paired with that evolution gives continuous scalar functions; approximate its trace-class density by finite-rank matrices to prove this. Compact-time norm approximation then gives continuity of omega(A*alpha_t(A)). Stationarity implies

\[
\|(U_t-I)\pi(A)\Omega\|^2
=2\omega(A^*A)-2\operatorname{Re}\omega(A^*\alpha_t(A))\to0.
\]

Local vectors are dense, and the U_t are isometries, so continuity holds throughout GNS. Stone's theorem gives U_t=exp(it H_infinity/hbar), H_infinity self-adjoint and H_infinity Omega=0. This fixes the physical energy clock; the generator in frequency units would be H_infinity/hbar.

## 4. Nonnegative energy from actual correlations

For every bounded local A, the finite correlations omega_Lambda(A*alpha_t^Lambda(A)) converge to omega(A*alpha_t(A)), uniformly on compact t. Approximate both by the same fixed-region evolution: local trace-norm convergence controls its state error uniformly in t, and the other two errors are the dynamics norm bounds. The finite functions are Fourier transforms of positive spectral measures of the actual centered K_Lambda>=0 on A Omega_Lambda.

For f smooth and compactly supported in negative physical energies, write f(E)=integral k_f(t)exp(itE/hbar)dt with integrable Fourier kernel k_f. The correlations are uniformly bounded by ||A||². Dominated convergence therefore passes this integral to the GNS spectral measure. Its finite values are zero, so every such negative-energy test has zero limiting integral. Nonnegative tests exhaust the negative half-line; hence the spectral measure on every local GNS vector has no negative support. Density makes the negative spectral projection zero, proving H_infinity>=0.

This establishes a nonnegative physical-energy GNS dynamics. Gauge-fixed sector completion and a positive physical gap are reserved for AQ2; no gap is inferred here from compactness alone.

## Controls, source reading and limits

Trace-one states |e_n><e_n| on an infinite onsite space are not trace-norm precompact (pairwise distance2); their energy escapes for h e_n=n e_n. Two individually normalized marginals may also be incompatible. Both failures explain why energy compactness and consistency are necessary. Incoming-star and negative-owner checks retain actual geometry.

For a concrete time-topology control, take h e_n=n²e_n and the unilateral shift S. At t_k=pi/(2k+1), its evolved matrix element from e_k to e_(k+1) changes sign, so ||exp(it_k h)S exp(-it_k h)-S||=2 although t_k→0. Each fixed vector has strong continuity. This distinguishes the topology used above.

Run `python research/round29/reverse/aq1/check.py --output /absolute/new-directory`. Exact controls check ownership, shells, convolution factors, all-star reset budgets, cutoff inequalities and clock/topology distinctions. The source packet lists PDF hashes and reading scopes; NS Section3/Theorem4.1 and Gauvin A.10 were inspected directly. Normal/optimized outputs agree and owned input/report/code/result bytes are frozen. Existence of a subsequential locally normal state is the conclusion; uniqueness of all ground states, old-state identity, continuum construction and all-boundary equivalence remain unproved.
