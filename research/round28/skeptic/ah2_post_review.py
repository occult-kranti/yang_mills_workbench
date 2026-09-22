#!/usr/bin/env python3
"""AH2 exact post-exchange audit; no producer algorithm imports."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];P='research/round28/';COUNTS=Counter()
def need(ok,label):
    COUNTS[label]+=1
    if not ok:raise RuntimeError(label)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def q(x):return Q(x['numerator'],x['denominator']) if isinstance(x,dict) else Q(x)
def enc(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x
def expbox(x):
    t=s=Q(1)
    for j in range(1,97):t*=x/j;s+=t
    upper=s+t*x/97/(1-x/98)
    return 1/upper,1/s

def main(output):
    bindings={};data={};provenance={}
    expected={'forward':'86cd639386b3f2ce3850037cea518467636d24d7b5566c9513d795d0781e5746',
              'reverse':'e74a8c24abaff73f33b4abedba1e6ee54a60e87ef9a13cd2f914520d4823fd5c'}
    con=read(P+'contracts/ah2.json')
    invname=P+'skeptic/ah2-post-review-inputs/source-inventory.json'
    for e in read(invname)['entries']:
        need(sha(e['source'])==e['sha256']==sha(e['snapshot']),'post-exchange snapshot equality')
        bindings[e['source']]=bindings[e['snapshot']]=e['sha256']
    bindings[invname]=sha(invname)
    for side,h in expected.items():
        base=P+side+'/ah2/';fr=read(base+'freeze.json')
        need(sha(base+'freeze.json')==h,'exact producer freeze')
        files=fr['bindings'] if side=='forward' else {base+k:v for k,v in fr['files'].items()}
        for name,digest in files.items():need(sha(name)==digest,'all producer freeze bindings')
        d=read(base+'output/results.json');data[side]=d
        for name,digest in d['bindings'].items():need(sha(name)==digest,'runtime scientific and source bindings')
        entries={e['source']:e for e in read(base+'inputs/source-inventory.json')['entries']}
        for name,digest in con['sources'].items():
            need(entries[name]['sha256']==sha(name)==sha(entries[name]['snapshot'])==digest,'all contract source closures')
        for name in ['freeze.json','report.md','check.py','output/results.json','inputs/source-inventory.json']:
            bindings[base+name]=sha(base+name)
        replay=P+'skeptic/ah2-'+side+'-fresh-replay/results.json'
        need(sha(replay)==sha(base+'output/results.json'),'fresh stored output equality')
        bindings[replay]=sha(replay)
        initial='prepublication-freeze-binding-draft.json' if side=='forward' else 'freeze-initial-inventory-format.json'
        initial_doc=read(base+initial)
        initial_files=initial_doc['bindings'] if side=='forward' else {base+k:v for k,v in initial_doc['files'].items()}
        need(all(files.get(name)==digest==sha(name) for name,digest in initial_files.items()),'initial inventory bound bytes unchanged')
        added=set(files)-set(initial_files)
        added_source_freezes=[p for p in added if p.endswith('/ah1/freeze.json')]
        need(len(added_source_freezes)==2 and base+initial in added and len(added)==3,'only missing source-freezes and historical draft added')
        for rel in ['check.py','report.md','output/results.json']:
            need(initial_files.get(base+rel)==files[base+rel],'inventory repair changed no scientific bytes')
        bindings[base+initial]=sha(base+initial)
        provenance[side]={'initial_record':base+initial,'initial_sha256':sha(base+initial),
                          'added_source_freeze_snapshots':sorted(added_source_freezes),
                          'scientific_bytes_unchanged':True,'final_inventory_complete':True}
    ownfr=P+'skeptic/ah2-independent-freeze.json'
    need(sha(ownfr)=='af2ef98e8af732fbb704879fb69d0f52daef03b04ec75df6301b53763d9df270','independent freeze preserved')
    for name,digest in read(ownfr)['bindings'].items():need(sha(name)==digest,'all independent frozen bytes');bindings[name]=digest
    bindings[ownfr]=sha(ownfr)
    receipt=P+'skeptic/ah2-replay-receipt.json'
    for side,modes in read(receipt)['results'].items():
        for mode,r in modes.items():
            need(r['exit_code']==0 and r['all_outputs_byte_identical'] is True and r['fresh_output_created'] is True,'required fresh normal optimized executions')
            need(r['outputs']['results.json']==sha(P+side+'/ah2/output/results.json'),'fresh replay receipt binds actual output')
    bindings[receipt]=sha(receipt)
    fw,rv=data['forward'],data['reverse'];own=read(P+'skeptic/ah2-independent.json')
    oldname=P+'skeptic/ah2-inputs/research/round28/skeptic/ah1-independent.json';old=read(oldname);bindings[oldname]=sha(oldname)
    need(fw['check_count']==6605 and rv['check_count']==717 and own['check_count']==3146,'exact executed check counts')
    need(fw['checks_passed'] is True and all(v is True for v in fw['controls'].values()) and rv['all_checks_passed'] is True and all(v is True for v in rv['checks'].values()),'all producer controls passed')
    basis=old['physical_basis'];S={(i,j):q(v) for i,j,v in old['magnetic_sparse_action']}
    T={(i,j-1):v for (i,j),v in S.items() if i>=30 and 1<=j<=29}
    need({(i,j):q(v) for i,j,v in fw['blocks']['C_without_minus_lambda_entries']}==T,'all forward complete loading entries')
    need(len(rv['full_blocks']['N_rows'])==531,'all reverse new rows')
    gram=[[Q(0) for _ in range(29)] for _ in range(29)]
    for row in rv['full_blocks']['N_rows']:
        i=row['basis_id'];b=basis[i];entries={j-1:q(v) for j,v in row['face_coefficients']};metric=q(b['metric'])
        need(entries=={j:v for (k,j),v in T.items() if i==k},'each reverse loading row complete')
        need(q(row['metric'])==metric and q(row['energy'])==q(b['energy']),'each physical row metric and electric energy')
        loss=metric*sum(entries.values())**2/29
        need(q(row['deleted_bright_quadratic_loss'])==loss>0,'all531 discriminating row deletion controls')
        for i1,x in entries.items():
            for j1,y in entries.items():gram[i1][j1]+=metric*x*y
    need(all(gram[i][j]==7*(i==j)+Q(1,4) for i in range(29) for j in range(29)),'entire source Gram recomputed')
    need(all(not(i>=30 and j>=30) for i,j in S),'full new-to-new magnetic zero')
    need(min(q(b['energy']) for b in basis[30:])==Q(9,2),'actual centered new-block damping floor')
    fu=fw['uniform_inputs'];re=rv['envelopes'];oc=own['uniform_constants']
    mapping={'lambda':'Lambda','eta_class':'eta_theorem','g':'g','d':'d','r0':'r0','p0':'p0_full',
             'rplus':'r_plus','pplus':'p_plus','delta':'delta_plus','q0_reverse_AH1':'q0_reverse_AH1',
             'q':'stationary_face_bound','b':'excited_input_bound','denominator':'D_true',
             'outside_norm_bar':'Bbar','face_to_new_norm_bar':'Cbar'}
    for a,b in mapping.items():need(q(fu[a])==q(re[b]),'both producer scalar constants agree')
    L=Q(1,100);g=3-29*L;d=Q(9,2);p0=Q(41,12)*L*L/g;rp=29*L*p0;pp=rp/g;delta=rp*rp/g
    q0=Q(9,10)*L;station=q0+p0;excited=station+Q(1,100);den=1-Q(29,72)*L*L-Q(1,100)-p0;C=Q(19,5)*L;B=29*L
    expectedvals={'g':g,'d':d,'p0':p0,'rplus':rp,'pplus':pp,'delta':delta,'q':station,'b':excited,'denominator':den,'face_to_new_norm_bar':C,'outside_norm_bar':B}
    for k,v in expectedvals.items():need(q(fu[k])==v,'fresh formula for inherited and new envelopes')
    need(q(re['p0_nested'])==q(re['p0_full'])==p0,'two distinct original projector comparisons')
    early=3*delta+B*C*(station*3/d+excited/(g*d));late=pp+(2*excited+pp)/3000;rel=early/den
    fj=fw['join_certificate'];rj=rv['join_certificate']
    for fkey,rkey,value in [('join','join',Q(3)),('early_absolute','early_absolute_upper',early),('late_absolute','late_absolute_upper',late),('all_time_absolute','all_time_absolute_upper',early),('all_time_relative','all_time_true_relative_upper',rel)]:
        need(q(fj[fkey])==q(rj[rkey])==value,'both exact all-time join formulas')
    need(late<early and rel<Q(1,10000)<Q(11,5000),'strict main target and all-time branch dominance')
    need(expbox(3*g)[1]<Q(1,3000),'fresh outward all-time exponential certificate')
    ownabs=q(own['all_time']['early_monotone_absolute_upper']);ownrel=q(own['all_time']['true_relative_upper'])
    need((ownabs-3*delta)==Q(151,152)*(early-3*delta),'different valid source caps explain entire result difference')
    need(q(oc['c'])==Q(151,40)*L and Q(151,40)**2>Q(57,4),'independent tighter source cap valid')
    need(ownrel==ownabs/den<rel,'independent attribution kept; no equality or optimality claim')
    # All prescribed certificate rows, with fresh narrower scalar exponential enclosures.
    fgrid={}
    for row in fw['fixtures']:
        key=(q(row['lambda']),q(row['sigma']));fgrid.setdefault(key,[]).append(row)
    need(len(fgrid)==9 and len(fw['fixtures'])==27 and len(rv['certificate_grid'])==9 and len(rv['fixture_combinations'])==27,'exact prescribed fixture counts')
    need(set(fgrid)=={(l,t) for l in [Q(0),Q(1,200),Q(1,100)] for t in [Q(0),Q(1),Q(3)]},'no additional physical fixture parameters')
    for rr in rv['certificate_grid']:
        l,t=q(rr['lambda']),q(rr['sigma']);rows=fgrid[l,t];fr=rows[0]
        need(len({x['preparation'] for x in rows})==3,'all three preparations per certificate')
        gg=3-29*l;dd=Q(9,2);p=Q(41,12)*l*l/gg;r=29*l*p;de=r*r/gg
        a=Q(9,10)*l+p;b=a+Q(1,100);cc=Q(19,5)*l;bb=29*l;D=1-Q(29,72)*l*l-Q(1,100)-p
        for rate,keyf,keyr in [(gg,'exp_minus_g_interval','exp_g_interval'),(dd,'exp_minus_d_interval','exp_d_interval')]:
            goldlo,goldhi=expbox(rate*t)
            for box in [fr[keyf],rr['certificate'][keyr]]:
                lo,hi=map(q,box);need(lo<=goldlo<=goldhi<=hi,'each published exponential enclosure contains fresh rigorous interval')
        for side,row in [('forward',fr),('reverse',rr['certificate'])]:
            eg=tuple(map(q,row['exp_minus_g_interval' if side=='forward' else 'exp_g_interval']))
            ed=tuple(map(q,row['exp_minus_d_interval' if side=='forward' else 'exp_d_interval']))
            load=cc*(a*(1-ed[0])/dd+b*(eg[1]-ed[0])/(dd-gg))
            I=cc*(a/dd*(t-(1-ed[1])/dd)+b/(dd-gg)*((1-eg[0])/gg-(1-ed[1])/dd))
            V=de*t+bb*I
            need(q(row['N_loading_upper' if side=='forward' else 'loading_upper'])==load,'full stationary-plus-excited loading arithmetic')
            need(q(row['physical_early_absolute_upper' if side=='forward' else 'early_upper'])==V,'complete integrated physical and center arithmetic')
            need(load>=0 and V>=0,'nonnegative physical certificate')
            if l==0 or t==0:need(V==load==0,'zero coupling/time exact envelopes')
        need(q(rr['true_denominator'])==D and q(fr['full_preparation_radius_used'])==Q(1,100),'point true denominator and unchanged class')
        trueupper=0 if l==0 or t==0 else min(q(rr['certificate']['early_upper']),q(rr['certificate']['late_upper']))
        need(q(rr['absolute_upper'])==trueupper and q(rr['true_relative_upper'])==trueupper/D<=rel,'reverse point certificate and true quotient')
        for row in rows:need(q(row['physical_early_relative_upper'])==q(row['physical_early_absolute_upper'])/D,'all forward true relative rows')
    eta=Q(1,200);rad=1-eta*eta
    need(rad+eta*eta==1 and rad<(1-eta*eta/2)**2,'complex metric normalization and amplitude not distance')
    for prep in fw['preparations']:
        need(q(prep['norm_squared'])==1 and q(prep['distance_squared_upper'])<Q(1,100)**2,'forward preparation certificate')
    for prep in rv['preparations'][1:]:
        lo,hi=map(q,prep['vacuum_coefficient']['interval'])
        need(lo*lo<=rad<=hi*hi and q(prep['distance_squared_upper'])==2-2*lo<Q(1,100)**2,'reverse exact preparation radical and class')
    # Audit the additional actual-model denominator control from the forward report.
    neighbors={i:set() for i in range(561)}
    for (i,j),v in S.items():
        need(v>0,'all nonzero magnetic entries have positive phase')
        neighbors[i].add(j)
    reached={0};front={0}
    while front:
        nxt=set().union(*(neighbors[i] for i in front))-reached;reached|=nxt;front=nxt
    need(len(reached)==561,'irreducible retained magnetic adjacency in positive physical metric')
    # Necessary SU2 tensor-product selection on every original edge. Only c0*W0
    # can have the outside target j=3/2 on all four first-face edges and0 elsewhere.
    face_sets=[set(e for e,s in f['word']) for f in old['geometry']['faces']]
    target={e:3 for e in face_sets[0]};contributors=[]
    for i,b in enumerate(basis):
        spins={int(e):j for e,j in b['twice_spin_support'].items()}
        for p,edges in enumerate(face_sets):
            possible=True
            for e in range(46):
                j=spins.get(e,0);wanted=target.get(e,0)
                if (wanted not in (abs(j-1),j+1)) if e in edges else (wanted!=j):
                    possible=False;break
            if possible:contributors.append((i,p))
    need(contributors==[(30,0)] and basis[30]['kind']=='spin_one','unique complete representation-support contributor to first-face spin3/2')
    m2,m4,m6=Q(1),Q(2),Q(5)
    need(m6-4*m4+4*m2==1 and (m6-3*m4+2*m2)/2==Q(1,2),'normalized outside witness and unique coefficient')
    feedback=eta*eta*L**4*sum(gram[j][0]**2 for j in range(29))
    need(q(rv['control_evidence']['prepared_face_second_derivative_return_squared'])==feedback>0,'reverse full feedback norm on actual preparation')
    need(q(fw['control_evidence']['positive_feedback_second_derivative_difference'])==L*L*gram[0][0]>0,'forward face feedback coefficient')
    need(q(own['controls']['full_feedback_prepared_first_face_second_derivative_return'])==eta*L*L*gram[0][0],'independent preparation feedback coefficient')
    need(fw['nondiscriminating_controls'][0]['lambda']=='0' and q(fw['nondiscriminating_controls'][0]['second_derivative_difference'])==0 and rv['control_evidence']['vacuum_second_order_return_nondiscriminating'] is True,'distinct blind feedback candidates explicitly preserved')
    drop=Q(29,12)*L*L/(1+Q(29,36)*L*L);z=1-Q(29,72)*L*L
    stationary_lower=2*drop*(z-p0)**2/(L*Q(27,5))
    need(q(rv['control_evidence']['stationary_face_limit_on_vacuum_lower_at_cap'])==stationary_lower>0,'actual reverse stationary lower witness')
    need(q(rv['control_evidence']['denominator_diagnostic_full_squared'])==Q(13,25)<1,'reverse abstract denominator diagnostic retained as abstract')
    result={'schema':'ym28-ah2-skeptic-post-review-v1','loop':'ah2','accepted_mathematical_scope':True,
            'blocking_issues':[],'check_groups':dict(COUNTS),'check_count':sum(COUNTS.values()),
            'bindings':bindings,'provenance_review':provenance,
            'producer_relative_upper':rel,'independent_relative_upper':ownrel,
            'common_public_strict_upper':Q(1,10000),'actual_true_denominator':den,
            'source_caps':{'forward':C,'reverse':C,'independent':q(oc['c'])},
            'actual_forward_denominator_control':{'adjacency_connected_rank':561,'all_metric_normalized_offdiagonals_negative_for_positive_lambda':True,
                'outside_target':'normalized spin3/2 first-face character','only_input_and_multiplier':contributors,
                'outside_coefficient':Q(-1,2),'strict_full_energy_below_retained_for_positive_lambda':True,
                'true_minus_retained_squared_norm_derivative_on_vacuum':'2(epsilon-mu)<0',
                'argument':'Absolute-value variational ground plus connected negative offdiagonals gives strictly positive coordinates. Unique nonzero outside term then gives BfP nonzero. Smooth complementary trial lowers Rayleigh quotient. This is analytic, not an evaluated heat vector.'},
            'controls_scope':{'forward_denominator':'actual AH model proof; checked complete support and metric adjacency',
                              'reverse_denominator':'explicit two-state countermodel only',
                              'independent_denominator':'abstract norm-inference counterexample only',
                              'blind_feedback_candidates_preserved':True},
            'limitations':['One fixed graph and declared original preparation class.',
                'Exact own-ground-centered heat; no numerical heat vector or rounded-center evaluator.',
                'Upper certificates differ by valid source cap and do not measure actual errors or optimality.',
                'No real-time, graph-size, physical matching, thermodynamic or continuum Yang-Mills theorem.'],
            'new_research_loops':0}
    output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'check_count':result['check_count'],'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'blocking_issues':[]}))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'ah2-post-review.json');main(ap.parse_args().output)
