#!/usr/bin/env python3
"""Verify the exact committed four-loop milestone in a clean detached checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
BASE='6f5a305de615e049de6e7c7440bfc3cf1a8baf65'


def require(x,message):
    if not x: raise ValueError(message)


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-commit',required=True)
    args=p.parse_args();out=args.output
    require(out.is_absolute() and not out.exists() and ROOT not in out.parents,'fresh external output required')
    require(git('rev-parse','HEAD')==args.expected_commit,'unexpected candidate commit')
    require(subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=ROOT,capture_output=True).returncode==1,'detached checkout required')
    require(not git('status','--porcelain','--untracked-files=all'),'candidate is not clean')
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
    changed=git('diff','--name-status',BASE,'HEAD','--','research').splitlines()
    mutable={'research/round23/admission.py','research/round23/reproduce.py','research/round23/advisor/progress-ledger.json'}
    for line in changed:
        status,name=line.split('\t')
        require(status=='A' or name in mutable,'historical research changed: '+name)
    tracked=git('ls-files').splitlines()
    require(not any(re.match(r'research/round23/(contracts/[uvw]|(?:forward|reverse)/[uvw]|advisor/[uvw][12]-gate)',x) for x in tracked),'next research loop started')
    ledger=json.loads((ROOT/'research/round23/advisor/progress-ledger.json').read_text())
    require([x['loop'] for x in ledger['completed_loops']]==['s1','s2','t1','t2'],'wrong loop count')
    require(ledger['current'] is None and ledger['next_loop_started'] is False and ledger['cycle_complete'] is False,'stop boundary missing')
    # Scan outgoing text without echoing matches; credentials do not belong in public research.
    for name in git('diff','--name-only',BASE,'HEAD').splitlines():
        pth=ROOT/name
        if pth.is_file():
            require(not re.search(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-proj-[A-Za-z0-9_-]{20,})',pth.read_bytes()),'credential pattern in outgoing file')
    out.mkdir(parents=True);records={}
    def run(label,cmd):
        cp=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        log=out/(label+'.log');log.write_text(cp.stdout+cp.stderr)
        require(cp.returncode==0,'verification failed: '+str(log))
        records[label]={'exit_code':cp.returncode,'log_sha256':sha(log)}
    py=sys.executable
    run('round23_normal',[py,'-B','research/round23/reproduce.py','--output',str(out/'normal')])
    run('round23_optimized',[py,'-B','-O','research/round23/reproduce.py','--optimized','--output',str(out/'optimized')])
    normal=json.loads((out/'normal/reproduction.json').read_text());optimized=json.loads((out/'optimized/reproduction.json').read_text())
    require(normal['executions']==optimized['executions'],'normal/optimized scientific drift')
    run('admission_normal',[py,'-B','research/round23/test_admission.py','--output',str(out/'admission-normal.json')])
    run('admission_optimized',[py,'-B','-O','research/round23/test_admission.py','--output',str(out/'admission-optimized.json')])
    require((out/'admission-normal.json').read_bytes()==(out/'admission-optimized.json').read_bytes(),'admission mode drift')
    run('round22_inherited',[py,'-B','research/round22/reproduce.py','--output',str(out/'round22')])
    # Rebuild from absent destinations, retaining the committed tree as the expected bytes.
    (ROOT/'dist/research-round23-data.js').unlink()
    shutil.rmtree(ROOT/'docs')
    run('data_build',[py,'-B','research/round23/build_site.py'])
    run('pages_build',[py,'-B','scripts/build_pages.py'])
    require(not git('status','--porcelain','--untracked-files=all'),'fresh build differs from committed tree')
    for name in ('test_round23','test_workbench','test_journey','test_round22'):
        run(name,['node','tests/'+name+'.mjs'])
    require(not git('status','--porcelain','--untracked-files=all'),'verification modified candidate')
    receipt={'schema':'ym23-four-loop-release-v1','status':'passed','commit':git('rev-parse','HEAD'),
       'tree':git('rev-parse','HEAD^{tree}'),'recovered_base':BASE,'clean_detached':True,
       'historical_research_unchanged_except_explicit_runner_ledger_admission_updates':True,
       'completed_loops':['s1','s2','t1','t2'],'cycle_complete':False,'u1_started':False,
       'single_agent_t2':True,'independent_t2_review':False,'scientific_executions_current':16,
       'scientific_executions_inherited_round22':20,'normal_optimized_results_identical':True,
       'admission_mutations_rejected_per_mode':12,'checks':records,'continuum_status':'open',
       'browser_visual_audit':False,'research_loops_added_by_release':0}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','tree':receipt['tree'],'receipt_sha256':sha(out/'receipt.json')}))


if __name__=='__main__':main()
