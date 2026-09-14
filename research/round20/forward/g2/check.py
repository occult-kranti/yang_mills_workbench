#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(ok,m):
    if not ok:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def rank(a):
    a=[list(map(F,r)) for r in a];row=0
    for col in range(len(a[0])):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];p=a[row][col];a[row]=[v/p for v in a[row]]
        for j in range(len(a)):
            if j!=row:
                v=a[j][col];a[j]=[x-v*y for x,y in zip(a[j],a[row])]
        row+=1
    return row
def gram(rho):
    units=[(i,j) for i in range(2) for j in range(2)]
    # E_ij* E_kl = delta_ik E_jl; Tr(rho E_jl)=rho_lj.
    return [[rho[l][j] if i==k else F(0) for k,l in units] for i,j in units]
def budget(tau=F(1,64),alpha=F(1),positive_reference=True):
    require(positive_reference is True and alpha>0,'positive fixed energy reference required')
    beta=alpha*abs(tau)*F(107,135);delta=alpha/8
    require(beta<delta,'strict smallness is required for GNS gap')
    return beta,delta-beta
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,list):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/g2.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'G1 gate changed')
    psi=[F(3,5),F(4,5)];rho_pure=[[x*y for y in psi] for x in psi];rho_mix=[[F(1,2),F(0)],[F(0),F(1,2)]]
    pure,mixed=gram(rho_pure),gram(rho_mix);rp,rm=rank(pure),rank(mixed)
    require((rp,rm)==(2,4),'pure/mixed GNS ranks wrong')
    diagonal_orbit=[[1,0],[0,0]];restricted_rank=rank(diagonal_orbit)
    H=[F(-1),F(2)];e=min(H);K=[v-e for v in H]
    rows=[]
    for a in (F(1),F(2)):
        for t in (F(0),F(1,64),F(-1,64),F(1,8)):
            b,g=budget(t,a);rows.append({'alpha_over_E_star':a,'tau':t,'beta_over_E_star':b,'gap_lower_over_E_star':g})
    controls={
      'pure_mixed_GNS_not_confused':rp!=rm,
      'reducible_algebra_cyclicity_rejected':rejected(lambda:require(restricted_rank==2,'diagonal algebra orbit does not fill C2')),
      'omit_ground_energy_shift_rejected':rejected(lambda:require(H[0]==0 and min(H)>=0,'unshifted generator fails normalized ground invariance')),
      'correct_shift_positive_with_invariant_ground':K==[F(0),F(3)],
      'threshold_gap_equality_rejected':rejected(lambda:require(F(2)==K[1],'absolute threshold differs from actual gap')),
      'strict_beta_boundary_rejected':rejected(lambda:budget(F(135,856))),
      'zero_reference_rejected':rejected(lambda:budget(positive_reference=False)),
      'signed_tau_preserves_bound':budget(F(1,64))==budget(F(-1,64)),
    }
    require(all(controls.values()),'GNS control failed')
    result={'schema':'ym20-forward-g2-v1','loop':'g2','status':'passed','gap_fixtures':rows,'pure_gram':pure,'mixed_gram':mixed,'pure_gram_rank':rp,'mixed_gram_rank':rm,'restricted_diagonal_orbit_rank':restricted_rank,'controls':controls,'GNS_unitary':'[A] -> A Psi','implementer':'exp(it(H-e)/hbar)','energy_generator':'H-e','default_gap_lower_over_alpha':'973/8640','scope':'full bounded local complete-factor algebra in selected product representation; restricted Gauss algebra not identified'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',contract,gate,ROOT/'research/round20/advisor/e2-gate.json',ROOT/'research/round19/advisor/a2-gate.json',ROOT/'research/round20/forward/g1/report.md']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'g2','pure_rank':rp,'mixed_rank':rm,'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
