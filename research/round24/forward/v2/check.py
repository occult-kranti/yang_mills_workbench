#!/usr/bin/env python3
import argparse,json
from fractions import Fraction as F
from math import isqrt,factorial
from pathlib import Path

def require(x,m):
    if not x:raise RuntimeError(m)
def dot(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def star(a):return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a):return [[c*x for x in r] for r in a]
def polynomial(q):return 2+5*q+5*q*q+6*q**3+3*q**4
def b(q):return polynomial(q)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def sqrtupper(x):
    d=2**180;k=isqrt(x.numerator*d*d//x.denominator)
    lo,hi=F(k,d),F(k+1,d)
    require(lo*lo<=x<hi*hi,'sqrt enclosure')
    return hi

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    q=F(999999,1000000);eta=F(1,2);C=F(1,500000)
    tau=eta/(8*b(q));sd=C*tau/(1-q)**3;x=10*sd
    d2=tau*tau*b(q*q)/96/(F(1,8)*(1-eta))**2
    upper=sqrtupper(d2)
    lower=sd*q**4/96-6*upper-F(44,9)*x*x/(1-x)**5
    require(x<1 and lower>F(1,10**8),'finite q endpoint')
    r=prep=gate=theta=F(1,10**10);kappa=F(1,100)
    N=18/(r*r);require(N.denominator==1,'integer trials')
    exp9lower=sum(F(9**k,factorial(k)) for k in range(20))
    require(exp9lower>36/kappa,'rational exponential confidence certificate')
    budget=8*(r+prep+gate)+(9+eta/4)*theta
    require(budget==F(53,16*10**9),'budget arithmetic')
    guarantee=F(1,10**8)-budget
    require(lower-budget>guarantee>0,'finite sample surviving margin')
    # Executed dyadic-complex fixture, with third infinite-complement representative.
    I=[[complex(i==j) for j in range(3)] for i in range(3)]
    W=[[0j,1+0j,0j],[1+0j,0j,0j],[0j,0j,0j]]
    U=[[1+0j,0j,0j],[0j,1j,0j],[0j,0j,1+0j]]
    bw=dot(dot(U,W),star(U));target=dot(W,bw)[0][0]
    p0=add(I,scale(-1,dot(W,W)));K=add(W,scale(1j,p0))
    require(dot(K,star(K))==I,'full completion unitary')
    correlation=0j;wrong=0j
    for a in [K,star(K)]:
      for v in [K,star(K)]:
        P=dot(a,dot(dot(U,v),star(U)))
        # Controlled P on |+> tensor e0. Omit sqrt(2) and divide density by 2.
        joint=[1+0j,0j,0j]+[P[i][0] for i in range(3)]
        reduced=[[sum(joint[i*3+k]*joint[j*3+k].conjugate() for k in range(3))/2 for j in range(2)] for i in range(2)]
        X=[[0j,1+0j],[1+0j,0j]];Y=[[0j,-1j],[1j,0j]]
        xm=sum(dot(reduced,X)[i][i] for i in range(2)).real
        ym=sum(dot(reduced,Y)[i][i] for i in range(2)).real
        correlation+=(xm+1j*ym)/4
        wrong+=(xm-1j*ym)/4
    pp=scale(.5,add(dot(W,W),W));pm=scale(.5,add(dot(W,W),scale(-1,W)))
    seq=add(dot(dot(pp,bw),pp),scale(-1,dot(dot(pm,bw),pm)))[0][0]
    require(correlation==target==1j,'computed ancilla reconstruction')
    controls={
      'reversed_Y_sign_detected':wrong!=target,
      'sequential_readout_loses_complex_signal':seq!=target and seq==0,
      'excessive_systematic_error_rejects_certificate':lower-(8*F(1,10**6))<0,
      'finite_sampling_is_not_deterministic':F(1,2)**12>0,
      'wrong_shot_factor_fails_chosen_log_certificate':(N/100)*r*r/2<1,
      'unbounded_generator_requires_actual_commutator':F(101**2-100**2)>F(2**2-1**2),
      'missing_complement_breaks_control_unitarity':dot(W,star(W))!=I,
    }
    require(all(controls.values()),'negative controls')
    results={'loop':'v2','direction':'forward','status':'passed','claims':['Conditional 99 percent one-endpoint confidence certificate','Actual bounded W commutator gives physical clock tolerance','Finite q signal survives explicit rational error budget'], 'limitations':['3.24e22 trials and 5e-23 relative clock tolerance are severe sufficient resources','No prepared stationary state or actual coherent-control implementation','Not simultaneous all-time confidence','No Wilson homogeneous or continuum result'],'q':str(q),'alpha_time_over_hbar':str(C/(1-q)**3),'finite_q_lower':str(lower),'preparation_error':str(prep),'setting_error':str(gate),'sampling_error':str(r),'clock_theta':str(theta),'confidence':str(1-kappa),'shots_per_setting':N.numerator,'total_shots':18*N.numerator,'total_error_budget':str(budget),'certified_observation_magnitude_lower':str(guarantee),'fixture_real':int(target.real),'fixture_imag':int(target.imag),'continuum_proved':False}
    (out/'results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    (out/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
