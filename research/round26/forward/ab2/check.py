#!/usr/bin/env python3
"""Rational checks supporting the actual Gaussian proof and boundary estimate."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);out=Path(p.parse_args().output);require(not out.exists(),'fresh output')
    cap=F(5,1664);M=7*cap;s=F(4);ratio=(6*M+1/s)/(1-M)
    require(ratio==F(626,1629) and ratio<F(77,200),'actual uniform contraction coefficient')
    require(1-7*M==F(1419,1664),'positive contraction threshold')
    signs=[]
    for tau in (-cap,F(0),cap):
        m=7*abs(tau);r2=F(16,9)*(F(7,12)*tau*tau)**3
        signs.append({'tau':str(tau),'source_norm_squared_upper':str(r2),'residual_norm_squared_upper':str(((6*m+1/s)/(1-m))**2*r2)})
        require((r2==0)==(tau==0),'zero exact source exception')
    # Exact rational spectral-multiplier algebra control. q stands for an actual
    # Gaussian transform value; this does not assign a model spectrum.
    energies=(F(0),F(1),F(1));source=((F(0),F(2),F(0)),(F(2),F(0),F(3)),(F(0),F(3),F(0)))
    retained_equal=F(0)
    for i in range(3):
        for j in range(3):
            omega=energies[i]-energies[j];q=F(1) if omega==0 else F(1,3)
            k=F(0) if omega==0 else (1-q)*source[i][j]/omega
            residual=q*source[i][j]
            require(-omega*k==-source[i][j]+residual,'homological sign')
            if omega==0:retained_equal=max(retained_equal,abs(residual))
    require(retained_equal==3,'zero-frequency source cannot be deleted')
    # Source-degree and duration controls are continuous symbolic inequalities;
    # these endpoints check arithmetic, not a sampled replacement for the proof.
    require((6*M+1)/(1-M)>1,'s=1 conservative certificate fails')
    require(6*M/(1-M)==F(70,543)>0,'nonzero upper-bound floor remains')
    contract=json.loads((ROOT/'research/round26/contracts/ab2.json').read_text());paths=['research/round26/contracts/ab2.json',*contract['bindings'],str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for path,digest in contract['bindings'].items():require(bindings[path]==digest,'dependency binding '+path)
    result={'schema':'ym26-forward-ab2-v1','s':str(s),'full_operator_residual_ratio_upper':str(ratio),'uniform_finite_volume':True,'signs':signs,'kernel':{'normalization':'1 proved by polar Gaussian integral','L1_primitive':'s*sqrt(2/pi)','derivative_total_variation':'sqrt(2/pi)/s','jump':'1','derivative':'delta_0-p_s'},'controls':{'homological_sign':True,'equal_energy_retained':True,'s_one_bound_fails':True,'floor_not_lower_bound':True,'short_time_series_cannot_certify_Gaussian_locality':True,'fixture_not_actual_spectrum':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
