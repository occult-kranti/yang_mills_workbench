"""Independent advisor checks for the revised round-6 coefficient experiment.

Uses high-precision integration and digamma, with explicit argument/axis
conventions. Does not call the implementation's reference evaluator.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'round5' / 'deps'))
import mpmath as mp


def main() -> dict:
    path = ROOT / 'experiments.py'
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location('reviewed_round6_experiments', path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    checks = []

    def add(identifier, passed, **evidence):
        checks.append({'id': identifier, 'passed': bool(passed), 'evidence': evidence})

    with mp.workdps(90):
        for a in (1000.0, 10000.0, 100000.0, 1000000.0, 10000000.0, 1e30):
            aa, kk = mp.mpf(str(a)), mp.mpf(20)
            # Normalize before quadrature so the absolute stopping tolerance
            # does not accept a poor relative result for integrals ~1e-150.
            normalization = (1 + aa**2)**mp.mpf('-2.5')
            reference = 10 / (16 * mp.pi**2) * normalization * mp.quad(
                lambda k: ((1 + aa**2) / (1 + (k-aa)**2))**mp.mpf('2.5'), [-kk, kk]
            )
            actual = module.exact_C(10, 0, 20, a)
            relative = abs(mp.mpf(actual)-reference) / reference
            add(f'endpoint_cancellation_{a:g}', actual > 0 and relative < mp.mpf('2e-13'),
                a=a, actual=actual, reference=mp.nstr(reference, 35), relative_error=float(relative))

        for row in module.cofinal_gate()['rows']:
            b, N = mp.mpf(str(row['b'])), int(row['N'])
            # E9 already includes its 1/4; the level measure is b*d/(4*pi^2).
            lower = b/(4*mp.pi**2)*sum(
                (1 if n == 0 else 2)*5/(12*mp.sqrt(2)*(1+2*b*n))
                for n in range(N+1)
            )
            actual = mp.mpf(str(row['lower_bound']))
            relative = abs(actual-lower)/lower
            add(f'cofinal_normalization_N{N}', relative < mp.mpf('2e-13'),
                actual=float(actual), reference=mp.nstr(lower, 35), relative_error=float(relative))

        for row in module.tail_rows():
            if 'log10_N_plus_1' in row:
                log10_n1 = mp.mpf(str(row['log10_N_plus_1']))
                n1 = mp.power(10, log10_n1)
                e2 = mp.mpf(str(module.E2))
                expected = 1-e2/(12*mp.pi**2)*(mp.log(20)+mp.digamma(n1+mp.mpf('0.05')))
                difference = abs(mp.mpf(str(row['Z_N_infinity']))-expected)
                add(f'tail_argument_log10Nplus1_{log10_n1}', difference < mp.mpf('2e-13'),
                    expected=mp.nstr(expected,35), actual=row['Z_N_infinity'], abs_difference=float(difference))
            elif 'log10_N_critical_asymptotic' in row:
                expected = (12*mp.pi**2/mp.mpf(str(module.E2))-mp.log(20))/mp.log(10)
                difference = abs(mp.mpf(str(row['log10_N_critical_asymptotic']))-expected)
                add('critical_log10_units', difference < mp.mpf('2e-10'),
                    expected=mp.nstr(expected,35), actual=row['log10_N_critical_asymptotic'])
            elif 'ln_N_critical_asymptotic' in row:
                expected = 12*mp.pi**2/mp.mpf(str(module.E2))-mp.log(20)
                difference = abs(mp.mpf(str(row['ln_N_critical_asymptotic']))-expected)
                add('critical_natural_log_units', difference < mp.mpf('2e-10'),
                    expected=mp.nstr(expected,35), actual=row['ln_N_critical_asymptotic'])
            else:
                add('recognized_tail_row', False, row=row)

    for a in (True, False, '0.3', float('nan'), float('inf')):
        try:
            module.exact_C(10,0,20,a)
            add(f'potential_rejected_{a!r}', False, reason='accepted')
        except ValueError:
            add(f'potential_rejected_{a!r}', True, reason='explicit ValueError')
        except Exception as exc:
            add(f'potential_rejected_{a!r}', False, reason=type(exc).__name__)

    record = json.loads((ROOT/'experiment_results.json').read_text())
    recorded_hash = record.get('hashes',{}).get('qeg-research/round6/experiments.py')
    add('executed_results_match_reviewed_source', recorded_hash == source_hash,
        source_sha256=source_hash, recorded_sha256=recorded_hash)
    add('declared_gates_pass', record.get('all_conventional_gates_pass') is True,
        gates={k:v.get('passed') for k,v in record.get('gates',{}).items()})
    # Confirms the retained initial failure, so fixes cannot erase the audit.
    initial = ROOT/'advisor_review'/'experiments_initial_observed.py'
    add('initial_buggy_source_retained', initial.exists() and
        hashlib.sha256(initial.read_bytes()).hexdigest() ==
        'ba8fa923b28fc4fa9d0b75fe0e566417806a3a5a573d96c075fe8d407bbd8915')

    out = {'schema_version':1,'date':'2026-09-09','reviewed_source_sha256':source_hash,
        'independent_reference':'90-decimal-digit direct integral and digamma; not interval arithmetic',
        'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),
        'all_passed':all(c['passed'] for c in checks)}
    (ROOT/'advisor_independent_results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'checks'},indent=2))
    return out


if __name__ == '__main__':
    result = main()
    raise SystemExit(0 if result['all_passed'] else 1)
