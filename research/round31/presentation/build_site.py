"""Build the Round31 reader only from three complete, source-bound reviews.

This is a presentation admission check, not a substitute for scientific review.
--check validates all inputs and compares the generated bundle without writing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
ROUND = 'research/round31'
AUTHOR = 'Hruday N M (BUNZEEY)'
LOOP_IDS = ('at4', 'at5', 'at6')
RELATIONS = {'proven-dependency', 'proposed-transfer', 'review-selection',
             'source-dependency', 'scope-boundary', 'recorded-equation'}
VERDICT = r'(accepted|limited|insufficient|rejected|failed)(?:[_ -][a-zA-Z0-9 _-]+)?'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name):
    require(isinstance(name, str) and bool(name), 'missing relative source path')
    require(not Path(name).is_absolute() and
            not re.search(r'[\\:#?<>\"\'\x00-\x20\x7f%]', name) and
            all(part not in ('', '.', '..') for part in name.split('/')),
            'unsafe source path ' + name)
    candidate = root
    for part in name.split('/'):
        candidate /= part
        require(not candidate.is_symlink(), 'symlink source ' + name)
    require(candidate.is_file(), 'missing source ' + name)
    return candidate


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def text_list(value, label, required=False):
    require(isinstance(value, list) and (not required or bool(value)) and
            all(nonempty(item) for item in value), 'invalid ' + label)
    return value


def build(root=ROOT):
    root = Path(root).resolve()
    bindings = {}

    def bind(name):
        path = local(root, name)
        bindings[name] = sha256(path)
        return path

    def read(name):
        data = json.loads(bind(name).read_text(encoding='utf-8'))
        require(isinstance(data, dict), 'expected JSON object ' + name)
        return data

    findings = read(ROUND + '/advisor/findings.json')
    rows = findings.get('loops')
    require(type(findings.get('completed')) is int and findings['completed'] == 3
            and isinstance(rows, list) and len(rows) == 3,
            'exactly three completed investigations required')
    loops = []
    for sequence, (loop_id, row) in enumerate(zip(LOOP_IDS, rows), 1):
        require(isinstance(row, dict) and row.get('id') == loop_id and
                type(row.get('sequence')) is int and row['sequence'] == sequence,
                'findings order/identifier mismatch ' + loop_id)
        expected_gate = ROUND + '/advisor/' + loop_id + '-gate.json'
        require(row.get('gate_path') == expected_gate, 'gate path mismatch ' + loop_id)
        gate = read(expected_gate)
        require(re.fullmatch(VERDICT, str(gate.get('verdict', ''))),
                'nonfinal verdict ' + loop_id)
        for key in ('title', 'accepted'):
            require(nonempty(gate.get(key)) and row.get(key) == gate[key],
                    'findings/gate ' + key + ' mismatch ' + loop_id)
        for key in ('summary', 'model', 'contribution_id'):
            require(nonempty(row.get(key)), 'missing ' + key + ' ' + loop_id)
        limitations = text_list(row.get('limitations'), 'limitations ' + loop_id, True)
        steps = text_list(row.get('derivation_steps'), 'derivation steps ' + loop_id, True)
        applications = text_list(row.get('applications'), 'applications ' + loop_id)
        for key in ('model', 'limitations', 'sequence'):
            if key in gate:
                require(gate[key] == row[key], 'findings/gate ' + key + ' mismatch ' + loop_id)
        if 'loop' in gate:
            require(str(gate['loop']).lower() == loop_id, 'gate loop mismatch ' + loop_id)
        source_bindings = gate.get('bindings')
        reviewer = gate.get('reviewer_path')
        require(isinstance(source_bindings, dict) and bool(source_bindings),
                'missing proof bindings ' + loop_id)
        require(nonempty(reviewer) and reviewer in source_bindings,
                'unbound skeptical review ' + loop_id)
        for name, expected in source_bindings.items():
            require(re.fullmatch(r'[0-9a-f]{64}', str(expected)),
                    'invalid source hash ' + str(name))
            require(sha256(bind(name)) == expected, 'changed gate input ' + name)
        reader_sources = row.get('evidence', [expected_gate, reviewer])
        require(isinstance(reader_sources, list) and reader_sources and
                all(name == expected_gate or name in source_bindings for name in reader_sources),
                'unbound reader evidence ' + loop_id)
        loops.append({
            'id': loop_id, 'sequence': sequence, 'title': gate['title'],
            'stage': 'reviewed', 'accepted': gate['accepted'], 'verdict': gate['verdict'],
            'summary': row['summary'], 'limitations': limitations, 'model': row['model'],
            'contribution_id': row['contribution_id'], 'derivation_steps': steps,
            'applications': applications, 'gate_path': expected_gate,
            'gate_sha256': bindings[expected_gate], 'reviewer_path': reviewer,
            'sources': list(dict.fromkeys(reader_sources)),
            'all_sources': [expected_gate] + sorted(source_bindings),
        })
    require(len({row['contribution_id'] for row in loops}) == 3,
            'duplicate contribution identifiers')

    registry_path = 'papers/draft-03/registry/hnm-registry.json'
    registry = read(registry_path)
    contributions = registry.get('contributions')
    require(registry.get('human_author') == AUTHOR and isinstance(contributions, list)
            and bool(contributions), 'invalid inherited HNM registry')
    old_ids = {row['id'] for row in contributions}
    require(len(old_ids) == len(contributions), 'duplicate inherited contribution')
    additions = []
    for loop in loops:
        require(loop['contribution_id'] not in old_ids, 'new alias replaces inherited contribution')
        additions.append({
            'id': loop['contribution_id'], 'legacy_id': loop['id'].upper(),
            'display_name': loop['title'], 'title': loop['title'], 'round': 31,
            'source_rounds': [31], 'status': loop['verdict'], 'summary': loop['summary'],
            'application': ' '.join(loop['applications']), 'limitation': '; '.join(loop['limitations']),
            'source_paths': loop['sources'], 'route': 'round31-' + loop['id'],
            'model': loop['model'], 'priority_status': 'Scientific priority unverified; project record alias.',
        })
    registry = {**registry, 'contributions': contributions + additions,
                'contribution_count': len(contributions) + 3,
                'presentation_extension': 'Round31 additive aliases; inherited records unchanged'}

    roadmap = read(ROUND + '/advisor/roadmap.json')
    goals = roadmap.get('goals', roadmap.get('next_goals'))
    require(isinstance(goals, list) and bool(goals) and
            all(isinstance(row, dict) and nonempty(row.get('id')) and
                nonempty(row.get('title', row.get('target'))) for row in goals),
            'post-cycle roadmap missing or invalid')
    network = read(ROUND + '/network.json')
    nodes, edges = network.get('nodes'), network.get('edges')
    require(isinstance(nodes, list) and nodes and isinstance(edges, list),
            'invalid network lists')
    require(all(isinstance(row, dict) and nonempty(row.get('id')) and
                nonempty(row.get('title')) for row in nodes), 'invalid network node')
    node_ids = {row['id'] for row in nodes}
    require(len(node_ids) == len(nodes), 'duplicate network node')
    require(all(isinstance(row, dict) and row.get('from') in node_ids and
                row.get('to') in node_ids and row.get('type') in RELATIONS
                for row in edges), 'invalid network relation')
    for loop in loops:
        require(any(row.get('route') == 'round31-' + loop['id'] for row in nodes),
                'network omits reviewed loop ' + loop['id'])
    for node in nodes:
        for item in node.get('sources', []):
            name = item if isinstance(item, str) else item.get('path')
            if name and not name.startswith(('https://', 'http://')):
                bind(name)

    survey = []
    ledgers = sorted((root / ROUND / 'experts').glob('*/sources.json'))
    require(bool(ledgers), 'missing expert source ledgers')
    for path in ledgers:
        name = path.relative_to(root).as_posix()
        ledger = read(name)
        records = ledger.get('sources', ledger.get('records'))
        require(isinstance(records, list) and bool(records), 'empty source ledger ' + name)
        for record in records:
            require(isinstance(record, dict) and nonempty(record.get('id')) and
                    nonempty(record.get('title')), 'invalid source record ' + name)
            passages = record.get('passages', record.get('sections_read', record.get('section', [])))
            if isinstance(passages, str):
                passages = [passages]
            survey.append({**record, 'area': path.parent.name, 'ledger': name,
                           'date': record.get('date', record.get('version_date', '')),
                           'reading_depth': record.get('reading_depth', record.get('read_depth', '')),
                           'use': record.get('relevance', record.get('modern_use', record.get('use', ''))),
                           'limits': record.get('limits', record.get('unresolved', record.get('unresolved_verification', ''))),
                           'passages': passages or []})

    addendum = findings.get('addendum')
    require(isinstance(addendum, dict) and nonempty(addendum.get('title')),
            'missing Round31 addendum metadata')
    addendum_path = bind(addendum.get('path'))
    published_addendum = dict(addendum, sha256=sha256(addendum_path))
    if addendum.get('url'):
        require(not addendum['url'].startswith('dist/'), 'addendum URL must be relative to dist')
        rendered = bind('dist/' + addendum['url'])
        require(rendered.read_bytes() == addendum_path.read_bytes(), 'addendum download mismatch')
    calculator = None
    at5 = next(row for row in loops if row['id'] == 'at5')
    if at5['verdict'].startswith('accepted'):
        result_path = ROUND + '/forward/at5/output/results.json'
        calculator_path = ROUND + '/forward/at5/calculator.py'
        require(result_path in at5['all_sources'] and calculator_path in at5['all_sources'],
                'AT5 calculator and output must both be bound by the admitted gate')
        result = read(result_path)
        bind(calculator_path)
        require(result.get('actual_aq_enclosure') is True and result.get('target_met') is True
                and result.get('selected_coefficients_over_alpha') == ['0', '0', '0'],
                'AT5 recorded calculator result scope mismatch')
        for key in ('certified_datum', 'certified_absolute_error', 'interval_width'):
            require(nonempty(result.get(key)), 'missing AT5 exact output ' + key)
        require(isinstance(result.get('costs'), dict) and result['costs']
                and isinstance(result.get('parameters'), dict), 'missing AT5 error budget')
        require(result.get('loop') == 'AT5' and result.get('fixed_design') is True
                and result.get('free_reference_included') is True
                and result.get('resolved_interaction_shift') is False
                and result.get('inverse_response_evaluated') is False
                and result.get('continuum_claim') is False
                and result.get('uniform_wilson_claim') is False,
                'AT5 calculator interpretation mismatch')
        parameters = result['parameters']
        require(Fraction(parameters['tau']) == Fraction(1, 10**14)
                and Fraction(parameters['s']) == 1 and Fraction(parameters['L']) == 10**9,
                'AT5 recorded preset changed')
        datum, radius = Fraction(result['certified_datum']), Fraction(result['certified_absolute_error'])
        require(0 < radius <= Fraction(1, 10**6)
                and Fraction(result['interval_width']) == 2 * radius
                and Fraction(result['actual_C_interval']['lower']) == datum - radius
                and Fraction(result['actual_C_interval']['upper']) == datum + radius
                and sum(Fraction(value) for value in result['costs'].values()) == radius,
                'AT5 recorded radius, width, or error budget mismatch')
        calculator = {
            'loop_id': 'at5', 'gate_path': at5['gate_path'], 'gate_sha256': at5['gate_sha256'],
            'source': calculator_path, 'result_path': result_path, 'record': result,
            'formula_id': 'zero-selected-reference-comparison-gap-six',
            'preview_only': True,
        }
    draft_path = 'papers/draft-03/main.pdf'
    draft = bind(draft_path)
    require(draft.read_bytes().startswith(b'%PDF-'), 'invalid preserved Draft03 PDF')
    require(bind('dist/ym-draft-03.pdf').read_bytes() == draft.read_bytes(),
            'preserved Draft03 download mismatch')
    return {
        'schema': 'hnm-round31-presentation-v1', 'author': AUTHOR,
        'summary': findings.get('summary', 'Three reviewed investigations, each with an explicit model and limitations.'),
        'scope_statement': findings.get('scope_statement',
            'Read each model restriction before applying a bound. Fixed-lattice results for a patterned subfamily do not establish the four-dimensional continuum Yang–Mills existence and mass-gap problem, which remains open.'),
        'progress': {'requested': 3, 'completed': 3, 'cycle_complete': True},
        'loops': loops, 'roadmap': {**roadmap, 'goals': goals},
        'network': network, 'survey': survey, 'addendum': published_addendum,
        'registry': registry, 'registry_source': registry_path,
        'calculator': calculator,
        'previous_draft': {'path': draft_path, 'url': 'ym-draft-03.pdf',
                           'title': 'Preserved Draft03 · through Round30', 'sha256': sha256(draft)},
        'input_bindings': dict(sorted(bindings.items())),
    }


def bundle(data):
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    encoded = encoded.replace('</', r'<\/').replace('\u2028', r'\u2028').replace('\u2029', r'\u2029')
    return ('/* Generated from three complete Round31 source-bound reviews. */\n'
            'window.ROUND31_DATA = ' + encoded + ';\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--require-complete', action='store_true',
                        help='Completeness is always required.')
    args = parser.parse_args()
    data = build(args.root)
    output = args.root / 'dist/research-round31-data.js'
    encoded = bundle(data)
    if args.check:
        require(output.is_file() and output.read_text(encoding='utf-8') == encoded,
                'Round31 bundle differs from its sources')
    else:
        require(output.parent.is_dir() and not output.is_symlink(), 'unsafe bundle output')
        output.write_text(encoded, encoding='utf-8')
    print(json.dumps({'status': 'passed', 'completed': 3,
                      'sources': len(data['survey']), 'network_nodes': len(data['network']['nodes'])}))


if __name__ == '__main__':
    main()
