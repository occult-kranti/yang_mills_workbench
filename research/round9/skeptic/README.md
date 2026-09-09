# Independent verification package

From the full round-9 package directory, run:

```bash
python skeptic/audit_independent.py
python skeptic/audit_theorems_and_data.py
python skeptic/audit_acceptance.py
```

The second command requires the full raw Monte Carlo CSV files. A compact website bundle may omit those files and cannot claim to have rerun that command. None of these commands reruns Monte Carlo sampling.

Dependencies: Python, NumPy and SciPy. High-precision references use the standard-library Decimal module. Scripts discover sibling `lattice`, `transfer`, `advisor` directories, and also recognize the original `ym9-*` working names. `YM9_REVIEW_ROOT` can explicitly identify the directory containing those siblings and the proof/stability scripts.

Outputs: `independent_audit.json` (82 gates), `theorems_and_data_audit.json` (125 gates), and `acceptance_audit.json` (27 gates). Each records actual executed evidence and source hashes. `REVIEW.md` explains the verdict and its limits; `source_audit_scope.json` distinguishes reviewed functions from executed coverage. Historical source-path names in retained records identify the original run and do not imply a missing dependency.
