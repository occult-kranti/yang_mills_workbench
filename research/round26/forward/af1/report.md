# AF1 forward: a certified293-component heat vector at the frozen point

Independent first-loop evaluation of the actual AC compression, before reading reverse AF1. The point is exactly lambda=1/100, sigma=alpha t/hbar=1 and input Omega. The output contains all293 rational coordinates in the actual basis, including its nontrivial triplet Gram. A retained ground-center enclosure, polynomial error, exported-coordinate rounding and complete physical error are all charged separately.

## Actual sparse operator and a proved retained minimum

Use the exact AC1 basis and metric Gdiag:231 entries one and62 entries three. Every magnetic entry is reconstructed from the named product/fusion branch and checked, including the metric reverse coefficient. There are1088 directed nonzero entries, all other entries are zero, K is diagonal and the actual compression is A=K+(1/100)(20-S). Thus A is self-adjoint in this Gram. Positivity of20-S gives A>=K, so the second eigenvalue is at least3; the vacuum trial gives its simple minimum mu<=1/5. This spectral isolation is proved before using a residual.

To enclose mu more tightly, take an explicit rational trial vector v: vacuum coefficient one, every face coefficient lambda/6, and each new component i set to lambda(NS v_old)_i/E_i. This is a single residual correction using the complete new electric inverse. It does not solve the eigenproblem by assumption. The checker calculates exactly

    a=<v,Av>_G/<v,v>_G,
    rho²=<Av,Av>_G/<v,v>_G-a².

Because a<3 and all eigenvalues other than mu are at least3, the spectral measure gives

    a-rho²/(3-a)<=mu<=a.                           (AF1.1)

Indeed <(A-mu)(A-3)>_v>=0 implies rho²>=(a-mu)(3-a). This is a proof of the lowest eigenvalue enclosure, not a floating Ritz residual without an isolation check. The exact rational endpoints are saved. Their midpoint is rounded to a denominator10^24; the maximum distance from that rounded muhat to either endpoint is the certified center radius d_mu. The executed d_mu is below10^-11. No source-file eigenvalue or machine-float diagonalizer is trusted.

## Executed heat action and arithmetic certificate

For H=A-muhat I, the actual metric operator norm is at most9: K<=8P and ||lambda(20-S)||<=2/5, while0<muhat<1/5. Let p_100(H)=sum_(j=0)^100(-H)^j/j!. The checker evaluates its action on Omega exactly using integer Horner recursion after putting every matrix coefficient over10^24. It runs all293 coordinates and all1088 sparse entries at every stage; there is no hidden symmetry compression or discarded channel.

The finite-dimensional spectral theorem and the exponential Taylor remainder give

    ||exp(-H)Omega-p_100(H)Omega||_G
      <=2^14*9^101/101! <10^-55.                  (AF1.2)

Here exp(9)<2^14 follows from the rationally certified exp(2/3)<2. Exact intermediate integers make accumulated floating roundoff zero. The final coordinates are rounded independently to the nearest multiple of10^-50. Since the sum of Gram weights is417<21², their combined metric rounding error is at most21/(2*10^50). Every coordinate is exported as an integer numerator with a shared denominator10^50; decimal float values are separately labeled display-only.

The actual desired retained center is mu, not muhat. At sigma=1 its additional error is bounded by

    |exp(muhat-mu)-1|<=d_mu/(1-d_mu).             (AF1.3)

This uses ||exp[-(A-mu)]Omega||<=1 and d_mu<1. Adding(AF1.2), (AF1.3) and the coordinate rounding certifies the complete retained vector. At zero time the evaluator's mathematical target is exactly Omega; at lambda=0 the vacuum is an exact zero-energy vector and its centered heat stays Omega. These are distinct exact controls, not claims inferred from the frozen nonzero point.

## Full-space error and true denominator

The retained vector still differs from the actual full Gauss-invariant heat state. AC2's state-sensitive theorem applies at this exact point with eta=0. Use g=14/5, q+=61/8000, Cbar=1/32, Mbar=1/5 and delta+=1/10080000000. Its complete physical omission plus actual full/new ground-center error is bounded by

    e_phys=delta+ +(1/5)(1/32)
       [(61/8000)/(9/2)+(61/8000)/((14/5)(9/2))].

Every newly retained input is still covered by the full B envelope. B P21=0 is used only through AC2's proved gradual-loading estimate; it does not imply closed293-state dynamics. The true full output denominator is at least

    D=1-5lambda²/9-1/12000 >0.                   (AF1.4)

For the exported vector v_export, adding the center, Taylor and rounding errors to e_phys and dividing by D gives

    ||v_export-exp[-(L-epsilon)]Omega||/||exp[-(L-epsilon)]Omega||
       <0.000015.                               (AF1.5)

The exact rational total is in results.json. The reported physical time is hbar/alpha; no rate is fitted. The center radius in(AF1.3) is an arithmetic/model-evaluation uncertainty for the retained matrix. The difference mu-epsilon in e_phys is the actual physical omitted-channel centering error; they are not merged or double-substituted.

## What has and has not been computed

This loop executes one actual293-state retained vector and a full-Hilbert error certificate at the frozen point. It does not execute an all-time vector table or a uniform algorithm over the coupling interval. AC2's separately established all-time mathematical bound remains intact. No orthonormal-coordinate claim is made for unnormalized triplets, and a float rendering of a coefficient carries no independent certification.

Source inventories bind the frozen matrix, proofs and checker. All gates are explicit exceptions and survive optimized Python. Normal and optimized replays must produce identical coordinates and certificates. Newton's reconstruction motivates certifying the spectral minimum before centering; Tesla's loading discipline keeps every new input and the full omitted map. This finite-graph heat computation supplies no homogeneous inverse, physical mass calibration or continuum construction. Scientific priority is unverified.
