#!/usr/bin/env python3
"""Candidate inventory and externally pinned, read-only Round22 release verification."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'research/round22'))
from admission import LOOPS, digest, gate, read, require, source, unlinked
INVENTORY = 'research/round22/release/final-inventory.json'
SCHEMA = 'ym22-release-inventory-v1'
RECOVERED_BASE = '382e61571b029e198d87abbeec99d88157d3c168'
TREES = ('research/round22', '.codex/skills', 'scripts', 'tests', 'dist', 'docs')
FIXED = ('AGENTS.md', 'README.md', 'package.json',
         'research/round21/release/final-inventory.json')
INHERITED = ('i1','i2','j1','j2','k1','k2','l1','l2','m1','m2')

ADMISSION_CONTROLS=(
    'missing_required_report','dropped_required_report_inventory','changed_source_bytes',
    'coherent_false_result_status','coherent_wrong_loop','coherent_wrong_direction',
    'coherent_nonboolean_passed','coherent_false_passed','coherent_changed_reviewed_claims',
    'coherently_removed_required_controls','coherently_removed_declared_instruction_snapshot',
    'coherent_failed_controls','coherent_truthy_nonboolean_controls','coherent_failed_nested_control',
    'symlinked_parent_with_identical_bytes','duplicate_contract_key_with_rebound_hashes')


def validate_replay_summary(replay, loops, optimized):
    require(replay.get('status')=='passed' and replay.get('loops')==list(loops) and
            replay.get('optimized') is optimized, 'incomplete scientific replay')
    rows=replay.get('executions')
    require(type(rows) is list and [(r.get('loop'),r.get('direction')) for r in rows]==
            [(n,d) for n in loops for d in ['forward','reverse']], 'replay pair identity drift')
    current = tuple(loops) == LOOPS
    require(current or tuple(loops) == INHERITED, 'unknown replay family')
    round_name = 'round22' if current else 'round21'
    for row in rows:
        loop, direction = row['loop'], row['direction']
        prefix = 'research/'+round_name+'/'+direction+'/'+loop+'/'
        files = read(source('research/'+round_name+'/advisor/'+loop+'-gate.json'))['files']
        require(row.get('source_sha256') == files[prefix+'check.py'] and
                row.get('result_sha256') == files[prefix+'output/results.json'],
                'replay source or result hash differs from admitted evidence')
        if current:
            require(type(row.get('outputs_compared')) is int and row['outputs_compared'] ==
                    sum(name.startswith(prefix+'output/') for name in files),
                    'replay output count differs from admitted inventory')
    if current:
        require(replay.get('admitted_gates') == {
            n:digest(source('research/round22/advisor/'+n+'-gate.json')) for n in loops},
            'replay admitted gate bindings changed')
        require(type(replay.get('research_loops_added')) is int and replay['research_loops_added'] == 0,
                'replay must add exactly zero research loops')
    else:
        require(type(replay.get('pair_comparisons')) is int and replay['pair_comparisons'] == len(loops),
                'inherited pair comparison count changed')
    return rows


def validate_c2_summary(c2):
    require(c2.get('schema')=='ym21-c2-replay-v1' and c2.get('status')=='completed' and
            c2.get('optimized') is False and type(c2.get('research_loops_added')) is int and
            c2['research_loops_added']==0 and
            c2.get('historical_failure',{}).get('historical_gate_remains_failed') is True and
            set(c2.get('replays',{}))=={'forward','backward','comparison'}, 'C2 repair semantics drift')
    comparison=c2['replays']['comparison']
    require(type(comparison.get('semantic_checks')) is int and comparison['semantic_checks']==34 and
            type(comparison.get('rejected_scientific_mutations')) is int and
            comparison['rejected_scientific_mutations']==27 and
            comparison.get('identical_to_historical_except_validated_absolute_paths') is True,
            'C2 semantic checks incomplete')


def validate_admission_summary(controls, optimized):
    require(controls.get('status')=='passed' and controls.get('loop')=='n1' and
            controls.get('optimized') is optimized, 'admission summary status drift')
    rows=controls.get('controls')
    require(type(rows) is list and [r.get('control') for r in rows]==list(ADMISSION_CONTROLS) and
            all(r.get('rejected') is True for r in rows), 'admission mutation identities failed')
    require(controls.get('gate_sha256')==digest(source('research/round22/advisor/n1-gate.json')),
            'admission mutations used a different gate')



def load(name, path):
    spec=importlib.util.spec_from_file_location(name, path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def fresh(path):
    path=unlinked(path.absolute()).resolve()
    require(not path.exists() and path != ROOT and ROOT not in path.parents,
            'output must be fresh and outside source tree')
    return path


def preflight():
    ledger=read(source('research/round22/advisor/progress-ledger.json'))
    require(type(ledger.get('completed_research_loops')) is int and
            ledger['completed_research_loops']==10, 'exactly ten completed research loops required')
    require(ledger.get('base_commit')==RECOVERED_BASE, 'recovered base identity changed')
    rows=ledger.get('loops')
    require(type(rows) is list and [r.get('id') for r in rows]==list(LOOPS),
            'missing, duplicate, reordered or additional loop')
    require(ledger.get('unselected')==[], 'unselected loop remains')
    gates={loop:gate(loop) for loop in LOOPS}
    for row in rows:
        loop=row['id']
        require(row.get('status')==gates[loop]['status'], 'ledger verdict drift')
        require(row.get('gate_sha256')==digest(source('research/round22/advisor/'+loop+'-gate.json')),
                'ledger gate binding drift')
        require(row.get('contract_sha256')==digest(source('research/round22/contracts/'+loop+'.json')),
                'ledger contract binding drift')
        for direction in ['forward','reverse']:
            name='research/round22/'+direction+'/'+loop+'/submission.json'
            require(row.get(direction+'_submission')=={'path':name,'sha256':digest(source(name))},
                    'ledger frozen submission binding drift')
    for checkpoint,count in [('post-six-review.json',6),('post-ten-review.json',10)]:
        review=read(source('research/round22/skeptic/'+checkpoint))
        require(review.get('schema')=='ym22-checkpoint-review-v1' and
                type(review.get('completed_research_loops')) is int and
                review['completed_research_loops']==count and review.get('passed') is True,
                'required skeptical checkpoint missing or failed')
        require(review.get('reviewed_gates')=={
            n:digest(source('research/round22/advisor/'+n+'-gate.json')) for n in LOOPS[:count]},
            'checkpoint gate bindings incomplete')
        require(type(review.get('findings')) is list and bool(review['findings']) and
                all(isinstance(f,(str,dict)) and bool(f) for f in review['findings']) and
                review.get('continuum_status')=='open', 'checkpoint review content absent')
        if count==6:
            require(type(review.get('ranked_candidates')) is list and len(review['ranked_candidates'])>=2,
                    'six-loop ranked alternatives missing')
        else:
            require(review.get('claim_map_sha256')==digest(source('research/round22/advisor/claim-dependency-map.json')),
                    'ten-loop review lacks actual claim map')
    checkpoints=ledger.get('checkpoints')
    require(type(checkpoints) is list and [c.get('after_loops') for c in checkpoints]==[6,10] and
            all(type(c.get('after_loops')) is int for c in checkpoints),
            'ledger checkpoint order invalid')
    for entry,count,label in zip(checkpoints,[6,10],['six','ten']):
        require(entry.get('review_sha256')==digest(source('research/round22/skeptic/post-'+label+'-review.json')),
                'ledger checkpoint binding changed')
    selection_name='research/round22/advisor/post-six-selection.json'
    selection=read(source(selection_name))
    require(type(selection.get('completed_research_loops')) is int and selection['completed_research_loops']==6 and
            [g.get('id') for g in selection.get('goals',[])]==['Q','R'],
            'Q/R selection must follow the first six completed loops')
    require(all(type(g) is dict and all(type(g.get(k)) is str and bool(g[k].strip())
                for k in ['id','title','target','reason']) for g in selection['goals']),
            'Q/R goal content missing')
    require(selection.get('reviewed_gates')=={
        n:digest(source('research/round22/advisor/'+n+'-gate.json')) for n in LOOPS[:6]},
        'Q/R selection does not bind all six reviewed gates')
    require(selection.get('skeptic_review_sha256')==digest(source('research/round22/skeptic/post-six-review.json')),
            'Q/R selection does not bind the six-loop skeptical checkpoint')
    for later,earlier in [('n2','n1'),('o2','o1'),('p2','p1'),('q2','q1'),('r2','r1')]:
        contract=read(source('research/round22/contracts/'+later+'.json'))
        deps=contract['dependencies']
        for name in ['research/round22/advisor/'+earlier+'-gate.json',
                     'research/round22/skeptic/'+earlier+'.md']:
            require(deps.get(name)==digest(source(name)), 'second loop lacks frozen first review')
    for loop in ['q1','r1']:
        deps=read(source('research/round22/contracts/'+loop+'.json'))['dependencies']
        require(deps.get(selection_name)==digest(source(selection_name)), 'later goal lacks post-six selection')
    roadmap=read(source('research/round22/advisor/post-ten-roadmap.json'))
    require(type(roadmap.get('goals')) is list and len(roadmap['goals'])==3,
            'exactly three next goals must be planned')
    require(roadmap.get('executed') is False, 'extra research execution not authorized by this cycle')
    goal_ids=[]
    for goal in roadmap['goals']:
        require(type(goal) is dict and all(type(goal.get(k)) is str and bool(goal[k].strip())
                for k in ['id','title','target','missing_premise']), 'future goal content missing')
        goal_ids.append(goal['id'])
    require(len(set(goal_ids))==3, 'duplicate future goal')
    require(roadmap.get('skeptic_review_sha256')==digest(source('research/round22/skeptic/post-ten-review.json')),
            'future goals lack ten-loop feedback binding')
    # Historical scientific admission remains separate from its old presentation inventory.
    legacy=load('ym22_legacy_final',source('research/round21/release/final_verify.py'))
    _, old_gates, c2=legacy.preflight()
    return ledger,gates,legacy,old_gates,c2


def collect():
    ledger,gates,legacy,old_gates,c2=preflight()
    files=legacy.collect_files(old_gates,c2)
    names=set(files)|set(FIXED)
    for tree in TREES:
        for path in unlinked(ROOT/tree).rglob('*'):
            unlinked(path)
            if path.is_file() and str(path.relative_to(ROOT)) != INVENTORY:
                names.add(str(path.relative_to(ROOT)))
    for g in gates.values(): names.update(g['files'])
    return ledger,{name:digest(source(name)) for name in sorted(names)}


def inventory():
    ledger,files=collect()
    return {'schema':SCHEMA,'loops':list(LOOPS),'inherited_admission_loops':list(INHERITED),
            'base_commit':ledger['base_commit'],'excluded_self_referential_path':INVENTORY,
            'files':files,'review_status':'candidate_requires_external_digest_review',
            'trust':'The caller must supply the independently reviewed exact inventory SHA256; the inventory is not its own admission.'}


def validate(path, expected):
    require(type(expected) is str and re.fullmatch('[0-9a-f]{64}',expected), 'invalid reviewed digest')
    require(digest(unlinked(path.absolute()))==expected,'reviewed inventory digest changed')
    require(source(INVENTORY).read_bytes()==path.read_bytes(), 'canonical in-tree inventory differs or is missing')
    frozen=read(path)
    actual=inventory()
    require(frozen==actual,'release inventory is incomplete, inconsistent or has changed bytes')
    return frozen


def run(command, log, cwd=ROOT):
    p=subprocess.run(command,cwd=cwd,text=True,capture_output=True)
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(p.stdout+p.stderr)
    require(p.returncode==0,'verification command failed: '+str(log))
    return {'exit_code':0,'log_sha256':digest(log)}


def git_state(args, frozen):
    def git(*values):
        p=subprocess.run(['git',*values],cwd=ROOT,text=True,capture_output=True)
        require(p.returncode==0,'Git release check failed: '+str(values))
        return p.stdout.strip()
    require(Path(git('rev-parse','--show-toplevel')).resolve()==ROOT,'verification root is not a Git worktree')
    detached=subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=ROOT,text=True,capture_output=True)
    require(detached.returncode==1 and not detached.stdout, 'release worktree must have detached HEAD')
    require(not git('status','--porcelain','--untracked-files=all'),'release Git tree is not clean')
    require(re.fullmatch('[0-9a-f]{40}',args.git_commit) and
            re.fullmatch('[0-9a-f]{40}',args.git_tree),'invalid reviewed Git identity')
    require(git('rev-parse','HEAD')==args.git_commit,'reviewed Git commit changed')
    require(git('rev-parse','HEAD^{tree}')==args.git_tree,'reviewed Git tree changed')
    # Status can hide ignored files or assume-unchanged/skip-worktree modifications.
    # Compare every inventoried disk byte directly to the pinned committed blob.
    raw_tree=subprocess.run(['git','ls-tree','-r','-z','HEAD'],cwd=ROOT,capture_output=True)
    require(raw_tree.returncode==0, 'cannot enumerate committed release tree')
    committed={}
    for row in raw_tree.stdout.split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1); mode,kind,oid=meta.decode('ascii').split()
        committed[name.decode('utf-8')]=(mode,kind,oid)
    for name in [*frozen['files'],INVENTORY]:
        require(name in committed, 'inventoried file is absent from Git tree: '+name)
        mode,kind,oid=committed[name]
        require(kind=='blob' and mode in ['100644','100755'], 'nonregular committed release input: '+name)
        path=source(name); data=path.read_bytes()
        actual_oid=hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()
        require(actual_oid==oid, 'disk bytes differ from committed blob: '+name)
        actual_mode='100755' if path.stat().st_mode & 0o100 else '100644'
        require(mode==actual_mode, 'disk executable mode differs from committed mode: '+name)
    base=frozen['base_commit']
    require(base==RECOVERED_BASE, 'unanchored recovered base')
    git('merge-base','--is-ancestor',base,'HEAD')
    historical=['research/round'+str(n) for n in range(8,22)]
    require(not git('diff','--name-only',base,'HEAD','--',*historical),
            'historical research changed after recovered base')
    changed=git('diff','--name-only',base,'HEAD').splitlines()
    require(all(n in frozen['files'] or n==INVENTORY for n in changed),
            'changed published file lies outside reviewed inventory')
    return {'commit':args.git_commit,'tree':args.git_tree,'base_commit':base,
            'clean':True,'detached':True,'inventoried_disk_blobs_match_git':True,
            'historical_research_unchanged':True,'changed_paths':len(changed)}


def verify_site(frozen, out):
    """Rebuild every generated presentation output from absent destinations."""
    result={}
    mirror=out/'site-work'
    for name in frozen['files']:
        target=mirror/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source(name),target)
    map_name='research/round22/advisor/claim-dependency-map.json'
    (mirror/map_name).unlink()
    result['claim_map_build']=run([sys.executable,'-B',str(mirror/'research/round22/build_claim_map.py')],out/'claim-map-build.log',mirror)
    require(digest(mirror/map_name)==frozen['files'][map_name], 'rebuilt claim map differs from reviewed map')
    (mirror/'dist/research-round22-data.js').unlink()
    result['data_build']=run([sys.executable,'-B',str(mirror/'research/round22/build_site.py')],out/'data-build.log',mirror)
    expected={n:d for n,d in frozen['files'].items() if n.startswith('dist/')}
    actual={str(p.relative_to(mirror)):digest(p) for p in (mirror/'dist').rglob('*') if p.is_file()}
    require(actual==expected,'source-built current data changed bound dist assets')
    shutil.rmtree(mirror/'docs')
    result['pages_build']=run([sys.executable,'-B',str(mirror/'scripts/build_pages.py')],out/'pages-build.log',mirror)
    expected={n:d for n,d in frozen['files'].items() if n.startswith('docs/')}
    actual={str(p.relative_to(mirror)):digest(p) for p in (mirror/'docs').rglob('*') if p.is_file()}
    require(actual==expected,'fresh Pages build differs from reviewed docs')
    node=shutil.which('node');require(node is not None,'Node required for release UI checks')
    result['ui_tests']={}
    for name in ['test_workbench.mjs','test_journey.mjs','test_round22.mjs']:
        result['ui_tests'][name]=run([node,str(mirror/'tests'/name)],out/(name+'.log'),mirror)
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal'
        target=out/('presentation-schema-'+mode+'.json')
        result['presentation_schema_'+mode]=run([sys.executable,'-B',*(['-O'] if optimized else []),
            str(mirror/'research/round22/release/check_presentation_schema.py'),
            '--output',str(target)],out/('presentation-schema-'+mode+'.log'),mirror)
        require(target.read_bytes()==(mirror/'research/round22/release/presentation-schema-checks.json').read_bytes(),
                'presentation rejection controls differ from reviewed outputs')
    return result


def verify(args):
    frozen=validate(args.inventory,args.inventory_sha256)
    git_receipt=git_state(args,frozen)
    out=fresh(args.output);out.mkdir(parents=True)
    result={'schema':'ym22-final-verification-v1','status':'running','loops':list(LOOPS),
            'inventory_sha256':args.inventory_sha256,'bound_files':len(frozen['files']),
            'research_loops_added':0,'git':git_receipt}
    try:
        replay_rows=[]
        for optimized in [False,True]:
            mode='optimized' if optimized else 'normal'
            flags=['-B']+(['-O'] if optimized else [])
            command=[sys.executable,*flags,str(source('research/round22/reproduce.py')),
                     '--output',str(out/mode)]
            if optimized:command.append('--optimized')
            result[mode]=run(command,out/(mode+'.log'))
            replay=read(out/mode/'reproduction.json')
            rows=validate_replay_summary(replay,LOOPS,optimized)
            replay_rows.append(rows)
            result['admission_'+mode]=run([sys.executable,*flags,str(source('research/round22/test_admission.py')),
                '--loop','n1','--output',str(out/('admission-'+mode+'.json'))],out/('admission-'+mode+'.log'))
            controls=read(out/('admission-'+mode+'.json'))
            validate_admission_summary(controls,optimized)
        require(replay_rows[0]==replay_rows[1],'normal/optimized scientific hashes differ')
        result['normal_optimized_scientific_hashes_equal']=True
        # Recovering unchanged historical semantics is a separate dependency replay, never new research.
        result['inherited']=run([sys.executable,'-B',str(source('research/round21/reproduce.py')),
            '--output',str(out/'inherited'),'--loops',*INHERITED],out/'inherited.log')
        legacy_replay=read(out/'inherited/reproduction.json')
        validate_replay_summary(legacy_replay,INHERITED,False)
        result['c2_repair']=run([sys.executable,'-B',str(source('research/round21/release/replay_c2.py')),
            '--output',str(out/'c2')],out/'c2.log')
        c2=read(out/'c2/replay.json')
        validate_c2_summary(c2)
        result.update(verify_site(frozen,out))
        validate(args.inventory,args.inventory_sha256)
        require(git_state(args,frozen)==git_receipt,'Git release state changed during verification')
        result['status']='passed'
        result['research_producer_executions']=40
        result['inherited_producer_executions']=20
        result['browser_audit']='separate reviewed artifact; these commands check static rendering and behavior fixtures'
    except Exception as error:
        result.update(status='failed',error=str(error));write(out/'final-verification.json',result);raise
    write(out/'final-verification.json',result)
    print(json.dumps({'status':'passed','research_loops':10,'producer_executions':40,'output':str(out)}))


def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True)
    for name in ['inventory','preflight']:
        s=sub.add_parser(name);s.add_argument('--output',type=Path,required=True)
    s=sub.add_parser('verify');s.add_argument('--output',type=Path,required=True)
    s.add_argument('--inventory',type=Path,required=True);s.add_argument('--inventory-sha256',required=True)
    s.add_argument('--git-commit',required=True);s.add_argument('--git-tree',required=True)
    args=p.parse_args()
    if args.mode=='verify':verify(args);return
    out=fresh(args.output)
    if args.mode=='inventory':data=inventory()
    else:
        _,gates,*_=preflight();data={'status':'passed','verdicts':{n:g['status'] for n,g in gates.items()}}
    write(out,data);print(json.dumps({'status':data.get('status','candidate'),'sha256':digest(out)}))


if __name__=='__main__':main()
