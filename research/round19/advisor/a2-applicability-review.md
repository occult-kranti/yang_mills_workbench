# Round19 A2 advisor applicability review in progress

Status: **A2 not gated**. This is an advisor applicability review while the A2 researchers revise the proof and comparison. It does not freeze the post-A decision.

Branch inspected: `research/round19-paired` at `211fae57b1dd93fdd334dc583f1a549abc386342`. Root reported that main publication was blocked by automatic review and the safer branch is now being used for continued Round19 milestones. This review only concerns advisor-owned records.

## Current evidence inspected

- A2 contract: `research/round19/advisor/contract-a2.json`, SHA-256 `ddc4cb6ae18458ae21b0b18afdec346386f5dfcf0e1c1a1b6974a5a072244a8b`.
- Forward A2 checker/report/output: `forward/a2/check.py` SHA-256 `37be46b23dafdf8ff96ab7e7f6aa36aa87a9a89589daf0df263077149464a483`, report SHA-256 `810ce8a2e5621b18837b2e0a249558f8132b701cc3989ee57b2e1726f641530d`, results SHA-256 `1002624d19e0480b096328fd283688abef310768ddb3a5ac41f2be0ed3752cc8`.
- Backward A2 preliminary checker/report/output: `backward/a2/check.py` SHA-256 `79599cdfbb8d8526c69695ca3953e7cad1f0f274ff2c051224816fa47b16e179`, report SHA-256 `bcbe3519bc1e61fb3bf7718597bb294223fcca720026c892b49f4efb43a8bcec`, results SHA-256 `b22e91b4ee5b16e78e002275504e150d834a2ee2d9dc893efa6be038aeb663ab`.

The forward and reverse records both target the direct incomplete tensor-product representation with complete strip ground states, free Haar factors, `H_ref`, a summable omitted-face perturbation and a `delta-beta` spectral isolation estimate. The forward output reports default `tau=1/64`, crude gap `7/64` in alpha units, exact omitted ledger `107/135`, and sharper internal gap `973/8640` in alpha units. The reverse output reports `status=passed` for its own preliminary checks. No final independent forward comparison output is present under `backward/a2/comparison/` at this review point.

## Substantive mathematical applicability

The selected A2 route remains feasible as a narrow product-representation summable exception. It is not a mere finite budget rerun if the final proof explicitly constructs the infinite reference representation, defines the operator/form domain, proves the bounded perturbation and proves spectral isolation. It still does not complete finite clipped-restriction convergence, homogeneous dense stability, or the continuum mass-gap target.

Four proof obligations must be strengthened before acceptance.

### 1. Actual dyadic coefficient sum

The forward checker contains the intended closed-form arithmetic:

```text
sum_all_faces w_f = 3 * (1/24) * (sum_x 2^-x)^3 = 1,
sum_selected w_f = (1/24) * (sum over x mod 4 in 0,1,2 of 2^-x) * (sum over even y of 2^-y) * (sum_z 2^-z) = 28/135,
sum_omitted w_f = 107/135.
```

A final A2 report/comparison should write this derivation explicitly, including the role of face orientations and the fact that selected faces are only xy faces on even-y rows with x residues `0,1,2`. The finite tail fixtures illustrate convergence but cannot replace the closed-form infinite sum.

### 2. Exhaustive unused-link witness classes

The current route uses three omitted-face classes: non-xy faces, odd-y xy faces and x-separator xy faces. A final proof must show these are exhaustive for the infinite assignment and identify an actual link in each omitted face word that is not used by any complete selected strip support:

| Omitted class | Required witness | Reason it must be explicit |
|---|---|---|
| non-xy `xz` or `yz` face | a z-direction link in the face | selected reference strips use only xy links, so z links are free factors |
| odd-y xy face | an odd-y vertical/y-direction link in the face | selected strips occur only on even-y rows |
| x-residue-3 separator xy face | a horizontal x-direction separator link in the face | residue 3 separates complete strip supports |

The current evidence samples these classes and records examples. Sampling is not enough for the gate; the report and independent comparison must prove the classification for all orthant coordinates and reject any omitted-face class without a free factor.

### 3. Form core and local domain vectors

The product representation should not be described as the orbit of arbitrary bounded local operators if the unbounded reference Hamiltonian is being controlled. The final proof needs a core made from finite tensor products of local domain/spectral vectors: complete-strip operator-domain or form-domain vectors for `H_C-E_C`, and Casimir domain/form-domain vectors for free links, with only finitely many factors outside the reference vector. The closed nonnegative form should be the closure of the monotone sum on that core.

The desired inequality is

```text
q_ref[psi] >= delta ||Q psi||^2
```

on the closed form domain, with `Q=1-|Omega_ref><Omega_ref|` and `delta=alpha/8`. The proof must explain why local block gaps imply this inequality on finite excitations and why closure preserves it. This is stronger than recording a finite list of exact levels.

### 4. Spectral projection and actual isolated eigenvalue

The codimension-one argument must be stated as a spectral projection result, not only a Rayleigh quotient slogan. For `H=H_ref+V`, bounded `V`, `||V||<=beta`, `beta<delta`, and zero trial mean:

- every normalized vector orthogonal to `Omega_ref` has form value at least `delta-beta`;
- therefore the spectral projection of `H` on `(-infinity, delta-beta)` has rank at most one;
- since the variational infimum is at most `q_H(Omega_ref)=0<delta-beta`, that projection is nonzero;
- finite-rank spectral projection below the threshold gives an actual isolated ground eigenvalue, and the next spectral point is at least `delta-beta` above zero, hence the gap from the ground is at least `delta-beta` because the ground energy is at most zero.

A final independent comparison should mutate or delete this projection-rank step and reject the proof. If physical-gap wording is used, the proof also needs gauge-sector handling and non-vacuity: the product reference and resulting ground must be in the Gauss sector or the statement must be limited to the product representation; at least one gauge-invariant local observable should be shown to have nonzero variance if the word “physical” is used beyond sector restriction.

## Current blockers before A2 gate

- No final `backward/a2/comparison/comparison.json` has been reviewed.
- The reverse preliminary report/checks appear to acknowledge the right themes, but they do not yet constitute the final source/evidence comparison against canonical forward output.
- The final reports need the four obligations above in explicit proof text, not only JSON flags.
- The forward report contains visible control-character rendering in formulas around `beta` and `frac`; this is editorial, but it should be fixed before publication to avoid ambiguity in the scientific statement.
- Any A2 gate must include normal/optimized deterministic evidence and source manifests, counted once, with Round19-relative hashes.

## Provisional decision

Continue A2 on the constructive product-representation route. Do not accept yet. The route is worth finishing because it could produce a substantive second Goal A loop: a direct infinite product-sector theorem for a summable perturbation. The resulting claim must stay narrow even if accepted:

```text
In the declared product representation, for |tau|<1/8 under the crude beta<=alpha|tau| bound, the summable omitted-face perturbation has an isolated ground and gap at least alpha(1/8-|tau|), with the default conservative value 7 alpha/64 when tau=1/64.
```

That statement does not imply convergence of finite clipped restrictions, homogeneous dense stability, explicit Yarotsky dense constants, continuum Yang-Mills or the Clay mass gap.
