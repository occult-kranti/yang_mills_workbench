# AD1 reverse: the elementary Wilson face has a null slow endpoint

Independent reverse reconstruction, frozen before reading current forward work. On the canonical summable full-link family, fix the free cube at O=(3,1,0) and its bottom xy face f=(x,y;3,1,0). The observable is the actual multiplication B=2x_f=Tr(U_f), extended by identity everywhere else. It is gauge invariant, self-adjoint and bounded with norm 2. Conditional Haar integration gives <B>_0=0 and <B²>_0=1, so its reference vacuum variance is exactly one. This is neither a rank operator nor a two-state replacement.

With the original negative-time Heisenberg convention and the full stationary connected correlation C_q^B, the result is

    lim_(q->1-) exp(i 3alpha T_q/hbar) C_q^B(T_q)=1,
    T_q=(z/eta)(hbar/alpha)(1-q)^-3,
    0<eta<1, 0<z<=10^-6.                            (AD1.R1)

The demodulation removes the actual reference energy 3alpha, not the rank observable's energy 9alpha/2. It changes no physical time. Fixed a,E_star,alpha/E_star,hbar remain positive. Newton's inverse test identifies the null observable's inability to fit a slow clock; Tesla's loading check is the exterior spectral argument below.

## Actual reached vector and complete exterior exclusion

Let phi=B Omega. Its four occupied free links carry spin 1/2, so K phi=3phi, ||phi||=1. Complete free-cube gauge-invariant energy-3 states are the six elementary face characters: 3 n_(1/2)+8 n_1=12 in quarter units permits only four half-spin edges; Gauss invariance requires an even occupied degree at each cube vertex; four occupied edges therefore form a square. This gives six orthogonal vectors. The conclusion below is stronger than merely computing their six-by-six compression: it excludes every exterior equal-energy image of the actual phi.

For any internal cube plaquette h, let r be the number of its edges occupied in phi and m the number of occupied edges fusing to spin one. Its energy change is

    Delta=3-(3/2)r+2m.                             (AD1.R2)

For an elementary input face and an internal cube face, r is 0, 1, or 4, never 2. For every integer 0<=m<=r the change is nonzero in those three cases. This checks an overcomplete list of fusion branches, so gauge-forbidden branches cannot restore a zero. Thus P_3 x_h phi=0 for every internal h; the same holds for all six input face vectors.

Every omitted face touching the cube but not internal shares exactly one cube edge. There are twenty, including the positive-octant boundary convention. The opposite parallel edge is a free reference factor. If the shared edge was occupied, the least -3/4 change is canceled by +3/4 on that opposite free edge. The two remaining sides occupy distinct exterior reference factors. A free side costs at least 3/4; a selected-strip side lies orthogonal to its gauge-invariant strip ground because a single open fundamental matrix transforms nontrivially at an endpoint. Its complete spectral support therefore lies above the inherited strip gap 1/8. The two side costs sum to at least 1/4. If the shared edge was unoccupied, its extra +3/4 only increases the cost.

The full matrix-index contraction remains inside these tensor spectral subspaces. This is a spectral-support bound, not an expectation-only estimate. The opposite and two side owners are enumerated by the checker. Faces disjoint from cube links leave phi unchanged on the cube and create a positive outside excitation, since each omitted face has zero outside reference expectation. They also cannot return to energy 3. Sharing a vertex does not change factor support. No supposed gap between all regional excited levels is used.

Consequently every complete-factor region containing the cube and its relevant faces obeys

    Abar_(q,k) phi=0, Abar_(q,k) Omega=0,
    Abar_(q,k)=sum_E P_E[-sum_(h in O_k) q^|anchor(h)| x_h/24]P_E. (AD1.R3)

The one-dimensional reached space span(phi) is a reducing null component of this bounded self-adjoint pinched operator. The entire regional energy-3 space may be larger; it need not be enumerated. All one-step nonzero frequencies reached from phi or Omega have absolute value at least 1/8 (the internal arithmetic is stronger, the exterior and vacuum gap supply this common conservative value). Instantaneous dynamics does not reduce span(phi): B² Omega already includes a spin-one face. Equation (AD1.R3) concerns the averaged operator only.

## Full-system limit and finite-q remainder

Use complete-factor collars beginning with all twelve free cube links, a harmless enlargement of B's four-link support. Add every owner of every omitted face meeting the accumulated complete factors, and retain every omitted face wholly supported there. All reference factors and boundary returns are preserved. At the jth ordered commutator there are at most 12+3j factors, each incident to at most 40 faces. With coefficient norm alpha tau_q/24, commutator factor two and ordered simplex 1/n!, the complete nth term for a norm-one initial observable is bounded by

    (4)_n x^n/n!, x=10alpha tau_q|t|/hbar.

This includes repetitions and all orderings. At T_q, x<=15z<1. Matching all words of length <=k between the full and regional evolutions gives the complete omitted tail

    D_k^cube(x)=[(4)_(k+1)/(k+1)!] x^(k+1)/(1-x)^(k+5). (AD1.R4)

The bound follows directly from the Taylor remainder of (1-x)^-4. The larger p=4 is required by the twelve-factor support; the prior eight-factor p=8/3 is not substituted. Since ||B||=2, the correlation spatial cost is at most 4D_k^cube(15z).

Write N_k=|O_k|, M_k=N_k/24 and use the actual canonical profile

    b(q)=(2+5q+5q²+6q³+3q⁴)/[24(1-q)³(1+q)²(1+q²)],
    tau_q=eta/[8b(q)], s_q=(z/eta)tau_q/(1-q)³<=3z/2,
    dhat_q=tau_q sqrt[b(q²)/96]/[(1-eta)/8].

The source-specific 1/8 frequency separation gives the Y2 strong primitive bound 16tau_q M_k on Omega and phi. Integration by parts along their constant averaged orbits gives the conservative full evolution bound b_k=16tau_q M_k(1+3z M_k) on each. This uses the full finite-factor compact-resolvent operator and actual Gauss sector, not a finite-spin truncation. Both Z and Z* columns are controlled.

The exact ordered identity is

    exp(i3alpha T_q/hbar)<Omega,B beta_q^(T_q)(B)Omega>
      =<phi,Z B Z*Omega>.

Replacing Z and Z* by their averaged columns costs at most 4b_k (a conservative allowance using ||B||=2, ||phi||=1). Their averaged matrix element is exactly <phi,phi>=1 by (AD1.R3), for every q; there is no coefficient-to-one or slow-time substitution error. Replacing the actual full stationary state, including both connected means, costs at most 6||B||² dhat_q=24dhat_q. Comparing to the regional reference-state dynamics and including the complete spatial tail gives

    |exp(i3alpha T_q/hbar)C_q^B(T_q)-1|
      <=24dhat_q+4D_k^cube(15z)
         +64tau_q M_k(1+3z M_k).                    (AD1.R5)

Every term is a full-system cost with its original physical clock. At fixed k, dhat_q and tau_q tend to zero as q tends to one. The limsup is therefore at most 4D_k^cube(15z), which tends to zero as k increases. This proves (AD1.R1) in the correct order of limits without constructing a global q=1 Hamiltonian. The checker supplies rational enclosures of (AD1.R5), not simulated trajectories. The exact center is one and has no floating subtraction error.

## Reserved discriminator and what the null response cannot identify

The endpoint scalar in (AD1.R1) is constant in z. It cannot identify a slow-time calibration, the sign of a clock, or matching to another Hamiltonian. A held-out six-cycle Wilson character D=Tr(U_C) on this same free cube is explicitly reserved: choose the lexicographically first six-edge cycle in the checker's sorted cube-edge indexing. The inherited AA1/AA2 complete shell and exterior proof give its endpoint scalar <e_C,exp(i(z/84)A)e_C>, where A is the sixteen-cycle adjacency. Its slope is zero but its second derivative is

    F_D''(0)=-degree(C)/84² <0.                       (AD1.R6)

The checker reconstructs the exact cycle and its degree independently; no fitted coefficient uses this held-out information. This supplies a dynamic discriminator that distinguishes the elementary face's null endpoint from a nontrivial Wilson endpoint. A formal future matching test must freeze its preparation, second derivative or full curve and error budget before fitting any model. That matching task is not claimed completed here.

The established scope is one full stationary scalar endpoint and its finite-q error certificate in the canonical summable model. It is not a global operator limit, an all-observable endpoint law, a homogeneous gap, a calibrated physical mass or continuum construction. Scientific priority is unverified.
