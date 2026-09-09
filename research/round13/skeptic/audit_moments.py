"""Independent exact certificate, principal-minor, and mutation audit."""
from pathlib import Path
from fractions import Fraction as Q
import argparse, copy, csv, hashlib, importlib.util, json, math, random, sys
from independent_oracle import (bessel_mean_interval, haar_tilt_interval, independent_moments,
                               haar, all_principal_minors_psd, intersects)

p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--label',default='moments_normal');args=p.parse_args()
source=Path(args.source).resolve();before=hashlib.sha256(source.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('producer_moments',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
checks=[];failures=[];records=[]

def check(name,ok,detail=''):
    row={'name':name,'status':'passed' if ok else 'failed','detail':detail}
    checks.append(row)
    if not ok:failures.append(row)

def reject(name,func):
    try:func()
    except (ValueError,TypeError,ArithmeticError,RuntimeError):check(name,True);return
    check(name,False,'Invalid input unexpectedly accepted')

def qform(matrix,v):
    return sum((v[i]*matrix[i][j]*v[j] for i in range(len(v)) for j in range(len(v))),Q(0))

def independent_pairs(k,r,family):
    m=independent_moments(k,2*r)
    if family=='H':return [[m[i+j] for j in range(r+1)] for i in range(r+1)]
    return [[tuple(m[i+j][a]-m[i+j+2][a] for a in (0,1)) for j in range(r)] for i in range(r)]

def eval_pairs(matrix,u):return [[a+b*u for a,b in row] for row in matrix]

cases=[('0',1),('0',6),('1/1000',2),('1/1000',6),('-1/1000',4),('1',1),('1',2),('1',4),('1',6),('-1',6),('5',4),('-5',4),('20',6),('-20',6),('100',3),('-100',3)]
certs={}
for k,r in cases:
    c=mod.certify(k,r,bits=32);certs[k,r]=c
    tag=k+'_r'+str(r)
    check('producer_replay_'+tag,mod.verify(c) is True)
    lo,hi=map(Q,c['mean_interval']);vl,vu=map(Q,c['variance_interval'])
    oracle=bessel_mean_interval(k,180);haar_oracle=haar_tilt_interval(k,1,360)
    check('series_agree_'+tag,intersects(oracle,haar_oracle))
    check('contains_bessel_'+tag,lo<=oracle[0]<=oracle[1]<=hi)
    second=haar_tilt_interval(k,2,360)
    absmin=Q(0) if oracle[0]<=0<=oracle[1] else min(oracle[0]**2,oracle[1]**2)
    varoracle=(second[0]-max(oracle[0]**2,oracle[1]**2),second[1]-absmin)
    check('contains_variance_'+tag,vl<=varoracle[0]<=varoracle[1]<=vu)
    if Q(k):
        for j,w in enumerate(c['witnesses']):
            pairs=independent_pairs(k,r,w['family']);v=list(map(Q,w['vector']))
            aa=qform([[a for a,b in row] for row in pairs],v)
            bb=qform([[b for a,b in row] for row in pairs],v)
            check('dual_direct_'+tag+'_'+str(j),(bb>0)==(j==0) and aa==Q(w['constant']) and bb==Q(w['slope']) and -aa/bb==Q(w['root']))
        for j,u in enumerate(map(Q,c['feasible_inner_points'])):
            okay=all(all_principal_minors_psd(eval_pairs(independent_pairs(k,r,f),u)) for f in ('H','L'))
            check('exhaustive_principal_minor_'+tag+'_'+str(j),okay)
        if r==1 and Q(k)>0:
            check('r1_analytic_interval_'+tag,lo<=0<=hi and hi*hi+3*hi/Q(k)-1>=0)
    else:check('zero_haar_moments_'+tag,list(map(Q,c['moments']))==[haar(j) for j in range(2*r+1)])
    records.append({'kappa':k,'level':r,'mean_interval':c['mean_interval'],'variance_interval':c['variance_interval'],'bessel_interval':list(map(str,oracle)),'haar_interval':list(map(str,haar_oracle))})
for r in (1,2,4):
    a=certs['1',r];b=certs['1',{1:2,2:4,4:6}[r]]
    # Outer enclosures are optimization-accurate, but generic heuristic cut sets need not nest.
    check('positive_fixture_refinement_r'+str(r),Q(b['mean_interval'][0])>=Q(a['mean_interval'][0]) and Q(b['mean_interval'][1])<=Q(a['mean_interval'][1]))
for k,r in [('1',6),('5',4),('20',6),('100',3)]:
    a=certs[k,r];b=certs['-'+k,r]
    check('signed_symmetry_'+k,list(map(Q,b['mean_interval']))==[-Q(a['mean_interval'][1]),-Q(a['mean_interval'][0])])

# A separate exhaustive principal-minor oracle attacks congruence and zero pivots.
fixtures=[[[0,1],[1,0]],[[0,0],[0,-1]],[[0,0],[0,0]],[[1,1],[1,1]],[[1,0],[0,0]],[[1,2],[2,1]],[[1,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,1],[0,1,1]]]
rng=random.Random(1309)
for _ in range(20):
    n=rng.choice([2,3,4]);a=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i,n):a[i][j]=a[j][i]=rng.randrange(-2,3)
    fixtures.append(a)
for j,a in enumerate(fixtures):
    v=mod.negative_witness(a);psd=all_principal_minors_psd(a)
    check('congruence_vs_principal_minors_'+str(j),(v is None)==psd and (v is None or qform(a,v)<0))

base=certs['1',4]
def mutate(name,edit):
    d=copy.deepcopy(base);edit(d);reject('mutation_'+name,lambda:mod.verify(d))
mutate('source',lambda d:d.update(source_sha256='0'*64))
mutate('scope',lambda d:d.update(scope='four dimensional quantum mass gap'))
mutate('schema',lambda d:d.update(schema='wrong'))
mutate('status',lambda d:d.update(status='solved'))
mutate('method',lambda d:d.update(method='finite floating eigenvalue'))
mutate('missing_field',lambda d:d.pop('bits'))
mutate('unknown_field',lambda d:d.update(hidden_assumption=True))
mutate('kappa',lambda d:d.update(kappa='2'))
mutate('level',lambda d:d.update(level=3))
mutate('bits',lambda d:d.update(bits=31))
mutate('lower',lambda d:d['mean_interval'].__setitem__(0,'1/2'))
mutate('upper',lambda d:d['mean_interval'].__setitem__(1,'1/2'))
mutate('variance',lambda d:d.update(variance_interval=['0','0']))
mutate('family',lambda d:d['witnesses'][0].update(family='D'))
mutate('vector_zero',lambda d:d['witnesses'][0].update(vector=['0']*len(d['witnesses'][0]['vector'])))
mutate('vector_shape',lambda d:d['witnesses'][0]['vector'].pop())
mutate('vector_sign_direction_swap',lambda d:d.update(witnesses=list(reversed(d['witnesses']))))
mutate('coefficient',lambda d:d['witnesses'][0].update(constant='0'))
mutate('root',lambda d:d['witnesses'][0].update(root='0'))
mutate('slope',lambda d:d['witnesses'][0].update(slope='0'))
mutate('interior',lambda d:d.update(feasible_inner_points=['-1','1']))
mutate('slack',lambda d:d.update(optimization_slack_per_side='1'))
mutate('boolean_witness',lambda d:d['witnesses'][0]['vector'].__setitem__(0,True))
for bad in [True,False,1.0,float('nan'),float('inf'),None,[],{},'nan','inf','1/0','101','-101']:
    reject('invalid_kappa_'+repr(bad),lambda bad=bad:mod.certify(bad,2))
for bad in [True,False,0,7,1.0,'2',None]:reject('invalid_level_'+repr(bad),lambda bad=bad:mod.certify('1',bad))
for bad in [True,7,97,48.0,'48',None]:reject('invalid_bits_'+repr(bad),lambda bad=bad:mod.certify('1',2,bad))
for bad in [[],[[1,2]],[[1,1],[0,1]],[[True]]]:reject('invalid_matrix_'+repr(bad),lambda bad=bad:mod.negative_witness(bad))
reject('zero_affine',lambda:mod.affine('0',4))
for bits in (8,96):
    c=mod.certify('1',2,bits);check('endpoint_precision_'+str(bits),mod.verify(c))
check('point_closure_passes_r1',mod.witness(Q(9,8),1,Q(1,3)) is None)
check('point_closure_fails_r2',mod.witness(Q(9,8),2,Q(1,3)) is not None)
check('point_closure_next_residual',1-4*Q(1,3)**2+Q(9,8)*(Q(1,3)-Q(1,3)**3)==Q(8,9))
study_path=source.parent/'output'/'study.json'
if study_path.exists():
    study=json.loads(study_path.read_text())
    for name,digest in study['source_hashes'].items():
        check('study_source_'+name,hashlib.sha256((source.parent/name).read_bytes()).hexdigest()==digest)
    dataset=json.loads((source.parent/'output'/'certificates.json').read_text())
    rows=list(csv.DictReader((source.parent/'output'/'bounds.csv').open()))
    check('study_record_count',len(dataset['certificates'])==len(rows)==study['cases']==28)
    check('study_dataset_hash',dataset['source_sha256']==before)
    for j,(c,row) in enumerate(zip(dataset['certificates'],rows)):
        lo,hi=map(Q,c['mean_interval']);oracle=bessel_mean_interval(c['kappa'],180)
        check('stored_certificate_'+str(j),mod.verify(c) and lo<=oracle[0]<=oracle[1]<=hi)
        equal=(row['kappa']==c['kappa'] and int(row['level'])==c['level']
               and row['mean_lower']==c['mean_interval'][0] and row['mean_upper']==c['mean_interval'][1]
               and Q(row['mean_width'])==hi-lo
               and [row['variance_lower'],row['variance_upper']]==c['variance_interval'])
        if hi>lo:equal=equal and abs(float(row['log10_mean_width'])-math.log10(float(hi-lo)))<1e-12
        else:equal=equal and row['log10_mean_width']==''
        check('stored_csv_binding_'+str(j),equal)
check('unchanged_source',before==hashlib.sha256(source.read_bytes()).hexdigest())
out={'status':'passed' if not failures else 'failed','source_sha256':before,'source':str(source),'count':len(checks),'checks':checks,'failures':failures,'records':records,'scope':'Finite compact tilted Haar moment hierarchy; independent exact series, principal minors and metadata mutations. No spectral gap.'}
Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'count':len(checks),'failures':failures},indent=2))
if failures:raise SystemExit(1)
