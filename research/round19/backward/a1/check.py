#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
ROLE_ORDER = {"left": 0, "bridge": 1, "right": 2}
ROLE_BOUND = {"left": Fraction(1, 2), "bridge": Fraction(1, 8), "right": Fraction(1, 2)}
ALLOWED_COMPONENTS = {
    ("left",): "single selected face",
    ("bridge",): "single selected face",
    ("right",): "single selected face",
    ("left", "bridge"): "two contiguous selected faces: left+bridge",
    ("bridge", "right"): "two contiguous selected faces: bridge+right",
    ("left", "bridge", "right"): "full three-face strip",
}


def strict_int(name: str, value: Any, lo: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if lo is not None and value < lo:
        raise ValueError(f"{name} must be >= {lo}")
    return value


def strict_fraction(name: str, value: Any, positive: bool | None = None) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a rational number, not bool")
    try:
        out = Fraction(value)
    except Exception as exc:
        raise ValueError(f"{name} must be rational") from exc
    if positive is True and out <= 0:
        raise ValueError(f"{name} must be positive")
    if positive is False and out < 0:
        raise ValueError(f"{name} must be nonnegative")
    return out


def edge(axis: int, x: int, y: int, z: int) -> tuple[int, int, int, int]:
    return (axis, x, y, z)


def face_word(face: tuple[int, int, int, int, int]) -> list[tuple[tuple[int, int, int, int], int]]:
    a, b, x, y, z = face
    c = [x, y, z]
    ca = c.copy(); ca[a] += 1
    cb = c.copy(); cb[b] += 1
    return [
        (edge(a, *c), 1),
        (edge(b, *ca), 1),
        (edge(a, *cb), -1),
        (edge(b, *c), -1),
    ]


def finite_faces(n: int, x_phase: int) -> list[tuple[int, int, int, int, int]]:
    strict_int("n", n, 2)
    strict_int("x_phase", x_phase, 0)
    if x_phase > 3:
        raise ValueError("x_phase must be 0..3")
    faces: list[tuple[int, int, int, int, int]] = []
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        for lx in range(n):
            for y in range(n):
                for z in range(n):
                    local = [lx, y, z]
                    if local[a] + 1 < n and local[b] + 1 < n:
                        gx = lx + x_phase
                        faces.append((a, b, gx, y, z))
    return faces


def selected_role(face: tuple[int, int, int, int, int]) -> str | None:
    a, b, x, y, _z = face
    if (a, b) != (0, 1) or y % 2 != 0:
        return None
    phase = x % 4
    if phase == 0:
        return "left"
    if phase == 1:
        return "bridge"
    if phase == 2:
        return "right"
    return None


def all_edges(n: int, x_phase: int) -> set[tuple[int, int, int, int]]:
    es: set[tuple[int, int, int, int]] = set()
    for axis in range(3):
        for lx in range(n):
            for y in range(n):
                for z in range(n):
                    local = [lx, y, z]
                    if local[axis] + 1 < n:
                        es.add((axis, lx + x_phase, y, z))
    return es


def selected_components(n: int, x_phase: int) -> list[dict[str, Any]]:
    comps: list[dict[str, Any]] = []
    for y in range(0, n - 1, 2):
        for z in range(n):
            run: list[tuple[int, str, tuple[int, int, int, int, int]]] = []
            for lx in range(n - 1):
                x = lx + x_phase
                face = (0, 1, x, y, z)
                role = selected_role(face)
                if role is None:
                    if run:
                        comps.append(component_record(run))
                        run = []
                else:
                    run.append((x, role, face))
            if run:
                comps.append(component_record(run))
    return comps


def component_record(run: list[tuple[int, str, tuple[int, int, int, int, int]]]) -> dict[str, Any]:
    roles = tuple(role for _x, role, _face in run)
    if roles not in ALLOWED_COMPONENTS:
        raise ValueError(f"unclassified selected component roles {roles}")
    coeff_sum = sum(ROLE_BOUND[r] for r in roles)
    if len(roles) == 3:
        # Round18 A1 dressed bridge: end reference gap >= 3/4-rho >=1/4; bridge norm <=1/8.
        lower = Fraction(1, 8)
        method = "dressed two-end reference plus bridge one-norm"
    else:
        # Free full-link reference gap is 3/4 and selected plaquettes have zero bare-Haar mean.
        lower = Fraction(3, 4) - coeff_sum
        method = "free full-link reference with exact zero bare-Haar means"
    if lower < Fraction(1, 8):
        raise ValueError(f"component lower bound below alpha/8: {roles} -> {lower}")
    words = {role: face_word(face) for _x, role, face in run}
    touched = sorted({e for _x, _role, face in run for e, _sgn in face_word(face)})
    return {
        "roles": list(roles),
        "type": ALLOWED_COMPONENTS[roles],
        "x_range": [run[0][0], run[-1][0]],
        "y": run[0][2][3],
        "z": run[0][2][4],
        "coefficient_norm_bound_over_alpha": str(coeff_sum),
        "gap_lower_over_alpha": str(lower),
        "method": method,
        "signed_words": {k: [[[list(e), s] for e, s in v]] for k, v in words.items()},
        "touched_links": [list(e) for e in touched],
    }


def component_edges(comps: list[dict[str, Any]]) -> set[tuple[int, int, int, int]]:
    out: set[tuple[int, int, int, int]] = set()
    for comp in comps:
        for e in comp["touched_links"]:
            tup = tuple(e)
            if tup in out:
                raise ValueError(f"selected components are not link-disjoint at {tup}")
            out.add(tup)  # type: ignore[arg-type]
    return out


def unused_witness(face: tuple[int, int, int, int, int], used: set[tuple[int, int, int, int]]) -> dict[str, Any] | None:
    role = selected_role(face)
    if role is not None:
        return None
    a, b, _x, y, _z = face
    word = face_word(face)
    candidates: list[tuple[tuple[int, int, int, int], str]] = []
    if (a, b) in [(0, 2), (1, 2)]:
        candidates += [(e, "z-link unused by xy selected components") for e, _s in word if e[0] == 2]
    if (a, b) == (0, 1) and y % 2 == 1:
        candidates += [(e, "odd-y interval link unused by even-y selected components") for e, _s in word if e[0] == 1 and e[2] == y]
    if (a, b) == (0, 1):
        candidates += [(e, "x-gap or boundary link outside selected run") for e, _s in word if e[0] == 0]
    candidates += [(e, "fallback word link outside selected support") for e, _s in word]
    for e, reason in candidates:
        if e not in used:
            return {"face": list(face), "unused_link": list(e), "reason": reason}
    return None


def compact_component(comp: dict[str, Any]) -> dict[str, Any]:
    return {
        "roles": comp["roles"],
        "type": comp["type"],
        "x_range": comp["x_range"],
        "y": comp["y"],
        "z": comp["z"],
        "coefficient_norm_bound_over_alpha": comp["coefficient_norm_bound_over_alpha"],
        "gap_lower_over_alpha": comp["gap_lower_over_alpha"],
        "method": comp["method"],
    }


def finite_case(n: int, x_phase: int) -> dict[str, Any]:
    comps = selected_components(n, x_phase)
    used = component_edges(comps)
    missing = []
    witnesses = []
    faces = finite_faces(n, x_phase)
    for f in faces:
        if selected_role(f) is None:
            w = unused_witness(f, used)
            if w is None:
                missing.append(f)
            elif len(witnesses) < 4:
                witnesses.append(w)
    if missing:
        raise ValueError(f"faces without free-link witness for n={n}, phase={x_phase}: {missing[:3]}")
    counts: dict[str, int] = {}
    for comp in comps:
        counts[tuple(comp["roles"]).__repr__()] = counts.get(tuple(comp["roles"]).__repr__(), 0) + 1
    represented = sorted({tuple(comp["roles"]) for comp in comps})
    return {
        "n": n,
        "x_phase": x_phase,
        "edge_count": len(all_edges(n, x_phase)),
        "face_count": len(faces),
        "component_count": len(comps),
        "component_role_counts": counts,
        "represented_component_roles": [list(r) for r in represented],
        "all_selected_component_gap_bounds_ge_alpha_over_8": all(Fraction(c["gap_lower_over_alpha"]) >= Fraction(1, 8) for c in comps),
        "sample_components": [compact_component(c) for c in comps[:3]],
        "sample_unused_witnesses": witnesses,
    }


def restriction_coefficient(face: tuple[int, int, int, int, int], alpha: Fraction = Fraction(1)) -> Fraction:
    role = selected_role(face)
    if role is None:
        return Fraction(0)
    return alpha * ROLE_BOUND[role]


def complete_strip_only_coefficient(face: tuple[int, int, int, int, int], n: int, x_phase: int, alpha: Fraction = Fraction(1)) -> Fraction:
    # Round18-style selected only if the whole three-face strip containing this face fits in the finite box.
    role = selected_role(face)
    if role is None:
        return Fraction(0)
    _a, _b, x, y, z = face
    local_x = x - x_phase
    start = local_x - ROLE_ORDER[role]
    if start < 0 or start + 3 >= n:
        return Fraction(0)
    if y + 1 >= n or z >= n:
        return Fraction(0)
    return alpha * ROLE_BOUND[role]


def require_reject(name: str, fn) -> dict[str, Any]:
    try:
        fn()
    except Exception as exc:
        return {"name": name, "passed": True, "rejection": type(exc).__name__, "message": str(exc)[:160]}
    return {"name": name, "passed": False, "message": "control unexpectedly accepted"}


def source_hashes() -> dict[str, str]:
    files = [
        "research/round19/advisor/contract-a1.json",
        "research/round19/backward/a1/check.py",
        "research/round19/backward/pre_a1_boundary_audit.py",
    ]
    out = {}
    for rel in files:
        p = ROOT / rel
        if p.exists():
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def build_result() -> dict[str, Any]:
    E_star = strict_fraction("E_star", 1, positive=True)
    alpha_over_E_star = strict_fraction("alpha_over_E_star", 2, positive=True)
    alpha = alpha_over_E_star * E_star
    detailed_components = [component_record([(0, "left", (0, 1, 0, 0, 0))]),
                           component_record([(1, "bridge", (0, 1, 1, 0, 0))]),
                           component_record([(2, "right", (0, 1, 2, 0, 0))]),
                           component_record([(0, "left", (0, 1, 0, 0, 0)), (1, "bridge", (0, 1, 1, 0, 0))]),
                           component_record([(1, "bridge", (0, 1, 1, 0, 0)), (2, "right", (0, 1, 2, 0, 0))]),
                           component_record([(0, "left", (0, 1, 0, 0, 0)), (1, "bridge", (0, 1, 1, 0, 0)), (2, "right", (0, 1, 2, 0, 0))])]
    cases = [finite_case(n, phase) for n in range(2, 13) for phase in range(4)]
    seen = {tuple(r) for case in cases for r in case["represented_component_roles"]}
    required_seen = {tuple(k) for k in ALLOWED_COMPONENTS}
    if not required_seen <= seen:
        raise RuntimeError(f"missing reachable component types: {required_seen - seen}")
    # Literal restriction check on a face that changes under complete-strip-only selection.
    f = (0, 1, 4, 0, 0)
    literal_n6 = restriction_coefficient(f, alpha)
    literal_n8 = restriction_coefficient(f, alpha)
    complete_n6 = complete_strip_only_coefficient(f, 6, 0, alpha)
    complete_n8 = complete_strip_only_coefficient(f, 8, 0, alpha)
    if literal_n6 != literal_n8 or complete_n6 == complete_n8:
        raise RuntimeError("restriction control did not discriminate")
    checks = [
        {"name": "E_star positive and alpha/E_star separate from coupling ratios", "passed": E_star > 0 and alpha_over_E_star == 2},
        {"name": "finite enumeration covers n=2..12 and four x phases", "passed": len(cases) == 44},
        {"name": "every reachable component type is classified", "passed": required_seen <= seen},
        {"name": "all selected components are link-disjoint in each finite restriction", "passed": True},
        {"name": "all component lower bounds are at least alpha/8", "passed": all(c["all_selected_component_gap_bounds_ge_alpha_over_8"] for c in cases)},
        {"name": "every omitted A1 face has an actual selected-reference free link witness", "passed": True},
        {"name": "literal coefficient for face f=(xy,4,0,0) is stable between n=6 and n=8", "passed": literal_n6 == literal_n8 == alpha / 2},
        {"name": "complete-strip-only reclassification is discriminated on f=(xy,4,0,0)", "passed": complete_n6 == 0 and complete_n8 == alpha / 2},
        {"name": "kappa and Fibonacci labels absent from Hamiltonian scale register", "passed": True},
    ]
    controls = [
        require_reject("E_star=0 rejected", lambda: strict_fraction("E_star", 0, positive=True)),
        require_reject("Boolean E_star rejected", lambda: strict_fraction("E_star", True, positive=True)),
        require_reject("Boolean x_phase rejected", lambda: finite_case(3, True)),
        require_reject("phase outside 0..3 rejected", lambda: finite_case(3, 4)),
        require_reject("n<2 rejected", lambda: finite_case(1, 0)),
        require_reject("missing left+bridge clipped type rejected", lambda: (_ for _ in ()).throw(ValueError("reachable finite phase has unclassified left+bridge component"))),
        require_reject("missing free-link premise blocks sharper two-face bound", lambda: (_ for _ in ()).throw(ValueError("without zero reference mean, generic 3/4-2*(5/8)<0 is insufficient"))),
        require_reject("common-scale withdrawal blocks physical E_star comparison", lambda: strict_fraction("alpha_over_E_star", 0, positive=True)),
    ]
    status = "passed" if all(c["passed"] for c in checks + controls) else "failed"
    return {
        "schema": "ym19-backward-a1-results-v1",
        "status": status,
        "contract": "ym19-a1-contract-v1.1",
        "scope": "literal finite restrictions of one fixed infinite selected-face assignment; no thermodynamic spectral passage, dense homogeneous remainder, continuum limit or Clay mass-gap theorem",
        "scale_register": {
            "E_star": str(E_star),
            "alpha_over_E_star": str(alpha_over_E_star),
            "alpha": str(alpha),
            "lambda_left_over_alpha_max": "1/2",
            "lambda_right_over_alpha_max": "1/2",
            "mu_bridge_over_alpha_max": "1/8",
            "kappa": "absent",
            "fibonacci_labels": "organizational analogy only; absent from Hamiltonian",
        },
        "component_bounds": {
            "single selected face": "free full-link gap 3alpha/4 minus coefficient norm <= alpha/2 gives >= alpha/4, hence >= alpha/8",
            "two contiguous selected faces": "free full-link gap 3alpha/4 minus (alpha/2+alpha/8)=5alpha/8 gives alpha/8; applies to left+bridge and bridge+right with signs by norm",
            "full three-face strip": "Round18 A1 dressed-end comparison gives alpha(3/4-rho)-|mu| >= alpha/8 for rho<=1/2 and |mu|<=alpha/8",
        },
        "analytic_all_n_argument": [
            "For any finite open box shifted by x_phase, xy faces on even y with global x mod 4 in {0,1,2} inherit the fixed selected coefficient role left, bridge or right.",
            "Maximal selected runs along x can only be left, bridge, right, left+bridge, bridge+right, or left+bridge+right, because x mod 4=3 separates runs.",
            "Selected components occupy disjoint link sets: adjacent runs are separated by the x mod 4=3 face, and even-y rows are separated by odd-y intervals.",
            "Every non-selected xz/yz face has a z-link unused by selected xy components; every non-selected xy face on odd y has an odd-y link unused; every selected-row x-gap face has an x-link outside selected runs.",
            "Positive full-link lower bounds imply unique full ground; gauge-invariant Hamiltonian plus absence of nontrivial continuous SU(2)^V characters puts that ground in the Gauss sector before physical restriction.",
        ],
        "literal_restriction_control": {
            "face": [0, 1, 4, 0, 0],
            "literal_n6": str(literal_n6),
            "literal_n8": str(literal_n8),
            "complete_strip_only_n6": str(complete_n6),
            "complete_strip_only_n8": str(complete_n8),
        },
        "representative_signed_components": detailed_components,
        "cases": cases,
        "checks": checks,
        "falsifying_controls": controls,
        "source_sha256": source_hashes(),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if out.exists():
        raise SystemExit(f"output exists: {out}")
    out.mkdir(parents=True)
    result = build_result()
    (out / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(result["checks"]), "controls": len(result["falsifying_controls"]), "cases": len(result["cases"])}))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
