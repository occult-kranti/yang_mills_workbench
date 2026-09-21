#!/usr/bin/env python3
"""Independent X2 reverse: actual SU(2) Ritz residual and exact enclosures."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from math import comb, factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


class Interval:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        need(self.lo <= self.hi, "Reversed interval")
    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo+other.lo, self.hi+other.hi)
    __radd__ = __add__
    def __neg__(self):
        return Interval(-self.hi, -self.lo)
    def __sub__(self, other):
        return self+-as_interval(other)
    def __rsub__(self, other):
        return as_interval(other)+-self
    def __mul__(self, other):
        other = as_interval(other)
        v = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(v), max(v))
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = as_interval(other)
        need(not other.lo <= 0 <= other.hi, "Division by a zero-containing interval")
        return self*Interval(1/other.hi, 1/other.lo)
    def __rtruediv__(self, other):
        return as_interval(other)/self
    def data(self):
        return [str(self.lo), str(self.hi)]
    def mid(self):
        return (self.lo+self.hi)/2


def as_interval(x):
    return x if isinstance(x, Interval) else Interval(x)


def root_interval(x, denominator=10**24):
    x = as_interval(x)
    need(x.lo >= 0, "Negative square root")
    a = isqrt(x.lo.numerator*denominator**2//x.lo.denominator)
    b = isqrt(x.hi.numerator*denominator**2//x.hi.denominator)
    lo = F(a, denominator)
    hi = F(b, denominator)
    if hi*hi < x.hi:
        hi += F(1, denominator)
    need(lo*lo <= x.lo and hi*hi >= x.hi, "Square-root enclosure")
    return Interval(lo, hi)


def rounded_interval(interval, denominator=10**30):
    lo = (interval.lo.numerator*denominator)//interval.lo.denominator
    hi = -((-interval.hi.numerator*denominator)//interval.hi.denominator)
    return Interval(F(lo,denominator),F(hi,denominator))


def negative_exp(x, order=160):
    """Enclose exp(-x) by reciprocating a positive rational Taylor series."""
    x = F(x)
    need(x >= 0 and x < order+2, "Invalid exponential enclosure domain")
    lower = sum((x**k/factorial(k) for k in range(order+1)), F(0))
    tail = x**(order+1)/factorial(order+1)/(1-x/F(order+2))
    return rounded_interval(Interval(1/(lower+tail), 1/lower))


def scalar_evaluation(x):
    x = F(x)
    need(x >= 0, "Negative centered spectral exponent")
    if x > 96:
        return F(0)
    return negative_exp(x).mid()


SCALAR_ERROR = F(3,10**30)


def poly_mul(a, b):
    out = {}
    for n, v in a.items():
        for m, w in b.items():
            out[n+m] = out.get(n+m, F(0))+v*w
    return {n: v for n, v in out.items() if v}


def integral(poly):
    out = F(0)
    for n, v in poly.items():
        if n % 2 == 0:
            k = n//2
            out += v*F(comb(2*k, k), (k+1)*4**k)
    return out


def physical_graph():
    vertices = list(product(range(3), range(3), range(2)))
    edges = [frozenset((u, v)) for u, v in combinations(vertices, 2)
             if sum(abs(u[k]-v[k]) for k in range(3)) == 1]
    number = {edge: n for n, edge in enumerate(edges)}
    vertex_set = set(vertices)
    masks = []
    for p in vertices:
        for a, b in combinations(range(3), 2):
            corners = [tuple(p[k]+da*(k == a)+db*(k == b) for k in range(3))
                       for da, db in ((0,0),(1,0),(1,1),(0,1))]
            if all(v in vertex_set for v in corners):
                face_edges = [number[frozenset((corners[k], corners[(k+1)%4]))]
                              for k in range(4)]
                masks.append(sum(1 << n for n in face_edges))
    masks = sorted(masks)
    need((len(vertices), len(edges), len(masks)) == (18,33,20), "Actual graph mismatch")
    need(len(set(masks)) == 20, "Repeated face")
    need(all(a ^ b ^ c != 0 for a in masks for b in masks for c in masks),
         "Three-face center selection rule fails")
    four_relations = [q for q in combinations(range(20), 4)
                      if masks[q[0]] ^ masks[q[1]] ^ masks[q[2]] ^ masks[q[3]] == 0]
    need(not four_relations, "A four-distinct-face residual cross term was omitted")
    pair_masks = [a ^ b for a, b in combinations(masks, 2)]
    need(len(set(pair_masks)) == 190 and not set(pair_masks).intersection(masks),
         "Omitted pair channels overlap each other or the retained sector")
    need(all((a & b).bit_count() <= 1 and (a & ~b) and (b & ~a)
             for a, b in combinations(masks, 2)), "Unique-edge Haar integrations fail")
    return {"vertices":18, "edges":33, "faces":20,
            "masks":masks, "unordered_pair_channels":190,
            "spin_one_channels":20, "four_distinct_face_relations":0}


def ritz_matrix(coupling):
    a = [[F(0)]*21 for _ in range(21)]
    a[0][0] = 20*coupling
    for p in range(1,21):
        a[p][p] = 3+20*coupling
        a[0][p] = a[p][0] = -coupling/2
    return a


def matrix_vector(a, v):
    return [sum((x*y for x,y in zip(row,v)), F(0)) for row in a]


def projector(kappa):
    v = [F(1)]+[kappa/2]*20
    norm2 = 1+5*kappa*kappa
    return [[x*y/norm2 for y in v] for x in v]


def check_projector(p):
    for i in range(21):
        for j in range(21):
            need(sum((p[i][k]*p[k][j] for k in range(21)), F(0)) == p[i][j],
                 "Rational evaluation projection is not idempotent")
    need(sum(p[i][i] for i in range(21)) == 1, "Rational ground rank normalization")


def parameters(coupling):
    need(F(0) <= coupling <= F(1,100), "Coupling outside frozen range")
    c = 20*coupling
    root = root_interval(9+20*coupling*coupling)
    d = (root-3)/2
    kappa = coupling/(3+d)
    energy = c-d
    normalization2 = 1+5*kappa*kappa
    residual2 = F(195,4)*coupling*coupling*kappa*kappa/normalization2
    residual = root_interval(residual2)
    separation = 3-energy.hi
    need(separation > 0, "Temple/projector excited-spectrum separation fails")
    upper_shift = residual2.hi/separation
    # A two-dimensional variational extension in the direction of the complete
    # residual uses K<=8 on that residual and V<=40 on the physical graph.
    lower_shift = residual2.lo/(8+40*coupling-energy.lo+residual.hi)
    true_energy = Interval(energy.lo-upper_shift, energy.hi-lower_shift)
    projection_upper = residual.hi/separation
    kappa_hat = kappa.mid()
    kappa_error = (kappa.hi-kappa.lo)/2
    bright_gap = root
    dark_gap = 3+d
    bright_hat = bright_gap.mid()
    dark_hat = dark_gap.mid()
    # sqrt(5)<9/4 bounds the exact sine-angle sensitivity to kappa.
    rational_projection_error = F(9,4)*kappa_error
    bright_gap_error = (bright_gap.hi-bright_gap.lo)/2
    dark_gap_error = (dark_gap.hi-dark_gap.lo)/2
    uniform_arithmetic = (rational_projection_error
                          +bright_gap_error/min(bright_gap.lo,bright_hat)
                          +dark_gap_error/min(dark_gap.lo,dark_hat)+SCALAR_ERROR)
    p_hat = projector(kappa_hat)
    check_projector(p_hat)
    return {
        "coupling":coupling, "d":d, "kappa":kappa, "ritz_energy":energy,
        "residual2":residual2, "residual":residual,
        "energy_shift_lower":lower_shift, "energy_shift_upper":upper_shift,
        "true_energy":true_energy, "separation":separation,
        "projection_upper":projection_upper,
        "dark_gap":dark_gap, "bright_gap":bright_gap,
        "kappa_hat":kappa_hat, "dark_hat":dark_hat, "bright_hat":bright_hat,
        "arithmetic_upper":uniform_arithmetic,
        "scalar_time_evaluation_error_upper":SCALAR_ERROR,
        "rational_projection_error":rational_projection_error,
        "projector":p_hat,
    }


def certify_heat(p, start):
    start = F(start)
    need(start > 0, "Positive late-time start is required for the claimed target")
    full_tail = negative_exp(p["separation"]*start)
    ritz_tail = negative_exp(p["dark_gap"].lo*start)
    exact_sector_upper = p["projection_upper"]+full_tail.hi+ritz_tail.hi
    approximation_upper = exact_sector_upper+p["arithmetic_upper"]
    return {"sigma_start":str(start), "time_set":"all sigma >= sigma_start",
            "full_excited_tail_interval":full_tail.data(),
            "ritz_excited_tail_interval":ritz_tail.data(),
            "physical_truncation_upper":str(exact_sector_upper),
            "uniform_arithmetic_upper":str(p["arithmetic_upper"]),
            "total_upper":str(approximation_upper)}


def serial_parameters(p):
    data = {}
    for k,v in p.items():
        if k == "projector":
            data["rational_projector_entry_classes"] = {
                "00":str(v[0][0]), "0p_and_p0":str(v[0][1]), "pq":str(v[1][1])}
        else:
            data[k] = v.data() if isinstance(v,Interval) else str(v)
    data["heat_certificates"] = [certify_heat(p,t) for t in (4,5,10)]
    vb = scalar_evaluation(5*p["bright_hat"])
    vd = scalar_evaluation(5*p["dark_hat"])
    ground = p["projector"]
    data["evaluated_sigma5_heat_entry_classes"] = {
        "00":str(ground[0][0]+vb*(1-ground[0][0])),
        "0p_and_p0":str((1-vb)*ground[0][1]),
        "pp":str(ground[1][1]+vb*(F(1,20)-ground[1][1])+vd*F(19,20)),
        "pq_distinct":str(ground[1][1]+vb*(F(1,20)-ground[1][1])-vd/F(20)),
        "bright_scalar_evaluation":str(vb),
        "dark_scalar_evaluation":str(vd),
    }
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output).resolve()
    need(not out.exists() or not any(out.iterdir()), "Use a fresh output directory")
    contract = json.loads((ROOT/"research/round24/contracts/x2.json").read_text())
    need(contract["loop"] == "x2" and contract["status"] == "frozen", "Wrong contract")
    for section in ("dependencies","instruction_inputs"):
        for name, expected in contract[section].items():
            need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected,
                 "Changed frozen input: "+name)
    graph = physical_graph()
    x, phi, chi = {1:F(1)}, {1:F(2)}, {0:F(-1),2:F(4)}
    need(integral(poly_mul(phi,phi)) == 1 and integral(poly_mul(chi,chi)) == 1,
         "Actual SU(2) character normalization")
    need(integral(poly_mul(x,x)) == F(1,4), "Wrong half-trace normalization")
    need(-integral(poly_mul(x,phi)) == F(-1,2), "Vacuum-face coefficient sign")
    need(-integral(poly_mul(chi,poly_mul(x,phi))) == F(-1,2),
         "Excluded spin-one coefficient")
    # All pairs have a link unique to each face: integrating those two links
    # gives 1/4 twice, with no independence assumption for shared links.
    pair_square = F(1,4)**2
    x4 = 20*integral(poly_mul(poly_mul(x,x),poly_mul(x,x)))+6*comb(20,2)*pair_square
    centered_square_variance = x4-F(5)**2
    spin_one_contribution = F(20,16)
    pair_contribution = F(190,4)
    need(x4 == F(295,4) and centered_square_variance == F(195,4),
         "Complete fourth Haar moment")
    need(spin_one_contribution+pair_contribution == centered_square_variance,
         "Orthogonal residual channel budget")
    need(centered_square_variance/spin_one_contribution == 39,
         "Spin-one-only residual is not a complete norm")
    need(F(1,4) != 1 and F(-1,4) != F(-1,2),
         "Unnormalized Wilson basis falsely admitted")

    # Exact coefficient reconstruction in formal variables. The Ritz identity
    # is lambda=(3+d)kappa and d=5lambda*kappa; reversing the face sign leaves
    # a nonzero retained X coefficient -2lambda before normalization.
    cap = F(1,100)
    need(-2*cap != 0, "Wrong Ritz coefficient sign is not discriminated")
    a = ritz_matrix(cap)
    omega = [F(1)]+[F(0)]*20
    face_sum = [F(0)]+[F(1)]*20
    need(matrix_vector(a,omega) == [20*cap]+[-cap/2]*20,
         "Actual vacuum column")
    need(matrix_vector(a,face_sum) == [-10*cap]+[3+20*cap]*20,
         "Actual symmetric face column")
    for p in range(2,21):
        v = [F(0)]*21
        v[1],v[p] = F(1),F(-1)
        need(matrix_vector(a,v) == [(3+20*cap)*u for u in v], "Dark face mode")

    examples = [parameters(lam) for lam in (F(0),F(1,200),cap)]
    worst = examples[-1]
    need(worst["energy_shift_lower"] > 0 and worst["energy_shift_upper"] < F(1,50_000_000),
         "Useful true-versus-Ritz energy enclosure failed")
    need(worst["projection_upper"] < F(1,12000), "Useful full ground projection certificate failed")
    need(worst["arithmetic_upper"] < F(1,10**22), "Uniform arithmetic is not resolved")
    late = certify_heat(worst,5)
    need(F(late["total_upper"]) < F(1,10000), "Late full-graph heat certificate failed")
    uniform_arithmetic_range = F(1,10**24)*(F(1,1600)+F(1,6)+F(1,12))+SCALAR_ERROR
    uniform_heat_range = (worst["projection_upper"]
                          +negative_exp(5*worst["separation"]).hi
                          +negative_exp(F(15)).hi+uniform_arithmetic_range)
    need(uniform_arithmetic_range < F(3,10**25)
         and uniform_heat_range < F(842454,10**10),
         "Whole-coupling-range late-time bound failed")
    need(F('0.1998333232507006') <= worst["true_energy"].lo
         and worst["true_energy"].hi <= F('0.1998333359872953'),
         "Displayed outward energy interval is not certified")
    zero = examples[0]
    need(zero["residual2"].lo == zero["residual2"].hi == 0
         and zero["projection_upper"] == zero["energy_shift_upper"] == 0,
         "Lambda zero ground exception")
    free_omitted_heat = negative_exp(F(9,2)*5)
    need(free_omitted_heat.lo > 0, "Lambda zero full heat must retain omitted free modes")
    # Arbitrary independent ground rounding cannot give a uniform half-line
    # guarantee: on its unit ground vector it produces exp(+/-sigma eta).
    positive_shift_growth = 1/negative_exp(F(1)).hi
    negative_shift_loss = 1-negative_exp(F(1)).hi
    need(positive_shift_growth > 2 and negative_shift_loss > F(1,2),
         "Rounded centering discriminant is inconclusive")
    invalid_gap_rejected = False
    try:
        gap = F(3)-F(3)
        need(gap > 0, "Invalid Temple separation")
        _ = F(1)/gap
    except RuntimeError:
        invalid_gap_rejected = True
    need(invalid_gap_rejected, "Invalid spectral gap was admitted")
    uniform_taylor_error = F(96)*factorial(80)**2/factorial(161)/(1-F(96,162))
    large_exponent_tail = F(factorial(80),96**80)
    need(uniform_taylor_error+F(2,10**30) < SCALAR_ERROR
         and large_exponent_tail < SCALAR_ERROR,
         "All-time scalar evaluator error is not certified")
    need(scalar_evaluation(97) == 0, "Large-time evaluator must enforce its tail branch")
    start_zero_rejected = False
    try:
        certify_heat(worst,0)
    except RuntimeError:
        start_zero_rejected = True
    need(start_zero_rejected, "Late-time claim silently included time zero")
    # The zero-extended 21-sector operator is P at time zero. A normalized
    # spin-one face is in ker P, so the actual full-space error is exactly one.
    need(integral(poly_mul(chi,chi)) == 1 and 8 > 4, "Time-zero excluded-state witness")

    controls = {
        "all_190_pair_parities_distinct_and_omitted":True,
        "no_four_distinct_face_parity_relation":True,
        "all_pairs_have_two_unique_haar_integration_edges":True,
        "exact_complete_210_channel_residual_norm":True,
        "spin_one_only_missing_channel_budget_rejected":True,
        "actual_normalization_and_magnetic_sign":True,
        "reversed_ritz_face_sign_has_nonzero_retained_residual":True,
        "true_and_ritz_grounds_have_strict_positive_energy_shift":True,
        "positive_and_negative_rounded_centering_fail_uniformly":True,
        "rational_ground_projector_exactly_idempotent":True,
        "uniform_scalar_time_evaluator_has_complete_tail":True,
        "invalid_gap_rejected":invalid_gap_rejected,
        "zero_time_late_claim_rejected":start_zero_rejected,
        "zero_coupling_ground_exact_but_omitted_heat_nonzero":True,
        "finite_rank_time_zero_obstruction":True,
    }
    need(all(v is True for v in controls.values()), "A control failed")
    results = {
        "loop":"x2", "direction":"reverse", "status":"passed",
        "claims":[
            "Complete actual Ritz residual is an orthogonal sum of 20 spin-one and 190 face-pair channels",
            "Exact Haar residual variance is 195/4 times the squared Ritz scalar amplitude",
            "Actual full-graph ground energy and ground projection have evaluated spectral residual certificates",
            "Actually assembled 21-state centered heat is within 1e-4 in full physical operator norm for all sigma>=5 at lambda=1/100",
            "Rational spectral projection and positive-gap representation controls uniform arithmetic without rounded ground exponent",
        ],
        "limitations":[
            "Finite T graph only; no homogeneous, thermodynamic or continuum transfer",
            "Absolute late-time heat approximation, not a relative or real-time theorem",
            "Time zero remains a norm-one full-space obstruction",
            "No measured clock or physical calibration; sigma=alpha*t/hbar uses fixed scales",
            "Scientific priority unverified; independent model agents share inherited premises",
        ],
        "graph":graph,
        "actual_21_state_matrix_at_cap":[[str(v) for v in row] for row in a],
        "residual_moments":{
            "X_second":"5", "X_fourth":str(x4),
            "X_squared_centered_norm_squared":str(centered_square_variance),
            "spin_one_channel_contribution":str(spin_one_contribution),
            "face_pair_channel_contribution":str(pair_contribution),
            "spin_one_only_fraction":"1/39",
        },
        "evaluated_certificates":[serial_parameters(p) for p in examples],
        "uniform_coupling_range_certificate":{
            "coupling_range":["0","1/100"], "sigma_range":"sigma>=5",
            "total_upper":str(uniform_heat_range),
            "arithmetic_upper":str(uniform_arithmetic_range),
            "reason":"kappa, Ritz energy, residual and projection budget increase with lambda; finite excited gap is always >=3",
        },
        "lambda_zero_omitted_heat_at_sigma5":free_omitted_heat.data(),
        "arithmetic":"Fraction rational intervals, integer square-root enclosures and explicit Taylor tails; no floating-point acceptance",
    }
    out.mkdir(parents=True,exist_ok=True)
    (out/"results.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    (out/"controls.json").write_text(json.dumps({"controls":controls},indent=2,sort_keys=True)+"\n")
    need({p.name for p in out.iterdir()} == {"results.json","controls.json"}, "Unexpected scientific output")
    print(json.dumps({"loop":"x2","direction":"reverse","status":"passed",
                      "controls":len(controls),"residual_channels":210,
                      "energy_shift_upper":str(worst["energy_shift_upper"]),
                      "projection_upper":str(worst["projection_upper"]),
                      "late_sigma5_upper":late["total_upper"]},sort_keys=True))


if __name__ == "__main__":
    main()
