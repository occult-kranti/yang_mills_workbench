#!/usr/bin/env python3
"""AJ1 independent forward exact fixtures; analytic theorems are in report.md.

Run with --output a fresh absolute directory. Only the standard library is used.
No historical or opposite-direction checker is imported or executed.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT_SHA = "a9660ab26b0116958c11721e5461eab3391d50149306e06a0ec2476cdbc21571"
PACK_SHA = "a18b36cecf48204d5946ae6233a5228adf43a9750a6f05c55d5730d2cc0fc8ac"
ZERO = (0, 0, 0)
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
STAR = (ZERO,) + AXES


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def rational(x):
    x = Q(x)
    return {"numerator": x.numerator, "denominator": x.denominator}


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def owner(tail):
    return (tail[0] // 4, tail[1] // 2, tail[2])


def owned_links(b):
    return {((4*b[0] + x, 2*b[1] + y, b[2]), d)
            for x, y, d in product(range(4), range(2), range(3))}


def endpoints(links):
    return {v for tail, d in links for v in (tail, add(tail, AXES[d]))}


def square(a, i, j):
    # Positive canonical links with signs in cyclic boundary order.
    return (((a, i), 1), ((add(a, AXES[i]), j), 1),
            ((add(a, AXES[j]), i), -1), ((a, j), -1))


def faces(b):
    answer = []
    for x, y in product(range(4), range(2)):
        a = (4*b[0] + x, 2*b[1] + y, b[2])
        for i, j in combinations(range(3), 2):
            edges = square(a, i, j)
            support = {owner(link[0]) for link, _ in edges}
            selected = i == 0 and j == 1 and y == 0 and x < 3
            answer.append({"anchor": a, "axes": (i, j), "edges": edges,
                           "support": support, "selected": selected})
    return answer


def geometric_checks():
    local = faces(ZERO)
    selected = [f for f in local if f["selected"]]
    omitted = [f for f in local if not f["selected"]]
    selected_links = {e for f in selected for e, _ in f["edges"]}
    require(len(local) == 24 and len(selected) == 3 and len(omitted) == 21,
            "Full anchor face count")
    require(len(owned_links(ZERO)) == 24 and len(selected_links) == 10,
            "Full site and selected strip link counts")
    require(selected_links <= owned_links(ZERO), "Strip ownership")
    classes = Counter(tuple(sorted(f["support"])) for f in omitted)
    expected = {
        (ZERO, AXES[0]): 1,
        (ZERO, AXES[1]): 3,
        tuple(sorted((ZERO, AXES[0], AXES[1]))): 1,
        (ZERO, AXES[2]): 10,
        tuple(sorted((ZERO, AXES[0], AXES[2]))): 2,
        tuple(sorted((ZERO, AXES[1], AXES[2]))): 4,
    }
    expected = {tuple(sorted(k)): v for k, v in expected.items()}
    require(dict(classes) == expected, "Independent 21-face support dictionary")
    require(set().union(*(f["support"] for f in omitted)) == set(STAR),
            "Actual union of complete anchor group is full star")
    require(all(len(f["support"]) >= 2 for f in omitted), "No onsite omitted face")
    fixtures = []
    detected_incoming = False
    detected_clipping_difference = False
    for sides in ((2, 2, 2), (3, 2, 2), (3, 3, 3)):
        sites = set(product(*(range(n) for n in sides)))
        all_links = set().union(*(owned_links(b) for b in sites))
        require(len(all_links) == 24 * len(sites), "Unique ownership at finite boundary")
        group_support = {b: {add(b, s) for s in STAR} for b in sites}
        retained = {b: S for b, S in group_support.items() if S <= sites}
        require(len(retained) == (sides[0]-1)*(sides[1]-1)*(sides[2]-1),
                "Whole-star anchor count")
        all_faces = [(b, f) for b in sorted(sites) for f in faces(b) if not f["selected"]]
        retained_faces = [(b, f) for b, f in all_faces if b in retained]
        actual_support_faces = [(b, f) for b, f in all_faces if f["support"] <= sites]
        require(len(retained_faces) == 21 * len(retained), "Complete retained groups")
        require(all({e for e, _ in f["edges"]} <= all_links for _, f in retained_faces),
                "Every retained face has all four full owned links")
        extra = len(actual_support_faces) - len(retained_faces)
        require(extra > 0, "Whole-star versus individual-face boundary control must discriminate")
        detected_clipping_difference |= extra > 0
        region_records = []
        for points in ((ZERO,), (ZERO, (1, 0, 0)), ((1, 1, 1),)):
            F = set(points)
            if not F <= sites:
                continue
            incident = {b for b, S in retained.items() if S & F}
            outgoing_only = {b for b in retained if b in F}
            incoming = incident - outgoing_only
            inverse_incidence = {b for x in F for s in STAR
                                 for b in [tuple(x[d]-s[d] for d in range(3))]
                                 if b in retained}
            require(incident == inverse_incidence, "Incoming and outgoing anchors match direct inverse rule")
            require(len(incident) <= 4*len(F), "All-volume incidence coefficient")
            links_F = set().union(*(owned_links(b) for b in F))
            gauge_F = endpoints(links_F)
            tail_vertices = {a for a, _ in links_F}
            missing_heads = gauge_F - tail_vertices
            require(missing_heads, "Endpoint control must detect outgoing link heads")
            affected_faces = [f for b, f in retained_faces if b in incident and f["support"] & F]
            complete_groups_faces = [f for b, f in retained_faces if b in incident]
            require(len(complete_groups_faces) == 21*len(incident), "Reset budget retains every incident group whole")
            if sides == (3, 3, 3) and points == ((1, 1, 1),):
                require(len(incident) == 4 and len(incoming) == 3 and len(outgoing_only) == 1,
                        "Interior fixture must detect three incoming anchors")
                detected_incoming = True
            region_records.append({
                "region": sorted(F), "owned_link_count": len(links_F),
                "endpoint_vertex_count": len(gauge_F), "endpoint_vertices": sorted(gauge_F),
                "outgoing_head_vertices_lost_by_tail_only_gauge": sorted(missing_heads),
                "incident_anchor_count": len(incident), "incident_anchors": sorted(incident),
                "incoming_anchors": sorted(incoming), "outgoing_only_count": len(outgoing_only),
                "complete_incident_group_face_count": len(complete_groups_faces),
                "actually_touching_face_count": len(affected_faces),
                "normalized_local_energy_ceiling_as_multiple_of_M": 2*len(incident),
                "volume_independent_ceiling_as_multiple_of_M": 8*len(F),
                "spectral_escape_ceiling": "2 M N_F,Lambda / L; bounded by 8 M |F| / L"
            })
        fixtures.append({"sides": sides, "site_count": len(sites),
                         "owned_link_count": len(all_links), "all_endpoint_count": len(endpoints(all_links)),
                         "retained_anchor_count": len(retained), "retained_anchors": sorted(retained),
                         "retained_omitted_face_count": len(retained_faces),
                         "individually_contained_omitted_face_count": len(actual_support_faces),
                         "boundary_rule_difference": extra, "regions": region_records})
    require(detected_incoming and detected_clipping_difference, "Boundary controls did not discriminate")
    return {"owned_links_per_site": 24, "selected_strip_links": 10, "free_links": 14,
            "selected_faces": 3, "omitted_faces_per_anchor": 21,
            "support_classes": [{"support": k, "count": v} for k, v in sorted(classes.items())],
            "fixtures": fixtures}


def quat(a, b):
    w, x, y, z = a
    v, p, q, r = b
    return (w*v-x*p-y*q-z*r, w*p+x*v+y*r-z*q,
            w*q-x*r+y*v+z*p, w*r+x*q-y*p+z*v)


def inv(a):
    return (a[0], -a[1], -a[2], -a[3])


ONE = (Q(1), Q(0), Q(0), Q(0))
RATIONAL_SU2 = ((Q(3,5), Q(4,5), Q(0), Q(0)),
                (Q(5,13), Q(0), Q(12,13), Q(0)),
                (Q(8,17), Q(0), Q(0), Q(15,17)))


def holonomy(edges, links):
    value = ONE
    for link, orientation in edges:
        u = links[link]
        value = quat(value, u if orientation == 1 else inv(u))
    return value


def gauge_transform(links, gauge, omit_head=False):
    return {e: quat(quat(gauge.get(e[0], ONE), u),
                    ONE if omit_head else inv(gauge.get(add(e[0], AXES[e[1]]), ONE)))
            for e, u in links.items()}


def average_quaternions(values):
    return tuple(sum(v[d] for v in values) / len(values) for d in range(4))


def gauge_controls():
    for u in RATIONAL_SU2:
        require(quat(u, inv(u)) == ONE, "Exact rational SU(2) unit norm")
    # An omitted xz square genuinely crosses its coarse anchor boundary.
    face = next(f for f in faces(ZERO) if f["axes"] == (0, 2))
    es = sorted(e for e, _ in face["edges"])
    links = {e: RATIONAL_SU2[i % 3] for i, e in enumerate(es)}
    vertices = sorted(endpoints(es))
    gauge = {v: RATIONAL_SU2[(i+1) % 3] for i, v in enumerate(vertices)}
    before = holonomy(face["edges"], links)
    after = holonomy(face["edges"], gauge_transform(links, gauge))
    require(before[0] == after[0], "Closed Wilson trace gauge invariance")
    require(after == quat(quat(gauge[face["anchor"]], before), inv(gauge[face["anchor"]])),
            "Closed holonomy conjugates at basepoint")
    open_edge = es[0]
    open_after = gauge_transform(links, gauge)[open_edge]
    require(open_after != links[open_edge], "Charged open-link control must discriminate")
    bad = holonomy(face["edges"], gauge_transform(links, gauge, omit_head=True))
    require(bad[0] != before[0], "Dropping head actions must change closed Wilson trace")
    q8 = [tuple(Q(s if d == k else 0) for d in range(4))
          for k in range(4) for s in (-1, 1)]
    closed_averages = []
    for vertex in vertices:
        values = [holonomy(face["edges"], gauge_transform(links, {vertex: g}))[0] for g in q8]
        require(all(v == before[0] for v in values), "Q8 closed-loop invariance at every endpoint")
        closed_averages.append(sum(values)/8)
    charged_mean = average_quaternions([gauge_transform(links, {open_edge[0]: g})[open_edge] for g in q8])
    require(charged_mean == (0,0,0,0), "Exact fundamental charged Haar first moment")
    matrix_proxy = (Q(2), Q(3), Q(5), Q(7))
    conjugation_mean = average_quaternions([quat(quat(g, matrix_proxy), inv(g)) for g in q8])
    require(conjugation_mean == (2,0,0,0), "Finite irreducible conjugation average")
    return {"model": "Exact rational unit-quaternion SU(2) holonomy and finite Q8 averages",
            "scope": "Q8 checks these first moments and covariance only; it is not full SU(2) Haar on arbitrary operators and does not prove SU(2) character triviality",
            "closed_wilson_before": rational(before[0]), "closed_wilson_after": rational(after[0]),
            "wrong_missing_head_wilson": rational(bad[0]),
            "charged_link_changes": True, "charged_finite_haar_mean": [rational(v) for v in charged_mean],
            "closed_average_at_each_vertex": [rational(v) for v in closed_averages],
            "conjugation_average": [rational(v) for v in conjugation_mean]}


def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def analytic_controls():
    # Exact finite prefixes of explicitly stated infinite countermodels.
    escape = []
    for m in (1,2,4,8):
        n = m+1
        cutoff = Q(int(n <= m))
        require(cutoff == 0, "Escaping vector misses finite cutoff")
        escape.append({"cutoff_rank": m, "state_index": n,
                       "finite_cutoff_expectation": rational(cutoff), "identity_expectation": rational(1)})
    strong_not_norm = []
    for k in (1,2,4,8,16):
        # U(t)e_n=exp(i*n*t)e_n, S e_n=e_(2n), t=pi/k, n=k.
        exponent_multiple_of_pi = Q(2*k-k, k)
        require(exponent_multiple_of_pi == 1, "Exact witness phase at n=k")
        strong_not_norm.append({"time": "pi/"+str(k), "witness_basis_index": k,
                                "phase": -1, "operator_norm_difference": 2})
    domain = []
    for N in (1,2,4,8,16):
        norm_sq = sum((Q(1,n*n) for n in range(1,N+1)), Q(0))
        generator_norm_sq = sum((Q(n*n,n*n) for n in range(1,N+1)), Q(0))
        require(norm_sq < 2 and generator_norm_sq == N, "Bounded vector need not lie in generator domain")
        domain.append({"N": N, "vector_norm_squared": rational(norm_sq),
                       "generator_norm_squared": rational(generator_norm_sq)})
    H = [[1,1],[1,1]]
    P = [[1,0],[0,0]]
    HP, PH = matmul(H,P), matmul(P,H)
    require(HP != PH, "Compression control must not reduce")
    require(matmul(H,H) == [[2*x for x in row] for row in H], "Full H has spectrum in {0,2}")
    compression = matmul(matmul(P,H),P)[0][0]
    require(compression == 1 and compression*(compression-2) != 0,
            "Compression creates a value outside full spectrum")
    # Commuting physical projection can retain only the vacuum.
    K = [[0,0],[0,1]]
    require(matmul(P,K) == matmul(K,P), "Vacuum-only physical projection reduces")
    require(matmul(matmul(P,K),P) == [[0,0],[0,0]], "No excited physical vector in countermodel")
    sums = [{"N": N, "homogeneous_norm_budget_in_units_M": N,
             "abstract_summable_budget": rational(sum((Q(1,2**n) for n in range(1,N+1)),Q(0)))}
            for N in (1,2,4,8)]
    require(all(x["abstract_summable_budget"]["numerator"] < x["abstract_summable_budget"]["denominator"]
                for x in sums), "Summable contrast")
    alpha, hbar, raw_ground, raw_excited = Q(24), Q(2), Q(7), Q(9)
    delta = alpha/8
    centered = raw_excited-raw_ground
    energy, frequency = delta*centered, delta*centered/hbar
    require((delta, centered, energy, frequency) == (3,2,6,3), "Ground center and physical scaling")
    require(delta*raw_ground != 0 and energy != centered, "Wrong-center and missing-scale controls discriminate")
    return {
        "weak_star_normality_and_WOT_representation_control": {
            "prefixes": escape,
            "infinite_countermodel": "On B(ell2), weak-star subnet limits of |e_n><e_n| give every finite-rank cutoff value0 but I value1; singular GNS cannot preserve P_m increasing strongly/WOT to I.",
            "scope": "Rejects automatic local normality and generic WOT-interchange principle; actual Haar compatibility is proved analytically, not inferred from this diagnostic."},
        "strong_unitary_not_point_norm_conjugation": strong_not_norm,
        "bounded_local_vector_not_generator_domain": domain,
        "compression_not_reducing": {"H": H, "P": P, "HP": HP, "PH": PH,
                                      "full_spectral_values": [0,2], "compressed_value": compression},
        "gap_not_nonzero_excitation": {"full_generator": K, "physical_projection": P,
                                       "physical_dimension": 1, "excited_physical_dimension": 0,
                                       "scalar_observable_variance": 0},
        "nonsummable_not_summable": sums,
        "wrong_model_gap": {"inherited_I1_normalized_lower_bound": rational(Q(1,2)),
                            "J2_normalized_lower_bound_NOT_TRANSFERRED": rational(Q(973,1080)),
                            "equal": Q(1,2) == Q(973,1080)},
        "ground_center_and_units": {"abstract_fixture_alpha": rational(alpha), "hbar": rational(hbar),
                                    "raw_ground": rational(raw_ground), "raw_excited": rational(raw_excited),
                                    "delta": rational(delta), "centered_normalized_excitation": rational(centered),
                                    "physical_energy": rational(energy), "frequency": rational(frequency)},
        "all_infinite_claims_require_report_proofs": True
    }


def verify_inputs():
    contract_file = HERE / "inputs/research/round28/contracts/aj1.json"
    pack_file = HERE / "inputs/input-pack-freeze.json"
    require(digest(contract_file) == CONTRACT_SHA, "Frozen contract bytes changed")
    require(digest(pack_file) == PACK_SHA, "Frozen input pack bytes changed")
    contract = json.loads(contract_file.read_text())
    require(contract["sequence"] == 7 and contract["loop"] == "aj1", "Wrong investigation")
    require(len(contract["sources"]) == 48, "Source count")
    pack = json.loads(pack_file.read_text())
    for path, expected in pack["bindings"].items():
        require(digest(ROOT/path) == expected, "Input hash mismatch: "+path)
    for path, expected in contract["sources"].items():
        require(digest(HERE/"inputs"/path) == expected, "Contract snapshot mismatch: "+path)
    return {"contract_sha256": CONTRACT_SHA, "input_pack_sha256": PACK_SHA,
            "input_binding_count": len(pack["bindings"]),
            "checker_sha256": digest(Path(__file__).resolve()),
            "algorithm": "independent forward standard-library exact enumeration and rational controls"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), "--output must be absolute")
    require(not out.exists(), "--output must be a fresh nonexistent directory")
    provenance = verify_inputs()
    geometry = geometric_checks()
    gauge = gauge_controls()
    controls = analytic_controls()
    results = {
        "schema": "ym28-aj1-forward-results-v1", "loop": "aj1", "sequence": 7,
        "status": "exact_contract_fixtures_pass; analytic_forward_proof_in_report_pending_independent_review",
        "scope": {"actual_I1_homogeneous_omitted_orthant": True, "all24_links_all21_faces": True,
                  "local_energy_tightness_and_normality": "analytic proof",
                  "physical_cyclic_equals_joint_fixed": "analytic proof",
                  "closed_generator_reducing_restriction": "analytic proof using inherited tested resolvent limit",
                  "tau_star": "positive unevaluated min(c1(S),1/(2c2(S)))/7",
                  "numerical_nonzero_tau_certified": False, "new_gap_constant": False,
                  "nonzero_homogeneous_Wilson_excitation": False, "all_boundary_limits_equal": False,
                  "continuum_yang_mills": False, "AJ2_executed": False},
        "exact_coefficients": {"delta_over_alpha": rational(Q(1,8)),
                               "inherited_normalized_gap": rational(Q(1,2)),
                               "inherited_physical_threshold_over_alpha": rational(Q(1,16)),
                               "M_over_abs_tau": rational(7),
                               "reset_local_energy_per_incident_group_over_M": rational(2),
                               "max_incident_groups_per_site": 4,
                               "local_energy_per_site_over_M_ceiling": rational(8),
                               "local_energy_per_site_over_abs_tau_ceiling": rational(56)},
        "geometry": geometry, "gauge_controls": gauge,
        "discriminating_controls": controls, "provenance": provenance,
        "caveat": "Finite checks audit exact supports, constants and countermodel prefixes. They do not prove local normality, all-volume bounds, source theorems or infinite-dimensional GNS statements."}
    out.mkdir(parents=True, exist_ok=False)
    for name, data in (("results.json", results), ("source-manifest.json", provenance)):
        (out/name).write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print("AJ1 exact fixtures passed; wrote two deterministic source-bound JSON files.")


if __name__ == "__main__":
    main()
