#!/usr/bin/env python3
"""AT3 forward exact 4097-sample synthetic checks; does not compute AQ data."""
import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import evaluator as ev

HERE=Path(__file__).resolve().parent
CHECKS=[]
def test(name,condition):
    if name in {x['id'] for x in CHECKS}:raise RuntimeError('duplicate '+name)
    if not condition:raise RuntimeError('failed '+name)
    CHECKS.append({'id':name,'passed':True})
def rejects(name,call):
    try:call()
    except ValueError:test(name,True)
    else:test(name,False)
def put(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,(tuple,list)):return [encode(v) for v in o]
    return o
def outer_decimal(x,places,upper=False):
    Q=10**places;n=ev.ceil_fraction(x*Q) if upper else (x*Q).__floor__()
    return ('-' if n<0 else '')+str(abs(n)//Q)+'.'+str(abs(n)%Q).zfill(places)

def finite_integral(atoms,T):
    lo=hi=F(0)
    for w,x in atoms:
        a,b=ev.exp_negative_interval(T*x)
        lo+=w*(1-b)/x;hi+=w*(1-a)/x
    return lo,hi

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output)
    if not out.is_absolute() or out.exists():raise SystemExit('output must be fresh absolute directory')
    contract=json.loads((HERE/'inputs/research/round30/contracts/at3.json').read_text())
    controls=['wrong-trapezoid-error-sign','omit-infinite-time-tail','replace-deterministic-noise-by-root-N','missing-centering-adds-zero-atom','wrong-energy-time-units','short-cutoff-or-coarse-grid-insufficient','fixture-samples-are-not-AQ-data','uncontrolled-floating-exponential','malformed-sample-count-or-design']
    test('contract-id',contract['id']=='AT3');test('contract-controls',contract['controls']==controls)
    d=contract['frozen_design']
    test('frozen-design',F(d['T'])==ev.DESIGN_T and F(d['h'])==ev.DESIGN_H and d['N']==ev.DESIGN_N and d['sample_count']==ev.DESIGN_N+1 and F(d['epsilon'])==ev.DESIGN_EPS and F(d['target_interval_width'])==F(1,500))
    T=ev.DESIGN_T;h=ev.DESIGN_H;N=ev.DESIGN_N;eps=ev.DESIGN_EPS
    qerr=h*h*ev.FIRST/8;noise=T*eps
    test('exact-quadrature-budget',qerr==F(47,512000))
    test('exact-noise-budget',noise==F(2,15625))
    weights=[h/2]+[h]*(N-1)+[h/2]
    test('all-4097-positive-weights',len(weights)==4097 and min(weights)>0 and sum(weights)==T)
    # Cell kernel k(t)=t(h-t)/2: k(0)=k(h)=0, k'=h/2-t, k''=-1.
    test('peano-kernel-endpoints',F(0)*(h-0)/2==0 and h*(h-h)/2==0)
    test('peano-kernel-max',h/2*(h-h/2)/2==h*h/8)
    test('peano-constant-curvature-integral',h*(0+h*h)/2-h**3/3==h**3/6)
    exp8lo,exp8hi=ev.exp_negative_interval(F(8));tail=ev.MASS/ev.A*exp8hi
    test('tail-exponential-outward-nondegenerate',0<exp8lo<exp8hi<1)
    test('uniform-exact-sample-width',qerr+tail+2*noise<F(170039,100000000)<F(1,500))
    test('exponential-zero-exact',ev.exp_negative_interval(F(0))==(F(1),F(1)))
    for y in (F(1,32),F(5,32),F(1,2),F(8),F(128)):
        lo,hi=ev.exp_negative_interval(y)
        test('exp-positive-enclosure-'+str(y),0<=lo<=hi<=1)
        # Structural sanity: division into two half arguments and positive products
        # yields an independently rounded interval overlapping the direct enclosure.
        halflo,halfhi=ev.exp_negative_interval(y/2)
        test('exp-squaring-consistency-'+str(y),max(lo,halflo*halflo)<=min(hi,halfhi*halfhi))
    atoms={'A':[(F(1,8),F(2)),(F(1,8),F(4))],'B':[(F(1,32),F(1)),(F(3,16),F(3)),(F(1,32),F(5))]}
    exact={'A':F(3,32),'B':F(1,10)}
    data={};results={}
    for name,terms in atoms.items():
        nodes=ev.fixture_nodes(terms);data[name]=nodes
        test('node-count-'+name,len(nodes)==4097)
        test('node-zero-'+name,nodes[0]==(F(1,4),F(1,4)))
        test('all-node-ordered-nonnegative-'+name,all(0<=lo<=hi<=F(1,4) for lo,hi in nodes))
        test('source-moments-'+name,[sum(w*x**k for w,x in terms) for k in range(3)]==[F(1,4),F(3,4),F(5,2)])
        # Direct exp(-j h x), with separate range reduction, checks selected nodes;
        # the report induction certifies all recursively generated nodes.
        for j in (1,17,1024,4096):
            dlo=dhi=F(0)
            for w,x in terms:
                lo,hi=ev.exp_negative_interval(j*h*x);dlo+=w*lo;dhi+=w*hi
            test(f'direct-node-overlap-{name}-{j}',max(dlo,nodes[j][0])<=min(dhi,nodes[j][1]))
        results[name]={}
        for sign in (-1,0,1):
            shifted=[(lo+sign*eps,hi+sign*eps) for lo,hi in nodes]
            result=ev.evaluate(shifted);results[name][str(sign)]=result
            test(f'exact-I-contained-{name}-{sign}',result['lower']<=exact[name]<=result['upper'])
            test(f'target-width-{name}-{sign}',result['width']<F(1701,1000000)<F(1,500))
            test(f'arithmetic-budget-{name}-{sign}',result['arithmetic_trap_width']<F(1,10**24))
            test(f'conditional-provenance-{name}-{sign}',result['conditional_on_sample_contract'] and not result['computed_AQ_samples'])
        base=results[name]['0'];finlo,finhi=finite_integral(terms,T)
        test('finite-trapezoid-excess-positive-'+name,base['trap_lower']>finhi)
        test('finite-trapezoid-excess-bounded-'+name,base['trap_upper']-finlo<=qerr)
        for sign in (-1,1):
            rr=results[name][str(sign)]
            test(f'constant-error-attains-bound-{name}-{sign}',rr['trap_lower']-base['trap_lower']==sign*noise and rr['trap_upper']-base['trap_upper']==sign*noise)
    separation=results['B']['-1']['lower']-results['A']['1']['upper']
    test('worst-Aplus-Bminus-separated',separation>F(4293,1000000)>0)
    test('noise-envelope-not-only-noiseless',results['A']['1']['upper']>results['A']['0']['upper'] and results['B']['-1']['lower']<results['B']['0']['lower'])
    # Wrong-sign lower endpoint loses the exact integral even for central data.
    baseA=results['A']['0']
    test('control-wrong-trapezoid-error-sign',baseA['trap_lower']+qerr-noise>exact['A'])
    # Slow atom is a theorem-hypothesis countercontrol, NOT an AQ realization.
    slowI=F(1,4)/ev.A;slow_first=F(1,4)*ev.A
    slow_trap_upper=slowI*(1-exp8lo)+h*h*slow_first/8
    test('control-omit-infinite-time-tail',slow_trap_upper+noise<slowI)
    rootN_wrong=eps*h*F(64) # N=4096, sqrt(N)=64; even this more generous endpoint simplification fails.
    test('control-replace-deterministic-noise-by-root-N',noise>rootN_wrong and sum(w*eps for w in weights)==noise)
    vacuum_mass=F(1,100)
    test('control-missing-centering-adds-zero-atom',sum(w*vacuum_mass for w in weights)==T*vacuum_mass and vacuum_mass>0)
    # Positive constant correlation has integral T*m, unbounded as T increases;
    # it violates support x>=a. This is not represented as a finite inverse.
    test('zero-atom-tail-cannot-decay',2*T*vacuum_mass>T*vacuum_mass and 0<ev.A)
    alpha=F(3);hbar=F(2)
    test('physical-time-clock',alpha*(hbar*h/alpha)/hbar==h and alpha*(hbar*T/alpha)/hbar==T)
    test('control-wrong-energy-time-units',(hbar/alpha)*exact['A']/hbar==exact['A']/alpha and (hbar/alpha)*exact['A']!=exact['A']/alpha)
    shortlo,shorthi=ev.exp_negative_interval(ev.A*16)
    test('control-short-cutoff-insufficient',ev.MASS/ev.A*shortlo>F(1,500))
    test('control-coarse-grid-insufficient',F(1,2)**2*ev.FIRST/8>F(1,500))
    test('control-fixtures-are-not-AQ-data',contract['model'].startswith('The actual AQ centered spectral measure') and all(not results[k]['0']['computed_AQ_samples'] for k in results))
    rejects('float-sample-rejected',lambda:ev.evaluate([0.0]*4097))
    rejects('nonfinite-sample-rejected',lambda:ev.evaluate(['NaN']*4097))
    rejects('wrong-sample-count-rejected',lambda:ev.evaluate([0]*4096))
    rejects('wrong-step-rejected',lambda:ev.evaluate([0]*4097,h='1/16'))
    rejects('wrong-duration-rejected',lambda:ev.evaluate([0]*4097,T='64'))
    rejects('wrong-count-design-rejected',lambda:ev.evaluate([0]*4097,N=4095))
    rejects('wrong-error-rejected',lambda:ev.evaluate([0]*4097,epsilon='1/1000'))
    rejects('negative-error-rejected',lambda:ev.evaluate([0]*4097,epsilon='-1/1000000'))
    rejects('float-design-rejected',lambda:ev.evaluate([0]*4097,T=128.0))
    rejects('reversed-enclosure-rejected',lambda:ev.evaluate([(1,0)]*4097))
    rejects('three-endpoint-enclosure-rejected',lambda:ev.evaluate([(0,1,2)]*4097))
    # API accepts exact scalar data but labels output conditional rather than
    # validating whether any AQ model could produce these arbitrary numbers.
    scalar=ev.evaluate(['0']*4097)
    test('scalar-api-still-conditional',scalar['conditional_on_sample_contract'] and not scalar['computed_AQ_samples'])
    test('wide-arithmetic-enclosure-fails-width',not ev.evaluate([('0','1')]*4097)['target_width_passed'])
    files=[HERE/'check.py',HERE/'evaluator.py',HERE/'report.md']+sorted(p for p in (HERE/'inputs').rglob('*') if p.is_file())
    manifest={p.relative_to(HERE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    result={'loop':'AT3','direction':'forward','human_author':'Hruday N M (BUNZEEY)','ai_assisted':True,'classification':'conditional actual-AQ theorem; executed abstract synthetic fixtures; established quadrature application; scientific priority unverified','claims':{'conditional_AQ_readout_theorem':True,'all_4097_nodes_executed':True,'fixed_design_width_passed':True,'all_error_vector_fixture_separation':True,'computed_actual_AQ_samples':False,'computed_actual_AQ_inverse_value':False,'static_susceptibility':False,'spectral_pole':False,'optimal_design':False,'continuum_claim':False,'fourth_investigation':False},'design':d,'budgets':{'quadrature':qerr,'sample_error':noise,'tail_upper':tail,'exp_minus_8':[exp8lo,exp8hi],'exact_sample_width_upper':qerr+tail+2*noise},'fixture_outputs':results,'fixture_exact_I':exact,'worst_separation_lower':separation,'display_outward_9dp':{name:{sign:[outer_decimal(r['lower'],9),outer_decimal(r['upper'],9,True)] for sign,r in signs.items()} for name,signs in results.items()},'controls':{c:True for c in controls},'checks':CHECKS,'fixture_scope':'Only AT2 A/B executed as benchmark spectra. Slow atom and zero atom are logical countercontrols. None is actual AQ data.'}
    out.mkdir(parents=True)
    put(out/'results.json',encode(result));put(out/'source-manifest.json',manifest)
    for name,nodes in data.items():
        with (out/f'synthetic-{name}-4097-enclosures.csv').open('w',newline='') as f:
            writer=csv.writer(f);writer.writerow(['index','lower','upper'])
            writer.writerows((j,str(lo),str(hi)) for j,(lo,hi) in enumerate(nodes))
    print(json.dumps({'loop':'AT3','checks':len(CHECKS),'all_passed':True,'output':str(out)}))
if __name__=='__main__':main()
