# AC1 forward: an exact 293-state physical enrichment and its complete remainder

Independent forward derivation before reading the current reverse solution. Newton's reconstruction keeps the actual identifying Gram and electric operator; Tesla's loading check retains the complete omitted map. No historical analogy is a physical premise. The graph is exactly the open 18-vertex, 33-link, 20-face graph and L=K+lambda(20-S), S=sum_p W_p, 0<=lambda<=1/100. Time sigma=alpha t/hbar and positive physical scales remain unchanged.

## Actual vectors, Gram and electric completeness

Start with P21=span{Omega,phi_p=2W_p}. Adjoin all residual channels occurring in S phi_p, and close under K. For a pair sharing an edge, let X_pq=W_p W_q, X_s its shared-edge Haar projection and X_t=X_pq-X_s. The actual X2 Clebsch-Gordan/Haar calculation gives ||X_s||²=1/64 and ||X_t||²=3/64, with electric energies 9/2 and 13/2. These are the singlet and triplet of that link, not two arbitrary fitted vectors.

Use the following rational-coordinate basis:

| Vectors | Count | Norm squared | K eigenvalue |
|---|---:|---:|---:|
| Omega | 1 | 1 | 0 |
| phi_p | 20 | 1 | 3 |
| chi_p=4W_p²-1 | 20 | 1 | 8 |
| d_pq=4W_p W_q, no shared edge | 128 | 1 | 6 |
| s_pq=8X_s, shared edge | 62 | 1 | 9/2 |
| t_pq=8X_t, shared edge | 62 | 3 | 13/2 |

The dimension is 293. Distinct two-face parity masks are distinct and nonempty; none equals a single-face mask. They give orthogonality between distinct pairs and the old sector. Singlet/triplet pieces are orthogonal electric eigenspaces. Spin-one characters have distinct nonzero representation supports and are orthogonal to each other and all other listed vectors. Thus the exact Gram is diagonal, with 62 entries equal to three and all others one; no dependence or zero vector is omitted.

All vectors are smooth invariant polynomials on the actual full group space, hence lie in the common invariant core of K and L. Their span reduces K because it is spanned by K eigenvectors. This does not exhaust every intertwiner in the ambient electric shells. For pairs meeting only at a vertex, other degree-four intertwiners can share the energy six; the chosen product eigenvector is sufficient for a reducing subspace, and all unretained intertwiners stay in Q. For shared edges both fusion channels are included. No assertion of a complete energy cutoff is made for this P293.

## The entire retained matrix is exact

The actual link-center transformation of X2 sends every W_p to -W_p. Omega and all 272 new vectors are even; the twenty phi_p are odd. S is odd, so all within-parity retained matrix elements vanish. The complete remaining columns follow from

    S Omega=(1/2)sum_p phi_p,
    S phi_p=(1/2)Omega+(1/2)chi_p
      +(1/2)sum_(q disjoint edges from p) d_pq
      +(1/4)sum_(q sharing edge with p)(s_pq+t_pq).  (AC1.1)

Metric self-adjointness gives every even-to-odd entry. In particular S t_pq has retained coefficients 3/4 on each of phi_p,phi_q. All other reversals use equal Gram weights. This constructs all 293² entries exactly over the rationals in the stated metric, including every zero. The checker saves a sparse coordinate matrix, diagonal Gram, electric eigenvalues and actual face/pair labels. In an orthonormal basis the triplet entries are sqrt(3)/4 instead. These are equivalent coordinate descriptions of the same operator.

For every retained input, including every new vector, the actual full omitted map is

    B=Q293 L P293=-lambda Q293 S P293,
    B P21=0,  ||B||<=20lambda.                       (AC1.2)

The first identity uses complete K reduction; the zero old columns use (AC1.1). The second bound uses the full multiplication norm ||S||<=20 and orthogonal projections in the actual Gram norm. This is a rigorous full remainder on all 272 potentially nonzero new columns. It is not an evaluation of each cubic omitted amplitude, nor an estimate from just one selected channel. At lambda=0 the entire omitted map vanishes exactly. The full map bound is worse than X2's sharp old bound sqrt(39)lambda/2; enrichment does not automatically improve a worst-input bound.

There are 293 stored basis labels, 62 unnormalized triplet weights and 1088 directed nonzero magnetic entries. Dense storage would use 85,849 entries; the exact sparse construction costs O(number of face pairs). This includes the matrix construction, not the cost of certified exponentiation of the enlarged matrix. Such a scalar/matrix evaluator remains an implementation step; this report proves approximation bounds for its exact semigroup and supplies its exact matrix.

## Ground accuracy improves even though the full omitted upper bound worsens

Let f,mu21,rho21 be the inherited normalized 21-state Ritz ground, energy and full residual. In P293 its residual is entirely retained, with norm rho21; all other compressed eigenvalues are >=3 because L>=K and the actual K gap is three. Let f293,mu293 be the new normalized simple Ritz ground, with phases chosen to have nonnegative overlap. Min-max gives 0<=mu293<=mu21<=c=20lambda<3. Spectral expansion of f in the new compression gives

    sin angle(f,f293)<=rho21/(3-mu21).

Since Bf=0 exactly, decomposing f293 along f shows

    rho293:=||(L-mu293)f293||
      <=20lambda rho21/(3-mu21).                   (AC1.3)

This is a full-Hilbert residual, not a retained one. Applying the same proved actual spectral-measure argument as X2 gives

    0<=mu293-epsilon<=rho293²/(3-mu293),
    ||G-G293||<=rho293/(3-mu293).                   (AC1.4)

Uniform rational envelopes on 0<=lambda<=Lambda<=1/100 are g=3-20Lambda, r21=7Lambda²/3 (since sqrt(195)<14), p21=r21/g, r293=20Lambda p21, p293=r293/g and d293=r293²/g. At the cap these are

    p21<=1/12000, r293<=1/60000,
    p293<=1/168000, d293<=1/10080000000.

Thus the projection error is below 5.953e-6 and new ground-energy error below 9.921e-11 in alpha units. These are certified upper bounds, not numerically observed errors. No exact ground energy is printed because the new matrix has not been diagonally evaluated here.

## Same preparation class, clock and true denominator

For normalized retained x with ||x-Omega||<=eta=1/100, the old preparation class embeds in the new one. Let E=exp[-sigma(L-epsilon)], E293=exp[-sigma(A293-mu293)]P293. From the old exact f and the angle bound, ||f293-f||<=sqrt(2)p21<=3p21/2. Therefore define

    a=1-5Lambda²/9-3p21/2-eta,
    b=3Lambda/4+3p21/2+eta,
    d0=a-p293>0.                                  (AC1.5)

Here |<f293,x>|>=a, ||(I-G293)x||<=b and ||E(sigma)x||>=d0. The last is the true full-state denominator. The vacuum case uses eta=0. These estimates deliberately retain a little slack so all certification is rational.

Duhamel on the actual common domain and the retained spectral decomposition gives the early absolute error

    V(t)=(r293+d293)t+(20Lambda)b(1-exp(-g t))/g.

The complete full/Ritz spectral decomposition independently gives the late error

    J(t)=p293+(2b+p293)exp(-g t).

For a join t0=2, V increases and J decreases, so every sigma>=0 obeys

    ||E293(sigma)x-E(sigma)x||/||E(sigma)x||
      <=max(V(2),J(2))/d0.                         (AC1.6)

At Lambda=1/100, exact rational bounds 1-exp(-2g)<=1 and exp(-2g)<1/250 yield a relative bound below 0.0014 for the same 0.01 vacuum ball, and below 0.00059 for the vacuum. This is weaker than Z2's sharper 21-state all-time guarantee, despite improved ground bounds. It is valid for the same physical clock, same input/target and true denominator. A norm-close preparation outside P293 needs its own initial truncation cost; it is not admitted here. At sigma=0 the exact error is zero; at lambda=0 the exact semigroups agree on every retained input. Those identities supersede the coarse nonzero spectral-tail bounds.

## Verification and remaining work

The checker independently reconstructs actual edges, faces, central parity, every pair, the positive Gram, complete K diagonal and exact magnetic matrix. It checks metric self-adjointness, all old-column closure coefficients, the shared-triplet metric correction and the source's complete electric weights. Rational certificates verify the continuous-coupling envelopes and all-time denominator. Controls reject treating triplets as norm-one in rational coordinates, dropping shared singlets, claiming a complete ambient shell and substituting the new bound for an exact omitted norm. Checks use explicit exceptions under normal and optimized Python. SHA source inventories bind the inherited reports.

Accepted scope: an actual 293-state compression with complete electric action, exact retained magnetic matrix, rigorous all-input omitted remainder and improved ground certificates. Limited scope: the entire omitted map is bounded rather than expanded in cubic intertwiners; the sharper same-preparation all-time target is not improved, and no certified enlarged exponential evaluator is delivered in this loop. No graph-size uniformity, real-time relative theorem, homogeneous inverse, canonical endpoint or continuum result follows. Scientific priority is unverified.
