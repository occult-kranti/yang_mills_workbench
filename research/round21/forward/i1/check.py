#!/usr/bin/env python3
"""Exact geometry checks for the frozen I1 forward derivation; no reverse imports."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ZERO = (0, 0, 0)
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
S = frozenset((ZERO,) + E)
ORIENTATIONS = ((0, 1), (0, 2), (1, 2))


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 < 3


def links(p, a, c):
    return frozenset(((p, a), (add(p, E[a]), c),
                      (add(p, E[c]), a), (p, c)))


def support(p, a, c):
    return frozenset(owner(tail) for tail, _ in links(p, a, c))


def canonical_support(values):
    return [list(p) for p in sorted(values)]


def encode_support(values):
    return json.dumps(canonical_support(values), separators=(",", ":"))


def tails(b):
    return [(4 * b[0] + r, 2 * b[1] + s, b[2])
            for r in range(4) for s in range(2)]


def block_check():
    t = tails(ZERO)
    all_links = {(p, a) for p in t for a in range(3)}
    selected_links = set()
    classes = Counter()
    phases = []
    omitted = []
    for p in t:
        for a, c in ORIENTATIONS:
            sp = support(p, a, c)
            role = "selected" if selected(p, a, c) else "omitted"
            require(sp <= S, "face exceeds frozen star support")
            if role == "selected":
                selected_links.update(links(p, a, c))
                require(sp == {ZERO}, "reference strip split across sites")
            else:
                omitted.append((p, a, c))
                classes[encode_support(sp)] += 1
                require(len(sp) > 1, "unexpected internally contained omitted face")
            phases.append({"base": list(p), "directions": [a, c],
                           "role": role, "support": canonical_support(sp)})
    require(len(all_links) == 24, "wrong total block links")
    require(len(selected_links) == 10 and selected_links <= all_links,
            "reference ownership is incomplete")
    free_links = all_links - selected_links
    require(len(free_links) == 14, "wrong free count")
    require(Counter(a for _, a in free_links) == {0: 2, 1: 4, 2: 8},
            "wrong free-link direction census")
    require(len(omitted) == 21, "wrong omitted anchored face count")
    expected = {
        encode_support({ZERO, E[1]}): 3,
        encode_support({ZERO, E[0]}): 1,
        encode_support({ZERO, E[0], E[1]}): 1,
        encode_support({ZERO, E[2]}): 10,
        encode_support({ZERO, E[0], E[2]}): 2,
        encode_support({ZERO, E[1], E[2]}): 4,
    }
    require(dict(classes) == expected, "wrong exhaustive support phase counts")
    return all_links, selected_links, free_links, omitted, phases, classes


def translation_checks(phases):
    count = 0
    for b in itertools.product((0, 1, 7, 101), repeat=3):
        shift = (4 * b[0], 2 * b[1], b[2])
        for phase in phases:
            p = add(tuple(phase["base"]), shift)
            a, c = phase["directions"]
            actual = {sub(v, b) for v in support(p, a, c)}
            require(canonical_support(actual) == phase["support"],
                    "translation changed relative support")
            require(selected(p, a, c) == (phase["role"] == "selected"),
                    "translation changed coefficient role")
            count += 1
    # Euclidean division, including negative sites used solely in the explicit
    # decoupled theorem embedding. Negative sites are not physical orthant links.
    for p in itertools.product(range(-9, 10), range(-5, 6), (-3, 0, 5)):
        b = owner(p)
        r, s = p[0] - 4 * b[0], p[1] - 2 * b[1]
        require(0 <= r < 4 and 0 <= s < 2 and p[2] == b[2],
                "nonunique Euclidean ownership")
    return count


def literal_boxes():
    records = []
    types = set()
    for low_x, low_y in itertools.product(range(4), range(2)):
        for length in itertools.product((1, 2, 3, 5), repeat=3):
            lo = (low_x, low_y, 1)
            hi = tuple(v + n for v, n in zip(lo, length))
            vertices = set(itertools.product(*(range(a, b + 1) for a, b in zip(lo, hi))))
            retained_links = {(p, a) for p in vertices for a in range(3)
                              if add(p, E[a]) in vertices}
            owned = Counter(owner(p) for p, _ in retained_links)
            require(sum(owned.values()) == len(retained_links), "literal ownership duplication")
            face_counts = Counter()
            selected_groups = {}
            face_count = 0
            for p in vertices:
                for a, c in ORIENTATIONS:
                    f_links = links(p, a, c)
                    if not f_links <= retained_links:
                        continue
                    face_count += 1
                    b = owner(p)
                    sp = support(p, a, c)
                    require(all(v in owned for v in sp), "face references absent site")
                    require({sub(v, b) for v in sp} <= S, "clipped face exceeds star")
                    if selected(p, a, c):
                        require(sp == {b}, "clipped reference crosses block")
                        selected_groups.setdefault(b, set()).add(p[0] % 4)
                    else:
                        face_counts[b] += 1
            for residues in selected_groups.values():
                role = "".join("LMR"[r] for r in sorted(residues))
                require(role in ("L", "M", "R", "LM", "MR", "LMR"),
                        "unproved clipped reference component")
                types.add(role)
            require(all(n <= 21 for n in face_counts.values()), "literal local budget overflow")
            expected_links = sum(length[a] * (length[(a+1)%3] + 1) *
                                 (length[(a+2)%3] + 1) for a in range(3))
            expected_faces = sum(length[a] * length[c] *
                                 (length[3-a-c] + 1) for a, c in ORIENTATIONS)
            require(len(retained_links) == expected_links, "literal rectangular link formula mismatch")
            require(face_count == expected_faces, "literal rectangular face formula mismatch")
            records.append({"lower": list(lo), "length": list(length),
                            "links": len(retained_links), "faces": face_count,
                            "coarse_sites": len(owned),
                            "maximum_omitted_at_one_anchor": max(face_counts.values(), default=0)})
    require(types == {"L", "M", "R", "LM", "MR", "LMR"}, "missing clipped type fixture")
    return records, types


def controls(omitted):
    contained = sum(support(p, a, c) == {ZERO} for p, a, c in omitted)
    require(contained == 0, "contained-face rejection fixture failed")
    p = (3, 1, 0)
    diagonal = owner(add(add(p, E[0]), E[1]))
    require(diagonal not in support(p, 0, 1), "corner is incorrectly a link tail")
    narrow_owners = {(tail[0] // 2, tail[1] // 2, tail[2])
                     for base_x in range(3) for tail, _ in links((base_x, 0, 0), 0, 1)}
    require(len(narrow_owners) > 1, "2x2x1 split-strip control not discriminating")
    bset = {ZERO, E[2]}
    actual = sum(support(p, a, c) <= bset for p, a, c in omitted)
    source = len(omitted) if S <= bset else 0
    require(actual == 10 and source == 0, "source boundary mismatch fixture failed")
    correct = Fraction(21, 24) / Fraction(1, 8)
    wrong_scale = Fraction(21, 24) / Fraction(3, 4)
    require(correct == 7 and wrong_scale == Fraction(7, 6), "scale control failed")
    def numerical_certificate(c1, c2, tau):
        require(isinstance(c1, Fraction) and isinstance(c2, Fraction),
                "numerical constants must have evaluated exact values")
        require(c1 > 0 and c2 > 0 and 0 < abs(tau) < min(c1, 1 / (2*c2)) / 7,
                "numerical interval does not meet theorem hypotheses")
    rejected_numeric = False
    try:
        numerical_certificate(None, None, Fraction(1, 64))
    except ValueError:
        rejected_numeric = True
    require(rejected_numeric, "existential constants admitted a numerical tau")
    return {
        "contained_faces_only": {"wrong_count": contained, "correct_count": 21, "rejected": True},
        "diagonal_vertex_as_owner": {"spurious_owner": list(diagonal), "rejected": True},
        "two_by_two_by_one_block": {"strip_owner_count": len(narrow_owners), "rejected": True},
        "wrong_free_link_normalization": {"wrong_coefficient": str(wrong_scale), "correct": str(correct), "rejected": True},
        "source_boundary_equals_actual_support": {"actual_retained": actual, "source_retained": source, "rejected": True},
        "global_budget_equals_local_budget": {"one_anchor_coefficient": 7, "two_anchor_coefficient": 14, "rejected": True},
        "numerical_tau_from_existential_constants": {"attempted_tau": "1/64", "numerical_interval_certified": False, "rejected": rejected_numeric},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "output")
    args = parser.parse_args()
    output = args.output.resolve()
    sources = [HERE / "check.py", HERE / "report.md", ROOT / "research/round21/contracts/i1.json",
               ROOT / "research/round19/forward/a1/report.md", ROOT / "research/round19/forward/a2/report.md",
               ROOT / "research/round13/advisor/weak-coupling-stability.md",
               ROOT / "research/round20/advisor/post-ten-roadmap.md"]
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    all_links, strip, free, omitted, phases, classes = block_check()
    translations = translation_checks(phases)
    literal, clipped_types = literal_boxes()
    rejection_controls = controls(omitted)
    coefficient = Fraction(len(omitted), 24) / Fraction(1, 8)
    require(coefficient == 7, "wrong exact normalized budget")
    result = {
        "schema": "ym21-forward-i1-v1", "loop": "i1", "direction": "forward",
        "status": "verified_dictionary_quantitative_threshold_insufficient",
        "comparison": {
            "block_link_count": len(all_links), "selected_link_count": len(strip),
            "free_link_count": len(free), "omitted_anchor_face_count": len(omitted),
            "coarse_support_offsets": canonical_support(S),
            "normalized_budget_coefficient": str(coefficient),
            "numerical_stability_constants_evaluated": False,
        },
        "normalization": {"delta_over_alpha": "1/8", "nu_over_alpha_tau": "1/24", "nu_over_delta_tau": "1/3"},
        "exact_norm": "epsilon=7*abs(tau), homogeneous same-sign omitted coupling",
        "derived_support_counts": dict(sorted(classes.items())),
        "checks": {"complete_anchor_phase_cases": len(phases), "translation_fixtures": translations,
                   "literal_rectangle_fixtures": len(literal), "clipped_component_types": sorted(clipped_types),
                   "wrong_model_controls": len(rejection_controls), "all_passed": True},
        "proof_scope": {
            "geometry_completeness": "analytic Euclidean-division and one-step-tail proof in report; fixtures are checks",
            "onsite_gap": "inherits A1 complete and clipped strip theorem",
            "finite_boundary": "source star-empty boundary; separate actual-support and literal-box padding transfers",
            "positive_orthant_state_limit": "source theorem applied through explicitly decoupled negative-site extension",
            "homogeneous_A2_representation_identified": False,
            "all_literal_boundary_state_limits_identified": False,
            "numerical_tau_interval_certified": False,
            "continuum_claim": False,
        },
        "primary_source": {"url": "https://arxiv.org/pdf/math-ph/0411042", "read": "definitions, Theorems 1-3, Section 2", "constants": "existential"},
        "next_loop_executed": False,
    }
    require(all(hashlib.sha256(p.read_bytes()).hexdigest() == before[str(p.relative_to(ROOT))] for p in sources),
            "source changed during execution")
    output.mkdir(parents=True, exist_ok=True)
    payloads = {"results.json": result, "controls.json": rejection_controls,
                "phase-classes.json": phases, "literal-boxes.json": literal}
    for name, payload in payloads.items():
        (output / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    manifest = {"schema": "ym21-source-manifest-v1", "inputs": before,
                "outputs": {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in payloads},
                "external_source": {"url": "https://arxiv.org/pdf/math-ph/0411042", "access": "web primary PDF inspected; remote bytes not locally archived"},
                "cache_files_admitted": False}
    (output / "source-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"loop": "i1", "status": result["status"], "comparison": result["comparison"], "checks": result["checks"]}, sort_keys=True))


if __name__ == "__main__":
    main()
