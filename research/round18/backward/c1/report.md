# Independent C1 review: complete central Gram data

The complete joint Gram matrix of `(b,a1,a2,a3,a4)` is sufficient for the declared central-link observable and action. This is an ordinary mathematical implication, supported here by exact independent arithmetic; it is not a formal proof-assistant certificate. The result does not identify a mass gap or transform a surrounding-link measure.

For unit vectors `a_i` in real four-dimensional Euclidean space and `b=sum_i kappa_i a_i`, set

`O(q)=product_i(4(q dot a_i)^2-1)/81`, with normalized uniform `q` on `S^3`.

Suppose two complete vector tuples have equal Gram matrices. The linear map sending each source vector to its paired target is well-defined: a source linear relation has squared norm zero as computed from the Gram, and the same is therefore true of its target relation. This map preserves inner products on the two spans. Complete orthonormal bases of their orthogonal complements to extend it to an element of `O(4)`. This argument permits all ranks, including one, two and zero action vectors; it never inverts a singular Gram. Uniform sphere measure is invariant under this orthogonal transformation, including reflections. Therefore the untruncated numerator `E[O exp(t q dot b)]` and partition `E[exp(t q dot b)]` are equal for every finite real `t`. The positive partition also gives equality of the corresponding normalized expectations.

The statement uses the complete declared tuple and its ordering. It does not assert that complete Gram is minimal or necessary for equality of this single observable, nor that an orthogonal transformation is an `SU(2)` group automorphism. It does not cover an extra orientation-sensitive insertion or justify transforming another link's conditional measure without checking that measure.

## Independent arithmetic and admissibility

The forward implementation uses a Gram contraction recurrence and semidefinite Schur elimination. Our `coordinates.py` instead multiplies actual four-coordinate polynomials. For a coordinate monomial with an odd exponent its integral is zero. With exponents `2m_i`, `M=sum m_i`, the exact integral is

`E product q_i^(2m_i) = product (2m_i)! / (4^M product m_i! (M+1)!)`.

This follows by dividing the corresponding independent Gaussian coordinate moment by the Gaussian radial moment in four dimensions. Direct polynomial expansion of the entire observable and action gives the numerator and partition coefficients. A separately organized expansion into all sixteen observable subsets reconstructs them from 112 primitive moments per fixture. Both calculations include the `1/n!` Taylor factor.

All eleven frozen rational-coordinate fixtures were independently rebuilt: tetrahedral and commuting directions, common Hadamard rotations, common reflections, ranks one and two, zero coefficients, signed coefficients and zero action with nonzero cancelling coefficients. All 1,232 primitive moments and 77 numerator/partition coefficient pairs agree with the producer. The primitive moments also reproduce our independently expanded observable polynomial. These finite-degree checks do not supply a remainder bound at nonzero `t`; `t` is a formal auxiliary parameter, not physical time. Central odd coefficients vanish by `q -> -q`; this parity must be rederived for a different joint action.

Our admissibility implementation checks symmetry and all 31 nonempty principal minors, then obtains rank by independent row elimination. It checks rank at most four, unit observable directions, the four action cross relations and the action norm relation. This differs from the forward Schur algorithm and accepts its rank-deficient cases. Rational input is not a claim that every rational admissible Gram has a rational coordinate realization: the general theorem is over real coordinates, while this executable fixture oracle uses explicit rational coordinates.

## Discriminating outcomes and edge cases

The common tetrahedral and commuting examples both have `b=(1/8,0,0,0)` and identical partition coefficients. Their zero-degree numerators are respectively `-1/405` and `13/1215`. Action-only caching would therefore return the wrong observable. Their full Grams differ. Applying a common orthogonal map to every vector preserves the full Gram and every checked coefficient.

The historical quaternion convention uses conjugate boundary quaternions. The common reflection `diag(1,-1,-1,-1)` relates the current listed directions to that convention. It preserves the full Gram and leaves the two common scalar-axis action vectors unchanged. This convention clarification causes no change to the declared fixtures.

A concrete symmetric matrix with a zero first row has all leading principal minors zero, while a non-leading two-by-two principal minor is `-3`. It is rejected. This exposes why leading minors alone are inadequate for semidefinite admission. Other rejected data include a rank-five identity matrix, nonunit direction, asymmetric Gram, a realizable but wrongly declared doubled action, a forged action norm with valid cross relations, noncanonical rational encoding, malformed Boolean coordinates and exponents, wrong dimensions and negative exponents.

The actual public cache boundaries are tested after a valid cache entry is populated. Boolean aliases still reject; returned coefficient tuples/Fractions are immutable and returned certificate mutations do not affect later results. Source mutations and runtime producer dimension changes reject. Complete-evidence replay rejects omissions, source/schema changes, incorrect action data and false finite-error claims.

## Source review, results and retained correction

Reviewed the complete forward `gram.py` and `check.py` files: parsing, Schur pivots, rank and action constraints, recurrence multiplicities, cache entry points, coefficient normalization, fixture reconstruction, certificate replay and output serialization. The recurrence skips a zero multiplicity before lowering indices. Public validation precedes cache access. The independent implementation shares no forward moment or validator code. The comparison imports the producer only in an isolated process to attack its public validation boundary after independent arithmetic has already reconstructed the complete collection.

The independent science suite passes **41 named checks** and the full producer comparison passes **31 named checks**. Ordinary and optimized Python produce identical semantic output bytes; these are counted once. Separate portability checks confirm the accepted nested output layout and rejection of an undeclared source file.

One real test-harness interruption is preserved in `history/`: the immutable Fraction correctly raised `AttributeError` when its numerator was assigned, but the initial helper only caught `ValueError` and `TypeError`. The helper was corrected. This was an exception-handling repair in the test harness, not a failed moment calculation; the interrupted run had written no successful result.

No new mathematical or producer-code defect was found in this bounded C1 review. The full surrounding-link integration remains the gated next loop. Its conditional central reduction will require the actual off-axis action and all declared surrounding weights; this C1 result alone does not establish that reduction.

Run `python check.py --output ../c1-output`. Run the focused comparison with `python compare.py --producer PRODUCER_SOURCE --evidence PRODUCER_OUTPUT --output ../c1-comparison`. Output directories must remain outside this independent source directory. The producer may use its accepted child `output/` layout; the comparison excludes only known generated-output roots and still rejects undeclared source files.
