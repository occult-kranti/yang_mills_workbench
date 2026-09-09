"""Independent finite-matrix, scalar-identity, stability and raw-data audit."""
from pathlib import Path
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import sys
import os
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get("YM9_REVIEW_ROOT",str(HERE.parent))).resolve()
LATTICE=ROOT/("lattice" if (ROOT/"lattice").exists() else "ym9-lattice")
checks=[]


def gate(name, condition, **evidence):
    checks.append({'name':name,'passed':bool(condition),**evidence})


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    path=ROOT/'stability.py' if (ROOT/'stability.py').exists() else ROOT/'physics-observatory/research/round9/stability.py'
    initial=digest(path)
    spec=importlib.util.spec_from_file_location('independent_stability',path)
    S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    # Independent eigenvalue calculation on held-out sizes and parameters.
    markov=[]
    for n in [3,7,19,77]:
        c,delta=.31,.17
        v=np.zeros(n);v[0]=1/math.sqrt(2);v[1]=-1/math.sqrt(2)
        B=np.eye(n);B[:2,:2]=.5
        P0=(1-c)*B+c*np.ones((n,n))/n
        P1=P0+delta*np.outer(v,v)
        D=P1-P0
        eig0=np.linalg.eigvalsh(P0);eig1=np.linalg.eigvalsh(P1)
        op=float(np.linalg.svd(D,compute_uv=False)[0])
        l1=float(np.abs(n*D).mean())
        schur=float(np.max(np.abs(D).sum(axis=1)))
        gate(f'counterexample_PSD_stochastic_positive_n{n}',
            eig0.min()>-2e-14 and eig1.min()>-2e-14 and P0.min()>0 and P1.min()>0
            and np.max(abs(P0.sum(axis=1)-1))<2e-14 and np.max(abs(P1.sum(axis=1)-1))<2e-14)
        gate(f'counterexample_independent_SVD_n{n}',abs(op-delta)<2e-14 and abs(schur-delta)<2e-14 and abs(l1-2*delta/n)<2e-14)
        gate(f'product_L1_does_not_bound_operator_n{n}',op>l1)
        markov.append({'n':n,'operator_norm':op,'product_L1':l1,'Schur_row_bound':schur,'P0_min_eigenvalue':float(eig0.min())})

    # Exact center-supported false measure, independent of advisor code.
    scalar=sum(Fraction(-3)*Fraction(17,10)*u/Fraction(2) for u in [1,-1])
    full=sum(Fraction(u*u,4) for u in [1,-1])
    gate('center_measure_passes_scalar_Ward_exact',scalar==0)
    gate('center_measure_fails_inserted_SD_exact',full==Fraction(1,2))
    # Verify the stated inserted derivative directly through matrix group curves.
    eps=1e-4
    residual=[]
    for sign in [1,-1]:
        # U(t)=sign*(cos(t/2) I+i sin(t/2) sigma_a); f=u0*u_a.
        fp=sign*math.cos(eps/2)*sign*math.sin(eps/2)
        fm=sign*math.cos(eps/2)*sign*math.sin(-eps/2)
        residual.append((fp-fm)/(2*eps))
    gate('center_inserted_SD_matrix_curve_derivative',abs(np.mean(residual)-.5)<1e-8)

    stability=[]
    for a,mass,epsilon in [(0.19,1.3,.017),(.031,2.7,.002),(1e-10,1.,2e-11),(1e-100,1.,2e-101),(1e-200,1.,2e-201),(100.,1.,.2)]:
        with localcontext() as ctx:
            ctx.prec=260
            da,dm,de=map(Decimal.from_float,[a,mass,epsilon])
            reference=-((-da*dm).exp()+de).ln()/da
        value=S.lower_gap(a,mass,epsilon)
        error=abs(value-float(reference))/max(1.,abs(float(reference)))
        gate(f'stability_Decimal260_a{a}_m{mass}',error<3e-15,scaled_error=error)
        stability.append({'a':a,'mass':mass,'epsilon':epsilon,'value':value,'reference':str(reference),'scaled_error':error})
    for a in [.2,.1,.05,.025]:
        n=round(1/a)
        for power in [1,2]:
            epsilon=.2*a**power
            q=math.exp(-a);r=q+epsilon
            # Closed scalar powers, independent of production matrix_power.
            actual=abs(math.exp(n*math.log(r))-math.exp(-n*a))
            gate(f'stability_telescoping_scalar_a{a}_power{power}',actual<=n*epsilon+1e-15)
    gate('SU2_strong_coupling_normalization_exact',Fraction(4,16*(4-1))==Fraction(1,12))

    # Recompute chain diagnostics from saved raw measurements without production
    # series_summary. np.correlate supplies an independent autocorrelation path.
    results=LATTICE/'results'
    data=json.loads((results/'all_diagnostics.json').read_text())
    manifest=json.loads((results/'experiment_manifest.json').read_text())
    gate('six_predeclared_chains_present',len(data['chains'])==6)
    summaries=[]
    for chain in data['chains']:
        csv_path=results/chain['raw_csv']
        raw=np.genfromtxt(csv_path,delimiter=',',names=True)
        tag=f"beta{chain['beta']}_{chain['start']}"
        gate(tag+'_2048_finite_raw_rows',len(raw)==2048 and all(np.isfinite(raw[n]).all() for n in raw.dtype.names))
        gate(tag+'_acceptance_range',np.all((raw['acceptance']>=0)&(raw['acceptance']<=1)))
        for label,col in [('plaquette','plaquette_mean'),('plaquette_square','plaquette_square_mean'),('ward','ward_mean')]:
            x=raw[col];n=len(x);mean=float(np.mean(x))
            for batch in [16,32,64]:
                nb=n//batch
                bm=np.array([np.mean(x[i*batch:(i+1)*batch]) for i in range(nb)])
                se=float(np.sqrt(np.sum((bm-bm.mean())**2)/(nb*(nb-1))))
                row=chain['statistics'][label][str(batch)]
                gate(tag+f'_{label}_batch{batch}_mean_se',abs(mean-row['mean'])<1e-13 and abs(se-row['se'])<1e-13)
            row=chain['statistics'][label]['64']
            centered=x-mean
            if np.var(x)==0:
                gate(tag+'_'+label+'_degenerate_flag',row['status']=='degenerate')
                continue
            cov=np.correlate(centered,centered,mode='full')[n-1:]
            cov=cov/np.arange(n,0,-1)
            rho=cov/cov[0]
            tau=.5
            for k in range(1,min(n//2,512),2):
                pair=rho[k]+rho[k+1]
                if pair<=0:break
                tau+=pair
            expected='usable' if n//64>=20 and tau<=64/5 else 'insufficient'
            gate(tag+'_'+label+'_autocorrelation_and_status',abs(tau-row['tau_int'])<2e-12 and row['status']==expected,tau=float(tau),status=expected)
            summaries.append({'chain':tag,'observable':label,'tau':float(tau),'status':expected,'mean':mean,'se64':row['se']})
        gate(tag+'_raw_hash_matches_manifest',manifest['output_sha256'][csv_path.name]==digest(csv_path))
    high=[r for r in summaries if r['chain'].startswith('beta2.2') and r['observable']=='plaquette']
    gate('both_high_beta_plaquette_flags_retained',len(high)==2 and all(r['status']=='insufficient' for r in high))
    cmp=next(c for c in data['hot_cold_comparisons'] if c['beta']==2.2)
    gate('high_beta_hot_cold_not_promoted',cmp['comparison']['status']=='insufficient')
    gate('simulation_source_hashes_stable_during_actual_run',manifest['source_sha256_before']==manifest['source_sha256_after'])
    gate('stability_source_stable_during_audit',digest(path)==initial)
    report={'scope':'Independent finite-matrix and raw-data audit; handwritten H3 proof reviewed separately, no formal proof-kernel verification',
            'passed':bool(checks) and all(r['passed'] for r in checks),'count':len(checks),
            'checks':checks,'failures':[r for r in checks if not r['passed']],
            'stability_source_sha256':initial,'counterexample_records':markov,
            'stability_reference_records':stability,'raw_summary_records':summaries,
            'script_sha256':digest(Path(__file__))}
    (HERE/'theorems_and_data_audit.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    print(json.dumps({k:report[k] for k in ['passed','count','failures']},indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
