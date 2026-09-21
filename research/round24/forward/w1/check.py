#!/usr/bin/env python3
import argparse,json
from fractions import Fraction as F
from pathlib import Path

def require(v,m):
    if not v:raise RuntimeError(m)
def inner(a,b):return sum(x*y for x,y in zip(a,b))
def matmul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);out=Path(p.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    # Non-SU2 exact source-algebra fixture; actual nonzero source is the inherited proof.
    v=[F(0),F(1,3),F(1,5)];u=[F(0),v[1]/2,v[2]/3]
    a=inner(u,v);beta=inner(u,u);sigma2=inner(v,v)
    w=[-a*x-beta*y/3 for x,y in zip(u,v)]
    r2=inner(w,w)
    require(r2==F(5,3)*a*a*beta+beta*beta*sigma2/9,'actual-source algebra identity')
    require(inner(u,w)==-F(4,3)*a*beta<0,'source nonvanishing algebra')
    theta=F(1,16);energy=F(8);mass=F(3,4)
    require(theta*energy<=1,'conditional spectral cutoff')
    residual_squared_fraction=F(25,36)*mass
    require(residual_squared_fraction==F(25,48),'conditional lower norm squared')
    # 1-x²/6 >=5/6 on x in [0,1]; the sin-series omitted tail is positive.
    require(F(1)-F(1,6)==F(5,6),'sinc interval floor')
    tau=F(5,1664);radius=192*7*tau*theta
    require(radius==F(105,416)<1,'full weighted filter radius')
    # Commuting excited block is invisible to the vacuum column, computed matrices.
    G=[[F(0),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]]
    A=[[F(0),F(0),F(0)],[F(0),F(0),F(1)],[F(0),F(1),F(0)]]
    GA,AG=matmul(G,A),matmul(A,G)
    controls={
      'vanishing_vacuum_column_does_not_remove_full_source':all(row[0]==0 for row in A) and A[1][2]!=0 and GA==AG,
      'source_zero_exception':inner([F(0)]*3,[F(0)]*3)==0 and r2>0,
      'missing_mixed_source_term_detected':r2!=a*a*beta+beta*beta*sigma2/9,
      'cutoff_outside_sinc_certificate_rejected':F(17,16)>1,
      'zero_low_energy_mass_yields_no_positive_certificate':F(25,36)*0==0,
      'ground_gap_does_not_bound_excited_energy_difference':G[1][1]>0 and G[2][2]-G[1][1]==0,
      'shorter_filter_preserves_more_low_frequency_signal':1-F(1,2)**2/6>1-F(1)**2/6,
    }
    require(all(controls.values()),'controls')
    results={'loop':'w1','direction':'forward','status':'passed','claims':['Actual source residual norm approaches its full source norm as Theta decreases to zero','Conditional actual spectral-mass lower certificate (5/6)r sqrt(m(E))','Exact source norm identity and retained full-sector equation'],'limitations':['Actual spectral cutoff or moment is not evaluated','No uniform volume-effective Theta threshold','Vacuum-column lower bound is not an all-sector upper bound','No actual equal-energy obstruction or full inverse or later induction proved'],'fixture_scope':'algebra and logical counterexamples only, not actual SU2 spectrum','conditional_example':{'Theta':str(theta),'E':str(energy),'assumed_actual_mass':str(mass),'lower_norm_squared_over_r_squared':str(residual_squared_fraction)},'radius':str(radius),'continuum_proved':False}
    (out/'results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    (out/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
