#!/usr/bin/env python3
"""AL2 reverse: exact eligibility tests, not an evaluated I1 theorem radius."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def demand(p,m):
    if not p: raise AssertionError(m)
def pos(v):
    if isinstance(v,bool) or F(v)<=0:raise ValueError('strictly positive scale required')
    return F(v)
def eligibility(g2,s,c1,c2):
    g2=pos(g2);c1=pos(c1);c2=pos(c2);s=F(s)
    if s<0:raise ValueError('positive-branch deformation only')
    r=4*s/(g2*g2);eps=168*r
    original=(r<=F(1,2),r<=F(1,8),eps<c1,c2*eps<F(1,2))
    caps=(s<=g2*g2/32,s<c1*g2*g2/672,s<g2*g2/(1344*c2))
    demand(all(original)==all(caps),'independent capped versus direct test')
    return {'eligible':all(original),'r':str(r),'tau':str(24*r),'epsilon':str(eps),'original_hypotheses':original,'reduced_caps':caps}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    demand(json.loads((BASE/'inputs/research/round29/contracts/al2.json').read_text())['id']=='AL2','contract')
    fixtures=[]
    # Deliberately synthetic source constants test algebra, never certify actual I1 constants.
    for g2,s,c1,c2,label in [(1,F(1,32),100,F(1,100),'bridge equality'),(1,F(1,672),1,F(1,100),'first omitted strict boundary'),(1,F(1,1344),100,1,'second omitted strict boundary'),(1,0,1,1,'zero'),(F(1,2),F(1,100000),1,1,'interior'),(1,F(1,16),100,F(1,100),'bridge violated')]:
      result=eligibility(g2,s,c1,c2);result['label']=label;fixtures.append(result)
    demand(fixtures[0]['eligible'] and not fixtures[1]['eligible'] and not fixtures[2]['eligible'] and fixtures[3]['eligible'] and fixtures[4]['eligible'] and not fixtures[5]['eligible'],'fixture outcomes')
    invariance=[]
    for q in (F(1,7),F(1),F(9)):
      alpha,lam=F(3),F(2);delta=alpha/8
      demand((q*lam)/(q*alpha)==lam/alpha,'ratio invariant')
      demand(21*q*lam/(q*delta)==21*lam/delta,'local norm invariant')
      # Two exact eigenvalues: qH+bI gaps scale by q, b alone cancels.
      e0,e1,b=F(-2),F(5),F(13)
      demand((q*e1+b)-(q*e0+b)==q*(e1-e0),'gap scalar check')
      t,hbar=F(2),F(3)
      demand((q*delta)*(t/q)/hbar==delta*t/hbar,'explicit reciprocal clock')
      invariance.append({'q':str(q),'ratio':str(lam/alpha),'physical_gap_scale':str(q),'physical_time_scale':str(1/q)})
    invalid=0
    for f in [lambda:pos(0),lambda:pos(-1),lambda:eligibility(1,-1,1,1),lambda:eligibility(0,0,1,1)]:
      try:f()
      except ValueError:invalid+=1
    demand(invalid==4,'invalid scale/deformation rejection')
    controls={'magnetic_only_changes_ratio': F(2)*F(2)/3!=F(2)/3,'first_strict_boundary_rejected':not fixtures[1]['eligible'],'second_strict_boundary_rejected':not fixtures[2]['eligible'],'scalar_does_not_change_gap':(F(5)+13)-(-F(2)+13)==7,'fixed_clock_rescaling_changes_u':F(9)*F(3)/8*2/3!=F(3)/8*2/3,'omitting_bridge_false_accept':fixtures[5]['original_hypotheses'][0] and not fixtures[5]['original_hypotheses'][1]}
    demand(all(controls.values()),'control outcomes')
    result={'loop':'AL2','direction':'reverse','verdict':'iff sufficient-domain membership derived; suppression is action deformation','formula':['0<=s<=g^4/32','s<c1(S)g^4/672','s<g^4/(1344c2(S))'],'fixtures_use_synthetic_constants_only':True,'fixtures':fixtures,'common_rescaling':invariance,'controls':controls,'invalid_rejections':invalid,'physical_scope':'Sufficient I1 eligibility only; no actual I1 constants evaluated, no continuum construction.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(p for p in (BASE/'inputs').rglob('*') if p.is_file())
    h=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n')
    print(json.dumps({'loop':'AL2','passed':True,'controls':len(controls),'invalid_rejections':invalid}))
if __name__=='__main__':main()
