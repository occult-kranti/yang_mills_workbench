# AD1 forward: the elementary Wilson witness has a trivial slow endpoint

This independent first-loop calculation uses the canonical summable family, the actual free cube at O=(3,1,0), and the original clock T_q=(z/eta)(hbar/alpha)(1-q)^-3, 0<z<=10^-6. No current reverse solution was read. Newton's reconstruction tests whether this observable identifies a rate; Tesla's loading test retains every exterior face and actual strip excitation. The outcome differs from the inherited rank observable: the demodulated elementary Wilson correlation tends exactly to one.

## Fixed actual multiplication observable

Fix f0 to be the yz face anchored at O, and B=2x_f0=Tr(U_boundary(f0)), as bounded multiplication extended by the exterior identity. All four links are free Haar factors. B is real, self-adjoint, gauge invariant and has operator norm two. Its actual reference mean is zero and variance one by fundamental-character Haar orthogonality. Let psi=B Omega. Then ||psi||=1 and K psi=3psi for K=H0/alpha, since its four half-spin edges cost 4(3/4). These are full-reference statements including the unchanged strip grounds. B is not the U/AA local rank operator, and B psi is not Omega: the same-face product gives

    x_f0 psi=(Omega+chi_1,f0)/2,
    B psi=Omega+chi_1,f0.                            (AD1.1)

The spin-one character is normalized with K energy eight. The actual interacting variance differs from one by at most 8 d_q+16 d_q², using ||B||=2 and the inherited projector-distance bound d_q. It tends to one. This is not a zero-variance constant observable.

## Complete source-specific energy selection

For every complete-factor collar k>=1 used by AA2/Y2, write A_(q,k)=-sum_f q^r_f x_f/24 and Abar_(q,k)=sum_E P_E A_(q,k)P_E. We prove P_3 A_(q,k)psi=0 in the actual regional Hilbert space, without enumerating the whole energy-three shell.

Inside the free cube, the six faces intersect the occupied square in r=4 (itself), r=1 (four adjacent faces), or r=0 (opposite face) edges. Fundamental multiplication changes electric energy by

    Delta=3-(3/2)r+2m,  m=0,...,r.

For these three r values no Delta is zero. The actual same-face fusion restricts further to energies zero and eight as (AD1.1); allowing the other algebraic branches only weakens the nonzero separation. Adjacent faces cost at least 3/2, and the opposite face costs three.

Every face meeting the cube but not contained in it meets exactly one cube edge. AA2's complete enumeration and owner proof apply equally to the present occupied subset: the opposite edge is free; the two remaining sides belong to distinct outside reference factors. If the shared cube edge is occupied, its lowest energy decrease -3/4 is canceled by the opposite free edge's +3/4, while the two other sides each cost at least 1/8. If unoccupied, there is an additional positive cost. Strip sides lie spectrally orthogonal to their gauge-invariant ground through the charged endpoint action, so this is a bound on spectral support, not just mean energy. Thus all such images have energy at least 3+1/4. Finally a cube-disjoint omitted face excites the outside reference by at least 1/8 and leaves the square energy unchanged.

Consequently

    Abar_(q,k)psi=0,  Abar_(q,k)Omega=0,
    dist(0, nonzero participating energy differences)>=1/8.
                                                        (AD1.2)

The first equality means the actual averaged reachable component is the one-dimensional span of psi with zero averaged generator. It is a reducing zero eigenspace of Abar. It neither says psi spans the whole reference energy-three shell nor that the unaveraged A preserves it. Indeed <Omega,A_(q,k)psi>=-q^4/48 is nonzero for q>0, proving actual instantaneous leakage.

## Original-clock limit and full-system error

Use tau_q=eta/[8b(q)], s_q=(z/eta)tau_q/(1-q)^3<=3z/2 and M_k=N_k/24. The inherited strong primitive/integration-by-parts proof, now with the participating-frequency bound (AD1.2), gives on each of the two unit inputs psi and Omega

    ||(Z_(q,k)(s_q)-I)input||
       <=b_k:=16tau_q M_k(1+3z M_k).              (AD1.3)

It also bounds the corresponding adjoint error, by unitarity and the zero averaged action. No all-input operator-norm averaging is used. The correctly ordered reference scalar is

    exp(i3alpha t/hbar)<Omega,B beta_q^t(B)Omega>
       =<psi,Z_q(s) B Z_q(s)*Omega>.

Because ||B||=2 and B Omega=psi, its regional error from one is at most 2b_k+b_k=3b_k. The second factor cannot be treated as a rank operator with norm one. Changing the full stationary connected state to the reference costs at most 6||B||² d_q=24d_q, including its connected mean. The support of B is a subset of the original eight free U links, so the inherited complete-factor collars and connected-word tail apply; with both B factors their bound is 4D_k(15z). Thus the actual full stationary connected correlation C_B,q obeys

    |exp(i3alpha T_q/hbar) C_B,q(T_q)-1|
      <=24 dhat_q+4D_k(15z)
         +48tau_q M_k(1+3z M_k),                  (AD1.4)

where dhat_q=tau_q sqrt(b(q²)/96)/[(1-eta)/8], and D_k is the exact inherited positive connected-tail certificate. This retains full stationary replacement, every external loading path and the original physical clock. It introduces neither a regional stationary state nor an interacting-ground phase deletion. The q-dependent coefficients need no replacement: the averaged action is zero for every q.

Taking q to one at fixed k kills the state and averaging terms; then k to infinity kills D_k. Therefore

    lim_(q->1) exp(i3alpha T_q/hbar) C_B,q(T_q)=1

for every admitted z. The undemodulated scalar still has its rapidly oscillating reference phase. There is no conclusion of a global q=1 Hamiltonian or full-operator dynamics.

For eta=1/2,z=10^-6,q=1-10^-12 and k=3, N_k=332, the checker gives a rational disk about one with radius below 5e-18. The physical time remains 2e30 hbar/alpha. This is a mathematical enclosure, not a practical instrument or measured frequency.

## Held-out dynamic discriminator and obstruction to clock identification

The already-admitted AA2 rank-observable endpoint has slope +i/84 in z, while the present actual Wilson-multiplication endpoint has every z derivative zero. Applying the AA2 oscillatory formula to B therefore fails an actual held-out observable test: the lower bound z/84-z²/3528 is strictly positive throughout 0<z<=10^-6. No constant rescaling of z converts this constant scalar into the AA2 nonconstant one. This is not evidence that either physical model has changed; their probes reach different electric sectors in the same canonical family.

Consequently B alone carries no slow-endpoint rate information at this clock. A new observable or higher-order clock could be investigated only under a separately frozen follow-up contract. No such additional experiment is executed here, and no empirical or continuum scale match follows from either scalar. Tau_q and q retain their original model meanings; alpha,hbar and the physical clock are not fitted.

## Verification and scope

The standard-library checker reconstructs all twelve free cube links, six internal faces and twenty exterior faces with all factor owners; it verifies the exact occupied-edge intersection counts, distinct strip factors, charged-side energy bounds, same-face Haar moments and instantaneous vacuum leakage. It independently rebuilds the inherited support collars and full rational error budget. Wrong-model controls reject treating B as norm one or replacing its square action by the rank swap. Normal and optimized outputs must agree. The source inventory includes the additionally consulted U1 report and all frozen dependencies. Mathematical source-support proofs, not a sampled strip spectrum, establish the selection rule. Scientific priority is unverified.

Accepted scope: an actual elementary Wilson scalar endpoint and finite-q full-system enclosure. Limited parent: this witness does not supply the requested nontrivial scale bridge; no homogeneous source inverse, Hamiltonian operator limit, larger-volume calibration or continuum mass gap follows.
