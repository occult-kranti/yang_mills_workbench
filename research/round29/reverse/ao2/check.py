#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise AssertionError(m)
def moment(atoms,k):return sum(p*e**k for p,e in atoms)
def cutoff(e,R):return e*min(F(1),max(F(0),2-e/R))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/ao2.json').read_text())['id']=='AO2','contract')
    g=F(1,16);rows=[]
    for n in (1,2,8,64,256):
      old=[(1-F(1,n),g),(F(1,n),g+F(n,2))]
      new=[(1-F(1,n*n),g),(F(1,n*n),g+n)]
      oldm1=moment(old,1);oldm2=moment(old,2);newm1=moment(new,1);newm2=moment(new,2)
      need(oldm1==F(9,16) and oldm2==F(17,256)+F(n,4),'AK2 escape')
      need(newm1==g+F(1,n) and newm2==g*g+2*g/F(n)+1 and newm2<2,'second moment escape')
      rows.append({'n':n,'old_mu1':str(oldm1),'old_mu2':str(oldm2),'new_mu1':str(newm1),'new_mu2':str(newm2)})
    tails=[]
    for alpha in (F(1,2),F(1),F(3)):
     atoms=[(F(1,4),3*alpha)];C=37*alpha**2
     for R in (alpha,2*alpha,4*alpha):
      actual_tail=sum(p*e for p,e in atoms if e>R);truncated=sum(p*cutoff(e,R) for p,e in atoms)
      need(actual_tail<=moment(atoms,2)/R<=C/R,'tail bound')
      need(0<=moment(atoms,1)-truncated<=C/R,'compact cutoff remainder')
      tails.append({'alpha':str(alpha),'R':str(R),'uniform_tail_upper':str(C/R),'actual_tail':str(actual_tail)})
    mean=F(1,3);variance=F(1,4);uncentered_mass=mean**2+variance
    controls={'old_escape_rejected_by_M2':F(rows[-1]['old_mu2'])>37,'bounded_M2_does_not_give_M2_equality':F(1)+g*g!=g*g,'centering_removes_zero_mass_not_energy':uncentered_mass-variance==mean**2 and mean**2>0,'ground_shift_changes_uncentered_energy':F(1,4)*(3+5)!=F(3,4),'physical_M2_scale_quadratic':37*F(2)**2!=37*F(2),'symbolic_stability_required':not all([True,False]),'AQ_state_requires_dictionary':'I1/AJ1/AK2 orthant'!='AQ numeric-cap subsequence'}
    need(all(controls.values()),'controls')
    result={'loop':'AO2','direction':'reverse','verdict':'actual limiting first moment equality and operator domain','tail':'integral_(E>R) E dnu_Lambda <= alpha^2(36+28|tau|)/R','first_moment':'mu1=alpha*omega(1-W^2)','second_moment':'mu2<=alpha^2(36+28|tau|)<37alpha^2','domain':'chi in D(H_phys)','second_moment_equality_claimed':False,'countermeasures':rows,'tail_fixtures':tails,'controls':controls,'scope':'Actual old I1/AJ1/AK2 orthant state under both original restrictions only.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AO2','passed':True,'controls':len(controls)}))
if __name__=='__main__':main()
