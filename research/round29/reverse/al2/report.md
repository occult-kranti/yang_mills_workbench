# HNM scale-invariant eligibility — independent reverse AL2

Project author: Hruday N M (BUNZEEY). The HNM name is a project audit label, with external theorem authorship unchanged and scientific novelty unverified. The derivation used the frozen AL2 contract and inherited accepted AL1 report; no current forward or skeptic AL2 result was read.

## Reconstruct the desired repair

Suppose K is the actual centered AL1 Hamiltonian and the raw operator changes as H'=qH+bI, q>0. Its true ground energy becomes E0'=qE0+b, so K'=qK. Every electric and magnetic coefficient gains q, as does delta=alpha/8. Thus lambda/alpha, tau=24lambda/alpha and epsilon=21lambda/delta are invariant. The same sufficient hypotheses pass or fail. Its physical gap scales by q; b does not affect the gap. At fixed hbar and physical t the evolution changes to exp(-itqK/hbar). Equality with the old evolution requires the explicit reciprocal time change t'=t/q. Merely calling q a unit change while retaining the same physical clock does not identify dynamics.

A separate modification lambda'=s(g)lambda with electric alpha unchanged is a change of the magnetic/electric ratio. It is an action deformation unless a separate matching theorem establishes equivalence. Restrict to s>=0 and g>0; q,a,hbar,E_star are strictly positive. For the uniform positive branch, the exact normalized quantities are r'=4s/g^4, tau'=96s/g^4 and epsilon'=672s/g^4.

## Necessary and sufficient conditions for this inherited domain

Assume the source's fixed constants c1(S),c2(S)>0, still unevaluated. I1 requires r'<=1/2 at both endpoints, r'<=1/8 at the bridge, epsilon'<c1 and c2epsilon'<1/2. The bridge inequality implies the endpoint inequalities. Direct algebra gives the iff statement

\[
0\le s(g)\le {g^4\over32},\qquad
s(g)<{c_1(S)g^4\over672},\qquad
s(g)<{g^4\over1344c_2(S)}.
\]

The bridge endpoint is nonstrict; both omitted restrictions remain strict. Replacing all three by a single nonstrict minimum changes membership at a strict boundary and is incorrect. This iff concerns the explicitly inherited sufficient theorem domain, not necessary and sufficient conditions for an actual spectral gap. s=0 satisfies the inequalities and recovers the unperturbed electric product model, but it does not satisfy a separate demand for a nonzero magnetic interaction. No zero or negative energy scale is admitted.

For any weak-coupling family g→0 which obeys these caps, 0<=s(g)<=g^4/32→0 by the squeeze theorem. For the AL1 path g_n²=1/n, the necessary bridge cap is s_n<=1/(32n²). Hence a common magnetic suppression capable of passing this test asymptotically vanishes relative to the original magnetic coefficient. This repairs sufficient-domain membership only by modifying the specified family; a common energy or clock rescaling cannot do it.

## Executed controls and limits

The rational checker independently evaluates both the original four inequalities and the reduced three caps. Exact fixtures include a valid bridge equality, invalid equality at each omitted cap, zero source, an interior point, and a bridge-only failure. Arbitrary positive rational q values check ratio invariance, scalar cancellation in actual energy differences and reciprocal clock matching. Negative magnetic suppression and zero/negative scales are rejected. Synthetic c1,c2 values are algebra fixtures and certify no value for the actual source constants.

Reproduce with `python research/round29/reverse/al2/check.py --output /absolute/new-directory`. The same command under `python -O` produces byte-identical semantic results. Input snapshots, report, code and results are source-bound; freeze.json records the normal/optimized parity. No new numerical stability interval, spectral estimate, physical observation or continuum theorem results from this loop.
