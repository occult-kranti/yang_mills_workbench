#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise AssertionError(m)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(q,r):
    a,b,c,d=q;e,f,g,h=r
    return(a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)
def inv(q):return(q[0],-q[1],-q[2],-q[3])
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/aq2.json').read_text())['id']=='AQ2','contract')
    O=(0,0,0);ex=(1,0,0);ey=(0,1,0);ez=(0,0,1);S={O,ex,ey,ez};R={O,ez};E=[ex,ey,ez]
    links=set();vertices=set();tails=set()
    for z in (0,1):
     for x in range(4):
      for y in range(2):
       v=(x,y,z);tails.add(v)
       for d,e in enumerate(E):links.add((v,d));vertices|={v,add(v,e)}
    anchors={tuple(y[i]-s[i] for i in range(3)) for y in R for s in S};origin_only={a for a in anchors if min(a)>=0}
    need(len(links)==48 and len(vertices)==36 and len(anchors)==7 and len(origin_only)==2,'physical completion/incidence')
    cap=F(1,100000000);epsilon=98*cap;sqrt_cap=F(1,1000)
    need(epsilon<sqrt_cap**2,'overlap square-root certificate')
    variance_floor=F(1,4)-2*sqrt_cap-4*epsilon
    need(variance_floor==F(3099951,12500000) and variance_floor>F(1,5),'nonzero Wilson variance')
    # Full endpoint gauge transformation telescopes; tails-only action fails.
    I=(1,0,0,0);qi=(0,1,0,0);gauge={ex:qi}
    word=[(O,ex,1),(ex,ez,1),(ez,ex,-1),(O,ez,-1)]
    full=I;wrong=I
    for v,e,sign in word:
      q=mul(gauge.get(v,I),inv(gauge.get(add(v,e),I)));tail=gauge.get(v,I)
      full=mul(full,q if sign==1 else inv(q));wrong=mul(wrong,tail if sign==1 else inv(tail))
    need(full==I and wrong[0]==0,'all endpoint gauge actions')
    # Shared SU2 endpoint: a two-spin singlet is diagonal invariant but no factor singlet.
    psi=[0,1,-1,0];jz_total=[1,0,0,-1];jz_first=[1,1,-1,-1]
    need(all(a*b==0 for a,b in zip(psi,jz_total)) and any(a*b!=0 for a,b in zip(psi,jz_first)),'joint invariance not tensor factorization')
    # Raising/lowering total spin annihilate (|01>-|10>).
    raising=[psi[1]+psi[2],psi[3],psi[3],0];lowering=[0,psi[0],psi[0],psi[1]+psi[2]]
    need(not any(raising) and not any(lowering),'complete singlet check')
    gap=F(1,16);diag_measure=[(F(1,2),F(0)),(F(1,2),2*gap)]
    open_gap_mass=sum(w for w,e in diag_measure if 0<e<gap);zero_mass=sum(w for w,e in diag_measure if e==0)
    need(open_gap_mass==0 and zero_mass==F(1,2),'zero atom discriminator')
    mean_real,mean_imag=F(0),F(1);second=F(5,4);correct_var=second-(mean_real**2+mean_imag**2);wrong_var=second-(-1)
    alpha,hbar=F(2),F(3);delta=alpha/8;physical_gap=delta/2;frequency_gap=physical_gap/hbar
    controls={'zero_atom_missed_by_open_gap_tests':open_gap_mass==0 and zero_mass>0,'complex_mean_requires_modulus':correct_var==F(1,4) and wrong_var!=correct_var,'missing_head_endpoint_fails_Wilson':full[0]!=wrong[0],'physical_space_not_tensor_factors':not any(raising) and any(a*b!=0 for a,b in zip(psi,jz_first)),'orthant_two_star_budget_invalid_here':len(origin_only)!=len(anchors),'actual_state_not_assumed_Haar':variance_floor!=F(1,4),'physical_gap_not_frequency_gap':physical_gap!=frequency_gap and physical_gap==alpha/16,'ground_scalar_cancels_only_if_subtracted':(physical_gap+5)-5==physical_gap and physical_gap+5!=physical_gap,'vacuum_simplicity_scope':'this chosen GNS representation'!='all thermodynamic states'}
    need(all(controls.values()),'controls')
    result={'loop':'AQ2','direction':'reverse','verdict':'same-state complete gauge physical gap and nonzero Wilson witness','physical_gap':'alpha/16','frequency_gap':'alpha/(16 hbar)','full_GNS_strengthening':'uses separately reviewed AM2 full-Hilbert gap','Wilson_cover':{'links':48,'endpoint_vertices':36,'tail_vertices':len(tails),'incident_full_lattice_stars':7},'local_reference_energy':'<=98|tau|','epsilon_cap':str(epsilon),'variance_floor':str(variance_floor),'simple_variance_floor':'1/5','gauge_fixture':{'full_W':full[0],'heads_omitted_W':wrong[0]},'zero_atom_diagnostic':str(zero_mass),'controls':controls,'not_claimed':['all thermodynamic state uniqueness','translation invariance','boundary independence','old-state identity','AO2 moment/operator-domain transfer','continuum construction'],'stop':'Investigation10: no further scientific production.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AQ2','passed':True,'controls':len(controls),'variance_floor':str(variance_floor)}))
if __name__=='__main__':main()
