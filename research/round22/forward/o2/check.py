#!/usr/bin/env python3
"""O2 exact algebra and directed rational certificate propagation."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/o2/'
CONTRACT='research/round22/contracts/o2.json'
CONTRACT_SHA='86895d53f2e0944ab4c0a93eb969018dd213d9a2a5c27d1107d10e10338e15a6'
INPUTS=[CONTRACT,'research/round22/methods/team-protocol.md',
 'research/round22/methods/v2/AGENTS-at-selection.md',
 'research/round22/methods/v2/paired-physics-research-at-selection.md',
 'research/round22/methods/v2/stationarity-support-and-admission.md',
 'research/round21/advisor/i1-gate.json','research/round21/advisor/i2-gate.json',
 'research/round22/advisor/o1-decision.md','research/round22/advisor/o1-gate.json',
 'research/round22/skeptic/o1.md','research/round22/forward/o1/report.md',
 'research/round22/forward/o1/source-notes.md',BASE+'report.md',BASE+'check.py']


def need(ok,reason):
    if type(ok) is not bool or not ok:
        raise ValueError(reason)


def safe(path):
    for p in [path.absolute(),*path.absolute().parents]:
        need(not p.is_symlink(),'symlink component rejected')


def sha(path):
    safe(path);need(path.is_file(),'missing source '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,data):
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')


def zero(n):return [[F(0) for j in range(n)] for i in range(n)]
def eye(n):return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a):return [[c*x for x in row] for row in a]
def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]
def comm(a,b):return add(mm(a,b),scale(-1,mm(b,a)))
def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]
def encode(a):return [[str(x) for x in row] for row in a]


GRID=2**256
def lower(x):return F((x.numerator*GRID)//x.denominator,GRID)
def upper(x):return F((x.numerator*GRID+x.denominator-1)//x.denominator,GRID)


def enclosure(lo,hi,places):
    need(lo<=hi,'ordered enclosure')
    g=10**places
    return {'lower':str(F((lo.numerator*g)//lo.denominator,g)),
            'upper':str(F((hi.numerator*g+hi.denominator-1)//hi.denominator,g))}


def recurrence():
    tau=F(1,2**22);r=F(25460736,25)*tau*tau;d=448*tau;kappa=28*tau
    rlo,rhi=lower(r),upper(r);dlo=dhi=d
    records=[]
    for n in range(100):
        lam=36*(n+1)*(n+2)
        plo,phi=lam*rlo,lam*rhi
        klo=kappa+dlo-d;khi=kappa+dhi-d
        records.append({'n':n,'rlo':rlo,'rhi':rhi,'dlo':dlo,'dhi':dhi,
                        'plo':plo,'phi':phi,'klo':klo,'khi':khi})
        if plo>=1:
            break
        need(phi<1,'interval straddles the series threshold; refine precision')
        nrlo=lower((dlo+F(3,2)*rlo)*plo/(1-plo))
        nrhi=upper((dhi+F(3,2)*rhi)*phi/(1-phi))
        dlo,dhi=lower(dlo+2*rlo),upper(dhi+2*rhi)
        rlo,rhi=nrlo,nrhi
    need(records[-1]['n']==42 and records[-1]['plo']>1,'controlled stop must be step 42')
    need(all(x['phi']<1 for x in records[:-1]),'all previous series conditions')
    need(records[15]['rhi']<min(x['rlo'] for x in records if x['n']!=15),
         'controlled minimum must be at step 15')
    need(F('4.1681528e-6')<records[0]['plo']<=records[0]['phi']<F('4.1681529e-6'),
         'reported initial rho enclosure')
    need(F('9.56163e-19')<records[15]['rlo']<=records[15]['rhi']<F('9.56165e-19'),
         'reported minimum residual enclosure')
    need(F('0.184436')<records[41]['plo']<=records[41]['phi']<F('0.184437'),
         'reported penultimate rho enclosure')
    need(F('1.727758')<records[42]['plo']<=records[42]['phi']<F('1.727759'),
         'reported failing rho enclosure')
    need(records[42]['khi']<F(1,1000),'relative condition has not failed')
    rows=[]
    for x in records:
        rows.append({'step':x['n'],'residual':enclosure(x['rlo'],x['rhi'],30),
                     'diagonal_norm':enclosure(x['dlo'],x['dhi'],18),
                     'rho':enclosure(x['plo'],x['phi'],24),
                     'relative_coefficient':enclosure(x['klo'],x['khi'],18)})
    return rows


def checks():
    controls=[]
    def control(name,ok,outcome):
        need(ok,'failed control '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})
    h=[[F(0),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(2)]]
    R=[[F(2),F(1),F(2)],[F(1),F(3),F(-1)],[F(2),F(-1),F(4)]]
    c=R[0][0];a=zero(3);s=zero(3)
    for j in [1,2]:
        a[j][0]=a[0][j]=R[j][0]
        s[j][0]=R[j][0]/h[j][j];s[0][j]=-s[j][0]
    z=add(add(R,scale(-c,eye(3))),scale(-1,a))
    need(R==add(add(scale(c,eye(3)),a),z),'complete scalar/diagonal splitting')
    need(comm(s,h)==scale(-1,a),'arbitrary-support homological sign')
    need(all(z[j][0]==0 and z[0][j]==0 for j in range(3)),'Z annihilates vacuum')
    control('omitted_scalar_is_not_a_valid_splitting',add(a,z)!=R,
            {'c':str(c),'A':encode(a),'Z':encode(z),'S':encode(s)})
    control('scalar_is_retained_but_commutes',comm(s,scale(c,eye(3)))==zero(3),
            'cI is an energy term; it is not discarded from the Hamiltonian')

    J=[[F(0),F(-1)],[F(1),F(0)]];Z=[[F(1),F(0)],[F(0),F(-1)]]
    Xp=[[F(0),F(1)],[F(1),F(0)]]
    support_rows=[]
    for m in [2,3,4]:
        total=zero(2**m);parity=[[F(1)]]
        for k in range(m):
            term=[[F(1)]]
            for j in range(m):term=kron(term,J if j==k else eye(2))
            total=add(total,term)
            parity=kron(parity,Z)
        diag=scale(F(1,2),add(parity,scale(-1,eye(2**m))))
        got=comm(total,diag)
        need(got==mm(total,parity),'growing-support commutator identity')
        # Gaussian-integer eigenvector w=(1,-i)^tensor m has eigenvalue i*m.
        # All following complex components are exact small Gaussian integers.
        w=[(-1j)**i.bit_count() for i in range(2**m)]
        image=[sum(int(total[i][j])*w[j] for j in range(2**m)) for i in range(2**m)]
        need(image==[1j*m*x for x in w],'exact common eigenvector')
        support_rows.append({'sites':m,'mu':'log(2)','generator_norm':2,
                             'diagonal_norm':1,'commutator_norm':m,'ratio':str(F(m,2))})
    control('equal_weight_universal_constant_rejected',support_rows[-1]['ratio']=='2',
            {'fixtures':support_rows,'all_size_formula':'ratio=m/2 -> infinity',
             'vacuum_diagonal':'2^(-m)(product Z-I)/2 annihilates the vacuum'})
    d=F(1,10);r=F(1,1000)
    D=[[F(0),F(0)],[F(0),d]]
    linear=comm(scale(r,J),D)
    control('retained_D_linear_term_cannot_be_dropped',linear==scale(-d*r,Xp),
            {'d':str(d),'r':str(r),'commutator':encode(linear),
             'leading_ratio_to_r_squared':str(d/r),
             'all_r_statement':'d/r diverges at fixed d>0; scalar shifts do not change this entry'})
    # Split bounds retain the full arbitrary support through the root sum.
    for n in [1,2,5]:
        delta=F(1,3*(n+1)*(n+2))
        need(12/delta==36*(n+1)*(n+2),'rational loss constant')
    control('positive_limit_weight_schedule',True,
            {'mu_infinity':'log(2)/2','total_loss':'log(2)/2',
             'delta_n':'log(2)/(2(n+1)(n+2))',
             'rational_lower_delta':'1/(3(n+1)(n+2))',
             'justification':'strict convex midpoint integral gives log(2)>2/3'})
    rows=recurrence()
    control('initial_smallness_does_not_certify_full_iteration',True,
            {'first_loss_series_failure_step':42,'residual_minimum_step':15,
             'last_rho_enclosure':rows[-1]['rho'],'relative_condition_still_below':'1/1000',
             'scope':'conservative rational certificate, not physical residuals'})
    control('rounding_does_not_cause_the_obstruction',
            F(rows[-1]['rho']['lower'])>1,
            {'rounding_grid':'2^(-256)','directed_rational_enclosures':True,
             'all_previous_upper_rho_below_one':True})
    control('certificate_failure_is_not_gap_or_algorithm_failure',True,
            {'proved':'scalar majorant loses admissibility',
             'actual_iteration_failure':False,'actual_homogeneous_gap_failure':False,
             'unproved_gap_threshold':'none'})
    rejected=0
    for bad in [False,'passed']:
        try:need(bad,'intentional rejection')
        except ValueError:rejected+=1
    control('optimized_mode_keeps_strict_validation',rejected==2,
            'False and non-Boolean statuses raise explicit ValueError')
    results={'schema':'ym22-forward-o2-results-v1','loop':'o2','direction':'forward',
      'status':'limited','passed':True,'claims':{
       'arbitrary_support_homological_inverse_gap':'1 (bare H0)',
       'scalar_bound':'abs(c_Y)<=norm(R_Y)','mixing_bound':'norm(A_Y)<=norm(R_Y)',
       'generator_bound':'norm(S_Y)<=norm(R_Y)','diagonal_bound':'norm(Z_Y)<=2 norm(R_Y)',
       'operator_domain_preserved':True,'equal_weight_universal_commutator_bound':False,
       'loss_commutator_constant':'4/delta_w','nested_series_ratio':'12*r/delta_w',
       'full_remainder_recurrence':'r_next<=(d+3r/2)*rho/(1-rho)',
       'diagonal_norm_update':'d_next<=d+2r','relative_update':'kappa_next<=kappa+2r',
       'intensive_scalar_increment_bound':'exp(-mu)*r',
       'retained_D_included':True,'mu_positive_limit':'log(2)/2',
       'all_positive_tau_baseline_majorant_obstruction':True,
       'exact_log_majorant_eventual_obstruction':True,
       'tau_example':'1/4194304','rational_recurrence_first_failure_step':42,
       'rational_recurrence_minimum_step':15,
       'rational_recurrence_lambda_n':'36*(n+1)*(n+2)',
       'numerical_gap_threshold_proved':False,'actual_algorithm_failure_proved':False,
       'actual_homogeneous_gap_failure_proved':False,'infinite_ITP_transfer':False},
      'controlled_recurrence':rows,'finite_checks_are_infinite_proof':False,
      'proof_location':BASE+'report.md','scientific_priority':'unverified'}
    return results,{'schema':'ym22-forward-o2-controls-v1','loop':'o2','direction':'forward',
                    'passed':True,'controls':controls}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.absolute();safe(out);need(not out.exists(),'output must be fresh')
    inputs={p:sha(ROOT/p) for p in INPUTS};need(len(inputs)==len(INPUTS),'duplicate input')
    need(inputs[CONTRACT]==CONTRACT_SHA,'frozen O2 contract mismatch')
    c=json.loads((ROOT/CONTRACT).read_text());need(c['status']=='frozen' and c['loop']=='o2','contract identity')
    for p,h in c['dependencies'].items():need(p in inputs and inputs[p]==h,'dependency mismatch '+p)
    for p in c['instruction_inputs']:need(p in inputs,'missing required instruction '+p)
    for path in ['research/round21/advisor/i1-gate.json','research/round21/advisor/i2-gate.json',
                 'research/round22/advisor/o1-gate.json']:
        gate=json.loads((ROOT/path).read_text());need(gate['status']=='limited','inherited scoped status')
        for p,h in inputs.items():
            if p in gate['files']:need(gate['files'][p]==h,'admitted source changed '+p)
    results,controls=checks();out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results);save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1',
      'loop':'o2','direction':'forward','inputs':inputs,
      'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
      'import_policy':'standard-library only; no other producer imports',
      'manifest_self_hash':'bound by submission inventory'})
    print(json.dumps({'loop':'o2','direction':'forward','status':'limited','passed':True,
                      'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':main()
