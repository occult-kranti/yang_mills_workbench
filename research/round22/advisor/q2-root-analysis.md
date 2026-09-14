# Q2 advisor derivation before producer review

This derives the frozen question independently for advisor comparison. It is not a gate or a preselected conclusion supplied to either producer. Source, proof and controls still require the paired and skeptical review.

## Actual complementary electric spectrum

A nonconstant physical Peter–Weyl spin assignment has a nonempty set of positive-spin links. All-vertex Gauss invariance forbids exactly one positive-spin incident edge at any vertex, because a nontrivial irreducible representation has no invariant vector. That subgraph therefore contains a cycle. The actual simple rectangular graph has girth4, and each positive link Casimir is at least3/4, so every nonconstant physical electric eigenvalue is at least3alpha. The constant is the sole zero eigenvector. Since P preserves it, Q is orthogonal to it. Face0 is in Q and has energy3alpha, proving that C0 has sharp lower bound3alpha. This is a full representation-tower argument, not a cutoff computation.

## Fixed channels and graph-specific leading weights

Write X for the actual six-link P2 completion of U, with edges14,2,28,3,15,26. B1f0 is minus the sum of the19 non-retained physical faces. Each has energy3alpha, and distinct faces are Haar orthogonal. Thus the leading00 kernel divided by(alpha lambda)^2 is19/4 times exp(−3alpha s/hbar).

For f1=Tr X, the19 vectors W_p f1 are mutually orthogonal under every electric spectral projector: their link-center parity signatures differ whenever p differs. Their intersections with X are single connected paths, with overlap length r distributed as follows:

| r | Face IDs | Count |
|---|---|---|
| 0 | 4,5,6,7,11,13,14,18,19 | 9 |
| 1 | 0,1,10,12,16,17 | 6 |
| 2 | 2,3 | 2 |
| 3 | 9,15 | 2 |

For r=0, all10 links carry fundamental spin, yielding energy15alpha/2 and squared norm1/4. For r>0, the shared path carries spin0 or1; its internal degree-two Gauss constraints force the same representation along the path. Integrating the shared path gives half the normalized Wilson trace around the remaining simple loop, with squared norm1/16. Total squared norm is1/4, so spin1 has weight3/16. The corresponding energies are alpha(15−3r)/2 and alpha(15+r)/2. Thus the11 spectral weights are:

| Energy / alpha | Weight |
|---|---|
| 3 | 1/8 |
| 9/2 | 1/8 |
| 6 | 3/8 |
| 15/2 | 9/4 |
| 8 | 9/8 |
| 17/2 | 3/8 |
| 9 | 3/8 |

They sum to19/4, equal to the00 value at s0, but their first energy moment is285alpha/8 rather than57alpha/4. Hence the fixed nonconstant channel discriminates a scalar reference shortcut even when its instantaneous diagonal norm happens to agree.

The off-diagonal inner product is <f0,M_K f1>=E[2xK]=1/4. Since B1f0 is a3alpha eigenvector, both off-diagonal leading kernels equal exp(−3alpha s/hbar)/4. Replace each exponential weight by weight/(energy+z) for the leading self-energy matrix. The entire3alpha weight matrix has entries19/4,1/4,1/8 and determinant17/32>0; the remaining matrix weights are nonnegative in the11 entry only.

## Exact dynamics and explicit operator remainders

C_lambda=C0+alpha lambda QVmagQ is self-adjoint on QD(H_E) and has lower bound3alpha. With ||Vmag||<=40 and ||B1||²=25/4, bounded-perturbation Duhamel gives

    ||K_lambda(s)−(alpha lambda)^2 B1*e^(−sC0/hbar)B1||
      <=250(alpha lambda)^3(s/hbar)e^(−3alpha s/hbar).

The same resolvent identity gives

    ||Sigma_lambda(z)−(alpha lambda)^2 B1*(C0+z)^−1 B1||
      <=250(alpha lambda)^3/(3alpha+z)^2.

These bounds hold for every lambda>=0, hence on the frozen0..1/100 interval. Their dimensions are energy² and energy. The absolute kernel remainder is uniformly bounded over s>=0 by250alpha²lambda³/(3e); a relative-in-time error does not remain small merely from this estimate. Self-energy bounds stay finite as z decreases to0 at fixedalpha, but the full resolvent may not; its contract remains z>0.

The projected complementary component solves Y'=−C_lambda Y/hbar−B_lambda T/hbar. Substitution gives the exact strong Volterra equation T'=−A_lambda T/hbar+hbar^−2 integral_0^t K_lambda(t−u)T(u)du, with T0=I, or its mild double-integral form. In this formula the kernel uses C_lambda and the other factor uses the full T. This is different from Q1's symmetric formula with full-H compression in the middle and A at both ends.

For z>0, the bounded off-diagonal block factorization gives

    J*(H_lambda+z)^−1J=(A_lambda+z−Sigma_lambda(z))^−1.

The Schur operator has domain D(A_lambda) and lower form boundz: minimize the positive quadratic form of H_lambda+z over the complementary variable. The triangular inverse maps into D(C_lambda), so the formal block equation is a closed-domain identity. Sigma is positive and its norm derivative is−B_lambda*(C_lambda+z)^−2B_lambda, strictly negative as a quadratic form on each nonzero selected vector when lambda>0. Its energy dependence cannot be discarded by a single constant fit.

All parameters and the physical clock stay fixed as in Q1. The channels are Haar-reference Hilbert matrix elements, not interacting-ground correlations. A common energy shift changes both diagonal blocks and the resolvent energy argument consistently. These finite-graph results do not imply autonomous closure, homogeneous stability or a continuum theorem.


## Post-freeze root comparison

Both full reports and source notes, both complete checker sources (including the separately read reverse opening), and the frozen skeptical preparation were read. Four fresh root normal/optimized replays reproduced all expected files bytewise. The independently derived seven energy matrices, moment285/8, cross weight1/4, complementary gap3alpha and full-Hilbert cubic constants agree. Both sources derive Schur positivity by the actual closed block form; Dusson Theorem1.2 is not imported across its bounded-map premise. The electric reference state remains distinct from an interacting ground. Both prove positive self-energy ordering by inverse order, without assuming heat-operator order. No producer repair is indicated by root review. Skeptical review remains required before admission.
