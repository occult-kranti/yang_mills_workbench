"""Bind proof planning metadata to exact local artifact bytes.

A successful guard proves file integrity, not the truth of prose in those files.
The manifest is created once for this research snapshot and is never refreshed by
this verifier. A changed artifact requires a new reviewed version and manifest.
"""
from pathlib import Path
import hashlib, importlib.util, json, re, sys
ROOT=Path(__file__).resolve().parents[2]

class EvidenceFailure(RuntimeError):
    pass

def verify_manifest(manifest_path: Path, root: Path = ROOT) -> dict:
    manifest=json.loads(Path(manifest_path).read_text())
    records=manifest.get('files')
    if not isinstance(records,dict) or not records:
        raise EvidenceFailure('manifest must contain a nonempty file map')
    resolved_root=root.resolve()
    for rel,expected in records.items():
        path=(resolved_root/rel).resolve()
        if not path.is_relative_to(resolved_root):
            raise EvidenceFailure(f'path leaves project: {rel}')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise EvidenceFailure(f'changed or missing bound artifact: {rel}')
    return manifest

def bound_plan(fixture_path: Path, manifest_path: Path, root: Path = ROOT) -> dict:
    manifest_digest=hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()
    manifest=verify_manifest(manifest_path,root)
    fixture_path=Path(fixture_path).resolve()
    rel=str(fixture_path.relative_to(root.resolve()))
    if rel not in manifest['files']:
        raise EvidenceFailure('fixture itself is not hash bound')
    data=json.loads(fixture_path.read_text())
    all_libraries=[data]+list(data.get('scenarios',{}).values())
    for library in all_libraries:
        for rule in library.get('rules',[]):
            refs=re.findall(r'round\d+/[A-Za-z0-9_./-]+\.(?:md|py|json)',rule['proof_ref'])
            if not refs:
                raise EvidenceFailure(f"rule {rule['id']} has no bound local proof reference")
            for reference in refs:
                if reference not in manifest['files']:
                    raise EvidenceFailure(f'unbound proof reference: {reference}')
    source=Path(__file__).with_name('proof_search.py')
    source_rel=str(source.resolve().relative_to(root.resolve()))
    if source_rel not in manifest['files']:
        raise EvidenceFailure('planner source is not hash bound')
    spec=importlib.util.spec_from_file_location('guarded_round6_proof_search',source)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    result=module.plan(data)
    result['scenario_results']={name:module.plan(library) for name,library in data.get('scenarios',{}).items()}
    verify_manifest(manifest_path,root)
    if hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()!=manifest_digest:
        raise EvidenceFailure("manifest changed during planning")
    result['evidence_guard']={'passed':True,'manifest_sha256':hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest(),'bound_file_count':len(manifest['files']),'scope':'Artifact integrity and checked Horn trace only; proof prose is not machine verified.'}
    return result

if __name__=='__main__':
    output=ROOT/'round6/bound_search_results.json'
    result=bound_plan(ROOT/'round5/search_fixture.json',ROOT/'round6/evidence_manifest.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cost':result['certified_cost'],'guard_passed':result['evidence_guard']['passed']}))
