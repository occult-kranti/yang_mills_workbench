"""Exact rational bound for the real ODE with the frozen rounded coefficients.

This does not enclose the floating-point trajectory or certify digamma evaluation.
The already computed floats are interpreted as exact rational model inputs.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent.parent / 'round4/code/response.py'
LEGACY = ROOT.parent.parent / 'round3/code/backreaction.py'
EXPECTED = {
    SOURCE: '0a197f5b46de8114d790c937059018d21df3f55a436c76067b91c09277035867',
    LEGACY: '32008bfc4fc3f731ac7ed968006fd58642820e0f421766a1ace022a2d7f08e88',
}


def main():
    hashes = {str(p.relative_to(ROOT.parent.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in EXPECTED}
    for p, expected in EXPECTED.items():
        if hashes[str(p.relative_to(ROOT.parent.parent))] != expected:
            raise RuntimeError(f'Frozen source mismatch: {p.name}; audit the new model first')
    sys.path.insert(0, str(SOURCE.parent))
    import numpy as np
    import scipy
    import response
    grid = response.Grid(response.Params(nK=1024))
    if not (bool(np.all(grid.weights > 0)) and bool(np.all(grid.M > 0))):
        raise RuntimeError("coefficient positivity failed")
    cstar = Q(0)
    groups = []
    for n in range(5):
        mask = grid.n == n
        masses = {Q.from_float(float(x)) for x in grid.M[mask]}
        if len(masses) != 1:
            raise RuntimeError("Landau group has inconsistent masses")
        mass = next(iter(masses))
        wsum = sum((Q.from_float(float(w)) for w in grid.weights[mask]), Q(0))
        cstar += wsum / (4 * mass**3)
        groups.append({'landau_index': n, 'weight_sum': str(wsum), 'mass': str(mass)})
    e2 = Q.from_float(float(response.E2))
    chi = Q.from_float(float(response._chi(10)))
    lower = 1 + chi - e2 * cstar
    margin = lower - Q(3, 4)
    if margin <= 0:
        raise RuntimeError("global Z bound does not exceed three quarters")
    output = {
        'status': 'exact_rational_rounded_coefficient_bound_passed',
        'nK': 1024, 'groups': groups, 'e2': str(e2), 'chi': str(chi),
        'Cstar': str(cstar), 'Z_global_lower': str(lower),
        'margin_above_three_quarters': str(margin),
        'display_only_lower': float(lower), 'proved_comparison': 'Z(a) > 3/4 for every real a',
        'input_source_hashes': hashes, 'numpy': np.__version__, 'scipy': scipy.__version__,
        'certificate_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Real-arithmetic ODE with the generated binary-rational coefficient list and admissible exact initial states.',
        'trajectory_integration_rerun': False, 'floating_trajectory_enclosed': False,
        'analytic_digamma_value_enclosed': False,
    }
    (ROOT.parent / 'coefficient_certificate_results.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'display_only_lower': float(lower)}))


if __name__ == '__main__':
    main()
