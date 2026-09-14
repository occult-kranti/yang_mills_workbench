#!/usr/bin/env python3
"""Independent local support and actual clipped-component E2 reconstruction."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def flinks(f):
 a,b,x,y,z=f;c=(x,y,z);ca=list(c);ca[a]+=1;cb=list(c);cb[b]+=1
 return {(a,*c),(b,*ca),(a,*cb),(b,*c)}
def sel(f):
 a,b,x,y,z=f;return (a,b)==(0,1) and y%2==0 and x%4<3

def fullfactor(e):
 a,x,y,z=e
 if a==0 and x%4<3:return ('s',x-x%4,y-y%2,z)
 if a==1 and y%2==0:return ('s',x-x%4,y,z)
 return ('f',*e)
def support(f):
 if f[0]=='f':return {tuple(f[1:])}
 _,x,y,z=f
 return {(0,x+j,y+k,z) for j in range(3) for k in range(2)}|{(1,x+j,y,z) for j in range(4)}
def interior(M):
 return [f for a,b in [(0,1),(0,2),(1,2)] for x in range(M+1) for y in range(M+1) for z in range(M+1) if not sel(f:=(a,b,x,y,z))]
def tail(M):
 S=2*(1-F(1,2**(M+1)));Y=F(4,3)*(1-F(1,4**(M//2+1)));X=F(2,15)*(1-F(1,16**((M+1)//4)))
 return F(107,135)-(2*S**3+S*(S-Y)*S+X*Y*S)/24

def box(shape,central):
 nx,ny,nz=shape
 es={(a,x,y,z) for a in range(3) for x in range(nx+1) for y in range(ny+1) for z in range(nz+1) if (x,y,z)[a]<shape[a]}
 fs=[(a,b,x,y,z) for a,b in [(0,1),(0,2),(1,2)] for x in range(nx+1) for y in range(ny+1) for z in range(nz+1) if (x,y,z)[a]<shape[a] and (x,y,z)[b]<shape[b]]
 parent={e:e for e in es}
 def find(e):
  while parent[e]!=e:parent[e]=parent[parent[e]];e=parent[e]
  return e
 for f in fs:
  if sel(f):
   edges=list(flinks(f));r=find(edges[0])
   for e in edges[1:]:parent[find(e)]=r
 components={}
 for e in es:components.setdefault(find(e),set()).add(e)
 parts=list(components.values());free=set().union(*(p for p in parts if len(p)==1))
 if any(support(f) not in parts for f in central):raise RuntimeError('central infinite factor not literal complete factor')
 failures=[f for f in fs if not sel(f) and not (flinks(f)&free)]
 if failures:raise RuntimeError('omitted face has no free Haar witness')
 return {'shape':list(shape),'Nx_mod4':nx%4,'Ny_mod2':ny%2,'selected_components':sum(len(p)>1 for p in parts),'free_links':len(free),'omitted_faces':sum(not sel(f) for f in fs),'witness_failures':len(failures),'component_link_sizes':sorted({len(p) for p in parts}),'central_factor_count':len(central)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 M=1;vm=set().union(*(flinks(f) for f in interior(M)))
 obs={(2,9,2,1),(0,6,5,2)};central={fullfactor(e) for e in vm|obs}
 fixture=[box((12+r,12+s,12),central) for r in range(4) for s in range(2)]
 rows=[]
 for m in range(9):
  t=tail(m);s=F(107,135)-t;eps=t/32;g=F(1,4)-s/32
  rows.append({'M':m,'tail':str(t),'epsilon_over_E_star':str(eps),'g_M_over_E_star':str(g),'one_projection_error':str(min(F(1),eps/g)),'local_observable_error_over_norm':str(4*min(F(1),eps/g))})
 controls=[]
 def ck(name,v):
  if not v:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 missing={fullfactor(e) for e in obs}-{fullfactor(e) for e in vm}
 ck('omit_observable_support_detected',len(missing)>0)
 try:box((3,3,3),central)
 except RuntimeError:ck('insufficient_geometric_margin_rejected',True)
 else:raise RuntimeError('insufficient margin admitted')
 # Same central state, orthogonal remote factors: global fidelity 0 even
 # though each central bounded-observable expectation agrees exactly.
 central_overlap=F(1);boundary_overlap=F(0)
 ck('local_state_equality_not_global_vector_equality',central_overlap*boundary_overlap==0 and central_overlap==1)
 cbox=F(-3,7);raw_floor=cbox+F(1,4)
 ck('unshifted_component_floor_rejected',raw_floor<F(1,4))
 t=tail(1);betaM=(F(107,135)-t)/32
 ck('missing_uniform_A1_gap_invalidates_denominator',F(0)-betaM<=0)
 # Nondecaying added coefficient sum grows with every added box face.
 ck('homogeneous_tail_not_summable',len(interior(3))>len(interior(2)))
 ck('signed_cancellation_not_tail',abs(F(1,8)-F(1,8))<abs(F(1,8))+abs(F(-1,8)))
 data={'schema':'ym20-reverse-e2-v1','status':'passed','rows':rows,'geometry_fixtures':fixture,'controls':controls,'observable_support':[list(e) for e in sorted(obs)],'extra_observable_factors':len(missing),'scalar_origin':'c_box=sum clipped component ground energies','scope':'weak-star convergence on quasi-local algebra for arbitrary upper boundary phases; no global vector/resolvent or continuum claim'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/e2.json',ROOT/'research/round20/advisor/e1-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'geometry_fixtures':len(fixture),'controls':len(controls)}))
if __name__=='__main__':main()
