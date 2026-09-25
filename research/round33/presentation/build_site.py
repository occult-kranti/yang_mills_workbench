"""Build the Round33 reader only from source-bound reviewed records.

Round33 is a four-sub-round, eight-investigation cycle: three research
sub-rounds (BA1/BA2, BB1/BB2, BC1/BC2) and an applications stage (BD1/BD2).
This is a presentation admission check, not a substitute for scientific
review. --check validates all inputs and compares the generated bundle without
writing. --allow-incomplete permits building with fewer than eight reviewed
investigations while the cycle is still in progress; with zero reviewed
investigations it writes the placeholder bundle (bound to advisor/findings.json
only), and the renderer shows nothing scientific unless the bundle is exactly
complete. While the cycle is incomplete the research network and the roadmap
(written at integration) may be absent. --allow-missing-addendum permits
building before the Round33 addendum PDF exists (it may be produced after the
research record).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
ROUND = 'research/round33'
AUTHOR = 'Hruday N M (BUNZEEY)'
LOOP_IDS = ('ba1', 'ba2', 'bb1', 'bb2', 'bc1', 'bc2', 'bd1', 'bd2')
REQUESTED = 8
SUBROUND_COUNT = 4
DELIBERATION_LOOP_COUNTS = (2, 3)
SCHEMA = 'hnm-round33-presentation-v1'
ADDENDUM_TITLE = 'Round33 research addendum'
RELATIONS = {'proven-dependency', 'proposed-transfer', 'review-selection',
             'source-dependency', 'scope-boundary', 'recorded-equation'}
VERDICT = r'(accepted|limited|insufficient|rejected|failed)(?:[_ -][a-zA-Z0-9 _-]+)?'
DIRECTIONS = {
    'paired': ['forward', 'reverse'],
    'single+skeptic': ['forward'],
    'statement+skeptic': ['forward'],
    'statement-only': ['forward'],
}
APPLICATION_KINDS = ('transfer', 'obstruction', 'partial')
INHERITED_ALIAS_ROUNDS = ((31, 'research/round31/advisor/findings.json'),
                          (32, 'research/round32/advisor/findings.json'))
PRESERVED_PDFS = (
    ('previous_draft', 'papers/draft-03/main.pdf', 'ym-draft-03.pdf', 'Preserved Draft03 · through Round30'),
    ('round31_addendum', 'papers/round31-addendum/main.pdf', 'ym-round31-addendum.pdf', 'Preserved Round31 addendum'),
    ('round32_addendum', 'papers/round32-addendum/main.pdf', 'ym-round32-addendum.pdf', 'Preserved Round32 addendum'),
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_name(name):
    return (isinstance(name, str) and bool(name) and not Path(name).is_absolute() and
            not re.search(r'[\\:#?<>\"\'\x00-\x20\x7f%]', name) and
            all(part not in ('', '.', '..') for part in name.split('/')))


def local(root, name):
    require(isinstance(name, str) and bool(name), 'missing relative source path')
    require(safe_name(name), 'unsafe source path ' + name)
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


def build(root=ROOT, allow_incomplete=False, allow_missing_addendum=False):
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

    def read_list(name):
        data = json.loads(bind(name).read_text(encoding='utf-8'))
        require(isinstance(data, list), 'expected JSON list ' + name)
        return data

    def exists(name):
        return (root / name).is_file()

    findings = read(ROUND + '/advisor/findings.json')
    require(findings.get('human_author') == AUTHOR, 'invalid findings author')
    require(findings.get('requested') == REQUESTED, 'findings does not request eight investigations')
    completed = findings.get('completed')
    require(type(completed) is int and 0 <= completed <= REQUESTED, 'invalid completed count')
    require(completed == REQUESTED or allow_incomplete,
            'exactly eight completed investigations required (pass --allow-incomplete during the cycle)')
    rows = findings.get('loops')
    require(isinstance(rows, list) and len(rows) == completed,
            'findings loop count does not match completed')
    if 'subrounds' in findings:
        require(isinstance(findings['subrounds'], list), 'invalid findings subrounds summary')
    cycle_complete = completed == REQUESTED

    def addendum_record(placeholder=False):
        addendum = findings.get('addendum')
        if placeholder and addendum is None:
            addendum = {'title': ADDENDUM_TITLE}
        require(isinstance(addendum, dict) and nonempty(addendum.get('title')),
                'missing Round33 addendum metadata')
        path_value = addendum.get('path')
        if nonempty(path_value) and not exists(path_value):
            # The findings record may already name the future PDF; before it is
            # built the addendum is published as unavailable, never bound.
            require(safe_name(path_value), 'unsafe addendum path ' + path_value)
            require(allow_missing_addendum,
                    'Round33 addendum PDF is not yet built; pass --allow-missing-addendum')
            path_value = None
        if nonempty(path_value):
            addendum_file = bind(path_value)
            require(addendum_file.read_bytes().startswith(b'%PDF-'), 'invalid Round33 addendum PDF')
            if addendum.get('url'):
                require(safe_name(addendum['url']) and not addendum['url'].startswith('dist/'),
                        'addendum URL must be a safe path relative to dist')
                rendered = bind('dist/' + addendum['url'])
                require(rendered.read_bytes() == addendum_file.read_bytes(), 'addendum download mismatch')
            return dict(addendum, sha256=sha256(addendum_file), available=True)
        require(allow_missing_addendum,
                'Round33 addendum PDF is not yet built; pass --allow-missing-addendum')
        return {'title': addendum['title'], 'path': None, 'url': None, 'sha256': None, 'available': False}

    if completed == 0:
        # In-progress placeholder: nothing reviewed exists, so nothing
        # scientific is bound or displayed. The renderer's incomplete()
        # view is shown on every Round33-owned route.
        published_addendum = addendum_record(placeholder=True)
        return {
            'schema': SCHEMA, 'author': AUTHOR, 'placeholder': True,
            'summary': findings.get('summary', 'Round33 in progress.'),
            'scope_statement': findings.get('scope_statement',
                'No Round33 scientific findings are displayed until eight source-bound reviews exist.'),
            'progress': {'requested': REQUESTED, 'completed': 0, 'cycle_complete': False,
                         'subrounds_completed': 0},
            'subrounds': [], 'loops': [], 'applications': [],
            'roadmap': {'goals': []}, 'network': {'nodes': [], 'edges': []}, 'survey': [],
            'panel': {'deliberation': [], 'updates': []}, 'calculators': [], 'figures': [],
            'addendum': published_addendum, 'registry': {'contributions': []},
            'input_bindings': dict(sorted(bindings.items())),
        }

    loops = []
    for sequence, (loop_id, row) in enumerate(zip(LOOP_IDS[:completed], rows), 1):
        subround_expected = (sequence + 1) // 2
        require(isinstance(row, dict) and row.get('id') == loop_id and
                type(row.get('sequence')) is int and row['sequence'] == sequence and
                row.get('subround') == subround_expected,
                'findings order/identifier mismatch ' + loop_id)
        expected_gate = ROUND + '/advisor/' + loop_id + '-gate.json'
        require(row.get('gate_path') == expected_gate, 'gate path mismatch ' + loop_id)
        gate = read(expected_gate)
        require(re.fullmatch(VERDICT, str(gate.get('verdict', ''))),
                'nonfinal verdict ' + loop_id)
        require(gate.get('sequence') == sequence and gate.get('subround') == subround_expected,
                'gate sequence/subround mismatch ' + loop_id)
        if 'loop' in gate:
            require(str(gate['loop']).lower() == loop_id, 'gate loop mismatch ' + loop_id)
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
        producers = row.get('producers')
        require(producers in (['forward', 'reverse'], ['forward']), 'invalid producers ' + loop_id)
        require(gate.get('producers') == producers, 'findings/gate producers mismatch ' + loop_id)
        direction = row.get('direction')
        require(direction in DIRECTIONS and DIRECTIONS[direction] == producers,
                'invalid direction ' + loop_id)
        contract = read(ROUND + '/contracts/' + loop_id + '.json')
        require(contract.get('direction') == direction, 'findings/contract direction mismatch ' + loop_id)
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
            'id': loop_id, 'sequence': sequence, 'subround': subround_expected,
            'title': gate['title'], 'stage': 'reviewed', 'accepted': gate['accepted'],
            'verdict': gate['verdict'], 'summary': row['summary'], 'limitations': limitations,
            'model': row['model'], 'contribution_id': row['contribution_id'],
            'derivation_steps': steps, 'applications': applications,
            'producers': producers, 'direction': direction,
            'gate_path': expected_gate, 'gate_sha256': bindings[expected_gate],
            'reviewer_path': reviewer, 'sources': list(dict.fromkeys(reader_sources)),
            'all_sources': [expected_gate] + sorted(source_bindings),
        })
    require(len({row['contribution_id'] for row in loops}) == completed,
            'duplicate contribution identifiers')
    loops_by_id = {row['id']: row for row in loops}
    subrounds_completed = completed // 2

    # Applications stage: transfers of admitted equations to named related
    # problems, and recorded obstructions where an equation does not transfer.
    applications = []
    raw_applications = findings.get('applications', [])
    require(isinstance(raw_applications, list), 'invalid findings applications list')
    for entry in raw_applications:
        require(isinstance(entry, dict), 'invalid application entry')
        loop_id = str(entry.get('loop_id', '')).lower()
        require(loop_id in loops_by_id, 'application references unreviewed loop ' + loop_id)
        for key in ('problem', 'equation', 'outcome', 'model'):
            require(nonempty(entry.get(key)), 'missing application ' + key + ' ' + loop_id)
        kind = entry.get('kind')
        require(kind is None or kind in APPLICATION_KINDS, 'invalid application kind ' + loop_id)
        detail = entry.get('detail', '')
        require(isinstance(detail, str), 'invalid application detail ' + loop_id)
        app_sources = entry.get('sources', [])
        require(isinstance(app_sources, list) and
                all(nonempty(name) and name in loops_by_id[loop_id]['all_sources'] for name in app_sources),
                'application source unbound ' + loop_id)
        applications.append({
            'loop_id': loop_id, 'problem': entry['problem'], 'equation': entry['equation'],
            'outcome': entry['outcome'], 'model': entry['model'], 'kind': kind, 'detail': detail,
            'sources': app_sources, 'gate_path': loops_by_id[loop_id]['gate_path'],
            'gate_sha256': loops_by_id[loop_id]['gate_sha256'], 'route': 'round33-' + loop_id,
        })

    registry_path = 'papers/draft-03/registry/hnm-registry.json'
    registry = read(registry_path)
    contributions = registry.get('contributions')
    require(registry.get('human_author') == AUTHOR and isinstance(contributions, list)
            and bool(contributions), 'invalid inherited HNM registry')
    old_ids = {row['id'] for row in contributions}
    require(len(old_ids) == len(contributions), 'duplicate inherited contribution')
    inherited_aliases = []
    for round_number, findings_path in INHERITED_ALIAS_ROUNDS:
        # Earlier cycles' aliases are presentation records rebuilt from their
        # own gated findings; their evidence is validated by their own rounds.
        earlier = read(findings_path)
        for row in earlier.get('loops', []):
            gate = read(row['gate_path'])
            require(gate.get('accepted') == row.get('accepted'),
                    'inherited finding differs from its gate ' + str(row.get('id')))
            evidence = row.get('evidence') or [row['gate_path']]
            for name in evidence:
                bind(name)
            inherited_aliases.append({
                'id': row['contribution_id'], 'legacy_id': row['id'].upper(),
                'display_name': row['title'], 'title': row['title'], 'round': round_number,
                'source_rounds': [round_number], 'status': gate['verdict'], 'summary': row['summary'],
                'application': ' '.join(row.get('applications', [])),
                'limitation': '; '.join(row.get('limitations', [])),
                'source_paths': evidence, 'route': 'round%d-%s' % (round_number, row['id'].lower()),
                'model': row.get('model', ''),
                'priority_status': 'Scientific priority unverified; project record alias.',
            })
    additions = []
    for loop in loops:
        additions.append({
            'id': loop['contribution_id'], 'legacy_id': loop['id'].upper(),
            'display_name': loop['title'], 'title': loop['title'], 'round': 33,
            'source_rounds': [33], 'status': loop['verdict'], 'summary': loop['summary'],
            'application': ' '.join(loop['applications']), 'limitation': '; '.join(loop['limitations']),
            'source_paths': loop['sources'], 'route': 'round33-' + loop['id'],
            'model': loop['model'], 'priority_status': 'Scientific priority unverified; project record alias.',
        })
    new_ids = [row['id'] for row in inherited_aliases + additions]
    require(len(set(new_ids)) == len(new_ids) and not (set(new_ids) & old_ids),
            'new alias replaces inherited contribution')
    registry = {**registry, 'contributions': contributions + inherited_aliases + additions,
                'contribution_count': len(contributions) + len(inherited_aliases) + len(additions),
                'presentation_extension': 'Round31, Round32 and Round33 additive aliases; inherited records unchanged'}

    roadmap_path = ROUND + '/advisor/roadmap.json'
    if cycle_complete or exists(roadmap_path):
        roadmap = read(roadmap_path)
        goals = roadmap.get('goals', roadmap.get('next_goals'))
        require(isinstance(goals, list) and bool(goals) and
                all(isinstance(row, dict) and nonempty(row.get('id')) and
                    nonempty(row.get('title', row.get('target'))) for row in goals),
                'post-cycle roadmap missing or invalid')
    else:
        roadmap, goals = {}, []

    network_path = ROUND + '/network.json'
    if cycle_complete or exists(network_path):
        network = read(network_path)
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
            require(any(row.get('route') == 'round33-' + loop['id'] for row in nodes),
                    'network omits reviewed loop ' + loop['id'])
        for node in nodes:
            for item in node.get('sources', []):
                name = item if isinstance(item, str) else item.get('path')
                if name and not name.startswith(('https://', 'http://')):
                    bind(name)
    else:
        network = {'nodes': [], 'edges': []}

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

    panel_raw = read(ROUND + '/advisor/panel.json')
    deliberation_raw = panel_raw.get('deliberation')
    require(isinstance(deliberation_raw, list) and bool(deliberation_raw),
            'missing panel deliberation loops')
    deliberation, seen_deliberation = [], set()
    for entry in deliberation_raw:
        require(isinstance(entry, dict), 'invalid deliberation entry')
        number = entry.get('loop')
        require(type(number) is int and 1 <= number <= max(DELIBERATION_LOOP_COUNTS)
                and number not in seen_deliberation, 'invalid deliberation loop number')
        seen_deliberation.add(number)
        path = entry.get('path')
        require(nonempty(path), 'missing deliberation path')
        bind(path)
        require(nonempty(entry.get('summary')), 'missing deliberation summary')
        deliberation.append({'loop': number, 'path': path, 'summary': entry['summary']})
    require(len(seen_deliberation) in DELIBERATION_LOOP_COUNTS and
            seen_deliberation == set(range(1, len(seen_deliberation) + 1)),
            'incomplete panel deliberation loops')
    deliberation.sort(key=lambda row: row['loop'])

    updates_raw = panel_raw.get('updates', [])
    require(isinstance(updates_raw, list), 'invalid panel updates')
    updates = []
    for entry in updates_raw:
        require(isinstance(entry, dict), 'invalid panel update entry')
        subround_number = entry.get('subround')
        require(type(subround_number) is int and 1 <= subround_number <= SUBROUND_COUNT,
                'invalid panel update subround')
        path = entry.get('path')
        require(nonempty(path), 'missing panel update path')
        bind(path)
        lenses = entry.get('lenses', [entry['lens']] if nonempty(entry.get('lens')) else [])
        require(isinstance(lenses, list) and lenses and all(nonempty(x) for x in lenses),
                'missing panel update lens')
        assistants = entry.get('assistants', [])
        require(isinstance(assistants, list) and all(nonempty(x) for x in assistants),
                'invalid panel update assistants')
        for name in [*lenses, *assistants]:
            bind(name)
        updates.append({'subround': subround_number, 'lens': ', '.join(Path(x).parent.name if Path(x).name.startswith('update') else Path(x).parent.parent.name for x in lenses),
                        'lenses': lenses, 'assistants': assistants, 'path': path,
                        'goal_changes': entry.get('goal_changes', '')})

    plan = read(ROUND + '/advisor/plan.json')
    plan_subrounds = plan.get('subrounds')
    require(isinstance(plan_subrounds, list) and len(plan_subrounds) == SUBROUND_COUNT,
            'plan must define four subrounds')
    subrounds, seen_subrounds = [], set()
    for entry in plan_subrounds:
        require(isinstance(entry, dict), 'invalid subround entry')
        sid = entry.get('id')
        require(type(sid) is int and 1 <= sid <= SUBROUND_COUNT and sid not in seen_subrounds,
                'invalid subround id')
        seen_subrounds.add(sid)
        require(nonempty(entry.get('title')), 'missing subround title ' + str(sid))
        require(nonempty(entry.get('goal_id')), 'missing subround goal id ' + str(sid))
        expected_loops = list(LOOP_IDS[(sid - 1) * 2: sid * 2])
        entry_loops = entry.get('loops')
        require(isinstance(entry_loops, list) and
                [str(item).lower() for item in entry_loops] == expected_loops,
                'subround loop mismatch ' + str(sid))
        selection_note_path = entry.get('selection_note_path')
        panel_update_path = entry.get('panel_update_path')
        if sid <= subrounds_completed:
            require(nonempty(selection_note_path), 'missing selection note for completed subround ' + str(sid))
            require(nonempty(panel_update_path), 'missing panel update for completed subround ' + str(sid))
            bind(selection_note_path)
            bind(panel_update_path)
        else:
            selection_note_path = selection_note_path if nonempty(selection_note_path) else None
            panel_update_path = panel_update_path if nonempty(panel_update_path) else None
            if selection_note_path:
                bind(selection_note_path)
            if panel_update_path:
                bind(panel_update_path)
        subrounds.append({'id': sid, 'title': entry['title'], 'goal_id': entry['goal_id'],
                          'loops': expected_loops, 'selection_note_path': selection_note_path,
                          'panel_update_path': panel_update_path})
    require(seen_subrounds == set(range(1, SUBROUND_COUNT + 1)), 'plan missing a subround id')
    subrounds.sort(key=lambda row: row['id'])

    calculators = []
    calculators_path = ROUND + '/advisor/calculators.json'
    if exists(calculators_path):
        for entry in read_list(calculators_path):
            require(isinstance(entry, dict), 'invalid calculator entry')
            loop_id = str(entry.get('loop_id', '')).lower()
            require(loop_id in loops_by_id, 'calculator references unknown loop ' + loop_id)
            loop = loops_by_id[loop_id]
            require(nonempty(entry.get('title')), 'missing calculator title ' + loop_id)
            require(nonempty(entry.get('formula_id')), 'missing calculator formula id ' + loop_id)
            source, result_path = entry.get('source'), entry.get('result_path')
            require(nonempty(source) and source in loop['all_sources'],
                    'calculator source unbound ' + loop_id)
            require(nonempty(result_path) and result_path in loop['all_sources'],
                    'calculator result unbound ' + loop_id)
            bind(source)
            record = read(result_path)
            record_keys = entry.get('record_keys')
            if record_keys is not None:
                require(isinstance(record_keys, list) and record_keys and
                        all(nonempty(k) and k in record for k in record_keys),
                        'calculator record_keys must name existing top-level fields ' + loop_id)
                record = {k: record[k] for k in record_keys}
            require(bool(record), 'empty calculator record ' + loop_id)
            calculators.append({
                'loop_id': loop_id, 'title': entry['title'], 'gate_path': loop['gate_path'],
                'gate_sha256': loop['gate_sha256'], 'source': source, 'result_path': result_path,
                'formula_id': entry['formula_id'], 'record': record, 'preview_only': True,
            })

    figures = []
    figures_path = ROUND + '/advisor/figures.json'
    if exists(figures_path):
        for entry in read_list(figures_path):
            require(isinstance(entry, dict), 'invalid figure entry')
            fig_path = entry.get('path')
            require(nonempty(fig_path) and safe_name(fig_path), 'unsafe figure path ' + str(fig_path))
            dist_file = root / 'dist' / fig_path
            require(dist_file.is_file() and not dist_file.is_symlink(),
                    'missing dist figure ' + fig_path)
            require(nonempty(entry.get('title')) and nonempty(entry.get('caption')),
                    'missing figure text ' + fig_path)
            source_path = entry.get('source_path')
            if nonempty(source_path):
                bind(source_path)
            else:
                source_path = None
            figures.append({'path': fig_path, 'title': entry['title'], 'caption': entry['caption'],
                            'source_path': source_path})

    published_addendum = addendum_record()

    def preserved_pdf(path_str, dist_url, title):
        pdf = bind(path_str)
        require(pdf.read_bytes().startswith(b'%PDF-'), 'invalid preserved PDF ' + path_str)
        rendered = bind('dist/' + dist_url)
        require(rendered.read_bytes() == pdf.read_bytes(), 'preserved download mismatch ' + path_str)
        return {'path': path_str, 'url': dist_url, 'title': title, 'sha256': sha256(pdf)}

    preserved = {key: preserved_pdf(path_str, url, title) for key, path_str, url, title in PRESERVED_PDFS}

    return {
        'schema': SCHEMA, 'author': AUTHOR,
        'summary': findings.get('summary',
            'Eight reviewed investigations across four sub-rounds, each with an explicit model and limitations.'),
        'scope_statement': findings.get('scope_statement',
            'Read each model restriction before applying a bound. Fixed-lattice results do not establish the four-dimensional continuum Yang–Mills existence and mass-gap problem, which remains open.'),
        'progress': {'requested': REQUESTED, 'completed': completed,
                     'cycle_complete': cycle_complete,
                     'subrounds_completed': subrounds_completed},
        'subrounds': subrounds, 'loops': loops, 'applications': applications,
        'roadmap': {**roadmap, 'goals': goals}, 'network': network, 'survey': survey,
        'panel': {'deliberation': deliberation, 'updates': updates},
        'calculators': calculators, 'figures': figures,
        'addendum': published_addendum, 'registry': registry, 'registry_source': registry_path,
        'inherited_alias_sources': [path for _, path in INHERITED_ALIAS_ROUNDS],
        **preserved,
        'input_bindings': dict(sorted(bindings.items())),
    }


def bundle(data):
    completed = data['progress']['completed']
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    encoded = encoded.replace('</', '<\\/').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    if data.get('placeholder'):
        header = ('/* Placeholder generated from research/round33/advisor/findings.json (0 of '
                  f'{REQUESTED} reviewed Round33 investigations); the renderer displays no scientific findings. */\n')
    else:
        header = f'/* Generated from {completed} of {REQUESTED} source-bound reviewed Round33 investigations. */\n'
    return header + 'window.ROUND33_DATA = ' + encoded + ';\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--allow-incomplete', action='store_true',
                        help='Allow fewer than eight reviewed investigations while the cycle is in progress.')
    parser.add_argument('--allow-missing-addendum', action='store_true',
                        help='Allow building before the Round33 addendum PDF exists.')
    args = parser.parse_args()
    data = build(args.root, allow_incomplete=args.allow_incomplete,
                 allow_missing_addendum=args.allow_missing_addendum)
    output = args.root / 'dist/research-round33-data.js'
    encoded = bundle(data)
    if args.check:
        require(output.is_file() and output.read_text(encoding='utf-8') == encoded,
                'Round33 bundle differs from its sources')
    else:
        require(output.parent.is_dir() and not output.is_symlink(), 'unsafe bundle output')
        output.write_text(encoded, encoding='utf-8')
    print(json.dumps({'status': 'passed', 'completed': data['progress']['completed'],
                      'cycle_complete': data['progress']['cycle_complete'],
                      'placeholder': bool(data.get('placeholder')),
                      'sources': len(data['survey']), 'network_nodes': len(data['network']['nodes'])}))


if __name__ == '__main__':
    main()
