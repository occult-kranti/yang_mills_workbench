# C2: a common action variable does not determine the joint observable

This sixth scientific loop retains C1's actual four-cube graph and four signed three-edge paths around the central link. It uses the same three research roles. No extra physical field, Hamiltonian coupling or new scientific loop is introduced.

## A valid common variable and its missing information

For a unit central quaternion q and four boundary holonomies H_i, put a_i=(H_i0,-H_ivec). The normalized fundamental face character is x_i=q dot a_i. For four individual Euclidean coefficients kappa_i, the central action is q dot b, where b=sum_i kappa_i a_i. These dimensionless Euclidean coefficients are separate from the physical Hamiltonian energy scale alpha used by the earlier spectral bounds.

A Haar-preserving four-dimensional rotation can align a nonzero b with a coordinate axis. It must also rotate the a_i in the observable. If b=0, the action is zero and the unrotated Haar branch applies; dividing by its norm would be invalid. This implementation explicitly accepts scalar-axis b and rejects an off-axis b instead of silently discarding its directions. For the certified Taylor remainder it also requires |b0|<N+2 and an integer degree 0<=N<=16.

Compare the accepted tetrahedral boundary T with the commuting boundary C=(I,I,i,-i). With all four coefficients kappa, both give b=(2kappa,0,0,0). Their conditional partition functions are consequently identical:

    Z = E_Haar exp(2 kappa q0).

The same four-face observable functional O=product_i chi_2(UH_i)/81 gives different functions of the central link on the two boundaries. It is not correct to claim the two observable integrands coincide. The tetrahedral direction Gram matrix is the identity, whereas the commuting data have repeated and opposite directions. In particular,

    O_C = (4q0^2-1)^2 (4q1^2-1)^2 / 81 >= 0.

Both boundary sets are realized on the actual lattice: each path has a distinct outer vertical link, to which H_i or H_i inverse is assigned according to its orientation. The complete link assignments are retained in every certificate. A nontrivial central-link sample checks the actual face word U H_i and the common action. The other sixteen faces omit the central edge, so their action terms cancel from this normalized conditional expectation. They still affect the surrounding marginal in a bulk integral.

## Exact polynomial integration and complete error bounds

Every factor 4(q dot a_i)^2-1 is expanded as a polynomial in the four quaternion coordinates before the factors are multiplied. Division by 81 is included in the polynomial. For uniform S3 Haar measure, odd powers have zero mean. If powers are 2a_0,...,2a_3 with A=sum a_i, the normalized even moment is

    E product_i q_i^(2a_i)
      = [product_i (2a_i)!] / [4^A (A+1)! product_i a_i!].

This follows from normalized independent Gaussian coordinates, whose squared fractions have the Dirichlet distribution with all parameters 1/2. The numerical implementation uses the exact factorial ratio, not sampled spherical quadrature. The independent reviewer uses conditional spatial angular integration followed by scalar semicircle moments; it does not import this producer arithmetic.

For degree N, both series retain every term through that degree:

    A_N = sum_(n=0)^N b0^n E[O q0^n]/n!,
    Z_N = sum_(n=0)^N b0^n E[q0^n]/n!.

For M=|b0| and N+2>M, the complete exponential tail obeys

    R_N = M^(N+1)/(N+1)! / (1-M/(N+2)).

Indeed, |q0|<=1, and each subsequent absolute Taylor term has ratio at most M/(N+2). Each normalized adjoint factor is in [-1/3,1], so |O|<=1. Thus |A-A_N|<=R_N and |Z-Z_N|<=R_N. The difference of two observables is bounded in absolute value by two, giving a numerator-difference tail 2R_N. No extra perturbation parameter is attached to the observable insertions.

Jensen gives Z>=1 because the mean action is zero. The certified denominator is [max(1,Z_N-R_N),Z_N+R_N]. The numerator interval is [A_N-R_N,A_N+R_N]. All four quotient endpoints are compared, preserving signs when the numerator is negative or crosses zero. The contrast C-T is bounded using its numerator difference and the same positive denominator, rather than pretending that the two normalizations are unrelated. Exact rational interval endpoints are authoritative.

## Results and actual failed precision levels

At kappa=0 the intervals collapse exactly:

    E[O_T] = -1/405,
    E[O_C] = 13/1215,
    E[O_C]-E[O_T] = 16/1215.

At the primary kappa=1/8 fixture, the finite central action is q0/4. The final degree-16 enclosures give approximately

    E[O_T] = -0.0024691143942351377,
    E[O_C] =  0.01073813525633129,
    E[O_C]-E[O_T] = 0.013207249650566428.

The contrast enclosure width is approximately 6.630033793875718 times 10^-25, below the required 10^-12. Degrees 0,4,8 remain insufficient; degrees 12 and 16 pass all three sign and width criteria. The full coefficient arrays, both numerator and denominator tails, every refinement and every failed status are retained. A coarse truncation is not promoted to success because its midpoint happens to look accurate.

The tetrahedral single-factor conditional mean is exactly zero for every scalar-axis weight. At fixed q0=t, rotational symmetry gives E[(q dot a_i)^2|t]=a_i0^2 t^2 + |a_ivec|^2(1-t^2)/3. Each tetrahedral boundary has a_i0^2=1/4 and |a_ivec|^2=3/4, so this conditional second moment is 1/4. The constant and t^2 coefficients of each normalized adjoint mean are therefore both zero; the code derives those coefficients. Their vanishing does not force the joint mean to vanish.

The deliberately wrong action-only cache stores T's joint result under b and reuses it for C. It has the correct action and partition, yet its predicted negative interval is disjoint from C's certified positive interval. This is a concrete failure of an action-variable-only observable closure. It does not refute the legitimate coordinate reduction itself.

## Signed, zero-vector and implementation controls

The fixed extra fixtures include both boundaries at kappa=0,-1/8,1/16, and the commuting boundary with individual coefficients (1/8,-1/8,1/8,1/8). In the last case not all coefficients vanish, but b=0; the code returns the exact Haar value 13/1215 with partition one and tail zero. The negative common coupling gives the same even-observable integrals as positive coupling. Every individual coefficient and boundary is retained; a missing fixture cannot pass collection replay.

Validation precedes all public cache entry points, including nested Boolean aliases, negative powers, malformed coordinate tuples, nonunit quaternions and invalid Taylor degrees. Observable cache values are immutable tuples. Controls reject omitted partition remainders, a missing factor 81, missing boundary realization, an off-axis action and deleted coarse failures. Normal and optimized runs must reproduce identical evidence bytes.

The independent reviewer found a concrete helper defect before acceptance: direct calls to integrate accepted Boolean False as scalar power zero, and a negative scalar power could be hidden by an existing positive monomial exponent. Certified fixture inputs already passed the stricter degree validation, so the displayed scientific coefficients were unaffected. The old source, its forty-check result and exact reproductions are retained in history. The corrected helper validates its scalar index and polynomial structure before arithmetic; three held-out controls cover these cases.

Run `python -B check.py --output ../c2-output` from the source directory. The standalone package copies the frozen C1 geometry locally and pins its source hash; no import depends on another scratch path. Outputs include collection.json, refinement.csv, coupling.csv, results.json and a hash manifest.

This establishes a finite conditional integral and an obstruction to identifying joint observables from their action variable alone. It does not compute the full bulk contraction, a dense volume-uniform Hamiltonian gap, or the continuum Yang-Mills mass gap. The six requested scientific loops end here; further goals require an advisor decision based on the accepted results and remaining premises.
