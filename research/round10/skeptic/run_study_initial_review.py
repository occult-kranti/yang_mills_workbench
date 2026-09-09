"""Reproduce rational stationary certificates and explicitly numerical dynamics."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.special import mathieu_b
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from certified_plaquette import certify,verify_certificate,float_matrix

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
GATES=[]


def gate(name,condition,**details):
    row={"name":name,"passed":bool(condition),**details}
    GATES.append(row)
    if not condition:
        raise RuntimeError(f"failed evaluated gate: {name}; {details}")


def number(z):
    return float(F(z))


def write_json(path,data):
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")


def write_csv(path,rows):
    if not rows:
        raise ValueError("refuse empty evidence")
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def stationary():
    rows=[];certs=[];radial=[];selected={}
    cases=[("0",8),("1/10",8),("1",8)]
    cases += [(str(lam),N) for lam in (2,4,6,8,10) for N in (8,16)]
    cases += [("100",N) for N in (8,16,24)]
    for lam,N in cases:
        c=certify("1",lam,N,40);verify_certificate(c);certs.append(c)
        low,high=[number(c["gap_interval"][z]) for z in ("lower","upper")]
        vals=eigh_tridiagonal(*float_matrix("1",lam,N),select="i",select_range=(0,1),eigvals_only=True)
        exact_oracle=float(mathieu_b(4,-2*float(F(lam)))-mathieu_b(2,-2*float(F(lam))))/4
        row={"coupling":lam,"N":N,"gap_lower":low,"gap_upper":high,
             "interval_width":high-low,"mathieu_gap_float":exact_oracle,
             "finite_matrix_gap_float":float(vals[1]-vals[0]),
             "positive_gap_certified":c["positive_gap_certified"]}
        rows.append(row)
        # Floating special functions are an independent check, not certification.
        gate(f"Mathieu consistency lambda={lam},N={N}",low-2e-10 <= exact_oracle <= high+2e-10,
             distance=max(low-exact_oracle,exact_oracle-high,0.0))
        selected[lam]=c
    for lam,c in selected.items():
        lo,hi=(F(c["gap_interval"][z]) for z in ("lower","upper"))
        gate(f"stationary enclosure precision lambda={lam}",hi-lo < F(1,10**8)*max(F(1),lo))
        gate(f"stationary positive gap lambda={lam}",lo>0)
    # Coverage uses exact rational centers/radii, not nearest floating samples.
    centers=[F(k) for k in (0,2,4,6,8,10)]
    cells=[(max(F(0),v-1),min(F(10),v+1)) for v in centers]
    gate("closed cells cover [0,10]",cells[0][0]==0 and cells[-1][1]==10 and
         all(left[1]>=right[0] for left,right in zip(cells,cells[1:])))
    lower=min(F(selected[str(v)]["gap_interval"]["lower"]) for v in centers)-2
    gate("continuous [0,10] gap lower is positive",lower>0)
    convenient=F(999999,1000000)
    gate("simple uniform lower 999999/1000000 is certified",lower>=convenient)
    cover={"scope":"alpha=1; single plaquette; coupling in closed [0,10]",
           "gap_lipschitz_constant":"2","nearest_center_radius":"1",
           "centers":[str(v) for v in centers],"cells":[[str(a),str(b)] for a,b in cells],
           "certificate_index_by_center":{str(v):certs.index(selected[str(v)]) for v in centers},
           "uniform_gap_lower":str(lower),"conservative_uniform_gap_lower":str(convenient),
           "status":"certified-conditional-on-gap-Lipschitz-theorem"}
    for lam in (0,1,10,100):
        previous=None;errors=[]
        oracle=float(mathieu_b(4,-2*lam)-mathieu_b(2,-2*lam))/4
        for M in (256,512,1024,2048):
            h=np.pi/(M+1);theta=h*np.arange(1,M+1)
            d=2/h**2-1+lam*(1-np.cos(theta));b=np.full(M-1,-1/h**2)
            energies=eigh_tridiagonal(d,b,select="i",select_range=(0,1),eigvals_only=True)
            gap=float(energies[1]-energies[0]);err=abs(gap-oracle);errors.append(err)
            radial.append({"coupling":lam,"interior_nodes":M,"spacing":h,"gap":gap,
                           "mathieu_gap_float":oracle,"absolute_error":err,
                           "observed_order":None if previous is None else np.log2(previous/err)})
            previous=err
        order=np.log2(errors[-2]/errors[-1])
        gate(f"radial independent order lambda={lam}",1.8<order<2.2,order=float(order))
        gate(f"radial final relative error lambda={lam}",errors[-1]/max(1,oracle)<1e-4,
             mixed_relative_error=errors[-1]/max(1,oracle))
    write_json(OUT/"stationary_certificates.json",certs)
    write_json(OUT/"continuous_range_certificate.json",cover)
    write_csv(OUT/"stationary_intervals.csv",rows)
    write_csv(OUT/"radial_comparison.csv",radial)
    fig,axes=plt.subplots(1,2,figsize=(10,4),layout="constrained")
    finalrows=[r for r in rows if selected[r["coupling"]]["N"]==r["N"]]
    x=[float(F(r["coupling"])) for r in finalrows if float(F(r["coupling"]))<=10]
    y=[(r["gap_lower"]+r["gap_upper"])/2 for r in finalrows if float(F(r["coupling"]))<=10]
    order=np.argsort(x);axes[0].plot(np.array(x)[order],np.array(y)[order],"o-",label="Certified point enclosures")
    axes[0].axhline(float(convenient),ls="--",color="#b35b32",label="Proved interval-wide lower bound")
    axes[0].set(xlabel="Magnetic coupling λ (α=1)",ylabel="Single-plaquette gap",title="Continuous coupling, bounded gap")
    axes[0].legend(fontsize=8)
    extreme=[r for r in rows if r["coupling"]=="100"]
    axes[1].semilogy([r["N"] for r in extreme],[r["interval_width"] for r in extreme],"o-")
    axes[1].set(xlabel="Retained characters N",ylabel="Certified gap enclosure width",title="Infinite-tail control at λ=100")
    fig.savefig(OUT/"stationary_bounds.svg");fig.savefig(OUT/"stationary_bounds.png",dpi=160);plt.close(fig)
    return rows,cover


def protocol(t,T=2.0):
    if t<0 or t>T:
        raise ValueError("protocol time outside [0,T]")
    return 5*(1-np.cos(np.pi*t/T)),5*np.pi/T*np.sin(np.pi*t/T)


def kinetic(n):
    x=np.arange(n,dtype=float)
    return x*(x+2)


def potential(psi):
    out=psi.copy();out[1:]-=.5*psi[:-1];out[:-1]-=.5*psi[1:]
    return out


def dynamic_reference(N,tolerance):
    kin=kinetic(N);initial=np.zeros(N+1,dtype=complex);initial[0]=1
    def rhs(t,y):
        lam,rate=protocol(t);psi=y[:-1];v=potential(psi)
        return np.r_[-1j*(kin*psi+lam*v),rate*np.vdot(psi,v).real]
    times=np.linspace(0,2,401)
    sol=solve_ivp(rhs,(0,2),initial,method="DOP853",rtol=tolerance,atol=tolerance*.01,t_eval=times)
    if not sol.success or len(sol.t)!=len(times) or not np.isfinite(sol.y).all():
        raise RuntimeError("incomplete or nonfinite dynamic reference")
    states=sol.y[:-1].T;work=sol.y[-1].real
    energy=np.array([np.vdot(p,kin*p+protocol(t)[0]*potential(p)).real for t,p in zip(times,states)])
    norms=np.sum(abs(states)**2,axis=1)
    return times,states,work,energy,norms,sol.nfev


def midpoint_unitary(N,steps):
    # Separate propagation algorithm. Work uses actual lambda derivative and
    # Simpson expectations of left/mid/right states, not endpoint energy.
    psi=np.zeros(N,dtype=complex);psi[0]=1;work=0.0;h=2.0/steps;kin=kinetic(N)
    def v_exp(p):
        return float(np.sum(abs(p)**2)-np.vdot(p[:-1],p[1:]).real)
    for step in range(steps):
        t=step*h;lam,_=protocol(t+h/2)
        energies,vectors=eigh_tridiagonal(kin+lam,np.full(N-1,-lam/2))
        coeff=vectors.T@psi
        mid=vectors@(np.exp(-1j*energies*h/2)*coeff)
        right=vectors@(np.exp(-1j*energies*h)*coeff)
        work+=h/6*(protocol(t)[1]*v_exp(psi)+4*protocol(t+h/2)[1]*v_exp(mid)+protocol(t+h)[1]*v_exp(right))
        psi=right
    energy=float(np.sum(kin*abs(psi)**2)+10*v_exp(psi))
    return psi,work,energy


def dynamics():
    results=[]
    runs={}
    for N,tol in ((16,1e-9),(16,1e-11),(24,1e-11)):
        times,states,work,energy,norms,nfev=dynamic_reference(N,tol)
        key=f"N{N}-tol{tol:g}";runs[key]=(states,work,energy,norms)
        normerr=float(np.max(abs(norms-1)));workerr=float(np.max(abs(energy-energy[0]-work)))
        gate(f"DOP853 norm {key}",normerr<1e-8,max_norm_error=normerr)
        gate(f"independently integrated work {key}",workerr<1e-8,max_work_defect=workerr)
        results.append({"method":"DOP853","N":N,"control":tol,"state_error":None,
                        "max_norm_defect":normerr,"max_work_defect":workerr,"nfev":nfev})
    ref=runs["N16-tol1e-11"][0]
    temporal=float(np.max(np.linalg.norm(runs["N16-tol1e-09"][0]-ref,axis=1)))
    spatial=float(np.max(np.linalg.norm(np.pad(ref,((0,0),(0,8)))-runs["N24-tol1e-11"][0],axis=1)))
    gate("DOP853 tolerance refinement",temporal<1e-7,state_discrepancy=temporal)
    gate("representation truncation refinement",spatial<1e-7,state_discrepancy=spatial)
    errors=[]
    for steps in (256,512,1024):
        psi,work,energy=midpoint_unitary(16,steps)
        err=float(np.linalg.norm(psi-ref[-1]));errors.append(err)
        results.append({"method":"independent-unitary-midpoint","N":16,"control":steps,
                        "state_error":err,"max_norm_defect":float(abs(np.vdot(psi,psi)-1)),
                        "max_work_defect":abs(energy-work),"nfev":None})
    order=float(np.log2(errors[-2]/errors[-1]))
    gate("independent midpoint convergence order",1.7<order<2.3,order=order)
    gate("independent midpoint final state accuracy",errors[-1]<1e-4,state_error=errors[-1])
    energy=runs["N24-tol1e-11"][2];work=runs["N24-tol1e-11"][1];states=runs["N24-tol1e-11"][0]
    defect=energy-energy[0]
    gate("omitted external work negative control",float(np.max(abs(defect)))>1,
         omitted_work_defect=float(np.max(abs(defect))))
    history=[]
    for i,t in enumerate(times):
        history.append({"time":t,"coupling":protocol(t)[0],"energy":energy[i],"integrated_work":work[i],
                        "work_defect":energy[i]-energy[0]-work[i],"norm":float(np.sum(abs(states[i])**2)),
                        "last_character_probability":float(abs(states[i,-1])**2)})
    write_csv(OUT/"dynamic_history.csv",history);write_json(OUT/"dynamic_comparisons.json",results)
    write_json(OUT/"dynamic_summary.json",{"scope":"numerical finite-Galerkin dynamics, not a certified time-error enclosure",
        "protocol":"alpha=1; lambda(t)=5[1-cos(pi*t/2)], 0<=t<=2; initial chi_0",
        "tolerance_state_discrepancy":temporal,"N16_to_N24_state_discrepancy":spatial,
        "independent_midpoint_final_state_discrepancy":errors[-1],"midpoint_order":order,
        "energy_change":float(energy[-1]-energy[0]),"integrated_work":float(work[-1]),
        "omitted_work_negative_control":float(np.max(abs(defect)))})
    fig,axes=plt.subplots(1,2,figsize=(10,4),layout="constrained")
    axes[0].plot(times,energy,label="Quantum energy");axes[0].plot(times,work,"--",label="Integrated external work")
    axes[0].set(xlabel="Dimensionless time (α=1)",ylabel="Energy",title="Changing coupling carries an energy cost")
    axes[0].legend(fontsize=8)
    axes[1].plot(times,energy-energy[0]-work,label="Full work identity")
    axes[1].set(xlabel="Dimensionless time",ylabel="Energy minus integrated work",title="A numerical conservation diagnostic")
    fig.savefig(OUT/"coupling_ramp.svg");fig.savefig(OUT/"coupling_ramp.png",dpi=160);plt.close(fig)
    return results


def main():
    OUT.mkdir(exist_ok=True)
    stationary();dynamics()
    if not GATES or not all(g["passed"] for g in GATES):
        raise RuntimeError("cannot report incomplete acceptance")
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob("*.py"))}
    write_json(OUT/"validation.json",{"status":"passed","gates":GATES,"gate_count":len(GATES),"source_hashes":hashes,
         "limits":"Rational stationary enclosures use proved finite-graph tail inequalities; dynamics and radial comparison remain numerical."})
    print(json.dumps({"status":"passed","gate_count":len(GATES),"output":str(OUT)}))


if __name__=="__main__":
    main()
