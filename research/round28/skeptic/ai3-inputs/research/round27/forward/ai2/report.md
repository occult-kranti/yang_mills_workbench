# AI2 forward: two physical Wilson probes distinguish selected finite profiles

Independent forward work under the frozen AI2 contract. No current reverse AI2 solution was read. All calculations use the canonical summable full-link SU(2) model, fixed positive alpha, hbar and alpha/E_star, the original physical clock, and the inherited component-wide AA2 theorem. Exact results are in `output/results.json`; decimal displays are illustrative.

## Actual observables and support

Use the free unit cube with origin O=(3,1,0). Let X be the six-cycle made from paths `O -> (3,2,0) -> (3,2,1)` and `O -> (4,1,0) -> (4,2,0) -> (4,2,1) -> (3,2,1)`, the second traversed backwards. Let f4 be the yz square anchored at O and f5 the opposite yz square anchored at (4,1,0). Define cycles Y4=X symmetric-difference f4 and Y5=X symmetric-difference f5. All are simple physical six-cycles. Write chi_C for the actual fundamental trace multiplication along C and set

\[
 B_r=(\chi_X+\chi_{Y_r})/\sqrt2,\qquad r=4,5.
 \tag{AI2-F1}
\]

These are real bounded self-adjoint gauge-invariant multiplication operators, extended by identity. Each pair shares a four-link path; the two remaining two-link paths have independent Haar holonomies conditional on the common path. The fundamental SU(2) character has Haar mean zero, second moment one and fourth moment two. Consequently each B_r has reference mean zero, variance one, and fourth moment 5/2. Its exact operator norm is `2sqrt(2)`: the triangle upper bound is attained arbitrarily closely near identity holonomies on sets of positive Haar measure. In particular the source `psi_r=B_r Omega` is normalized, but B_r does not have norm one.

Each observable uses eight free links, but their **common support has ten**, verified from actual paths. The checker rejects the old B4 eight-link seed as incomplete for B5. Every cycle character has reference electric energy `9alpha/2`. Their source vectors lie in the inherited full sixteen-state cube component. The AA2 exterior-exclusion argument was proved for that whole component and therefore applies to both sources; this does not assert that the component exhausts the whole regional energy shell. The checker re-enumerates all twenty exterior touching faces, the free opposite edge, distinct side owners and their minimum spectral increment 1/4. It preserves the participating nonzero frequency lower bound 1/8 and the unaveraged exterior loading.

## Recomputed complete-factor collars and full spatial tail

Start from the ten singleton free factors in the common seed. Complete reference factors are either free links or ten-link selected strips. At each step include every factor owning any link of an omitted plaquette touching the current factors; retain an omitted face only when all its owners are included. All positive-orthant boundaries and complete strips remain. The checker records depth 0 through 5 counts in `collars` and verifies that every collar at depth at least one contains the complete cube. None of the old seed counts is copied.

The Y1 connected-word proof extends with ten initial factors. At each interaction at most three factors are added; each factor meets at most forty faces. Keeping every ordered word, repetition, commutator factor two and time-simplex denominator gives rising-factor coefficients `(10/3)_n/n!` with the same `x=10 alpha tau_q |t|/hbar`. Matching all words through order k leaves a single full-series tail. At the original clock, `x<=15z`, and a rational upper bound is

\[
 D^{(10)}_k(x)=\frac{(10/3)_{k+1}}{(k+1)!}
 \frac{x^{k+1}}{(1-x)^{k+5}},\qquad x=15z<1.
 \tag{AI2-F2}
\]

Taylor's positive integral remainder has exponent `10/3+k+1=k+13/3`; the integer exponent k+5 is a conservative upper bound. Thus the whole omitted spatial contribution to each correlation is at most `J^2 D=8D`. This includes paths leaving the collar and returning to the source. It is not a finite-spin cutoff or global-propagator norm claim.

## Retained matrix, exact moments, and the conditional ratio

Reconstruct all sixteen simple six-cycles and all six cube faces. The retained symmetric matrix Q(q) has entry q^4 or q^5 on the corresponding physical face flip, zero otherwise. Its row norm is at most six. With

\[
 p(q)=2+5q+5q^2+6q^3+3q^4,\quad
 s_q=\frac{3z(1+q)^2(1+q^2)}{p(q)},\quad v=s_q/96,
\]
\[
 h_r(q,z)=\langle\psi_r,e^{ivQ(q)}\psi_r\rangle,
 \quad m_{n,r}=\langle\psi_r,Q(q)^n\psi_r\rangle,
 \quad m_{1,4}=q^4,\quad m_{1,5}=q^5.
 \tag{AI2-F3}
\]

All moments through degree eight are calculated exactly for every prescribed q. At q=1, both moment sequences through degree six are `(1,1,4,8,32,80,320)`. The formal retained first-coefficient ratio is exactly q. If those retained derivatives were independently available, q would be identified; known alpha and calibrated physical rate `alpha eta/[768 hbar b(q)]` would then identify eta from the coefficient of physical time. This is a conditional inverse of the retained map, not a derivative theorem for actual correlations.

For a single positive v, spectral calculus gives a value bound

\[
 |\operatorname{Im} h_r-vq^r|\le L_r:=v^3\|Q\|^3/6.
 \tag{AI2-F4}
\]

Let y_r be the imaginary part of the actual demodulated connected correlation, and let R_r bound its complete distance from the exact retained h_r. Then `|y_r-vq^r|<=E_r=R_r+L_r`. If `v q^4-E_4>0` and `v q^5-E_5>=0`, the actual measured ratio belongs to

\[
 \frac{vq^5-E_5}{vq^4+E_4}
 \le\frac{y_5}{y_4}\le
 \frac{vq^5+E_5}{vq^4-E_4}.
 \tag{AI2-F5}
\]

Both positivity conditions are checked in every frozen grid cell. This is used as a predicted interval for each frozen hypothesis. Conversely, observed values with independently known E_r yield an interval for the ideal ratio q by dividing their interval bounds, provided the observed denominator interval is positive. When the numerator interval crosses zero, take the minimum and maximum of all four corner quotients; the general helper does so. Unknown preparation/readout error must be added first. The checker includes denominator-failure and signed-numerator cases. No finite-q derivative is obtained by differentiating a value-only disk.

## Complete scalar disks

Use the actual AD2 scalar transfer with J²=8 and `1+J<4`. For `M_k=N_k/24`, `tau_q=eta/[8b(q)]`, and `dhat_q=tau_q sqrt(b(q²)/96)/[(1-eta)/8]`,

\[
 R_{\rm physical}=48\widehat d_q+
 8D^{(10)}_k(15z)+64\tau_qM_k(1+3zM_k).
 \tag{AI2-F6}
\]

The first term replaces the full stationary state including the connected mean; the second is the complete spatial error; the third includes both source and vacuum averaging errors and the actual multiplier norm. The script uses an integer-square-root upward enclosure for dhat. It computes exact rational degree-eight centers, with a separate unitary arithmetic error `(v ||Q||)^9/9!`. Its full disk radius is `R=R_physical+R_arithmetic`. Adding this arithmetic amount also to the simple-ratio bound is conservative. The two probes share the same certified R because their norm and common support agree.

Dropping the factor eight, normalizing away the multiplier, or retaining only the source column gives an inadmissible smaller disk. The exact checks retain the component-wide AA2 theorem; instantaneous closure is not assumed. The wrong matrix assigning q^4 to the q^5 face makes the retained slope ratio one and destroys its q dependence.

## Frozen hypotheses and decision rule

For every prescribed `u in {10^-12,10^-18,10^-24}`, compare

\[
 H_1:(q,\eta)=(1-u,1/2),\qquad
 H_2:(q,\eta)=(1-2u,1/16).
 \tag{AI2-F7}
\]

Both have `eta(1-q)^3=u^3/2`; at the same fixed alpha and `z=10^-6` they therefore use exactly the same physical time

\[
 T=2\cdot10^{-6}u^{-3}\,\hbar/\alpha.
 \tag{AI2-F8}
\]

The carrier `exp(i9alpha T/(2hbar))` is also common. Thus a disjoint-disk result applies equally before demodulation, assuming the same independently fixed alpha. The times are respectively `2e30`, `2e48`, and `2e66` in units hbar/alpha. These are mathematical observation schedules, not practical laboratory demonstrations.

At each k in {3,4,5}, compare the imaginary projections of the two rational scalar disks. Let `Delta_r=|Im center_(r,1)-Im center_(r,2)|`. If

\[
 m_r:=\Delta_r-R_1-R_2>0,
 \tag{AI2-F9}
\]

the full complex disks are disjoint and the actual two model predictions differ. This uses complete physical error, so it is stronger than a retained-matrix difference. When the margin is not positive, the certificate is insufficient; that does not prove equality of the actual models. Every row, including failures, is retained. Each positive margin tolerates an extra equal absolute error less than `m_r/2` per hypothesis. The output records that exact threshold.

The simple finite-time ratio intervals retain their cubic sine-remainder floor. The frozen scalar comparison may succeed even when these more conservative ratio intervals overlap. Such a result is pairwise discrimination of the two named hypotheses, not a certified continuous inverse for all eta and q.

The executed grid gives the following decisions for both B4 and B5:

| u | k=3 | k=4 | k=5 | Common physical time in hbar/alpha |
|---|---|---|---|---:|
| 10^-12 | insufficient disk separation | insufficient disk separation | insufficient disk separation | 2e30 |
| 10^-18 | insufficient disk separation | insufficient disk separation | **disjoint actual-model disks** | 2e48 |
| 10^-24 | insufficient disk separation | insufficient disk separation | insufficient disk separation | 2e66 |

All nine simple-ratio comparisons have overlapping intervals. At the successful cell, the recomputed depth-five region has 993 complete reference factors, 1,857 links and 1,171 retained omitted faces. The two disk radii are below `9.012e-27` and `4.762e-27`. The q4 imaginary-center difference is approximately `4.59184e-26`, leaving margin above `3.2145e-26`; q5 gives approximately `5.78231e-26`, leaving margin above `4.4050e-26`. Consequently the q5 test tolerates an additional equal absolute error strictly below `2.2e-26` on each hypothesis. Exact rational values, all separate costs and failed cells are in the output. This is a narrow successful finite-q discriminator for a pair that the fixed-z endpoint identifies as identical.

## Reproduction and boundaries

Run `python3 -B research/round27/forward/ai2/check.py --output /absolute/new/output-directory`. Fractions are authoritative; no floating arithmetic determines a verdict. The producer refuses existing or relative output paths. Snapshots include the frozen contract, instruction files, inherited physical sources and the actual additional Y1/Y2/AA2 dependencies used for the support and transfer argument. Normal and optimized Python are compared before freeze.

Extra absolute scalar uncertainty can be budgeted by (AI2-F9). Unknown timing and carrier calibration cannot silently be converted to this allowance: a full actual-model sensitivity theorem or independently bounded phase/time error is required. A phase uncertainty alone can be bounded conservatively using the connected-correlation norm bound, but no such instrument specification is supplied. Preparation, measurement, continuous parameter inversion, homogeneous generator matching and continuum Yang–Mills remain open. Priority is unverified.
