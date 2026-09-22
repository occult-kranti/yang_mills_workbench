#!/usr/bin/env python3
"""Exact post-exchange AH1 comparison, including all auxiliary physical matrices."""
import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];P='research/round28/';CHECKS=[]
def need(ok,label):
    if not ok:raise RuntimeError(label)
    CHECKS.append(label)
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def q(x):return F(x['numerator'],x['denominator']) if isinstance(x,dict) else F(x)
def matrix(rows):return {(i,j):q(v) for i,j,v in rows}
def qm(a,b):
    w,x,y,z=a;W,X,Y,Z=b
    return (w*W-x*X-y*Y-z*Z,w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W)
def inv(a):return (a[0],-a[1],-a[2],-a[3])
def word(w,values):
    v=(F(1),F(0),F(0),F(0))
    for i,s in w:v=qm(v,values[i] if s==1 else inv(values[i]))
    return v[0]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'ah1-post-review.json');out=ap.parse_args().output
    c=read(P+'contracts/ah1.json');bindings={};data={}
    expected={'forward':'ecd653e0a3f1886395bb0accc0d543c653f357ace6f14785fd3a83e8726da7fe','reverse':'aaf7a50f53fd83b0de085aa91500dbd86f2886b2bc96be1e83c61068238623b7'}
    need(sha(P+'contracts/ah1.json')=='9c6f5bc1a71fcd49b93a1212e1b1837a82bc588b27b695fd600cbec46be17053','exact frozen contract')
    for side in expected:
        p=P+side+'/ah1/';fr=read(p+'freeze.json');need(sha(p+'freeze.json')==expected[side],side+' freeze identity')
        fb=fr['bindings'] if side=='forward' else {p+k:v for k,v in fr['files'].items()}
        for name,digest in fb.items():need(sha(name)==digest,'frozen '+name)
        invt=read(p+'inputs/source-inventory.json');entries={e['source']:e for e in invt['entries']}
        for name,digest in c['sources'].items():
            need(entries[name]['sha256']==sha(name)==digest and sha(entries[name]['snapshot'])==digest,'complete contract source '+side+':'+name)
        d=read(p+'output/results.json');data[side]=d
        for name,digest in d['bindings'].items():need(sha(name)==digest,'producer runtime binding '+side+':'+name)
        files=['results.json'] if side=='forward' else ['results.json','graph.json','basis.json','magnetic.json']
        for name in files:
            replay=P+'skeptic/ah1-'+side+'-fresh-replay/'+name
            need(sha(replay)==sha(p+'output/'+name),'fresh '+side+' byte equality '+name)
            bindings[replay]=sha(replay);bindings[p+'output/'+name]=sha(p+'output/'+name)
        for name in ('freeze.json','report.md','check.py','inputs/source-inventory.json'):
            bindings[p+name]=sha(p+name)
    ownfreeze=read(P+'skeptic/ah1-independent-freeze.json')
    need(sha(P+'skeptic/ah1-independent-freeze.json')=='a7482ea5e8010234e781cd558de491f252414cd96a445128ac05c190d3c7d76a','independent freeze preserved')
    for name,digest in ownfreeze['bindings'].items():need(sha(name)==digest,'independent immutable '+name);bindings[name]=digest
    bindings[P+'skeptic/ah1-independent-freeze.json']=sha(P+'skeptic/ah1-independent-freeze.json')
    receipt=read(P+'skeptic/ah1-replay-receipt.json')
    for side,modes in receipt['results'].items():
        for mode,r in modes.items():
            need(r['exit_code']==0 and r['fresh_output_created'] is True and r['all_outputs_byte_identical'] is True,'fresh executed '+side+' '+mode)
            for name,h in r['outputs'].items():need(h==sha(P+side+'/ah1/output/'+name),'fresh receipt '+side+' '+mode+' '+name)
    bindings[P+'skeptic/ah1-replay-receipt.json']=sha(P+'skeptic/ah1-replay-receipt.json')
    fw=data['forward'];rv=data['reverse'];own=read(P+'skeptic/ah1-independent.json')
    rg=read(P+'reverse/ah1/output/graph.json');rb=read(P+'reverse/ah1/output/basis.json');rm=read(P+'reverse/ah1/output/magnetic.json')
    for name,digest in rv['artifact_sha256'].items():need(sha(P+'reverse/ah1/output/'+name)==digest,'reverse multi-file artifact binding '+name)
    need(own['check_count']==4594 and rv['check_count']==320 and fw['checks_passed'] is True and len(fw['controls'])==27,'producer check status and meaningful count conventions')
    need(all(v is True for v in fw['controls'].values()) and all(v is True for v in rv['checks'].values()),'all declared producer controls explicitly true')
    need(own['geometry']['vertices']==fw['graph']['vertices']==rg['vertices'],'all original24 vertices')
    for i,(o,f,r) in enumerate(zip(own['geometry']['links'],fw['graph']['edges'],rg['links'])):
        need(o['tail']==f['tail']==r['tail_coordinate'] and o['axis']==f['axis']==r['axis'],'exact original link '+str(i))
    for i,(o,f,r) in enumerate(zip(own['geometry']['faces'],fw['graph']['faces'],rg['faces'])):
        need(o['anchor']==f['tail']==r['base'] and o['axes']==f['axes']==r['axes'] and o['word']==f['word']==r['word'] and o['mask']==f['mask']==r['mask'],'complete oriented face '+str(i))
    need(fw['graph']['internal_face_ids']==rg['internal_faces'] and len(rg['internal_faces'])==7,'all internal faces retained')
    fkind={'face':'fundamental','spin1':'spin_one','pair':'disjoint'};rkind={'product':'disjoint'}
    ob=own['physical_basis'];fb=fw['enrichment']['basis'];revb=rb['basis']
    need(len(ob)==len(fb)==len(revb)==561 and rb['Gram_nullspace']==[] and fw['enrichment']['nullity']==0,'entire561-state positive physical quotient')
    for i,(o,f,r) in enumerate(zip(ob,fb,revb)):
        need(o['kind']==fkind.get(f['kind'],f['kind'])==rkind.get(r['kind'],r['kind']) and o['faces']==f['faces']==r['faces'],'same actual individual function label '+str(i))
        need(q(o['metric'])==q(f['norm2'])==q(r['metric'])>0 and q(o['energy'])==q(f['energy'])==q(r['electric']),'same physical metric and electric action '+str(i))
        need(o['twice_spin_support']==r['twice_edge_spins'],'complete original-link representation support '+str(i))
    for i,(o,f,r) in enumerate(zip(own['geometry']['unordered_pairs'],fw['enrichment']['pairs'],rg['face_pairs'])):
        need([o['p'],o['q']]==f['faces']==r['faces'] and o['mask']==f['mask']==r['mask'] and o['shared_link']==f['shared_edge']==r['shared_edge'],'all pair masks and common edge '+str(i))
        if o['shared_link'] is not None:
            signs=[next(s for e,s in own['geometry']['faces'][p]['word'] if e==o['shared_link']) for p in (o['p'],o['q'])]
            need(f['shared_orientation_signs']==signs,'physical common-edge orientations '+str(i))
    om=matrix(own['magnetic_sparse_action']);fm=matrix(fw['retained_magnetic']['entries']);revm=matrix(rm['entries'])
    need(om==fm==revm and len(om)==2124,'every retained magnetic entry and complete sparse support identical')
    need(561**2-len(om)==312597==fw['retained_magnetic']['zero_count']==rm['zero_entries'],'every structural zero represented by complete support complement')
    need(all(q(ob[i]['metric'])*v==q(ob[j]['metric'])*om[j,i] for (i,j),v in om.items()),'physical metric adjoint all matrix entries')
    # Recompute published generator examples on both real and imaginary parts.
    lam=q(fw['generator_demonstrations']['lambda'])
    for row in fw['generator_demonstrations']['cases']:
        x={i:(q(a),q(b)) for i,a,b in row['input_sparse']};y={}
        for i in range(561):
            parts=[]
            for component in range(2):
                value=(q(ob[i]['energy'])+29*lam)*x.get(i,(F(0),F(0)))[component]
                value-=lam*sum(v*x.get(j,(F(0),F(0)))[component] for (ii,j),v in om.items() if ii==i)
                parts.append(value)
            if any(parts):y[i]=tuple(parts)
        need(y=={i:(q(a),q(b)) for i,a,b in row['L_action_sparse']},'actual full generator demonstration '+row['name'])
        need(sum(q(ob[i]['metric'])*(a*a+b*b) for i,(a,b) in x.items())==q(row['norm_squared']),'actual preparation metric '+row['name'])
    # Reconstruct the reverse wrong-orientation fixture independently, preserving
    # its actual initial failure rather than turning it into a claimed success.
    fixtures=[(F(1),F(0),F(0),F(0)),(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17))]
    values=[fixtures[(i*i+i//3+1)%4] for i in range(46)];gauges=[fixtures[(i*i+2*i+1)%4] for i in range(24)]
    transformed=[qm(qm(gauges[e['tail']],values[e['id']]),inv(gauges[e['head']])) for e in rg['links']]
    bad=[];horizontal_blind=True
    for f in rg['faces']:
        need(word(f['word'],values)==word(f['word'],transformed),'reverse valid Gauss trace '+str(f['id']))
        for position in range(4):
            mutation=[(e,-s if n==position else s) for n,(e,s) in enumerate(f['word'])]
            different=word(mutation,values)!=word(mutation,transformed)
            if different:bad.append([f['id'],position])
            if rg['links'][f['word'][position][0]]['axis']<2:horizontal_blind &= not different
    need([0,2] not in bad and rg['orientation_control']['first_face_nondiscriminating'] is True,'original reverse orientation fixture honestly remains blind')
    need(bad==rg['orientation_control']['discriminating_faces'] and bool(bad),'all replacement orientation discrepancies independently reconstructed')
    need(horizontal_blind and all(rg['links'][rg['faces'][f]['word'][p][0]]['axis']==2 for f,p in bad),'reported horizontal blindness and vertical replacement provenance')
    # Full spectral/error envelopes reconstructed independently from actual m.
    cap=F(1,100);g=3-29*cap;r0=F(41,12)*cap**2;p0=r0/g;rp=29*cap*p0;pp=rp/g;dp=rp*rp/g;z=1-29*cap**2/72;D=z-cap-p0
    common={'r0':r0,'p0':p0,'rplus':rp,'pplus':pp,'dplus':dp,'denominator':D}
    need(41**2>29*57 and F(27,5)**2>29 and F(11,2)**2>29 and D>0,'valid distinct radical and true-denominator bounds')
    f=fw['uniform_certificate'];r=rv['certificates'];o=own['heat_certificate'];bounds={}
    for side,d,keys,qcoef,einv in [('forward',f,['r0_bar','p0_bar','rplus_bar','pplus_bar','dplus_bar','true_denominator'],F(11,12),F(1,int(f['exp_integer_lower']))),('reverse',r,['r0','p0_full_ground','r_plus','p_plus','ground_energy_error','true_output_floor'],F(9,10),F(1,225))]:
        need([q(d[k]) for k in keys]==list(common.values()),side+' shared complete residual/projector/denominator constants')
        b=qcoef*cap+p0+cap;early=2*(rp+dp)+29*cap*b/g;late=pp+(2*b+pp)*einv;relative=max(early,late)/D
        ek,lk,bk,rk=('early_absolute','late_absolute','b_bar','all_time_relative') if side=='forward' else ('early_join_upper','late_join_upper','excited_input_bound','all_time_true_relative_upper')
        need(q(d[bk])==b and q(d[ek])==early and q(d[lk])==late and q(d[rk])==relative,side+' exact heat error with its actual valid angle bound')
        need(sum((2*g)**n/F(math.factorial(n)) for n in range(41))>1/einv and early>late and relative<F(11,5000),side+' all-time join and common public bound')
        bounds[side]=str(relative)
    need(q(r['p0_enriched_ground'])==p0 and q(r['p0_full_ground'])==p0,'both separate nested projector envelopes explicitly retained')
    need(F(bounds['forward'])==q(o['all_time_true_relative_upper']) and F(bounds['reverse'])<F(43,20000),'valid forward-independent equality and sharper reverse attribution')
    need(fw['full_outside']['exact_cubic_outside_Gram_evaluated'] is False and rv['scope']['full_outside_Gram_evaluated'] is False,'full outside bound not misreported as evaluated Gram')
    need(q(own['outside']['spin_one_input_spin_three_halves_lower_coefficient'])==F(1,2) and q(fw['full_outside']['nonzero_witness']['output_energy'])==15,'actual new-input leakage witness retained')
    result={'schema':'ym28-ah1-post-review-v1','accepted_mathematics_with_limits':True,'blocking_issues':[],'check_count':len(CHECKS),'checks':CHECKS,'bindings':bindings,'physical_construction':{'vertices':24,'links':46,'faces':29,'P0_rank':30,'Pplus_rank':561,'shared_pairs':96,'edge_disjoint_pairs':310,'magnetic_nonzeros':2124,'magnetic_zeros':312597,'Gram_nullity':0},'relative_heat_bounds':bounds,'common_public_upper':'11/5000','reverse_attributed_upper':'43/20000','reverse_orientation_review':{'initial_control_nondiscriminating':True,'horizontal_mutations_nondiscriminating':horizontal_blind,'reconstructed_discriminating_replacements':bad},'scope':'Complete fixed-graph physical construction and exact own-ground-centered all-time heat bound for declared normalized complex P0 vacuum-near preparations; complete outside envelope, no exact outside Gram or numerical heat evaluation. Distinct valid radical/heat constants retained; no graph-size, real-time, matching or continuum theorem.','research_loop_increment':0}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','checks':len(CHECKS),'orientation_replacements':len(bad)}))


if __name__=='__main__':main()
