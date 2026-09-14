#!/usr/bin/env python3
"""O2 review: exact support declarations, structured parity test and budgets."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def need(ok, message):
    if ok is not True:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    need(not out.exists(), 'fresh output required')
    for p in (out.absolute(), *out.absolute().parents):
        need(not p.is_symlink(), 'symlink rejected')
    S = {(0,0,0), (1,0,0), (0,1,0), (0,0,1)}
    def star(a): return {tuple(a[j]+s[j] for j in range(3)) for s in S}
    chain_rows = []
    for N in (1,2,3,10,100):
        Y = set().union(*(star((i,0,0)) for i in range(N)))
        m = len(Y)
        need(m == 3*N+1, 'chain cardinality')
        # One D_i=N_i/64, uniquely declared on the star anchored at i.
        declared = {i: star(i) for i in Y}
        padded = set().union(*declared.values())
        maximum = max(sum(x in Z for Z in declared.values()) for x in padded)
        need(maximum <= 4, 'unique declarations maintain overlap bound')
        union_weight_ratio = sum(2**(len(Y | Z)-m) for Z in declared.values())
        need(union_weight_ratio == 9*N+16, 'exact indexed pair-union weights')
        indexed = F(union_weight_ratio,64)
        indexed_homological = indexed/m
        need(indexed >= F(m,64), 'actual-support lower benchmark')
        need(indexed_homological <= F(8,64), 'inverse cancellation remains bounded')
        chain_rows.append({'stars': N, 'sites': m, 'max_declared_site_overlap': maximum,
            'indexed_pair_union_bracket': str(indexed),
            'indexed_pair_union_homological_bracket': str(indexed_homological),
            'regrouped_actual_support_bracket': str(F(m,64)),
            'regrouped_actual_support_homological_bracket': '1/64'})

    # Independent sparse basis calculation for the stronger forward parity fixture.
    # Gaussian integers are exact integer pairs; no floating-point matrices.
    def gaussian_i(z): return (-z[1], z[0])
    def gaussian_scale(c,z): return (c*z[0], c*z[1])
    def gaussian_add(a,b): return (a[0]+b[0], a[1]+b[1])
    powers = ((1,0),(0,-1),(-1,0),(0,1))
    parity_rows = []
    for m in (1,4,7):
        w = [powers[b.bit_count()%4] for b in range(2**m)]
        image = [(0,0) for _ in w]
        for col in range(2**m):
            parity = (-1)**col.bit_count()
            bcol = F(parity-1, 2**(m+1))
            for i in range(m):
                row = col^(1<<i)
                sign = -1 if col&(1<<i) else 1
                brow = F((-parity)-1, 2**(m+1))
                need(sign*(bcol-brow) == F(sign*parity,2**m), 'parity commutator coefficient')
                image[row] = gaussian_add(image[row], gaussian_scale(sign,w[col]))
        need(image == [gaussian_scale(m,gaussian_i(x)) for x in w], 'common eigenvector norm witness')
        parity_rows.append({'sites':m,'homological_residual_norm_at_log2':'2',
            'generator_norm_at_log2':'2','vacuum_diagonal_norm_at_log2':'1',
            'commutator_norm_at_log2':str(m),'bilinear_ratio':str(F(m,2))})

    # Independent two-sided propagation of forward's rational scalar recurrence,
    # with a decimal grid rather than the producer's dyadic grid.
    grid = 10**120
    def down(x): return F((x.numerator*grid)//x.denominator,grid)
    def up(x): return F(-((-x.numerator*grid)//x.denominator),grid)
    tau=F(1,2**22); r=F(25460736,25)*tau*tau; d=448*tau
    rl,rh=down(r),up(r); dl=dh=d
    rows=[]
    for n in range(100):
        lam=36*(n+1)*(n+2); pl,ph=lam*rl,lam*rh
        rows.append((n,rl,rh,pl,ph))
        if pl>=1: break
        need(ph<1,'enclosure straddles radius')
        nl=down((dl+F(3,2)*rl)*pl/(1-pl))
        nh=up((dh+F(3,2)*rh)*ph/(1-ph))
        dl,dh=down(dl+2*rl),up(dh+2*rh)
        rl,rh=nl,nh
    need(n==42 and rows[-1][3]>1,'forward rational first failure')
    need(rows[15][2]<min(x[1] for x in rows if x[0]!=15),'forward rational minimum')
    need(F('1.727758')<rows[-1][3]<=rows[-1][4]<F('1.727759'),'terminal enclosure')
    # Reverse's exact contraction condition and coarse doubling index.
    for loss in (F(1,10),F(1,100),F(1,1000)):
        rr,bb=F(1,100000),F(1,1000)
        value=4*rr*(bb+F(3,2)*rr)/(loss-4*rr)
        need((value<rr)==(loss>4*bb+10*rr),'reverse exact shrink condition')
    b0=448*F(1,10**8)
    need(197*198 < F(7,40)/b0 <= 198*199,'coarse doubling index')
    result={'schema':'ym22-skeptic-independent-check-v1','loop':'o2','passed':True,
        'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'producer_imports':False,'post_freeze_clarification':True,
        'chain_union_checks':chain_rows,'structured_parity_checks':parity_rows,
        'forward_rational_first_failure':42,'forward_rational_minimum':15,
        'forward_terminal_rho_enclosure':['1.727758','1.727759'],
        'independent_directed_grid':'10^(-120)',
        'reverse_shrink_iff':'delta>4*b+10*r','reverse_coarse_doubling_index':197,
        'scope':'All-support lemma controls and stated scalar certificates; no actual SU2 algorithm or gap failure',
        'research_loops_added':0}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'loop':'o2','passed':True,'independent_checks':'support declarations, parity and recurrence'}))


if __name__=='__main__':
    main()
