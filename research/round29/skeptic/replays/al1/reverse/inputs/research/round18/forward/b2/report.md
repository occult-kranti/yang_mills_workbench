# B2: a full physical gap on the signed dense two-cube coefficient box

This loop proves a sufficient lower bound for the **full untruncated physical Hamiltonian on one fixed twelve-vertex, twenty-link, eleven-face graph**. It uses the accepted B1 theorem as a source-bound premise. It does not replace the omitted space by a numerical truncation, establish a homogeneous volume-uniform gap, or complete continuum Yang–Mills theory.

For every real coefficient vector with \(|\lambda_p|\leq3\alpha/8\), \(\alpha>0\), the conclusion is

\[
 \Delta\geq\alpha R_*,\qquad
 R_*={27-3\sqrt{70}\over16}>0.
\]

For arbitrary signs at **all eleven endpoint magnitudes**, \(|\lambda_p|=3\alpha/8\), the stronger conclusion is

\[
 \Delta\geq\alpha D_*,\qquad
 D_*={3+15\sqrt3-3\sqrt{70}\over16}>R_*.
\]

Exact outward rational enclosures give \(R_*\approx0.118762450248608\), \(D_*\approx0.242560082344431\). Their widths are respectively \(3/2^{52}\) and \(18/2^{52}\), both below the frozen dimensionless target \(10^{-12}\). These intervals enclose **analytic lower-bound expressions**, not the actual physical gap: their upper endpoints are not upper bounds on \(\Delta\).

## 1. Operator, domain and accepted premises

Use normalized product Haar measure and

\[
 \mathcal H_{\rm phys}=L^2(SU(2)^{20})^{SU(2)^{12}},\quad
 H=H_0+V=\alpha\sum_e C_e-\sum_{p=1}^{11}\lambda_p x_p,
 \quad x_p=\tfrac12\operatorname{Tr}U_p.
\]

All vertices impose Gauss law; no external charges or omitted boundary Gauss constraints are allowed. The positive link Casimir has eigenvalues \(j(j+1)\). The finite product of compact groups gives a self-adjoint positive elliptic \(H_0\) with compact resolvent. Real Wilson multiplication is bounded, with \(\|V\|\leq\sum_p|\lambda_p|\); hence the sum is self-adjoint on \(D(H_0)\), has the same closed form domain, and retains compact resolvent. Gauge transformations commute with both terms, so the closed physical subspace reduces the operator. The physical eigenvalues \(E_0\leq E_1\leq\cdots\) count multiplicities.

Let \(\Omega=1\), \(\chi_p=2x_p\), and let \(P\) project onto the twelve orthonormal states \(\Omega,\chi_1,\ldots,\chi_{11}\). Put \(Q=I-P\). The local frozen copies `premises/b1-gate.json`, `b1-report.md`, and `graph.json` bind the following B1 premises:

* The **entire physical complement**, including all spin representations and intertwiners, obeys \(QH_0Q\geq(9\alpha/2)Q\). The proof classified every support with at most five active links, every elementary four-cycle, and the associated degree-two intertwiners; a six-link Wilson state attains the threshold.
* \(H_0\chi_p=3\alpha\chi_p\), and all face-to-face matrix elements of \(PVP\) vanish. The remaining vacuum-to-face entries are \(-\lambda_p/2\).
* For \(W=QVP\), the vacuum row and column of \(W^*W\) vanish. Its face block has diagonal \(\sum_q\lambda_q^2/4\) and off-diagonal \(\lambda_p\lambda_q/4\). Thus, if \(r=\max_p|\lambda_p|/\alpha\),
  \(\|QVP\|^2\leq21\alpha^2r^2/4\), valid for arbitrary signs and unequal magnitudes.
* \(\langle\Omega,H\Omega\rangle=0\).

The old geometry file retains its original Euclidean metadata, including `time_generator:none`. Only its actual incidence, oriented loops, and unweighted Haar inner products are reused. The displayed physical Hamiltonian explicitly defines \(\alpha,\lambda_p\); it is not derived from those old Euclidean labels. The B1 amendment remains applicable: independent one-face Haar variables really agree through degree four, a Gaussian fourth moment does not, and six-face products distinguish the full joint measure. No incorrect independence claim is used here.

## 2. The codimension-one form, in both proof directions

**Backward obligation.** A lower bound for the full \(E_1\) can be obtained by finding a lower quadratic-form bound on one codimension-one subspace. The subspace need not be perpendicular to the unknown interacting ground state. Choose \(\Omega^\perp\).

**Forward derivation.** For a form-domain state \(\psi\perp\Omega\), set \(u=P\psi\) and \(v=Q\psi\). Then \(u\) contains only face coordinates. Consequently,

\[
 \langle u,Hu\rangle=3\alpha\|u\|^2,
 \quad \langle v,Hv\rangle\geq\alpha c\|v\|^2,
 \quad |\langle v,Vu\rangle|\leq\alpha b\|u\|\|v\|,
\]

where

\[
 c={9\over2}-11r,\qquad b={\sqrt{21}\over2}r.
\]

The electric cross form is zero because \(P\) is an \(H_0\)-reducing finite spectral subspace. The full form therefore satisfies

\[
 {\langle\psi,H\psi\rangle\over\alpha}
 \geq3X^2+cY^2-2bXY,
 \qquad X=\|u\|\geq0,\quad Y=\|v\|\geq0.
\]

The lower eigenvalue of the auxiliary scalar matrix \(\bigl(\begin{smallmatrix}3&-b\\-b&c\end{smallmatrix}\bigr)\) is

\[
 R(r)={3+c-\sqrt{(3-c)^2+21r^2}\over2}.
\]

Thus the form is at least \(\alpha R(r)\|\psi\|^2\). The variational principle now gives

\[
 E_1=\sup_{\dim L=1}\inf_{\psi\perp L}{\langle\psi,H\psi\rangle\over\|\psi\|^2}
 \geq\alpha R(r).
\]

Separately, the bare-vacuum trial gives \(E_0\leq0\). Hence \(\Delta=E_1-E_0\geq\alpha R(r)\). A positive bound also proves a simple ground eigenvalue: a multiplicity of two would give \(E_1=E_0\leq0\), contradicting \(E_1>0\).

This meeting of forward premises and backward variational obligations is an ordinary complete form argument. It is not a bidirectional search certificate that invents a missing premise, and the twelve-dimensional trial spectrum is not substituted for \(E_1\).

## 3. Analytic coverage of the entire signed box

For \(0\leq r\leq3/8\), \(c\geq3/8\) and \(b\leq3\sqrt{21}/16\). Because \(X,Y\) are nonnegative norms,

\[
3X^2+cY^2-2bXY
\geq3X^2+{3\over8}Y^2-{3\sqrt{21}\over8}XY.
\]

This is a comparison on the nonnegative norm pair. **It is not a Loewner ordering of the varying scalar matrices on arbitrary signed scalar vectors.** The endpoint matrix itself is a symmetric matrix whose lower eigenvalue is

\[
 {27-3\sqrt{70}\over16}=R_*.
\]

Its determinant is \(99/256>0\), and \(R_*>0\) follows exactly from \(81>70\). These inequalities cover every one of the eleven real coefficients, not merely the sampled diagonal families. Degenerate cross blocks, zero coefficients and \(r=0\) require no division by \(b\); the code obtains \(R(0)=3\) exactly.

If every member of a family has \(\alpha\geq\alpha_{\min}>0\), this proof gives the common physical floor \(\alpha_{\min}R_*\). A positive dimensionless constant alone would not give such a floor if \(\alpha\to0\). Even with a common floor, this remains a fixed-graph family, not a statement across growing volumes.

## 4. Independent use of the ground-state trial

The exact twelve-state compressed matrix has the arrowhead form with vacuum energy zero, eleven equal face energies \(3\alpha\), and couplings \(-\lambda_p/2\). Its smallest eigenvalue supplies a **ground-energy upper bound**

\[
 E_0\leq E_{\rm trial}={3\alpha-\sqrt{9\alpha^2+\sum_p\lambda_p^2}\over2}.
\]

This statement is an upper bound from a trial subspace; it is not a lower bound for the full spectrum. Combining it with the independently established full \(E_1\) lower bound yields an instance-specific lower bound for the physical gap. At all endpoint magnitudes,

\[
 \sum_p\lambda_p^2={99\over64}\alpha^2,
 \qquad E_{\rm trial}={24-15\sqrt3\over16}\alpha<0.
\]

Its negativity is certified by \(675>576\). Subtracting this upper bound from \(\alpha R_*\) proves \(\Delta\geq\alpha D_*\). The argument depends only on the squared coefficients at this step, so allplus, allminus and alternating endpoint signs are equally valid.

## 5. Exact arithmetic, decisive controls and retained failure

The producer recognizes exact rational squares, then otherwise uses an integer square root on a denominator \(2^{48}\). Each radical is bounded by exact squaring, and each scalar lower bound passes the two diagonal and determinant conditions for a positive-semidefinite shifted matrix. The independent reviewer uses rational Newton brackets and separate scalar identities; those checks are not counted as author checks.

The complete collection retains the frozen samples \(r=0,1/8,1/4,12/43,1/3,3/8,2/5,1/2\). The first six lie in the accepted box; the final two are outside it and have negative, insufficient scalar lower bounds. A negative lower bound is not a proof of a closed physical gap. The samples illustrate the curve; Section3 supplies the continuum of coefficient values. The CSV contains exact rational interval endpoints for the formula, not measured eigenvalues or stochastic confidence intervals.

Eleven parameter fixtures include three endpoint sign patterns, zero, sparse and mixed interior vectors, two physical scales with declared common floors, the two outside cases, and one deliberately coarse endpoint. With zero precision bits, the actual radical enclosure gives \(R_*\in[0,3/16]\), which cannot numerically certify strict positivity or the requested precision. This is retained as an `insufficient-precision` result while the exact analytic proof remains valid.

Three concrete inference controls are kept separate from computed Yang–Mills eigenstates:

1. Deleting the cross term would suggest the scalar lower bound \(3/8\) at the endpoint. The actual endpoint scalar form on \((1,\sqrt{21})\) has Rayleigh quotient \(3/22<3/8\), so that scalar shortcut fails.
2. Without \(\psi\perp\Omega\), the bare vacuum has quadratic form zero, refuting the claimed face-only value \(3\alpha\). Omitting a face from \(P\) similarly leaves an actual energy-\(3\alpha\) state in the purported \(9\alpha/2\) complement.
3. A separate matrix \(\operatorname{diag}(0,1/8,3)\) has full gap \(1/8\), while its first-and-third-coordinate trial space has Ritz gap3. This rejects the generic Ritz-gap-to-full-gap substitution.

The independent verifier found a genuine implementation error before freeze: changing the module's mutable `REQUIRED_PREMISES['complement_is_full_Q']` to false could redefine the accepted premise without changing the source file. The original implementation and reproduced failure are preserved under `history/`. The correction binds all premise metadata, source pins, the target and sample inventory to an immutable canonical snapshot before certificate admission. Four regression controls now reject those runtime changes. This repair changes certificate integrity; it does not alter the spectral formulas or numerical values. Additional focused checks reject missing premises, omitted fixtures, falsely passing outside-box labels, Boolean precision aliases, invalid scales and incomplete coefficient vectors.

## 6. Physical matching and the unresolved backward bridge

The advisor's targeted review of [Bauer, D’Andrea, Freytsis and Grabowska, *A new basis for Hamiltonian SU(2) simulations*](https://arxiv.org/pdf/2307.11829), equations55–56, supplies

\[
 H_E={g^2\over2a}\sum_e C_e,\quad
 H_B={1\over2g^2a}\sum_p\operatorname{Tr}(2I-U_p-U_p^\dagger).
\]

For \(SU(2)\), the trace in the second expression is \(4-4x_p\). Removing the additive constant \(2N_p/(g^2a)\), which leaves all gaps unchanged, gives

\[
 \alpha={g^2\over2a},\quad\lambda={2\over g^2a},\quad r={4\over g^4}.
\]

The arithmetic was checked independently here. On this standard positive homogeneous branch, membership in the chosen box requires \(g^4\geq32/3\). It therefore does not cover the weak-bare-coupling path \(g\to0\). Failure of applicability is not evidence that a continuum mass gap is absent. The signed coefficient box is a mathematical extension beyond the usual positive homogeneous bare coupling. The inhomogeneous summable family from GoalA has its own coefficient assignment and cannot silently substitute for that branch.

Reading depth: the supplied advisor source note and displayed Hamiltonian equations were used; this forward loop did not reproduce the paper's basis construction or numerical claims. No source gap constant was imported.

## Reproduce and inspect

Run `python check.py --output ../b2-output` and `python -O check.py --output ../b2-output-optimized` from this directory. All code uses the Python standard library. Outputs must be outside immutable sources. `collection.json` contains the full eleven-fixture and eight-sample inventory; `coupling.csv` carries exact plot data; `results.json` names the **43 author checks**. `source-manifest.json` and the output manifest bind source and evidence bytes. The `history/` implementation is retained evidence of a repaired defect and is not an active dependency.

The independent complete comparison and the advisor gate are separate acceptance steps. C1 has not been executed by this loop.
