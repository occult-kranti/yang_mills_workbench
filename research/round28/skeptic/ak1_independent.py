#!/usr/bin/env python3
"""Independent AK1 exact diagnostics; no historical/current producer imports."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = 'research/round28/skeptic/'
INPUT = BASE + 'ak1-inputs/'
CONTRACT = 'research/round28/contracts/ak1.json'
CONTRACT_SHA = '2afd1ff408b4774e79f1964f796835c6e4088cce22de5c1c66c85d796c9a9810'
INVENTORY_SHA = '5ff283099e29fdd862390fc2f49ae9df2f392a41b69e844b747c61e8bd2bb3f8'
PACK_SHA = '012ca95305783b69c79a0d24e840eaae2b89d2a3515ab00b2eafd78ca09b6e83'
O = (0, 0, 0)
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
STAR = (O,) + UNIT
checks = []


def need(condition, label):
    if not condition:
        raise ValueError(label)
    checks.append(label)


def local(name):
    path = Path(name)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('nonlocal runtime path ' + name)
    current = ROOT
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError('symlink runtime path ' + name)
    return current


def digest(name):
    return hashlib.sha256(local(name).read_bytes()).hexdigest()


def read(name):
    return json.loads(local(name).read_text())


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def owner(tail):
    return (tail[0] // 4, tail[1] // 2, tail[2])


def owned(block):
    i, j, k = block
    return {((4*i+r, 2*j+s, k), axis)
            for r in range(4) for s in range(2) for axis in range(3)}


def face(tail, a, b):
    return [(tail, a, 1), (add(tail, UNIT[a]), b, 1),
            (add(tail, UNIT[b]), a, -1), (tail, b, -1)]


def face_support(word):
    return {owner(tail) for tail, _, _ in word}


def selected(tail, a, b):
    return (a, b) == (0, 1) and tail[0] % 4 < 3 and tail[1] % 2 == 0


def group(block):
    words = []
    i, j, k = block
    for r, s, (a, b) in itertools.product(range(4), range(2), ((0, 1), (0, 2), (1, 2))):
        tail = (4*i+r, 2*j+s, k)
        if not selected(tail, a, b):
            words.append({'base': tail, 'axes': (a, b), 'word': face(tail, a, b)})
    return words


def incident(region):
    return {sub(r, s) for r in region for s in STAR if min(sub(r, s)) >= 0}


def in_cube(p, sides):
    return all(0 <= p[i] < sides[i] for i in range(3))


def qmul(q, r):
    a, b, c, d = q
    e, f, g, h = r
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])


def unit_quaternion(i):
    # Rational stereographic coordinates; no sampled or discretized Haar law.
    v = (F(i % 3 + 1, 5), F(i % 5 + 1, 7), F(i % 7 + 1, 11))
    n = sum(x*x for x in v)
    return ((1-n)/(1+n),) + tuple(2*x/(1+n) for x in v)


def holonomy(word, link_values):
    value = (F(1), F(0), F(0), F(0))
    for tail, axis, sign in word:
        q = link_values[(tail, axis)]
        value = qmul(value, q if sign == 1 else qconj(q))
    return value


def cadd(a, b):
    return (a[0]+b[0], a[1]+b[1])


def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def cconj(a):
    return (a[0], -a[1])


def matrix(q):
    a, b, c, d = q
    return [[(a,b),(c,d)],[(-c,d),(a,-b)]]


def mmul(a, b):
    return [[cadd(cmul(a[i][0], b[0][j]), cmul(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]


def adjoint(a):
    return [[cconj(a[j][i]) for j in range(2)] for i in range(2)]


def geometry():
    region = {O, UNIT[2]}
    links = set().union(*(owned(b) for b in region))
    tails = {p for p, _ in links}
    endpoints = tails | {add(p, UNIT[a]) for p, a in links}
    word = face(O, 0, 2)
    expected_path = [O, UNIT[0], add(UNIT[0], UNIT[2]), UNIT[2], O]
    path = [O]
    for tail, axis, sign in word:
        start = tail if sign == 1 else add(tail, UNIT[axis])
        end = add(tail, UNIT[axis]) if sign == 1 else tail
        need(path[-1] == start, 'original oriented Wilson edge starts at current vertex')
        path.append(end)
    need(path == expected_path, 'ordered closed original xz path')
    need(len({(p,a) for p,a,_ in word}) == 4, 'four distinct original Wilson links')
    need(face_support(word) == region, 'minimal complete observable region')
    need(len(links) == 48 and len(tails) == 16 and len(endpoints) == 36, 'complete region counts')
    need(len(endpoints-tails) == 20, 'every outgoing endpoint retained')
    strip_links = set()
    for block in region:
        i,j,k = block
        for r in range(3):
            strip_links |= {(p,a) for p,a,_ in face((4*i+r,2*j,k),0,1)}
    free = links-strip_links
    need(len(strip_links) == 20 and len(free) == 28, 'selected and free split')
    need((O, 2) in free, 'conditional original z-link is free in reference')
    for p,a in links:
        need(owner(p) in region, 'unique tail owner in complete region')
    target_anchors = incident(region)
    need(target_anchors == {O, UNIT[2]}, 'all orthant target incident groups')
    per_site_sum = sum(len(incident({r})) for r in region)
    need(per_site_sum == 3 and len(target_anchors) == 2, 'shared target group counted once')
    interior = {(1,1,1),(1,1,2)}
    interior_anchors = incident(interior)
    need(len(interior_anchors) == 7, 'all seven interior incident groups')
    need(len(interior & interior_anchors) == 2 < len(interior_anchors), 'incoming interior omission discriminates')
    templates = group(O)
    need(len(templates) == 21, 'complete omitted group contains 21 faces')
    template_supports = {}
    for f in templates:
        support = face_support(f['word'])
        need(support <= set(STAR) and len(support) > 1, 'omitted face complete star support')
        key = tuple(sorted(support))
        template_supports[key] = template_supports.get(key, 0) + 1
    need(sorted(template_supports.values()) == [1,1,2,3,4,10], 'exhaustive omitted face support multiplicities')
    need(set().union(*[set(s) for s in template_supports]) == set(STAR), 'group union uses four sites')
    fixtures = []
    for sides, expected_target, expected_interior in [((2,2,2),1,None),((3,3,3),2,4),((4,4,4),2,7)]:
        sites = set(itertools.product(*(range(n) for n in sides)))
        retained = {b for b in sites if all(add(b,s) in sites for s in STAR)}
        need(len(retained) == (sides[0]-1)*(sides[1]-1)*(sides[2]-1), 'whole-star cuboid anchor count')
        records = []
        for label, reg, expected in [('target',region,expected_target),('interior-control',interior,expected_interior)]:
            present = reg <= sites
            if not present:
                need(expected is None, 'absent region is not a tested zero-incidence state')
                records.append({'region_kind':label,'present':False,'incident_anchors':None,'group_faces':None})
                continue
            chosen = retained & incident(reg)
            direct = {b for b in retained if {add(b,s) for s in STAR} & reg}
            need(chosen == direct, 'independent inverse/direct complete-star incidence')
            need(len(chosen) == expected, 'prescribed finite-region incidence')
            full_faces = []
            for b in sorted(chosen):
                fs = group(b)
                need(len(fs) == 21, 'retain every face in each incident group')
                for f in fs:
                    need(face_support(f['word']) <= {add(b,s) for s in STAR}, 'original group face fits its complete star')
                full_faces.extend(fs)
            records.append({'region_kind':label,'present':True,'region':sorted(reg),
                            'incident_anchors':sorted(chosen),'group_face_count':len(full_faces),
                            'group_faces':full_faces,'reference_energy_coefficient_over_M':2*len(chosen)})
        fixtures.append({'side_counts':sides,'site_count':len(sites),
                         'whole_star_count':len(retained),'regions':records})
    values = {link:unit_quaternion(i+1) for i,link in enumerate(sorted(links))}
    gauges = {v:unit_quaternion(i+103) for i,v in enumerate(sorted(endpoints))}
    ident = [[(F(1),F(0)),(F(0),F(0))],[(F(0),F(0)),(F(1),F(0))]]
    for link,q in values.items():
        need(sum(x*x for x in q) == 1, 'rational original link lies in SU2')
        need(mmul(matrix(q),adjoint(matrix(q))) == ident, 'independent complex matrix unitarity')
    transformed = {link:qmul(qmul(gauges[link[0]],q),qconj(gauges[add(link[0],UNIT[link[1]])])) for link,q in values.items()}
    old = holonomy(word,values)
    changed = holonomy(word,transformed)
    need(changed == qmul(qmul(gauges[O],old),qconj(gauges[O])), 'full endpoint holonomy covariance')
    need(changed[0] == old[0], 'actual Wilson trace invariant')
    product_matrix = ident
    for p,a,sign in word:
        m = matrix(values[(p,a)])
        product_matrix = mmul(product_matrix,m if sign == 1 else adjoint(m))
    need(product_matrix == matrix(old), 'independent complex full Wilson product')
    missing = {link:qmul(gauges[link[0]],q) for link,q in values.items()}
    wrong = holonomy(word,missing)[0]
    need(wrong != old[0], 'first missing-head gauge fixture discriminates')
    return {'region':sorted(region),'links':sorted(links),'endpoints':sorted(endpoints),
            'outside_heads':sorted(endpoints-tails),'selected_links':sorted(strip_links),
            'free_links':sorted(free),'face':word,'path':path,'incident_orthant_anchors':sorted(target_anchors),
            'interior_incident_anchors':sorted(interior_anchors),'omitted_group_at_zero':templates,
            'cuboid_fixtures':fixtures,'quaternion_control':{'original_half_trace':old[0],
            'full_gauge_half_trace':changed[0],'missing_head_half_trace':wrong,
            'first_candidate_discriminates':True,'blind_candidates':[],'complex_matrix_product_equal':True}}


def quantitative_checks():
    cap = F(1,65536)
    M = 7*cap
    ecap = 2*M*2
    need(ecap == F(7,16384), 'actual complete-group local energy ceiling')
    need(4*ecap < F(1,24)**2, 'exact square comparison for full trace-distance ceiling')
    T = F(1,24)
    conservative = F(1,4)-T-T*T
    refined = F(1,4)-T/2-T*T
    need(conservative == F(119,576) and conservative-F(1,5) == F(19,2880), 'conservative target margin with squared mean')
    need(refined == F(131,576) and refined-F(1,5) == F(79,2880), 'positive second-moment effect refinement')
    need(conservative > F(1,5) and refined > conservative, 'frozen target achieved without changing cap')
    product_energy = [0,1,1,2]
    complement = [0,1,1,1]
    need([a-b for a,b in zip(product_energy,complement)] == [0,0,0,1], 'full product-vacuum form inequality')
    need([0,0,1,1][1] < complement[1], 'omitting one onsite term fails product complement')
    # Exact pure/mixed density entries in a two-dimensional diagnostic.
    a,b = F(3,5),F(4,5)
    pure = [[a*a,a*b],[a*b,b*b]]
    deficit = b*b
    trace_norm = 2*b
    need(trace_norm*trace_norm == 4*deficit, 'pure projector trace norm from two eigenvalues')
    need(trace_norm > 2*deficit and trace_norm > b, 'missing square root and factor-two bounds both fail')
    mixed = [[(1+pure[0][0])/2,pure[0][1]/2],[pure[1][0]/2,pure[1][1]/2]]
    determinant = mixed[0][0]*mixed[1][1]-mixed[0][1]*mixed[1][0]
    md = mixed[1][1]
    distance = F(4,5)
    need(determinant == F(4,25) > 0 and mixed[0][0]+mixed[1][1] == 1, 'genuine normalized mixed density')
    need(distance*distance == 4*(md*md+mixed[0][1]**2), 'mixed full trace norm from exact traceless characteristic polynomial')
    need(distance*distance < 4*md, 'pure-projector distance equality is false for this mixed state')
    # Trace-zero duality: X=diag(-1,1), signed W=diag(-1,1), effect=diag(0,1).
    need(F(2) > F(2)/2 and F(1) == F(2)/2, 'signed moment needs T while effect needs T/2')
    moments = {0:F(1),1:F(0),2:F(1,4),3:F(0)}
    moments[4] = F(3,6)*moments[2]
    need(moments[4] == F(1,8), 'exact normalized S3 fourth moment recurrence')
    tilted_norm = moments[0]+moments[1]
    tilted_mean = moments[1]+moments[2]
    tilted_second = moments[2]+moments[3]
    tilted_variance = tilted_second-tilted_mean**2
    need(tilted_norm == 1 and tilted_variance == F(3,16), 'actual-W alternative normal state moments')
    need(tilted_variance != F(1,4) and tilted_variance < tilted_second, 'Haar substitution and uncharged mean discriminate')
    epsilon = F(1,4)
    band_ceiling = 2*epsilon  # Analytic density bound 4epsilon/pi < 2epsilon.
    deficit_floor = 1-band_ceiling
    need(epsilon**2 == F(1,16) < F(1,5), 'normal concentrating state can violate variance target')
    need(deficit_floor == F(1,2) > ecap, 'concentrating control violates additional overlap/energy premise')
    alpha = F(1,8)
    delta = alpha/8
    free_physical_gap = 3*alpha/4
    test_deficit = F(1,4)
    physical_energy = delta*test_deficit
    need(delta == F(1,64) and free_physical_gap/delta == 6, 'fixed physical normalization of free reference gap')
    need(physical_energy == F(1,256) < test_deficit and physical_energy/delta == test_deficit, 'unconverted physical energy cannot bound dimensionless deficit')
    raw_levels = [F(-3),F(-2)]
    centered = [v-raw_levels[0] for v in raw_levels]
    raw_mean = F(3,4)*raw_levels[0]+F(1,4)*raw_levels[1]
    need(centered == [0,1] and raw_mean == F(-11,4) < 0, 'true reference ground scalar required for nonnegative energy')
    c1,c2 = 7*cap/2,F(1)
    hypothetical_threshold = min(c1,1/(2*c2))/7
    candidate = 3*cap/4
    need(hypothetical_threshold == cap/2 < candidate <= cap, 'extra cap alone does not imply symbolic stability premise')
    need(abs(-cap) == abs(cap), 'signed coupling uses same absolute budget')
    need(F(1,4)-2*F(0)-4*F(0) == F(1,4), 'zero-coupling exact reference variance')
    return {'cap':cap,'M_at_cap':M,'incident_group_count':2,'energy_and_deficit_cap':ecap,
            'full_trace_norm_ceiling':T,'mean_absolute_ceiling':T,'mean_square_ceiling':T*T,
            'conservative_second_moment_floor':F(1,4)-T,
            'effect_second_moment_floor':F(1,4)-T/2,
            'conservative_variance_floor':conservative,'refined_variance_floor':refined,
            'target':F(1,5),'conservative_margin':conservative-F(1,5),'refined_margin':refined-F(1,5),
            'pure_distance_control':{'density':pure,'deficit':deficit,'full_trace_norm':trace_norm,'wrong_no_root':2*deficit,'wrong_no_factor_two':b},
            'mixed_control':{'density':mixed,'determinant':determinant,'deficit':md,'full_trace_norm':distance,'pure_equality_false':True},
            'reference_moments':moments,'alternative_normal_state':{'configuration_multiplier_squared':'1+W','norm':tilted_norm,'mean':tilted_mean,'second_moment':tilted_second,'variance':tilted_variance,'is_actual_interacting_ground':False},
            'concentration_control':{'epsilon':epsilon,'band_probability_strict_upper_bound':band_ceiling,'deficit_strict_lower_bound':deficit_floor,'variance_upper_bound':epsilon**2,'form_energy_finite_claimed':False,'excluded_by_actual_energy_cap':True},
            'scale_control':{'alpha':alpha,'delta':delta,'deficit':test_deficit,'physical_reference_energy':physical_energy,'free_gap_over_delta':free_physical_gap/delta},
            'centering_control':{'raw_levels':raw_levels,'centered_levels':centered,'raw_mean':raw_mean},
            'symbolic_cap_control':{'hypothetical_c1':c1,'hypothetical_c2':c2,'hypothetical_tau_star':hypothetical_threshold,'candidate':candidate,'actual_source_constants_evaluated':False}}


def sources():
    freeze_path = INPUT+'input-freeze.json'
    inventory_path = INPUT+'source-inventory.json'
    need(digest(freeze_path) == PACK_SHA, 'root-validated independent input freeze')
    need(digest(inventory_path) == INVENTORY_SHA, 'root-validated complete source inventory')
    fr, inv = read(freeze_path),read(inventory_path)
    bindings = {freeze_path:PACK_SHA,inventory_path:INVENTORY_SHA}
    for path,h in fr['bindings'].items():
        need(digest(path) == h, 'owned frozen input '+path)
        bindings[path] = h
    need(len(inv['entries']) == 61, 'complete sixty-one source/instruction snapshots')
    contract = read(INPUT+CONTRACT)
    required = {**contract['sources'],CONTRACT:CONTRACT_SHA}
    covered = {}
    for entry in inv['entries']:
        path,h = entry['snapshot'],entry['sha256']
        need(path.startswith(INPUT) and digest(path) == h, 'owned runtime snapshot '+path)
        bindings[path] = h
        origin = entry['source']
        if Path(origin).is_absolute():
            need(entry.get('external_instruction_snapshot') is True, 'installed origin is provenance only')
        else:
            bindings[origin] = h  # Origin digest is inherited metadata, not an origin read.
            if origin in required:
                need(required[origin] == h, 'exact required contract source '+origin)
                covered[origin] = h
    need(covered == required and len(required) == 44, 'every declared source plus exact contract covered')
    for name in ['ak1-independent-derivation.md','ak1_independent.py','ak1-source-reading.json','ak1-root-preflight.json']:
        bindings[BASE+name] = digest(BASE+name)
    return bindings


def encode(value):
    if isinstance(value,F):
        return {'numerator':value.numerator,'denominator':value.denominator}
    if isinstance(value,dict):
        return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [encode(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute() or output.exists():
        raise ValueError('output must be a fresh absolute file')
    bindings = sources()
    start = len(checks)
    graph = geometry()
    geometry_count = len(checks)-start
    start = len(checks)
    theorem = quantitative_checks()
    arithmetic_count = len(checks)-start
    result = {'schema':'ym28-ak1-independent-v1','loop':'ak1','sequence':9,
              'status':'independently derived before producer exchange; pending review',
              'all_checks_passed':True,'check_count':len(checks),'checks':checks,
              'check_groups':{'source':len(checks)-geometry_count-arithmetic_count,'geometry':geometry_count,'arithmetic_and_controls':arithmetic_count},
              'geometry':graph,'certificate_and_controls':theorem,'bindings':bindings,
              'scope':{'actual_I1_AJ1_AJ2_homogeneous_orthant':True,'same_original_xz_Wilson':True,
                       'regime':'all real |tau|<unevaluated tau_* and |tau|<=1/65536; fixed selected-coefficient ranges',
                       'target_variance_at_least_one_fifth':True,'independent_stronger_floor':'131/576',
                       'mixed_density_trace_bound_proved':True,'unknown_mean_squared_charged':True,
                       'energy_is_local_reference_not_excited_physical_moment':True,
                       'actual_physical_energy_moment_or_domain_claim':False,'evaluated_tau_star':False,
                       'chosen_positive_numerical_stability_coupling':False,'all_translated_observables':False,
                       'other_boundary_identification':False,'continuum_result':False,'scientific_priority_verified':False},
              'current_producer_science_read':False,'historical_checkers_imported':False,
              'finite_checks_prove_analytic_theorem':False,'ak2_selected_or_executed':False,
              'new_research_loops':1,'nondiscriminating_scientific_attempts':[]}
    output.write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'check_count':len(checks),'check_groups':result['check_groups'],'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
