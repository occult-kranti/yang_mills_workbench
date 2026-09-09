#!/usr/bin/env python3
"""Independent exact action/certificate audit, with mutations in a private copy."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse,ast,copy,hashlib,importlib.util,json,shutil,sys

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def independent_pi():
    # atan(1/2)+atan(1/3)=pi/4, using a different Machin-type identity.
    def bounds(q,N=90):
        x=F(1,q);s=sum(((-1)**j*x**(2*j+1)/(2*j+1) for j in range(N)),F(0));term=x**(2*N+1)/(2*N+1)
        return s,s+term
    a,b=bounds(2);c,d=bounds(3);return 4*(a+c),4*(b+d)
def independent_cosine_action(T,s1,s2,t):
    amp=abs(s1)+abs(s2)
    if t==0 or amp==0:return F(0),F(0)
    if t==T:return amp*T,amp*T
    pl,ph=independent_pi();s=t/T;lo=hi=F(0)
    # Forty even-ending terms of the integrated cosine Taylor series are lower;
    # adding the next positive term gives an upper endpoint.
    for k in range(1,41):
        lower=pl**(2*k)*s**(2*k+1)/factorial(2*k+1);upper=ph**(2*k)*s**(2*k+1)/factorial(2*k+1)
        if k%2:lo+=lower;hi+=upper
        else:lo-=upper;hi-=lower
    hi+=ph**82*s**83/factorial(83)
    return amp*T*lo,amp*T*hi

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--label',default='drive_audit');args=ap.parse_args();src=args.source.resolve()
    before=digest(src);m=load(src,'reviewed_drive_bound');records=[];defects=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        records.append({'test':name,'passed':True,'detail':detail})
    def rejects(fn,name):
        try:fn()
        except (ValueError,TypeError,RuntimeError,KeyError,AttributeError) as e:records.append({'test':name,'passed':True,'rejection':str(e)});return
        raise RuntimeError('Unexpected acceptance: '+name)
    pl,ph=m.pi_interval();ql,qh=independent_pi();check(pl<ql<qh<ph,'independent_pi_identity_enclosure')
    certificates=[]
    for T in (F(1,3),F(2),F(7)):
        for s1,s2 in [(F(1),F(3,2)),(F(-2),F(1,3)),(F(0),F(0))]:
            protocol={'kind':'cosine_ramp','duration':str(T),'lambda1_scale':str(s1),'lambda2_scale':str(s2)}
            for fraction in (F(0),F(1,1000000),F(1,10),F(1,2),F(9,10),F(999999,1000000),F(1)):
                t=T*fraction;lo,hi=m.action_interval(protocol,t);il,ih=independent_cosine_action(T,s1,s2,t)
                check(lo<=il<=ih<=hi,f'cosine_action.{T}.{s1}.{s2}.{fraction}')
            c=m.certificate(protocol,4,time=T/2);check(m.verify_certificate(c),'cosine_certificate.'+str(len(certificates)));certificates.append(c)
    piece={'kind':'piecewise_constant','segments':[{'duration':'1/3','lambda1':'2','lambda2':'-3'},{'duration':'2/3','lambda1':'-1','lambda2':'1/2'}]}
    for t,A in [(F(0),F(0)),(F(1,6),F(5,6)),(F(1,3),F(5,3)),(F(1,2),F(23,12)),(F(1),F(8,3))]:
        check(m.action_interval(piece,t)==(A,A),'piecewise_absolute_action.'+str(t))
    for A in (F(0),F(1,100),F(1,2),F(3),F(100)):
        for D in range(6):
            for d0 in range(D+1):
                expected=min(F(2),A**(D-d0+1)/factorial(D-d0+1))
                check(m.factorial_bound(A,D,d0)==expected,f'factorial.{A}.{D}.{d0}')
    c=certificates[1]
    mutations={
      'wrong_norm':lambda x:x.__setitem__('norm','Euclidean-coefficients'),
      'wrong_target':lambda x:x.__setitem__('target','certified-floating-state'),
      'wrong_initial':lambda x:x.__setitem__('initial_state','arbitrary-state'),
      'wrong_order':lambda x:x.__setitem__('factorial_order',1),
      'wrong_action':lambda x:x.__setitem__('action_interval',['0','0']),
      'wrong_cap':lambda x:x.__setitem__('state_error_upper','0'),
      'false_timestep_claim':lambda x:x.__setitem__('time_step_error','certified'),
      'bool_degree':lambda x:x.__setitem__('degree',True),
      'integer_bool':lambda x:x.__setitem__('bound_is_below_trivial_two',1),
      'empty_source_set':lambda x:x.__setitem__('source_hashes',{}),
      'missing_scope':lambda x:x.pop('scope'),
      'wrong_source':lambda x:x['source_hashes'].__setitem__('drive_bound.py','0'*64),
    }
    for name,mutate in mutations.items():
        changed=copy.deepcopy(c);mutate(changed);rejects(lambda:m.verify_certificate(changed),'metadata_mutation.'+name)
    for bad_args in [(-1,1,0),(1,0,1),(1,True,0),(1,1,False)]:rejects(lambda:m.factorial_bound(*bad_args),'invalid_factorial.'+str(bad_args))
    for protocol in [{'kind':'unknown'},{'kind':'piecewise_constant','segments':[]},
                     {'kind':'constant','duration':'-1','lambda1_scale':'1','lambda2_scale':'0'},
                     {'kind':'constant','duration':True,'lambda1_scale':'1','lambda2_scale':'0'}]:rejects(lambda:m.canonical_protocol(protocol),'invalid_protocol.'+str(protocol))
    zero={'kind':'cosine_ramp','duration':'0','lambda1_scale':'100','lambda2_scale':'-100'}
    check(m.action_interval(zero)==(0,0) and m.certificate(zero,0)['state_error_upper']=='0','zero_duration_exact')
    # All provenance mutations stay in a reviewer-owned copied package.
    probe=Path(__file__).parent/'drive_probe';probe.mkdir(exist_ok=True);(probe/'vendor').mkdir(exist_ok=True)
    declared=json.loads((src.parent/'dependencies.json').read_text())['expected_dependencies']
    for rel in ('drive_bound.py','dependencies.json',*(d['path'] for d in declared)):
        (probe/rel).parent.mkdir(parents=True,exist_ok=True);(probe/rel).write_bytes((src.parent/rel).read_bytes())
    copied=load(probe/'drive_bound.py','copied_drive_bound');manifest=probe/'dependencies.json';raw=manifest.read_bytes();data=json.loads(raw)
    for name,mutate in [('empty',lambda d:d.__setitem__('expected_dependencies',[])),('extra',lambda d:d['expected_dependencies'].append(copy.deepcopy(d['expected_dependencies'][0]))),('wrong_digest',lambda d:d['expected_dependencies'][0].__setitem__('sha256','0'*64))]:
        changed=copy.deepcopy(data);mutate(changed);manifest.write_text(json.dumps(changed));rejects(copied.expected_dependencies,'dependency_mutation.'+name);manifest.write_bytes(raw)
    vendor=probe/'vendor/two_plaquette.py';vraw=vendor.read_bytes();target=probe/'vendor/same_bytes.py';target.write_bytes(vraw);vendor.unlink();vendor.symlink_to(target.name)
    try:rejects(copied.expected_dependencies,'vendor_same_bytes_symlink_rejected')
    finally:vendor.unlink();vendor.write_bytes(vraw);target.unlink()
    target=probe/'same_manifest.json';target.write_bytes(raw);manifest.unlink();manifest.symlink_to(target.name)
    try:
        try:copied.expected_dependencies()
        except (ValueError,RuntimeError):check(True,'manifest_same_bytes_symlink_rejected')
        else:defects.append({'defect':'dependency manifest symlink accepted','scope':'input-path identity; digest bytes unchanged','fixture':'dependencies.json -> same_manifest.json'})
    finally:manifest.unlink();manifest.write_bytes(raw);target.unlink()
    check(digest(src)==before,'source_unchanged_during_audit')
    tree=ast.parse(src.read_text());functions=[{'name':n.name,'first_line':n.lineno,'last_line':n.end_lineno} for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]
    result={'status':'passed-with-input-path-defect' if defects else 'passed','optimized_python':not __debug__,'source_sha256':before,'audit_sha256':digest(__file__),
      'gate_count':len(records),'records':records,'defects':defects,'reviewed_functions':functions,'certificates':certificates,
      'scope':'Exact action enclosure, factorial arithmetic, typed certificate semantics and input provenance; theorem hypotheses are explicitly conditional.'}
    output=Path(__file__).with_name(args.label+'_results.json');output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'gate_count':len(records),'source_sha256':before,'defects':defects}))
if __name__=='__main__':main()
