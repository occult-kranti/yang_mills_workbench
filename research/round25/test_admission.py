"""Reject dropped proof bindings and false attribution without modifying evidence."""
import copy,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parent
ns=runpy.run_path(str(R/'admission.py'));checked=0
for loop in ['aa1','aa2']:
    g=json.loads((R/f'advisor/{loop}-gate.json').read_text());ns['metadata'](g,loop)
    mutations=[]
    for suffix in ['report.md','check.py','output/results.json']:
        d=copy.deepcopy(g);del d['sha256'][f'research/round25/solo/{loop}/'+suffix];mutations.append(d)
    d=copy.deepcopy(g);d['review']='independent peer review';mutations.append(d)
    d=copy.deepcopy(g);d['normal_optimized_equal']='true';mutations.append(d)
    d=copy.deepcopy(g);d['verdict']='solved_continuum';mutations.append(d)
    for d in mutations:
        try:ns['metadata'](d,loop)
        except ValueError:checked+=1
        else:raise ValueError('mutation admitted')
print(json.dumps({'status':'passed','rejected_mutations':checked,'research_loops_added':0}))
