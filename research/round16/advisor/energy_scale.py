"""Exact scale audit for finite physical SU(2) graph Hamiltonians."""
from fractions import Fraction as Q
from pathlib import Path
import argparse, csv, hashlib, json


def rational(value):
    if type(value) not in (int, str, Q):
        raise ValueError('exact integer, fraction string or Fraction required')
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('finite exact rational required') from exc


def physical_lower(alpha, dimensionless_lower):
    alpha, lower = rational(alpha), rational(dimensionless_lower)
    if alpha <= 0:
        raise ValueError('positive energy normalization required')
    return alpha * lower


def box_row(n, alpha, ratio):
    if type(n) is not int or not 2 <= n <= 10000:
        raise ValueError('vertex extent must be an integer2..10000')
    alpha, ratio = rational(alpha), rational(ratio)
    if alpha <= 0:
        raise ValueError('positive energy normalization required')
    # Open cubic vertex box. Simple graph, Gauss at ALL vertices, no charges.
    faces = 3*n*(n-1)**2
    lower = alpha*(3-faces*abs(ratio))
    return {'n':n, 'plaquettes':faces, 'alpha':str(alpha),
            'lambda_over_alpha':str(ratio), 'free_gap':str(3*alpha),
            'global_norm_lower':str(lower),
            'bound_status':'positive' if lower > 0 else 'insufficient'}


def execute(output):
    output=Path(output); output.mkdir(parents=True, exist_ok=False)
    checks=[]
    def check(name, condition):
        if not condition: raise RuntimeError(name)
        checks.append({'name':name, 'passed':True})
    def rejects(name, fn):
        try: fn()
        except ValueError: check(name, True); return
        raise RuntimeError('accepted invalid input: '+name)
    check('fixed positive scale multiplies a dimensionless bound exactly',physical_lower('2/3','7/5')==Q(14,15))
    check('zero bound stays insufficient',physical_lower(1,0)==0)
    check('negative sufficient bound retained, never clipped',physical_lower(2,-1)==-2)
    for bad in [True,0,-1,'nan','1/0',0.5]:
        rejects('bad alpha '+repr(bad),lambda b=bad:physical_lower(b,1))
    for bad in [True,1,0,-1,10001,2.0]:
        rejects('bad extent '+repr(bad),lambda b=bad:box_row(b,1,0))
    rows=[]
    for n in (2,3,4,8,16,32,64):
        fixed=box_row(n,1,0); shrinking=box_row(n,Q(1,n),0)
        coupled=box_row(n,1,Q(1,100))
        check('fixed-scale free gap n='+str(n),Q(fixed['free_gap'])==3)
        check('shrinking-scale counterexample n='+str(n),Q(shrinking['free_gap'])==Q(3,n))
        check('scaling covariance n='+str(n),box_row(n,7,Q(1,100))['global_norm_lower']==str(7*Q(coupled['global_norm_lower'])))
        rows.append({'n':n,'plaquettes':fixed['plaquettes'],'alpha_fixed':'1','alpha_shrinking':str(Q(1,n)),
                     'fixed_free_gap':'3','shrinking_free_gap':str(Q(3,n)),
                     'ratio':'1/100','global_norm_lower':coupled['global_norm_lower'],
                     'bound_status':coupled['bound_status']})
    check('global norm estimate fails at64 despite fixed free gap',rows[-1]['bound_status']=='insufficient')
    with (output/'energy_scale.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    result={'schema':'ym16-scale-audit-v1','status':'passed','checks_count':len(checks),'checks':checks,'rows':rows,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'theorem':'H_N=alpha_N K_N implies Delta(H_N)=alpha_N Delta(K_N), alpha_N>0, for the same spectral domain.',
      'counterexample':'At lambda=0 on open cubic boxes n>=2, Delta(K_n)=3; alpha_n=1/n gives Delta(H_n)=3/n ->0.',
      'conditional_uniform_bridge':'If inf_N alpha_N>=alpha_min>0 AND inf_N Delta(K_N)>=d>0, then inf_N Delta(H_N)>=alpha_min*d.',
      'limits':'No interacting dimensionless uniform d is proved here. alpha_min is necessary for this inference, not a universal necessary condition for arbitrary scaled spectra.'}
    (output/'review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();execute(a.output)
