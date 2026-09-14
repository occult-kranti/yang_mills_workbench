#!/usr/bin/env python3
"""Replay inherited C2 admission holes, then require repaired rejection."""
from pathlib import Path
import importlib.util,json,hashlib
from fractions import Fraction
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[4]
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
oldpath=ROOT/'research/round19/backward/c2/history/pre-round20-validator-audit/compare.py'
newpath=ROOT/'research/round19/backward/c2/compare.py'
old=module(oldpath,'old_c2');new=module(newpath,'new_c2')
prod=new.normalize(new.load_output(ROOT/'research/round19/forward/c2/output'))
exp=new.normalize(new.load_output(ROOT/'research/round19/backward/c2/output'))
a=deepcopy(prod);a['asymmetry']['H']='1000';a['asymmetry']['range']='0 < kappa <= 1000'
b=deepcopy(prod);c=b['primary'];c['exp_upper_E']='1';c['quotient_coefficient_lower']=c['C_N'];c['target_margin']=str(Fraction(c['C_N'])-Fraction(c['target_coefficient']))
rows=[]
for name,obj in [('baseline',prod),('widen_asymmetry_to_1000',a),('invalid_exp_bound_E1',b)]:
 rows.append({'name':name,'old_failures':old.admission_failures(obj,exp),'repaired_failures':new.admission_failures(obj,exp)})
if rows[0]['old_failures'] or rows[0]['repaired_failures'] or any(r['old_failures'] or not r['repaired_failures'] for r in rows[1:]):
 raise RuntimeError('audit reproduction did not exhibit expected old/new behavior')
out={'status':'passed','rows':rows,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [oldpath,newpath,Path(__file__)]}}
(Path(__file__).parent/'c2-mutation-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2))
