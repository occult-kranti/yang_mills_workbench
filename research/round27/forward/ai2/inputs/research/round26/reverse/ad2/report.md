# AD2 reverse: two actual six-cycle Wilson endpoint laws

Independent reverse derivation under the frozen AD2 contract, without current forward AD2 access. Both observables are bounded multiplication in the canonical summable full-link model at the original physical clock. The frozen cycles are exactly AA1's u_indices [10,6], in its fixed twelve-edge cube indexing, translated by O=(3,1,0):

    C_X={1,2,5,7,9,11}, C_Y={0,2,3,7,9,11},
    B_X=chi_X, B_sum=(chi_X+chi_Y)/sqrt(2).

Here chi_C=Tr(U_C), never a finite-rank swap. Newton's inverse reconstruction uses the complete spectral measures; Tesla's loading check reuses the actual AA2 reducing-component proof, not only a two-state matrix. Physical a,E_star,alpha/E_star,hbar are fixed, E=9alpha/2, and T_q=(z/eta)(hbar/alpha)(1-q)^-3 with 0<eta<1, 0<z<=10^-6.

## Actual norms, states and the inherited complete component

Each character has norm two as multiplication, mean zero and Haar variance one. The distinct cycles are orthogonal by an unmatched free-link center parity, so B_sum also has mean zero and variance one. Its exact operator norm is 2sqrt(2): the triangle upper bound is attained at identity transports, and continuity on neighborhoods gives the same essential supremum. Thus

    ||B_X||²=4, ||B_sum||²=8,
    B_X Omega=phi_X, B_sum Omega=psi=(phi_X+phi_Y)/sqrt(2),
    K phi_X=(9/2)phi_X, K psi=(9/2)psi.

The reference vectors are normalized. Actual stationary variances tend to one by the state projector-distance bound; they are not asserted equal to one at finite q.

The complete AA1 sixteen-cycle energy-9/2 cube shell and AA2 exterior exclusion apply to both inputs. Every exterior touching face has strictly positive source-specific loading on its distinct complete owners, every disjoint face excites the outside reference, and the six internal faces produce the exact cycle-flip adjacency. This proves a reducing observable-reachable component of every sufficiently large regional averaged operator. It does not enumerate the entire regional energy shell or assert instantaneous invariance.

Let A be the sixteen-cycle adjacency and Q(q) its face-weighted form: a flip across face h has weight q^|anchor(h)| with anchor sum four or five. On this actual component Abar_(q,k)=-Q(q)/96, and Q(1)=A. The source-specific nonzero participating-frequency separation remains at least 1/8 for the entire component and the vacuum. These are exactly the inherited AA2 hypotheses; no new global excited-level gap is fitted.

## Full endpoint measures reconstructed from the frozen inputs

The checker rebuilds the cube, all sixteen six-cycles, all face flips and the complete matrix polynomial A(A²-4I)(A²-12I)=0. It computes powers on the two frozen input vectors. The adjacency moments of orders zero through six are

    single X: 1,0,2,0,16,0,160;
    sum:      1,1,4,8,32,80,320.

The complete spectral measures are:

| Adjacency eigenvalue | B_X weight | B_sum weight |
|---|---:|---:|
| 0 | 2/3 | 1/3 |
| +2 | 1/8 | 3/8 |
| -2 | 1/8 | 1/8 |
| +2sqrt(3) | 1/24 | 1/12+1/(8sqrt(3)) |
| -2sqrt(3) | 1/24 | 1/12-1/(8sqrt(3)) |

For example the single-source squared-energy weights solve w0+w4+w12=1, 4w4+12w12=2 and 16w4+144w12=16, yielding 2/3,1/4,1/12; its odd moments vanish, splitting nonzero pairs equally. For the sum, the squared weights are 1/3,1/2,1/6 and first/third moments determine the signed pair differences. The actual matrix polynomial proves there are no additional spectral values; moments alone without that completeness fact would not identify a measure.

Set theta=z/84. The full stationary connected endpoint scalars, after the correct common reference demodulation, are therefore

    F_X(z)=2/3+(1/4)cos(2theta)+(1/12)cos(2sqrt(3)theta),
    F_sum(z)=1/3+(1/2)cos(2theta)+(1/6)cos(2sqrt(3)theta)
      +i[(1/4)sin(2theta)+(1/(4sqrt(3)))sin(2sqrt(3)theta)]. (AD2.R1)

These are full scalar limits at the original T_q. Equality of F_sum to AA2's rank-observable endpoint follows only after the state-specific averaging proof below; it does not identify the two observables as operators.

The sum gives the nonzero first-order witness

    |F_sum-1-i theta|<=2theta²,
    |F_sum-1|>=theta-2theta²>0.

The single loop has zero first derivative but a nonzero second-order witness. The global real inequality 1-cos x>=x²/2-x⁴/24 and its actual moments give

    1-F_X>=theta²-(2/3)theta⁴>0.                   (AD2.R2)

Thus an elementary face's null slow endpoint does not imply all Wilson multiplication endpoints are null. Their probes reach different reference sectors of the same model.

## Complete finite-q stationary-correlation errors

Use the inherited eight-free-factor support cover C_X union C_Y and its complete-factor collars. The independently reconstructed internally retained face counts are N_1=20,N_2=129,N_3=332. The full positive connected-word tail is D_k(x)=(8/3)_(k+1)x^(k+1)/[(k+1)!(1-x)^(k+4)], x=15z. Every repeated face, external factor and return is retained. For B_X this cover is a legitimate enlargement of its six-link support.

Let tau_q=eta/[8b(q)], s_q=(z/eta)tau_q/(1-q)^3<=3z/2, M_k=N_k/24, dhat_q=tau_q sqrt[b(q²)/96]/[(1-eta)/8] and b_k=16tau_q M_k(1+3zM_k). Source-specific averaging bounds the actual full regional Z on every vector of the reducing sixteen-cycle component and on the vacuum, including the required adjoint vacuum column. The ordered scalar identity for either observable is

    exp(i E T_q/hbar)<Omega,B beta_q^(T_q)(B)Omega>
      =<psi_B,Z B Z*Omega>.

Replacing its right vacuum column costs ||B||b_k, and replacing its left component evolution costs b_k because B Omega=psi_B is normalized. This proves the multiplier-specific errors relative to the exact finite-q matrix scalars

    f_X(q,z)=<e_X,exp[i s_q Q(q)/96]e_X>,
    f_sum(q,z)=<psi,exp[i s_q Q(q)/96]psi>:

    error_X <=24dhat_q+4D_k(15z)+48tau_q M_k(1+3zM_k),
    error_sum <=48dhat_q+8D_k(15z)+64tau_q M_k(1+3zM_k). (AD2.R3)

The sum's averaging coefficient uses 1+2sqrt(2)<4. The state factors 24 and 48 are 6||B||²; both connected means are included. This route compares to the full stationary state directly and introduces no regional stationary replacement. It also retains the original physical clock and every q weight. No uncontrolled ground-energy phase is removed.

The exact rational degree-eight Taylor scalar has remainder at most (s_q||Q(q)||/96)^9/9!, with ||Q(q)||<=6 by its symmetric row sum. The checker adds this arithmetic remainder separately to (AD2.R3). It never rounds a value near one to infer a tiny real shift. Taking q to one first at fixed k, then increasing k, proves (AD2.R1). The finite-q-to-limit comparison adds at most

    s_q(1-q^5)/16 + |s_q-8z/7|/16,                  (AD2.R4)

independently of the normalized source. This uses only bounded finite matrices on the actual reached component.

At eta=1/2,z=10^-6,q=1-10^-12,k=3, the checker certifies radii below 10^-17 for each exact rational scalar center. The original physical time is 2*10^30 hbar/alpha. The single-loop real shift is about -1.4172*10^-16, and the sum imaginary shift is about 1.19048*10^-8. Subtracting each complete certified radius from the corresponding center displacement remains strictly positive, giving actual finite-q nonzero witnesses as well as limiting ones. These are mathematical enclosures, not measurements or practical clocks.

## Held-out controls and limits of identification

The common vacuum-created vector is insufficient to replace multiplication by a rank operator at finite q. Actual Haar fourth moments give

    ||B_X² Omega||²=2,
    ||B_sum² Omega||²=5/2.

For the second, E chi_X^4=E chi_Y^4=2, E chi_X²chi_Y²=1 by sequential integration over exclusive edges, and both odd mixed fourth terms vanish by unmatched parity. The rank operator's squared action on Omega is Omega and has norm squared one. The missing excited components therefore have squared norms one and 3/2 respectively. Rank-norm error budgets would undercount both state and spatial terms even though F_sum happens to agree in the limit.

A single phase fitted to F_sum's slope predicts adjacency second moment one, while the held-out actual value is four. The exact two-cycle compression makes the same wrong prediction on their coherent sum; the missing outward cycles are necessary. A constant fitted to B_X's zero slope fails its held-out second moment two. AD1's elementary face retains the null endpoint and distinguishes reference sectors. These checks reject specific wrong substitutions, not every possible model with the same finite observations. No physical clock or action parameter is refitted using the held-out data.

The result establishes two specified Wilson multiplication scalar endpoints, complete finite-q bounds and explicit failed model substitutions. It provides no universal observable reconstruction, homogeneous inverse, global q=1 generator, experimental mass calibration or continuum construction. Scientific priority remains unverified.
