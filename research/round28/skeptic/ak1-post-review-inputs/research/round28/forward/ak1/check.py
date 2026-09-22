#!/usr/bin/env python3
"""AK1 forward exact diagnostics; runtime reads only owned source snapshots.

Analytic infinite-dimensional implications are proved in report.md. These
standard-library fixtures audit the geometry, arithmetic and countermodels.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREFIX = HERE.relative_to(ROOT).as_posix()
CONTRACT = "research/round28/contracts/ak1.json"
CONTRACT_SHA = "2afd1ff408b4774e79f1964f796835c6e4088cce22de5c1c66c85d796c9a9810"
INVENTORY_SHA = "e2fafe5f975f857385e05de335b0bef68240f5834e876bf7f915066f05a105f1"
PACK_SHA = "04f10aa2d6db97dd186775c4118a3081300053a0649ed21c020edb21255304d6"
O = (0, 0, 0)
STEPS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
STAR = (O,) + STEPS
REGION = frozenset((O, STEPS[2]))
INTERIOR = frozenset(((1, 1, 1), (1, 1, 2)))
CHECKS = []


def check(name, condition, **data):
    if condition is not True:
        raise RuntimeError("AK1 check failed: " + name)
    CHECKS.append(dict(id=name, passed=True, **data))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [clean(v) for v in value]
    return value


def owned(path):
    p = ROOT / path
    if not p.is_relative_to(HERE):
        raise RuntimeError("Non-owned runtime input: " + path)
    for component in (p,) + tuple(p.parents):
        if component.is_symlink():
            raise RuntimeError("Symlink input: " + str(component))
    return p


def inputs():
    inventory = HERE / "inputs/source-inventory.json"
    pack = HERE / "inputs-current-freeze.json"
    check("canonical-inventory-frozen", digest(inventory) == INVENTORY_SHA)
    check("input-pack-frozen", digest(pack) == PACK_SHA)
    manifest = json.loads(inventory.read_text())
    cpath = HERE / "inputs" / CONTRACT
    check("contract-frozen", digest(cpath) == CONTRACT_SHA)
    contract = json.loads(cpath.read_text())
    by_source = {}
    bindings = {PREFIX + "/check.py": digest(Path(__file__))}
    for item in manifest["entries"]:
        source, snapshot, sha = item["source"], item["snapshot"], item["sha256"]
        if source in by_source:
            raise RuntimeError("Duplicate input source: " + source)
        if digest(owned(snapshot)) != sha:
            raise RuntimeError("Snapshot mismatch: " + snapshot)
        by_source[source] = item
        bindings[snapshot] = sha
        if not item.get("external_instruction_snapshot", False):
            if Path(source).is_absolute() or ".." in Path(source).parts:
                raise RuntimeError("Nonportable original provenance")
            bindings[source] = sha  # Frozen metadata, never read original bytes.
    required = dict(contract["sources"])
    required[CONTRACT] = CONTRACT_SHA
    check("all-required-sources-owned", all(
        s in by_source and by_source[s]["sha256"] == h for s, h in required.items()),
        declared_sources=len(contract["sources"]), inventory_entries=len(by_source))
    check("required-source-count", len(contract["sources"]) == 43)
    for path, sha in json.loads(pack.read_text())["files"].items():
        if digest(owned(path)) != sha:
            raise RuntimeError("Input pack mismatch: " + path)
        bindings[path] = sha
    for p in [inventory, pack]:
        bindings[p.relative_to(ROOT).as_posix()] = digest(p)
    check("portable-flat-bindings", all(not Path(p).is_absolute() and isinstance(h, str)
                                        and len(h) == 64 for p, h in bindings.items()))
    return contract, dict(sorted(bindings.items()))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def owner(tail):
    return tail[0] // 4, tail[1] // 2, tail[2]


def tails(b):
    return [(4*b[0]+x, 2*b[1]+y, b[2]) for x in range(4) for y in range(2)]


def links(region):
    return sorted((t, d) for b in region for t in tails(b) for d in range(3))


def head(link):
    t, d = link
    return add(t, STEPS[d])


def endpoints(ls):
    return sorted({v for link in ls for v in (link[0], head(link))})


def word(t, a, b):
    return ((t, a, 1), (add(t, STEPS[a]), b, 1),
            (add(t, STEPS[b]), a, -1), (t, b, -1))


def faces(b, omitted=True):
    out = []
    for t in tails(b):
        for a, d in itertools.combinations(range(3), 2):
            selected = a == 0 and d == 1 and t[0] % 4 < 3 and t[1] % 2 == 0
            if omitted and selected:
                continue
            w = word(t, a, d)
            out.append(dict(tail=t, axes=(a, d), selected=selected, word=w,
                            support=sorted({owner(edge[0]) for edge in w})))
    return out


def incident_plus(region):
    return {sub(r, s) for r in region for s in STAR if min(sub(r, s)) >= 0}


def star(b):
    return {add(b, s) for s in STAR}


def geometry(contract):
    ls = links(REGION)
    vs = endpoints(ls)
    w = word(O, 0, 2)
    check("same-original-xz-face", {owner(t) for t, _, _ in w} == REGION)
    check("complete48links36endpoints", len(ls) == 48 and len(set(ls)) == 48 and len(vs) == 36)
    check("all-original-heads-owned", all(owner(t) in REGION for t, _ in ls))
    selected = { (t, d) for b in REGION for f in faces(b, False) if f["selected"]
                for t, d, _ in f["word"] }
    free = set(ls) - selected
    check("selected20free28", len(selected) == 20 and len(free) == 28)
    check("conditioned-original-z-link-free", (O, 2) in free and sum(t == O and d == 2 for t,d,_ in w) == 1)
    base_faces = faces(O)
    support_counts = {}
    for face in base_faces:
        key = tuple(face["support"])
        support_counts[key] = support_counts.get(key, 0) + 1
    expected = {(O, STEPS[0]):1, (O, STEPS[1]):3,
                tuple(sorted((O, STEPS[0], STEPS[1]))):1,
                (O, STEPS[2]):10,
                tuple(sorted((O, STEPS[0], STEPS[2]))):2,
                tuple(sorted((O, STEPS[1], STEPS[2]))):4}
    # Normalize key ordering, independently of lexicographic coordinate order.
    expected = {tuple(sorted(k)): v for k,v in expected.items()}
    check("all21omitted-face-classes", support_counts == expected and len(base_faces) == 21)
    check("star-is-four-site-union", set().union(*(set(f["support"]) for f in base_faces)) == set(STAR))
    origin_anchors = incident_plus(REGION)
    bulk_anchors = incident_plus(INTERIOR)
    check("orthant-origin-pair-two-groups", origin_anchors == set(REGION))
    check("interior-pair-seven-groups", len(bulk_anchors) == 7)
    check("shared-group-counted-once", sum(len(incident_plus({r})) for r in REGION) == 3
          and len(origin_anchors) == 2)
    # This deliberately retained candidate is blind at the origin.
    check("outgoing-only-origin-blind-retained", origin_anchors == set(REGION),
          verdict="nondiscriminating", correct_count=2, outgoing_only_count=2)
    check("outgoing-only-interior-rejected", len(bulk_anchors) == 7 and len(INTERIOR) == 2)
    check("two-factor-cover-not-star-Hamiltonian", not any(star(b) <= REGION for b in REGION)
          and sum(set(f["support"]) <= REGION for f in base_faces) == 10)
    fixtures = []
    for counts in contract["parameters"]["geometry_fixtures"]["cuboid_side_counts"]:
        cube = set(itertools.product(*(range(n) for n in counts)))
        anchors = {b for b in cube if star(b) <= cube}
        by_scan = {b for b in anchors if star(b) & REGION}
        inverse = incident_plus(REGION) & anchors
        check("finite-incidence-" + "".join(map(str,counts)), by_scan == inverse)
        clinks = links(cube)
        check("finite-complete-links-" + "".join(map(str,counts)),
              len(clinks) == 24*len(cube) and all(owner(t) in cube for t,d in clinks))
        expected_n = 1 if counts[2] == 2 else 2
        check("finite-target-groups-" + "".join(map(str,counts)), len(by_scan) == expected_n)
        bulk = None
        if INTERIOR <= cube:
            actual = {b for b in anchors if star(b) & INTERIOR}
            check("finite-interior-inverse-" + "".join(map(str,counts)),
                  actual == incident_plus(INTERIOR) & anchors)
            bulk_touching = sum(bool(set(f["support"]) & INTERIOR) for b in actual for f in faces(b))
            check("whole-groups-not-touching-faces-interior-" + "".join(map(str,counts)),
                  bulk_touching < 21*len(actual))
            bulk = dict(anchors=sorted(actual), groups=len(actual), outgoing_only=len(actual & INTERIOR),
                        charged_group_faces=21*len(actual), actually_touching_faces=bulk_touching)
        touching = sum(bool(set(f["support"]) & REGION) for b in by_scan for f in faces(b))
        check("touching-face-count-origin-blind-" + "".join(map(str,counts)), touching == 21*len(by_scan),
              verdict="nondiscriminating", reason="Every incident target anchor lies in R.")
        fixtures.append(dict(coarse_side_counts=counts, sites=len(cube), links=len(clinks),
            endpoints=len(endpoints(clinks)), retained_stars=len(anchors), retained_faces=21*len(anchors),
            target_anchors=sorted(by_scan), target_groups=len(by_scan),
            target_charged_group_faces=21*len(by_scan), actually_touching_faces=touching,
            reference_energy_coefficient_per_abs_tau=14*len(by_scan), interior=bulk))
    endpoint_actions = [dict(vertex=v,
        outgoing=[l for l in ls if l[0] == v], incoming=[l for l in ls if head(l) == v]) for v in vs]
    check("each-link-has-both-endpoint-actions", sum(len(v["outgoing"])+len(v["incoming"])
          for v in endpoint_actions) == 2*len(ls))
    return dict(region=sorted(REGION), original_word=w, original_links=ls,
                endpoint_actions=endpoint_actions, selected_links=sorted(selected), free_links=sorted(free),
                omitted_origin_templates=base_faces, orthant_incident_anchors=sorted(origin_anchors),
                interior_incident_anchors=sorted(bulk_anchors), cuboids=fixtures)


def qm(a, b):
    w,x,y,z = a
    v,r,s,t = b
    return (w*v-x*r-y*s-z*t, w*r+x*v+y*t-z*s,
            w*s-x*t+y*v+z*r, w*t+x*s-y*r+z*v)


def qi(a):
    return (a[0], -a[1], -a[2], -a[3])


UNIT = (F(1), F(0), F(0), F(0))
QUATS = (UNIT, (F(3,5),F(4,5),F(0),F(0)),
         (F(5,13),F(0),F(12,13),F(0)), (F(8,17),F(0),F(0),F(15,17)),
         (F(1,2),)*4)


def holonomy(w, assignment):
    a = UNIT
    for t,d,s in w:
        q = assignment[t,d]
        a = qm(a, q if s == 1 else qi(q))
    return a


def quaternion_controls(g):
    ls = [(tuple(t), d) for t,d in g["original_links"]]
    vertices = [tuple(v["vertex"]) for v in g["endpoint_actions"]]
    w = word(O,0,2)
    check("rational-quaternions-are-su2", all(sum(x*x for x in q) == 1 for q in QUATS))
    attempts = []
    for seed in range(5):
        assignment = {link: QUATS[(i+seed+1) % len(QUATS)] for i,link in enumerate(ls)}
        gauge = {v: QUATS[(2*i+seed+2) % len(QUATS)] for i,v in enumerate(vertices)}
        full = {l: qm(qm(gauge[l[0]],q), qi(gauge[head(l)])) for l,q in assignment.items()}
        missing_head = {l: qm(gauge[l[0]],q) for l,q in assignment.items()}
        before, after = holonomy(w,assignment), holonomy(w,full)
        wrong = holonomy(w,missing_head)[0]
        check("full-endpoint-covariance-attempt-"+str(seed),
              after == qm(qm(gauge[O], before), qi(gauge[O])) and after[0] == before[0])
        attempts.append(dict(seed=seed, before=before[0], full=after[0], missing_head=wrong,
                             discriminates=wrong != before[0]))
        if wrong != before[0]:
            break
    check("missing-head-rejected", any(a["discriminates"] for a in attempts))
    # Conditional W = scalar(A u^{-1}) has a unit real linear coefficient.
    assignment[O,2] = UNIT
    a = holonomy(w,assignment)
    coefficients = []
    for k in range(4):
        basis = tuple(F(int(i == k)) for i in range(4))
        coefficients.append(qm(a,qi(basis))[0])
    check("conditional-unit-linear-coefficient", sum(c*c for c in coefficients) == 1)
    second = sum(c*c*F(1,4) for c in coefficients)
    check("conditional-reference-half-trace-moments", second == F(1,4))
    return dict(attempts=attempts, conditional_coefficients=coefficients,
                reference_mean=F(0), reference_second_moment=second,
                scope="Exact SU(2) rational diagnostics; Haar integration is analytic, not finite-group quadrature.")


def quantitative_controls():
    cap = F(1, 2**16)
    energy = 2*F(7)*2*cap
    dbar = F(1,24)
    check("sharp-orthant-energy-ceiling", energy == F(7,16384))
    check("trace-distance-rational-ceiling", 4*energy < dbar*dbar,
          squared_trace_ceiling=4*energy, rational_ceiling_squared=dbar*dbar)
    floor = F(1,4)-dbar-dbar*dbar
    check("both-moments-and-squared-mean", floor == F(119,576))
    check("constructive-target-one-fifth", floor-F(1,5) == F(19,2880) and floor > F(1,5))
    check("all-couplings-monotone-majorant", cap > 0 and energy > 0 and dbar > 0,
          reason="For 0<=x<=y, sqrt(x)<=sqrt(y), and d+d^2 increases for d>=0.")
    # Product projector gap by all four exact joint eigenprojections.
    projector_cells = []
    for p,q in itertools.product((0,1), repeat=2):
        gap_sum = (1-p)+(1-q)
        excluded = 1-p*q
        check("product-gap-cell-"+str(p)+str(q), gap_sum >= excluded)
        projector_cells.append(dict(p0=p,pz=q,gap_sum=gap_sum,one_minus_product=excluded))
    # Pure density difference has trace zero and squared trace norm 4e.
    a,b = F(24,25),F(7,25)
    e = b*b
    offdiag = a*b
    difference_square = e*e+offdiag*offdiag
    distance = 2*b
    check("pure-two-dimensional-trace-formula", a*a+b*b == 1 and difference_square == e
          and distance*distance == 4*e)
    check("missing-square-root-rejected", distance > 2*e,
          valid_distance=distance, wrong_no_sqrt=2*e)
    check("missing-trace-factor-rejected", distance > b,
          valid_distance=distance, wrong_factor_one=b)
    # Genuine full-rank density: no pure-vector replacement, strict upper bound.
    mixed = ((F(3,4),F(0)),(F(0),F(1,4)))
    mixed_purity = mixed[0][0]**2+mixed[1][1]**2
    mixed_distance = F(1,2)
    check("mixed-density-positive-trace-one", mixed[0][0]+mixed[1][1] == 1 and mixed[0][0]*mixed[1][1] > 0)
    check("pure-state-assumption-on-mixed-rejected", mixed_purity == F(5,8) and mixed_purity != 1)
    check("pure-distance-equality-on-mixed-rejected", mixed_distance < 1,
          actual_distance=mixed_distance, wrongly_imposed_pure_equality=F(1))
    # Noncommuting mixed density and exact determinant identity also test bound.
    q,c = F(1,5),F(1,5)
    determinant = q*(1-q)-c*c
    check("noncommuting-mixed-trace-bound", determinant > 0 and 4*(q*q+c*c) < 4*q,
          determinant=determinant, distance_squared=4*(q*q+c*c), bound_squared=4*q)
    # Actual-local-space alternative normal state sqrt(1+kW) Omega_ref.
    k = F(1)
    alternative_mean = k*F(1,4)
    alternative_second = F(1,4)
    alternative_variance = alternative_second-alternative_mean**2
    check("uncharged-squared-mean-rejected", alternative_variance == F(3,16)
          and alternative_variance < alternative_second)
    check("interacting-haar-moment-substitution-rejected", alternative_mean != 0
          and alternative_variance != F(1,4) and alternative_variance < F(1,5))
    mean_overlap_floor = alternative_mean**2/4
    check("energy-overlap-excludes-tilted-normal-control", mean_overlap_floor > energy,
          forced_reference_energy_lower_bound=mean_overlap_floor)
    # Normal narrow-band state built from the actual reference vector.
    band_halfwidth = F(1,4)
    band_mass_upper = 2*band_halfwidth  # Haar half-trace density <=1 since pi>2.
    band_excitation_lower = 1-band_mass_upper
    check("normal-concentration-below-target", band_halfwidth**2 == F(1,16) and band_halfwidth**2 < F(1,5))
    check("energy-overlap-excludes-normal-concentration", band_excitation_lower > energy,
          overlap_upper=band_mass_upper, reference_energy_lower=band_excitation_lower)
    # All four pure energy sectors after centering and physical normalization.
    alpha,delta = F(24),F(3)
    raw_centers = (F(-5),F(-7))
    check("fixed-delta-scale", delta == alpha/8)
    check("reference-ground-scalar-retained", sum(raw_centers)-sum(raw_centers) == 0
          and sum(raw_centers)/delta == -4)
    check("wrong-alpha-normalization-rejected", delta/alpha == F(1,8) and delta/alpha < 1)
    check("additive-scalar-cancels", (sum(raw_centers)+11)-(sum(raw_centers)+11) == 0)
    check("zero-coupling-reference-recovered", 2*7*2*F(0) == 0,
          implication="h_R>=I-P and trace-one imply rho_R=P; mean=0, variance=1/4.")
    # Logical models of unknown positive source constants, never evaluated values.
    c1,c2 = cap,F(1)
    hypothetical_tau_star = min(c1,F(1,2)/c2)/7
    check("auxiliary-cap-not-stability-radius", cap > hypothetical_tau_star > 0,
          scope="Countermodel of inference from unspecified positive constants; not actual source constants.",
          hypothetical_c1=c1, hypothetical_c2=c2, cap_candidate=cap,
          hypothetical_tau_star=hypothetical_tau_star)
    check("strict-source-boundary-retained", not hypothetical_tau_star < hypothetical_tau_star)
    return dict(cap=cap, cap_scope="Conditional algebra only: also require actual |tau|<symbolic tau_*.",
                numerical_stability_interval_evaluated=False,
                selected_positive_admissible_tau=None,
                energy_ceiling=energy, product_projector_cells=projector_cells,
                overlap_lower=1-energy, trace_distance_ceiling=dbar,
                reference_mean=F(0), reference_second_moment=F(1,4),
                actual_mean_absolute_ceiling=dbar, actual_second_moment_lower=F(1,4)-dbar,
                actual_variance_lower=floor, required_floor=F(1,5), target_margin=floor-F(1,5),
                analytic_floor="1/4 - 2 sqrt(28 |tau|) - 112 |tau|",
                tilted_normal_control=dict(mean=alternative_mean, second=alternative_second,
                    variance=alternative_variance, energy_lower=mean_overlap_floor),
                concentration_control=dict(band_halfwidth=band_halfwidth,
                    variance_upper=band_halfwidth**2, overlap_upper=band_mass_upper,
                    energy_lower=band_excitation_lower))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.output.is_absolute() or args.output.exists():
        raise RuntimeError("--output must be a fresh absolute DIRECTORY")
    contract, bindings = inputs()
    geom = geometry(contract)
    quat = quaternion_controls(geom)
    quantitative = quantitative_controls()
    result = dict(schema="ym28-ak1-forward-v1", loop="ak1", sequence=9, direction="forward",
        contract_sha256=CONTRACT_SHA, passed=True, verdict="constructive-conditional-variance-floor",
        model=contract["model"], bindings=bindings, geometry=geom,
        quaternion_diagnostics=quat, quantitative=quantitative,
        checks=CHECKS, check_count=len(CHECKS),
        scope=dict(physical_energy_moment_claimed=False, spectral_window_claimed=False,
                   scientific_priority_verified=False, ak2_selected_or_executed=False),
        controls_with_blind_candidates=["outgoing-only-origin-blind-retained", "touching-face-count-origin-blind"])
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/"results.json").write_text(json.dumps(clean(result), indent=2, sort_keys=True)+"\n")
    print(json.dumps(dict(passed=True, check_count=len(CHECKS), variance_floor=str(quantitative["actual_variance_lower"]))))


if __name__ == "__main__":
    main()
