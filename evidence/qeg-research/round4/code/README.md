# Round-four tangent response code

`response.py` integrates the finite-grid round-three Maxwell–Dirac closure and
its analytic tangent system together with DOP853.  The source-amplitude tangent
uses `v=δa`, `u=δx`, `η=δr`, and `q=δk-v`; its initial tangents are zero.  The
source and current use the coupled sum
`S = sum(weights * (rz + p/omega))`.  The round-three separate-sum value is
reported as `S_legacy` so its floating-point effect can be measured without
changing archived round-three files.

The tangent is checked with centered finite differences at several epsilons,
including smaller values to show the second-order region and any tolerance
floor.  The gauge check uses `δk=δa0=1`, hence `q=0`, and verifies physical
invariance.  Energy and tangent-energy residuals, raw Bloch norm error,
minimum `Z`, and un-clipped occupation extrema are retained in each result.

`response_run.py` writes `../response_results.json` and `.csv` for production
(`b=10`, levels 0–4, `Kmax=20`, `t=20`, `nK=128,256`), a single `nK=512`
and `nK=1024` targeted refinement baselines, an independently held out source case (including the exact
small verifier fixture), a delayed probe case, and the small verifier case.  The delayed
probe changes only the tangent source after the baseline pump; it tests causal
support and post-pump energy conservation.

Run with:

```bash
python response_run.py
```

This is a finite-regulator sensitivity computation of the existing coupled
model.  It does not establish a continuum limit, a full Einstein–QED result,
or a quantum-validity certificate.

The targeted fixed-window check records the full-history change from `nK=512` to `nK=1024`: max `|Δu| = 2.16e-10` and max `|Δ(deltaJmatter)| = 8.43e-8`. This satisfies the numerical response gate used for this finite regulator.
The coarse `128→256` and `256→512` source-tangent pairs remain above the full-history `1e-6` gate. The targeted `512→1024` pair passes (`max |delta u|=2.16e-10`), resolving the tested `Kmax=20`, levels 0–4, `t=20` momentum refinement. The finite Landau cutoff, momentum window, and other response sectors remain untested; this is not a continuum claim.
