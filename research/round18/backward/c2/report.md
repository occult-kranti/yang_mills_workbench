# Independent C2 review: the full conditional two-link integral

The independently reconstructed four-cube complex has 18 vertices, 33 links and 20 faces. The variable links are the central vertical link `U: (1,1,0)->(1,1,1)` and the surrounding vertical link `V: (1,0,0)->(1,0,1)`. All other 31 links are fixed to identity. Four faces touch U, three touch V and exactly one belongs to both sets. Every signed square word is explicitly reconstructed from its endpoints. The six affected normalized traces are three copies of `x=Tr U/2`, two copies of `y=Tr V/2` and one `w=Tr(U Vdagger)/2`. The fourteen remaining traces are one. Their action constant `14*kappa` cancels in this conditional quotient; it is not permission to discard the same terms from a different surrounding marginal.

We calculate

`E_k[O] = E[O exp(kappa*(3x+d*y+w))] / E[exp(kappa*(3x+d*y+w))]`,

where `O=(4x^2-1)^3*(4w^2-1)/81` and U,V have independent normalized SU(2) Haar measure. The complete six-face action has `d=2`. The cases `d=1` and `d=0` deliberately omit one or both V-only face weights. They remain valid different actions on the same observable and measure. They are not alternative implementations of the primary model.

## Independent angular derivation

Write the quaternions as `U=(x,sqrt(1-x^2)*n)` and `V=(y,sqrt(1-y^2)*m)`. The scalar coordinates x,y are independent with density `(2/pi)*sqrt(1-x^2)` on `[-1,1]`. Conditional on x,y, the relative angular coordinate `z=n dot m` is uniform on `[-1,1]`. Consequently

`w=xy+sqrt((1-x^2)*(1-y^2))*z`.

For nonnegative integer exponents a,b,c, expand the even z powers. Let `s_p` be zero for odd p and `Catalan(p/2)/4^(p/2)` for even p, and define

`B(p,j)=sum_{h=0}^j (-1)^h binomial(j,h) s_(p+2h)`.

Then the exact independent moment formula is

`E[x^a y^b w^c] = sum_{j=0}^{floor(c/2)} binomial(c,2j)/(2j+1) * B(a+c-2j,j)*B(b+c-2j,j)`.

This expression contains no division by `sqrt(1-x^2)` or `sqrt(1-y^2)` and stays regular at the endpoints. Our source expands the observable and powers of the complete action as coordinate polynomials before integrating. The producer instead decomposes fundamental trace powers into characters and uses a representation-dimension divisor. No producer moment or recurrence is used by this independent oracle. The full comparison reconstructs all 969 moments of total degree at most sixteen, a complete superset of the monomials in the degree-eight observable/action expansion.

The exact correlated moments include `E[xyw]=1/16` and `E[x^2 y^2 w^2]=1/48`. Three independent semicircle trace coordinates would instead give zero and `1/64`. Omitting the character-dimension divisor gives `1/8` in the first test. These are valid integrated discriminators.

The graph and measure give zero unweighted mean of O: at fixed U, integration over V kills the shared adjoint factor. Holding V at identity is a different one-link calculation, whose zero-action value is `E[(4x^2-1)^4]/81=1/27`.

## Small-coupling checks and finite remainder

Direct polynomial integration gives numerator coefficients

`[kappa^0]N=[kappa^1]N=0`,

`[kappa^2]N=(d^2+1)/648`, and `[kappa^3]N=d/108`.

The partition coefficients are `Z0=1`, `Z1=0`, `Z2=(10+d^2)/8`, and `Z3=3d/16`. Thus the complete d=2 numerator has quadratic coefficient `5/648`, cubic coefficient `1/54`, and partition cubic coefficient `3/8`. Dropping one V-only weight changes the quadratic coefficient to `1/324`; dropping both gives `1/648`. The nonzero cubic terms show why an even-in-kappa assumption is invalid for the full model. The d=0 action has the separate even branch verified in the signed fixtures.

For the primary `kappa=1/64`, the full absolute action is at most `M=6/64=3/32`. Each normalized adjoint factor has absolute value at most one, hence `|O|<=1`. If `M<N+2`, the sum of all omitted exponential terms is bounded by

`R_N = M^(N+1)/(N+1)! / (1-M/(N+2))`.

The same bound controls the numerator and partition remainders. Moreover the Haar expectation of `S=3x+d*y+w` is exactly zero, because each single trace has mean zero. Jensen therefore gives `Z=E exp(kappa*S)>=1`, including signed kappa. The denominator lower endpoint is consequently `max(1,Z_N-R_N)`. This is an explicit mathematical premise for the stronger denominator floor, not a numerical clamp. All four numerator/denominator endpoint quotients are evaluated, so coarse intervals crossing zero retain their negative lower endpoints.

The frozen levels 0,2,4,6,8 are all retained. Degrees0 and2 do not establish a sign. Degrees4 and6 establish positivity but fail the requested width. Degree8 gives a lower endpoint approximately `1.9555278081641146e-6` and width approximately `3.111099138388648e-15`, below `1e-12`. These approximations are display values; the evidence stores exact rational endpoints. The numerator partial sum alone lies outside the final normalized expectation interval, so omitting the denominator is a discriminating error.

All nine declared `(d,kappa)` fixtures are retained for d2,1,0 and kappa `+1/64,0,-1/64`. The three positive-kappa omission intervals are disjoint. The signed complete-action intervals differ; the d0 signed intervals agree. The results establish a conditional two-link expectation, not an infinite-volume estimate, a complete twenty-face bulk integral, a Hamiltonian eigenvalue or a Yang–Mills mass gap.

## The precise C1 connection and its measure

For a fixed V with scalar coordinate y, the three unshared central directions are e0 and the shared direction is V. The central action vector is `b=kappa*(3e0+V)`. The complete joint Gram obeys

`b dot b=kappa^2*(10+6y)`, `b dot e0=kappa*(3+y)`,

`b dot V=kappa*(3y+1)`, and `e0 dot V=y`.

The direction Gram has rank two for `|y|<1` and rank one at y=±1; the action vector belongs to this span even when kappa is zero. An explicit realization `V=(y,sqrt(1-y^2),0,0)` proves positive semidefiniteness and the complete action relations on the whole interval. The executable y fixtures `-1,0,3/5,1` also check every principal minor and the action cross/norm relations without a singular inversion. C1's full-Gram theorem therefore justifies the dependence of the central integrals on this y, for this identity boundary.

The outer denominator is `integral rho(y)*exp(2*kappa*y)*Z_U(G(y)) dy`, and the numerator replaces `Z_U` by `N_U`. Averaging an already normalized inner observable `N_U/Z_U` needs the additional `Z_U` weight. This weight is not constant: its second-order coefficient contains `(10+6y)/8`. Bare outer Haar averaging is a different measure. Replacing the semicircle y density by uniform density also fails its second-moment test, `1/4` versus `1/3`. No scalar reduction for arbitrary surrounding boundary links is inferred.

## Dagger exception, code review and retained finding

At fixed `U=V=(3/5,4/5,0,0)`, the correct relative trace w is one whereas `Tr(UV)/2=-7/25`. This distinguishes signed words pointwise. A consistent replacement of w everywhere by `Tr(UV)/2` nevertheless preserves this integrated joint law: the substitution `V->Vdagger` preserves Haar and y, and maps the latter trace to the former. It would be incorrect to demand an integrated numerical discrepancy from that consistent substitution in this specific model. A single malformed signed edge in the original graph remains invalid; complete signed geometry is checked before reduction.

The full producer `joint.py` source was reviewed: coefficient combinatorics, moment caps and cache boundaries, actual graph words, conditional Grams, total-action remainder, Jensen floor, signed division, fixture inventory and complete source-bound replay. The implementation's factor `1/(n+1)` is essential to its character method. Public exponent validation occurs before cache access, and returning fresh tuples or dictionaries avoids cache poisoning.

A real pre-freeze input-boundary weakness was identified in the public `divide()` helper: direct Fraction conversion admitted Boolean and noncanonical interval endpoints and did not verify the declared width. The repaired helper requires complete canonical rational interval objects and consistent nonnegative widths before division. Its original behavior and source are retained by the producer. This did not invalidate the generated scientific certificates, which already supplied valid exact endpoints, nor the complete verifier, which already rejected altered full certificates. The independent comparison explicitly retries the repaired Boolean, noncanonical and forged-width cases.

Independent science passes **40 named checks** and the complete producer comparison passes **39 named checks**. Two accepted-layout checks are recorded separately. Ordinary and optimized output bytes agree and their check counts are counted once. The scope of this review is the final scientific C2 loop. Subsequent proof-adapter and reproduction review is integration work, not another physics experiment.

Run `python check.py --output ../c2-output`; compare using `python compare.py --producer PRODUCER_SOURCE --evidence PRODUCER_OUTPUT --output ../c2-comparison`. The source manifest binds all code, reviews and evidence. No network or nonstandard numerical package is needed for the exact scientific programs.
