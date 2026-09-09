#!/usr/bin/env python3
"""Independent raw-monomial RK45 oracle and bounded numerical API challenges."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json,sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from round11_independent_algebra import my_matrices,load

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--label',default='numerical_audit');args=ap.parse_args();src=args.source.resolve();sys.path.insert(0,str(src.parent));m=load(src,'reviewed_run_study');before=hashlib.sha256(src.read_bytes()).hexdigest();records=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        records.append(dict(test=name,passed=True,detail=detail))
    def rejects(fn,name):
        try:fn()
        except (ValueError,TypeError,KeyError,RuntimeError):check(True,name);return
        raise RuntimeError('Unexpected acceptance: '+name)
    p={'kind':'cosine_ramp','duration':'2','lambda1_scale':'1/10','lambda2_scale':'3/20'}
    basis,G,K,X,Y=my_matrices(3,F(1));G,K,X,Y=[np.array(a,dtype=float) for a in (G,K,X,Y)];n=len(G);ts=np.linspace(0,2,21)
    def rhs(t,v):
        shape=1-np.cos(np.pi*t/2);rate=np.pi/2*np.sin(np.pi*t/2);c=v[:n]
        H=K-shape*(.1*X+.15*Y)
        work=rate*np.vdot(c,(.1*(G-X)+.15*(G-Y))@c).real
        return np.r_[-1j*np.linalg.solve(G,H@c),work]
    initial=np.zeros(n+1,dtype=complex);initial[0]=1
    ref=solve_ivp(rhs,(0,2),initial,method='RK45',rtol=2e-12,atol=2e-13,t_eval=ts)
    check(ref.success and np.all(np.isfinite(ref.y)),'independent_RK45_success_and_finiteness')
    prod=m.evolve(p,3,tolerance=1e-12,points=len(ts));check(m.numerical_gate(prod),'production_DOP_own_norm_work')
    differences=[];normdef=[];workdef=[]
    for j,t in enumerate(ts):
        c=ref.y[:n,j];diff=c-prod['coefficients'][:,j];differences.append(float(np.sqrt(np.vdot(diff,G@diff).real)))
        norm=np.vdot(c,G@c).real;shape=1-np.cos(np.pi*t/2);energy=np.vdot(c,(K+shape*(.1*(G-X)+.15*(G-Y)))@c).real
        normdef.append(abs(norm-1));workdef.append(abs(energy-ref.y[n,j].real))
    check(max(normdef)<1e-9,'independent_RK45_norm',max(normdef));check(max(workdef)<1e-9,'independent_RK45_work',max(workdef));check(max(differences)<1e-9,'raw_monomial_RK45_vs_orthogonal_DOP',max(differences))
    mids=[m.midpoint(p,3,k) for k in (80,160,320)];end=prod['states'][:,-1];errors=[float(np.linalg.norm(x['state']-end)) for x in mids]
    check(all(x['max_norm_defect']<1e-8 and x['max_work_defect']<2e-4 for x in mids),'each_midpoint_own_norm_and_work')
    orders=[float(np.log2(errors[j]/errors[j+1])) for j in range(2)]
    check(all(1.9<q<2.1 for q in orders),'midpoint_independent_method_refinement',dict(errors=errors,orders=orders))
    for name,change in [('times',lambda x:x['rows'][5].__setitem__('t',.1)),('phase',lambda x:x.__setitem__('state_phase_convention','physical-H-with-scalar')),('shape',lambda x:x.__setitem__('states',x['states'][:,:1])),('protocol',lambda x:x['protocol'].__setitem__('lambda1_scale','1/5')),('nan',lambda x:x['states'].__setitem__((0,5),np.nan))]:
        c=copy.deepcopy(prod);change(c);rejects(lambda:m.state_difference(prod,c),'state_comparison_rejects_'+name)
    for name,change in [('empty',lambda x:x.__setitem__('rows',[])),('transient_nan',lambda x:x['rows'][4].__setitem__('work_defect',np.nan)),('false_summary',lambda x:x.__setitem__('max_norm_defect',0))]:
        c=copy.deepcopy(prod);change(c);rejects(lambda:m.numerical_gate(c),'numerical_gate_rejects_'+name)
    for name,fn in [('bool_degree',lambda:m.evolve(p,True)),('bad_tolerance',lambda:m.evolve(p,3,tolerance=float('nan'))),('one_sample',lambda:m.evolve(p,3,points=1)),('midpoint_zero_steps',lambda:m.midpoint(p,3,0))]:rejects(fn,'public_'+name)
    # A bounded finite two-state oracle for MID1. This is a diagnostic, not an
    # outward-rounded temporal certificate. It also exposes a dropped commutator.
    B=np.diag([1.,-1.]);C=np.array([[0.,1.],[1.,0.]]);I=np.eye(2,dtype=complex);h=.1
    sol=solve_ivp(lambda t,u:(-1j*(B+(t-h/2)*C)@u.reshape(2,2)).reshape(4),(0,h),I.reshape(4),method='DOP853',rtol=2e-13,atol=2e-14)
    err=float(np.linalg.norm(sol.y[:,-1].reshape(2,2)-expm(-1j*h*B),2));comm=float(np.linalg.norm(B@C-C@B,2));bound=h**3*comm/12+h**4/32
    check(err<bound and err>h**4/32,'MID1_commutator_term_is_necessary',dict(error=err,bound=bound,wrong_dropped_commutator_bound=h**4/32))
    curverror=float(np.linalg.norm(expm(-1j*h**3*C/12)-I,2));check(curverror<=h**3/12,'MID1_curvature_coefficient_fixture',dict(error=curverror,bound=h**3/12))
    # Exact independent Gram matrices show compressed multiplication can fail to commute.
    Xc=np.linalg.solve(G,X);Yc=np.linalg.solve(G,Y);comm_xy=np.max(np.abs(Xc@Yc-Yc@Xc))
    check(comm_xy>.001,'compressed_multiplication_commutator_nonzero',float(comm_xy))
    check(hashlib.sha256(src.read_bytes()).hexdigest()==before,'numerical_source_unchanged')
    result=dict(status='passed',gate_count=len(records),optimized_python=not __debug__,source_sha256=before,audit_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),records=records,scope='Independent finite-dimensional floating diagnostics and input failures; no certified cosine time stepping, floating rounding, or reference-cutoff tail.')
    Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:result[k] for k in ('status','gate_count','source_sha256')}))
if __name__=='__main__':main()
