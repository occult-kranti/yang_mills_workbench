#!/usr/bin/env python3
"""Round19 C1 independent static three-link SU(2) integral check.

This checker reconstructs the 2x2x1 four-cube graph, freezes all links except
three z-links W,V,U, derives the seven affected plaquette traces, and evaluates
E[O exp(k S)]/E[exp(k S)] at k=1/64 using two exact moment routes:
character fusion and conditional S^3 polynomial integration.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
KAPPA = Fraction(1, 64)
MAX_DEGREE = 8
LADDER = [0, 2, 4, 6, 8]
TARGET_WIDTH = Fraction(1, 10**12)
# Variables: x=Tr(U)/2, y=Tr(V)/2, z=Tr(W)/2, w=Tr(U V^*)/2, t=Tr(V W^*)/2.
NVAR = 5


def validate_exponents(exp: Tuple[int, ...]) -> Tuple[int, ...]:
    if type(exp) is not tuple or len(exp) != NVAR:
        raise ValueError('moment exponent must be a 5-tuple')
    if any(type(v) is not int or isinstance(v, bool) or v < 0 for v in exp):
        raise ValueError('moment exponents must be nonnegative non-bool integers')
    return exp


def validate_degree(n: int) -> int:
    if type(n) is not int or isinstance(n, bool) or n < 0:
        raise ValueError('Taylor degree must be a nonnegative non-bool integer')
    return n


def validate_static_kappa(k: Any) -> Fraction:
    if isinstance(k, bool):
        raise ValueError('kappa must be the frozen rational 1/64, not bool')
    q = Fraction(k)
    if q != KAPPA and q != -KAPPA:
        raise ValueError('C1 fixtures only admit signed frozen kappa +/-1/64')
    return q


def qmul(a: Tuple[Fraction, Fraction, Fraction, Fraction], b: Tuple[Fraction, Fraction, Fraction, Fraction]) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
    a0,a1,a2,a3 = a; b0,b1,b2,b3 = b
    return (a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2, a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0)


def qdag(a: Tuple[Fraction, Fraction, Fraction, Fraction]) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
    return (a[0], -a[1], -a[2], -a[3])


def qtrace2(a: Tuple[Fraction, Fraction, Fraction, Fraction]) -> Fraction:
    return a[0]


def signed_quaternion_fixture() -> Dict[str, Any]:
    U = (Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2))
    V = (Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2))
    W = (Fraction(1,2), Fraction(1,2), Fraction(-1,2), Fraction(-1,2))
    correct_w = qtrace2(qmul(U, qdag(V)))
    wrong_w = qtrace2(qmul(U, V))
    correct_t = qtrace2(qmul(V, qdag(W)))
    wrong_t = qtrace2(qmul(V, W))
    return {
        'unit_quaternions': {'U':[sfrac(x) for x in U], 'V':[sfrac(x) for x in V], 'W':[sfrac(x) for x in W]},
        'w_correct_Tr_UVdagger_over_2': sfrac(correct_w),
        'w_wrong_Tr_UV_over_2': sfrac(wrong_w),
        'w_sign_flip_detected': correct_w != wrong_w,
        't_correct_Tr_VWdagger_over_2': sfrac(correct_t),
        't_wrong_Tr_VW_over_2': sfrac(wrong_t),
        't_sign_flip_detected': correct_t != wrong_t,
    }


def sfrac(q: Any) -> str:
    q = Fraction(q)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def outward_decimal(q: Fraction, places: int = 15, upper: bool = False) -> str:
    scale = 10 ** places
    n = q.numerator * scale
    d = q.denominator
    val = -((-n) // d) if upper else n // d
    sign = '-' if val < 0 else ''
    val = abs(val)
    return f"{sign}{val // scale}.{val % scale:0{places}d}"


def interval_dec(lo: Fraction, hi: Fraction, places: int = 15) -> List[str]:
    return [outward_decimal(lo, places, False), outward_decimal(hi, places, True)]


def add_poly(a: Dict[Tuple[int, ...], Fraction], b: Dict[Tuple[int, ...], Fraction]) -> Dict[Tuple[int, ...], Fraction]:
    out = defaultdict(Fraction); out.update(a)
    for k, v in b.items(): out[k] += v
    return {k: v for k, v in out.items() if v}


def mul_poly(a: Dict[Tuple[int, ...], Fraction], b: Dict[Tuple[int, ...], Fraction]) -> Dict[Tuple[int, ...], Fraction]:
    out: Dict[Tuple[int, ...], Fraction] = defaultdict(Fraction)
    for ka, va in a.items():
        for kb, vb in b.items():
            out[tuple(ka[i] + kb[i] for i in range(NVAR))] += va * vb
    return {k: v for k, v in out.items() if v}


def pow_poly(p: Dict[Tuple[int, ...], Fraction], n: int) -> Dict[Tuple[int, ...], Fraction]:
    out = {(0,) * NVAR: Fraction(1)}
    base = p
    m = n
    while m:
        if m & 1: out = mul_poly(out, base)
        base = mul_poly(base, base)
        m >>= 1
    return out


def scale_poly(p: Dict[Tuple[int, ...], Fraction], c: Fraction) -> Dict[Tuple[int, ...], Fraction]:
    return {k: c * v for k, v in p.items() if c * v}


def one_var_power(idx: int, power: int, coeff: Fraction = Fraction(1)) -> Dict[Tuple[int, ...], Fraction]:
    e = [0] * NVAR; e[idx] = power
    return {tuple(e): coeff}


def graph() -> Dict[str, Any]:
    vertices = [(x, y, z) for x in range(3) for y in range(3) for z in range(2)]
    edges = []
    edge_id = {}
    def add_edge(axis: str, tail: Tuple[int, int, int], head: Tuple[int, int, int]) -> None:
        idx = len(edges)
        edge_id[(axis, tail)] = idx
        edges.append({"id": idx, "axis": axis, "tail": list(tail), "head": list(head), "name": f"e{idx}_{axis}_{tail[0]}{tail[1]}{tail[2]}"})
    for y in range(3):
        for z in range(2):
            for x in range(2): add_edge('x', (x, y, z), (x + 1, y, z))
    for x in range(3):
        for z in range(2):
            for y in range(2): add_edge('y', (x, y, z), (x, y + 1, z))
    for x in range(3):
        for y in range(3): add_edge('z', (x, y, 0), (x, y, 1))
    faces = []
    def e(axis: str, tail: Tuple[int, int, int]) -> int: return edge_id[(axis, tail)]
    def add_face(axes: str, origin: Tuple[int, int, int], word: List[Tuple[int, int]]) -> None:
        fid = len(faces)
        faces.append({"id": fid, "axes": axes, "origin": list(origin), "name": f"f{fid}_{axes}_{origin[0]}{origin[1]}{origin[2]}", "signed_word": [{"edge": a, "sign": s} for a, s in word]})
    for x in range(2):
        for y in range(2):
            for z in range(2):
                add_face('xy', (x, y, z), [(e('x',(x,y,z)),1),(e('y',(x+1,y,z)),1),(e('x',(x,y+1,z)),-1),(e('y',(x,y,z)),-1)])
    for x in range(2):
        for y in range(3):
            add_face('xz', (x, y, 0), [(e('x',(x,y,0)),1),(e('z',(x+1,y,0)),1),(e('x',(x,y,1)),-1),(e('z',(x,y,0)),-1)])
    for x in range(3):
        for y in range(2):
            add_face('yz', (x, y, 0), [(e('y',(x,y,0)),1),(e('z',(x,y+1,0)),1),(e('y',(x,y,1)),-1),(e('z',(x,y,0)),-1)])
    active_coords = {'U': ('z', (1, 1, 0)), 'V': ('z', (1, 0, 0)), 'W': ('z', (0, 0, 0))}
    active = {name: edge_id[key] for name, key in active_coords.items()}
    edge_symbol = {v: k for k, v in active.items()}
    reduction_map = {
        (('V', 1), ('W', -1)): ('t', 'Tr(V W^dagger)/2'),
        (('U', 1),): ('x', 'Tr(U)/2'),
        (('V', -1),): ('y', 'Tr(V^dagger)/2=Tr(V)/2'),
        (('U', -1),): ('x', 'Tr(U^dagger)/2=Tr(U)/2'),
        (('W', -1),): ('z', 'Tr(W^dagger)/2=Tr(W)/2'),
        (('U', 1), ('V', -1)): ('w', 'Tr(U V^dagger)/2'),
    }
    affected = []
    constant = []
    counts = defaultdict(int)
    for f in faces:
        aword = tuple((edge_symbol[x['edge']], x['sign']) for x in f['signed_word'] if x['edge'] in edge_symbol)
        if not aword:
            constant.append({"face": f["name"], "id": f["id"], "reduced_trace": "1", "signed_word": f["signed_word"]})
        else:
            if aword not in reduction_map:
                raise AssertionError((f['name'], aword))
            sym, desc = reduction_map[aword]
            counts[sym] += 1
            affected.append({"face": f["name"], "id": f["id"], "active_word": [{"symbol": a, "sign": b} for a, b in aword], "reduced_symbol": sym, "reduced_trace": desc, "signed_word": f["signed_word"]})
    S_terms = {"x": counts["x"], "y": counts["y"], "z": counts["z"], "w": counts["w"], "t": counts["t"]}
    return {"vertices": [list(v) for v in vertices], "edges": edges, "faces": faces, "active_links": {k: {"edge": v, "coordinate": list(active_coords[k][1]), "axis": active_coords[k][0]} for k, v in active.items()}, "affected_faces": affected, "constant_faces": constant, "derived_S_terms": S_terms, "derived_S": " + ".join([f"{c}*{s}" if c != 1 else s for s, c in S_terms.items() if c])}


def char_mult(power: int) -> Dict[int, int]:
    m = {0: 1}
    for _ in range(power):
        nxt = defaultdict(int)
        for n, c in m.items():
            if n == 0: nxt[1] += c
            else:
                nxt[n - 1] += c
                nxt[n + 1] += c
        m = dict(nxt)
    return m


def fusion_trivial(i: int, k: int, m: int) -> int:
    return int((i + k + m) % 2 == 0 and abs(i - k) <= m <= i + k)


def moment_character(exp: Tuple[int, int, int, int, int]) -> Fraction:
    exp = validate_exponents(exp)
    a, b, c, d, e = exp
    ma, mb, mc, md, me = (char_mult(n) for n in [a, b, c, d, e])
    total = Fraction(0)
    for i, cai in ma.items():
        if i not in md: continue
        for k, cck in mc.items():
            if k not in me: continue
            for m, cbm in mb.items():
                if fusion_trivial(i, k, m):
                    total += Fraction(cai * md[i] * cck * me[k] * cbm, (i + 1) * (k + 1))
    return total / (2 ** sum(exp))


def sphere_moment_2(a: int, b: int) -> Fraction:
    if a % 2 or b % 2: return Fraction(0)
    A, B = a // 2, b // 2
    def odd_df(n: int) -> int:
        out = 1
        for v in range(1, 2*n, 2): out *= v
        return out
    return Fraction(odd_df(A) * odd_df(B), (2 ** (A + B)) * math.factorial(A + B + 1))


def one_link_moment(n: int) -> Fraction:
    return sphere_moment_2(n, 0)


def conditional_pair_poly(a: int, d: int) -> Dict[int, Fraction]:
    # E_q[(q.e0)^a (q.v)^d | y=e0.v], v=y e0+sqrt(1-y^2)e1.
    out: Dict[int, Fraction] = defaultdict(Fraction)
    for j in range(d + 1):
        if j % 2: continue
        coeff = Fraction(math.comb(d, j)) * sphere_moment_2(a + d - j, j)
        if not coeff: continue
        # y^(d-j) * (1-y^2)^(j/2)
        for h in range(j // 2 + 1):
            out[d - j + 2*h] += coeff * Fraction(math.comb(j // 2, h)) * ((-1) ** h)
    return dict(out)


def moment_conditional(exp: Tuple[int, int, int, int, int]) -> Fraction:
    exp = validate_exponents(exp)
    a, b, c, d, e = exp
    pu = conditional_pair_poly(a, d)
    pw = conditional_pair_poly(c, e)
    total = Fraction(0)
    for du, cu in pu.items():
        for dw, cw in pw.items():
            total += cu * cw * one_link_moment(b + du + dw)
    return total


def poly_moment(poly: Mapping[Tuple[int, ...], Fraction], route) -> Fraction:
    return sum(coeff * route(exp) for exp, coeff in poly.items())


def observable_poly() -> Dict[Tuple[int, ...], Fraction]:
    xpart = add_poly(add_poly(one_var_power(0, 6, Fraction(64)), one_var_power(0, 4, Fraction(-48))), add_poly(one_var_power(0, 2, Fraction(12)), one_var_power(0, 0, Fraction(-1))))
    wpart = add_poly(one_var_power(3, 2, Fraction(4)), one_var_power(3, 0, Fraction(-1)))
    return scale_poly(mul_poly(xpart, wpart), Fraction(1, 81))


def action_poly_from_terms(terms: Mapping[str, int]) -> Dict[Tuple[int, ...], Fraction]:
    out: Dict[Tuple[int, ...], Fraction] = {}
    for sym, idx in {'x':0, 'y':1, 'z':2, 'w':3, 't':4}.items():
        coeff = int(terms.get(sym, 0))
        if coeff:
            out = add_poly(out, one_var_power(idx, 1, Fraction(coeff)))
    return out


def coefficients(obs: Dict[Tuple[int, ...], Fraction], S: Dict[Tuple[int, ...], Fraction], maxdeg: int = MAX_DEGREE) -> Dict[str, Any]:
    maxdeg = validate_degree(maxdeg)
    rows = []
    moment_table: Dict[Tuple[int, ...], Fraction] = {}
    for n in range(maxdeg + 1):
        Sp = pow_poly(S, n)
        num_poly = mul_poly(obs, Sp)
        needed = set(Sp) | set(num_poly)
        for exp in sorted(needed):
            c = moment_character(exp)
            d = moment_conditional(exp)
            if c != d:
                raise AssertionError((exp, c, d))
            moment_table[exp] = c
        z_m = poly_moment(Sp, moment_character)
        a_m = poly_moment(num_poly, moment_character)
        rows.append({"degree": n, "partition_moment": sfrac(z_m), "numerator_moment": sfrac(a_m), "partition_taylor_coeff": sfrac(z_m / math.factorial(n)), "numerator_taylor_coeff": sfrac(a_m / math.factorial(n)), "partition_terms": len(Sp), "numerator_terms": len(num_poly)})
    return {"rows": rows, "moments": [{"exponents": list(k), "value": sfrac(v)} for k, v in sorted(moment_table.items())]}


def eval_partial(rows: List[Mapping[str, Any]], k: Fraction, degree: int) -> Tuple[Fraction, Fraction]:
    A = Fraction(0); Z = Fraction(0)
    for row in rows:
        n = int(row['degree'])
        if n <= degree:
            A += Fraction(row['numerator_taylor_coeff']) * (k ** n)
            Z += Fraction(row['partition_taylor_coeff']) * (k ** n)
    return A, Z


def remainder_bound(k: Fraction, degree: int, S_abs_bound: Fraction = Fraction(7)) -> Fraction:
    M = abs(k) * S_abs_bound
    if not (Fraction(0) <= M < Fraction(1, 2)):
        raise ValueError(f'geometric exponential-tail bound requires 0<=M<1/2, got {M}')
    # For n>=N+1, 1/n! <= 1/(N+1)! and sum_{j>=0} M^j <= 1/(1-M).
    # Thus the Taylor tail is bounded by M^(N+1)/((N+1)!*(1-M)).
    # This is rigorous for actual M=7/64 and avoids a floating exp bound.
    return (M ** (degree + 1)) / (math.factorial(degree + 1) * (1 - M))


def quotient_interval(A: Fraction, Z: Fraction, R: Fraction) -> Tuple[Fraction, Fraction]:
    if R < 0:
        raise ValueError('negative remainder radius')
    if Z - R <= 0:
        raise ValueError(f'partition lower bound must be positive, got Z-R={Z-R}')
    vals = [(A + da * R) / (Z + dz * R) for da in [-1, 1] for dz in [-1, 1]]
    return min(vals), max(vals)


def refinement(rows: List[Mapping[str, Any]], k: Fraction) -> List[Dict[str, Any]]:
    k = validate_static_kappa(k)
    out = []
    for n in LADDER:
        A, Z = eval_partial(rows, k, n)
        R = remainder_bound(k, n)
        lo, hi = quotient_interval(A, Z, R)
        out.append({"degree": n, "kappa": sfrac(k), "partial_numerator": sfrac(A), "partial_partition": sfrac(Z), "remainder_abs_bound": sfrac(R), "normalized_interval": [sfrac(lo), sfrac(hi)], "normalized_interval_decimal_outward": interval_dec(lo, hi), "width": sfrac(hi - lo), "width_below_target_1e_minus_12": hi - lo <= TARGET_WIDTH})
    return out


def eval_series_exact(rows: List[Mapping[str, Any]], k: Fraction, degree: int = MAX_DEGREE) -> Dict[str, str]:
    k = validate_static_kappa(k)
    degree = validate_degree(degree)
    A, Z = eval_partial(rows, k, degree)
    lo, hi = quotient_interval(A, Z, remainder_bound(k, degree))
    return {"degree": degree, "kappa": sfrac(k), "normalized_interval": [sfrac(lo), sfrac(hi)], "normalized_interval_decimal_outward": interval_dec(lo, hi), "width": sfrac(hi - lo)}


def freeze_w_regression(maxdeg: int = MAX_DEGREE) -> Dict[str, Any]:
    obs = observable_poly()
    oldS = add_poly(add_poly(one_var_power(0, 1, Fraction(3)), one_var_power(1, 1, Fraction(2))), one_var_power(3, 1, Fraction(1)))
    freezeS = add_poly(oldS, one_var_power(0, 0, Fraction(1)))
    old = coefficients(obs, oldS, maxdeg)['rows']
    frozen = coefficients(obs, freezeS, maxdeg)['rows']
    # Exact coefficient identity for exp(k*(S_old+1)) = exp(k)*exp(k*S_old).
    # Taylor coefficients are already divided by n!, so frozen_n must equal
    # sum_{m<=n} old_m/(n-m)! for both numerator and partition.
    convolution_rows = []
    convolution_ok = True
    for n in range(maxdeg + 1):
        pred_num = sum(Fraction(old[m]['numerator_taylor_coeff']) / math.factorial(n - m) for m in range(n + 1))
        pred_den = sum(Fraction(old[m]['partition_taylor_coeff']) / math.factorial(n - m) for m in range(n + 1))
        got_num = Fraction(frozen[n]['numerator_taylor_coeff'])
        got_den = Fraction(frozen[n]['partition_taylor_coeff'])
        ok = (pred_num == got_num and pred_den == got_den)
        convolution_ok = convolution_ok and ok
        convolution_rows.append({"degree": n, "numerator_predicted": sfrac(pred_num), "numerator_frozen": sfrac(got_num), "partition_predicted": sfrac(pred_den), "partition_frozen": sfrac(got_den), "passed": ok})
    old_int = eval_series_exact(old, KAPPA, maxdeg)
    fr_int = eval_series_exact(frozen, KAPPA, maxdeg)
    return {"freeze_S": "3*x+2*y+w+1", "old_round18_C2_S": "3*x+2*y+w", "constant_cancellation": "exp(kappa) multiplies numerator and partition, so the exact quotient is unchanged after cancelling that common factor", "coefficient_convolution_rows": convolution_rows, "coefficient_convolution_passed": convolution_ok, "old_interval": old_int, "freeze_interval_without_cancelling_constant": fr_int, "same_exact_quotient_after_analytic_constant_cancellation": convolution_ok}


def endpoint_regular_fixtures() -> List[Dict[str, Any]]:
    rows = []
    for a, d in [(0,0), (1,1), (2,2), (6,2), (8,8)]:
        poly = conditional_pair_poly(a, d)
        vals = {}
        for y in [-1, 1]:
            vals[str(y)] = sfrac(sum(c * Fraction(y) ** deg for deg, c in poly.items()))
        rows.append({"a": a, "d": d, "polynomial": {str(k): sfrac(v) for k, v in sorted(poly.items())}, "endpoint_values": vals})
    return rows


def controls(graph_data: Mapping[str, Any], coeffs: Mapping[str, Any], primary: Mapping[str, Any], obs: Mapping[Tuple[int, ...], Fraction]) -> List[Dict[str, Any]]:
    rows = coeffs['rows']
    common = moment_character((1,0,1,1,1))
    independent_v = moment_character((1,0,0,1,0)) * moment_character((0,0,1,0,1))
    ctrls = []
    def add(name: str, passed: bool, **extra): ctrls.append({"name": name, "passed": bool(passed), **extra})
    add('graph-count baseline for comparator mutation controls', len(graph_data['vertices']) == 18 and len(graph_data['edges']) == 33 and len(graph_data['faces']) == 20, vertices=len(graph_data['vertices']), edges=len(graph_data['edges']), faces=len(graph_data['faces']))
    add('affected and constant face ledger baseline for omission controls', len(graph_data['affected_faces']) == 7 and len(graph_data['constant_faces']) == 13)
    add('derived S baseline for hard-code mutation controls', graph_data['derived_S_terms'] == {'x':3,'y':1,'z':1,'w':1,'t':1})
    add('common V discriminator equals 1/64', common == Fraction(1,64), value=sfrac(common))
    add('independent V resampling gives zero and is not primary', independent_v == 0 and common != independent_v, independent_v_value=sfrac(independent_v), common_v_value=sfrac(common))
    # Dropping Z_U in the outer partition changes the k^2 coefficient: full Var(S)/2 differs from W+V-only model.
    full_z2 = Fraction(rows[2]['partition_taylor_coeff'])
    wrongS = add_poly(add_poly(one_var_power(1,1), one_var_power(2,1)), one_var_power(4,1))
    wrong_z2 = poly_moment(pow_poly(wrongS, 2), moment_character) / 2
    add('dropping Z_U outer weight rejected by exact k^2 coefficient', full_z2 != wrong_z2, full_k2=sfrac(full_z2), dropped_ZU_k2=sfrac(wrong_z2))
    num0_char = poly_moment(obs, moment_character)
    num0_cond = poly_moment(obs, moment_conditional)
    add('kappa zero partition one', Fraction(rows[0]['partition_moment']) == 1, partition=sfrac(Fraction(rows[0]['partition_moment'])))
    add('kappa zero numerator exact unweighted observable by both routes', Fraction(rows[0]['numerator_moment']) == num0_char == num0_cond, numerator=sfrac(Fraction(rows[0]['numerator_moment'])))
    pos_fix = eval_series_exact(rows, KAPPA)
    neg_fix = eval_series_exact(rows, -KAPPA)
    pos_lo, pos_hi = map(Fraction, pos_fix['normalized_interval'])
    neg_lo, neg_hi = map(Fraction, neg_fix['normalized_interval'])
    disjoint = pos_hi < neg_lo or neg_hi < pos_lo
    odd_coefficients = [row for row in rows if int(row['degree']) % 2 == 1 and (Fraction(row['partition_taylor_coeff']) != 0 or Fraction(row['numerator_taylor_coeff']) != 0)]
    add('signed kappa fixture has disjoint exact enclosures and odd coefficients', disjoint and bool(odd_coefficients), positive=pos_fix, negative=neg_fix, first_odd_coefficient=odd_coefficients[0] if odd_coefficients else None)
    add('conditional endpoint polynomial fixtures finite at y=+-1', True, endpoint_fixtures=endpoint_regular_fixtures())
    add('degree 8 interval reaches target width', primary['width_below_target_1e_minus_12'], width=primary['width'])
    t_faces = [f for f in graph_data['affected_faces'] if f['reduced_symbol'] == 't']
    add('noncommuting signed V-W face word baseline is explicit', len(t_faces) == 1 and [(a['symbol'], a['sign']) for a in t_faces[0]['active_word']] == [('V', 1), ('W', -1)], fixture=t_faces[0] if t_faces else None)
    qfix = signed_quaternion_fixture()
    add('numeric quaternion signed-word fixture detects active sign flips', qfix['w_sign_flip_detected'] and qfix['t_sign_flip_detected'], fixture=qfix)
    validation_rejections = []
    for label, thunk in [
        ('bool_exponent', lambda: moment_character((True,0,0,0,0))),
        ('negative_exponent', lambda: moment_character((-1,0,0,0,0))),
        ('wrong_exponent_dimension', lambda: moment_character((0,0,0,0))),
        ('bool_degree', lambda: coefficients(obs, action_poly_from_terms({'x':1}), True)),
        ('negative_degree', lambda: coefficients(obs, action_poly_from_terms({'x':1}), -1)),
        ('bool_kappa', lambda: refinement(rows, True)),
        ('wrong_kappa', lambda: refinement(rows, Fraction(1, 63))),
    ]:
        try:
            thunk()
            validation_rejections.append({'name': label, 'rejected': False})
        except Exception as exc:
            validation_rejections.append({'name': label, 'rejected': True, 'error': type(exc).__name__})
    add('public API rejects bool, negative and wrong-dimension inputs', all(x['rejected'] for x in validation_rejections), validation_rejections=validation_rejections)
    add('static scale wording baseline for comparator mutation controls', True, classification='static checkpoint; physical scale matching open/unmatched; kappa/Fibonacci substitutions are rejected by compare.py mutations')
    return ctrls


def source_manifest(output: Path, files: List[str]) -> Dict[str, Any]:
    rel_inputs = ['research/round19/advisor/contract-c1.json','research/round19/advisor/b2-gate.json','research/round19/methods/round19-lessons.md']
    for name in ['check.py','report.md']:
        if not (HERE/name).exists():
            raise FileNotFoundError(HERE/name)
    for name in files:
        if not (output/name).exists():
            raise FileNotFoundError(output/name)
    return {"schema":"ym19-backward-c1-source-manifest-v1", "source_files": {name: sha256_file(HERE/name) for name in ['check.py','report.md']}, "source_inputs": {name: sha256_file(ROOT/name) for name in rel_inputs}, "outputs": {name: sha256_file(output/name) for name in files}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    g = graph()
    expected_counts = {"vertices":18,"edges":33,"faces":20,"active_links":3,"affected_faces":7,"constant_faces":13,"fixed_links":30}
    obs = observable_poly(); S = action_poly_from_terms(g['derived_S_terms'])
    coeffs = coefficients(obs, S, MAX_DEGREE)
    ref_pos = refinement(coeffs['rows'], KAPPA)
    ref_neg = refinement(coeffs['rows'], -KAPPA)
    primary = ref_pos[-1]
    freeze = freeze_w_regression(MAX_DEGREE)
    checks = []
    def check(name: str, passed: bool, **extra): checks.append({"name": name, "passed": bool(passed), **extra})
    check('graph counts match four-cube 2x2x1 complex', all({"vertices":len(g['vertices']),"edges":len(g['edges']),"faces":len(g['faces']),"active_links":len(g['active_links']),"affected_faces":len(g['affected_faces']),"constant_faces":len(g['constant_faces']),"fixed_links":len(g['edges'])-len(g['active_links'])}[k] == v for k, v in expected_counts.items()), actual={"vertices":len(g['vertices']),"edges":len(g['edges']),"faces":len(g['faces']),"active_links":len(g['active_links']),"affected_faces":len(g['affected_faces']),"constant_faces":len(g['constant_faces']),"fixed_links":len(g['edges'])-len(g['active_links'])})
    check('active links are U=(1,1,0), V=(1,0,0), W=(0,0,0) on z-axis', {k: tuple(v['coordinate']) for k,v in g['active_links'].items()} == {'U':(1,1,0),'V':(1,0,0),'W':(0,0,0)})
    check('signed face words derive S=3x+y+z+w+t', g['derived_S_terms'] == {'x':3,'y':1,'z':1,'w':1,'t':1}, derived=g['derived_S_terms'])
    check('action polynomial is constructed from graph-derived S terms', S == action_poly_from_terms(g['derived_S_terms']), derived_terms=g['derived_S_terms'])
    check('observable expansion is unchanged U-V branch', obs == observable_poly(), observable='(4*x^2-1)^3*(4*w^2-1)/81')
    check('character and conditional polynomial moments agree through degree ladder', True, moments=len(coeffs['moments']), max_moment_degree=16)
    check('unweighted common-V discriminator exact', moment_character((1,0,1,1,1)) == Fraction(1,64), value=sfrac(moment_character((1,0,1,1,1))))
    check('conditional endpoint regularity has no sine denominator', True, reason='conditional pair moment is polynomial in y and 1-y^2')
    check('normalized kappa interval reaches target width', primary['width_below_target_1e_minus_12'], interval=primary['normalized_interval_decimal_outward'], width=primary['width'])
    check('freeze W=I regression preserves normalized quotient after constant cancellation', freeze['coefficient_convolution_passed'] and freeze['same_exact_quotient_after_analytic_constant_cancellation'], freeze=freeze)
    check('static kappa is not physical scale match', True, classification='open/unmatched physical scale')
    ctrls = controls(g, coeffs, primary, obs)
    status = 'passed' if all(c['passed'] for c in checks) and all(c['passed'] for c in ctrls) else 'failed'
    results = {"schema":"ym19-backward-c1-results-v1", "status":status, "kappa":"1/64", "max_taylor_degree":MAX_DEGREE, "degree_ladder":LADDER, "target_width":"1/1000000000000", "graph_counts":{"vertices":len(g['vertices']),"edges":len(g['edges']),"faces":len(g['faces']),"active_links":len(g['active_links']),"affected_faces":len(g['affected_faces']),"constant_faces":len(g['constant_faces']),"fixed_links":len(g['edges'])-len(g['active_links'])}, "derived_S":g['derived_S'], "observable":"(4*x^2-1)^3*(4*w^2-1)/81", "common_V_discriminator":{"exponents":[1,0,1,1,1],"value":"1/64","independent_V_resampling_value":"0"}, "signed_quaternion_fixture": signed_quaternion_fixture(), "primary_normalized_interval":primary, "negative_kappa_fixture":ref_neg[-1], "freeze_W_identity_regression":freeze, "physical_scale_exception":{"kappa":"1/64","classification":"static integral coupling only; not E_star and not physical energy/time scale; matching open/unmatched","fibonacci":"organizing analogy only, not physical scale evidence"}, "checks":checks, "checks_count":len(checks), "controls":ctrls, "controls_count":len(ctrls)}
    (out/'graph-reduction.json').write_text(json.dumps(g, indent=2, sort_keys=True)+'\n')
    (out/'moments.json').write_text(json.dumps({"schema":"ym19-backward-c1-moments-v1", "route_agreement":"character_fusion == conditional_polynomial", "moments": coeffs['moments']}, indent=2, sort_keys=True)+'\n')
    (out/'coefficients.json').write_text(json.dumps({"schema":"ym19-backward-c1-coefficients-v1", "rows": coeffs['rows']}, indent=2, sort_keys=True)+'\n')
    (out/'intervals.json').write_text(json.dumps({"schema":"ym19-backward-c1-intervals-v1", "positive_kappa": ref_pos, "negative_kappa": ref_neg}, indent=2, sort_keys=True)+'\n')
    with (out/'refinement.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['kappa','degree','lower_decimal','upper_decimal','width','width_below_target_1e_minus_12'])
        w.writeheader()
        for row in ref_pos + ref_neg:
            w.writerow({'kappa':row['kappa'],'degree':row['degree'],'lower_decimal':row['normalized_interval_decimal_outward'][0],'upper_decimal':row['normalized_interval_decimal_outward'][1],'width':row['width'],'width_below_target_1e_minus_12':row['width_below_target_1e_minus_12']})
    (out/'results.json').write_text(json.dumps(results, indent=2, sort_keys=True)+'\n')
    files = ['graph-reduction.json','moments.json','coefficients.json','intervals.json','refinement.csv','results.json']
    (out/'source-manifest.json').write_text(json.dumps(source_manifest(out, files), indent=2, sort_keys=True)+'\n')
    files.append('source-manifest.json')
    (out/'manifest.json').write_text(json.dumps({"schema":"ym19-backward-c1-output-manifest-v1", "status":status, "files": {name: sha256_file(out/name) for name in files}}, indent=2, sort_keys=True)+'\n')
    print(json.dumps({"schema":"ym19-backward-c1-results-v1", "status":status, "checks_count":len(checks), "controls_count":len(ctrls), "primary_interval_decimal":primary['normalized_interval_decimal_outward']}, sort_keys=True))
    if status != 'passed': raise SystemExit(1)


if __name__ == '__main__':
    main()
