#!/usr/bin/env python3
"""Z2 reverse: complete retained residual, joined heat estimates and preparation.

Standalone standard-library arithmetic. No producer module imports, floating
point admission, finite full-Hamiltonian surrogate, or assert statements.
The report proves the full-space semigroup/domain claims checked here.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OWN = Path(__file__).resolve().parent
SCALE = 10**30
CAP = F(1, 100)
JOIN = F(29, 10)
PREPARATION = F(1, 100)


def need(value, message):
    if not value:
        raise RuntimeError(message)


def rejects(call):
    try:
        call()
    except RuntimeError:
        return True
    return False


class I:
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)
        need(self.lo <= self.hi, "Reversed interval")

    def __add__(self, other):
        other = iv(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -iv(other)

    def __rsub__(self, other):
        return iv(other) + -self

    def __mul__(self, other):
        other = iv(other)
        p = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return I(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = iv(other)
        need(not other.lo <= 0 <= other.hi, "Interval denominator includes zero")
        return self * I(1/other.hi, 1/other.lo)

    def __rtruediv__(self, other):
        return iv(other) / self


def iv(value):
    return value if isinstance(value, I) else I(value)


def packed(value):
    if isinstance(value, I):
        return [str(value.lo), str(value.hi)]
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): packed(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [packed(v) for v in value]
    return value


def rounded_interval(value, scale=SCALE):
    value = iv(value)
    lo = value.lo.numerator*scale // value.lo.denominator
    hi = -((-value.hi.numerator*scale) // value.hi.denominator)
    return I(F(lo, scale), F(hi, scale))


def sqrt_interval(value, scale=SCALE):
    value = iv(value)
    need(value.lo >= 0, "Negative radical")
    lo = F(isqrt(value.lo.numerator*scale**2 // value.lo.denominator), scale)
    hi = F(isqrt(value.hi.numerator*scale**2 // value.hi.denominator), scale)
    if hi*hi < value.hi:
        hi += F(1, scale)
    need(lo*lo <= value.lo <= value.hi <= hi*hi, "Invalid square root enclosure")
    return I(lo, hi)


def decay_interval(x):
    """Enclose exp(-x); the x>96 branch is a proved all-time tail."""
    x = F(x)
    need(x >= 0, "Negative heat exponent")
    if x == 0:
        return I(1)
    if x > 96:
        return I(0, F(factorial(80), 96**80))
    partial = sum((x**k / factorial(k) for k in range(161)), F(0))
    tail = x**161 / factorial(161) / (1-x/F(162))
    return rounded_interval(I(1/(partial+tail), 1/partial))


def scalar_decay(x):
    """Actual rational scalar evaluator: midpoint below cutoff, zero above."""
    x = F(x)
    if x > 96:
        return F(0)
    enclosure = decay_interval(x)
    return (enclosure.lo + enclosure.hi)/2


def square_graph():
    dims = (3, 3, 2)
    vertices = list(product(*(range(n) for n in dims)))
    edges = []
    for v in vertices:
        for axis in range(3):
            if v[axis]+1 < dims[axis]:
                w = list(v)
                w[axis] += 1
                edges.append((v, tuple(w)))
    index = {frozenset(e): n for n, e in enumerate(edges)}
    masks = []
    for v in vertices:
        for a, b in combinations(range(3), 2):
            if v[a]+1 >= dims[a] or v[b]+1 >= dims[b]:
                continue
            va, vb, vab = list(v), list(v), list(v)
            va[a] += 1
            vb[b] += 1
            vab[a] += 1
            vab[b] += 1
            ring = [v, tuple(va), tuple(vab), tuple(vb)]
            mask = sum(1 << index[frozenset((ring[j], ring[(j+1) % 4]))]
                       for j in range(4))
            masks.append(mask)
    need((len(vertices), len(edges), len(masks)) == (18, 33, 20), "Actual T graph")
    pairs = [a ^ b for a, b in combinations(masks, 2)]
    need(len(set(masks)) == 20 and len(set(pairs)) == 190, "Lost face parity channel")
    need(0 not in pairs and not set(pairs) & set(masks), "Pair channel belongs to retained space")
    need(all(a ^ b ^ c ^ d for a, b, c, d in combinations(masks, 4)),
         "Unexpected fourth-moment term")
    return masks


def complete_residual_map(lam):
    """Rows chi_p and eta_pq, columns Omega and normalized 2*x_p.

    T=QLP has chi row -lambda*b_p/2 and pair row
    -lambda*(b_p+b_q)/2. All 210 orthonormal physical channels occur.
    """
    rows = []
    for p in range(1, 21):
        row = [F(0)]*21
        row[p] = -lam/2
        rows.append(row)
    for p, q in combinations(range(1, 21), 2):
        row = [F(0)]*21
        row[p] = row[q] = -lam/2
        rows.append(row)
    gram = [[sum((row[p]*row[q] for row in rows), F(0)) for q in range(21)]
            for p in range(21)]
    expected = [[F(0) if p == 0 or q == 0 else lam*lam/F(4)*(20 if p == q else 1)
                 for q in range(21)] for p in range(21)]
    need(gram == expected, "Complete retained residual Gram identity")
    need(all(row[0] == 0 for row in rows), "Vacuum has a spurious first omitted source")
    # Squared norm on the symmetric face vector, using its unnormalized
    # coefficients and exact normalization by 20, gives beta^2.
    symmetric_square = sum((sum(row[1:])**2 for row in rows), F(0))/20
    need(symmetric_square == 39*lam*lam/4, "Full residual norm misses pair channels")
    spin_only = sum((sum(row[1:])**2 for row in rows[:20]), F(0))/20
    need(spin_only == lam*lam/4, "Spin-only control coefficients")
    return rows, gram, symmetric_square, spin_only


# Arithmetic in Q(sqrt(9+20lambda^2)) checks the actual 21-state matrix.
def q(a=0, b=0):
    return (F(a), F(b))


def qa(x, y):
    return (x[0]+y[0], x[1]+y[1])


def qm(x, y, rad):
    return (x[0]*y[0]+x[1]*y[1]*rad, x[0]*y[1]+x[1]*y[0])


def qdiv(x, y, rad):
    det = y[0]**2-y[1]**2*rad
    need(det != 0, "Quadratic field zero divisor")
    return qm(x, (y[0]/det, -y[1]/det), rad)


def actual_ritz(lam):
    rad = 9+20*lam*lam
    d = q(F(-3, 2), F(1, 2))
    kappa = qdiv(q(lam), qa(q(3), d), rad)
    mu = qa(q(20*lam), (-d[0], -d[1]))
    matrix = [[F(0)]*21 for _ in range(21)]
    matrix[0][0] = 20*lam
    for p in range(1, 21):
        matrix[p][p] = 3+20*lam
        matrix[0][p] = matrix[p][0] = -lam/2
    ground = [q(1)]+[qm(q(F(1, 2)), kappa, rad)]*20
    av = [tuple(sum((qm(q(a), v, rad)[k] for a, v in zip(row, ground)), F(0))
                for k in range(2)) for row in matrix]
    need(av == [qm(mu, v, rad) for v in ground], "Actual Ritz ground equation")
    need(d == qm(q(5*lam), kappa, rad), "Actual vacuum row")
    need(qm(kappa, qa(q(3), d), rad) == q(lam), "Actual face row")
    return matrix, kappa


def bounds(lam):
    """Point enclosures and simple continuous-range majorants at this cap.

    Every 0<=coupling<=lam satisfies kappa<=lam/3, mu<=20*lam,
    rho<=sqrt(195/4)*lam^2/3, s<=sqrt(9+20*lam^2), gamma>=3.
    No sampled monotonicity is used to certify the coupling interval.
    """
    lam = F(lam)
    need(0 <= lam <= CAP, "Coupling outside frozen interval")
    s = sqrt_interval(9+20*lam*lam)
    d = (s-3)/2
    kappa = lam/(3+d)
    n2 = 1/(1+5*kappa*kappa)
    n = sqrt_interval(n2)
    mu = 20*lam-d
    rho2 = F(195, 4)*lam*lam*kappa*kappa*n2
    rho = sqrt_interval(rho2)
    h = 3-mu.hi
    need(h > 0, "Invalid physical separation")
    exact_delta_hi = rho2.hi/h
    delta_lo = rho2.lo/(8+40*lam-mu.lo+rho.hi)
    rho_upper = sqrt_interval(F(195, 4)).hi*lam*lam/3
    h_lower = 3-20*lam
    projection_upper = rho_upper/h_lower
    delta_upper = rho_upper*rho_upper/h_lower
    n_lower = (1/sqrt_interval(1+5*lam*lam/9)).lo
    beta_upper = sqrt_interval(39).hi*lam/2
    floor = n_lower-projection_upper
    need(h_lower > 0 and floor > 0, "Continuous-range denominator missing")
    return dict(lam=lam, s=s, d=d, kappa=kappa, n=n, n2=n2, mu=mu,
                point_rho2=rho2, point_rho=rho,
                point_delta_interval=I(delta_lo, exact_delta_hi),
                rho_upper=rho_upper, h_lower=h_lower,
                delta_upper=delta_upper, projection_upper=projection_upper,
                n_lower=n_lower, beta_upper=beta_upper, vacuum_floor=floor)


def positive_floor(floor):
    need(floor > 0, "Strictly positive true-output floor required")
    return floor


def early(p, sigma, eta=F(0)):
    sigma, eta = F(sigma), F(eta)
    need(sigma >= 0 and eta >= 0, "Invalid time or preparation radius")
    if sigma == 0 or p['lam'] == 0:
        return F(0)
    # J_s(t)=integral_0^t (1-exp(-s*u))du is increasing in s.
    s = p['s'].hi
    j_upper = max(F(0), sigma-(1-decay_interval(s*sigma).hi)/s)
    vacuum = p['delta_upper']*sigma+p['rho_upper']*j_upper
    # Decompose the arbitrary preparation error into Ritz ground/excited
    # components before integrating the complete retained residual map.
    prep = eta*((p['delta_upper']+p['rho_upper'])*sigma
                + p['beta_upper']*(1-decay_interval(3*sigma).lo)/3)
    return vacuum+prep


def late(p, sigma, eta=F(0)):
    need(sigma >= 0 and eta >= 0, "Invalid late-time arguments")
    return (1+eta)*(p['projection_upper']
                    + decay_interval(p['h_lower']*sigma).hi
                    + decay_interval(3*sigma).hi)


def general_early(p, sigma):
    need(sigma >= 0, "Negative time")
    if sigma == 0 or p['lam'] == 0:
        return F(0)
    return ((p['delta_upper']+p['rho_upper'])*sigma
            + p['beta_upper']*(1-decay_interval(3*sigma).lo)/3)


def overlap_relative(p, sigma, a):
    denom = positive_floor(F(a)-p['projection_upper'])
    return min(general_early(p, sigma), late(p, sigma))/denom


def alltime(p, eta, evaluation):
    denom = positive_floor(p['vacuum_floor']-eta)
    e, l = early(p, JOIN, eta), late(p, JOIN, eta)
    physical = F(0) if p['lam'] == 0 else max(e, l)/denom
    arithmetic = F(0) if p['lam'] == 0 and eta == 0 else evaluation*(1+eta)/denom
    return dict(join_sigma=JOIN, preparation_radius=eta, true_output_floor=denom,
                early_absolute_at_join=e, late_absolute_at_join=l,
                alltime_physical_relative_upper=physical,
                arithmetic_relative_upper=arithmetic,
                alltime_evaluated_relative_upper=physical+arithmetic)


def evaluated_ritz(p, sigma):
    need(sigma >= 0, "Negative evaluated time")
    kappa = (p['kappa'].lo+p['kappa'].hi)/2
    s = (p['s'].lo+p['s'].hi)/2
    gamma = (3+s)/2
    denominator = 1+5*kappa*kappa
    vector = [F(1)]+[kappa/2]*20
    gh = [[a*b/denominator for b in vector] for a in vector]
    need(all(sum((gh[a][k]*gh[k][b] for k in range(21)), F(0)) == gh[a][b]
             for a in range(21) for b in range(21)), "Rounded ground is not a projection")
    need(sum(gh[a][a] for a in range(21)) == 1, "Rounded projection has wrong rank")
    # U-Ghat and P-U remain exact orthogonal projections.
    u = [[F(1) if a == b == 0 else F(1, 20) if a > 0 and b > 0 else F(0)
          for b in range(21)] for a in range(21)]
    dark = [[F(a == b)-u[a][b] for b in range(21)] for a in range(21)]
    eb, ed = scalar_decay(s*sigma), scalar_decay(gamma*sigma)
    heat = [[gh[a][b]+eb*(u[a][b]-gh[a][b])+ed*dark[a][b]
             for b in range(21)] for a in range(21)]
    return dict(kappa_hat=kappa, bright_gap_hat=s, dark_gap_hat=gamma,
                ground_entry_types=[gh[0][0], gh[0][1], gh[1][1]],
                heat_entry_types=[heat[0][0], heat[0][1], heat[1][1], heat[1][2]],
                vacuum_column=[heat[a][0] for a in range(21)],
                bright_decay_evaluated=eb, dark_decay_evaluated=ed,
                heat=heat)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    need(not output.exists() or (output.is_dir() and not any(output.iterdir())),
         "Fresh output directory required")
    contract = json.loads((ROOT/'research/round24/contracts/z2.json').read_text())
    need(contract['status'] == 'frozen' and contract['loop'] == 'z2', "Wrong contract")
    for section in ('dependencies', 'instruction_inputs'):
        for name, digest in contract[section].items():
            need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                 "Changed declared input: "+name)
    # Actual additional reads are independently frozen as checker inputs.
    inventory = json.loads((OWN/'source-inventory.json').read_text())
    for name, digest in inventory['additional_input_hashes'].items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
             "Changed additional input: "+name)

    masks = square_graph()
    rows, gram, beta2, spin2 = complete_residual_map(CAP)
    matrix, exact_kappa = actual_ritz(CAP)
    factor = F(20, 16)+F(190, 4)
    fourth = F(20, 8)+6*F(190, 16)
    need(factor == F(195, 4) == fourth-25, "Complete residual/fourth moment mismatch")
    p = bounds(CAP)

    # Uniform scalar arithmetic, including the unbounded-time branch.
    width_unrounded = F(96*factorial(80)**2, factorial(161))/(1-F(96, 162))
    scalar_error = F(3, 10**30)
    need(width_unrounded/2+F(1, SCALE) < scalar_error, "Scalar midpoint error")
    tail = F(factorial(80), 96**80)
    need(tail < scalar_error, "Scalar cutoff tail")
    need(scalar_decay(0) == 1 and scalar_decay(97) == 0, "Scalar endpoint branches")
    representation_error = F(9, 4*SCALE)+F(2, 3*SCALE)
    evaluation_error = representation_error+scalar_error
    need(evaluation_error < F(6, 10**30), "Uniform arithmetic budget too large")
    vacuum = alltime(p, F(0), evaluation_error)
    neighborhood = alltime(p, PREPARATION, evaluation_error)
    need(vacuum['alltime_evaluated_relative_upper'] < F(6, 10000),
         "Useful all-time vacuum relative target not proved")
    need(neighborhood['alltime_evaluated_relative_upper'] < F(72, 100000),
         "Useful all-time preparation-neighborhood target not proved")
    normed_overlap = (p['n_lower']-PREPARATION)/(1+PREPARATION)
    need(normed_overlap > F(98, 100) > p['projection_upper'], "Preparation overlap margin")
    general_alltime = max(general_early(p, JOIN), late(p, JOIN))/(F(98, 100)-p['projection_upper'])
    need(general_alltime < F(12, 1000), "General overlap cone certificate")

    evaluated = evaluated_ritz(p, JOIN)
    initial = evaluated_ritz(p, F(0))
    need(initial['heat'] == [[F(a == b) for b in range(21)] for a in range(21)],
         "Evaluated retained heat is not exact identity at time zero")
    zero = bounds(F(0))
    zero_eval = evaluated_ritz(zero, F(100))
    need(zero_eval['vacuum_column'] == [F(1)]+[F(0)]*20, "Zero-coupling vacuum evaluation")
    need(early(zero, F(100), PREPARATION) == 0 and early(p, F(0), PREPARATION) == 0,
         "Physical endpoint error must vanish exactly")

    # Meaningful wrong-model/scope controls, executed as Boolean conditions.
    lost_pair_control = beta2 == 39*spin2 and factor == 39*F(20, 16) and beta2 > spin2
    need(lost_pair_control, "Missing-channel control fails to discriminate")
    zero_floor_control = rejects(lambda: overlap_relative(p, JOIN, p['projection_upper']))
    zero_a_control = rejects(lambda: overlap_relative(p, JOIN, F(0)))
    bad_prep_control = rejects(lambda: alltime(p, p['vacuum_floor'], evaluation_error))
    need(zero_floor_control and zero_a_control and bad_prep_control, "Zero-floor control")
    need(p['point_delta_interval'].lo > 0, "Own-centering control requires actual positive delta")
    center_time = 1/p['point_delta_interval'].lo
    wrong_center_control = decay_interval(1).hi < F(1, 2)
    # At this actual dimensionless time, centering Ritz at epsilon loses
    # more than half its ground component; centering true L at mu grows >2.
    need(wrong_center_control and 1/decay_interval(1).hi > 2, "Wrong centering undetected")
    # The late bound is too large at zero; the early bound grows at long
    # times. Neither half alone establishes the stated useful all-time result.
    scope_control = late(p, F(0)) > 2 and early(p, F(100)) > F(1, 100)
    need(scope_control and early(p, F(0)) == 0, "Missing joined-time mechanism")
    # Actual Taylor residual: Q(L-epsilon)^2 Omega = T A Omega,
    # whereas Q(L-epsilon)Omega=0. The second derivative is nonzero.
    second = [sum((row[j]*matrix[j][0] for j in range(21)), F(0)) for row in rows]
    second_square = sum((value*value for value in second), F(0))
    need(second_square == factor*CAP**4 > 0, "Retained vacuum short-time source lost")
    need(sum(v*v for v in second[:20]) == second_square/39,
         "Lost-pair second-derivative control")
    need(rejects(lambda: bounds(CAP+F(1, 10000))) and rejects(lambda: decay_interval(-1)),
         "Coupling/time domain controls")
    # A concrete retained Ritz bright vector has zero computable overlap,
    # so the positive overlap class does not silently include all inputs.
    rad = 9+20*CAP*CAP
    d_exact = q(F(-3, 2), F(1, 2))
    bright_inner = qa(d_exact, qm(q(-5*CAP), exact_kappa, rad))
    need(bright_inner == q(0), "Ritz bright vector fails exclusion control")
    controls = {
        'actual_T_graph_and_210_orthogonal_channels_reconstructed': len(masks) == 20 and len(rows) == 210,
        'actual_21_state_Ritz_equations_exact': len(matrix) == 21,
        'complete_retained_residual_Gram_identity_and_norm': beta2 == 39*CAP*CAP/4,
        'lost_face_pairs_change_residual_norm_by_factor_39': lost_pair_control,
        'vacuum_first_omitted_source_zero_but_second_nonzero': all(row[0] == 0 for row in rows) and second_square > 0,
        'true_denominator_zero_floor_rejected': zero_floor_control and zero_a_control,
        'preparation_radius_cannot_destroy_denominator': bad_prep_control,
        'actual_energy_displacement_rejects_one_sided_centering': wrong_center_control,
        'early_and_late_estimates_are_both_needed': scope_control,
        'retained_Ritz_bright_vector_excluded_by_positive_overlap': bright_inner == q(0),
        'exact_time_zero_retained_identity_and_scalar_value': initial['heat'][0][0] == 1 and scalar_decay(0) == 1,
        'lambda_zero_physical_error_and_evaluated_vacuum_are_exact': early(zero, F(100), PREPARATION) == 0 and zero_eval['vacuum_column'][0] == 1,
        'uniform_scalar_tail_and_rational_ground_projection_checked': tail < scalar_error,
        'continuous_interval_uses_analytic_majorants_not_sampling': p['h_lower'] == F(14, 5) and p['rho_upper'] > p['point_rho'].hi,
        'one_percent_neighborhood_has_certified_ritz_overlap_above_098': normed_overlap > F(98, 100),
    }
    need(all(type(v) is bool and v for v in controls.values()), "A genuine Boolean control failed")
    times = []
    for sigma in [F(0), F(1, 10), F(1), F(2), JOIN, F(5), F(10), F(100)]:
        e, l = early(p, sigma), late(p, sigma)
        pn = early(p, sigma, PREPARATION)
        ln = late(p, sigma, PREPARATION)
        times.append(dict(sigma=sigma,
                          vacuum_physical_relative_upper=min(e, l)/p['vacuum_floor'],
                          preparation_physical_relative_upper=min(pn, ln)/(p['vacuum_floor']-PREPARATION),
                          early_vacuum_absolute=e, late_vacuum_absolute=l))
    coupling_examples = []
    for lam in [F(0), F(1, 1000), F(1, 200), CAP]:
        entry = bounds(lam)
        cert = alltime(entry, F(0), evaluation_error)
        coupling_examples.append(dict(lambda_value=lam, certificate=cert))
    results = {
        'loop': 'z2', 'direction': 'reverse', 'status': 'passed',
        'claims': [
            'Actual vacuum true-output-relative evaluated heat error is below 0.000600 for all sigma>=0 and every lambda in [0,1/100]',
            'For every retained f with ||f-Omega||<=1/100, the same-input true-output-relative evaluated error is below 0.000720 for all times and couplings',
            'A complete retained residual map has squared norm 39*lambda^2/4 and yields a genuine early-time Duhamel bound',
            'The preparation neighborhood has computable normalized Ritz overlap above 0.98 and a positive true-output floor',
            'A general retained Ritz-overlap cone a>D has a separate joined all-time certificate; at a=0.98 its physical bound is below 0.012',
        ],
        'limitations': [
            'The relative denominator is always the exact true output for the same input; vector preparation relative to an ideal target has a separate bias',
            'No guarantee for every retained input; the Ritz bright vector and Z1 obstruction lie outside the positive-floor class',
            'Exact lambda-zero equality applies to physical retained evolution; rounded excited scalar evaluation can still have its stated arithmetic error on nonvacuum preparations',
            'All-time evaluated vacuum error is exactly zero at lambda zero and all evaluated retained inputs agree exactly at time zero',
            'Finite actual T graph, fixed physical scales and heat only; no real-time, model transfer, growing-volume, continuum or priority claim',
            'Independent model-agent derivation from shared admitted premises, not external peer review',
        ],
        'relative_definition': '||(S(sigma)-S_evaluated(sigma))f|| / ||S(sigma)f||, S=e^[-sigma(L-epsilon)], exact Ritz=e^[-sigma(A-mu)]P',
        'fixed_clock': 'sigma=alpha*t/hbar; joining time and preparation radius are diagnostics, with no action or clock fitting',
        'actual_matrix_at_cap': matrix,
        'complete_residual_map': {
            'chi_rows': 20, 'pair_rows': 190,
            'coefficient_rule': 'T Omega=0; T sum b_p phi_p=-(lambda/2)[sum b_p chi_p+sum_(p<q)(b_p+b_q)eta_pq]',
            'gram_at_cap': gram, 'operator_norm_squared_at_cap': beta2,
            'spin_only_norm_squared_at_cap': spin2,
            'vacuum_second_omitted_derivative_squared_at_cap': second_square,
            'residual_Haar_factor': factor,
        },
        'cap_point_enclosures_and_continuous_majorants': p,
        'uniform_vacuum_certificate': vacuum,
        'uniform_preparation_certificate': neighborhood,
        'alltime_formula': 'min{E_eta(sigma), (1+eta)[D+exp(-h*sigma)+exp(-3*sigma)]}/(N_lower-D-eta), with E_eta as report equation (7)',
        'continuous_coupling_proof': 'For coupling<=lambda_cap, kappa<=lambda_cap/3, mu<=20lambda_cap, rho<=sqrt(195/4)*lambda_cap^2/3, s<=sqrt(9+20lambda_cap^2), gamma>=3; displayed uniform certificate uses cap=1/100',
        'ritz_overlap': {
            'condition': '|<phi_R,f>|>=a||f||, a>D; certified denominator (a-D)||f||',
            'neighborhood_normalized_floor': normed_overlap,
            'general_cone_a': F(98, 100), 'general_cone_alltime_physical_relative_upper': general_alltime,
            'arithmetic_overlap_rule': 'If a computed normalized overlap has certified absolute error e, require a_hat-e>D; vector coefficient uncertainty is charged separately',
            'ideal_vacuum_preparation_bias_rule': '||S f-S Omega||<=eta; compare evaluated S_R f with ideal S Omega by adding eta to its absolute same-input numerator and dividing by (N_lower-D)',
        },
        'time_examples_not_used_as_time_coverage': times,
        'coupling_examples_not_used_as_interval_coverage': coupling_examples,
        'arithmetic': {
            'method': 'Exact fractions, integer-square-root outward intervals, positive Taylor reciprocal enclosures and proved scalar tail',
            'scalar_uniform_error_upper': scalar_error,
            'scalar_unrounded_width_majorant': width_unrounded,
            'scalar_tail_upper': tail,
            'representation_uniform_error_upper': representation_error,
            'total_uniform_evaluation_error_upper': evaluation_error,
            'scope': 'Rational coupling/time inputs; coefficients and scalar enclosures have analytic all-time uniform bounds. Arbitrary real input encoding error is separate.',
        },
        'evaluated_21_state_at_join': {k: v for k, v in evaluated.items() if k != 'heat'},
        'wrong_centering_control': {
            'sigma': center_time,
            'true_centered_at_mu_ground_factor_lower': 1/decay_interval(1).hi,
            'Ritz_centered_at_epsilon_ground_factor_upper': decay_interval(1).hi,
            'uses': 'Actual positive lower bound on delta=mu-epsilon; no clock alteration',
        },
    }
    output.mkdir(parents=True, exist_ok=True)
    (output/'results.json').write_text(json.dumps(packed(results), indent=2, sort_keys=True)+'\n')
    (output/'controls.json').write_text(json.dumps(dict(loop='z2', direction='reverse', status='passed',
                                                       controls=controls), indent=2, sort_keys=True)+'\n')
    need({p.name for p in output.iterdir()} == {'results.json', 'controls.json'}, "Unexpected output files")
    print(json.dumps(dict(loop='z2', direction='reverse', status='passed', controls=len(controls))))


if __name__ == '__main__':
    main()
