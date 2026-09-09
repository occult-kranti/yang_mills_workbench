#!/usr/bin/env python3
"""Source-bound proof replay and mutations. ALWAYS copies inputs before mutation."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,shutil,sys

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('round12',type=Path);ap.add_argument('--label',default='proof_audit');a=ap.parse_args();src=a.round12.resolve();root=Path(__file__).resolve().parent/(a.label+'_probe')
    if root==src:raise ValueError('A distinct isolated destination is mandatory')
    if root.exists():shutil.rmtree(root)
    root.mkdir();manifest=json.loads((src/'proof_manifest.json').read_text());names=['proof_manifest.json',*manifest['sha256']]
    baseline={name:(src/name).read_bytes() for name in names}
    for name,raw in baseline.items():p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    spec=importlib.util.spec_from_file_location('reviewed_proof_routes',root/'proof_routes.py');w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w);records=[];defects=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        records.append(dict(test=name,passed=True,detail=detail))
    def restore():
        for name,raw in baseline.items():
            p=root/name
            if p.is_symlink():p.unlink()
            p.write_bytes(raw)
    def rejects(fn,name):
        try:fn()
        except (ValueError,TypeError,KeyError,RuntimeError,FileNotFoundError) as e:check(True,name,str(e));return
        raise RuntimeError('Unexpected acceptance: '+name)
    w.execute();result=json.loads((root/'proof_results.json').read_text())
    expected={'cosine_representation':('proved',6),'exact_piecewise_computed_state':('proved',12),'finite_volume_comparison':('proved',3),'vanishing_bound_is_not_gap_closure':('proved',2),'defined_point_closure_rejected':('proved',3)}
    for name,(status,cost) in expected.items():r=result['routes'][name]['result'];check(r['status']==status and r['certified_cost']==cost,'route.'+name)
    for name in ('cosine_total_error_unavailable','without_degree_bandwidth','without_initial_support','without_absolute_action','without_exact_vector_replay','four_dimensional_yang_mills'):check(result['routes'][name]['result']['status']=='not_derivable','negative_route.'+name)
    _,frozen=w.checked_inputs();search=w.load_frozen('reviewer_search','proof_search.py',frozen);lib=w.make_library(frozen)
    check('validated_time_error_gate' not in lib['initial_facts'] and not any('numeric' in x for x in lib['initial_facts']),'no_hidden_floating_error_seed')
    bad=copy.deepcopy(lib);bad['initial_facts'].append('four_dimensional_yang_mills_gap');rejects(lambda:search.plan(bad),'final_target_cannot_be_seeded')
    for name in ('advisor/advisor.md','solver/drive_bound.py','solver/exact_stepper.py','proof_routes.py','solver/output/exact_step_certificate.json'):
        p=root/name;p.write_bytes(baseline[name]+b' ');rejects(w.checked_inputs,'stale_or_self_source.'+name);restore()
    for name in ('proof_manifest.json','solver/drive_bound.py','solver/output/exact_step_certificate.json'):
        p=root/name;target=p.with_name(p.name+'.samebytes');target.write_bytes(baseline[name]);p.unlink();p.symlink_to(target.name)
        try:rejects(w.checked_inputs,'same_bytes_symlink.'+name)
        finally:restore();target.unlink()
    p=root/'proof_manifest.json';data=json.loads(baseline['proof_manifest.json']);data['sha256'].pop('solver/exact_stepper.py');p.write_text(json.dumps(data));rejects(w.checked_inputs,'manifest_missing_required_source');restore()
    p=root/'solver/drive_bound.py';p.unlink();rejects(w.checked_inputs,'missing_source_before_import');restore()
    # Algebraic mutations operate on an already frozen, otherwise original byte map,
    # thereby testing semantic reconstruction beyond the manifest's byte checksum.
    for name,mutate in [('analytic_bound',lambda c:c['cases'][0]['certificate'].__setitem__('state_error_upper','0')),('duplicate_named_case',lambda c:c['cases'].__setitem__(1,copy.deepcopy(c['cases'][0]))),('numeric_scope',lambda c:c.__setitem__('scope','certified-floating-cosine'))]:
        f=copy.deepcopy(frozen);c=json.loads(f['solver/output/analytic_certificates.json']);mutate(c);f['solver/output/analytic_certificates.json']=json.dumps(c).encode();rejects(lambda:w.replay_arithmetic(f),'semantic.'+name)
    for name,mutate in [('exact_vector',lambda c:c['final_coefficients'][0].__setitem__('real','0')),('exact_fixture',lambda c:c['protocol']['segments'][0].__setitem__('lambda1','1/10')),('renormalized_vector',lambda c:c.__setitem__('computed_vector_was_renormalized',True))]:
        f=copy.deepcopy(frozen);c=json.loads(f['solver/output/exact_step_certificate.json']);mutate(c);f['solver/output/exact_step_certificate.json']=json.dumps(c).encode();rejects(lambda:w.replay_arithmetic(f),'semantic.'+name)
    f=copy.deepcopy(frozen);deps=json.loads(f['solver/dependencies.json']);deps['expected_dependencies'][0]['role']='unreviewed-substitute';f['solver/dependencies.json']=json.dumps(deps).encode();rejects(lambda:w.replay_arithmetic(f),'fixed_historical_dependency_role')
    # A valid but differently specified analytic certificate must not be admitted
    # under one of the named fixtures merely because its label survived.
    w.replay_arithmetic(frozen);db=sys.modules['drive_bound'];f=copy.deepcopy(frozen);c=json.loads(f['solver/output/analytic_certificates.json']);item=next(x for x in c['cases'] if x['case']=='original');old=item['certificate'];p=copy.deepcopy(old['protocol']);p['lambda1_scale']='1/2';item['certificate']=db.certificate(p,old['degree']);f['solver/output/analytic_certificates.json']=json.dumps(c).encode();rejects(lambda:w.replay_arithmetic(f),'valid_certificate_wrong_named_protocol')
    # Freeze, then damage on-disk source: replay must use only checked bytes.
    (root/'solver/drive_bound.py').write_text("raise RuntimeError('UNFROZEN_IMPORT')\n")
    (root/'solver/vendor/two_plaquette.py').write_text("raise RuntimeError('UNFROZEN_VENDOR_IMPORT')\n")
    check(w.replay_arithmetic(frozen)['status']=='passed','arithmetic_executes_frozen_source_bytes');restore()
    (root/'proof_search.py').write_text("raise RuntimeError('UNFROZEN_SEARCH_IMPORT')\n")
    sf=w.load_frozen('frozen_search_probe','proof_search.py',frozen);check(sf.plan(lib)['status']=='proved','planner_executes_frozen_source_bytes');restore()
    check(all((src/name).read_bytes()==raw for name,raw in baseline.items()),'upstream_inputs_unchanged')
    out=dict(status='passed',gate_count=len(records),optimized_python=not __debug__,records=records,reviewed_source_hashes=manifest['sha256'],source_sha256=sha(baseline['proof_routes.py']),audit_sha256=sha(Path(__file__).read_bytes()),scope='Bounded exact arithmetic admission, frozen execution and finite implication routes; mathematical lemmas independently reviewed, not formalized; no continuum target admitted.')
    Path(__file__).with_name(a.label+'_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','gate_count','source_sha256')}))
if __name__=='__main__':main()
