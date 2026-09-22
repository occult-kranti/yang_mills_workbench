# AD2 forward: actual Wilson multiplication reaches the nontrivial endpoint

Independent second-loop derivation from the frozen AD1/AA evidence, before current reverse AD2 access. Both observables are the precisely named U paths, not conveniently chosen eigenvectors. Their actual multiplication correlations have full canonical endpoint formulas and finite-q error budgets. Equality of one vacuum-created vector does not identify the multiplication operator with the old rank operator.

## Fixed observables and actual operator distinctions

Translate the unit cube by O=(3,1,0). Use the original paths X: O to (3,2,0) to (3,2,1); Y: O to (3,1,1) to (3,2,1); Z: O to (4,1,0) to (4,2,0) to (4,2,1) to (3,2,1). Set chi_X=Tr(XZ^-1), chi_Y=Tr(YZ^-1), and actual multiplication operators

    B_X=chi_X,  B_sum=(chi_X+chi_Y)/sqrt(2).

They are bounded self-adjoint Gauss-invariant operators extended by identity. Their exact norms are 2 and 2sqrt(2), respectively: the upper trace bounds are attained at identity holonomies and neighborhoods have positive Haar measure. Both have reference mean zero and variance one. Indeed independent Haar X,Y,Z give orthogonal normalized characters; conditional on Z the X and Y characters retain independent Haar-character laws. The vectors B_X Omega=phi_X and B_sum Omega=psi+=(phi_X+phi_Y)/sqrt(2) have reference energy E=9alpha/2.

Their fourth vacuum moments are two and 5/2, whereas the old rank W has fourth moment one. In particular

    ||(B_X²-I)Omega||²=1,
    ||(B_sum²-I)Omega||²=3/2.

Thus B_sum Omega=W Omega is true but B_sum=W and B_sum²Omega=Omega are false. Norm-one state/remainder estimates from W cannot be copied unchanged.

## Whole actual reached component and exact spectral measures

AA1 proves the complete free-cube six-cycle shell consists of sixteen orthonormal characters. AA2 proves, using all twenty exterior faces and the actual charged strip gaps, that their span times the exterior ground is a reducing component of every regional pinched operator. The proof applies to every vector of that span, including each new source here. It does not claim the entire regional energy shell consists of these sixteen vectors. Its reachable nonzero frequencies and the vacuum source are separated from zero by at least 1/8.

The fixed X,Y paths are reconstructed from physical coordinates and match inherited indices 10 and 6. The full sixteen-by-sixteen adjacency A is reconstructed by face symmetric differences, and obeys A(A²-4I)(A²-12I)=0. The checker uses exact polynomial projectors to recompute each source measure. For theta=z/84, the single-cycle measure is

| Adjacency eigenvalue | B_X source weight |
|---|---:|
| 0 | 2/3 |
| +2, -2 | 1/8 each |
| +2sqrt(3), -2sqrt(3) | 1/24 each |

Consequently its full demodulated endpoint is

    F_X(z)=2/3+(1/4)cos(2theta)+(1/12)cos(2sqrt(3)theta).
                                                        (AD2.1)

For B_sum the recomputed weights are 1/3 at zero, 3/8 and 1/8 at +2 and -2, and 1/12+1/(8sqrt(3)), 1/12-1/(8sqrt(3)) at +2sqrt(3), -2sqrt(3). They give

    F_sum(z)=1/3+(1/2)cos(2theta)+(1/6)cos(2sqrt(3)theta)
      +i[(1/4)sin(2theta)+(1/(4sqrt(3)))sin(2sqrt(3)theta)].
                                                        (AD2.2)

These are the actual full stationary scalar limits, with demodulation exp(i E T_q/hbar) and original T_q=(z/eta)(hbar/alpha)(1-q)^-3. The equality of (AD2.2) with AA2's rank-scalar formula follows from the shared source vector and the separately proved state-specific transfer below, not equality of full operators.

The source moments m_0 through m_6 are (1,0,2,0,16,0,160) for X and (1,1,4,8,32,80,320) for the coherent sum. Thus

    theta²-(2/3)theta^4 <=1-F_X(z)<=theta²,
    |F_sum(z)-1-i theta|<=2theta².

The lower bound for X is positive throughout the admitted z range. Both are nontrivial Wilson-multiplication endpoint witnesses; one has quadratic leading change and the coherent sum has linear imaginary change. They retain multiple frequencies at the same physical clock.

## Full finite-q transfer with the actual multiplier norms

Use exactly the eight-link U seed and its complete-factor collars, which contain both sources. For k>=1, AA2 gives the actual weighted flip matrix Q(q), with entries q^r_f for a face flip, r_f in {4,5}, and Abar_(q,k)|L=-Q(q)/96. Its symmetric row norm is at most six. Let

    tau_q=eta/[8b(q)], s_q=(z/eta)tau_q/(1-q)^3,
    M_k=N_k/24, b_k=16tau_q M_k(1+3zM_k),
    f_j(q,z)=<psi_j,exp(i s_q Q(q)/96)psi_j>.

On psi_j and the vacuum, the full regional interaction evolution has error at most b_k from the corresponding averaged orbit, by AA2's actual reducing and participating-frequency proof. For J=||B_j||, the ordered reference identity

    exp(iEt/hbar)<Omega,B_j beta_q^t(B_j)Omega>
      =<psi_j,Z_q(s) B_j Z_q(s)*Omega>

costs at most (1+J)b_k when both evolutions are replaced. The first source is normalized; the second multiplier contributes its actual norm J. The full stationary connected state replacement costs 6J² dhat_q, including its squared mean, and the complete spatial tail costs J² D_k(15z). Therefore

    |exp(iET_q/hbar)C_j,q(T_q)-f_j(q,z)|
      <=6J² dhat_q+J² D_k(15z)+(1+J)b_k.          (AD2.3)

For B_X use J=2 exactly. For B_sum use J²=8 exactly and 1+J<4 in the averaging term. No normalized-rank substitution is made. At fixed k the state/averaging terms vanish as q tends to one; Q(q) tends to A and s_q tends to8z/7. The tail tends to zero with k, giving (AD2.1)-(AD2.2). This is an ordered scalar/spatial limit, not a global q=1 generator or an operator-norm averaging theorem.

For finite q the checker computes the degree-eight scalar Taylor center exactly in rational arithmetic, using integer source vectors with normalization squared one or two. The full unitary remainder is at most (s_q/16)^9/9!. This arithmetic remainder is separate from (AD2.3). At eta=1/2,z=10^-6,q=1-10^-12,k=3,N_k=332, the total radius about the rational center is below 5e-18 for X and below 1e-17 for the coherent sum. The original physical time is2e30 hbar/alpha. If comparing directly to the limiting formula, add s_q(1-q^5)/16+|s_q-8z/7|/16; no finite-q coefficient error is silently discarded.

## Held-out checks and interpretation

The AD1 elementary yz plaquette has constant demodulated endpoint one despite variance one. It is a null check against treating all Wilson probes as equivalent. The fixed X six-cycle has zero slope and second moment two; a single cosine matching that second moment would have fourth moment four, contradicting the actual sixteen. The coherent sum's second moment four rejects a single phase fitted to its mean one. The exact fourth vacuum moments additionally reject copying the rank-operator norm budget even when its endpoint scalar agrees.

These multiple observables and higher moments are source-specific tests in the same canonical family. They do not calibrate alpha in physical units, establish a measured resonance, or match the distinct homogeneous and finite-graph generators. Changing the original clock is unnecessary for the nontrivial multiplier witness and is not done here. Scientific priority is unverified.

The checker reconstructs paths, all sixteen cycles, every flip, the minimal polynomial, exact source moments, spectral weights and finite-q scalar centers. It binds frozen proof dependencies, uses standard-library exact fractions, and has explicit exceptions active under optimization. Domain, exterior exclusion and state-transfer proofs supply the infinite-system claim; a finite matrix alone would not. The accepted result is an actual Wilson-multiplication scalar bridge with complete error costs. Continuum scale matching and a mass-gap construction remain open.
