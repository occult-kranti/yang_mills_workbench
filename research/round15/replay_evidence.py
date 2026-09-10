#!/usr/bin/env python3
"""Fresh-process independent arithmetic admission for the three finite routes."""
from pathlib import Path
from fractions import Fraction as Q
import contextlib,hashlib,importlib.util,io,json,sys
HERE=Path(__file__).resolve().parent

def load(name,path,dependencies=()):
    for dep in dependencies:sys.path.insert(0,str(dep))
    try:
        spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module
    finally:
        for _ in dependencies:sys.path.pop(0)
def read(name):return json.loads((HERE/name).read_bytes())
def digest(name):return hashlib.sha256((HERE/name).read_bytes()).hexdigest()

def main(output):
    gates=[]
    a=load('independent_adaptive',HERE/'backward/A2/verify_adaptive.py')
    ar=a.Review(HERE/'forward').verify(read('forward/A2/output/refinement.json'))
    if ar['status']!='certified-positive-cover' or ar['cells']!=21 or Q(ar['minimum_lower'])<=0:raise ValueError('Complete cover goal failed')
    gates+=['derivative_gate','cover_gate']
    with contextlib.redirect_stdout(io.StringIO()):
        graph=load('independent_cube_graph',HERE/'backward/B1/verify_cube.py',(HERE/'backward/B1',))
        gr=graph.audit(HERE/'forward/B1/graph.json',HERE/'forward/B1/cube.py',HERE/'replayed-graph')
    if gr['status']!='passed' or gr['cube_full_haar_moment']!='1/1024':raise ValueError('Cube graph replay failed')
    gates+=['graph_gate','trial_haar_gate']
    b=load('independent_cube_series',HERE/'backward/B2/verify_series.py',(HERE/'backward/B2',))
    br=b.Review(HERE/'forward').collection(read('forward/B2/output/certificates.json'))
    if Q(br['expectation_width'])>=Q(1,10**12) or Q(br['enclosures']['partition_excess'][0])<=0:raise ValueError('Cube target failed')
    gates+=['cube_tail_gate','cube_target_gate']
    c=load('independent_graph_bound',HERE/'backward/C1/verify_bound.py')
    c.verify_collection(read('forward/C1/output/certificates.json'),digest('forward/C1/spectral_bound.py'))
    gates+=['free_gap_gate','minmax_gate']
    cr=replay_c2()
    gates+=['trial_interval_gate']
    result={'status':'passed','gates':sorted(gates),'A':ar,'B':{'k':br['k'],'width':br['expectation_width'],'partition_excess':br['enclosures']['partition_excess']},'C':cr,
      'scope':'Exact finite evidence plus reviewed conventional derivative, character, spin-network and min-max arguments; no uniform or continuum admission.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');return result

def replay_c2():
    c=load('independent_cube_variational',HERE/'backward/C2/verify_variational.py',(HERE/'backward/C2',))
    c.verify_collection(read('forward/C2/output/certificates.json'),HERE/'forward')
    central=read('forward/C2/output/central_certificate.json')
    c.Review(HERE/'forward').verify(central)
    if central['alpha']!='1' or central['couplings']!=['1/2']*6 or Q(central['certified_gap_lower'])<=0 or central['precision_status']!='target-met':raise ValueError('Central physical bound failed')
    return {'alpha':'1','couplings':['1/2']*6,'certified_gap_lower':central['certified_gap_lower'],'formula_interval':central['gap_bound_interval'],'uniform_goal':'open'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: replay_evidence.py OUTPUT_JSON')
    main(sys.argv[1])
