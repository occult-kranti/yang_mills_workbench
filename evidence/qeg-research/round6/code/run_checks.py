"""Run fresh round-six gates; a zero process exit alone is insufficient."""
from pathlib import Path
import hashlib,json,platform,subprocess,sys,time
ROOT=Path(__file__).resolve().parent.parent

def execute(args,output_name,predicate):
    output=ROOT/output_name
    previous=output.stat().st_mtime_ns if output.exists() else None
    source=ROOT/args[0]
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    proc=subprocess.run([sys.executable]+args,cwd=ROOT,capture_output=True,text=True)
    after=hashlib.sha256(source.read_bytes()).hexdigest()
    fresh=output.is_file() and output.stat().st_mtime_ns != previous
    payload=json.loads(output.read_text()) if fresh else None
    accepted=proc.returncode==0 and before==after and fresh and predicate(payload)
    return {'args':args,'passed':bool(accepted),'exit_code':proc.returncode,'fresh_output':fresh,'source_unchanged':before==after,'source_sha256':before,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest() if fresh else None,'stdout':proc.stdout,'stderr':proc.stderr}

def main():
    jobs=[
      (['test_planner_compatibility.py'],'planner_compatibility_results.json',lambda x:x.get('passed') is True and x.get('tests_run')==24),
      (['test_code_regressions.py'],'code_regression_results.json',lambda x:x.get('passed') is True and x.get('tests_run',0)>0 and x.get('failures')==0 and x.get('errors')==0),
      (['code/symbolic_checks.py'],'symbolic_results.json',lambda x:x.get('all_checks_passed') is True and len(x.get('checks',[]))==16 and all(c.get('passed') is True for c in x['checks'])),
      (['code/coefficient_certificate.py'],'coefficient_certificate_results.json',lambda x:x.get('status')=='exact_rational_rounded_coefficient_bound_passed'),
      (['code/evidence_guard.py'],'bound_search_results.json',lambda x:x.get('status')=='proved' and x.get('evidence_guard',{}).get('passed') is True and x.get('scenario_results',{}).get('full_selected_regulator',{}).get('certified_cost')==14),
    ]
    records=[]
    for args,path,predicate in jobs:
        try:record=execute(args,path,predicate)
        except Exception as exc:record={'args':args,'passed':False,'error':f'{type(exc).__name__}: {exc}'}
        records.append(record);print(args[0]+': '+('PASS' if record['passed'] else 'FAIL'),flush=True)
    report={'passed':all(r['passed'] for r in records),'commands':records,'python':platform.python_version(),'optimized':sys.flags.optimize,'scope':'Round-six regression fixes and exact finite-model checks; no continuum or trajectory enclosure claim.'}
    (ROOT/'code_validation_results.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
