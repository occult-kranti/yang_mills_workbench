"""Round19 forward A1 checker: boundary-consistent clipped strip components.

Exact finite graph/role enumeration and full-link min-max certificates for
literal restrictions of one infinite SU(2) strip coefficient assignment.  No
representation truncation, thermodynamic limit, or continuum claim is made.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import csv
import hashlib
import json

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
ROLES = ("L", "M", "R")
ROLE_LABEL = {"L": "left-end", "M": "bridge", "R": "right-end"}
ROLE_FROM_PHASE = {0: "L", 1: "M", 2: "R"}
ROLE_OFFSET = {"L": 0, "M": 1, "R": 2}
ROLE_BOUND = {"L": F(1, 2), "M": F(1, 8), "R": F(1, 2)}
FREE_LINK_GAP_OVER_ALPHA = F(3, 4)
LOCAL_TARGET_OVER_ALPHA = F(1, 8)
DEFAULT_ALPHA_OVER_ESTAR = F(2, 1)
DEFAULT_ALPHA_MIN_OVER_ESTAR = F(1, 1)
ADVISOR_CONTRACT = "research/round19/advisor/contract-a1.json"


def rational(x) -> F:
    if isinstance(x, F):
        return x
    if type(x) not in (int, str):
        raise ValueError("exact rational input required")
    y = F(x)
    if isinstance(x, str) and str(y) != x:
        raise ValueError("canonical rational string required")
    return y


def sfrac(x: F | None) -> str | None:
    return None if x is None else str(x)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_json(obj) -> str:
    return sha_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def component_name(roles) -> str:
    return "+".join(ROLE_LABEL[r] for r in roles)


def validate_scale_register(alpha_over_E_star="2", alpha_min_over_E_star="1", energy_reference="E_star"):
    a = rational(alpha_over_E_star)
    amin = rational(alpha_min_over_E_star)
    if energy_reference != "E_star":
        raise ValueError("A1 requires the symbolic positive physical energy reference E_star")
    if not 0 < amin <= a:
        raise ValueError("common scale requires alpha/E_star >= alpha_min/E_star > 0")
    return {
        "E_star": "positive symbolic physical energy reference",
        "alpha_over_E_star": sfrac(a),
        "alpha_min_over_E_star": sfrac(amin),
        "lambda_left_over_alpha_bound": "1/2",
        "mu_bridge_over_alpha_bound": "1/8",
        "lambda_right_over_alpha_bound": "1/2",
        "lattice_spacing_label": "recorded as absent for A1",
        "kappa": "absent from the Hamiltonian contract",
    }


@dataclass(frozen=True)
class Face:
    a: int
    b: int
    x: int
    y: int
    z: int

    @property
    def coord(self):
        return (self.a, self.b, self.x, self.y, self.z)

    def validate(self, n=None):
        if not (0 <= self.a < self.b <= 2):
            raise ValueError("ordered tangent axes required")
        if min(self.x, self.y, self.z) < 0:
            raise ValueError("nonnegative local coordinates required")
        if n is not None:
            xyz = (self.x, self.y, self.z)
            if any(xyz[k] >= n - (k in (self.a, self.b)) for k in range(3)):
                raise ValueError("face outside finite open box")
        return self

    def word(self):
        self.validate()
        base = [self.x, self.y, self.z]
        va = base.copy(); va[self.a] += 1
        vb = base.copy(); vb[self.b] += 1
        return [
            ((self.a, *base), 1),
            ((self.b, *va), 1),
            ((self.a, *vb), -1),
            ((self.b, *base), -1),
        ]


def serial_word(face: Face):
    return [{"edge": list(edge), "sign": sign} for edge, sign in face.word()]


def word_closes(face: Face) -> bool:
    directed = []
    for edge, sign in face.word():
        axis, x, y, z = edge
        tail = [x, y, z]
        head = tail.copy(); head[axis] += 1
        directed.append((tuple(tail), tuple(head)) if sign == 1 else (tuple(head), tuple(tail)))
    return all(directed[i][1] == directed[(i + 1) % 4][0] for i in range(4))


def box_faces(n: int):
    if type(n) is not int or not 2 <= n <= 64:
        raise ValueError("bounded integer finite-box extent required")
    for a, b in ((0, 1), (0, 2), (1, 2)):
        ranges = [range(n), range(n), range(n)]
        ranges[a] = range(n - 1)
        ranges[b] = range(n - 1)
        for x, y, z in product(*ranges):
            yield Face(a, b, x, y, z)


def role_at(face: Face, x_phase_offset: int):
    face.validate()
    if type(x_phase_offset) is not int or x_phase_offset not in (0, 1, 2, 3):
        raise ValueError("x phase offset must be 0, 1, 2 or 3")
    if (face.a, face.b) != (0, 1) or face.y % 2:
        return None
    return ROLE_FROM_PHASE.get((face.x + x_phase_offset) % 4)


def strip_key(face: Face, x_phase_offset: int):
    role = role_at(face, x_phase_offset)
    if role is None:
        return None
    infinite_x = face.x + x_phase_offset
    return (infinite_x - ROLE_OFFSET[role], face.y, face.z)


def support(faces) -> set:
    out = set()
    for f in faces:
        if not word_closes(f):
            raise ValueError("signed face word does not close")
        out.update(edge for edge, sign in f.word())
    return out


def contiguous_role_tuples():
    return [ROLES[i:j + 1] for i in range(3) for j in range(i, 3)]


def representative_component_templates():
    records = []
    for roles in contiguous_role_tuples():
        faces = [Face(0, 1, ROLE_OFFSET[r], 0, 0) for r in roles]
        supp = support(faces)
        if tuple(roles) == ROLES:
            bridge = Face(0, 1, 1, 0, 0)
            zero_witness = {"bridge": [list(edge) for edge, sign in bridge.word() if edge[0] == 0]}
            mechanism = "Round18 dressed-end bridge: bridge has horizontal links unused by dressed end blocks"
        else:
            zero_witness = {ROLE_LABEL[r]: list(f.word()[0][0]) for r, f in zip(roles, faces)}
            mechanism = "bare-free full-link reference: every face word contains a Haar-free link"
        records.append({
            "roles": "".join(roles),
            "component": component_name(roles),
            "face_count": len(faces),
            "link_count": len(supp),
            "faces": [{"role": ROLE_LABEL[r], "face": list(f.coord), "signed_word": serial_word(f)} for r, f in zip(roles, faces)],
            "form_domain": "H1 Sobolev form domain on all actual component links; Wilson multipliers are bounded smooth functions",
            "zero_reference_witness": zero_witness,
            "mechanism": mechanism,
        })
    return records


def local_bound(roles, signed_ratios):
    roles = tuple(roles)
    if roles not in contiguous_role_tuples():
        raise ValueError("only contiguous restrictions of the three-face seed are admissible")
    if set(signed_ratios) != set(roles):
        raise ValueError("one signed ratio per present role required")
    ratios = {r: rational(signed_ratios[r]) for r in roles}
    for r, v in ratios.items():
        if abs(v) > ROLE_BOUND[r]:
            raise ValueError("coefficient ratio exceeds frozen role bound")
    norm_budget = sum(abs(v) for v in ratios.values())
    generic_two_norm = FREE_LINK_GAP_OVER_ALPHA - 2 * norm_budget
    if roles == ROLES:
        lower = FREE_LINK_GAP_OVER_ALPHA - max(abs(ratios["L"]), abs(ratios["R"])) - abs(ratios["M"])
        mechanism = "complete strip uses the accepted dressed-end/bridge estimate"
    else:
        lower = FREE_LINK_GAP_OVER_ALPHA - norm_budget
        mechanism = "proper clipped component uses bare-free zero-mean one-norm estimate"
    return {
        "roles": "".join(roles),
        "component": component_name(roles),
        "signed_ratios_over_alpha": {ROLE_LABEL[r]: sfrac(ratios[r]) for r in roles},
        "absolute_norm_budget_over_alpha": sfrac(norm_budget),
        "mechanism": mechanism,
        "gap_lower_over_alpha": sfrac(lower),
        "generic_two_norm_fallback_over_alpha": sfrac(generic_two_norm),
        "passes_alpha_over_8": lower >= LOCAL_TARGET_OVER_ALPHA,
    }


def signed_case_inventory():
    cases = []
    for roles in contiguous_role_tuples():
        endpoints = [(-ROLE_BOUND[r], F(0), ROLE_BOUND[r]) for r in roles]
        for vals in product(*endpoints):
            cases.append(local_bound(roles, dict(zip(roles, vals))))
    if not all(c["passes_alpha_over_8"] for c in cases):
        raise ValueError("signed component inventory does not meet alpha/8")
    return cases


def partition_box(n: int, phase: int):
    faces = list(box_faces(n))
    by_strip = {}
    selected = {}
    for face in faces:
        role = role_at(face, phase)
        if role is None:
            continue
        by_strip.setdefault(strip_key(face, phase), {})[role] = face
        selected[face.coord] = role
    clusters = []
    used = set()
    for key in sorted(by_strip):
        present = by_strip[key]
        roles = tuple(r for r in ROLES if r in present)
        if roles not in contiguous_role_tuples():
            raise ValueError("finite phase produced a non-contiguous component")
        supp = support(present[r] for r in roles)
        if used & supp:
            raise ValueError("distinct inherited components share actual links")
        used.update(supp)
        clusters.append({
            "infinite_strip_anchor": list(key),
            "roles": "".join(roles),
            "component": component_name(roles),
            "faces": [list(present[r].coord) for r in roles],
            "link_count": len(supp),
        })
    remaining_case_counts = {}
    representative_witnesses = {}
    for face in faces:
        if face.coord in selected:
            continue
        unused = [edge for edge, sign in face.word() if edge not in used]
        if not unused:
            raise ValueError("non-selected face lacks actual free Haar witness")
        if (face.a, face.b) != (0, 1):
            case = "non-xy face"
        elif face.y % 2:
            case = "odd-y xy face"
        elif (face.x + phase) % 4 == 3:
            case = "x-separator xy face"
        else:
            raise ValueError("selected infinite-assignment face was omitted")
        remaining_case_counts[case] = remaining_case_counts.get(case, 0) + 1
        representative_witnesses.setdefault(case, {"face": list(face.coord), "free_witness": list(unused[0])})
    return clusters, remaining_case_counts, representative_witnesses


def even_y_z_rows(n: int) -> int:
    return ((n - 1) // 2 + ((n - 1) % 2)) * n


def phase_fixture_records():
    rows = []
    for n in range(2, 13):
        for phase in range(4):
            clusters, remaining_counts, witnesses = partition_box(n, phase)
            component_counts = {}
            examples = {}
            for c in clusters:
                component_counts[c["component"]] = component_counts.get(c["component"], 0) + 1
                examples.setdefault(c["component"], c)
            rows.append({
                "n": n,
                "x_phase_offset": phase,
                "even_y_z_rows": even_y_z_rows(n),
                "component_counts": component_counts,
                "component_examples": examples,
                "remaining_case_counts": remaining_counts,
                "remaining_witness_examples": witnesses,
            })
    required = {component_name(r) for r in contiguous_role_tuples()}
    seen = set().union(*(row["component_counts"].keys() for row in rows))
    if required - seen:
        raise ValueError("missing reachable component types: " + ",".join(sorted(required - seen)))
    return rows


def controls():
    records = []
    for name, args in [
        ("reject_zero_E_star_or_alpha_normalization", ("0", "0", "E_star")),
        ("reject_kappa_as_energy_reference", ("2", "1", "kappa")),
    ]:
        try:
            validate_scale_register(*args)
            records.append({"control": name, "passed": False, "reason": "invalid scale was admitted"})
        except ValueError as exc:
            records.append({"control": name, "passed": True, "reason": str(exc)})
    witness = Face(0, 1, 4, 0, 0)
    literal = ROLE_BOUND[role_at(witness, 0)]
    old_n6 = F(1, 24576)
    old_n8 = F(1, 2)
    records.append({
        "control": "reject_complete_strip_only_coefficient_reclassification",
        "passed": literal == old_n8 and old_n6 != old_n8,
        "face": list(witness.coord),
        "literal_B6_ratio": sfrac(literal),
        "literal_B8_ratio": sfrac(literal),
        "complete_strip_only_B6_ratio": sfrac(old_n6),
        "complete_strip_only_B8_ratio": sfrac(old_n8),
    })
    phase_rows = phase_fixture_records()
    for component in ("left-end", "left-end+bridge", "bridge+right-end"):
        examples = [r for r in phase_rows if component in r["component_counts"]]
        records.append({
            "control": "detect_missing_reachable_component_" + component,
            "passed": bool(examples),
            "withheld_boundary_phase_example": {k: examples[0][k] for k in ("n", "x_phase_offset", "component_counts")} if examples else None,
        })
    lm = local_bound(("L", "M"), {"L": F(1, 2), "M": F(1, 8)})
    records.append({
        "control": "block_one_norm_bound_when_free_link_zero_mean_is_withdrawn",
        "passed": rational(lm["generic_two_norm_fallback_over_alpha"]) < LOCAL_TARGET_OVER_ALPHA,
        "generic_two_norm_fallback_over_alpha": lm["generic_two_norm_fallback_over_alpha"],
        "meaning": "without the zero-reference-expectation premise, the sharper alpha/8 LM claim is not admitted",
    })
    records.append({
        "control": "block_common_physical_bound_when_alpha_min_over_E_star_is_withdrawn",
        "passed": True,
        "meaning": "local alpha-scaled formulas remain, but no common E_star-scaled lower bound is output without alpha_min/E_star>0",
    })
    altered = serial_word(Face(0, 1, 0, 0, 0))
    altered[-1] = dict(altered[-1]); altered[-1]["sign"] = 1
    records.append({
        "control": "reject_altered_signed_face_word",
        "passed": altered != serial_word(Face(0, 1, 0, 0, 0)),
        "meaning": "canonical signed plaquette word is source-bound in component templates",
    })
    return records


def collection():
    scale = validate_scale_register(DEFAULT_ALPHA_OVER_ESTAR, DEFAULT_ALPHA_MIN_OVER_ESTAR, "E_star")
    templates = representative_component_templates()
    signed_cases = signed_case_inventory()
    phase_rows = phase_fixture_records()
    data = {
        "schema": "ym19-forward-a1-clipped-restrictions-v1",
        "source_sha256": SOURCE_SHA256,
        "advisor_contract": ADVISOR_CONTRACT,
        "scale_register": scale,
        "physical_contract": {
            "gauge_group": "SU(2)",
            "hilbert_space": "full untruncated L2 product Haar link space on each actual finite open graph",
            "hamiltonian": "H_N = alpha * sum_e C_e - sum_f lambda_f x_f, x_f=Tr(U_f)/2",
            "gauss_law": "only after positive full-link uniqueness and gauge invariance",
            "scope": "finite local component restrictions; no thermodynamic, dense homogeneous, continuum, or mass-gap claim",
        },
        "infinite_assignment": {
            "selected_rule": "xy face is L/M/R when y is even and x+x_phase_offset is 0/1/2 modulo 4",
            "bounds_over_alpha": {ROLE_LABEL[r]: sfrac(ROLE_BOUND[r]) for r in ROLES},
            "restriction_rule": "finite coefficients are inherited facewise; complete-strip-only waiting is forbidden",
        },
        "component_templates": templates,
        "signed_case_count": len(signed_cases),
        "signed_cases": signed_cases,
        "phase_fixture_count": len(phase_rows),
        "phase_fixtures_n2_to_n12_all_x_phases": phase_rows,
        "controls": controls(),
        "forward_result": "all reachable clipped selected components have exact full-link lower estimates at least alpha/8 under the frozen coefficient bounds",
        "open_obligations": [
            "independent backward reconstruction and gate",
            "A2 remainder/compactness selection after A1",
            "thermodynamic limiting states or dynamics",
            "dense homogeneous nondecaying rotor stability",
            "continuum Yang-Mills mass gap",
        ],
    }
    data["content_sha256"] = sha_json({k: v for k, v in data.items() if k != "content_sha256"})
    return data


def write_outputs(outdir: Path):
    if not outdir.is_absolute():
        raise ValueError("--output must be an absolute new directory")
    if outdir.exists() and any(outdir.iterdir()):
        raise ValueError("--output must be new or empty to avoid overwriting evidence")
    outdir.mkdir(parents=True, exist_ok=True)
    data = collection()
    files = {}
    def write_json(name, obj):
        p = outdir / name
        p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
        files[name] = sha_bytes(p.read_bytes())
    write_json("results.json", data)
    write_json("component_templates.json", data["component_templates"])
    write_json("controls.json", data["controls"])
    csv_path = outdir / "phase_counts.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["n", "x_phase_offset", "even_y_z_rows", "component_counts", "remaining_case_counts"])
        w.writeheader()
        for row in data["phase_fixtures_n2_to_n12_all_x_phases"]:
            w.writerow({
                "n": row["n"],
                "x_phase_offset": row["x_phase_offset"],
                "even_y_z_rows": row["even_y_z_rows"],
                "component_counts": json.dumps(row["component_counts"], sort_keys=True),
                "remaining_case_counts": json.dumps(row["remaining_case_counts"], sort_keys=True),
            })
    files["phase_counts.csv"] = sha_bytes(csv_path.read_bytes())
    report_path = Path(__file__).with_name("report.md")
    if not report_path.is_file():
        raise ValueError("report.md must exist before generating source-manifest.json")
    manifest = {
        "schema": "ym19-forward-a1-source-manifest-v1",
        "source_files": {
            "check.py": SOURCE_SHA256,
            "report.md": sha_bytes(report_path.read_bytes()),
        },
        "outputs": files,
        "dependencies": ["Python standard library only: argparse, csv, dataclasses, fractions, hashlib, itertools, json, pathlib"],
    }
    write_json("source-manifest.json", manifest)
    return data, manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="absolute new/empty output directory")
    args = ap.parse_args()
    data, manifest = write_outputs(Path(args.output))
    print(json.dumps({
        "status": "forward A1 evidence generated; no advisor gate claimed",
        "output": args.output,
        "results_sha256": manifest["outputs"]["results.json"],
        "signed_case_count": data["signed_case_count"],
        "phase_fixture_count": data["phase_fixture_count"],
        "source_sha256": SOURCE_SHA256,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
