# Prospective third-loop method advice

Recorded after the advisor reported the AT2 mathematical review passed, before
the next contract was selected. This note is source/method advice, not a fourth
production investigation, a frozen proof, or an admission gate.

For the dimensionless positive spectral measure, let its actual mass be s and
actual first moment be u. The inherited inputs give support x ≥ a = 1/16,
s ≤ 63/250 and u ≤ 94/125. Define C(t)=∫exp(−tx)dη(x).
The target is I=∫C(t)dt=αR, an inverse-energy quadratic form. It is not a
new static susceptibility identification or an estimate from actual AQ data.

The advisor's fixed grid h=1/32, n=4096, T=128 and per-sample absolute
error ε=10^−6 are suitable for a bounded prospective protocol. On each cell,
two integrations by parts give the trapezoid excess as

    (1/2) ∫ (t−jh)((j+1)h−t) C''(t) dt.

The kernel is nonnegative and bounded above by h²/8. Positivity and Tonelli
give ∫₀ᵀC''(t)dt=∫x(1−exp(−Tx))dη(x)≤u. AT1's second moment also supplies
ordinary C² regularity at zero. Thus the proposed quadrature allowance
h²u_upper/8 has the correct sign and constant. The tail is between zero and
s_upper exp(−aT)/a. Positive trapezoid weights sum to T, so every permitted
sample-error vector changes the sum by at most Tε; the two constant-sign
error vectors attain these extrema. Merely trying several random errors
would not certify this statement.

Consequently the proposed interval is

    [Trap(samples) − h²u_upper/8 − Tε,
     Trap(samples) + s_upper exp(−aT)/a + Tε].

Include certified exponential enclosure error separately or absorb it into
the declared sample-error budget with exact bookkeeping. For disjointness
of the A/B output intervals under every allowable noise vector, compare
their worst output endpoints: the interval envelope expands by an additional
Tε on each side when the measured values themselves vary. This is distinct
from enclosure of each known I under one permitted sample vector.

The two AT2 abstract controls have I_A=3/32 and I_B=1/10. They are logical
test spectra, not constructed AQ Hamiltonian states. A passed separation
test would establish operational discrimination of those controls by this
protocol, and a conditional AQ enclosure if future certified samples are
available. It would not reconstruct the true AQ measure, identify a pole,
or supply actual AQ sample data.

Closest source attribution: NIST DLMF §3.5(i), Eqs.3.5.1–3.5.3 supplies the
standard elementary and composite trapezoidal formulas and the error sign.
The positive integral-kernel bound above is written out for this application.
Abbott et al., arXiv:2605.20509v1, already formulate spectral bounds from
Euclidean data through positive kernel certificates. No new generic
quadrature, Laplace inversion, or spectral bootstrap method is claimed.

Reading: https://dlmf.nist.gov/3.5 (accessed 2026-09-22), selected §3.5(i),
lines corresponding to definitions and Eqs.3.5.1–3.5.3. No whole chapter
audit. https://arxiv.org/html/2605.20509v1 was reopened; the original
selected-section reading is recorded in the fixed modern source ledger.
