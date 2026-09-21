#!/usr/bin/env python3
"""Root-advisor gate creation after mathematical review, followed by independent replay."""
import argparse,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from admission import ROOT,ROUND,LOOPS,read,source,digest,submission,require
import json
p=argparse.ArgumentParser();p.add_argument('loop',choices=LOOPS);p.add_argument('--verdict',required=True,choices=['accepted_within_scope','limited','insufficient']);a=p.parse_args()
prefix=f'{ROUND}/advisor/{a.loop}'
target=ROOT/(prefix+'-gate.json');require(not target.exists(),'historical gate already exists')
files={};ss={};pp={}
for d in ('forward','reverse'):
    s,data=submission(a.loop,d);ss[d]=s;pp[d]=data
    files.update(s['files']);name=f'{ROUND}/{d}/{a.loop}/submission.json';files[name]=digest(source(name))
for name in [f'{ROUND}/skeptic/{a.loop}-review.md',prefix+'-decision.md']:
    files[name]=digest(source(name))
g={'schema':'ym24-gate-v1','loop':a.loop,'reviewed':True,'verdict':a.verdict,'review_mode':'independent model-agent review; not external peer review','submissions':ss,'payloads':pp,'files':files,'scope':'Checks and source integrity are reproducible; the written mathematical argument and skeptical decision establish only the declared scope.'}
target.write_text(json.dumps(g,indent=2,sort_keys=True)+'\n');print(a.loop+' recorded')
