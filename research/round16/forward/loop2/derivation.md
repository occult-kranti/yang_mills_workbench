# Loop2: exact shared-face action comparison on the fixed two-cube complex

## Selected target and unchanged observable

Keep the reviewed20link/11face graph and normalized product Haar measure. Define O=product_(all11faces) x_f with x_f=Tr(U_face_f)/2. Every outer coefficient is1/8. Compare the normalized expectation at shared coefficient1/8 with the expectation at shared coefficient0. The graph and the all11trace observable remain identical. A zero shared action coefficient does not remove its trace from O.

The target is a strictly positive lower endpoint and interval width at most10^-12 for D=E_full[O]-E_omit[O]. Degrees0,6,12,18,24, cap24, are fixed before execution. Coefficients are dimensionless finite Euclidean action parameters; no physical time, Hamiltonian normalization or continuum limit is introduced.

## Exact per-face coefficients and total degree

For spin n/2 and d=n+1, write exp(u*x)=sum_n a_n(u)chi_n(U), with

a_n(u)=sum_(j>=0) d*u^(n+2j)/[2^(n+2j)*j!*(n+1+j)!].

Introduce one formal bookkeeping variable epsilon in exp(epsilon*sum_f k_f*x_f), truncate total epsilon degree N, and then evaluate epsilon=1. The polynomial coefficients retain all individual eleven rational k_f values. For the numerator insertion x_f exp(epsilon*k_f*x_f), the correct character coefficient is a_n'(epsilon*k_f). A term of original power p=n+2j contributes p*c_p*k_f^(p-1)*epsilon^(p-1). There is no extra epsilon or k_f. Equivalently, expand x_f exp(...) directly and project its powers onto characters. This formula remains valid at k_f=0 because p=1 contributes a nonzero constant1/2 in the fundamental channel.

Within each five-face disk, multiply the five character coefficient polynomials and divide by d_n^4. Combine the left n, right m and shared k channels with the reviewed SU(2) fusion condition |n-m|<=k<=n+m and even n+m+k. In a partition polynomial, each disk label contributes at least5n powers, so n<=floor(N/5). For the all-trace numerator, n>=1 contributes at least5(n-1) powers, so n<=floor(N/5)+1. Label0 is retained separately by the same bound. Shared labels range over all permitted n,m fusion outputs. These bounds make the retained sums finite without discarding any total-degree term.

The coefficient routine supports independent face values; it does not assume all ten outer coefficients coincide. The held-out unequal-signed fixture changes one particular outer coefficient, while binding its face identifier and all other coefficients.

## Global remainder and normalization

For S=sum_f k_f*x_f, M=sum_f|k_f| and |O|<=1. When N+2>M, the absolute uniform Taylor remainder is

R_N = [M^(N+1)/(N+1)!]/[1-M/(N+2)].

If z_N=E0[sum_(j=0)^N S^j/j!] and a_N=E0[O sum_(j=0)^N S^j/j!], then Z lies in[z_N-R_N,z_N+R_N] and A lies in[a_N-R_N,a_N+R_N]. The Haar mean of every distinct fundamental face trace is0, hence E0[S]=0 and Jensen gives Z>=1. Intersect the partition interval with[1,infinity), reject an empty intersection, and retain all numerator-sign/positive-denominator quotient corners.

For the full action M=11/8; for the omitted shared coefficient M=10/8. Enclose both expectations independently. If their intervals are[f0,f1] and[o0,o1], then D lies in[f0-o1,f1-o0]. No presumed error cancellation or zero baseline is used. All endpoints, widths and statuses are exact rational values.

## Why the omitted-action baseline is not zero

Center parity identifies the first allowed numerator contributions when all outer coefficients equal t and the shared coefficient is0. The minimal derivative support consists of all five faces of either the left or right disk. Each contribution has Haar coefficient41/(81*2^19); the sum is41/(81*2^18). Therefore A(t,t,0)=41/(81*2^18)*t^5+O(t^7). The partition is1+O(t^2), so the normalized expectation has the same leading coefficient. This local expansion diagnoses the baseline but does not replace its finite-t enclosure.

By contrast, the first shared-coefficient derivative at the all-zero action is the exact Loop1 mixed moment2^-19. This motivates testing the shared-face response. It does not establish monotonicity for arbitrary coefficients or a general sign theorem.

## Required fixtures and review boundary

The fixed-degree collection requires, in order: allzero; negative shared; omitted shared; half shared; full shared; outerzero with shared1/8; and unequal-signed individual outer coefficient. The primary comparison alone is refined through all five degrees. Missing cases, reordered identifiers, altered face order, changed graph/source hashes, invalid numeric types, dropped tails or invented status fields fail replay.

The producer uses factorial coefficients and allowed fusion channels. The backward verifier projects explicit character polynomials using Catalan Haar moments and integrates the resulting boundary polynomial directly. The earlier raw shared-edge projector calculation remains a graph prerequisite; it does not independently check new Taylor coefficients. Exact finite integral results remain separate from physical spectral and continuum obligations.

## Recorded outcome

At degree24 the full expectation is approximately2.430920616729664*10^-7 and the omitted expectation is approximately5.931251320486862*10^-11. Their difference has exact lower endpoint approximately2.4303274915976136*10^-7 and exact width approximately4.1729944948126505*10^-22. Rational endpoints, not these rounded display numbers, are authoritative.

Degrees0and6 fail both useful positivity and requested width. Degree12 already has positive difference lower endpoint approximately2.2894205288980868*10^-7, but its width approximately2.8181392775852724*10^-8 fails the precision gate. Degrees18and24 meet the complete target. Retaining the degree12 failure demonstrates that positivity alone is not the requested acceptance condition.

The negative-shared fixture has a negative expectation; the allzero action gives exact zero. The omitted-shared, half-shared, full-shared, outerzero and unequal-signed fixtures have positive enclosed expectations at their declared values. These isolated exact signs do not prove a monotonicity or continuous-range theorem. The only primary accepted comparison is the predeclared full-minus-omitted action difference.
