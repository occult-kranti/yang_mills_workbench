#!/usr/bin/env python3
"""Independent exact AT1 geometry, commutator, energy and tail controls.

These fixtures test scope and algebra; the analytic review proves the
infinite-dimensional statements. This script never modifies producer output.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

def execute():
    checks = []
    def need(condition, label):
        if condition is not True:
            raise RuntimeError(label)
        if label in checks:
            raise RuntimeError('duplicate check: ' + label)
        checks.append(label)

    zero=(0,0,0); ex=(1,0,0); ey=(0,1,0); ez=(0,0,1)
    directions=(ex,ey,ez)
    def add(a,b): return tuple(x+y for x,y in zip(a,b))
    def sub(a,b): return tuple(x-y for x,y in zip(a,b))
    def factor(b):
        return {( (4*b[0]+r,2*b[1]+s,b[2]), d )
                for r in range(4) for s in range(2) for d in directions}
    region={zero,ez}; links=set().union(*(factor(b) for b in region))
    ends={v for x,d in links for v in (x,add(x,d))}
    anchors={sub(b,s) for b in region for s in (zero,ex,ey,ez)}
    orthant={b for b in anchors if min(b)>=0}
    need(len(links)==48,'complete_48_links')
    need(len(ends)==36,'complete_36_original_endpoints')
    need(len(anchors)==7,'seven_incident_full_lattice_stars')
    need(len(orthant)==2 and orthant!=anchors,'two_star_boundary_substitution_rejected')
    face={(zero,ex),(ex,ez),(ez,ex),(zero,ez)}
    need(len(face)==4 and face.issubset(links),'four_distinct_original_wilson_links')
    for shift in [(-9,2,-4),(0,0,0),(4,-3,7)]:
        moved={add(b,shift) for b in region}
        need(len({sub(b,s) for b in moved for s in (zero,ex,ey,ez)})==7,
             'bulk_translation_incidence_'+str(shift))

    cap=F(1,100000000)
    need(2*7*7==98,'seven_star_reset_coefficient')
    for j,tau in enumerate([-cap,F(0),cap]):
        kinetic=F(9,4)+F(98,8)*abs(tau)
        b2=18+8*kinetic
        need(b2==36+98*abs(tau),'full_kinetic_to_second_moment_'+str(j))
        need(b2<37,'numerical_second_moment_cap_'+str(j))
    need(F(1,4)-F(1,2)-F(-1,4)==0,'actual_selected_scalar_exact_identity')
    need(F(1,4)-F(1,2)!=0,'deleting_selected_scalar_changes_identity')
    need(F(1,4)>0,'selected_reference_zero_energy_not_zero_kinetic_fixture')

    # Radial four-link Casimir: Qf=-(1-w^2)f''+3w f'.
    # For psi=1+w/3, calculate Q(w psi)-w Q(psi) independently.
    for j,w in enumerate([F(-4,5),F(0),F(3,5),F(1)]):
        exact=3*w+F(5,3)*w*w-F(2,3)
        product=3*w*(1+w/3)-2*(1-w*w)/3
        need(exact==product,'radial_product_rule_'+str(j))
    need(F(-2,3)!=0,'missing_gradient_cross_term_rejected_at_zero')
    need(4*F(3,4)==3,'half_pauli_four_link_casimir')
    need(4*F(1,4)==1,'half_pauli_four_link_gradient_budget')
    need(4*F(3,4)*4!=3,'doubled_lie_generators_rejected')
    for j,alpha in enumerate([F(1,3),F(1),F(7,2)]):
        free_m1=F(1,4)*3*alpha
        free_m2=F(1,4)*(3*alpha)**2
        need(free_m1==alpha*(1-F(1,4)), 'free_first_moment_physical_units_'+str(j))
        need(free_m2==F(9,4)*alpha**2,'free_second_moment_physical_units_'+str(j))
        need(free_m2>0,'zero_reference_energy_not_excitation_moment_'+str(j))
    need(F(1,8)!=1 and F(1,64)!=F(1,8),'wrong_delta_alpha_units_rejected')
    m=F(1,5);v=F(1,4)
    need(v+m*m!=v,'uncentered_vacuum_mass_contamination')
    need(m*m*0==0 and m*m*0**2==0,'centering_can_change_mass_without_positive_moments')
    # A=M2 direct-sum M2, same component H=diag(0,1), but the two
    # ground-state representations select different summands.  For the
    # single algebra element W=(sigma_x/2, 2*sigma_x/3), both vacua are
    # simple and have gap one; its spectral weights are 1/4 and 4/9.
    amplitudes=(F(1,2),F(2,3));weights=tuple(a*a for a in amplitudes)
    need(all(0<a<=1 for a in amplitudes),'distinct_state_fixture_bounded_observable')
    need(weights==(F(1,4),F(4,9)) and weights[0]!=weights[1],
         'same_gap_does_not_identify_distinct_state_moments')

    def theta(e,L):
        return F(0) if e<0 else min(F(1),max(F(0),2-e/L))
    def cut(e,L,k): return e**k*theta(e,L)
    for j,e in enumerate([F(-3),F(0),F(1,3),F(2),F(13)]):
        for k in (1,2):
            vals=[cut(e,L,k) for L in (F(1,4),F(1),F(4),F(16))]
            need(all(a<=b for a,b in zip(vals,vals[1:])),f'compact_cutoff_monotonicity_{j}_{k}')
            if e<0:
                need(vals==[0]*4,f'negative_energy_zero_extension_{k}')
    for n in (2,5,20,200):
        first_only=[(1-F(1,n),F(1)),(F(1,n),F(n))]
        m1=sum(p*e for p,e in first_only);m2=sum(p*e*e for p,e in first_only)
        need(m1<2 and m2>n,'bounded_first_does_not_bound_second_'+str(n))
        second=[(1-F(1,n*n),F(1)),(F(1,n*n),F(n))]
        m1=sum(p*e for p,e in second);m2=sum(p*e*e for p,e in second)
        need(m2==2-F(1,n*n) and m2<2,'bounded_second_unequal_limit_'+str(n))
        need(m1==1+F(1,n)-F(1,n*n),'first_moment_converges_'+str(n))
        for j,L in enumerate((F(1,2),F(3),F(11))):
            rem=m1-sum(p*cut(e,L,1) for p,e in second)
            need(0<=rem<=m2/L,f'first_uniform_integrability_{n}_{j}')
            tail=sum(p for p,e in second if e>L)
            need(tail<=m2/L**2,f'mass_tail_{n}_{j}')
    return {'schema':'hnm-r30-independent-skeptic-controls-v1','loop':'AT1',
            'passed':True,'checks_count':len(checks),'checks':checks,
            'candidate_B2_over_alpha2_at_cap':str(36+98*cap),
            'scope':'Exact diagnostic algebra and counterexamples supplement the analytic review; no numerical fixture proves completeness.',
            'second_moment_equality':False,'AQ_AO_state_identification':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    result=execute();(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':result['checks_count']}))
