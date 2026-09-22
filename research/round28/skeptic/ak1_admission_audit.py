#!/usr/bin/env python3
"""Additive AK1 final specification audit; no producer or release arithmetic imports.

The generic exact-expression evaluator is carried from this reviewer's AJ2
admission audit. This is post-exchange review, not another science investigation.
"""
import argparse
import hashlib
import json
import operator
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = 'research/round28/'
SPEC = BASE + 'advisor/ak1-admission.json'
EXPECTED = 'cc5f011aa98b0b93de22705e2dee242eacd2cbad33271f1d88b647846b0b5eb0'
checks = []
bindings = {}


def require(condition, label):
    if not condition:
        raise ValueError(label)
    checks.append(label)


def local(path):
    p = Path(path)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('nonlocal evidence path: ' + path)
    q = ROOT
    for part in p.parts:
        q /= part
        if q.is_symlink():
            raise ValueError('symlink evidence path: ' + path)
    return q


def sha(path):
    return hashlib.sha256(local(path).read_bytes()).hexdigest()


def bind(path, digest):
    require(sha(path) == digest, 'exact binding ' + path)
    if path in bindings:
        require(bindings[path] == digest, 'consistent repeated binding ' + path)
    bindings[path] = digest


def read(path):
    return json.loads(local(path).read_text())


def pointer(obj, path):
    if not path.startswith('/'):
        raise ValueError('invalid pointer')
    for key in path[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj


def rational(value):
    if type(value) is dict:
        if set(value) != {'numerator', 'denominator'}:
            raise ValueError('rational object fields')
        n, d = value['numerator'], value['denominator']
        if type(n) is not int or type(d) is not int or d <= 0:
            raise ValueError('rational integer fields')
        return Fraction(n, d)
    if type(value) not in (str, int):
        raise ValueError('rational scalar type')
    return Fraction(value)


def expression(expr, data, depth=0):
    if depth > 20 or type(expr) is not dict or len(expr) != 1:
        raise ValueError('expression shape')
    kind, args = next(iter(expr.items()))
    if kind == 'constant':
        return rational(args)
    if kind == 'pointer':
        return rational(pointer(data, args))
    if kind == 'length':
        return Fraction(len(pointer(data, args)))
    values = [expression(x, data, depth + 1) for x in args]
    if kind == 'sum':
        return sum(values, Fraction(0))
    if kind == 'product':
        result = Fraction(1)
        for value in values:
            result *= value
        return result
    if kind in ('difference', 'quotient', 'power') and len(values) != 2:
        raise ValueError('binary expression arity')
    if kind == 'difference':
        return values[0] - values[1]
    if kind == 'quotient':
        return values[0] / values[1]
    if kind == 'power':
        if values[1].denominator != 1 or abs(values[1]) > 64:
            raise ValueError('power outside audit range')
        return values[0] ** int(values[1])
    if kind == 'minimum':
        return min(values)
    if kind == 'maximum':
        return max(values)
    if kind == 'absolute' and len(values) == 1:
        return abs(values[0])
    raise ValueError('unsupported arithmetic operation')


OPS = {'eq': operator.eq, 'ne': operator.ne, 'lt': operator.lt,
       'le': operator.le, 'gt': operator.gt, 'ge': operator.ge}


def project(section, data, label):
    before = len(checks)
    for control in section['semantic_controls']:
        actual = json.dumps(pointer(data, control['pointer']), sort_keys=True)
        expected = json.dumps(control['equals'], sort_keys=True)
        require(actual == expected, label + ' semantic ' + control['id'])
    for control in section['rational_relations']:
        left = expression(control['left'], data)
        right = expression(control['right'], data)
        require(OPS[control['op']](left, right), label + ' relation ' + control['id'])
    return len(checks) - before


LIMITATIONS = [
    'Fixed I1/AJ1/AJ2 homogeneous omitted interaction, positive physical scales, original origin xz Wilson and whole-star positive-orthant boundary only.',
    'Requires |tau| < unevaluated tau_* and additionally |tau| <= 2^-16; no certified numerical stability radius or selected positive admissible numerical coupling.',
    '119/576 is the common producer lower bound; 131/576 is the independent skeptic effect refinement. Neither is an evaluated interacting variance, sharp constant or interacting Haar moment.',
    'The controlled energy is normalized local reference energy for a generally mixed reduced density, not a physical Wilson-excited-vector first moment or purity statement.',
    'No physical excited-vector form/operator domain, f-sum identity, finite physical first moment, spectral-window mass, heat lower bound or AK2 theorem is established.',
    'Translated regions are incidence controls only; no uniform numerical target for all translates, other boundaries, models or couplings outside the stated regime.',
    'Finite exact diagnostics and source/replay audits support the analytic proof; the original I1 stability theorem is inherited and manuscript/network reading depths differ as disclosed.',
    'No continuum construction, continuum Yang-Mills mass gap, scientific-priority claim, historical validation or defensible percentage of the Millennium problem follows.'
]


def audit_repository_freeze(side, section):
    prefix = BASE + side + '/ak1/'
    require(section['freeze_binding_field'] == 'files' and section['freeze_path_base'] == 'repository',
            'explicit approved AK1-only repository files namespace: ' + side)
    freeze_path = prefix + 'freeze.json'
    require(section['freeze'] == freeze_path, 'exact top-level freeze: ' + side)
    frozen = read(freeze_path)['files']
    require(all(isinstance(p, str) and p.startswith(prefix) for p in frozen), 'all repository members owned: ' + side)
    paths = list(local(prefix).rglob('*'))
    require(not any(p.is_symlink() for p in paths), 'no linked producer member: ' + side)
    actual = {str(p.relative_to(ROOT)) for p in paths if p.is_file() and p != local(freeze_path)}
    require(set(frozen) == actual and len(frozen) == (85 if side == 'forward' else 65),
            'exact entire frozen producer owned file set: ' + side)
    for p, h in frozen.items():
        bind(p, h)
    # Nested input freezes are actual members, never broadly excluded.
    input_freeze = prefix + ('inputs-current-freeze.json' if side == 'forward' else 'inputs/freeze.json')
    require(input_freeze in frozen, 'input freeze retained in complete closure: ' + side)
    require(set(frozen) - {input_freeze} != actual, 'dropping input freeze is discriminating: ' + side)
    require({prefix + p for p in frozen} != actual, 'old producer-prefix interpretation rejected: ' + side)
    return frozen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    target = Path(parser.parse_args().output)
    if not target.is_absolute() or target.exists():
        raise ValueError('output must be a fresh absolute file')
    bind(SPEC, EXPECTED)
    spec = read(SPEC)
    require(spec['loop'] == 'ak1', 'exact AK1 loop')
    require(spec['status'] == 'advisor-approved admission specification; mathematical acceptance is recorded by the separate gate',
            'root-approved specification status')
    require(len(spec['bindings']) == 560, 'exact final 560 direct bindings')
    for p, h in spec['bindings'].items():
        bind(p, h)
    cpath = BASE + 'contracts/ak1.json'
    require(sha(cpath) == '2afd1ff408b4774e79f1964f796835c6e4088cce22de5c1c66c85d796c9a9810', 'original ninth contract')
    contract = read(cpath)
    required = {**contract['sources'], cpath: sha(cpath)}
    require(contract['sequence'] == 9 and len(contract['sources']) == 43, '43 original contract sources')
    counts, closures, snapshots = {}, {}, {}
    freeze_hashes = {'forward': '75fb5ec51c63e3264350be3236fa9dd3067c3a425381fb978bda126dc9e40ecd',
                     'reverse': 'c6810b72b2fef46cbab574d32ad205f4daccdc1c1267dc49774366df0ddbd588'}
    require(set(spec['producers']) == set(freeze_hashes), 'exact paired producers')
    for side, section in spec['producers'].items():
        prefix = BASE + side + '/ak1/'
        output = prefix + 'output/results.json'
        result = read(output)
        counts[side] = project(section, result, side)
        require(counts[side] == (107 if side == 'forward' else 100), 'all final producer semantic and rational relations: ' + side)
        require(section['scope_pointer'] == '/scope' and bool(result['scope']), 'actual producer scope: ' + side)
        bind(section['freeze'], freeze_hashes[side])
        frozen = audit_repository_freeze(side, section)
        closures[side] = len(frozen)
        require(section['binding_field'] == 'bindings', 'actual flat runtime map: ' + side)
        for p, h in result['bindings'].items():
            bind(p, h)
        require({prefix + 'check.py', cpath, *contract['sources']} <= result['bindings'].keys(),
                'active checker and all source originals directly runtime bound: ' + side)
        require(prefix + 'report.md' in frozen and section['report_binding'] == 'freeze', 'declared actual report convention: ' + side)
        copied, origins = {}, {}
        for manifest in section['source_manifests'] + section['instruction_manifests']:
            require(manifest in frozen and manifest in result['bindings'], 'executed frozen source inventory: ' + manifest)
            for entry in read(manifest)['entries']:
                p, h = entry['snapshot'], entry['sha256']
                bind(p, h)
                require(p in frozen and result['bindings'].get(p) == h, 'snapshot present in both closures: ' + p)
                require(p not in copied, 'unique required snapshot: ' + p)
                copied[p] = h
                if entry['source'] in required:
                    require(h == required[entry['source']], 'contract origin copied exactly: ' + entry['source'])
                    origins[entry['source']] = h
        require(origins == required, 'every controlling contract source and contract copied: ' + side)
        require(copied == section['required_snapshots'], 'exact declared snapshot projection: ' + side)
        snapshots[side] = len(copied)
        require(len(copied) == (74 if side == 'forward' else 57), 'all actual snapshots counted: ' + side)
        for p in section['adoption_records']:
            require(p in frozen, 'frozen input adoption record: ' + p)
        actual_outputs = {str(p.relative_to(local(prefix + 'output'))) for p in local(prefix + 'output').rglob('*') if p.is_file()}
        require(actual_outputs == {'results.json'}, 'entire stored output set: ' + side)
    supplemental = {s['path']: s for s in spec['supplemental_evidence']}
    independent = BASE + 'skeptic/ak1-independent.json'
    postpath = BASE + 'skeptic/ak1-post-review.json'
    require(set(supplemental) == {independent, postpath}, 'exact independent and postreview supplemental evidence')
    for p, section in supplemental.items():
        counts[p] = project(section, read(p), p)
        require(section['scope_pointer'] == ('/scope' if p == independent else '/supported'), 'actual supplemental scope: ' + p)
    require(counts[independent] == 27 and counts[postpath] == 9, 'all 27/9 supplemental controls')
    for name, expected, count in [
        ('ak1-independent-freeze.json','1296a0116c3f756bcad564dca5f9553d5eee397dfd11a507c0ea05886aa87bc0',72),
        ('ak1-post-review-freeze.json','1bb91799d30cd3ceff8e036c5655abd30f5bcd3a999a750ac2074240d7db41cd',281)]:
        p = BASE + 'skeptic/' + name
        bind(p, expected)
        require(len(read(p)['bindings']) == count, 'unchanged skeptical freeze member count: ' + name)
        for source, h in read(p)['bindings'].items():
            bind(source, h)
    expected_checkers = {BASE + 'skeptic/ak1_independent.py': (independent,757,119),
                         BASE + 'skeptic/ak1_post_review.py': (postpath,2477,549)}
    require({x['script'] for x in spec['skeptic_checkers']} == set(expected_checkers), 'both unchanged skeptical interfaces')
    for checker in spec['skeptic_checkers']:
        output, number, inputs = expected_checkers[checker['script']]
        require(checker['output'] == output and checker['output_mode'] == 'file'
                and checker['arguments'] == ['--output', '{output}'], 'exact executed file interface: ' + checker['script'])
        result = read(output)
        require(result['check_count'] == number and len(checker['inputs']) == inputs, 'exact interface counts: ' + checker['script'])
        require(set(checker['inputs']) == set(result['bindings']), 'entire actual runtime input projection: ' + checker['script'])
        for p in [checker['script'], output] + checker['inputs']:
            require(p in spec['bindings'], 'directly bound checker dependency: ' + p)
        for p, h in result['bindings'].items():
            bind(p, h)
    for name in ['ak1-inputs/source-inventory.json', 'ak1-post-review-inputs/source-inventory.json']:
        for entry in read(BASE + 'skeptic/' + name)['entries']:
            bind(entry['snapshot'], entry['sha256'])
            if entry.get('external_instruction_snapshot'):
                require(Path(entry['source']).is_absolute(), 'installed provenance remains metadata only')
            else:
                bind(entry['source'], entry['sha256'])
    post = read(postpath)
    require(post['blocking_objections'] == [] and post['supported']['new_research_loops'] == 0, 'scoped postreview has no blockers or new investigation')
    require(post['supported']['common_producer_lower_bound'] == '119/576'
            and post['supported']['independent_skeptic_effect_lower_bound'] == '131/576', 'separate exact proof attribution')
    require(post['supported']['finer_face_decomposition_universally_forbidden'] is False,
            'no broad impossibility inference from inherited group budget')
    require(post['supported']['requires_unevaluated_symbolic_tau_star'] is True
            and post['supported']['numeric_stability_radius_evaluated'] is False
            and post['supported']['physical_excited_vector_energy_moment_or_domain'] is False,
            'conditional cap and reference versus physical energy scope')
    replay = read(BASE + 'skeptic/ak1-post-producer-replay.json')
    require(replay['all_fresh_normal_optimized_exact_outputs_equal'] is True and len(replay['runs']) == 4,
            'existing required four producer replays relied upon without repetition')
    for r in replay['runs']:
        expected = {'results.json': sha(BASE + r['direction'] + '/ak1/output/results.json')}
        require(r['exit_code'] == 0 and r['files'] == r['frozen_files'] == expected,
                'full-output replay record: ' + r['direction'] + ':' + r['mode'])
    for name in ['ak1-independent-replay.json', 'ak1-post-review-replay.json']:
        p = BASE + 'skeptic/' + name
        bind(p, sha(p))
    # This reviewed implementation is bound, but never imported or executed here.
    implementation = BASE + 'reproduce.py'
    bind(implementation, '6ebf9b5116aba99cae5432796b890745872d7785d1bdedd8afee17d2a517b5fd')
    adapter = BASE + 'release/ak1-freeze-path-repair.md'
    bind(adapter, sha(adapter))
    for bad in [True, 0.5, {'numerator': True, 'denominator': 1}, {'numerator': 1, 'denominator': 0}]:
        try:
            rational(bad)
        except ValueError:
            require(True, 'reject inexact/malformed rational: ' + repr(bad))
        else:
            raise ValueError('invalid rational admitted')
    for path in ['/tmp/foreign', BASE + 'forward/ak1/../foreign']:
        try:
            local(path)
        except ValueError:
            require(True, 'reject foreign/traversal path: ' + path)
        else:
            raise ValueError('unsafe path admitted')
    require(json.dumps(True) != json.dumps(1), 'strict Boolean semantic equality')
    own = str(Path(__file__).resolve().relative_to(ROOT))
    bind(own, sha(own))
    require(len(LIMITATIONS) == 8, 'eight explicit accepted-scope limitations')
    result = {'schema': 'ym28-ak1-admission-spec-review-v1', 'loop': 'ak1', 'sequence': 9,
              'accepted': True, 'blocking_issues': [], 'specification': SPEC, 'specification_sha256': EXPECTED,
              'check_count': len(checks), 'checks': checks, 'bindings': dict(sorted(bindings.items())),
              'semantic_and_rational_counts': counts, 'producer_closure_counts': closures,
              'required_snapshot_counts': snapshots, 'limitations': LIMITATIONS,
              'extra_research_loops': 0, 'producer_or_release_evaluator_imported': False,
              'review_role': 'Original independent AK1 skeptic, frozen before exchange, now final reviewer. Earlier AJ2 handoff role is distinct.',
              'scope': 'Exact final semantics/relations and complete source, snapshot, runtime and frozen closure; reviewed AK1-only repository files adapter; existing full-output normal/-O replays preserved without duplication.'}
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'check_count': len(checks), 'counts': counts, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
