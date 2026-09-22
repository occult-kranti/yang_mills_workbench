#!/usr/bin/env python3
"""Verify a committed Round29 release in a clean linked Git worktree.

All replays, mutation fixtures, reviewer writes, site rebuilds and receipts are
external to the source checkout. The resulting receipt pins the tested commit
and Git tree. This is a reproducibility/admission check, not formal proof or
external human peer review; it adds zero research investigations.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from research.round29.release.admission import digest, require, local


def load(path): return json.loads(path.read_text())
def write(path, record): path.write_text(json.dumps(record, indent=2) + '\n')


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    require(result.returncode == 0, 'Git command failed: ' + ' '.join(args) + '\n' + result.stderr)
    return result.stdout.strip()


def tree_files(root, revision):
    output = subprocess.run(['git', '-C', str(root), 'ls-tree', '-rz', '--full-tree', revision], capture_output=True, check=True).stdout
    records = {}
    for entry in output.split(b'\0'):
        if not entry: continue
        meta, name = entry.split(b'\t', 1); mode, kind, oid = meta.decode().split()
        if kind == 'blob': records[name.decode()] = {'mode': mode, 'git_blob': oid}
    return records


def historical(path):
    match = re.match(r'research/round(\d+)/', path)
    if match: return int(match.group(1)) < 29
    if path.startswith(('evidence/', 'papers/draft-01/', 'papers/round27-addendum/', 'papers/round28-addendum/')): return True
    # Every baseline research presentation asset belongs to the preserved archive.
    if re.match(r'(?:dist|docs)/research(?:[-.])', path): return not re.match(r'(?:dist|docs)/research-round29[-.]', path)
    return bool(re.match(r'(?:dist|docs)/ym-(?:draft-01|round2[78])[-.]', path))


def preserve_history(root, baseline, current):
    require(subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',baseline,current],capture_output=True).returncode == 0, 'Historical baseline is not an ancestor')
    before, after = tree_files(root, baseline), tree_files(root, current)
    protected = {path: value for path, value in before.items() if historical(path)}
    changed = [path for path, value in protected.items() if after.get(path) != value]
    require(not changed, 'Historical frozen bytes/modes changed: ' + ', '.join(changed[:12]))
    return {'baseline_commit': git(root,'rev-parse',baseline), 'protected_files': len(protected), 'changed': changed, 'rule': 'Rounds before29, evidence, Draft01, R27/R28 addenda and all baseline research static assets except Round29.'}


def inventory(directory):
    return {str(path.relative_to(directory)): digest(path) for path in sorted(directory.rglob('*')) if path.is_file()}


def extract_tree(root, destination):
    destination.mkdir(parents=True)
    archive = destination.parent / 'source-tree.tar'
    with archive.open('wb') as output:
        subprocess.run(['git','-C',str(root),'archive','--format=tar','HEAD'],stdout=output,check=True)
    with tarfile.open(archive) as source: source.extractall(destination, filter='data')
    archive.unlink()


def pdf_report(root, output):
    import fitz
    path = root/'papers/draft-02/main.pdf'; qa_path = root/'papers/draft-02/pdf-qa.json'
    require(path.is_file() and qa_path.is_file(), 'Final PDF/QA record missing')
    qa = load(qa_path)
    require(qa.get('status') == 'passed' and qa.get('mode') == 'final_source_build', 'PDF QA is not final')
    require(qa.get('pdf_sha256') == digest(path), 'Final PDF QA binds different bytes')
    require(qa.get('references_resolved') is True, 'Final PDF references are not resolved')
    require(not qa.get('overfull_warnings'), 'Final PDF has overfull compilation warnings')
    document = fitz.open(path); pages = []; first_text = ''; outside = []
    for index, page in enumerate(document):
        text = page.get_text()
        if index < 3: first_text += text
        require('??' not in text, f'Unresolved reference on PDF page {index+1}')
        for block in page.get_text('dict')['blocks']:
            if block.get('type') != 0: continue
            for line in block['lines']:
                for span in line['spans']:
                    x0,y0,x1,y1 = span['bbox']
                    if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                        outside.append({'page': index+1, 'text': span['text']})
        pages.append({'page': index+1, 'characters': len(text)})
    require(not outside, 'PDF has text outside page bounds')
    require('Hruday' in first_text and 'BUNZEEY' in first_text, 'Human author missing from PDF front matter')
    require(qa.get('page_count', qa.get('pages')) == len(document), 'PDF page-count QA mismatch')
    reviewed_pages=qa.get('visually_reviewed_pages', [])
    require(isinstance(reviewed_pages,list) and all(type(page) is int for page in reviewed_pages) and sorted(reviewed_pages) == list(range(1,len(document)+1)), 'Final PDF lacks complete recorded page review')
    for alias in ('dist/ym-draft-02.pdf', 'docs/ym-draft-02.pdf'):
        require(digest(root/alias) == digest(path), 'Static PDF is stale: ' + alias)
    visual = qa.get('visual_review_record')
    require(isinstance(visual, str), 'Final visual-review record missing')
    visual_path=local(root,visual)
    require(qa.get('visual_review_record_sha256') == digest(visual_path), 'PDF QA binds a different visual review')
    coverage_relative=qa.get('visual_review_coverage_record')
    require(isinstance(coverage_relative,str), 'Actual visual-review coverage record missing')
    coverage_path=local(root,coverage_relative); coverage=load(coverage_path)
    require(qa.get('visual_review_coverage_sha256') == digest(coverage_path), 'PDF QA binds a different coverage record')
    require(coverage.get('status') == 'passed' and coverage.get('pdf_sha256') == digest(path) and coverage.get('page_count') == len(document), 'Visual coverage does not pass this PDF')
    require(coverage.get('contact_sheet_pages') == reviewed_pages, 'Recorded visual page coverage differs')
    full_size=qa.get('full_size_reviewed_pages', [])
    require(isinstance(full_size,list) and full_size and all(type(page) is int for page in full_size) and len(set(full_size)) == len(full_size) and set(full_size) <= set(reviewed_pages), 'Invalid full-size visual page coverage')
    require(coverage.get('full_size_pages') == full_size, 'Recorded full-size visual coverage differs')
    require(bool(coverage.get('method')) and coverage['method'] == qa.get('visual_review_method'), 'Visual coverage method missing or different')
    manifest_path=root/'papers/draft-02/artifact-manifest.json'
    require(manifest_path.is_file(), 'Final manuscript inventory missing')
    manifest=load(manifest_path)
    require(manifest.get('pdf_sha256') == digest(path) and manifest.get('pages') == len(document), 'Manuscript inventory PDF mismatch')
    require(manifest.get('review_record') == visual and manifest.get('review_sha256') == digest(visual_path), 'Manuscript inventory visual-review mismatch')
    files=manifest.get('sha256', {})
    expected={str(p.relative_to(root)) for p in (root/'papers/draft-02').rglob('*') if p.is_file() and p.name != 'artifact-manifest.json' and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    require(set(files) == expected, 'Manuscript inventory omits or adds an artifact')
    for relative, expected_digest in files.items():
        require(digest(local(root, relative)) == expected_digest, 'Manuscript artifact changed: ' + relative)
    result = {'status': 'passed', 'scope': 'Final PDF bytes, author, all-page extracted-text bounds and unresolved-reference screen; visual review remains the separately recorded human-readable model-agent inspection.', 'source': 'papers/draft-02/main.pdf', 'pdf_sha256': digest(path), 'page_count': len(document), 'author_in_front_matter': True, 'qa_source': 'papers/draft-02/pdf-qa.json', 'qa_sha256': digest(qa_path), 'visual_review_record': visual, 'visual_review_sha256': digest(visual_path), 'visual_review_coverage_record': coverage_relative, 'visual_review_coverage_sha256': digest(coverage_path), 'contact_sheet_pages_checked': len(reviewed_pages), 'full_size_reviewed_pages': full_size, 'artifact_manifest': 'papers/draft-02/artifact-manifest.json', 'artifact_manifest_sha256': digest(manifest_path), 'artifacts_checked': len(files), 'text_outside_page': outside, 'pages': pages}
    write(output, result); return {key: value for key,value in result.items() if key != 'pages'}



def site_render_report(root):
    relative='research/round29/presentation/site-qa-final.json'
    path=local(root,relative); qa=load(path)
    require(qa.get('status') == 'passed' and qa.get('mode') == 'final_source_render', 'Final rendered-site QA missing')
    require(qa.get('checkpoint',{}).get('completed') == 10, 'Rendered site is not the ten-loop release')
    require(qa.get('visual_review',{}).get('status') == 'passed' and qa.get('pageErrors') == [], 'Rendered site inspection not complete')
    sources=qa.get('source_sha256', {})
    required={'research/round29/build_site.py','research/round29/advisor/findings.json','research/round29/network.json','research/round29/experts/sources.json','papers/draft-02/registry/hnm-registry.json','papers/draft-02/main.pdf','tests/round29_browser.mjs'}
    required|={folder+'/'+name for folder in ('dist','docs') for name in ('index.html','research-round29.js','research-round29.css','research-round29-data.js','hnm-registry.json','ym-draft-02.pdf')}
    require(required <= sources.keys(), 'Rendered QA omits a required source/artifact')
    for name,sha in sources.items(): require(digest(local(root,name)) == sha, 'Rendered-site source changed: '+name)
    screenshots=qa.get('screenshot_sha256', {})
    require(len(screenshots) == 5, 'Final rendered screenshot inventory incomplete')
    for name,sha in screenshots.items(): require(digest(local(root,name)) == sha, 'Rendered screenshot changed: '+name)
    checked={row['route'] for row in qa.get('checks',[]) if row.get('mobileOverflow') is False}
    expected={'home','hnm-priorities','hnm-findings','research-network','round29-results','round29-sources','round29-roadmap','round29-proof','drafts','sharing','round28-home','round28-ak2'}
    expected|={'round29-'+row['id'].lower() for row in load(root/'research/round29/advisor/findings.json')['loops']}
    require(expected <= checked, 'Final rendered QA omits a current/archive route')
    return {'status':'passed','source':relative,'sha256':digest(path),'source_files_bound':len(sources),'screenshots_bound':len(screenshots),'mobile_routes':len(checked),'scope':'Recorded rendered browser checks and actual visual inspection bound to the committed source and screenshot bytes; browser is not rerun by this release helper.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--baseline', required=True, help='Commit whose frozen historical evidence must remain identical')
    parser.add_argument('--expected-tree', help='Optional required Git tree ID supplied by the release coordinator')
    args = parser.parse_args(); root = ROOT.resolve(); receipt = args.receipt
    require(receipt.is_absolute() and not receipt.resolve().is_relative_to(root), 'Receipt must be external and absolute')
    require(not receipt.exists(), 'Receipt already exists')
    require((root/'.git').is_file(), 'Run the final verifier in a fresh linked worktree, not the primary checkout')
    require(not git(root,'status','--porcelain','--untracked-files=all'), 'Release worktree is dirty')
    commit = git(root,'rev-parse','HEAD'); tree = git(root,'rev-parse','HEAD^{tree}')
    if args.expected_tree: require(tree == args.expected_tree, 'Unexpected release Git tree')
    evidence = receipt.parent / (receipt.stem + '-evidence')
    require(not evidence.exists(), 'External evidence directory already exists')
    evidence.mkdir(parents=True); logs=evidence/'logs'; logs.mkdir()
    commands = []
    def run(label, command, cwd=root):
        result = subprocess.run(command,cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        (logs/(label+'.stdout.txt')).write_text(result.stdout); (logs/(label+'.stderr.txt')).write_text(result.stderr)
        normalized = [str(value).replace(str(evidence),'@evidence').replace(str(root),'@source') for value in command]
        record={'step':label,'command':normalized,'cwd':'@source' if cwd==root else '@evidence/checkout','returncode':result.returncode,'stdout':str((logs/(label+'.stdout.txt')).relative_to(receipt.parent)),'stderr':str((logs/(label+'.stderr.txt')).relative_to(receipt.parent))}; commands.append(record)
        require(result.returncode==0,'Release step failed: '+label+'\n'+result.stderr[-3000:]); return result
    history=preserve_history(root,args.baseline,commit)
    run('admission',[sys.executable,'-B','research/round29/reproduce.py','--complete','--validate-only'])
    findings=load(root/'research/round29/advisor/findings.json'); require(len(findings['loops'])==10,'Ten reviewed loops required')
    run('normal-producers',[sys.executable,'-B','research/round29/reproduce.py','--complete','--output',str(evidence/'normal')])
    run('optimized-producers',[sys.executable,'-B','-O','research/round29/reproduce.py','--complete','--optimized','--output',str(evidence/'optimized')])
    run('admission-mutations',[sys.executable,'-B','research/round29/release/test_admission.py','--complete','--output',str(evidence/'admission-mutations.json')])
    checkpoint=evidence/'checkout'; extract_tree(root,checkpoint)
    reviewer_runs=[]
    for row in findings['loops']:
        loop=row['id'].lower(); relative=f'research/round29/skeptic/{loop}_check.py'
        run('skeptic-'+loop,[sys.executable,'-B',relative],checkpoint)
        output=f'research/round29/skeptic/{loop}-checks.json'
        require((checkpoint/output).read_bytes()==(root/output).read_bytes(),'Skeptical replay differs: '+loop)
        reviewer_runs.append({'loop':loop,'script':relative,'result':output,'results_sha256':digest(root/output)})
    run('source-bound-site',[sys.executable,'-B','research/round29/build_site.py','--require-complete'],checkpoint)
    run('static-site',[sys.executable,'-B','scripts/build_pages.py'],checkpoint)
    for directory in ('dist','docs'):
        require(inventory(checkpoint/directory)==inventory(root/directory),'Static build is not byte-identical: '+directory)
    run('site-integration',['node','tests/round29_site.mjs'],checkpoint)
    pdf=pdf_report(root,evidence/'pdf-report.json')
    rendered=site_render_report(root)
    require(not git(root,'status','--porcelain','--untracked-files=all'),'Verifier changed source checkout')
    result={'schema':'ym29-committed-release-v1','status':'passed','verified_at':datetime.now(timezone.utc).isoformat(),'source_commit':commit,'source_tree':tree,'fresh_linked_worktree':True,'source_checkout_unchanged':True,'research_loops_added':0,'reviewed_loops':10,'producer_runs':{'normal':20,'optimized':20,'counting_scope':'Direct full-suite producer executions; reviewer validators may run additional internal replays.','comparison':'Complete recorded producer output inventories and bytes, including source manifests.'},'skeptical_validators':reviewer_runs,'historical_preservation':history,'admission_mutations':load(evidence/'admission-mutations.json'),'static_build':'byte-identical dist and docs rebuilt from committed source','pdf':pdf,'rendered_site':rendered,'commands':commands,'evidence_directory':str(evidence.relative_to(receipt.parent)),'source_paths_are_repository_relative':True,'limits':['Programmed controls and written mathematical review are distinct. This verifier does not certify the continuum Yang–Mills problem.','The receipt pins the trusted validator/specification tree; it cannot defend against replacing both trusted code and the claimed external receipt.']}
    write(receipt,result)
    print(json.dumps({'status':'passed','source_commit':commit,'source_tree':tree,'producer_runs':40,'reviewed_loops':10,'skeptical_validators':len(reviewer_runs),'historical_files_preserved':history['protected_files'],'pdf_pages':pdf['page_count']}))

if __name__=='__main__': main()
