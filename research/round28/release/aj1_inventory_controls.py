"""Portable prescience inventory-format controls; no scientific producer runs."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reproduce import PREFIX, Validator, digest, require

BASE = PREFIX + 'forward/aj1/'
SOURCE = BASE + 'inputs/source-inventory.json'
INSTRUCTIONS = BASE + 'inputs/instruction-inventory.json'
CONTRACT = PREFIX + 'contracts/aj1.json'


def put(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + '\n' if isinstance(value, (dict, list)) else value)


def fixture(root):
    repository = ['AGENTS.md', PREFIX + 'methods/prospective-guide.md',
                  'research/round27/methods/historical-physics-panel/SKILL.md',
                  'research/round27/methods/historical-physics-panel/references/lenses-and-evidence.md']
    repository += ['.codex/skills/synthetic/references/instruction-' + str(i) + '.md' for i in range(7)]
    for name in repository + [PREFIX + 'advisor/cycle.json', 'synthetic-data.txt']:
        put(root, name, 'Synthetic local input: ' + name + '\n')
    sources = {name: digest(root / name) for name in repository + [PREFIX + 'advisor/cycle.json', 'synthetic-data.txt']}
    put(root, CONTRACT, {'schema': 'ym28-contract-v1', 'loop': 'aj1', 'model': 'synthetic only',
        'frozen_at': 'synthetic-prescience', 'acceptance': 'No physics claim', 'goal': 'AJ',
        'requirements': ['complete source snapshots'], 'parameters': {'fixture': True}, 'sources': sources})
    sources[CONTRACT] = digest(root / CONTRACT)
    snapshots = {BASE + 'inputs/' + name: value for name, value in sources.items()}
    for name in sources:
        put(root, BASE + 'inputs/' + name, (root / name).read_text())
    resources = []
    for i in range(6):
        path = BASE + 'inputs/installed-methods/synthetic-' + str(i) + '.md'
        put(root, path, 'Synthetic installed instruction ' + str(i) + '\n')
        resources.append({'path': path, 'sha256': digest(root / path),
                          'resource': 'skill://flora-skills/root/.codex/skills/remote-skills/skill-' + '1' * 32 + '/references/synthetic-' + str(i) + '.md'})
    put(root, SOURCE, {'schema': 'ym28-aj1-forward-source-inventory-v1', 'contract': CONTRACT,
        'contract_sha256': sources[CONTRACT], 'sources': sources, 'snapshots': snapshots, 'instructions': INSTRUCTIONS})
    put(root, INSTRUCTIONS, {'schema': 'ym28-aj1-forward-instructions-v1',
        'repository_instructions': {BASE + 'inputs/' + name: sources[name] for name in repository},
        'installed_resources': resources})


def run():
    rejected = []
    with tempfile.TemporaryDirectory(prefix='ym28-aj1-inventory-controls-') as directory:
        temporary = Path(directory)
        original = temporary / 'baseline'
        fixture(original)
        def validate(root):
            return Validator(root).manifests('aj1', 'forward', [SOURCE], [INSTRUCTIONS])
        _, snapshots, sources = validate(original)
        require(len(snapshots) == len(sources) + 6, 'repository instructions counted twice or installed snapshots lost')
        def edit(name, change):
            def action(root):
                value = json.loads((root / name).read_text())
                change(value)
                put(root, name, value)
            return action
        def attack(label, change):
            root = temporary / label
            shutil.copytree(original, root)
            change(root)
            try:
                validate(root)
            except ValueError:
                rejected.append(label)
            else:
                raise ValueError('invalid AJ1 input inventory admitted: ' + label)
        attack('different-source-snapshot-map', edit(SOURCE, lambda d: d['snapshots'].__setitem__(BASE + 'inputs/AGENTS.md', '0' * 64)))
        attack('missing-snapshot-map-entry', edit(SOURCE, lambda d: d['snapshots'].pop(BASE + 'inputs/AGENTS.md')))
        def remove_source(d, name):
            d['sources'].pop(name)
            d['snapshots'].pop(BASE + 'inputs/' + name)
        attack('omitted-contract-in-both-maps', edit(SOURCE, lambda d: remove_source(d, CONTRACT)))
        attack('omitted-contract-source-in-both-maps', edit(SOURCE, lambda d: remove_source(d, 'AGENTS.md')))
        attack('wrong-contract-identity', edit(SOURCE, lambda d: d.__setitem__('contract', PREFIX + 'contracts/ah2.json')))
        attack('wrong-contract-digest', edit(SOURCE, lambda d: d.__setitem__('contract_sha256', '0' * 64)))
        attack('undeclared-instruction-manifest', edit(SOURCE, lambda d: d.__setitem__('instructions', BASE + 'inputs/other.json')))
        attack('changed-original-source', lambda root: put(root, 'AGENTS.md', 'Changed original\n'))
        attack('changed-copied-source', lambda root: put(root, BASE + 'inputs/AGENTS.md', 'Changed copy\n'))
        attack('foreign-snapshot-map-path', edit(SOURCE, lambda d: d['snapshots'].__setitem__(PREFIX + 'reverse/aj1/inputs/AGENTS.md', d['snapshots'].pop(BASE + 'inputs/AGENTS.md'))))
        attack('missing-repository-instruction', edit(INSTRUCTIONS, lambda d: d['repository_instructions'].pop(BASE + 'inputs/AGENTS.md')))
        attack('wrong-repository-instruction-hash', edit(INSTRUCTIONS, lambda d: d['repository_instructions'].__setitem__(BASE + 'inputs/AGENTS.md', '0' * 64)))
        attack('missing-installed-instruction', edit(INSTRUCTIONS, lambda d: d['installed_resources'].pop()))
        attack('wrong-installed-instruction-hash', edit(INSTRUCTIONS, lambda d: d['installed_resources'][0].__setitem__('sha256', '0' * 64)))
        attack('foreign-installed-owned-path', edit(INSTRUCTIONS, lambda d: d['installed_resources'][0].__setitem__('path', PREFIX + 'reverse/aj1/inputs/instruction.md')))
        attack('duplicate-installed-snapshot', edit(INSTRUCTIONS, lambda d: d['installed_resources'][1].__setitem__('path', d['installed_resources'][0]['path'])))
        attack('duplicate-installed-origin', edit(INSTRUCTIONS, lambda d: d['installed_resources'][1].__setitem__('resource', d['installed_resources'][0]['resource'])))
        valid = json.loads((original / INSTRUCTIONS).read_text())['installed_resources'][0]['resource']
        for label, locator in [
            ('wrong-origin-host', valid.replace('flora-skills', 'unreviewed-host')),
            ('escaping-origin-reference', valid.replace('references/', 'references/../')),
            ('origin-query', valid + '?runtime=true'),
            ('origin-percent-escape', valid.replace('references/', 'references/%2e%2e/')),
            ('absolute-origin-in-typed-skill-field', '/outside/runtime/SKILL.md'),
            ('relative-origin-in-typed-skill-field', 'references/SKILL.md'),
            ('network-origin', 'https://example.org/SKILL.md')]:
            attack(label, edit(INSTRUCTIONS, lambda d, locator=locator: d['installed_resources'][0].__setitem__('resource', locator)))
        attack('untyped-skill-origin', edit(INSTRUCTIONS, lambda d: d.update(schema='unknown-instruction-format')))
        # Other historical external-instruction formats still require absolute
        # provenance. They cannot gain URI admission through a caller-supplied tag.
        legacy = BASE + 'inputs/legacy-instruction-inventory.json'
        snapshot = BASE + 'inputs/instructions/example.md'
        put(original, snapshot, 'Frozen external instruction\n')
        put(original, legacy, {'example.md': {'origin': '/external/original/SKILL.md', 'sha256': digest(original / snapshot)}})
        Validator(original).manifests('aj1', 'forward', [SOURCE], [INSTRUCTIONS, legacy])
        put(original, legacy, {'example.md': {'origin': valid, 'sha256': digest(original / snapshot)}})
        try:
            Validator(original).manifests('aj1', 'forward', [SOURCE], [INSTRUCTIONS, legacy])
        except ValueError:
            rejected.append('legacy-external-origin-uri-not-admitted')
        else:
            raise ValueError('untyped external URI admitted')
    return {'status': 'passed', 'inventory_mutations_rejected': len(rejected), 'controls': rejected,
            'new_research_loops': 0, 'scope': 'Synthetic prescience inventory and local provenance validation only.'}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
