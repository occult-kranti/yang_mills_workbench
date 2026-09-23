# AV1 independent derivation before producer comparison

**Standing.** I wrote this after the AV1 contract froze (`frozen_at` 2026-09-23T21:23:47Z) and before opening, listing or reading `research/round32/forward/av1/` or `research/round32/reverse/av1/`. I worked from the frozen contract, the shared premises it names (AM2 forward and reverse reports and checker, AT4 forward, I1 forward, `selection-av1.md`) and my own earlier triage and loop notes. I am a model-agent skeptic with correlated ancestry: I share the model family of the advisor, the lenses and the producers, and my triage seeded the contract's mechanism. This note is therefore not human peer review and not an independent discovery. Exact values come from `av1_check.py`; every decimal is a preview. Human project author: Hruday N M (BUNZEEY).

**Route chosen: purification and contractivity.** This is a third route, used by neither producer contract. It needs neither the explicit reduced density (the forward route) nor the mixture inequality AT4 F08 (the reverse route), only the exact overlap identity <psi,psi_out> = ||psi_out||^2 and the contractivity of the partial trace. It reproduces the reverse constant 2e/sqrt(1+e^2). The forward formula is evaluated as a comparator.

## 1. Model and AM2 objects
- **Model.** Take coarse boxes Lambda_N=[-N,N]^3 with V=sum_{b+S subset Lambda_N} phi_b and phi_b=-(tau/3) sum_{f in O_b} W_f (I1.5, delta=alpha/8). At the zero triple, h_b=8 sum_e C_e, with Haar vacuum Omega_b and h_b >= 6Q_b >= Q_b. These are I1.6 empty-boundary volumes with |X|<=4 and h>=Q, which are AM2's hypotheses.
- **AQ1 uses the same family.** AQ1 uses the same Lambda_N, the same whole stars and the same onsite operators, so AM2 applies to every AQ1 box at both signs.
- **Per-site sum.** J=max_u sum_{X ni u}||V_X|| <= |S| * 21 * |tau|/3 = 28|tau|, with fewer stars at the boundary.
- **Cutoff and fixed point.** In each product cutoff Q_n = (x) Q_{x,n} (onsite spectral projections that contain Omega_x), AM2 gives the unique fixed point c with ||c||_a <= R=1/64. The creators c^_I=|c_I><Omega_I| (x) 1 commute and are nilpotent, and c^_I c^_J=0 when I and J meet. Hence psi = e^{-C}Omega_0 = prod_I(1-c^_I)Omega_0, with vacuum coefficient 1 and a gap of at least 1/2.
- **Constants.** e^{1/8} < 8/7 is certified by a Taylor series with a geometric tail. G(R)=16e^{1/8}(74/64) < 148/7 and G'(R)=308e^{1/8} < 352. J_0=7/25000000, J_0G(R)=37/6250000 < 1/64 and 2J_0G'(R) < 77/390625 < 1.

## 2. The split, the straddling supports and the two-creation term
Order the product so that the creations meeting R={0,e_z} act last. Put psi_out := prod_{I cap R empty}(1-c^_I)Omega_0 = Omega_R (x) phi_out. In prod_{I meets R}(1-c^_I), only products of pairwise-disjoint supports survive, and each such support meets the two-site R. A surviving product therefore has at most two factors: I containing 0 and not e_z, and J containing e_z and not 0. So

  delta := psi - psi_out = - sum_{I meets R} c^_I psi_out + sum_{I ni 0, J ni e_z, I cap J empty} c^_I c^_J psi_out.

**Straddling supports.** For a straddling I (one meeting both R and R^c), c^_I psi_out = c_I (x) (<Omega_{I\R}| (x) 1)phi_out. The vacuum bra contracts phi_out on I\R, so the result is **not** c_I (x) phi_out. Its norm is at most ||c_I|| ||psi_out||, because ||c^_I||=||c_I||. The two-creation term is at most (sum_{I ni 0}||c_I||)(sum_{J ni e_z}||c_J||)||psi_out||.

**Orthogonality.** Every c_I lies in (x)_{x in I} Q_x H_x and I meets R, so every term of delta is excited on R. Hence (P_R (x) 1)delta=0, (P_R (x) 1)psi=psi_out and <delta,psi_out>=0.

**Size of delta.** Put t := max_{u in R} sum_{I ni u}||c_I|| <= ||c||_a. Since sum_{I meets R} <= sum_{u in R} sum_{I ni u} <= 2t,

  e := ||delta||/||psi_out|| <= eps := 2t + t^2.

## 3. The normalization trap (derived here, checked on a fixture)
**The trap.** <psi,psi> = ||psi_out||^2(1+e^2), and ||psi_out||^2 = ||phi_out||^2 >= 1 grows with |Lambda_N|, because each outside creation adds orthogonal excited mass. The following shortcuts are all volume-dependent: keeping the outside creations in <psi,A psi> and dividing by 1+O(tau^2); deleting ||delta||^2 from Z; or evaluating the numerator with only the creations that meet R. The cancellation is exact only because psi_out is the product Omega_R (x) phi_out and delta is contracted against that same phi_out. Discarding the outside creations altogether is also wrong, because the straddling supports see them.

**Model-class counterexample (fixture A).** The fixture has R={0,1}, one outside site {2}, and creations on {0}, {1}, {0,1}, {0,2}, {1,2} and {2} with exact rational amplitudes, plus 0 to 3 padding sites (amplitude 1/3 each).
- ρ_R is identical for every padding count.
- The unnormalized <psi,P_R psi> grows by exactly 10/9 per padding site.
- The naive numerator-only and R-only values vary with the padding.
- The split with the two-creation term reproduces psi exactly, and dropping the pair term breaks it.
- Dropping |Omega><xi|, its adjoint, Tr_out|delta><delta| or ||delta||^2 from Z each changes ρ_R.
- The straddling creation enters xi only when the outside site is excited: with g=0, xi does not depend on s. So it enters at order s*g, and it enters the density block at order s^2.
- The overlap of the two terms c^_0 psi_out and c^_{02} psi_out is nonzero, so a root-sum-square epsilon undercounts, and the terms must be added linearly.

Fixture B (R={0} with two outside sites) checks the exact 2x2 trace norm against both route bounds.

## 4. Bound by purification
Put psi^ = psi/||psi|| and psi^_out = psi_out/||psi_out||. Then Tr_out|psi^_out><psi^_out| = P_R exactly, and Tr_out|psi^><psi^| = rho_{N,R}. The partial trace is trace-norm contractive, and || |u><u|-|v><v| ||_1 = 2 sqrt(1-|<u,v>|^2) for unit vectors. Since <psi^,psi^_out> = ||psi_out||/||psi|| = (1+e^2)^{-1/2},

  ||rho_{N,R} - P_R||_1 <= 2e/sqrt(1+e^2) <= 2eps/sqrt(1+eps^2) <= 2eps, uniformly in N (and in the cutoff n).

This also gives Tr(rho P_R) = 1/(1+e^2), which is the reverse identity.

**Forward comparator.** rho = [||psi_out||^2 P_R + |Omega_R><xi| + |xi><Omega_R| + Tr_out|delta><delta|] / (||psi_out||^2(1+e^2)), with xi=(1 (x) <phi_out|)delta orthogonal to Omega_R and ||xi|| <= ||psi_out|| ||delta||. This gives 2e(1+e)/(1+e^2), which is increasing on [0,1+sqrt2] and at least as large as the purification bound when eps <= 1.

**Why the square root disappears.** The infidelity e^2/(1+e^2) is quadratic in the vector perturbation. AT4 instead bounded the infidelity by the reset energy, which is linear in tau.

## 5. Face counts derived from the I1 table (translation covariance)
**The 21 omitted classes.** The checker parses the printed I1 §3 table and re-derives it from I1.1 and I1.4. The classes are:

| Class support | Count |
|---|---:|
| {0,e_y} | 3 |
| {0,e_x} | 1 |
| {0,e_x,e_y} | 1 |
| {0,e_z} | 10 (6 xz + 4 yz) |
| {0,e_x,e_z} | 2 |
| {0,e_y,e_z} | 4 |

Every class contains its anchor 0 and at least one other site.

- **Faces per factor.** Site u lies in the owner set M(f) of class k anchored at b if and only if u-b is in S_k. The count is therefore sum_k |S_k| = 6+2+3+20+6+12 = **49**.
- **Owner sets through u.** These are the sets u+(S_k-o) with o in S_k:
  - {0,e_y}: 3 and {0,-e_y}: 3;
  - {0,+-e_x}: 1 each;
  - the three xy-triple translates: 1 each;
  - {0,+-e_z}: 10 each;
  - the three xz-triple translates: 2 each;
  - the three yz-triple translates: 4 each.

  That makes **15** sets with multiplicities {1^5, 2^3, 3^2, 4^3, 10^2}, which sum to 49.
- **Faces meeting R.** 49+49-16 = **82**. The 16 faces whose owner set contains R are {0,e_z} (10), {0,e_x,e_z} (2) and {0,e_y,e_z} (4). **10** faces lie inside R: an owner set inside R needs b in R and S_k=R-b, which leaves only {0,e_z} at b=0 (6 xz + 4 yz). The Wilson face is one of these 10. The remaining **72** faces are straddling.
- **All-site brute force.** On Lambda_1, Lambda_2 and Lambda_3 (168, 1344 and 4536 faces), the per-site maximum is 49, attained in the bulk. Every site's owner-set multiplicities are dominated by the bulk ones, so boundary counts are at most bulk counts. Faces meeting R number 82 for N>=2, and 49 at N=1, where incident stars are missing. Distinct faces share at most one link.
- **Anchors and cover.** R-S has 7 anchors, whereas an orthant count finds 2 anchors and 42 faces. The cover has 48 links and 36 endpoints.
- **Bounds only.** 84=4*21 and 168 are labelled bounds only.

## 6. First-order vector, remainder and the two tiers
**Haar facts.** The spin-0 multiplicities in (1/2)^{(x)k} give E[W]=0, E[W^2]=1/4, E[W^3]=0 and E[W^4]=1/8. Each W_f Omega_0 carries j=1/2 on four distinct links, so it has h-energy 8*4*(3/4)=**24** (3 in alpha units). It lies in the sector P_{M(f)} and has norm 1/2. Two different faces give orthogonal vectors, because a link of f that is not in g carries a lone j=1/2 matrix element with Haar mean 0. Also <Omega_0,V Omega_0>=0.

**First-order vector.** c^(1)_I = H_I^{-1}P_I V Omega_0 = -(tau/72) sum_{M(f)=I} W_f Omega_0, so ||c^(1)_I|| = sqrt(n_I)|tau|/144. The amplitude is the same in both unit systems: (tau/3)/24 = (tau/24)/3. The mixed forms (tau/3)/3 and (tau/24)/24 are eightfold errors. This gives

  t_1 = ||c^(1)||_a = (11+3sqrt2+2sqrt3+2sqrt10)|tau|/144 ~ 0.173828|tau| <= 49|tau|/144 (triangle bound).

**Remainder.** c-c^(1) = sum_{k=1..8} L_k(c,...)/k!, whose anchored norm is at most J(G(t)-16). Since G is convex and t <= R (the AM2 ball), J(G(t)-16) <= J t G'(t) <= 352 J t. Hence t <= t_1 + 352Jt, that is, **t <= t_1/(1-352J)**. The remainder is charged and is never zero. In the cutoff space the first-order vector is Q_n c^(1), because Q_n commutes with H_0, so the bound is uniform in the cutoff.

**Exact constants at tau = +10^-8 and -10^-8.** They are identical, because only |tau| enters; the checker runs both signs. In the table, D_fwd is 2eps(1+eps)/(1+eps^2) and D_pur is 2eps/sqrt(1+eps^2), which lies in [2eps-eps^3, 2eps].

| Tier | t | eps | D_fwd | D_pur upper (2eps) |
|---|---|---|---|---|
| (i) J_0G(R) | 37/6250000 | 462501369/39062500000000 | 36133347268157653748322/1525878906463907516326874161 ~ 2.368035e-5 | 462501369/19531250000000 ~ 2.368007e-5 |
| (i) iterated (labelled; 3 directed-exp steps, rounded up to 10^-20) | 224018065320441/5*10^19 ~ 4.48036e-6 | exact in results.json | ~1.792165e-5 | ~1.79215e-5 |
| (ii) triangle 49/144 | 49/14398580736 (t_1=49/14400000000, 352J_0=77/781250) | 1411060914529/207319127211110301696 | 585079838465912592144137406066050/42981220507576537932303142777593983768257 ~ 1.3612452870e-8 | 1411060914529/103659563605555150848 ~ 1.3612452778e-8 |
| (ii) grouped sqrt (labelled; rational sqrt uppers) | 6257824405648451/3599645184*10^15 ~ 1.738456e-9 | exact in results.json | ~6.953824e-9 | ~6.95382e-9 |

The tier-(ii) remainder charge is 352J_0t = 3773/11248891200000000 ~ 3.35e-13. The consequences for tier (ii) are |omega(W)| <= D ~ 1.3612e-8, |omega(W^2)-1/4| <= D/2 ~ 6.806e-9 (trace-zero effect refinement, since 0 <= W^2 <= 1) and m^2 <= D^2 ~ 1.85e-16. For tier (i) they are 2.368e-5, 1.184e-5 and 5.6e-10.

## 7. Removing the cutoff for the ground vector
**Setting.** Fix N. H=H_0+V is self-adjoint on D(H_0) with V bounded, and it has a unique ground phi with energy E (AM2 §6). Let H_n=Q_nHQ_n on Q_n H, with ground psi_n and energy E_n. The gap in each cutoff space is at least 1/2 (AM2 §4). Since Q_n H is a subspace, E_n >= E. Because phi lies in Q(H_0) and Q_n are H_0 spectral projections increasing to 1, Q_n phi -> phi in the form norm. Hence <Q_n phi, H Q_n phi> -> E and ||Q_n phi|| -> 1.

**Argument.** The cutoff gap gives <Q_n phi,H_nQ_n phi> >= E_n||Q_n phi||^2 + (1/2)(||Q_n phi||^2 - |<psi_n,phi>|^2). Therefore (1/2)(||Q_n phi||^2-|<psi_n,phi>|^2) <= <Q_n phi,HQ_n phi> - E||Q_n phi||^2 -> 0. So |<psi_n,phi>| -> 1, and the projections satisfy || |psi_n><psi_n| - |phi><phi| ||_1 = 2sqrt(1-|<psi_n,phi>|^2) -> 0. The reduced densities converge in trace norm, and the closed trace-norm ball keeps ||rho_{N,R}-P_R||_1 <= D.

**What is needed.** The uniform gap is essential. Without it, eigenvalue convergence (AM2 §6) does not move vectors: alternating diag(0,1/n) and diag(1/n,0) have energies tending to 0 and mutually orthogonal ground vectors. The checker verifies the gap inequality on a rational orthogonal 3x3 fixture.

## 8. Passage to AQ1
**Finite states.** AQ1's finite states are the unique untruncated full-Hilbert grounds on Lambda_N; by AM2 uniqueness they are gauge invariant. The bound holds for every N with R contained in Lambda_N, uniformly in N.

**Limit.** Along AQ1's diagonal subsequence, rho_{N_k,R} -> rho_R in trace norm, so ||rho_R-P_R||_1 <= D for every subsequential limit of that construction.

**Exclusions.** Two such limits are within 2D on R. That is uniform local closeness, **not** uniqueness, whole-sequence convergence or a rate in N.

## 9. Scaling, targets and AV2 feasibility
**Scaling.** The exact ratio D(tau)/D(tau/100) is 100.00147 for tier (i) and 100.00976 for tier (ii); the purification brackets also lie in [99,101]. For AT4, D=2sqrt(49|tau|/3) has a squared ratio of exactly 100, so its ratio is 10, inside [9.9,10.1]; the linear band rejects it. The tau=+10^-10 point is a scaling control only.

**AV2 threshold.** AV2 needs 2(D+D^2)+49*10^-8/pi <= 10^-6. Machin gives a directed pi bracket (rounded outward to 10^-30). Then D=4/10^7 and 4.22*10^-7 are feasible, while 4.23*10^-7 is infeasible even at the favourable end of the pi bracket.

**Results.**
- **Tier (ii) passes.** D_ii (1.361e-8 by the triangle bound, 6.95e-9 grouped) passes 4/10^7, with a margin of about 29, and 10^-6 at both signs. The AV2 radius preview with D_ii is 1.832e-7.
- **Tier (i) fails.** D_i (2.368e-5; 1.792e-5 iterated) fails both targets by a factor of about 59 against 4/10^7. That failure is retained, not retuned.
- **Comparison with AT4.** AT4's 8.083e-4 is about 5.9*10^4 times D_ii.

## 10. Review checklist: where a producer is most likely to err
1. Normalizing by 1+O(tau^2), dropping ||delta||^2 from Z, or letting the outside creations "cancel" in the numerator only.
2. Writing c^_I psi_out = c_I (x) phi_out for a straddling I, or calling straddling terms "outside"; or counting only the 10 faces inside R.
3. Omitting the two-creation term c^_I c^_J (I ni 0, J ni e_z, disjoint), after which psi is no longer psi_out+delta.
4. Defining e with ||psi|| instead of ||psi_out||, which breaks Tr(rho P_R)=1/(1+e^2); or asserting orthogonality without the fact that every c_I is excited on every site of I.
5. Not proving that 2e(1+e)/(1+e^2) is monotone (it is, on [0,1+sqrt2]), or that e <= eps.
6. Using 49|tau|/144 as the exact anchored norm (it is a triangle bound), or putting grouped square roots in as floats. Using 82/144 as the anchored norm: 82/144 may bound only sum_{I meets R}||c^(1)_I||, and then 2*352Jt must be added. That labelled refinement gives eps ~ 5.6951e-9 and D ~ 1.1390e-8.
7. Getting t <= t_1/(1-352J) without the AM2 ball t <= R and the convexity of G; setting the remainder to zero; using the circular t_1(1+352J); or combining the crude tier-(i) t with the exact c^(1) (tier mixing).
8. Counting faces at sites 0 and e_z only, hard-coding 49, or presenting 84 as exact.
9. Not noting that c^(1) in the cutoff space is Q_n c^(1); citing AM2 §6 (eigenvalues) for the vector limit; or omitting E_n >= E or the uniform cutoff gap.
10. Adding a uniqueness, whole-sequence or rate statement at the AQ passage; or forgetting that AQ1's finite states are full-Hilbert grounds.
11. Inserting a negative tau without |.|, or presenting the -tau run as an independent confirmation (it is a replay of the same |tau| formula).
12. Reporting the irrational 2eps/sqrt(1+eps^2) as a decimal without a rational directed bound; letting a float reach an admission Boolean; or testing the ratio with float logarithms.
13. Mixing units: the face energy is 24 normalized versus 3 in alpha units, and the amplitude tau/72 must agree in both; the per-site sum is 28|tau| (four incoming stars), not 7|tau|.
14. Scope creep: the sign of omega(W), the coefficient 1/144, or first-order parity vanishing (all excluded, AW1). Reverse inputs that go beyond AGENTS.md, the contract and shared_premises.
