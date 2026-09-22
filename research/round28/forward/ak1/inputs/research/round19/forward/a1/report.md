# Forward A1: literal clipped restrictions of one infinite strip assignment

This is the forward execution for the frozen Round19 A1 contract. It is not an advisor gate, not an independent backward reconstruction and not an A2 result.

## Contract and scale

The finite operator is the full-link SU(2) rotor Hamiltonian

\[
H_N=\alpha\sum_{e\subset B_N}C_e-\sum_{f\subset B_N}\lambda_f x_f,
\qquad x_f=\operatorname{Tr}(U_f)/2.
\]

The Hilbert space is the untruncated product Haar link space. The all-vertex Gauss restriction is only invoked after a positive full-space estimate gives a unique ground state and the continuous vertex gauge action leaves the Hamiltonian invariant.

A1 records a symbolic positive physical reference energy \(E_\star\), with \(\alpha/E_\star\) and \(\alpha_{\min}/E_\star\) separate from \(\lambda/\alpha\), \(\mu/\alpha\), volume and phase. The checker rejects attempts to use zero normalization or \(\kappa\) as the A1 energy reference.

## Infinite assignment

The fixed infinite coefficient assignment labels xy faces on even-y rows by the x phase:

| phase | role | bound |
|---:|---|---:|
| 0 | left end | \(|\lambda_L|\le \alpha/2\) |
| 1 | bridge | \(|\mu_M|\le \alpha/8\) |
| 2 | right end | \(|\lambda_R|\le \alpha/2\) |
| 3 | omitted in A1 | — |

Finite boxes inherit coefficients face by face. They do not wait for a complete three-face strip. This removes the Round18 coefficient jump: face `(0,1,4,0,0)` is a left-end face whenever it appears, rather than a remainder in `B_6` and a cluster face in `B_8`.

Across all four x-phase offsets, the reachable clipped selected components are exactly `L`, `M`, `R`, `LM`, `MR` and `LMR`. The checker materializes `n=2..12` for phases `0,1,2,3`, validates signed plaquette words and component link disjointness, and records representative free-link witnesses for non-selected faces.

## Component bounds

For a proper clipped component \(S\ne LMR\), use the bare full-link reference on the actual component links. The constant vacuum is unique, the first nonconstant full-link excitation costs \(3\alpha/4\), and each retained Wilson face has zero Haar-vacuum mean through an actual free link. Hence

\[
\Delta_S\ge \alpha\left(\frac34-\sum_{t\in S}|c_t|/\alpha\right).
\]

The worst one-face case is an end face, giving \(\alpha/4\). The worst two-face cases are `LM` and `MR`, each giving \(3\alpha/4-(\alpha/2+\alpha/8)=\alpha/8\). The bridge-only case gives \(5\alpha/8\). Signs and zero coefficients are included explicitly and do not weaken the absolute-norm estimates.

For the complete `LMR` strip, the bare norm budget can be \(9\alpha/8\), so the checker uses the accepted Round18 dressed-end bridge formula:

\[
\Delta_{LMR}\ge \alpha\left(\frac34-\max(|\lambda_L|,|\lambda_R|)/\alpha\right)-|\mu_M|\ge \alpha/8.
\]

Thus every selected clipped component produced by a literal finite restriction has a full-link lower estimate at least \(\alpha/8\). Tensoring link-disjoint components with free links preserves the selected-part reference gap at \(\alpha/8\). This remains a finite local result; thermodynamic states, limiting dynamics, dense homogeneous stability and continuum mass-gap claims remain open.

## Evidence

The canonical executable is:

```bash
python -B check.py --output /absolute/new/output_dir
```

The generated evidence includes:

- `results.json`: scale register, infinite assignment, 54 signed local endpoint cases and 44 phase fixtures;
- `component_templates.json`: exact representative signed face words and zero-mean witnesses for the six component types;
- `phase_counts.csv`: compact count table for `n=2..12` and all four x phases;
- `controls.json`: scale, coefficient-reclassification, missing-component, zero-mean-withdrawal, common-scale and signed-word controls;
- `source-manifest.json`: source hash and output hashes.

Normal and optimized executions were run in separate new output directories and produced identical semantic files for `results.json`, `component_templates.json`, `controls.json` and `phase_counts.csv`; the comparison hashes are recorded separately in `optimized-comparison.json`.
