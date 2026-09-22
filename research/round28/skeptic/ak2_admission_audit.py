#!/usr/bin/env python3
"""Additive AK2 final specification audit; no producer or release arithmetic imports.

The generic exact-expression evaluator is carried from this reviewer's AK1/AJ2
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
SPEC = BASE + 'advisor/ak2-admission.json'
EXPECTED = '7e4994db9dbae28682756f3379aadc6bce653690ea34ab6acebcfd5289c573b8'
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


def audit_repository_freeze(side, section):
    prefix = BASE + side + '/ak2/'
    require(section['freeze_binding_field'] == 'bindings' and 'freeze_path_base' not in section,
            'existing repository-relative bindings convention: ' + side)
    freeze_path = prefix + 'freeze.json'
    require(section['freeze'] == freeze_path, 'exact top-level freeze: ' + side)
    frozen = read(freeze_path)['bindings']
    require(all(type(p) is str and p.startswith(prefix) for p in frozen), 'all producer members owned: ' + side)
    paths = list(local(prefix).rglob('*'))
    require(not any(p.is_symlink() for p in paths), 'no linked producer member: ' + side)
    actual = {str(p.relative_to(ROOT)) for p in paths if p.is_file() and p != local(freeze_path)}
    require(set(frozen) == actual and len(frozen) == (91 if side == 'forward' else 74),
            'exact entire frozen producer owned file set: ' + side)
    for p, h in frozen.items():
        bind(p, h)
    for p in section['adoption_records']:
        require(p in frozen, 'nested input adoption record retained: ' + p)
    return frozen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    target = Path(parser.parse_args().output)
    if not target.is_absolute() or target.exists():
        raise ValueError('output must be a fresh absolute file')
    bind(SPEC, EXPECTED)
    spec = read(SPEC)
    require(spec['loop'] == 'ak2', 'exact AK2 loop')
    require(spec['status'] == 'advisor-approved admission specification; mathematical acceptance is recorded by the separate gate',
            'root-approved specification status')
    require(len(spec['bindings']) == 640, 'exact final 640 direct bindings')
    for p, h in spec['bindings'].items():
        bind(p, h)
    cpath = BASE + 'contracts/ak2.json'
    require(sha(cpath) == 'ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601', 'original tenth contract')
    contract = read(cpath)
    required = {**contract['sources'], cpath: sha(cpath)}
    require(contract['sequence'] == 10 and len(contract['sources']) == 50, '50 original contract sources')
    counts, closures, snapshots = {}, {}, {}
    freeze_hashes = {'forward': 'ce0e3aefea9cc699d66a205a3093ca9cb2126ead6f87f22fd05b83d39d13881d',
                     'reverse': 'fee1e8b39c5f2f07766d3ba098d73cb3f3ae29d2480a753ca09fecc3f18218a5'}
    require(set(spec['producers']) == set(freeze_hashes), 'exact paired producers')
    for side, section in spec['producers'].items():
        prefix = BASE + side + '/ak2/'
        output = prefix + 'output/results.json'
        result = read(output)
        counts[side] = project(section, result, side)
        require(counts[side] == (138 if side == 'forward' else 144), 'all final producer semantic and rational relations: ' + side)
        scope = '/analytic_claims' if side == 'forward' else '/scope'
        require(section['scope_pointer'] == scope and bool(pointer(result, scope)), 'actual producer scope: ' + side)
        bind(section['freeze'], freeze_hashes[side])
        frozen = audit_repository_freeze(side, section)
        closures[side] = len(frozen)
        require(section['binding_field'] == 'bindings', 'actual flat runtime map: ' + side)
        for p, h in result['bindings'].items():
            bind(p, h)
        require(len(result['bindings']) == (139 if side == 'forward' else 124), 'entire runtime binding count: ' + side)
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
        require(len(copied) == (81 if side == 'forward' else 66), 'all actual snapshots counted: ' + side)
        actual_outputs = {str(p.relative_to(local(prefix + 'output'))) for p in local(prefix + 'output').rglob('*') if p.is_file()}
        require(actual_outputs == {'results.json'}, 'entire stored output set: ' + side)
    supplemental = {s['path']: s for s in spec['supplemental_evidence']}
    independent = BASE + 'skeptic/ak2-independent.json'
    postpath = BASE + 'skeptic/ak2-post-review.json'
    newtonpath = BASE + 'experts/newton/ak2-comparison-sources.json'
    expected_supplements = {independent: ('/scope', 51), newtonpath: ('/method_scope', 15), postpath: ('/supported', 27)}
    require(set(supplemental) == set(expected_supplements), 'exact independent, Newton and postreview supplements')
    for p, section in supplemental.items():
        data = read(p)
        counts[p] = project(section, data, p)
        scope, n = expected_supplements[p]
        require(section['scope_pointer'] == scope and bool(pointer(data, scope)), 'actual supplemental scope: ' + p)
        require(counts[p] == n, 'all supplemental semantics and relations: ' + p)
        if 'binding_field' in section:
            require(section['binding_field'] == 'bindings', 'actual supplemental binding field: ' + p)
            for source, h in data['bindings'].items():
                require(spec['bindings'].get(source) == h, 'directly bound supplemental source: ' + source)
                bind(source, h)
    for name, expected, count in [
        ('ak2-independent-freeze.json','08ab8f8b7278fb0db731b5b43a09b53b76a6617972ec01761657c2e2dee706f1',81),
        ('ak2-post-review-freeze.json','64ee47060506121dc8706de1b4b11181eae92abc69cb3f15370faccbdc7a8eec',326)]:
        p = BASE + 'skeptic/' + name
        bind(p, expected)
        require(len(read(p)['bindings']) == count, 'unchanged skeptical freeze member count: ' + name)
        for source, h in read(p)['bindings'].items():
            bind(source, h)
    expected_checkers = {BASE + 'skeptic/ak2_independent.py': (independent,515,143),
                         BASE + 'skeptic/ak2_post_review.py': (postpath,1655,637)}
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
    for name, n in [('ak2-inputs/source-inventory.json',73), ('ak2-post-review-inputs/source-inventory.json',317)]:
        entries = read(BASE + 'skeptic/' + name)['entries']
        require(len(entries) == n, 'all skeptical owned snapshots: ' + name)
        for entry in entries:
            bind(entry['snapshot'], entry['sha256'])
            if entry.get('external_instruction_snapshot'):
                require(Path(entry['source']).is_absolute(), 'installed provenance remains metadata only')
            else:
                bind(entry['source'], entry['sha256'])
    post = read(postpath)
    supported = post['supported']
    require(post['blocking_objections'] == [] and supported['new_research_loops'] == 0, 'scoped postreview has no blockers or new investigation')
    require(supported['physical_first_moment_upper_over_alpha'] == '1' and supported['actual_physical_form_domain'] is True
            and supported['closed_window_in_alpha_units'] == ['1/16','10'] and supported['closed_window_mass_lower'] == '1/10'
            and supported['lower_heat_prefactor'] == '1/5' and supported['lower_heat_exponent_alpha_t_over_hbar'] == '5',
            'all four frozen quantitative targets')
    require(supported['strict_symbolic_tau_star_and_extra_cap_required'] is True
            and supported['source_constants_evaluated'] is False
            and supported['limiting_first_moment_equality_claim'] is False
            and supported['infinite_operator_domain_or_second_moment'] is False,
            'conditional coupling and upper-moment/form-only scope')
    require(supported['forward_preexecution_syntax_failure_preserved'] is True
            and supported['reading_depths_disclosed'] is True and supported['eleventh_science_investigation'] is False,
            'preserved preparation history, reading depths and investigation stopping boundary')
    local_control = post['local_character_clarification']
    require(local_control['extension'] == 'A_R tensor identity outside R'
            and local_control['global_vacuum_projector_used'] is False
            and local_control['local_region_links'] == 48 and local_control['endpoint_actions'] == 36
            and local_control['local_vectors_endpoint_invariant'] is True,
            'complete actual-local tensor-identity clarification')
    newton = read(newtonpath)
    clarification = newton['reverse_centering_metadata_clarification']
    require(clarification['frozen_value'] == 1 and clarification['implemented_positive_energy_over_alpha'] == 4
            and clarification['status'] == 'stale unused diagnostic metadata'
            and clarification['retrospective_intentional_lower_bound_claimed'] is False
            and clarification['actual_state_theorem_affected'] is False,
            'stale reverse diagnostic label explicitly acknowledged without retroactive reinterpretation')
    for p in [newtonpath, BASE + 'experts/newton/ak2-comparison.md']:
        require(p in spec['bindings'], 'Newton comparison and provenance directly approved: ' + p)
    replay = read(BASE + 'skeptic/ak2-post-producer-replay.json')
    require(replay['all_fresh_normal_optimized_exact_outputs_equal'] is True and len(replay['runs']) == 4,
            'existing required four producer replays relied upon without repetition')
    require({(r['direction'],r['mode']) for r in replay['runs']} ==
            {(d,m) for d in ['forward','reverse'] for m in ['normal','optimized']}, 'all paired replay modes')
    for r in replay['runs']:
        expected = {'results.json': sha(BASE + r['direction'] + '/ak2/output/results.json')}
        require(r['exit_code'] == 0 and r['files'] == r['frozen_files'] == expected,
                'full-output replay record: ' + r['direction'] + ':' + r['mode'])
        require(Path(r['command'][2 if r['mode'] == 'normal' else 3]).is_absolute()
                and Path(r['cwd']) != ROOT and r['fresh_absolute_directory'] is True,
                'absolute entrypoint from nonrepository cwd: ' + r['direction'] + ':' + r['mode'])
    for name, output in [('ak2-independent-replay.json',independent), ('ak2-post-review-replay.json',postpath)]:
        p = BASE + 'skeptic/' + name
        bind(p, sha(p))
        record = read(p)
        require(record['normal_optimized_byte_identical'] is True and record['passed'] is True,
                'existing skeptical replay equality: ' + name)
        require(len(record['runs']) == 2 and all(r['exit_code'] == 0 and r['sha256'] == sha(output) for r in record['runs']),
                'existing skeptical replay output identity: ' + name)
    # Bound as current release machinery, never imported or executed here.
    bind(BASE + 'reproduce.py', '6ebf9b5116aba99cae5432796b890745872d7785d1bdedd8afee17d2a517b5fd')
    own = str(Path(__file__).resolve().relative_to(ROOT))
    bind(own, sha(own))
    limitations = post['limitations']
    require(len(limitations) == 8 and all(type(x) is str and x for x in limitations), 'eight explicitly approved scope limitations')
    result = {'schema': 'ym28-ak2-admission-spec-review-v1', 'loop': 'ak2', 'sequence': 10,
              'accepted': True, 'blocking_issues': [], 'specification': SPEC, 'specification_sha256': EXPECTED,
              'check_count': len(checks), 'checks': checks, 'bindings': dict(sorted(bindings.items())),
              'semantic_and_rational_counts': counts, 'producer_closure_counts': closures,
              'required_snapshot_counts': snapshots, 'limitations': limitations, 'supported': supported,
              'extra_research_loops': 0, 'producer_or_release_evaluator_imported': False,
              'review_role': 'Original independent AK2 skeptic, frozen before exchange, now final reviewer. Earlier AJ2 handoff role is distinct.',
              'scope': 'Exact final semantics/relations and full source, snapshot, runtime and frozen closures; unchanged existing repository bindings format and reproducibility machinery; existing full-output normal/-O replays preserved without duplication.'}
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'check_count': len(checks), 'counts': counts, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
