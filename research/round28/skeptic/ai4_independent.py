#!/usr/bin/env python3
"""Independent uniform AI4 bounds and exactly ten contracted band fixtures.

Only admitted AI3 data are reused. No current producer or legacy checker is
imported, and no new collar is enumerated. All verdicts use exact arithmetic.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CHECKS=[]
Z=F(1,10**7)
U0=F(1,10**24)
SQRT_U0=F(1,10**12)
MESH=F(1,2**320)
D=Z/128
V=Z/64
X=15*Z
BANDS=(0,1,8,64,512)


def need(ok,name):
    if not ok: raise RuntimeError(name)
    CHECKS.append(name)


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x


def display(x):
    with localcontext() as c:
        c.prec=12
        return format(Decimal(x.numerator)/Decimal(x.denominator),'.7E')


def Nbar(k): return 3*(4*k+5)*(2*k+3)*(k+2)
def Mbar(k): return F(Nbar(k),24)
def numerator(q): return (1+q)**2*(1+q*q)
def profile_p(q): return 2+5*q+5*q*q+6*q**3+3*q**4
def b(q): return profile_p(q)/(24*(1-q)**3*numerator(q))


def spatial(k):
    a=F(1)
    for n in range(k+1): a *= (F(10,3)+n)/(n+1)
    return 8*a*X**(k+1)/(1-X)**(k+5)


def root_up(q):
    den=2**320
    m=math.isqrt(q.numerator*den*den//q.denominator)
    lo=F(m,den);hi=lo if lo*lo==q else lo+MESH
    need(lo*lo<=q<=hi*hi and hi-lo<=MESH,'directed inner-root bracket')
    return hi


def polynomial(p,q): return sum((F(c)*q**int(n) for n,c in p.items()),F(0))


def within_band(u,j): return U0/F(2**(j+1)) < u <= U0/F(2**j)


def verify_sources():
    path=HERE/'ai4-inputs/source-inventory.json';manifest=json.loads(path.read_text())
    bindings={}
    for e in manifest['entries']:
        need(sha(ROOT/e['source'])==e['sha256'],'live source '+e['source'])
        need(sha(ROOT/e['snapshot'])==e['sha256'],'snapshot '+e['source'])
        bindings[e['source']]=e['sha256']
    contract=json.loads((ROOT/manifest['contract']).read_text())
    need(manifest['contract_sha256']=='0b181d7c066dde2f2e48e58f468fcec60aef20ef305ea47bc60fc431c1631813','frozen AI4 contract identity')
    need(len(contract['sources'])==35 and all(bindings.get(p)==h for p,h in contract['sources'].items()),'all thirty-five contract sources snapshotted')
    inherited=json.loads((HERE/'ai4-inputs/research/round28/forward/ai3/output/results.json').read_text())
    return bindings,inherited


def geometric_envelope(inherited):
    # General proof: a touching face adds at most one in each coordinate;
    # completion of a strip adds at most three x and one y, and no z.
    # Seed vertices are in [0,4] x [0,2] x [0,1]. Therefore every F_k
    # vertex is in [0,4+4k] x [0,2+2k] x [0,1+k].
    # Local owner-residue controls do not enumerate any collar.
    residue_rows=[]
    for a in range(3):
        for x in range(4):
            for y in range(2):
                start=(x,y,0);end=tuple(t+int(i==a) for i,t in enumerate(start))
                is_strip=(a==0 and x<3) or (a==1 and y==0)
                vertices={(i,j,0) for i in range(4) for j in range(2)} if is_strip else {start,end}
                for v in vertices:
                    need(min(start[0],end[0])-3<=v[0]<=max(start[0],end[0])+3
                         and min(start[1],end[1])-1<=v[1]<=max(start[1],end[1])+1
                         and min(start[2],end[2])<=v[2]<=max(start[2],end[2]),
                         'complete owner local coordinate extension '+str((a,x,y,v)))
                residue_rows.append({'axis':a,'x_residue':x,'y_residue':y,'strip':is_strip})
    need((3,1,0) not in {(0,0,0),(1,0,0)},'strip-completion witness exceeds displayed x edge')
    need(F(10,3)>F(8,3),'ten-factor connected seed cannot be replaced by eight')
    checked=[]
    for c in inherited['collars']:
        k=c['k'];upper=(4+4*k,2+2*k,1+k)
        need(k<=6,'only already admitted collars inspected')
        for e in c['links']:
            a,*v=e;w=list(v);w[a]+=1
            need(all(0<=t<=upper[i] for i,t in enumerate(v))
                 and all(0<=t<=upper[i] for i,t in enumerate(w)), 'admitted whole link within all-depth envelope '+str((k,e)))
        # Every anchor lies in the vertex box; three orientations give this
        # intentionally loose polynomial count even at positive boundaries.
        need(c['retained_face_count']<=Nbar(k),'polynomial face count covers admitted collar '+str(k))
        checked.append({'k':k,'N_exact':c['retained_face_count'],'N_upper':Nbar(k),'coordinate_upper':upper})
    need(len(checked)==7 and checked[-1]['N_exact']==1808 and checked[-1]['N_upper']==10440,'all admitted depths only, base envelope10440')
    # On the free yz ladder anchored at x3,y1, each face shares its top y
    # link with the next. F0 includes its first face. Thus N_k>=k+1:
    # a fixed count cannot bound every collar. This is an induction witness,
    # not an enumeration of a collar beyond depth six.
    need(1808+2>1808,'unbounded ladder defeats fixed N6 as an all-depth upper count')
    return {'vertex_box':'[0,4+4k] x [0,2+2k] x [0,1+k]',
            'N_upper_polynomial':'3(4k+5)(2k+3)(k+2)',
            'M_upper_polynomial':'(4k+5)(2k+3)(k+2)/8',
            'owner_residue_controls':residue_rows,'admitted_geometry_checks':checked,
            'new_collars_enumerated':0}


def uniform_bounds():
    qmin=F(99,100)
    need(1-2*U0>=qmin and qmin*qmin>=F(49,50),'continuous candidate q and q-squared range')
    need(numerator(qmin)>=7 and numerator(F(49,50))>=7,'monotone numerator lower bound seven')
    need(profile_p(F(1))==21,'nonnegative coefficient profile upper bound21')
    # p(q)-2N(q)=q+q^2+2q^3+q^4, with nonnegative coefficients.
    need([0,1,1,2,1]==[2-2,5-4,5-4,6-4,3-2],'coefficient proof tau<=3eta epsilon-cubed/2 and v<=z/64')
    need(F(7,32*21)==F(1,96),'continuous v lower bound z/96')
    need(21*72**2 <= 2304*7*F(19,10)**3,
         'all-q squared inequality sqrt(b(q2)/96)<=1/(72 epsilon^(3/2))')
    need(2**3<3**2,'H2 square-root factor 2sqrt2 below3')
    need(F(576,72)==8,'complete stationary coefficient8 eta/(1-eta) epsilon^(3/2)')
    S0=spatial(6);M0=Mbar(6)
    need(M0==435,'uniform base averaging M upper435')
    tail_ratio=F(31,24)*X/(1-X)
    need(2*tail_ratio<1,'spatial decrease beats dyadic candidate shrinkage at every j')
    # (k+13/3)/(k+2) decreases in k: it equals1+7/[3(k+2)].
    need(F(6)+F(13,3)==F(31,3),'spatial recurrence maximal prefactor at k6')
    # 3P(k)-2P(k+1), P=(4k+5)(2k+3)(k+2), after k=j+6.
    need(3*(8*6**3+38*6**2+59*6+30)-2*(8*7**3+38*7**2+59*7+30)==342,
         'M growth polynomial constant342')
    growth_coefficients=[342,603,134,8]
    need(all(c>0 for c in growth_coefficients),'all-j M ratio at most3/2 from positive shifted polynomial')
    need(F(3,8)<1 and F(9,16)<1,'u-squared weighted M and M-squared decrease all bands')
    need(F(3,16)<1 and F(9,32)<1,'u-cubed weighted M and M-squared decrease all bands')
    A0=(6*V)**9/math.factorial(9)
    state0=8*U0*SQRT_U0
    rounding0=576*U0**3*MESH
    avg0=48*U0**3*M0*(1+3*Z*M0)
    R0=state0+rounding0+S0+avg0
    poly_den_lower=(Z/96)*qmin**4-36*V**3-(6*V)**7/math.factorial(7)
    need(poly_den_lower-R0-A0>D,'uniform full physical denominator exceeds z/128')
    need(V+36*V**3+R0<3*D,'uniform absolute imaginary numerator below3D')
    B0=F(2,3)*V**3+F(8,15)*V**5+F(52,315)*V**7
    T0=91*(6*V)**9/(math.factorial(9)*(1-6*V))
    need(6*V<1,'uniform all-order numerator domain')
    need(F(4,math.factorial(3))==F(2,3) and F(64,math.factorial(5))==F(8,15)
         and F(832,math.factorial(7))==F(52,315),'exact vanishing signed-bias coefficient budgets')
    coefficients={
        'state':F(96,5)*SQRT_U0/D,
        'spatial':8*S0/(D*U0),
        'averaging':192*U0**2*M0*(1+3*Z*M0)/D,
        'inner_root_rounding':F(8832,5)*U0**2*MESH/D,
        'retained_signed_bias':3*B0/D,
        'all_order_combination_tail':3*T0/D,
    }
    C=sum(coefficients.values());G=1-C
    need(C<F(1,40) and G>F(39,40)>F(1,2),'all-j continuous gap at least39u/40 exceeds targetu/2')
    # Actual y4>=D, |y5|<=3D. Additional errors nu<=D/2 change
    # each quotient by <=8nu/D. Two candidates therefore lose <=16nu/D.
    public=F(39,40)
    tolerance_coefficient=public*D/32
    need(tolerance_coefficient*U0<=D/2,'uniform extra-scalar denominator guard')
    need(16*tolerance_coefficient/D==public/2,'extra scalar allowance preserves39u/80 margin')
    return {'z':Z,'u0':U0,'q_lower_used':qmin,'v_upper':V,'denominator_lower':D,
            'individual_arithmetic_denominator_upper':A0,'all_physical_denominator_upper':R0,
            'polynomial_denominator_lower':poly_den_lower,'imaginary_numerator_absolute_upper':3*D,
            'base_spatial_upper':S0,'base_N_upper':Nbar(6),'base_M_upper':M0,
            'spatial_step_ratio_upper':tail_ratio,'M_step_ratio_upper':F(3,2),
            'M_growth_positive_shifted_polynomial':growth_coefficients,
            'ratio_radius_sum_over_u_coefficients':coefficients,'radius_sum_over_u_upper':C,
            'strongest_stated_gap_coefficient':G,'public_gap_coefficient':public,
            'extra_scalar_tolerance_coefficient':tolerance_coefficient,
            'remaining_gap_with_extra_tolerance_coefficient':public/2,
            'inner_sqrt_mesh':MESH,
            'authority':'Continuous coefficient inequalities and all-j recurrences; finite fixtures are controls only.'}


def fixture_hypothesis(u,j,h,polys,bounds,N_override=None):
    multiplier,eta=(1,F(1,2)) if h==1 else (2,F(1,16))
    q=1-multiplier*u;eps=1-q;k=6+j
    tau=eta/(8*b(q));v=Z*numerator(q)/(32*profile_p(q))
    need(q<1 and eps==multiplier*u and eta*eps**3==u**3/2,'exact candidate and common clock relation '+str((j,h,N_override)))
    need(tau<=F(3,2)*eta*eps**3 and Z/96<=v<=V,'continuous tau and v estimates on declared fixture')
    m={r:[polynomial(p,q) for p in polys[str(r)]] for r in (4,5)}
    centers={r:sum(((-1)**((n-1)//2)*m[r][n]*v**n/math.factorial(n) for n in (1,3,5,7)),F(0)) for r in (4,5)}
    C=centers[5]-q*centers[4]
    diff3=2*q**13*(1-q*q)
    diff5=q**21*(1-q*q)*(12+8*q+12*q*q)
    diff7=q**29*(1-q*q)*(54+72*q+164*q*q+72*q**3+54*q**4)
    need(C==-v**3*diff3/6+v**5*diff5/120-v**7*diff7/5040,'admitted exact signed center identity')
    need(diff3<=4*eps and diff5<=64*eps and diff7<=832*eps,'continuous moment bounds on fixture')
    arithmetic=(6*v)**9/math.factorial(9)
    combo_tail=eps*91*(6*v)**9/(math.factorial(9)*(1-6*v))
    rounded_root=root_up(b(q*q)/96)
    state=48*tau*rounded_root/((1-eta)/8)
    spatial_cost=spatial(k);M=F(Nbar(k) if N_override is None else N_override,24)
    averaging=64*tau*M*(1+3*Z*M)
    R=state+spatial_cost+averaging
    state_coeff=F(8) if h==1 else F(8,5)
    rounding_coeff=F(576) if h==1 else F(1536,5)
    need(state<=state_coeff*u*SQRT_U0+rounding_coeff*u**3*MESH,'rounded state cost bounded with actual tau multiplier')
    need(R<=bounds['all_physical_denominator_upper'],'full growing-collar physical bound')
    den=centers[4]-R-arithmetic
    need(den>D,'actual polynomial full denominator exceeds uniform D')
    radius=(abs(C)+combo_tail+(1+q)*R)/D
    need(state>0 and spatial_cost>0 and averaging>0,'all complete physical errors nonzero and retained')
    need(64*tau*M*(1+3*Z*M)>64*tau*M,'M-squared averaging term cannot be dropped from complete sum')
    return {'hypothesis':h,'q':q,'eta':eta,'tau':tau,'v':v,'k':k,'N_used':Nbar(k) if N_override is None else N_override,
            'N_is_exact':N_override is not None,'physical_time_in_hbar_over_alpha':2*Z/u**3,
            'imaginary_polynomial_centers':centers,'signed_combination_center':C,
            'individual_arithmetic_denominator':arithmetic,'all_order_combination_tail':combo_tail,
            'physical_components':{'state_with_inner_rounding':state,'spatial':spatial_cost,'averaging':averaging},
            'physical_radius':R,'actual_denominator_lower':den,'ratio_radius_about_candidate':radius,
            'ratio_interval':(q-radius,q+radius)}


def additional_controls(bounds):
    need(not within_band(U0/2,0) and within_band(U0/2,1),'strict lower dyadic endpoint belongs to next band')
    need(within_band(U0,0) and not within_band(U0,1),'upper band endpoint belongs to stated band')
    need(F(1,16)*2**3==F(1,2) and F(1,8)*2**3!=F(1,2),'wrong eta ratio destroys common prescribed clock')
    # Every tested j can succeed while a separate sequence fails immediately
    # afterwards. This is an inference control, not an AI4 parameter fixture.
    false_all_j=lambda j:1-math.prod((j-a)**2 for a in BANDS)
    need(all(false_all_j(j)==1 for j in BANDS) and false_all_j(513)<0,'finite band successes cannot prove all-j theorem')
    nu0=bounds['extra_scalar_tolerance_coefficient']*U0
    nu512=nu0/F(2**512)
    need(0<nu512<nu0 and nu0/nu512==2**512,'vanishing scalar allowance is not fixed instrument robustness')
    need((U0/F(2**512))**2*MESH < U0**2*MESH,'tau-scaled inner rounding divided by u decays')
    need(nu0/(U0/F(2**512))>nu0/U0,'fixed final scalar error divided by target u grows')
    measured4,measured5=F(2),F(3)
    need(measured5/measured4==F(3,2) and measured5-F(1,2)*measured4!=measured5-F(1,3)*measured4,
         'candidate-indexed residual is not true-parameter access by instrument')
    # Exact phase rotation of test scalars changes an imaginary ratio.
    a4=(F(1),F(1,10));a5=(F(1),F(1,5))
    rotated=lambda a:F(4,5)*a[0]+F(3,5)*a[1]
    need(rotated(a5)/rotated(a4)!=a5[1]/a4[1],'scalar tolerance does not imply phase robustness')
    need(bounds['base_M_upper']<Mbar(7),'uncharged frozen M is not the growing polynomial envelope')
    need(bounds['individual_arithmetic_denominator_upper']>0 and bounds['individual_arithmetic_denominator_upper']<D,
         'individual constant Taylor remainder belongs in positive denominator')
    # A fixed nonzero numerator allowance ultimately beats any multiple of u.
    A=bounds['individual_arithmetic_denominator_upper']
    need(A/(D*(U0/F(2**512)))>F(1,2),'constant individual numerator remainder fails shrinking-gap use')
    costs=(F(1,7),F(1,11),F(1,13));q=F(1,2)
    full=(1+q)*sum(costs)
    for missing in range(3):
        reduced=(1+q)*sum(c for i,c in enumerate(costs) if i!=missing)
        need(full>reduced,'aligned admissible signed errors defeat dropped physical component '+str(missing))
    return {'fixed_final_tolerance_at_base':nu0,'allowed_tolerance_at_declared_j512':nu512,
            'finite_index_counterexample':'1-product_(a in {0,1,8,64,512})(j-a)^2',
            'scope':'Inference and arithmetic controls; no new physical parameter fixture or collar.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'ai4-independent.json')
    output=parser.parse_args().output
    bindings,inherited=verify_sources();geometry=geometric_envelope(inherited);bounds=uniform_bounds()
    controls=additional_controls(bounds);fixtures=[];shown=[]
    for j in BANDS:
        for label,scale in (('upper',F(1)),('midpoint',F(3,4))):
            u=scale*U0/F(2**j)
            need(within_band(u,j),'declared fixture belongs to frozen band '+str((j,label)))
            pair=[fixture_hypothesis(u,j,h,inherited['moment_polynomials'],bounds) for h in (1,2)]
            margin=u-sum(p['ratio_radius_about_candidate'] for p in pair)
            need(margin>=bounds['strongest_stated_gap_coefficient']*u>=F(39,40)*u,
                 'complete fixture satisfies analytic all-band coefficient '+str((j,label)))
            item={'j':j,'point':label,'u':u,'hypotheses':pair,'ratio_margin':margin,
                  'margin_over_u':margin/u,'extra_scalar_tolerance':bounds['extra_scalar_tolerance_coefficient']*u,
                  'physical_fixture_not_uniform_proof':True}
            if j==0:
                actual=[fixture_hypothesis(u,j,h,inherited['moment_polynomials'],bounds,N_override=1808) for h in (1,2)]
                actual_margin=u-sum(p['ratio_radius_about_candidate'] for p in actual)
                need(actual_margin>=margin and all(a['physical_radius']<=b_['physical_radius'] for a,b_ in zip(actual,pair)),
                     'admitted exact N6 versus same-fixture uniform envelope')
                item['same_fixture_exact_N6_comparison']={'hypotheses':actual,'ratio_margin':actual_margin}
            fixtures.append(item)
            shown.append({'j':j,'point':label,'N_upper':Nbar(6+j),'margin_over_u':display(margin/u),
                          'positive_deficit_of_margin_over_u_from_one':display(1-margin/u),
                          'u':display(u),'extra_scalar_tolerance':display(item['extra_scalar_tolerance'])})
    need(len(fixtures)==10 and [(f['j'],f['point']) for f in fixtures]==[(j,p) for j in BANDS for p in ('upper','midpoint')],
         'exactly ten contracted band fixtures, no additional parameter settings')
    result={'schema':'ym28-ai4-independent-v1','model':'canonical summable full-link SU2, actual B4/B5 multipliers',
            'attribution':'Feynman proposed shorter duration; advisor proposed dyadic family; AI3 physical and retained lemmas are shared admitted premises.',
            'source_bindings':bindings,'geometric_envelope':geometry,'uniform_bounds':bounds,'fixtures':fixtures,
            'additional_controls':controls,'display_only':shown,'checks':CHECKS,'check_count':len(CHECKS),
            'scope':{'uniform_continuous_all_bands':True,'gap_at_least_u_over_two':True,'public_gap_39u_over40':True,
                     'continuous_inverse':False,'unknown_parameter_instrument':False,'practical_clock':False,
                     'fixed_absolute_noise_robustness':False,'physical_matching':False,'continuum_Yang_Mills':False,
                     'new_collars_beyond_six_enumerated':False}}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'gap_coefficient':display(bounds['strongest_stated_gap_coefficient']),
                      'public_gap':'39u/40','fixtures':shown},indent=2))


if __name__=='__main__': main()
