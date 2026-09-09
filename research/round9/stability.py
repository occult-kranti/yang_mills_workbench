#!/usr/bin/env python3
"""Exact diagonal transfer fixtures for a conditional lemma, not Yang--Mills."""
from pathlib import Path
import csv
import json
import math
import numpy as np

HERE=Path(__file__).resolve().parent

def lower_gap(a, mass, epsilon):
    values=(a,mass,epsilon)
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in values):
        raise ValueError('finite real scalar parameters required')
    if a<=0 or mass<=0 or epsilon<0:
        raise ValueError('a,mass positive; epsilon nonnegative')
    # expm1 preserves the distance from one for small a.
    shift=math.expm1(-mass*a)+epsilon
    if not -1<shift<0:
        raise ValueError('positive strict contraction margin not certified')
    result=-math.log1p(shift)/a
    if not math.isfinite(result) or result<=0:
        raise ValueError('nonfinite or lost gap margin')
    return result

def run():
    checks=[]; rows=[]
    def check(name, ok):
        if not bool(ok): raise AssertionError(name)
        checks.append({'name':name,'passed':True})
    for a in (0.25,0.125,0.0625,0.03125,0.015625,0.0078125,0.00390625):
        for power in (1,2):
            eps=0.2*a**power; q=math.exp(-a); s=q+eps
            T=np.diag([1.,q]); S=np.diag([1.,s]); n=round(1/a)
            bound=lower_gap(a,1.,eps)
            difference=float(np.linalg.norm(S-T,2))
            semigroup=float(np.linalg.norm(np.linalg.matrix_power(S,n)-np.linalg.matrix_power(T,n),2))
            check(f'shared vacuum and positive contractions {a} {power}',np.array_equal(T[:,0],S[:,0]) and 0<q<=s<1)
            check(f'operator difference {a} {power}',abs(difference-eps)<3e-16)
            check(f'gap saturation {a} {power}',abs(bound+math.log(s)/a)<3e-14)
            check(f'telescoping {a} {power}',semigroup<=n*eps+1e-15)
            rows.append(dict(a=a,power=power,epsilon=eps,gap_lower_bound=bound,actual_semigroup_error=semigroup,telescoping_bound=n*eps))
    for a in (1e-3,1e-6,1e-10):
        check('o(a) restores reference gap '+str(a),abs(lower_gap(a,1,.2*a*a)-1)<.201*a)
        check('O(a) allows persistent gap shift '+str(a),abs(lower_gap(a,1,.2*a)-.8)<.201*a)
    for args in ((0,1,0),(1,0,0),(1,1,-1),(1,1,1),(float('nan'),1,0),(1,float('inf'),0),(True,1,0),(1,1,'bad')):
        try:lower_gap(*args)
        except ValueError: checks.append({'name':'invalid or unproven margin rejected '+repr(args),'passed':True})
        else:raise AssertionError(args)
    # epsilon->0 is insufficient: sqrt(a) dominates the O(a) distance to one.
    for a in (1e-2,1e-4,1e-6):
        try:lower_gap(a,1,math.sqrt(a))
        except ValueError:checks.append({'name':'vanishing error without scale control rejected '+str(a),'passed':True})
        else:raise AssertionError('bad scale accepted')
    with (HERE/'stability.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    report={'status':'passed','count':len(checks),'checks':checks,'scope':'Exact two-state diagonal fixtures for the shared-vacuum conditional transfer bound. No interacting Yang--Mills estimate.'}
    (HERE/'stability-validation.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks)}))

if __name__=='__main__':run()
