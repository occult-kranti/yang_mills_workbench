#!/usr/bin/env python3
"""Execute deliberately wrong source clones against independent exact equations."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib
from audit_solver import load,divergence_kinetic,my_basis

ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);args=ap.parse_args()
path=args.source.resolve();original=path.read_text();outdir=Path(__file__).parent/'source_mutants';outdir.mkdir(exist_ok=True)
def sh(s):return hashlib.sha256(s.encode()).hexdigest()
mutations={
 'shared_cross_sign': [('-r/2)','r/2)')],
 'independent_rotors': [('-r/2)','F(0))'),('else F(9,2)','else F(6)'),('else F(-3,2)','else F(-2)'),
                         ('deriv(deriv(p,0),2)),F(-3,2))','deriv(deriv(p,0),2)),F(-2))'),
                         ('deriv(deriv(p,1),2)),F(-3,2))','deriv(deriv(p,1),2)),F(-2))')],
 'magnetic_diagonal_in_tail': [('F(5,8)*d*d+2*d+F(3,8)*(d%2)','F(5,8)*d*d+2*d+F(3,8)*(d%2)+2')],
}
records=[]
for name,replacements in mutations.items():
    source=original
    for before,after in replacements:
        count=source.count(before)
        if count!=1:raise RuntimeError(f'{name}: expected one source match for {before!r}, found {count}')
        source=source.replace(before,after,1)
    target=outdir/(name+'.py');target.write_text(source);m=load(target,'mutant_'+name)
    failures=[]
    if name=='magnetic_diagonal_in_tail':
        exact=min(m.free_energy(k) for k in my_basis(3) if sum(k)==3)
        wrong=m.tail_lower(2)
        if wrong!=exact:failures.append({'fixture':'first omitted degree3','correct':str(exact),'wrong':str(wrong)})
    else:
        for k in my_basis(2):
            actual=m.kinetic({k:F(1)});expected=divergence_kinetic({k:F(1)})
            if actual!=expected:failures.append({'monomial':list(k),'correct':str(expected),'wrong':str(actual)})
    if not failures:raise RuntimeError('wrong model was not detected: '+name)
    records.append({'mutation':name,'source_sha256':sh(source),'detected':True,'failures':failures,'source_file':str(target.relative_to(Path(__file__).parent))})
result={'status':'all-source-mutations-rejected','optimized_python':not __debug__,'production_source_sha256':sh(original),
        'mutation_runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'records':records}
dest=Path(__file__).with_name('source_mutation_results.json');dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'count':len(records),'production_source_sha256':result['production_source_sha256']}))
