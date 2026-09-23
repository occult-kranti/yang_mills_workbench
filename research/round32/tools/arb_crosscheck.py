#!/usr/bin/env python3
"""Independent open-source cross-check of exact rational enclosures with Arb and mpmath.

The workbench admits results only through exact `fractions.Fraction` arithmetic.
This tool re-evaluates the transcendental constants that those certificates
enclose (exp, log, sqrt, pi, atan) with two independent open-source
implementations of rigorous arithmetic:

  * python-flint (Arb ball arithmetic, FLINT/Arb library, MIT/LGPL), and
  * mpmath interval arithmetic (mpmath.iv, BSD).

A cross-check passes when every recorded rational interval [lo, hi] contains
the Arb ball and the mpmath interval of the same quantity. Failure of a
cross-check is evidence of a defect; success is a comparison, not admission.

Usage:
  python3 -B research/round32/tools/arb_crosscheck.py --at5    # recorded Round31 AT5 constants
  python3 -B research/round32/tools/arb_crosscheck.py --json path/to/enclosures.json
where enclosures.json is a list of {"name":..., "expr":..., "lower":"p/q", "upper":"p/q"}
and expr is one of: exp(-<rational>), log(<rational>), sqrt(<rational>), pi, atan(<rational>).
"""
import argparse
import json
import re
from fractions import Fraction as Q
from pathlib import Path

try:
    import flint
except ImportError:  # pragma: no cover
    flint = None
try:
    import mpmath
except ImportError:  # pragma: no cover
    mpmath = None

ROOT = Path(__file__).resolve().parents[3]
PREC = 256
EXPR = re.compile(r'^(exp|log|sqrt|atan)\((-?\d+(?:/\d+)?)\)$|^pi$')


def arb_of(expr):
    flint.ctx.prec = PREC
    if expr == 'pi':
        return flint.arb.pi()
    m = EXPR.match(expr)
    if not m or not m.group(1):
        raise ValueError('unsupported expression ' + expr)
    fn, arg = m.group(1), Q(m.group(2))
    x = flint.arb(flint.fmpq(arg.numerator, arg.denominator))
    return {'exp': x.exp, 'log': x.log, 'sqrt': x.sqrt, 'atan': x.atan}[fn]()


def iv_of(expr):
    mpmath.mp.prec = PREC
    iv = mpmath.iv
    iv.prec = PREC
    if expr == 'pi':
        return iv.pi
    m = EXPR.match(expr)
    fn, arg = m.group(1), Q(m.group(2))
    x = iv.mpf(arg.numerator) / iv.mpf(arg.denominator)
    table = {'exp': iv.exp, 'log': iv.log, 'sqrt': iv.sqrt}
    if fn == 'atan':
        return iv.atan2(x, iv.mpf(1)) if hasattr(iv, 'atan2') else None
    return table[fn](x)


def rational_bounds_arb(ball):
    # Arb balls expose a rigorous [lower, upper] through rad/mid at the working precision.
    lo = ball.lower(); hi = ball.upper()
    return Q(str(lo.str(80, radius=False))), Q(str(hi.str(80, radius=False)))


def to_q(s):
    return Q(str(s))


def crosscheck(rows):
    report = []
    for row in rows:
        lo, hi = Q(row['lower']), Q(row['upper'])
        entry = {'name': row['name'], 'expr': row['expr'], 'lower': str(lo), 'upper': str(hi)}
        ok = True
        if flint is not None:
            ball = arb_of(row['expr'])
            mid = to_q(ball.mid().str(60, radius=False))
            rad = to_q(ball.rad().str(20, radius=False)) if ball.rad() != 0 else Q(0)
            # Outward-round the decimal rendering by the printed radius plus one unit of the last place.
            slack = rad + Q(1, 10**58)
            arb_lo, arb_hi = mid - slack, mid + slack
            entry['arb'] = {'mid': ball.mid().str(40), 'contained': lo <= arb_lo and arb_hi <= hi}
            ok &= entry['arb']['contained']
        v = iv_of(row['expr']) if mpmath is not None else None
        if v is not None:
            a = Q(str(mpmath.nstr(mpmath.mpf(v.a), 70, strip_zeros=False)))
            b = Q(str(mpmath.nstr(mpmath.mpf(v.b), 70, strip_zeros=False)))
            slack = Q(1, 10**66)
            entry['mpmath_iv'] = {'a': mpmath.nstr(v.a, 40), 'b': mpmath.nstr(v.b, 40),
                                  'contained': lo <= a - slack and b + slack <= hi}
            ok &= entry['mpmath_iv']['contained']
        entry['passed'] = bool(ok)
        report.append(entry)
    return report


def at5_rows():
    """Recorded Round31 AT5 forward constants re-derived from its calculator."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('at5calc', ROOT / 'research/round31/forward/at5/calculator.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    rows = []
    lo, hi = mod.exp_negative(Q(3)); rows.append({'name': 'free reference exp(-3)', 'expr': 'exp(-3)', 'lower': str(lo), 'upper': str(hi)})
    lo, hi = mod.pi_interval(); rows.append({'name': 'pi (Machin)', 'expr': 'pi', 'lower': str(lo), 'upper': str(hi)})
    lo, hi = mod.log_positive(1 + Q(10**9) ** 2); rows.append({'name': 'log(1+L^2), L=1e9', 'expr': f'log({1 + 10**18})', 'lower': str(lo), 'upper': str(hi)})
    lo, hi = mod.sqrt_interval(Q(49, 3) * Q(1, 10**14)); rows.append({'name': 'sqrt(49 tau/3), tau=1e-14', 'expr': 'sqrt(49/300000000000000)', 'lower': str(lo), 'upper': str(hi)})
    lo, hi = mod.exp_negative(Q(3, 32)); rows.append({'name': 'AT6 step ratio exp(-3/32)', 'expr': 'exp(-3/32)', 'lower': str(lo), 'upper': str(hi)})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--at5', action='store_true')
    ap.add_argument('--json', type=Path)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    rows = at5_rows() if a.at5 else json.loads(a.json.read_text())
    report = crosscheck(rows)
    result = {'tool': 'arb_crosscheck', 'precision_bits': PREC,
              'libraries': {'python-flint': getattr(flint, '__version__', None), 'mpmath': getattr(mpmath, '__version__', None)},
              'passed': all(r['passed'] for r in report), 'rows': report,
              'interpretation': 'Containment of independent rigorous enclosures inside the recorded exact rational intervals; a comparison, not an admission decision.'}
    text = json.dumps(result, indent=2) + '\n'
    if a.output:
        a.output.write_text(text)
    print(text if not a.output else json.dumps({'passed': result['passed'], 'rows': len(report)}))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
