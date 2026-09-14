"""Round19 forward A1: exact clipped-strip restrictions from one infinite assignment.

This is a local/full-link certificate generator, not a finite representation
truncation and not a thermodynamic spectral construction.  It enumerates the
nonempty contiguous restrictions of one infinite three-face strip seed and the
canonical open-box boundary cases induced by restricting that seed to B_n.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
ROLES = ("L", "M", "R")
ROLE_OFFSET = {"L": 0, "M": 1, "R": 2}
ROLE_BOUND = {"L": F(1, 2), "M": F(1, 8), "R": F(1, 2)}
FREE_LINK_GAP_OVER_ALPHA = F(3, 4)
TARGET_LOCAL_GAP_OVER_ALPHA = F(1, 8)
DEFAULT_TAU = F(1, 64)


def q(x) -> F:
    if isinstance(x, F):
        return x
    if type(x) not in (int, str):
        raise ValueError("exact rational input required")
    y = F(x)
    if isinstance(x, str) and str(y) != x:
        raise ValueError("canonical rational string required")
    return y


def fstr(x: F | None) -> str | None:
    return None if x is None else str(x)


def contiguous_subsets():
    """All nonempty interval intersections with the ordered strip [L,M,R]."""
    out = []
    for i in range(3):
        for j in range(i, 3):
            out.append(ROLES[i : j + 1])
    return out


def proper_cluster_bound(roles, magnitudes):
    """Bare-free min-max bound for a proper clipped cluster.

    H0 is alpha times the sum of SU(2) link Casimirs on every actual link in
    the clipped face union.  Its full-link vacuum is the constant function and
    its first nonconstant energy is 3 alpha / 4.  Every retained Wilson face
    multiplier has Haar-vacuum mean zero.  Hence E0(H)<=0 and
    E1(H)>=3alpha/4-alpha*sum |kappa_f|.
    """
    budget = sum(abs(magnitudes[r]) for r in roles)
    return FREE_LINK_GAP_OVER_ALPHA - budget, budget


def full_strip_bound(magnitudes):
    """Use the accepted Round18 A1 three-face mechanism for the complete strip."""
    end_ratio = max(abs(magnitudes["L"]), abs(magnitudes["R"]))
    bridge_ratio = abs(magnitudes["M"])
    dressed_end_gap = FREE_LINK_GAP_OVER_ALPHA - end_ratio
    return dressed_end_gap - bridge_ratio, end_ratio + bridge_ratio + abs(magnitudes["R"])


def mechanism_for(roles):
    return "dressed-end plus conditional-Haar bridge" if tuple(roles) == ROLES else "bare-free clipped cluster"


def local_case(roles, signs):
    if tuple(roles) not in contiguous_subsets():
        raise ValueError("only contiguous clipped strip restrictions are admissible")
    if set(signs) != set(roles):
        raise ValueError("one sign per present role required")
    if any(s not in (-1, 0, 1) for s in signs.values()):
        raise ValueError("signs must be -1, 0 or 1")
    magnitudes = {r: ROLE_BOUND[r] * signs.get(r, 0) for r in ROLES}
    if tuple(roles) == ROLES:
        lower, norm_budget = full_strip_bound(magnitudes)
        bare_lower, bare_budget = proper_cluster_bound(roles, magnitudes)
        note = "bare-free norm is insufficient at the nonzero endpoint; use Round18 A1"
    else:
        lower, norm_budget = proper_cluster_bound(roles, magnitudes)
        bare_lower, bare_budget = lower, norm_budget
        note = "proper clipping has total norm at most 5/8, so the free gap leaves at least 1/8"
    return {
        "roles": "".join(roles),
        "signs": {r: signs[r] for r in roles},
        "mechanism": mechanism_for(roles),
        "magnetic_norm_budget_over_alpha": fstr(norm_budget),
        "bare_free_lower_over_alpha": fstr(bare_lower),
        "certified_lower_over_alpha": fstr(lower),
        "passes_alpha_over_8_local_target": lower >= TARGET_LOCAL_GAP_OVER_ALPHA,
        "note": note,
    }


def enumerate_signed_local_cases():
    cases = []
    for roles in contiguous_subsets():
        for signs_tuple in product((-1, 0, 1), repeat=len(roles)):
            signs = dict(zip(roles, signs_tuple))
            cases.append(local_case(roles, signs))
    if not cases or not all(c["passes_alpha_over_8_local_target"] for c in cases):
        raise ValueError("a clipped signed local case failed the alpha/8 target")
    return cases


@dataclass(frozen=True)
class Face:
    a: int
    b: int
    x: int
    y: int
    z: int

    def validate(self, n=None):
        if not (0 <= self.a < self.b <= 2):
            raise ValueError("ordered tangent axes required")
        if min(self.x, self.y, self.z) < 0:
            raise ValueError("nonnegative orthant coordinates required")
        if n is not None:
            coords = (self.x, self.y, self.z)
            if any(coords[k] >= n - (k in (self.a, self.b)) for k in range(3)):
                raise ValueError("face outside the open box")
        return self

    @property
    def normal(self):
        return ({0, 1, 2} - {self.a, self.b}).pop()

    @property
    def base(self):
        return (self.x, self.y, self.z)

    def word_edges(self):
        self.validate()
        coords = [self.x, self.y, self.z]
        def edge(axis, base):
            return (axis, *base)
        va = coords.copy(); va[self.a] += 1
        vb = coords.copy(); vb[self.b] += 1
        return [
            (edge(self.a, coords), 1),
            (edge(self.b, va), 1),
            (edge(self.a, vb), -1),
            (edge(self.b, coords), -1),
        ]


def box_faces(n):
    if type(n) is not int or n < 2 or n > 64:
        raise ValueError("bounded exact box extent required")
    for a, b in ((0, 1), (0, 2), (1, 2)):
        ranges = [range(n), range(n), range(n)]
        ranges[a] = range(n - 1)
        ranges[b] = range(n - 1)
        for x, y, z in product(*ranges):
            yield Face(a, b, x, y, z)


def strip_role(face: Face):
    face.validate()
    if (face.a, face.b) != (0, 1):
        return None
    if face.y % 2:
        return None
    r = face.x % 4
    if r in (0, 1, 2):
        return ROLES[r]
    return None


def strip_anchor(face: Face):
    role = strip_role(face)
    if role is None:
        return None
    return (face.x - ROLE_OFFSET[role], face.y, face.z)


def face_weight(face: Face):
    face.validate()
    return F(1, 24 * (1 << sum(face.base)))


def cluster_support(faces):
    support = set()
    for face in faces:
        support.update(edge for edge, sign in face.word_edges())
    return support


def canonical_box_partition(n):
    faces = list(box_faces(n))
    by_anchor = {}
    for face in faces:
        role = strip_role(face)
        if role is not None:
            by_anchor.setdefault(strip_anchor(face), {})[role] = face
    clusters = []
    occupied = set()
    for anchor in sorted(by_anchor):
        role_map = by_anchor[anchor]
        roles = tuple(r for r in ROLES if r in role_map)
        # In the positive-orthant boxes used in Round18, actual clipped strips
        # are prefixes.  The local theorem separately covers translated-window
        # suffixes R and MR.
        if roles not in (("L",), ("L", "M"), ROLES):
            raise ValueError(f"unexpected canonical clipped role set {roles}")
        support = cluster_support(role_map[r] for r in roles)
        if occupied & support:
            raise ValueError("distinct restricted infinite strips share links")
        occupied.update(support)
        clusters.append({"anchor": list(anchor), "roles": "".join(roles), "face_count": len(roles), "link_count": len(support)})
    remaining = []
    selected_faces = {role_map[r] for role_map in by_anchor.values() for r in role_map}
    for face in faces:
        if face in selected_faces:
            continue
        unused = [edge for edge, sign in face.word_edges() if edge not in occupied]
        if not unused:
            raise ValueError("remaining face lacks an actual free Haar witness")
        if (face.a, face.b) != (0, 1):
            case = "non-xy face with z-directed free witness"
        elif face.y % 2:
            case = "odd-y xy face with odd-y free witness"
        elif face.x % 4 == 3:
            case = "x-separator xy face with horizontal free witness"
        else:
            raise ValueError("a strip face was left as remainder; coefficient jump reintroduced")
        remaining.append({"face": [face.a, face.b, face.x, face.y, face.z], "case": case, "witness": list(unused[0]), "weight": fstr(face_weight(face))})
    return {"n": n, "clusters": clusters, "remaining": remaining, "occupied_link_count": len(occupied)}


def canonical_counts_formula(n):
    if type(n) is not int or n < 2:
        raise ValueError("integer n>=2 required")
    y_pairs = (n + 0) // 2 if n % 2 == 0 else (n - 1) // 2
    # equivalently ceil((n-1)/2) xy rows with even lower y
    y_pairs = (n - 1 + 1) // 2
    z_layers = n
    q, r = divmod(n, 4)
    # full anchors at 0,4,...,4(q-1), plus terminal prefix for r=2,3.
    full = q * y_pairs * z_layers
    one = (1 if r == 2 else 0) * y_pairs * z_layers
    two = (1 if r == 3 else 0) * y_pairs * z_layers
    return {"L": one, "LM": two, "LMR": full, "total_nonempty_restricted_strips": full + one + two}


def restriction_stability_witness():
    """Known Round18 jump removed by the infinite assignment.

    Face (0,1,4,0,0), equivalently old f2:4,0,0, exists in B_6 and B_8.
    Complete-strip-only scheduling changed it from remainder to cluster.  The
    infinite role assignment gives role L in both boxes.
    """
    f = Face(0, 1, 4, 0, 0)
    return {
        "face": [f.a, f.b, f.x, f.y, f.z],
        "role_in_B6": strip_role(f),
        "role_in_B8": strip_role(f),
        "same_coefficient_for_every_box_containing_face": strip_role(f) == "L",
        "canonical_ratio_bound": fstr(ROLE_BOUND["L"]),
    }


def total_remainder_weight_upper(n):
    part = canonical_box_partition(n)
    return sum((q(row["weight"]) for row in part["remaining"]), F(0))


def exact_collection():
    local_cases = enumerate_signed_local_cases()
    boxes = []
    for n in range(2, 13):
        p = canonical_box_partition(n)
        counts = {k: 0 for k in ("L", "LM", "LMR")}
        for c in p["clusters"]:
            counts[c["roles"]] += 1
        formula = canonical_counts_formula(n)
        if any(counts[k] != formula[k] for k in counts):
            raise ValueError("canonical clipped-count formula mismatch")
        boxes.append({
            "n": n,
            "cluster_type_counts": counts,
            "formula_counts": formula,
            "remaining_case_counts": {case: sum(r["case"] == case for r in p["remaining"]) for case in sorted({r["case"] for r in p["remaining"]})},
            "remaining_weight": fstr(total_remainder_weight_upper(n)),
        })
    # Non-occurring controls: these must not be admitted as clipped restrictions
    # of the ordered three-face seed.
    rejected = []
    for roles in [("L", "R"), ("L", "M", "R", "extra")]:
        try:
            local_case(roles, {r: 1 for r in roles})
        except ValueError as exc:
            rejected.append({"roles": "".join(roles), "rejected": True, "reason": str(exc)})
    return {
        "schema": "ym19-forward-a1-clipped-restrictions-v0",
        "source_sha256": SOURCE_SHA256,
        "physical_contract": {
            "group": "SU(2)",
            "hilbert_space": "full untruncated L2 of actual finite link set with normalized Haar; Gauss restriction only after a positive full-space bound",
            "electric_scale": "alpha times every actual link Casimir, with alpha >= alpha_min > 0 for common physical statements",
            "strip_seed": "one infinite ordered xy three-face seed with role bounds |L|,|R|<=alpha/2 and |M|<=alpha/8",
            "claim_status": "local finite restriction formulas only; no thermodynamic state, dense homogeneous bound or continuum limit claimed",
        },
        "local_signed_case_count": len(local_cases),
        "local_signed_cases": local_cases,
        "canonical_box_fixtures": boxes,
        "restriction_stability_witness": restriction_stability_witness(),
        "rejected_non_restrictions": rejected,
        "proposed_with_summable_remainder": {
            "tau": fstr(DEFAULT_TAU),
            "norm_upper_over_alpha": fstr(DEFAULT_TAU),
            "formal_gap_lower_over_alpha_if_remainder_free-link_gate_passes": fstr(TARGET_LOCAL_GAP_OVER_ALPHA - DEFAULT_TAU),
            "common_physical_lower_if_alpha_ge_alpha_min": "7*alpha_min/64",
            "status": "proposed next check, not accepted gate",
        },
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="output/clipped_restrictions_results.json")
    args = ap.parse_args()
    data = exact_collection()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "wrote": str(out),
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "local_signed_case_count": data["local_signed_case_count"],
        "box_fixture_count": len(data["canonical_box_fixtures"]),
        "status": "proposal evidence generated; no gate claimed",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
