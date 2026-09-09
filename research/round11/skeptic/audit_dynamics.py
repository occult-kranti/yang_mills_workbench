#!/usr/bin/env python3
"""Independent monomial-coordinate RK45 evolution versus orthonormal DOP853."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,sys,copy
import numpy as np
from scipy.integrate import solve_ivp
from audit_solver import load,my_matrices

ap=argparse.ArgumentParser();ap.add_argument('solver_directory',type=Path);args=ap.parse_args();root=args.solver_directory.resolve()
sys.path.insert(0,str(root));m=load(root/'run_study.py','reviewed_dynamic_study')
hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('two_plaquette.py','run_study.py','test_solver.py')}
records=[]
def check(ok,name,detail=None):
    if not ok:raise RuntimeError(name)
    records.append({'test':name,'passed':True,'detail':detail})
def rejects(fn,name):
    try:fn()
    except (ValueError,RuntimeError) as e:records.append({'test':name,'passed':True,'rejection':str(e)});return
    raise RuntimeError('Unexpected acceptance: '+name)
bs,G,K,MX,MY=my_matrices(3,F(1))
flo=lambda A:np.array([[float(x) for x in row] for row in A])
G,K,MX,MY=map(flo,(G,K,MX,MY));V1,V2=G-MX,G-MY;n=len(G)
Gi=np.linalg.inv(G);c0=np.zeros(n+1,dtype=complex);c0[0]=1
def direct_rhs(t,c):
    u=np.pi*t/2;l1=1-np.cos(u);l2=F(3,2)*l1
    dl1=np.pi*np.sin(u)/2;dl2=3*np.pi*np.sin(u)/4
    psi=c[:n];H=K+float(l1)*V1+float(l2)*V2
    return np.r_[-1j*Gi@H@psi,dl1*np.vdot(psi,V1@psi).real+dl2*np.vdot(psi,V2@psi).real]
ts=np.linspace(0,2,161)
sol=solve_ivp(direct_rhs,(0,2),c0,method='RK45',rtol=1e-11,atol=1e-12,t_eval=ts)
check(sol.success and np.all(np.isfinite(sol.y)),'independent_monomial_RK45_complete')
production=m.dop_driver(3,1e-11);check(m.dynamic_acceptance(production,'DOP853'),'DOP853_own_gates')
diff=sol.y[:n,-1]-production['coeff'];error=float(np.sqrt(np.vdot(diff,G@diff).real))
check(error<2e-8,'independent_basis_and_integrator_state',error)
energy=float(np.vdot(sol.y[:n,-1],(K+2*V1+3*V2)@sol.y[:n,-1]).real)
work=float(sol.y[n,-1].real);norm=float(np.vdot(sol.y[:n,-1],G@sol.y[:n,-1]).real)
check(abs(energy-production['final_energy'])<2e-8,'independent_final_energy',abs(energy-production['final_energy']))
check(abs(work-production['final_work'])<2e-8,'independent_integrated_work',abs(work-production['final_work']))
check(abs(energy-work)<2e-8 and abs(norm-1)<2e-9,'independent_work_norm',{'work_defect':energy-work,'norm_defect':norm-1})
mid=m.midpoint_driver(3,160);check(m.dynamic_acceptance(mid,'midpoint'),'midpoint_own_gates')
for method,bad in [('DOP853',m.dop_driver(3,1e-10,True)),('midpoint',m.midpoint_driver(3,80,True))]:
    rejects(lambda:m.dynamic_acceptance(bad,method),'omitted_work_rejected.'+method)
    check(bad['work_max']>1,'omitted_work_is_discriminating.'+method,bad['work_max'])
rejects(lambda:m.dynamic_acceptance(production,'unsupported'),'unknown_method_rejected')
bad=copy.deepcopy(production);bad['rows']=[];rejects(lambda:m.dynamic_acceptance(bad,'DOP853'),'empty_history_rejected')
bad=copy.deepcopy(production);bad['rows'][10]['energy']=float('nan');rejects(lambda:m.dynamic_acceptance(bad,'DOP853'),'transient_nonfinite_energy_rejected')
bad=copy.deepcopy(production);bad['work_max']=0;rejects(lambda:m.dynamic_acceptance(bad,'DOP853'),'dishonest_summary_rejected')
check(hashes=={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in hashes},'dynamic_sources_unchanged')
result={'status':'passed','optimized_python':not __debug__,'gate_count':len(records),'records':records,'reviewed_source_hashes':hashes,
        'independent_method':'Unorthonormalized exact-moment monomial form matrices, generalized Schrodinger equation with RK45; compared against orthonormal DOP853',
        'scope':'Finite D3 time evolution only; no untruncated dynamic error bound.',
        'diagnostics':{'state_difference_Haar_norm':error,'energy':energy,'integrated_work':work,'norm':norm}}
output=Path(__file__).with_name('dynamic_audit_results.json');output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'gate_count':len(records),'state_error':error,'source_hashes':hashes}))
