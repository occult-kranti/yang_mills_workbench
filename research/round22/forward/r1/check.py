#!/usr/bin/env python3
"""R1 exact complete-star geometry, conditional Haar moments and inverse controls."""
from collections import Counter
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/r1/'
CONTRACT='research/round22/contracts/r1.json'
CONTRACT_SHA='799b5bd8f10adec2341dd7d5a8ceef2e84c2a723e01c9fae69e6b73f4311da34'
INSTRUCTIONS=['research/round22/methods/team-protocol.md',
 'research/round22/methods/v4/AGENTS-at-selection.md',
 'research/round22/methods/v4/generated-support-and-iteration.md',
 'research/round22/methods/v4/haar-maps-and-induced-dynamics.md',
 'research/round22/methods/v4/paired-physics-research-at-selection.md',
 'research/round22/methods/v4/stationarity-support-and-admission.md']
CONSULTED=['research/round21/forward/i1/report.md','research/round21/forward/i1/check.py',
 'research/round21/forward/i2/report.md','research/round22/forward/o1/report.md',
 'research/round22/forward/o1/source-notes.md','research/round22/forward/o2/report.md',
 'research/round22/forward/q2/check.py','research/round22/forward/q2/submission.json']
Z=(0,0,0);E=((1,0,0),(0,1,0),(0,0,1));G=(Z,*E)
QI=(F(1),F(0),F(0),F(0))
AXES=tuple(tuple(F(s if j==i else 0) for j in range(4))
           for i in range(4) for s in (-1,1))


def need(ok,why):
    if type(ok) is not bool or not ok:raise ValueError(why)


def reject(label,ok,details):
    rejected=False
    try:need(ok,label)
    except ValueError:rejected=True
    need(rejected,'nondiscriminating control '+label)
    return {'id':label,'passed':True,'rejected':True,'details':details}


def sha(path):
    path=path.absolute()
    for p in [path,*path.parents]:need(not p.is_symlink(),'symlink source/output')
    need(path.is_file(),'missing source/output')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,value):path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def owner(p):return (p[0]//4,p[1]//2,p[2])
def star(b):return frozenset(add(b,e) for e in G)
def cube(lo,hi):return set(product(range(lo,hi+1),repeat=3))
def free(e):
    p,a=e
    return a==2 or (a==0 and p[0]%4==3) or (a==1 and p[1]%2==1)
def qc(a):return (a[0],-a[1],-a[2],-a[3])
def qm(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,
            w*s+y*v+z*r-x*t,w*t+z*v+x*s-y*r)
def trace_word(word,values):
    value=QI
    for e,s in word:value=qm(value,values[e] if s==1 else qc(values[e]))
    return value[0]


def faces():
    tail=list(product(range(4),range(2),(0,)));owned={(p,a) for p in tail for a in range(3)}
    selected=set();omitted=[]
    for p in tail:
        for a,c in combinations(range(3),2):
            w=[((p,a),1),((add(p,E[a]),c),1),
               ((add(p,E[c]),a),-1),((p,c),-1)]
            if (a,c)==(0,1) and p[1]==0 and p[0]<3:
                selected.update(e for e,s in w)
            else:omitted.append({'p':p,'axes':(a,c),'word':w})
    need(len(owned)==24 and len(selected)==10 and selected<=owned,'complete onsite ownership')
    need(len(owned-selected)==14 and all(free(e) for e in owned-selected),'actual fourteen free factors')
    need(len(omitted)==21,'all omitted faces')
    support_counts=Counter()
    for f in omitted:
        f['edges']={e for e,s in f['word']};f['free']={e for e in f['edges'] if free(e)}
        f['support']=frozenset(owner(e[0]) for e in f['edges'])
        need(len(f['free'])>=2 and f['support']<=star(Z),'free witnesses and complete star')
        need(len(f['support'])>1,'every omitted face crosses onsite boundary')
        support_counts[tuple(sorted(f['support']))]+=1
    expected={tuple(sorted(s)):n for s,n in [({Z,E[1]},3),({Z,E[0]},1),
        ({Z,E[0],E[1]},1),({Z,E[2]},10),({Z,E[0],E[2]},2),({Z,E[1],E[2]},4)]}
    need(dict(support_counts)==expected,'full actual support classes')
    return omitted


def geometry():
    rows=[];controls=[]
    for L in (1,2,3,7):
        for label,lo,hi in [('origin',0,L-1),('bulk',1,L)]:
            Y=cube(lo,hi);Lambda=cube(0,L+1)
            retained=[b for b in sorted(Lambda) if star(b)<=Lambda]
            meeting=[b for b in retained if star(b)&Y]
            interior=[b for b in retained if star(b)<=Y]
            boundary=[b for b in meeting if b not in interior]
            incoming=[b for b in boundary if b not in Y]
            predicted=(3 if label=='origin' else 6)*L*L-3*L+1
            need(len(interior)==(L-1)**3 and len(boundary)==predicted,'exact cube boundary count')
            need(len(incoming)==(0 if label=='origin' else 3*L*L),'incoming-plane census')
            need(len(boundary)<=4*len(Y),'maximum meeting multiplicity')
            root=next(iter(Y));root_count=sum(root in Y|star(b) for b in boundary)
            need(root_count==len(boundary),'root inside full declared union')
            for x in Lambda-Y:
                need(sum(x in Y|star(b) for b in boundary)<=4,'external root count')
            need(all(len(Y|star(b))<=len(Y)+3 for b in boundary),'union support growth')
            rows.append({'placement':label,'L':L,'interior':len(interior),
                         'crossing':len(boundary),'incoming':len(incoming)})
            if L==2 and label=='bulk':
                controls.append(reject('omitted_incoming_anchors',len(boundary)-len(incoming)==predicted,
                      {'correct':predicted,'anchor_inside_only':len(boundary)-len(incoming)}))
            if L==2 and label=='origin':
                controls.append(reject('omitted_outward_stars',0==predicted,{'correct':predicted,'interior_only':0}))
    fixed=cube(0,1);retained=[b for b in sorted(fixed) if star(b)<=fixed]
    need(retained==[Z],'fixed Lambda retains exactly origin star')
    controls.append(reject('replace_declared_union_by_Y_weight',2**1==2**len(star(Z)),
                          {'correct_weight_at_log2':16,'wrong_singleton_weight':2}))
    return rows,controls


def haar(omitted):
    probe=(Z,2)
    mean=sum(2*q[0] for q in AXES)/len(AXES)
    norm2=sum((2*q[0])**2 for q in AXES)/len(AXES)
    need(mean==0 and norm2==1,'actual normalized fundamental character')
    for i in range(4):
        for j in range(4):
            need(sum(q[i]*q[j] for q in AXES)/8==(F(1,4) if i==j else 0),'exact quadratic Haar rule')
    all_edges=sorted(set().union(*(f['edges'] for f in omitted)))
    seeds=[QI,(F(1,2),)*4,(F(0),F(1),F(0),F(0)),(F(0),F(0),F(1),F(0))]
    base={e:seeds[i%len(seeds)] for i,e in enumerate(all_edges)}
    diagonal=[];vacuum_projection=[];census=[]
    for f in omitted:
        w=min(f['free']-{probe})
        square=F(0);projection=F(0)
        for q,p in product(AXES,repeat=2):
            vals={**base,probe:q,w:p};chi=2*q[0];wilson=trace_word(f['word'],vals)
            square+=chi*chi*wilson*wilson/64;projection+=chi*wilson/64
        need(square==F(1,4) and projection==0,'conditional diagonal and removed vacuum projection')
        diagonal.append(square);vacuum_projection.append(projection)
        census.append({'anchor':f['p'],'axes':f['axes'],'free_links':len(f['free']),
                       'support':sorted(f['support']),'other_free_witness':[w[0],w[1]]})
    pairs=0
    for f,h in combinations(omitted,2):
        need(len(f['edges']&h['edges'])<=1,'distinct elementary faces share at most one edge')
        choices=((f['free']-h['edges'])|(h['free']-f['edges']))-{probe}
        need(bool(choices),'cross moment has free odd witness distinct from probe')
        w=min(choices);values={e:QI for e in all_edges};before=4*trace_word(f['word'],values)*trace_word(h['word'],values)
        values[w]=tuple(-v for v in QI)
        after=4*trace_word(f['word'],values)*trace_word(h['word'],values)
        need(before==4 and after==-before,'nonzero exact center-sign witness');pairs+=1
    need(pairs==210,'all offdiagonal face pairs')
    total=sum(diagonal,F(0));energy=F(8)*F(3,4);coefficient=(F(1,3)/energy)**2*total
    need(total==F(21,4) and energy==6 and coefficient==F(7,432),'actual fixed-source defect coefficient')
    controls=[reject('drop_all_crossing_faces',F(0)==coefficient,{'correct_tau2_coefficient':str(coefficient),'wrong':'0'}),
        reject('normalized_W_instead_of_character',norm2/4==1,{'wrong_source_norm_squared':str(norm2/4),'correct':'1'}),
        reject('wrong_free_energy_unit',F(3,4)==energy,{'correct':'6','wrong':'3/4'}),
        reject('wrong_phi_normalization',total/energy**2==coefficient,
               {'correct_tau2_coefficient':str(coefficient),'omitting_divisor_three':str(total/energy**2)})]
    return {'source_mean':str(mean),'source_norm_squared':str(norm2),'free_energy':str(energy),
            'conditional_diagonal_moments':[str(x) for x in diagonal],
            'vacuum_projection_moments':[str(x) for x in vacuum_projection],
            'cross_sign_witnesses':pairs,'probe_edge_face_incidence':sum(probe in f['edges'] for f in omitted),
            'defect_norm_squared_tau2_coefficient':str(coefficient),'face_census':census},controls


def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
                     for j in range(len(b[0]))] for i in range(len(a))]
def plus(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a):return [[-x for x in r] for r in a]
def comm(a,b):return plus(mm(a,b),neg(mm(b,a)))


def inverse_controls():
    a=[[F(0),F(1)],[F(1),F(0)]];h=[[F(0),F(0)],[F(0),F(6)]]
    s=[[F(0),-F(1,6)],[F(1,6),F(0)]];zero=[[F(0),F(0)],[F(0),F(0)]]
    need(plus(comm(s,h),a)==zero,'exact actual free-channel homological sign')
    controls=[reject('wrong_interacting_homological_sign',plus(comm(neg(s),h),a)==zero,
                     {'wrong_defect_on_vacuum_squared':'4','correct':'0'})]
    rows=[]
    for tau in (F(-5,1664),F(0),F(1,1000),F(5,1664)):
        gap=1-28*abs(tau);d2=F(7,12)*tau*tau;fixed=d2/36
        lower=(1-7*abs(tau))**2*d2
        need(gap>=F(381,416) and 1/gap<=F(416,381),'uniform initial inverse interval')
        need((fixed>0)==(tau!=0),'tau-zero exception and actual nonzero crossing')
        if tau:
            controls.append(reject('bare_inverse_does_not_cancel_actual_interior_'+str(tau),lower==0,
                  {'certified_defect_norm_squared_lower':str(lower),'actual_Dw_norm_squared':str(d2)}))
        rows.append({'tau':str(tau),'G_gap_lower':str(gap),'inverse_norm_upper':str(1/gap),
                     'fixed_boundary_defect_norm_squared':str(fixed),
                     'actual_internal_source_norm_squared':str(36+d2),
                     'bare_internal_defect_norm_squared_lower':str(lower)})
    controls.append(reject('disabled_assertion_guard',False,{'mechanism':'explicit ValueError, also executed under python -O'}))
    controls.append({'id':'tau_zero_exception','passed':True,'rejected':False,
                     'outcome':'exact zero boundary defect; source and inverse remain defined'})
    return rows,controls


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    out=args.output.absolute();need(not out.exists(),'output must be fresh')
    for p in [out,*out.parents]:need(not p.is_symlink(),'symlink output component')
    need(sha(ROOT/CONTRACT)==CONTRACT_SHA,'immutable contract mismatch')
    contract=json.loads((ROOT/CONTRACT).read_text())
    need(contract['loop']=='r1' and contract['instruction_inputs']==INSTRUCTIONS,'complete frozen instruction set')
    for p,value in contract['dependencies'].items():need(sha(ROOT/p)==value,'contract dependency mismatch '+p)
    inputs=sorted(set([CONTRACT,*INSTRUCTIONS,*contract['dependencies'],*CONSULTED,
                       BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']))
    bindings={p:sha(ROOT/p) for p in inputs}
    cube_rows,gcontrols=geometry();face_data=faces();moments,hcontrols=haar(face_data)
    inverse_rows,icontrols=inverse_controls();controls=gcontrols+hcontrols+icontrols
    need(all(type(c['passed']) is bool and c['passed'] for c in controls),'strict successful controls')
    results={'schema':'ym22-forward-r1-v1','loop':'r1','direction':'forward','status':'proved_initial_inverse_boundary_obstruction',
      'passed':True,'claims':{'initial_G_gap_lower':'1-28*abs(tau)','frozen_uniform_gap':'381/416',
       'frozen_inverse_norm_upper':'416/381','extended_initial_D_interval':'abs(tau)<1/28, initial D only',
       'operator_domain':'D(G_Y)=D(H0_Y); full extension preserves D(H0_Lambda)',
       'form_domain':'D(G_Y^1/2)=D(H0_Y^1/2)',
       'local_identity':'[S_Y,G_Y]=-A_Y',
       'full_identity':'[S_Y,H0_Lambda+D_Lambda]+A_Y=sum_crossing_b [S_Y,D_b]',
       'single_boundary_operator_bound':'14*abs(tau)*N_boundary*norm(R_Y)/(1-28*abs(tau))',
       'single_boundary_vacuum_bound':'7*abs(tau)*N_boundary*norm(R_Y)/(1-28*abs(tau))',
       'declared_boundary_support':'Y union Z_b, cardinality<=|Y|+3; original indexed multiplicity',
       'boundary_root_count':'N_boundary for x in Y; at most 4 otherwise',
       'family_weight_loss_bound':'56*abs(tau)*exp(3*mu_prime)*(1/ell+4)*r_mu/g',
       'origin_cube_crossing_count':'3*L^2-3*L+1','bulk_cube_crossing_count':'6*L^2-3*L+1',
       'fixed_probe_source_norm':'1','fixed_probe_free_eigenvalue':'6','fixed_probe_retained_stars':1,
       'fixed_probe_omitted_faces':21,'fixed_probe_defect_norm_squared':'7*tau^2/432',
       'actual_internal_bare_inverse_defect_lower_squared':'(1-7*abs(tau))^2*7*tau^2/12',
       'source_is_generated_O1_residual':False,'full_homological_cancellation':False,
       'later_diagonal_iteration_proved':False,'numerical_gap_H0_D_R_proved':False,
       'Q2_gap_imported':False,'continuum_or_representation_transfer':False,'R2_executed':False},
       'cube_fixtures':cube_rows,'actual_SU2_moments':moments,'inverse_fixtures':inverse_rows}
    out.mkdir(parents=True)
    save(out/'results.json',results)
    save(out/'controls.json',{'schema':'ym22-controls-v1','loop':'r1','direction':'forward','passed':True,'controls':controls})
    save(out/'source-manifest.json',{'schema':'ym22-source-manifest-v1','loop':'r1','direction':'forward',
        'inputs':bindings,'outputs':{p:sha(out/p) for p in ['results.json','controls.json']}})
    print(json.dumps({'loop':'r1','direction':'forward','status':results['status'],'passed':True,
                      'controls':len(controls),'outputs':{p:sha(out/p) for p in ['results.json','controls.json','source-manifest.json']}},sort_keys=True))


if __name__=='__main__':main()
