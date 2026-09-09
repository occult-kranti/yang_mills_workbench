"""Final comparison against an independently produced spinor-reference JSON.

This script imports the production Bloch solver. The reference generator,
independent_checks.py, does not. Source hashes distinguish numerical evidence
from a claim that a mutable source file was frozen throughout a longer run.
"""
from pathlib import Path
import hashlib, json, sys
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from backreaction import Params, run


def main():
    source=ROOT/'code/backreaction.py'
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    reference_path=ROOT/'independent_results.json'
    reference=json.loads(reference_path.read_text())['spinor_backreaction']
    parameters=Params(**reference['parameters'],sample_count=81)
    production=run(parameters)
    after=hashlib.sha256(source.read_bytes()).hexdigest()
    delta_E=float(np.max(abs(np.array(production['macro']['x'])-np.array(reference['E']))))
    delta_A=float(np.max(abs(np.array(production['macro']['a'])-parameters.a0-np.array(reference['a_minus_a0']))))
    result={'reference_generator':'independent_checks.py, spinor equations; no production imports',
        'production_representation':'real Bloch vectors',
        'parameters':reference['parameters'],'max_E_difference':delta_E,
        'max_A_difference':delta_A,'production_final_E':production['diagnostics']['final_x'],
        'reference_final_E':reference['E'][-1],
        'production_energy_work_residual':production['diagnostics']['max_energy_work_residual_abs'],
        'reference_energy_work_residual':reference['max_energy_work_residual'],
        'source_hash_before':before,'source_hash_after':after,'source_unchanged':before==after,
        'reference_results_sha256':hashlib.sha256(reference_path.read_bytes()).hexdigest(),
        'comparison_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'passed':before==after and delta_E<2e-8 and delta_A<2e-8,
        'scope':'same finite regulator and shared model, independent numerical representations'}
    (ROOT/'implementation_comparison.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    if not result['passed']: raise AssertionError(result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
