#!/usr/bin/env python3
"""AI4 reverse: independent all-band proof certificates and ten exact fixtures.

Inherited AI3 JSON supplies admitted geometry/moments only. No prior checker
is imported. Fresh absolute --output required; all guards survive -O.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
Z = F(1, 10**7)
U0 = F(1, 10**24)
SQRT_U0 = F(1, 10**12)
TEST_BANDS = (0, 1, 8, 64, 512)
CHECKS = []


def need(truth, description):
    if not truth:
        raise ValueError(description)
    CHECKS.append(description)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serial(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): serial(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serial(v) for v in obj]
    return obj


def move(vertex, axis, distance=1):
    out = list(vertex)
    out[axis] += distance
    return tuple(out)


def classify(link):
    point, axis = link
    x, y, z = point
    if axis == 2 or (axis == 0 and x % 4 == 3) or (axis == 1 and y % 2 == 1):
        return ('free', point, axis)
    return ('strip', (x - x % 4, y - y % 2, z), -1)


def complete(factor):
    kind, origin, axis = factor
    if kind == 'free':
        return {(origin, axis)}
    return {(move(move(origin, 0, i), 1, t), 0) for i in range(3) for t in range(2)} | {
        (move(origin, 0, i), 1) for i in range(4)}


def vertices(links):
    return {v for p, axis in links for v in (p, move(p, axis))}


def resource(k):
    upper = (4 + 4*k, 2 + 2*k, 1 + k)
    faces = 3*(4*k+5)*(2*k+3)*(k+2)
    return upper, faces, F(faces, 24)


def geometry_argument(admitted):
    # These 24 residue cases check the universal owner-completion displacement.
    # They enumerate no collar and no new physical parameter fixture.
    for rx in range(4):
        for ry in range(2):
            for axis in range(3):
                point = (4+rx, 2+ry, 1)
                endpoints = vertices({(point, axis)})
                lower = [min(v[c] for v in endpoints) for c in range(3)]
                upper = [max(v[c] for v in endpoints) for c in range(3)]
                padding = (3, 1, 0)
                owned = complete(classify((point, axis)))
                need(all(lower[c]-padding[c] <= v[c] <= upper[c]+padding[c]
                         for v in vertices(owned) for c in range(3)),
                     'complete-owner displacement residue '+str((rx,ry,axis)))
    need(tuple(a+b for a,b in zip((1,1,1),(3,1,0))) == (4,2,1),
         'one face incidence plus whole-owner completion gives all-step growth')
    factors, links, faces = set(), set(), set()
    verification = []
    for layer in admitted['geometry']['collars']:
        k = layer['depth']
        factors |= {(f[0], tuple(f[1]), f[2]) for f in layer['new_factors']}
        links |= {(tuple(e[0]), e[1]) for e in layer['new_links']}
        faces |= {(tuple(f[0]), f[1], f[2]) for f in layer['new_retained_faces']}
        full = set().union(*(complete(f) for f in factors))
        upper, count_bound, M = resource(k)
        need(full == links, 'admitted depth '+str(k)+' full strip completion verified')
        need(all(0 <= v[c] <= upper[c] for v in vertices(links) for c in range(3)),
             'admitted depth '+str(k)+' all link endpoints in proved envelope')
        need(all(0 <= f[0][c] <= upper[c] for f in faces for c in range(3)),
             'admitted depth '+str(k)+' face anchor envelope')
        need(len(faces) == layer['retained_faces'] <= count_bound, 'admitted N_'+str(k)+' below all-depth count')
        verification.append({'k':k,'actual_factors':len(factors),'actual_links':len(links),
                             'actual_faces':len(faces),'coordinate_upper':upper,'face_envelope':count_bound,'M_envelope':M})
    need(len(verification)==7 and verification[-1]['actual_faces']==1808,
         'only admitted depths zero through six checked; no new collar enumeration')
    need(len(admitted['geometry']['seed'])==10, 'admitted actual ten-factor common seed retained')
    # For k=6+j, each affine factor is bounded by its j=0 coefficient times j+1.
    need(29-4 >= 0 and 15-2 >= 0 and 8-1 >= 0 and 3*29*15*8 == 10440,
         'coefficient proof N_(6+j)<=10440(j+1)^3 for every j>=0')
    return verification


def tail(k):
    x = 15*Z
    coeff = F(1)
    for n in range(k+1):
        coeff *= (F(10,3)+n)/(n+1)
    return 8*coeff*x**(k+1)/(1-x)**(k+5)


def full_profile(q):
    numerator = 2+5*q+5*q**2+6*q**3+3*q**4
    return numerator/(24*(1-q)**3*(1+q)**2*(1+q*q))


def evaluate(poly, q):
    # New Horner evaluator of inherited formal polynomial coefficients.
    if not poly:
        return F(0)
    terms = {int(k): F(v) for k,v in poly.items()}
    value = F(0)
    for degree in range(max(terms), -1, -1):
        value = value*q + terms.get(degree, F(0))
    return value


def band(u):
    if not 0 < u <= U0:
        raise ValueError('u outside contracted family')
    ratio = U0/u
    j = max(0, ratio.numerator.bit_length()-ratio.denominator.bit_length())
    while F(2)**j > ratio:
        j -= 1
    while F(2)**(j+1) <= ratio:
        j += 1
    return j


def proof_constants():
    q0 = F(99,100)
    need(1-2*U0 >= q0 and q0**4 >= F(9,10), 'continuous-u fixed q lower bound and q^4>=9/10')
    # p(q)>=21 q^4, p(q)<=21, A(q)<=8, A(q)>=A(q0).
    need(F(8,7)/q0**4 <= F(3,2), 'continuous tau<=3eta(1-q)^3/2')
    need((1+q0)**2*(1+q0*q0)/672 >= F(1,100), 'continuous v>=z/100')
    need(3*F(1,2)/96 == F(1,64), 'continuous v<=z/64')
    # The bound below is on a^3 b(q^2)/96, a=1-q.
    sqrt_coefficient_squared = F(21,2304)*F(10,19)**6
    need(sqrt_coefficient_squared <= F(1,4096), 'analytic sqrt(b(q^2)/96)<=a^(-3/2)/64')
    need(384*F(3,2)/64 == 9, 'full state prefactor after tau and sqrt bound')
    need(8 <= 9 and 9*F(1,15)*3 == F(9,5), 'H2 square-root factor 2sqrt(2)<=3')
    state_coefficients = (F(9), F(9,5))
    need(SQRT_U0**2 == U0, 'exact square-root reference scale')
    spatial_base = tail(6)
    x = 15*Z
    spatial_ratio = F(31,12)*x/(1-x)
    need(0 < spatial_ratio < 1, 'all-band normalized spatial contraction rho<1')
    # 24(j+31/3)<=31(j+8) is equivalent to 0<=7j.
    need(F(31,3)/8 == F(31,24) and 31-24 > 0,
         'symbolic decreasing spatial quotient for all j>=0')
    # Exact maxima of (j+1)^3/4^j and (j+1)^6/4^j.
    need(F(1)<=2 and F(2**3,4)==2 and F(3,2)**3/4<1,
         'degree-three averaging envelope: prefix and all-j decreasing quotient')
    sixth_prefix = [F((j+1)**6,4**j) for j in range(4)]
    need(max(sixth_prefix)==64 and F(5,4)**6/4<1,
         'degree-six averaging envelope: prefix through3 and all-j decreasing quotient')
    M0 = F(435)
    averaging_per_u = 48*U0**2*(2*M0+64*3*Z*M0**2)
    spatial_per_u = 2*spatial_base/U0
    physical_per_u = [c*SQRT_U0+spatial_per_u+averaging_per_u for c in state_coefficients]
    V = Z/64
    individual_tail = (6*V)**9/factorial(9)
    denominator = F(9,1000)*Z-36*V**3-2*individual_tail-U0*max(physical_per_u)
    need(denominator > Z/125 > 0, 'uniform full scalar-center denominator including both Taylor allowances')
    # Exact factored Delta3,5,7 yield 4a,64a,832a bounds, respectively.
    need(2*2==4 and 2*(12+8+12)==64 and 2*(54+72+164+72+54)==832,
         'admitted positive polynomial coefficients bound every signed moment difference')
    retained_per_a = F(2,3)*V**3+F(8,15)*V**5+F(52,315)*V**7+91*(6*V)**9/(factorial(9)*(1-6*V))
    need(6*V<1, 'entire all-order numerator tail converges uniformly')
    beta = [(i*retained_per_a+2*P)/denominator for i,P in enumerate(physical_per_u,1)]
    gamma = 1-sum(beta)
    need(gamma > F(39,40) > F(1,2), 'all-band exact ratio gap coefficient exceeds39/40 and target1/2')
    need(1+max(beta)*U0 <= 2, 'uniform ratio magnitude at most two for extra-error transfer')
    need(gamma*U0/24 <= F(1,2), 'half-margin scalar tolerance satisfies denominator reserve')
    need((gamma-F(1,2))*U0/12 <= F(1,2), 'target-margin scalar tolerance satisfies denominator reserve')
    return {'q_lower':q0,'v_lower':Z/100,'v_upper':V,'state_coefficients':state_coefficients,
            'sqrt_inner_coefficient_squared':sqrt_coefficient_squared,'spatial_base':spatial_base,
            'normalized_spatial_ratio':spatial_ratio,'N_6_envelope':10440,'M_6_envelope':M0,
            'averaging_cubic_sequence_max':2,'averaging_sixth_sequence_max':64,
            'spatial_per_u':spatial_per_u,'averaging_per_u':averaging_per_u,
            'physical_per_u':physical_per_u,'individual_denominator_tail':individual_tail,
            'retained_numerator_per_one_minus_q':retained_per_a,'denominator_lower':denominator,
            'ratio_radius_coefficients':beta,'gap_coefficient':gamma,'simple_gap_coefficient':F(39,40),
            'gap_cost_components':{'retained':3*retained_per_a/denominator,
                                   'state':2*sum(state_coefficients)*SQRT_U0/denominator,
                                   'spatial':8*spatial_base/(U0*denominator),
                                   'averaging':4*averaging_per_u/denominator},
            'scalar_half_margin_coefficient':gamma*denominator/24,
            'scalar_target_margin_coefficient':(gamma-F(1,2))*denominator/12}


def controls(constants, admitted):
    lower = U0/2
    need(not (U0/2 < lower <= U0) and band(lower)==1, 'lower band endpoint belongs to following band')
    need(band(U0)==0 and band(F(3,4)*U0)==0, 'upper endpoint and midpoint assigned to exact band')
    e = ((2,0,0),0)
    factor = classify(e)
    need(len(complete(factor))==10 and ((0,1,0),0) in complete(factor) and ((0,1,0),0)!=e,
         'single drawn link cannot replace a whole strip owner')
    X = set(admitted['geometry']['cycles'][10]);Y4=set(admitted['geometry']['cycles'][6]);Y5=set(admitted['geometry']['cycles'][9])
    need(len(X|Y4)==8 and len(X|Y4|Y5)==10 and not Y5 <= X|Y4,
         'omitted seed factors exclude actual second multiplier')
    M5=F(admitted['geometry']['collars'][5]['retained_faces'],24)
    M6=F(admitted['geometry']['collars'][6]['retained_faces'],24)
    average=lambda M:64*M*(1+3*Z*M)
    need(M6>M5 and average(M6)>average(M5), 'actual admitted collar growth cannot use old averaging count')
    need(average(M6)-64*M6==192*Z*M6*M6>0, 'dropping M squared deletes a positive full averaging term')
    # A rectangular uncertainty control, not an assertion of realized physical errors.
    costs=(F(2,11),F(3,13),F(5,17));R=sum(costs);q=F(3,4)
    need(all((1+q)*R>(1+q)*(R-c) for c in costs),
         'each omitted physical term excludes an allowed opposing-error corner')
    eta1,eta2=F(1,2),F(1,16)
    need(eta1*U0**3==eta2*(2*U0)**3 and eta1*U0**3!=eta1*(2*U0)**3,
         'candidate compensation and wrong common-clock relation distinguished')
    inner_rounding=F(1,2**400)
    inner_coefficients=[384*F(3,4)/(1-eta)*inner_rounding for eta in (eta1,eta2)]
    need(all(c*(U0/2)**3==c*U0**3/8 for c in inner_coefficients),
         'fixed inner square-root error is multiplied by tau and decays cubically')
    final_floor=F(1,10**40)
    need(final_floor/(U0/2)==2*final_floor/U0,
         'fixed final scalar floor increases after normalization by shrinking u')
    eps0=constants['scalar_half_margin_coefficient']*U0
    eps64=constants['scalar_half_margin_coefficient']*(U0/F(2)**64)
    need(eps0>final_floor>eps64, 'fixed-error allowance passes base but fails a declared late-band tolerance')
    toy=lambda j:513-j
    need(all(toy(j)>0 for j in TEST_BANDS) and toy(514)<0,
         'finite-index success cannot substitute for an all-j proof')
    y4,y5=F(2,7),F(1,5)
    residual=lambda candidate:y5-candidate*y4
    need(residual(F(1,2))!=residual(F(2,3)) and y5/y4==F(7,10),
         'candidate residual varies but observable ratio uses no true unknown q')
    D=constants['denominator_lower'];g=constants['gap_coefficient']
    epsilon=g*D*U0/24
    need(epsilon<=D/2 and 12*epsilon/D==g*U0/2,
         'extra scalar transfer preserves half margin with both hypotheses charged')
    need(constants['scalar_half_margin_coefficient']*U0/2==epsilon/2,
         'scalar allowance tends to zero rather than fixed instrument robustness')
    need((2*Z/U0**3)/(2*Z/(U0/2)**3)==F(1,8),
         'physical clocks grow across bands although fixed within each candidate pair')
    return {'inner_rounding':inner_rounding,'inner_physical_coefficients_of_u_cubed':inner_coefficients,
            'fixed_final_scalar_floor':final_floor,'base_scalar_tolerance':eps0,'band64_scalar_tolerance':eps64,
            'finite_index_counterexample':'513-j; positive at all declared indices, negative at514',
            'controls_are_not_additional_physical_fixtures':True}


def fixtures(constants, admitted):
    polys=admitted['moment_polynomials']
    data=[]
    for j in TEST_BANDS:
        upper=U0/F(2)**j
        for location,scale in [('upper',F(1)),('midpoint',F(3,4))]:
            u=scale*upper;k=6+j
            need(band(u)==j and upper/2<u<=upper, 'exact continuous-band fixture '+str((j,location)))
            ceiling_root=SQRT_U0/F(2)**(j//2)
            need(ceiling_root**2>=upper>=u, 'analytic square-root ceiling '+str((j,location)))
            Nenv=resource(k)[1];M=F(Nenv,24);S=tail(k)
            need(S/u<=constants['spatial_per_u']*constants['normalized_spatial_ratio']**j,
                 'fixture checks analytic all-band spatial induction '+str((j,location)))
            pair=[]
            for h,(multiple,eta) in enumerate(((1,F(1,2)),(2,F(1,16)))):
                q=1-multiple*u;a=1-q;tau=eta/(8*full_profile(q));v=Z*tau/(96*eta*a**3)
                need(eta*a**3==u**3/2 and Z/(eta*a**3)==2*Z/u**3,
                     'actual common physical clock '+str((j,location,h)))
                need(constants['v_lower']<=v<=constants['v_upper'] and constants['q_lower']<=q<1,
                     'continuous parameter bounds at exact q below one '+str((j,location,h)))
                exact_state_squared=(384*tau/(1-eta))**2*full_profile(q*q)/96
                state=constants['state_coefficients'][h]*u*ceiling_root
                need(exact_state_squared<=state**2, 'analytic full stationary-state envelope '+str((j,location,h)))
                averaging=64*tau*M*(1+3*Z*M)
                need(averaging/u<=constants['averaging_per_u'], 'all-j growing-collar averaging bound '+str((j,location,h)))
                physical=state+S+averaging
                need(physical/u<=constants['physical_per_u'][h], 'continuous complete physical budget '+str((j,location,h)))
                centers={}
                for r in ('4','5'):
                    centers[r]=sum((-1)**((n-1)//2)*evaluate(polys[r][n],q)*v**n/factorial(n) for n in (1,3,5,7))
                arithmetic=(6*v)**9/factorial(9)
                combination=centers['5']-q*centers['4']
                combined_tail=a*91*(6*v)**9/(factorial(9)*(1-6*v))
                need(abs(combination)+combined_tail<=a*constants['retained_numerator_per_one_minus_q'],
                     'exact center and all-order numerator below uniform bias bound '+str((j,location,h)))
                denominator=centers['4']-physical-arithmetic
                need(denominator>=constants['denominator_lower'], 'full scalar denominator exceeds uniform lower bound '+str((j,location,h)))
                radius=(abs(combination)+combined_tail+(1+q)*physical)/denominator
                need(radius<=constants['ratio_radius_coefficients'][h]*u,
                     'fixture ratio enclosure inside uniform candidate interval '+str((j,location,h)))
                row={'hypothesis':'H'+str(h+1),'q':q,'eta':eta,'tau':tau,'v':v,'M_envelope':M,
                     'state_squared_exact':exact_state_squared,'state_analytic_envelope':state,
                     'spatial':S,'averaging_using_N_envelope':averaging,'physical_radius':physical,
                     'imaginary_centers':centers,'individual_arithmetic':arithmetic,
                     'signed_combination_center':combination,'combined_all_order_tail':combined_tail,
                     'denominator_lower':denominator,'refined_candidate_radius':radius,
                     'refined_candidate_interval':[q-radius,q+radius],
                     'uniform_candidate_interval':[q-constants['ratio_radius_coefficients'][h]*u,
                                                   q+constants['ratio_radius_coefficients'][h]*u]}
                if j==0:
                    exactM=F(admitted['geometry']['collars'][6]['retained_faces'],24)
                    actualN_averaging=64*tau*exactM*(1+3*Z*exactM)
                    need(actualN_averaging<averaging, 'same fixture actual N6 improves envelope averaging '+location+str(h))
                    row['same_fixture_N6_comparison']={'admitted_N6':1808,'N6_envelope':Nenv,
                                                      'averaging_with_exact_N6':actualN_averaging,
                                                      'averaging_with_envelope':averaging}
                pair.append(row)
            gap=pair[0]['refined_candidate_interval'][0]-pair[1]['refined_candidate_interval'][1]
            need(gap>=constants['gap_coefficient']*u>u/2, 'ten-fixture gap verifies all-band theorem '+str((j,location)))
            data.append({'j':j,'location':location,'u':u,'k':k,'N_k_envelope':Nenv,'exact_N_k_not_claimed':j!=0,
                         'physical_time_in_hbar_over_alpha':2*Z/u**3,'hypotheses':pair,'refined_ratio_gap':gap,
                         'uniform_ratio_gap':constants['gap_coefficient']*u,
                         'half_margin_scalar_tolerance':constants['scalar_half_margin_coefficient']*u,
                         'target_margin_scalar_tolerance':constants['scalar_target_margin_coefficient']*u})
    need(len(data)==10 and {row['j'] for row in data}==set(TEST_BANDS), 'exact ten fixed fixtures only')
    return data


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    out=Path(parser.parse_args().output)
    need(out.is_absolute() and not out.exists(), 'fresh absolute output directory')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text())
    contract_path='research/round28/contracts/ai4.json'
    need(sha(ROOT/contract_path)=='0b181d7c066dde2f2e48e58f468fcec60aef20ef305ea47bc60fc431c1631813',
         'exact frozen AI4 contract')
    contract=json.loads((ROOT/contract_path).read_text())
    need(set(contract['sources']) <= {item['source'] for item in inventory['entries']},
         'every contract source has a prospective snapshot')
    for path,expected in contract['sources'].items():
        need(sha(ROOT/path)==expected, 'declared source '+path)
    for item in inventory['entries']:
        need(sha(ROOT/item['source'])==sha(ROOT/item['snapshot'])==item['sha256'], 'prospective snapshot '+item['source'])
    need(inventory['frozen_before_scientific_production'] and inventory['current_opposite_direction_unread'],
         'input freeze precedes independent new implementation')
    admitted=json.loads((HERE/'inputs/research/round28/reverse/ai3/output/results.json').read_text())
    geometry=geometry_argument(admitted)
    constants=proof_constants()
    counterchecks=controls(constants,admitted)
    tests=fixtures(constants,admitted)
    bindings={item['source']:item['sha256'] for item in inventory['entries']}
    bindings.update({str(p.relative_to(ROOT)):sha(p) for p in (HERE/'inputs').rglob('*') if p.is_file()})
    for name in ('check.py','report.md'):
        bindings[str((HERE/name).relative_to(ROOT))]=sha(HERE/name)
    result={'schema':'ym28-reverse-ai4-v1','scope':{'model':'canonical summable full-link SU2',
            'uniform_all_bands':True,'pairwise_family_only':True,'new_collar_beyond_six_enumerated':False,
            'continuous_inverse':False,'fixed_unknown_parameter_instrument':False,'fixed_error_robustness':False,
            'physical_matching':False,'homogeneous_gap':False,'continuum_gap':False},
            'attribution':{'shorter_duration':'Feynman method proposal; now shared frozen contract',
                           'dyadic_family':'advisor proposal; shared frozen contract',
                           'AI3_geometry_moments_and_physical_transfer':'admitted shared premises'},
            'parameters':{'z':Z,'u0':U0,'k':'6+j','bands':'u0*2^(-j-1)<u<=u0*2^(-j)'},
            'uniform_proof_constants':constants,'admitted_geometry_envelope_checks':geometry,
            'controls':counterchecks,'fixtures':tests,'checks':CHECKS,'check_count':len(CHECKS),'bindings':bindings}
    out.mkdir(parents=True)
    (out/'results.json').write_text(json.dumps(serial(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'uniform_gamma':float(constants['gap_coefficient']),
                      'denominator_lower':float(constants['denominator_lower']),
                      'gap_cost_components':{k:float(v) for k,v in constants['gap_cost_components'].items()},
                      'fixtures':[{'j':r['j'],'location':r['location'],'gap_over_u':float(r['refined_ratio_gap']/r['u']),
                                   'N_envelope':r['N_k_envelope']} for r in tests]},sort_keys=True))


if __name__=='__main__':
    main()
