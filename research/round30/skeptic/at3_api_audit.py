#!/usr/bin/env python3
"""Independent direct calls into both frozen AT3 reusable evaluators."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import csv
import importlib.util
import json
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def execute():
    forward=load('hnm_frozen_forward_at3',ROOT/'research/round30/forward/at3/evaluator.py')
    reverse=load('hnm_frozen_reverse_at3',ROOT/'research/round30/reverse/at3/check.py')
    checks=[]
    def need(value,label):
        if value is not True or label in checks:raise RuntimeError(label)
        checks.append(label)
    def rejects(call,label):
        try:call()
        except (ValueError,TypeError,ZeroDivisionError):need(True,label)
        else:need(False,label)
    for fixture in ('A','B'):
        path=ROOT/f'research/round30/reverse/at3/output/fixture-{fixture}.csv'
        with path.open() as stream:rows=list(csv.DictReader(stream))
        need(len(rows)==4097,'external_csv_count_'+fixture)
        need(all(row['index']==str(j) and F(row['s'])==F(j,32) for j,row in enumerate(rows)),
             'external_csv_full_index_time_grid_'+fixture)
        samples=[(F(row['value_lower']),F(row['value_upper'])) for row in rows]
        expected={'A':F(3,32),'B':F(1,10)}[fixture]
        f=forward.evaluate(samples);r=reverse.evaluate(samples)
        need(f['lower']<=expected<=f['upper'] and f['target_width_passed'] is True,
             'forward_external_dataset_coverage_'+fixture)
        need(r['interval_I'][0]<=expected<=r['interval_I'][1] and r['meets_target'] is True,
             'reverse_external_dataset_coverage_'+fixture)
        need(reverse.evaluate_csv(path)==r,'reverse_external_csv_api_'+fixture)
        need(f['computed_AQ_samples'] is False and r['actual_aq_samples_computed'] is False,
             'external_input_does_not_assert_AQ_production_'+fixture)
    zeros=[(F(0),F(0))]*4097
    for name,module in [('forward',forward),('reverse',reverse)]:
        rejects(lambda:module.evaluate(zeros[:-1]),name+'_reject_missing_sample')
        rejects(lambda:module.evaluate(zeros+[(F(0),F(0))]),name+'_reject_extra_sample')
        rejects(lambda:module.evaluate([(F(1),F(0))]+zeros[1:]),name+'_reject_reversed_interval')
        rejects(lambda:module.evaluate([(float('nan'),F(0))]+zeros[1:]),name+'_reject_NaN')
        rejects(lambda:module.evaluate([(True,F(0))]+zeros[1:]),name+'_reject_boolean_sample')
        rejects(lambda:module.evaluate(zeros,epsilon='-1/1000000'),name+'_reject_negative_error')
        rejects(lambda:module.evaluate(zeros,epsilon='1/1000'),name+'_reject_large_error')
        rejects(lambda:module.evaluate(zeros,epsilon=True),name+'_reject_boolean_error')
    rejects(lambda:forward.evaluate(zeros,N=True),'forward_reject_boolean_design')
    rejects(lambda:reverse.evaluate(zeros,N_value=True),'reverse_reject_boolean_design')
    rejects(lambda:forward.evaluate(zeros,h='1/16'),'forward_reject_changed_grid')
    rejects(lambda:reverse.evaluate(zeros,h_value='1/16'),'reverse_reject_changed_grid')
    rejects(lambda:forward.evaluate(zeros,T='64'),'forward_reject_changed_cutoff')
    rejects(lambda:reverse.evaluate(zeros,T_value='64'),'reverse_reject_changed_cutoff')
    rejects(lambda:forward.evaluate(zeros,epsilon='0'),'forward_reject_changed_error_contract')
    rejects(lambda:reverse.evaluate(zeros,epsilon='0'),'reverse_reject_changed_error_contract')
    # The two API contracts intentionally differ: the forward evaluator
    # accepts wide bins and reports the actual width verdict; reverse
    # restricts every bin width so all accepted data pass the width bound.
    wide=[(F(0),F(1))]*4097
    f=forward.evaluate(wide)
    need(f['width']>F(1,500) and f['target_width_passed'] is False,
         'forward_wide_enclosure_returns_insufficient_width')
    rejects(lambda:reverse.evaluate(wide),'reverse_wide_enclosure_rejected')
    borderline=[(F(0),F(2,10**12))]*4097
    need(forward.evaluate(borderline)['target_width_passed'] is True,
         'forward_wider_than_reverse_limit_can_still_meet_target')
    rejects(lambda:reverse.evaluate(borderline),'reverse_declared_width_limit_enforced')
    malformed=(ROOT/'research/round30/reverse/at3/output/fixture-A.csv').read_text()
    rejects(lambda:reverse.read_csv_text(malformed.replace('1,1/32,','1,1/16,',1)),
            'reverse_csv_time_corruption_rejected')
    return {'loop':'AT3','passed':True,'checks_count':len(checks),'checks':checks,
            'api_distinction':'Forward reports conditional intervals at any arithmetic width and a target verdict; reverse rejects per-node widths above 1e-12.',
            'actual_AQ_data_validated':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);result=execute()
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':result['checks_count']}))
