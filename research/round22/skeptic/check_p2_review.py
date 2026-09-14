#!/usr/bin/env python3
"""Post-freeze independent matrix-derivative checks; no producer imports."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path


def need(value, message):
    if value is not True:
        raise RuntimeError(message)


Z=(F(0),F(0)); O=(F(1),F(0))


def za(a,b):return (a[0]+b[0],a[1]+b[1])
def zs(a,c):return (a[0]*c,a[1]*c)
def zm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def zc(a):return (a[0],-a[1])
MI=(O,Z,Z,O); MZ=(Z,Z,Z,Z)


def ma(a,b):return tuple(za(x,y) for x,y in zip(a,b))
def ms(a,c):return tuple(zs(x,c) for x in a)
def md(a):return (zc(a[0]),zc(a[2]),zc(a[1]),zc(a[3]))
def mm(a,b):
    return tuple(za(zm(a[2*i],b[j]),zm(a[2*i+1],b[2+j]))
                 for i in range(2) for j in range(2))


def matrix(q):
    a,x,y,z=map(F,q)
    return ((a,-z),(-y,-x),(y,-x),(a,z))


def trace(a):
    z=zs(za(a[0],a[3]),F(1,2))
    need(z[1]==0,'normalized SU2 trace must be real')
    return z[0]


def constant(a):return (a,MZ,MZ)


def derivative_product(a,b):
    # Actual first/second derivatives, with the explicit factor two.
    return (mm(a[0],b[0]),ma(mm(a[1],b[0]),mm(a[0],b[1])),
            ma(ma(mm(a[2],b[0]),ms(mm(a[1],b[1]),2)),mm(a[0],b[2])))


def derivative_adjoint(a):return tuple(md(x) for x in a)


def word_derivatives(word,configuration,edge,generator):
    value=constant(MI)
    for e,sign in word:
        g=configuration[e]
        factor=(g,mm(generator,g),mm(mm(generator,generator),g)) if e==edge else constant(g)
        if sign<0:factor=derivative_adjoint(factor)
        value=derivative_product(value,factor)
    return value


def scalar_product_second(a,b):
    return a[2]*b[0]+2*a[1]*b[1]+a[0]*b[2]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.absolute()
    need(not out.exists(),'fresh output required')
    for p in (out,*out.parents):need(not p.is_symlink(),'symlink rejected')
    base=Path(__file__).resolve().parent
    preparation_path=base/'p2-preparation-checks.json'
    preparation=json.loads(preparation_path.read_text())
    need(preparation['current_producers_read'] is False,'independent pre-freeze topology source')
    words={int(e):word for e,word in preparation['all_chord_loop_words'].items()}
    tree=set(preparation['tree_edges']);chords=preparation['chords'];selected=[28,27,24]
    cuts=preparation['all_tree_cut_coefficients']
    def budget(kept):
        coeff={e:1 for e in kept}
        for row in cuts:
            n={e:sum(abs(a) for a in row['left_right_coefficients'][str(e)]) for e in kept}
            total=sum(n.values())
            for e in kept:coeff[e]+=total*n[e]
        return max(coeff.values()),coeff
    full,full_coeff=budget(chords);partial,partial_coeff=budget(selected)
    need(full==77 and partial==16 and partial_coeff=={28:12,27:16,24:14},
         'independent representation-block form budget')
    pool=[matrix(q) for q in [(F(3,5),F(4,5),0,0),
          (F(1,3),F(2,3),F(2,3),0),(F(1,3),0,F(2,3),F(2,3)),
          (F(5,13),0,0,F(12,13))]]
    need(all(mm(m,md(m))==MI for m in pool),'exact SU2 matrix fixtures')
    generators=[matrix((0,F(1,2)*int(i==0),F(1,2)*int(i==1),F(1,2)*int(i==2)))
                for i in range(3)]
    need(all(mm(t,t)==ms(MI,F(-1,4)) for t in generators),'Casimir normalization')
    config={e:MI if e in tree else pool[e%4] for e in range(33)}
    config.update({28:pool[0],27:pool[1],24:pool[2],16:pool[2]})
    actual_joint=wrong_joint=actual_single=wrong_single=F(0)
    for t in generators:
        a=word_derivatives(words[16],config,14,t)
        u=word_derivatives(words[28],config,14,t)
        v=word_derivatives(words[27],config,14,t)
        actual=derivative_product(a,derivative_adjoint(u))
        wrong=derivative_product(constant(config[16]),derivative_adjoint(u))
        actual_trace=tuple(map(trace,actual));wrong_trace=tuple(map(trace,wrong))
        y=tuple(map(trace,v))
        actual_single-=actual_trace[2];wrong_single-=wrong_trace[2]
        actual_joint-=scalar_product_second(actual_trace,y)
        wrong_joint-=scalar_product_second(wrong_trace,y)
    need(actual_single==wrong_single==F(3,20),'original single-trace control is nondiscriminating')
    need(actual_joint==F(29,90) and wrong_joint==F(-1,30),
         'replacement invariant product discriminates internal-chord omission')
    need(actual_joint-wrong_joint==F(16,45),'nonzero replacement-control margin')
    pure=matrix((0,1,0,0));cross={e:MI for e in range(33)}
    cross[28]=cross[27]=pure
    full_cross=F(0)
    for e in range(33):
        for t in generators:
            x=tuple(map(trace,word_derivatives(words[28],cross,e,t)))
            y=tuple(map(trace,word_derivatives(words[27],cross,e,t)))
            full_cross-=scalar_product_second(x,y)
    need(full_cross==F(-3,2) and trace(pure)==0,'all-link mixed derivative control')
    # Independent positive exponential series, not the producer alternating sum.
    half=F(1,2);N=30
    s=sum((half**n/F(factorial(n)) for n in range(N+1)),F(0))
    tail=half**(N+1)/F(factorial(N+1))/(1-half/F(N+2))
    lo,hi=1/(s+tail),1/s
    dlo,dhi=(lo**9-hi**12)/4,(hi**9-lo**12)/4
    interval=['0.00215756109039398701827449','0.00215756109039398701827450']
    need(F(interval[0])<dlo<dhi<F(interval[1]),'tight fixed-time discrepancy interval')
    result={'schema':'ym22-skeptic-review-check-v1','loop':'p2','passed':True,
      'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'preparation_check_sha256':hashlib.sha256(preparation_path.read_bytes()).hexdigest(),
      'producer_imports':False,'current_producers_read_after_both_frozen':True,
      'arithmetic':'Exact 2x2 Gaussian-rational matrices and actual second derivatives',
      'full_form_upper':full,'full_form_coefficients':full_coeff,
      'selected_form_upper':partial,'selected_form_coefficients':partial_coeff,
      'single_trace_correct_and_wrong_tree14_C':'3/20',
      'joint_trace_correct_tree14_C':str(actual_joint),
      'joint_trace_wrong_tree14_C':str(wrong_joint),
      'joint_replacement_control_margin':str(actual_joint-wrong_joint),
      'all_link_xy_C':str(full_cross),'wrong_diagonal_xy_C':'0',
      'original_link_axis_variations_for_cross_control':99,
      'fixed_time_strict_interval':interval,
      'controls':{'K77_full_K16_selected_verified':True,
       'original_single_trace_control_not_counted_as_rejection':True,
       'replacement_internal_chord_control_rejects':True,
       'dropping_mixed_derivatives_rejects':True,
       'independent_tight_time_interval_passes':True},
      'research_loops_added':0,
      'scope':'Proof-supporting review checks, not a finite proof of Hilbert or domain claims'}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'p2','passed':True,'controls':len(result['controls'])}))


if __name__=='__main__':main()
