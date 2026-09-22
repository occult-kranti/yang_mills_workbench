#!/usr/bin/env python3
"""Exact AT2 certificates; no actual AQ spectral samples are evaluated."""
import argparse
from fractions import Fraction as F
import json


def certificate(alpha=F(1), tau=F(1, 100000000)):
    alpha, tau = F(alpha), F(tau)
    if alpha <= 0:
        raise ValueError('alpha must be a positive physical energy coefficient')
    if abs(tau) > F(1, 100000000):
        raise ValueError('tau is outside the admitted numerical cap')
    a, L, c, b = F(1, 16), F(8), F(3), F(49)
    qlo, qhi, w2hi = F(31, 125), F(63, 250), F(1, 250000)
    slo, shi = qlo - w2hi, qhi
    ulo, uhi = 1 - qhi, 1 - qlo
    B = 36 + 98 * abs(tau)
    window = (L * slo - uhi) / (L - a)
    tangent = 2 * slo / c - uhi / c**2
    cauchy = slo**2 / uhi
    upper = (B - (2 * b + a) * ulo + (b**2 + 2 * a * b) * shi) / (a * b**2)
    return {
        'human_author': 'Hruday N M (BUNZEEY)',
        'model': 'Actual AQ numerical-cap state, conditional on the admitted AT1/AT2 premises',
        'alpha': str(alpha), 'tau': str(tau),
        'window_physical_energy': [str(alpha * a), str(alpha * L)],
        'unnormalized_window_mass_lower': str(window),
        'inverse_energy_form_interval': [str(max(tangent, cauchy) / alpha), str(upper / alpha)],
        'dimensionless_inverse_interval': [str(max(tangent, cauchy)), str(upper)],
        'tangent_lower_dimensionless': str(tangent),
        'second_energy_moment_upper': str(alpha**2 * B),
        'actual_response_evaluated': False,
        'physical_susceptibility_claim': False,
        'scientific_priority': 'unverified; project application of established methods',
        'source': 'research/round30/advisor/at2-gate.json'
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--alpha', default='1', help='Positive physical energy coefficient in chosen energy units')
    ap.add_argument('--tau', default='1/100000000', help='Signed dimensionless coupling within the admitted cap')
    args = ap.parse_args()
    try:
        result = certificate(F(args.alpha), F(args.tau))
    except (ValueError, ZeroDivisionError) as error:
        ap.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
