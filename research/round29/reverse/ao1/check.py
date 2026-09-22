#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise AssertionError(m)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/ao1.json').read_text())['id']=='AO1','contract')
    cap=F(1,65536);selected=F(1,2)+F(1,8)+F(1,2);kinetic=28*cap/8+2*selected;moment=18+8*kinetic
    need(selected==F(9,8) and kinetic==F(9,4)+F(7,2)*cap,'kinetic dictionary')
    need(moment==36+28*cap and moment<37,'moment ceiling')
    fixtures=[]
    for tau in (-cap,F(0),cap):
     for alpha in (F(1,3),F(1),F(7,2)):
      m2=alpha**2*(36+28*abs(tau));free=9*alpha**2/4
      need(free<=m2<37*alpha**2,'physical scaling')
      fixtures.append({'tau':str(tau),'alpha':str(alpha),'m2_bound':str(m2),'free_m2':str(free)})
    lam=F(1,4);t=lam/3;trial=(3*t*t/4-lam*t/2)/(1+t*t/4)
    need(trial==F(-3,577),'nonzero selected reference')
    cross=[]
    for w in (F(0),F(1,2),F(1)):
      full=5*w*w-2;need(full==3*w*w-2*(1-w*w),'cross term')
      cross.append({'W':str(w),'full':str(full),'dropped':str(3*w*w)})
    S={(0,0,0),(1,0,0),(0,1,0),(0,0,1)};R={(0,0,0),(0,0,1)}
    anchors={tuple(y[i]-s[i] for i in range(3)) for y in R for s in S};orthant={x for x in anchors if min(x)>=0}
    need(len(anchors)==7 and len(orthant)==2,'incidence')
    escaping=[]
    for n in (2,16,256):
      g=F(1,16);weights=[1-F(1,n),F(1,n)];energies=[g,g+F(n,2)]
      m1=sum(w*e for w,e in zip(weights,energies));m2=sum(w*e*e for w,e in zip(weights,energies))
      need(m1==F(9,16) and m2==F(17,256)+F(n,4),'escaping moment')
      escaping.append({'n':n,'m1':str(m1),'m2':str(m2)})
    controls={'reference_energy_not_excited_moment':F(0)!=F(9,4),'selected_potential_budget_nonzero':2*selected>0,'selected_ground_scalar_not_zero':trial<0,'drop_gradient_cross_term':cross[0]['full']!=cross[0]['dropped'],'wrong_half_Pauli_m2_factor16':F(12**2,4)==16*F(9,4),'energy_factor_alpha_squared':F(2)**2*F(9,4)!=2*F(9,4),'first_moment_not_second':F(escaping[-1]['m2'])>37,'origin_not_bulk_incidence':len(orthant)!=len(anchors)}
    need(all(controls.values()),'controls')
    result={'loop':'AO1','direction':'reverse','verdict':'uniform finite physical second moment bound','kinetic_cap':str(kinetic),'moment_cap_in_alpha_squared':str(moment),'exact_bound':'alpha^2(36+28|tau|)','simplified_bound':'37 alpha^2','fixtures':fixtures,'selected_trial_energy':str(trial),'cross_checks':cross,'escaping_tail':escaping,'controls':controls,'scope':'Finite actual-ground states only; no limiting equality/operator-domain assertion.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AO1','passed':True,'controls':len(controls),'moment_cap':str(moment)}))
if __name__=='__main__':main()
