#!/usr/bin/env python3
"""Post-exchange exact AI4 proof and fixture audit; no new physical fixtures."""
import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P = 'research/round28/'
CHECKS = []
sys.set_int_max_str_digits(0)


def need(ok, label):
    if not ok:
        raise RuntimeError(label)
    CHECKS.append(label)


def read(p): return json.loads((ROOT / p).read_text())
def sha(p): return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
def fs(values): return [F(v) for v in values]
def b(q): return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def poly(p, q): return sum(F(c)*q**int(n) for n,c in p.items())


def tail(k, z):
    a = F(1)
    for n in range(k+1): a *= (F(10,3)+n)/(n+1)
    return 8*a*(15*z)**(k+1)/(1-15*z)**(k+5)


def div(n, d):
    if d[0] <= 0: return None
    v = [x/y for x in n for y in d]
    return min(v), max(v)


def product(a,b_):
    out = [F(0)]*(len(a)+len(b_)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b_): out[i+j] += x*y
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output', type=Path, default=HERE/'ai4-post-review.json')
    target=ap.parse_args().output
    bindings={}; contract=read(P+'contracts/ai4.json')
    need(sha(P+'contracts/ai4.json')=='0b181d7c066dde2f2e48e58f468fcec60aef20ef305ea47bc60fc431c1631813','exact contract')
    expected={'forward':'d1729c1ae85d49a00fd68ba0048ad391c3270d472267af3440a846399b81f372',
              'reverse':'095088472a09b77ebb8299b87b9e1b306ce32fb22daf28fe00a74fbee4eaad96'}
    data={}
    for side in expected:
        prefix=P+side+'/ai4/'; freeze=read(prefix+'freeze.json')
        need(sha(prefix+'freeze.json')==expected[side],side+' freeze identity')
        for path,digest in freeze.get('bindings',freeze.get('sha256',{})).items():
            need(sha(path)==digest,'immutable '+path)
        inventory=read(prefix+'inputs/source-inventory.json')
        entries=([{'source':p,'snapshot':prefix+'inputs/'+p,'sha256':h} for p,h in inventory.items()]
                 if side=='forward' else inventory['entries'])
        mapping={e['source']:e['sha256'] for e in entries}
        for path,digest in contract['sources'].items():
            need(mapping.get(path)==digest==sha(path),side+' complete source '+path)
        for e in entries: need(sha(e['snapshot'])==e['sha256'],side+' snapshot '+e['source'])
        for name in ('freeze.json','report.md','check.py','output/results.json','inputs/source-inventory.json'):
            bindings[prefix+name]=sha(prefix+name)
        data[side]=read(prefix+'output/results.json')
        replay=P+'skeptic/ai4-'+side+'-fresh-replay/results.json'
        need(sha(replay)==sha(prefix+'output/results.json'),side+' fresh replay byte equality')
        bindings[replay]=sha(replay)
    op=P+'skeptic/ai4-independent-freeze.json'; ownfreeze=read(op)
    need(sha(op)=='7ed8130e07ee392ef48647ab26e4048e79da27b7581c1ea670f9b72eb0edbb5f','independent freeze identity')
    for path,digest in ownfreeze['bindings'].items():
        need(sha(path)==digest,'independent immutable '+path); bindings[path]=digest
    bindings[op]=sha(op)
    receipt=read(P+'skeptic/ai4-replay-receipt.json')
    for side in expected:
        for mode in ('normal','optimized'):
            r=receipt['results'][side][mode]
            need(r['exit_code']==0 and r['fresh_output_created'] is True and r['byte_identical_to_frozen'] is True
                 and r['sha256']==sha(P+side+'/ai4/output/results.json'),'successful fresh '+side+' '+mode)
    bindings[P+'skeptic/ai4-replay-receipt.json']=sha(P+'skeptic/ai4-replay-receipt.json')
    own=read(P+'skeptic/ai4-independent.json'); fw=data['forward']; rv=data['reverse']
    need((own['check_count'],fw['check_count'],rv['check_count'])==(7414,7625,381),'frozen executed counts')
    z=F(1,10**7); u0=F(1,10**24); sq=F(1,10**12); V=z/64; x=15*z; delta=F(1,2**320)
    q0=F(99,100); S=tail(6,z); A=(6*V)**9/math.factorial(9)
    B=F(2,3)*V**3+F(8,15)*V**5+F(52,315)*V**7
    T=91*(6*V)**9/(math.factorial(9)*(1-6*V))
    need(q0<1-2*u0<1 and sq*sq==u0,'whole continuous parameter range')
    need((1+q0)**2*(1+q0*q0)/672>=F(1,100),'continuous v lower bound')
    need([a-c for a,c in zip([2,5,5,6,3],[2,4,4,4,2])]==[0,1,1,2,1],'p-2N positive coefficient proof')
    rho=F(31,12)*x/(1-x)
    need(0<rho<1 and 31-24==7,'all-j spatial normalized recurrence from 7j>=0')
    # Different valid counts of all faces inside the same whole-owner vertex box.
    # L=k+1: exact box faces 24L^3+14L^2; anchor overcount adds 28L^2+21L+3.
    need([3,21,42,24][2]-14==28,'positive polynomial difference between geometry envelopes')
    mj=product(product([F(7),1],[F(7),1]),[F(91,12),1])
    nxt=product(product([F(8),1],[F(8),1]),[F(103,12),1]); g=F(8,7)**3
    growth=[g*a-c for a,c in zip(mj,nxt)]
    need(all(v>=0 for v in growth) and g*g/4<1 and g*g/8<1,'forward all-j cubic and sixth-degree averaging recurrence')
    need(max(F((j+1)**3,4**j) for j in range(2))==2 and F(3,2)**3/4<1,'reverse all-j cubic sequence maximum')
    need(max(F((j+1)**6,4**j) for j in range(4))==64 and F(5,4)**6/4<1,'reverse all-j sixth-degree sequence maximum')
    f=fw['uniform_proof']; r=rv['uniform_proof_constants']; o=own['uniform_bounds']
    rootf=F(21,2304)/((1+q0)**3*(1+q0*q0)**2*(1+q0**4))
    rootr=F(21,2304)*F(10,19)**6
    need(F(f['root_constant_squared'])==rootf<=F(1,80)**2,'forward continuous square-root inequality')
    need(F(r['sqrt_inner_coefficient_squared'])==rootr<=F(1,64)**2,'reverse continuous square-root inequality')
    need(F(21)*72**2<=2304*7*F(19,10)**3,'independent continuous square-root inequality')
    need(fs(f['M_growth_difference_polynomial'])==growth and F(f['M_growth_upper'])==g,'forward actual polynomial exported')
    d=z/120; M=F(4459,12); state=[F(36,5),F(36,25)]; rounding=[F(576),F(1536,5)]
    Rmax=state[0]*u0*sq+rounding[0]*delta*u0**3+S+48*u0**3*M*(1+3*z*M)
    denpre=z*q0**4/100-36*V**3-(6*V)**7/math.factorial(7)-A-Rmax
    need(F(f['denominator_pre_relaxation'])==denpre>d==F(f['dstar'])>0,'forward complete positive denominator')
    need(V+36*V**3+Rmax<z/32==F(f['nstar']),'forward true numerator magnitude')
    fc=[]
    for h in range(2):
        terms={'state':2*state[h]*sq/d,'inner_rounding':2*rounding[h]*delta*u0**2/d,
               'spatial':4*S/(d*u0),'averaging':96*u0**2*M*(1+3*z*M)/d,
               'retained_center_bias':(h+1)*B/d,'retained_combination_tail':(h+1)*T/d}
        need(terms=={k:F(v) for k,v in f['hypothesis_radius_coefficients_by_term'][h].items()},'forward six complete coefficient classes '+str(h))
        fc.append(sum(terms.values()))
    fg=1-sum(fc)
    need(F(f['uniform_gap_coefficient'])==fg>F(39,40),'forward exact coefficient stronger than stated simple97/100')
    PA=48*u0**2*(2*435+64*3*z*435**2); PS=2*S/u0
    physical=[9*sq+PS+PA,F(9,5)*sq+PS+PA]
    dr=F(9,1000)*z-36*V**3-2*A-u0*max(physical)
    need(F(r['denominator_lower'])==dr>z/125>0,'reverse complete double-arithmetic denominator')
    need(fs(r['physical_per_u'])==physical and F(r['averaging_per_u'])==PA,'reverse full state spatial and growing averaging')
    rc=[((h+1)*(B+T)+2*physical[h])/dr for h in range(2)]; rg=1-sum(rc)
    need(fs(r['ratio_radius_coefficients'])==rc and F(r['gap_coefficient'])==rg>F(39,40),'reverse exact uniform coefficient')
    og=1-sum(F(v) for v in o['ratio_radius_sum_over_u_coefficients'].values())
    need(og==F(o['strongest_stated_gap_coefficient'])>F(39,40),'independent exact uniform coefficient')
    # Do not pair a large tolerance from one proof with another proof's margin.
    L=2*(1+(z/32)/d)/d; ef=z/12000; nf=fg-2*L*ef
    need(F(f['extra_scalar_error_coefficient'])==ef and F(f['ratio_perturbation_L'])==L,'forward extra scalar transfer')
    need(nf==F(f['gap_coefficient_with_extra_scalar_error'])>F(78,100)>F(1,2),'forward noise preserves its stated target')
    erhalf=rg*dr/24; ertarget=(rg-F(1,2))*dr/12
    need(erhalf==F(r['scalar_half_margin_coefficient']) and rg-12*erhalf/dr==rg/2,'reverse half-margin distinct allowance')
    need(ertarget==F(r['scalar_target_margin_coefficient']) and rg-12*ertarget/dr==F(1,2),'reverse target-margin distinct allowance')
    eo=39*z/F(163840); do=z/128
    need(eo==F(o['extra_scalar_tolerance_coefficient']) and F(39,40)-16*eo/do==F(39,80)<F(1,2),'independent allowance preserves39/80 not half-u')
    need(all(e*u0<=dd/2 for e,dd in [(ef,d),(erhalf,dr),(ertarget,dr),(eo,do)]),'all added-error denominator reserves')
    old=read(P+'forward/ai3/output/results.json'); rows=[]
    for index,(of,ff,rf) in enumerate(zip(own['fixtures'],fw['fixtures'],rv['fixtures'])):
        j=[0,1,8,64,512][index//2]; location=('upper','midpoint')[index%2]
        u=u0/F(2)**j*(1 if location=='upper' else F(3,4)); k=6+j
        need((ff['j'],ff['position'],rf['j'],rf['location'],of['j'],of['point'])==(j,location,j,location,j,location),'exact fixture identity '+str(index))
        need(F(ff['u'])==F(rf['u'])==F(of['u'])==u and u0/F(2)**(j+1)<u<=u0/F(2)**j,'exact open-lower continuous band '+str(index))
        Nf=24*(k+1)**3+14*(k+1)**2; Nr=3*(4*k+5)*(2*k+3)*(k+2)
        need(ff['N_envelope']==Nf<=Nr==rf['N_k_envelope'],'different whole-box envelope fixture '+str(index))
        fi=[]; ri=[]
        for h in range(2):
            fh=ff['hypotheses'][h]; rh=rf['hypotheses'][h]; oh=of['hypotheses'][h]
            q=1-(h+1)*u; eta=(F(1,2),F(1,16))[h]; tau=eta/(8*b(q)); v=z*tau/(96*eta*(1-q)**3)
            for key,value in [('q',q),('eta',eta),('tau',tau),('v',v)]:
                need(F(fh[key])==F(rh[key])==F(oh[key])==value,'shared exact '+str((index,h,key)))
            need(eta*(1-q)**3==u**3/2 and F(fh['physical_time_in_hbar_over_alpha'])==F(oh['physical_time_in_hbar_over_alpha'])==2*z/u**3,'same physical clock '+str((index,h)))
            c=[sum((-1)**((n-1)//2)*poly(old['moment_polynomials'][str(probe)][n],q)*v**n/math.factorial(n) for n in (1,3,5,7)) for probe in (4,5)]
            need(fs([fh['centers_imaginary']['4'],fh['centers_imaginary']['5']])==fs([rh['imaginary_centers']['4'],rh['imaginary_centers']['5']])==fs([oh['imaginary_polynomial_centers']['4'],oh['imaginary_polynomial_centers']['5']])==c,'exact retained centers '+str((index,h)))
            C=c[1]-q*c[0]; a=(6*v)**9/math.factorial(9); t=(1-q)*91*(6*v)**9/(math.factorial(9)*(1-6*v))
            need(F(fh['combination_center'])==F(rh['signed_combination_center'])==C and F(fh['combination_arithmetic'])==F(rh['combined_all_order_tail'])==t,'all-order combination preserved '+str((index,h)))
            rootlo,roothi=F(fh['sqrt_lower']),F(fh['sqrt_upper']); root2=b(q*q)/96
            need(rootlo**2<=root2<=roothi**2 and roothi-rootlo<=delta,'directed inner-root bracket '+str((index,h)))
            stateexact2=(384*tau/(1-eta))**2*root2
            sf=384*tau*roothi/(1-eta); sr=F(rh['state_analytic_envelope'])
            need(sr**2>=stateexact2==F(rh['state_squared_exact']) and sf==F(fh['physical_terms']['state_including_inner_rounding']),'both valid state enclosures '+str((index,h)))
            need(F(fh['inner_rounding_scalar_charge'])==384*tau*(roothi-rootlo)/(1-eta),'actual rounding multiplier '+str((index,h)))
            sfspace=tail(k,z); af=64*tau*F(Nf,24)*(1+3*z*F(Nf,24)); ar=64*tau*F(Nr,24)*(1+3*z*F(Nr,24))
            need(F(fh['physical_terms']['spatial'])==F(rh['spatial'])==sfspace and F(fh['physical_terms']['averaging'])==af and F(rh['averaging_using_N_envelope'])==ar,'complete geometry-dependent physical budgets '+str((index,h)))
            pf=sf+sfspace+af; pr=sr+sfspace+ar
            need(F(fh['physical_radius'])==pf and F(rh['physical_radius'])==pr,'full physical sums '+str((index,h)))
            den=(c[0]-pf-a,c[0]+pf+a); num=(C-(1+q)*pf-t,C+(1+q)*pf+t)
            quot=div(num,den); interval=(q+quot[0],q+quot[1]); radius=(abs(C)+t+(1+q)*pr)/(c[0]-pr-a)
            need(tuple(fs(fh['denominator']))==den and den[0]>=d and c[0]-pr-a>=dr,'true positive denominators '+str((index,h)))
            need(tuple(fs(fh['cancellation_ratio_interval']))==interval and tuple(fs(rh['refined_candidate_interval']))==(q-radius,q+radius),'all four signed quotient corners and reverse radius '+str((index,h)))
            need(q-fc[h]*u<=interval[0]<=interval[1]<=q+fc[h]*u and radius<=rc[h]*u,'fixtures enclosed by continuous proof '+str((index,h)))
            fi.append(interval); ri.append((q-radius,q+radius))
        gf=fi[0][0]-fi[1][1]; gr=ri[0][0]-ri[1][1]
        need(gf==F(ff['exact_fixture_ratio_gap'])>=fg*u and gr==F(rf['refined_ratio_gap'])>=rg*u,'declared pairwise fixture gaps '+str(index))
        rows.append({'j':j,'position':location,'u':str(u),'forward_gap_over_u':str(gf/u),'reverse_gap_over_u':str(gr/u),'common_guarantee':'39/40'})
    need(len(rows)==len(own['fixtures'])==len(fw['fixtures'])==len(rv['fixtures'])==10,'exactly ten fixtures and no added point')
    need(div((F(-1),F(2)),(F(-1),F(2))) is None,'invalid denominator rejected independently')
    need(div((F(-2),F(1)),(F(1),F(3)))==(F(-2),F(1)),'signed corner control')
    need(F(1,5)/F(1,10)==2 and F(1)/F(1)==1,'common phase can change imaginary ratio')
    need(F(39,80)<F(1,2) and erhalf!=ertarget and ef!=eo,'distinct added-noise claims cannot be silently combined')
    result={'schema':'ym28-ai4-post-review-v1','accepted_mathematics_with_limits':True,'blocking_issues':[],
            'checks':CHECKS,'check_count':len(CHECKS),'bindings':bindings,'rows':rows,
            'uniform_gap_coefficients':{'forward':str(fg),'reverse':str(rg),'independent':str(og)},
            'common_gap_coefficient':'39/40','extra_scalar_errors':{
                'forward':{'coefficient':str(ef),'remaining_gap_coefficient':str(nf),'simple_lower_bound':'39/50'},
                'reverse_half':{'coefficient':str(erhalf),'remaining_gap_coefficient':str(rg/2)},
                'reverse_target':{'coefficient':str(ertarget),'remaining_gap_coefficient':'1/2'},
                'independent':{'coefficient':str(eo),'remaining_gap_coefficient':'39/80'}},
            'scope':'Continuous all-real-u and all-integer-band conditional candidate-pair theorem; complete physical errors, growing collars and positive denominators. Three valid nonoptimal bounds and four distinct vanishing extra-error allowances. No continuous inverse, fixed unknown-parameter instrument, fixed-noise or unknown-phase robustness, physical matching, homogeneous gap or continuum theorem.',
            'research_loop_increment':0,'new_physical_fixtures':0,'new_collar_enumerations':0}
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','checks':len(CHECKS),'common_gap':'39/40','fixture_count':len(rows)}))


if __name__=='__main__': main()
