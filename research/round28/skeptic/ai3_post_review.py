#!/usr/bin/env python3
"""AI3 post-exchange comparison of frozen producers and independent evidence."""
import argparse
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CHECKS=[]
sys.set_int_max_str_digits(0)


def need(ok,label):
    if not ok: raise RuntimeError(label)
    CHECKS.append(label)


def read(path): return json.loads((ROOT/path).read_text())
def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def frac(x): return F(x)
def interval(x): return tuple(map(F,x))
def div(n,d):
    if d[0]<=0: return None
    corners=[a/b for a in n for b in d]
    return min(corners),max(corners)
def box(c,r): return c-r,c+r
def gap(a,b): return max(a[0]-b[1],b[0]-a[1])
def b(q): return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'ai3-post-review.json')
    out=ap.parse_args().output;bindings={};prefix='research/round28/'
    contract=read(prefix+'contracts/ai3.json')
    need(sha(prefix+'contracts/ai3.json')=='20cab55ea76681df9fdcb1d07d74d97312a618e41e96d1ab540b6240b2537074','exact frozen contract')
    expected_freezes={'forward':'a3f02c5967c293174dd692feb136367a588bb4d13101ad6d0fb51409c5097925',
                      'reverse':'b26ea3c6421dd6a0736926c887e0a157fa305b4ea52c4313f457023c709028e7'}
    data={}
    for side in ('forward','reverse'):
        p=prefix+side+'/ai3/';fpath=p+'freeze.json';fr=read(fpath)
        need(sha(fpath)==expected_freezes[side],'current '+side+' freeze identity')
        for file,digest in fr.get('bindings',fr.get('sha256',{})).items():
            need(sha(file)==digest,'frozen producer file '+file)
        inventory=read(p+'inputs/source-inventory.json')
        entries=[{'source':a,'snapshot':p+'inputs/'+a,'sha256':h} for a,h in inventory.items()] if side=='forward' else inventory['entries']
        bysource={e['source']:e for e in entries}
        for file,digest in contract['sources'].items():
            need(file in bysource and bysource[file]['sha256']==digest,'full contract source coverage '+side+':'+file)
        for e in entries: need(sha(e['snapshot'])==e['sha256'],'snapshot '+side+':'+e['source'])
        d=read(p+'output/results.json');data[side]=d
        replay=prefix+'skeptic/ai3-'+side+'-fresh-replay/results.json'
        need(sha(replay)==sha(p+'output/results.json'),'fresh retained replay exact '+side)
        for name in ('check.py','report.md','freeze.json','output/results.json','inputs/source-inventory.json'):
            bindings[p+name]=sha(p+name)
        bindings[replay]=sha(replay)
    own_path=prefix+'skeptic/ai3-independent-freeze.json';ownfreeze=read(own_path)
    need(sha(own_path)=='0a016b529ceed2eacf9fcfb2bc17685ad9d29df3809efebfddf3d466331df970','independent pre-exchange freeze identity')
    for p,digest in ownfreeze['bindings'].items():
        need(sha(p)==digest,'independent frozen evidence '+p);bindings[p]=digest
    bindings[own_path]=sha(own_path)
    receipt=read(prefix+'skeptic/ai3-replay-receipt.json')
    for side in ('forward','reverse'):
        for mode in ('normal','optimized'):
            r=receipt['results'][side][mode]
            need(r['exit_code']==0 and r['fresh_output_created'] is True and r['byte_identical_to_frozen'] is True
                 and r['sha256']==sha(prefix+side+'/ai3/output/results.json'),'fresh successful '+side+' '+mode+' receipt')
    bindings[prefix+'skeptic/ai3-replay-receipt.json']=sha(prefix+'skeptic/ai3-replay-receipt.json')
    own=read(prefix+'skeptic/ai3-independent.json');fw=data['forward'];rv=data['reverse']
    need(own['check_count']==489 and fw['checks_count']==526 and rv['check_count']==375,'producer and independent execution counts')
    # Geometry comparison converts all three coordinate conventions to endpoint pairs.
    def fend(e):
        a,*v=e;w=list(v);w[a]+=1
        return tuple(v),tuple(w)
    def rend(e):
        v,a=e;w=list(v);w[a]+=1
        return tuple(v),tuple(w)
    rev_links=set();rev_faces=set();georows=[]
    for k in range(7):
        a=own['collars'][k];f=fw['collars'][k];r=rv['geometry']['collars'][k]
        need((a['factors'],a['links'],a['retained_faces'],a['crossing_faces'])==
             (f['factor_count'],f['link_count'],f['retained_face_count'],f['boundary_face_count'])==
             (r['factors'],r['links'],r['retained_faces'],r['crossing_faces']),'all collar counts '+str(k))
        f_links={fend(e) for e in f['links']};rev_links|={rend(e) for e in r['new_links']}
        need(f_links==rev_links,'complete geometric link sets '+str(k))
        need(hashlib.sha256(repr(sorted(f_links)).encode()).hexdigest()==a['complete_links_sha256'],'independently hashed whole links '+str(k))
        # Producer face formats are axis-axis-anchor and anchor-axis-axis.
        f_faces={(tuple(x[2:]),x[0],x[1]) for x in f['retained_faces']}
        rev_faces|={(tuple(v),a,b_) for v,a,b_ in r['new_retained_faces']}
        need(f_faces==rev_faces,'complete retained face sets '+str(k))
        georows.append({'k':k,'factors':a['factors'],'links':a['links'],'retained_faces':a['retained_faces']})
    for probe in (4,5):
        for n in range(9):
            need(own['moments'][probe-4][n]==fw['moment_polynomials'][str(probe)][n]==rv['moment_polynomials'][str(probe)][n],
                 'exact symbolic source moment '+str((probe,n)))
    for n in range(9):
        need(own['moment_differences'][n]==fw['difference_polynomials'][str(n)]==rv['moment_differences'][str(n)],'exact moment difference '+str(n))
    need(own['geometry']['reflection_permutation']==fw['geometry']['reflection_permutation']==rv['geometry']['reflection_cycles'], 'entire retained reflection agrees')
    need(fw['all_order_reflection_proved'] is True,'forward all-order proof flag')
    # Every changed precision remains an upper square-root enclosure. Reverse's
    # smaller valid row-norm arithmetic is preserved rather than forced equal.
    rows=[];not_contained=0
    for index,orig in enumerate(own['rows']):
        power,k=orig['power'],orig['k'];forward=fw['rows'][index];reverse=rv['decisions'][index]
        need((power,k)==(forward['power'],forward['k'])==(reverse['power'],reverse['k']),'same declared cell '+str(index))
        pair_intersections=[]
        for h in range(2):
            o=orig['hypotheses'][h];f=forward['hypotheses'][h];r=rv['samples'][2*index+h]
            q,eta,v,tau=map(F,(o['q'],o['eta'],o['v'],o['tau']))
            need(all(F(f[name])==F(r[name])==F(o[name]) for name in ('q','eta','v','tau')),'same fixed candidate parameters '+str((index,h)))
            need(F(o['physical_time'])==F(f['time_in_hbar_over_alpha'])==F(r['physical_time_in_hbar_over_alpha']), 'same original time '+str((index,h)))
            for probe in (4,5):
                need(o['centers'][probe-4]==f['centers'][str(probe)]==r['centers'][str(probe)], 'exact scalar center '+str((index,h,probe)))
            a,b_=map(F,(o['centers'][0]['imag'],o['centers'][1]['imag']))
            C=F(o['combination_center']);T=F(o['combination_tail'])
            need(C==F(f['combination_center'])==F(r['signed_cancellation_center'])==b_-q*a,'exact signed center combination '+str((index,h)))
            need(T==F(f['combination_all_order_remainder'])==F(r['combined_all_order_remainder']), 'all-order tail equality '+str((index,h)))
            for label,d,component,Akey in [('forward',f,'physical_components','scalar_arithmetic_remainder'),('reverse',r,'physical_errors','individual_arithmetic_remainder')]:
                comp={name:F(x) for name,x in d[component].items()};A=F(d[Akey]);P=sum(comp.values());R=P+A
                need(comp['spatial']==F(o['spatial']) and comp['averaging']==F(o['averaging']), 'same complete spatial/averaging '+str((index,h,label)))
                factor=48*tau/((1-eta)/8);root=comp['state']/factor;target=b(q*q)/96
                precision=F(1,2**(320 if label=='forward' else 400))
                need(root*root>=target and (root-precision)**2<target,'proved precision upper state enclosure '+str((index,h,label)))
                need(F(d['physical_radius'])==P and F(d['full_scalar_radius'])==R,'complete physical and arithmetic radius '+str((index,h,label)))
                need(a-R>0,'strict actual scalar denominator '+str((index,h,label)))
                den=box(a,R);direct=div(box(b_,R),den);cancel0=div(box(C,(1+q)*P+T),den);cancel=(q+cancel0[0],q+cancel0[1])
                if label=='forward':
                    recorded_direct=(F(d['ratio_all_corners']['lower']),F(d['ratio_all_corners']['upper']))
                    recorded_cancel=(F(d['ratio_cancellation']['lower']),F(d['ratio_cancellation']['upper']))
                    need(A==F(o['ordinary_arithmetic']), 'forward same conservative arithmetic '+str((index,h)))
                    need(direct[1]-direct[0] < cancel[1]-cancel[0], 'forward tighter means interval width '+str((index,h)))
                    if not(cancel[0]<=direct[0] and direct[1]<=cancel[1]): not_contained+=1
                else:
                    recorded_direct=interval(d['all_corner_quotient']);recorded_cancel=interval(d['cancellation_interval'])
                    norm=F(d['Q_norm_bound'])
                    need(norm<=6 and A==(v*norm)**9/math.factorial(9)<=F(o['ordinary_arithmetic']), 'reverse valid smaller row arithmetic '+str((index,h)))
                    shared_vals=[q+(C+dc+e5-q*e4)/(a+d4+e4) for dc,d4,e4,e5 in itertools.product((-T,T),(-A,A),(-P,P),(-P,P))]
                    shared=(min(shared_vals),max(shared_vals))
                    need(shared==interval(d['shared_e4_cancellation_interval']), 'shared physical denominator all sixteen corners '+str((index,h)))
                    best=(max(direct[0],cancel[0],shared[0]),min(direct[1],cancel[1],shared[1]))
                    need(best==interval(d['best_ratio_interval']) and best[0]<=best[1], 'all valid reverse intervals intersected '+str((index,h)))
                    pair_intersections.append(best)
                need(direct==recorded_direct and cancel==recorded_cancel,'independently recomputed ratio endpoints '+str((index,h,label)))
        refined=gap(*pair_intersections)
        need(refined==F(reverse['ratio_margin'])<0 and reverse['ratio_disjoint'] is False,'full refined ratio insufficient '+str(index))
        need(all(F(value)<0 for value in forward['signed_ratio_margins'].values()), 'all forward ratio methods insufficient '+str(index))
        need(all(F(value)<0 for value in orig['ratio_margins'].values()), 'all independent ratio methods insufficient '+str(index))
        for probe in ('4','5'):
            success=(power,k)==(18,5)
            need(forward['scalar_discrimination'][probe]['disjoint'] is success and reverse['direct_scalar_baseline'][probe]['disjoint'] is success, 'unchanged direct scalar baseline '+str((index,probe)))
        for component in ('state','spatial','averaging'):
            vals=[F(orig['component_only_ratio_margins'][component]),F(forward['single_physical_component_box_margins_diagnostic_only'][component]),F(reverse['physical_component_diagnostics'][component]['single_component_box_margin'])]
            need(all((v<0)==(vals[0]<0) for v in vals),'same component-only diagnostic verdict '+str((index,component)))
        rows.append({'power':power,'k':k,'reverse_shared_intersection_margin':str(refined),'ratio_disjoint':False,'scalar_disjoint':(power,k)==(18,5)})
    need(len(rows)==10,'exactly ten reviewed cells')
    need(not_contained>0,'width ordering does not imply blanket endpoint containment')
    result={'schema':'ym28-ai3-post-review-v1','accepted_mathematics_with_limits':True,'blocking_issues':[],
            'checks':CHECKS,'check_count':len(CHECKS),'rows':rows,'collars':georows,'forward_noncontained_direct_intervals':not_contained,
            'bindings':bindings,'scope':'Frozen producers independently replayed and compared. Exact retained all-order lemma accepted, all ten full ratio methods insufficient, scalar baseline preserved. Width versus containment and common-phase imaginary-ratio sensitivity require explicit scope. Different valid square-root/row arithmetic ceilings preserved. No new investigation.'}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'checks':len(CHECKS),'noncontained':not_contained,'status':'passed'}))


if __name__=='__main__': main()
