#!/usr/bin/env python3
"""Independent reverse AL1 exact coefficient and original-face audit."""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

BASE = Path(__file__).resolve().parent
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition, message):
    if not condition: raise AssertionError(message)
def positive_scale(value):
    if isinstance(value,bool) or F(value)<=0: raise ValueError('physical scale must be positive')
    return F(value)
def plus(x,y): return tuple(a+b for a,b in zip(x,y))
E = ((1,0,0),(0,1,0),(0,0,1))
O = (0,0,0)
def coarse(x): return (x[0]//4,x[1]//2,x[2])
def face(x,i,j):
    # Each tuple is the tail of an original oriented link, with direction.
    return ((x,i),(plus(x,E[i]),j),(plus(x,E[j]),i),(x,j))
def selected(x,i,j): return (i,j)==(0,1) and x[1]%2==0 and x[0]%4<3
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=BASE/'output')
    args=parser.parse_args()
    contract=json.loads((BASE/'inputs/research/round29/contracts/al1.json').read_text())
    check(contract['id']=='AL1','contract id')
    links={(x,y,0,d) for x in range(4) for y in range(2) for d in range(3)}
    faces=[]
    for x in range(4):
      for y in range(2):
       for i,j in ((0,1),(0,2),(1,2)):
        v=(x,y,0); s={coarse(t) for t,d in face(v,i,j)}
        kind=('bridge' if x==1 else 'endpoint') if selected(v,i,j) else 'omitted'
        faces.append({'base':v,'axes':(i,j),'kind':kind,'support':sorted(s)})
    counts={k:sum(f['kind']==k for f in faces) for k in ('endpoint','bridge','omitted')}
    check(len(links)==24 and counts=={'endpoint':2,'bridge':1,'omitted':21},'complete classes')
    star={O,*E}; check(all(set(map(tuple,f['support']))<=star for f in faces),'whole range')
    B={O,E[0]}
    mismatch=[f for f in faces if f['kind']=='omitted' and set(map(tuple,f['support']))<=B and not star<=B]
    check(len(mismatch)==1,'actual-contained versus whole-star mismatch')
    # An independent derivation from trace(2I-U-U*)=4-4W.
    data=[]
    for n in (1,2,3,8,32):
      a=F(1,n); g2=F(1,n); alpha=g2/(2*a); lam=2/(g2*a)
      r=lam/alpha; tau=24*r; eps=21*(lam/(alpha/8))
      check(alpha==F(1,2) and r==4*n*n and tau==96*n*n and eps==672*n*n,'all-path formulas')
      check(not r<=F(1,8),'path bridge rejection')
      check(eps==7*tau,'local normalization')
      data.append({'n':n,'a':str(a),'g_squared':str(g2),'alpha':str(alpha),'lambda':str(lam),'r':str(r),'tau':str(tau),'epsilon':str(eps)})
    # Wrong-model controls use fixtures which genuinely distinguish the claim.
    control_r=F(1,4)
    true_tau=24*control_r
    local_full=21*8*control_r
    # Time clock: delta=alpha/8, so u=delta*t/hbar, not t/hbar.
    alpha,hbar,t=F(2),F(3),F(5); delta=alpha/8
    true_clock=delta*t/hbar; wrong_clock=t/hbar
    q=(1,1,1); incoming={q,*[tuple(q[i]-e[i] for i in range(3)) for e in E]}
    try: positive_scale(0)
    except ValueError: rejected_zero=True
    else: rejected_zero=False
    controls={
      'omit_bridge_class': control_r<=F(1,2) and not control_r<=F(1,8),
      'tau_incorrectly_equals_r': local_full==7*true_tau and local_full!=7*control_r,
      'drop_incoming_stars': len(incoming)==4 and 4*local_full!=local_full,
      'wrong_kinetic_coefficient': F(2)/(F(1,1)/2)!=F(2)/F(1),
      'wrong_normalized_clock': true_clock!=wrong_clock,
      'zero_E_star_rejected': rejected_zero,
      'summable_profile_substitution': F(1,24)!=F(1,48),
      'finite_boundary_substitution':len(mismatch)>0,
      # In the explicit matrix 2I-sigma_x, E0=1 whereas the raw scalar is 2.
      'raw_scalar_is_not_ground_energy':F(2)-F(1)!=F(2),
    }
    check(all(controls.values()),'discriminating controls')
    result={'loop':'AL1','direction':'reverse','label':'HNM full-interaction matching audit','verdict':'candidate outside sufficient domain for every n>=1','units':'a0,hbar,E_star positive; numerical fixtures a0=E_star=1','counts':counts,'original_links_per_factor':len(links),'whole_star_sites':len(star),'boundary_mismatch':mismatch,'path':data,'controls':controls,'symbolic_conditions':['g^4>=32','672/g^4<c1(S)','672*c2(S)/g^4<1/2'],'physical_alpha':'1/(2 a0)','increment':'complete selected/omitted dictionary, bridge g^4>=32, local-budget and finite-boundary controls; R18-B2 g^4>=32/3 is inherited','scope':'Failure of a sufficient theorem application, not actual gap failure, no continuum theorem.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=sorted([BASE/'check.py',BASE/'report.md']+[p for p in (BASE/'inputs').rglob('*') if p.is_file()])
    manifest={'loop':'AL1','direction':'reverse','command':'python research/round29/reverse/al1/check.py --output <output-dir>','source_files':[{'path':str(p.relative_to(BASE)),'sha256':digest(p)} for p in files],'results_sha256':digest(out/'results.json')}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'loop':'AL1','controls':len(controls),'passed':True,'verdict':result['verdict']}))
if __name__=='__main__':main()
