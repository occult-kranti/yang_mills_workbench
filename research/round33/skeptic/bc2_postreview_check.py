#!/usr/bin/env python3
"""BC2 post-comparison skeptic checks (route-B uniform model, single forward producer).

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated ancestry (same model family as the advisor,
the lenses and the producer; the frozen BC2 texts carry the skeptic's pre-freeze edits); not human peer review or formal
verification.

Adds to the frozen pre-comparison package (bc2_check.py; values final by 04:58:27Z, committed at 5ec599f 05:00:47Z,
before the forward commit ee45eed 05:04:31Z):
  * integrity: the contract hash; the unchanged pre-comparison package and a byte replay of bc2_check.py; the forward
    freeze closure file by file (46 files); the forward inventory on the real snapshots (42 files, equal to the
    contract-derived list and to the inventory recorded before production, byte-identical to the repository); replays of
    the producer reproducing output/ byte for byte (normal, or -O when this program runs under -O); the frozen artifacts
    pinned; no interpreter cache under research/round32/forward/ax2/ or in the producer closure after every run (R7);
  * every producer value against an independent recomputation (never from a producer value): K_B, C_B, c_site,B, the
    union and nested whole-sequence constants, t_0, t_W, c_1, c_2, beta*, S_lambda, the crude tier, the admissibility
    values and the route-A extremes, the ledger, the labelled values, the tau/100 ratios, the node (own replay of the
    admitted calculator, D' recomputed, the producer's labelled own radius bracketed from below by an own Machin pi and
    e^3 series), the example and translation rows, the geometry counts (own enumeration of the piece graph of Lambda_3,
    the incidence on R, the source faces, the flip set and the grouping-preserving translations) and the fixture counts;
  * the pre-comparison predictions against the producer (exact rational equality) and the readings R1, R2 and R7;
  * text: the round phrase tool (subprocess) on the report, the template once as one line, every clause mentioning
    uniqueness classified, and the report's labelled numbers against the recomputation;
  * damaged producer packets rejected by this review's validator;
  * source-edit runs on temporary copies outside the checkout: one validator weakening per contract control (52), route-A
    substitutions into the producer's check.py (each must abort), other must-abort edits (constants, inputs, report),
    silent edits (one harmless, the others damaging and caught only by this review's validator), an unmutated copy
    reproducing the frozen output, and a run without -B that must write no interpreter cache.

Standard library only; exact Fractions decide every Boolean; failures are explicit exceptions (never assert), so the output
bytes match under python -O.

Usage: python3 -B research/round33/skeptic/bc2_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import bc2_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R33 = ROOT / 'research/round33'
CONTRACT = R33 / 'contracts/bc2.json'
CONTRACT_SHA = '28abe3775455087384b3c9dbbb2df67b923e31b964d40efa7ea9787ee8b6b98a'
FWD = R33 / 'forward/bc2'
FWD_REL = 'research/round33/forward/bc2'
AX2_DIR = ROOT / 'research/round32/forward/ax2'
PRE_SCRIPT = HERE / 'bc2_check.py'
PRE_RESULTS = HERE / 'bc2-independent/results.json'
PRE_FREEZE = HERE / 'bc2-independent-freeze.json'
PHRASE_TOOL = R33 / 'tools/phrase_scan.py'
PHRASE_TOOL_SHA = '1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2'
FROZEN = {  # frozen producer artifacts (sha256 at review time; commit ee45eed)
    'check.py': 'f118b8475b8c43f8fcbd38a93093317d0de4c7786711e50748f06ab3edac5477',
    'report.md': 'd5ea7d4b27dc88eb904d5a59a16da7219e35a9882d6e3c8d7b4db8c091e7eb96',
    'freeze.json': 'c70fad5bad990ef46d0a00169ef60cf584820728fea39950b3f6cd42b6fd93f9',
    'output/results.json': 'efbea72b1ffa6936aa86d848a88b37e0d340734f96e862a440cc79d28cb44f08',
    'output/source-manifest.json': 'c1fa8dccfd30acc51048d6b2635bbe921af6a0c1b1e645fd380ff6226f738ef9',
}
AX1_GATE = 'research/round32/advisor/ax1-gate.json'
AX2_GATE = 'research/round32/advisor/ax2-gate.json'
BA1_GATE = 'research/round33/advisor/ba1-gate.json'
BB1_GATE = 'research/round33/advisor/bb1-gate.json'
BB2_GATE = 'research/round33/advisor/bb2-gate.json'
TAU = F(1, 10 ** 8)
Q = F(1, 64)
W = 1024
SECONDARY = ['certificate_restated_for_limit', 'reference_unresolved', 'static_not_dynamic']
OBLIGATIONS = ['a route-B boundary-prescription comparison (an all-contained analogue with its own itemization)',
               'route-B dynamics and correlation functions (a route-B BA2)', 'uniqueness of any ground state',
               'anything uniform in the lattice spacing a', 'the continuum problem']


class ReviewFailure(RuntimeError):
    """A post-review check failed."""


class Rejected(Exception):
    """The skeptic's value and report validator refused a producer packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def q_(x):
    return str(F(x))


def preview(x, digits=12):
    return format(float(x), '.%de' % digits)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rat(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('non-exact value in producer results: ' + repr(value))
    if isinstance(value, int):
        return F(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        return F(value)
    raise Rejected('malformed exact value: ' + repr(value))


def dec(s):
    """A decimal string with an optional exponent (1.25e-7, 4.23e0, 2.14) as an exact Fraction."""
    m = re.fullmatch(r'(-?\d+)(?:\.(\d+))?(?:e([+-]?\d+))?', s)
    if m is None:
        raise Rejected('malformed decimal: ' + repr(s))
    frac = m.group(2) or ''
    val = F(int(m.group(1) + frac), 10 ** len(frac))
    return val * F(10) ** int(m.group(3) or 0)


def ulp(s):
    """One unit of the last written digit of a decimal string."""
    m = re.fullmatch(r'-?\d+(?:\.(\d+))?(?:e([+-]?\d+))?', s)
    return F(10) ** (int(m.group(2) or 0) - len(m.group(1) or ''))


def is_truncation(s, x):
    """The written decimal is x cut after its last digit (the producer's previews are truncated)."""
    d = dec(s)
    return d <= F(x) < d + ulp(s)


def within_ulp(s, x):
    return abs(dec(s) - F(x)) < ulp(s)


def check_by_id(res, cid):
    for c in res['checks']:
        if c['id'] == cid:
            return c
    raise Rejected('producer check missing: ' + cid)


# ------------------------------------------------------------ the skeptic's own values (nothing from the producer)
def enumerate_geometry():
    """Own enumerations with the pre-comparison geometry (I1 classes, route-B grouping)."""
    def faces(vol):
        g = pre.route_b_groups(vol)
        return g, {(k, i): own for k, owns in g.items() for i, own in enumerate(owns)}

    # piece graph of Lambda_3: distinct owner sets of retained faces; order = 1 + graph distance from pieces containing u
    g3, f3 = faces(pre.cube(3))
    pieces = sorted({own for own in f3.values()}, key=lambda s: sorted(s))
    by_site = {}
    for i, p in enumerate(pieces):
        for x in p:
            by_site.setdefault(x, []).append(i)
    bfs = {}
    for u in ((0, 0, 0), (0, 0, 1), (1, 1, 1), (2, 0, 0), (-2, 1, 2)):
        order = {i: 1 for i in by_site.get(u, [])}
        frontier = list(order)
        while frontier:
            nxt = []
            for i in frontier:
                for x in pieces[i]:
                    for j in by_site[x]:
                        if j not in order:
                            order[j] = order[i] + 1
                            nxt.append(j)
            frontier = nxt
        slack = min(n - 1 - min(pre.dinf(u, s) for s in pieces[i]) for i, n in order.items()
                    if min(pre.dinf(u, s) for s in pieces[i]) >= 1)
        bfs[str(u)] = {'min_slack': slack, 'singles_reached': sum(1 for i in order if len(pieces[i]) == 1)}
    # selected source faces of c1B (single groups present in one box only, 3 faces each)
    sel_src = {}
    for n in (2, 3, 4):
        ga, gb = pre.route_b_groups(pre.cube(n)), pre.route_b_groups(pre.cube(n + 1))
        sel_src[n] = 3 * sum(1 for k in set(ga) ^ set(gb) if k[0] == 'single')
    # incidence on R at N=2
    g2, f2 = faces(pre.cube(2))
    R = set(pre.R_COVER)
    stars = [k for k in g2 if k[0] == 'star' and any(pre.add(k[1], s) in R for s in pre.S_STAR)]
    singles = [k for k in g2 if k[0] == 'single' and k[1] in R]
    charged = [own for k in stars + singles for own in g2[k]]
    meet = [o for o in charged if o & R]
    inside = [o for o in meet if o <= R]
    inc = (len(stars), len(singles), len(charged), len(meet), len(inside), len(meet) - len(inside),
           sum(1 for o in meet if o > R))
    # first-order faces through the origin: omitted faces of the stars anchored at -s (s in S) whose owner set contains
    # the origin, plus the three selected faces of the origin's single group
    origin = (0, 0, 0)
    per_site_faces = sum(1 for d in pre.S_STAR for k in pre.OMITTED
                         if origin in {pre.add(pre.sub(origin, d), r) for r in k['rel']}) + len(pre.SELECTED)
    # flip set E: links (p,x) with p_y even, (p,y) with p_z even, (p,z) with p_x even (AX1 gate item 7)
    def in_e(p, d):
        return (d == 'x' and p[1] % 2 == 0) or (d == 'y' and p[2] % 2 == 0) or (d == 'z' and p[0] % 2 == 0)
    sizes, total, sel = set(), 0, 0
    for p in product(range(-4, 8), range(-2, 4), range(-2, 2)):
        for a, c in pre.ORIENT:
            sizes.add(sum(1 for t, d in pre.face_links(p, a, c) if in_e(t, d)))
            total += 1
            sel += 1 if pre.is_selected(p, a, c) else 0
    # grouping-preserving fine translations of the period window 8x4x2
    window = list(product(range(8), range(4), range(2)))
    keep = []
    for t in window:
        ok = True
        shift = None
        for p in window:
            q = pre.add(p, t)
            for a, c in pre.ORIENT:
                if pre.is_selected(p, a, c) != pre.is_selected(q, a, c):
                    ok = False
                op = [pre.pi_map(x) for x, _ in pre.face_links(p, a, c)]
                oq = [pre.pi_map(x) for x, _ in pre.face_links(q, a, c)]
                dset = {pre.sub(y, x) for x, y in zip(op, oq)}
                if len(dset) != 1 or (shift is not None and dset != shift):
                    ok = False
                shift = dset if shift is None else shift
        if ok:
            keep.append(t)
    plaquettes = 20 * 10 * 5 * 3
    return {'pieces': len(pieces), 'single_pieces': sum(1 for p in pieces if len(p) == 1), 'bfs': bfs,
            'selected_source_faces': sel_src, 'incidence_R_N2': inc, 'per_site_faces': per_site_faces,
            'flip': {'plaquettes': total, 'selected': sel, 'sizes': sorted(sizes)},
            'translations': {'count': len(keep), 'all_coarse': all(t[0] % 4 == 0 and t[1] % 2 == 0 for t in keep)},
            'partition_plaquettes_Lambda_2': plaquettes}


def reference():
    gates = {rel: json.loads((ROOT / rel).read_text()) for rel in pre.GATES}
    for rel, want in pre.GATES.items():
        if sha(ROOT / rel) != want:
            raise ReviewFailure('gate hash ' + rel)
    ax1 = gates[AX1_GATE]['accepted']
    t_prime = F(re.search(r"T'=t_1'/\(1-352J'\)=(\d+/\d+)", ax1).group(1))
    d_prime = F(re.search(r"bound value D'_ii=(\d+/\d+)", ax1).group(1))
    pre.PINNED_T_PRIME['T'] = t_prime
    ax2 = gates[AX2_GATE]['accepted']
    d_gate = F(int(re.search(r'exact datum d=(\d+)/\(4\*10\^40\)', ax2).group(1)), 4 * 10 ** 40)
    r_gate = F(int(re.search(r"exact radius bound R'=(\d+)/10\^40", ax2).group(1)), 10 ** 40)
    rb = pre.route_b_constants(TAU)
    rb100 = pre.route_b_constants(TAU / 100)
    crude = pre.route_b_constants(TAU, tier='crude_majorant')
    sp = rb['split']
    K, C, cs = rb['K_B'], rb['C_B'], rb['c_site_B']
    f = K * sp['S_lambda'] * (1 + Q)
    ledger = {'near': 2 * K * (1 + Q), 'straddling': f * 4 * sp['tW'] / (1 - 8 * sp['tW']),
              'normalization': f * 4 * sp['t0'] * sp['tW'],
              'removal': f * 4 * sp['t0'] * sp['tW'] / ((1 - sp['t0']) * (1 - 8 * sp['tW'])),
              'feedback': f * (sp['beta'] - sp['c1'])}
    if sum(ledger.values()) != C:
        raise ReviewFailure('own ledger does not sum to C_B')
    j, gr, gpr = pre.J_B, pre.G_R, pre.GP_R
    admis = {'disc_self_map': j * 64 * TAU * gr, 'disc_contraction': j * 64 * TAU * gpr,
             'split_self_map': j * W * TAU * gr, 'split_contraction': j * W * TAU * gpr,
             'route_A_extremes_self_map': j * F(1, 37888) * gr, 'route_B_disc_radius_max': pre.R_BALL / (j * gr),
             'route_B_split_weight_max': pre.R_BALL / (j * gr) / TAU, 'route_A_extremes_contraction': j * F(1, 37888) * gpr}
    labelled = {'union_volume_C_B': 2 * C, 'nested_telescoping_C_prime_B': C / (1 - Q),
                'nested_telescoping_c_prime_site_B': cs / (1 - Q), 'telescoped_coefficient_input_K': K * (2 - Q) / (1 - Q),
                'refined_weighted_first_order_(49W+3)/144': 2 * F(49 * W + 3, 144) * TAU / (1 - j * 352 * W * TAU)}
    res_p, ns = pre.run_calculator()
    res_m, _ = pre.run_calculator(tau='-1/100000000')
    res100, _ = pre.run_calculator(fixed=False, tau='1/10000000000')
    eps = 2 * t_prime + t_prime ** 2
    pi_lo, pi_hi = pre.pi_bracket()
    e3 = pre.exp_bracket(3, 60)
    free_lo, free_hi = 1 / (4 * e3[1]), 1 / (4 * e3[0])
    dist_lo = F(0) if free_lo <= d_gate <= free_hi else min(abs(free_lo - d_gate), abs(free_hi - d_gate))
    own_r_lower = 2 * (d_prime + d_prime ** 2) + 51 * TAU / pi_hi + dist_lo
    own_r_upper_mine = 2 * (d_prime + d_prime ** 2) + 51 * TAU / pi_lo + max(abs(free_lo - d_gate), abs(free_hi - d_gate))
    t0 = sp['t0']
    depth = next(k for k in range(1, 10 ** 4) if (2 * k + 1) ** 3 * t0 >= 1)
    harmonic, n_h = F(0), 1
    while harmonic <= 3:
        n_h += 1
        harmonic += F(1, n_h)
    geo = enumerate_geometry()
    bb1 = gates[BB1_GATE]['accepted']
    route_a = {'K_BA1': F(re.search(r'K=(49/111790368)', gates[BA1_GATE]['accepted']).group(1)),
               'BB2_C_prime': F(4, 984375), 'BB2_c_prime_site': F(2, 984375)}
    for i, v in enumerate(re.findall(r'\bC=(\d+/\d+)', bb1)):
        route_a['BB1_C_%d' % i] = F(v)
    for i, v in enumerate(re.findall(r'c_site=(\d+/\d+)', bb1)):
        route_a['BB1_c_site_%d' % i] = F(v)
    return {'gates': gates, 'T_prime': t_prime, 'D_prime': d_prime, 'd': d_gate, 'R': r_gate, 'rb': rb, 'rb100': rb100,
            'crude': crude, 'ledger': ledger, 'admis': admis, 'labelled': labelled,
            'calc': {'plus': res_p, 'minus': res_m, 'tau_over_100': res100, 'ns': ns},
            'D_re': 2 * eps * (1 + eps) / (1 + eps * eps), 'own_r_lower': own_r_lower, 'own_r_upper_mine': own_r_upper_mine,
            'depth_without_decay': depth, 'harmonic_first_N_above_3': n_h,
            'region_factor_T_prime': (1 + t_prime) ** 2 - 1, 'region_factor_2T_prime': (1 + 2 * t_prime) ** 2 - 1,
            'geo': geo, 'route_a': route_a,
            'ratios': {'K_B': K / rb100['K_B'], 'C_B': C / rb100['C_B'], 'c_site_B': cs / rb100['c_site_B'],
                       'C_prime_B': C / rb100['C_B'], 'c_prime_site_B': cs / rb100['c_site_B'],
                       'node_radius_replay': F(res_p['certified_absolute_error_outward_1e-40']) /
                       F(res100['certified_absolute_error_outward_1e-40'])}}


# ------------------------------------------------------------ the review's value and report validator
def validate_producer(res, report, ref, contract):
    rb, sp = ref['rb'], ref['rb']['split']
    targets = {'K_B': F(1, 1000000), 'C_B': F(1, 250000), 'c_site_B': F(1, 500000), 'C_prime_B': F(1, 250000),
               'c_prime_site_B': F(1, 400000)}
    want = {'K_B': rb['K_B'], 'C_B': rb['C_B'], 'c_site_B': rb['c_site_B'], 'C_prime_B': rb['C_prime_B_union'],
            'c_prime_site_B': rb['c_prime_site_B_union']}
    hd = res['headline']
    for k, v in want.items():
        row = hd[k]
        if rat(row['exact']) != v or not is_truncation(row['preview'], v):
            raise Rejected('headline ' + k + ' differs from the recomputation')
        if rat(row['target']) != targets[k] or not is_truncation(row['margin'], targets[k] / v) or row['q'] != '1/64':
            raise Rejected('headline ' + k + ' target, margin or q differs')
        if row['tier'] != 'exact_first_order' or row['route'] != ('analytic_disc' if k == 'K_B' else 'iterated_split'):
            raise Rejected('headline ' + k + ' tier or route differs')
        if (k in ('C_prime_B', 'c_prime_site_B')) != (row.get('assembly') == 'union_comparison'):
            raise Rejected('headline ' + k + ' assembly differs (union_comparison: one direct c4B comparison)')
    for k in ('K_B', 'C_B', 'c_site_B'):
        if rat(hd['crude_tier'][k]['exact']) != ref['crude'][k]:
            raise Rejected('crude tier ' + k + ' differs')
        if not ref['crude'][k] > targets[k]:
            raise ReviewFailure('own crude tier meets a target')
    if rat(hd['node']['datum']) != ref['d'] or rat(hd['node']['radius_R_prime']) != ref['R'] or hd['node']['s'] != '1':
        raise Rejected('node values differ from the AX2 gate')
    for field, k in (('self_map', 'disc_self_map'), ('contraction', 'disc_contraction'), ('split_self_map', 'split_self_map'),
                     ('split_contraction', 'split_contraction')):
        if rat(hd['disc_admissibility'][field]) != ref['admis'][k]:
            raise Rejected('admissibility value differs: ' + k)
    if rat(hd['disc_admissibility']['route_A_extreme_self_map']) != ref['admis']['route_A_extremes_self_map']:
        raise Rejected('route-A extreme self-map differs')
    lem = check_by_id(res, 'marginal_locality_lemma_constants_route_b')
    for k, mine in (('beta_star', sp['beta']), ('c1', sp['c1']), ('c2', sp['c2']), ('t0', sp['t0']), ('tW', sp['tW']),
                    ('per_level_factor', sp['per_level_factor'])):
        if rat(lem[k]['exact']) != mine:
            raise Rejected('split constant differs: ' + k)
    if rat(lem['S_lambda']) != sp['S_lambda'] or lem['lemma']['eta'] != '0' or rat(lem['lemma']['w_prime']) != 512:
        raise Rejected('lemma form differs')
    lab = check_by_id(res, 'labelled_values_not_bound')['labelled']
    for k, v in ref['labelled'].items():
        if rat(lab[k]['exact']) != v:
            raise Rejected('labelled value differs: ' + k)
    wd = check_by_id(res, 'weights_declared_and_admissible')
    if rat(wd['weights']['route_B_disc_radius_max']) != ref['admis']['route_B_disc_radius_max'] \
            or rat(wd['weights']['route_B_split_weight_max']) != ref['admis']['route_B_split_weight_max'] \
            or rat(wd['weights']['split_creation_weight']) != W or rat(wd['weights']['lambda']) != F(2, W):
        raise Rejected('declared weights differ')
    ratios = check_by_id(res, 'tau_scaling_every_constant')['ratios']
    for k, v in ref['ratios'].items():
        if rat(ratios[k]['exact']) != v:
            raise Rejected('tau/100 ratio differs: ' + k)
    if rat(ratios['node_datum']['exact']) != 1 or rat(ratios['q_and_rho_over_tau']['exact']) != 1:
        raise Rejected('frozen ratios differ from 1')
    nr = check_by_id(res, 'node_replay_equals_ax2_gate')
    ci = ref['calc']['plus']['actual_C_interval']
    lo, hi = rat(nr['interval']['lower']), rat(nr['interval']['upper'])
    if rat(nr['datum']) != ref['d'] or rat(nr['radius_R_prime']) != ref['R'] or [lo, hi] != [F(ci['lower']), F(ci['upper'])] \
            or not ref['d'] - ref['R'] <= lo < hi <= ref['d'] + ref['R'] \
            or nr['sub_label'] != 'reference_unresolved' or nr['free_reference_inside'] is not True:
        raise Rejected('node replay record differs')
    oc = check_by_id(res, 'node_own_reevaluation_cross_check')
    own = rat(oc['own_radius_upper_labelled']['exact'])
    if not (ref['own_r_lower'] <= own <= ref['R']) or rat(oc['D_prime_recomputed_route_b']) != ref['D_prime']:
        raise Rejected('labelled own radius is not an upper bound of the formula below R\'')
    led = res['error_ledger']
    parts = {'near': rat(led['route_b_every_site_coefficient_input']['contribution_to_C_B']['exact']),
             'straddling': rat(led['straddling_supports_route_b']['contribution_to_C_B']['exact']),
             'normalization': rat(led['normalization']['contribution_to_C_B']['exact']),
             'removal': rat(led['split_remainder']['removal']['exact']),
             'feedback': rat(led['split_remainder']['closure_feedback']['exact'])}
    if parts != ref['ledger'] or sorted(led) != sorted(contract['preregistration']['error_terms_itemized']):
        raise Rejected('error ledger differs')
    ex = check_by_id(res, 'example_values_N_2_3_4')['C_B_q_pow_N_minus_1']
    for n in (2, 3, 4):
        if not is_truncation(ex[str(n)], rb['C_B'] * Q ** (n - 1)):
            raise Rejected('example values differ from C_B q^(N-1)')
    rows = check_by_id(res, 'item_4_coarse_translations')['rows']
    for key, e in (('(N,v)=(2,0)', 1), ('(3,(1,0,0))', 1), ('(4,(1,-1,0))', 2), ('(6,(2,1,0))', 3)):
        if not is_truncation(rows[key], rb['C_B'] * Q ** e):
            raise Rejected('translation rows differ from C_B q^(N-|v|_inf-1)')
    if rat(check_by_id(res, 'item_2a_exhaustion')['record']['constant']) != rb['exhaustion_union']:
        raise Rejected('exhaustion constant differs')
    rf = check_by_id(res, 'region_form_factor_route_b_t')
    if rat(rf['one_plus_t_sq_minus_1']['exact']) != ref['region_factor_T_prime']:
        raise Rejected('region-factor fixture not read with T\' (R1)')
    geo = ref['geo']
    pg = check_by_id(res, 'route_b_piece_graph_order_vs_distance')
    if pg['pieces'] != geo['pieces'] or pg['single_site_pieces'] != geo['single_pieces'] \
            or any(pg['orders'][u]['min_slack_over_1_plus_d'] != geo['bfs'][u]['min_slack']
                   or pg['orders'][u]['single_site_pieces_reached'] != geo['bfs'][u]['singles_reached'] for u in geo['bfs']):
        raise Rejected('piece graph differs from the own enumeration')
    cc = check_by_id(res, 'route_b_every_site_common_core')['rows']
    if [r['selected_source_faces'] for r in cc[:3]] != [geo['selected_source_faces'][n] for n in (2, 3, 4)] \
            or not all(r['ok'] for r in cc):
        raise Rejected('common-core rows differ')
    inc = check_by_id(res, 'route_b_incidence_on_R')['N2']
    if (inc['stars'], inc['singles'], inc['faces_charged'], inc['meeting_R'], inc['inside_R'], inc['straddling'],
            inc['straddling_strictly_containing_R']) != geo['incidence_R_N2']:
        raise Rejected('incidence on R differs')
    fx = check_by_id(res, 'item_2b_sign_mirror_pointwise')['flip_set']
    if (fx['plaquettes'], fx['selected_plaquettes'], fx['intersection_sizes']) != \
            (geo['flip']['plaquettes'], geo['flip']['selected'], geo['flip']['sizes']):
        raise Rejected('flip set differs')
    tf = check_by_id(res, 'item_4_coarse_translations')['fixture']
    if tf['count'] != geo['translations']['count'] or tf['all_coarse'] is not True:
        raise Rejected('translation fixture differs')
    if check_by_id(res, 'per_site_charging_versus_growing_sizes')['first_depth_without_decay'] != ref['depth_without_decay'] \
            or check_by_id(res, 'fixture_whole_sequence_versus_subsequence')['fixture']['harmonic_first_N_above_3'] != \
            ref['harmonic_first_N_above_3']:
        raise Rejected('fixture counts differ')
    if res['gate_fields'] != contract['preregistration']['gate_fields_required'] or 'dynamics_level' in res \
            or any(res[k] != v for k, v in res['gate_fields'].items()):
        raise Rejected('gate fields differ from the contract')
    if res['label'] != 'convergence_of_named_constructions' or res['secondary_labels'] != SECONDARY:
        raise Rejected('sub-labels differ')
    if res['obligations'] != OBLIGATIONS:
        raise Rejected('obligations differ from contract item 6')
    tmpl = contract['preregistration']['mandatory_sentence_template']
    if res['mandatory_sentence_template'] != tmpl or pre.normalize(hd['statement']).count(pre.normalize(tmpl)) != 1:
        raise Rejected('mandatory template differs')
    if res['uniform_wilson_claim'] is not True or 'no uniform Wilson-mean sign certificate' not in res['uniform_wilson_claim_scope']:
        raise Rejected('uniform_wilson_claim without its scope')
    validate_report(report, res, ref)
    return True


def validate_report(report, res, ref):
    rb = ref['rb']
    vals = {'K_B': rb['K_B'], 'C_B': rb['C_B'], 'c_site,B': rb['c_site_B']}
    targets = {'K_B': F(1, 1000000), 'C_B': F(1, 250000), 'c_site,B': F(1, 500000)}
    rows = re.findall(r'^\| `(K_B|C_B|c_site,B)` \(T\d[^|]*\| `(\d+/\d+)` \| `([0-9.e-]+)` \| `(\d+/\d+)` \| `([0-9.]+)` \|',
                      report, re.M)
    rows += re.findall(r'^\| `(C_B|c_site,B)` \| `(\d+/\d+)` \| `([0-9.e-]+)` \| `(\d+/\d+)` \| `([0-9.]+)` \|$', report, re.M)
    if len(rows) != 5:
        raise Rejected('report constant tables not found (%d rows)' % len(rows))
    for name, exact, prev, target, margin in rows:
        v = vals[name]
        if F(exact) != v or not is_truncation(prev, v) or F(target) != targets[name] or not is_truncation(margin, targets[name] / v):
            raise Rejected('report table row differs from the recomputation: ' + name)
    for name, tgt, v in (("C'_B", F(1, 250000), rb['C_prime_B_union']), ("c'_site,B", F(1, 400000), rb['c_prime_site_B_union'])):
        m = re.search(r"^\| `" + re.escape(name) + r"` \(T\d[^|]*\| equal to `[^`]+` \| `([0-9.e-]+)` \| `(\d+/\d+)` \| `([0-9.]+)` \|",
                      report, re.M)
        if m is None or not is_truncation(m.group(1), v) or F(m.group(2)) != tgt or not is_truncation(m.group(3), tgt / v):
            raise Rejected('report whole-sequence row differs: ' + name)
    for label, exact, prev in (('crude `C_B`', ref['crude']['C_B'], None), ('crude `c_site,B`', ref['crude']['c_site_B'], None)):
        m = re.search(r'^\| ' + re.escape(label) + r' \(reported only\) \| `(\d+/\d+)` \| `([0-9.e-]+)` \|', report, re.M)
        if m is None or F(m.group(1)) != exact or not is_truncation(m.group(2), exact):
            raise Rejected('report crude row differs: ' + label)
    m = re.search(r'Example values of `C_B q\^\(N-1\)`[^:]*: `([0-9.e-]+)` \(`N=2`\), `([0-9.e-]+)` \(`N=3`\), `([0-9.e-]+)` \(`N=4`\)',
                  report)
    if m is None or not all(is_truncation(m.group(i), rb['C_B'] * Q ** i) for i in (1, 2, 3)):
        raise Rejected('report example values differ from C_B q^(N-1)')
    m = re.search(r"Rows: `\(N,v\)=\(2,0\)` and `\(3,\(1,0,0\)\)`: `([0-9.e-]+)`; `\(4,\(1,-1,0\)\)`: `([0-9.e-]+)`; "
                  r"`\(6,\(2,1,0\)\)`: `([0-9.e-]+)`", report)
    if m is None or not all(is_truncation(m.group(i), rb['C_B'] * Q ** i) for i in (1, 2, 3)):
        raise Rejected('report translation rows differ')
    m = re.search(r'`K_B` ratio `([0-9.e]+)`, `C_B`, `c_site,B`, `C\'_B`, `c\'_site,B` ratio `([0-9.e]+)`', report)
    if m is None or not is_truncation(m.group(1), ref['ratios']['K_B']) or not is_truncation(m.group(2), ref['ratios']['C_B']):
        raise Rejected('report tau/100 ratios differ')
    m = re.search(r'node radius replay ratio `([0-9.e]+)`', report)
    if m is None or not is_truncation(m.group(1), ref['ratios']['node_radius_replay']):
        raise Rejected('report node radius ratio differs')
    m = re.search(r'is `(\d+)/\(5\*10\^59\)` \(about `([0-9.e-]+)`\) and satisfies `r_own<=R\'` with slack about `([0-9.e-]+)`', report)
    own = rat(check_by_id(res, 'node_own_reevaluation_cross_check')['own_radius_upper_labelled']['exact'])
    if m is None or F(int(m.group(1)), 5 * 10 ** 59) != own or not within_ulp(m.group(3), ref['R'] - own):
        raise Rejected('report own radius differs from the results')
    m = re.search(r'`2\*29 rho G\(R\)=(\d+/\d+)` \(about `([0-9.e-]+)`\)', report)
    if m is None or F(m.group(1)) != ref['crude']['K_B'] or not within_ulp(m.group(2), ref['crude']['K_B']):
        raise Rejected('report crude K_B differs')
    if '(1639 pieces, 343 of them single sites)' not in report or ref['geo']['pieces'] != 1639:
        raise Rejected('report piece-graph counts differ')
    return True


# ------------------------------------------------------------ closure, replays, mutation harness
def verify_closure():
    freeze = json.loads((FWD / 'freeze.json').read_text())
    prefix = FWD_REL + '/'
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in FWD.rglob('*') if p.is_file() and p != FWD / 'freeze.json'}
    ok = (freeze['loop'] == 'BC2' and freeze['direction'] == 'forward' and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(prefix) for n in sources) and set(sources) == files and len(sources) == 46
          and all(sha(ROOT / n) == d for n, d in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files)
          and freeze['normal_optimized_identical'] is True and freeze['independent_before_current_counterpart_exchange'] is True
          and freeze['verdict'].startswith('accepted_within_scope'))
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    snapshots_equal = all((FWD / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, snapshots_equal, freeze


def caches():
    roots = [AX2_DIR, FWD, ROOT / 'research/round32/forward']
    return sorted({p.relative_to(ROOT).as_posix() for r in roots for p in r.rglob('*')
                   if p.name == '__pycache__' or p.suffix == '.pyc'})


def replay(script, pre_mode=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bc2-skeptic-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + str(script) + ' ' + done.stderr[-300:])
        return {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}, \
            ((out / 'results.json').read_bytes() if pre_mode else None)


def mutated_run(edits=(), report_edits=(), report_append=None, extra_input=None, input_edit=None, no_b=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bc2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique (%d): %r' % (code.count(old), old[:80]))
            code = code.replace(old, new)
        (dst / 'check.py').write_text(code)
        if report_edits or report_append is not None:
            rp = dst / 'report.md'
            text = rp.read_text()
            for old, new in report_edits:
                if text.count(old) != 1:
                    raise ReviewFailure('report mutation anchor not unique: %r' % old[:70])
                text = text.replace(old, new)
            if report_append is not None:
                text += report_append
            rp.write_text(text)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if input_edit is not None:
            rel, old, new = input_edit
            ip = dst / 'inputs' / rel
            raw = ip.read_bytes()
            if raw.count(old) != 1:
                raise ReviewFailure('input mutation anchor not unique: ' + rel)
            ip.write_bytes(raw.replace(old, new))
        out = Path(tmp) / 'out'
        flags = ([] if no_b else ['-B']) + (['-O'] if sys.flags.optimize else [])
        env = None
        if no_b:
            env = {k: v for k, v in os.environ.items() if k != 'PYTHONDONTWRITEBYTECODE'}
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo), env=env)
        results = json.loads((out / 'results.json').read_text()) if (out / 'results.json').is_file() else None
        outputs = {p.name: p.read_bytes() for p in sorted(out.glob('*.json'))} if out.is_dir() else {}
        report = (dst / 'report.md').read_text()
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        cache = sorted(p.relative_to(repo).as_posix() for p in repo.rglob('*') if p.name == '__pycache__' or p.suffix == '.pyc')
        return done.returncode, results, outputs, report, last.replace(tmp, '<tmp>'), cache


def parallel(fn, jobs):
    with ThreadPoolExecutor(max_workers=4) as ex:
        return list(ex.map(fn, jobs))


def tru(anchor):
    """Validator weakening: insert 'True or ' into the require(...) at the anchor."""
    if not anchor.lstrip().startswith('require('):
        raise ReviewFailure('weakening anchor is not a require: ' + anchor[:60])
    return [(anchor, anchor.replace('require(', 'require(True or ', 1))]


WEAK = [
    ('coherent_evidence_tampering', tru("    require(rc['coefficient_input_T0']['q'] == '1/64' and rc['coefficient_input_T0']['K_B_target'] == '1/1000000'"), 'K_B_target_relaxed'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))", "        return Q(value)")], 'float_input'),
    ('no_priority_or_continuum_claim', tru("        require(flags.get(k) is False, 'claim flag must be false: ' + k)"), 'continuum_true'),
    ('changed_model_relabelled', tru("    require(abs(parse_q(pk['tau'])) == parse_q(pre['tau']['value']), 'packet tau differs from the contract')"), 'tau_changed'),
    ('insufficient_verdict_retained', tru("    require(recorded == producer_outcome(ev), 'recorded outcome differs from the executed evidence')"), 'missed_target_relabelled_accepted'),
    ('tau_scaling_exponent', tru("    require(bracket[0] <= Q(ratio) <= bracket[1], 'tau/100 ratio outside the prefrozen bracket')"), 'quadratic_headline'),
    ('wrong_delta_alpha_hbar_clock', tru("    require(Q(value) == -Q(tau) / 72, 'first-order coefficient is not -tau/72 in delta units')"), 'amplitude_tau_over_576'),
    ('tier_mixing_rejected', tru("    require(rec['route'] == allowed_route[rec['name']], 'route label not allowed for ' + rec['name'])"), 'polymer_kp_route'),
    ('uniform_in_N_not_in_a', tru("        require('fixed spacing' in stripped or 'cutoff' in stripped, 'unqualified uniformity next to a rate')"), 'unqualified_uniform_next_to_rate'),
    ('placeholder_span_rejected', tru("    require(re.search(r'<[^<>]*(\\s|\\||e\\.g\\.)[^<>]*>', s) is None, 'placeholder span in an exported statement')"), 'angle_span_space'),
    ('negation_aware_phrase_scan', tru("    require(bad == [], 'forbidden phrasing used affirmatively, never allowed ['"), 'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window', [("PARAM_KEYS = ('metric', 'weights', 'window', 'clock',", "PARAM_KEYS = ('metric', 'weights', 'clock',")], 'window_removed'),
    ('rate_constant_pair_prefrozen', tru("        require(rec['q'] == parse_q(rc['coefficient_input_T0']['q']), 'rate differs from the frozen q=1/64')"), 'q_1_over_128'),
    ('decay_rate_in_N_not_a', tru("    require(unit == 'per coarse l-infinity step in N at fixed spacing', 'rate unit is not the coarse step in N at fixed spacing')"), 'per_fm'),
    ('topology_named', tru("    require(t == 'trace norm on B(H_Y)', 'state topology is not the trace norm on B(H_Y)')"), 'weak_star'),
    ('subsequence_versus_whole_sequence', tru("    require(obj['whole_sequence'] is True and obj['source'] == 'cauchy_bound_all_M_greater_than_N',"), 'whole_sequence_from_compactness'),
    ('common_clock', tru("    require(rec['coupling_plus'] == -rec['coupling_minus'], 'the two signs at different |tau|')"), 'signs_at_different_tau'),
    ('coefficient_decay_not_marginal_decay', tru("    require(not (inference == 'marginal_decay_from_coefficient_decay'),"), 'state_decay_from_coefficients'),
    ('normalization_couples_supports', tru("    require(includes_straddling is True, 'straddling supports dropped from the split')"), 'straddling_dropped'),
    ('outside_vector_not_ground_state', tru("    require(uses_gap_of_outside_vector is False, 'a gap argument applied to the outside vector')"), 'gap_argument_on_outside_vector'),
    ('global_fidelity_orthogonality_catastrophe', tru("    require(route in ('per_support_telescoping', 'iterated_split'), 'a bound through the global overlap of the two box vectors')"), 'global_overlap_route'),
    ('cutoff_uniform_then_removed', tru("    require(rec['constants_depend_on_L'] is False, 'constants depend on the on-site cutoff')"), 'constants_depend_on_L'),
    ('cutoff_vector_removal', tru("    require(method == 'ground_vector_eckart_with_route_b_gap_1/2', 'eigenvalue convergence alone or no route-B gap')"), 'eigenvalues_only'),
    ('region_constant_scales_with_Y', tru("    require(rec.get('Y_factor') == '|Y|', 'region bound without the |Y| factor (R constant reused)')"), 'R_constant_reused'),
    ('named_construction_not_uniqueness', [("    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])",
                                            "    forbidden = [p_ for p_ in ROUND_FORBIDDEN + list(pre['forbidden_phrasings']) if 'unique' not in p_ and 'infinite-volume' not in p_]")],
     'uniqueness_phrase'),
    ('global_lipschitz_not_decay', tru("    require(provenance == 'covering_chain_weights_and_site_potential',"), 'route_B_fixed_point_lipschitz'),
    ('fixture_second_order_propagation', tru("    require(claim['order_in_straddling_amplitudes'] == 2,"), 'first_order_claim'),
    ('fixture_split_lipschitz_and_trace', tru("        require(rule_factor_at_depth(dpt) < 1,"), 'growing_region_sizes'),
    ('zero_free_region_required', tru("    require(obj == 'creation_coefficients' or zero_free_region_proved is True,"), 'reduced_density_analytic'),
    ('every_site_coefficient_input', tru("    require(Q(rec['K']) != Q(49, 111790368), 'the BA1 gate value used as the route-B input')"), 'BA1_gate_value'),
    ('cutoff_limit_order', tru("    require(order == 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N', 'the N and cutoff limits exchanged')"), 'limits_exchanged'),
    ('cauchy_estimate_not_compactness', tru("    require(route == 'cauchy_bound_and_trace_class_completeness', 'convergence from compactness plus closeness')"), 'compactness_plus_closeness'),
    ('limit_identified_with_aq1_limits', tru("    require(rec['order'] == ['identification_on_every_finite_region', 'inheritance'], 'inheritance before identification')"), 'inheritance_first'),
    ('translation_invariance_separate_item', tru("    require(rec['nested_cubes_only'] is False, 'invariance derived from nested cubes alone')"), 'nested_cubes_only'),
    ('route_b_constants_not_route_a', tru("    require(rec['per_site_sum_over_tau'] == 29, 'per-site sum under the route-B label is not 29|tau|')"), 'per_site_sum_28'),
    ('disc_admissible_under_J_prime', tru("    require(sm <= R_BALL, label + ': self-map J rho G(R) <= R fails')"), None),
    ('support_one_groups', tru("    require(rec['straddles'] is False, 'single-factor group charged as straddling')"), 'charged_as_straddling'),
    ('route_b_first_order_marginal', tru("    require(rec['faces_moving_rho_R_at_first_order'] == 16,"), 'route_A_ten_faces'),
    ('selected_face_site_energy', tru("    require(rec['first_order_site_energy_max'] == 24, 'first-order site energies read as at most 18 (route A)')"), 'route_A_at_most_18'),
    ('one_family_no_common_limit', tru("    require(rec['common_limit_claimed'] is False, 'common limit of two route-B families claimed')"), 'common_limit_claimed'),
    ('exhaustion_within_prescription_only', tru("    require(rec['phrasing'] == 'exhaustion within the route-B prescription',"), 'boundary_condition_phrasing'),
    ('sign_mirror_pointwise', tru("    require(rec['minus_tau_status'] == 'U_E mirror replay (no real g)',"), 'second_coupling'),
    ('identification_before_inheritance_route_b', tru("    require(rec['regions'] == 'every finite region', 'identification not on every finite region')"), 'R_only_identification'),
    ('region_form_load_bearing_for_node', tru("    require(rec['region_form_proved_untruncated'] is True, 'node restated without the region-form Cauchy bound')"), 'R_form_only'),
    ('node_values_unchanged', tru("    require(Q(rec['radius']) == gate_R,"), 'rederived_radius_headline'),
    ('reference_unresolved_retained_route_b', tru("    require(rec['resolved_interaction_shift'] is False, 'an interaction shift claimed')"), 'shift_claimed'),
    ('no_finite_box_node_convergence', tru("    require(rec['finite_box_node_convergence_claimed'] is False,"), 'C_N_to_C_inf'),
    ('no_route_b_dynamics_claim', tru("    require(rec['route_b_dynamics_comparison'] is False and rec['correlation_function_statement'] is False,"), 'dynamics_comparison'),
    ('non_coarse_translation_no_claim', tru("    require(rec['non_coarse_claim'] == 'none',"), 'invariance_claimed'),
    ('model_crossing_rejected', tru("    require(rec['limit_identified_with'] in ('AX1 route-B AQ1-type states',),"), 'identified_with_BB2_limit'),
    ('direct_comparison_required', tru("    require(rec['kind'] == 'direct', 'a union-volume or telescoped comparison used to establish a target')"), 'telescoped_input'),
    ('rate_range_stated', tru("            require(re.search(r'(every N at least 2|every N_k at least 2|N at least \\|v\\|_inf\\+2|every N at least N_Y)', clause)"), 'rate_without_range'),
]
# The disc self-map guards two sites: the route-A extremes check before any constant and the control itself; a weakened
# self-map is exposed at the earlier one.
WEAK_EARLIER = {'disc_admissible_under_J_prime': 'check failed: weights_declared_and_admissible'}
CONSTS_CALL = "            consts[(tier, sign)] = routeb_constants(tier, tau, W_SPLIT, rho_factor * abs(tau), q, J_UNIT, F_FACES)"
KCS = "    K_B, C_B, cs_B = H['K'], H['C'], H['c_site']"
CP = "    Cp_B, csp_B = C_B * 1, cs_B * 1"
ROUTE_A = [
    ('per-site sum 28|tau| (single group dropped from the sum)',
     {'edits': [("len(OMITTED_IDX) + len(SELECTED_IDX), 3)", "len(OMITTED_IDX) + 0, 3)")]}, 'route-B per-site inputs'),
    ('49 first-order faces (selected faces dropped)',
     {'edits': [("if (f[1] in SELECTED_IDX and f[0] == u) or f[1] in OMITTED_IDX))", "if f[1] in OMITTED_IDX))")]}, 'route-B per-site inputs'),
    ('4 interaction groups per site', {'edits': [("    groups = len(stars_containing) + 1", "    groups = len(stars_containing) + 0")]},
     'route-B per-site inputs'),
    ('every constant evaluated with (28, 49)', {'edits': [(CONSTS_CALL, CONSTS_CALL.replace('q, J_UNIT, F_FACES)', 'q, 28, 49)'))]},
     'K_B formula'),
    ('contraction coefficient 9856=28*352 in the circle bound',
     {'edits': [("    return Q(F, 144) * rho / (1 - J_unit * 352 * rho)", "    return Q(F, 144) * rho / (1 - 9856 * rho)")]},
     'T_B(|tau|) equals the AX1 gate T prime'),
    ("G'(R) rescaled so that 29 G'(R) = 9856", {'edits': [("GPR_UP = Q(352)", "GPR_UP = Q(9856, 29)")]}, "G(R)<148/7 and G'(R)<352"),
    ('K_B replaced by the BA1 gate K=49/111790368', {'edits': [(KCS, "    K_B, C_B, cs_B = ba1_K, H['C'], H['c_site']")]}, 'K_B formula'),
    ('C_B replaced by a BB1 gate C', {'edits': [(KCS, "    K_B, C_B, cs_B = H['K'], bb1_C[-1], H['c_site']")]}, 'ledger sums to C_B'),
    ('c_site,B replaced by a BB1 gate c_site', {'edits': [(KCS, "    K_B, C_B, cs_B = H['K'], H['C'], bb1_cs[-1]")]},
     'tau/100 ratio outside the prefrozen bracket'),
    ("C'_B replaced by the BB2 gate C'=4/984375", {'edits': [(CP, "    Cp_B, csp_B = bb2_Cp, cs_B * 1")]}, 'bound exceeds its target'),
    ("c'_site,B replaced by the BB2 gate c'_site=2/984375", {'edits': [(CP, "    Cp_B, csp_B = C_B * 1, bb2_csp")]},
     'tau/100 ratio outside the prefrozen bracket'),
    ('disc radius set to the route-A extreme 1/37888', {'edits': [("    rho = rho_factor * TAU", "    rho = Q(1, 37888)")]},
     'disc: self-map J rho G(R) <= R fails'),
    ('split weight set to the route-A extreme 1/(37888|tau|)',
     {'edits': [(CONSTS_CALL, CONSTS_CALL.replace('tau, W_SPLIT,', 'tau, 1 / (37888 * TAU),'))]}, 'split weight: self-map J rho G(R) <= R fails'),
    ('split weight W=2600 (admissible only under 28|tau|)',
     {'edits': [(CONSTS_CALL, CONSTS_CALL.replace('tau, W_SPLIT,', 'tau, Q(2600),'))]}, 'split weight: self-map J rho G(R) <= R fails'),
    ('route-A ten-face first-order marginal (single groups dropped from the R incidence)',
     {'edits': [("    singles = [b for b in sorted(vol) if b in R_COVER]", "    singles = []")]}, 'route-B incidence on R at N=2'),
    ("D' recomputed with 28|tau|", {'edits': [("    Jt = 29 * TAU", "    Jt = 28 * TAU")]}, 'route-B D prime recomputed'),
    ("D' recomputed with 49 faces", {'edits': [("    t1 = Q(52, 144) * TAU", "    t1 = Q(49, 144) * TAU")]}, 'route-B D prime recomputed'),
    ('node slope 49|tau|/4 (seven stars)', {'edits': [("'k_prime_over_tau': rp['incidence']['k_prime_over_abs_tau'],", "'k_prime_over_tau': '49/4',")]},
     'a slope other than 51|tau|/4'),
    ('selected predicate without r=2', {'edits': [("p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)", "p[1] % 2 == 0 and p[0] % 4 in (0, 1)")]},
     'I1 table row disagrees with the derived class'),
    ('single groups not kept by route-B volumes', {'edits': [("def routeb_faces(vol, keep_singles=True,", "def routeb_faces(vol, keep_singles=False,")]},
     'single-factor group clipped by a route-B volume'),
    ('route-A rejection list emptied (weakening of route_b_constants_not_route_a)',
     {'edits': tru("            require(Q(v) != av, 'route-A constant ' + aname + ' under the route-B label ' + name)")},
     'damaging mutation accepted: BA1_K_under_route_B'),
    ("defence in depth: T' pin and per-site must removed, 49 faces",
     {'edits': [("    must(TB_tau == T_PRIME, 'T_B(|tau|) equals the AX1 gate T prime')", "    pass"),
                ("    must(J_UNIT == 29 and F_FACES == 52", "    must(True or J_UNIT == 29 and F_FACES == 52"),
                ("    F_FACES = ps['faces_per_site']", "    F_FACES = 49")]}, 'check failed: boundary_counts_at_most_bulk'),
]
TEMPLATE_ANCHOR = 'For the uniform Kogut-Susskind SU(2) model at fixed spacing and strong bare coupling handled by route B'
MUST_ABORT = [
    ('lattice sum without its 24r^2 shell', {'edits': [("    return 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)", "    return 1 + 2 * x / (1 - x)")]},
     'check failed: report_pins_exact_values'),
    ('C_B without the (1+q) of e_z', {'edits': [("    C = csite * (1 + q)", "    C = csite")]}, 'ledger sums to C_B'),
    ('near term 2 replaced by 1', {'edits': [("    csite = K * (2 + beta * S)", "    csite = K * (1 + beta * S)")]}, 'ledger sums to C_B'),
    ("C'_B with a union-volume factor 2", {'edits': [(CP, "    Cp_B, csp_B = C_B * 2, cs_B * 1")]}, 'tau/100 ratio outside the prefrozen bracket'),
    ('AX2 gate datum perturbed by 10^-40 (the producer audit edit)',
     {'edits': [("ax2['accepted']).group(1)), 4 * 10 ** 40)", "ax2['accepted']).group(1)), 4 * 10 ** 40) + Q(1, 10 ** 40)")]},
     'calculator replay equals the AX2 gate rationals'),
    ('input: AX2 calculator slope edited', {'input_edit': ('research/round32/forward/ax2/calculator.py', b'K_PRIME_OVER_TAU = 2 * B_N_OVER_TAU_G_UNITS',
                                                           b'K_PRIME_OVER_TAU = 2 * B_N_OVER_TAU_G_UNITS - Q(1, 2)')},
     'AX2 calculator bytes differ from the pinned sha256'),
    ("input: AX1 gate T' edited", {'input_edit': (AX1_GATE, b"T'=t_1'/(1-352J')=13/3599632512", b"T'=t_1'/(1-352J')=13/3599632513")},
     'admitted gate bytes differ from the pinned sha256'),
    ('input: contract snapshot edited', {'input_edit': ('research/round33/contracts/bc2.json', b'"N_min": "2"', b'"N_min": "3"')},
     'contract snapshot hash differs from the bound constant'),
    ('input: undeclared skeptic file', {'extra_input': 'research/round33/skeptic/bc2-independent-derivation.md'},
     'forbidden premise in producer inputs'),
    ('report: forbidden phrase appended', {'report_append': '\nThe route-B limit is the thermodynamic limit.\n'},
     'forbidden phrasing used affirmatively'),
    ('report: template altered', {'report_edits': [(TEMPLATE_ANCHOR, 'For the uniform Kogut-Susskind SU(2) model handled by route B')]},
     'mandatory template not quoted exactly once'),
    ('report: pinned ledger value altered', {'report_edits': [('845/894120192', '845/894120193')]}, 'check failed: report_pins_exact_values'),
]
SILENT = [
    ('harmless: e^(1/8) enclosure with 30 terms', {'edits': [("def exp_upper(x, terms=24):", "def exp_upper(x, terms=30):")]}, None),
    ('example values with exponent N instead of N-1', {'edits': [("sci(C_B * q ** (N - 1)) for N in (2, 3, 4)}", "sci(C_B * q ** N) for N in (2, 3, 4)}")]},
     'example values differ from C_B q^(N-1)'),
    ('translation row (4,(1,-1,0)) with exponent 3', {'edits': [("'(4,(1,-1,0))': sci(C_B * q ** 2)", "'(4,(1,-1,0))': sci(C_B * q ** 3)")]},
     'translation rows differ'),
    ('labelled own radius with the seven-star slope 49|tau|/4',
     {'edits': [("    own_E = ceil_to(2 * (D_PRIME + D_PRIME ** 2) + 51 * TAU / pi_lo, 10 ** 60)",
                 "    own_E = ceil_to(2 * (D_PRIME + D_PRIME ** 2) + 49 * TAU / pi_lo, 10 ** 60)")]},
     'labelled own radius is not an upper bound'),
    ('report: K_B margin changed in the verdict table', {'report_edits': [('| `1/1000000` | `2.14932738461` |', '| `1/1000000` | `2.24932738461` |')]},
     'report table row differs'),
    ('report: C_B exact changed at one of its two sites',
     {'report_edits': [('| `C_B` (T1, R form) | `2326328761843649826272217312701707175/',
                        '| `C_B` (T1, R form) | `2326328761843649826272217312701707176/')]}, 'report table row differs'),
]


def uniqueness_clauses(report, template):
    body = pre.normalize(report).replace(pre.normalize(template), ' ')
    cls = pre.clauses(body)
    out = []
    for i, cl in enumerate(cls):
        if not re.search(r'unique', cl, re.I):
            continue
        prev = cls[i - 1].strip() if i else ''
        if 'unique gauge-invariant ground' in cl:
            kind = 'AX1 gate finite-volume statement (every finite complete-factor route-B volume)'
        elif 'uniqueness in the ball' in cl or 'the only one in the ball' in cl:
            kind = 'fixed point unique in the AM2 ball'
        elif re.search(r'uniqueness_of_ground_state_claimed|named_construction_not_uniqueness', cl):
            kind = 'control or field identifier'
        elif '| uniqueness of any ground state | a uniqueness mechanism beyond the named construction |' in cl:
            kind = 'open obligation row'
        elif pre.NEGATION.search(cl) or prev.endswith('Not inherited') or prev.endswith('(respected)**'):
            kind = 'negated or excluded'
        elif 'Contract exclusions (respected)' in cl or cl.strip() == 'uniqueness of every infinite-volume ground state':
            kind = 'claim-exclusion list quoted verbatim'
        elif 'the member through the first site of `T` is unique' in cl:
            kind = 'combinatorial (the covering member through a site)'
        else:
            kind = 'other'
        out.append({'clause': cl[:170], 'kind': kind})
    return out


def run(args):
    # 1. contract, pre-comparison package unchanged and replayed ------------------------------------------------------
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_sha256_pinned', sha256=CONTRACT_SHA)
    con = json.loads(CONTRACT.read_text())
    pf = json.loads(PRE_FREEZE.read_text())
    ok_pf = pf['contract_sha256'] == CONTRACT_SHA and pf['loop'] == 'BC2' and pf['stage'] == 'pre_comparison' \
        and all(sha(ROOT / p) == h for p, h in pf['files'].items())
    _, pre_bytes = replay(PRE_SCRIPT, pre_mode=True)
    need(ok_pf and pre_bytes == PRE_RESULTS.read_bytes(), 'pre_comparison_package_unchanged_and_replayed',
         freeze=pf['files'], note='the committed pre-comparison package (5ec599f, before the forward commit ee45eed) is '
                                  'unchanged; bc2_check.py reproduces bc2-independent/results.json byte for byte in this '
                                  'interpreter mode')

    # 2. closure, inventory, replays, pinned artifacts, caches ---------------------------------------------------------
    ok, inputs, snaps, freeze = verify_closure()
    declared = sorted(set(['AGENTS.md', 'research/round33/contracts/bc2.json'] + con['shared_premises']))
    need(ok and inputs == declared and snaps and inputs == sorted(pre.OBSERVED_INPUTS)
         and all(sha(FWD / 'inputs' / n) == pre.OBSERVED_INPUTS[n] for n in inputs),
         'producer_closure_and_inventory', closure_files=len(freeze['sources']), inputs=len(inputs),
         note='46 closure files verified one by one; 42 inputs equal the contract-derived list and the inventory recorded '
              'before production; every snapshot byte-identical to the repository')
    need(all(sha(FWD / p) == h for p, h in FROZEN.items()), 'frozen_artifacts_pinned', pinned=FROZEN)
    outs, _ = replay(FWD / 'check.py')
    frozen_out = {p: sha(FWD / 'output' / p) for p in ('results.json', 'source-manifest.json')}
    need(outs == frozen_out and frozen_out['results.json'] == FROZEN['output/results.json']
         and frozen_out['source-manifest.json'] == FROZEN['output/source-manifest.json'],
         'producer_replay_byte_identical', outputs=outs,
         note='the producer replay in this interpreter mode (-B, or -B -O when this program runs under -O) reproduces output/')
    res = json.loads((FWD / 'output/results.json').read_text())
    report = (FWD / 'report.md').read_text()

    # 3. values against the independent recomputation -------------------------------------------------------------------
    ref = reference()
    need(validate_producer(res, report, ref, con) is True, 'producer_values_equal_independent_recomputation',
         K_B=q_(ref['rb']['K_B']), C_B=q_(ref['rb']['C_B']), c_site_B=q_(ref['rb']['c_site_B']),
         C_prime_B_union=q_(ref['rb']['C_prime_B_union']), c_prime_site_B_union=q_(ref['rb']['c_prime_site_B_union']),
         previews={k: preview(ref['rb'][k]) for k in ('K_B', 'C_B', 'c_site_B')},
         margins={'K_B': preview(F(1, 1000000) / ref['rb']['K_B'], 8), 'C_B': preview(F(1, 250000) / ref['rb']['C_B'], 8),
                  'c_site_B': preview(F(1, 500000) / ref['rb']['c_site_B'], 8),
                  'C_prime_B_union': preview(F(1, 250000) / ref['rb']['C_B'], 8),
                  'c_prime_site_B_union': preview(F(1, 400000) / ref['rb']['c_site_B'], 8)},
         note='every exported constant, the split closure, crude tier, admissibility, ledger, labelled values, tau/100 '
              'ratios, node record, example and translation rows, geometry counts, fixture counts, gate fields, labels, '
              'obligations and the report tables equal the recomputation (route-B inputs only; nothing read from the producer)')
    pr = json.loads(PRE_RESULTS.read_text())
    same_pred = all(F(pr['constants'][k]) == F(res['headline'][h]['exact']) for k, h in
                    (('K_B', 'K_B'), ('C_B', 'C_B'), ('c_site_B', 'c_site_B'), ('C_prime_B_union', 'C_prime_B'),
                     ('c_prime_site_B_union', 'c_prime_site_B')))
    lem = check_by_id(res, 'marginal_locality_lemma_constants_route_b')
    same_split = all(F(pr['split'][k]) == F(lem[p]['exact']) for k, p in
                     (('t0', 't0'), ('tW', 'tW'), ('c1', 'c1'), ('c2', 'c2'), ('beta', 'beta_star'), ('per_level_factor', 'per_level_factor')))
    lab = check_by_id(res, 'labelled_values_not_bound')['labelled']
    same_nested = F(pr['constants']['C_prime_B_nested']) == F(lab['nested_telescoping_C_prime_B']['exact']) \
        and F(pr['constants']['c_prime_site_B_nested']) == F(lab['nested_telescoping_c_prime_site_B']['exact'])
    ratio_c = check_by_id(res, 'tau_scaling_every_constant')['ratios']['C_B']['exact']
    need(same_pred and same_split and same_nested and F(pr['split']['S_lambda']) == F(lem['S_lambda'])
         and pr['margins']['K_B'].startswith('2.1493') and pr['margins']['c_site_B'].startswith('2.1491')
         and pr['tau_over_100']['C_B'].startswith('1.0066145') and F(ratio_c) < F(1006615, 10000),
         'pre_comparison_predictions_equal_exactly',
         equal=['K_B', 'C_B', 'c_site_B', "C'_B (union)", "c'_site,B (union)", 't0', 'tW', 'c1', 'c2', 'beta*', 'S_lambda',
                "C'_B and c'_site,B nested (labelled)"],
         skeptic_rounding_slip='the derivation prediction table (section 10) rounds the density-constant tau/100 ratio to '
                               '100.662; the exact ratio is about 100.6614518 (100.661 to three decimals, as the contract '
                               'review and results.json record)',
         note='the frozen pre-comparison rationals equal the producer rationals digit for digit')

    # 4. readings R1, R2 and R7 -------------------------------------------------------------------------------------------
    rf = check_by_id(res, 'region_form_factor_route_b_t')
    wfo = F(lab['refined_weighted_first_order_(49W+3)/144']['exact'])
    need(F(rf['one_plus_t_sq_minus_1']['exact']) == ref['region_factor_T_prime'] <= F(1, 10 ** 8) < ref['region_factor_2T_prime']
         and rf['t'] == 'T_B(|tau|)=13/3599632512' and wfo == ref['labelled']['refined_weighted_first_order_(49W+3)/144']
         and wfo < F(lem['tW']['exact']) == ref['rb']['split']['tW'] == F(26, 3148137)
         and 'The refinement `(49W+3)/144` is labelled and not used.' in report,
         'readings_R1_R2', R1={'producer_t': 'T\' (per-box anchored bound)', '(1+T\')^2-1': preview(ref['region_factor_T_prime']),
                                '(1+2T\')^2-1': preview(ref['region_factor_2T_prime'])},
         R2={'labelled_refined_t_W': preview(wfo), 'bound_t_W': q_(ref['rb']['split']['tW'])},
         note='R1: the producer re-checks (1+t)^2<=1+10^-8 with t=T\' (it fails with 2T\'); R2: the weighted first order '
              '(49W+3)|tau|/144 is labelled, the bound t_W uses 52W|tau|/144')
    calc_rel = 'research/round32/forward/ax2/calculator.py'
    need(caches() == [] and "load_calculator(INPUTS / CALCULATOR_REL)" in (FWD / 'check.py').read_text()
         and 'sys.dont_write_bytecode = True' in (FWD / 'check.py').read_text(), 'reading_R7_no_interpreter_cache',
         checked=['research/round32/forward/ax2/', FWD_REL + '/ (inputs included)', 'research/round32/forward/'],
         note='after the producer replays and this review\'s own calculator runs (executed from source bytes), no '
              '__pycache__ or .pyc exists under the checked trees; the producer loads ' + calc_rel +
              ' from its inputs/ snapshot with bytecode writing disabled (a run without -B is exercised below)')

    # 5. geometry, node and fixtures recorded ----------------------------------------------------------------------------
    geo = ref['geo']
    need(geo['per_site_faces'] == 52 and geo['pieces'] == 1639 and geo['single_pieces'] == 343 and all(v['min_slack'] == 0 for v in geo['bfs'].values())
         and geo['incidence_R_N2'] == (7, 2, 153, 88, 16, 72, 6) and geo['selected_source_faces'] == {2: 654, 3: 1158, 4: 1806}
         and geo['flip'] == {'plaquettes': 864, 'selected': 108, 'sizes': [1, 3]}
         and geo['translations'] == {'count': 8, 'all_coarse': True},
         'geometry_reenumerated',
         piece_graph_Lambda_3={'pieces': geo['pieces'], 'single_site_pieces': geo['single_pieces'], 'bfs': geo['bfs']},
         per_site_first_order_faces=geo['per_site_faces'], incidence_R=list(geo['incidence_R_N2']), c1B_selected_source_faces=geo['selected_source_faces'],
         flip_set=geo['flip'], grouping_preserving_translations=geo['translations'],
         note='own enumeration with the pre-comparison grouping; 19 single-site pieces of Lambda_3 (two or more '
              'coordinates equal to +3) meet no star inside the box and are unreachable, hence 324 reached from each u')
    cp, cm, c100 = ref['calc']['plus'], ref['calc']['minus'], ref['calc']['tau_over_100']
    own = F(check_by_id(res, 'node_own_reevaluation_cross_check')['own_radius_upper_labelled']['exact'])
    need(F(cp['certified_datum']) == ref['d'] and F(cp['certified_absolute_error_outward_1e-40']) == ref['R']
         and F(cm['certified_datum']) == ref['d'] and F(cm['certified_absolute_error_outward_1e-40']) == ref['R']
         and cp['free_reference_included'] is True and cp['sub_label'] == 'reference_unresolved'
         and F(cp['state_bound_D_prime']) == ref['D_prime'] == ref['D_re'] and F(c100['certified_datum']) == ref['d']
         and ref['own_r_lower'] <= own <= ref['R'] and own <= ref['own_r_upper_mine'] + F(1, 10 ** 59),
         'node_replayed_and_cross_checked', datum=q_(ref['d']), R_prime=q_(ref['R']),
         producer_own_radius=preview(own), own_radius_slack=preview(ref['R'] - own, 4),
         own_lower_bound_of_formula=preview(ref['own_r_lower']),
         note='the admitted calculator (executed from its pinned source bytes) returns d and R\' at +tau and at the mirror; '
              'D\'=2eps(1+eps)/(1+eps^2), eps=2T\'+T\'^2; the producer\'s labelled r_own lies between the formula\'s '
              'rigorous lower value (own Machin pi, own e^3 series) and R\', about 2.7e-41 below R\'')

    # 6. text: phrase tool, template, uniqueness clauses --------------------------------------------------------------
    need(sha(PHRASE_TOOL) == PHRASE_TOOL_SHA, 'phrase_tool_pinned')
    done = subprocess.run([sys.executable, '-B', str(PHRASE_TOOL), str(CONTRACT), str(FWD / 'report.md')],
                          capture_output=True, text=True, cwd=str(ROOT))
    tool_out = json.loads(done.stdout)
    template = con['preregistration']['mandatory_sentence_template']
    forbidden = pre.ROUND_FORBIDDEN + con['preregistration']['forbidden_phrasings']
    need(done.returncode == 0 and list(tool_out.values()) == [[]] and pre.affirmative_hits(report, forbidden, template) == []
         and pre.normalize(report).count(pre.normalize(template)) == 1
         and sum(1 for ln in report.splitlines() if ln.strip() == '> ' + template) == 1, 'phrase_scan_and_template',
         tool_exit=done.returncode, template_lines=1)
    uq = uniqueness_clauses(report, template)
    need(not [u for u in uq if u['kind'] == 'other'] and any(u['kind'].startswith('AX1 gate finite-volume') for u in uq),
         'uniqueness_wording_classified', clauses=uq,
         note='every clause mentioning uniqueness is negated or excluded, a field or control identifier, the open '
              'obligation row, the fixed point unique in the AM2 ball, or the AX1 finite-volume statement (a simple '
              'ground in every finite route-B volume); no infinite-volume uniqueness is asserted')

    # 7. damaged packets rejected by this review's validator ---------------------------------------------------------------
    def damaged(fn):
        pk = json.loads(json.dumps(res))
        fn(pk)
        try:
            validate_producer(pk, report, ref, con)
        except Rejected as exc:
            return str(exc)
        return None

    def setp(path, value):
        def fn(pk):
            node = pk
            for key in path[:-1]:
                node = check_by_id(pk, key[6:]) if key.startswith('check:') else node[key]
            node[path[-1]] = value(node[path[-1]]) if callable(value) else value
        return fn

    rbv = ref['rb']
    dmg = [
        ('K_B halved', setp(['headline', 'K_B', 'exact'], lambda v: q_(F(v) / 2)), 'headline K_B'),
        ('C_B replaced by a BB1 gate C', setp(['headline', 'C_B', 'exact'], q_(ref['route_a']['BB1_C_1'])), 'headline C_B'),
        ("c'_site,B replaced by the nested value under union_comparison",
         setp(['headline', 'c_prime_site_B', 'exact'], q_(rbv['c_prime_site_B_nested'])), 'headline c_prime_site_B'),
        ("C'_B assembly relabelled nested_telescoping", setp(['headline', 'C_prime_B', 'assembly'], 'nested_telescoping'), 'assembly'),
        ('crude C_B changed', setp(['headline', 'crude_tier', 'C_B', 'exact'], q_(2 * rbv['C_B'])), 'crude tier'),
        ("node radius replaced by the re-derived own radius",
         setp(['headline', 'node', 'radius_R_prime'], check_by_id(res, 'node_own_reevaluation_cross_check')['own_E_prime_upper']['exact']),
         'node values'),
        ('uniqueness flag true', setp(['gate_fields', 'uniqueness_of_ground_state_claimed'], True), 'gate fields'),
        ('dynamics_level exported', setp(['dynamics_level'], 'correlation_functions_compact_window'), 'gate fields'),
        ('C_B tau/100 ratio set to 100', setp(['check:tau_scaling_every_constant', 'ratios', 'C_B', 'exact'], '100'), 'tau/100 ratio'),
        ('label changed to common_limit_of_named_constructions', setp(['label'], 'common_limit_of_named_constructions'), 'sub-labels'),
        ('obligation dropped', setp(['obligations'], OBLIGATIONS[:4]), 'obligations'),
        ('template trimmed in the results', setp(['mandatory_sentence_template'], template.replace('not uniqueness of any ground state, ', '')),
         'mandatory template'),
        ('beta* altered', setp(['check:marginal_locality_lemma_constants_route_b', 'beta_star', 'exact'], q_(rbv['split']['beta'] * 2)),
         'split constant'),
        ('ledger normalization doubled', setp(['error_ledger', 'normalization', 'contribution_to_C_B', 'exact'],
                                              q_(ref['ledger']['normalization'] * 2)), 'error ledger'),
        ('route-A extreme self-map changed to 1/64', setp(['headline', 'disc_admissibility', 'route_A_extreme_self_map'], '1/64'),
         'route-A extreme self-map'),
        ('region fixture read with 2T\'', setp(['check:region_form_factor_route_b_t', 'one_plus_t_sq_minus_1', 'exact'],
                                               q_(ref['region_factor_2T_prime'])), 'region-factor fixture'),
    ]
    rows_d = []
    for label, fn, reason in dmg:
        got = damaged(fn)
        if got is None or reason not in got:
            raise ReviewFailure('damaged packet accepted or rejected for another reason: %s (%s)' % (label, got))
        rows_d.append({'mutation': label, 'rejected_for': reason})
    need(len(rows_d) == len(dmg), 'damaged_packets_rejected_by_review_validator', rows=rows_d)

    # 8. source-edit runs ----------------------------------------------------------------------------------------------------
    label_sets = {c['id']: sorted(c['rejected_mutations']) for c in res['checks'] if c.get('rejected_mutations')}
    if sorted(w[0] for w in WEAK) != sorted(con['controls']):
        raise ReviewFailure('weakening table does not cover the 52 controls')
    for cid, _, label in WEAK:
        if label is not None and label not in label_sets.get(cid, []):
            raise ReviewFailure('expected label is not a mutation of the control: %s %s' % (cid, label))
    base = mutated_run()
    frozen_bytes = {p.name: p.read_bytes() for p in sorted((FWD / 'output').glob('*.json'))}
    nob = mutated_run(no_b=True)
    need(base[0] == 0 and base[2] == frozen_bytes and base[5] == [] and nob[0] == 0 and nob[2] == frozen_bytes and nob[5] == [],
         'unmutated_copies_and_run_without_B',
         note='an unmutated copy outside the checkout reproduces the frozen output byte for byte; a run without -B (and '
              'without PYTHONDONTWRITEBYTECODE) reproduces it too and writes no __pycache__ or .pyc anywhere in the copy, '
              'the calculator snapshot included (R7)')
    weak_out = parallel(lambda w: mutated_run(edits=w[1]), WEAK)
    weak_rows = []
    for (cid, _, label), (rc, _, outs, _, last, cache) in zip(WEAK, weak_out):
        expect = ('damaging mutation accepted: ' + label) if label is not None else WEAK_EARLIER[cid]
        if rc == 0 or outs or not last.endswith(expect) or cache:
            raise ReviewFailure('weakening of %s not exposed as expected: %s' % (cid, last[-200:]))
        weak_rows.append({'control': cid, 'aborted_with': expect})
    need(len(weak_rows) == 52, 'control_validator_weakenings', runs=len(weak_rows), rows=weak_rows,
         note='one validator weakened per contract control on a temporary copy ("True or " inserted into the require that '
              'rejects the named mutation, or the float branch returning a Fraction, or one key dropped from the declared '
              'parameter list, or the uniqueness vocabulary dropped); each run aborts naming a mutation of that control, '
              'except the disc self-map, which is exposed one guard earlier (the route-A extremes check)')

    def run_expect(table):
        outs = parallel(lambda t: mutated_run(**t[1]), table)
        rows = []
        for (label, _, expect), (rc, _, o, _, last, cache) in zip(table, outs):
            if rc == 0 or o or expect not in last or cache:
                raise ReviewFailure('edit ran or aborted elsewhere: %s: %s' % (label, last[-200:]))
            rows.append({'edit': label, 'aborted_with': expect})
        return rows

    ra_rows = run_expect(ROUTE_A)
    need(len(ra_rows) == len(ROUTE_A), 'route_a_substitutions_abort', runs=len(ra_rows), rows=ra_rows,
         note='every route-A input (28|tau|, 49 faces, 4 groups, 9856, the route-A disc and split-weight extremes, W=2600) '
              'and every route-A gate constant (BA1 K, BB1 C and c_site, BB2 C\' and c\'_site) substituted into the '
              'producer check.py aborts without output; with the T\' pin and the per-site must removed, 49 faces are '
              'still caught (the per-site face counts of the boxes exceed the substituted bulk value)')
    ab_rows = run_expect(MUST_ABORT)
    need(len(ab_rows) == len(MUST_ABORT), 'must_abort_edits', runs=len(ab_rows), rows=ab_rows)
    sil_out = parallel(lambda t: mutated_run(**t[1]), SILENT)
    silent_rows = []
    for (label, _, expect), (rc, out_res, _, out_report, last, cache) in zip(SILENT, sil_out):
        if rc != 0 or out_res is None or cache:
            raise ReviewFailure('silent edit aborted: %s: %s' % (label, last))
        try:
            validate_producer(out_res, out_report, ref, con)
        except Rejected as exc:
            if expect is None or expect not in str(exc):
                raise ReviewFailure('silent edit rejected for the wrong reason: %s: %s' % (label, exc))
            silent_rows.append({'edit': label, 'producer': 'ran', 'review_validator': 'rejected: ' + expect})
            continue
        if expect is not None:
            raise ReviewFailure('silent edit not caught by the review validator: ' + label)
        silent_rows.append({'edit': label, 'producer': 'ran', 'review_validator': 'accepted (non-damaging: every '
                                                                                   'exported admitted value unchanged)'})
    need(len(silent_rows) == len(SILENT), 'silent_edits_accounted', rows=silent_rows)
    need(caches() == [], 'no_interpreter_cache_after_all_runs', checked=['research/round32/forward/', FWD_REL + '/'])

    n_runs = 2 + len(weak_rows) + len(ra_rows) + len(ab_rows) + len(silent_rows)
    return {
        'loop': 'BC2', 'stage': 'post_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': CONTRACT_SHA, 'producer': 'forward (single producer, single+skeptic)',
        'source_edit_runs': n_runs,
        'source_edit_breakdown': {'unmutated_and_no_B': 2, 'control_validator_weakenings': len(weak_rows),
                                  'route_a_substitutions': len(ra_rows), 'must_abort_edits': len(ab_rows),
                                  'silent_edits': len(silent_rows)},
        'checks': CHECKS,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = run(args)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'source_edit_runs': result['source_edit_runs']}))


if __name__ == '__main__':
    main()
