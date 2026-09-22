#!/usr/bin/env python3
"""Post-freeze interpretation control: compare correction to passive reweighting."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('ag3-passive-comparator.json'))
    args=parser.parse_args()
    checks=[]
    def require(name,condition):
        if not condition:raise RuntimeError(name)
        checks.append(name)
    passive=Q(3,4)**4;main=Q(3060,3623);narrow=Q(5949,96812)
    require('passive_minimum_support_factor',passive==Q(81,256))
    require('main_correction_ceiling_weaker_than_passive',main>passive)
    require('narrow_correction_ceiling_improves_universal_passive_ceiling',narrow<passive)
    examples=[]
    for m in (4,16,64):
        ratio=Q(3,4)**m
        require('passive_embedding_bound_size_'+str(m),ratio<=passive)
        if m>=16:
            require('no_actual_output_norm_comparison_size_'+str(m),ratio<narrow<main)
        examples.append({'assigned_support_size':m,'actual_norm_ratio_for_single_term':str(ratio)})
    require('no_positive_universal_lower_ratio',Q(3,4)**64<Q(1,10**7))
    record={'schema':'ym28-ag3-passive-comparison-v1','checks':len(checks),'check_names':checks,
            'passive_factor':str(passive),'main_factor':str(main),'narrow_factor':str(narrow),
            'single_term_class_examples':examples,
            'attribution':'Advisor raised passive reweighting after skeptic independent freeze; skeptic additionally identifies missing lower comparison to the actual lower-weight input norm.',
            'interpretation':'Doing no correction already gives ||B||_(3/2)<=81/256 ||B||_2. Main AG3 ceiling is weaker; narrow improves this universal upper ceiling. Neither compares corrected output with actual uncorrected ||B||_(3/2) without further source information. A single-term class witness has ratio(3/4)^m, arbitrarily small; it is not an evaluation of actual AG2 B.',
            'scope':'Additive interpretation control in AG3; no frozen scientific bytes changed and no new research loop.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'status':'passed'},sort_keys=True))


if __name__=='__main__':main()
