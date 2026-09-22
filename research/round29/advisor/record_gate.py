#!/usr/bin/env python3
"""Record an advisor decision supplied on stdin; never derive admission from counts."""
import datetime, hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
R = ROOT / 'research/round29'
sys.path.insert(0,str(ROOT))
from research.round29.release.admission import validate_loop
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    d = json.load(sys.stdin)
    loop = d['loop'].lower()
    target = R / 'advisor' / f'{loop}-gate.json'
    if target.exists(): raise SystemExit('A recorded gate is immutable; make an explicit repair record')
    findings_path = R / 'advisor/findings.json'
    f = json.loads(findings_path.read_text()) if findings_path.exists() else {'round':29,'author':'Hruday N M (BUNZEEY)','loops':[],'completed':0,'planned_next':[]}
    if d['sequence'] != len(f['loops']) + 1: raise SystemExit('Nonsequential gate')
    if d['sequence'] > 10: raise SystemExit('Authorized research-loop boundary')
    required = [R/'contracts'/f'{loop}.json']
    for direction in ('forward','reverse'):
        p=R/direction/loop
        if not (p/'report.md').is_file() or not (p/'freeze.json').is_file(): raise SystemExit(f'Missing frozen {direction}')
        required += [x for x in sorted(p.rglob('*')) if x.is_file() and '__pycache__' not in x.parts]
    review = R/'skeptic'/f'{loop}.md'
    if not review.is_file(): raise SystemExit('Missing independent review')
    required += [review]
    required += [p for p in sorted((R/'skeptic').glob(f'{loop}*')) if p.is_file()]
    d['completed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    d['bindings'] = {str(p.relative_to(ROOT)):sha(p) for p in sorted(set(required))}
    validate_loop(ROOT,loop,gate=d,require_spec=False)
    target.write_text(json.dumps(d,indent=2)+'\n')
    f['loops'].append({'id':d['loop'],'sequence':d['sequence'],'title':d['title'],'status':d['verdict'],'accepted':d['accepted'],'limitations':d['limitations'],'evidence':str(target.relative_to(ROOT))})
    f['completed']=len(f['loops'])
    findings_path.write_text(json.dumps(f,indent=2)+'\n')
    print(json.dumps({'loop':d['loop'],'verdict':d['verdict'],'bindings':len(d['bindings'])}))
if __name__ == '__main__': main()
