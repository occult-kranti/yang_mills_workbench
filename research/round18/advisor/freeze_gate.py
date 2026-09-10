"""Freeze complete role evidence; math must also be independently replayed."""
from pathlib import Path
import argparse, hashlib, json
HERE = Path(__file__).resolve().parents[1]
LOOPS = ('a1', 'a2', 'b1', 'b2', 'c1', 'c2')

def checked_path(path):
    # Do not resolve the supplied path: resolution would erase a symlink.
    p=Path(path)
    if not p.is_absolute():p=Path.cwd()/p
    try:relative=p.relative_to(HERE)
    except ValueError as exc:raise ValueError('Evidence path is outside the accepted round') from exc
    if '..' in relative.parts:raise ValueError('Parent traversal in evidence path')
    current=HERE
    if current.is_symlink():raise ValueError('Symlink evidence root')
    for part in relative.parts:
        current/=part
        if current.is_symlink():raise ValueError('Symlink evidence component')
    return current

def digest(path):
    return hashlib.sha256(checked_path(path).read_bytes()).hexdigest()

def inventory(loop):
    if loop not in LOOPS:
        raise ValueError('Unknown loop')
    files = []
    for role in ('forward', 'backward'):
        root = checked_path(HERE / role / loop)
        if not root.is_dir():
            raise ValueError('Missing role evidence')
        for path in sorted(root.rglob('*')):
            if '__pycache__' in path.parts:
                continue
            if path.is_symlink():
                raise ValueError('Symlink evidence')
            if path.is_file():
                files.append(path)
    files += [HERE/'advisor/initial-plan.md', HERE/'advisor/planning-gate.json', HERE/'advisor/source-audit.md']
    contract = HERE/'advisor'/(loop+'-contract.md')
    if not contract.is_file():
        raise ValueError('Missing frozen loop contract')
    files.append(contract)
    index=LOOPS.index(loop)
    if index>=2:
        files.append(HERE/'advisor/b1-amendment.md')
    if index>=3:
        files += [HERE/'advisor/b2-matching-note.md',HERE/'advisor/physical-matching-supplement.md']
    if index:
        files.append(HERE/'advisor'/(LOOPS[index-1]+'-gate.json'))
    if index>=2:
        files.append(HERE/'advisor/post-a-roadmap.md')
        files.append(HERE/'advisor/post-a-gate.json')
        files.extend(sorted(checked_path(HERE/'advisor/post-a-reviews').glob('*')))
    return {str(p.relative_to(HERE)): digest(p) for p in files}

def verify(path):
    record = json.loads(checked_path(path).read_bytes())
    if type(record) is not dict:raise ValueError('Invalid gate object')
    if record.get('status') != 'accepted' or record.get('files') != inventory(record.get('loop')):
        raise ValueError('Stale or incomplete loop evidence')
    return record

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('gate'); args = p.parse_args()
    print(json.dumps({'status':'passed','loop':verify(args.gate)['loop']}))
