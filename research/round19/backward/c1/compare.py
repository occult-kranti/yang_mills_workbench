#!/usr/bin/env python3
"""Round19 C1 independent comparison.

Standard API:
  python3 compare.py --producer SOURCE --evidence OUTPUT --output NEW_DIR

The comparator reruns backward C1 into NEW_DIR/independent-reconstruction,
normalizes evidence with the C1 source-bound schema, compares graph reduction,
moment coefficients, normalized intervals, static-scale wording, and source
manifest bindings, then mutates normalized evidence and requires rejection.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from fractions import Fraction
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Mapping

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CHECK = HERE / 'check.py'
CONTRACT_SHA = '3fdfbbe6accad4a3ca6ca6849b73f930789bf8fa02169b5b5427773f08da7bbf'
B2_GATE_SHA = 'cd0c1082b460ca3af1c465daf2398c698ca5819caa11781bc64688f539709b8c'
LESSONS_SHA = 'f120ef9657b0d301cbe15b0730e5d6d45544e4f2875407f646a48ed848f738a1'
BACKWARD_REQUIRED_OUTPUTS = ['results.json','graph-reduction.json','moments.json','coefficients.json','intervals.json','refinement.csv','source-manifest.json']
FORWARD_REQUIRED_OUTPUTS = ['results.json','graph-reduction.json','moments.json','moment-table.json','coefficients.json','intervals.json','controls.json','freeze-W-regression.json','refinement.csv']
ALL_KNOWN_OUTPUTS = sorted(set(BACKWARD_REQUIRED_OUTPUTS + FORWARD_REQUIRED_OUTPUTS + ['source-manifest.json']))
TARGET_WIDTH = Fraction(1, 10**12)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def run_independent(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, '-B']
    if sys.flags.optimize:
        cmd.append('-' + 'O' * sys.flags.optimize)
    cmd += [str(CHECK), '--output', str(out)]
    subprocess.run(cmd, check=True)


def load_output(evidence: Path) -> Dict[str, Any]:
    data = {name: load_json(evidence / name) for name in ALL_KNOWN_OUTPUTS if name.endswith('.json') and (evidence / name).exists()}
    if (evidence / 'refinement.csv').exists():
        data['refinement.csv.sha256'] = sha256_file(evidence / 'refinement.csv')
    missing = [name for name in ['results.json','graph-reduction.json','coefficients.json','intervals.json'] if name not in data]
    if missing:
        raise FileNotFoundError(f'missing required C1 evidence files: {missing}')
    return data



def norm_moments(data: Mapping[str, Any]) -> List[Dict[str, str]]:
    if 'moments.json' in data and 'moments' in data['moments.json']:
        rows = data['moments.json']['moments']
        out = []
        for row in rows:
            exp = row['exponents']
            if isinstance(exp, dict):
                exp = [exp[k] for k in ['x','y','z','w','t']]
            out.append({'exponents': list(exp), 'value': str(row.get('value', row.get('moment')))})
        return sorted(out, key=lambda r: (sum(r['exponents']), r['exponents']))
    mt = data['moment-table.json']
    out = []
    for row in mt['rows']:
        expd = row['exponents']
        out.append({'exponents': [expd['x'], expd['y'], expd['z'], expd['w'], expd['t']], 'value': str(row['moment'])})
    return sorted(out, key=lambda r: (sum(r['exponents']), r['exponents']))


def interval_rows(intervals: Mapping[str, Any], sign: str) -> List[Mapping[str, Any]]:
    key = 'positive_kappa' if sign == '+' else 'negative_kappa'
    return list(intervals[key])


def geometric_tail_bound(k: Fraction, degree: int, S_abs_bound: Fraction = Fraction(7)) -> Fraction:
    M = abs(k) * S_abs_bound
    if not (Fraction(0) <= M < Fraction(1, 2)):
        raise ValueError('bad M for C1 geometric tail')
    return (M ** (degree + 1)) / (math.factorial(degree + 1) * (1 - M))


def quotient_interval(A: Fraction, Z: Fraction, R: Fraction) -> tuple[Fraction, Fraction]:
    if R < 0 or Z - R <= 0:
        raise ValueError('invalid quotient denominator interval')
    vals = [(A + da * R) / (Z + dz * R) for da in [-1, 1] for dz in [-1, 1]]
    return min(vals), max(vals)


def partial_from_coeffs(coeff_rows: List[Mapping[str, Any]], k: Fraction, degree: int) -> tuple[Fraction, Fraction]:
    A = Fraction(0); Z = Fraction(0)
    for row in coeff_rows:
        n = int(row['degree'])
        if n <= degree:
            A += Fraction(row['numerator_taylor_coeff']) * (k ** n)
            Z += Fraction(row['partition_taylor_coeff']) * (k ** n)
    return A, Z


def interval_pair(row: Mapping[str, Any]) -> List[str]:
    if 'normalized_interval' in row:
        return list(row['normalized_interval'])
    return [str(row['lower']), str(row['upper'])]


def validate_interval_ladder(intervals: Mapping[str, Any], coeff_rows: List[Mapping[str, Any]]) -> List[str]:
    problems = []
    for sign, k in [('+', Fraction(1,64)), ('-', Fraction(-1,64))]:
        rows = interval_rows(intervals, sign)
        if [int(r['degree']) for r in rows] != [0,2,4,6,8]:
            problems.append(f'{sign}:degree_ladder')
            continue
        for row in rows:
            n = int(row['degree'])
            if str(row['kappa']) != ('1/64' if sign == '+' else '-1/64'):
                problems.append(f'{sign}:{n}:kappa')
            A, Z = partial_from_coeffs(coeff_rows, k, n)
            if Fraction(row['partial_numerator']) != A or Fraction(row['partial_partition']) != Z:
                problems.append(f'{sign}:{n}:partial')
            R = Fraction(row.get('remainder_abs_bound', row.get('tail_bound')))
            if R < geometric_tail_bound(k, n):
                problems.append(f'{sign}:{n}:tail_too_small')
            try:
                lo, hi = quotient_interval(A, Z, R)
            except Exception:
                problems.append(f'{sign}:{n}:bad_denominator')
                continue
            got_lo, got_hi = map(Fraction, interval_pair(row))
            if (got_lo, got_hi) != (lo, hi):
                problems.append(f'{sign}:{n}:interval_endpoints')
            if Fraction(row['width']) != hi - lo:
                problems.append(f'{sign}:{n}:width')
            target_flag = row.get('width_below_target_1e_minus_12', row.get('meets_target'))
            if n == 8 and not (hi - lo <= TARGET_WIDTH and target_flag is True):
                problems.append(f'{sign}:{n}:target_width')
    return problems


def expected_freeze_old_coefficients() -> Dict[str, List[str]]:
    spec = importlib.util.spec_from_file_location('ym19_backward_c1_check', CHECK)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    obs = mod.observable_poly()
    oldS = mod.add_poly(mod.add_poly(mod.one_var_power(0, 1, Fraction(3)), mod.one_var_power(1, 1, Fraction(2))), mod.one_var_power(3, 1, Fraction(1)))
    rows = mod.coefficients(obs, oldS, 8)['rows']
    return {'numerator': [str(r['numerator_taylor_coeff']) for r in rows], 'partition': [str(r['partition_taylor_coeff']) for r in rows]}


def freeze_ok(prod_freeze: Mapping[str, Any], exp_freeze: Mapping[str, Any]) -> bool:
    if prod_freeze == exp_freeze:
        return True
    coeffs = expected_freeze_old_coefficients()
    if prod_freeze.get('coefficients_match_round18_C2_V_only_2') is not True:
        return False
    if prod_freeze.get('reduced_action_after_canceling_constant') != '3*x + 2*y + w':
        return False
    if prod_freeze.get('numerator_coefficients') != coeffs['numerator']:
        return False
    if prod_freeze.get('partition_coefficients') != coeffs['partition']:
        return False
    final = prod_freeze.get('final', {})
    try:
        return Fraction(final['upper']) >= Fraction(final['lower']) and Fraction(final['width']) == Fraction(final['upper']) - Fraction(final['lower']) and final.get('meets_target') is True
    except Exception:
        return False

def normalize(data: Mapping[str, Any]) -> Dict[str, Any]:
    r = data['results.json']
    g = data['graph-reduction.json']
    moments = norm_moments(data)
    coeffs = data['coefficients.json']
    intervals = data['intervals.json']
    sm = data.get('source-manifest.json', {})
    affected = sorted((f['face'], tuple((a['symbol'], a['sign']) for a in f['active_word']), f['reduced_symbol']) for f in g['affected_faces'])
    constants = sorted(f['face'] for f in g['constant_faces'])
    kind = 'forward' if 'moment-table.json' in data or 'freeze-W-regression.json' in data else 'backward'
    return {
        'kind': kind,
        'schema': r.get('schema'),
        'status': r.get('status'),
        'kappa': r.get('kappa'),
        'max_taylor_degree': r.get('max_taylor_degree'),
        'degree_ladder': r.get('degree_ladder'),
        'graph_counts': r.get('graph_counts'),
        'active_links': g.get('active_links'),
        'affected_faces': affected,
        'constant_faces': constants,
        'derived_S': r.get('derived_S'),
        'observable': r.get('observable'),
        'common_V_discriminator': r.get('common_V_discriminator'),
        'signed_quaternion_fixture': r.get('signed_quaternion_fixture'),
        'primary_normalized_interval': r.get('primary_normalized_interval'),
        'negative_kappa_fixture': r.get('negative_kappa_fixture'),
        'freeze_W_identity_regression': r.get('freeze_W_identity_regression') or data.get('freeze-W-regression.json'),
        'physical_scale_exception': r.get('physical_scale_exception'),
        'coefficient_rows': coeffs.get('rows'),
        'moments': moments,
        'intervals': intervals,
        'manifest': sm,
    }


def static_scope_ok(scale: Mapping[str, Any]) -> bool:
    text = ' '.join((str(k) + ' ' + str(v)).lower() for k, v in scale.items())
    return 'static' in text and 'not e_star' in text and 'open/unmatched' in text and 'physical' in text and 'fibonacci' in text


def admission_failures(prod: Mapping[str, Any], exp: Mapping[str, Any], producer_source: Path | None = None, evidence_dir: Path | None = None) -> List[str]:
    failures: List[str] = []
    if prod['status'] != 'passed': failures.append('producer_status')
    if prod['kappa'] != '1/64': failures.append('kappa')
    if prod['max_taylor_degree'] != 8 or prod['degree_ladder'] != [0,2,4,6,8]: failures.append('degree_ladder')
    if prod['graph_counts'] != {'active_links':3,'affected_faces':7,'constant_faces':13,'edges':33,'faces':20,'fixed_links':30,'vertices':18}: failures.append('graph_counts')
    coords = {k: tuple(v['coordinate']) for k, v in prod['active_links'].items()}
    if coords != {'U':(1,1,0),'V':(1,0,0),'W':(0,0,0)}: failures.append('active_link_coordinates')
    if prod['affected_faces'] != exp['affected_faces']: failures.append('affected_face_words')
    if prod['constant_faces'] != exp['constant_faces']: failures.append('constant_face_ledger')
    if prod['derived_S'] != '3*x + y + z + w + t': failures.append('derived_S')
    if prod['observable'] != '(4*x^2-1)^3*(4*w^2-1)/81': failures.append('observable')
    if prod['common_V_discriminator'] != {'exponents':[1,0,1,1,1], 'value':'1/64', 'independent_V_resampling_value':'0'}: failures.append('common_V_discriminator')
    qfix = prod.get('signed_quaternion_fixture') or {}
    if not (qfix.get('w_sign_flip_detected') is True and qfix.get('t_sign_flip_detected') is True and qfix.get('w_correct_Tr_UVdagger_over_2') != qfix.get('w_wrong_Tr_UV_over_2') and qfix.get('t_correct_Tr_VWdagger_over_2') != qfix.get('t_wrong_Tr_VW_over_2')):
        failures.append('signed_quaternion_fixture')
    for key in ['coefficient_rows','moments']:
        if prod[key] != exp[key]: failures.append(key)
    interval_problems = validate_interval_ladder(prod['intervals'], prod['coefficient_rows'])
    if interval_problems: failures.append('interval_ladder:' + ','.join(interval_problems[:5]))
    try:
        pos_last = interval_rows(prod['intervals'], '+')[-1]
        neg_last = interval_rows(prod['intervals'], '-')[-1]
        if prod.get('primary_normalized_interval') and interval_pair(prod['primary_normalized_interval']) != interval_pair(pos_last):
            failures.append('primary_interval_fixture')
        if prod.get('negative_kappa_fixture') and interval_pair(prod['negative_kappa_fixture']) != interval_pair(neg_last):
            failures.append('negative_kappa_fixture')
        plo, phi = map(Fraction, interval_pair(pos_last))
        nlo, nhi = map(Fraction, interval_pair(neg_last))
        if not (phi < nlo or nhi < plo):
            failures.append('signed_kappa_enclosures_not_disjoint')
    except Exception:
        failures.append('signed_kappa_fixture')
    # Keep backward self-comparison byte-exact, but allow producer intervals to use a different rigorous tail bound.
    if prod['kind'] == 'backward' and prod['intervals'] != exp['intervals']:
        failures.append('intervals')
    if not freeze_ok(prod['freeze_W_identity_regression'], exp['freeze_W_identity_regression']):
        failures.append('freeze_W_identity_regression')
    if not static_scope_ok(prod['physical_scale_exception']): failures.append('static_physical_scale_exception')
    if producer_source is not None and evidence_dir is not None:
        sm = prod.get('manifest')
        if not sm: failures.append('source_manifest_missing')
        else:
            src_dir = producer_source if producer_source.is_dir() else producer_source.parent
            for name in ['check.py','report.md']:
                p = src_dir / name
                if name not in sm.get('source_files', {}): failures.append(f'source_manifest_missing_source:{name}')
                elif not p.exists(): failures.append(f'source_manifest_source_file_missing:{name}')
                elif sm['source_files'][name] != sha256_file(p): failures.append(f'source_manifest_source_hash:{name}')
            src_inputs = sm.get('source_inputs', {})
            expected_inputs = {
                'research/round19/advisor/contract-c1.json': CONTRACT_SHA,
                'research/round19/advisor/b2-gate.json': B2_GATE_SHA,
                'research/round19/methods/round19-lessons.md': LESSONS_SHA,
            }
            for name, h in expected_inputs.items():
                if src_inputs.get(name) != h: failures.append(f'source_manifest_input_hash:{name}')
            outs = sm.get('outputs', {})
            required_outputs = FORWARD_REQUIRED_OUTPUTS if prod.get('kind') == 'forward' else BACKWARD_REQUIRED_OUTPUTS[:-1]
            for name in required_outputs:
                p = evidence_dir / name
                if name not in outs: failures.append(f'source_manifest_missing_output:{name}')
                elif not p.exists(): failures.append(f'source_manifest_output_file_missing:{name}')
                elif outs[name] != sha256_file(p): failures.append(f'source_manifest_output_hash:{name}')
    return sorted(set(failures))


def mutation_controls(prod: Dict[str, Any], exp: Dict[str, Any], producer_source: Path, evidence_dir: Path) -> List[Dict[str, Any]]:
    controls = []
    def run(name: str, mutator) -> None:
        m = deepcopy(prod); mutator(m)
        failures = admission_failures(m, exp, producer_source, evidence_dir)
        controls.append({'name': name, 'passed': bool(failures), 'detected_failures': failures})
    run('wrong_graph_counts', lambda m: m['graph_counts'].__setitem__('edges', 32))
    run('wrong_active_link_U', lambda m: m['active_links']['U'].__setitem__('coordinate', [1,0,0]))
    run('omit_affected_face', lambda m: m['affected_faces'].pop())
    def alter_signed_word(m):
        rows = list(m['affected_faces'])
        face, word, sym = rows[0]
        for idx, row in enumerate(rows):
            if row[2] == 't':
                face, word, sym = row
                rows[idx] = (face, (('V', -1), ('W', 1)), sym)
                break
        m['affected_faces'] = rows
    run('alter_noncommuting_signed_VW_word', alter_signed_word)
    run('omit_constant_face_ledger', lambda m: m['constant_faces'].pop())
    run('hardcode_wrong_S', lambda m: m.__setitem__('derived_S', '3*x+y+z+w+t'))
    run('alter_observable', lambda m: m.__setitem__('observable', '(4*x^2-1)^3/27'))
    run('independent_V_claimed_primary', lambda m: m['common_V_discriminator'].__setitem__('value', '0'))
    run('numeric_quaternion_sign_flip_hidden', lambda m: m['signed_quaternion_fixture'].__setitem__('w_wrong_Tr_UV_over_2', m['signed_quaternion_fixture']['w_correct_Tr_UVdagger_over_2']))
    run('drop_moment_divisor_effect', lambda m: m['moments'][0].__setitem__('value', '2'))
    run('truncate_degree_6_as_final', lambda m: m.__setitem__('max_taylor_degree', 6))
    run('negative_kappa_evenness_forced', lambda m: m.__setitem__('negative_kappa_fixture', m['primary_normalized_interval']))
    run('delete_freeze_regression', lambda m: m.__setitem__('freeze_W_identity_regression', {}))
    run('kappa_as_physical_scale', lambda m: m.__setitem__('physical_scale_exception', {'kappa':'E_star'}))
    run('fibonacci_as_physical_match', lambda m: m.__setitem__('physical_scale_exception', {'classification':'Fibonacci physical scale matched'}))
    def remove_manifest_check(m):
        m['manifest'] = deepcopy(m['manifest']); m['manifest'].setdefault('source_files', {}).pop('check.py', None)
    run('manifest_missing_check_hash', remove_manifest_check)
    def remove_manifest_output(m):
        m['manifest'] = deepcopy(m['manifest']); m['manifest'].setdefault('outputs', {}).pop('results.json', None)
    run('manifest_missing_results_hash', remove_manifest_output)
    return controls


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--producer', required=True)
    ap.add_argument('--evidence', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    producer_source = Path(args.producer).resolve()
    evidence_dir = Path(args.evidence).resolve()
    output_dir = Path(args.output).resolve(); output_dir.mkdir(parents=True, exist_ok=True)
    indep = output_dir / 'independent-reconstruction'
    run_independent(indep)
    exp = normalize(load_output(indep))
    prod = normalize(load_output(evidence_dir))
    failures = admission_failures(prod, exp, producer_source, evidence_dir)
    checks = []
    def add(name: str, passed: bool, **extra):
        row = {'name': name, 'passed': bool(passed)}; row.update(extra); checks.append(row)
    add('graph counts and active coordinates match contract', not any(f in failures for f in ['graph_counts','active_link_coordinates']), graph_counts=prod['graph_counts'])
    add('signed affected face words and constant ledger match independent reconstruction', not any(f in failures for f in ['affected_face_words','constant_face_ledger']), affected_count=len(prod['affected_faces']), constant_count=len(prod['constant_faces']))
    add('S=3*x+y+z+w+t is derived and observable unchanged', not any(f in failures for f in ['derived_S','observable']))
    add('character-fusion and conditional-polynomial moment table matches', 'moments' not in failures, moment_count=len(prod['moments']))
    add('Taylor coefficients match and interval ladder validates', not any(f == 'coefficient_rows' or f == 'intervals' or f.startswith('interval_ladder') for f in failures), primary_interval=prod['primary_normalized_interval'])
    add('common-V discriminator and independent-V failure are exact', 'common_V_discriminator' not in failures, discriminator=prod['common_V_discriminator'])
    add('numeric quaternion signed-word fixture detects active sign flips', 'signed_quaternion_fixture' not in failures, fixture=prod.get('signed_quaternion_fixture'))
    add('freeze-W identity regression is present', 'freeze_W_identity_regression' not in failures)
    add('static kappa is marked unmatched to physical scale', 'static_physical_scale_exception' not in failures, scale_exception=prod['physical_scale_exception'])
    add('source manifest binds source, gates and required outputs', not any(f.startswith('source_manifest') for f in failures))
    muts = mutation_controls(prod, exp, producer_source, evidence_dir)
    for c in muts: checks.append({'name': 'mutation rejects ' + c['name'], 'passed': c['passed'], 'detected_failures': c['detected_failures']})
    status = 'accepted' if not failures and all(c['passed'] for c in checks) else 'rejected'
    comp = {'schema':'ym19-backward-c1-comparison-v1', 'status':status, 'producer_source':str(producer_source), 'producer_evidence':str(evidence_dir), 'producer_results_sha256':sha256_file(evidence_dir/'results.json'), 'independent_results_sha256':sha256_file(indep/'results.json'), 'checks_count':len(checks), 'checks':checks, 'admission_failures':failures, 'mutation_controls':muts}
    (output_dir/'comparison.json').write_text(json.dumps(comp, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status':status, 'checks_count':len(checks), 'output':str(output_dir/'comparison.json')}, sort_keys=True))
    if status != 'accepted': raise SystemExit(1)


if __name__ == '__main__':
    main()
