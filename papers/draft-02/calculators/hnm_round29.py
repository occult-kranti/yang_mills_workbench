#!/usr/bin/env python3
"""HNM-C-AM2 exact arithmetic companion; the model proof lives in its frozen gate.

This calculator checks only admitted majorant arithmetic and physical-unit
conversion. It does not inspect a Hamiltonian, establish an infinite-volume
state, evaluate a spectral gap, or validate an arbitrary chosen model.
"""
from fractions import Fraction
import argparse,json

def calculate(tau,alpha=Fraction(1),hbar=Fraction(1),energy_reference=Fraction(1)):
    tau,alpha,hbar,energy_reference=map(Fraction,(tau,alpha,hbar,energy_reference))
    if min(alpha,hbar,energy_reference)<=0:
        raise ValueError('alpha, hbar and the physical energy reference must be positive.')
    radius=Fraction(1,64);cap=Fraction(1,100000000);budget=28*abs(tau)
    g_upper=Fraction(148,7);derivative_upper=Fraction(352)
    values={
        'tau':tau,'admitted_absolute_tau_cap':cap,'creation_radius':radius,
        'indexed_interaction_budget_upper':budget,
        'majorant_at_radius_strict_upper':g_upper,
        'majorant_derivative_at_radius_strict_upper':derivative_upper,
        'self_map_upper':budget*g_upper,
        'fixed_point_lipschitz_upper':budget*derivative_upper,
        'shifted_exclusion_lipschitz_upper':2*budget*derivative_upper,
        'physical_gap_lower_if_model_and_cap_apply':alpha/16,
        'frequency_threshold_lower_if_model_and_cap_apply':alpha/(16*hbar),
        'gap_in_fixed_reference_units_lower_if_model_and_cap_apply':alpha/(16*energy_reference),
    }
    within=abs(tau)<=cap
    arithmetic=budget*g_upper<radius and 2*budget*derivative_upper<1
    return {
        'record':'HNM-C-AM2','author':'Hruday N M (BUNZEEY)',
        'source':'research/round29/advisor/am2-gate.json',
        'inside_admitted_parameter_cap':within,
        'passes_displayed_majorant_arithmetic':arithmetic,
        'scope':'Conditional arithmetic companion for the complete untruncated finite-volume I1 model, uniform over its declared nonempty complete-factor volumes. Both signs of tau are allowed. The actual selected-strip onsite bound and whole-star interaction are hypotheses, not checked by this script.',
        'interpretation':'Inside the admitted cap; conditional finite-volume theorem applies only if all model hypotheses hold.' if within else 'Outside the admitted cap: no extension of the gated theorem is asserted, even if these scalar sufficient inequalities pass.',
        'not_claimed':['a measured gap','an infinite-volume state or numerical infinite-state interval','a continuum bridge or Yang-Mills solution','an optimized coupling cap','new scientific priority by HNM naming'],
        'exact':{k:str(v) for k,v in values.items()},
        'display_decimal':{k:float(v) for k,v in values.items()},
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tau',default='1/100000000',type=Fraction)
    parser.add_argument('--alpha',default='1',type=Fraction)
    parser.add_argument('--hbar',default='1',type=Fraction)
    parser.add_argument('--energy-reference',default='1',type=Fraction)
    args=parser.parse_args()
    try:result=calculate(args.tau,args.alpha,args.hbar,args.energy_reference)
    except ValueError as exc:parser.error(str(exc))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
