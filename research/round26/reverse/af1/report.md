# AF1 reverse: an actual certified 293-coordinate heat vector

Independent reverse computation, without current forward AF1 access. This executes the frozen point lambda=1/100, sigma=1, input Omega, for the actual 293-state compression of the 18-vertex, 33-link, 20-face Gauss-invariant graph. The output contains all 293 coordinates in the exact rational AC1 basis, a certified minimum-energy interval, and separate physical, ground-center, polynomial and export errors. Their combined true-output-relative error is below 0.000014. This is a point computation; earlier continuous-time certificates do not make this one exported vector an all-time evaluator.

## Actual metric matrix and the minimum, not an arbitrary Ritz root

The checker independently rebuilds every graph face and pair, all rational Gram weights and energies, and all 1088 sparse magnetic entries; it compares them to the frozen forward-origin AC1 matrix. Triplet basis vectors have squared norm three, so every vector norm and transpose uses that diagonal metric. Let A=P293 L P293, with L=K+lambda(20-S). All actual retained vectors are physical smooth polynomials, and its common core and K reduction are inherited. Since 0<=L and the physical electric gap is three, A>=0 and its second eigenvalue is at least three. The vacuum trial gives its minimum mu<=1/5.

Use the actual old 21-state Ritz ground f21, whose exact eigenvalue is

    m=1/5-[sqrt(9+20/10000)-3]/2.

Its full A residual is entirely inside P293 and has norm at most r21=7/30000. This inherited residual includes every former omitted channel. The spectral measure of f21 under A has every eigenvalue other than mu at least three. Thus, by taking the expectation of (A-mu)(A-3)>=0 on its spectrum,

    0<=m-mu<=r21²/(3-m)<=r21²/(14/5)=:d21.      (AF1.R1)

This encloses the actual minimum using the actual second-eigenvalue separation, not a floating residual near an unidentified root. The checker encloses the square root by integer-square inequalities at denominator 10^30, giving a rational interval [m_lo-d21,m_hi] containing mu. Its width is below 2e-8. Choose the midpoint rounded to denominator 10^12 as m_hat and record u=max(|m_hat-mu_lo|,|m_hat-mu_hi|)<1e-8. The interval and rounding displacement are both retained; no exact new ground value is claimed.

## Executed heat action and all arithmetic

The target retained vector is v293=exp[-(A-mu)]Omega. The actual computed center uses C=A-m_hat I and the degree-80 polynomial

    v80=sum_(j=0)^80 (-C)^j Omega/j!.           (AF1.R2)

Every matrix-vector operation is exact rational arithmetic with the complete sparse matrix. On this retained space K<=8 and ||S||<=20, so 0<=A<=8.4; with 0<m_hat<0.2, ||C||<=9 and C>=-0.2. The integral Taylor remainder therefore obeys

    ||exp(-C)Omega-v80||<=exp(0.2)9^81/81!<2*9^81/81!. (AF1.R3)

No floating Krylov stopping criterion is used. The bound follows from the operator exponential's integral remainder and self-adjoint spectral bounds, not from a sampled eigenvalue maximum. Exact rational powers avoid cancellation-related roundoff even though intermediate terms alternate.

Each of the 293 rational coefficients is rounded to the nearest multiple of 10^-30 for export. The sum of all Gram weights is 417, so its physical vector error is at most sqrt(417)/(2*10^30)<11/10^30. The output decimal strings are exact rational coordinates; optional floating summaries are labeled display-only. The Taylor and export errors are stored separately.

The uncertain own-ground center is also separate. Since ||v293||<=1,

    ||exp[-(A-m_hat)]Omega-v293||
      <=exp(u)-1<=u/(1-u).                       (AF1.R4)

Here u<1e-8, so this dominates the deliberately tiny polynomial/export errors but remains much smaller than physical omitted-channel uncertainty. The exported vector is not normalized after computation; the true heat output norm need not equal one.

## Transfer to the true full heat at the original point

Let vfull=exp[-(L-epsilon)]Omega with epsilon the actual full ground. The AC2 full-system Duhamel bound retains every newly omitted column, the exact old-input cancellation and the difference mu-epsilon. For the vacuum at sigma=1, the reverse delayed-leakage formula yields

    ||vfull-v293||<=d293+(130/9)Lambda²(4Lambda/3)
                      [1-(1-exp(-3))/3],
    Lambda=1/100, d293=1/10080000000.

A positive Taylor sum proves exp(3)>20, hence an exact rational physical upper bound is

    P=d293+(130/9)Lambda²(4Lambda/3)(41/60).      (AF1.R5)

It includes the full physical leakage and true-versus-retained ground-centering cost. The independent true denominator from the old full-ground certificate is

    ||vfull||>=1-5Lambda²/9-p21=7199/7200,
    p21=1/12000.                                 (AF1.R6)

If v_export is the supplied rational vector, the complete point certificate is

    ||vfull-v_export||/||vfull||
      <=[P+u/(1-u)+2*9^81/81!+11/10^30]/(7199/7200)
      <0.000014.                                (AF1.R7)

This is a bound for the same full input and same physical heat time t=hbar/alpha. No normalization, denominator replacement, fitted rate or source-class change is made. The interval-center approximation is not folded into physical leakage or vice versa.

## Controls and interpretation

The executable checks the complete metric self-adjoint matrix, its original vacuum column, the integer-square enclosure, positivity and spectral minimum separation, the exact rational Taylor and coordinate-export bounds, and (AF1.R7). At sigma=0 the evaluated action returns exactly Omega with zero point error; at lambda=0 the vacuum is the exact zero-energy eigenvector and the evaluated action again returns Omega. Those identities bypass the generic coarse upper budgets. Applying a Euclidean norm to the rational triplet coordinates is explicitly rejected.

Newton's reconstruction requires identifying the minimum before centering; Tesla's loading test keeps the full omitted envelope. The output is a useful computed finite-graph heat vector with a certified error relative to the full physical Hilbert-space evolution. It is not a computed full ground wavefunction, an all-time exported trajectory, a large-volume solver, real-time certificate, homogeneous model result, physical mass calibration or continuum construction. Scientific priority remains unverified.
