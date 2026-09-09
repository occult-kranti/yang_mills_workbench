#!/usr/bin/env python3
"""Review a self-contained copied proof wrapper; all mutations stay in that copy."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys
ap=argparse.ArgumentParser();ap.add_argument('probe',type=Path);args=ap.parse_args();root=args.probe.resolve()
def load(p,name):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
m=load(root/'proof_routes.py','reviewed_proof_routes');manifest,frozen=m.checked_inputs();records=[]
def check(ok,name,detail=None):
    if not ok:raise RuntimeError(name)
    records.append({'test':name,'passed':True,'detail':detail})
def rejects(fn,name):
    try:fn()
    except (ValueError,RuntimeError,KeyError,TypeError) as e:records.append({'test':name,'passed':True,'rejection':str(e)});return
    raise RuntimeError('Unexpected acceptance: '+name)
mf=root/'proof_manifest.json';original=mf.read_bytes()
for name,change in [('empty',lambda x:x.__setitem__('sha256',{})),
                    ('missing',lambda x:x['sha256'].pop('advisor/advisor.md')),
                    ('extra',lambda x:x['sha256'].__setitem__('unreviewed.py','0'*64)),
                    ('bad_digest',lambda x:x['sha256'].__setitem__('advisor/advisor.md','Q'*64)),
                    ('wrong_digest',lambda x:x['sha256'].__setitem__('advisor/advisor.md','0'*64))]:
    changed=copy.deepcopy(manifest);change(changed);mf.write_text(json.dumps(changed))
    rejects(m.checked_inputs,'manifest_rejects.'+name);mf.write_bytes(original)
advisor=root/'advisor/advisor.md';raw=advisor.read_bytes();target=root/'advisor/same_bytes_target.md';target.write_bytes(raw)
advisor.unlink();advisor.symlink_to(target.name)
try:rejects(m.checked_inputs,'same_bytes_symlink_rejected')
finally:advisor.unlink();advisor.write_bytes(raw);target.unlink()
advisor.write_bytes(raw+b'\nChanged after review.\n')
try:rejects(m.checked_inputs,'changed_theorem_bytes_rejected')
finally:advisor.write_bytes(raw)
check(m.replay_arithmetic(frozen)['conservative_lower']=='24/25','full_arithmetic_and_conservative_rectangle')
collection=json.loads(frozen['solver/output/stationary_certificates.json'])
for name,change in [('empty',lambda c:c.__setitem__('certificates',[])),('scope',lambda c:c.__setitem__('scope','continuum')),('outer_field_missing',lambda c:c.pop('contract'))]:
    changed=copy.deepcopy(collection);change(changed);f=frozen.copy();f['solver/output/stationary_certificates.json']=json.dumps(changed).encode()
    rejects(lambda:m.replay_arithmetic(f),'stationary_schema_rejects.'+name)
cover=json.loads(frozen['solver/output/continuous_rectangle_certificate.json'])
for name,change in [('hole',lambda c:c['cells'].pop()),('false_margin',lambda c:c.__setitem__('gap_lower','1')),
                    ('wrong_lipschitz',lambda c:c.__setitem__('gap_lipschitz_l1','1')),('typed_positive',lambda c:c.__setitem__('positive',1))]:
    changed=copy.deepcopy(cover);change(changed);f=frozen.copy();f['solver/output/continuous_rectangle_certificate.json']=json.dumps(changed).encode()
    rejects(lambda:m.replay_arithmetic(f),'rectangle_replay_rejects.'+name)
# A real post-read disk mutation cannot substitute the compiled frozen solver
# or its source identity. Its bytes are restored before the manifest replay.
solver=root/'solver/two_plaquette.py';raw=solver.read_bytes();solver.write_text("raise RuntimeError('post-read solver substitution executed')\n")
try:check(m.replay_arithmetic(frozen)['centers']==9,'frozen_solver_exec_and_digest_after_disk_change')
finally:solver.write_bytes(raw)
search=m.load_frozen('reviewed_frozen_search','proof_search.py',frozen);base=m.make_library()
check(search.plan(base)['status']=='proved','rectangle_route')
heat=copy.deepcopy(base);heat['goals']=['C_all_finite'];check(search.plan(heat)['status']=='proved','analytic_route')
for name,atom in [('gauss','C_gauss'),('point_arithmetic','C_exact_points'),('cover','C_exact_cover')]:
    v=copy.deepcopy(base);v['initial_facts'].remove(atom);check(search.plan(v)['status']=='not_derivable','withhold.'+name)
for name,atom in [('shared_operator','C_kinetic'),('tail','C_tail')]:
    v=copy.deepcopy(base);v['rules']=[r for r in v['rules'] if r['conclusion']!=atom];check(search.plan(v)['status']=='not_derivable','withhold.'+name)
prize=copy.deepcopy(base);prize['goals']=['C_millennium'];check(search.plan(prize)['status']=='not_derivable','continuum_remains_underivable')
prize['initial_facts'].append('C_millennium');rejects(lambda:search.plan(prize),'target_cannot_be_seed')
for name,change in [('unsafe_review',lambda v:v['rules'][0].__setitem__('review_status','unreviewed')),
                    ('cross_scope',lambda v:v['nodes'][0].__setitem__('scope','different')),
                    ('bool_cost',lambda v:v['rules'][0].__setitem__('cost',True))]:
    v=copy.deepcopy(base);change(v);rejects(lambda:search.plan(v),'typed_graph_rejects.'+name)
# Preserve the initial observed schema defect as a deliberately reconstructed
# code mutation; the parent corrected it before the first file snapshot.
legacy_source=(root/'proof_routes.py').read_text()
start=legacy_source.index("    collection=json.loads(frozen['solver/output/stationary_certificates.json'])")
end=legacy_source.index("    cover=json.loads",start)
legacy_source=legacy_source[:start]+"    certificates=json.loads(frozen['solver/output/stationary_certificates.json'])\n"+legacy_source[end:]
legacy_path=root/'initial_schema_mutation.py';legacy_path.write_text(legacy_source)
legacy=load(legacy_path,'reconstructed_initial_schema')
rejects(lambda:legacy.replay_arithmetic(frozen),'retained_initial_schema_failure')
check(m.checked_inputs()[0]==manifest,'copied_proof_inputs_restored')
result={'status':'passed','optimized_python':not __debug__,'gate_count':len(records),'records':records,
        'reviewed_hashes':manifest['sha256'],'reconstructed_initial_schema_sha256':hashlib.sha256(legacy_source.encode()).hexdigest(),
        'initial_schema_note':'Initial mismatch was reported from source review and corrected before this copied snapshot; retained mutation reproduces that exact schema failure.',
        'limits':'Typed Horn planning replays admitted conventional mathematical implications; it does not independently prove their analytic contents or any continuum claim.'}
dest=Path(__file__).with_name('proof_audit_results.json');dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'gate_count':len(records),'wrapper_sha256':manifest['sha256']['proof_routes.py'],'optimized_python':not __debug__}))
