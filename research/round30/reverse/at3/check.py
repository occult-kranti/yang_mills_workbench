#!/usr/bin/env python3
"""AT3 exact interval readout API and abstract benchmark checks, standard library.

CSV schema: index,s,value_lower,value_upper; all numbers exact decimal or rational.
value_lower/value_upper enclose the observed sample, whose additional deterministic
absolute error relative to the actual centered correlation must be <= epsilon.
The evaluator does not itself certify the provenance of observations.
"""
import argparse
import csv
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
T=F(128);H=F(1,32);N=4096;EPS=F(1,1000000);TARGET=F(1,500)
A=F(1,16);S_UP=F(63,250);U_UP=F(94,125)
D=10**30
MAX_SAMPLE_ARITH_WIDTH=F(1,10**12)
checks=[]

def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    return x

def write(p,x):p.write_text(json.dumps(clean(x),indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,ok,**evidence):
    if any(c['id']==name for c in checks):raise ValueError('duplicate '+name)
    if not ok:raise ValueError('failed '+name+': '+repr(evidence))
    checks.append({'id':name,'passed':True,'evidence':evidence})
def expect_error(name,fn):
    try:fn()
    except (ValueError,TypeError,ZeroDivisionError) as err:
        check(name,True,rejected_reason=str(err));return
    raise ValueError('expected rejection '+name)

def exact(x):
    if isinstance(x,F):return x
    if isinstance(x,int) and not isinstance(x,bool):return F(x)
    if isinstance(x,str) and re.fullmatch(r'[+-]?\d+(?:/\d+|\.\d+)?',x):return F(x)
    raise TypeError('only exact integer, Fraction, decimal or rational string is allowed')

def floor_scaled(x):return x.numerator*D//x.denominator
def ceil_scaled(x):return -((-x.numerator*D)//x.denominator)

def imul(p,q):
    if min(p+q)<0:raise ValueError('positive interval multiplication only')
    return (p[0]*q[0]//D,(p[1]*q[1]+D-1)//D)

@lru_cache(None)
def exp_small(q):
    """For 0<=q<=1/2, S_33 <= exp(-q) <= S_32, then round outward."""
    q=exact(q)
    if not 0<=q<=F(1,2):raise ValueError('small exponential argument outside proved range')
    term=F(1);partial=F(1)
    for k in range(1,33):
        term*=(-q)/k;partial+=term
    upper=partial
    lower=partial+term*(-q)/33
    return (floor_scaled(lower),ceil_scaled(upper))

def exp_negative(q):
    """Scale q by a power of two to <=1/2 and square positive intervals."""
    q=exact(q)
    if q<0:raise ValueError('negative decay argument')
    squarings=0
    while q>F(1,2):q/=2;squarings+=1
    interval=exp_small(q)
    for _ in range(squarings):interval=imul(interval,interval)
    return (F(interval[0],D),F(interval[1],D))

def atom_nodes(energy,count=N,step=H):
    """All count+1 nodes, no replacement by unproved finite-sum shortcut."""
    r=exp_small(exact(energy)*exact(step));p=(D,D);out=[]
    for j in range(count+1):
        out.append((F(p[0],D),F(p[1],D)))
        if j<count:p=imul(p,r)
    return out

def fixture_nodes(atoms):
    out=[(F(0),F(0)) for _ in range(N+1)]
    for energy,weight in atoms:
        for j,(lo,hi) in enumerate(atom_nodes(energy)):
            out[j]=(out[j][0]+weight*lo,out[j][1]+weight*hi)
    return out

def trap(samples,step=H):
    step=exact(step)
    return tuple(step*(sum((p[k] for p in samples[1:-1]),F(0))+(samples[0][k]+samples[-1][k])/2) for k in (0,1))

def evaluate(samples,*,T_value=T,h_value=H,N_value=N,epsilon=EPS):
    """Return a conditional I interval for the frozen design and exact sample bins.

    Each pair encloses an observed d_j; |d_j-C(jh)|<=epsilon is a caller's
    certified scientific premise, not inferred by this function. Widths represent
    arithmetic uncertainty separately. Bounds have dimensionless I=alpha R units.
    """
    if isinstance(N_value,bool) or not isinstance(N_value,int):raise TypeError('N must be integer')
    tv=exact(T_value);hv=exact(h_value);ep=exact(epsilon)
    if (tv,hv,N_value,ep)!=(T,H,N,EPS):raise ValueError('design/error differs from frozen AT3 contract')
    if not isinstance(samples,(list,tuple)) or len(samples)!=N+1:raise ValueError('exactly 4097 samples required')
    parsed=[]
    for j,p in enumerate(samples):
        if not isinstance(p,(list,tuple)) or len(p)!=2:raise ValueError('sample must be lower/upper pair')
        lo,hi=exact(p[0]),exact(p[1])
        if lo>hi:raise ValueError('inverted sample interval')
        if hi-lo>MAX_SAMPLE_ARITH_WIDTH:raise ValueError('sample arithmetic width exceeds 1e-12')
        if hi < -EPS or lo>S_UP+EPS:raise ValueError('sample incompatible with mass/error envelope')
        parsed.append((lo,hi))
    qlo,qhi=trap(parsed,hv)
    tail=S_UP/A*exp_negative(A*tv)[1]
    quadrature=hv*hv*U_UP/8;noise=tv*ep
    interval=(qlo-quadrature-noise,qhi+tail+noise)
    return {'interval_I':interval,'width':interval[1]-interval[0],'meets_target':interval[1]-interval[0]<TARGET,'trap_interval':(qlo,qhi),'budget':{'quadrature_one_sided':quadrature,'tail_one_sided':tail,'sample_error_each_side':noise,'arithmetic_trap_width':qhi-qlo},'conditional_on_certified_centered_data':True,'actual_aq_samples_computed':False,'units':'I dimensionless; divide endpoints by alpha for R'}

def csv_text(samples):
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['index','s','value_lower','value_upper'])
    for j,(lo,hi) in enumerate(samples):writer.writerow([j,str(j*H),str(lo),str(hi)])
    return stream.getvalue()

def read_csv_text(text):
    reader=csv.reader(io.StringIO(text));rows=list(reader)
    if not rows or rows[0]!=['index','s','value_lower','value_upper']:raise ValueError('invalid CSV header')
    if len(rows)!=N+2:raise ValueError('CSV must contain 4097 data rows')
    samples=[]
    for j,row in enumerate(rows[1:]):
        if len(row)!=4 or row[0]!=str(j) or exact(row[1])!=j*H:raise ValueError('CSV index/time grid mismatch')
        samples.append((exact(row[2]),exact(row[3])))
    return samples

def evaluate_csv(path):
    return evaluate(read_csv_text(Path(path).read_text()))

def shifted(samples,delta):return [(lo+delta,hi+delta) for lo,hi in samples]
def fmt(x):return str(x)

def science(out):
    check('frozen-node-design',N*H==T and N+1==4097 and EPS==F(1,1000000))
    weights=[H/2]+[H]*(N-1)+[H/2]
    check('positive-weights-sum-to-T',min(weights)>0 and sum(weights)==T,sum_weights=sum(weights),node_count=len(weights))
    # Analytic kernel coefficient: k(r)=r(h-r)/2, max h^2/8.
    kernel=lambda r:r*(H-r)/2
    check('peano-kernel-sign-and-maximum',kernel(0)==0 and kernel(H)==0 and kernel(H/2)==H*H/8,max_kernel=kernel(H/2))
    tail=exp_negative(8);quad=H*H*U_UP/8;noise=T*EPS
    budget=quad+S_UP/A*tail[1]+2*noise+T*MAX_SAMPLE_ARITH_WIDTH
    check('uniform-full-budget-below-target',budget<TARGET,quadrature=quad,tail_upper=S_UP/A*tail[1],noise_each_side=noise,api_arithmetic_allowance=T*MAX_SAMPLE_ARITH_WIDTH,total=budget,target=TARGET)
    check('exp-zero-exact',exp_negative(0)==(F(1),F(1)))
    lo8,hi8=tail
    check('exp-tail-narrow-enclosure',F(0)<lo8<hi8<F(1) and hi8-lo8<F(1,10**26),lower=lo8,upper=hi8)
    # Check stable interval construction under an independent rational series identity.
    for q in (F(1,32),F(1,8),F(5,32)):
        lo,hi=exp_small(q)
        term=F(1);s=F(1)
        for k in range(1,41):term*=(-q)/k;s+=term
        low41=s+term*(-q)/41
        check('exp-encloses-longer-alternating-series-'+str(q),F(lo,D)<=low41<=s<=F(hi,D),outer=[F(lo,D),F(hi,D)],inner=[low41,s])
    atoms={'A':[(F(2),F(1,8)),(F(4),F(1,8))],'B':[(F(1),F(1,32)),(F(3),F(3,16)),(F(5),F(1,32))]}
    truths={'A':F(3,32),'B':F(1,10)}
    rows={};reports={}
    for name,aa in atoms.items():
        samples=fixture_nodes(aa);rows[name]=samples
        (out/('fixture-'+name+'.csv')).write_text(csv_text(samples))
        exactI=sum(w/x for x,w in aa)
        check('fixture-exact-inverse-'+name,exactI==truths[name],I=exactI)
        check('fixture-all-nodes-'+name,len(samples)==4097 and samples[0]==(F(1,4),F(1,4)),count=len(samples),last=samples[-1])
        cases={}
        for tag,delta in [('zero',F(0)),('plus',EPS),('minus',-EPS)]:
            case=evaluate(shifted(samples,delta));cases[tag]=case
            lo,hi=case['interval_I']
            check('fixture-coverage-'+name+'-'+tag,lo<=exactI<=hi and case['meets_target'],interval=[lo,hi],truth=exactI,width=case['width'])
            observed=case['trap_interval'];base=trap(samples)
            check('noise-shift-exact-'+name+'-'+tag,observed[0]-base[0]==T*delta and observed[1]-base[1]==T*delta,shift=observed[0]-base[0])
        reports[name]=cases
        roundtrip=read_csv_text((out/('fixture-'+name+'.csv')).read_text())
        check('csv-roundtrip-'+name,roundtrip==samples and evaluate_csv(out/('fixture-'+name+'.csv'))==cases['zero'])
        write(out/('fixture-'+name+'-evaluations.json'),cases)
    # Independently choose all-positive A and all-negative B observed errors;
    # their returned intervals already include another +/-T epsilon allowance.
    Aupper=reports['A']['plus']['interval_I'][1];Blower=reports['B']['minus']['interval_I'][0]
    check('uniform-Aplus-Bminus-interval-separation',Aupper<Blower,A_worst_upper=Aupper,B_worst_lower=Blower,gap=Blower-Aupper,independent_error_vectors=True)
    Alo,Ahi=trap(rows['A']);Blo,Bhi=trap(rows['B'])
    check('separation-counts-both-noise-layers',Aupper==Ahi+S_UP/A*tail[1]+2*T*EPS and Blower==Blo-quad-2*T*EPS)
    # Correct excess sign: fast-decay A has negligible tail and Trap>I exactly.
    check('wrong-trapezoid-error-sign',Alo>truths['A'],invalid_lower=Alo,truth=truths['A'])
    # Equal moment-compatible tail fixture: total mass1/4, first moment3/4.
    tailatoms=[(F(1,16),F(1,10)),(F(119,24),F(3,20))]
    tailsamples=fixture_nodes(tailatoms);tailtruth=sum(w/x for x,w in tailatoms);tailtrap=trap(tailsamples)
    check('omit-infinite-time-tail',tailtrap[1]+noise<tailtruth and sum(w*x for x,w in tailatoms)==F(3,4),invalid_no_tail_upper=tailtrap[1]+noise,true_inverse=tailtruth)
    wrong_noise=T*EPS/64
    check('replace-deterministic-noise-by-root-N',noise>wrong_noise and sum(w*EPS for w in weights)==noise,actual_worst=noise,wrong_rootN=wrong_noise)
    # A zero atom contributes a constant; its time integral diverges.
    zero_mass=F(1,1000)
    check('missing-centering-adds-zero-atom',zero_mass>S_UP*hi8 and 2*T*zero_mass>T*zero_mass,constant_tail=zero_mass,gapped_envelope_at_T=S_UP*hi8,integral_prefix_T=T*zero_mass,integral_prefix_2T=2*T*zero_mass)
    alpha=F(4);hbar=F(3);tE=T*hbar/alpha
    check('wrong-energy-time-units',alpha*tE/hbar==T and alpha*tE!=T and truths['A']/alpha!=truths['A'],physical_tE=tE,dimensionless_s=T,physical_R=truths['A']/alpha)
    short_tail=S_UP/A*exp_negative(A*16)[0];coarse_quad=F(1,4)**2*U_UP/8
    check('short-cutoff-or-coarse-grid-insufficient',short_tail>TARGET and coarse_quad>TARGET,short_T16_tail_lower=short_tail,coarse_h_quadrature=coarse_quad,verdict='these uniform certificates exceed width target; no claim of actual algorithm divergence')
    check('fixture-samples-are-not-AQ-data',sum(w*x*x for x,w in atoms['A'])==F(5,2)<36,source='explicit abstract AT2 atomic measures',second_moment=F(5,2),actual_aq_sample_count=0)
    # Binary float is deliberately disallowed from the certificate API.
    expect_error('uncontrolled-floating-exponential',lambda:exact(0.36787944117144233))
    expect_error('malformed-sample-count',lambda:evaluate(rows['A'][:-1]))
    expect_error('malformed-grid-design',lambda:evaluate(rows['A'],h_value=F(1,16)))
    expect_error('malformed-error-negative',lambda:evaluate(rows['A'],epsilon=F(-1,1000000)))
    expect_error('malformed-error-too-large',lambda:evaluate(rows['A'],epsilon=F(1,1000)))
    expect_error('malformed-integer-design',lambda:evaluate(rows['A'],N_value=True))
    expect_error('malformed-inverted-interval',lambda:evaluate([(F(1),F(0))]+rows['A'][1:]))
    expect_error('malformed-arithmetic-width',lambda:evaluate([(F(0),F(1,1000))]+rows['A'][1:]))
    expect_error('malformed-nonfinite',lambda:exact('NaN'))
    expect_error('malformed-csv-header',lambda:read_csv_text('index,s,value\n'))
    validtext=csv_text(rows['A'])
    expect_error('malformed-csv-time',lambda:read_csv_text(validtext.replace('1,1/32,','1,1/16,',1)))
    expect_error('malformed-csv-rational',lambda:read_csv_text(validtext.replace('0,0,1/4,1/4','0,0,1/0,1/4',1)))
    return {'loop':'AT3','direction':'reverse','checks':checks,'check_count':len(checks),'design':{'T':T,'h':H,'N':N,'sample_count':N+1,'epsilon':EPS,'target_width':TARGET,'decimal_denominator':D,'maximum_api_sample_arithmetic_width':MAX_SAMPLE_ARITH_WIDTH},'uniform_width_upper':budget,'tail_exp_interval':tail,'fixture_certificates':reports,'uniform_separation_margin':Blower-Aupper,'claims':{'actual_aq_state_conditional_theorem':True,'actual_aq_samples_computed':False,'actual_aq_response_computed':False,'fixtures_are_actual_aq_spectra':False,'continuum_claim':False,'static_susceptibility_claim':False,'optimal_design_claim':False,'new_quadrature_claim':False,'fourth_investigation_started':False}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--csv');args=ap.parse_args();out=Path(args.output)
    if not out.is_absolute() or out.exists() or any(p.is_symlink() for p in [out]+list(out.parents)):raise ValueError('output requires fresh absolute nonsymlink path')
    inv=json.loads((HERE/'inputs/source-inventory.json').read_text())
    filelist={str(p.relative_to(HERE/'inputs')) for p in (HERE/'inputs').rglob('*') if p.is_file()}
    if filelist!=set(inv)|{'source-inventory.json'}:raise ValueError('input inventory mismatch')
    for rel,h in inv.items():
        p=HERE/'inputs'/rel
        if p.is_symlink() or any(q.is_symlink() for q in p.parents) or sha(p)!=h:raise ValueError('source mismatch '+rel)
    contract=json.loads((HERE/'inputs/research/round30/contracts/at3.json').read_text())
    f=contract['frozen_design']
    if contract['id']!='AT3' or (f['T'],f['h'],f['N'],f['epsilon'])!=(128,'1/32',4096,'1/1000000'):raise ValueError('contract mismatch')
    out.mkdir(parents=True)
    data=evaluate_csv(args.csv) if args.csv else science(out)
    write(out/'results.json',data)
    sources={str(p.relative_to(HERE)):sha(p) for p in sorted((HERE/'inputs').rglob('*')) if p.is_file()}
    sources.update({'check.py':sha(HERE/'check.py'),'report.md':sha(HERE/'report.md')})
    if args.csv:sources['external_csv_sha256']=sha(Path(args.csv))
    write(out/'manifest.json',{'loop':'AT3','direction':'reverse','sources':sources,'outputs':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}})
    print(json.dumps({'loop':'AT3','checks':len(checks),'results_sha256':sha(out/'results.json')}))

if __name__=='__main__':main()
