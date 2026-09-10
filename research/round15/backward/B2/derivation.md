# B2 independent total-degree character certificate

Use the graph and Haar measure frozen in B1. All six face couplings equal the same real rational k. Set S=k sum_f x_f and O=product_f x_f. Both |O|<=1 and |S|<=M=6|k| are graph-matched bounds.

The independent coefficient oracle decomposes the n-fold fundamental tensor power. The multiplicity of character label r is binom(n,(n-r)/2)-binom(n,(n-r)/2-1), when n-r is even and nonnegative, and zero otherwise. Since x=chi_1/2, the character coefficient in x^n is this multiplicity divided by2^n. This construction is independent of the producer's closed factorial exponential formula.

For the partition, each face's coefficient of k^n/n! is the character decomposition of x^n. For the all-six insertion, it is instead the decomposition of x^(n+1). Form six separate series, convolve them and truncate their TOTAL degree toN. Sum over the shared label with the reviewed cube denominator(r+1)^4. This gives exactly T_N(O)=integral O sum_(j=0)^N S^j/j!, including the correct multinomial weights. Six insertion shifts correspond to differentiating once in each independent face coupling and only then restricting to the diagonal. Taking the sixth derivative along a common coupling would sum many different repeated-face insertions and is a different observable.

For N+2>M, the uniform exponential remainder is bounded by

R_N=[M^(N+1)/(N+1)!]/[1-M/(N+2)].

Every omitted term ratio after the first is at mostM/(N+2); summing that geometric majorant proves the bound without a transcendental numerical oracle. The polynomial estimates for the numerator and partition receive their own signed +/-R_N intervals. Jensen's inequality gives Z>=1 since every individual face has zero Haar mean. Normalize only with a strictly positive ordered partition interval, using all signed numerator/denominator corners.

For the independent-face baseline Z_ind=Z0(k)^6, the same total-action bound M and centered Haar action prove the same remainder. Its exact Taylor polynomial is the label0 contribution. The partition excess enclosure is [Z_cube_lower-Z_ind_upper,Z_cube_upper-Z_ind_lower]; both errors must be retained. This is not a covariance or the all-six insertion.

There is also a conventional sign theorem for this common-coupling finite sphere: Z_cube-Z_ind=sum_(r>=1) (r+1)^-4 a_r(k)^6. For k!=0, a_1(k) has the sign of k and is nonzero, as seen from its odd series with positive coefficients (or the strictly increasing one-face partition). Every sixth power is nonnegative, so the excess is strictly positive. This does not give a mass gap or a general inequality at independently signed face couplings.

All computations below are finite graph statements. A Taylor degree is an algorithmic remainder parameter and cannot substitute for a physical lattice-spacing or representation-cutoff limit.
