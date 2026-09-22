# AL2 forward: HNM scale-invariant eligibility and deformation bound

Human project author: **Hruday N M (BUNZEEY)**. This is the independent forward derivation under the frozen AL2 contract, before reading the current reverse or skeptic results. The label denotes a project result, with scientific priority unverified.

**A common positive energy rescaling or additive scalar does not repair the AL1 coupling-ratio obstruction.** Changing the magnetic coefficient independently can enter the sufficient region, but is an action deformation. The following is an if-and-only-if statement about inherited sufficient membership, not a criterion for an actual spectral gap.

Let `g,a,E_star,hbar` be strictly positive, let `alpha=g²/(2a)`, `lambda=2/(g²a)`, and let `c1,c2` denote the positive unevaluated I1 source constants. For `k>0` and real C, the operator `H'=kH+CI` has `alpha'=kalpha`, `lambda'=klambda`, `delta'=kdelta`, so

\[
{\lambda'\over\alpha'}={\lambda\over\alpha},\qquad
\tau'={24\lambda'\over\alpha'}=\tau,\qquad
\epsilon'=7|\tau'|=\epsilon.
\tag{HNM-AL2.1}
\]

The scalar cancels under actual ground subtraction: `E0'=kE0+C` and `H'-E0'=k(H-E0)`. Thus a scalar alone does not change gaps. Positive common multiplication does scale physical gaps, even though it preserves eligibility ratios. At fixed hbar and the same physical time it changes evolution; equivalent time parameters obey `t'=t/k`. At fixed `E_star`, `alpha'/E_star=kalpha/E_star`, so this is not secretly the same fixed physical energy calibration. A mere units conversion would convert the reference unit as well and would still preserve every eligibility ratio.

Now hold alpha fixed and take `lambda_s=s lambda`, uniformly on both selected and omitted original plaquettes. For `s>0`, exact AL1 membership is equivalent to

\[
0<s\le {g^4\over32},\qquad
s<{c_1g^4\over672},\qquad
s<{g^4\over1344c_2}.
\tag{HNM-AL2.2}
\]

If the word suppression is used, impose additionally `s<=1`; that linguistic restriction is separate from the theorem inequalities. Necessity follows from the selected bridge ratio `4s/g⁴<=1/8`, normalized omitted norm `672s/g⁴<c1`, and the positive half-gap condition `672c2s/g⁴<1/2`. Sufficiency follows by reversing these steps: the endpoint condition is weaker than the bridge condition, all complete support/domain/boundary premises remain those of AL1, and the two strict source inequalities are exactly retained. Equality is permitted only at the selected bridge cap, not at either omitted cap.

In particular every eligible `s(g)` along `g->0` obeys `0<s(g)<=g⁴/32`, hence tends to zero. On AL1's exact sequence, `s_n<=1/(32n²)`. The needed change is therefore not a uniformly small relative correction to the magnetic coefficient: its retained fraction vanishes. Writing an HNM label or auxiliary parameter does not produce physical equivalence. This does not exclude a continuum construction through a different proof regime.

At `s=0`, the formal inequalities hold, but the nonzero omitted interaction requested for I1 is absent. The model becomes the all-free electric reference (selected terms also vanish), with its inherited tensor-product vacuum and gap; it is a degenerate control, not a successful nonzero homogeneous bridge. Negative s is outside the declared nonnegative uniform branch. A zero or negative k is not an allowed positive common energy rescaling; k=0 destroys the reference gap and k<0 reverses lower-boundedness. Zero physical normalization is rejected.

The exact checker verifies the two formulations of membership over rational diagnostic constants and coefficients, including isolated strict-threshold equality controls. Those rational constants are **test parameters**, never evaluated Yarotsky constants. It separately tests scalar centering and physical-clock mismatch, the omitted bridge, and the misleading identification of magnetic-only suppression with a units conversion. No SU(2) truncation or numerical mass calculation is performed.

The incremental result beyond AL1 is the invariance statement and the required deformation fraction, rather than a new mass-gap theorem. Newton's inverse-map discipline identifies what scale changes cannot alter; Tesla's energy/clock accounting keeps the physical generator fixed. The next missing premise is still an actual full-model quantitative stability interval or a different matched continuum strategy.

Reproduce: `python -B research/round29/forward/al2/check.py --output /absolute/new/output`.
