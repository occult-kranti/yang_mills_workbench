#!/usr/bin/env python3
"""Preserved pre-fix solver snapshot and literal initial exactness-API fixture."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,hashlib,sys,copy

p=Path(__file__).with_name('initial_precision_solver.py')
spec=importlib.util.spec_from_file_location('initial_precision_solver',p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

def initial_coupling_square(degree,lambda1,lambda2,rho=F(1)):
    # Literal function body inspected before the first API fix; it calls current
    # helper algebra because those helper functions were unchanged by that fix.
    bs,G,_,MX,MY=m.matrices(degree,rho);n=len(bs)
    W=m.add(m.X,m.Y,lambda2/lambda1) if lambda1 else {k:v*lambda2 for k,v in m.Y.items()}
    if lambda1: W={k:v*lambda1 for k,v in W.items()}
    WP=[m.mul(W,{p:F(1)}) for p in bs]
    W2=[[m.inner(p,q) for q in WP] for p in WP]
    M=[[lambda1*MX[i][j]+lambda2*MY[i][j] for j in range(n)] for i in range(n)]
    solved=m.solve_exact(G,M)
    return [[W2[i][j]-sum((M[i][k]*solved[k][j] for k in range(n)),F(0)) for j in range(n)] for i in range(n)]

direct=initial_coupling_square(1,22,15);rational=initial_coupling_square(1,F(22),F(15))
types=sorted({type(v).__name__ for row in direct for v in row})
if types==['Fraction'] or direct==rational: raise RuntimeError('initial int-division mutation did not fail')
c=m.certificate(1,10**20+1,0,0)
try: m.verify_certificate(c)
except ValueError as e: rejection=str(e)
else: raise RuntimeError('initial insufficient precision was not rejected by replay')
typed=m.certificate(2,1,1,1);typed['A_brackets'][0]['lower_inertia'][0]=False
accepted_false_count=m.verify_certificate(typed)
rectangle=m.rectangle_certificate([m.certificate(2,1,i,j) for i in range(3) for j in range(3)])
rectangle['positive']=1;accepted_integer_positive=m.verify_rectangle(rectangle)
if not (accepted_false_count and accepted_integer_positive): raise RuntimeError('initial metadata loopholes did not reproduce')
result={'status':'expected-initial-defects-reproduced','optimized_python':not __debug__,
        'snapshot_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
        'reproducer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'literal_first_exactness_defect':{'input':'coupling_square(1,22,15)','wrong_types':types,
          'entrywise_equal_to_rational':direct==rational,'scope':'public API; certificate path supplied Fractions'},
        'initial_precision_defect':{'input':'certificate(1,10**20+1,0,0)',
          'returned_status':c['status'],'requested_width':c['width_requested'],
          'actual_A1_width':str(F(c['A_brackets'][1]['upper'])-F(c['A_brackets'][1]['lower'])),
          'verifier_rejection':rejection},
        'initial_metadata_defects':{'bool_in_inertia_count_accepted':accepted_false_count,
          'integer_rectangle_positive_accepted':accepted_integer_positive,
          'arithmetic_values_changed':False,'semantic_type_contract_broken':True},
        'initial_certificate':c}
out=p.with_name('initial_failures.json');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='initial_certificate'}))
