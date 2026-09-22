#!/usr/bin/env python3
"""Post-freeze AT6 every-row, actual-error, readout and provenance audit."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import argparse,csv,hashlib,importlib.util,json,sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run():
    checks=[]
    def need(value,name):
        if value is not True or name in checks:raise RuntimeError(name)
        checks.append(name)
    def rejected(call,name):
        try:call()
        except (ValueError,TypeError):pass
        else:raise RuntimeError(name)
        need(True,name)
    def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
    freeze=json.loads((HERE/'at6-independent-freeze.json').read_text())
    need(all(sha(ROOT/n)==h for n,h in freeze['files'].items()),'precomparison_independent_bytes_preserved')
    need(sha(ROOT/'research/round31/contracts/at6.json')==freeze['contract_sha256'],'independent_contract_unchanged')
    fwbase=ROOT/'research/round31/forward/at6'
    rvbase=ROOT/'research/round31/reverse/at6'
    sys.path.insert(0,str(fwbase))
    fw=load('at6_forward_review',fwbase/'check.py')
    sys.path.pop(0)
    rv=load('at6_reverse_review',rvbase/'check.py')
    replay=load('at6_replay_verification',HERE/'replay_loop.py')
    for name,base in [('forward',fwbase),('reverse',rvbase)]:
        replay.verify_freeze(base)
        need(True,name+'_complete_frozen_closure_and_shared_premises')
        inputs=list((base/'inputs').rglob('*'))
        need(all((ROOT/p.relative_to(base/'inputs')).is_file() and
                 p.read_bytes()==(ROOT/p.relative_to(base/'inputs')).read_bytes()
                 for p in inputs if p.is_file()),name+'_every_input_snapshot_matches_source')
        manifest=json.loads((base/'output/source-manifest.json').read_text())
        need(all(sha(base/n)==h for n,h in manifest['sources'].items()) and
             all(sha(base/'output'/n)==h for n,h in manifest['outputs'].items()),
             name+'_all_manifest_source_and_output_bindings')
    oldpath=ROOT/'research/round30/forward/at3/evaluator.py'
    need((fwbase/'historical_evaluator.py').read_bytes()==oldpath.read_bytes() and
         (rvbase/'inputs/research/round30/forward/at3/evaluator.py').read_bytes()==oldpath.read_bytes(),
         'both_historical_evaluator_copies_byte_identical')

    # Independent tighter reference recurrence; no producer arithmetic is used.
    G=10**60
    def down(x):return F(x.numerator*G//x.denominator,G)
    def up(x):return F(-((-x.numerator*G)//x.denominator),G)
    def exp_bounds(x):
        turns=0
        while x>F(1,2):x/=2;turns+=1
        term=partial=F(1)
        for j in range(1,71):term*=-x/j;partial+=term
        low=down(partial-term*x/71);high=up(partial)
        for j in range(turns):low,high=down(low*low),up(high*high)
        return low,high
    qlo,qhi=exp_bounds(F(3,32));plo=phi=F(1);reference=[]
    for j in range(4097):
        reference.append((plo/4,phi/4))
        if j<4096:plo,phi=down(plo*qlo),up(phi*qhi)
    # Independent Machin, integer-root and base-ten logarithm bounds.
    def atan_bounds(x,n=48):
        lo=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
        return lo,lo+x**(2*n+1)/F(2*n+1)
    def log_bounds(x,n):
        z=(x-1)/(x+1)
        lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
        return lo,lo+2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
    a,b=atan_bounds(F(1,5));c,d=atan_bounds(F(1,239))
    pi_low=16*a-4*d
    tau=F(1,10**14);T=F(128);H=F(1,32);L=F(10**9);eps=F(1,10**6)
    p=F(49,3)*tau;root=isqrt(p.numerator*G*G//p.denominator);Dhi=2*F(root+1,G)
    y=1+(L/T)**2
    log10=log_bounds(F(10),500);mantissa=log_bounds(y/10**13,300)
    loghi=13*log10[1]+mantissa[1]
    dynamic=F(49,4)*tau*T*loghi/pi_low
    fconstants=fw.constants();rpositive,rzero,rendpoint=rv.uniform_budget()
    fcost=fconstants['costs'];rcost=rendpoint['error_budget']
    need(fcost['state']>=Dhi and rcost['state_trace_norm_upper']>=Dhi,'both_outward_state_constants')
    need(fcost['centering']>=4*p and rcost['centering_mean_square_upper']>=4*p,'both_actual_mean_square_costs')
    need(fcost['real_time_comparison']>=dynamic and rcost['duhamel_inside_upper']>=dynamic,'both_outward_window_Duhamel_constants')
    need(fcost['Poisson_tail']>=(F(1,2)+Dhi/2)*2*T/(pi_low*L),'forward_full_effect_Poisson_tail')
    need(rcost['poisson_tail_upper']>=4*T/(pi_low*L),'reverse_full_conservative_Poisson_tail')
    need(fconstants['zero_time_error']==fconstants['D']/2+fconstants['D']**2 and
         rzero==rcost['state_trace_norm_upper']+rcost['centering_mean_square_upper'],
         'separate_zero_variance_bounds_retain_true_centering')
    need(exp_bounds(F(2))[0]>F(1,10) and L/T>4,'continuous_derivative_margin_independent')
    saved={name:json.loads((base/'output/results.json').read_text())
           for name,base in [('forward',fwbase),('reverse',rvbase)]}
    csvrows={}
    for name,base,filename in [('forward',fwbase,'aq-certified-grid.csv'),('reverse',rvbase,'aq-analytic-grid.csv')]:
        with (base/'output'/filename).open(newline='') as stream:raw=list(csv.DictReader(stream))
        rows=[{k:int(v) if k=='index' else F(v) for k,v in r.items()} for r in raw]
        csvrows[name]=rows
        need(len(rows)==4097,name+'_all_exported_nodes_present')
        for j,r in enumerate(rows):
            lo,hi=reference[j]
            arith=r['arithmetic_radius' if name=='forward' else 'reference_arithmetic_error']
            analytic=r['analytic_error' if name=='forward' else 'analytic_comparison_error']
            error=r['certified_actual_error' if name=='forward' else 'actual_correlation_error']
            expected=(fconstants['zero_time_error'] if j==0 else fconstants['uniform_positive_time_error']) if name=='forward' else (rzero if j==0 else rpositive)
            valid=(r['index']==j and r['s']==j*H and r['reference_lower']<=lo<=hi<=r['reference_upper']
                   and r['datum']==(r['reference_lower']+r['reference_upper'])/2
                   and arith==(r['reference_upper']-r['reference_lower'])/2
                   and analytic==expected and error==analytic+arith and F(0)<error<=eps)
            if name=='forward':valid=valid and r['tau']==tau and r['trapezoid_weight']==(H/2 if j in (0,4096) else H)
            else:valid=valid and r['actual_lower']==max(F(0),r['datum']-error) and r['actual_upper']==min(F(1),r['datum']+error)
            need(valid,name+'_complete_exact_node_'+str(j))
        need(rows[0]['datum']==F(1,4) and rows[-1]['reference_lower']==0 and rows[-1]['reference_upper']>0,name+'_zero_and_tiny_endpoint_semantics')

    frows=csvrows['forward'];rrows=csvrows['reverse']
    fproof=json.loads((fwbase/'output/input-provenance.json').read_text())
    rproof=saved['reverse']['provenance']
    oldf,secondf=fw.readout(frows,fproof)
    readoutr=rv.apply_readout(rrows,rproof,rpositive,rzero)
    need(fw.serial(oldf)==saved['forward']['historical_evaluator_output'] and
         fw.serial(secondf)==saved['forward']['endpoint_informed_actual_inverse_interval'],'forward_API_matches_frozen_readout')
    need(rv.serial(readoutr)==saved['reverse']['readout'] and
         rv.serial(readoutr)==json.loads((rvbase/'output/inverse-enclosures.json').read_text()),'reverse_API_and_separate_inverse_export_match')
    for name,rows,old,secondary in [('forward',frows,oldf,secondf),('reverse',rrows,readoutr['historical_evaluator_result'],None)]:
        trap=sum(((H/2 if j in (0,4096) else H)*r['datum'] for j,r in enumerate(rows)),F(0))
        Q=F(47,512000);J=T*eps;mass=old['tail_upper']
        error=rows[-1]['certified_actual_error' if name=='forward' else 'actual_correlation_error']
        endpoint=rows[-1]['datum']+error
        tail=min(mass,16*endpoint)
        primary=[old['lower'],old['upper']]
        actual_second=[secondary['lower'],secondary['upper']] if name=='forward' else list(readoutr['secondary_I_interval'])
        need(old['trap_lower']==old['trap_upper']==trap and old['arithmetic_trap_width']==0,name+'_every_weight_exact_bin_readout')
        need(old['quadrature_allowance']==Q and old['noise_allowance']==J and primary==[trap-Q-J,trap+mass+J],name+'_unchanged_primary_budget_and_sign')
        need(mass>=F(504,125)*exp_bounds(F(8))[1],name+'_outward_mass_tail_independent')
        need(actual_second==[max(F(0),trap-Q-J),trap+tail+J] and endpoint>rows[-1]['reference_upper'],name+'_complete_actual_endpoint_tail_readout')
        need(primary[1]-primary[0]<F(1,500) and actual_second[1]-actual_second[0]<F(1,2500),name+'_both_exact_width_targets')
        need(primary[0]<=F(1,12)<=primary[1] and actual_second[0]<=F(1,12)<=actual_second[1],name+'_free_inverse_not_resolved')
        need(old['conditional_on_sample_contract'] is True and old['computed_AQ_samples'] is False,name+'_historical_flags_preserved')
        need(sum(((H/2 if j in (0,4096) else H)*eps for j in range(4097)),F(0))==J and J/64<J,name+'_fully_correlated_error_requires_T_epsilon')
        need(trap+Q-J>F(1,12),name+'_wrong_quadrature_sign_excludes_free_truth')

    for name,rows,proof,call in [('forward',frows,fproof,lambda r,p:fw.readout(r,p)),
                               ('reverse',rrows,rproof,lambda r,p:rv.apply_readout(r,p,rpositive,rzero))]:
        rejected(lambda:call(rows,None),name+'_reject_missing_provenance')
        bad=dict(proof);bad['tau']='1/100000000'
        rejected(lambda:call(rows,bad),name+'_reject_changed_coupling_provenance')
        rejected(lambda:call(rows[:-1],proof),name+'_reject_missing_endpoint')
        badrows=[dict(r) for r in rows];badrows[1]['datum']+=F(1,100)
        rejected(lambda:call(badrows,proof),name+'_reject_modified_exact_datum')
        badrows=[dict(r) for r in rows];badrows[0]['s']=F(1,32)
        rejected(lambda:call(badrows,proof),name+'_reject_clock_change')
        badrows=[dict(r) for r in rows]
        badrows[-1]['certified_actual_error' if name=='forward' else 'actual_correlation_error']=F(0)
        rejected(lambda:call(badrows,proof),name+'_reject_deleted_endpoint_actual_error')
    zero_const=dict(fconstants);zero_const['zero_time_error']=zero_const['uniform_positive_time_error']=F(0)
    rejected(lambda:fw.readout(fw.generate_rows(zero_const),fproof),'forward_reject_coherently_regenerated_zero_budget')
    rejected(lambda:rv.apply_readout(rv.generate_rows(F(0),F(0)),rproof,F(0),F(0)),'reverse_reject_coherently_regenerated_zero_budget')
    rejected(lambda:rv.endpoint_tail(F(1,100),gap=F(0),centered=True),'reverse_reject_zero_gap_tail')
    rejected(lambda:rv.endpoint_tail(F(1,100),centered=False),'reverse_reject_uncentered_tail')
    rejected(lambda:fw.validate_control_measure([(F(1,4),F(0))]),'forward_reject_zero_energy_measure')
    # The pre-comparison slow control also retains the free mass and first moment.
    atoms=[(F(1,8),F(1,16)),(F(1,8),F(95,16))]
    moments=[sum((w*x**j for w,x in atoms),F(0)) for j in range(3)]
    need(moments[:2]==[F(1,4),F(3,4)] and moments[2]<36+98*tau and
         2*exp_bounds(F(8))[0]>F(47,512000)+T*eps,'valid_equal_first_moment_slow_control_rejects_deleted_tail')
    need(F(7)*F(1,12)/F(5)/F(7)==F(1,12)/F(5),'physical_time_integral_is_hbar_R_and_R_is_I_over_alpha')
    return {'schema':'hnm-r31-skeptic-api-audit-v1','loop':'AT6','passed':True,
            'checks_count':len(checks),'checks':checks,'exported_nodes_audited':8194,
            'scope':'Frozen actual-state analytic proxies, exact readouts and controls; no extra research loop'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    result=run();(output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':result['checks_count'],'nodes':result['exported_nodes_audited']}))
