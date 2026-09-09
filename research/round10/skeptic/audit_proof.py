"""Independent proof-wrapper omission, scope and arithmetic mutation checks."""
from pathlib import Path
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import shutil
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent if (HERE.parent/"proof_routes.py").is_file() else HERE.parent/"physics-observatory"/"research"/"round10"
DEST=HERE/"corrected_proof_probe"
checks=[]


def gate(name,passed,details=None):
    checks.append({"name":name,"passed":bool(passed),"details":details})


def main():
    DEST.mkdir(exist_ok=True)
    manifest=json.loads((SOURCE/"proof_manifest.json").read_text())
    original={}
    for rel in [*manifest["sha256"],"proof_manifest.json"]:
        path=DEST/rel;path.parent.mkdir(parents=True,exist_ok=True)
        original[rel]=(SOURCE/rel).read_bytes()
        path.write_bytes(original[rel])
    sys.path.insert(0,str(DEST))
    sys.modules.pop("proof_search",None)
    spec=importlib.util.spec_from_file_location("independent_route_probe",DEST/"proof_routes.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    def reset():
        for rel,data in original.items():
            (DEST/rel).write_bytes(data)
    def execute_rejected():
        try:
            with contextlib.redirect_stdout(io.StringIO()):module.execute()
        except (RuntimeError,ValueError,KeyError,TypeError):
            return True
        return False
    gate("unchanged proof package executes",not execute_rejected())
    result=json.loads((DEST/"proof_results.json").read_text())
    gate("positive route retains13 replayed rules",
         result["routes"]["certified_parameter_range"]["result"]["certified_cost"]==13)
    for label in ("without_gauge_projection","without_tail_positivity","without_exact_brackets",
                  "without_continuous_cover","yang_mills_prize"):
        gate("unavailable route "+label,result["routes"][label]["result"]["status"]=="not_derivable")
    for name,change in (
        ("empty required inputs",lambda m:m.update(sha256={})),
        ("omitted advisor",lambda m:m["sha256"].pop("advisor/advisor.md")),
        ("surplus escaped path",lambda m:m["sha256"].update({"../unreviewed.txt":"0"*64})),
        ("invalid digest",lambda m:m["sha256"].update({"advisor/advisor.md":"not-a-digest"})),
    ):
        reset();mutant=copy.deepcopy(manifest);change(mutant)
        (DEST/"proof_manifest.json").write_text(json.dumps(mutant))
        gate("manifest rejects "+name,execute_rejected())

    # Update the mutated JSON's manifest hash deliberately, so this tests the
    # semantic arithmetic replay beyond simple stale-byte detection.
    for name,rel,change in (
        ("point scope escalation","solver/output/stationary_certificates.json",
         lambda d:d[0].update(scope="complete four-dimensional Yang-Mills")),
        ("point gap overstatement","solver/output/stationary_certificates.json",
         lambda d:d[0]["gap_interval"].update(lower="100")),
        ("range scope escalation","solver/output/continuous_range_certificate.json",
         lambda d:d.update(scope="all physical volumes and spacings")),
        ("range constant overstatement","solver/output/continuous_range_certificate.json",
         lambda d:d.update(conservative_uniform_gap_lower="2")),
        ("range endpoint hole","solver/output/continuous_range_certificate.json",
         lambda d:d["cells"][0].__setitem__(0,"1/2")),
    ):
        reset();data=json.loads(original[rel]);change(data)
        raw=json.dumps(data).encode();(DEST/rel).write_bytes(raw)
        adjusted=copy.deepcopy(manifest);adjusted["sha256"][rel]=hashlib.sha256(raw).hexdigest()
        (DEST/"proof_manifest.json").write_text(json.dumps(adjusted))
        gate("arithmetic replay rejects "+name,execute_rejected())
    reset()
    report={"status":"passed" if checks and all(c["passed"] for c in checks) else "failed",
            "check_count":len(checks),"checks":checks,
            "source_hashes":{rel:hashlib.sha256(data).hexdigest() for rel,data in original.items()},
            "scope":"Reviewed wrapper line/function logic and executed targeted controls. Reused full search implementation was not line-by-line re-audited. Horn certificate is conditional conventional mathematics, not a proof-assistant kernel."}
    (HERE/"proof_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"checks":len(checks),
                      "failures":[c["name"] for c in checks if not c["passed"]]}))
    if report["status"]!="passed":raise SystemExit(1)


if __name__=="__main__":main()
