#!/usr/bin/env python3
"""Exact reverse I2 geometry, vacuum moments and rigorously enclosed 2x2 dressing."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse, hashlib, itertools, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def need(ok, message):
    if not ok: raise RuntimeError(message)

def shift(a,d):
    b=list(a);b[d]+=1;return tuple(b)

def edges(a,i,j):
    return {(a,i),(shift(a,j),i),(a,j),(shift(a,i),j)}

def is_free(e):
    a,d=e
    return d==2 or (d==1 and a[1]%2==1) or (d==0 and a[0]%4==3)

def inter(x):
    return (F(x),F(x))

def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def minus(a):return (-a[1],-a[0])
def mul(a,b):
    vals=[x*y for x in a for y in b]
    return (min(vals),max(vals))
def maximum_abs(a):return max(abs(a[0]),abs(a[1]))
def abs_lower(a):return F(0) if a[0]<=0<=a[1] else min(abs(a[0]),abs(a[1]))

def trig(t,sine):
    # Alternating Taylor theorem, |t|<=1/2: consecutive partial sums enclose exactly.
    need(F(0)<=t<=F(1,2),'trig fixture domain')
    def term(k):
        degree=2*k+int(sine)
        return (-1)**k*t**degree/F(factorial(degree))
    a=sum((term(k) for k in range(10)),F(0));b=a+term(10)
    return min(a,b),max(a,b)

def matrix_mul(a,b):
    return [[plus(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]

def trans(a):return [list(c) for c in zip(*a)]

def compact(a):
    scale=10**18
    lo=(a[0].numerator*scale)//a[0].denominator
    hi=-((-a[1].numerator*scale)//a[1].denominator)
    return [str(F(lo,scale)),str(F(hi,scale))]

def fixture(t):
    s,c=trig(t,True),trig(t,False)
    unitary=[[c,minus(s)],[s,c]]
    h=[[inter(0),inter(t)],[inter(t),inter(1+t/2)]]
    transformed=matrix_mul(matrix_mul(unitary,h),trans(unitary))
    remainder=[[plus(transformed[i][j],inter(-(1+t/2) if i==j==1 else 0)) for j in range(2)] for i in range(2)]
    # ||phi||<=3t/2 from row sums; ||v||=||u||=t, so lemma gives ||R||<=4t².
    frobenius_squared_upper=sum((maximum_abs(a)**2 for row in remainder for a in row),F(0))
    need(frobenius_squared_upper <= (4*t*t)**2,'rigorous fixture remainder bound')
    need(remainder[0][0][1]<0,'omitted remainder must change vacuum energy')
    wrong=trans(unitary)
    wrong_t=matrix_mul(matrix_mul(wrong,h),trans(wrong))
    need(abs_lower(wrong_t[0][1])>t,'wrong sign failed to retain first-order mixing')
    ratios=[]
    for amplitude in [F(1,2),F(1,8),F(1,32),F(1,128)]:
        ratio=2/amplitude+t/2
        ratios.append({'amplitude':str(amplitude),'form_ratio':str(ratio)})
    need(all(F(b['form_ratio'])>F(a['form_ratio']) for a,b in zip(ratios,ratios[1:])),'relative-bound falsifier')
    return {'tau':str(t),'H0':[['0','0'],['0','1']],
      'phi':[['0',str(t)],[str(t),str(t/2)]],
      'generator_S':[['0',str(-t)],[str(t),'0']],
      'remainder_entry_enclosures':[[compact(a) for a in row] for row in remainder],
      'remainder_norm_bound':str(4*t*t),
      'frobenius_squared_upper_enclosure':compact(inter(frobenius_squared_upper)),
      'wrong_sign_offdiagonal_enclosure':compact(wrong_t[0][1]),
      'pure_relative_ratios':ratios}

def run():
    omitted=[]
    for a in itertools.product(range(4),range(2),range(1)):
        for i,j in itertools.combinations(range(3),2):
            if (i,j)==(0,1) and a[1]%2==0 and a[0]%4<3:continue
            ee=edges(a,i,j);free={e for e in ee if is_free(e)}
            need(len(free)>=2,'omitted plaquette lacks two independent free Haar factors')
            omitted.append({'anchor':a,'plane':(i,j),'edges':ee,'free':free})
    need(len(omitted)==21,'inherited anchor count')
    pair_count=0
    for a,b in itertools.combinations(omitted,2):
        need(len(a['edges']&b['edges'])<=1,'distinct faces share multiple links')
        need(a['free']-b['edges'],'missing unmatched independent free link')
        pair_count+=1
    # Haar S^3 invariance: all four coordinate squares agree and sum to one.
    haar_second=F(1,4)
    coefficient=sum((F(1,3)**2*haar_second for _ in omitted),F(0))
    need(coefficient==F(7,12),'variance coefficient')
    sqrt_upper=F(4,5)
    need(sqrt_upper**2>coefficient,'invalid rational square-root upper bound')
    remainder_coefficient=coefficient+14*sqrt_upper
    need(remainder_coefficient==F(707,60),'rational remainder coefficient')
    # Exact symbolic commutator identity on the canonical two-dimensional fixture.
    t=F(1,7);S=[[F(0),-t],[t,F(0)]];H=[[F(0),F(0)],[F(0),F(1)]]
    def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(2)),F(0)) for j in range(2)] for i in range(2)]
    SH,HS=mm(S,H),mm(H,S)
    comm=[[SH[i][j]-HS[i][j] for j in range(2)] for i in range(2)]
    need(comm==[[F(0),-t],[-t,F(0)]],'cancellation sign')
    fixtures=[fixture(t) for t in [F(1,100),F(1,10),F(1,2)]]
    return {
      'schema':'ym21-reverse-i2-v1','loop':'i2','direction':'reverse','passed':True,
      'target_verdict':'local_dressing_lemma_verified_global_numeric_interval_insufficient',
      'comparison':{'variance_coefficient':str(coefficient),'generator_norm_square_bound':str(coefficient),
        'rational_remainder_coefficient':str(remainder_coefficient),'pure_relative_bound_possible':False,
        'numerical_global_interval_certified':False},
      'exact_geometry':{'omitted_faces':len(omitted),'independent_pair_cancellations':pair_count,
        'haar_second_moment':str(haar_second),
        'free_witnesses':[{'anchor':list(r['anchor']),'plane':list(r['plane']),
          'free_links':[[list(a),d] for a,d in sorted(r['free'])]} for r in omitted]},
      'local_lemma':{'space':'one four-coarse-site star, full L2 Haar link space',
        'H0_gap':'1','v':'phi Omega','u':'(H0|Q)^(-1) v',
        'S':'|u><Omega|-|Omega><u|','conjugation':'exp(S)(H0+phi)exp(-S)',
        'result':'H0+Q phi Q+R','exact_remainder_coefficient':'7/12+14 sqrt(7/12)',
        'rational_root_upper':str(sqrt_upper),'physical_remainder_bound':'delta*(707/60)*tau^2, delta=alpha/8',
        'domain':'D(H0) preserved because range(S) lies in span{Omega,u} subset D(H0)',
        'method':'finite-rank local unitary coordinate change; no action deformation'},
      'fixtures':fixtures,
      'controls':{'wrong_sign_rejected':True,'dropped_remainder_rejected':True,
        'bare_pure_relative_bound_rejected':True,'independent_plaquette_assumption_used':False,
        'numerical_global_constant_inference_rejected':True},
      'open_obligations':['Explicit convergent many-star weighted interaction expansion',
        'Uniform bounds for overlapping commutators and induced supports',
        'Numerical c1(S),c2(S) or valid replacement stability constants',
        'Physical continuum scaling and mass matching']}

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    inputs=[HERE/'check.py',HERE/'report.md',HERE/'source-review.json',
       ROOT/'research/round21/contracts/i2.json',ROOT/'research/round21/advisor/i1-gate.json',
       ROOT/'research/round21/reverse/i1/report.md',ROOT/'research/round21/reverse/i1/source-dictionary.json',
       ROOT/'research/round20/reverse/h2/report.md']
    need(all(p.is_file() for p in inputs),'source input absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    contract=json.loads((ROOT/'research/round21/contracts/i2.json').read_text())
    need(contract['loop']=='i2' and contract['status']=='frozen','contract not frozen I2')
    need(digest(ROOT/contract['depends_on']['gate'])==contract['depends_on']['sha256'],'I1 dependency mismatch')
    result=run()
    need(before=={str(p.relative_to(ROOT)):digest(p) for p in inputs},'source changed during execution')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
       'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))

if __name__=='__main__':main()
