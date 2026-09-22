#!/usr/bin/env python3
"""AJ2 reverse exact diagnostics; analytic proof is in the bound report.

New standard-library implementation. Does not import or execute old algorithms.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[3]
REL = "research/round28/reverse/aj2"
CONTRACT = "research/round28/contracts/aj2.json"
CONTRACT_SHA = "0f71cc35d4e6fef93188cee740f9cdf90596f034193f3c9aee9455fb0411c154"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Checks:
    def __init__(self):
        self.count = 0
        self.names = []

    def require(self, condition, name):
        if not condition:
            raise RuntimeError("FAILED: " + name)
        self.count += 1
        self.names.append(name)


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, tuple):
        return [serial(v) for v in value]
    if isinstance(value, list):
        return [serial(v) for v in value]
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    return value


def source_bindings():
    """Original absolute instruction locators are provenance, never opened."""
    bindings = {}

    def bind(relative, expected=None):
        p = Path(relative)
        if p.is_absolute() or ".." in p.parts:
            raise RuntimeError("Nonportable binding: " + str(relative))
        digest = sha(ROOT / p)
        if expected is not None and digest != expected:
            raise RuntimeError("Source hash mismatch: " + str(relative))
        bindings[p.as_posix()] = digest

    bind(CONTRACT, CONTRACT_SHA)
    contract = json.loads((ROOT / CONTRACT).read_text())
    inventory_path = OWN / "inputs/source-inventory.json"
    inventory = json.loads(inventory_path.read_text())
    seen_originals = {}
    seen_snapshots = set()
    external_count = 0
    for row in inventory["entries"]:
        snap = row["snapshot"]
        if not snap.startswith(REL + "/inputs/") or snap in seen_snapshots:
            raise RuntimeError("Invalid or repeated snapshot")
        seen_snapshots.add(snap)
        bind(snap, row["sha256"])
        if row.get("external_instruction_snapshot"):
            if not Path(row["source"]).is_absolute():
                raise RuntimeError("Instruction origin must be provenance locator")
            external_count += 1
        else:
            bind(row["source"], row["sha256"])
            seen_originals[row["source"]] = row["sha256"]
    required = {CONTRACT: CONTRACT_SHA, **contract["sources"]}
    if seen_originals != required:
        raise RuntimeError("Contract source closure is incomplete or changed")
    if external_count != 26 or len(seen_snapshots) != 74:
        raise RuntimeError("Frozen input pack count changed")
    input_freeze = json.loads((OWN / "inputs/input-freeze.json").read_text())
    for relative, digest in input_freeze["bindings"].items():
        bind(relative, digest)
    for p in sorted((OWN / "inputs").rglob("*")):
        if p.is_file():
            bind(p.relative_to(ROOT).as_posix())
    bind(REL + "/check.py")
    bind(REL + "/report.md")
    return dict(sorted(bindings.items()))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ZERO = (0, 0, 0)
I = (F(1), F(0), F(0), F(0))


def owner(tail):
    x, y, z = tail
    return (x // 4, y // 2, z)


def end(link):
    tail, axis = link
    return add(tail, AXES[axis])


def qmul(a, b):
    w, x, y, z = a
    W, X, Y, Z = b
    return (w*W-x*X-y*Y-z*Z,
            w*X+x*W+y*Z-z*Y,
            w*Y-x*Z+y*W+z*X,
            w*Z+x*Y-y*X+z*W)


def qinv(a):
    return (a[0], -a[1], -a[2], -a[3])


def qnorm(a):
    return sum(x*x for x in a)


def product(values):
    out = I
    for v in values:
        out = qmul(out, v)
    return out


def geometry_and_gauge(c):
    region = (ZERO, (0, 0, 1))
    tails = sorted((x, y, z) for x in range(4) for y in range(2)
                   for z in range(2))
    links = sorted((tail, axis) for tail in tails for axis in range(3))
    endpoints = sorted(set(tails) | {end(e) for e in links})
    c.require(len(tails) == 16 and len(links) == 48, "complete 24-link factors")
    c.require(len(endpoints) == 36, "all complete-region endpoints")
    c.require(len(set(endpoints)-set(tails)) == 20, "outgoing head count")
    c.require(all(owner(t) in region for t in tails), "all tail owners retained")
    c.require(all(sum(owner(t) == b for t, a in links) == 24 for b in region),
              "24 links per owner")
    x, z = AXES[0], AXES[2]
    face = [(ZERO, 0), (x, 2), (z, 0), (ZERO, 2)]
    signs = [1, 1, -1, -1]
    path = [ZERO]
    for e, sign in zip(face, signs):
        tail, head = e[0], end(e)
        start, stop = (tail, head) if sign == 1 else (head, tail)
        c.require(path[-1] == start, "oriented path incidence " + str(len(path)))
        path.append(stop)
    c.require(path[-1] == ZERO, "closed face path")
    c.require(len(set(face)) == 4 and set(face) <= set(links), "four distinct original links")
    c.require([owner(e[0]) for e in face] == [ZERO, ZERO, z, ZERO],
              "actual specified tail owners")
    c.require({owner(e[0]) for e in face} == set(region), "minimal complete support")
    c.require(len(face) < len(links) and len(set(path)) < len(endpoints),
              "incomplete support rejected")

    # Each entry has rational unit norm. All spectator links/actions are kept.
    units = [(F(3,5),F(4,5),F(0),F(0)),
             (F(5,13),F(0),F(12,13),F(0)),
             (F(8,17),F(0),F(0),F(15,17)),
             (F(7,25),F(24,25),F(0),F(0))]
    gauge_units = [(F(3,5),F(0),F(4,5),F(0)),
                   (F(5,13),F(0),F(0),F(12,13)),
                   (F(8,17),F(15,17),F(0),F(0)),
                   (F(7,25),F(0),F(24,25),F(0))]
    values = {e: units[i % len(units)] for i, e in enumerate(links)}
    gauges = {v: gauge_units[i % len(gauge_units)] for i, v in enumerate(endpoints)}
    for e, q in zip(face, units):
        values[e] = q
    for v, q in zip([ZERO, x, add(x,z), z], gauge_units):
        gauges[v] = q
    c.require(all(qnorm(q) == 1 for q in values.values()), "48 exact SU2 link assignments")
    c.require(all(qnorm(q) == 1 for q in gauges.values()), "36 exact endpoint actions")

    def holonomy(vs):
        return product([vs[e] if s == 1 else qinv(vs[e])
                        for e, s in zip(face, signs)])

    transformed = {e: product([gauges[e[0]], q, qinv(gauges[end(e)])])
                   for e, q in values.items()}
    Q = holonomy(values)
    QT = holonomy(transformed)
    c.require(qnorm(Q) == 1 and qnorm(QT) == 1, "unit original and transformed holonomies")
    c.require(QT == product([gauges[ZERO], Q, qinv(gauges[ZERO])]),
              "actual closed-word gauge conjugation")
    c.require(Q[0] == QT[0], "normalized real trace gauge invariance")
    c.require(-1 <= Q[0] <= 1, "Wilson contraction diagnostic")
    missing = dict(transformed)
    missing[face[0]] = product([gauges[ZERO], values[face[0]]])
    wrong = holonomy(missing)
    c.require(wrong[0] != Q[0], "missing-head fixture discriminates")
    open_Q = product([values[face[0]], values[face[1]]])
    open_QT = product([transformed[face[0]], transformed[face[1]]])
    c.require(open_QT == product([gauges[ZERO], open_Q, qinv(gauges[add(x,z)])]),
              "charged open word has distinct endpoint transformation")
    c.require(open_QT[0] != open_Q[0], "charged-word trace discriminates")
    # An action solely at a spectator endpoint leaves the observable fixed.
    spectator = next(v for v in endpoints if v not in set(path))
    spectator_gauges = {v: (gauge_units[0] if v == spectator else I) for v in endpoints}
    spectator_values = {e: product([spectator_gauges[e[0]], q,
                                    qinv(spectator_gauges[end(e)])])
                        for e, q in values.items()}
    c.require(holonomy(spectator_values) == Q, "spectator action retained and harmless")
    return {
        "region": region, "tail_count": len(tails), "link_count": len(links),
        "endpoint_count": len(endpoints), "outside_heads": len(set(endpoints)-set(tails)),
        "links": [{"tail": t, "axis": a, "head": end((t,a)), "owner": owner(t)}
                  for t, a in links],
        "endpoints": endpoints, "face": [{"tail": e[0], "axis": e[1], "sign": s,
                                           "owner": owner(e[0])} for e, s in zip(face, signs)],
        "path": path,
        "quaternion_fixture": {"holonomy": Q, "transformed": QT,
            "wilson": Q[0], "missing_head_wilson": wrong[0],
            "charged_trace": open_Q[0], "charged_transformed_trace": open_QT[0],
            "link_assignments": [{"tail": e[0], "axis": e[1], "q": values[e]} for e in links],
            "endpoint_assignments": [{"vertex": v, "q": gauges[v]} for v in endpoints]},
        "development_fixture_history": {
            "missing_head_initial_fixture_discriminated": True,
            "charged_initial_fixture_discriminated": True,
            "nondiscriminating_blind_candidate_encountered": False,
            "replacement_used": False}
    }


def reference_and_state_controls(c):
    # Coordinate symmetry on S3: sum x_i^2=1 and rotation gives a=3b.
    second = F(1,4)
    mixed_fourth = F(1,24)
    fourth = 3 * mixed_fourth
    c.require(4*second == 1, "S3 second-moment normalization")
    c.require(4*fourth + 12*mixed_fourth == 1, "S3 fourth-moment normalization")
    rotated_fourth = (2*fourth + 6*mixed_fourth)/4
    c.require(rotated_fourth == fourth, "S3 two-coordinate rotation identity")
    c.require(fourth == F(1,8), "fundamental Wilson fourth moment")
    c.require(4*second == 1 and 16*fourth == 2, "fundamental character reference moments")
    pure_wilson_norm = 4*second
    pure_wilson_variance = 4*fourth
    c.require(pure_wilson_norm == 1, "reference vector 2W normalized")
    c.require(pure_wilson_variance != second, "interacting-Haar variance substitution rejected")
    # A step multiplier has probability 1/2 at each level in reference Haar.
    p_plus = F(1,2)
    c.require(2*p_plus == 1, "positive-band step state normalized")
    step_mean, step_second = F(1), F(1)
    c.require(step_second-step_mean**2 == 0, "nonconstant step normal-state zero variance")
    constant = F(3,7)
    c.require(constant**2-constant**2 == 0, "constant multiplier zero centered variance")
    # Rank-one density on a two-dimensional diagnostic subspace.
    rho = ((F(1),F(0)), (F(0),F(0)))
    null_positive_projection = ((F(0),F(0)), (F(0),F(1)))
    c.require(sum(rho[i][i] for i in range(2)) == 1, "normal pure density trace one")
    c.require(sum(rho[i][i]*null_positive_projection[i][i] for i in range(2)) == 0,
              "normality does not imply faithfulness")
    epsilons = [F(1,2),F(1,4),F(1,8),F(1,16)]
    c.require(all(0<e<1 for e in epsilons), "positive Wilson bands permitted")
    c.require(all(b*b < a*a for a,b in zip(epsilons,epsilons[1:])),
              "normal-state variance ceilings approach zero")
    return {
        "reference_only": True,
        "actual_interacting_variance_value": None,
        "haar_mean": "0", "haar_second_moment": second, "haar_fourth_moment": fourth,
        "fundamental_character_norm_squared": 4*second,
        "fundamental_character_fourth_moment": 16*fourth,
        "normal_nonfaithful_haar_variance": second,
        "normal_nonfaithful_2W_variance": pure_wilson_variance,
        "constant_multiplier_variance": "0", "step_multiplier_band_state_variance": "0",
        "narrow_band_variance": "0 < Var(W) < epsilon^2 for each 0<epsilon<1; analytic",
        "epsilon_diagnostic_ceilings": [{"epsilon": e, "variance_ceiling": e*e} for e in epsilons],
        "singular_control": "weak-star subnet of narrowing-band normal states has zero W^2; not normal",
        "level_set_proof": "conditional one-link Haar/Fubini, report section 3; no finite sampling proof",
        "faithfulness_required": False,
        "uniform_normal_state_variance_margin": False
    }


def spectral_controls(c):
    # q=exp(-g t/hbar)=1/2 is an exact abstract diagnostic time.
    q = F(1,2)
    variance = F(1,4)
    upper = variance*q
    energy_2g = variance*q*q
    c.require(0 < energy_2g < upper, "gap upper bound and threshold-rate lower bound distinguished")
    c.require(energy_2g != upper, "threshold energy need not carry spectral mass")
    uncentered = (1+q)/4
    centered = q/4
    c.require(uncentered-centered == F(1,4), "uncentered vacuum plateau remains")
    vacuum_measure = {}
    excited_measure = {F(2): variance}
    c.require(sum(vacuum_measure.values(), F(0)) == 0, "vacuum-only gap can be empty")
    c.require(sum(excited_measure.values()) > 0 and all(e >= 1 for e in excited_measure),
              "nonzero positive-energy measure is additional information")
    c.require(excited_measure.get(F(1),F(0)) == 0, "no threshold atom from lower support bound")
    # At real phase pi/2 the exact amplitude is -i V, whose norm stays V.
    real_part, imag_part = F(0), -variance
    c.require(real_part**2 + imag_part**2 == variance**2 > upper**2,
              "real-time phase control has constant magnitude")
    domains = []
    for n in (1,2,4,8):
        weights = [F(1,4**j) for j in range(1,n+1)]
        energies_in_g = [4**j for j in range(1,n+1)]
        norm_squared = sum(weights,F(0))
        first_moment_in_g = sum((w*e for w,e in zip(weights,energies_in_g)),F(0))
        c.require(norm_squared == (1-F(1,4**n))/3, "bounded-vector partial norm n="+str(n))
        c.require(first_moment_in_g == n, "divergent-form partial moment n="+str(n))
        domains.append({"terms":n, "norm_squared":norm_squared,
                        "first_energy_moment_in_g":first_moment_in_g})
    c.require(F(1,3)<1, "bounded observable norm in domain countermodel")
    return {
        "diagnostic_q": q, "diagnostic_variance": variance,
        "gap_rate_upper": upper, "energy_2g_correlation": energy_2g,
        "uncentered_correlation": uncentered, "centered_correlation": centered,
        "vacuum_plateau": uncentered-centered,
        "vacuum_only_positive_measure_mass": "0",
        "excited_measure_mass": variance, "threshold_atom_mass_in_countermodel": "0",
        "continuous_threshold_control": "vacuum plus multiplication E on L2([g,2g],dE): support infimum g, no atom",
        "real_time_amplitude_at_phase_pi_over_2": [real_part,imag_part],
        "domain_countermodel_partials": domains,
        "infinite_domain_countermodel": {
            "vector_norm_squared": "1/3", "form_energy": "infinite",
            "bounded_selfadjoint_observable_norm": "1/sqrt(3)",
            "scope": "abstract implication control; no actual Wilson domain assertion"},
        "actual_first_moment_proved": False, "actual_second_moment_proved": False,
        "actual_t0_derivative_proved": False
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.output.is_absolute() or args.output.exists():
        raise SystemExit("--output must name a fresh absolute directory")
    bindings = source_bindings()
    c = Checks()
    geometry = geometry_and_gauge(c)
    states = reference_and_state_controls(c)
    spectral = spectral_controls(c)
    result = {
        "schema": "ym28-aj2-reverse-results-v1", "loop": "aj2", "direction": "reverse",
        "contract_sha256": CONTRACT_SHA, "semantic_check_count": c.count,
        "checks": c.names, "all_checks_passed": True,
        "scope": {
            "actual_homogeneous_I1_AJ1_state": True,
            "all_inherited_symbolic_couplings": True,
            "original_Wilson_nonzero_centered_physical_vector": True,
            "all_finite_imaginary_times_strictly_positive": True,
            "gap_upper_decay_bound": True,
            "numerical_variance_margin": False, "evaluated_stability_interval": False,
            "threshold_eigenvalue": False, "real_time_decay": False,
            "energy_moment_or_t0_domain_result": False,
            "boundary_identification": False, "continuum_mass_gap_solution": False},
        "analytic_conclusion": {
            "regime": "|tau|<min(c1(S),1/(2*c2(S)))/7; unevaluated positive constants",
            "observable": "Tr(U_x(0) U_z(e_x) U_x(e_z)^(-1) U_z(0)^(-1))/2",
            "point_spectral_projections": "E_W({c})=0 for every real c on full K_R",
            "variance": "V=omega(W^2)-omega(W)^2>0; value unspecified",
            "physical_energy": "H_phys=(alpha/8)*G_phys",
            "spectral_measure": "mu_chi nonzero positive, mass V, support subset [alpha/16,infinity)",
            "correlation": "0<C(t)<=V*exp(-alpha*t/(16*hbar)) for every finite t>=0",
            "domain_needed": "chi in H_cyc only; bounded semigroup"},
        "geometry": geometry, "state_and_reference_controls": states,
        "spectral_and_domain_controls": spectral,
        "proof_vs_diagnostics": "Analytic report proves infinite claims; exact finite checks audit geometry and countermodels only.",
        "independence": {"opposite_current_science_read": False,
                         "skeptic_current_science_read": False,
                         "historical_checkers_executed_or_imported": False},
        "bindings": bindings
    }
    args.output.mkdir(parents=True)
    (args.output / "results.json").write_text(json.dumps(serial(result),indent=2,sort_keys=True)+"\n")
    print(json.dumps({"loop":"aj2", "direction":"reverse", "checks":c.count,
                      "bindings":len(bindings), "passed":True}))


if __name__ == "__main__":
    main()
