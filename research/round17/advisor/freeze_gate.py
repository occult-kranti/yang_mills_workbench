"""Freeze complete role evidence; math must also be independently replayed."""
from pathlib import Path
import argparse, hashlib, json
HERE = Path(__file__).resolve().parents[1]
LOOPS = ('a1', 'a2', 'b1', 'b2', 'c1', 'c2')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inventory(loop):
    if loop not in LOOPS:
        raise ValueError('Unknown loop')
    files = []
    for role in ('forward', 'backward'):
        root = HERE / role / loop
        if not root.is_dir():
            raise ValueError('Missing role evidence')
        for path in sorted(root.rglob('*')):
            if '__pycache__' in path.parts:
                continue
            if path.is_symlink():
                raise ValueError('Symlink evidence')
            if path.is_file():
                files.append(path)
    files += [HERE/'advisor/revised-plan.md', HERE/'advisor/source-audit.md']
    contract = HERE/'advisor'/(loop+'-contract.md')
    if not contract.is_file():
        raise ValueError('Missing frozen loop contract')
    files.append(contract)
    index=LOOPS.index(loop)
    if index:
        files.append(HERE/'advisor'/(LOOPS[index-1]+'-gate.json'))
    if index>=2:
        files.append(HERE/'advisor/post-a-roadmap.md')
    return {str(p.relative_to(HERE)): digest(p) for p in files}

def verify(path):
    record = json.loads(Path(path).read_bytes())
    if record.get('status') != 'accepted' or record.get('files') != inventory(record.get('loop')):
        raise ValueError('Stale or incomplete loop evidence')
    return record

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('gate'); args = p.parse_args()
    print(json.dumps({'status':'passed','loop':verify(args.gate)['loop']}))
