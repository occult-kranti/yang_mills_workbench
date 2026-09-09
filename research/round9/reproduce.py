#!/usr/bin/env python3
"""Bounded deterministic replay; stochastic sampling is an explicit separate run."""
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent
jobs=['lattice/test_lattice.py','transfer/run_benchmark.py','advisor/check_exact_counterexamples.py','stability.py','proof_routes.py','skeptic/audit_independent.py']
for name in jobs:
    print('RUN '+name,flush=True)
    subprocess.run([sys.executable,str(HERE/name)],cwd=HERE,check=True)
print('Deterministic replay completed. Raw sampling diagnostics require the full package and a separate command.')
