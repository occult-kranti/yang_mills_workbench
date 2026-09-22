#!/usr/bin/env python3
"""AG3 frozen-source, exact endpoint and passive interpretation comparison."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def num(x):return Q(x['exact']) if 'exact' in x else Q(x['numerator'],x['denominator'])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('ag3-post-review.json'))
    args=parser.parse_args();checks=[];bindings={};data={}
    def check(name,c):
        if not c:raise RuntimeError(name)
        checks.append(name)
    for side in ('forward','reverse'):
        folder=ROOT/f'research/round28/{side}/ag3';freeze=json.loads((folder/'freeze.json').read_text())
        for p,h in freeze.get('files',freeze.get('sha256')).items():
            resolved=folder/p if side=='forward' else ROOT/p
            check(side+':freeze:'+p,sha(resolved)==h)
        replay=ROOT/f'research/round28/skeptic/ag3-{side}-replay/results.json'
        check(side+':retained_replay_byte_equality',(folder/'output/results.json').read_bytes()==replay.read_bytes())
        for p in [folder/'freeze.json',folder/'check.py',folder/'report.md',folder/'output/results.json',replay]:bindings[str(p.relative_to(ROOT))]=sha(p)
        data[side]=json.loads((folder/'output/results.json').read_text())
    sk=ROOT/'research/round28/skeptic'
    for name in ('ag3-independent-freeze.json','ag3-passive-comparator-freeze.json'):
        p=sk/name;bindings[str(p.relative_to(ROOT))]=sha(p)
        for rel,h in json.loads(p.read_text())['bindings'].items():
            check(name+':'+rel,sha(ROOT/rel)==h);bindings[rel]=h
    independent=json.loads((sk/'ag3-independent.json').read_text())
    expected={num(row['M']):row for row in independent['endpoints']}
    maps={
      'forward':{'K2_cap':'K_cap','D2_cap':'d_cap','theta_cap':'radius_cap','ratio':'factor_cap','R_b_cap':'residual_cap_at_weight_3_over_2','total_scalar_density_cap':'total_scalar_density_cap','reference_gap_lower':'reference_gap_lower'},
      'reverse':{'AG2_K_cap':'K_cap','D_next_2_upper':'d_cap','theta_upper':'radius_cap','ratio':'factor_cap','residual_b_upper':'residual_cap_at_weight_3_over_2','complete_scalar_density_upper':'total_scalar_density_cap','next_reference_gap_lower':'reference_gap_lower'}}
    for side in ('forward','reverse'):
        for label,row in data[side]['endpoints'].items():
            m=num(row['M' if side=='forward' else 'M_endpoint']);own=expected[m]
            for p,q in maps[side].items():check(f'{side}:{label}:exact:{p}',num(row[p])==num(own[q]))
            check(f'{side}:{label}:actual_factor_target',num(row['ratio'])<Q(17,20))
            check(f'{side}:{label}:reference_only_positive',num(own['reference_gap_lower'])>Q(99,100))
            if m==Q(1,10000):check(side+':narrow_1_over_16',num(row['ratio'])<Q(1,16))
            if side=='reverse':
                check(side+':passive_carried_diagonal:'+label,num(row['full_centered_diagonal_b_upper'])==Q(81,256)*num(own['d_cap'])+2*num(own['residual_cap_at_weight_3_over_2']))
            else:
                check(side+':looser_carried_diagonal:'+label,num(row['complete_diagonal_b_cap'])==num(own['d_cap'])+2*num(own['residual_cap_at_weight_3_over_2']))
                check(side+':passive_interpretation:'+label,row['beats_passive_upper_budget']==(num(row['ratio'])<Q(81,256)) and row['actual_lower_weight_input_contraction'] is False)
    passive=json.loads((sk/'ag3-passive-comparator.json').read_text())
    check('passive_factor',Q(passive['passive_factor'])==Q(81,256))
    check('main_not_better_than_passive_ceiling',Q(passive['main_factor'])>Q(passive['passive_factor']))
    check('narrow_better_than_passive_ceiling',Q(passive['narrow_factor'])<Q(passive['passive_factor']))
    note=ROOT/'research/round28/reverse/ag3/post-freeze-passive-comparison.json';nd=json.loads(note.read_text())
    for p,h in nd['bindings'].items():check('reverse_addendum_binding:'+p,sha(ROOT/p)==h)
    for label in ('main','narrow'):
        row=nd['comparison'][label]
        check('reverse_addendum_exact_difference:'+label,Q(row['difference_active_minus_passive'])==Q(row['active_coefficient'])-Q(row['passive_coefficient']))
        check('reverse_addendum_meaning:'+label,row['active_budget_stronger_than_passive']==(Q(row['active_coefficient'])<Q(row['passive_coefficient'])))
    for p in (note,note.with_suffix('.md')):bindings[str(p.relative_to(ROOT))]=sha(p)
    contract=json.loads((ROOT/'research/round28/contracts/ag3.json').read_text())
    f=json.loads((ROOT/'research/round28/forward/ag3/inputs/source-inventory.json').read_text())
    rr=json.loads((ROOT/'research/round28/reverse/ag3/inputs/source-inventory.json').read_text())
    reverse={e['source']:e['sha256'] for e in rr['entries']}
    for p,h in contract['sources'].items():
        check('forward_complete_contract_source:'+p,f.get(p)==h)
        check('reverse_complete_contract_source:'+p,reverse.get(p)==h)
    check('checksum_negative_control',sha(ROOT/'research/round28/contracts/ag3.json')!='0'*64)
    payload={'schema':'ym28-ag3-post-review-v1','checks':len(checks),'check_names':checks,'bindings':bindings,
             'mathematical_review':'Both full reports and complete implementations reviewed after all scientific freezes. Complete source/domain/BCH/root-loss estimate accepted. No blocking mathematical issue found.',
             'interpretation':'A complete one-step map with an estimate from weight2 to3/2. Main ceiling is weaker than passive81/256; narrow improves the universal passive upper ceiling only. Neither bounds output relative to the actual uncorrected lower-weight norm.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'status':'passed'},sort_keys=True))


if __name__=='__main__':main()
