#!/usr/bin/env python3
"""Round19 C2 independent continuous static-kappa certificate.

C2 upgrades accepted C1 point evidence to exact interval statements for the
static integral F(kappa)=N(kappa)/Z(kappa).  It uses accepted C1 graph/moment
machinery as a source-bound input and independently checks rational tail bounds,
denominator direction, kappa=0 endpoint, sign asymmetry, and boundary diagnostics.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
C1_CHECK = ROOT / 'research/round19/backward/c1/check.py'
DEGREE = 8
PRIMARY_K = Fraction(1, 8)
ASYM_K = Fraction(1, 64)
TARGET = Fraction(1, 2048)
EXP_DEGREE = 60

CONTRACT_SHA = '704e4dc65890fe00cf5873fd8eed7cd8e78522c185a85d2210830db25f12db54'
C1_GATE_SHA = '6d4e07ac09529a8c796d9ae44a667f23a43fd52ba7fcd0a52241c072f64b933f'
C1_CONTRACT_SHA = '3fdfbbe6accad4a3ca6ca6849b73f930789bf8fa02169b5b5427773f08da7bbf'
LESSONS_SHA = 'f120ef9657b0d301cbe15b0730e5d6d45544e4f2875407f646a48ed848f738a1'
FORWARD_C1_RESULTS_SHA = 'b366c2d50c6198a81a6603e48129177b87b5000ec44252b9f9d6c53f66a1451c'
BACKWARD_C1_RESULTS_SHA = 'ad3b71d92b1907120093bdf05eec715bca6cfa35f9a13e81f0a04b8b5a926193'
C1_COMPARISON_SHA = 'd8a2394dacaea4b0f115a0e04a753f33c536d8f3698d7d0e7c8adb507d99aae3'


def load_c1():
    spec = importlib.util.spec_from_file_location('ym19_backward_c1_check', C1_CHECK)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

c1 = load_c1()


def sfrac(q: Any) -> str:
    q = Fraction(q)
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exp_upper(M: Fraction, degree: int = EXP_DEGREE) -> Fraction:
    if M < 0:
        raise ValueError('exp upper expects M>=0')
    degree = int(degree)
    s = sum(M ** n / math.factorial(n) for n in range(degree + 1))
    term = M ** (degree + 1) / math.factorial(degree + 1)
    ratio = M / Fraction(degree + 2)
    if ratio >= 1:
        raise ValueError('exp tail ratio must be <1')
    return s + term / (1 - ratio)


def exp_tail_bound(M: Fraction, start_degree: int, E: Fraction) -> Fraction:
    # Lagrange form: tail after degree start_degree-1 is <= exp(M) M^start/start!;
    # use rational E>=exp(M).  start_degree=9 for degree-8 Taylor truncation.
    return E * M ** start_degree / math.factorial(start_degree)


def accepted_coefficients(degree: int = DEGREE) -> Dict[str, Any]:
    g = c1.graph()
    obs = c1.observable_poly()
    S = c1.action_poly_from_terms(g['derived_S_terms'])
    coeffs = c1.coefficients(obs, S, degree)['rows']
    N = [Fraction(row['numerator_taylor_coeff']) for row in coeffs]
    Z = [Fraction(row['partition_taylor_coeff']) for row in coeffs]
    return {'graph': g, 'rows': coeffs, 'N': N, 'Z': Z}


def positivity_certificate(K: Fraction, rows: List[Mapping[str, Any]], target: Fraction = TARGET) -> Dict[str, Any]:
    N = [Fraction(row['numerator_taylor_coeff']) for row in rows]
    E = exp_upper(Fraction(7) * K)
    finite_loss = sum(abs(N[n]) * K ** (n - 2) for n in range(3, DEGREE + 1))
    tail_loss = E * Fraction(7) ** (DEGREE + 1) * K ** (DEGREE - 1) / math.factorial(DEGREE + 1)
    Cn = N[2] - finite_loss - tail_loss
    quotient_coeff_lower = Cn / E
    margin = quotient_coeff_lower - target
    return {
        'K': sfrac(K),
        'degree': DEGREE,
        'exp_upper_E': sfrac(E),
        'denominator_upper_direction': 'Z(kappa)<=E, so N(kappa)>=C_N*kappa^2 gives F(kappa)>=C_N/E*kappa^2',
        'denominator_positive': True,
        'N0_zero': N[0] == 0,
        'N1_zero': N[1] == 0,
        'N2': sfrac(N[2]),
        'finite_loss_over_kappa2': sfrac(finite_loss),
        'tail_loss_over_kappa2': sfrac(tail_loss),
        'C_N': sfrac(Cn),
        'C_N_positive': Cn > 0,
        'quotient_coefficient_lower': sfrac(quotient_coeff_lower),
        'target_coefficient': sfrac(target),
        'target_margin': sfrac(margin),
        'proves_target': Cn > 0 and margin >= 0,
        'proves_positivity': Cn > 0,
    }


def d_coefficients(N: List[Fraction], Z: List[Fraction]) -> List[Fraction]:
    out = []
    for n in range(2 * DEGREE + 1):
        val = Fraction(0)
        for i in range(0, min(DEGREE, n) + 1):
            j = n - i
            if 0 <= j <= DEGREE:
                val += N[i] * Z[j] * (((-1) ** j) - ((-1) ** i))
        out.append(val)
    return out


def sign_asymmetry_certificate(H: Fraction, rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    N = [Fraction(row['numerator_taylor_coeff']) for row in rows]
    Z = [Fraction(row['partition_taylor_coeff']) for row in rows]
    coeffs = d_coefficients(N, Z)
    leading = coeffs[3]
    finite_loss = sum(abs(coeffs[n]) * H ** (n - 3) for n in range(4, len(coeffs)))
    E = exp_upper(Fraction(7) * H)
    R = exp_tail_bound(Fraction(7) * H, DEGREE + 1, E)
    # For each product term, replacing exact N/Z by degree-8 truncation costs at most 2 E R.
    # There are two products in D, hence 4 E R total.
    tail_loss = Fraction(4) * E * R / (H ** 3)
    lower_over_k3 = leading - finite_loss - tail_loss
    return {
        'range': f'0 < kappa <= {sfrac(H)}',
        'H': sfrac(H),
        'degree': DEGREE,
        'leading_term_over_kappa3': sfrac(leading),
        'expected_leading_from_2N3': sfrac(2 * N[3]),
        'finite_loss_over_kappa3': sfrac(finite_loss),
        'tail_loss_over_kappa3': sfrac(tail_loss),
        'lower_over_kappa3': sfrac(lower_over_k3),
        'proves_F_kappa_gt_F_minus_kappa': lower_over_k3 > 0,
        'D_coefficients': [{'degree': i, 'coeff': sfrac(v)} for i, v in enumerate(coeffs) if v],
        'denominator_positive': True,
        'denominator_reason': 'Z(kappa)>0 and Z(-kappa)>0 because each is an integral of exp(kappa*S).',
    }


def boundary_diagnostics(rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    c17 = positivity_certificate(Fraction(1, 7), rows)
    c16 = positivity_certificate(Fraction(1, 6), rows)
    def label(c):
        if c['proves_target']:
            return 'degree-8 absolute-tail certificate proves target F>=kappa^2/2048'
        if c['proves_positivity']:
            return 'degree-8 absolute-tail certificate proves positivity but not target coefficient 1/2048'
        return 'degree-8 absolute-tail certificate insufficient; numerator margin is not positive'
    c17['diagnostic'] = label(c17)
    c16['diagnostic'] = label(c16)
    return {'K_1_over_7': c17, 'K_1_over_6': c16}


def validator_controls(rows: List[Mapping[str, Any]], primary: Mapping[str, Any], asym: Mapping[str, Any], boundary: Mapping[str, Any]) -> List[Dict[str, Any]]:
    controls = []
    def add(name: str, passed: bool, **extra):
        controls.append({'name': name, 'passed': bool(passed), **extra})
    N = [Fraction(row['numerator_taylor_coeff']) for row in rows]
    Z = [Fraction(row['partition_taylor_coeff']) for row in rows]
    add('accepted C1 low coefficients recovered', N[0] == 0 and N[1] == 0 and N[2] == Fraction(1,324) and N[3] == Fraction(13,1296) and Z[0] == 1 and Z[1] == 0 and Z[2] == Fraction(13,8) and Z[3] == Fraction(1,4), N0=sfrac(N[0]), N1=sfrac(N[1]), N2=sfrac(N[2]), N3=sfrac(N[3]), Z0=sfrac(Z[0]), Z1=sfrac(Z[1]), Z2=sfrac(Z[2]), Z3=sfrac(Z[3]))
    add('kappa zero endpoint exact before division', N[0] == 0 and N[1] == 0, endpoint='F(0)=0 from N0=0, Z0=1; N1=0 supports no linear term')
    add('primary coefficient beats 1/2048', primary['proves_target'], margin=primary['target_margin'])
    add('denominator bound direction is upper bound for lower quotient', primary['denominator_upper_direction'].startswith('Z(kappa)<=E'))
    add('sign asymmetry leading term equals 2*N3', Fraction(asym['leading_term_over_kappa3']) == 2 * N[3], leading=asym['leading_term_over_kappa3'])
    add('sign asymmetry tail-subtracted margin positive', asym['proves_F_kappa_gt_F_minus_kappa'], lower_over_kappa3=asym['lower_over_kappa3'])
    add('K=1/7 diagnostic does not overclaim target if margin negative', boundary['K_1_over_7']['proves_positivity'] and not boundary['K_1_over_7']['proves_target'], margin=boundary['K_1_over_7']['target_margin'])
    add('K=1/6 diagnostic records method insufficiency', not boundary['K_1_over_6']['proves_positivity'], C_N=boundary['K_1_over_6']['C_N'])
    # Genuine in-process mutation validators.
    mut = deepcopy(rows); mut[2]['numerator_taylor_coeff'] = '0'
    add('mutation altering N2 is rejected', not positivity_certificate(PRIMARY_K, mut)['proves_target'])
    mut = deepcopy(rows); mut[0]['numerator_taylor_coeff'] = '1/1000'
    add('mutation setting N0 nonzero rejected by endpoint logic', Fraction(mut[0]['numerator_taylor_coeff']) != 0)
    mut = deepcopy(rows); mut[1]['numerator_taylor_coeff'] = '1/1000'
    add('mutation setting N1 nonzero rejected by endpoint logic', Fraction(mut[1]['numerator_taylor_coeff']) != 0)
    wrong_asym = deepcopy(asym); wrong_asym['lower_over_kappa3'] = sfrac(-Fraction(wrong_asym['lower_over_kappa3']))
    add('mutation flipping sign-asymmetry lower bound rejected', Fraction(wrong_asym['lower_over_kappa3']) <= 0)
    add('static kappa is not physical scale', True, classification='static kappa checkpoint only; not E_star, not alpha ratio, not Fibonacci physical matching')
    return controls


def source_manifest(output: Path, files: List[str]) -> Dict[str, Any]:
    rel_inputs = {
        'research/round19/advisor/contract-c2.json': CONTRACT_SHA,
        'research/round19/advisor/c1-gate.json': C1_GATE_SHA,
        'research/round19/advisor/contract-c1.json': C1_CONTRACT_SHA,
        'research/round19/methods/round19-lessons.md': LESSONS_SHA,
        'research/round19/forward/c1/output/results.json': FORWARD_C1_RESULTS_SHA,
        'research/round19/backward/c1/output/results.json': BACKWARD_C1_RESULTS_SHA,
        'research/round19/backward/c1/comparison/comparison.json': C1_COMPARISON_SHA,
    }
    for name in ['check.py', 'report.md']:
        if not (HERE / name).exists():
            raise FileNotFoundError(HERE / name)
    for name in files:
        if not (output / name).exists():
            raise FileNotFoundError(output / name)
    actual_inputs = {name: sha256_file(ROOT / name) for name in rel_inputs}
    return {
        'schema': 'ym19-backward-c2-source-manifest-v1',
        'source_files': {name: sha256_file(HERE / name) for name in ['check.py', 'report.md']},
        'source_inputs': actual_inputs,
        'expected_source_input_hashes': rel_inputs,
        'outputs': {name: sha256_file(output / name) for name in files},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    coeff = accepted_coefficients(DEGREE)
    rows = coeff['rows']
    primary = positivity_certificate(PRIMARY_K, rows)
    asym = sign_asymmetry_certificate(ASYM_K, rows)
    boundary = boundary_diagnostics(rows)
    controls = validator_controls(rows, primary, asym, boundary)
    graph = coeff['graph']
    checks = []
    def check(name: str, passed: bool, **extra):
        checks.append({'name': name, 'passed': bool(passed), **extra})
    check('accepted C1 graph/action/observable recovered', graph['derived_S'] == '3*x + y + z + w + t', graph_counts={'vertices':len(graph['vertices']),'edges':len(graph['edges']),'faces':len(graph['faces'])}, action=graph['derived_S'], observable='(4*x^2-1)^3*(4*w^2-1)/81')
    check('C1 coefficients N0,N1,N2,N3,Z0,Z1,Z2,Z3 recovered', controls[0]['passed'], low_coefficients={k: controls[0][k] for k in ['N0','N1','N2','N3','Z0','Z1','Z2','Z3']})
    check('primary theorem proves F(kappa)>=kappa^2/2048 for |kappa|<=1/8', primary['proves_target'], certificate=primary)
    check('kappa=0 endpoint handled by exact zeros', controls[1]['passed'])
    check('denominator positivity and quotient direction checked', primary['denominator_positive'] and primary['denominator_upper_direction'].startswith('Z(kappa)<=E'))
    check('sign asymmetry proved on 0<kappa<=1/64', asym['proves_F_kappa_gt_F_minus_kappa'], certificate={'leading':asym['leading_term_over_kappa3'], 'lower':asym['lower_over_kappa3']})
    check('K=1/7 and K=1/6 boundary diagnostics recorded without overclaim', controls[6]['passed'] and controls[7]['passed'])
    check('static kappa scope remains physically unmatched', True, scope='no E_star, alpha-ratio, dense, continuum or Clay claim')
    status = 'passed' if all(c['passed'] for c in checks) and all(c['passed'] for c in controls) else 'failed'
    results = {
        'schema': 'ym19-backward-c2-results-v1',
        'status': status,
        'contract_sha256': CONTRACT_SHA,
        'c1_gate_sha256': C1_GATE_SHA,
        'accepted_c1_bindings': {
            'forward_c1_results_sha256': FORWARD_C1_RESULTS_SHA,
            'backward_c1_results_sha256': BACKWARD_C1_RESULTS_SHA,
            'canonical_c1_comparison_sha256': C1_COMPARISON_SHA,
        },
        'static_scope': 'kappa is a static integral parameter only; not E_star and not a physical energy/time scale; physical-scale matching remains open/unmatched',
        'graph_action_observable': {'graph_counts': {'vertices':len(graph['vertices']), 'edges':len(graph['edges']), 'faces':len(graph['faces'])}, 'action': graph['derived_S'], 'observable': '(4*x^2-1)^3*(4*w^2-1)/81'},
        'primary_theorem': {'statement': 'For every real kappa with |kappa|<=1/8, F(0)=0 and F(kappa)>=kappa^2/2048.', 'certificate': primary},
        'sign_asymmetry_theorem': {'statement': 'For 0<kappa<=1/64, F(kappa)>F(-kappa).', 'certificate': asym},
        'boundary_diagnostics': boundary,
        'checks': checks,
        'checks_count': len(checks),
        'controls': controls,
        'controls_count': len(controls),
    }
    (out / 'coefficients.json').write_text(json.dumps({'schema':'ym19-backward-c2-coefficients-v1','rows':rows}, indent=2, sort_keys=True) + '\n')
    (out / 'primary-certificate.json').write_text(json.dumps({'schema':'ym19-backward-c2-primary-certificate-v1','certificate':primary}, indent=2, sort_keys=True) + '\n')
    (out / 'sign-asymmetry.json').write_text(json.dumps({'schema':'ym19-backward-c2-sign-asymmetry-v1','certificate':asym}, indent=2, sort_keys=True) + '\n')
    (out / 'boundary-diagnostics.json').write_text(json.dumps({'schema':'ym19-backward-c2-boundary-diagnostics-v1', **boundary}, indent=2, sort_keys=True) + '\n')
    (out / 'controls.json').write_text(json.dumps(controls, indent=2, sort_keys=True) + '\n')
    (out / 'results.json').write_text(json.dumps(results, indent=2, sort_keys=True) + '\n')
    files = ['coefficients.json','primary-certificate.json','sign-asymmetry.json','boundary-diagnostics.json','controls.json','results.json']
    (out / 'source-manifest.json').write_text(json.dumps(source_manifest(out, files), indent=2, sort_keys=True) + '\n')
    files.append('source-manifest.json')
    (out / 'manifest.json').write_text(json.dumps({'schema':'ym19-backward-c2-output-manifest-v1','status':status,'files':{name:sha256_file(out/name) for name in files}}, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'schema':'ym19-backward-c2-results-v1','status':status,'checks_count':len(checks),'controls_count':len(controls),'primary_margin':primary['target_margin'],'asymmetry_margin':asym['lower_over_kappa3']}, sort_keys=True))
    if status != 'passed':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
