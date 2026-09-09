"""Bounded reproducible two-plaquette study; all paths relative to this file."""
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib,json,sys,time
import numpy as np
import scipy
from scipy.linalg import cholesky,solve_triangular,eigh,expm
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import two_plaquette as tp

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output'
GATES=[]
def gate(name,passed,detail=None):
    GATES.append({'name':name,'passed':bool(passed),'detail':detail})
    if not passed: raise RuntimeError('acceptance gate failed: '+name)
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def write_csv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def hash_file(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def orthogonal_matrices(degree,rho=1):
    bs,G,K,MX,MY=tp.matrices(degree,F(str(rho)));L=cholesky(tp.floating(G),lower=True)
    def transform(M):
        T=solve_triangular(L,tp.floating(M),lower=True)
        return solve_triangular(L,T.T,lower=True).T
    return transform(K),np.eye(len(G))-transform(MX),np.eye(len(G))-transform(MY),L,bs

def protocol(t):
    # Both existing plaquette coefficients vary continuously, each with zero endpoint derivative.
    u=np.pi*t/2
    return (1-np.cos(u),1.5*(1-np.cos(u)),np.pi/2*np.sin(u),.75*np.pi*np.sin(u))

def dop_driver(degree,tol,omit_work=False):
    K,V1,V2,L,bs=orthogonal_matrices(degree);n=len(bs)
    # e0 in monomial coordinates is the normalized constant; transform y=L^T e0.
    y0=np.r_[L.T[:,0].astype(complex),0j]
    def rhs(t,y):
        l1,l2,d1,d2=protocol(t);psi=y[:n];H=K+l1*V1+l2*V2
        work=0 if omit_work else d1*np.vdot(psi,V1@psi).real+d2*np.vdot(psi,V2@psi).real
        return np.r_[-1j*(H@psi),work]
    ts=np.linspace(0,2,161)
    sol=solve_ivp(rhs,(0,2),y0,method='DOP853',rtol=tol,atol=tol/10,t_eval=ts)
    if not sol.success:raise RuntimeError(sol.message)
    if not np.all(np.isfinite(sol.y)):raise ValueError('nonfinite integrated state/work')
    rows=[]
    for i,t in enumerate(ts):
        psi=sol.y[:n,i];l1,l2,d1,d2=protocol(t);H=K+l1*V1+l2*V2
        norm=np.vdot(psi,psi).real;energy=np.vdot(psi,H@psi).real;work=sol.y[n,i].real
        v1=np.vdot(psi,V1@psi).real;v2=np.vdot(psi,V2@psi).real
        rows.append({'t':float(t),'lambda1':l1,'lambda2':l2,'energy':energy,'integrated_work':work,'work_defect':energy-work,'norm_defect':norm-1,'V1':v1,'V2':v2})
    coeff=solve_triangular(L.T,sol.y[:n,-1],lower=False)
    return {'degree':degree,'dimension':n,'tolerance':tol,'norm_max':max(abs(r['norm_defect']) for r in rows),'work_max':max(abs(r['work_defect']) for r in rows),'final_energy':rows[-1]['energy'],'final_work':rows[-1]['integrated_work'],'rows':rows,'coeff':coeff,'psi':sol.y[:n,-1]}

def midpoint_driver(degree,steps,omit_work=False):
    K,V1,V2,L,bs=orthogonal_matrices(degree);psi=L.T[:,0].astype(complex);dt=2/steps;work=0.;max_norm=0.;max_work=0.;rows=[]
    def expectation(t,p):
        l1,l2,d1,d2=protocol(t)
        return (np.vdot(p,(K+l1*V1+l2*V2)@p).real,d1*np.vdot(p,V1@p).real+d2*np.vdot(p,V2@p).real)
    for s in range(steps):
        t=s*dt;l1,l2,_,_=protocol(t+dt/2);H=K+l1*V1+l2*V2
        # Diagonal exponential is a unitary midpoint propagator independent of DOP853.
        vals,vec=eigh(H);a=vec.conj().T@psi
        middle=vec@(np.exp(-.5j*dt*vals)*a);end=vec@(np.exp(-1j*dt*vals)*a)
        if not omit_work:work+=dt/6*(expectation(t,psi)[1]+4*expectation(t+dt/2,middle)[1]+expectation(t+dt,end)[1])
        psi=end
        if not np.all(np.isfinite(psi)):raise ValueError('nonfinite midpoint state')
        energy=expectation(t+dt,psi)[0]
        norm_defect=np.vdot(psi,psi).real-1
        max_norm=max(max_norm,abs(norm_defect));max_work=max(max_work,abs(energy-work))
        rows.append({'steps':steps,'t':t+dt,'energy':energy,'integrated_work':work,'work_defect':energy-work,'norm_defect':norm_defect})
    return {'steps':steps,'norm_max':max_norm,'work_max':max_work,'final_energy':energy,'final_work':work,'psi':psi,'rows':rows}

def dynamic_acceptance(r,method):
    if method not in ('DOP853','midpoint'):raise ValueError('unknown integration method')
    rows=r.get('rows')
    if not isinstance(rows,list) or not rows:raise ValueError('nonempty raw diagnostic history required')
    required=('energy','integrated_work','work_defect','norm_defect')
    if any(any(k not in row or not np.isfinite(row[k]) for k in required) for row in rows):raise ValueError('nonfinite/incomplete raw dynamic diagnostics')
    if r['norm_max']!=max(abs(row['norm_defect']) for row in rows) or r['work_max']!=max(abs(row['work_defect']) for row in rows):raise ValueError('raw/summary diagnostic mismatch')
    vals=[r['norm_max'],r['work_max'],r['final_energy'],r['final_work']]
    if not all(np.isfinite(v) for v in vals):raise ValueError('incomplete/nonfinite dynamic diagnostics')
    norm_limit=1e-8;work_limit=1e-7 if method=='DOP853' else 2e-4
    if r['norm_max']>norm_limit or r['work_max']>work_limit:raise ValueError(method+' failed its own norm/work gates')
    return True

def dynamics():
    coarse=dop_driver(3,1e-9);tight=dop_driver(3,1e-11);fine=dop_driver(4,1e-11)
    for name,r in [('D3 coarse',coarse),('D3 tight',tight),('D4 tight',fine)]:gate(name+' own work/norm',dynamic_acceptance(r,'DOP853'))
    tol_error=float(np.linalg.norm(coarse['psi']-tight['psi']));gate('DOP tolerance refinement',tol_error<1e-7,tol_error)
    _,G4,_,_,_=tp.matrices(4,F(1));diff=fine['coeff'].copy();diff[:len(tight['coeff'])]-=tight['coeff']
    degree_norm_squared=float(np.vdot(diff,tp.floating(G4)@diff).real)
    if not np.isfinite(degree_norm_squared) or degree_norm_squared<0:raise ValueError('invalid degree-refinement norm squared')
    degree_error=float(np.sqrt(degree_norm_squared))
    # This degree difference is a convergence diagnostic, not an untruncated dynamics error bound.
    mids=[midpoint_driver(3,n) for n in (80,160,320)]
    errors=[float(np.linalg.norm(m['psi']-tight['psi'])) for m in mids]
    orders=[float(np.log2(errors[i]/errors[i+1])) for i in range(2)]
    for m in mids:gate('midpoint '+str(m['steps'])+' own work/norm',dynamic_acceptance(m,'midpoint'))
    gate('independent midpoint converges',errors[-1]<2e-4 and all(1.7<o<2.3 for o in orders),{'state_errors':errors,'orders':orders})
    for method,bad in [('DOP853',dop_driver(3,1e-10,True)),('midpoint',midpoint_driver(3,80,True))]:
        failed=False
        try:dynamic_acceptance(bad,method)
        except ValueError:failed=True
        gate('omitted work mutation '+method,failed and bad['work_max']>1,{'defect':bad['work_max']})
    write_csv('dynamic_history.csv',fine['rows'])
    write_csv('dynamic_midpoint_history.csv',[row for m in mids for row in m['rows']])
    write_csv('dynamic_dop_comparison_history.csv',[dict(degree=r['degree'],tolerance=r['tolerance'],**row) for r in (coarse,tight,fine) for row in r['rows']])
    clean=lambda r:{k:v for k,v in r.items() if k not in ('rows','coeff','psi')}
    summary={'scope':'finite-Galerkin-time-evolution-no-infinite-tail-dynamics-certificate','protocol':'alpha=rho=1; lambda1(t)=1-cos(pi*t/2),lambda2(t)=1.5*(1-cos(pi*t/2)),0<=t<=2; initial constant Haar wavefunction','work_identity':'d<H>/dt=lambda1_dot*<1-x>+lambda2_dot*<1-y>','dop853':[clean(r) for r in (coarse,tight,fine)],'midpoint':[dict(clean(m),state_error=err) for m,err in zip(mids,errors)],'midpoint_orders':orders,'DOP_tolerance_state_error':tol_error,'D3_to_D4_state_difference':degree_error,'certified_dynamic_truncation_error':None}
    save('dynamic_summary.json',summary)
    fig,ax=plt.subplots(1,2,figsize=(10,4));rows=fine['rows'];ts=[r['t'] for r in rows]
    ax[0].plot(ts,[r['energy'] for r in rows],label='Energy');ax[0].plot(ts,[r['integrated_work'] for r in rows],'--',label='Integrated external work');ax[0].set(xlabel='Time',ylabel='Energy / work',title='Both plaquette couplings driven');ax[0].legend()
    ax[1].plot(ts,[r['lambda1'] for r in rows],label='λ₁(t)');ax[1].plot(ts,[r['lambda2'] for r in rows],label='λ₂(t)');ax[1].set(xlabel='Time',ylabel='Magnetic energy coefficient',title='Specified continuous protocol');ax[1].legend();fig.tight_layout()
    for ext in ('png','svg'):fig.savefig(OUT/('coupled_drive.'+ext),dpi=160)
    plt.close(fig)
    return summary

def stationary():
    cases=[(1,1,1,1),(1,1,2,1),(F(1,2),1,1,1),(1,1,1,F(1,2)),(1,1,1,2)]
    certs=[]
    for a,l1,l2,r in cases:
        c=tp.certificate(3,a,l1,l2,r);gate('exact certificate '+str((a,l1,l2,r)),tp.verify_certificate(c) and c['positive']);certs.append(c)
    # Same physical case, separate representation-degree convergence.
    rows=[]
    for d in range(1,6):
        e=tp.ritz(d,1,2,3)
        rows.append({'degree':d,'dimension':len(e),'alpha':1,'lambda1':2,'lambda2':3,'rho':1,'E0_Ritz':e[0],'E1_Ritz':e[1],'gap_Ritz_estimate':e[1]-e[0]})
    for i in range(1,len(rows)):
        gate('Ritz minmax monotonic energies D'+str(rows[i]['degree']),rows[i]['E0_Ritz']<=rows[i-1]['E0_Ritz']+1e-11 and rows[i]['E1_Ritz']<=rows[i-1]['E1_Ritz']+1e-11)
    for d in (2,3,4):
        c=tp.certificate(d,1,2,3);gate('matched convergence certificate D'+str(d),tp.verify_certificate(c) and c['positive']);certs.append(c)
        rows[d-1]['gap_certified_lower']=float(F(c['gap'][0]));rows[d-1]['gap_certified_upper']=float(F(c['gap'][1]))
    for row in rows:
        row.setdefault('gap_certified_lower','');row.setdefault('gap_certified_upper','')
    # Keep CSV field order stable across dictionary insertions.
    rows=[{k:r[k] for k in rows[0]} for r in rows]
    write_csv('stationary_convergence.csv',rows)
    sweep=[]
    for axis,values in [('alpha',[.5,1,2]),('lambda1',[0,.5,1,2,4]),('lambda2',[0,.5,1,2,4]),('rho',[.5,1,2])]:
        for value in values:
            p={'alpha':1,'lambda1':1,'lambda2':2,'rho':1};p[axis]=value;e=tp.ritz(4,**p)
            sweep.append(dict(axis=axis,value=value,degree=4,**p,E0_Ritz=e[0],E1_Ritz=e[1],gap_Ritz_estimate=e[1]-e[0]))
    write_csv('parameter_sweep.csv',sweep)
    pointcerts=[tp.certificate(2,1,i,j) for i in range(3) for j in range(3)]
    box=tp.rectangle_certificate(pointcerts);gate('continuous two-coupling rectangle',tp.verify_rectangle(box) and box['positive']);save('continuous_rectangle_certificate.json',box)
    save('stationary_certificates.json',{'contract':tp.CONTRACT,'scope':tp.SCOPE,'certificates':certs})
    fig,ax=plt.subplots(1,2,figsize=(10,4));d=[r['degree'] for r in rows]
    ax[0].plot(d,[r['gap_Ritz_estimate'] for r in rows],'o-',label='Ritz gap estimate')
    for r in rows:
        if r['gap_certified_lower']!='':ax[0].plot([r['degree']]*2,[r['gap_certified_lower'],r['gap_certified_upper']],color='#dc6b19',linewidth=4)
    ax[0].plot([],[],color='#dc6b19',linewidth=4,label='Exact infinite-space enclosure');ax[0].set(xlabel='Total polynomial degree D',ylabel='Gap',title='Matched α=1, λ₁=2, λ₂=3, ρ=1');ax[0].legend(fontsize=8)
    for axis in ('lambda1','lambda2'):
        sub=[r for r in sweep if r['axis']==axis];ax[1].plot([r['value'] for r in sub],[r['gap_Ritz_estimate'] for r in sub],'o-',label=axis)
    ax[1].set(xlabel='Varied magnetic coefficient',ylabel='Numerical Ritz gap estimate',title='One parameter at a time, D=4');ax[1].legend();fig.tight_layout()
    for ext in ('png','svg'):fig.savefig(OUT/('stationary_convergence.'+ext),dpi=160)
    plt.close(fig)
    return {'continuous_gap_lower':box['gap_lower'],'matched_gap_D4':certs[-1]['gap'],'matched_Ritz_D5':rows[-1]['gap_Ritz_estimate']}

def main():
    OUT.mkdir(exist_ok=True);GATES.clear();sources={p.name:hash_file(p) for p in [ROOT/'two_plaquette.py',ROOT/'run_study.py',ROOT/'test_solver.py']}
    save('validation.json',{'status':'running','source_hashes':sources})
    start=time.time()
    try:
        spec=stationary();dyn=dynamics()
        gate('all reported numerical diagnostics finite',all(np.isfinite(r['final_energy']) for r in dyn['dop853']))
        gate('frozen source bytes',sources=={p.name:hash_file(p) for p in [ROOT/'two_plaquette.py',ROOT/'run_study.py',ROOT/'test_solver.py']})
        result={'status':'passed','scope':tp.SCOPE,'source_hashes':sources,'optimized_python':not __debug__,'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'gates':GATES,'stationary_summary':spec,'elapsed_seconds':time.time()-start,'limitations':['Finite open graph only; no volume or continuum limit.','Dynamic representation error is unbounded; D3-to-D4 difference is diagnostic.','Parameter-sweep gaps are numerical Ritz differences unless individually certified.']}
        save('validation.json',result);print(json.dumps(result,indent=2))
    except Exception as e:
        save('validation.json',{'status':'failed','source_hashes':sources,'gates':GATES,'error':str(e)});raise
if __name__=='__main__':main()
