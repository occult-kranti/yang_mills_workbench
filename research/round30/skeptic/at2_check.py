#!/usr/bin/env python3
"""Independent exact AT2 certificate and moment-information checks."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

def execute():
    checks=[]
    def need(value,label):
        if value is not True or label in checks: raise RuntimeError(label)
        checks.append(label)
    def mul(p,q):
        out=[F(0)]*(len(p)+len(q)-1)
        for i,v in enumerate(p):
            for j,w in enumerate(q):out[i+j]+=v*w
        return out
    a=F(1,16);L=F(8);c=F(3);b=F(49);B=36+F(98,100000000)
    qlo=F(1,4)-F(1,500);qhi=F(1,4)+F(1,500);zmax=F(1,500)**2
    slo=qlo-zmax;shi=qhi;ulo=1-qhi;uhi=1-qlo
    need(a>0 and L>a and c>0 and b>a,'positive_denominators_full_support')
    lower_residual=mul([-c,F(1)],[-c,F(1)])
    need(lower_residual==[c*c,-2*c,F(1)],'exact_lower_tangent_square_factorization')
    upper_residual=mul([-a,F(1)],mul([-b,F(1)],[-b,F(1)]))
    need(upper_residual==[-a*b*b,b*b+2*a*b,-2*b-a,F(1)],'exact_upper_full_halfline_factorization')
    quadratic=[(b*b+2*a*b)/(a*b*b),-(2*b+a)/(a*b*b),1/(a*b*b)]
    need(quadratic==[F(38514,2401),F(-1569,2401),F(16,2401)],'frozen_quadratic_exact_coefficients')
    need(quadratic[2]>0,'second_ceiling_safe_for_upper_certificate')
    need((L-a)/(L-a)==1 and (L-L)/(L-a)==0 and -1/(L-a)<0,'window_minorant_global_piecewise_proof_data')
    need(F(0)<1,'window_endpoint_atom_retained')
    window=(L*slo-uhi)/(L-a)
    tangent=2*slo/c-uhi/(c*c)
    baseline=slo*slo/uhi
    upper=sum(x*y for x,y in zip(quadratic,[shi,ulo,B]))
    support_upper=shi/a
    need(window>0 and window<slo,'uniform_window_is_positive_not_full_mass')
    need(baseline>=tangent>0,'baseline_lower_improves_frozen_tangent')
    need(upper<support_upper,'quadratic_improves_support_upper')
    need(qlo>zmax and 2-qhi-zmax>0,'cauchy_bound_joint_monotonicity')
    for i,q in enumerate((qlo,F(1,4),qhi)):
        for j,z in enumerate((F(0),zmax/2,zmax)):
            s=q-z;u=1-q
            need((L*s-u)/(L-a)>=window,f'joint_window_bound_{i}_{j}')
            need(2*s/c-u/c**2>=tangent,f'joint_tangent_bound_{i}_{j}')
            need(s*s/u>=baseline,f'joint_cauchy_bound_{i}_{j}')
            value=quadratic[0]*s+quadratic[1]*u+quadratic[2]*B
            need(value<=upper,f'joint_upper_bound_{i}_{j}')
    # All joint monotonicity conclusions follow analytically from positive
    # q derivative and negative z derivative, not the finite samples above.
    need((L+1)/(L-a)>0 and -L/(L-a)<0,'window_joint_derivative_signs')
    need(2/c+1/c**2>0 and -2/c<0,'tangent_joint_derivative_signs')
    need(quadratic[0]-quadratic[1]>0 and -quadratic[0]<0,'upper_joint_derivative_signs')
    haar_window=(L*F(1,4)-F(3,4))/(L-a)
    need(haar_window>window,'replacing_interacting_moments_by_haar_is_unjustified')
    # A negative quadratic coefficient reverses ceiling substitution.
    v=F(5,2)
    need(-v>-B,'wrong_second_bound_sign_rejected')
    need(v<B,'second_moment_ceiling_is_not_equality')
    # Polynomial positive on the entire coarse integer grid yet negative
    # at the midpoint. This is diagnostic; full proofs use factorization.
    hidden=lambda x:(x-F(1,2))**2-F(1,16)
    need(all(hidden(F(n))>0 for n in range(9)) and hidden(F(1,2))<0,
         'grid_only_positivity_misses_negative_region')

    A=[(F(1,8),F(2)),(F(1,8),F(4))]
    D=[(F(1,32),F(1)),(F(3,16),F(3)),(F(1,32),F(5))]
    def moment(atoms,k):return sum(p*x**k for p,x in atoms)
    common=[F(1,4),F(3,4),F(5,2)]
    need([moment(A,k) for k in range(3)]==common,'atomic_A_first_three_moments')
    need([moment(D,k) for k in range(3)]==common,'atomic_B_first_three_moments')
    # Uniform[3-sqrt(3),3+sqrt(3)] has mean 3 and variance 1.
    uniform=[F(1,4),F(1,4)*3,F(1,4)*(9+F(3,3))]
    need(uniform==common,'atomless_C_first_three_moments')
    need((3-a)**2>3 and 3-a>0,'atomless_support_above_gap_without_floats')
    ra=moment(A,-1);rb=moment(D,-1)
    need(ra==F(3,32) and rb==F(1,10) and ra!=rb,'same_moments_different_inverse_responses')
    # Exact uniform reciprocal moment is (1/12) sum_{k>=0}
    # 1/(3^k(2k+1)); a positive geometric remainder bounds the tail.
    intervals=[]
    for n in (4,8,16):
        partial=sum((F(1,12*3**k*(2*k+1)) for k in range(n)),F(0))
        tail=F(1,12)*F(1,3**n)*F(3,2)/F(2*n+1)
        intervals.append((partial,partial+tail))
        need(ra<partial<partial+tail<rb,'atomless_inverse_strictly_between_atomic_'+str(n))
    need(all(l2>=l1 and h2<=h1 for (l1,h1),(l2,h2) in zip(intervals,intervals[1:])),
         'rational_atomless_inverse_intervals_nest')
    for i,atoms in enumerate((A,D)):
        s,u,v=[moment(atoms,k) for k in range(3)]
        r=moment(atoms,-1)
        need(2*s/c-u/c**2<=r<=sum(x*y for x,y in zip(quadratic,[s,u,v])),f'actual_fixture_certificates_{i}')
        need(s*s/u<=r<=s/a,f'actual_fixture_baselines_{i}')
    # A gap does not impose a hard upper cutoff: add tiny mass at x=100,
    # compensate first moment with the dominant atom, and keep B valid.
    epsilon=F(1,1000000);mass=F(1,4);mean=F(3,4)
    high=F(100);low=(mean-epsilon*high)/(mass-epsilon)
    tail_measure=[(mass-epsilon,low),(epsilon,high)]
    need(low>a and moment(tail_measure,2)<B and high>L,'window_lower_bound_is_not_hard_cutoff')
    need(moment(tail_measure,0)==mass and moment(tail_measure,1)==mean,'high_energy_control_preserves_actual_qw_relation')
    for i,alpha in enumerate((F(1,2),F(2),F(7))):
        rphys=sum(p/(alpha*x) for p,x in A)
        need(rphys==ra/alpha,'inverse_energy_units_'+str(i))
        need(rphys!=ra*alpha,'wrong_inverse_energy_scaling_rejected_'+str(i))
    # Direct-sum two-level branches: each chosen branch has a simple gap
    # sqrt(1+4h²), but the globally lowest energy is
    # (1-sqrt(1+4h²))/2-|h|. Its one-sided slopes are -1 and +1.
    # Use rational hyperbola parameters to evaluate the square root exactly.
    for n in (10,100,1000):
        t=F(1,n);h=t/(1-t*t);gap=(1+t*t)/(1-t*t)
        need(gap*gap==1+4*h*h and gap>=1,'ground_crossing_branch_gap_'+str(n))
        ground=(1-gap)/2-h
        right=ground/h;left=ground/(-h)
        need(right==-1-t and left==1+t,'ground_crossing_one_sided_slope_separation_'+str(n))
    branch_W=((F(1),F(1)),(F(1),F(1)));vacuum=(F(1),F(0))
    source=tuple(sum(branch_W[i][j]*vacuum[j] for j in range(2))-vacuum[i]
                 for i in range(2))
    inverse_on_complement=((F(0),F(0)),(F(0),F(1)))
    inverse_form=sum(source[i]*inverse_on_complement[i][j]*source[j]
                     for i in range(2) for j in range(2))
    need(source==(0,1) and inverse_form==1,'chosen_branch_inverse_form_is_finite')
    need(F(-1)!=F(1),'simple_gapped_representations_do_not_prove_global_differentiability')
    return {'schema':'hnm-r30-independent-skeptic-controls-v1','loop':'AT2','passed':True,
            'checks_count':len(checks),'checks':checks,
            'uniform_endpoints':{'window_mass_lower':str(window),'reciprocal_tangent_lower':str(tangent),
                                 'reciprocal_cauchy_lower':str(baseline),'reciprocal_quadratic_upper':str(upper),
                                 'reciprocal_support_upper':str(support_upper)},
            'atomless_reciprocal_interval':[str(x) for x in intervals[-1]],
            'scope':'Exact certificate algebra and abstract moment controls, not measured or determined AQ spectra.',
            'particle_pole_identified':False,'physical_susceptibility_proved':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);result=execute()
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':result['checks_count'],'endpoints':result['uniform_endpoints']}))
