#!/usr/bin/env python3
"""Pre-producer O2 scalar comparator; no producer import or research admission."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, why):
    if ok is not True:
        raise RuntimeError(why)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    output = parser.parse_args().output
    require(not output.exists(), 'fresh output required')
    for part in (output.absolute(), *output.absolute().parents):
        require(not part.is_symlink(), 'symlink rejected')
    C, tau = F(25460736, 25), F(1, 2**22)
    log2_lower = F(69, 100)
    partial = 2*(F(1, 3)+F(1, 81)+F(1, 1215))
    require(partial > log2_lower, 'strict lower bound from positive atanh series')
    grid = 10**100
    def upward(x): return F(-((-x.numerator*grid)//x.denominator), grid)
    r, d = C*tau*tau, 448*tau
    rows = []
    minimum = (0, r)
    for n in range(200):
        loss_lower = log2_lower/F(2*(n+1)*(n+2))
        z = 4*r/loss_lower
        if r < minimum[1]: minimum = (n, r)
        if n in (0, 1, 10, 30, 70) or z >= 1:
            rows.append({'step': n, 'r': str(r), 'd': str(d), 'xi': str(z),
                         'series_condition_met': z < 1})
        if z >= 1:
            break
        next_r = upward((d+F(3, 2)*r)*z/(1-z))
        d, r = d+2*r, next_r
    else:
        raise RuntimeError('expected comparator failure not located')
    require(n == 75, 'rational comparator first invalid step')
    # Universal same-weight bracket fixture on a union of m consecutive stars:
    # N=3m+1 sites, normalized rank-two S_Y and normalized onsite projectors.
    # At mu=log(2), exact bracket norm/input norm product is N/2.
    bracket_rows = [{'stars_in_union': m, 'support_size': 3*m+1,
                     'same_weight_bracket_ratio_at_log2': str(F(3*m+1, 2))}
                    for m in (1, 4, 16, 64)]
    result = {
        'schema': 'ym22-skeptic-preparation-check-v1', 'loop': 'o2',
        'passed': True, 'current_producers_read': False,
        'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'tau': str(tau), 'C_O1': str(C), 'r0': str(C*tau*tau), 'd0': str(448*tau),
        'majorant': 'xi=4*r/loss_lower; r_next=ceil_grid((d+3r/2)*xi/(1-xi)); d_next=d+2r',
        'loss_lower': '(69/100)/(2*(n+1)*(n+2))',
        'log2_lower_proof_partial_sum': str(partial),
        'upward_rounding_grid_denominator': str(grid), 'rows': rows,
        'minimum_residual_step': minimum[0], 'minimum_residual': str(minimum[1]),
        'first_invalid_step': n, 'same_weight_counterexample_ratios': bracket_rows,
        'scope': 'Independent conservative scalar certificate only; no actual algorithm or gap failure inferred',
        'research_loops_added': 0
    }
    output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'loop': 'o2', 'prepared': True, 'first_invalid_comparator_step': n}))


if __name__ == '__main__':
    main()
