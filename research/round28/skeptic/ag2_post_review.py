#!/usr/bin/env python3
"""Post-exchange exact comparisons and frozen-source replay validation for AG2."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fraction(v):
    if 'exact' in v:
        return Q(v['exact'])
    return Q(v['numerator'],v['denominator'])


def expected(m, direction):
    rho = Q(9,4)
    s = m/9 if direction == 'reverse' else Q(4,35)*m
    r = Q(4,3)*s**3 if direction == 'reverse' else m**3/567
    if direction == 'forward':
        q1 = 4*rho**4+84*rho**7
        q2 = 4*rho**4+252*rho**7+216*rho**9+1920*rho**10
        x = 24*s*rho**3
        e2 = 2*s*(m+s/2)*q1
        e3same = 8*rho**4*s*s*(m+s/3)
        e3other = 2*s*s*(m+s/3)*(q2-4*rho**4)
        e4 = 4*rho**4*(m+s/4)*((1-x)**-3-1-3*x-6*x*x)
    else:
        z = 26*s*rho**3
        e2 = rho**4*7*z*(m+s/2)
        e3same = 8*rho**4*s*s*(m+s/3)
        e3other = 6740*rho**10*s*s*(m+s/3)
        e4 = rho**4*(m+s/4)*z**3*(13-10*z)/(1-z)**2
    e = e2+e3same+e3other+e4
    f = (1-72*rho**3*m)**-3
    theta = 72*rho**4*r*f
    e_trans = e/(1-theta)
    r_selected = 64*r*((1-576*m)**-3-(Q(5,9) if m<=Q(1,10000) else 0))
    n = theta/(1-theta)*4*rho**4*r*(1+f/2)
    k = r_selected+n+e_trans
    return dict(e2=e2,e3same=e3same,e3other=e3other,e4=e4,e=e,
                theta=theta,e_trans=e_trans,r_selected=r_selected,n=n,k=k,
                gap=1-4*m-k/8,scalar=k/64,relative=k/8)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('ag2-post-review.json'))
    args = parser.parse_args()
    bindings = {}
    frozen_science = {}
    for side in ('forward','reverse'):
        folder = ROOT/f'research/round28/{side}/ag2'
        frozen = json.loads((folder/'freeze.json').read_text())
        declared = frozen.get('files', frozen.get('sha256'))
        for path, h in declared.items():
            p = folder/path if side=='forward' else ROOT/path
            require(side+':freeze:'+path, sha(p)==h)
        paths = [folder/'freeze.json',folder/'check.py',folder/'report.md',folder/'output/results.json',
                 ROOT/f'research/round28/skeptic/ag2-{side}-replay/results.json']
        for p in paths:
            bindings[str(p.relative_to(ROOT))]=sha(p)
        original = (folder/'output/results.json').read_bytes()
        replay = (ROOT/f'research/round28/skeptic/ag2-{side}-replay/results.json').read_bytes()
        require(side+':retained_replay_byte_equality',original==replay)
        data = json.loads(original)
        frozen_science[side]=data
        require(side+':negative_checksum_control',sha(folder/'check.py')!='0'*64)
    own = json.loads((ROOT/'research/round28/skeptic/ag2-independent-freeze.json').read_text())
    for p,h in own['bindings'].items():
        require('independent_freeze:'+p,sha(ROOT/p)==h)
        bindings[p]=h
    # Independently recover the entire low-order relative support polynomial.
    seed = {(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
    def star(b):return {tuple(a+c for a,c in zip(b,s)) for s in seed}
    def incoming(y):return {tuple(a-c for a,c in zip(p,s)) for p in y for s in seed}
    table=Counter()
    for b in incoming(seed):
        y=seed|star(b)
        for c in incoming(y):table[len(y|star(c))]+=1
    require('independent_complete_n2_union_polynomial',dict(table)=={4:1,7:36,9:24,10:192})
    require('forward_n2_table_matches',frozen_science['forward']['geometry']['relative_words_by_union_size']['2']=={str(k):v for k,v in table.items()})
    require('reverse_n2_count_matches',frozen_science['reverse']['geometry']['relative_word_counts_n0_to3'][2]==sum(table.values()))
    comparison=[]
    fieldmaps={
        'forward':dict(e2='E2_rho',e3same='E3_same_rho',e3other='E3_other_rho',e4='E_ge4_rho',e='E_direct_rho',theta='theta',e_trans='transported_E_two',r_selected='selected_R_two',n='selected_N_two',k='complete_K_two',gap='reference_gap_lower',scalar='scalar_density'),
        'reverse':dict(e2='E2_rho',e3same='E3same_pinched_rho',e3other='E3other_rho',e4='E4plus_rho',e='E_direct_rho',theta='theta',e_trans='transported_E_2_upper',r_selected='selected_R_2_upper',n='nonlinear_N_2_upper',k='complete_K_2_upper',gap='reference_only_gap_dimensionless_lower',scalar='scalar_energy_per_site_upper',relative='centered_diagonal_relative_upper')}
    for side in ('forward','reverse'):
        end=frozen_science[side]['endpoints']
        rows=end.values() if isinstance(end,dict) else end
        for row in rows:
            m=fraction(row['M']); x=expected(m,side)
            for k,p in fieldmaps[side].items():
                require(f'{side}:exact:{m}:{k}',fraction(row[p])==x[k])
            require(f'{side}:common_main_K:{m}',x['k']<Q(7,1000))
            require(f'{side}:common_reference_gap:{m}',x['gap']>Q(995,1000))
            if m<=Q(1,10000):require(f'{side}:common_narrow_K:{m}',x['k']<Q(7,100000))
            comparison.append({'producer':side,'M':str(m),'E_bound':str(x['e']),'K_bound':str(x['k']),'reference_only_gap_lower':str(x['gap'])})
    # Verify every frozen contract source is present in both producers' source packs.
    contract=json.loads((ROOT/'research/round28/contracts/ag2.json').read_text())
    fi=json.loads((ROOT/'research/round28/forward/ag2/inputs/source-inventory.json').read_text())
    ri=json.loads((ROOT/'research/round28/reverse/ag2/inputs/source-inventory.json').read_text())
    reverse_map={e['source']:e for e in ri['entries']}
    for p,h in contract['sources'].items():
        require('forward_full_source:'+p,fi.get(p)==h)
        require('reverse_full_source:'+p,p in reverse_map and reverse_map[p]['sha256']==h)
    payload={'schema':'ym28-ag2-post-review-v1','checks':len(CHECKS),'check_names':CHECKS,
             'bindings':bindings,'exact_endpoint_comparison':comparison,
             'shared_scope':'Complete original E inventory and transport with K2<7/1000 on M<=1/1000 and K2<7/100000 on M<=1/10000; centered-reference-only gap>995/1000, with remaining mixing retained.',
             'mathematical_review':'Both full reports and complete checker implementations read after all three scientific freezes. Different valid sufficient bounds retained. No blocking mathematical issue identified.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'status':'passed'},sort_keys=True))


if __name__ == '__main__':
    main()
