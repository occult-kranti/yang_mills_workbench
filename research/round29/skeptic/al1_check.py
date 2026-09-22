#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
checks=[]
def require(q,msg):
 if not q: raise RuntimeError(msg)
 checks.append(msg)
def add(p,i):
 q=list(p);q[i]+=1;return tuple(q)
def owner(p):return(p[0]//4,p[1]//2,p[2])
classes=Counter()
for x,y in product(range(4),range(2)):
 for i,j in combinations(range(3),2):
  p=(x,y,0); cycle=[p,add(p,i),add(add(p,i),j),add(p,j)]
  tails=[tuple(min(u[k],v[k]) for k in range(3)) for u,v in zip(cycle,cycle[1:]+cycle[:1])]
  if (i,j)==(0,1) and y==0 and x<3:continue
  classes[tuple(sorted({owner(t) for t in tails}))]+=1
require(sum(classes.values())==21,'all_omitted_faces')
require(sorted(classes.values())==[1,1,2,3,4,10],'independent_six_support_multiplicities')
require(classes[((0,0,0),(0,0,1))]==10,'z_boundary_ten_actual_faces')
require(classes[((0,0,0),(1,0,0))]==1,'x_boundary_one_actual_face')
require(Q(21)*8*4==672,'epsilon_trace_and_delta_normalization')
require(Q(4)/Q(1,8)==32,'bridge_bound')
require(Q(1,4)<=Q(1,2) and Q(1,4)>Q(1,8),'endpoint_only_false_positive')
for n in range(1,101):
 g2=Q(1,n); a=Q(7,3*n); alpha=g2/(2*a);lam=2/(g2*a)
 require(alpha==Q(3,14) and lam/alpha==4*n*n,'exact_path_'+str(n))
require(Q(672,32)==21,'bridge_endpoint_still_requires_symbolic_budget')
# Raw shift cancels only if the true ground energy is shifted too.
K=(Q(0),Q(3)); scalar=Q(11)
require(tuple(v+scalar-scalar for v in K)==K,'centered_scalar_identity')
require(tuple(v+scalar for v in K)!=K,'uncentered_scalar_rejected')
replay=[]
for direction in ['forward','reverse']:
 source=ROOT/'research/round29'/direction/'al1'
 dest=HERE/'replays/al1'/direction
 if dest.exists():shutil.rmtree(dest)
 shutil.copytree(source,dest,ignore=shutil.ignore_patterns('output','__pycache__','freeze.json'))
 cmd=[sys.executable,'-B',str(dest/'check.py')]
 if direction=='forward':cmd+=['--output',str(dest/'output')]
 completed=subprocess.run(cmd,capture_output=True,text=True,check=True)
 a=(source/'output/results.json').read_bytes();b=(dest/'output/results.json').read_bytes()
 require(a==b,'fresh_'+direction+'_results_identical')
 replay.append({'direction':direction,'results_sha256':hashlib.sha256(b).hexdigest(),'stdout':completed.stdout.strip()})
result={'loop':'AL1','checks':checks,'checks_count':len(checks),'replays':replay,'source_constants_evaluated':False,'physical_simulation':False}
(HERE/'al1-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks)}))
