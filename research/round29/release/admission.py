#!/usr/bin/env python3
"""Validate transitive Round29 evidence and declared semantic control contracts.

This checks recorded scope integrity, not arbitrary mathematical English. The
release contract is a separately versioned review inventory; a release receipt
pins the complete Git tree containing that inventory and this validator.
"""
from __future__ import annotations
import hashlib
import ast
from fractions import Fraction
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'research/round29/'
FINAL = {'accepted_within_scope', 'accepted_with_limitations', 'accepted_within_scope_limited', 'limited', 'insufficient'}


def require(ok, why):
    if not ok: raise ValueError(why)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path): return json.loads(path.read_text())


def scope_digest(gate):
    record = {key: gate.get(key) for key in ('loop', 'sequence', 'title', 'verdict', 'accepted', 'limitations')}
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def local(root, relative):
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute(), 'Unsafe relative evidence path')
    require(not any(part in ('', '.', '..') for part in relative.split('/')), 'Noncanonical evidence path')
    path = root / relative
    require(not path.is_symlink() and path.resolve().is_relative_to(root.resolve()), 'Evidence escapes source tree')
    require(path.is_file(), 'Missing evidence: ' + relative)
    return path


def bindings(root, values, context):
    require(isinstance(values, dict) and values, context + ': bindings missing')
    for relative, expected in values.items():
        require(isinstance(expected, str) and re.fullmatch('[0-9a-f]{64}', expected), context + ': invalid digest')
        require(digest(local(root, relative)) == expected, context + ': changed ' + relative)


def validate_loop(root, loop, gate=None, row=None, *, require_spec=True):
    """Return review receipt; permit unknown prospective specs only at initial gate recording."""
    root = Path(root).resolve(); loop = str(loop).lower()
    require(re.fullmatch('[a-z]+[12]', loop), 'Invalid loop identifier')
    base = root / PREFIX
    gate = load(base / f'advisor/{loop}-gate.json') if gate is None else gate
    require(str(gate.get('loop', '')).lower() == loop, 'Gate loop mismatch')
    require(type(gate.get('sequence')) is int and 1 <= gate['sequence'] <= 10, 'Gate sequence missing')
    require(gate.get('completed_at'), 'Gate completion missing')
    require(gate.get('verdict') in FINAL, 'Gate final verdict missing')
    require(isinstance(gate.get('accepted'), str) and gate['accepted'].strip(), 'Accepted scope missing')
    require(isinstance(gate.get('limitations'), list) and gate['limitations'] and all(isinstance(v, str) and v.strip() for v in gate['limitations']), 'Explicit limitations missing')
    if row is not None:
        for field, rowfield in [('loop', 'id'), ('sequence', 'sequence'), ('title', 'title'), ('verdict', 'status'), ('accepted', 'accepted'), ('limitations', 'limitations')]:
            require(gate[field] == row.get(rowfield), 'Findings/gate mismatch: ' + field)
    required = {PREFIX + f'contracts/{loop}.json'}
    required |= {PREFIX + f'skeptic/{loop}{tail}' for tail in ('.md', '.json', '_check.py', '-checks.json')}
    for side in ('forward', 'reverse'):
        required |= {PREFIX + f'{side}/{loop}/{name}' for name in ('check.py', 'report.md', 'freeze.json', 'output/results.json')}
    require(required <= gate.get('bindings', {}).keys(), 'Gate omits required counterpart/review/source')
    bindings(root, gate['bindings'], 'Gate')
    contract = load(base / f'contracts/{loop}.json')
    require(str(contract.get('id', contract.get('loop', ''))).lower() == loop, 'Contract loop mismatch')
    control_statements = contract.get('controls', []) + [value for value in contract.get('required', []) if 'control' in str(value).lower()]
    require(bool(control_statements), 'Prospective negative controls missing')
    release_contract_path = base / 'release/admission-contract.json'
    release = load(release_contract_path) if release_contract_path.is_file() else {}
    spec = release.get('loops', {}).get(loop)
    require(spec is not None or not require_spec, 'Reviewed semantic specification missing: ' + loop)
    if spec:
        require(spec['contract_sha256'] == digest(base / f'contracts/{loop}.json'), 'Prospective contract changed')
        require(spec['reviewed_scope_sha256'] == scope_digest(gate), 'Recorded accepted scope or limitations changed')
    for side in ('forward', 'reverse'):
        relative = PREFIX + f'{side}/{loop}/'; producer = root / relative
        freeze = load(producer / 'freeze.json')
        require(str(freeze.get('loop', '')).lower() == loop and freeze.get('direction') == side, 'Freeze identity mismatch')
        require(freeze.get('frozen') is True or freeze.get('status') == 'frozen_for_review', 'Producer is not frozen')
        raw = freeze.get('files')
        if isinstance(raw, list):
            require(len(raw) == len({item['path'] for item in raw}), 'Duplicate frozen input')
            inventory = {item['path']: item['sha256'] for item in raw}
        else: inventory = raw
        require(isinstance(inventory, dict), 'Freeze inventory missing')
        required_local = {'check.py', 'report.md', 'output/results.json', f'inputs/{PREFIX}contracts/{loop}.json'}
        required_local |= {str(p.relative_to(producer)) for p in (producer/'output').glob('*manifest.json') if p.is_file()}
        required_local |= {str(p.relative_to(producer)) for p in (producer / 'inputs').rglob('*') if p.is_file()}
        require(required_local <= inventory.keys(), 'Freeze omits required input or result')
        for name, expected in inventory.items():
            path = local(producer, name)
            require(digest(path) == expected, 'Changed frozen producer input: ' + relative + name)
            require(gate['bindings'].get(relative + name) == expected, 'Gate omits frozen producer dependency')
        require((producer / f'inputs/{PREFIX}contracts/{loop}.json').read_bytes() == (base / f'contracts/{loop}.json').read_bytes(), 'Copied prospective contract differs')
        result = load(producer / 'output/results.json')
        require(str(result.get('loop', '')).lower() == loop and result.get('direction') == side, 'Result identity mismatch')
        controls = result.get('controls', {})
        require(isinstance(controls, dict) and all(value is True for value in controls.values()), 'A negative control did not discriminate')
        checks = result.get('checks', [])
        require(isinstance(checks, list) and len(checks) == len(set(checks)), 'Duplicate/invalid executed checks')
        require(controls or checks, 'No semantic checks recorded')
        if spec:
            expected = spec['directions'][side]
            require(set(expected.get('controls', [])) <= controls.keys(), 'Required control omitted')
            require(set(expected.get('checks', [])) <= set(checks), 'Required executable check omitted')
            for key, value in expected.get('assertions', {}).items():
                require(type(result.get(key)) is type(value) and result[key] == value, 'Result scope assertion changed: ' + key)
        if loop == 'am2':
            keys = ('G_cap','G_prime_cap','self_map_cap','Lipschitz_cap','exclusion_cap') if side == 'forward' else ('G_upper','Gprime_upper','selfmap_upper','lipschitz_upper','shifted_resolvent_contraction_upper')
            majorant, derivative, selfmap, contraction, exclusion = [Fraction(result[key]) for key in keys]
            J = Fraction(result['J_cap']); radius = Fraction(1,64)
            require(J == Fraction(28,100000000) and majorant == Fraction(148,7) and derivative == 352, 'AM2 numerical source budgets changed')
            require(selfmap == J*majorant and selfmap < radius, 'AM2 self-map is not strict')
            require(contraction == J*derivative and exclusion == 2*contraction and 0 <= exclusion < 1, 'AM2 contraction/exclusion is not strict')
        # These manifests record the actual producer dependencies, independent of gate hashes.
        manifests = [producer / 'output/source-manifest.json', producer / 'output/manifest.json']
        manifest = next((load(p) for p in manifests if p.is_file()), None)
        require(isinstance(manifest, dict), 'Producer source inventory missing')
        source_values = manifest.get('sources') or {item['path']: item['sha256'] for item in manifest.get('source_files', [])}
        require({'check.py', 'report.md'} | {name for name in required_local if name.startswith('inputs/')} <= source_values.keys(), 'Producer manifest omits declared source')
        for name, expected in source_values.items():
            require(digest(local(producer, name)) == expected, 'Producer manifest source mismatch')
        result_sha = manifest.get('results_sha256', manifest.get('outputs', {}).get('results.json'))
        require(result_sha == digest(producer / 'output/results.json'), 'Producer manifest result mismatch')
    review = load(base / f'skeptic/{loop}.json')
    require(str(review.get('loop', '')).lower() == loop and bool(re.match(r'^(accepted|limited|insufficient)(?:$|[_ -])', str(review.get('verdict', '')))), 'Skeptical verdict identity missing')
    require(review.get('blocking_issues') == [], 'Blocking or absent independent review')
    reviewed_sources = {PREFIX + f'contracts/{loop}.json'} | {PREFIX + f'{side}/{loop}/{name}' for side in ('forward', 'reverse') for name in ('check.py', 'report.md', 'freeze.json')}
    reviewed_sources |= {PREFIX + f'skeptic/{loop}{tail}' for tail in ('.md','_check.py','-checks.json')}
    reviewer_source = base/f'skeptic/{loop}_check.py'
    for node in ast.walk(ast.parse(reviewer_source.read_text())):
        modules = [node.module] if isinstance(node,ast.ImportFrom) and node.module else [alias.name for alias in node.names] if isinstance(node,ast.Import) else []
        for module in modules:
            helper=reviewer_source.parent/(module.split('.')[0]+'.py')
            if helper.is_file(): reviewed_sources.add(str(helper.relative_to(root)))
    require(reviewed_sources <= review.get('bindings', {}).keys(), 'Reviewer omits a frozen counterpart')
    bindings(root, review['bindings'], 'Independent review')
    checks = load(base / f'skeptic/{loop}-checks.json')
    require(str(checks.get('loop', '')).lower() == loop, 'Skeptical checks loop mismatch')
    if spec:
        require(set(spec.get('skeptic_checks', [])) <= set(checks.get(spec.get('skeptic_check_field','checks'), [])), 'Skeptical semantic check omitted')
        for key, value in spec.get('skeptic_assertions', {}).items():
            require(type(checks.get(key)) is type(value) and checks[key] == value, 'Skeptical scope assertion changed: ' + key)
        for relative, expected in release.get('support_dependencies', {}).items():
            require(digest(local(root, relative)) == expected, 'Release support dependency changed')
    return {'loop': loop, 'sequence': gate['sequence'], 'controls_semantically_checked': spec is not None, 'scope_sha256': scope_digest(gate)}
