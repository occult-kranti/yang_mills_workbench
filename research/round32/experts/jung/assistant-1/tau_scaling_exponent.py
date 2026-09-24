#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 1, assistant script 2 of 3: tau-scaling exponent.

Pre-registration audit / test only (loop3-signoff.md section 4, item 2). Counts zero
research loops; not a producer, contract, gate or skeptical review. Human project
author: Hruday N M (BUNZEEY); AI-assisted.

Fits the exponent p of D(tau) ~ tau^p over tau in {10^-8, 10^-9, 10^-10} for AV1 tier
(i), AV1 tier (ii) and the AT4 square-root state bound D_sqrt(tau)=2*sqrt(49|tau|/3),
using the AV1/AV2 producers' *exported formulas* re-implemented with exact
``fractions.Fraction`` (no import of any producer/skeptic module). The ratio
D(tau_a)/D(tau_b) between consecutive nodes is computed exactly as a Fraction; only
the log of that exact ratio is taken as a float, purely for the reported exponent
(never for an admission Boolean).

PASS iff:
  - tiers (i) and (ii) give exponent p in [0.99, 1.01] (within 1% of the linear
    value 1) at every consecutive pair of nodes, and
  - the AT4 square-root formula gives p in [0.49, 0.51] (within 1% of 0.5), and
  - a label-swap mutation that certifies the sqrt bound under the *linear* [0.99,1.01]
    band (i.e. calls it "linear") is detected and rejected.

Usage: python3 -B tau_scaling_exponent.py
"""
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

TAUS = (Q(1, 10 ** 8), Q(1, 10 ** 9), Q(1, 10 ** 10))
LINEAR_BAND = (Q(99, 100), Q(101, 100))   # p in [0.99, 1.01]
SQRT_BAND = (Q(49, 100), Q(51, 100))      # p in [0.49, 0.51]


def exponent_from_ratio(d_ratio, tau_ratio):
    """p such that d_ratio = tau_ratio^p, from the exact rational d_ratio and
    tau_ratio; the log itself is a float, for reporting only."""
    return math.log(float(d_ratio)) / math.log(float(tau_ratio))


def admit_exponent_band(p, lo, hi, label):
    K.require(float(lo) <= p <= float(hi),
              'exponent %.6f for %s falls outside [%.3f,%.3f]' % (p, label, float(lo), float(hi)))


def fit_series(D_fn, C, label, band):
    values = [D_fn(t, C) if C is not None else D_fn(t) for t in TAUS]
    D_values = [v['D'] if isinstance(v, dict) else v for v in values]
    pairs = []
    for i in range(len(TAUS) - 1):
        tau_a, tau_b = TAUS[i], TAUS[i + 1]
        D_a, D_b = D_values[i], D_values[i + 1]
        K.require(D_a > 0 and D_b > 0, label + ': D must be strictly positive at every node')
        d_ratio = D_a / D_b          # exact Fraction
        tau_ratio = tau_a / tau_b    # exact Fraction, =10 for these nodes
        p = exponent_from_ratio(d_ratio, tau_ratio)
        admit_exponent_band(p, band[0], band[1], label)
        pairs.append({'tau_a': K.s(tau_a), 'tau_b': K.s(tau_b), 'D_a': K.s(D_a), 'D_b': K.s(D_b),
                       'D_ratio_exact': K.s(d_ratio), 'tau_ratio_exact': K.s(tau_ratio),
                       'exponent_p': p})
    return {'label': label, 'band': [float(band[0]), float(band[1])],
            'D_values': [K.s(v) for v in D_values], 'D_values_preview': [K.dec(v) for v in D_values],
            'pairs': pairs, 'all_within_band': True}


def run():
    C1 = K.av1_constants()

    tier_i = fit_series(K.D_tier_i, C1, 'tier_i_linear', LINEAR_BAND)
    tier_ii = fit_series(K.D_tier_ii, C1, 'tier_ii_linear', LINEAR_BAND)

    # AT4 sqrt formula: D_sqrt(tau)^2 = 4*49*|tau|/3 is exactly linear in |tau|, so the
    # ratio of D_sqrt values across nodes is the *exact* rational sqrt of the tau
    # ratio; only the directed rational bracket (below) and the reported float log
    # are approximate, and neither decides the pass/fail band membership on its own
    # (both bracket endpoints are checked).
    sqrt_pairs = []
    for i in range(len(TAUS) - 1):
        tau_a, tau_b = TAUS[i], TAUS[i + 1]
        tau_ratio = tau_a / tau_b
        sq_ratio = K.D_sqrt_squared(tau_a) / K.D_sqrt_squared(tau_b)
        K.require(sq_ratio == tau_ratio, 'D_sqrt^2 must scale exactly linearly in |tau|')
        lo_a, hi_a = K.D_sqrt_bracket(tau_a)
        lo_b, hi_b = K.D_sqrt_bracket(tau_b)
        K.require(lo_a > 0 and lo_b > 0, 'D_sqrt bracket must be strictly positive')
        p_lo = exponent_from_ratio(lo_a / hi_b, tau_ratio)
        p_hi = exponent_from_ratio(hi_a / lo_b, tau_ratio)
        K.require(p_lo <= p_hi, 'sqrt exponent bracket malformed')
        admit_exponent_band(p_lo, SQRT_BAND[0], SQRT_BAND[1], 'at4_sqrt (lower)')
        admit_exponent_band(p_hi, SQRT_BAND[0], SQRT_BAND[1], 'at4_sqrt (upper)')
        sqrt_pairs.append({'tau_a': K.s(tau_a), 'tau_b': K.s(tau_b),
                            'D_sqrt_squared_ratio_exact': K.s(sq_ratio), 'tau_ratio_exact': K.s(tau_ratio),
                            'D_sqrt_bracket_a': [K.s(lo_a), K.s(hi_a)], 'D_sqrt_bracket_b': [K.s(lo_b), K.s(hi_b)],
                            'exponent_p_bracket': [p_lo, p_hi]})
    at4_sqrt = {'label': 'at4_sqrt', 'band': [float(SQRT_BAND[0]), float(SQRT_BAND[1])],
                'pairs': sqrt_pairs, 'all_within_band': True}

    # -------------------- label-swap mutation: call the sqrt bound "linear" --------------------
    def mutation_label_sqrt_as_linear():
        for pair in sqrt_pairs:
            p_lo, p_hi = pair['exponent_p_bracket']
            admit_exponent_band(p_lo, LINEAR_BAND[0], LINEAR_BAND[1], 'at4_sqrt mislabelled linear')
            admit_exponent_band(p_hi, LINEAR_BAND[0], LINEAR_BAND[1], 'at4_sqrt mislabelled linear')

    mutation_rejected_because = K.expect_rejected(mutation_label_sqrt_as_linear)

    result = {
        'id': 'tau_scaling_exponent',
        'role': 'pre-registration audit / test; zero research loops',
        'formulas_source': 'research/round32/contracts/av1.json (re-implemented; no producer modules imported)',
        'nodes_tau': [K.s(t) for t in TAUS],
        'linear_band_p': [float(LINEAR_BAND[0]), float(LINEAR_BAND[1])],
        'sqrt_band_p': [float(SQRT_BAND[0]), float(SQRT_BAND[1])],
        'tier_i': tier_i,
        'tier_ii': tier_ii,
        'at4_sqrt': at4_sqrt,
        'label_swap_mutation': {
            'description': 'certify the AT4 sqrt bound under the linear [0.99,1.01] band (call it "linear")',
            'rejected': True,
            'rejected_because': mutation_rejected_because,
        },
        'checks': [
            {'id': 'tier_i_exponent_within_1pct_of_1', 'passed': all(
                float(LINEAR_BAND[0]) <= pr['exponent_p'] <= float(LINEAR_BAND[1]) for pr in tier_i['pairs'])},
            {'id': 'tier_ii_exponent_within_1pct_of_1', 'passed': all(
                float(LINEAR_BAND[0]) <= pr['exponent_p'] <= float(LINEAR_BAND[1]) for pr in tier_ii['pairs'])},
            {'id': 'at4_sqrt_exponent_within_1pct_of_half', 'passed': all(
                float(SQRT_BAND[0]) <= pr['exponent_p_bracket'][0]
                and pr['exponent_p_bracket'][1] <= float(SQRT_BAND[1]) for pr in sqrt_pairs)},
            {'id': 'label_swap_mutation_rejected', 'passed': mutation_rejected_because is not None},
        ],
    }
    result['pass'] = all(c['passed'] for c in result['checks'])
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'tau_scaling_exponent', result)
    print('tau_scaling_exponent: %s' % ('PASS' if result['pass'] else 'FAIL'))
    for label, block in (('tier_i', result['tier_i']), ('tier_ii', result['tier_ii']), ('at4_sqrt', result['at4_sqrt'])):
        ps = [p.get('exponent_p', p.get('exponent_p_bracket')) for p in block['pairs']]
        print('  %s exponents: %s' % (label, ps))
    print('  label-swap mutation rejected because: %s' % result['label_swap_mutation']['rejected_because'])
    for c in result['checks']:
        print('   [%s] %s' % ('x' if c['passed'] else ' ', c['id']))
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
