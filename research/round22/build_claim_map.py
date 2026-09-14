#!/usr/bin/env python3
"""Assemble the complete claim/dependency index from already admitted gates."""
import json
import sys
sys.dont_write_bytecode=True
from admission import ROOT,LOOPS,gate,read,source,digest,require
from presentation_schema import loop_metadata


def main():
    metadata=read(source('research/round22/site-data.json'))
    gates={loop:gate(loop) for loop in LOOPS}
    rows=[]
    for loop,g in gates.items():
        contract=read(source(f'research/round22/contracts/{loop}.json'))
        item=loop_metadata(metadata['loops'][loop],loop)
        rows.append({'loop':loop,'verdict':g['status'],'target_verdict':g['target_verdict'],
            'original_question':contract['target'],'supported_statement':g['claim'],
            'supported_equations':g['equations'],'assumptions_and_scope':g['scope'],
            'frozen_proposal':{'status':'proposal_at_selection_not_automatically_accepted',
                               'text':contract.get('proposed_not_accepted')},
            'derivation_steps':item['steps'],'forward_route':item['forward'],
            'reverse_route':item['reverse'],'skeptical_objection':item['objection'],
            'exception_or_amended_hypothesis':item['exception'],
            'closest_checked_prior_work':item['prior_work'],
            'novelty_category':item['novelty_category'],'scientific_priority':'unverified',
            'independence':g['independence'],'limitations':g.get('limits',[]),
            'next_missing_premise':g['next_missing_premise'],
            'dependency_bindings':contract['dependencies'],
            'instruction_snapshots':contract['instruction_inputs'],
            'gate_sha256':digest(source(f'research/round22/advisor/{loop}-gate.json')),
            'reproduction_command':f'python3 -B research/round22/reproduce.py --loops {loop} --output /absolute/new/{loop}-replay'})
    payload={'schema':'ym22-claim-dependency-map-v1','completed_research_loops':10,
        'index_generation_adds_research_loops':0,'index_is_not_a_new_admission':True,
        'continuum_status':'Four-dimensional continuum Yang–Mills construction and mass gap remain open.',
        'source_reading_depth':'See each bound producer source note and skeptical primary-source map; no exhaustive novelty audit.',
        'claims':rows,'future_goals_record':'research/round22/advisor/post-ten-roadmap.json'}
    (ROOT/'research/round22/advisor/claim-dependency-map.json').write_text(json.dumps(payload,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'built','reviewed_loops':10,'research_loops_added':0}))


if __name__=='__main__':main()
