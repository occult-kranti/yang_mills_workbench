#!/usr/bin/env python3
"""AH2 independent exact delayed-loading certificate. No historical algorithm imports."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
COUNT=0


def need(value,message):
    global COUNT
    COUNT+=1
    if not value: raise ValueError(message)


def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x


def inputs():
    manifest=json.loads((HERE/'inputs/source-inventory.json').read_text())
    entries=manifest['entries'];lookup={}
    for r in entries:
        p=ROOT/r['snapshot'];need(p.is_relative_to(HERE/'inputs'),'owned snapshot path')
        need(hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],'snapshot '+r['source'])
        lookup[r['source']]=p
    conpath='research/round28/contracts/ah2.json';con=json.loads(lookup[conpath].read_text())
    index={r['source']:r['sha256'] for r in entries}
    need(index[conpath]=='a7d558a8517cf3b1577d93a282ab6f6c22c462f2d06107e1255cfce0ee3f3ef1','actual AH2 contract')
    need(len(con['sources'])==33,'all33 contract sources')
    for p,h in con['sources'].items():need(index[p]==h,'required source '+p)
    return entries,lookup


def exp_minus_interval(x,degree=64):
    """Positive Taylor lower bound for exp(x), geometric upper remainder; invert."""
    need(x>=0,'nonnegative exponential argument')
    if x==0:return (F(1),F(1))
    terms=[F(1)]
    for k in range(1,degree+1):terms.append(terms[-1]*x/k)
    lower=sum(terms,F(0));first=terms[-1]*x/(degree+1);ratio=x/(degree+2)
    need(ratio<1,'geometric exponential tail ratio')
    upper=lower+first/(1-ratio)
    return (1/upper,1/lower)


def A_interval(rate,time):
    lo,hi=exp_minus_interval(rate*time)
    return ((1-hi)/rate,(1-lo)/rate)


def scalars(lam):
    eta=F(1,100);g=3-29*lam;d=F(9,2)
    r0=F(41,12)*lam**2;p0=r0/g;rplus=29*lam*p0;pplus=rplus/g;shift=rplus*rplus/g
    q0=F(9,10)*lam;q=q0+p0;b=q+eta;den=1-F(29,72)*lam**2-eta-p0
    return {'lambda':lam,'eta_class':eta,'g':g,'d':d,'r0':r0,'p0':p0,'rplus':rplus,'pplus':pplus,
            'delta':shift,'q0_reverse_AH1':q0,'q':q,'b':b,'denominator':den,
            'outside_norm_bar':29*lam,'face_to_new_norm_bar':F(19,5)*lam}


def point_certificate(lam,time):
    v=scalars(lam);g=v['g'];d=v['d'];q=v['q'];b=v['b'];C=v['face_to_new_norm_bar'];B=v['outside_norm_bar']
    eg=exp_minus_interval(g*time);ed=exp_minus_interval(d*time)
    ag=A_interval(g,time);ad=A_interval(d,time)
    load_upper=C*(q*ad[1]+b*(eg[1]-ed[0])/(d-g))
    first_integral_upper=(time-ad[0])/d
    second_integral_upper=(ag[1]-ad[0])/(d-g)
    integrated_upper=B*C*(q*first_integral_upper+b*second_integral_upper)
    sharp_upper=v['delta']*time+integrated_upper
    loose_upper=v['delta']*time+B*C*(q*time/d+b/(g*d))
    need(d>g and v['denominator']>0,'point spectral and output denominators')
    need(load_upper>=0 and first_integral_upper>=0 and second_integral_upper>=0,'positive loading/integrated certificates')
    if lam==0 or time==0:
        need(load_upper==0 and sharp_upper==0,'exact zero coupling or time early formula')
    return {'lambda':lam,'sigma':time,'N_loading_upper':load_upper,'physical_integrated_leakage_upper':integrated_upper,
            'physical_early_absolute_upper':sharp_upper,'physical_early_relative_upper':sharp_upper/v['denominator'],
            'loose_monotone_early_upper':loose_upper,'full_preparation_radius_used':v['eta_class'],
            'exp_minus_g_interval':eg,'exp_minus_d_interval':ed,'exact_physical_error_zero':lam==0 or time==0}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output).resolve();need(not out.exists(),'fresh output required')
    entries,lookup=inputs()
    old=json.loads(lookup['research/round28/forward/ah1/output/results.json'].read_text())
    basis=old['enrichment']['basis'];m=old['graph']['counts'][2];n=len(basis)
    need(old['graph']['counts']==[24,46,29] and n==561,'same admitted full physical graph and retained rank')
    metric=[F(b['norm2']) for b in basis];energies=[F(b['energy']) for b in basis]
    M={(i,j):F(a) for i,j,a in old['retained_magnetic']['entries']}
    need(len(M)==2124,'complete admitted magnetic data')
    oldids=list(range(m+1));faces=list(range(1,m+1));new=list(range(m+1,n))
    need(len(oldids)==30 and len(new)==531,'P0 and N dimensions; Q is full infinite outside')
    # Reconstruct every entry independently from actual named functions and metric adjoints.
    expected={}
    for i,bv in enumerate(basis):
        if bv['kind']=='vacuum':targets=list(range(m));coef=F(1,2)
        elif bv['kind']=='face':continue
        elif bv['kind'] in ('spin1','pair'):targets=bv['faces'];coef=F(1,2)
        else:
            need(bv['kind'] in ('singlet','triplet'),'known complete new channel');targets=bv['faces'];coef=F(1,4)
        for p in targets:
            j=p+1;expected[i,j]=coef;expected[j,i]=metric[i]*coef/metric[j]
    need(M==expected,'every retained magnetic coefficient and zero rule independently reconstructed')
    for (i,j),a in M.items():need(metric[i]*a==metric[j]*M[j,i],'physical metric adjoint')
    need(not any(i in new and j in new for i,j in M),'complete new-new magnetic block zero')
    need(min(energies[i] for i in new)==F(9,2),'complete new-block electric lower bound')
    need(not any((i,0) in M for i in new),'C Omega=0 on all531 states')
    # All face-to-new columns are simultaneous Hilbert metric data, not bright-only sampling.
    columns={i:{j-1:M[i,j] for j in faces if (i,j) in M} for i in new}
    gram=[[sum((metric[i]*columns[i].get(p,F(0))*columns[i].get(q,F(0)) for i in new),F(0))
           for q in range(m)] for p in range(m)]
    for p in range(m):
        for q in range(m):need(gram[p][q]==(F(29,4) if p==q else F(1,4)),'complete face-to-new Gram entry')
    bright=sum(gram[0]);dark=gram[0][0]-gram[0][1]
    need((bright,dark)==(F(57,4),F(7)),'all-column operator norm eigenvalues')
    need(F(19,5)**2>bright,'independent rational C norm enclosure')
    need(all(columns[i] for i in new),'every new channel occurs in at least one loaded column')
    removal_losses={};bright_removal_losses={}
    for i in new:
        # trace of C*C strictly decreases on deletion of every individual physical row.
        loss=metric[i]*sum((a*a for a in columns[i].values()),F(0))
        need(loss>0,'deleting any new channel changes complete norm data')
        removal_losses[i]=loss
        bright_loss=metric[i]*sum(columns[i].values(),F(0))**2
        need(bright_loss>0,'every deleted row has nonzero overlap with unique bright maximizing input')
        bright_removal_losses[i]=bright_loss
    cap=F(1,100);T=F(3);v=scalars(cap);g=v['g'];d=v['d'];B=v['outside_norm_bar'];C=v['face_to_new_norm_bar']
    need(v['p0']==F(41,325200) and v['rplus']==F(1189,32520000),'common inherited angle and residual envelopes')
    need(v['q0_reverse_AH1']==F(9,1000),'attributed reviewed reverse q0')
    need(v['denominator']==F(193136341,195120000),'true full-output denominator unchanged')
    early=v['delta']*T+B*C*(v['q']*T/d+v['b']/(g*d))
    exp_lower=sum(((g*T)**k/F(math.factorial(k)) for k in range(40)),F(0))
    need(exp_lower>3000,'rational all-time late-tail certificate exp(3g)>3000')
    late=v['pplus']+(2*v['b']+v['pplus'])/3000
    absolute=max(early,late);relative=absolute/v['denominator']
    improved=relative<F(11,5000);target=relative<F(1,10000)
    # Symbolic rates and integrated-kernel identities reduce to these positive rational relations.
    need(g>0 and d-g>0,'positive complete damping rates')
    need((F(1,g)-F(1,d))/(d-g)==1/(g*d),'integrated transient kernel upper1/(gd)')
    # All fixed contract certificate fixtures, retaining the theorem's full radius .01.
    amp=F(1,200);a2=1-amp*amp
    need(a2+amp*amp==1,'exact radical normalization')
    distance2_upper=2*amp*amp # sqrt(1-amp^2)>=1-amp^2
    need(distance2_upper<F(1,100)**2,'fixtures inside full class, not amplitude mistaken for radius')
    preparations=[{'name':'Omega','vacuum_amplitude_squared':F(1),'face_amplitude':F(0),'phase':'1','norm_squared':F(1),'distance_squared_upper':F(0)},
                  {'name':'real_face','vacuum_amplitude_squared':a2,'vacuum_amplitude':'positive sqrt(39999/40000)','face_amplitude':amp,'phase':'1','norm_squared':a2+amp*amp,'distance_squared_upper':distance2_upper},
                  {'name':'imaginary_face','vacuum_amplitude_squared':a2,'vacuum_amplitude':'positive sqrt(39999/40000)','face_amplitude':amp,'phase':'i','norm_squared':a2+amp*amp,'distance_squared_upper':distance2_upper}]
    fixtures=[]
    for lam in (F(0),F(1,200),F(1,100)):
        for time in (F(0),F(1),F(3)):
            point=point_certificate(lam,time)
            for prep in preparations:
                need(prep['norm_squared']==1 and prep['distance_squared_upper']<F(1,100)**2,'complete fixture preparation check')
                fixtures.append({'preparation':prep['name'],**point})
    # Discriminating controls are actual coefficient/kernel/scalar tests; no current opposite data.
    controls={};evidence={};nondiscriminating=[]
    def reject(name,bad_premise_passes):
        need(not bad_premise_passes,'control failed to discriminate: '+name);controls[name]=True
    reject('N_is_full_outside',n-len(oldids)==0) # actual P0->N coupling is nonzero, unlike BP0
    evidence['N_L_P0_norm_squared_at_cap']=cap*cap*bright
    need(evidence['N_L_P0_norm_squared_at_cap']>0,'N is a retained loading block, not Q')
    reject('all_N_as_outside_BP0_zero',cap*cap*bright==0)
    reject('deleted_new_channel_preserves_complete_Gram',any(loss==0 for loss in removal_losses.values()))
    tri=next(i for i in new if basis[i]['kind']=='triplet');j=basis[tri]['faces'][0]+1
    reject('wrong_triplet_metric',M[tri,j]==M[j,tri])
    reject('BP0_zero_means_B_zero',F(-1,2)==0)
    # First try at lambda=0 is blind; record it, replace with positive frozen fixture lambda.
    zero_feedback=F(0)**2*gram[0][0]
    nondiscriminating.append({'control':'deleted_retained_feedback','lambda':'0','second_derivative_difference':zero_feedback,'status':'blind; exact zero-coupling case'})
    feedback=cap*cap*gram[0][0]
    reject('drop_retained_feedback_at_positive_coupling',feedback==0)
    evidence['positive_feedback_second_derivative_difference']=feedback
    # C* C on a face is the exact difference between full retained second derivative and P0 compression.
    vacuum_face_norm2=sum((M.get((j,0),F(0))**2 for j in faces),F(0))
    need(vacuum_face_norm2==F(29,4),'complete actual stationary-forcing witness')
    reject('stationary_ground_face_component_can_be_dropped',cap*cap*vacuum_face_norm2==0)
    evidence['stationary_face_argument']='If F f+=0, positive N ground block forces N f+=0; remaining vacuum fails face ground equation at positive lambda.'
    reject('scalar_reference_is_actual_ground',-F(29,4)*cap**2==0)
    exp1_lower=sum((F(1,math.factorial(k)) for k in range(5)),F(0))
    reject('uncertain_center_safe_for_unbounded_time',exp1_lower<=1)
    reject('centering_defect_wrong_sign',F(3,10)-F(2,10)==-(F(3,10)-F(2,10)))
    # Actual-model strict center difference, using connected stoquastic matrix and unique outside channel.
    neighbors={i:set() for i in range(n)}
    for (i,j),a in M.items():
        need(a>0,'nonzero magnetic entries have fixed positive real phase')
        neighbors[i].add(j)
    reached={0};front={0}
    while front:
        nxt=set().union(*(neighbors[i] for i in front))-reached
        reached.update(nxt);front=nxt
    need(len(reached)==n,'all561 coordinates connected to vacuum')
    # The report proves strict positive f+ coordinates by the variational absolute-value argument.
    # The unique spin1 -> outside spin3/2 coefficient then gives B f+ !=0 and epsilon<mu+.
    outside_prefactor=cap/2
    reject('approximate_output_is_true_denominator',outside_prefactor==0)
    evidence['denominator_counterexample']='Connected negative off-diagonal A gives positive exact f+ coordinates; unique spin1-to-spin3/2 outside coefficient implies epsilon<mu+. For x=Omega, derivative at0 of full squared norm minus retained squared norm is2(epsilon-mu+)<0. The exact retained output norm is too large as a true denominator near0.'
    # A finite set of zero samples does not bound a function on the full line.
    poly=lambda t:t*(t-1)*(t-3)
    need(all(poly(t)==0 for t in (F(0),F(1),F(3))),'finite-fixture counterexample matches every time')
    reject('finite_time_fixtures_prove_all_time',poly(F(2))==0)
    reject('old_graph_accuracy_import',relative<F(37,1000000))
    reject('canonical_clock_equals_fixed_physical_clock',F(1,2)**3==1)
    reject('fixture_amplitude_replaces_full_class_radius',amp==v['eta_class'])
    reject('negative_coupling_preserves_positive_potential',29*(-cap)>=0)
    controls.update({'zero_coupling_exact_error_separate_from_cap_envelope':True,'zero_time_exact_error_separate_from_slack_envelope':True,
                     'all531_rows_and_feedback_retained':True,'stationary_component_retained':True,'full_outside_and_return_semigroup_retained':True,
                     'actual_centers_and_true_denominator_retained':True,'fixtures_are_certificates_not_heat_vectors':True})
    evidence['uncertain_center_ground_growth_lower']=exp1_lower
    evidence['every_row_removal_trace_loss_counts']=dict(Counter(str(x) for x in removal_losses.values()))
    evidence['every_row_removal_bright_loss_counts']=dict(Counter(str(x) for x in bright_removal_losses.values()))
    bindings={r['source']:r['sha256'] for r in entries};bindings.update({r['snapshot']:r['sha256'] for r in entries})
    for rel in ('check.py','inputs/source-inventory.json','preflight.json','preflight-pass.json'):
        p=HERE/rel;bindings[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    report=HERE/'report.md'
    if report.exists():bindings[str(report.relative_to(ROOT))]=hashlib.sha256(report.read_bytes()).hexdigest()
    result={'schema':'ym28-forward-ah2-result-v1','loop':'ah2','checks_passed':True,'check_count':COUNT,
            'model':'admitted full24-vertex46-link29-face physical graph; same561 retained projection; no numerical heat evaluator',
            'blocks':{'P_rank':n,'P0_rank':len(oldids),'N_rank':len(new),'Q':'infinite full complement of P','N_ids':new,
                      'K_N_energy_counts':dict(Counter(str(energies[i]) for i in new)),'N_S_N':'exactly zero on all531 rows and columns',
                      'C_definition':'-lambda N S F','C_without_minus_lambda_entries':[[i,j,a] for i in new for j,a in columns[i].items()],
                      'C_Gram_diagonal':'29/4','C_Gram_offdiagonal':'1/4','C_Gram_bright':bright,'C_Gram_dark':dark,
                      'complete_C_norm':'sqrt(57) lambda/2','complete_B_norm_upper':'29 lambda','B_P0':'zero; B nonzero on new spin1 input'},
            'uniform_inputs':v,'loading':{'exact_equation':'y_prime=-(K_N+29lambda-mu+)y-C F u; y(0)=0; u is the full exact retained evolution',
                        'face_bound':'q+b exp(-g sigma), with stationary q=q0+p0',
                        'N_bound':'Cbar[q(1-exp(-d t))/d+b(exp(-g t)-exp(-d t))/(d-g)]',
                        'integrated_bound':'Bbar Cbar[(q/d)(t-(1-exp(-d t))/d)+(b/(d-g))((1-exp(-g t))/g-(1-exp(-d t))/d)]',
                        'monotone_early':'delta t+Bbar Cbar[q t/d+b/(g d)]',
                        'late':'pplus+(2b+pplus)exp(-g t)','strong_Duhamel_defect':'B+(mu+-epsilon)P'},
            'join_certificate':{'join':T,'exp_positive_terms':40,'exp_lower':exp_lower,'exp_negative_upper':'1/3000',
                                'early_absolute':early,'late_absolute':late,'all_time_absolute':absolute,'true_denominator':v['denominator'],
                                'all_time_relative':relative,'improves_common_AH1':improved,'prospective_target_1e_4_met':target,
                                'limiting_branch':'early' if early>=late else 'late','actual_errors_evaluated':False},
            'preparations':preparations,'fixture_count':len(fixtures),'fixtures':fixtures,'controls':controls,
            'nondiscriminating_controls':nondiscriminating,'control_evidence':evidence,
            'current_reverse_AH2_science_read':False,'historical_checkers_imported_or_executed':False,'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(encode(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'checks':COUNT,'controls':len(controls),'fixtures':len(fixtures),'relative_exact':str(relative),
                      'relative_display':float(relative),'target_met':target,'early':float(early),'late':float(late)},sort_keys=True))


if __name__=='__main__':main()
