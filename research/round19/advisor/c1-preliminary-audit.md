# C1 preliminary advisor audit

Status: preliminary audit only. This is not a C1 gate and does not freeze C2.

## Current evidence inspected

I inspected the current forward and reverse C1 outputs after the first root-flagged repairs. The artifacts are active prelock outputs; both normal and optimized role checkers currently replay byte-for-byte to their saved output directories. The current final forward-vs-reverse comparator does not accept yet.

Inspected scope sources:

- `advisor/contract-c1.json`
- `advisor/b2-gate.json`
- `methods/round19-lessons.md`
- `forward/c1/check.py`, `forward/c1/report.md`, normal/optimized outputs
- `backward/c1/check.py`, `backward/c1/report.md`, normal/optimized outputs
- `backward/c1/compare.py`, current self-comparison

## Mathematical findings so far

The core C1 values are consistent between the two scientific implementations. Both reconstruct the 18-vertex, 33-edge, 20-face graph with three active vertical links, seven affected faces, thirteen constant faces, and the reduction

\[
S=3x+y+z+w+t.
\]

Both keep the observable

\[
O=(4x^2-1)^3(4w^2-1)/81.
\]

Both report 6054 exact moments through max total degree 16. Compared as a set keyed by exponent vector, the forward and reverse moment tables have no missing exponents, no extra exponents, and no value mismatches. The Taylor coefficient rows through degree 8 agree exactly, including

- `N0=0`, `N1=0`, `N2=1/324`, `N3=13/1296` for numerator Taylor coefficients;
- `Z0=1`, `Z1=0`, `Z2=13/8`, `Z3=1/4` for partition Taylor coefficients.

The exact common-V discriminator is present:

\[
E[x z w t]=1/64,
\]

while independent V-resampling gives `0`. This supports the intended failed-independence exception. Both signs at `kappa=±1/64` are enclosed with target width, and the intervals are disjoint, so the static sign asymmetry is real at the point fixture. Reverse additionally records the first odd coefficient evidence behind the asymmetry.

The current reverse proof/control semantics are substantially stronger than the earlier flagged draft: it has actual exponent/kappa validators, positive partition denominator checks in interval division, a geometric exponential tail condition `M<1/2` for the actual `M=7/64`, a coefficient-convolution freeze-W regression, a noncommuting signed-word fixture, and explicit static scale wording.

The current forward proof/control semantics have also improved: scale controls call `validate_kappa`, the signed quaternion fixture is now present at top level, `K_m1_coeff` is corrected to `kappa^2*(1+y)/4`, interval division checks positive denominator intervals, and normal/optimized outputs replay deterministically.

## Current blockers before any gate

1. The current forward-vs-reverse comparison rejects. A fresh ordinary run of `backward/c1/compare.py` against `forward/c1/output` reports admission failures: `moments`, `intervals`, `primary_normalized_interval`, `negative_kappa_fixture`, and `freeze_W_identity_regression`.
2. The moment failure is not a mathematical mismatch: the two 6054-row moment tables agree exactly as exponent-keyed sets, but their list order/schema differ. The final comparator should canonicalize by exponent vector rather than compare list order.
3. The interval failure is not presently a contradiction: forward uses a wider rigorous tail enclosure and reverse uses a tighter geometric enclosure. The forward positive and negative final intervals contain the reverse intervals. The final gate needs a clear rule: either require a shared canonical interval method, or compare exact partial coefficients plus prove each reported interval is valid and meets target. Exact equality of interval JSON from different rigorous bounds is too brittle unless made part of the producer contract.
4. The freeze-W regression still differs by representation. Reverse proves the regression through exact coefficient convolution for `exp(kappa*(S_old+1)) = exp(kappa) exp(kappa*S_old)`. Forward currently checks coefficient equality to the Round18 C2 V-only-2 arrays and interval overlap. The coefficient evidence is useful, but interval overlap alone is not an exact regression proof. Final comparison should require the analytic constant-cancellation/convolution statement or an equivalent exact coefficient identity, not just overlap.
5. Some forward controls remain thin as standalone evidence, especially `conditional_weight_not_bare_Haar` recorded as a hard-coded true with metadata. This can be acceptable only if the final independent comparison reconstructs and mutates the corresponding coefficient/outer-weight semantics; it should not be accepted from the producer boolean alone.
6. C1 remains a static mathematical checkpoint. Static `kappa=1/64` is not `E_star`, not physical time/energy matching, and cannot close the common physical scale analogy.

## Provisional C2 planning consequence

Do not freeze C2 yet. If C1 gates with the current coefficient structure intact, the strongest next-loop candidate is not another point `kappa=1/64` run. The actual coefficients support investigating a continuous static-kappa certificate, for example a proof over `|kappa|<=1/8` with `F(kappa)>=kappa^2/2048` and a separate signed-asymmetry certificate from the cross-difference `N(k)Z(-k)-N(-k)Z(k)`. That remains a candidate only until C1 final evidence is accepted.
