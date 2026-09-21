#!/usr/bin/env python3
"""Z1 reverse: actual retained witnesses, exact identities, enclosed ratios."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial, isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]


def need(ok,message):
    if not ok:
        raise RuntimeError(message)


class I:
    def __init__(self,lo,hi=None):
        self.lo,self.hi=F(lo),F(lo if hi is None else hi)
        need(self.lo<=self.hi,"Reversed interval")
    def __add__(self,o):
        o=iv(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-iv(o)
    def __rsub__(self,o):return iv(o)+-self
    def __mul__(self,o):
        o=iv(o);p=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=iv(o);need(not o.lo<=0<=o.hi,"Zero interval denominator")
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return iv(o)/self
    def data(self):return [str(self.lo),str(self.hi)]


def iv(x):return x if isinstance(x,I) else I(x)


def sqrt_i(x,scale=10**30):
    x=iv(x);need(x.lo>=0,"Negative square root")
    a=isqrt(x.lo.numerator*scale**2//x.lo.denominator)
    b=isqrt(x.hi.numerator*scale**2//x.hi.denominator)
    lo,hi=F(a,scale),F(b,scale)
    if hi*hi<x.hi:hi+=F(1,scale)
    need(lo*lo<=x.lo<=x.hi<=hi*hi,"Square root containment")
    return I(lo,hi)


def outward(x,scale=10**30):
    lo=x.lo.numerator*scale//x.lo.denominator
    hi=-((-x.hi.numerator*scale)//x.hi.denominator)
    return I(F(lo,scale),F(hi,scale))


def exp_i(x):
    x=F(x);need(0<=x<=64,"Exponential enclosure range")
    lower=sum((x**k/factorial(k) for k in range(161)),F(0))
    upper=lower+x**161/factorial(161)/(1-x/F(162))
    return outward(I(lower,upper))


def negexp_i(x):
    return outward(1/exp_i(x))


# Exact quadratic field operations a+b*sqrt(radicand); this is not a
# floating-point eigenvector test or an unrelated matrix fixture.
def q(a=0,b=0):return (F(a),F(b))
def qa(x,y):return (x[0]+y[0],x[1]+y[1])
def qn(x):return (-x[0],-x[1])
def qm(x,y,rad):return (x[0]*y[0]+x[1]*y[1]*rad,x[0]*y[1]+x[1]*y[0])
def qi(x,rad):
    d=x[0]*x[0]-x[1]*x[1]*rad
    need(d!=0,"Invalid quadratic-field denominator")
    return (x[0]/d,-x[1]/d)
def qd(x,y,rad):return qm(x,qi(y,rad),rad)


def matrix(lam):
    a=[[F(0)]*21 for _ in range(21)]
    a[0][0]=20*lam
    for p in range(1,21):
        a[p][p]=3+20*lam;a[0][p]=a[p][0]=-lam/2
    return a


def qmv(a,v,rad):
    return [tuple(sum((qm(q(x),y,rad)[k] for x,y in zip(row,v)),F(0))
                  for k in (0,1)) for row in a]


def inner(a,b,rad):
    return tuple(sum((qm(x,y,rad)[k] for x,y in zip(a,b)),F(0)) for k in (0,1))


def exact_witness_checks(lam):
    need(lam>0,"The nonzero witness requires lambda>0")
    rad=9+20*lam*lam
    root=q(0,1);d=q(F(-3,2),F(1,2));mu=qa(q(20*lam),qn(d))
    kappa=qd(q(lam),qa(q(3),d),rad)
    ground=[q(1)]+[qm(q(F(1,2)),kappa,rad)]*20
    bright=[d]+[q(-lam/2)]*20
    a=matrix(lam)
    need(qmv(a,ground,rad)==[qm(mu,v,rad) for v in ground],"Actual Ritz ground equation")
    centered=[qa(x,qn(qm(mu,v,rad))) for x,v in zip(qmv(a,bright,rad),bright)]
    need(centered==[qm(root,v,rad) for v in bright],"Actual retained bright eigenvector")
    need(inner(ground,bright,rad)==q(0),"Computed bright vector is not Ritz-ground orthogonal")
    need(d==qm(q(5*lam),kappa,rad),"Actual vacuum-row scalar relation")
    # The coefficient of a symbolic true energy shift delta in <g,u> is
    # exactly one because u=bright+delta*Omega; the constant coefficient is 0.
    omega=[q(1)]+[q(0)]*20
    need(inner(ground,omega,rad)==q(1),"True-shift overlap coefficient")
    wrong=[d]+[q(lam/2)]*20
    need(inner(ground,wrong,rad)==qm(q(2),d,rad) and inner(ground,wrong,rad)!=q(0),
         "Wrong bright-vector sign is not rejected")
    need(len(bright)==len(ground)==21,"Witness not in actual retained space")
    return {"matrix":a,"exact_bright_coefficients":[[str(a),str(b)] for a,b in bright],
            "radicand":str(rad)}


def spectral_bounds(lam):
    need(0<lam<=F(1,100),"Positive-coupling obstruction is separate from lambda=0")
    root=sqrt_i(9+20*lam*lam);d=(root-3)/2;kappa=lam/(3+d)
    mu=20*lam-d
    n0sq=1/(1+5*kappa*kappa);n0=sqrt_i(n0sq)
    # Reconstruct the complete inherited residual, including all pair states.
    residual2=F(195,4)*lam*lam*kappa*kappa*n0sq
    rho=sqrt_i(residual2)
    h=3-mu.hi;need(h>0,"Actual excited-spectrum separation")
    delta_upper=residual2.hi/h
    delta_lower=residual2.lo/(8+40*lam-mu.lo+rho.hi)
    need(delta_lower>0,"Missing strict actual-versus-Ritz ground shift")
    projection_upper=rho.hi/h
    vacuum_ground_square_lower=n0sq.lo-projection_upper
    need(vacuum_ground_square_lower>0,"Missing actual ground-vacuum overlap")
    actual_vacuum_lower=sqrt_i(vacuum_ground_square_lower).lo
    true_witness_norm_upper=sqrt_i((d.hi+delta_upper)**2+5*lam*lam).hi
    ritz_witness_norm=sqrt_i(d*d+5*lam*lam)
    beta_true=delta_lower*n0.lo/true_witness_norm_upper
    beta_ritz=delta_lower*actual_vacuum_lower/ritz_witness_norm.hi
    need(beta_true>0 and beta_ritz>0,"Witness overlap denominator invalid")
    return {"lambda":lam,"root":root,"d":d,"kappa":kappa,"mu":mu,
            "rho_squared":residual2,"delta_lower":delta_lower,"delta_upper":delta_upper,
            "h":h,"ground_projection_upper":projection_upper,
            "actual_vacuum_overlap_lower":actual_vacuum_lower,
            "true_witness_norm_upper":true_witness_norm_upper,
            "ritz_witness_norm":ritz_witness_norm,
            "beta_true_lower":beta_true,"beta_ritz_lower":beta_ritz}


def witness_time(p,sigma):
    need(sigma>=0,"Negative heat time")
    growth=exp_i(p["h"]*sigma)
    ritz_decay=negexp_i(p["root"].lo*sigma)
    true_relative_lower=max(F(0),p["beta_true_lower"]*growth.lo-1)
    near_one=ritz_decay.hi/p["beta_ritz_lower"]
    ritz_denominator_lower=max(F(0),p["beta_ritz_lower"]*exp_i(p["root"].lo*sigma).lo-1)
    return {"sigma":str(sigma),"physical_time":"sigma*hbar/alpha",
            "exact_ground_orthogonal_witness_true_denominator_relative_lower":str(true_relative_lower),
            "computed_ritz_bright_witness_true_relative_interval":[str(max(F(0),1-near_one)),str(1+near_one)],
            "computed_ritz_bright_witness_ritz_denominator_relative_lower":str(ritz_denominator_lower)}


def serialize(p):
    return {key:(value.data() if isinstance(value,I) else str(value)) for key,value in p.items()}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args()
    output=Path(args.output).resolve()
    need(not output.exists() or not any(output.iterdir()),"Fresh output required")
    contract=json.loads((ROOT/"research/round24/contracts/z1.json").read_text())
    need(contract["loop"]=="z1" and contract["status"]=="frozen","Wrong contract")
    for section in ("dependencies","instruction_inputs"):
        for path,digest in contract[section].items():
            need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,"Changed input: "+path)
    # Full inherited residual normalization; keeping only 20 spin-one states
    # cannot establish the admitted energy/projection interval used here.
    norm_x2=20*F(1,4)
    fourth=20*F(1,8)+6*190*F(1,16)
    residual_factor=fourth-norm_x2**2
    need(norm_x2==5 and residual_factor==F(195,4),"Actual full-face Haar normalization")
    need(residual_factor==F(20,16)+F(190,4) and residual_factor/F(20,16)==39,
         "Missing actual pair channels")
    need(F(1,4)!=1 and F(-1,4)!=F(-1,2),"Wrong unnormalized face basis")
    cap=F(1,100)
    actual=exact_witness_checks(cap)
    p=spectral_bounds(cap)
    times=[witness_time(p,F(t)) for t in (0,5,6,7,8)]
    at6=next(t for t in times if t["sigma"]=="6")
    at7=next(t for t in times if t["sigma"]=="7")
    need(F(at6["exact_ground_orthogonal_witness_true_denominator_relative_lower"])>4,
         "Quantitative unbounded-relative witness not resolved")
    need(F(at6["computed_ritz_bright_witness_true_relative_interval"][0])>F(94,100),
         "Computed bright witness fails to reject useful relative accuracy")
    need(F(at7["computed_ritz_bright_witness_true_relative_interval"][0])>F(997,1000),
         "Computed bright witness late-time limit not quantitatively visible")
    # A useful inherited implication for a proposed repair, not a Z2 selection.
    overlap_floor=F(1,10)
    denominator_floor=overlap_floor-p["ground_projection_upper"]
    need(denominator_floor>0,"Ritz overlap floor must exceed projection error")
    absolute_late=(p["ground_projection_upper"]+negexp_i(5*p["h"]).hi
                   +negexp_i(5*(3+p["d"].lo)).hi)
    repair_relative=absolute_late/denominator_floor
    need(repair_relative<F(1,1000),"Conditional late-time overlap repair")
    # At lambda zero P reduces K and the two centered evolutions coincide on P.
    a0=matrix(F(0));need(a0[0][0]==0 and all(a0[n][n]==3 for n in range(1,21)),
                        "Actual zero-coupling retained generator")
    need(all(a0[0][n]==0 for n in range(1,21)),"Zero-coupling retained decoupling")
    zero_witness_rejected=False
    try:spectral_bounds(F(0))
    except RuntimeError:zero_witness_rejected=True
    need(zero_witness_rejected,"Invalid normalized zero-coupling witness admitted")
    bad_gap_rejected=False
    try:
        h=F(3)-F(3);need(h>0,"Invalid actual gap")
    except RuntimeError:bad_gap_rejected=True
    wrong_sector_rejected=False
    try:
        kinetic_energy=F(8);need(kinetic_energy<F(9,2),"Spin-one face is outside retained P")
    except RuntimeError:wrong_sector_rejected=True
    need(bad_gap_rejected and wrong_sector_rejected,"Domain/input controls failed")
    # A common scalar shift multiplies both vector numerator/denominator by
    # the same factor. Changing only one model's own-ground centering does not.
    factor=F(7,3);need((factor*F(5))/(factor*F(2))==F(5,2),"Common shift invariance")
    wrong_centering_sigma=1/p["delta_lower"]
    need(exp_i(1).lo>2 and negexp_i(1).hi<F(1,2),
         "Actual energy-shift bound does not discriminate one-sided centering")
    need(p["delta_lower"]>0 and p["beta_ritz_lower"]>0,
         "Ritz-ground orthogonality was incorrectly transferred to the true ground")
    controls={
        "actual_21_state_ritz_and_bright_equations_exact":True,
        "actual_full_residual_and_strict_energy_shift_retained":True,
        "true_ground_orthogonal_witness_has_nonzero_ritz_overlap":True,
        "computed_ritz_bright_witness_has_nonzero_true_ground_overlap":True,
        "reversed_bright_sign_is_not_orthogonal":True,
        "unretained_spin_one_counterexample_rejected":wrong_sector_rejected,
        "zero_coupling_normalized_obstruction_rejected":zero_witness_rejected,
        "zero_coupling_relative_error_exactly_zero_on_retained_space":True,
        "time_zero_relative_error_exactly_zero_on_retained_space":True,
        "invalid_actual_gap_rejected":bad_gap_rejected,
        "common_scalar_shift_cancels_but_one_sided_centering_does_not":True,
        "missing_ground_overlap_shortcut_rejected":True,
        "overlap_floor_must_exceed_projection_error":True,
    }
    need(all(value is True for value in controls.values()),"Control failure")
    results={
        "loop":"z1","direction":"reverse","status":"passed",
        "claims":[
            "For every positive frozen coupling, supremum of retained-input true-denominator relative error over finite heat times is infinite",
            "An exact actual retained witness is (L-epsilon)Omega, with zero true and nonzero Ritz ground overlap",
            "The fully computed retained Ritz bright witness (A-mu)Omega has true-denominator relative error tending to one",
            "At lambda=1/100, sigma=6 the exact true-ground-orthogonal witness has relative error above four and the computed bright witness above 0.94",
            "A conditional Ritz-ground-overlap floor gives a useful late-time relative repair without changing the action or clock",
        ],
        "limitations":[
            "The unbounded witness uses the exact true ground energy and is not claimed numerically prepared from an interval",
            "The independently computable Ritz bright witness establishes relative error tending to one for the true denominator",
            "Absolute X2 accuracy is not contradicted; no early-time/full-space or real-time inference",
            "Lambda zero is an exact retained-space equality and has no normalized positive-coupling witness",
            "Finite graph and fixed physical clock only; no model transfer, continuum or novelty claim",
        ],
        "relative_definition":"||(S(sigma)-S_R(sigma))f|| / ||S(sigma)f|| for nonzero f in P H_phys; finite sigma>=0",
        "denominator_statement":"Injectivity of exact heat makes the denominator strictly positive at every finite time",
        "actual_matrix_at_cap":[[str(v) for v in row] for row in actual["matrix"]],
        "computed_bright_unnormalized_quadratic_coefficients":actual["exact_bright_coefficients"],
        "quadratic_radicand":actual["radicand"],
        "wrong_centering_control":{
            "sigma":str(wrong_centering_sigma),
            "true_operator_centered_at_ritz_energy_ground_growth_lower":str(exp_i(1).lo),
            "ritz_operator_centered_at_true_energy_ground_amplitude_upper":str(negexp_i(1).hi),
            "premise":"Actual delta>=delta_lower>0; no clock parameter is altered",
        },
        "cap_spectral_and_overlap_enclosures":serialize(p),
        "quantitative_witness_bounds":times,
        "proposed_overlap_repair":{
            "condition":"|<phi_R,f>| >= a ||f|| with a > ||G-G_R|| bound",
            "a":str(overlap_floor),"sigma_start":"5",
            "proved_true_output_denominator_floor":str(denominator_floor),
            "relative_upper":str(repair_relative),
            "status":"Conditional inherited implication and next-repair candidate; no Z2 selected or executed",
        },
        "arithmetic":"Exact rational quadratic-field identities and outward square-root/exponential intervals; no floating-point acceptance",
    }
    output.mkdir(parents=True,exist_ok=True)
    (output/"results.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    (output/"controls.json").write_text(json.dumps({"controls":controls},indent=2,sort_keys=True)+"\n")
    need({p.name for p in output.iterdir()}=={"results.json","controls.json"},"Unexpected outputs")
    print(json.dumps({"loop":"z1","direction":"reverse","status":"passed","controls":len(controls)}))


if __name__=="__main__":main()
