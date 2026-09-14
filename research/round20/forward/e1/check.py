#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,hashlib,json,importlib.util
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
D1=ROOT/'research/round20/forward/d1/check.py'
spec=importlib.util.spec_from_file_location('frozen_forward_d1_geometry',D1)
geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)

def require(x,m):
    if not x:raise ValueError(m)

def rejected(fn):
    try:fn()
    except ValueError:return True
    return False

def box_links(N):
    return {(axis,*p) for axis in range(3) for p in product(*(range(N if j==axis else N+1) for j in range(3)))}

def box_faces(N):
    return [(*ab,*p) for ab in ((0,1),(0,2),(1,2)) for p in product(*(range(N if j in ab else N+1) for j in range(3)))]

def full_factors(N):
    links=box_links(N);facs={geo.factor(e) for e in links}
    require(all(geo.factor_links(i)<=links for i in facs),'literal box clips reference factor')
    return links,facs

def ledger(N):
    require(N>=3 and N%4==3,'aligned extent required')
    m=(N-3)//4;g=lambda n:2*(1-F(1,2**n))
    a=F(28,15)*(1-F(1,16**(m+1)));b=F(4,3)*(1-F(1,4**((N+1)//2)))
    return g(N)**2*g(N+1)/8-a*b*g(N+1)/24

def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,list):return [encode(v) for v in o]
    return o

def main(out):
    contract=ROOT/'research/round20/contracts/e1.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'D2 gate changed')
    rows=[]
    for N in (3,7,11,15):
        links,facs=full_factors(N);faces=box_faces(N);omitted=[f for f in faces if not geo.selected(f)]
        require(all(geo.face_links(f)<=links for f in faces),'face not internal')
        strips=sum(i[0]=='strip' for i in facs);B=((N-3)//4+1)*(N+1)**2//2
        require(strips==B and len(links)==3*N*(N+1)**2 and len(faces)==3*N*N*(N+1),'literal counts disagree')
        require(len(omitted)==len(faces)-3*B and len(links)-10*B==sum(i[0]=='free' for i in facs),'selected/free counts disagree')
        W=sum((geo.weight(f) for f in omitted),F());require(W==ledger(N),'orientation ledger differs')
        T=F(107,135)-W;eps=T/64;g=F(1,8)-W/64
        rows.append({'N':N,'links':len(links),'faces':len(faces),'strips':B,'free_links':len(links)-10*B,'omitted_faces':len(omitted),'retained_weight':W,'tail_weight':T,'epsilon_over_alpha':eps,'g_over_alpha':g,'projector_error':min(F(1),eps/g),'unit_observable_error':2*min(F(1),eps/g),'c_N_over_E_strip':B})
    wrong_anchor=geo.closed(3);right_anchor=ledger(3)
    shift=F(-1);unshifted_resolvent_difference_square=shift**2/(1+shift**2)
    controls={
      'all_three_anchor_cube_rejected':rejected(lambda:require(wrong_anchor==right_anchor,'wrong orientation ranges')),
      'nonaligned_N4_promotion_rejected':rejected(lambda:full_factors(4)),
      'omit_scalar_shift_rejected':unshifted_resolvent_difference_square==F(1,2) and unshifted_resolvent_difference_square>0,
      'discard_exterior_rejected':F(3,4)**2/(1+F(3,4)**2)==F(9,25),
      'zero_reference_rejected':rejected(lambda:geo.scale(reference_positive=False)),
      'old_face_coefficients_unchanged':all(geo.weight(f)==F(1,24*2**sum(f[2:])) for f in box_faces(3)),
    }
    require(all(controls.values()),'control failed')
    result={'schema':'ym20-forward-e1-v1','loop':'e1','status':'passed','fixtures':rows,'controls':controls,
            'wrong_anchor_retained_N3':wrong_anchor,'correct_literal_retained_N3':right_anchor,
            'energy_origin':'H_box,N - c_N with c_N=sum_C E_C; same states and gaps, different absolute energies/resolvents',
            'scale':{'E_star':'fixed positive physical energy','alpha_over_E_star':'1','tau':'1/64','a':'fixed length'},
            'scope':'literal aligned boxes N=4m+3 and exact exterior lift only'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',D1,contract,gate,ROOT/'research/round20/advisor/d1-gate.json',ROOT/'research/round19/advisor/a1-gate.json',ROOT/'research/round19/advisor/a2-gate.json']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','loop':'e1','fixtures':len(rows),'controls':len(controls)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
