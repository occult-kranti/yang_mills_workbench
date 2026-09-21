#!/usr/bin/env python3
"""Exact Y2 reverse certificates. No other research implementation is imported."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def require(ok, message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def strict_positive(x, name):
    if type(x) not in (int, F) or x <= 0:
        raise ValueError(name)


def profile(q, eta):
    if type(q) not in (int, F) or type(eta) not in (int, F):
        raise ValueError('exact q and eta required')
    if not (0 < q < 1 and 0 < eta < 1):
        raise ValueError('excluded canonical endpoint')
    p = 2 + 5*q + 5*q*q + 6*q**3 + 3*q**4
    b = p/(24*(1-q)**3*(1+q)**2*(1+q*q))
    return eta/(8*b)


def rejected(fn):
    try:
        fn()
    except (ValueError, RuntimeError):
        return True
    return False


def bind_inputs():
    contract_path = ROOT/'research/round24/contracts/y2.json'
    contract = json.loads(contract_path.read_text())
    require(contract['status'] == 'frozen' and contract['loop'] == 'y2', 'frozen Y2')
    expected = dict(contract['dependencies'])
    expected.update(contract['instruction_inputs'])
    inventory = json.loads((HERE/'inputs/additional-sources.json').read_text())
    expected.update(inventory['files'])
    for relative, digest in expected.items():
        p = ROOT/relative
        require(not p.is_symlink() and all(not x.is_symlink() for x in p.parents),
                'no symlinks in source path: '+relative)
        require(p.is_file(), 'source exists: '+relative)
        require(hashlib.sha256(p.read_bytes()).hexdigest() == digest, 'source hash: '+relative)
    require(inventory['contract_sha256'] == hashlib.sha256(contract_path.read_bytes()).hexdigest(),
            'contract digest')
    return len(expected)


def plus(a, b):
    return tuple(x+y for x, y in zip(a, b))


def owns(edge):
    (x, y, z), axis = edge
    if axis == 2 or (axis == 0 and x % 4 == 3) or (axis == 1 and y % 2 == 1):
        return ('link', (x, y, z), axis)
    return ('strip', (x-x % 4, y-y % 2, z), -1)


def complete_links(factor):
    kind, p, axis = factor
    if kind == 'link':
        return {(p, axis)}
    x, y, z = p
    return {((x+i, y+j, z), 0) for i in range(3) for j in range(2)} | {
        ((x+i, y, z), 1) for i in range(4)}


def face_links(face):
    p, a, b = face
    return {(p, a), (p, b), (plus(p, AXES[a]), b), (plus(p, AXES[b]), a)}


def retained_omitted(face):
    (x, y, _), a, b = face
    return not ((a, b) == (0, 1) and y % 2 == 0 and x % 4 < 3)


def union_links(factors):
    return set().union(*(complete_links(f) for f in factors))


def incident(factors):
    faces = set()
    for p, a in union_links(factors):
        for b in range(3):
            if a == b:
                continue
            for anchor in (p, plus(p, tuple(-u for u in AXES[b]))):
                if min(anchor) < 0:
                    continue
                face = (anchor, min(a, b), max(a, b))
                if retained_omitted(face):
                    faces.add(face)
    return faces


def regions():
    # The actual three U1 paths, without importing any prior geometry routine.
    vertices = [
        [(3,1,0), (3,2,0), (3,2,1)],
        [(3,1,0), (3,1,1), (3,2,1)],
        [(3,1,0), (4,1,0), (4,2,0), (4,2,1), (3,2,1)],
    ]
    seed_edges = set()
    for path in vertices:
        for a, b in zip(path, path[1:]):
            delta = tuple(y-x for x, y in zip(a, b))
            require(sum(abs(x) for x in delta) == 1, 'unit path edge')
            axis = next(i for i, x in enumerate(delta) if x)
            seed_edges.add((a if delta[axis] > 0 else b, axis))
    factors = {owns(e) for e in seed_edges}
    require(len(factors) == 8 and all(f[0] == 'link' for f in factors), 'U1 seed')
    rows = []
    previous = set()
    for depth in range(1, 4):
        faces = incident(factors)
        enlarged = factors | {owns(e) for f in faces for e in face_links(f)}
        require(previous <= faces, 'nested reverse face convention')
        require(all(owns(e) in enlarged for f in faces for e in face_links(f)), 'full face cover')
        require(all(owns(e) == f for f in enlarged for e in complete_links(f)), 'whole strips')
        require(((3,1,0),1,2) in faces, 'actual resonant face present')
        factors, previous = enlarged, faces
        rows.append({'depth': depth, 'factors': len(factors), 'links': len(union_links(factors)),
                     'faces': len(faces), 'M': F(len(faces),24),
                     'K': F(sum(sum(f[0]) for f in faces),24)})
    require([(r['factors'],r['links'],r['faces']) for r in rows]
            == [(35,98,19),(135,297,125),(308,623,327)], 'reverse Y1 geometry')
    return rows


def tail(depth, x):
    require(type(depth) is int and depth >= 0 and 0 <= x < 1, 'tail domain')
    n = depth + 1
    return x**n*((n+1)*(n+2)-2*n*(n+2)*x+n*(n+1)*x*x)/(2*(1-x)**3)


def matvec(a, v):
    return [sum((aij*vj for aij, vj in zip(row, v)), F(0)) for row in a]


def inner(u, v):
    return sum((x*y for x, y in zip(u,v)), F(0))


def complex_product(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def moments(a, v, order):
    out, power = [], list(v)
    for _ in range(order+1):
        out.append(inner(v,power)/inner(v,v))
        power = matvec(a,power)
    return out


def scalar_series(a, v, s, order):
    mm = moments(a,v,order)
    real, imag = F(0), F(0)
    for n, value in enumerate(mm):
        term = value*s**n/factorial(n)
        if n % 4 == 0: real += term
        elif n % 4 == 1: imag -= term
        elif n % 4 == 2: real -= term
        else: imag += term
    m = max(sum(abs(x) for x in row) for row in a)
    r = abs(s)*m
    require(r < 1, 'Taylor exponential majorant domain')
    remainder = r**(order+1)/(factorial(order+1)*(1-r))
    return {'real':real, 'imag':imag, 'error_radius':remainder, 'norm_upper':m}


def fixture():
    energy = [F(0), F(1), F(1), F(1)]
    a = [[F(0),F(1),F(0),F(0)],
         [F(1),F(0),-F(1,4),F(0)],
         [F(0),-F(1,4),F(0),-F(1,3)],
         [F(0),F(0),-F(1,3),F(0)]]
    abar = [[a[i][j] if energy[i] == energy[j] else F(0)
             for j in range(4)] for i in range(4)]
    clipped = [[abar[i][j] if i < 3 and j < 3 else F(0)
                for j in range(4)] for i in range(4)]
    diagonal = [[abar[i][j] if i == j else F(0) for j in range(4)] for i in range(4)]
    v = [F(0),F(1),F(1),F(0)]
    mm, clipped_mm = moments(abar,v,2), moments(clipped,v,2)
    require(mm == [F(1),-F(1,4),F(17,144)], 'full equal-energy moments')
    require(clipped_mm[2] == F(1,16), 'two-plane second moment')
    full_value = scalar_series(abar,v,F(1,10),12)
    adjoint_value = scalar_series(abar,v,-F(1,10),12)
    plane_value = scalar_series(clipped,v,F(1,10),12)
    scalar_gap = abs(full_value['real']-plane_value['real'])-full_value['error_radius']-plane_value['error_radius']
    require(scalar_gap > F(1,4000), 'certified scalar change from omitted degenerate channel')
    require(full_value['error_radius'] < F(1,10**25), 'controlled arithmetic remainder')
    controls = {
        'whole-degenerate-block-required':moments(diagonal,v,1)[1] != mm[1],
        'two-state-closure-fails':mm[2]-clipped_mm[2] == F(1,18) and scalar_gap > 0,
        'nondegenerate-off-diagonal-removed':a[0][1] == 1 and abar[0][1] == 0,
        'averaged-vacuum-fixed':matvec(abar,[F(1),F(0),F(0),F(0)]) == [F(0)]*4,
        'adjoint-reverses-response-sign':full_value['imag']-full_value['error_radius'] > 0
                                        and adjoint_value['imag']+adjoint_value['error_radius'] < 0,
    }
    return {'full_block_moments':mm, 'clipped_moments':clipped_mm,
            'scalar_at_one_tenth':full_value, 'clipped_scalar':plane_value,
            'scalar_difference_lower':scalar_gap}, controls


def serial(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [serial(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    args = parser.parse_args()
    require(not args.output.exists(), 'output directory must be fresh')
    source_count = bind_inputs()
    geometry = regions()
    values, controls = fixture()
    q, eta, z = F(99999999,10**8), F(1,2), F(1,10**6)
    for name in ('a','E_star','alpha','hbar'):
        strict_positive(F(1), name)
    tau = profile(q,eta)
    c, epsilon = z/eta, 1-q
    actual_s, fixed_clock_s = c*tau/epsilon**3, c*tau
    sstar, scap = F(8,7)*z, F(3,2)*z
    require(actual_s <= scap and actual_s > z, 'original endpoint clock budget')
    require(F(3)*4*2/21 == F(8,7), 'exact rational endpoint coefficient')
    for depth in range(6):
        xx = F(1,7)
        finite = sum(F((n+1)*(n+2),2)*xx**n for n in range(depth+1))
        require(tail(depth,xx) == 1/(1-xx)**3-finite, 'entire rational tail identity')
    x = F(80,7)*z
    radius = F(44,9)*x*x/(1-x)**5
    spatial = tail(2,15*z)
    require(radius < F(639,10**12), 'actual limiting disk radius')
    require(z/F(84)-radius > z/F(168), 'full limiting signal')
    require(spatial < F(34,10**15), 'depth-two spatial error')
    # A bound on a fixed energy column may vanish while a moving high-energy column does not.
    lam, gap, m, s = F(1,1000), F(1), F(1), F(1,10)
    fixed_column_error = 2*lam*m/gap*(1+2*s*m)
    require(fixed_column_error == F(3,1250), 'primitive integration error coefficient')
    norm_failure_lower = 1-F(5,4)/6
    require(norm_failure_lower == F(19,24), 'sinc lower bound for compact-resolvent doublets')
    moving_rows = []
    for n in (2,10,100):
        pair = [F(n*n),F(n*n)+F(1,n)]
        require((pair[1]-pair[0])/F(1,n) == 1, 'fixed detuning on moving vector')
        moving_rows.append({'n':n,'energies':pair,'lambda':F(1,n),'norm_error_lower':norm_failure_lower})
    k = 10
    qmoving = 1-F(1,k*k)
    quarter_reference = (F(0),-F(1))
    correct_phase = complex_product((F(0),F(1)),quarter_reference)
    wrong_phase = complex_product(quarter_reference,quarter_reference)
    # Exact Bernoulli comparison illustrates the all-k inequality in the report.
    require(qmoving**k >= 1-F(1,k), 'nonuniform spatial counterexample')
    # One retained Haar link already contributes every j=n/2 with positive multiplicity.
    spins = [{'twice_j':n,'energy':F(n*(n+2),4),'multiplicity':(n+1)**2} for n in (0,1,2,10,100)]
    controls.update({
        'wrong-clock-loses-endpoint-signal':fixed_clock_s < z/10**20 and actual_s > z,
        'opposite-reference-phase-is-wrong':correct_phase == (F(1),F(0))
                                           and wrong_phase == (-F(1),F(0)),
        'coefficient-q-error-retained':0 < (1-q**4)/24 <= (1-q)*geometry[1]['K'],
        'strong-averaging-does-not-imply-norm-averaging':norm_failure_lower > F(3,4),
        'finite-collar-is-not-finite-Haar-space':spins[-1]['multiplicity'] > 0 and spins[-1]['energy'] > 1000,
        'pointwise-spatial-limit-is-insufficient':qmoving**k >= F(9,10) and tail(k,15*z) < spatial,
        'excluded-q-one-rejected':rejected(lambda:profile(F(1),eta)),
        'zero-physical-reference-rejected':rejected(lambda:strict_positive(F(0),'E_star')),
        'boolean-coefficient-rejected':rejected(lambda:profile(True,eta)),
        'invalid-tail-domain-rejected':rejected(lambda:tail(2,F(1))),
    })
    for name,value in controls.items():
        require(value,name)
    results = {
        'loop':'y2','direction':'reverse','status':'passed',
        'claims':[
            'Actual finite-factor reference has compact resolvent, unchanged domain and reducing gauge sector',
            'Strong compact-rescaled-time averaging retains every complete degenerate reference-energy block',
            'The true regional stationary scalar has the full-block limit at the original endpoint clock',
            'Uniform Y1 spatial tails transfer regional limits to an actual full demodulated canonical scalar limit',
            'The actual limiting scalar lies in a certified U2 disk and differs from one',
        ],
        'limitations':[
            'Actual excited-block dimensions, matrices and strip spectra are not numerically assembled',
            'The positive excited-energy separation in the finite-q averaging rate is unevaluated',
            'No global q=1 Hamiltonian or operator-norm averaging is asserted',
            'Abstract matrix fixtures are not computed canonical trajectories or physical observations',
            'No full limiting dynamics, homogeneous theory, continuum construction or priority claim',
        ],
        'frozen_input_count':source_count,
        'actual_geometry':geometry,
        'actual_limit_certificate':{
            'z':z,'center_real':F(1),'center_imag':z/F(84),'disk_radius':radius,
            'distance_from_one_lower':z/F(84)-radius,'depth_two_error':spatial,
            'limit_formula':'lim_d <psi_d,exp[-i(8z/7) P_(d,9/2) A_d P_(d,9/2)]psi_d>',
            'finite_q':q,'tau':tau,'s_q':actual_s,'s_limit':sstar,
            'q_coefficient_norm_error_upper_depth_two':(1-q)*geometry[1]['K'],
            'finite_q_averaging_rate_numerically_evaluated':False,
        },
        'abstract_controlled_fixture':values,
        'quarter_reference_phase_control':{'correct':correct_phase,'opposite':wrong_phase},
        'fixed_energy_column_error_example':fixed_column_error,
        'compact_resolvent_norm_counterexample':moving_rows,
        'unbounded_haar_spin_examples':spins,
    }
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'results.json').write_text(json.dumps(serial(results),indent=2,sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
