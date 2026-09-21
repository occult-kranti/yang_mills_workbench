#!/usr/bin/env python3
"""Verify a clean committed ten-loop candidate, including its published data."""
import argparse, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE='7765e2c7ecc56c6b33b28a88b020a0b4aa8f13ca'
LOOPS=['v1','v2','w1','w2','x1','x2','y1','y2','z1','z2']
def require(ok,message):
    if not ok: raise ValueError(message)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-commit',required=True);a=p.parse_args()
    out=a.output
    require(out.is_absolute() and not out.exists() and not out.resolve().is_relative_to(ROOT.resolve()),'fresh external output required')
    require(git('rev-parse','HEAD')==a.expected_commit,'unexpected commit')
    require(subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=ROOT,capture_output=True).returncode==1,'detached checkout required')
    require(not git('status','--porcelain','--untracked-files=all'),'dirty candidate')
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
    for line in git('diff','--name-status',BASE,'HEAD','--','research').splitlines():
        status,name=line.split('\t')
        require(status=='A' and name.startswith('research/round24/'),'historical research changed: '+name)
    require(not git('diff',BASE,'HEAD','--','AGENTS.md','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md'),'bound live guidance changed')
    roadmap=json.loads((ROOT/'research/round24/advisor/roadmap.json').read_text())
    require(roadmap['completed_loops']==LOOPS,'wrong completed loop set')
    require(roadmap.get('cycle_complete') is True and roadmap.get('next_loop_started') is False,'stop boundary missing')
    figure=json.loads((ROOT/'research/round24/advisor/figure-review.json').read_text())
    require(figure.get('visually_inspected') is True and figure.get('scope')=='analytic W1 lower-bound plot','missing figure review')
    require({'dist/round24-residual-bound.svg','research/round24/build_figures.py','research/round24/advisor/w1-gate.json'}<=set(figure['files']),'incomplete figure binding')
    for name,expected in figure['files'].items():require(digest(ROOT/name)==expected,'figure changed after inspection')
    # Public artifacts must not contain credentials. Never print any matching text.
    for name in git('diff','--name-only',BASE,'HEAD').splitlines():
        path=ROOT/name
        if path.is_file():require(not re.search(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-proj-[A-Za-z0-9_-]{20,})',path.read_bytes()),'credential pattern in outgoing artifact')
    out.mkdir(parents=True);records={}
    def run(label,command):
        cp=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        log=out/(label+'.log');log.write_text(cp.stdout+cp.stderr)
        require(cp.returncode==0,'failed check: '+str(log))
        records[label]={'exit_code':0,'log_sha256':digest(log)}
    py=sys.executable
    for optimized in (False,True):
        label='optimized' if optimized else 'normal';mode=['-O'] if optimized else []
        run('round24_'+label,[py,'-B',*mode,'research/round24/admission.py','--loops',*LOOPS,'--output',str(out/('round24-'+label)),*(['--optimized'] if optimized else [])])
        run('round23_'+label,[py,'-B',*mode,'research/round23/reproduce.py','--output',str(out/('round23-'+label)),*(['--optimized'] if optimized else [])])
        run('admission_'+label,[py,'-B',*mode,'research/round24/test_admission.py','--output',str(out/('admission-'+label+'.json'))])
        run('skill_test_'+label,[py,'-B',*mode,'research/round24/skill-tests/separated-shift/check.py'])
        reproduced=json.loads((out/('round24-'+label)/'reproduction.json').read_text())
        require([row['loop'] for row in reproduced['loops']]==LOOPS,'missing or duplicated replay')
        historical=json.loads((out/('round23-'+label)/'reproduction.json').read_text())
        require(historical['loops']==['s1','s2','t1','t2','u1','u2'] and len(historical['executions'])==12,'historical replay incomplete')
    require((out/'admission-normal.json').read_bytes()==(out/'admission-optimized.json').read_bytes(),'admission mode drift')
    require((out/'skill_test_normal.log').read_bytes()==(out/'skill_test_optimized.log').read_bytes(),'skill-test mode drift')
    (ROOT/'dist/research-round24-data.js').unlink();shutil.rmtree(ROOT/'docs')
    run('data_build',[py,'-B','research/round24/build_site.py'])
    run('pages_build',[py,'-B','scripts/build_pages.py'])
    require(not git('status','--porcelain','--untracked-files=all'),'fresh build differs from committed tree')
    for name in ('test_round24','test_round23','test_round22','test_workbench','test_journey'):
        run(name,['node','tests/'+name+'.mjs'])
    require(not git('status','--porcelain','--untracked-files=all'),'checks modified candidate')
    receipt={'schema':'ym24-release-v1','status':'passed','local_commit':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}'),'baseline':BASE,'clean_detached':True,'historical_research_unchanged':True,'completed_loops':LOOPS,'research_loops_added_by_release':0,'new_producer_executions':40,'historical_producer_executions':24,'checks':records,'review_mode':'independent model-agent review; not external peer review','browser_visual_audit':False,'scientific_figure_visual_inspection':True,'continuum_status':'open'}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','tree':receipt['tree'],'receipt_sha256':digest(out/'receipt.json')}))
if __name__=='__main__':main()
