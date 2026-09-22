#!/usr/bin/env python3
"""Source-bound mathematical companions, not a reproduction of the full solver.

Exact rational quantities are JSON strings; high-precision diagnostics are
decimal strings. See README.md for domains, units, assumptions and source links.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import factorial, isqrt, comb
from pathlib import Path
from typing import Any

import mpmath as mp

HERE = Path(__file__).resolve().parent
COMMIT = "40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02"
# The documented API and CLI both start at 70 decimal digits. This is working
# precision, not a certified accuracy statement. Call configure_precision to
# change the process-wide mpmath context explicitly.
mp.mp.dps = max(mp.mp.dps, 70)


def configure_precision(digits: int = 70) -> None:
    integer(digits, "precision", 30, 200)
    mp.mp.dps = digits


def exact(value: Any, name: str = "value") -> F:
    """Preserve user decimal/rational inputs; reject Boolean and binary floats."""
    if isinstance(value, bool) or not isinstance(value, (str, int, F)):
        raise ValueError(f"{name} must be an integer or a decimal/rational string")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"{name} must be finite and rational") from e


def real(value: Any, name: str = "value") -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must not be Boolean")
    try:
        if isinstance(value, F):
            result = mp.mpf(value.numerator) / value.denominator
        elif isinstance(value, str) and "/" in value:
            result = real(exact(value, name), name)
        else:
            result = mp.mpf(value)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        raise ValueError(f"{name} must be a finite real number") from e
    if not mp.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def integer(value: Any, name: str, minimum: int, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}")
    return value


def jsonable(value: Any) -> Any:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, mp.mpf):
        return mp.nstr(value, min(mp.mp.dps, 60))
    if isinstance(value, mp.mpc):
        return {"real": jsonable(value.real), "imag": jsonable(value.imag)}
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def sqrt_upper(x: F, digits: int = 50) -> F:
    """Integer-arithmetic upper enclosure of a rational square root."""
    if x < 0:
        raise ValueError("square-root argument is negative")
    scale = 10**digits
    n = isqrt(x.numerator * scale**2 // x.denominator)
    if n*n*x.denominator < x.numerator*scale**2:
        n += 1
    return F(n, scale)


def exp_lower_positive(x: F, degree: int = 100) -> F:
    """Exact positive partial sum <= exp(x), for x>=0."""
    if x < 0:
        raise ValueError("positive exponential sum requires x>=0")
    term = total = F(1)
    for k in range(1, degree + 1):
        term *= x / k
        total += term
    return total


def exp_upper_positive(x: F, degree: int = 30) -> F:
    """Positive Taylor sum plus geometric upper tail, using exact arithmetic."""
    if x < 0 or x >= degree+2:
        raise ValueError("exponential upper-tail ratio must be below one")
    partial = exp_lower_positive(x, degree)
    first_omitted = x**(degree+1)/factorial(degree+1)
    return partial+first_omitted/(1-x/F(degree+2))


def jacobi(ratio: Any = "1", alpha: Any = "1", dimension: int = 24,
           refine: bool = False) -> dict:
    """Finite character compression n=0,...,dimension-1; diagnostic only."""
    r, a = real(ratio, "lambda/alpha"), real(alpha, "alpha")
    integer(dimension, "dimension", 2, 160)
    if r < 0 or a <= 0:
        raise ValueError("requires lambda/alpha>=0 and alpha>0")
    matrix = mp.matrix(dimension)
    for n in range(dimension):
        matrix[n, n] = a*(n*(n+2) + r)
        if n + 1 < dimension:
            matrix[n, n+1] = matrix[n+1, n] = -a*r/2
    vals = mp.eigsy(matrix, eigvals_only=True)
    result = {
        "model": "one physical SU(2) square; dimensionless ratio lambda/alpha",
        "status": "high-precision finite-compression diagnostic; no tail certificate",
        "dimension": dimension, "alpha": a, "lambda_over_alpha": r,
        "E0": vals[0], "E1": vals[1], "gap": vals[1]-vals[0],
        "gap_over_alpha": (vals[1]-vals[0])/a,
        "analytic_lower_bound_over_alpha": 3-r,
        "source_exact_gap_floor_over_alpha": F(999999, 1000000) if r <= 10 else None,
        "source_exact_gap_floor_domain": "0<=lambda/alpha<=10; inherited Round10 theorem, not proved by this calculation",
    }
    if refine:
        if dimension > 80:
            raise ValueError("refinement requires dimension<=80")
        fine = jacobi(r, a, 2*dimension, False)
        result["refined_dimension"] = 2*dimension
        result["gap_change_on_doubling"] = abs(fine["gap"]-result["gap"])
        result["refinement_note"] = "Difference between compressions is not an error enclosure."
    return result


def haar_moment(n: int) -> F:
    integer(n, "moment order", 0, 100)
    if n % 2:
        return F(0)
    k = n//2
    return F(comb(2*k, k), (k+1)*4**k)


def static_response(kappa: Any = "1", moments: int = 6) -> dict:
    """Tilted semicircle/Haar integral, kept distinct from Hamiltonian dynamics."""
    k = real(kappa, "kappa")
    integer(moments, "moments", 2, 20)
    # The shift avoids a needlessly huge positive exponential in quadrature.
    def density(theta: mp.mpf) -> mp.mpf:
        return 2/mp.pi * mp.sin(theta)**2 * mp.exp(k*mp.cos(theta)-abs(k))
    scaled_Z = mp.quad(density, [0, mp.pi/2, mp.pi])
    ms = [mp.mpf(1)]
    for n in range(1, moments+1):
        ms.append(mp.quad(lambda t: mp.cos(t)**n*density(t), [0, mp.pi/2, mp.pi])/scaled_Z)
    u = mp.mpf(0) if k == 0 else mp.besseli(2, k)/mp.besseli(1, k)
    variance = ms[2]-ms[1]**2
    identities = [n*ms[n-1]-(n+3)*ms[n+1]+k*(ms[n]-ms[n+2])
                  for n in range(moments-1)]
    point = 2*k/(3+mp.sqrt(9+4*k*k))
    return {
        "model": "static tilted SU(2) Haar measure; kappa is dimensionless",
        "status": "high-precision numerical quadrature/Bessel diagnostics; no interval enclosure",
        "kappa": k, "Z": scaled_Z*mp.exp(abs(k)), "mean_Bessel": u,
        "moments_quadrature": ms, "variance_quadrature": variance,
        "mean_representation_difference": abs(ms[1]-u),
        "Haar_identity_residuals": identities,
        "Riccati_residual_using_quadrature_variance": k*variance+3*u-k*(1-u*u),
        "origin_values_exact": {"mean": F(0), "susceptibility": F(1,4)},
        "wrong_zero_variance_closure_mean": point,
        "wrong_closure_origin_slope": F(1,3),
    }


def scalar_series(degree: int = 7, epsilon: Any = "1/100") -> dict:
    """Exact local-series coefficients and a proved launch-error upper bound."""
    integer(degree, "degree", 1, 31)
    if degree % 2 == 0:
        raise ValueError("degree must be odd")
    e = exact(epsilon, "epsilon")
    if not 0 < e <= F(1,2):
        raise ValueError("launch bound requires 0<epsilon<=1/2")
    coefficients = [F(1,4)]
    for n in range(1, (degree+1)//2):
        coefficients.append(-sum(coefficients[i]*coefficients[n-1-i] for i in range(n))/(2*n+4))
    p = {2*n+1: a for n, a in enumerate(coefficients)}
    residual = {1: F(-1)}
    for power, a in p.items():
        residual[power] = residual.get(power, F(0)) + (power+3)*a
    for i, a in p.items():
        for j, b in p.items():
            residual[i+j+1] = residual.get(i+j+1, F(0)) + a*b
    residual = {k: v for k,v in residual.items() if v}
    positive = coefficients[0]-sum(abs(a)*e**(2*n) for n,a in enumerate(coefficients) if n)
    if positive <= 0:
        raise ValueError("the sufficient nonnegative-polynomial witness failed")
    bound = sum(abs(a)*e**power/F(power+3) for power,a in residual.items())
    return {"status": "exact rational launch certificate only", "degree": degree,
            "epsilon": e, "coefficients_by_power": p, "residual_by_power": residual,
            "positivity_witness": positive,
            "polynomial_value": sum(a*e**power for power,a in p.items()),
            "analytic_launch_error_upper": bound,
            "scope": "Does not certify subsequent floating ODE evolution."}


def profile(q: Any) -> Any:
    """B(q), preserving Fraction arithmetic if called with a Fraction."""
    if not 0 < q < 1:
        raise ValueError("canonical profile requires 0<q<1")
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def support_product(q: Any, L: int) -> mp.mpf:
    q = real(q, "q")
    integer(L, "L", 1)
    if not 0 < q < 1:
        raise ValueError("requires 0<q<1; q=1 is not an infinite Hamiltonian")
    return mp.fprod(-mp.expm1(r*L*mp.log(q)) for r in [4,2,1])


def window_budget(q: Any = "99/100", eta: Any = "1/2", L: int | None = 1,
                  ell: Any = "1", beta: Any = "0", gamma: Any = "1",
                  C: Any = "1") -> dict:
    q, eta, ell, beta, gamma, C = [real(v,n) for v,n in
        [(q,"q"),(eta,"eta"),(ell,"ell"),(beta,"beta"),(gamma,"gamma"),(C,"C")]]
    if not 0 < q < 1 or not 0 < eta < 1:
        raise ValueError("requires 0<q<1 and 0<eta<1")
    if ell <= 0 or C <= 0 or beta < 0 or gamma < 0:
        raise ValueError("requires ell,C>0 and beta,gamma>=0")
    eps = 1-q
    use_growth = L is None
    if use_growth:
        L = max(1, int(mp.floor(ell*eps**(-beta))))
    integer(L, "L", 1)
    b = profile(q)
    tau = eta/(8*b)
    sigma_over_alpha = tau*mp.sqrt(profile(q*q)/96)
    state = 6*sigma_over_alpha/((1-eta)/8)
    product = support_product(q,L)
    dynamic = eta*C/4 * eps**(-gamma)*product
    return {"model": "canonical summable profile; complete origin-tail cube support",
            "status": "high-precision evaluation of proved upper-budget formulas",
            "q": q, "eta": eta, "L": L, "links": 24*L**3,
            "incident_omitted_faces": 21*L**3,
            "B_profile": b, "tau": tau, "P_L": product,
            "D_L": b*product, "state_term": state, "dynamic_term": dynamic,
            "normalized_correlation_error_upper": state+dynamic,
            "sigma_window_alpha_T_over_hbar": C*eps**(-gamma),
            "support_rule": "max(1,floor(ell epsilon^-beta))" if use_growth else "fixed L",
            "asymptotic_vanishing_certificate": beta<1 and gamma<3*(1-beta) if use_growth else gamma<3,
            "scope": "Budget failure is not actual nonconvergence. q=1 is excluded; no clock match to other models."}


def filter_budget(kind: str = "gaussian", M: Any = "35/1664", duration: Any = "4",
                  omega: Any = "0") -> dict:
    M, T = exact(M,"M"), exact(duration,"duration")
    w = real(omega,"omega")
    if kind not in {"gaussian","triangle"}:
        raise ValueError("kind must be gaussian or triangle")
    if not 0 <= M <= F(35,1664) or T <= 0:
        raise ValueError("requires 0<=M<=35/1664 and positive proof duration")
    mt = real(T)
    if kind == "gaussian":
        multiplier = mp.exp(-mt*mt*w*w/2)
        numerator = -mp.expm1(-mt*mt*w*w/2)
        conservative = min(F(1),(6*M+1/T)/(1-M))
        sharper = min(mp.mpf(1),(6*real(M)+mp.sqrt(2/mp.pi)/mt)/(1-real(M)))
        crossings, inverse_bound = 3, T
        weighted = None
    else:
        multiplier = mp.sinc(w*mt/2)**2
        numerator = 1-multiplier
        conservative = min(F(1),(24*M+2/T)/(1-M))
        sharper = real(conservative)
        crossings, inverse_bound = 12, T/3
        x = 192*M*T
        weighted = {"radius_parameter_192MT": x,
                    "residual_series_finite_certificate": x<1,
                    "inverse_series_at_endpoint_finite": x==1,
                    "simultaneous_open_duration_interval_exists": 409*M<1,
                    "contraction_lower_duration": 2/(1-25*M),
                    "cardinality_upper_duration": 1/(192*M) if M else None,
                    "rooted_weight2_residual_over_rstar_upper": 64/(1-x)**3 if x<1 else None,
                    "rooted_weight2_inverse_over_rstar_upper": (T/3)*64/(1-x)**3 if x<1 else None,
                    "weighted_contraction_proved": False}
    return {"model":"initial homogeneous operator; duration is a proof regulator",
            "kind":kind,"M":M,"duration":T,"crossing_stars":crossings,
            "operator_residual_over_r_rational_upper": conservative if M else None,
            "operator_residual_over_r_sharper_numeric_upper": sharper if M else None,
            "source_zero_exception": M==0,
            "inverse_norm_over_r_upper": inverse_bound if M else None,
            "omega":w,"spectral_residual_multiplier":multiplier,
            "spectral_inverse_multiplier": numerator/w if w else mp.mpf(0),
            "zero_frequency_residual_exact":F(1),"weight2":weighted,
            "scope":"Per-source contraction is not residual-family contraction or an exact inverse. Gaussian and triangle geometries have different crossing counts."}


def wilson(z: Any = "1/1000000") -> dict:
    z = real(z,"z")
    if z < 0 or z > mp.mpf("0.000001"):
        raise ValueError("the admitted endpoint witness range is 0<=z<=1e-6")
    theta = z/84
    # Stable deficits retain effects of order z^2 at very small clocks.
    deficit_x = mp.sin(theta)**2/2 + mp.sin(mp.sqrt(3)*theta)**2/6
    deficit_sum = mp.sin(theta)**2 + mp.sin(mp.sqrt(3)*theta)**2/3
    imag_sum = mp.sin(2*theta)/4 + mp.sin(2*mp.sqrt(3)*theta)/(4*mp.sqrt(3))
    return {"model":"canonical summable family; original slow clock; actual Wilson multiplication",
            "status":"high-precision evaluation of source-proved exact formulas; finite-q error is not included",
            "z":z,"theta":theta,"elementary_F":mp.mpf(1),
            "single_F":1-deficit_x,"single_deficit":deficit_x,
            "sum_F":mp.mpc(1-deficit_sum,imag_sum),
            "sum_real_deficit":deficit_sum,"sum_imaginary":imag_sum,
            "single_deficit_lower":theta**2-F(2,3)*theta**4,
            "single_deficit_upper":theta**2,
            "sum_linear_remainder_upper":2*theta**2,
            "adjacency_moments_single":[1,0,2,0,16,0,160],
            "adjacency_moments_sum":[1,1,4,8,32,80,320],
            "operator_comparison":{
                "rank":{"norm_squared":F(1),"vacuum_variance":F(1),"vacuum_fourth_moment":F(1)},
                "single":{"norm_squared":F(4),"vacuum_variance":F(1),"vacuum_fourth_moment":F(2)},
                "sum":{"norm_squared":F(8),"vacuum_variance":F(1),"vacuum_fourth_moment":F(5,2)}},
            "scope":"Equal vacuum-created vectors can transfer this scalar after the proved state argument; full norms and finite-q budgets do not transfer unchanged."}


def heat_envelopes(cap: Any = "1/100", eta: Any = "1/100", sigma: Any = "13/5") -> dict:
    """AC2 physical certificate, not a computed 293-coordinate heat vector."""
    cap, eta, t = exact(cap,"coupling cap"), exact(eta,"eta"), real(sigma,"sigma")
    if not 0 <= cap <= F(1,100) or not 0 <= eta <= F(1,100) or t<0:
        raise ValueError("requires 0<=cap<=0.01, 0<=eta<=0.01 and sigma>=0")
    g, d = 3-20*cap, F(9,2)
    r21 = 7*cap**2/3
    p21 = r21/g
    rplus = 20*cap*p21
    pplus = rplus/g
    delta = rplus*rplus/g
    qplus = 3*cap/4+3*p21/2
    b = qplus+eta
    Cbar, Mbar = 25*cap/8, 20*cap
    denom = 1-5*cap**2/9-eta-p21
    if denom <= 0:
        raise ValueError("true-output denominator certificate is nonpositive")
    gm, dm = real(g), real(d)
    ig = -mp.expm1(-gm*t)/gm
    id_ = -mp.expm1(-dm*t)/dm
    early = real(delta)*t+real(Mbar*Cbar)*(real(qplus/d)*(t-id_)+real(b/(d-g))*(ig-id_))
    coarse = real(delta)*t+real(Mbar*Cbar)*(real(qplus/d)*t+real(b/(g*d)))
    late = real(pplus)+real(2*b+pplus)*mp.exp(-gm*t)
    exact_zero = cap==0 or t==0
    return {"model":"fixed open (3,3,2) physical SU(2) graph; original normalized P21 vacuum ball",
            "status":"certificate arithmetic only; no 293-state heat action executed",
            "cap":cap,"preparation_radius":eta,"sigma":t,"g":g,"d":d,
            "r21":r21,"p21":p21,"rplus":rplus,"pplus":pplus,"delta_plus":delta,
            "qplus":qplus,"b":b,"Cbar":Cbar,"Mbar":Mbar,"denominator":denom,
            "early_absolute_numeric":early,"early_coarse_absolute_numeric":coarse,
            "late_absolute_numeric":late,
            "pointwise_relative_upper_numeric":mp.mpf(0) if exact_zero else min(early,late)/real(denom),
            "exact_zero_exception":exact_zero,
            "scope":"No arbitrary P293 preparation, graph-size limit, real-time, or continuum result."}


def heat_certificates() -> dict:
    """Reconstruct exact AC2 and AF scalar arithmetic from bundled source data."""
    data = json.loads((HERE/'source_data'/'heat_scalar_inputs.json').read_text())
    e = heat_envelopes()
    join = F(13,5)
    early = e['delta_plus']*join+e['Mbar']*e['Cbar']*(e['qplus']*join/e['d']+e['b']/(e['g']*e['d']))
    exp_positive = exp_lower_positive(e['g']*join)
    if exp_positive <= 1400:
        raise ArithmeticError("positive Taylor witness for exp(g t0)>1400 failed")
    late = e['pplus']+(2*e['b']+e['pplus'])/1400
    physical = max(early,late)/e['denominator']
    center = data['af1_center']
    a, rho2, muhat = map(F,[center['rayleigh'],center['retained_residual_squared'],center['rounded_center']])
    if not 0<a<3 or rho2<0:
        raise ArithmeticError("retained isolated-eigenvalue arithmetic hypotheses failed")
    lower, upper = a-rho2/(3-a), a
    dmu = max(abs(muhat-lower),abs(muhat-upper))
    if not 8*dmu<F(1,2):
        raise ArithmeticError("early polynomial factor two lacks its center-error bound")
    early_center = 8*dmu/(1-8*dmu)
    early_poly = F(2*72**257,factorial(257))
    rounding = F(15,10**40)
    pa = F(data['af2_late_rayleigh'])
    prho2 = F(data['af2_late_residual_squared'])
    projector = F(data['af2_projector_error_upper'])
    if not 0<pa<3 or projector**2*(3-pa)**2 < prho2:
        raise ArithmeticError("imported rational projector upper bound fails its residual test")
    if exp_lower_positive(F(112,5)) <= 5*10**9:
        raise ArithmeticError("late excited-tail positive Taylor witness failed")
    late_tail = F(1,5*10**9)
    en = early_center+early_poly+rounding
    ln = projector+late_tail+rounding
    numerical = max(en,ln)
    full = physical+numerical/e['denominator']
    if exp_upper_positive(F(2,3)) >= 2:
        raise ArithmeticError("AF1 exponential prefactor witness failed")
    af1_poly = F(2**14*9**101,factorial(101))
    af1_center = dmu/(1-dmu)
    af1_round = F(21,2*10**50)
    q=F(61,8000)
    af1_physical = F(1,10080000000)+F(1,5)*F(1,32)*(q/F(9,2)+q/(F(14,5)*F(9,2)))
    af1_denom = 1-F(5,9)*F(1,100)**2-F(1,12000)
    return {"status":"exact rational recomputation of scalar certificates conditional on source-proved operator premises",
            "source_commit":COMMIT,"heat_vector_computed_here":False,
            "AC2":{"denominator":e['denominator'],"join":join,"early_absolute":early,
                   "late_absolute":late,"all_time_physical_relative":physical},
            "AF1":{"retained_mu_lower":lower,"retained_mu_upper":upper,"center_radius":dmu,
                   "degree100_Taylor":af1_poly,"center_heat":af1_center,"export_rounding":af1_round,
                   "physical_absolute":af1_physical,"true_denominator":af1_denom,
                   "full_relative":(af1_poly+af1_center+af1_round+af1_physical)/af1_denom},
            "AF2":{"early_center":early_center,"early_polynomial":early_poly,
                   "export_rounding":rounding,"early_total":en,"late_projector":projector,
                   "late_excited_tail":late_tail,"late_total":ln,"numerical_maximum":numerical,
                   "full_relative_total":full},
            "scope":"Does not reconstruct sparse matrix, fusion channels, or exported vectors; run pinned original AF solver for those."}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--precision',type=int,default=70,help='mpmath decimal precision, 30..200; diagnostics only')
    p.add_argument('--output',type=Path,help='optional JSON output file; otherwise stdout')
    s=p.add_subparsers(dest='command',required=True)
    j=s.add_parser('jacobi',help='one-square character compression; no certified infinite tail')
    j.add_argument('--ratio',default='1');j.add_argument('--alpha',default='1');j.add_argument('--dimension',type=int,default=24);j.add_argument('--refine',action='store_true')
    a=s.add_parser('static',help='tilted-Haar moments, Bessel response and wrong closure')
    a.add_argument('--kappa',default='1');a.add_argument('--moments',type=int,default=6)
    a=s.add_parser('series',help='exact rational local response series and launch certificate')
    a.add_argument('--degree',type=int,default=7);a.add_argument('--epsilon',default='1/100')
    a=s.add_parser('window',help='complete-support canonical correlation upper budget')
    for key,default in [('q','99/100'),('eta','1/2'),('ell','1'),('beta','0'),('gamma','1'),('C','1')]:
        a.add_argument('--'+key,default=default)
    a.add_argument('--L',type=int,default=None,help='fixed positive integer; omit to use ell,beta growth rule')
    a=s.add_parser('filter',help='Gaussian or triangular source/weight budgets')
    a.add_argument('--kind',choices=['gaussian','triangle'],default='gaussian');a.add_argument('--M',default='35/1664');a.add_argument('--duration',default='4');a.add_argument('--omega',default='0')
    a=s.add_parser('wilson',help='actual Wilson endpoint formulas within admitted z range')
    a.add_argument('--z',default='1/1000000')
    a=s.add_parser('heat',help='293-state physical omission budget; does not evolve a vector')
    a.add_argument('--cap',default='1/100');a.add_argument('--eta',default='1/100');a.add_argument('--sigma',default='13/5')
    s.add_parser('heat-certificates',help='exact AC2/AF1/AF2 scalar arithmetic from bundled source inputs')
    args=p.parse_args()
    try:
        configure_precision(args.precision)
        if args.command=='jacobi': result=jacobi(args.ratio,args.alpha,args.dimension,args.refine)
        elif args.command=='static': result=static_response(args.kappa,args.moments)
        elif args.command=='series': result=scalar_series(args.degree,args.epsilon)
        elif args.command=='window': result=window_budget(args.q,args.eta,args.L,args.ell,args.beta,args.gamma,args.C)
        elif args.command=='filter': result=filter_budget(args.kind,args.M,args.duration,args.omega)
        elif args.command=='wilson': result=wilson(args.z)
        elif args.command=='heat': result=heat_envelopes(args.cap,args.eta,args.sigma)
        else: result=heat_certificates()
        content=json.dumps(jsonable(result),indent=2,allow_nan=False)+'\n'
    except (ValueError,ArithmeticError) as exc:
        p.error(str(exc))
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content)
    else:
        print(content,end='')


if __name__=='__main__':
    main()
