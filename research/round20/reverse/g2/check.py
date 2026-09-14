#!/usr/bin/env python3
"""Exact finite discriminators for the analytic GNS identification."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return sum((A[i][i] for i in range(len(A))),F(0))
def adj(A):return [list(r) for r in zip(*A)]
def rank(A):
 A=[list(map(F,r)) for r in A];n=len(A);m=len(A[0]);r=0
 for j in range(m):
  piv=next((i for i in range(r,n) if A[i][j]),None)
  if piv is None:continue
  A[r],A[piv]=A[piv],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
  for i in range(n):
   if i!=r:
    v=A[i][j];A[i]=[a-v*b for a,b in zip(A[i],A[r])]
  r+=1
  if r==n:break
 return r

def gram(rho,basis):return [[tr(mm(rho,mm(adj(a),b))) for b in basis] for a in basis]
def energy(alpha,tau,E):
 if E<=0 or alpha<=0:raise ValueError('positive alpha and E_star required')
 beta=alpha*abs(tau)*F(107,135);delta=alpha/8
 if beta>=delta:raise ValueError('G2 restores ground isolation smallness')
 return beta/E,(delta-beta)/E

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 basis=[[[F(int(a==i and b==j)) for b in range(2)] for a in range(2)] for i in range(2) for j in range(2)]
 psi=[F(3,5),F(4,5)];pure=[[x*y for y in psi] for x in psi];mixed=[[F(1,2),F(0)],[F(0),F(1,2)]]
 Gp,Gm=gram(pure,basis),gram(mixed,basis);rp,rm=rank(Gp),rank(Gm)
 controls=[]
 def ck(name,v):
  if not v:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 ck('pure_GNS_Gram_rank2',rp==2);ck('mixed_GNS_Gram_rank4',rm==4);ck('mixed_state_not_same_vector_GNS',rm!=len(psi))
 diagonal=[basis[0],basis[3]];T=[[F(1),F(0)],[F(0),F(-1)]]
 ck('reducible_algebra_has_nonscalar_commutant',all(mm(T,A)==mm(A,T) for A in diagonal) and mm(T,basis[1])!=mm(basis[1],T))
 v=[[F(1)],[F(0)]];span=[list(r) for r in zip(*(sum(mm(A,v),[]) for A in diagonal))]
 ck('reducible_algebra_nonzero_vector_not_cyclic',rank(span)==1)
 e=F(-1,8);threshold=F(1,4);absolute=[e,threshold];shifted=[x-e for x in absolute]
 ck('ground_energy_subtraction_required',absolute[0]!=0 and shifted[0]==0)
 ck('threshold_distinct_from_exact_gap',shifted[1]==F(3,8) and shifted[1]>threshold)
 # The excitation phase in canonical GNS is E1-e; H alone does not fix Omega.
 ck('GNS_covariance_energy_phase',threshold-e==shifted[1] and e!=0)
 for name,args in [('zero_E',(F(2),F(1,64),F(0))),('missing_smallness',(F(2),F(1),F(1)))]:
  try:energy(*args)
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 beta,gap=energy(F(2),F(1,64),F(1))
 data={'schema':'ym20-reverse-g2-v1','status':'passed','controls':controls,'pure_gram':[[str(x) for x in r] for r in Gp],'mixed_gram':[[str(x) for x in r] for r in Gm],'pure_gram_rank':rp,'mixed_gram_rank':rm,'spectral_shift_fixture':{'absolute':list(map(str,absolute)),'shifted':list(map(str,shifted))},'scale':{'alpha/E_star':'2','tau':'1/64','beta/E_star':str(beta),'GNS_gap_floor/E_star':str(gap),'energy_generator':'H-e','Stone_frequency_generator':'(H-e)/hbar'},'scope':'full complete-factor local B algebra in A2 representation; no Gauss-only equality or continuum inference'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/g2.json',ROOT/'research/round20/advisor/g1-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','Gram_ranks':[rp,rm],'controls':len(controls)}))
if __name__=='__main__':main()
