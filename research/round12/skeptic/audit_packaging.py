#!/usr/bin/env python3
"""Bounded, isolated review of lossless proof-trace packaging.

No scientific sources or scientific acceptance files are written.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,copy,gzip,hashlib,importlib.util,json,shutil,zipfile

HERE=Path(__file__).resolve().parent
SOURCES=['trace_archive.py','build_site_data.py','package_review.py']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def file_sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    return h.hexdigest()
def unpacked_sha(path):
    h=hashlib.sha256();size=0
    with gzip.open(path,'rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk);size+=len(chunk)
    return h.hexdigest(),size

def main():
    ap=argparse.ArgumentParser();ap.add_argument('round12',type=Path);ap.add_argument('--label',required=True);args=ap.parse_args();root=args.round12.resolve();dist=root.parents[1]/'dist'
    sources={p:file_sha(root/p) for p in SOURCES};acceptance_before=file_sha(HERE/'acceptance.json');records=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        records.append({'test':name,'passed':True,'detail':detail})
    def rejects(fn,name):
        try:fn()
        except (ValueError,TypeError,OSError,KeyError):check(True,name);return
        raise RuntimeError('Unexpected acceptance: '+name)
    acceptance=json.loads((HERE/'acceptance.json').read_text())
    check(all(file_sha(root/p)==h for p,h in acceptance['reviewed_source_hashes'].items()),'all_scientific_sources_unchanged')
    baseline=json.loads((HERE/'packaging_baseline.json').read_text())['records'];inventory=json.loads((root/'trace-archives.json').read_text())['files']
    check(set(inventory)=={x['path'] for x in baseline},'all_four_precompression_trace_identities_retained')
    for old in baseline:
        rel=old['path'];item=inventory[rel];p=root/(rel+'.gz');digest,size=unpacked_sha(p)
        check(digest==old['sha256']==item['original_sha256'] and size==old['bytes']==item['original_bytes'] and
              file_sha(p)==item['gzip_sha256'] and p.stat().st_size==item['gzip_bytes'],
              'independent_lossless_gzip.'+rel,{'original_bytes':size,'gzip_bytes':p.stat().st_size,'uncompressed_sha256':digest})
    check(all((root/(rel+'.gz')).read_bytes()[4:8]==b'\0'*4 for rel in inventory),'actual_gzip_timestamps_zero')
    probe=HERE/(args.label+'_probe')
    if probe.exists():shutil.rmtree(probe)
    probe.mkdir();(probe/'trace_archive.py').write_bytes((root/'trace_archive.py').read_bytes())
    spec=importlib.util.spec_from_file_location('isolated_trace_archive',probe/'trace_archive.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    raw=b'{"status":"passed","marker":"current"}\n';oldraw=b'{"status":"passed","marker":"historical"}\n'
    current=probe/'proof_results.json';historical=probe/'historical'/'proof_results.json';historical.parent.mkdir();current.write_bytes(raw);historical.write_bytes(oldraw)
    check(m.read_json(current)==json.loads(raw),'raw_only_loader')
    m.main();first=(probe/'proof_results.json.gz').read_bytes();before_inventory=json.loads((probe/'trace-archives.json').read_text())
    m.main();check((probe/'proof_results.json.gz').read_bytes()==first and first==gzip.compress(raw,compresslevel=9,mtime=0),'deterministic_repeat_compression')
    historical.unlink();current.write_bytes(raw.replace(b'current',b'current-regenerated'));m.main()
    after=json.loads((probe/'trace-archives.json').read_text())
    check(set(after['files'])==set(before_inventory['files']) and after['files']['historical/proof_results.json']==before_inventory['files']['historical/proof_results.json'],
          'mixed_raw_compressed_only_historical_inventory_preserved')
    check(m.read_json(historical)==json.loads(oldraw),'compressed_only_historical_loader')
    current.unlink();m.main();check(set(m.verify_archives())==set(before_inventory['files']),'fully_compressed_only_inventory_replay')
    current.write_bytes(b'{"wrong":"stale"}');rejects(lambda:m.record_bytes(current),'stale_raw_compressed_pair_rejected');current.unlink()
    manifest_path=probe/'trace-archives.json';valid=manifest_path.read_bytes()
    for field in ['original_sha256','original_bytes','gzip_sha256','gzip_bytes']:
        changed=json.loads(valid);item=changed['files']['proof_results.json'];item[field]='0'*64 if 'sha256' in field else item[field]+1;manifest_path.write_text(json.dumps(changed))
        rejects(m.verify_archives,'altered_inventory_'+field+'_rejected');manifest_path.write_bytes(valid)
    altered=json.loads(valid);altered['files']['proof_results.json']['gzip_bytes']+=1;manifest_path.write_text(json.dumps(altered))
    rejects(m.main,'compression_merge_rejects_wrong_existing_gzip_size');manifest_path.write_bytes(valid)
    gzip_path=probe/'proof_results.json.gz';good=gzip_path.read_bytes();gzip_path.write_bytes(b'not gzip');rejects(m.verify_archives,'corrupted_compressed_payload_rejected');gzip_path.write_bytes(good)
    rejects(lambda:m.record_bytes(probe.parent/'outside.json'),'path_escape_rejected')
    other=probe/'samebytes.gz';other.write_bytes(good);gzip_path.unlink();gzip_path.symlink_to(other.name)
    rejects(lambda:m.record_bytes(current),'samebytes_compressed_symlink_rejected');gzip_path.unlink();gzip_path.write_bytes(good);other.unlink()
    script=(dist/'research-bridges-data.js').read_text();prefix='window.OBSERVATORY_BRIDGES=';check(script.startswith(prefix) and script.rstrip().endswith(';'),'site_payload_serialization')
    payload=json.loads(script[len(prefix):].strip()[:-1]);compact=json.loads(payload['documents']['routes']);exact=json.loads((root/'solver/output/exact_step_certificate.json').read_text())
    expected={'cosine_representation':6,'exact_piecewise_computed_state':12,'finite_volume_comparison':3,'vanishing_bound_is_not_gap_closure':2,'defined_point_closure_rejected':3}
    negatives={'cosine_total_error_unavailable','without_degree_bandwidth','without_initial_support','without_absolute_action','without_exact_vector_replay','four_dimensional_yang_mills'}
    routes=compact['routes'];outcomes=set(routes)==set(expected)|negatives
    for name,cost in expected.items():r=routes[name]['result'];outcomes=outcomes and r['status']=='proved' and r['certified_cost']==cost and bool(r['certified_proof'])
    outcomes=outcomes and all(routes[name]['result']['status']=='not_derivable' for name in negatives)
    check(outcomes,'compact_positive_and_negative_route_certificates_preserved')
    check(compact['arithmetic']['exact_evolution']==exact and json.loads(payload['documents']['exact'])==exact,'site_exact_certificate_preserved')
    check(all('search_trace' not in x['result'] and 'frontier' not in x['result'] for x in routes.values()) and (dist/'research-bridges-data.js').stat().st_size<2_000_000,'large_exploration_logs_omitted_from_display_only')
    check('Full unmodified search traces' in compact['trace_storage'] and '/research-round12-proof-trace.json.gz' in (dist/'research-bridges.js').read_text(),'full_trace_omission_and_download_link_disclosed')
    check(file_sha(dist/'research-round12-proof-trace.json.gz')==inventory['proof_results.json']['gzip_sha256'],'download_payload_matches_full_archived_trace')
    archive=dist/'research-round12.zip'
    with zipfile.ZipFile(archive) as z:
        prefix='yangmills-round12/';names=set(z.namelist());contents=json.loads(z.read(prefix+'ARCHIVE-CONTENTS.json'))['sha256']
        check(all(prefix+rel not in names and prefix+rel+'.gz' in names for rel in inventory),'portable_zip_omits_raw_duplicates_and_keeps_each_gzip')
        check(all(sha(z.read(prefix+rel+'.gz'))==item['gzip_sha256'] for rel,item in inventory.items()),'portable_zip_preserves_each_compressed_trace')
        check(json.loads(z.read(prefix+'trace-archives.json'))['files']==inventory,'portable_zip_preserves_original_byte_inventory')
        check(all(sha(z.read(prefix+rel))==digest for rel,digest in contents.items()),'portable_zip_full_file_inventory_replays',{'files':len(contents)})
        check(all(sha(z.read(prefix+rel))==digest for rel,digest in sources.items()),'portable_zip_includes_reviewed_integration_sources')
    check({p:file_sha(root/p) for p in SOURCES}==sources and file_sha(HERE/'acceptance.json')==acceptance_before,'reviewed_sources_and_scientific_acceptance_not_modified')
    result={'status':'passed','completed_utc':datetime.now(timezone.utc).isoformat(),'optimized_python':not __debug__,'gate_count':len(records),'records':records,
            'reviewed_source_hashes':sources,'audit_sha256':file_sha(Path(__file__)),'scientific_acceptance_sha256':acceptance_before,
            'trace_inventory_sha256':file_sha(root/'trace-archives.json'),'archive_sha256_at_review':file_sha(archive),
            'trace_original_total_bytes':sum(x['original_bytes'] for x in inventory.values()),'trace_compressed_total_bytes':sum(x['gzip_bytes'] for x in inventory.values()),
            'scope':'Lossless trace archives, deterministic compression, isolated loader/mutation/merge checks, compact site certificate data and portable ZIP inventory. Scientific acceptance remains separate and unchanged.',
            'resolved_findings':['Mixed raw/compressed-only regeneration now preserves historical inventory entries.','Declared gzip byte length is checked during verification and regeneration.']}
    (HERE/(args.label+'_results.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','gate_count':len(records),'optimized_python':not __debug__}))
    shutil.rmtree(probe)
if __name__=='__main__':main()
