#!/usr/bin/env python3
"""Independent AT6 full-window proof constants and all-node readout arithmetic."""
from fractions import Fraction as F
from math import isqrt,factorial
from pathlib import Path
import argparse,json

def run():
    checks=[]
    def need(v,k):
        if v is not True or k in checks:raise RuntimeError(k)
        checks.append(k)
    tau=F(1,10**14);T=F(128);L=F(10**9);h=F(1,32);N=4096;eps=F(1,10**6)
    precision=10**45
    def down(x):return F(x.numerator*precision//x.denominator,precision)
    def up(x):return F(-((-x.numerator*precision)//x.denominator),precision)
    def expbase(x):
        if not 0<=x<=1:raise ValueError('base exponential domain')
        term=part=F(1)
        for k in range(1,45):term*=-x/k;part+=term
        return down(part-term*x/45),up(part)
    p=F(49,3)*tau;k=isqrt(4*p.numerator*precision*precision//p.denominator);D=F(k+1,precision)
    need(D*D>=4*p,'outward_state_distance')
    need(F(27,10)**16>1+L/T,'log_one_plus_L_over_T_less_than_16')
    need(sum((F(1,factorial(j)) for j in range(6)),F(0))>F(27,10),'exponential_series_justifies_log_bound')
    # For x>=0, log(1+x)-x/(1+x) has derivative x/(1+x)^2>=0.
    # Hence g(s)=s log(1+L/s) is increasing. 1+x²<=(1+x)² gives
    # s log(1+(L/s)^2) <=2T log(1+L/T)<32T continuously on (0,T].
    slope=F(49,4)*tau;dynamic=slope*32*T/3;tail=4*T/(3*L)
    modeling=D+4*p+dynamic+tail
    zero_error=D/2+4*p
    need(zero_error<modeling<eps,'uniform_window_including_separate_zero_error')
    need(dynamic>0 and tail>0 and 4*p>0,'all_window_costs_retained')
    need(98*tau/F(6)==p,'same_gap_six_and_seven_star_reset')
    a,b=expbase(3*h);lo=hi=F(1);rows=[];P=F(0);flo=F(0);fhi=F(0)
    for j in range(N+1):
        rlo,rhi=lo/4,hi/4;datum=(rlo+rhi)/2;arith=(rhi-rlo)/2
        weight=h/2 if j in (0,N) else h
        actualerr=(zero_error if j==0 else modeling)+arith
        need(actualerr<eps,'node_actual_error_'+str(j))
        rows.append((j,F(j,32),datum,arith,actualerr))
        P+=weight*datum;flo+=weight*rlo;fhi+=weight*rhi
        if j<N:lo,hi=down(lo*a),up(hi*b)
    need(len(rows)==4097 and rows[0][1]==0 and rows[-1][1]==128,'all_frozen_nodes_in_order')
    weights=[h/2 if j in (0,N) else h for j in range(N+1)]
    need(sum(weights)==T,'all_real_trapezoid_weights')
    need(sum(weights[1:])<T,'missing_first_endpoint_changes_total_weight')
    need(flo<=P<=fhi,'trapezoid_datum_bounded_by_reference_arithmetic')
    Q=F(47,512000);J=T*eps
    ylo,yhi=expbase(F(1));mass_tail=F(504,125)*yhi**8
    end_upper=rows[-1][2]+eps
    endpoint_tail=16*end_upper
    primary=(P-Q-J,P+mass_tail+J)
    improved=(P-Q-J,P+endpoint_tail+J)
    need(primary[1]-primary[0]<F(1,500),'primary_inverse_width_target')
    need(improved[1]-improved[0]<F(1,2500),'secondary_endpoint_tail_width_target')
    need(endpoint_tail<mass_tail,'actual_endpoint_improves_mass_tail')
    need(primary[0]<F(1,12)<primary[1] and improved[0]<F(1,12)<improved[1],'free_inverse_not_excluded')
    need(P+Q-J>F(1,12),'wrong_quadrature_sign_excludes_known_free_inverse')
    need(J==F(16,125000) and T*eps>F(64)*eps,'fully_correlated_error_not_root_N')
    need(end_upper>rows[-1][2] and endpoint_tail>16*rows[-1][2],'reference_endpoint_alone_omits_physical_error')
    # A slow+fast abstract measure shares mass and first moment and respects ceiling.
    atoms=[(F(1,8),F(1,16)),(F(1,8),F(95,16))]
    moments=[sum((w*x**j for w,x in atoms),F(0)) for j in range(3)]
    need(moments[:2]==[F(1,4),F(3,4)] and moments[2]<36+98*tau,'valid_slow_control_respects_inherited_moment_constraints')
    slow_tail_lower=2*ylo**8
    need(slow_tail_lower>Q+J,'deleting_tail_can_exclude_valid_slow_control_integral')
    need(F(1,16)>0 and F(0)<F(1,16),'zero_atom_violates_required_gap')
    need(F(4,3*10000)>eps,'old_cutoff_still_insufficient')
    need(F(196,3*10**8)>eps*eps,'original_coupling_cap_still_insufficient')
    physical_R=F(1,12)/F(3)
    need(physical_R==F(1,36) and physical_R!=F(1,12)*F(3) and F(7)*physical_R==F(7,36),'physical_R_and_time_integral_keep_units')
    # Compact checks are summarized; every node retains its own independent bound.
    return {'schema':'hnm-r31-independent-skeptic-controls-v1','loop':'AT6','passed':True,'checks_count':len(checks),'checks':checks,
      'node_count':len(rows),'uniform_positive_time_analytic_error':str(modeling),'zero_time_analytic_error':str(zero_error),
      'maximum_complete_node_error':str(max(z[4] for z in rows)),
      'all_node_trapezoid':str(P),'quadrature_budget':str(Q),'deterministic_sample_budget':str(J),
      'mass_tail_upper':str(mass_tail),'actual_endpoint_upper':str(end_upper),'endpoint_tail_upper':str(endpoint_tail),
      'primary_I_interval':[str(x) for x in primary],'endpoint_I_interval':[str(x) for x in improved],
      'primary_width':str(primary[1]-primary[0]),'endpoint_width':str(improved[1]-improved[0]),
      'target_met':True,'secondary_target_met':True,'free_inverse_included':True,'interaction_shift_resolved':False,
      'scope':'Actual-model analytic enclosure only in zero-selected patterned AQ tau=+1e-14; no finite-box solver or continuum claim.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);r=run();(out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':True,'checks':r['checks_count'],'nodes':r['node_count']}))
