# Independent review replay

From the repository root, after installing the project's scientific requirements:

```bash
python -B research/round13/skeptic/audit_moments.py research/round13/moments/moment_bounds.py --label moments_normal
python -B research/round13/skeptic/audit_locality.py research/round13/locality/locality_checks.py --label locality_normal
python -B research/round13/skeptic/audit_response.py research/round13/response/response_checks.py --label response_normal
python -B research/round13/skeptic/audit_stability.py research/round13/advisor --label stability_normal
```

Repeat with `python -B -O` and the corresponding `_optimized` labels to confirm the checks remain active under optimized Python. Each script writes a result file beside itself and exits unsuccessfully if any gate fails. The locality and moment arithmetic oracles use Python exact fractions; the alternative response integration uses NumPy and SciPy and remains a numerical comparison.

`acceptance.json` binds the independently reviewed source bytes and the accepted scientific implication rules. `REVIEW.md` explains the result, defects and limitations. `analytic-review.md` gives additional derivations. The two initial failure records and their original source snapshots are retained evidence. Earlier/preflight results do not contribute to the final distinct-gate count.

## Separate proof-adapter review

Read `proof_adapter_review.md` and `proof_adapter_review.json` for the additional 69 independent adapter gates; these are separate from the 532 scientific gates. Run `python -B research/round13/skeptic/audit_proof_adapter.py --help` for its isolated-root and output-label options. The original post-replay mutation failure is preserved.
