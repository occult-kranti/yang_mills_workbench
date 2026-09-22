#!/usr/bin/env python3
"""Additive AK1 post-exchange audit; independent exact arithmetic, owned snapshots."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product, combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'research/round28/'
PACK = HERE / 'ak1-post-review-inputs'
INVENTORY_SHA = 'ed0053e52d8d297a03121bc317000de9be530999d8777eb6f692ad1e36e38732'
CONTRACT_SHA = '2afd1ff408b4774e79f1964f796835c6e4088cce22de5c1c66c85d796c9a9810'
FREEZES = {'forward': '75fb5ec51c63e3264350be3236fa9dd3067c3a425381fb978bda126dc9e40ecd',
           'reverse': 'c6810b72b2fef46cbab574d32ad205f4daccdc1c1267dc49774366df0ddbd588'}
CHECKS = []
BINDINGS = {}
SOURCES = {}


def require(ok, name):
    if not ok:
        raise ValueError(name)
    CHECKS.append({'name': name, 'passed': True})


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def safe(rel):
    require(isinstance(rel, str) and not Path(rel).is_absolute() and '..' not in Path(rel).parts,
            'safe relative path: ' + str(rel))
    p = ROOT / rel
    require(all(not q.is_symlink() for q in (p,) + tuple(p.parents) if q != ROOT),
            'no symlink: ' + rel)
    return p


def data(source):
    return json.loads(SOURCES[source]['path'].read_text())


def sources():
    invp = PACK / 'source-inventory.json'
    require(sha(invp) == INVENTORY_SHA, 'immutable post-review inventory')
    inv = json.loads(invp.read_text())
    declared = set()
    for entry in inv['entries']:
        origin, snap, expected = entry['source'], entry['snapshot'], entry['sha256']
        p = safe(snap)
        require(PACK in p.parents and p.is_file(), 'owned snapshot: ' + origin)
        require(origin not in SOURCES and snap not in declared, 'unique source/snapshot: ' + origin)
        require(sha(p) == expected, 'snapshot bytes: ' + origin)
        safe(origin)  # Validate metadata only; original files are not read.
        SOURCES[origin] = {'path': p, 'sha256': expected}
        declared.add(snap)
        BINDINGS.update({origin: expected, snap: expected})
    actual = {str(p.relative_to(ROOT)) for p in PACK.rglob('*') if p.is_file() and p != invp}
    require(actual == declared, 'exact owned snapshot set')
    BINDINGS[str(invp.relative_to(ROOT))] = sha(invp)
    for p in [Path(__file__).resolve(), HERE / 'ak1-post-review.md']:
        BINDINGS[str(p.relative_to(ROOT))] = sha(p)
    c = PREFIX + 'contracts/ak1.json'
    require(SOURCES[c]['sha256'] == CONTRACT_SHA, 'contract identity')
    contract = data(c)
    require(contract['sequence'] == 9 and len(contract['sources']) == 43, 'ninth frozen contract')
    for rel, expected in contract['sources'].items():
        require(SOURCES[rel]['sha256'] == expected, 'contract source: ' + rel)
    for side, freeze_sha in FREEZES.items():
        base = PREFIX + side + '/ak1/'
        freeze = base + 'freeze.json'
        require(SOURCES[freeze]['sha256'] == freeze_sha, 'original producer freeze: ' + side)
        fs = data(freeze)['files']
        expected = {p for p in SOURCES if p.startswith(base) and p != freeze}
        require(set(fs) == expected and len(fs) == (85 if side == 'forward' else 65),
                'exact repo-relative producer closure: ' + side)
        for rel, digest in fs.items():
            require(rel.startswith(base) and SOURCES[rel]['sha256'] == digest,
                    'producer frozen byte: ' + rel)
        output = data(base + 'output/results.json')
        require(output['passed'] is True, 'producer result passed: ' + side)
        for rel, digest in output['bindings'].items():
            require(rel in SOURCES and SOURCES[rel]['sha256'] == digest,
                    'producer runtime binding: ' + side + ':' + rel)
    indep = PREFIX + 'skeptic/ak1-independent-freeze.json'
    require(SOURCES[indep]['sha256'] == '1296a0116c3f756bcad564dca5f9553d5eee397dfd11a507c0ea05886aa87bc0',
            'independent pre-exchange freeze identity')
    frozen = data(indep)
    require(len(frozen['bindings']) == 72 and frozen['current_producer_science_read'] is False,
            'independent 72-file closure predates exchange')
    for rel, digest in frozen['bindings'].items():
        require(SOURCES[rel]['sha256'] == digest, 'independent frozen byte: ' + rel)
    replay = data(PREFIX + 'skeptic/ak1-post-producer-replay.json')
    require(replay['all_fresh_normal_optimized_exact_outputs_equal'] is True and len(replay['runs']) == 4,
            'four fresh full-output replays')
    require({(r['direction'], r['mode']) for r in replay['runs']} == set(product(FREEZES, ('normal', 'optimized'))),
            'both producer execution modes present')
    for r in replay['runs']:
        expected = {'results.json': SOURCES[PREFIX + r['direction'] + '/ak1/output/results.json']['sha256']}
        require(r['files'] == r['frozen_files'] == expected and r['exit_code'] == 0
                and r['fresh_absolute_directory'] is True and r['exact_output_set_and_bytes_equal'] is True,
                'complete replay bytes: ' + r['direction'] + ':' + r['mode'])
        script = r['command'][3 if r['mode'] == 'optimized' else 2]
        require(Path(script).is_absolute(), 'absolute replay entrypoint: ' + r['direction'] + ':' + r['mode'])


def frac(x):
    return F(x['numerator'], x['denominator']) if isinstance(x, dict) else F(x)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


O = (0, 0, 0)
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
STAR = (O,) + E
REGION = {O, E[2]}
INTERIOR = {(1, 1, 1), (1, 1, 2)}


def faces(b):
    out = []
    for i, j in product(range(4), range(2)):
        p = (4*b[0]+i, 2*b[1]+j, b[2])
        for a, c in combinations(range(3), 2):
            if (a, c) == (0, 1) and i < 3 and j == 0:
                continue
            tails = [p, add(p, E[a]), add(p, E[c]), p]
            support = {(x//4, y//2, z) for x, y, z in tails}
            out.append(support)
    return out


def compare():
    f = data(PREFIX + 'forward/ak1/output/results.json')
    r = data(PREFIX + 'reverse/ak1/output/results.json')
    s = data(PREFIX + 'skeptic/ak1-independent.json')
    fg, rg, sg = f['geometry'], r['geometry'], s['geometry']
    for key, fk, rk in [('region','region','region'), ('links','original_links','links'),
                       ('selected_links','selected_links','selected_links'), ('free_links','free_links','free_links'),
                       ('incident_orthant_anchors','orthant_incident_anchors','orthant_incident_anchors')]:
        require(sg[key] == fg[fk] == rg[rk], 'three-way exact geometry: ' + key)
    require(sg['endpoints'] == rg['endpoint_vertices'] == [a['vertex'] for a in fg['endpoint_actions']],
            'all 36 endpoint vertices agree')
    reverse_word = [[link[0], link[1], sign] for link, sign in rg['wilson_word']]
    require(sg['face'] == fg['original_word'] == reverse_word, 'actual original oriented Wilson word')
    require(len(sg['links']) == 48 and len(sg['endpoints']) == 36
            and len(sg['selected_links']) == 20 and len(sg['free_links']) == 28, 'complete local factor')
    rows = []
    for n, ff, rr, ss in zip((2, 3, 4), fg['cuboids'], rg['fixtures'], sg['cuboid_fixtures']):
        volume = set(product(range(n), repeat=3))
        anchors = {b for b in volume if {add(b, t) for t in STAR} <= volume}
        incident = {b for b in anchors if {add(b, t) for t in STAR} & REGION}
        require(ff['retained_stars'] == rr['retained_stars'] == ss['whole_star_count'] == len(anchors),
                'independent complete stars: ' + str(n))
        require(sorted(incident) == [tuple(b) for b in ff['target_anchors']]
                == [tuple(b) for b in rr['origin_anchors']]
                == [tuple(b) for b in ss['regions'][0]['incident_anchors']], 'three-way incident anchors: ' + str(n))
        origin_touching = sum(bool(face & REGION) for b in anchors for face in faces(b))
        require(origin_touching == 21*len(incident) == ff['actually_touching_faces'], 'origin face control blind: ' + str(n))
        row = {'side': n, 'stars': len(anchors), 'origin_groups': len(incident), 'origin_touching_faces': origin_touching}
        if INTERIOR <= volume:
            inner = {b for b in anchors if {add(b, t) for t in STAR} & INTERIOR}
            touching = sum(bool(face & INTERIOR) for b in anchors for face in faces(b))
            outgoing = len(anchors & INTERIOR)
            require(sorted(inner) == [tuple(b) for b in ff['interior']['anchors']]
                    == [tuple(b) for b in rr['interior']['anchors']]
                    == [tuple(b) for b in ss['regions'][1]['incident_anchors']], 'three-way interior anchors: ' + str(n))
            require((len(inner), outgoing, touching) == ((4, 1, 49) if n == 3 else (7, 2, 82)),
                    'independently reconstructed discriminating incidence: ' + str(n))
            require(touching == ff['interior']['actually_touching_faces'] < 21*len(inner),
                    'face counts do not replace inherited group counts: ' + str(n))
            row.update(interior_groups=len(inner), outgoing_only=outgoing, whole_group_faces=21*len(inner), individually_touching_faces=touching)
        rows.append(row)
    fq, rq, sq = f['quantitative'], r['certificate'], s['certificate_and_controls']
    for fk, rk, sk, expected in [
        ('cap','tau_extra_cap','cap',F(1,65536)),
        ('energy_ceiling','reference_energy_ceiling','energy_and_deficit_cap',F(7,16384)),
        ('trace_distance_ceiling','trace_norm_ceiling','full_trace_norm_ceiling',F(1,24)),
        ('actual_mean_absolute_ceiling','actual_mean_absolute_ceiling','mean_absolute_ceiling',F(1,24)),
        ('actual_second_moment_lower','second_moment_floor','conservative_second_moment_floor',F(5,24)),
        ('actual_variance_lower','variance_floor','conservative_variance_floor',F(119,576)),
        ('target_margin','margin_over_target','conservative_margin',F(19,2880))]:
        require(frac(fq[fk]) == frac(rq[rk]) == frac(sq[sk]) == expected, 'three-way exact certificate: ' + fk)
    cap, t = F(1,65536), F(1,24)
    require(28*cap == F(7,16384) and 4*28*cap < t*t, 'independent energy to trace ceiling')
    require(F(1,4)-t-t*t == F(119,576) > F(1,5), 'independent common charged-mean bound')
    require(F(1,4)-t/2-t*t == frac(sq['refined_variance_floor']) == F(131,576), 'independent effect refinement arithmetic')
    require(frac(sq['refined_margin']) == F(131,576)-F(1,5) == F(79,2880), 'independent refined margin')
    require(fq['numerical_stability_interval_evaluated'] is False and rq['tau_star_evaluated'] is False
            and fq['selected_positive_admissible_tau'] is None and rq['chosen_positive_admissible_tau'] is None,
            'conditional symbolic stability scope preserved')
    require(s['current_producer_science_read'] is False and s['ak2_selected_or_executed'] is False,
            'independent result is pre-exchange and excludes AK2')
    require(len(f['checks']) == f['check_count'] == 69 and all(c['passed'] is True for c in f['checks']),
            'all 69 published forward named checks')
    require(rg['origin_outgoing_only_control']['status'] == 'nondiscriminating_retained'
            and len(f['controls_with_blind_candidates']) == 2, 'original blind controls remain disclosed')
    for control in (fq['tilted_normal_control'], rq['tilted_normal_state']):
        require(frac(control['mean']) == F(1,4) and frac(control['variance']) == F(3,16),
                'tilted normal control differs from Haar variance')
    require(frac(fq['tilted_normal_control']['energy_lower']) == F(1,64) > 28*cap,
            'tilted normal control excluded by actual excitation cap')
    require(F(1,16) < F(1,5) and F(1,2) > 28*cap, 'band control excluded without finite-energy claim')
    reverse_reading = data(PREFIX + 'reverse/ak1/source-reading.json')
    require('focused' in reverse_reading['manuscript_reading_limitation'], 'reverse source-reading limitation retained')
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    if not out.is_absolute() or out.exists():
        raise ValueError('--output must be a fresh absolute file')
    sources()
    rows = compare()
    result = {'schema': 'ym28-ak1-post-review-v1', 'loop': 'ak1', 'sequence': 9,
              'passed': True, 'check_count': len(CHECKS), 'checks': CHECKS, 'bindings': dict(sorted(BINDINGS.items())),
              'supported': {'actual_origin_variance_at_least_one_fifth': True,
                'common_producer_lower_bound': '119/576', 'independent_skeptic_effect_lower_bound': '131/576',
                'interacting_variance_evaluated': False, 'lower_bounds_optimal': False,
                'full_mixed_trace_norm_bound_proved': True, 'unknown_mean_squared_charged': True,
                'requires_unevaluated_symbolic_tau_star': True, 'extra_cap': '1/65536',
                'numeric_stability_radius_evaluated': False, 'positive_numeric_admissible_tau_selected': False,
                'local_reference_energy_only': True, 'physical_excited_vector_energy_moment_or_domain': False,
                'spectral_window_or_AK2_science': False, 'all_translated_regions_covered': False,
                'finer_face_decomposition_universally_forbidden': False,
                'full_producer_reports_and_checkers_read': True, 'reading_depths_differ_and_are_disclosed': True,
                'all_full_output_normal_optimized_replays_equal': True, 'all_independent_files_unchanged': True,
                'new_external_primary_retrievals': 0, 'new_research_loops': 0,
                'continuum_mass_gap_or_percentage': False, 'scientific_priority_verified': False},
              'incidence_comparison': rows, 'blocking_objections': [],
              'final_admission_spec_review': 'pending root-approved specification'}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'passed': True, 'check_count': len(CHECKS), 'sha256': sha(out)}))


if __name__ == '__main__':
    main()
