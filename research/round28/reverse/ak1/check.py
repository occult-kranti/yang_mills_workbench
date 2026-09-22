#!/usr/bin/env python3
"""Fresh, exact AK1 reverse audits; standard library, snapshot-only runtime."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[3]
CONTRACT = 'research/round28/contracts/ak1.json'
CONTRACT_SHA = '2afd1ff408b4774e79f1964f796835c6e4088cce22de5c1c66c85d796c9a9810'
ZERO = (0, 0, 0)
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
STAR = (ZERO,) + AXES
R = {ZERO, AXES[2]}
INNER = {(1, 1, 1), (1, 1, 2)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_read(rel):
    path = ROOT / rel
    require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,
            'nonportable path: ' + rel)
    require(OWN == path or OWN in path.parents, 'runtime read outside owned closure')
    for item in (path,) + tuple(path.parents):
        if item == ROOT:
            break
        require(not item.is_symlink(), 'symlink in runtime path')
    return path


def source_bindings():
    invpath = OWN / 'inputs/source-inventory.json'
    inv = json.loads(invpath.read_text())
    entries = inv['entries']
    bindings = {}
    originals = {}
    snapshots = set()
    for entry in entries:
        snap = entry['snapshot']
        path = local_read(snap)
        require(snap not in snapshots, 'duplicate snapshot')
        snapshots.add(snap)
        sha = digest(path)
        require(sha == entry['sha256'], 'snapshot changed: ' + snap)
        bindings[snap] = sha
        if entry.get('external_instruction_snapshot'):
            require(Path(entry['source']).is_absolute(), 'external provenance missing')
        else:
            source = entry['source']
            require(not Path(source).is_absolute() and '..' not in Path(source).parts,
                    'nonportable original binding')
            require(source not in originals, 'duplicate source')
            originals[source] = (sha, snap)
            bindings[source] = sha
    require(CONTRACT in originals, 'contract snapshot missing')
    csha, cpath = originals[CONTRACT]
    require(csha == CONTRACT_SHA == inv['contract_sha256'], 'contract mismatch')
    contract = json.loads(local_read(cpath).read_text())
    require(len(contract['sources']) == 43, 'wrong required source count')
    for source, expected in contract['sources'].items():
        require(source in originals and originals[source][0] == expected,
                'required original/snapshot mismatch: ' + source)
    require(contract['loop'] == 'ak1' and contract['sequence'] == 9,
            'wrong investigation')
    freeze_path = OWN / 'inputs/freeze.json'
    frozen = json.loads(freeze_path.read_text())['files']
    actual = {str(p.relative_to(ROOT)) for p in (OWN / 'inputs').rglob('*')
              if p.is_file() and p != freeze_path}
    require(set(frozen) == actual, 'input closure differs from input freeze')
    for name, sha in frozen.items():
        require(digest(local_read(name)) == sha, 'frozen input changed: ' + name)
        bindings[name] = sha
    for p in (invpath, freeze_path, OWN / 'report.md', OWN / 'source-reading.json',
              Path(__file__).resolve()):
        bindings[str(p.relative_to(ROOT))] = digest(p)
    require(all(not Path(k).is_absolute() for k in bindings), 'absolute binding')
    return dict(sorted(bindings.items())), contract


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def owner(tail):
    x, y, z = tail
    return x // 4, y // 2, z


def tails(site):
    x, y, z = site
    return {(4*x + r, 2*y + s, z) for r in range(4) for s in range(2)}


def links(region):
    return {(tail, axis) for site in region for tail in tails(site)
            for axis in range(3)}


def head(link):
    return add(link[0], AXES[link[1]])


def endpoints(linkset):
    return {v for e in linkset for v in (e[0], head(e))}


def word(p, a, c):
    return (((p, a), 1), ((add(p, AXES[a]), c), 1),
            ((add(p, AXES[c]), a), -1), ((p, c), -1))


def all_faces(site):
    return [(p, a, c, word(p, a, c)) for p in sorted(tails(site))
            for a, c in combinations(range(3), 2)]


def selected(face):
    p, a, c, _ = face
    return (a, c) == (0, 1) and p[0] % 4 < 3 and p[1] % 2 == 0


def omitted(site):
    return [face for face in all_faces(site) if not selected(face)]


def support(face):
    return {owner(link[0]) for link, sign in face[3]}


def orthant_incident(region):
    return {sub(r, s) for r in region for s in STAR if min(sub(r, s)) >= 0}


def retained(volume):
    return {b for b in volume if {add(b, s) for s in STAR} <= volume}


def geometry(contract):
    selected_links = {link for b in R for face in all_faces(b) if selected(face)
                      for link, sign in face[3]}
    local = links(R)
    verts = endpoints(local)
    face = word(ZERO, 0, 2)
    require({owner(e[0]) for e, sign in face} == R, 'Wilson owner cover')
    require(len(local) == 48 and len(verts) == 36, 'full local factor/endpoints')
    require(len(selected_links) == 20 and len(local-selected_links) == 28,
            'selected/free split')
    require((ZERO, 2) in local-selected_links, 'conditioning link is not free')
    require(len({e for e, sign in face}) == 4, 'Wilson links not distinct')
    walked = ZERO
    for e, sign in face:
        start, end = (e[0], head(e)) if sign == 1 else (head(e), e[0])
        require(start == walked, 'broken oriented path')
        walked = end
    require(walked == ZERO, 'Wilson path not closed')
    classes = Counter(tuple(sorted(support(f))) for f in omitted(ZERO))
    expected = {tuple(sorted(k)): n for k, n in [
        ({ZERO, AXES[0]}, 1), ({ZERO, AXES[1]}, 3),
        ({ZERO, AXES[0], AXES[1]}, 1), ({ZERO, AXES[2]}, 10),
        ({ZERO, AXES[0], AXES[2]}, 2), ({ZERO, AXES[1], AXES[2]}, 4)]}
    require(dict(classes) == expected and sum(classes.values()) == 21,
            'complete omitted face multiplicities')
    require(set().union(*(support(f) for f in omitted(ZERO))) == set(STAR),
            'four-site star union')
    require(orthant_incident(R) == R, 'origin all-volume incidence')
    require(len(orthant_incident(INNER)) == 7, 'interior all-volume incidence')
    rows = []
    for sides in contract['parameters']['geometry_fixtures']['cuboid_side_counts']:
        volume = set(product(*(range(n) for n in sides)))
        anchors = retained(volume)
        complete = links(volume)
        require(len(complete) == 24*len(volume), 'unique full link ownership')
        require(all(owner(e[0]) in volume for e in complete), 'tail ownership')
        all_words = [f for b in anchors for f in omitted(b)]
        require(len(all_words) == 21*len(anchors), 'complete 21-face groups')
        require(all({e for e, sign in f[3]} <= complete for f in all_words),
                'retained word has unowned link')
        incident = {b for b in anchors if {add(b, s) for s in STAR} & R}
        inverse = orthant_incident(R) & anchors
        require(incident == inverse, 'direct versus inverse origin incidence')
        n = sides[0]
        require(len(complete) == 24*n**3 and len(endpoints(complete)) == 8*n**3+14*n*n,
                'analytic cuboid counts')
        require(len(anchors) == (n-1)**3 and len(incident) == (1 if n == 2 else 2),
                'cuboid full-star incidence')
        inner = None
        if INNER <= volume:
            ii = {b for b in anchors if {add(b, s) for s in STAR} & INNER}
            require(ii == orthant_incident(INNER) & anchors, 'interior inverse incidence')
            require(len(ii) == (4 if n == 3 else 7), 'interior retained groups')
            outgoing_only = anchors & INNER
            require(len(outgoing_only) < len(ii), 'interior dropped-group control blind')
            inner = {'anchors': sorted(ii), 'count': len(ii),
                     'outgoing_only_count': len(outgoing_only), 'wrong_rule_rejected': True}
        rows.append({'sides': sides, 'sites': len(volume), 'links': len(complete),
                     'endpoints': len(endpoints(complete)), 'retained_stars': len(anchors),
                     'retained_omitted_faces': len(all_words), 'origin_anchors': sorted(incident),
                     'origin_charged_group_faces': 21*len(incident),
                     'origin_energy_coefficient_times_abs_tau': 14*len(incident),
                     'interior': inner})
    return {'region': sorted(R), 'wilson_word': face, 'links': sorted(local),
            'endpoint_vertices': sorted(verts), 'selected_links': sorted(selected_links),
            'free_links': sorted(local-selected_links),
            'support_multiplicities': [{'support': s, 'count': n} for s, n in sorted(classes.items())],
            'orthant_incident_anchors': sorted(orthant_incident(R)), 'fixtures': rows,
            'origin_outgoing_only_control': {'status': 'nondiscriminating_retained',
                'true_count': 2, 'wrong_rule_count': 2,
                'replacement': 'interior fixtures detect missing incoming groups'}}


def qmul(a, b):
    w, x, y, z = a
    v, i, j, k = b
    return (w*v-x*i-y*j-z*k, w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i, w*k+x*j-y*i+z*v)


def qinv(q):
    return (q[0], -q[1], -q[2], -q[3])


def holonomy(values, face):
    out = (F(1), F(0), F(0), F(0))
    for e, sign in face:
        out = qmul(out, values[e] if sign == 1 else qinv(values[e]))
    return out


def covariance():
    pool = [(F(3,5),F(4,5),F(0),F(0)), (F(5,13),F(0),F(12,13),F(0)),
            (F(8,17),F(0),F(0),F(15,17)), (F(1,2),)*4,
            (F(0),F(0),F(1),F(0))]
    require(all(sum(x*x for x in q) == 1 for q in pool), 'nonunit quaternion')
    es = sorted(links(R)); vs = sorted(endpoints(es)); face = word(ZERO, 0, 2)
    values = {e: pool[(i*3+1) % len(pool)] for i, e in enumerate(es)}
    raw = holonomy(values, face)
    attempts = []
    for shift in range(len(pool)):
        gauges = {v: pool[(i*2+shift) % len(pool)] for i, v in enumerate(vs)}
        moved = {e: qmul(qmul(gauges[e[0]], values[e]), qinv(gauges[head(e)])) for e in es}
        wrong = {e: qmul(gauges[e[0]], values[e]) for e in es}
        correct = holonomy(moved, face)
        require(correct == qmul(qmul(gauges[ZERO], raw), qinv(gauges[ZERO])),
                'full endpoint covariance fails')
        bad_value = holonomy(wrong, face)[0]
        attempts.append({'shift': shift, 'wilson': raw[0], 'full_action': correct[0],
                         'head_dropped': bad_value, 'discriminates': bad_value != raw[0]})
        if bad_value != raw[0]:
            break
    require(attempts[-1]['discriminates'], 'all missing-head candidates blind')
    # Conditional scalar coefficients of A u^-1 retain an actual original link.
    coefficients = []
    for i in range(4):
        varied = dict(values)
        varied[(ZERO, 2)] = tuple(F(int(j == i)) for j in range(4))
        coefficients.append(holonomy(varied, face)[0])
    require(sum(x*x for x in coefficients) == 1, 'conditional Haar coefficient norm')
    return {'attempts': attempts, 'conditional_link': (ZERO, 2),
            'conditional_coefficients': coefficients,
            'reference_mean': F(0), 'reference_second_moment': F(1,4)}


def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def trace_square(a):
    return sum(a[i][j]*a[j][i] for i in range(2) for j in range(2))


def arithmetic():
    tau_cap = F(1, 65536)
    energy = 2*7*len(orthant_incident(R))*tau_cap
    d_ceiling = F(1,24)
    sufficient_overlap = (d_ceiling/2)**2
    floor = F(1,4)-d_ceiling-d_ceiling**2
    require(energy == F(7,16384) < sufficient_overlap == F(1,2304), 'overlap budget fails')
    require(4*energy < d_ceiling**2 and floor == F(119,576) > F(1,5), 'variance target fails')
    truth = []
    for a, b in product((0,1), repeat=2):
        sum_gap = (1-a)+(1-b)
        product_gap = 1-a*b
        require(sum_gap-product_gap == (1-a)*(1-b) >= 0, 'product projector inequality')
        truth.append({'p0': a, 'p1': b, 'sum_gap': sum_gap, 'product_gap': product_gap})
    rho = [[F(17,25),F(6,25)],[F(6,25),F(8,25)]]
    difference = [[rho[0][0]-1,rho[0][1]],[rho[1][0],rho[1][1]]]
    eps = 1-rho[0][0]
    trace_norm_squared = -4*det2(difference)
    require(rho[0][0]+rho[1][1] == 1 and det2(rho) == F(4,25), 'density positivity/trace')
    require(trace_square(rho) == F(17,25) < 1, 'mixed density accidentally pure')
    require(trace_norm_squared == F(16,25) < 4*eps, 'mixed distance bound')
    require(trace_norm_squared > eps, 'missing factor control blind')
    require(trace_norm_squared > (2*eps)**2, 'missing square root control blind')
    require(trace_norm_squared != 4*eps, 'pure equality imposed on mixed density')
    pure = [[F(9,25),F(12,25)],[F(12,25),F(16,25)]]
    pure_difference = [[pure[0][0]-1,pure[0][1]],[pure[1][0],pure[1][1]]]
    require(det2(pure) == 0 and trace_square(pure) == 1, 'pure control malformed')
    require(-4*det2(pure_difference) == 4*(1-pure[0][0]), 'pure endpoint equality')
    m, second = F(1,4), F(1,4)
    tilted_variance = second-m*m
    require(tilted_variance == F(3,16) < F(1,5) < second, 'uncharged mean control blind')
    band_half_width = F(1,4)
    band_mass_upper = 2*band_half_width  # analytic 2/pi < 1
    require(band_half_width**2 == F(1,16) < F(1,5), 'concentration upper bound')
    require(1-band_mass_upper > energy, 'concentration not excluded by overlap premise')
    alpha, ground, shift = F(24), F(-6), F(11)
    delta = alpha/8
    raw = [ground, ground+delta]
    normalized = [(x-ground)/delta for x in raw]
    shifted = [(x+shift-(ground+shift))/delta for x in raw]
    require(normalized == shifted == [0,1], 'reference centering changes under scalar shift')
    require(raw[0]/delta == -2 != 0, 'missing ground center control blind')
    defect = F(1,32)
    wrong_scaled_energy = defect*(raw[1]-ground)/alpha
    require(wrong_scaled_energy == F(1,256) < defect, 'wrong scale fails to challenge projector')
    hypothetical_c1, hypothetical_c2 = F(1,2**20), F(1)
    possible_radius = min(hypothetical_c1, 1/(2*hypothetical_c2))/7
    require(0 < possible_radius < tau_cap, 'additional cap/stability distinction blind')
    return {'tau_extra_cap': tau_cap, 'actual_state_requires_symbolic_tau_star': True,
            'tau_star_evaluated': False, 'chosen_positive_admissible_tau': None,
            'incident_groups': 2, 'reference_energy_ceiling': energy,
            'sufficient_overlap_defect': sufficient_overlap, 'trace_norm_ceiling': d_ceiling,
            'second_moment_floor': F(1,4)-d_ceiling,
            'actual_mean_absolute_ceiling': d_ceiling, 'charged_mean_square': d_ceiling**2,
            'variance_floor': floor, 'margin_over_target': floor-F(1,5),
            'product_projector_sectors': truth,
            'mixed_density_control': {'rho': rho, 'purity': trace_square(rho), 'epsilon': eps,
                'trace_norm_squared': trace_norm_squared, 'valid_ceiling_squared': 4*eps,
                'missing_factor_rejected': True, 'missing_root_rejected': True,
                'pure_equality_rejected': True, 'pure_saturation_checked': True},
            'tilted_normal_state': {'normalization': 1, 'mean': m, 'second_moment': second,
                'variance': tilted_variance, 'discarded_mean_would_falsely_pass': True,
                'haar_variance_substitution_rejected': True},
            'concentrating_normal_state': {'band_half_width': band_half_width,
                'strict_variance_upper_bound': band_half_width**2,
                'reference_overlap_upper_bound': band_mass_upper,
                'reference_energy_lower_bound': 1-band_mass_upper,
                'finite_energy_not_asserted': True, 'actual_energy_premise_excludes_it': True},
            'reference_scalar_and_scale': {'alpha': alpha, 'delta': delta, 'ground': ground,
                'normalized': normalized, 'after_joint_scalar_shift': shifted,
                'uncentered_vacuum': raw[0]/delta, 'defect': defect,
                'wrong_alpha_scaled_energy': wrong_scaled_energy},
            'cap_control': {'status': 'abstract_possible_constants_only',
                'c1': hypothetical_c1, 'c2': hypothetical_c2,
                'possible_tau_star': possible_radius, 'extra_cap_is_not_stability_radius': True}}


def serialize(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    require(output.is_absolute() and not output.exists(), 'output must be absolute and fresh')
    bindings, contract = source_bindings()
    result = {'schema': 'ym28-ak1-reverse-results-v1', 'loop': 'ak1', 'sequence': 9,
              'passed': True, 'bindings': bindings, 'geometry': geometry(contract),
              'covariance': covariance(), 'certificate': arithmetic(),
              'scope': {'actual_homogeneous_variance_target_supported': True,
                        'physical_first_moment_proved': False, 'operator_domain_proved': False,
                        'spectral_window_proved': False, 'continuum_claim': False,
                        'opposite_current_science_read': False}}
    output.mkdir(parents=True, exist_ok=False)
    (output/'results.json').write_text(json.dumps(result, default=serialize, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'passed': True, 'result_sha256': digest(output/'results.json'),
                      'variance_floor': str(result['certificate']['variance_floor'])}, sort_keys=True))


if __name__ == '__main__':
    main()
