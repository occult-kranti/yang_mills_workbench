# AI3 forward: exact retained cancellation, unchanged physical ratio obstruction

AI3 removes the crude cubic Taylor floor by exact moment calculation and proves the advisor's proposed all-order retained cancellation. **The complete physical ratio intervals nevertheless overlap in all ten frozen cells.** The inherited scalar distinction at `u=10^-18,k=5` remains valid for both actual Wilson multipliers. These are useful but limited results in the canonical summable full-link SU(2) model, at the fixed original physical clock. They neither prove equality of the candidates nor a general identification impossibility.

This is an independent forward implementation and derivation. The current reverse AI3 production remained unread through this freeze. The advisor supplied the prospective reflection lemma; the Tesla-method proposal supplied the candidate-indexed readout strategy. Neither was an admitted premise. Historical-source surveys motivate controls only and supply no Hamiltonian term or physical theorem. Prior accepted AA2/AD2/AI2 transfer arguments are shared inherited premises, not independently observed physics.

## 1. Actual physical sources and inherited full transfer

The free unit cube has origin `(3,1,0)`. Define X by the closed path

```
(3,1,0), (3,2,0), (3,2,1), (4,2,1),
(4,2,0), (4,1,0), (3,1,0).
```

Let f4 and f5 be the yz faces anchored at `(3,1,0)` and `(4,1,0)`, respectively. The simple six-cycles Y4=X symmetric-difference f4 and Y5=X symmetric-difference f5 give the actual multiplication observables

\[
B_r=(\chi_X+\chi_{Y_r})/\sqrt2,\quad
\psi_r=B_r\Omega=(e_X+e_{Y_r})/\sqrt2,\qquad r=4,5.
\]

Their mean is zero and their source norm is one: distinct cycle characters are orthogonal by the unmatched free-link center action. Conditional on the common four-link path, the exclusive two-link paths have independent Haar holonomies. The fundamental character has second moment one and fourth moment two, giving fourth moment `(2+6+2)/4=5/2` for each B. Its exact multiplication norm is `2sqrt(2)`, since the trace bound is approached on positive-Haar-measure neighborhoods of identity holonomies. In particular `||(B_r^2-I)Omega||^2=3/2`; source normalization does not justify a norm-one multiplier.

Each individual observable uses eight links; their union uses ten free factors. The checker reconstructs the complete cube from vertex walks, without importing an inherited implementation. Its sixteen simple six-cycles have reference energy `9alpha/2`. In the resulting order, X,Y4,Y5 have indices 10,6,9. The face-flip graph from either coherent source reaches all sixteen states. This is the **averaged reached component**, not the entire regional electric shell or an instantaneous invariant subspace.

The AA2 exterior-exclusion theorem applies to every vector in this component. The independent face-box enumeration recovers all twenty exterior touching faces. Each meets exactly one cube edge; the opposite edge is free and the two other sides have distinct outside factor owners. Removing an occupied shared spin-half edge saves at most 3/4, canceled by the free opposite edge's 3/4 cost; each charged side costs at least 1/8. Thus exterior touching faces add at least 1/4. Disjoint faces excite outside factors by at least 1/8, and the internal nonzero frequency changes `3-3r/2+2m` have magnitude at least 1/2. This verifies applicability of the inherited 1/8 participating-frequency bound to both sources, retaining all unaveraged exterior loading.

The full-link domains, actual strip gaps, finite-region pinching and strong averaging arguments are inherited from Y2/AA2. No finite matrix enumeration alone proves those facts. AD2 gives the correctly ordered reference identity

\[
e^{iEt/\hbar}\langle\Omega,B_r\beta_q^t(B_r)\Omega\rangle
=\langle\psi_r,Z_q(s)B_r Z_q(s)^*\Omega\rangle,
\qquad E=9\alpha/2.
\]

Both the source and vacuum evolution errors remain. With `J=2sqrt(2)`, stationary connected-state replacement costs `6J^2 dhat=48 dhat`, the spatial transfer costs `J^2 D=8D`, and averaging costs `(1+J)b_k<4b_k`, where `b_k=16 tau M_k(1+3zM_k)`. This is the complete inherited bound used below. Preparation, measurement and calibration uncertainty, if supplied, must be added separately.

## 2. Complete-factor collars through depth six

Reference factors are free singleton links or complete ten-link strips. A strip at `(4a,2b,c)` contains its six x links and four y links. Grow from the ten-link common seed by adjoining all owners of every omitted face meeting the complete current factors. An omitted face is retained exactly when every owner is included. The checker searches a finite bounding box containing every potentially incident positive-orthant face. Negative-coordinate faces are absent.

| k | Complete factors | Complete links | Retained omitted faces N_k |
|---:|---:|---:|---:|
| 0 | 10 | 10 | 2 |
| 1 | 41 | 113 | 25 |
| 2 | 149 | 329 | 143 |
| 3 | 333 | 675 | 359 |
| 4 | 610 | 1177 | 695 |
| 5 | 993 | 1857 | 1171 |
| 6 | 1497 | 2739 | 1808 |

Every owner, newly added owner, complete link and retained face is exported, not just its count. All six cube faces are retained by depth one. The eight-link B4 seed fails the actual B5 support test.

The Y1 connected-word proof uses at most forty incident faces per complete factor and at most three newly reached factors per interaction. Starting from ten factors, retaining every order, repetition, commutator factor two and time simplex gives coefficient `(10/3)_n/n!` in the variable `x=10 alpha tau |t|/hbar`. All full and regional words through degree k agree; every later word, including an exterior excursion and return, is bounded by one complete positive tail. At the frozen clock `x<=15z`, use

\[
D_k^{(10)}(15z)=\frac{(10/3)_{k+1}}{(k+1)!}
\frac{(15z)^{k+1}}{(1-15z)^{k+5}}.
\]

Taylor's positive remainder has denominator exponent `k+13/3`; replacing it by `k+5` is conservative. This is a complete factor/spatial estimate with infinite-dimensional onsite factors. It is not a representation cutoff or global propagator norm approximation.

## 3. Exact odd moments and a proved all-order retained lemma

The checker reconstructs every physical face flip. Q(q) has the weight `q^r` on a flip across a face of anchor sum r=4 or5 and zero otherwise. Its symmetric row norm obeys `||Q(q)||<=6`, and its polynomial derivative obeys `||Q'(q)||<=30` on `[0,1]`. Set

\[
p(q)=2+5q+5q^2+6q^3+3q^4,\quad
s_q=\frac{3z(1+q)^2(1+q^2)}{p(q)},\quad v=s_q/96,
\]
\[
h_r=\langle\psi_r,e^{ivQ(q)}\psi_r\rangle,
\quad m_{n,r}=\langle\psi_r,Q(q)^n\psi_r\rangle,
\quad \Delta m_n=m_{n,5}-q m_{n,4}.
\]

Polynomial propagation uses exact integer powers of formal q and rational coefficients, before evaluating any grid point. It gives

\[
\begin{aligned}
\Delta m_1&=0,\\
\Delta m_3&=2q^{13}-2q^{15},\\
\Delta m_5&=12q^{21}+8q^{22}-8q^{24}-12q^{25},\\
\Delta m_7&=54q^{29}+72q^{30}+110q^{31}
              -110q^{33}-72q^{34}-54q^{35}.
\end{aligned}
\]

The degree-eight complex centers P_r retain the alternating imaginary signs:

\[
\operatorname{Im}P_r=vm_{1,r}-v^3m_{3,r}/6+v^5m_{5,r}/120-v^7m_{7,r}/5040,
\]
\[
C:=\operatorname{Im}P_5-q\operatorname{Im}P_4
=-v^3\Delta m_3/6+v^5\Delta m_5/120-v^7\Delta m_7/5040.
\]

The sign of the cubic contribution is negative for `0<q<1`. All source moment polynomials through degree eight and both real and imaginary centers are exported as exact fractions.

The reflection `(x,y,z)->(7-x,y,z)` maps cube edges to cube edges, fixes X as an unoriented cycle, and exchanges Y4 and Y5. In the complete retained basis its exact permutation is

```
[15,14,2,12,11,5,9,8,7,6,10,4,3,13,1,0].
```

Every one of the 256 matrix entries verifies `P Q(1) P^-1=Q(1)`. Fundamental SU(2) loop traces are unchanged by reversal, so the coherent sources exchange with no sign. Therefore `m_(n,5)(1)=m_(n,4)(1)` for **every n**. This proof does not rely on the finite exported moment list. Weighted Q(q) does not share the reflection away from the endpoint; neither is the full anchored canonical Hamiltonian asserted reflection invariant or defined at q=1.

The sources are fixed and normalized, independently of q. The matrix product rule gives, for n>=1,

\[
|m'_{n,r}(q)|\le n\,30\,6^{n-1}=5n6^n,
\quad |\Delta m_n'(q)|\le(10n+1)6^n.
\]

Combining this with `Delta m_n(1)=0` and integrating the polynomial derivative from q to1 yields

\[
|\Delta m_n(q)|\le(1-q)(10n+1)6^n.
\]

For `x=6|v|<1`, the coefficients `(10n+1)/n!` decrease from n=9: the necessary difference is `10n^2+n-10`, which at n=m+9 is `10m^2+181m+809>0`. Bounding all n>=9, conservatively including the even powers, proves

\[
|\operatorname{Im}h_5-q\operatorname{Im}h_4-C|
\le T_\Delta:=\frac{(1-q)91(6|v|)^9}{9!(1-6|v|)}.
\]

This establishes the advisor's proposed lemma within this retained problem. Only fixed-source moment polynomials were differentiated; neither the physical value disks nor v(q) were differentiated. Each separate scalar center also has the unitary Taylor bound `A=(6|v|)^9/9!`. Under H1, A is approximately `1.334e-70`, whereas T_Delta is approximately `1.214e-80`, `1.214e-86` and `1.214e-92` at the three u scales. No reduction of physical error follows from this arithmetic improvement.

## 4. Full physical errors and two valid predicted ratio intervals

Use the actual b(q), coupling tau and stationary-state estimate

\[
b(q)=\frac{p(q)}{24(1-q)^3(1+q)^2(1+q^2)},\quad
\tau_q=\frac{\eta}{8b(q)},\quad
\widehat d_q=\frac{\tau_q\sqrt{b(q^2)/96}}{(1-\eta)/8},
\quad M_k=N_k/24.
\]

Integer square-root brackets with binary denominator `2^320` certify an upward value for dhat. The complete physical scalar radius is unchanged:

\[
R_{\rm phys}=48\widehat d_q+8D_k^{(10)}(15z)
             +64\tau_qM_k(1+3zM_k).
\]

Let `c_r=Im P_r` and let y_r be the imaginary part of the actual full connected correlation after the common known carrier is removed. The two separate scalar intervals are

\[
I_r=[c_r-(R_{\rm phys}+A),c_r+(R_{\rm phys}+A)].
\]

Every frozen denominator I4 has a strictly positive lower endpoint. The **all-corner ratio interval** is the minimum and maximum of `n/d` over both endpoints of I5 and I4. It is the exact range over that rectangular error enclosure, including signed numerator cases. Rectangular bounds need not describe the actual joint error set sharply, but no smaller joint set has been proved here.

The separate **cancellation-centered interval** starts from

\[
|y_5-qy_4-C|\le (1+q)R_{\rm phys}+T_\Delta.
\]

Divide this numerator interval by I4 using all corners, then add q. The full physical combination error remains `R5+qR4=(1+q)R_phys`. Equal radii do not imply equal signed errors; the worst choice `e5=R,e4=-R` attains `(1+q)R`. The same e4 enters the numerator and denominator, so independently enclosing them may lose dependence information. We consequently do not call this cancellation box sharp. Both intervals are reported; all-corner division of the original scalar boxes is slightly tighter on this grid.

The statistic **y5/y4 contains no unknown q**. A candidate q_c may index predictions or the residual `y5-q_c y4`; it cannot be secretly supplied to the measurement from the true unknown model. The inference here compares only the two frozen candidates. There are no measured data or derivative observations.

The old cubic comparator retains `|Im h_r-vq^r|<=36v^3` and uses intervals centered at `vq^r` with radius `R_phys+A+36v^3`. It is recalculated on the same ten cells, with complete denominator and signed-corner handling. All three methods retain all physical errors.

## 5. Ten frozen cells and the quantified remaining limitation

Throughout, `z=10^-6`. For each u compare

\[
H_1:(q,\eta)=(1-u,1/2),\qquad H_2:(q,\eta)=(1-2u,1/16).
\]

Both have `eta(1-q)^3=u^3/2`, and thus exactly the same physical time

\[
t_u=2\cdot10^{-6}u^{-3}\hbar/\alpha.
\]

The times are `2e30`, `2e48`, `2e66` in units hbar/alpha. Alpha, hbar, alpha/E_star and spacing remain fixed and positive. The time is not adjusted independently for either candidate. The sole extra cell `(10^-24,6)` was declared before production.

For intervals J1,J2 define the signed separation margin `max(lower1-upper2, lower2-upper1)`; positive means disjoint and negative means this interval certificate overlaps. Fractions determine every sign. The displayed decimals are approximate.

| u | k | All-corner ratio margin | Crude cubic margin | Dominant physical term H1 / H2 | B4,B5 scalar test |
|---:|---:|---:|---:|---|---|
| 1e-12 | 3 | -3.811493484e-9 | -3.811513893e-9 | spatial / spatial | insufficient |
| 1e-12 | 4 | -1.044822364e-9 | -1.044842772e-9 | state / state | insufficient |
| 1e-12 | 5 | -1.044761496e-9 | -1.044781904e-9 | state / state | insufficient |
| 1e-18 | 3 | -2.766731990e-9 | -2.766752399e-9 | spatial / spatial | insufficient |
| 1e-18 | 4 | -6.086906259e-14 | -8.127722585e-14 | spatial / spatial | insufficient |
| 1e-18 | 5 | -1.313885034e-18 | -2.040947715e-14 | state / spatial | both disjoint |
| 1e-24 | 3 | -2.766731990e-9 | -2.766752399e-9 | spatial / spatial | insufficient |
| 1e-24 | 4 | -6.086901682e-14 | -8.127718009e-14 | spatial / spatial | insufficient |
| 1e-24 | 5 | -1.268122540e-18 | -2.040943139e-14 | spatial / spatial | insufficient |
| 1e-24 | 6 | -2.436389698e-23 | -2.040816329e-14 | spatial / spatial | insufficient |

The cancellation-centered margin is also negative in every row; its exact endpoints and margins are exported. Removing the Taylor floor materially sharpens the last row, but its physical ratio width still exceeds the candidate q difference.

All individual state, spatial, averaging and arithmetic terms are in `output/results.json`. Three informative complete-budget cases are:

* At `u=1e-12,k=5`, H1/H2 state radii are about `5.237229366e-18` and `9.875414398e-19`, while each spatial radius is `3.774177199e-27`. The state bound limits the ratio long before arithmetic matters.
* At `u=1e-18,k=5`, the state radii are `5.237229366e-27` and `9.875414398e-28`, each spatial radius is `3.774177199e-27`, averaging is about `1.784642141e-51`, and scalar arithmetic is about `1.333781367e-70`. Complete radii are `9.011406565e-27` and `4.761718639e-27`. Scalar margins remain positive: B4 about `3.214524214e-26` and B5 about `4.405000405e-26`. Yet their ratio intervals overlap.
* At `u=1e-24,k=6`, each spatial radius is `7.548467626e-32`; state radii are `5.237229366e-36` and `9.875414398e-37`, averaging is about `2.755670260e-69`. Complete radii are `7.548991349e-32` and `7.548566380e-32`. The new combined arithmetic tail is about `1.214e-92` for H1. The limitation is spatial, not retained Taylor cancellation.

For every cell the output additionally recalculates the same center boxes with just one physical component at a time. These are explicitly **diagnostics of the bound**, never admitted replacements for the full error. They yield exact negative inequalities identifying sufficient floors: at `u=1e-18,k=5`, the state-only ratio margin is approximately `-4.576149531e-20` and the spatial-only margin `-2.681235390e-19`. Thus each inherited component by itself still prevents this particular interval separation. At `u=1e-24,k=6`, the spatial-only margin is `-2.436285122e-23`, whereas the state-only margin is positive, about `9.989542385e-25`. This isolates the relevant bound to improve without choosing or executing a later loop.

No ratio cell earns a positive additional-error allowance. The retained scalar success does: each extra absolute scalar error may be strictly less than half its scalar margin, separately for each hypothesis. For B5 that threshold is about `2.202500202e-26`. This is a mathematical allowance, not instrument sensitivity. The checker includes a generic positive-margin interval fixture exercising a sufficient extra-error formula; it is not an additional physical cell. If a ratio margin m were positive, with each denominator bounded below by d_i and scalar endpoint magnitudes bounded by D_i,N_i, the constants `K_i=2(D_i+N_i)/d_i^2` ensure that choosing `epsilon<=min(d_i/4,m/[2(K1+K2)])` preserves at least half the margin. The actual ten ratio results supply no such positive m.

## 6. Executed controls and evidence boundary

The independently written controls include:

* Replacing every q5 face weight by q4 makes the retained first-moment ratio one and violates `Delta m1=0` at q=1/2. It does not prove all other q dependence disappears.
* Exact integer powers of i verify the alternating signs; the nonzero Delta m3 at q=1/2 rejects the wrong cubic sign.
* The complete reflection permutation establishes every-order equality. A separate two-measure fixture matches moments zero through three but disagrees at four, rejecting inference from finite coincidence alone.
* The actual ten-link support rejects the old eight-link seed. The Haar fourth moment and identity-holonomy norm reject rank-source/multiplier-factor substitutions.
* A three-state unitary fixture has an exact source column but a nontrivial vacuum column; dropping the latter changes the scalar from `-1/5` to1. This tests the omitted-column inference, not the actual Hamiltonian's numerical dynamics.
* Opposing signed errors with equal radii attain the full physical combination sum. A separate residual/denominator fixture displays the loss from forgetting shared e4 dependence.
* A candidate-indexed residual changes when q_c changes while the measured ratio stays fixed. Signed numerator, denominator crossing and Boolean endpoint controls exercise interval semantics.
* Common rotation by i preserves complex disk distances but changes a raw imaginary ratio from2 to1; independent rotation of one probe changes it to10. Thus the common **known** carrier can be demodulated consistently. An unknown common phase is not harmless to an imaginary-only ratio, and independent phases cannot be fitted away.

The final checker uses explicit exceptions that remain active under Python optimization. All scientific arithmetic is rational; floating conversion is confined to labeled displays. The 40 contract sources, contract, consulted instruction snapshots and snapshot event precede production. `inputs/source-inventory.json` binds 68 copied files; additional bundled instructions are preserved prospectively even when no result depends on them. The initial successful run is preserved under `runs/initial/`; the final run adds exact sign controls, a positive-margin interval fixture and per-component diagnostics without changing physical bounds, cells or conclusions. Replays and these control refinements count as validation of AI3, not new loops.

Reproduce with:

```
python -B research/round28/forward/ai3/check.py --output /absolute/fresh/output
python -O -B research/round28/forward/ai3/check.py --output /absolute/other/fresh/output
```

`freeze.json` records fresh normal/optimized equality and hashes for the checker, report, outputs and complete source closure. This is an exact retained cancellation derivation plus a quantified insufficient full-ratio certificate, conditional on the inherited canonical transfer theorems. No continuous inverse, realized apparatus, independently calibrated alpha, homogeneous-model matching, nontrivial continuum construction or Yang–Mills mass-gap solution follows. Scientific priority is unverified. AI4 and the later goals remain unselected here.
