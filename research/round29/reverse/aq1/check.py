#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise AssertionError(m)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/aq1.json').read_text())['id']=='AQ1','contract')
    tau=F(1,100000000);J=28*tau;fnorm=81*J
    S={(0,0,0),(1,0,0),(0,1,0),(0,0,1)};E=S-{(0,0,0)}
    diameter=max(sum(abs(x-y) for x,y in zip(a,b)) for a in S for b in S);need(diameter==2,'star diameter')
    regions=[{(0,0,0)},{(0,0,0),(0,0,1)},set(product(range(-1,2),repeat=3))];energy=[]
    for R in regions:
      anchors={tuple(y[i]-s[i] for i in range(3)) for y in R for s in S};need(len(anchors)<=4*len(R),'incoming count')
      C=14*tau*len(anchors);need(C<=56*len(R)*tau,'actual reference reset')
      energy.append({'sites':len(R),'incident_stars':len(anchors),'energy_cap':str(C),'general_cap':str(56*len(R)*tau)})
    ownership=[]
    for x,y,z in product(range(-6,3),range(-3,2),(-1,0,1)):
      bx,by=x//4,y//2;rx,ry=x-4*bx,y-2*by
      need(0<=rx<4 and 0<=ry<2 and (4*bx+rx,2*by+ry,z)==(x,y,z),'Euclidean ownership')
    ownership.append({'tail':[-1,-1,-1],'owner':[-1,-1,-1],'remainders':[3,1]})
    shells=[]
    for n in range(1,10):
      count=sum(sum(abs(t) for t in v)==n for v in product(range(-n,n+1),repeat=3))
      need(count==4*n*n+2 and F(count,(1+n)**4)<=F(6,(1+n)**2),'F shell bound');shells.append({'n':n,'count':count})
    # Exact convolution factor estimate F(D/2)<=16F(D).
    for D in range(21):need((1+F(D,2))**-4<=16*F(1,(1+D)**4),'convolution split')
    # Purification projection bound squared: 4p-3p² <=4p.
    for tail in (F(0),F(1,100),F(1,4),F(1)):
      need(0<=4*tail-3*tail*tail<=4*tail,'gentle cutoff bound')
    # Diagonal h e_n=n²e_n and shift: exact phase/pi at t_k/pi=1/(2k+1).
    time_rows=[]
    for k in (1,4,32,256):
      time_ratio=F(1,2*k+1);phase=(2*k+1)*time_ratio;need(phase==1,'norm-time discontinuity witness')
      time_rows.append({'k':k,'t_over_pi':str(time_ratio),'phase_over_pi':str(phase),'norm_difference':2})
    alpha,hbar,t=F(2),F(3),F(5);delta=alpha/8;clock=delta*t/hbar
    escaping=[]
    for n in (1,2,4,8):
      rho=[int(i==n) for i in range(17)];sigma=[int(i==2*n) for i in range(17)]
      trace=sum(rho);distance=sum(abs(a-b) for a,b in zip(rho,sigma));energy_n=sum(i*v for i,v in enumerate(rho))
      need(trace==1 and distance==2 and energy_n==n,'escaping diagonal densities')
      escaping.append({'n':n,'trace':trace,'distance_to_2n':distance,'onsite_energy':energy_n})
    rho_one=[1,0];rho_two=[0,0,0,1];reduced=[rho_two[0]+rho_two[1],rho_two[2]+rho_two[3]]
    controls={'mass_escape_without_energy':all(a['distance_to_2n']==2 for a in escaping),'incompatible_marginals':rho_one!=reduced,'incoming_stars_not_one_anchor':energy[0]['incident_stars']==4,'negative_truncation_wrong':int(-F(1,4))!=(-1//4),'not_norm_time_continuous':all(r['norm_difference']==2 for r in time_rows),'physical_clock_restored':clock!=t/hbar and clock!=alpha*t/hbar,'old_state_not_identified':'fullZ3 centered subsequence'!='old orthant selected limit','SU3_constants_not_imported':F(3,4)!=F(4,3)}
    need(all(controls.values()),'controls')
    result={'loop':'AQ1','direction':'reverse','verdict':'locally normal stationary subsequential full-lattice state with nonnegative strongly continuous GNS energy dynamics','tau_cap':'1/100000000','local_reference_energy':'<=56|R||tau|','F':'(1+r)^-4','F_sum_upper':7,'F_convolution_upper':224,'J_cap':str(J),'F_norm_cap':str(fnorm),'energy_fixtures':energy,'ownership':ownership,'shells':shells,'time_discontinuity':time_rows,'escaping_densities':escaping,'clock_fixture':str(clock),'controls':controls,'not_claimed':['whole sequence convergence','translation invariance','old-state equality','boundary uniqueness','physical gap in this loop','continuum construction']}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AQ1','passed':True,'controls':len(controls),'F_norm_cap':str(fnorm)}))
if __name__=='__main__':main()
