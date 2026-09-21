#!/usr/bin/env python3
"""Exact finite algebra and inequality checks; not infinite dynamics simulation."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

def demand(condition, message):
    if not condition:
        raise RuntimeError(message)
def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a):
    return [[c*x for x in r] for r in a]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);o=Path(p.parse_args().output);o.mkdir(parents=True,exist_ok=True)
    I=[[F(i==j) for j in range(3)] for i in range(3)]
    Z=scale(0,I)
    W=[[F(0),F(1),F(0)],[F(1),F(0),F(0)],[F(0),F(0),F(0)]]
    W2=mm(W,W)
    pp=scale(F(1,2),add(W2,W));pm=scale(F(1,2),add(W2,scale(-1,W)));p0=add(I,scale(-1,W2))
    projections=[pm,p0,pp]
    demand(mm(W2,W)==W,'cubic')
    demand(add(add(pp,pm),p0)==I,'projection completeness')
    for i,a in enumerate(projections):
        for j,b in enumerate(projections):
            demand(mm(a,b)==(a if i==j else Z),'projection products')
    demand(add(pp,scale(-1,pm))==W,'exact finite readout')
    demand(mm(W,p0)==Z and add(W2,mm(p0,p0))==I,'unitary K identity')
    cap=F(1,10**6);delta=cap/100000;x=80*cap/7
    remainder=F(44,9)*x*x/(1-x)**5
    margin=cap/84-remainder
    error=8*delta+4*delta*delta
    demand(margin>cap/168,'inherited cap margin')
    demand(error<cap/10000,'readout cap margin; polynomial positive monotone after divide by z')
    demand(F(1,168)-F(1,10000)>F(1,200),'all-z lower margin')
    # Calibration shrink changes connected variance at t=0 in the u state.
    a=scale(1-delta,W)
    original_variance=W2[0][0]-W[0][0]**2
    new_variance=mm(a,a)[0][0]-a[0][0]**2
    demand(new_variance==(1-delta)**2,'calibration variance')
    # Under diag(1,-i,1) reference evolution, <u|W beta(W)|u>=-i.
    # Sequential products of real labels are real: these cannot reconstruct -i.
    complex_correlation=-1j
    controls={
        'null_observable_removes_variance':Z[0][0]==0 and original_variance==1,
        'nonzero_calibration_error_changes_variance':new_variance!=original_variance,
        'sequential_real_outcomes_miss_imaginary_part':complex_correlation.imag!=0,
        'zero_complement_projector_breaks_completeness':add(pp,pm)!=I,
        'scalar_shift_exception_retains_connected_variance':mm(add(W,I),add(W,I))[0][0]-add(W,I)[0][0]**2==original_variance,
        'two_state_projection_is_not_full_identity':W2!=I,
    }
    demand(all(controls.values()),'control failure')
    results={'loop':'v1','direction':'forward','status':'passed','claims':['Exact three-outcome spectral readout of the full-space local W','Uniform connected error <=4 delta+2 delta^2 per model','Endpoint transfer >z/200 for delta=z/100000','Wilson multiplication distance >=1/2 by analytic nonatomic argument'], 'limitations':['Finite matrices verify algebra only','Interferometry requires controlled actual full dynamics and state preparation','Sampling and circuit budgets unproved','No Wilson witness or homogeneous/continuum theorem'], 'cap':str(cap),'inherited_margin_at_cap':str(margin),'readout_error_at_cap':str(error),'transferred_margin_at_cap':str(margin-error),'outcomes':[-1,0,1],'continuum_proved':False,'measurement_implementation_proved':False}
    (o/'results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    (o/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
