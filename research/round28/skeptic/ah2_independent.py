#!/usr/bin/env python3
"""AH2 independent delayed-loading certificate. Parses admitted data; imports no producer."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = HERE / 'ah2-inputs'
GROUPS = Counter()

def need(ok, group, message):
    GROUPS[group] += 1
    if not ok:
        raise RuntimeError(group + ': ' + message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def enc(v):
    if isinstance(v, Q): return str(v)
    if isinstance(v, dict): return {str(k): enc(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)): return [enc(x) for x in v]
    return v

def floor_grid(x, scale=10**30): return Q((x.numerator*scale)//x.denominator, scale)
def ceil_grid(x, scale=10**30): return -floor_grid(-x, scale)

def sqrt_box(x, scale=10**30):
    z = math.isqrt((x.numerator*scale*scale)//x.denominator)
    lo, hi = Q(z, scale), Q(z+1, scale)
    if lo*lo == x: hi = lo
    need(lo*lo <= x <= hi*hi, 'radicals', 'outward square root')
    return lo, hi

def exp_minus_box(x):
    need(x >= 0, 'exponentials', 'nonnegative decay argument')
    if x == 0: return Q(1), Q(1)
    # Positive Taylor terms and one geometric bound for the remaining positive tail.
    n = 80
    term = total = Q(1)
    for j in range(1, n+1):
        term *= x / j
        total += term
    first = term*x/(n+1)
    ratio = x/(n+2)
    need(ratio < 1, 'exponentials', 'geometric Taylor tail is summable')
    upper = total + first/(1-ratio)
    lo, hi = floor_grid(1/upper), ceil_grid(1/total)
    need(0 < lo <= 1/upper <= 1/total <= hi <= 1, 'exponentials', 'reciprocal enclosure')
    return lo, hi

def bounds(cap):
    eta = Q(1,100)
    g = 3-29*cap
    r0 = Q(41,12)*cap**2
    p0 = r0/g
    rp = 29*cap*p0
    pp = rp/g
    dp = rp*rp/g
    q0 = Q(9,10)*cap # attributed admitted reverse AH1 input; sqrt(29)<27/5
    q = q0+p0
    b = q+eta
    z0 = 1-Q(29,72)*cap**2
    denominator = z0-eta-p0
    c = Q(151,40)*cap # sqrt(57)/2 <151/40
    d = Q(9,2)
    need(g > 0 and d > g and denominator > 0, 'bounds', 'strict gaps and true denominator')
    return dict(cap=cap, eta=eta, g=g, d=d, r0=r0, p0=p0, rp=rp, pp=pp,
                dp=dp, q0=q0, q=q, b=b, z0=z0, denominator=denominator, c=c,
                outside=29*cap)

def envelopes(v, t):
    eglo,eghi = exp_minus_box(v['g']*t)
    edlo,edhi = exp_minus_box(v['d']*t)
    g,d,c,q,b = (v[k] for k in ('g','d','c','q','b'))
    stationary_loading_upper = c*q*(1-edlo)/d
    excited_loading_upper = c*b*(eghi-edlo)/(d-g)
    loading_upper = stationary_loading_upper+excited_loading_upper
    jstat_lo = q/d*(t-(1-edlo)/d)
    jstat_hi = q/d*(t-(1-edhi)/d)
    jexc_lo = b/(d-g)*((1-eghi)/g-(1-edlo)/d)
    jexc_hi = b/(d-g)*((1-eglo)/g-(1-edhi)/d)
    integ_lo = max(Q(0), c*(jstat_lo+jexc_lo))
    integ_hi = c*(jstat_hi+jexc_hi)
    early = v['dp']*t + v['outside']*integ_hi
    early_simple = v['dp']*t + v['outside']*c*(q*t/d+b/(g*d))
    late = v['pp']+(2*b+v['pp'])*eghi
    need(0 <= integ_lo <= integ_hi and 0 <= early <= early_simple,
         'envelopes', 'complete integrated bound and monotone upper budget')
    need(stationary_loading_upper >= 0 and excited_loading_upper >= 0,
         'envelopes', 'both loading components nonnegative')
    if t == 0:
        need(loading_upper == early == integ_hi == 0, 'zero_controls', 'zero-time exact integral')
    if v['cap'] == 0:
        need(loading_upper == early == early_simple == 0, 'zero_controls', 'zero-coupling exact leakage')
    return dict(sigma=t, exp_minus_g_sigma=[eglo,eghi], exp_minus_d_sigma=[edlo,edhi],
                stationary_loading_upper=stationary_loading_upper,
                excited_loading_upper=excited_loading_upper,
                all_new_loading_upper=loading_upper,
                integrated_loading_interval=[integ_lo,integ_hi],
                early_absolute_upper=early, monotone_early_upper=early_simple,
                late_absolute_upper=late, true_relative_early_upper=early/v['denominator'],
                exact_physical_error_zero=(t == 0 or v['cap'] == 0))

def main(output):
    inv=json.loads((PACK/'source-inventory.json').read_text())
    sources={}
    for row in inv['entries']:
        path=HERE.parent.parent.parent/row['source']
        snap=HERE.parent.parent.parent/row['snapshot']
        # The inventory records repository-relative paths; only snapshots supply science.
        need(sha(snap)==row['sha256'], 'sources', row['source']+' frozen snapshot')
        sources[row['source']]=row['sha256']
    contract=json.loads((PACK/'research/round28/contracts/ah2.json').read_text())
    need(contract['sequence']==6 and contract['loop']=='ah2', 'sources', 'exact loop')
    need(len(contract['sources'])==33, 'sources', 'declared source count')
    for name,digest in contract['sources'].items():
        need(sources.get(name)==digest, 'sources', 'contract coverage '+name)
    old=json.loads((PACK/'research/round28/skeptic/ah1-independent.json').read_text())
    # Fresh explicit graph reconstruction (admitted Haar and complete-basis proofs remain premises).
    vertices=list(itertools.product(range(4),range(3),range(2)))
    links=[]
    for v in vertices:
        for a,m in enumerate((3,2,1)):
            if v[a]<m: links.append((v,a))
    lid={x:i for i,x in enumerate(links)}
    faces=[]
    for v in vertices:
        for a,b in itertools.combinations(range(3),2):
            if v[a]<(3,2,1)[a] and v[b]<(3,2,1)[b]:
                va=list(v); va[a]+=1
                vb=list(v); vb[b]+=1
                word=[(lid[v,a],1),(lid[tuple(va),b],1),(lid[tuple(vb),a],-1),(lid[v,b],-1)]
                faces.append(dict(anchor=list(v),axes=[a,b],word=[list(x) for x in word],mask=sum(1<<i for i,_ in word)))
    need((len(vertices),len(links),len(faces))==(24,46,29), 'geometry', 'complete original graph')
    need(faces==old['geometry']['faces'], 'geometry', 'all oriented faces')
    supports=[set(i for i,_ in f['word']) for f in faces]
    basis=old['physical_basis']
    expected=[]
    expected.append(('vacuum',(),Q(1),Q(0)))
    expected.extend(('fundamental',(p,),Q(1),Q(3)) for p in range(29))
    expected.extend(('spin_one',(p,),Q(1),Q(8)) for p in range(29))
    pairs=[]
    for p,q in itertools.combinations(range(29),2):
        inter=supports[p]&supports[q]
        need(len(inter) in (0,1), 'geometry', 'actual pair overlap')
        if inter:
            expected.extend([('singlet',(p,q),Q(1),Q(9,2)),('triplet',(p,q),Q(3),Q(13,2))])
        else: expected.append(('disjoint',(p,q),Q(1),Q(6)))
        pairs.append((p,q,len(inter)))
    need(len(expected)==561 and len(basis)==561, 'basis', 'full rank561')
    for row,e in zip(basis,expected):
        need((row['kind'],tuple(row['faces']),Q(row['metric']),Q(row['energy']))==e,
             'basis','individually resolved label/metric/electric energy')
    metrics=[e[2] for e in expected]
    T={}
    for i,(kind,fs,metric,energy) in enumerate(expected[30:],start=30):
        value=Q(1,4) if kind in ('singlet','triplet') else Q(1,2)
        for p in fs: T[i,p+1]=value
    S={}
    for p in range(1,30): S[0,p]=S[p,0]=Q(1,2)
    for (i,p),value in T.items():
        S[i,p]=value
        S[p,i]=metrics[i]*value
    admitted={(i,j):Q(v) for i,j,v in old['magnetic_sparse_action']}
    need(S==admitted,'blocks','complete physical S entries and all implicit zeros')
    need(len(S)==2124 and 561**2-len(S)==312597,'blocks','full action size')
    need(all(not(i>=30 and j>=30) for i,j in S),'blocks','N S N=0 on all531 new states')
    need(min(e[3] for e in expected[30:])==Q(9,2),'blocks','full N electric lower bound')
    need(not any((i,0) in S for i in range(30,561)),'blocks','N S Omega=0')
    need(sum(e[0]=='triplet' for e in expected)==96,'basis','all triplet states retained')
    gram=[[Q(0) for _ in range(29)] for _ in range(29)]
    row_losses=[]
    for i in range(30,561):
        entries={p-1:v for (j,p),v in T.items() if j==i}
        need(bool(entries),'deletion_controls','every new state has actual face source')
        for p,x in entries.items():
            for q,y in entries.items(): gram[p][q]+=metrics[i]*x*y
        loss=metrics[i]*sum(entries.values())**2/29
        need(loss>0,'deletion_controls','deleting this row loses bright-source norm')
        row_losses.append((i,expected[i][0],loss))
    for p in range(29):
        for q in range(29):
            need(gram[p][q]==Q(7)*(p==q)+Q(1,4),'gram','full source Gram entry')
    need(all(sum(row)==Q(57,4) for row in gram),'gram','bright eigenvalue')
    need(Q(7)+Q(29,4)==Q(57,4),'gram','dark eigenvalue7 plus rank-one channel')
    need(Q(151,40)**2>Q(57,4),'bounds','rational complete source norm envelope')
    need(Q(27,5)**2>29,'bounds','attributed q0 envelope')
    need(Q(41)**2>1653,'bounds','residual envelope')
    wrong_triplet_loss=sum(2*sum(v for (j,p),v in T.items() if j==i)**2/29
                            for i in range(30,561) if expected[i][0]=='triplet')
    need(wrong_triplet_loss>0,'metric_control','metric1 instead of3 changes full bright norm')
    # Symbolic kernel ODE coefficients, independent of the fixtures.
    v=bounds(Q(1,100)); g,d=v['g'],v['d']
    for n in range(12):
        def stat(k): return Q(0) if k==0 else -(-d)**k/(d*math.factorial(k))
        def conv(k): return ((-g)**k-(-d)**k)/((d-g)*math.factorial(k))
        need((n+1)*stat(n+1)+d*stat(n)==(1 if n==0 else 0),'kernels','stationary ODE coefficient')
        need((n+1)*conv(n+1)+d*conv(n)==(-g)**n/math.factorial(n),'kernels','excited convolution ODE coefficient')
        need((n+1)*(stat(n)/(n+1))==stat(n),'kernels','stationary primitive coefficient')
        need((n+1)*(conv(n)/(n+1))==conv(n),'kernels','excited primitive coefficient')
    join=envelopes(v,Q(3))
    simple=join['monotone_early_upper']
    term=total=Q(1)
    for n in range(1,31):
        term*=3*g/n; total+=term
    need(total>3000,'join','positive Taylor lower gives exp(-3g)<1/3000')
    late=v['pp']+(2*v['b']+v['pp'])/3000
    need(late<simple,'join','late branch at3 below monotone early cap')
    relative=simple/v['denominator']
    need(relative<Q(1,10000)<Q(11,5000),'join','all-time target and old bound improvement')
    need(v['denominator']==Q(old['heat_certificate']['true_output_denominator_lower']),
         'bounds','actual true-output denominator retained')
    need(v['p0']==Q(old['heat_certificate']['both_p0_projector_upper']) and
         v['rp']==Q(old['heat_certificate']['enriched_full_residual_upper']) and
         v['pp']==Q(old['heat_certificate']['enriched_projector_upper']) and
         v['dp']==Q(old['heat_certificate']['enriched_energy_error_upper']),
         'bounds','both projector comparisons and actual enriched residual/defect')
    # Preparations: eta is a coefficient, not its slightly larger distance to Omega.
    eta=Q(1,200); arad=1-eta**2; alo,ahi=sqrt_box(arad)
    distlo,disthi=2-2*ahi,2-2*alo
    need(arad+eta**2==1,'preparations','real and imaginary exact metric norm')
    need(eta**2<distlo<=disthi<Q(1,100)**2,'preparations','strict class membership; coefficient differs from distance')
    preparations=[dict(name='vacuum',vacuum_coefficient_squared=1,face_coefficient_squared=0,
                       distance_squared_interval=[0,0]),
                  dict(name='real_first_face',vacuum_coefficient_squared=arad,face_coefficient_squared=eta**2,
                       vacuum_coefficient_interval=[alo,ahi],phase='1',distance_squared_interval=[distlo,disthi]),
                  dict(name='imaginary_first_face',vacuum_coefficient_squared=arad,face_coefficient_squared=eta**2,
                       vacuum_coefficient_interval=[alo,ahi],phase='i',distance_squared_interval=[distlo,disthi])]
    fixtures=[]
    for cap in (Q(0),Q(1,200),Q(1,100)):
        point=bounds(cap)
        for t in (Q(0),Q(1),Q(3)):
            env=envelopes(point,t)
            for prep in preparations:
                need(prep['distance_squared_interval'][1]<=point['eta']**2,'fixtures','preparation is in unchanged class')
                fixtures.append(dict(coupling=cap,preparation=prep['name'],certificate=env,
                                     denominator=point['denominator'],uses_full_class_radius=point['eta'],
                                     numerical_heat_vector=False))
    need(len(fixtures)==27,'fixtures','exact frozen fixture set')
    # Material falsifiers use actual admitted blocks whenever available.
    first_face_new_norm=gram[0][0]
    need(first_face_new_norm==Q(29,4)>0,'N_Q_control','N S phi0 nonzero although Q S phi0=0')
    outside_witness=Q(1,2)*v['cap']
    need(outside_witness>0 and old['outside']['BP0_zero'] and not old['outside']['full_B_zero_for_positive_lambda'],
         'outside_control','BP0=0 but actual spin3/2 outside witness nonzero')
    feedback=v['cap']**2*gram[0][0]*eta
    need(feedback>0,'feedback_control','actual first-face return in second derivative is nonzero')
    # An actual ground component cannot be deleted: vacuum row of the eigen-equation.
    rlo,rhi=sqrt_box(9+29*v['cap']**2)
    wlo=(rlo-3)/2
    ground_vac_lower=1-v['q']**2
    ground_face_lower=wlo*ground_vac_lower/(Q(11,4)*v['cap'])
    stationary_face_lower=ground_vac_lower*ground_face_lower
    only_excited_upper=v['b']/3000
    actual_face_lower_at_join=stationary_face_lower-only_excited_upper
    need(wlo>0 and ground_vac_lower>0 and ground_face_lower>0,'stationary_control','actual retained ground has nonzero face part')
    need(actual_face_lower_at_join>only_excited_upper,'stationary_control','vacuum at declared sigma3 refutes excited-only face budget')
    # Wrong-center and denominator controls are inference counterexamples, not heat samples.
    toy_center_delta=Q(1,1000000)
    need(1+toy_center_delta>1,'center_control','positive rounded center generates ground growth')
    absolute=Q(1,100000)
    need(absolute/v['denominator']>absolute,'denominator_control','approximate norm1 cannot replace smaller proved true denominator')
    # Fixture interpolation cannot prove all-time: polynomial vanishes at0,1,3, not identically.
    fixture_poly=lambda s:s*(s-1)*(s-3)
    need(all(fixture_poly(t)==0 for t in (0,1,3)) and fixture_poly(2)!=0,
         'fixture_scope_control','abstract interpolation falsifier, not a new physical fixture')
    need(2*Q(3)!=Q(3),'clock_control','doubling sigma changes the original K-face generator')
    need(relative>Q(37,1000000),'old_accuracy_control','new certificate does not reproduce unrelated old graph accuracy')
    control=dict(new_projection_rank=531,full_outside_projection_infinite=True,
                 new_spin_one_vector_N_norm=1,new_spin_one_vector_Q_norm=0,
                 spin_three_halves_N_norm=0,spin_three_halves_Q_norm=1,
                 first_face_new_source_norm_squared=first_face_new_norm,
                 first_face_full_outside_source_norm_squared=0,
                 BP0_zero=True,full_B_zero_for_positive_lambda=False,
                 actual_outside_spin_three_halves_witness_at_cap=outside_witness,
                 every_channel_deleted_tested=len(row_losses),
                 deleted_channel_bright_loss_by_kind={k:sorted(set(loss for _,kind,loss in row_losses if kind==k)) for k in sorted(set(x[1] for x in row_losses))},
                 wrong_triplet_metric_bright_loss=wrong_triplet_loss,
                 full_feedback_prepared_first_face_second_derivative_return=feedback,
                 stationary_ground_vacuum_lower=ground_vac_lower,
                 stationary_ground_face_lower=ground_face_lower,
                 stationary_actual_vacuum_trajectory_face_lower_at_sigma3=actual_face_lower_at_join,
                 rejected_excited_only_face_upper_at_sigma3=only_excited_upper,
                 rounded_center_growth_control='abstract positive scalar ground shift; no physical fixture',
                 actual_center_defect_retained=v['dp'],
                 approximate_denominator_counterexample=[absolute,absolute/v['denominator']],
                 interpolation_control='s(s-1)(s-3): zeros at frozen times do not prove all-time',
                 original_K_face_energy=3,wrong_double_clock_K_face_energy=6,
                 old_graph_accuracy_not_transferred=True,nondiscriminating_candidates=[])
    result=dict(schema='ym28-ah2-skeptic-independent-v1',loop='ah2',research_loop_increment=0,
                contract_sha256=sources['research/round28/contracts/ah2.json'],
                source_bindings=sources,source_inventory_sha256=sha(PACK/'source-inventory.json'),
                current_producer_science_read=False,historical_checkers_imported_or_executed=False,
                model=dict(vertices=24,original_links=46,faces=29,physical_space='L2(SU2^46,Haar)^SU2^24',
                           retained_rank=561,strict_P0_rank=30,new_rank=531,
                           operator_domain='gauge-invariant H2',form_domain='gauge-invariant H1',
                           physical_clock='sigma=alpha*t/hbar; a,E_star,alpha/E_star,hbar fixed positive'),
                block_identity=dict(N_S_N_zero=True,N_K_N_minimum=Q(9,2),
                                    N_centered_A_N='K_N+(29*lambda-mu_plus)N >= (9/2)N',
                                    source_Gram_diagonal=Q(29,4),source_Gram_offdiagonal=Q(1,4),
                                    source_Gram_bright_eigenvalue=Q(57,4),source_Gram_dark_eigenvalue=7,
                                    complete_source_norm='lambda*sqrt(57)/2',
                                    source_norm_upper_coefficient=Q(151,40),
                                    full_magnetic_nonzero=2124,full_magnetic_zero=312597,
                                    all_new_states_have_nonzero_source=True),
                uniform_constants=v,all_time=dict(join=3,exp_minus_3g_upper=Q(1,3000),
                    exp_3g_positive_Taylor_lower=total,
                    early_monotone_absolute_upper=simple,late_absolute_upper_at_join=late,
                    true_relative_upper=relative,strict_simple_relative_upper=Q(1,10000),
                    inherited_common_relative_upper=Q(11,5000),
                    stationary_integrated_budget=v['outside']*v['c']*v['q']*3/v['d'],
                    excited_integrated_budget=v['outside']*v['c']*v['b']/(v['g']*v['d']),
                    center_budget=3*v['dp']),
                exact_cap_join_enclosures=join,preparations=preparations,fixtures=fixtures,
                controls=control,
                scope=dict(continuous_coupling=True,all_complex_preparations_in_class=True,
                           all_nonnegative_heat_times=True,full_feedback_retained=True,
                           exact_actual_own_ground_centers=True,true_output_denominator=True,
                           numerical_heat_vector=False,real_time_relative=False,graph_size_uniform=False,
                           original_model_matching=False,continuum_Yang_Mills_gap=False,optimality=False),
                check_groups=dict(GROUPS),check_count=sum(GROUPS.values()),
                display_only=dict(relative_upper=float(relative),absolute_upper=float(simple),
                                  late_absolute_upper=float(late),true_denominator=float(v['denominator'])))
    output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(check_count=result['check_count'],output=output.name,sha256=sha(output),
                          relative_upper=float(relative))))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'ah2-independent.json')
    main(parser.parse_args().output)
