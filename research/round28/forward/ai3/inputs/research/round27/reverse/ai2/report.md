# AI2 reverse: a finite-profile discriminator survives full scalar errors

Independent reverse derivation and implementation from the frozen AI2 contract; no current forward AI2 files were read. Instruction snapshots were frozen in `inputs/` before scientific production. Model: the inherited canonical summable full-link SU(2) family, fixed alpha/E_star and hbar. No lattice-spacing or physical-clock fit is introduced. The result is a narrow mathematical discrimination of two predeclared hypotheses, not general continuous calibration.

## 1. Actual multiplication operators and physical paths

Use the free unit cube based at O=(3,1,0). The following closed vertex paths specify Wilson characters chi_10, chi_6 and chi_9 exactly; reversing a path gives the same real SU(2) trace.

| Character | Closed physical path |
|---|---|
| chi_10 | (3,1,0), (3,2,0), (3,2,1), (4,2,1), (4,2,0), (4,1,0), (3,1,0) |
| chi_6 | (3,1,0), (3,1,1), (3,2,1), (4,2,1), (4,2,0), (4,1,0), (3,1,0) |
| chi_9 | (3,1,0), (3,2,0), (3,2,1), (4,2,1), (4,1,1), (4,1,0), (3,1,0) |

Define B4=(chi_10+chi_6)/sqrt(2), B5=(chi_10+chi_9)/sqrt(2) as multiplication extended by the outside identity. Each character has norm 2, zero Haar mean and squared Haar norm 1. Distinct characters are orthogonal: an unmatched free link changes sign under its center action, while Haar measure is invariant. Consequently each B has mean zero and variance one. Its operator norm is exactly 2sqrt(2), because the trace triangle bound is approached in neighborhoods of identity holonomies with positive Haar measure.

The two loops in each pair share a path but also have independent exclusive Haar paths. Integrating those exclusive paths gives their independent character laws conditional on the shared holonomy. Hence the fourth moment is (2+2+6)/4=5/2. These are not rank swaps: ||B^2 Omega||^2=5/2, while a normalized rank swap would give 1. All norms in the transfer below are multiplication norms.

Their normalized vacuum-created vectors are psi4=(e10+e6)/sqrt(2) and psi5=(e10+e9)/sqrt(2), in reference energy 9alpha/2. Enumerating all connected degree-two six-edge subsets of the actual twelve-edge cube reconstructs exactly sixteen cycles. Their symmetric differences give all face flips. The joining face for B4 is the yz face at (3,1,0), exponent 4; that for B5 is at (4,1,0), exponent 5. In the inherited pinched generator the complete reached matrix is -Q(q)/96 with those exact face weights.

The AA2 proof applies to the whole sixteen-dimensional reached component, not merely psi4. The checker re-enumerates all twenty exterior touching faces, the free opposite edge and distinct remaining complete-factor owners. Their spectral loading is at least 1/4 above the cube energy; disjoint faces load the outside ground by at least 1/8. These spectral subspace statements justify the inherited source-specific participating-frequency bound 1/8 and reducing-component theorem for psi5 as well. The unaveraged dynamics still leaks; no instantaneous closure is asserted.

## 2. Exact retained moments and conditional inverse

Write v=alpha tau_q t/(96 hbar), tau_q=eta/[8b(q)], and f_r(v)=<psi_r,exp(i v Q(q))psi_r>. Exact moment polynomials obtained by weighted walks on the full matrix are

| Moment | B4 | B5 |
|---|---|---|
| m0 | 1 | 1 |
| m1 | q^4 | q^5 |
| m2 | 2q^8+2q^10 | 2q^8+2q^10 |
| m3 | 3q^12+5q^14 | 5q^13+3q^15 |

The checker exports all moment polynomials through degree 8 and verifies their evaluations independently against rational matrix multiplication. Thus the retained imaginary derivatives with respect to v have ratio q. If a physical retained slope L4=alpha tau_q q^4/(96hbar) were separately identified, the conditional algebraic inverse would be

    q=L5/L4,
    eta=768 hbar b(q) L4/(alpha q^4).                 (R1)

This needs alpha and physical time calibration, nonzero slope, the specified model and justification of retained-slope inference. It is not obtained by differentiating the full-system value error. Differentiation with respect to z instead removes eta from the retained time coefficient, so it cannot be silently substituted into this inverse.

## 3. New support, complete collars and tail

The old eight-link seed for B4 misses B5 links. We use the union of all three cycles, exactly ten singleton free factors. For factor set F let E(F) contain every link of every complete factor. Grow F_(k+1) by adjoining all owners of every omitted face meeting E(F_k), and retain O_k={omitted f: owners(f) subset F_k}. The independent enumeration gives:

| k | Complete factors | Complete links | N_k=retained omitted faces | Crossing faces |
|---:|---:|---:|---:|---:|
| 0 | 10 | 10 | 2 | 21 |
| 1 | 41 | 113 | 25 | 114 |
| 2 | 149 | 329 | 143 | 211 |
| 3 | 333 | 675 | 359 | 330 |
| 4 | 610 | 1177 | 695 | 470 |
| 5 | 993 | 1857 | 1171 | 631 |

At every k>=1 the whole cube and its six faces are inside. No old N3=332 is reused. Strips retain their complete infinite-dimensional Hilbert spaces.

Each factor contains at most ten links, each link meets at most four faces, and a connected face can add at most three factors. Starting with ten factors gives the order-n majorant (p)_n x^n/n!, p=10/3, x=10 alpha tau_q |t|/hbar. This follows by multiplying the incidence bound 40(10+3j), interaction norm 1/24, commutator factor 2, and time-simplex factor 1/n!. Connected words of length <=k agree exactly in full and retained dynamics. One full-series omitted tail therefore suffices:

    D_k(x) <= [(10/3)_(k+1)/(k+1)!] x^(k+1)/(1-x)^(k+5). (R2)

Taylor's integral remainder actually gives exponent k+13/3; the integer exponent k+5 is a valid upper bound for 0<=x<1. This includes every ordering, repeated face, exterior excursion and return. At the original t=T_q(z), x<=15z, 0<z<=10^-6. Multiplying by the two B factors costs ||B||^2=8, independently of the ten-factor support count.

## 4. Complete finite-time disks and the ratio certificate

Use the unchanged rational profile

    b(q)=(2+5q+5q^2+6q^3+3q^4)/[24(1-q)^3(1+q)^2(1+q^2)],
    s_q=(z/eta) tau_q/(1-q)^3, v=s_q/96,
    d_hat=tau_q sqrt(b(q^2)/96)/[(1-eta)/8], M_k=N_k/24.

For either actual stationary connected correlation, with the common reference carrier removed, the inherited component-wide strong averaging argument and new support tail give

    |exp(i 9alpha T_q/(2hbar)) C_r,q(T_q)-f_r(v)|
      <=48 d_hat +8 D_k(15z)+64 tau_q M_k(1+3z M_k).     (R3)

The terms are respectively full stationary-state replacement (including the connected mean), complete spatial tail, and both correctly ordered evolution errors. The averaging coefficient uses 1+||B||<4. There is no regional stationary-state substitution or uncontrolled ground-phase deletion.

The degree-eight complex center is evaluated exactly as sum_n i^n v^n m_n/n!. If R=max row sum Q<=6, the independent unitary Taylor remainder is A=(vR)^9/9!. Add A to (R3) for full radius E. Square roots are rounded upward with integer arithmetic at binary denominator 2^300. All reported acceptance signs use exact fractions; decimal values below are only displays.

For a finite-difference ratio let y_r be the imaginary part of a demodulated full correlation and add any known absolute measurement/calibration error nu_r. The real spectral inequality |sin x-x|<=|x|^3/6 gives

    |y_r-v q^r| <= delta_r,
    delta_r=E_r+nu_r+(vR)^3/6.                          (R4)

Including the arithmetic term already in E is conservative. If D=vq^4-delta4>0, then

    |y5/y4-q| <= (delta5+q delta4)/D.                   (R5)

The checker explicitly returns no inference when D<=0. Equations (R4)-(R5) bound finite values; they take no derivative of (R3). They can define consistency regions given measured values and admitted parameter bounds, but do not supply an exact continuous inverse with noise.

## 5. Predeclared equal-time hypothesis tests

The contract fixes H1:(q,eta)=(1-u,1/2), H2:(1-2u,1/16), u in {10^-12,10^-18,10^-24}, z=10^-6 and k in {3,4,5}. Both hypotheses have exactly eta(1-q)^3=u^3/2, so they use the same original physical time T=2*10^-6*u^-3 hbar/alpha and the same known carrier. This is a genuine equal-time comparison, not independently fitted timestamps.

All nine simple-ratio comparisons fail to separate their intervals. The cubic linearization remainder alone produces ratio radii around 10^-14 near q=1, exceeding the 10^-18 and 10^-24 differences. At u=10^-12 the full state budget is too large. Failure here means insufficient certificates, not identical true correlations.

The full degree-eight scalar centers avoid this cubic linearization loss. A sufficient exact test is |Im center1-Im center2|>E1+E2. The outcomes for both probes are:

| u | k=3 | k=4 | k=5 | T in hbar/alpha |
|---:|---|---|---|---:|
| 10^-12 | overlap | overlap | overlap | 2*10^30 |
| 10^-18 | overlap | overlap | disjoint | 2*10^48 |
| 10^-24 | overlap | overlap | overlap | 2*10^66 |

“Overlap” means imaginary projections fail the sufficient test; no exact equality is inferred. At u=10^-18,k=5, the complete radius is approximately 9.0114065651*10^-27 under H1 and 4.7617186392*10^-27 under H2. The common spatial contribution is 3.7741771995*10^-27; H1/H2 state contributions are 5.2372293657*10^-27 and 9.8754143976*10^-28. Averaging is below 1.785*10^-51 and arithmetic below 1.334*10^-70.

The exact positive separation margins after both radii are approximately

    B4: 3.2145242143*10^-26,
    B5: 4.4050004047*10^-26.                           (R6)

Each candidate may receive an additional absolute error strictly less than half the appropriate margin while preserving disjointness. The saved conservative allowance per candidate is margin/4: approximately 8.0363105356*10^-27 for B4 and 1.1012501012*10^-26 for B5. This is a mathematical error allowance, not demonstrated instrument precision. It does not mean all nearby q values can be distinguished.

The q^5->q^4 mutation makes the ideal retained slope ratio 1, losing this ratio's q sensitivity. It is not asserted to erase every q-dependent feature of both full scalar functions. Removing loading or replacing norm 2sqrt(2) by 1 undercounts certified costs; the checker rejects those substitutions and the old seed's missing support.

## 6. Clock, noise, verification and remaining scope

Unknown physical-time error has no supplied full-correlation continuity modulus here and must be bounded separately before operational inference. Likewise, unknown alpha cannot be declared calibrated by demodulation. For a known timestamp T, an error Delta a in a=alpha/hbar used only for carrier removal adds at most 36 T |Delta a|, since |C|<=||B||^2=8 and |exp(i phi)-exp(i phi')|<=|phi-phi'|. Its cost must fit inside the additional absolute allowance along with readout noise. This bound does not cover changing the true Hamiltonian's alpha or an uncertain physical timestamp. The enormous 2*10^48 clock makes this especially demanding; no feasible laboratory experiment is claimed.

Run `python3 -B research/round27/reverse/ai2/check.py --output /absolute/fresh/directory`. The standard-library checker reconstructs geometry, complete owners, all sixteen cycles, exact moment polynomials and all eighteen hypothesis/collar evaluations. Both successful and failed settings are retained. All producer and consulted source bytes, frozen contract and instruction snapshots are bound. Optimized Python must give the same output, and no historical implementation is imported.

The accepted candidate contribution is a finite-q pairwise discriminator within the inherited full canonical model, resolving the specific AI1 compensated hypotheses despite their identical endpoint surrogate. General parameter calibration, a continuous finite-q inverse, an actual apparatus, a homogeneous matching map, and continuum existence/mass gap remain open. This is one research loop; exploratory executions and optimized replay do not increase its count. Scientific priority is unverified.
