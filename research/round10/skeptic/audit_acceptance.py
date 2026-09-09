"""Replay claim-integrity, continuous-domain and dynamic-work negative controls."""
from pathlib import Path
from fractions import Fraction as F
import copy
import importlib.util
import json
import hashlib
import sys

HERE=Path(__file__).resolve().parent
SOLVER=HERE.parent/"solver" if (HERE.parent/"solver").is_dir() else HERE.parent/"ym10-solver"
sys.path.insert(0,str(SOLVER))
import certified_plaquette as producer
import run_study as study
checks=[]


def gate(name,condition,details=None):
    checks.append({"name":name,"passed":bool(condition),"details":details})


def rejects(fn):
    try:
        fn()
    except (ValueError,TypeError,KeyError,ArithmeticError,RuntimeError):
        return True
    return False


def main():
    cover=json.loads((SOLVER/"output"/"continuous_range_certificate.json").read_text())
    certs=json.loads((SOLVER/"output"/"stationary_certificates.json").read_text())
    gate("original continuous certificate replays",producer.verify_continuous_range(cover,certs))
    mutations=[
        ("scope",lambda c:c.update(scope="four dimensional physical Yang-Mills")),
        ("half Lipschitz rate",lambda c:c.update(gap_lipschitz_constant="1")),
        ("half radius",lambda c:c.update(nearest_center_radius="1/2")),
        ("radius false label",lambda c:c["cell_radii"].__setitem__(2,"1/2")),
        ("endpoint gap",lambda c:c["cells"][0].__setitem__(0,"1/100")),
        ("interior gap",lambda c:c["cells"][2].__setitem__(0,"31/10")),
        ("empty cells",lambda c:c.update(cells=[])),
        ("wrong center",lambda c:c["certificate_index_by_center"].update({"2":0})),
        ("unproved uniform lower",lambda c:c.update(uniform_gap_lower="2")),
        ("rounded up simple bound",lambda c:c.update(conservative_uniform_gap_lower="1")),
    ]
    for name,mutate in mutations:
        candidate=copy.deepcopy(cover);mutate(candidate)
        gate("continuous certificate rejects "+name,
             rejects(lambda candidate=candidate:producer.verify_continuous_range(candidate,certs)))
    gate("continuous certificate rejects absent evidence",
         rejects(lambda:producer.verify_continuous_range(cover,[])))

    # The old version completed all gates with this exact mutation. The repaired
    # version must now fail before producing accepted output. Files stay local.
    destination=HERE/"corrected_omitted_work_probe";destination.mkdir(exist_ok=True)
    study.OUT=destination
    original=study.midpoint_unitary
    def omitted_work(n,steps):
        psi,work,energy=original(n,steps)
        return psi,0.0,energy
    study.midpoint_unitary=omitted_work
    study.GATES.clear()
    error=None
    try:
        study.dynamics()
    except RuntimeError as exc:
        error=str(exc)
    finally:
        study.midpoint_unitary=original
    gate("omitted midpoint work now fails evaluated gate",
         error is not None and "midpoint independent work" in error,error)
    gate("failure is a resolved physical work defect",bool(study.GATES)
         and study.GATES[-1].get("passed") is False
         and study.GATES[-1].get("work_defect",0)>1,study.GATES[-1] if study.GATES else None)

    # A failed rerun must replace old success instead of leaving stale evidence.
    original_stationary=study.stationary
    study.GATES.append({"name":"preexisting false pass","passed":True})
    destination.joinpath("validation.json").write_text('{"status":"passed"}')
    def fail_stationary():
        raise RuntimeError("injected study failure")
    study.stationary=fail_stationary
    try:
        did_reject=rejects(study.main)
    finally:
        study.stationary=original_stationary
    status=json.loads(destination.joinpath("validation.json").read_text())
    gate("failed rerun replaces stale success",did_reject and status.get("status")=="failed",status.get("failure"))
    gate("rerun clears prior gates",status.get("gates")==[])

    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (SOLVER/"certified_plaquette.py",SOLVER/"run_study.py")}
    result={"status":"passed" if checks and all(row["passed"] for row in checks) else "failed",
            "check_count":len(checks),"checks":checks,"source_hashes":hashes,
            "limitations":"Planted incorrect controls test rejection behavior; they are not new failures of the corrected scientific model."}
    path=HERE/("acceptance_audit_optimized.json" if not __debug__ else "acceptance_audit.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"checks":len(checks),"optimized":not __debug__}))
    if result["status"]!="passed":
        raise SystemExit(1)


if __name__=="__main__":
    main()
