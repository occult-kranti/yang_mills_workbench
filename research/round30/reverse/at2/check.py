#!/usr/bin/env python3
"""AT2 independent exact algebra and logical controls (Python standard library)."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
checks=[]
def check(name, condition, **evidence):
    if name in {x['id'] for x in checks}:
        raise ValueError('duplicate ID '+name)
    if not condition:
        raise ValueError('failed '+name+': '+repr(evidence))
    checks.append({'id':name,'passed':True,'evidence':evidence})
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(tuple,list)):return [clean(t) for t in x]
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    return x
def write(p,x):p.write_text(json.dumps(clean(x),indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def padd(p,q):return [sum(t) for t in zip(p+[F(0)]*max(0,len(q)-len(p)),q+[F(0)]*max(0,len(p)-len(q)))]
def pmul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return out
def pscale(p,c):return [c*x for x in p]
def peval(p,x):return sum(c*x**i for i,c in enumerate(p))
def moment(atoms,k):return sum((w*x**k for x,w in atoms),F(0))

def run():
    a=F(1,16);L=F(8);c=F(3);b=F(49);cap=F(1,100000000)
    qlo=F(1,4)-F(1,500);qhi=F(1,4)+F(1,500);zmax=F(1,250000);B=36+98*cap
    check('strict-positive-denominators',a>0 and L>a and c>0 and b>=a and a*b*b>0)
    check('aq-trace-distance-rational-enclosure',98*cap<F(1,1000)**2,epsilon=98*cap,root_upper=F(1,1000))
    # Exact polynomial identities verify coefficients for all real x.
    ell=[2/c,-1/(c*c)]
    lower_residual=padd([c*c],pscale(pmul([0,1],ell),-c*c))
    square_c=pmul([-c,1],[-c,1])
    check('reciprocal-lower-full-half-line-factorization',lower_residual==square_c,coefficients=lower_residual)
    P=pscale([b*b+2*a*b,-(2*b+a),1],1/(a*b*b))
    upper_residual=padd(pscale(pmul([0,1],P),a*b*b),[-a*b*b])
    factor=pmul([-a,1],pmul([-b,1],[-b,1]))
    check('reciprocal-upper-full-half-line-factorization',upper_residual==factor,coefficients=upper_residual)
    check('second-moment-coefficient-positive',P[2]>0,quadratic_coefficient=P[2])
    check('tangent-uses-no-second-moment',len(ell)==2,coefficients=ell)
    window=lambda q,z:((L+1)*q-L*z-1)/(L-a)
    low=lambda q,z:(7*q-6*z-1)/9
    upper=lambda q,z,ceiling:(ceiling-(2*b+a)+(2*b+a+b*b+2*a*b)*q-(b*b+2*a*b)*z)/(a*b*b)
    cfloor=lambda q,z:(q-z)**2/(1-q)
    A=2*b+a;D=b*b+2*a*b
    check('joint-window-monotonicity',L+1>0 and -L<0)
    check('joint-tangent-monotonicity',F(7,9)>0 and F(-6,9)<0)
    check('joint-upper-monotonicity',A+D>0 and -D<0 and P[2]>0,A=A,D=D)
    check('joint-cauchy-monotonicity',qlo-zmax>0 and 2-qhi-zmax>0 and 1-qhi>0,positive_derivative_numerators=[qlo-zmax,2-qhi-zmax])
    window_floor=window(qlo,zmax);tangent_floor=low(qlo,zmax);upper_ceiling=upper(qhi,0,B);cauchy_floor=cfloor(qlo,zmax);support_ceiling=qhi/a
    check('exact-window-endpoint',window_floor==F(307992,1984375) and window_floor>F(31,200),value=window_floor)
    check('exact-tangent-endpoint',tangent_floor==F(91997,1125000),value=tangent_floor)
    check('exact-upper-endpoint',upper_ceiling==F(28462237549,7503125000),value=upper_ceiling)
    check('exact-cauchy-endpoint',cauchy_floor==F(3843876001,47000000000),value=cauchy_floor)
    check('baseline-comparison',cauchy_floor>tangent_floor and upper_ceiling<support_ceiling,cauchy_minus_tangent=cauchy_floor-tangent_floor,support_minus_upper=support_ceiling-upper_ceiling)
    for q in (qlo,F(1,4),qhi):
        for z in (F(0),zmax):
            check('joint-corner-'+str(q)+'-'+str(z),window(q,z)>=window_floor and low(q,z)>=tangent_floor and upper(q,z,B)<=upper_ceiling and cfloor(q,z)>=cauchy_floor,q=q,z=z,s=q-z,u=1-q)
    # Boundary atom exactly at L stays in the requested closed interval.
    pwin=lambda x:(L-x)/(L-a)
    check('window-endpoint-atom',pwin(L)==0 and int(a<=L<=L)==1,minorant=pwin(L),closed_window_mass=1)
    # Explicit high tail while maintaining the same q=1/4,w=0 moment relations.
    # Mass 1/1000 at 9; remaining mass at (3/4-9/1000)/(1/4-1/1000).
    mass_hi=F(1,1000);mass_lo=F(1,4)-mass_hi;xhi=F(9);xlo=(F(3,4)-mass_hi*xhi)/mass_lo
    tail_atoms=[(xlo,mass_lo),(xhi,mass_hi)]
    check('window-is-not-hard-cutoff',a<xlo<L<xhi and moment(tail_atoms,0)==F(1,4) and moment(tail_atoms,1)==F(3,4) and moment(tail_atoms,2)<36 and mass_hi>0,atoms=tail_atoms,second_moment=moment(tail_atoms,2))
    Aatoms=[(F(2),F(1,8)),(F(4),F(1,8))]
    Batoms=[(F(1),F(1,32)),(F(3),F(3,16)),(F(5),F(1,32))]
    target=[F(1,4),F(3,4),F(5,2)]
    for k in range(3):
        am=moment(Aatoms,k);bm=moment(Batoms,k)
        check('equal-atomic-moment-'+str(k),am==bm==target[k],A=am,B=bm)
    # Uniform centered y on [-sqrt(3),sqrt(3)]: exact symbolic radius squared.
    mass=F(1,4);mean=F(3);radius_squared=F(3)
    Cm=[mass,mass*mean,mass*(mean*mean+radius_squared/3)]
    check('equal-atomless-moments',Cm==target,C=Cm,radius_squared=radius_squared)
    check('continuous-support-above-gap',radius_squared<4 and 3-2>a,lower_rational_support_bound=F(1))
    invA=moment(Aatoms,-1);invB=moment(Batoms,-1)
    N=8;partial=sum((F(1,3)**k/F(2*k+1) for k in range(N)),F(0))/12;remainder=F(1,3)**N/F(8*(2*N+1));chi=partial+remainder
    check('exact-atomic-inverse-values',invA==F(3,32) and invB==F(1,10),A=invA,B=invB)
    check('atomless-inverse-series-enclosure',partial==F(1872586,19702683) and chi==F(254674699,2679564888),lower=partial,upper=chi,remainder=remainder)
    check('same-moments-different-spectra',invA<partial<chi<invB and {x for x,w in Aatoms}!={x for x,w in Batoms},atomic_A=Aatoms,atomic_B=Batoms,atomless_density='constant 1/(8 sqrt(3)) on [3-sqrt(3),3+sqrt(3)]',inverse_C_interval=[partial,chi])
    v=target[2];poly_int=sum(w*peval(P,x) for x,w in Aatoms);poly_ceiling=P[0]*target[0]+P[1]*target[1]+P[2]*B
    check('second-moment-ceiling-is-not-equality',v<B and poly_ceiling-poly_int==P[2]*(B-v)>0,actual_second=v,ceiling=B,substitution_slack=poly_ceiling-poly_int)
    # Wrong sign: k=-x^2 is exactly polynomial; -B cannot upper-bound -v.
    wrong_upper=-B;actual_negative_second=-v
    check('wrong-second-bound-sign',wrong_upper<actual_negative_second,invalid_upper=wrong_upper,actual=actual_negative_second)
    bad=lambda x:(x-F(3,2))**2-F(1,16)
    grid=[a,F(1),F(2),F(3),F(8),F(49),F(100)]
    check('grid-only-positivity-misses-negative-region',all(bad(x)>0 for x in grid) and bad(F(3,2))<0,grid_values=[(x,bad(x)) for x in grid],unsampled_value=bad(F(3,2)))
    # A compatible abstract one-atom moment record differs from reference moments.
    s=qlo-zmax;u=1-qlo;x=u/s;one=[(x,s)]
    check('replace-interacting-moments-by-Haar-values',s!=F(1,4) and u!=F(3,4) and x>a and moment(one,2)<B and window(qlo,zmax)!=window(F(1,4),0),actual_compatible_s=s,actual_compatible_u=u,energy=x,second=moment(one,2),scope='rejects assigning unknown moments; not every substituted bound necessarily false')
    for alpha in (F(1,2),F(1),F(7)):
        response=invA/alpha
        check('inverse-energy-scaling-'+str(alpha),response*alpha==invA,response=response)
    alpha=F(7);hbar=F(3);energy_response=invA/alpha;frequency_response=hbar*energy_response
    check('wrong-inverse-energy-units',energy_response!=invA and frequency_response!=energy_response,dimensionless=invA,energy_inverse=energy_response,frequency_inverse=frequency_response)
    # Direct two-state Rayleigh perturbation coefficient: W10=1/2, gap=3.
    gap=F(3);off=F(1,2);R=off*off/gap
    derivative1=2*off*off/gap;derivative2=4*off*off/gap
    check('unproved-static-susceptibility',R==F(1,12) and derivative1==2*R and derivative2==4*R and derivative1!=derivative2,R=R,source_calibration_1=derivative1,source_calibration_2=derivative2,scope='same undeformed inverse form does not specify calibrated response or infinite-volume differentiability')
    return {'loop':'AT2','direction':'reverse','checks':checks,'check_count':len(checks),'bounds':{'window_mass_lower':window_floor,'inverse_tangent_lower_times_alpha':tangent_floor,'inverse_cauchy_lower_times_alpha':cauchy_floor,'inverse_quadratic_upper_times_alpha':upper_ceiling,'inverse_support_upper_times_alpha':support_ceiling},'equal_moment_controls':{'moments':target,'inverse_A':invA,'inverse_B':invB,'inverse_C_interval':[partial,chi]},'claims':{'actual_aq_state':True,'second_moment_equality':False,'continuum_claim':False,'static_susceptibility_claim':False,'global_optimality_claim':False,'fixtures_are_actual_aq_spectra':False,'scientific_priority_verified':False},'proof_method':'exact full-half-line residual factorizations and joint-moment monotonicity, not grid sampling'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();out=Path(args.output)
    if not out.is_absolute() or out.exists() or any(p.is_symlink() for p in [out]+list(out.parents)):
        raise ValueError('output must be fresh absolute nonsymlink path')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text())
    actual={str(p.relative_to(HERE/'inputs')) for p in (HERE/'inputs').rglob('*') if p.is_file()}
    if actual!=set(inventory)|{'source-inventory.json'}:raise ValueError('input file set mismatch')
    for rel,h in inventory.items():
        p=HERE/'inputs'/rel
        if p.is_symlink() or any(x.is_symlink() for x in p.parents) or sha(p)!=h:raise ValueError('source hash mismatch '+rel)
    contract=json.loads((HERE/'inputs/research/round30/contracts/at2.json').read_text())
    choices=contract['frozen_certificate_choices']
    if contract['id']!='AT2' or (choices['L'],choices['c'],choices['b'])!=(8,3,49):raise ValueError('wrong contract/choices')
    data=run();out.mkdir(parents=True);write(out/'results.json',data)
    sources={str(p.relative_to(HERE)):sha(p) for p in sorted((HERE/'inputs').rglob('*')) if p.is_file()}
    sources.update({'check.py':sha(HERE/'check.py'),'report.md':sha(HERE/'report.md')})
    write(out/'manifest.json',{'loop':'AT2','direction':'reverse','sources':sources,'outputs':{'results.json':sha(out/'results.json')}})
    print(json.dumps({'loop':'AT2','checks':len(checks),'results_sha256':sha(out/'results.json')}))

if __name__=='__main__':main()
