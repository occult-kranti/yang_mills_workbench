# R2 independent preparation — before current solution reading

Neither current producer nor root's current R2 work has been read. This is a skeptical comparator for the frozen tenth-loop contract, not admission or an extra executed loop. Use only the actual initial O1 diagonal on the fixed product-reference incomplete tensor product. Put k=28|tau|<=35/416, g=1-k>=381/416, and r=||v||. All displayed quantities are dimensionless in delta=alpha/8.

## Infinite form and inverse

Construct H0 as the nonnegative spectral tensor sum on the incomplete product, with the finite-support spectral-domain vectors as a dense core. The independent excitation-sector decomposition gives H0>=Q. For its form-domain vectors psi,phi, the actual star terms satisfy

`sum_b |<psi,D_b phi>| <= 7|tau| [sum_b||Q_b psi||^2]^(1/2)[sum_b||Q_b phi||^2]^(1/2) <= k ||H0^(1/2)psi|| ||H0^(1/2)phi||`.

This proves absolute convergence of the sesquilinear form, not convergence of the global operator series on every vector. The perturbation is Hermitian, annihilates the vacuum, and has relative form bound k<1. Thus the form sum is closed on Q(H0), defines a nonnegative self-adjoint G, and satisfies gH0<=G<=(1+k)H0 and G|Q>=g. The associated operator domain is defined through the form representation; equality D(G)=D(H0) globally is not a consequence.

On Q, H0^(-1/2) is bounded and maps into Q(H0). The sandwiched form defines bounded self-adjoint K, ||K||<=k. Derive the sign from the actual form sum: its reduced inverse is

`G_Q^(-1)=H0^(-1/2)(I+K)^(-1)H0^(-1/2)`.

For u given by this formula, pairing against arbitrary form-domain test vectors proves G u=v and u in D(G). Only then expand `(I+K)^(-1)=sum_n(-K)^n`. No commutation of H0 and D is assumed.

## Locality and response domains

A vector supported on a finite complete-factor set X means it has the exact reference vacuum outside X. H0 inverse powers preserve this property. Every D_b disjoint from X annihilates such a vector, so its action is a finite sum over at most 4|X| stars, with

`||D w|| <= k |X| ||w||`, `support(Dw) subset X^(1)`.

These facts justify K's action on local vectors and the coefficient recurrence

`u_0=H0^(-1)v`, `u_(n+1)=-H0^(-1)D u_n`.

The prescribed Neumann coefficients therefore have support in Y^(n), obey `||u_n||, ||H0^(1/2)u_n||<=r k^n`, and lie in D(H0). The operator estimate needs this additional finite-action argument:

`||H0u_0||=r`, `||H0u_n||<=r k^n |Y^(n-1)|` for n>=1.

The collar union bound is `|Y^(n)|<=|Y|(2n+1)^3`. Let U_N=sum_(n=0)^N u_n, and define

`B_N(k)=k^(N+1)/(1-k)`,

`T_N(k)=sum_(j=N+1)^infinity k^j(2j-1)^3`.

With a_N=2N+1, an explicit expression is

`T_N=k^(N+1)[a_N^3/g + 6a_N^2 k/g^2 + 12a_N k(1+k)/g^3 + 8k(1+4k+k^2)/g^4]`.

For N>=0 the independent candidate bounds are

| Quantity | Upper bound |
|---|---|
| ||u-U_N|| and ||H0^(1/2)(u-U_N)|| | r B_N |
| ||H0(u-U_N)|| | r |Y| T_N |
| ||G(u-U_N)|| | r |Y| (2N+1)^3 k^(N+1) |

The last identity follows from `G U_N=v+D u_N`. Absolute convergence of both u_n and H0u_n proves u in D(H0), specifically for this response. The convergent D u_n series agrees with the form action, so the inverse equation and the G-graph tail are justified. This does not establish equality of the global operator domains.

For a finite containing cuboid, use all and only its retained stars. If Y^(N) lies inside Lambda, coefficients through N agree exactly with the infinite coefficients. The same coefficient bounds hold uniformly. Vacuum-embedded finite responses consequently obey

`||u-u_Lambda||, ||H0^(1/2)(u-u_Lambda)|| <= 2r B_N`,

`||H0(u-u_Lambda)|| <= 2r |Y| T_N`.

Each finite response also belongs to D(G): it is supported in Lambda and the extra stars meeting Lambda form a finite sum. Since `G u_Lambda-v=(D-D_Lambda)u_Lambda`, only coefficients n>=N contribute to that exterior difference. Hence the additional comparator `||G(u-u_Lambda)||<=r|Y|T_N` is available. These are fixed-source/containing-collar estimates, not norm convergence of the global K_Lambda operators on every possible source.

At tau=0, k=0, all n>=1 coefficients and every displayed tail vanish; u=H0^(-1)v. At r=0 every response and majorant vanishes. These cases must not be lost by dividing by r or taking log k.

## Actual source-sector and boundary controls

For finite Lambda, S_vac=|u_Lambda><Omega_Lambda|-adjoint cancels exactly A_vac=|v_Lambda><Omega_Lambda|+adjoint on D(G_Lambda). It does not cancel A_Y tensor I. The exact difference is

`A_Y tensor (I-P_ext)`.

For the frozen Y={0}, let w_ext be the normalized free z-character at fine tail (4,0,0), at coarse site e_x. On the actual vector psi=Omega_Y tensor w_ext tensor remaining vacuum, A_vac psi=0 while `(A_Y tensor I)psi=v_Y tensor w_ext`, of norm one. These independent Haar factors have bare energies 6 and 12 for the input/output. They are actual local operator-domain vectors, with the strip ground unchanged. The source-sector mismatch is independent of tau and cannot be removed by an inverse estimate.

The bare truncation u_0=v/6 also has a genuine actual-model defect: `||G u_0-v||^2=7tau^2/432`, from R1's all21-face contraction. At the origin no negative incoming anchor exists, so the only star acting on this vector is the origin star. This rejects deleting boundary action in the proposed series for either nonzero coupling sign.

Spatially local response coefficients can be lifted to local skew rank-two operators on Y^(n), tensor identity outside. Their operator norms are ||u_n|| and their geometric norm sum converges. That lift acts on Omega with response u, but is not the global vacuum rank-two S_vac. A submission claiming equality must be rejected; a separate full operator identity or domain theorem needs its own proof. A vector tail, a bounded local-operator lift, and the weighted interaction certificate below remain distinct statements.

## Specified volume-weight certificate

For the origin singleton, the declared collar is exactly {0,...,n}^3 with volume (n+1)^3. For fixed r>0, tau!=0 and mu>0, the proposed upper-certificate term is

`exp(mu(n+1)^3) r k^n`.

Its logarithm tends to positive infinity, so these upper terms do not even tend to zero. This proves failure of this specified majorant only. The actual coefficient norms may be much smaller, and different connected-support decompositions or weights remain untested. No lower bound on actual coefficients or every possible algorithm follows.

At mu=log(2), the successive upper-term ratio is `k 2^(3n^2+9n+7)`. For the endpoint k=35/416 it already equals 140/13 at n=0. For k=1/1000 it begins at 16/125<1, then exceeds one: an early decrease does not give all-step summability. Replacing the cubic collar volume by n+1 would falsely reverse this conclusion. The r=0 and tau=0 exceptions are genuinely convergent.

## Primary hypotheses and acceptance checklist

The targeted [author-hosted mathematical source](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf) is recorded with version, theorem/page locators and reading depth in r2-primary-source-map.json. Its form representation and small-relative-form-bound hypotheses are matched directly; no global operator-domain equality is imported. The plus sign in I+K is derived independently.

Accept only proofs that establish the actual infinite form before the inverse, justify coefficient locality despite inverse powers, retain every star, and separate form/response-operator/global-operator domains. Tail formulas must include polynomial factors and the precise finite-volume collar margin. The exterior character control must be actual SU2, and the volume-weight finding must remain a failure of the stated upper certificate. The initial diagonal, arbitrary diagnostic source, fixed representation and unchanged physical scales are essential qualifications. No new research loop or future-goal execution follows from this preparation.
