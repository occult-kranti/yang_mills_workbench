#!/usr/bin/env python3
"""AI4 forward: continuous and all-band rational majorants plus ten fixtures.

The analytic proof is in report.md. Fixtures check that implementation, not its
unbounded quantifier. No inherited Python module is imported or new collar built.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial, isqrt
import argparse
import hashlib
import itertools
import json
import sys

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
CONTRACT = 'research/round28/contracts/ai4.json'
CONTRACT_SHA = '0b181d7c066dde2f2e48e58f468fcec60aef20ef305ea47bc60fc431c1631813'
Z = F(1, 10**7)
U0 = F(1, 10**24)
SQRT_U0 = F(1, 10**12)
ROUND = F(1, 2**320)
INDICES = (0, 1, 8, 64, 512)
CHECKS = []


def require(value, message):
    if value is not True:
        raise ValueError(message)
    CHECKS.append(message)


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serialize(x) for x in value]
    return value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_inputs():
    inp = HERE / 'inputs'
    manifest = json.loads((inp / 'source-inventory.json').read_text())
    contract = json.loads((inp / CONTRACT).read_text())
    require(sha(inp / CONTRACT) == CONTRACT_SHA, 'exact frozen AI4 contract')
    require(len(contract['sources']) == 35, 'all thirty-five contract sources required')
    require(manifest.get(CONTRACT) == CONTRACT_SHA, 'contract in manifest')
    for path, expected in contract['sources'].items():
        require(manifest.get(path) == expected, 'required source declaration ' + path)
    for path, expected in manifest.items():
        p = inp / path
        require(not Path(path).is_absolute() and '..' not in Path(path).parts, 'safe input ' + path)
        require(not any(x.is_symlink() for x in (p, *p.parents)), 'no symlink in input path ' + path)
        require(sha(p) == expected, 'copied source bytes ' + path)
    old = json.loads((inp / 'research/round28/forward/ai3/output/results.json').read_text())
    require(old['all_order_reflection_proved'] is True, 'admitted full retained reflection premise')
    require(old['multiplication_norm_squared'] == 8, 'admitted actual multiplier norm squared')
    require(len(old['geometry']['common_seed']) == 10, 'admitted ten-factor common support')
    require(len(old['geometry']['cycles']) == 16 and len(old['geometry']['exterior']) == 20,
            'entire reached component and all exterior loading premises')
    return manifest, old


def owner(e):
    a, x, y, z = e
    if (a == 0 and x % 4 < 3) or (a == 1 and y % 2 == 0):
        return ('s', 4 * (x // 4), 2 * (y // 2), z)
    return ('f', *e)


def completed(factor):
    if factor[0] == 'f':
        return (factor[1:],)
    _, x, y, z = factor
    return tuple((0, x + i, y + j, z) for i in range(3) for j in range(2)) + \
           tuple((1, x + i, y, z) for i in range(4))


def vertices(e):
    a, *v = e
    w = list(v); w[a] += 1
    return (tuple(v), tuple(w))


def face_envelope(k):
    if type(k) is not int or k < 0:
        raise ValueError('nonnegative integer collar depth required')
    length = k + 1
    return 24 * length**3 + 14 * length**2


def geometry_proof_controls(old):
    # Residues exhaust the periodic owner rule. These are single-factor tests,
    # not a new complete-collar enumeration.
    strip_tests = 0
    for a, x, y in itertools.product(range(3), range(4), range(2)):
        e = (a, x, y, 0)
        f = owner(e)
        if f[0] == 's':
            strip_tests += 1
            for other in completed(f):
                for v in vertices(other):
                    require(abs(v[0] - x) <= 3 and abs(v[1] - y) <= 1 and v[2] == 0,
                            'strip residue completion extends by at most (3,1,0)')
    box_checks = []
    for collar in old['collars']:
        k = collar['k']; length = k + 1
        upper = (4 * length, 2 * length, length)
        require(k <= 6, 'only admitted depths zero through six inspected')
        for e in collar['links']:
            require(all(0 <= v[i] <= upper[i] for v in vertices(e) for i in range(3)),
                    'admitted complete link inside all-depth vertex envelope')
        require(collar['retained_face_count'] <= face_envelope(k), 'admitted face count below polynomial envelope')
        # A*B*(C+1)+A*C*(B+1)+B*C*(A+1), all three orientations.
        A, B, C = upper
        require(A*B*(C+1) + A*C*(B+1) + B*C*(A+1) == face_envelope(k),
                'all-orientation box face count')
        box_checks.append({'k': k, 'vertices_upper': upper,
            'admitted_N': collar['retained_face_count'], 'N_envelope': face_envelope(k)})
    e = (1, 0, 0, 0); factor = owner(e)
    require((0, 2, 1, 0) in completed(factor) and (0, 2, 1, 0) != e,
            'edge-only strip shortcut misses actual required link')
    require(old['collars'][6]['retained_face_count'] > old['collars'][5]['retained_face_count'],
            'uncharged constant collar count rejected by admitted depth-five to six growth')
    return {'induction_step_vertex_growth': (4, 2, 1), 'initial_vertex_upper': (4, 2, 1),
        'initial_vertex_lower': (3, 1, 0), 'polynomial_N_coefficients_in_k_plus_one': [0, 0, 14, 24],
        'strip_residue_cases': strip_tests, 'admitted_collar_checks': box_checks,
        'new_collar_enumerations': 0,
        'proof': 'incident face adds at most one in each coordinate; strip completion adds at most (3,1,0); positive-orthant lower endpoint is zero; induction then counts every face orientation'}


def polynomial_product(a, b):
    result = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def tail(k):
    x = 15 * Z
    pochhammer = F(1)
    for n in range(k + 1):
        pochhammer *= (F(10, 3) + n) / (n + 1)
    return pochhammer * x**(k+1) / (1-x)**(k+5)


def uniform_proof():
    qmin = F(99, 100)
    require(1 - 2*U0 >= qmin and SQRT_U0**2 == U0, 'continuous q range and exact square root of u0')
    # p<=21; the lower numerator bound gives v>=z/100. The upper
    # v<=z/64 follows from p-2(1+q)^2(1+q^2)=q+q^2+2q^3+q^4.
    require((1+qmin)**2 * (1+qmin**2) / (32*21) >= F(1,100), 'continuous v lower bound')
    require(all(c >= 0 for c in [0, 1, 1, 2, 1]), 'continuous v upper polynomial has nonnegative coefficients')
    vmax = Z / 64
    root_constant_squared = F(21, 2304) / ((1+qmin)**3 * (1+qmin**2)**2 * (1+qmin**4))
    require(root_constant_squared <= F(1,80)**2, 'continuous inner square root bounded by 1/(80 e^(3/2))')
    require(F(8) < F(3)**2, 'sqrt eight bounded by three for H2 state cost')
    # Actual state upper, including inner rounding: H1 36/5 u^(3/2)
    # plus 576 delta u^3; H2 36/25 u^(3/2) plus 1536/5 delta u^3.
    state = [F(36,5), F(36,25)]
    rounding = [F(576), F(1536,5)]
    M0 = F(face_envelope(6),24)
    x = 15*Z
    spatial_ratio = 2 * x/(1-x) * F(31,24)
    require(spatial_ratio < 1, 'all-j spatial over u recurrence decreases')
    # M(j)=(j+7)^2*(j+7+7/12). Bound M(j+1)/M(j) by (8/7)^3.
    mj = polynomial_product(polynomial_product([F(7),1],[F(7),1]),[F(91,12),1])
    mj_next = polynomial_product(polynomial_product([F(8),1],[F(8),1]),[F(103,12),1])
    growth = F(8,7)**3
    growth_difference = [growth*a-b for a,b in zip(mj,mj_next)]
    require(all(c >= 0 for c in growth_difference), 'all-j M envelope growth polynomial coefficients nonnegative')
    average_ratio = growth**2/4
    require(average_ratio < 1, 'all-j averaging over u recurrence includes M squared and decreases')
    require(growth**2/8 < 1, 'all-j absolute averaging recurrence decreases')
    arithmetic = (6*vmax)**9/factorial(9)
    center_bias = F(2,3)*vmax**3 + F(8,15)*vmax**5 + F(52,315)*vmax**7
    combination_tail = 91*(6*vmax)**9/(factorial(9)*(1-6*vmax))
    require(6*vmax < 1, 'entire retained combination tail converges')
    state_max = state[0]*U0*SQRT_U0
    round_max = rounding[0]*ROUND*U0**3
    spatial_max = 8*tail(6)
    averaging_max = 48*U0**3*M0*(1+3*Z*M0)
    Rmax = state_max + round_max + spatial_max + averaging_max
    denominator_polynomial_lower = Z*qmin**4/100 - 36*vmax**3 - (6*vmax)**7/factorial(7)
    denominator_before_relaxation = denominator_polynomial_lower - arithmetic - Rmax
    dstar = Z/120
    require(denominator_before_relaxation > dstar > 0, 'uniform positive actual and scalar-box denominator')
    nstar = Z/32
    require(vmax+36*vmax**3+Rmax < nstar, 'uniform absolute imaginary numerator envelope')
    # Divide the entire cancellation numerator by dstar. Use u>Uj/2
    # for spatial and u<=Uj for state and averaging. Every term is charged.
    coefficients = []
    for h in range(2):
        coefficients.append({
            'state': 2*state[h]*SQRT_U0/dstar,
            'inner_rounding': 2*rounding[h]*ROUND*U0**2/dstar,
            'spatial': 32*tail(6)/(dstar*U0),
            'averaging': 96*U0**2*M0*(1+3*Z*M0)/dstar,
            'retained_center_bias': (h+1)*center_bias/dstar,
            'retained_combination_tail': (h+1)*combination_tail/dstar})
    radii = [sum(row.values()) for row in coefficients]
    beta = 1-sum(radii)
    require(beta > F(97,100) > F(1,2), 'uniform all-band gap coefficient exceeds requested one-half')
    require(all(value > 0 for row in coefficients for value in row.values()), 'all physical and arithmetic coefficient classes present')
    L = 2*(1+nstar/dstar)/dstar
    epsilon_coefficient = dstar/100
    require(epsilon_coefficient*U0 <= dstar/2, 'additional scalar error keeps denominator positive')
    residual_beta = beta-2*L*epsilon_coefficient
    require(residual_beta > F(78,100) > F(1,2), 'u-dependent scalar tolerance preserves positive uniform gap')
    return {'q_lower':qmin,'v_lower_coefficient':F(1,100),'v_upper':vmax,
        'root_constant_squared':root_constant_squared,'root_upper_coefficient':F(1,80),
        'state_scalar_coefficients':state,'inner_rounding_scalar_coefficients':rounding,
        'inner_rounding_absolute_width':ROUND,'M0_envelope':M0,
        'spatial_ratio_upper':spatial_ratio,'M_growth_upper':growth,
        'M_growth_difference_polynomial':growth_difference,
        'averaging_over_u_ratio_upper':average_ratio,
        'individual_arithmetic_denominator_allowance':arithmetic,
        'center_bias_coefficient_per_e':center_bias,'combination_tail_coefficient_per_e':combination_tail,
        'maximum_physical_scalar_terms':{'state':state_max,'inner_rounding':round_max,'spatial':spatial_max,'averaging':averaging_max},
        'denominator_pre_relaxation':denominator_before_relaxation,'dstar':dstar,'nstar':nstar,
        'hypothesis_radius_coefficients_by_term':coefficients,'hypothesis_total_radius_coefficients':radii,
        'uniform_gap_coefficient':beta,'simple_gap_coefficient':F(97,100),
        'extra_scalar_error_coefficient':epsilon_coefficient,'ratio_perturbation_L':L,
        'gap_coefficient_with_extra_scalar_error':residual_beta,
        'quantifier':'all real 0<u<=u0, in its unique band j>=0; induction/continuous proof, not finite fixtures',
        'proof_anchors':{'geometry_induction':True,'continuous_q_bounds':True,
            'all_j_spatial_recurrence':True,'all_j_growing_M_and_M_squared_recurrence':True,
            'all_order_numerator_tail':True,'fixed_inner_rounding_propagated':True}}


def band_index(u):
    if type(u) is not F or not 0 < u <= U0:
        raise ValueError('exact rational 0<u<=u0 required for executable band classifier')
    upper=U0; j=0
    while u <= upper/2:
        upper /= 2; j += 1
    return j


def pvalue(polynomial,q):
    return sum(F(coefficient)*q**int(power) for power,coefficient in polynomial.items())


def b(q):
    p=2+5*q+5*q*q+6*q**3+3*q**4
    return p/(24*(1-q)**3*(1+q)**2*(1+q*q))


def sqrt_interval(value):
    den=2**320
    n=isqrt(value.numerator*den*den//value.denominator)
    lo=F(n,den); hi=lo if lo*lo==value else F(n+1,den)
    require(lo*lo<=value<=hi*hi and hi-lo<=ROUND, 'exact inner square-root bracket')
    return lo,hi


def divide_interval(n,d):
    require(d[0]>0 and d[0]<=d[1] and n[0]<=n[1], 'ordered ratio intervals with positive denominator')
    values=[a/c for a,c in itertools.product(n,d)]
    return (min(values),max(values))


def scalar_data(u,h,old):
    e=(h+1)*u; q=1-e; eta=(F(1,2),F(1,16))[h]
    require(q<1 and q>0 and 1-q==e, 'q stays exact below endpoint at fixture')
    tau=eta/(8*b(q)); s=Z*tau/(eta*e**3); v=s/96
    lo,hi=sqrt_interval(b(q*q)/96)
    state_upper=384*tau*hi/(1-eta)
    state_rounding_charge=384*tau*(hi-lo)/(1-eta)
    centers={}; moments={}
    for r in (4,5):
        moment=[pvalue(p,q) for p in old['moment_polynomials'][str(r)]]
        moments[r]=moment
        centers[r]=sum((-1)**((n-1)//2)*moment[n]*v**n/factorial(n) for n in (1,3,5,7))
    C=sum((-1)**((n-1)//2)*pvalue(old['difference_polynomials'][str(n)],q)*v**n/factorial(n)
          for n in (3,5,7))
    require(C==centers[5]-q*centers[4], 'inherited signed exact combination evaluated consistently')
    A=(6*v)**9/factorial(9)
    T=e*91*(6*v)**9/(factorial(9)*(1-6*v))
    return {'q':q,'eta':eta,'e':e,'tau':tau,'s':s,'v':v,
        'physical_time_in_hbar_over_alpha':Z/(eta*e**3),
        'sqrt_lower':lo,'sqrt_upper':hi,'state_upper_including_rounding':state_upper,
        'inner_rounding_scalar_charge':state_rounding_charge,
        'centers_imaginary':centers,'combination_center':C,
        'scalar_arithmetic':A,'combination_arithmetic':T}


def fixture_hypothesis(data,u,j,N,proof,h):
    k=6+j; M=F(N,24)
    state=data['state_upper_including_rounding']
    spatial=8*tail(k)
    averaging=64*data['tau']*M*(1+3*Z*M)
    R=state+spatial+averaging
    c4,c5=data['centers_imaginary'][4],data['centers_imaginary'][5]
    D=(c4-R-data['scalar_arithmetic'],c4+R+data['scalar_arithmetic'])
    require(D[0]>=proof['dstar'], 'fixture denominator within uniform continuous proof')
    numerator_radius=(1+data['q'])*R+data['combination_arithmetic']
    residual=divide_interval((data['combination_center']-numerator_radius,
                              data['combination_center']+numerator_radius),D)
    ratio=(data['q']+residual[0],data['q']+residual[1])
    coefficient=proof['hypothesis_total_radius_coefficients'][h]
    uniform=(data['q']-coefficient*u,data['q']+coefficient*u)
    require(uniform[0]<=ratio[0]<=ratio[1]<=uniform[1], 'fixture cancellation interval inside proved uniform interval')
    require(state <= proof['state_scalar_coefficients'][h]*u*SQRT_U0 +
            proof['inner_rounding_scalar_coefficients'][h]*ROUND*u**3,
            'fixture full state including propagated arithmetic bounded continuously')
    require(abs(data['combination_center']) <= data['e']*proof['center_bias_coefficient_per_e'],
            'fixture retained signed center within vanishing uniform bias')
    require(data['combination_arithmetic']<=data['e']*proof['combination_tail_coefficient_per_e'],
            'fixture entire arithmetic tail within uniform bound')
    return {**data,'N_used':N,'N_status':'proved polynomial envelope' if N==face_envelope(k) else 'admitted exact N6 comparison',
        'M_used':M,'physical_terms':{'state_including_inner_rounding':state,'spatial':spatial,'averaging':averaging},
        'physical_radius':R,'denominator':D,'cancellation_ratio_interval':ratio,
        'uniform_ratio_interval':uniform,'full_combination_numerator_radius':numerator_radius,
        'radius_terms_over_u':{'state':(1+data['q'])*state/(proof['dstar']*u),
            'spatial':(1+data['q'])*spatial/(proof['dstar']*u),
            'averaging':(1+data['q'])*averaging/(proof['dstar']*u),
            'center_bias':abs(data['combination_center'])/(proof['dstar']*u),
            'combination_arithmetic':data['combination_arithmetic']/(proof['dstar']*u)}}


def inference_controls(proof,old,fixtures):
    result={}
    require(band_index(U0/2)==1 and not U0/2>U0/2, 'excluded lower endpoint assigned to next band')
    require(band_index(U0)==0 and band_index(F(3,4)*U0)==0, 'upper endpoint and midpoint belong to base band')
    try:
        band_index(True)
    except ValueError:
        boolean_rejected=True
    else:
        boolean_rejected=False
    require(boolean_rejected, 'Boolean unknown parameter rejected')
    result['band_endpoints']={'u0_over_two_band':1,'wrong_closed_lower_assignment_rejected':True}
    require(len(old['geometry']['common_seed'])==10>8, 'missing common seed factors is a demonstrated support defect')
    # Growth and M^2 cannot be suppressed. Use only an already frozen fixture.
    large=fixtures[-1]['hypotheses'][0]
    M=large['M_used']; tau=large['tau']
    omitted=64*tau*M
    actual=large['physical_terms']['averaging']
    require(actual-omitted==192*Z*tau*M*M>0, 'omitted M squared averaging has exact positive defect')
    require(M>proof['M0_envelope'], 'growing collar budget cannot be silently fixed at base envelope')
    result['collar_growth_and_M_squared']={'admitted_depth_five_N':old['collars'][5]['retained_face_count'],
        'admitted_depth_six_N':old['collars'][6]['retained_face_count'],
        'large_fixture_M':M,'large_fixture_missing_M_squared_defect':actual-omitted}
    for component in ('state_including_inner_rounding','spatial','averaging'):
        reduced=large['physical_radius']-large['physical_terms'][component]
        require(reduced<large['physical_radius'], 'dropping '+component+' demonstrably undercounts physical bound')
    result['missing_physical_terms_rejected']=True
    u=fixtures[0]['u']
    require(F(1,2)*u**3==F(1,16)*(2*u)**3, 'candidate compensation matches common original clock')
    require(F(1,2)*u**3!=F(1,2)*(2*u)**3, 'wrong candidate eta fails common-clock relation')
    result['wrong_clock']={'correct_composite':F(1,2)*u**3,'wrong_H2_composite':F(1,2)*(2*u)**3}
    tiny=fixtures[-1]['u']
    final_floor=ROUND/(proof['dstar']*tiny)
    inner_charge=proof['inner_rounding_scalar_coefficients'][0]*ROUND*tiny**2/proof['dstar']
    require(final_floor>1 and inner_charge<proof['hypothesis_radius_coefficients_by_term'][0]['inner_rounding'],
            'fixed final scalar floor fails while actual tau-scaled inner rounding decays')
    result['rounding_location']={'same_absolute_rounding':ROUND,
        'final_scalar_floor_normalized_by_gap':final_floor,'tau_scaled_inner_normalized_charge':inner_charge,
        'constant_final_floor_admitted':False}
    # General sequence control, unrelated to another physical parameter fixture.
    finite_indices=set(INDICES)
    spoof=lambda n: F(0) if n in finite_indices else F(1)
    require(all(spoof(n)==0 for n in INDICES) and spoof(3)==1,
            'finite-index success cannot establish all-integer statement')
    require(all(proof['proof_anchors'].values()), 'uniform acceptance requires explicit analytic proof anchors')
    result['finite_index_shortcut']={'tested_indices':INDICES,'uncontracted_abstract_sequence_index':3,
        'abstract_sequence_value':spoof(3),'not_a_physical_fixture':True}
    y4,y5=F(3),F(2)
    ratios=[y5/y4 for q in (F(1,2),F(2,3))]
    residuals=[y5-q*y4 for q in (F(1,2),F(2,3))]
    require(ratios[0]==ratios[1] and residuals[0]!=residuals[1], 'candidate residual is not a true-q-dependent measurement')
    result['candidate_circularity']={'q_independent_ratio':ratios[0],'candidate_residuals':residuals}
    eps0=proof['extra_scalar_error_coefficient']*U0
    eps_tiny=proof['extra_scalar_error_coefficient']*tiny
    require(eps_tiny<eps0 and eps0/eps_tiny==U0/tiny, 'vanishing scalar allowance is not fixed instrument robustness')
    # Exact 90-degree common phase: (1+i/10,1+i/5) ratio changes 2->1.
    require(F(1,5)/F(1,10)==2 and F(1)/F(1)==1, 'unknown common phase changes imaginary ratio')
    result['instrument_phase_timing_scope']={'base_allowance':eps0,'large_band_allowance':eps_tiny,
        'uniform_fixed_positive_scalar_noise_claim':False,'unknown_phase_ratio_before':2,
        'unknown_phase_ratio_after':1,'timestamp_sensitivity_supplied':False}
    return result


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    target=Path(parser.parse_args().output)
    require(target.is_absolute() and not target.exists(), 'fresh absolute output')
    manifest,old=check_inputs()
    geometry=geometry_proof_controls(old)
    proof=uniform_proof()
    fixtures=[]
    for j in INDICES:
        upper=U0/F(2)**j
        for position,u in (('upper',upper),('midpoint',F(3,4)*upper)):
            require(band_index(u)==j and upper/2<u<=upper, 'exact fixture band assignment')
            data=[scalar_data(u,h,old) for h in range(2)]
            require(data[0]['physical_time_in_hbar_over_alpha']==data[1]['physical_time_in_hbar_over_alpha']==2*Z/u**3,
                    'same original physical time for frozen fixture')
            pair=[fixture_hypothesis(d,u,j,face_envelope(6+j),proof,h) for h,d in enumerate(data)]
            gap=pair[0]['cancellation_ratio_interval'][0]-pair[1]['cancellation_ratio_interval'][1]
            require(gap>=proof['uniform_gap_coefficient']*u>=u/2, 'fixture obeys all-band gap theorem')
            row={'j':j,'position':position,'u':u,'k':6+j,'N_envelope':face_envelope(6+j),
                'hypotheses':pair,'exact_fixture_ratio_gap':gap,'gap_over_u':gap/u,
                'uniform_guaranteed_gap':proof['uniform_gap_coefficient']*u,
                'additional_scalar_allowance':proof['extra_scalar_error_coefficient']*u}
            if j==0:
                exact_N=old['collars'][6]['retained_face_count']
                exact_pair=[fixture_hypothesis(d,u,j,exact_N,proof,h) for h,d in enumerate(data)]
                row['admitted_exact_N6_comparison']={'N6':exact_N,'hypotheses':exact_pair,
                    'gap':exact_pair[0]['cancellation_ratio_interval'][0]-exact_pair[1]['cancellation_ratio_interval'][1],
                    'same_fixture_not_extra_parameter_point':True}
                require(all(a['physical_radius']<=b['physical_radius'] for a,b in zip(exact_pair,pair)),
                        'same-fixture exact N6 comparison only reduces averaging budget')
            fixtures.append(row)
    require([(r['j'],r['position']) for r in fixtures]==[(j,p) for j in INDICES for p in ('upper','midpoint')],
            'exactly ten predeclared fixtures and no new collars')
    controls=inference_controls(proof,old,fixtures)
    display={'uniform_beta':float(proof['uniform_gap_coefficient']),
        'uniform_term_sums':{key:float(sum(row[key] for row in proof['hypothesis_radius_coefficients_by_term']))
            for key in proof['hypothesis_radius_coefficients_by_term'][0]},
        'dstar':float(proof['dstar']), 'extra_scalar_allowance_at_u0':float(proof['extra_scalar_error_coefficient']*U0),
        'gap_coefficient_with_extra_scalar_error':float(proof['gap_coefficient_with_extra_scalar_error']),
        'fixtures':[{'j':r['j'],'position':r['position'],'k':r['k'],'N_envelope':r['N_envelope'],
            'gap_over_u':float(r['gap_over_u'])} for r in fixtures]}
    result={'schema':'ym28-forward-ai4-v1','contract_sha256':CONTRACT_SHA,
        'model':'canonical summable full-link SU(2), actual Wilson multipliers and full physical errors',
        'parameters':{'z':Z,'u0':U0,'indices':INDICES,'schedule':'k=6+j','band':'u0/2^(j+1)<u<=u0/2^j'},
        'geometry_envelope':geometry,'uniform_proof':proof,'fixtures':fixtures,'controls':controls,
        'display_only':display,'checks':CHECKS,'check_count':len(CHECKS),
        'current_reverse_AI4_read':False,'new_collar_enumerations':0,'source_inventory':manifest,
        'producer_bindings':{p:sha(HERE/p) for p in ('check.py','inputs/source-inventory.json','inputs/snapshot-event.json')},
        'attribution':'Feynman proposed shorter duration; advisor proposed dyadic family; AI3 sources are admitted shared premises. New forward uniform derivation and implementation.',
        'scope':'Uniform family of conditional candidate-pair mathematical tests; no continuous inverse, apparatus, matching or continuum claim'}
    target.mkdir(parents=True)
    (target/'results.json').write_text(json.dumps(serialize(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':len(CHECKS),'display':display},indent=2))


if __name__=='__main__':
    main()
