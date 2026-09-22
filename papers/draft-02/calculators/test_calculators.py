#!/usr/bin/env python3
"""Executable arithmetic, diagnostic and invalid-model checks (not new proofs)."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import mpmath as mp

import ym_calculators as y


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('output/test-results.json'))
    args=p.parse_args()
    mp.mp.dps=70
    records=[]
    def check(name, condition, kind='exact arithmetic', detail=None):
        records.append({'name':name,'passed':bool(condition),'kind':kind,'detail':y.jsonable(detail)})
        if not condition:
            raise ArithmeticError(name)
    def close(name,a,b,tol=mp.mpf('1e-55')):
        check(name,abs(a-b)<tol,'high-precision diagnostic',{'difference':abs(a-b),'tolerance':tol})
    def rejects(name,fn):
        try:
            fn()
        except ValueError:
            check(name,True,'invalid-input rejection')
        else:
            check(name,False,'invalid-input rejection')

    for bad in [True,False,float('nan'),float('inf'),1.0,None]:
        rejects('exact input rejects '+repr(bad),lambda b=bad:y.exact(b))
    check('rational decimal is exact',y.exact('0.1')==F(1,10))
    check('rational input not binary float',y.exact('1/3')==F(1,3))
    for v in [F(0),F(2),F(1,100000),F(1234567,891011)]:
        up=y.sqrt_upper(v)
        check('sqrt enclosure '+str(v),(up-F(1,10**50))**2<v<=up**2 if v else up==0)

    j=y.jacobi('0','7/3',8)
    close('Jacobi uncoupled ground',j['E0'],mp.mpf(0))
    close('Jacobi uncoupled gap=3alpha',j['gap'],mp.mpf(7))
    j1,j2=y.jacobi('2','1',16),y.jacobi('2','3',16)
    close('Jacobi units scale energies',j2['gap'],3*j1['gap'])
    fine=y.jacobi('10','1',32)
    coarse=y.jacobi('10','1',16)
    close('Jacobi N16/N32 gap comparison (not tail certificate)',fine['gap'],coarse['gap'],mp.mpf('1e-20'))
    check('finite Ritz first level min-max direction',fine['E0']<=coarse['E0'],'high-precision diagnostic')
    check('outside certified coupling window has no inherited floor',y.jacobi('11',dimension=8)['source_exact_gap_floor_over_alpha'] is None,'scope control')
    for name,fn in [('negative ratio',lambda:y.jacobi('-1')),('zero alpha',lambda:y.jacobi(alpha=0)),('Boolean dimension',lambda:y.jacobi(dimension=True)),('too small dimension',lambda:y.jacobi(dimension=1))]:
        rejects('Jacobi '+name,fn)

    for k in ['-5','-1','0','1/100000000','1','5']:
        s=y.static_response(k,6)
        close('static Bessel/integral mean k='+k,s['mean_Bessel'],s['moments_quadrature'][1])
        check('positive variance k='+k,s['variance_quadrature']>0,'high-precision diagnostic')
        for n,res in enumerate(s['Haar_identity_residuals']):
            close('static Haar identity n='+str(n)+' k='+k,res,mp.mpf(0))
    zero=y.static_response('0',8)
    for n,m in enumerate(zero['moments_quadrature']):
        close('Haar Catalan moment '+str(n),m,y.real(y.haar_moment(n)))
    pos,neg=y.static_response('2',4),y.static_response('-2',4)
    close('static odd reflection',pos['mean_Bessel'],-neg['mean_Bessel'])
    close('static even variance',pos['variance_quadrature'],neg['variance_quadrature'])
    coeff=y.scalar_series()
    check('response first four exact coefficients',list(coeff['coefficients_by_power'].values())==[F(1,4),-F(1,96),F(1,1536),-F(1,23040)])
    check('launch certificate is below 3e-24',0<coeff['analytic_launch_error_upper']<F(3,10**24))
    true=y.static_response('1/100',2)['mean_Bessel']
    check('launch actual diagnostic inside analytic bound',abs(true-y.real(coeff['polynomial_value']))<=y.real(coeff['analytic_launch_error_upper']),'high-precision diagnostic')
    k,u=F(9,8),F(1,3)
    check('wrong point closure passes first identity',3*u==k*(1-u*u),'wrong-model control')
    check('wrong point closure fails next identity',1-4*u*u+k*(u-u**3)==F(8,9),'wrong-model control')
    check('dropping variance changes origin slope',F(1,3)!=F(1,4),'wrong-model control')
    rejects('singular launch epsilon zero',lambda:y.scalar_series(epsilon=0))
    rejects('series even degree',lambda:y.scalar_series(degree=6))
    rejects('static NaN',lambda:y.static_response('nan'))

    for L,q in [(1,F(1,2)),(2,F(2,3)),(3,F(4,5))]:
        # Independently count actual anchored omitted faces, rather than reuse factorization.
        enumerated=F(0)
        count=0
        for x in range(4*L):
            for yy in range(2*L):
                for z in range(L):
                    faces=2 if yy%2==0 and x%4 in [0,1,2] else 3
                    count+=faces
                    enumerated+=faces*q**(x+yy+z)/24
        closed=y.profile(q)*(1-q**(4*L))*(1-q**(2*L))*(1-q**L)
        check('tail-cube exact face sum L='+str(L),enumerated==closed)
        check('tail-cube face count L='+str(L),count==21*L**3)
    w=y.window_budget('999/1000',L=None,ell='5/2',beta=0,gamma='2')
    check('beta zero uses floor ell',w['L']==2,'boundary control')
    w2=y.window_budget('999/1000',L=None,beta='1/2',gamma='3/2')
    check('critical support-time line not admitted as vanishing',not w2['asymptotic_vanishing_certificate'],'boundary control')
    w3=y.window_budget('999/1000',L=None,beta='1',gamma='0')
    check('beta=1 fails vanishing certificate at fixed time',not w3['asymptotic_vanishing_certificate'],'boundary control')
    check('finite budget differs from infinite budget',w['P_L']<1,'wrong-model control')
    for name,fn in [('q=1',lambda:y.window_budget(q=1)),('q=0',lambda:y.window_budget(q=0)),('eta=1',lambda:y.window_budget(eta=1)),('negative gamma',lambda:y.window_budget(gamma=-1)),('zero L',lambda:y.window_budget(L=0)),('Boolean L',lambda:y.window_budget(L=True))]:
        rejects('window '+name,fn)

    g=y.filter_budget()
    check('AB2 exact rational residual budget',g['operator_residual_over_r_rational_upper']==F(626,1629))
    check('AB2 target margin',g['operator_residual_over_r_rational_upper']<F(77,200))
    tr=y.filter_budget('triangle','1/1000','3')
    check('AE2 exact rational residual budget',tr['operator_residual_over_r_rational_upper']==F(2072,2997))
    check('AE2 exact radius',tr['weight2']['radius_parameter_192MT']==F(72,125))
    check('AE2 rooted envelope',tr['weight2']['rooted_weight2_residual_over_rstar_upper']==64*F(125,53)**3)
    check('AE2 norm finiteness is not weighted contraction',not tr['weight2']['weighted_contraction_proved'],'scope control')
    for kind in ['gaussian','triangle']:
        origin=y.filter_budget(kind,'1/1000','3',0)
        check(kind+' zero-frequency residual remains one',origin['spectral_residual_multiplier']==1,'boundary control')
        check(kind+' zero-frequency inverse vanishes',origin['spectral_inverse_multiplier']==0,'boundary control')
        for omega in ['-2','-1/10','1/10','2']:
            f=y.filter_budget(kind,'1/1000','3',omega)
            close(kind+' commutator sign '+omega,-y.real(omega)*f['spectral_inverse_multiplier'],-1+f['spectral_residual_multiplier'])
    endpoint=y.filter_budget('triangle','1/1000','125/24')
    check('triangle radius endpoint residual certificate fails',not endpoint['weight2']['residual_series_finite_certificate'],'boundary control')
    check('triangle radius endpoint inverse finiteness separate',endpoint['weight2']['inverse_series_at_endpoint_finite'],'boundary control')
    threshold=y.filter_budget('triangle','1/409','3')
    check('409M=1 has no simultaneous open interval',not threshold['weight2']['simultaneous_open_duration_interval_exists'],'boundary control')
    original=y.filter_budget('triangle','35/1664','3')
    check('original cap has disjoint certificate durations',original['weight2']['contraction_lower_duration']>original['weight2']['cardinality_upper_duration'],'wrong-model control')
    check('zero source omits undefined ratio',y.filter_budget(M=0)['operator_residual_over_r_rational_upper'] is None,'boundary control')
    for name,fn in [('negative duration',lambda:y.filter_budget(duration=-1)),('outside cap',lambda:y.filter_budget(M='1/10')),('negative M',lambda:y.filter_budget(M=-1))]:
        rejects('filter '+name,fn)

    w=y.wilson()
    th=w['theta']
    check('Wilson exact quadratic bounds at admitted cap',w['single_deficit_lower']<=w['single_deficit']<=w['single_deficit_upper'],'high-precision diagnostic')
    check('Wilson linear remainder diagnostic',abs(w['sum_F']-1-mp.j*th)<=2*th**2,'high-precision diagnostic')
    close('Wilson zero-clock single',y.wilson(0)['single_F'],mp.mpf(1))
    close('Wilson zero-clock sum',y.wilson(0)['sum_F'],mp.mpf(1))
    frequencies=[mp.mpf(0),mp.mpf(2),mp.mpf(-2),2*mp.sqrt(3),-2*mp.sqrt(3)]
    weights_x=[mp.mpf(2)/3,mp.mpf(1)/8,mp.mpf(1)/8,mp.mpf(1)/24,mp.mpf(1)/24]
    weights_s=[mp.mpf(1)/3,mp.mpf(3)/8,mp.mpf(1)/8,mp.mpf(1)/12+1/(8*mp.sqrt(3)),mp.mpf(1)/12-1/(8*mp.sqrt(3))]
    for name,weights,target in [('single',weights_x,w['adjacency_moments_single']),('sum',weights_s,w['adjacency_moments_sum'])]:
        for n,moment in enumerate(target):
            close('Wilson spectral moment '+name+' '+str(n),sum(a*x**n for a,x in zip(weights,frequencies)),mp.mpf(moment))
    check('single cosine fitted to second moment fails fourth',w['adjacency_moments_single'][4]!=w['adjacency_moments_single'][2]**2,'wrong-model control')
    check('single phase fitted to sum mean fails variance',w['adjacency_moments_sum'][2]!=w['adjacency_moments_sum'][1]**2,'wrong-model control')
    check('vacuum equality does not preserve full operator norms',w['operator_comparison']['rank']['norm_squared']!=w['operator_comparison']['sum']['norm_squared'],'wrong-model control')
    check('vacuum fourth moment discriminates rank/sum',w['operator_comparison']['rank']['vacuum_fourth_moment']!=w['operator_comparison']['sum']['vacuum_fourth_moment'],'wrong-model control')
    rejects('Wilson outside admitted clock range',lambda:y.wilson('1'))

    h=y.heat_certificates()
    check('AF1 rational exponential prefactor witness',y.exp_upper_positive(F(2,3))<2)
    check('AF2 early factor two has exact center margin',8*h['AF1']['center_radius']<F(1,2))
    check('AC2 true denominator',h['AC2']['denominator']==F(7127,7200))
    check('AC2 early exact arithmetic',h['AC2']['early_absolute']==F(457097,12600000000))
    check('AC2 late exact arithmetic',h['AC2']['late_absolute']==F(2441,78400000))
    check('AC2 all-time exact arithmetic',h['AC2']['all_time_physical_relative']==F(457097,12472250000))
    check('AF1 full relative target',h['AF1']['full_relative']<F(15,10**6))
    check('AF2 full relative target',h['AF2']['full_relative_total']<F(37,10**6))
    source=json.loads((y.HERE/'source_data/heat_scalar_inputs.json').read_text())
    for k,v in h['AF2'].items():
        check('AF2 matches pinned exact field '+k,v==F(source['af2_expected_errors'][k]))
    for k in ['center_heat','degree100_Taylor','export_rounding','full_relative']:
        check('AF1 matches pinned exact field '+k,h['AF1'][k]==F(source['af1_expected_errors'][k]))
    for t in ['0','1','8','1000']:
        check('heat lambda=0 exact physical cancellation t='+t,y.heat_envelopes(cap=0,sigma=t)['pointwise_relative_upper_numeric']==0,'boundary control')
    check('heat t=0 exact physical cancellation',y.heat_envelopes(sigma=0)['pointwise_relative_upper_numeric']==0,'boundary control')
    check('late coarse bound at time zero is not exact error',y.heat_envelopes(sigma=0)['late_absolute_numeric']>0,'wrong-model control')
    h1,h2=y.heat_envelopes(sigma='1'),y.heat_envelopes(sigma='5')
    check('early increases and late decreases (sample diagnostic)',h1['early_absolute_numeric']<h2['early_absolute_numeric'] and h1['late_absolute_numeric']>h2['late_absolute_numeric'],'high-precision diagnostic')
    check('physical omission exceeds numerical budget',h['AC2']['all_time_physical_relative']>h['AF2']['numerical_maximum'],'scope control')
    for name,fn in [('negative time',lambda:y.heat_envelopes(sigma=-1)),('larger cap',lambda:y.heat_envelopes(cap='1/50')),('larger preparation radius',lambda:y.heat_envelopes(eta='1/10'))]:
        rejects('heat '+name,fn)

    net=json.loads((y.HERE/'source_data/network_audit.json').read_text())
    check('network unique node accounting',net['node_count']==net['unique_node_ids']==158 and net['dangling_edges']==0)
    check('network edges accounting',sum(net['edges_by_type'].values())==net['edge_count']==260)
    check('network round counts accounting',sum(net['nodes_by_round'].values())==158)
    structure=json.loads((y.HERE/'source_data/network_structure.json').read_text())
    ids=[n['id'] for n in structure['nodes']]
    check('drawn network structural source has exact node count',len(ids)==len(set(ids))==158)
    check('drawn network structural source has exact edge count',len(structure['edges'])==260)
    check('drawn network structural source has no dangling edges',all(e['from'] in ids and e['to'] in ids for e in structure['edges']))
    check('drawn network structural source has declared edge types',set(e['type'] for e in structure['edges'])==set(net['edges_by_type']))
    api=subprocess.run([sys.executable,'-c','import ym_calculators as y; print(y.mp.mp.dps)'],cwd=y.HERE,capture_output=True,text=True)
    check('direct API import defaults to 70 decimal working digits',api.returncode==0 and int(api.stdout.strip())>=70,'precision control')
    rejects('API refuses precision below documented range',lambda:y.configure_precision(15))
    for command in [['filter','--M','nan'],['window','--q','1'],['jacobi','--dimension','0'],['heat','--eta','1']]:
        result=subprocess.run([sys.executable,str(y.HERE/'ym_calculators.py'),*command],capture_output=True,text=True)
        check('CLI rejects '+' '.join(command),result.returncode==2 and 'error:' in result.stderr,'CLI rejection')
    result={'status':'passed','count':len(records),'scope':'Checks corroborate declared formulas and implementation. Sampled diagnostics do not prove infinite-dimensional theorems or interval accuracy. Same-author checks are not independent review.',
            'precision_decimal_digits':mp.mp.dps,'versions':{'python':platform.python_version(),'mpmath':mp.__version__},'checks':records,
            'source_sha256':{name:hashlib.sha256((y.HERE/name).read_bytes()).hexdigest() for name in ['ym_calculators.py','test_calculators.py','source_data/heat_scalar_inputs.json','source_data/network_audit.json','source_data/network_structure.json','source_data/source_manifest.json']}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(y.jsonable(result),indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'count':result['count'],'output':str(args.output)}))


if __name__=='__main__':
    main()
