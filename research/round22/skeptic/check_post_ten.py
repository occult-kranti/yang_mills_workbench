#!/usr/bin/env python3
"""Read-only ten-loop map/dependency audit; does not execute research."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/round22'))
import admission


def require(value, message):
    if not value:
        raise RuntimeError(message)


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    map_path = 'research/round22/advisor/claim-dependency-map.json'
    metadata_path = 'research/round22/site-data.json'
    mapping = read(map_path)
    metadata = read(metadata_path)
    loops = list(admission.LOOPS)
    require(loops == ['n1', 'n2', 'o1', 'o2', 'p1', 'p2', 'q1', 'q2', 'r1', 'r2'], 'exact ten loop order')
    require(mapping['schema'] == 'ym22-claim-dependency-map-v1', 'map schema')
    require(type(mapping['completed_research_loops']) is int and mapping['completed_research_loops'] == 10, 'strict integer ten')
    require(mapping['index_generation_adds_research_loops'] == 0 and mapping['index_is_not_a_new_admission'] is True, 'index scope')
    require([row['loop'] for row in mapping['claims']] == loops, 'claim order')
    require(mapping['future_goals_record'] == 'research/round22/advisor/post-ten-roadmap.json', 'future roadmap path only')
    require('remain open' in mapping['continuum_status'], 'continuum status')
    files, gate_hashes, counts, statuses, dependency_edges = {}, {}, {}, {}, []
    for row in mapping['claims']:
        loop = row['loop']
        gate = admission.gate(loop)
        contract = read(f'research/round22/contracts/{loop}.json')
        for mapped, admitted in [('verdict', 'status'), ('target_verdict', 'target_verdict'),
                                  ('supported_statement', 'claim'), ('supported_equations', 'equations'),
                                  ('assumptions_and_scope', 'scope'), ('independence', 'independence'),
                                  ('next_missing_premise', 'next_missing_premise')]:
            require(row[mapped] == gate[admitted], f'{loop}: gate field {mapped}')
        require(row['limitations'] == gate.get('limits', []), f'{loop}: limits')
        for mapped, selected in [('original_question', 'target'), ('dependency_bindings', 'dependencies'),
                                 ('instruction_snapshots', 'instruction_inputs')]:
            require(row[mapped] == contract[selected], f'{loop}: contract field {mapped}')
        require(row['frozen_proposal'] == {'status': 'proposal_at_selection_not_automatically_accepted',
                                          'text': contract.get('proposed_not_accepted')}, f'{loop}: proposal retained as proposal')
        for mapped, authored in [('derivation_steps', 'steps'), ('forward_route', 'forward'),
                                 ('reverse_route', 'reverse'), ('skeptical_objection', 'objection'),
                                 ('exception_or_amended_hypothesis', 'exception'),
                                 ('closest_checked_prior_work', 'prior_work'), ('novelty_category', 'novelty_category')]:
            require(row[mapped] == metadata['loops'][loop][authored], f'{loop}: metadata field {mapped}')
        require(row['scientific_priority'] == 'unverified', f'{loop}: no priority promotion')
        gate_hashes[loop] = sha(f'research/round22/advisor/{loop}-gate.json')
        require(row['gate_sha256'] == gate_hashes[loop], f'{loop}: gate binding')
        counts[loop], statuses[loop] = len(gate['files']), gate['status']
        for path, digest in gate['files'].items():
            require(files.get(path, digest) == digest, 'shared source hash collision: ' + path)
            files[path] = digest
        for predecessor in loops:
            path = f'research/round22/advisor/{predecessor}-gate.json'
            if path in contract['dependencies']:
                require(loops.index(predecessor) < loops.index(loop), f'{loop}: forward scientific dependency')
                require(contract['dependencies'][path] == gate_hashes[predecessor], f'{loop}: predecessor hash')
                dependency_edges.append([predecessor, loop])
    require(list(statuses.values()).count('accepted') == 8 and statuses['o1'] == statuses['o2'] == 'limited', 'scoped verdicts')
    require('at least one retained anchor' in metadata['loops']['o1']['steps'][5], 'O1 retained-anchor qualification')
    require('190 distinct unordered' in metadata['loops']['q1']['reverse'], 'Q1 pair count precision')
    require('two ordered cross terms' in metadata['loops']['q2']['steps'][4], 'Q2 ordered cross-channel precision')
    print(json.dumps({'schema': 'ym22-post-ten-map-check-v1', 'passed': True,
                      'research_loops_added': 0, 'new_producer_replays': False,
                      'claim_map_sha256': sha(map_path), 'site_data_sha256': sha(metadata_path),
                      'admission_source_sha256': sha('research/round22/admission.py'),
                      'reviewed_gates': gate_hashes, 'statuses': statuses,
                      'bound_file_counts': counts, 'distinct_gate_bound_files': len(files),
                      'current_scientific_dependency_edges': dependency_edges,
                      'all_gate_contract_metadata_bindings_match': True}, indent=2, sort_keys=True) + '\n', end='')


if __name__ == '__main__':
    main()
