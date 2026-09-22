# AF2 reverse: a certified all-time piecewise 293-state evaluator

Independent reverse implementation under AF2, without current forward AF2 access. The fixed coupling is lambda=1/100 and the input class is exactly normalized x in the original P21 with ||x-Omega||<=0.01. The evaluator covers every sigma>=0 with an early branch sigma<=8 and late branch sigma>8. Its uniform retained-vector numerical error is below 1e-8, separately from the actual full-space physical approximation error. Adding the AC2 physical budget preserves a full true-output-relative bound below 0.000037.

The code executes vacuum and an exactly normalized rational nonvacuum at sigma=0,1,13/5,8,9 and 10^6. Every demonstration exports all 293 rational coordinates in the actual triplet-weighted basis. The analytic estimates establish continuous time and input coverage; the exported table alone does not.

## Exact matrix, minimum and a much sharper projector

All 293 basis records and 1088 sparse magnetic entries are reconstructed and compared with AC1 in its true diagonal Gram, with 62 triplet weights three and every other weight one. Let A=P293 L P293. Actual positivity gives A>=0, its second eigenvalue is at least three, its minimum mu is at most 1/5 by the vacuum trial, and A<=42/5. These full operator facts isolate the minimum before applying residual arguments.

Set T=I-A/9. It is positive and has the same eigenvectors. Its ground eigenvalue is at least 44/45, while every other eigenvalue is at most 2/3. The vacuum Rayleigh value is 1/5, so its squared ground overlap is at least 1-(1/5)/3=14/15. Consequently the power vector

    w=T^64 Omega

has angle to the ground bounded by 2(15/22)^64<1e-10. This independently shows that its small residual identifies the ground, not another root. The implementation computes w through exact integer multiplication: 3600T has integer entries. Its common denominator cancels from every Rayleigh quotient and projector, so no normalized square root is needed.

From the integer coordinates n representing w, compute exactly in the true metric

    a=<n,An>/<n,n>, rho²=||An||²/<n,n>-a².

With a<3 and the already isolated minimum, the actual spectral measure gives

    a-rho²/(3-a)<=mu<=a,
    ||P_n-G293||<=rho/(3-a),
    P_n x=n <n,x>/<n,n>.                           (AF2.R1)

The checker encloses rho/(3-a) by an outward integer-square rational. It rounds the midpoint of the minimum interval to a rational m_hat with denominator 10^24 and records the maximum center uncertainty u. Both the interval and projector are computed from all retained components, including their nontrivial Gram weights.

## Early branch: all sigma in [0,8]

For C=A-m_hat I evaluate the degree-240 polynomial

    P240(sigma)x=sum_(j=0)^240 (-sigma C)^j x/j!.

Since ||C||<=9 and C>=-1/5, the integral Taylor remainder is uniformly

    ||exp(-sigma C)-P240(sigma)||
      <=16*72^241/241!                             (AF2.R2)

on this whole interval. The harmless factor16 bounds exp(8/5), for example by splitting it into four factors and using exp(2/5)<=1/(1-2/5). This is an operator-norm bound in the true Hilbert metric, hence applies to every normalized admitted input, not only the computed vacuum.

The retained ground-center uncertainty costs at most

    exp(8u)-1<=8u/(1-8u),                          (AF2.R3)

with 8u<1 explicitly checked. The implementation uses exact integer Horner recurrence for rational sigma and rational input coefficients; there is no accumulated floating arithmetic. The final vector is rounded coordinatewise to a 10^-30 grid, at physical norm cost at most 11*10^-30 because the Gram weights sum to417. At sigma=0 the algorithm returns its input exactly, bypassing grid rounding.

Equations (AF2.R2)-(AF2.R3) and export error give an explicit rational early numerical budget e_early<1e-8. They establish the polynomial approximation as a linear map on all real or complex inputs. The executable interface and demonstrations use exact rational inputs/times; input measurement or representation uncertainty is not included in this exact-input theorem.

## Late branch: every sigma>8 without secular center error

Return P_n x, rounded with the same metric export allowance. The true retained own-ground-centered semigroup has excited gap at least 3-mu>=14/5. Thus

    ||exp[-sigma(A-mu)]x-P_n x||
      <=rho/(3-a)+exp[-(14/5)sigma].               (AF2.R4)

A positive rational Taylor sum certifies exp(112/5)>10^9, so the full late excited tail is less than 10^-9 uniformly for sigma>=8. Add coordinate export error. The resulting late numerical budget e_late<1e-8 has no factor growing with sigma: a rounded center is not exponentiated forever. The maximum of the two branch budgets is the uniform numerical allowance e_num, explicitly below the contract's 10^-7 target and below 10^-8.

Both estimates are valid at sigma=8. The checker evaluates the early branch and the projector there, and checks their vector difference against the sum of the two certified branch errors. The branch selection uses the polynomial at eight and the projector strictly above eight. A harmless small output jump is allowed by the proved uniform error; continuity of the underlying exact heat is unchanged.

## Same physical class and full-space certificate

The nonvacuum demonstration is the exact normalized rational vector

    x=(159999/160001)Omega+(800/160001)phi_0.

Its norm is one, and its squared distance from Omega is 4/160001<10^-4, placing it inside the original radius-0.01 P21 class. No newly retained component is inserted into the preparation. The code verifies both statements by rational arithmetic.

The sharper inherited forward AC2 bound has uniform physical absolute numerator

    e_phys=457097/12600000000,
    ||E_full(sigma)x||>=D=7127/7200.

That result includes the entire new omitted map, delayed loading, outside return and the actual full-versus-retained ground-center difference. It is inherited with its direction attribution; numerical centering uncertainty u above is a different cost. Therefore every returned vector from either branch obeys

    ||v_returned-E_full(sigma)x||/||E_full(sigma)x||
      <=(e_phys+e_num)/D <0.000037.                (AF2.R5)

The denominator is the true full output, and sigma remains alpha t/hbar. No clock, normalization or target is changed. Physical and numerical terms remain separately inspectable. The all-time numerical implementation is proved here only at lambda=1/100; AC2's broader analytic coupling interval does not make the executed evaluator uniform in lambda.

## Execution and limits

The standard-library program produces all twelve requested time/input vectors, exact ground-projector sufficient data, numerical budgets and source hashes. Optional `--sigma RATIONAL` evaluates another time, with vacuum input by default; `--input-vector PATH` accepts 293 rational strings and enforces exact normalization, original P21 support and the radius-0.01 condition before evaluation. Integer intermediates and rational endpoints are authoritative; display floats are optional summaries. The zero-time exact-input control, zero-coupling vacuum identity, triplet metric control and both-branch join check are explicit exceptions that remain active under optimized Python. Normal and optimized executions must agree byte for byte.

Newton's reconstruction identifies the ground before interpolation or exponentiation; Tesla's loading audit retains all physical channels and the late spectral tail. This completes the authorized tenth investigation. There is no subsequent physics execution in this submission. The evaluator supplies no all-input relative theorem beyond the admitted preparation class, no real-time result, large-volume uniformity, homogeneous inverse, physical mass calibration or continuum construction. Scientific priority is unverified.
