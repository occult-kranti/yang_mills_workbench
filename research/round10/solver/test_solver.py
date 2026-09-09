"""Explicit edge/mutation gates, retained under python -O."""
from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import json
import sys
import numpy as np
from certified_plaquette import *
import run_study as study

ROOT=Path(__file__).resolve().parent
gates=[]


def check(name,condition):
    gates.append({"name":name,"passed":bool(condition)})
    if not condition:
        raise RuntimeError("failed: "+name)


def rejected(name,function):
    try:
        function()
    except (ValueError,TypeError,KeyError,ArithmeticError):
        check(name,True)
    else:
        check(name,False)


def main():
    for a,lam,n,label in ((0,1,8,"zero alpha"),(-1,1,8,"negative alpha"),(1,-1,8,"negative lambda"),
       (1,1,1,"N one"),(1,1,0,"N zero"),(1,1,True,"N bool"),(1,1,2.0,"N float"),
       (float("nan"),1,8,"alpha NaN"),(1,float("inf"),8,"lambda infinity"),(True,1,8,"alpha bool")):
        rejected(label,lambda a=a,lam=lam,n=n:certify(a,lam,n))
    rejected("inadequate tail threshold",lambda:certify(1,100,2))
    for bits in (0,129,True,2.5):
        rejected(f"invalid precision {bits}",lambda bits=bits:eigen_interval([0,3],0,0,bits))
    for k in (-1,2,True):
        rejected(f"invalid eigen index {k}",lambda k=k:eigen_interval([0,3],0,k))
    rejected("empty Sturm evidence",lambda:sturm_count([],1,0))
    for x,count in ((F(-1),0),(F(0),1),(F(1),1),(F(2),2)):
        check(f"exact Jacobi endpoint {x}",sturm_count([0,0],1,x)==count)
    check("zero intermediate and terminal determinants",sturm_count([0,0,0],1,0)==1)
    check("reducible diagonal with repeated roots",sturm_count([0,0,3,3],0,3)==2)
    c=certify(1,10,16)
    check("unmodified rational certificate",verify_certificate(c))
    for label,mutator in (
        ("scope escalation",lambda q:q.update(scope="complete four-dimensional Yang-Mills")),
        ("precision escalation",lambda q:q.update(bits=128)),
        ("numeric bool",lambda q:q.update(positive_gap_certified=1)),
        ("false semantic status",lambda q:q.update(status="solved")),
        ("cutoff indexing",lambda q:q.update(N=q["N"]+1)),
        ("tail shift factor",lambda q:q["tail"].update(delta=str(2*F(q["tail"]["delta"])))),
        ("tail threshold index",lambda q:q["tail"].update(tau=str(F(q["tail"]["tau"])+1))),
        ("gap subtraction",lambda q:q["gap_interval"].update(lower=q["energy_intervals"][1]["lower"])),
        ("eigenvalue index swap",lambda q:q["A_eigen_intervals"].reverse()),
        ("missing eigenvalue",lambda q:q["B_eigen_intervals"].pop()),
        ("empty eigenvalues",lambda q:q.update(A_eigen_intervals=[])),
        ("NaN endpoint",lambda q:q["A_eigen_intervals"][0].update(lower="nan")),
    ):
        q=copy.deepcopy(c);mutator(q)
        rejected(label,lambda q=q:verify_certificate(q))
    free=certify("1",0,2)
    for k,E in ((0,F(0)),(1,F(3))):
        z=free["energy_intervals"][k]
        check(f"exact free eigenvalue {k}",F(z["lower"])<=E<=F(z["upper"]))
    scaled=certify("1/10",1,16)
    g1=c["gap_interval"];g2=scaled["gap_interval"]
    check("energy-unit scaling enclosure overlap",max(F(g1["lower"])/10,F(g2["lower"]))<=min(F(g1["upper"])/10,F(g2["upper"])))
    coarse=certify("1/1000000",0,32,16)
    check("coarse valid enclosure does not claim positivity",verify_certificate(coarse) and not coarse["positive_gap_certified"])
    centers=list(range(0,11,2));points=[certify(1,k,16,30) for k in centers]
    lower=min(F(p["gap_interval"]["lower"]) for p in points)-2
    cover={"scope":"alpha=1; single plaquette; coupling in closed [0,10]",
      "gap_lipschitz_constant":"2","nearest_center_radius":"1",
      "centers":[str(k) for k in centers],"cells":[[str(max(0,k-1)),str(min(10,k+1))] for k in centers],
      "cell_radii":["1"]*6,"certificate_index_by_center":{str(k):i for i,k in enumerate(centers)},
      "uniform_gap_lower":str(lower),"conservative_uniform_gap_lower":"999999/1000000",
      "status":"certified-conditional-on-gap-Lipschitz-theorem"}
    check("continuous cover callable replay",verify_continuous_range(cover,points))
    for label,mutator in (
      ("range scope",lambda q:q.update(scope="all continuum Yang-Mills")),
      ("range Lipschitz constant",lambda q:q.update(gap_lipschitz_constant="1")),
      ("range radius",lambda q:q.update(nearest_center_radius="1/2")),
      ("range cell radius",lambda q:q["cell_radii"].__setitem__(1,"1/2")),
      ("range endpoint hole",lambda q:q["cells"][0].__setitem__(0,"1/2")),
      ("range interior hole",lambda q:q["cells"][2].__setitem__(0,"7/2")),
      ("range wrong center certificate",lambda q:q["certificate_index_by_center"].update({"2":2})),
      ("range bool index",lambda q:q["certificate_index_by_center"].update({"2":True})),
      ("range altered lower",lambda q:q.update(uniform_gap_lower="3")),
      ("range excessive simple bound",lambda q:q.update(conservative_uniform_gap_lower="2")),
      ("range empty cells",lambda q:q.update(cells=[])),
      ("range erased conditional status",lambda q:q.update(status="proved-continuum")),
    ):
        q=copy.deepcopy(cover);mutator(q)
        rejected(label,lambda q=q:verify_continuous_range(q,points))
    rejected("range absent evidence",lambda:verify_continuous_range(cover,[]))
    wrong_alpha=copy.deepcopy(points);wrong_alpha[1]=certify(2,2,16,30)
    rejected("range different energy scale",lambda:verify_continuous_range(cover,wrong_alpha))
    for t in (-1,3,float("nan"),float("inf")):
        rejected(f"bad protocol time {t}",lambda t=t:study.protocol(t))
    for N,tol in ((1,1e-8),(True,1e-8),(16,0),(16,float("nan"))):
        rejected(f"bad dynamic inputs {N},{tol}",lambda N=N,tol=tol:study.dynamic_reference(N,tol))
    for steps in (0,True,1.5):
        rejected(f"bad midpoint steps {steps}",lambda steps=steps:study.midpoint_unitary(16,steps))
    rng=np.random.default_rng(324)
    psi=rng.normal(size=16)+1j*rng.normal(size=16)
    V=np.eye(16)-.5*np.diag(np.ones(15),1)-.5*np.diag(np.ones(15),-1)
    check("potential stencil against dense matrix",np.max(abs(study.potential(psi)-V@psi))<1e-14)
    check("potential operator positive",np.linalg.eigvalsh(V)[0]>0 and np.linalg.eigvalsh(V)[-1]<2)
    if "--inject-failure" in sys.argv:
        check("deliberate failure must survive optimization",False)
    check("nonempty evaluated gate list",len(gates)>0)
    report={"status":"passed","optimized":not __debug__,"gate_count":len(gates),"gates":gates,
            "source_hashes":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob("*.py"))}}
    destination=ROOT/"output"/("edge_tests_optimized.json" if not __debug__ else "edge_tests.json")
    destination.parent.mkdir(exist_ok=True);destination.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":"passed","gates":len(gates),"optimized":not __debug__}))


if __name__=="__main__":
    main()
