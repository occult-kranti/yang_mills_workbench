#!/usr/bin/env python3
"""Labelled ball/interval-arithmetic PREVIEW of the AW2 enclosure (never admission).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Recomputes the AW2 enclosure endpoints and margins at tau=+-10^-8 with
python-flint (Arb midpoint-radius balls) and mpmath interval arithmetic, from
the same hash-verified AW1 gate constant that calculator.py reads. Every ball
or interval is exported exactly as dyadic rational endpoints ('p/q' text), so
check.py can compare them with its exact Fraction values without any binary
floating value entering results.json. check.py does not import this script or
its libraries; it only reads the stored arb-preview.json as a labelled
comparison. Admission arithmetic is exact fractions.Fraction in check.py.

Usage (from anywhere): python3 -B arb_preview.py --output /absolute/path/arb-preview.json
"""
import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
import calculator as calc  # noqa: E402

import flint  # noqa: E402
import mpmath  # noqa: E402
from mpmath.libmp import to_rational  # noqa: E402

PREC = 256


def textq(x):
    return calc.textq(x)


def arb_bounds(ball):
    m, e = ball.mid().man_exp()
    r, f = ball.rad().man_exp()
    mid = Q(int(m)) * (Q(2) ** int(e))
    rad = Q(int(r)) * (Q(2) ** int(f))
    return mid - rad, mid + rad


def iv_bounds(x):
    a, b = x._mpi_
    return Q(*to_rational(a)), Q(*to_rational(b))


def main():
    ap = argparse.ArgumentParser(description='AW2 Arb/mpmath preview (labelled, not admission)')
    ap.add_argument('--output', required=True)
    out = Path(ap.parse_args().output)
    if not out.is_absolute():
        raise SystemExit('absolute output path required')
    G = calc.gate_constants()
    K, c1 = G['K'], G['c1']
    flint.ctx.prec = PREC
    mpmath.iv.prec = PREC
    Ka = flint.arb(flint.fmpq(K.numerator, K.denominator))
    Ki = mpmath.iv.mpf(K.numerator) / mpmath.iv.mpf(K.denominator)
    c1a = flint.arb(flint.fmpq(c1.numerator, c1.denominator))
    c1i = mpmath.iv.mpf(c1.numerator) / mpmath.iv.mpf(c1.denominator)
    records = {}
    for sign, s in (('+', 1), ('-', -1)):
        ta = flint.arb(s) / flint.arb(10) ** 8
        ti = mpmath.iv.mpf(s) / mpmath.iv.mpf(10) ** 8
        qa = {'lower': c1a * ta - Ka * ta * ta, 'upper': c1a * ta + Ka * ta * ta,
              'sign_margin': c1a * abs(ta) / (Ka * ta * ta), 'exclusion_margin': (c1a * abs(ta) - Ka * ta * ta) / (Ka * ta * ta)}
        tai = abs(ti)
        qi = {'lower': c1i * ti - Ki * ti * ti, 'upper': c1i * ti + Ki * ti * ti,
              'sign_margin': c1i * tai / (Ki * ti * ti), 'exclusion_margin': (c1i * tai - Ki * ti * ti) / (Ki * ti * ti)}
        rec = {}
        for name in ('lower', 'upper', 'sign_margin', 'exclusion_margin'):
            alo, ahi = arb_bounds(qa[name])
            ilo, ihi = iv_bounds(qi[name])
            rec[name] = {'arb_ball_bounds': {'lower': textq(alo), 'upper': textq(ahi)},
                         'arb_text': qa[name].str(20, radius=True),
                         'mpmath_iv_bounds': {'lower': textq(ilo), 'upper': textq(ihi)},
                         'mpmath_iv_text': mpmath.nstr(qi[name], 20)}
        records[sign] = rec
    packet = {
        'label': 'PREVIEW ONLY: Arb (python-flint) and mpmath interval comparison of the AW2 enclosure; never admission arithmetic',
        'preview_only': True, 'used_for_admission': False,
        'libraries': {'python-flint': flint.__version__, 'mpmath': mpmath.__version__, 'python': sys.version.split()[0]},
        'precision_bits': str(PREC),
        'K_2_plus_source': 'AW1 gate decision text via calculator.gate_constants (sha256 %s)' % G['gate_sha256'],
        'tau_values': {'+': '1/100000000', '-': '-1/100000000'},
        'quantities': records,
    }
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'written': str(out), 'preview_only': True}))


if __name__ == '__main__':
    main()
