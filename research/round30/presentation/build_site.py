"""Build the additive Round30 website bundle from exactly three reviewed loops.

This presentation gate fails on an incomplete release. It verifies bound sources,
but does not replace the scientific skeptical validators or PDF review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
ROUND = 'research/round30'
AUTHOR = 'Hruday N M (BUNZEEY)'
RELATIONS = {'proven-dependency', 'proposed-transfer', 'review-selection',
             'source-dependency', 'scope-boundary', 'recorded-equation'}
READER_SUMMARIES = {
    'at1': 'The Wilson excitation has controlled physical energy in the actual numerical-cap state. The proof establishes its operator domain, an exact first-moment identity and an upper second-moment bound.',
    'at2': 'Exact one-sided bounds place a nonzero amount of Wilson spectral mass in a finite energy window and bound a reduced inverse-energy form. Equal-moment controls show why these data do not identify a particle pole.',
    'at3': 'A conditional finite-readout procedure bounds the inverse-energy form from 4,097 Euclidean samples with separate tail, quadrature, sample and arithmetic errors. Actual AQ samples remain unevaluated.',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name):
    require(isinstance(name, str) and name and not Path(name).is_absolute(),
            'invalid relative source')
    require(not re.search(r'[\\\x00-\x1f]', name) and
            all(part not in ('', '.', '..') for part in name.split('/')),
            'unsafe source ' + name)
    candidate = root
    for part in name.split('/'):
        candidate = candidate / part
        require(not candidate.is_symlink(), 'symlink source ' + name)
    require(candidate.is_file(), 'missing source ' + name)
    return candidate


def build(root=ROOT):
    root = Path(root).resolve()
    bindings = {}

    def read(name):
        path = local(root, name)
        bindings[name] = digest(path)
        return json.loads(path.read_text())

    findings = read(ROUND + '/advisor/findings.json')
    registry_path = 'papers/draft-03/registry/hnm-registry.json'
    registry = read(registry_path)
    roadmap = read(ROUND + '/advisor/roadmap.json')
    network = read(ROUND + '/network.json')
    require(findings.get('completed') == 3 and len(findings.get('loops', [])) == 3,
            'exactly three completed investigations required')
    require(registry.get('human_author') == AUTHOR, 'Draft03 author mismatch')
    contributions = registry.get('contributions', [])
    require(contributions, 'empty Draft03 registry')
    require(len({row['id'] for row in contributions}) == len(contributions),
            'duplicate contribution identifiers')
    names = {str(row.get('legacy_id', '')).lower(): row for row in contributions}
    for section in ('contributions', 'equations', 'statements', 'quantities'):
        rows = registry.get(section, [])
        require(len({row['id'] for row in rows}) == len(rows), 'duplicate ' + section)
        for row in rows:
            for name in row.get('source_paths', []):
                local(root, name)
    loops = []
    for sequence, row in enumerate(findings['loops'], 1):
        loop = str(row.get('id', '')).lower()
        require(re.fullmatch(r'[a-z][a-z0-9]*', loop), 'invalid loop identifier')
        gate_path = ROUND + '/advisor/' + loop + '-gate.json'
        gate = read(gate_path)
        require(str(gate.get('loop', '')).lower() == loop and
                gate.get('sequence') == sequence, 'gate sequence/identifier mismatch ' + loop)
        require(bool(gate.get('completed_at')), 'missing completed review ' + loop)
        require(re.fullmatch(r'(accepted|limited|insufficient|rejected|failed)(?:[_ -][a-zA-Z0-9 _-]+)?',
                             str(gate.get('verdict', ''))), 'nonfinal verdict ' + loop)
        require(isinstance(gate.get('accepted'), str) and gate['accepted'].strip(),
                'missing scoped conclusion ' + loop)
        require(isinstance(gate.get('limitations'), list) and gate['limitations'] and
                all(isinstance(x, str) and x.strip() for x in gate['limitations']),
                'missing limitations ' + loop)
        required = [ROUND + '/contracts/' + loop + '.json',
                    ROUND + '/forward/' + loop + '/report.md',
                    ROUND + '/reverse/' + loop + '/report.md',
                    ROUND + '/skeptic/' + loop + '.md']
        source_bindings = gate.get('bindings', {})
        require(all(name in source_bindings for name in required),
                'missing required gate binding ' + loop)
        for name, expected in source_bindings.items():
            require(re.fullmatch(r'[a-f0-9]{64}', str(expected)) and
                    digest(local(root, name)) == expected, 'changed gate input ' + name)
        require(loop in names, 'Draft03 registry omits ' + loop)
        alias = names[loop]
        contract = read(required[0])
        require(contract.get('sequence') == sequence, 'contract order mismatch ' + loop)
        if row.get('accepted') is not None:
            require(row['accepted'] == gate['accepted'], 'findings expands accepted scope ' + loop)
        if row.get('status') is not None:
            require(row['status'] == gate['verdict'], 'findings verdict mismatch ' + loop)
        equations = row.get('equations', [])
        require(isinstance(equations, list), 'invalid equations ' + loop)
        loops.append({
            'id': loop, 'sequence': sequence, 'title': alias.get('display_name', row.get('title', loop.upper())),
            'contribution_id': alias['id'], 'stage': 'reviewed', 'verdict': gate['verdict'],
            'accepted': gate['accepted'], 'limitations': gate['limitations'],
            'model': gate.get('model', contract.get('model', '')),
            'target': contract.get('target', ''), 'equations': equations,
            'summary': row.get('summary', READER_SUMMARIES.get(loop, '')), 'derivation_steps': row.get('derivation_steps', []),
            'applications': row.get('applications', []), 'sources': required + [gate_path],
            'gate_sha256': bindings[gate_path], 'gate_path': gate_path,
            'statement_ids': alias.get('statement_ids', []),
        })
    require(len({row['id'] for row in loops}) == 3, 'duplicate loop')
    nodes, edges = network.get('nodes', []), network.get('edges', [])
    ids = {row['id'] for row in nodes}
    require(nodes and len(ids) == len(nodes), 'empty network or duplicate node')
    require(all(row.get('from') in ids and row.get('to') in ids and
                row.get('type') in RELATIONS for row in edges), 'invalid network edge')
    require(all(any(node.get('route') == 'round30-' + row['id'] for node in nodes)
                for row in loops), 'network omits a reviewed loop')
    goals = roadmap.get('goals', roadmap.get('next_goals', []))
    require(goals, 'post-cycle roadmap missing')
    survey = []
    ledger_sources = [(area, ROUND + '/experts/' + area + '/sources.json')
                      for area in ('historical', 'modern')]
    ledger_sources.append(('modern', ROUND + '/editorial/method-source-addendum.json'))
    for area, name in ledger_sources:
        ledger = read(name)
        records = ledger.get('sources', ledger.get('records', []))
        require(records, 'empty source ledger ' + area)
        for row in records:
            survey.append({**row, 'area': area, 'ledger': name,
                           'title': row.get('title', row.get('id', 'Unnamed source')),
                           'date': row.get('date', row.get('version_date', '')),
                           'reading_depth': row.get('reading_depth', ''),
                           'use': row.get('modern_use', row.get('relevance', row.get('use', ''))),
                           'limits': row.get('unresolved', row.get('limits', '')),
                           'passages': row.get('passages', row.get('sections_read', []))})
    for name in ('papers/draft-03/main.pdf', 'papers/draft-02/main.pdf'):
        path = local(root, name)
        require(path.read_bytes().startswith(b'%PDF-'), 'invalid PDF ' + name)
        bindings[name] = digest(path)
    calculator_path = ROUND + '/calculators/spectral_certificate.py'
    bindings[calculator_path] = digest(local(root, calculator_path))
    captions = read(ROUND + '/figures/captions.json')
    at2 = next((row for row in loops if row['id'] == 'at2'), None)
    require(at2 and captions.get('gate_sha256') == at2['gate_sha256'],
            'spectral figure caption does not match AT2 review')
    figure_path = ROUND + '/figures/hnm-spectral-certificates.png'
    bindings[figure_path] = digest(local(root, figure_path))
    return {
        'schema': 'hnm-round30-presentation-v1', 'author': AUTHOR,
        'summary': findings.get('summary', 'Three reviewed investigations connect Wilson energy control, spectral bounds and a conditional sampling procedure in the same fixed-lattice state.'),
        'scope_statement': findings.get('scope_statement', 'These results concern a specified model at fixed lattice spacing. The four-dimensional continuum Yang–Mills existence and mass-gap problem remains open.'),
        'loops': loops, 'progress': {'requested': 3, 'completed': 3, 'cycle_complete': True},
        'obligations': findings.get('obligations', []),
        'registry': registry, 'registry_source': registry_path, 'network': network,
        'roadmap': {**roadmap, 'goals': goals}, 'survey': survey,
        'calculator': {'source': calculator_path, 'gate_path': at2['gate_path'],
                       'gate_sha256': at2['gate_sha256'], 'loop_id': 'at2'},
        'figure': {'url': 'hnm-spectral-certificates.png', 'source': figure_path,
                   'caption': captions['caption'], 'accuracy': captions.get('curve_accuracy', ''),
                   'gate_sha256': captions['gate_sha256']},
        'draft': {'url': 'ym-draft-03.pdf', 'path': 'papers/draft-03/main.pdf',
                  'sha256': bindings['papers/draft-03/main.pdf'], 'title': 'Complete Hruday / HNM draft · through Round30'},
        'previous_draft': {'url': 'ym-draft-02.pdf', 'path': 'papers/draft-02/main.pdf',
                           'sha256': bindings['papers/draft-02/main.pdf'], 'title': 'Draft02 · through Round29'},
        'input_bindings': dict(sorted(bindings.items())),
    }


def bundle(data):
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', r'<\/').replace('\u2028', r'\u2028').replace('\u2029', r'\u2029')
    return ('/* Generated from the complete, source-bound Round30 release. */\n'
            'window.ROUND30_DATA = ' + encoded + ';\n'
            'if (window.ROUND29_DATA) {\n'
            '  window.ROUND29_DATA.registry = window.ROUND30_DATA.registry;\n'
            '  window.ROUND29_DATA.registry_source = window.ROUND30_DATA.registry_source;\n'
            '  window.ROUND29_DATA.network = window.ROUND30_DATA.network;\n'
            '}\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--require-complete', action='store_true', help='Completeness is always required.')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    data = build(args.root)
    output = args.root / 'dist/research-round30-data.js'
    text = bundle(data)
    if args.check:
        require(output.is_file() and output.read_text() == text, 'Round30 bundle differs from its sources')
        registry_output = args.root / 'dist/hnm-registry-r30.json'
        require(registry_output.is_file() and registry_output.read_bytes() ==
                (args.root / data['registry_source']).read_bytes(), 'Round30 registry download mismatch')
    else:
        output.write_text(text)
        (args.root / 'dist/hnm-registry-r30.json').write_bytes(
            (args.root / data['registry_source']).read_bytes())
    print(json.dumps({'status': 'passed', 'completed': 3, 'sources': len(data['survey']),
                      'registry': len(data['registry']['contributions']),
                      'network_nodes': len(data['network']['nodes'])}))


if __name__ == '__main__':
    main()
