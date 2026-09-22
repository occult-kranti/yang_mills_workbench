#!/usr/bin/env python3
"""Additive AJ2 closeout audit; no producer or release arithmetic imports.

This checks preserved evidence and the final advisor specification. It is a
handoff review, not a new pre-exchange derivation or physics investigation.
"""
import argparse
import hashlib
import json
import operator
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = 'research/round28/'
SPEC = BASE + 'advisor/aj2-admission.json'
EXPECTED = '03824de0d51d27f801b09112ba20c7d4ae79105c56cc90378110c93d41c2692b'
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    target = Path(args.output)
    if not target.is_absolute() or target.exists():
        raise ValueError('output must be a fresh absolute file')
    spec = read(SPEC)
    bind(SPEC, EXPECTED)
    require(spec['loop'] == 'aj2', 'exact AJ2 loop')
    require(spec['status'] == 'advisor-approved admission specification; mathematical acceptance is recorded by the separate gate', 'advisor approval status')
    for path, digest in spec['bindings'].items():
        bind(path, digest)
    contract_path = BASE + 'contracts/aj2.json'
    contract = read(contract_path)
    required_origins = {**contract['sources'], contract_path: sha(contract_path)}
    counts, snapshots, closures, outputs = {}, {}, {}, {}
    expected_freezes = {
        'forward': 'ebfb34dbb578e3c343827d4c447309aeadec7a97a3b2df47525c88ae8d99d77d',
        'reverse': '5125a67b717cae2373ddc6807cc3a56e41d1b67658f1f6fdaa08f3d8fc3d0ef9'}
    for side, section in spec['producers'].items():
        prefix = BASE + side + '/aj2/'
        result_path = prefix + 'output/results.json'
        result = read(result_path)
        counts[side] = project(section, result, side)
        require(section['scope_pointer'] == '/scope', 'actual producer scope ' + side)
        require(bool(result['scope']), 'nonempty scientific scope ' + side)
        bind(section['freeze'], expected_freezes[side])
        freeze = read(section['freeze'])
        frozen = {(p if p.startswith(BASE) else prefix + p): h
                  for p, h in freeze[section['freeze_binding_field']].items()}
        actual = {str(p.relative_to(ROOT)) for p in local(prefix).rglob('*')
                  if p.is_file() and p != local(section['freeze'])}
        require(set(frozen) == actual, 'entire unchanged owned closure ' + side)
        for path, digest in frozen.items():
            bind(path, digest)
        closures[side] = len(frozen)
        require(section['binding_field'] == 'bindings', 'ordinary flat runtime map ' + side)
        for path, digest in result['bindings'].items():
            bind(path, digest)
        require(prefix + 'check.py' in result['bindings'], 'runtime checker identity ' + side)
        require(contract_path in result['bindings'], 'runtime contract identity ' + side)
        require(prefix + 'report.md' in frozen, 'actual report frozen ' + side)
        if section['report_binding'] == 'output_and_freeze':
            require(prefix + 'report.md' in result['bindings'], 'runtime report identity ' + side)
        manifest_paths = section['source_manifests'] + section['instruction_manifests']
        required_snapshots = {}
        covered_origins = {}
        for path in manifest_paths:
            require(path in frozen, 'owned inventory ' + path)
            for entry in read(path)['entries']:
                snapshot, digest = entry['snapshot'], entry['sha256']
                bind(snapshot, digest)
                require(snapshot in frozen and snapshot in result['bindings'], 'snapshot in both closures ' + snapshot)
                required_snapshots[snapshot] = digest
                if entry['source'] in required_origins:
                    require(digest == required_origins[entry['source']], 'contract source snapshot ' + entry['source'])
                    covered_origins[entry['source']] = digest
        require(covered_origins == required_origins, 'every contract source and contract copied ' + side)
        require(required_snapshots == section['required_snapshots'], 'complete exact required snapshot projection ' + side)
        snapshots[side] = len(required_snapshots)
        for path in section['adoption_records']:
            require(path in frozen, 'adoption record frozen ' + path)
        output_set = {p.name for p in local(prefix + 'output').iterdir() if p.is_file()}
        require(output_set == {'results.json'}, 'sole declared producer output ' + side)
        outputs[side] = sorted(output_set)
    for section in spec['supplemental_evidence']:
        counts[section['path']] = project(section, read(section['path']), section['path'])
        require(section['scope_pointer'] == '/supported', 'postreview actual supported projection')
    independent_freeze = BASE + 'skeptic/aj2-independent-freeze.json'
    bind(independent_freeze, '773aefb004ada5d3baef8cd147be2aa1001bdd57c711fd2a53cb5109d81ed40c')
    for path, digest in read(independent_freeze)['bindings'].items():
        bind(path, digest)
    expected_checkers = {BASE + 'skeptic/aj2_independent.py': 249,
                         BASE + 'skeptic/aj2_post_review.py': 1057}
    require({x['script'] for x in spec['skeptic_checkers']} == set(expected_checkers), 'exact two preserved checker interfaces')
    for checker in spec['skeptic_checkers']:
        require(checker['output_mode'] == 'file' and checker['arguments'] == ['--output', '{output}'], 'declared file interface ' + checker['script'])
        require(read(checker['output'])['check_count'] == expected_checkers[checker['script']], 'preserved executed check count ' + checker['script'])
        for path in [checker['script'], checker['output']] + checker['inputs']:
            require(path in spec['bindings'], 'direct checker dependency bound ' + path)
    for name in ['aj2-inputs/source-inventory.json', 'aj2-post-review-inputs/source-inventory.json']:
        for entry in read(BASE + 'skeptic/' + name)['entries']:
            bind(entry['snapshot'], entry['sha256'])
            bind(entry['source'], entry['sha256'])
    post = read(BASE + 'skeptic/aj2-post-review.json')
    require(len(post['limitations']) == 8, 'eight explicit scientific limits')
    require(any(c['pointer'] == '/limitations' and c['equals'] == post['limitations']
                for x in spec['supplemental_evidence'] for c in x['semantic_controls']), 'eight limits exactly preserved by final specification')
    require(post['blocking_issues'] == [] and post['new_research_loops'] == 0, 'preserved scoped review with no extra investigation')
    require(post['geometry'] == {'endpoints': 36, 'links': 48, 'outside_heads': 20,
                                'spectator_links_outside_face': 44, 'tail_vertices': 16}, 'complete reviewed geometry dimensions')
    for bad in [True, 0.5, {'numerator': True, 'denominator': 1}, {'numerator': 1, 'denominator': 0}]:
        try:
            rational(bad)
        except ValueError:
            require(True, 'reject inexact or malformed rational ' + repr(bad))
        else:
            raise ValueError('invalid rational admitted')
    require(json.dumps(True) != json.dumps(1), 'strict Boolean semantic equality')
    result = {'schema': 'ym28-aj2-admission-spec-review-v1', 'accepted': True,
              'blocking_issues': [], 'specification': SPEC, 'specification_sha256': EXPECTED,
              'check_count': len(checks), 'checks': checks, 'bindings': bindings,
              'semantic_and_rational_counts': counts, 'required_snapshot_counts': snapshots,
              'producer_closure_counts': closures, 'all_output_artifacts': outputs,
              'review_handoff': 'New closeout reviewer audits preserved independent and post-exchange evidence; no new pre-exchange derivation is claimed.',
              'extra_research_loops': 0,
              'scope': 'Independent evaluator of final approved exact semantics and rational relations, all producer source/runtime/frozen closures, contract snapshot completeness and preserved skeptic interfaces. Existing normal/-O producer replay records are relied on; no producer or release arithmetic evaluator is imported.'}
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'check_count': len(checks), 'counts': counts, 'snapshots': snapshots,
                      'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
