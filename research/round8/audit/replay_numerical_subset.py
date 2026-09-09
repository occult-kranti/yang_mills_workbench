"""Replay only non-SymPy branches of the archived independent checker.

SymPy is unavailable in this environment. Remove that import from an in-memory
AST, execute exactly the archived numerical function definitions, and report
symbolic branches blocked. Neither historical source nor its results are edited.
"""
from pathlib import Path
import ast
import hashlib
import json
import sys
import types
HERE=Path(__file__).resolve().parent
source=HERE/'replay/qeg-research/round7/independent_checks.py'
tree=ast.parse(source.read_text(),filename=str(source))
tree.body=[node for node in tree.body if not (isinstance(node,ast.Import) and any(a.name=='sympy' for a in node.names))]
mod=types.ModuleType('r7_independent_numerical_subset')
mod.__file__=str(source)
sys.modules[mod.__name__]=mod
exec(compile(tree,str(source),'exec'),mod.__dict__)
cuts=mod.cutoff_checks()
scalar=mod.numerical_scalar()
result={'status':'passed_scoped_subset','passed_checks':len(mod.GATES),'gates':mod.GATES,
        'blocked':['symbolic()','finite_bridge_checks()'],
        'reason':'SymPy unavailable in both advertised Python runtimes; no symbolic identities counted as rerun',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'source_change':'In-memory AST omits only unavailable SymPy import. No numerical function definition changed.',
        'cutoff_samples':cuts,'scalar_benchmark':scalar}
(HERE/'independent_numerical_subset.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({'status':result['status'],'passed_checks':len(mod.GATES),'blocked':result['blocked']}))
