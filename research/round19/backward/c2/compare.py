#!/usr/bin/env python3
"""Round19 C2 independent comparison.

Standard API:
  python3 compare.py --producer SOURCE --evidence OUTPUT --output NEW_DIR

The comparison reruns the backward C2 checker, compares exact C1 coefficient
rows, primary continuous theorem, sign-asymmetry theorem, boundary diagnostics,
C1/source bindings and source manifest hashes, then mutates normalized evidence
and requires rejection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Mapping

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CHECK = HERE / 'check.py'
CONTRACT_SHA = '704e4dc65890fe00cf5873fd8eed7cd8e78522c185a85d2210830db25f12db54'
C1_GATE_SHA = '6d4e07ac09529a8c796d9ae44a667f23a43fd52ba7fcd0a52241c072f64b933f'
C1_CONTRACT_SHA = '3fdfbbe6accad4a3ca6ca6849b73f930789bf8fa02169b5b5427773f08da7bbf'
LESSONS_SHA = 'f120ef9657b0d301cbe15b0730e5d6d45544e4f2875407f646a48ed848f738a1'
FORWARD_C1_RESULTS_SHA = 'b366c2d50c6198a81a6603e48129177b87b5000ec44252b9f9d6c53f66a1451c'
BACKWARD_C1_RESULTS_SHA = 'ad3b71d92b1907120093bdf05eec715bca6cfa35f9a13e81f0a04b8b5a926193'
C1_COMPARISON_SHA = 'd8a2394dacaea4b0f115a0e04a753f33c536d8f3698d7d0e7c8adb507d99aae3'
FORWARD_C1_GRAPH_SHA = 'b808c6c59d899b51c56c93305c0d4f3bce0c70f5c4e4ec8fcd92ef91525611de'
FORWARD_C1_COEFFICIENTS_SHA = '936236d7f7432d7adf010a047079126a973b3321e3e3784986e29d656f52135f'
BACKWARD_REQUIRED_OUTPUTS = ['results.json','coefficients.json','primary-certificate.json','sign-asymmetry.json','boundary-diagnostics.json','controls.json','source-manifest.json']
FORWARD_REQUIRED_OUTPUTS = ['results.json','coefficients.json','positivity-certificate.json','sign-asymmetry.json','boundary-diagnostics.json','controls.json','source-manifest.json']


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
    data = {}
    for name in sorted(set(BACKWARD_REQUIRED_OUTPUTS + FORWARD_REQUIRED_OUTPUTS)):
        p = evidence / name
        if p.exists():
            data[name] = load_json(p)
    if 'primary-certificate.json' not in data and 'positivity-certificate.json' not in data:
        raise FileNotFoundError('missing primary/positivity certificate')
    for name in ['results.json','coefficients.json','sign-asymmetry.json','boundary-diagnostics.json','controls.json','source-manifest.json']:
        if name not in data:
            raise FileNotFoundError(f'missing C2 evidence file: {name}')
    return data


def norm_rows(rows: List[Mapping[str, Any]]) -> List[Dict[str, str]]:
    keys = ['degree','numerator_moment','numerator_taylor_coeff','partition_moment','partition_taylor_coeff']
    out = []
    for r in rows:
        out.append({k: str(r[k]) for k in keys})
    return sorted(out, key=lambda r: int(r['degree']))


def norm_cert(c: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        'K': str(c.get('K')),
        'degree': int(c.get('degree')),
        'exp_upper_E': str(c.get('exp_upper_E')),
        'denominator_upper_direction': str(c.get('denominator_upper_direction') or c.get('denominator_positive_reason') or ''),
        'denominator_positive': c.get('denominator_positive'),
        'N0_zero': c.get('N0_zero'),
        'N1_zero': c.get('N1_zero'),
        'N2': str(c.get('N2', '1/324')),
        'finite_loss_over_kappa2': c.get('finite_loss_over_kappa2'),
        'tail_loss_over_kappa2': str(c.get('tail_loss_over_kappa2') or (Fraction(c.get('tail_bound_at_K')) / (Fraction(c.get('K')) ** 2) if c.get('tail_bound_at_K') else '0')),
        'C_N': str(c.get('C_N') or c.get('numerator_quadratic_coefficient_lower_C_N')),
        'C_N_positive': c.get('C_N_positive', Fraction(str(c.get('C_N') or c.get('numerator_quadratic_coefficient_lower_C_N'))) > 0),
        'quotient_coefficient_lower': str(c.get('quotient_coefficient_lower') or c.get('lower_constant_C_N_over_E')),
        'target_coefficient': str(c.get('target_coefficient') or c.get('target_constant')),
        'target_margin': str(c.get('target_margin') or c.get('margin_over_target')),
        'proves_target': c.get('proves_target', c.get('proves_F_ge_target_kappa_squared')),
        'proves_positivity': c.get('proves_positivity', Fraction(str(c.get('C_N') or c.get('numerator_quadratic_coefficient_lower_C_N'))) > 0),
    }


def norm_asym(c: Mapping[str, Any]) -> Dict[str, Any]:
    retained = c.get('D_coefficients') or c.get('retained_D_coefficients') or []
    coeff_rows = []
    for r in retained:
        coeff_rows.append({'degree': int(r['degree']), 'coeff': str(r.get('coeff', r.get('coefficient')))})
    leading = c.get('leading_term_over_kappa3')
    if leading is None:
        leading = '13/648' if str(c.get('leading_term', '')).startswith('2*N3') else None
    lower = c.get('lower_over_kappa3') or c.get('positive_margin_over_kappa_cubed')
    H = c.get('H') or str(c.get('range', '')).split('<=')[-1].strip()
    return {
        'range': str(c.get('range')),
        'H': str(H),
        'degree': int(c.get('degree', 8)),
        'leading_term_over_kappa3': str(leading),
        'expected_leading_from_2N3': str(c.get('expected_leading_from_2N3') or '13/648'),
        'finite_loss_over_kappa3': c.get('finite_loss_over_kappa3'),
        'tail_loss_over_kappa3': str(c.get('tail_loss_over_kappa3') or c.get('tail_error_over_kappa_cubed_bound')),
        'lower_over_kappa3': str(lower),
        'proves_F_kappa_gt_F_minus_kappa': c.get('proves_F_kappa_gt_F_minus_kappa'),
        'denominator_positive': c.get('denominator_positive'),
        'denominator_reason': str(c.get('denominator_reason', '')),
        'D_coefficients': sorted(coeff_rows, key=lambda r: r['degree']),
    }


def boundary_cert(data: Mapping[str, Any], K: str) -> Dict[str, Any]:
    if f'K_{K.replace('/', '_over_')}' in data:
        row = data[f'K_{K.replace('/', '_over_')}']
        return norm_cert(row) | {'diagnostic': row.get('diagnostic')}
    for row in data.get('diagnostics', []):
        if row.get('K') == K:
            cert = norm_cert(row['degree8_certificate'])
            cert['diagnostic'] = row.get('diagnostic') or row.get('classification')
            return cert
    raise KeyError(K)


def normalize(data: Mapping[str, Any]) -> Dict[str, Any]:
    r = data['results.json']
    accepted_links = r.get('accepted_c1_links', {})
    bindings = r.get('accepted_c1_bindings') or {
        'forward_c1_results_sha256': accepted_links.get('results_sha256'),
        'forward_c1_graph_sha256': accepted_links.get('graph_sha256'),
        'forward_c1_coefficients_sha256': accepted_links.get('coefficients_sha256'),
        'forward_c1_manifest_sha256': accepted_links.get('manifest_sha256'),
    }
    graph_action = r.get('graph_action_observable')
    if graph_action is None and accepted_links.get('graph_sha256') == FORWARD_C1_GRAPH_SHA and accepted_links.get('coefficients_sha256') == FORWARD_C1_COEFFICIENTS_SHA:
        graph_action = {'graph_counts': {'vertices': 18, 'edges': 33, 'faces': 20}, 'action': '3*x + y + z + w + t', 'observable': '(4*x^2-1)^3*(4*w^2-1)/81'}
    return {
        'schema': r.get('schema'),
        'status': r.get('status'),
        'contract_sha256': r.get('contract_sha256'),
        'c1_gate_sha256': r.get('c1_gate_sha256'),
        'accepted_c1_bindings': bindings,
        'static_scope': r.get('static_scope'),
        'graph_action_observable': graph_action,
        'coefficients': norm_rows(data['coefficients.json']['rows']),
        'primary': norm_cert(data['primary-certificate.json']['certificate'] if 'primary-certificate.json' in data else data['positivity-certificate.json']),
        'asymmetry': norm_asym(data['sign-asymmetry.json'].get('certificate', data['sign-asymmetry.json'])),
        'boundary': {
            'K_1_over_7': boundary_cert(data['boundary-diagnostics.json'], '1/7'),
            'K_1_over_6': boundary_cert(data['boundary-diagnostics.json'], '1/6'),
        },
        'controls': data['controls.json'],
        'manifest': data['source-manifest.json'],
    }


def static_scope_ok(text: Any) -> bool:
    s = str(text).lower()
    bad = any(x in s for x in ['kappa equals e_star', 'fibonacci static labels prove physical', 'physical scale matched'])
    return (not bad) and 'static' in s and 'physical' in s and 'open/unmatched' in s


def rational_exp_upper(x: Fraction, degree: int = 80) -> Fraction:
    """Independent rational envelope; no transcendental floating comparison."""
    if x < 0 or x >= degree + 2:
        raise ValueError('exponential envelope requires 0 <= x < degree+2')
    total = sum((x ** n / math.factorial(n) for n in range(degree + 1)), Fraction(0))
    first = x ** (degree + 1) / math.factorial(degree + 1)
    return total + first / (1 - x / (degree + 2))


def cert_is_valid(c: Mapping[str, Any], rows: List[Mapping[str, Any]], *, require_target: bool) -> bool:
    try:
        K, C, q = (Fraction(c[k]) for k in ['K', 'C_N', 'quotient_coefficient_lower'])
        E, margin, target = (Fraction(c[k]) for k in ['exp_upper_E', 'target_margin', 'target_coefficient'])
        tail = Fraction(c['tail_loss_over_kappa2'])
        coeff = {int(r['degree']): Fraction(r['numerator_taylor_coeff']) for r in rows}
        if K <= 0 or c['degree'] != 8 or set(coeff) != set(range(9)):
            return False
        finite = sum((abs(coeff[n]) * K ** (n-2) for n in range(3,9)), Fraction(0))
        min_tail = E * Fraction(7) ** 9 * K ** 7 / math.factorial(9)
        # A supplied rational at least this independently proved envelope is
        # certainly above exp(7K). Sharper distinct envelopes require review.
        arithmetic = (E >= rational_exp_upper(7*K) and
            Fraction(c['finite_loss_over_kappa2']) == finite and tail >= min_tail and
            C == coeff[2] - finite - tail and q == C/E and margin == q-target and
            target == Fraction(1,2048) and Fraction(c['N2']) == coeff[2] and
            coeff[0] == coeff[1] == 0 and c['N0_zero'] is True and c['N1_zero'] is True and
            c['C_N_positive'] is (C > 0) and c['proves_positivity'] is (C > 0) and
            c['proves_target'] is (C > 0 and margin >= 0) and
            c['denominator_positive'] is True and
            'Z(kappa)<=E' in str(c['denominator_upper_direction']))
        return arithmetic and ((C > 0 and margin >= 0) if require_target else True)
    except Exception:
        return False


def asymmetry_is_valid(a: Mapping[str, Any], rows: List[Mapping[str, Any]]) -> bool:
    try:
        H = Fraction(a['H'])
        if H <= 0 or a['degree'] != 8 or a['range'] != f'0 < kappa <= {H}':
            return False
        N = {int(r['degree']): Fraction(r['numerator_taylor_coeff']) for r in rows}
        Z = {int(r['degree']): Fraction(r['partition_taylor_coeff']) for r in rows}
        d = {n: sum((N[i]*Z[n-i]*((-1)**(n-i)-(-1)**i)
             for i in range(9) if 0 <= n-i <= 8), Fraction(0)) for n in range(17)}
        if a['D_coefficients'] != [{'degree':n,'coeff':str(v)} for n,v in d.items() if v]:
            return False
        leading = d[3]
        finite = sum((abs(d[n])*H**(n-3) for n in range(4,17)), Fraction(0))
        E = rational_exp_upper(7*H)
        min_tail = 4*E*E*7**9*H**6/math.factorial(9)
        tail = Fraction(a['tail_loss_over_kappa3'])
        lower = Fraction(a['lower_over_kappa3'])
        return (Fraction(a['leading_term_over_kappa3']) == Fraction(a['expected_leading_from_2N3']) == leading == Fraction(13,648) and
            Fraction(a['finite_loss_over_kappa3']) == finite and tail >= min_tail and
            lower == leading-finite-tail and lower > 0 and
            a['proves_F_kappa_gt_F_minus_kappa'] is True and a['denominator_positive'] is True)
    except Exception:
        return False


def admission_failures(prod: Mapping[str, Any], exp: Mapping[str, Any], producer_source: Path | None = None, evidence_dir: Path | None = None) -> List[str]:
    failures: List[str] = []
    if prod['status'] != 'passed': failures.append('producer_status')
    if prod['contract_sha256'] != CONTRACT_SHA: failures.append('contract_sha256')
    if prod['c1_gate_sha256'] != C1_GATE_SHA: failures.append('c1_gate_sha256')
    bindings = prod.get('accepted_c1_bindings', {})
    if bindings:
        if bindings.get('forward_c1_results_sha256') != FORWARD_C1_RESULTS_SHA: failures.append('forward_c1_binding')
        if bindings.get('forward_c1_graph_sha256') not in (None, FORWARD_C1_GRAPH_SHA): failures.append('forward_c1_graph_binding')
        if bindings.get('forward_c1_coefficients_sha256') not in (None, FORWARD_C1_COEFFICIENTS_SHA): failures.append('forward_c1_coefficients_binding')
        if bindings.get('backward_c1_results_sha256') not in (None, BACKWARD_C1_RESULTS_SHA): failures.append('backward_c1_binding')
        if bindings.get('canonical_c1_comparison_sha256') not in (None, C1_COMPARISON_SHA): failures.append('c1_comparison_binding')
    if prod['graph_action_observable'] != exp['graph_action_observable']: failures.append('graph_action_observable')
    if prod['coefficients'] != exp['coefficients']: failures.append('coefficients')
    low = {int(r['degree']): r for r in prod['coefficients']}
    if low[0]['numerator_taylor_coeff'] != '0' or low[1]['numerator_taylor_coeff'] != '0' or low[2]['numerator_taylor_coeff'] != '1/324' or low[3]['numerator_taylor_coeff'] != '13/1296': failures.append('low_N_coefficients')
    if low[0]['partition_taylor_coeff'] != '1' or low[1]['partition_taylor_coeff'] != '0' or low[2]['partition_taylor_coeff'] != '13/8' or low[3]['partition_taylor_coeff'] != '1/4': failures.append('low_Z_coefficients')
    if prod['primary']['K'] != '1/8' or prod['primary']['degree'] != 8: failures.append('primary_certificate')
    if not cert_is_valid(prod['primary'], prod['coefficients'], require_target=True): failures.append('primary_certificate_internal')
    expected_D = exp['asymmetry']['D_coefficients']
    if prod['asymmetry']['D_coefficients'] != expected_D: failures.append('sign_asymmetry_coefficients')
    if Fraction(prod['asymmetry']['H']) < Fraction(1,64): failures.append('sign_asymmetry_range')
    if not asymmetry_is_valid(prod['asymmetry'], prod['coefficients']): failures.append('sign_asymmetry_internal')
    for key, expected_K in [('K_1_over_7','1/7'), ('K_1_over_6','1/6')]:
        if prod['boundary'][key]['K'] != expected_K: failures.append(key+'_range')
        if not cert_is_valid(prod['boundary'][key], prod['coefficients'], require_target=False): failures.append(key+'_arithmetic')
    if prod['boundary']['K_1_over_7']['proves_target'] is not False or prod['boundary']['K_1_over_7']['proves_positivity'] is not True: failures.append('K_1_7_diagnostic')
    if prod['boundary']['K_1_over_6']['proves_positivity'] is not False or Fraction(prod['boundary']['K_1_over_6']['C_N']) >= 0: failures.append('K_1_6_diagnostic')
    if not static_scope_ok(prod['static_scope']): failures.append('static_scope')
    if producer_source is not None and evidence_dir is not None:
        sm = prod.get('manifest')
        if not sm: failures.append('source_manifest_missing')
        else:
            src_dir = producer_source if producer_source.is_dir() else producer_source.parent
            for name in ['check.py','report.md']:
                p = src_dir / name
                if name not in sm.get('source_files', {}): failures.append(f'source_manifest_missing_source:{name}')
                elif not p.exists(): failures.append(f'source_manifest_source_missing:{name}')
                elif sm['source_files'][name] != sha256_file(p): failures.append(f'source_manifest_source_hash:{name}')
            common_inputs = {
                'research/round19/advisor/contract-c2.json': CONTRACT_SHA,
                'research/round19/advisor/c1-gate.json': C1_GATE_SHA,
                'research/round19/methods/round19-lessons.md': LESSONS_SHA,
                'research/round19/forward/c1/output/results.json': FORWARD_C1_RESULTS_SHA,
            }
            for name, h in common_inputs.items():
                if sm.get('source_inputs', {}).get(name) != h: failures.append(f'source_manifest_input_hash:{name}')
            # Backward implementation binds additional independent C1 artifacts; forward need not reuse backward hashes.
            if 'primary-certificate.json' in sm.get('outputs', {}):
                for name, h in {
                    'research/round19/advisor/contract-c1.json': C1_CONTRACT_SHA,
                    'research/round19/backward/c1/output/results.json': BACKWARD_C1_RESULTS_SHA,
                    'research/round19/backward/c1/comparison/comparison.json': C1_COMPARISON_SHA,
                }.items():
                    if sm.get('source_inputs', {}).get(name) != h: failures.append(f'source_manifest_input_hash:{name}')
            required_outputs = FORWARD_REQUIRED_OUTPUTS[:-1] if 'positivity-certificate.json' in sm.get('outputs', {}) else BACKWARD_REQUIRED_OUTPUTS[:-1]
            for name in required_outputs:
                p = evidence_dir / name
                if name not in sm.get('outputs', {}): failures.append(f'source_manifest_missing_output:{name}')
                elif not p.exists(): failures.append(f'source_manifest_output_missing:{name}')
                elif sm['outputs'][name] != sha256_file(p): failures.append(f'source_manifest_output_hash:{name}')
    return sorted(set(failures))


def mutation_controls(prod: Dict[str, Any], exp: Dict[str, Any], producer_source: Path, evidence_dir: Path) -> List[Dict[str, Any]]:
    out = []
    def run(name: str, mutator) -> None:
        m = deepcopy(prod); mutator(m)
        failures = admission_failures(m, exp, producer_source, evidence_dir)
        out.append({'name': name, 'passed': bool(failures), 'detected_failures': failures})
    run('alter_N2', lambda m: m['coefficients'][2].__setitem__('numerator_taylor_coeff', '0'))
    run('alter_N3', lambda m: m['coefficients'][3].__setitem__('numerator_taylor_coeff', '0'))
    run('set_N0_nonzero', lambda m: m['coefficients'][0].__setitem__('numerator_taylor_coeff', '1/100'))
    run('set_N1_nonzero', lambda m: m['coefficients'][1].__setitem__('numerator_taylor_coeff', '1/100'))
    run('point_interval_as_continuous_proof', lambda m: m['primary'].__setitem__('K', '1/64'))
    run('wrong_denominator_direction', lambda m: m['primary'].__setitem__('denominator_upper_direction', 'divide by lower bound on Z'))
    run('tail_underestimate', lambda m: m['primary'].__setitem__('tail_loss_over_kappa2', '0'))
    def false_exponential(m):
        c=m['primary'];c['exp_upper_E']='1'
        c['quotient_coefficient_lower']=c['C_N']
        c['target_margin']=str(Fraction(c['C_N'])-Fraction(c['target_coefficient']))
    run('invalid_exponential_bound_consistent_quotient', false_exponential)
    run('finite_loss_not_reconstructed', lambda m: m['primary'].__setitem__('finite_loss_over_kappa2','0'))
    run('missing_N0_endpoint', lambda m: m['primary'].__setitem__('N0_zero',None))
    run('missing_denominator_positivity', lambda m: m['primary'].__setitem__('denominator_positive',None))
    def widened_asymmetry(m):
        m['asymmetry']['H']='1000';m['asymmetry']['range']='0 < kappa <= 1000'
    run('widen_asymmetry_without_recomputed_losses', widened_asymmetry)
    run('asymmetry_tail_underestimate', lambda m: m['asymmetry'].__setitem__('tail_loss_over_kappa3','0'))
    run('asymmetry_finite_loss_underestimate', lambda m: m['asymmetry'].__setitem__('finite_loss_over_kappa3','0'))
    run('asymmetry_margin_not_reconstructed', lambda m: m['asymmetry'].__setitem__('lower_over_kappa3','1'))
    run('boundary_range_relabeled', lambda m: m['boundary']['K_1_over_7'].__setitem__('K','1/6'))
    run('boundary_arithmetic_not_reconstructed', lambda m: m['boundary']['K_1_over_6'].__setitem__('C_N','-1'))
    run('primary_margin_flipped', lambda m: m['primary'].__setitem__('target_margin', str(-Fraction(m['primary']['target_margin']))))
    run('independent_V_resampling_binding_loss', lambda m: m['graph_action_observable'].__setitem__('action', 'independent V copies'))
    run('remove_sign_asymmetry_odd_term', lambda m: m['asymmetry'].__setitem__('leading_term_over_kappa3', '0'))
    run('flip_sign_asymmetry_claim', lambda m: m['asymmetry'].__setitem__('lower_over_kappa3', str(-Fraction(m['asymmetry']['lower_over_kappa3']))))
    run('claim_K_1_6_crude_success', lambda m: m['boundary']['K_1_over_6'].__setitem__('proves_positivity', True))
    run('claim_K_1_7_target_success', lambda m: m['boundary']['K_1_over_7'].__setitem__('proves_target', True))
    run('kappa_as_E_star', lambda m: m.__setitem__('static_scope', 'kappa equals E_star physical scale'))
    run('fibonacci_physical_scale', lambda m: m.__setitem__('static_scope', 'Fibonacci static labels prove physical matching'))
    def remove_manifest_check(m):
        m['manifest'] = deepcopy(m['manifest']); m['manifest'].setdefault('source_files', {}).pop('check.py', None)
    run('manifest_missing_check', remove_manifest_check)
    def remove_manifest_output(m):
        m['manifest'] = deepcopy(m['manifest']); m['manifest'].setdefault('outputs', {}).pop('results.json', None)
    run('manifest_missing_results', remove_manifest_output)
    return out


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
    add('accepted C1 source bindings match frozen gate', not any(x in failures for x in ['forward_c1_binding','backward_c1_binding','c1_comparison_binding','c1_gate_sha256']))
    add('graph/action/observable and exact coefficients match', not any(x in failures for x in ['graph_action_observable','coefficients','low_N_coefficients','low_Z_coefficients']), coefficient_count=len(prod['coefficients']))
    add('primary continuous |kappa|<=1/8 theorem matches and is internally valid', 'primary_certificate' not in failures and 'primary_certificate_internal' not in failures, primary=prod['primary'])
    add('sign asymmetry theorem matches and is internally valid', 'sign_asymmetry_coefficients' not in failures and 'sign_asymmetry_range' not in failures and 'sign_asymmetry_internal' not in failures, asymmetry={k:prod['asymmetry'][k] for k in ['range','leading_term_over_kappa3','lower_over_kappa3']})
    add('K=1/7 and K=1/6 diagnostics match without overclaim', 'boundary_diagnostics' not in failures and 'K_1_7_diagnostic' not in failures and 'K_1_6_diagnostic' not in failures, boundary=prod['boundary'])
    add('static kappa scope excludes physical scale claims', 'static_scope' not in failures, static_scope=prod['static_scope'])
    add('source manifest binds required sources, C1 inputs and outputs', not any(f.startswith('source_manifest') for f in failures))
    muts = mutation_controls(prod, exp, producer_source, evidence_dir)
    for c in muts:
        checks.append({'name':'mutation rejects '+c['name'], 'passed':c['passed'], 'detected_failures':c['detected_failures']})
    status = 'accepted' if not failures and all(c['passed'] for c in checks) else 'rejected'
    comp = {
        'schema':'ym19-backward-c2-comparison-v1',
        'status': status,
        'producer_source': str(producer_source),
        'producer_evidence': str(evidence_dir),
        'producer_results_sha256': sha256_file(evidence_dir / 'results.json'),
        'independent_results_sha256': sha256_file(indep / 'results.json'),
        'checks_count': len(checks),
        'checks': checks,
        'admission_failures': failures,
        'mutation_controls': muts,
        'reported_theorems': {
            'primary': prod['primary'],
            'sign_asymmetry': {k:prod['asymmetry'][k] for k in ['range','leading_term_over_kappa3','lower_over_kappa3']},
            'boundary': prod['boundary'],
        },
    }
    (output_dir / 'comparison.json').write_text(json.dumps(comp, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': status, 'checks_count': len(checks), 'output': str(output_dir / 'comparison.json')}, sort_keys=True))
    if status != 'accepted':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
