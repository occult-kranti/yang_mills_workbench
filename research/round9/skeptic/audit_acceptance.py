"""Rerun repaired evidence/proof gates without executing Monte Carlo."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('YM9_REVIEW_ROOT',str(HERE.parent))).resolve()
LAT=ROOT/('lattice' if (ROOT/'lattice').exists() else 'ym9-lattice')
ADV=ROOT/('advisor' if (ROOT/'advisor').exists() else 'ym9-advisor')
PROOF=ROOT if (ROOT/'proof_routes.py').exists() else ROOT/'physics-observatory/research/round9'
checks=[]


def load(name,path):
    sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module


def gate(name,ok,**evidence):checks.append({'name':name,'passed':bool(ok),**evidence})


def main():
    R=load('skeptic_runner',LAT/'run_experiments.py')
    evidence=json.loads((LAT/'results/deterministic_checks_current.json').read_text())
    R.validate_deterministic_evidence(evidence)
    gate('current_nonempty_source_bound_lattice_tests',evidence['tests_run']==12)
    variants={'empty_success':{'successful':True,'tests_run':0,'failures':0,'errors':0}}
    for name,key,value in [('source_changed','source_sha256',{}),('test_omitted','test_names_run',evidence['test_names_run'][:-1]),('test_skipped','skipped',1),('failure_count','failures',1)]:
        variant=copy.deepcopy(evidence);variant[key]=value;variants[name]=variant
    for name,variant in variants.items():
        try:R.validate_deterministic_evidence(variant)
        except RuntimeError as exc:gate(name+'_rejected',True,reason=str(exc))
        else:gate(name+'_rejected',False)
    manifest=json.loads((LAT/'results/experiment_manifest.json').read_text())
    for name,digest in manifest['source_sha256_before'].items():
        path=LAT/'results/executed_sources'/name
        gate('executed_source_preserved_'+name,hashlib.sha256(path.read_bytes()).hexdigest()==digest)

    P=load('skeptic_routes',PROOF/'proof_routes.py')
    route_records=[]
    for name,lib in P.build().items():
        out=P.plan(lib)
        expected='proved' if name in ['complete_hierarchy','group_convolution','conditional_stability'] else 'not_derivable'
        gate('route_'+name,out['status']==expected,status=out['status'])
        route_records.append({'name':name,'status':out['status'],'cost':out.get('certified_cost')})
    for route,premise in [('complete_hierarchy','H_domain'),('conditional_stability','T_reference'),('conditional_stability','T_budget'),('conditional_stability','T_domain')]:
        lib=copy.deepcopy(P.build()[route]);lib['initial_facts'].remove(premise)
        out=P.plan(lib);gate('held_out_premise_'+premise,out['status']=='not_derivable')
    mutant=copy.deepcopy(P.build()['yang_mills_prize']);mutant['initial_facts'].append('Y_prize')
    try:P.plan(mutant)
    except P.ContractError:gate('prize_cannot_be_assumed_as_proved',True)
    else:gate('prize_cannot_be_assumed_as_proved',False)

    outputs=[]
    for optimize in [False,True]:
        flag=['-O'] if optimize else []
        output=HERE/f'advisor_exact_{"optimized" if optimize else "normal"}.json'
        proc=subprocess.run([sys.executable,*flag,str(ADV/'check_exact_counterexamples.py'),'--output',str(output)],capture_output=True,text=True)
        gate('advisor_explicit_gates_'+str(optimize),proc.returncode==0)
        if proc.returncode==0:outputs.append(json.loads(output.read_text()))
        failure=HERE/f'advisor_injected_failure_{optimize}.json'
        if failure.exists():failure.unlink()
        bad=subprocess.run([sys.executable,*flag,str(ADV/'check_exact_counterexamples.py'),'--inject-failure','--output',str(failure)],capture_output=True,text=True)
        gate('advisor_failed_gate_rejects_'+str(optimize),bad.returncode!=0 and not failure.exists(),returncode=bad.returncode)
    gate('optimized_normal_same_nonempty_gate_records',len(outputs)==2 and outputs[0]['executed_gates']==outputs[1]['executed_gates'] and outputs[0]['executed_gate_count']==68)

    source_files=[LAT/'run_experiments.py',LAT/'su2_lattice.py',ADV/'check_exact_counterexamples.py',PROOF/'proof_routes.py',PROOF/'proof_search.py',Path(__file__)]
    report={'passed':bool(checks) and all(c['passed'] for c in checks),'count':len(checks),'checks':checks,
            'failures':[c for c in checks if not c['passed']],'routes':route_records,
            'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
            'scope':'Executable acceptance and conditional Horn-route checks, not semantic proof-kernel verification; no Monte Carlo rerun'}
    (HERE/'acceptance_audit.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    print(json.dumps({k:report[k] for k in ['passed','count','failures']},indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
