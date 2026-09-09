#!/usr/bin/env python3
"""Run the self-contained downloadable Review 8 package without altering originals."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def run(path,*args):
    subprocess.run([sys.executable,*args,str(path)],cwd=path.parent,check=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='Also regenerate corrected finite/gravity suites and root implementation checks.')
    args=parser.parse_args()
    if not (HERE/'evidence/qeg-research/round7').is_dir():
        raise RuntimeError('Run reproduce.py from the extracted download package, which includes its evidence dependencies.')
    run(HERE/'gap-output/test_gap_diagnostics.py')
    run(HERE/'skeptic-output/regression_audit.py')
    run(HERE/'skeptic-output/regression_audit.py','-O')
    run(HERE/'skeptic-output/response_grid_audit.py')
    run(HERE/'proof/proof_routes.py')
    if args.full:
        out=HERE/'corrected-run/qeg-research'
        shutil.copytree(HERE/'evidence/qeg-research',out,dirs_exist_ok=True)
        for name in ['finite_scalar.py','gravity_sim.py']:
            shutil.copy(HERE/'skeptic-output/fixed'/name,out/'round7'/name)
        for name in ['finite_scalar.py','gravity_sim.py','validate_simulations.py']:
            run(out/'round7'/name)
    print('Requested finite-model checks completed. No Yang-Mills proof or continuum claim.')

if __name__=='__main__':main()
