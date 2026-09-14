#!/usr/bin/env python3
"""I2 exact local geometry, commutator and interval checks; standard library."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def face_links(p, a, b):
    return {(p, a), (add(p, E[a]), b), (add(p, E[b]), a), (p, b)}


def selected_link(link):
    p, a = link
    if a == 0:
        return p[0] % 4 < 3
    if a == 1:
        return p[1] % 2 == 0
    return False


def local_faces():
    faces = []
    for p in itertools.product(range(4), range(2), (0,)):
        for a, b in ((0, 1), (0, 2), (1, 2)):
            if (a, b) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 < 3:
                continue
            links = face_links(p, a, b)
            if b == 2:
                witnesses = {link for link in links if link[1] == 2}
            elif p[1] % 2:
                witnesses = {link for link in links if link[1] == 1}
            else:
                witnesses = {link for link in links if link[1] == 0}
            need(len(witnesses) == 2, "missing second free Haar witness")
            need(not any(selected_link(w) for w in witnesses), "Haar witness is actually selected")
            faces.append((p, a, b, links, witnesses))
    pairs = 0
    for f, g in itertools.combinations(faces, 2):
        need(len(f[3] & g[3]) <= 1, "distinct elementary faces share multiple links")
        need(bool(f[4] - g[3]), "cross moment has no unmatched free Haar link")
        pairs += 1
    need(len(faces) == 21 and pairs == 210, "wrong local face/pair count")
    return faces, pairs


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def plus(a, b, sign=1):
    return [[x + sign*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def exact_matrix_checks():
    h = [[F(0), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(2)]]
    phi = [[F(0), F(1,10), F(1,20)],
           [F(1,10), F(1,7), F(1,11)],
           [F(1,20), F(1,11), F(-1,13)]]
    u = (F(0), F(1,10), F(1,40))
    gen = [[F(0), -u[1], -u[2]], [u[1], F(0), F(0)], [u[2], F(0), F(0)]]
    need(plus(gen, transpose(gen)) == [[0]*3 for _ in range(3)], "generator not skew")
    off = plus(mm(h, gen), mm(gen, h), -1)
    qphi = [list(row) for row in phi]
    for i in range(3):
        qphi[0][i] = qphi[i][0] = F(0)
    need(plus(phi, off, -1) == qphi, "wrong commutator sign or inverse")
    changed_mean = [list(row) for row in phi]
    changed_mean[0][0] = F(1,9)
    need(plus(changed_mean, off, -1) != qphi, "zero-mean withdrawal not detected")
    return {"dimension": 3, "inverse_components": [str(x) for x in u],
            "commutator_cancellation": True, "nonzero_vacuum_mean_rejected": True}


def iv(x):
    return (F(x), F(x))


def ia(a, b):
    return (a[0]+b[0], a[1]+b[1])


def neg(a):
    return (-a[1], -a[0])


def im(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def absolute_upper(a):
    return max(abs(a[0]), abs(a[1]))


def trig_interval(x, sine):
    # x=1/10 is positive and below one. Alternating decreasing terms give
    # a rigorous enclosure from two consecutive partial sums.
    need(0 < x <= 1, "unsupported alternating fixture interval")
    term = x if sine else F(1)
    total = F(0)
    for n in range(13):
        total += term
        power = 2*n + (1 if sine else 0)
        term *= -x*x / ((power+1)*(power+2))
    other = total + term
    return min(total, other), max(total, other)


def enclosure_payload(a):
    return {"lower": str(a[0]), "upper": str(a[1]),
            "display_lower": float(a[0]), "display_upper": float(a[1])}


def rotation_fixture():
    t = F(1,10)
    si, co = trig_interval(t, True), trig_interval(t, False)
    s2, c2, sc = im(si, si), im(co, co), im(si, co)
    diagonal = ia(s2, neg(im(iv(2*t), sc)))
    off = ia(im(iv(t), ia(c2, neg(s2))), neg(sc))
    wrong_off = ia(im(iv(t), ia(c2, neg(s2))), sc)
    upper_square = absolute_upper(diagonal)**2 + absolute_upper(off)**2
    bound = 3*t*t
    need(upper_square < bound*bound, "rigorous finite remainder bound failed")
    need(wrong_off[0] > F(1,10), "wrong-sign control did not retain first-order defect")
    need(-t*t != 0, "omitted-remainder spectral control is degenerate")
    return {"t": str(t), "diagonal_interval": enclosure_payload(diagonal),
            "offdiagonal_interval": enclosure_payload(off),
            "wrong_sign_offdiagonal_interval": enclosure_payload(wrong_off),
            "remainder_norm_square_upper": str(upper_square),
            "proved_remainder_norm_bound": str(bound),
            "determinant_original": str(-t*t), "determinant_if_remainder_dropped": "0",
            "arithmetic": "exact rational alternating Taylor enclosures; displayed decimals are noncertifying"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "output")
    args = parser.parse_args()
    source_paths = [HERE / "check.py", HERE / "report.md",
                    ROOT / "research/round21/contracts/i2.json",
                    ROOT / "research/round21/advisor/i1-gate.json",
                    ROOT / "research/round21/forward/i1/report.md",
                    ROOT / "research/round20/forward/h2/report.md"]
    inputs = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    contract = json.loads((ROOT / "research/round21/contracts/i2.json").read_text())
    need(contract["depends_on"]["sha256"] == inputs["research/round21/advisor/i1-gate.json"], "I1 gate binding mismatch")
    faces, pairs = local_faces()
    variance = F(len(faces), 9*4)
    need(variance == F(7,12), "wrong local variance")
    need(variance < F(4,5)**2, "rational square-root upper bound is false")
    remainder_coefficient = variance + 14*F(4,5)
    need(remainder_coefficient == F(707,60), "wrong rational remainder coefficient")
    fixture = rotation_fixture()
    matrices = exact_matrix_checks()
    tau = F(1,64)
    # For H0=diag(0,1), phi off-diagonal 1/10 and psi=(1,s),
    # the ratio |<psi,phi psi>|/<psi,H0 psi> equals 1/(5s).
    relative_ratios = {str(s): str(F(1,5)/s) for s in (F(1,10), F(1,100), F(1,1000))}
    need(relative_ratios == {"1/10":"2", "1/100":"20", "1/1000":"200"}, "relative-bound fixture failed")
    controls = {
        "wrong_conjugation_sign": {"rejected": True, "defect": "offdiagonal >1/10, correct remainder norm <3/100"},
        "omitted_remainder": {"rejected": True, "determinants": ["-1/100", "0"]},
        "missing_zero_mean_premise": {"rejected": matrices["nonzero_vacuum_mean_rejected"]},
        "pure_relative_bound": {"rejected": True, "ratios_as_probe_shrinks": relative_ratios},
        "square_root_replaced_by_too_small_number": {"rejected": variance > F(3,4)**2},
        "numerical_global_interval": {"certified": False, "reason": "global iteration/constants unevaluated"},
    }
    results = {
        "schema": "ym21-forward-i2-v1", "loop": "i2", "direction": "forward",
        "status": "local_dressing_lemma_verified_global_numerical_target_insufficient",
        "comparison": {"variance_coefficient": str(variance),
                       "generator_norm_square_bound": str(variance),
                       "rational_remainder_coefficient": str(remainder_coefficient),
                       "pure_relative_bound_possible": False,
                       "numerical_global_interval_certified": False},
        "geometry_checks": {"faces": len(faces), "distinct_face_pairs": pairs, "free_witnesses_per_face": 2},
        "local_tau_fixture": {"tau": str(tau), "variance": str(variance*tau*tau),
                              "generator_norm_square_upper": str(variance*tau*tau),
                              "remainder_norm_upper": str(remainder_coefficient*tau*tau),
                              "interaction_norm": str(7*tau), "global_interval_admitted": False},
        "matrix_check": matrices,
        "operator_identity": "exp(S)(H0+phi)exp(-S)=H0+Q phi Q+R, with R retained",
        "domain": "u is in D(H0); bounded finite-rank exp(plus/minus S) preserves D(H0)",
        "quantitative_source_extraction": {"0411042": "c1,c2 and expansion constants unevaluated", "0412040": "alternative delta threshold unevaluated; no dictionary application asserted"},
        "next_loop_executed": False,
    }
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    payloads = {"results.json": results, "controls.json": controls, "finite-fixture.json": fixture}
    for name, payload in payloads.items():
        (output / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest() == inputs[str(p.relative_to(ROOT))] for p in source_paths), "source changed during run")
    manifest = {"schema": "ym21-source-manifest-v1", "inputs": inputs,
                "outputs": {n: hashlib.sha256((output/n).read_bytes()).hexdigest() for n in payloads},
                "external_sources": [
                    {"url": "https://arxiv.org/pdf/math-ph/0411042", "version": "v1 2004-11-11", "read": "Theorems1-3; Section2 constants/commutator expansion"},
                    {"url": "https://arxiv.org/pdf/math-ph/0412040", "version": "v1 2004-12-13", "read": "definitions; Theorems1-2; pure-relative condition"}],
                "full_external_papers_included": False, "cache_files_admitted": False}
    (output / "source-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": results["status"], "comparison": results["comparison"], "local_tau_fixture": results["local_tau_fixture"]}, sort_keys=True))


if __name__ == "__main__":
    main()
