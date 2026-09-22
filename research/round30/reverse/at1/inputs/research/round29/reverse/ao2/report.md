# HNM limiting Wilson energy identity — independent reverse AO2

Project author: Hruday N M (BUNZEEY). These are model-specific applications of standard uniform-integrability and spectral-domain arguments; scientific priority is unverified. No current forward/skeptic AO2 output was read.

## Exact state and admitted inputs

Use only AK2's actual I1/AJ1 homogeneous whole-star positive-orthant state and physical GNS generator H_phys, with the original xz Wilson on its complete 48-link/36-endpoint region. Keep alpha,hbar,a,E_star fixed positive, |tau|<tau_* and |tau|<=2^-16. Let nu_Lambda be the finite physical spectral measure of the actually centered vector chi_Lambda=(W-omega_Lambda(W))Omega_Lambda, and nu the actual limiting physical measure of chi=(pi(W)-omega(W))Omega.

AK2 proves convergence on C0 tests from its source-qualified tested resolvents, with moving finite means justified; local state convergence gives the masses and moments of W. It also proves the exact finite identity mu1,Lambda=alpha omega_Lambda(1-W²). AO1 adds the uniform finite second-moment bound C=alpha²(36+28|tau|)<37alpha². This C has units energy squared. None of these statements has been transferred to a later AQ state.

## Uniform integrability and the actual first-moment equality

For any physical energy cutoff R>0,

\[
\int_{E>R}E\,d\nu_\Lambda(E)\le C/R. \tag{HNM-AO2.1}
\]

This follows from E<=E²/R on the tail. It is uniform over the original finite volumes. Set theta_R(E)=min(1,max(0,2-E/R)), and f_R(E)=E theta_R(E). This continuous compactly supported function equals E below R and satisfies 0<=E-f_R(E)<=E 1_(E>R). Therefore

\[
0\le\mu_{1,\Lambda}-\int f_R\,d\nu_\Lambda\le C/R.
\]

For each fixed R, use the admitted C0 convergence and the bounded-local limit of 1-W² to obtain

\[
0\le\alpha\omega(1-W^2)-\int f_R\,d\nu\le C/R.
\]

As R increases, f_R increases pointwise to E. Monotone convergence followed by R→infinity proves the equality

\[
\boxed{\mu_1=\int E\,d\nu(E)=\alpha\omega(1-W^2).} \tag{HNM-AO2.2}
\]

This closes AK2's possible first-moment loss for the same actual state. It is not a formal derivative of a correlation and not an inference from bounded first moments alone.

## Second-moment upper bound and operator domain

Apply the same compact cutoffs to g_R(E)=E² theta_R(E). They increase to E², and finite integrals are bounded by C. C0 convergence then monotone convergence yields

\[
\int E^2\,d\nu(E)\le C.
\]

By the spectral theorem for the actual self-adjoint H_phys, finiteness of this integral is exactly chi in D(H_phys), and ||H_phys chi||² is that integral. This proves an upper bound and operator-domain membership. It does not prove convergence or equality of the second moments. The first-moment tail bound also holds for nu by its second-moment ceiling.

Centering, full physical restriction, ground subtraction and the positive energy scale remain exactly those of AK2. A nonzero mean adds a zero-energy atom to an uncentered W-vector, changing its mass although not its positive moments. A raw-ground scalar shifts energy moments if it is not canceled. The result is stated for physical E, not normalized E/delta, and no hbar enters an energy moment.

## Countercontrols and reproducibility

AK2's measures (1-1/n)delta_g+(1/n)delta_(g+n/2), g=1/16 in alpha units, have fixed first moment 9/16 but second moment 17/256+n/4. They violate the new uniform second-moment ceiling as n grows, so cannot refute the equality proved here.

In contrast, (1-1/n²)delta_g+(1/n²)delta_(g+n) have uniformly bounded second moments, first moments g+1/n→g, and second moments g²+2g/n+1→g²+1. Their bounded-test limit is delta_g, whose second moment is g². Thus second-moment equality would require additional uniform integrability or another argument; the present hypotheses do not supply it. Both are abstract positive spectral-measure diagnostics, not claimed actual Yang–Mills measures.

Run `python research/round29/reverse/ao2/check.py --output /absolute/new-directory`. Rational controls test both escaping families, compact-cutoff/tail inequalities, centering, physical scaling and source/state guards. Normal/optimized semantic outputs agree and the report, input snapshots, code and outputs are hash-bound. The conclusion remains restricted to the old actual state and its original symbolic stability restriction; it does not identify a new numerical-cap thermodynamic state or solve the continuum problem.
