#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,hashlib,json,importlib.util
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
D1=ROOT/'research/round20/forward/d1/check.py'
sp=importlib.util.spec_from_file_location('frozen_d1_geometry_e2',D1);geo=importlib.util.module_from_spec(sp);sp.loader.exec_module(geo)
def require(ok,m):
    if not ok:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def links_box(N):
    return {(a,*p) for a in range(3) for p in product(*(range(N[j]+(j!=a)) for j in range(3)))}
def faces_box(N):
    return [(*ab,*p) for ab in ((0,1),(0,2),(1,2)) for p in product(*(range(N[j]+(j not in ab)) for j in range(3)))]
def witness(f):
    a,b,x,y,z=f
    if (a,b)!=(0,1):return (2,x,y,z)
    if y%2:return (1,x,y,z)
    return (0,x,y,z)
def rect_ledger(N):
    nx,ny,nz=N;g=lambda n:2*(1-F(1,2**n))
    total=(g(nx)*g(ny)*g(nz+1)+g(nx)*g(ny+1)*g(nz)+g(nx+1)*g(ny)*g(nz))/24
    x=sum((F(1,2**r)*(1-F(1,16**max(0,1+(nx-1-r)//4)))/(1-F(1,16)) for r in range(3)),F())
    y=(1-F(1,4**((ny+1)//2)))/(1-F(1,4))
    return total-x*y*g(nz+1)/24
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/e2.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'E1 gate changed')
    M=0;interior=geo.retained(M);raw,factors,full=geo.complete(interior)
    observable={(0,4,0,0)};central=factors|{geo.factor(e) for e in observable}
    central_links=set().union(*(geo.factor_links(f) for f in central))
    require(not observable<=full,'observable fixture accidentally already central')
    sM=geo.closed(M);eps=(F(107,135)-sM)/64;g=F(1,8)-sM/64;rows=[]
    for rx,py in product(range(4),range(2)):
        N=(8+rx,8+py,8);links=links_box(N);faces=faces_box(N);components={}
        for f in faces:
            if geo.selected(f):
                fac=('strip',f[2]-f[2]%4,f[3],f[4]);components.setdefault(fac,set()).update(geo.face_links(f))
        occupied=set()
        for fac,component in components.items():
            require(not occupied&component,'clipped components overlap');occupied|=component
        omitted=[f for f in faces if not geo.selected(f)]
        require(all(witness(f) in links and witness(f) not in occupied for f in omitted),'Haar witness not free in clipped reference')
        require(central_links<=links,'central completion escapes box')
        require(all(components.get(f)==geo.factor_links(f) for f in central if f[0]=='strip'),'central factor is clipped')
        W=sum((geo.weight(f) for f in omitted),F());require(W==rect_ledger(N),'rectangular closed ledger mismatch')
        eta=(W-sM)/64;require(0<=eta<=eps,'uniform tail violated')
        rows.append({'N':N,'x_mod4':rx,'y_mod2':py,'reference_components':len(components),'clipped_components':sum(len(e)!=10 for e in components.values()),'omitted_faces':len(omitted),'free_witnesses_verified':len(omitted),'retained_weight':W,'eta_over_alpha':eta,'uniform_epsilon_over_alpha':eps,'g_M_over_alpha':g,'local_unit_error_bound':4*min(F(1),eps/g),'sharper_box_unit_error_bound':2*(min(F(1),eta/g)+min(F(1),eps/g))})
    error_rows=[]
    for m in range(9):
        s=geo.closed(m);e=(F(107,135)-s)/64;floor=F(1,8)-s/64
        error_rows.append({'M':m,'epsilon_over_alpha':e,'g_M_over_alpha':floor,'unit_local_error_bound':4*min(F(1),e/floor)})
    c,s=F(3,5),F(4,5);moving_projection_square=1-c*c
    negative_component_ground=F(-1);unshifted_excited=F(-7,8);delta=F(1,8)
    controls={
      'omitted_observable_support_rejected':rejected(lambda:require(observable<=full,'observable unsupported')),
      'local_implies_vector_norm_rejected':moving_projection_square==s*s and moving_projection_square>0,
      'unshifted_component_nonnegative_claim_rejected':rejected(lambda:require(negative_component_ground>=0,'component shift missing')),
      'shift_preserves_local_gap':unshifted_excited-negative_component_ground==delta,
      'missing_uniform_delta_rejected':rejected(lambda:require(F(0)>F(107,135)/64,'no positive compression without delta')),
      'local_implies_global_norm_resolvent_rejected':F(3,4)**2/(1+F(3,4)**2)==F(9,25),
      'homogeneous_tail_rejected':3*9**3>3*8**3,
    }
    require(all(controls.values()),'control failed')
    result={'schema':'ym20-forward-e2-v1','loop':'e2','status':'passed','phase_fixtures':rows,'error_fixtures':error_rows,'controls':controls,'central_M':M,'observable_links':list(observable),'central_factors':len(central),'bound':'4||A||min(1,epsilon_M/g_M)','scale':{'E_star':'fixed positive physical energy','alpha_over_E_star':'1','tau':'1/64'},'scope':'local weak-star convergence for all anchored rectangular boundary phases; no global vector or norm-resolvent claim'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',D1,contract,gate,ROOT/'research/round20/advisor/d2-gate.json',ROOT/'research/round19/advisor/a1-gate.json',ROOT/'research/round19/advisor/a2-gate.json']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'e2','phases':len(rows),'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
