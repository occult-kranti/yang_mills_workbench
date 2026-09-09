"""Bounded numerical diagnostics accompanying exact analytic drive certificates."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import sys,json,csv,hashlib,time
import numpy as np
import scipy
from scipy.linalg import cholesky,solve_triangular,eigh
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import drive_bound as db
from vendor import two_plaquette as tp

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output';GATES=[]
def gate(name,passed,detail=None):
    GATES.append({'name':name,'passed':bool(passed),'detail':detail})
    if not passed:raise RuntimeError('failed gate: '+name)
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def write_csv(name,rows):
    if not rows:raise ValueError('nonempty CSV required')
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def source_hashes():
    return {**db.source_hashes(),**{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('run_study.py','test_solver.py','exact_stepper.py')}}

@lru_cache(None)
def orthogonal(degree,alpha=F(1),rho=F(1)):
    bs,G,K,X,Y=tp.matrices(degree,rho);Gf=tp.floating(G);L=cholesky(Gf,lower=True)
    def transform(M):
        T=solve_triangular(L,tp.floating(M),lower=True)
        return solve_triangular(L,T.T,lower=True).T
    Kf=float(alpha)*transform(K);Xf=transform(X);Yf=transform(Y)
    metric=transform(G)
    return {'K':Kf,'X':Xf,'Y':Yf,'L':L,'G':Gf,'dimension':len(bs),'Gram_condition':float(np.linalg.cond(Gf)),'metric_transform_defect':float(np.linalg.norm(metric-np.eye(len(bs)),ord=2))}

def coefficients(protocol,t):
    p=db.canonical_protocol(protocol);T=float(db.duration(p))
    if p['kind']=='piecewise_constant':
        elapsed=0.
        for seg in p['segments']:
            elapsed+=float(F(seg['duration']))
            if t<elapsed or elapsed>=T:return float(F(seg['lambda1'])),float(F(seg['lambda2'])),0.,0.
    s1,s2=float(F(p['lambda1_scale'])),float(F(p['lambda2_scale']))
    if p['kind']=='constant':return s1,s2,0.,0.
    if T==0:return 0.,0.,0.,0.
    u=np.pi*t/T;shape=1-np.cos(u);rate=np.pi/T*np.sin(u)
    return s1*shape,s2*shape,s1*rate,s2*rate

def evolve(protocol,degree,tolerance=1e-11,points=41):
    p=db.canonical_protocol(protocol);T=float(db.duration(p));m=orthogonal(degree);n=m['dimension'];K,X,Y,L=(m[k] for k in ('K','X','Y','L'))
    initial=L.T[:,0].astype(complex);ts=np.linspace(0,T,points)
    if p['kind']=='piecewise_constant':raise ValueError('numerical study intentionally uses smooth ramps; theorem permits steps')
    def rhs(t,state):
        l1,l2,d1,d2=coefficients(p,t);psi=state[:n]
        work=d1*np.vdot(psi,psi-X@psi).real+d2*np.vdot(psi,psi-Y@psi).real
        return np.r_[-1j*(K@psi-l1*(X@psi)-l2*(Y@psi)),work]
    if T==0:states=np.repeat(np.r_[initial,0j][:,None],points,axis=1)
    else:
        result=solve_ivp(rhs,(0,T),np.r_[initial,0j],method='DOP853',rtol=tolerance,atol=tolerance/10,t_eval=ts)
        if not result.success:raise RuntimeError(result.message)
        states=result.y
    if not np.all(np.isfinite(states)):raise ValueError('nonfinite numerical state')
    records=[];e_initial=0.
    for i,t in enumerate(ts):
        psi=states[:n,i];l1,l2,_,_=coefficients(p,t);norm=np.vdot(psi,psi).real
        energy=np.vdot(psi,K@psi-l1*(X@psi)-l2*(Y@psi)).real+(l1+l2)*norm
        if i==0:e_initial=energy
        work=states[n,i].real
        records.append({'t':float(t),'energy':float(energy),'integrated_work':float(work),'work_defect':float(energy-e_initial-work),'norm_defect':float(norm-1)})
    if not all(np.isfinite(v) for row in records for v in row.values()):raise ValueError('nonfinite derived diagnostics')
    coeff=solve_triangular(L.T,states[:n],lower=False)
    return {'state_phase_convention':'common-scalar-potential-phase-removed','protocol':p,'degree':degree,'dimension':n,'tolerance':tolerance,'rows':records,'states':states[:n],'coefficients':coeff,'max_norm_defect':max(abs(r['norm_defect']) for r in records),'max_work_defect':max(abs(r['work_defect']) for r in records),'Gram_condition':m['Gram_condition'],'metric_transform_defect':m['metric_transform_defect']}

def numerical_gate(result):
    if not result['rows'] or not np.all(np.isfinite(result['states'])):raise ValueError('complete state/history required')
    if not all(np.isfinite(v) for r in result['rows'] for v in r.values()):raise ValueError('finite complete diagnostics required')
    for key,column in (('max_norm_defect','norm_defect'),('max_work_defect','work_defect')):
        if result[key]!=max(abs(r[column]) for r in result['rows']):raise ValueError('raw/summary mismatch')
    if result['max_norm_defect']>1e-8 or result['max_work_defect']>1e-8:raise ValueError('numerical norm/work diagnostic failed')
    return True

def state_difference(left,right):
    for result in (left,right):
        if result.get('state_phase_convention')!='common-scalar-potential-phase-removed':raise ValueError('known common phase convention required')
        if not result.get('rows') or len(result['rows'])!=result['states'].shape[1] or result['states'].shape[0]!=result['dimension'] or result['coefficients'].shape!=result['states'].shape:raise ValueError('complete compatible state/row shapes required')
        if any(not np.isfinite(row['t']) for row in result['rows']):raise ValueError('finite time grid required')
    if [r['t'] for r in left['rows']]!=[r['t'] for r in right['rows']]:raise ValueError('matched sample times required')
    if db.canonical_protocol(left['protocol'])!=db.canonical_protocol(right['protocol']):raise ValueError('matched protocol required')
    if left['degree']>right['degree']:left,right=right,left
    big=orthogonal(right['degree']);embedding=big['L'].T[:,:left['dimension']]@left['coefficients']
    diff=embedding-right['states'];out=np.linalg.norm(diff,axis=0)
    if not np.all(np.isfinite(out)):raise ValueError('nonfinite comparison norm')
    return out

def midpoint(protocol,degree,steps):
    if type(steps) is not int or steps<=0:raise ValueError('positive step count required')
    p=db.canonical_protocol(protocol)
    if p['kind']=='piecewise_constant':raise ValueError('midpoint oracle restricted to smooth or constant protocols')
    T=float(db.duration(p));m=orthogonal(degree);K,X,Y,L=(m[k] for k in ('K','X','Y','L'));psi=L.T[:,0].astype(complex);h=T/steps;work=0.;rows=[]
    def expectations(t,state):
        l1,l2,d1,d2=coefficients(p,t);norm=np.vdot(state,state).real
        energy=np.vdot(state,K@state-l1*(X@state)-l2*(Y@state)).real+(l1+l2)*norm
        rate=d1*np.vdot(state,state-X@state).real+d2*np.vdot(state,state-Y@state).real
        return float(energy),float(rate)
    initial_energy=expectations(0,psi)[0]
    for k in range(steps):
        t=k*h;l1,l2,_,_=coefficients(p,t+h/2);ev,U=eigh(K-l1*X-l2*Y);a=U.conj().T@psi
        middle=U@(np.exp(-.5j*h*ev)*a);end=U@(np.exp(-1j*h*ev)*a)
        work+=h/6*(expectations(t,psi)[1]+4*expectations(t+h/2,middle)[1]+expectations(t+h,end)[1]);psi=end
        if not np.all(np.isfinite(psi)):raise ValueError('nonfinite midpoint state')
        energy=expectations(t+h,psi)[0];rows.append({'steps':steps,'t':t+h,'energy':energy,'integrated_work':work,'norm_defect':float(np.vdot(psi,psi).real-1),'work_defect':energy-initial_energy-work})
    if not all(np.isfinite(v) for row in rows for v in row.values()):raise ValueError('nonfinite midpoint history')
    normmax=max(abs(row['norm_defect']) for row in rows);workmax=max(abs(row['work_defect']) for row in rows)
    if normmax>1e-8 or workmax>2e-4:raise ValueError('midpoint own norm/work gate failed')
    return {'state_phase_convention':'common-scalar-potential-phase-removed','state':psi,'rows':rows,'max_norm_defect':normmax,'max_work_defect':workmax}

def main():
    OUT.mkdir(exist_ok=True);GATES.clear();hashes=source_hashes();save('validation.json',{'status':'running','source_hashes':hashes});start=time.time()
    try:
        cases=[('original',{'kind':'cosine_ramp','duration':'2','lambda1_scale':'1','lambda2_scale':'3/2'}),('reduced',{'kind':'cosine_ramp','duration':'2','lambda1_scale':'1/10','lambda2_scale':'3/20'}),('short',{'kind':'cosine_ramp','duration':'1/5','lambda1_scale':'1','lambda2_scale':'3/2'}),('slow',{'kind':'cosine_ramp','duration':'4','lambda1_scale':'1/20','lambda2_scale':'3/40'})]
        certificates=[];summary=[];curves=[];histories=[];reference_records={};all_runs={}
        for name,p in cases:
            runs={d:evolve(p,d) for d in (3,4,5,6)};all_runs[name]=runs;ref=runs[6]
            for d,r in runs.items():
                gate(name+' D'+str(d)+' finite norm/work',numerical_gate(r))
                histories.extend(dict(case=name,degree=d,**row) for row in r['rows'])
            refdiff=state_difference(runs[5],ref)
            reference_records[name]={'reference_degree':6,'D5_D6_final_difference':float(refdiff[-1]),'D5_D6_max_difference':float(max(refdiff)),'status':'numerical-reference-refinement-diagnostic'}
            for d in (3,4):
                cert=db.certificate(p,d);gate(name+' D'+str(d)+' exact analytic certificate',db.verify_certificate(cert));certificates.append(dict(case=name,certificate=cert))
                error=state_difference(runs[d],ref);r=runs[d]
                summary.append({'case':name,'degree':d,'dimension':r['dimension'],'duration':str(db.duration(p)),'action_endpoint':cert['action_interval'][1],'analytic_state_error_upper':cert['state_error_upper'],'bound_below_two':cert['bound_is_below_trivial_two'],'empirical_final_D6_difference':float(error[-1]),'empirical_max_D6_difference':float(max(error)),'D5_D6_final_difference':float(refdiff[-1]),'Gram_condition':r['Gram_condition'],'metric_transform_defect':r['metric_transform_defect'],'max_norm_defect':r['max_norm_defect'],'max_work_defect':r['max_work_defect'],'time_step_error_certified':False})
                for i,err in enumerate(error):
                    t=db.duration(p)*F(i,len(error)-1);lo,hi=db.action_interval(p,t);bound=db.factorial_bound(hi,d)
                    curves.append({'case':name,'degree':d,'time':str(t),'time_float':float(t),'action_lower':str(lo),'action_upper':str(hi),'analytic_error_upper':str(bound),'analytic_error_upper_float':float(bound),'empirical_D6_difference':float(err)})
                # Exact triangle bound applies to both Galerkin levels; comparison remains floating.
                pair_bound=float(F(cert['state_error_upper'])+db.factorial_bound(db.action_interval(p)[1],6))
                gate(name+' D'+str(d)+' numerical comparison consistent with analytic pair bound',error[-1]<=pair_bound+1e-8,{'difference':float(error[-1]),'pair_bound':pair_bound,'floating_slack':1e-8})
        reduced=dict(cases)['reduced'];tight=all_runs['reduced'][4];coarse=evolve(reduced,4,1e-9);gate('coarser tolerance own norm/work',numerical_gate(coarse));time_error=float(state_difference(coarse,tight)[-1]);gate('DOP tolerance diagnostic',time_error<1e-7,time_error)
        midpoints=[midpoint(reduced,4,n) for n in (80,160,320)]
        midpoint_errors=[float(np.linalg.norm(m['state']-tight['states'][:,-1])) for m in midpoints]
        for n,m in zip((80,160,320),midpoints):gate('midpoint '+str(n)+' own norm/work',m['max_norm_defect']<=1e-8 and m['max_work_defect']<=2e-4)
        write_csv('midpoint_histories.csv',[row for m in midpoints for row in m['rows']])
        orders=[float(np.log2(midpoint_errors[i]/midpoint_errors[i+1])) for i in range(2)]
        gate('independent midpoint diagnostic convergence',all(1.7<x<2.3 for x in orders) and midpoint_errors[-1]<1e-5,{'state_errors':midpoint_errors,'orders':orders})
        write_csv('comparison_summary.csv',summary);write_csv('bound_curves.csv',curves);write_csv('numerical_histories.csv',histories)
        save('analytic_certificates.json',{'contract':db.CONTRACT,'scope':db.SCOPE,'cases':certificates})
        save('numerical_comparisons.json',{'reference_refinement':reference_records,'DOP_tolerance_difference':time_error,'midpoint_steps':[80,160,320],'midpoint_errors':midpoint_errors,'midpoint_orders':orders,'midpoint_norm_max':[m['max_norm_defect'] for m in midpoints],'midpoint_work_max':[m['max_work_defect'] for m in midpoints],'state_phase_convention':'common-scalar-potential-phase-removed','status':'floating-diagnostics-not-certified-time-stepping-or-quadrature','coefficient_conditioning':'Gram condition numbers and metric defects are diagnostics, not rounding-error bounds'})
        fig,axs=plt.subplots(1,2,figsize=(11,4.4))
        for d in (3,4):
            sub=[r for r in curves if r['case']=='reduced' and r['degree']==d]
            axs[0].semilogy([r['time_float'] for r in sub[1:]],[r['analytic_error_upper_float'] for r in sub[1:]],label='D'+str(d)+' analytic bound')
            axs[0].semilogy([r['time_float'] for r in sub[1:]],[max(r['empirical_D6_difference'],1e-16) for r in sub[1:]],'--',label='D'+str(d)+' numerical difference')
        axs[0].set(xlabel='Time',ylabel='Haar L² state distance',title='Reduced ramp: exact bound and diagnostics');axs[0].legend(fontsize=8)
        names=['reduced','short','slow'];x=np.arange(3)
        for d,shift in ((3,-.14),(4,.14)):
            rows=[next(r for r in summary if r['case']==name and r['degree']==d) for name in names]
            axs[1].semilogy(x+shift,[float(F(r['analytic_state_error_upper'])) for r in rows],'o-',label='D'+str(d)+' common bound')
            axs[1].semilogy(x+shift,[r['empirical_final_D6_difference'] for r in rows],'x--',label='D'+str(d)+' numerical difference')
        axs[1].set_xticks(x,names);axs[1].set(ylabel='Final Haar L² state distance',title='Same accumulated action A=1/2');axs[1].legend(fontsize=8)
        fig.text(.5,.015,'Analytic bounds exclude time stepping and roundoff; early numerical differences can exceed them.',ha='center',fontsize=9)
        fig.tight_layout(rect=(0,.055,1,1))
        for ext in ('png','svg'):fig.savefig(OUT/('driven_truncation_bounds.'+ext),dpi=170)
        plt.close(fig)
        gate('frozen complete source set',hashes==source_hashes())
        result={'status':'passed','contract':db.CONTRACT,'scope':db.SCOPE,'source_hashes':hashes,'optimized_python':not __debug__,'gates':GATES,'elapsed_seconds':time.time()-start,'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'limits':['The analytic certificate compares exact states in the finite graph Hilbert space.','Floating integration, matrix exponentials and coefficient conditioning errors remain uncertified.','Reference-degree comparisons and work checks are numerical diagnostics.','No increasing-volume or continuum Yang-Mills conclusion.']}
        save('validation.json',result);print(json.dumps(result,indent=2))
    except Exception as exc:
        save('validation.json',{'status':'failed','source_hashes':hashes,'gates':GATES,'error':str(exc)});raise
if __name__=='__main__':main()
