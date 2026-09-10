#!/usr/bin/env python3
"""Fresh-process independent reconstruction before any proof seed is admitted."""
from pathlib import Path
from fractions import Fraction as Q
import json, subprocess, sys
HERE=Path(__file__).resolve().parent

def main(output):
    # Caller executes this file over a frozen byte snapshot, in a fresh interpreter.
    commands=[('loop1',[sys.executable,str(HERE/'backward/loop1/verify_loop1.py'),'--producer',str(HERE/'forward/loop1'),'--scale',str(HERE/'advisor'),'--output',str(HERE/'admission-loop1')]),
              ('loop2',[sys.executable,str(HERE/'backward/loop2/verify_loop2.py'),'--producer',str(HERE/'forward/loop2'),'--output',str(HERE/'admission-loop2')])]
    reports={}
    for name,command in commands:
        p=subprocess.run(command,cwd=HERE,capture_output=True,text=True,timeout=120)
        if p.returncode:raise ValueError('Independent '+name+' replay failed: '+p.stderr[-1000:])
        report=json.loads((HERE/('admission-'+name)/'review.json').read_bytes())
        if report.get('status')!='passed' or type(report.get('checks_count')) is not int or report['checks_count']<=0:raise ValueError('Absent semantic acceptance '+name)
        reports[name]={'checks':report['checks_count'],'status':report['status']}
    collection=json.loads((HERE/'forward/loop2/output/collection.json').read_bytes())
    primary=collection['refinement'][-1]
    lo,hi=map(Q,primary['difference_interval'])
    if collection['primary_index']!=4 or primary['degree']!=24 or primary['status']!='target-met' or lo<=0 or hi-lo>Q(1,10**12):raise ValueError('Primary target not established')
    graph=json.loads((HERE/'forward/loop1/output/exact_evidence.json').read_bytes())
    if graph['references']['outer10_shared_square']['moment']!='1/524288' or graph['face_edge_rank_mod2']!=9:raise ValueError('Graph premises absent')
    result={'status':'passed','gates':sorted(['graph_gate','haar_gate','coefficient_gate','remainder_gate','difference_gate','scale_gate']),
            'independent':reports,'primary_difference':primary['difference_interval'],'primary_width':str(hi-lo),
            'scope':'Fresh finite arithmetic plus reviewed graph and scaling derivations. No unproved physical-generator, local-uniform or continuum premises.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: replay_evidence.py OUTPUT_JSON')
    main(sys.argv[1])
