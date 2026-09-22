# Proposed AI3 contract: finite-time profile ratios after exact center cancellation

**Status: proposal, not frozen or executed.** Prepared after the advisor reported scoped AG2 admission. AG3 remains ahead of AI3 in the execution sequence. This source/planning pass adds zero physics loops. AI4 and the final two Round28 goals are not selected here.

## Named model and bounded target

Use the unchanged canonical summable full-link SU(2) model and the actual Round27 AI2 multipliers B4 and B5. Preserve fixed positive alpha, hbar and alpha/E_star; neither q nor eta is a lattice spacing. Reuse the proved sixteen-state averaged reached component and complete physical transfer, including exterior loading. No derivative of the true finite-q correlation is assumed.

**Target:** replace AI2's separate cubic sine budgets by a rigorous cancellation-aware finite-time center calculation; determine whether full-error ratio intervals distinguish the same-clock frozen hypotheses. Accept a substantive limited result if the retained Taylor floor is removed but the unchanged physical errors still prevent ratio discrimination. Such a result must quantify the remaining obstruction, not merely report a failed run.

## Freeze before producer execution

Keep AI2's physical X, Y4 and Y5 paths, norms `2 sqrt(2)`, ten-link union and complete-factor ownership. At `z=10^-6`, use

\[
H_1:(q,\eta)=(1-u,1/2),\qquad
H_2:(q,\eta)=(1-2u,1/16).
\]

The primary grid is exactly the inherited nine cells `u in {10^-12,10^-18,10^-24}`, `k in {3,4,5}`. Both hypotheses in each cell share the **same physical time**

\[
t_u=2\cdot10^{-6}u^{-3}\hbar/\alpha,
\]

respectively `2e30`, `2e48`, `2e66` in hbar/alpha units. The common alpha makes their carrier common. Do not retune either candidate's clock independently.

**Advisor-confirmed additional predeclared cell:** `(u,k)=(10^-24,6)`, using the same original physical time `2e66 hbar/alpha`. Its purpose is to test whether the existing depth-five spatial floor, rather than the canceled Taylor term, limits that case. Reconstruct its full collar and N6 from the actual ten-link seed; no extrapolated face count is allowed. The advisor accepted this extension before contract freeze, making ten planned cells; no producer result selected it. No further search grid or adaptive collar sweep belongs to this loop.

## Exact center calculation and valid inference

Reconstruct Q(q) and the two normalized source vectors from physical face flips. With `v=s_q(z)/96`, let `m_(n,r)=<psi_r,Q(q)^n psi_r>`. Independently establish `m_(1,5)-q m_(1,4)=0`, audit the inherited proposed identity

\[
\Delta m_3(q):=m_{3,5}-q m_{3,4}=2q^{13}(1-q^2),
\]

and derive the exact degree-five and degree-seven differences. Compute the signed imaginary center combination before taking a modulus:

\[
C^{(8)}(q,z)=-v^3\Delta m_3/3!+v^5\Delta m_5/5!
                 -v^7\Delta m_7/7!.
\]

Since Q is self-adjoint with norm at most six, retain the separate degree-eight exponential remainders; the combination costs at most `(1+q)(6v)^9/9!`. Prove any further `(1-q)` factor in a tail before using it. Vanishing finite coefficients alone do not prove all-order cancellation.

### Advisor-proposed optional all-order retained lemma

This is a feasible prospective proof route, **not an admitted lemma**. The producers must reconstruct the permutation of all sixteen cycles induced by reflection of the free cube in x. Establish that it fixes X as an unoriented cycle, exchanges Y4 and Y5, preserves every face-flip edge, and hence commutes with Q(1). For fundamental SU(2) characters, reversing a loop does not change its trace; verify that the chosen normalized source vectors are exchanged without a sign. This would prove `m_(n,5)(1)=m_(n,4)(1)` for every n, rather than merely for a tested finite moment list.

On `0<=q<=1`, the symmetric row-sum estimates `||Q(q)||<=6` and `||Q'(q)||<=30` would follow from at most six entries of weights q4/q5 in each row and their polynomial derivatives. With fixed, q-independent normalized source vectors, the matrix product rule then gives

\[
|m_{n,r}'(q)|\le n\,30\,6^{n-1}=5n6^n,
\qquad |\Delta m_n'(q)|\le(10n+1)6^n.
\]

Integrating the last inequality from q to one, after the reflection proof, yields the candidate estimate

\[
|\Delta m_n(q)|\le(1-q)(10n+1)6^n.
\]

For `x=6|v|<1`, the coefficients `(10n+1)/n!` decrease for n at least nine. Consequently an all-order upper bound for the combination tail beyond degree eight is

\[
\sum_{n\ge9}\frac{|v|^n|\Delta m_n(q)|}{n!}
\le\frac{(1-q)\,91x^9}{9!(1-x)}.
\]

Summing every n is conservative for an imaginary part, where only odd terms occur. Bound the moment polynomials at fixed sources first, then substitute the actual v(q,z); no derivative of v or of a physical correlation is required. This reflection is used only in the retained cube at q=1 and does not assert reflection invariance of the full anchored canonical model. The full physical-error contribution remains `R5+q R4`. If the exact permutation/source proof fails, fall back to the separately certified exponential tail above and record the failed hypothesis explicitly.

Let actual demodulated scalar imaginary values be y4,y5 and exact-center errors be e4,e5. **Retain**

\[
|e_5-q e_4|\le R_5+qR_4
\]

without a newly proved joint full-model error relation. The R terms contain the existing stationary-state, complete spatial and both-column averaging costs; arithmetic remains separately identifiable. Identical state-error upper bounds do not make the signed errors identical.

For each hypothesis construct a rigorous predicted interval for the observable ratio `y5/y4`. Its denominator interval must be positive. Compare both (a) cancellation-centered interval division and (b) all-corner division of the two exact polynomial-center intervals with complete disks. Report the sharper justified result. Separately bounding `y5-q y4` and y4 loses their shared e4 dependence and may be wider; do not mistake that bookkeeping loss for a physical obstruction.

The actual measured statistic `y5/y4` uses no unknown q. Any use of `y5-q_c y4` must explicitly index **candidate** q_c and compare with that candidate's prediction. Do not choose the true q, calibrate on it, and present the result as its discovery. Here the candidate set is the two frozen hypotheses, so even success is pairwise discrimination, not a continuous inverse theorem. Additional measurement, preparation, phase or timing uncertainty is unsupplied; state only the scalar tolerance a proved margin allows and the sensitivity theorem still needed to convert it.

## Required decisions and controls

- For every frozen cell report full-error ratio separation/overlap, denominator status, signed center cancellation, the old cubic budget, new arithmetic/tail cost, each unchanged physical cost, and original physical time. Retain every failed cell.
- Check the cubic sine sign, exact rational odd moments and candidate q dependence. Use formal q=1 only as a retained-component cancellation control, not a global endpoint Hamiltonian.
- Replace q5 face weight by q4 as a wrong-model control. Reject the incomplete eight-link seed and altered multiplier norms. If k6 is selected, verify all newly owned factors and retained faces.
- Exercise zero-crossing and signed-numerator interval division. Include adversarial error signs showing that equal radii do not imply cancellation, and the distinction between common carrier calibration and independent phase offsets.
- Preserve direct scalar-disk separation as an inherited baseline. A newly failed ratio does not undo an admitted scalar distinction; an overlapping sufficient ratio interval does not prove physical equality.
- If ratios remain insufficient, identify the dominant certified term and give an exact inequality showing why this stated interval method fails in each relevant cell. Do not call it an information-theoretic impossibility.

## Exact inputs to snapshot and bind

The advisor should hash the authoritative current bytes before execution. Each producer additionally inventories every file actually read; binding the gate alone is not enough when its proof dependencies are consulted.

```
AGENTS.md
.codex/skills/qeg-research-advisor/references/locality-and-computed-observables.md
research/round27/HANDOFF.md
research/round27/advisor/roadmap.json
research/round27/network.json
research/round27/advisor/ai1-gate.json
research/round27/advisor/ai2-gate.json
research/round27/contracts/ai2.json
research/round27/forward/ai1/report.md
research/round27/reverse/ai1/report.md
research/round27/forward/ai2/report.md
research/round27/forward/ai2/check.py
research/round27/forward/ai2/output/results.json
research/round27/reverse/ai2/report.md
research/round27/reverse/ai2/check.py
research/round27/reverse/ai2/output/results.json
research/round27/skeptic/ai2.md
research/round27/skeptic/ai2-independent-derivation.md
research/round27/forward/ai2/repairs/ratio-sign-repair.json
research/round26/forward/ad2/report.md
research/round26/reverse/ad2/report.md
research/round25/solo/aa1/output/results.json
research/round25/solo/aa2/report.md
research/round25/solo/aa2/check.py
research/round24/forward/y1/report.md
research/round24/forward/y2/report.md
papers/round27-addendum/ai2.tex
research/round28/experts/tesla/triage.md
research/round28/experts/tesla/ai3-contract-proposal.md
```

Also snapshot the newly frozen AI3 contract and the exact prospective Round28 skill instructions selected by the advisor. Current opposite-direction AI3 solutions remain unread until both freezes. Independent exact checkers and a separate skeptical review are required; inherited code may inform the source audit but is not an independent new implementation. AI4 is selected only after the admitted AI3 outcome and its dominant remaining error are known.
