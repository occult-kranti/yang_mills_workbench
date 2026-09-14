#!/usr/bin/env python3
"""Independent exact controls for the M2 physical correlation bound."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path

LEXICAL_HERE = Path(__file__).absolute().parent
HERE = LEXICAL_HERE.resolve()
ROOT = HERE.parents[3]
CONTRACT = 'research/round21/contracts/m2.json'
PREFIX = 'research/round21/forward/m2/'
PREMISES = [
    ('research/round21/advisor/m1-gate.json', 'research/round21/forward/m1/report.md', None),
    ('research/round20/advisor/h2-gate.json', 'research/round20/forward/h2/report.md', None),
    ('research/round20/advisor/g2-gate.json', 'research/round20/forward/g2/report.md', None),
    ('research/round21/advisor/j1-gate.json', 'research/round21/forward/j1/report.md', None),
    ('research/round21/advisor/j2-gate.json', 'research/round21/forward/j2/report.md', None),
    ('research/round19/advisor/a2-gate.json', 'research/round19/forward/a2/report.md', 'forward/a2/report.md'),
]
INPUTS = [CONTRACT, 'research/round21/advisor/m1-decision.md',
          'research/round21/methods/agent-instructions-at-selection.md',
          'research/round21/methods/paired-physics-research.md',
          PREFIX + 'method-snapshot.md', PREFIX + 'check.py', PREFIX + 'report.md']
for gate, report, _ in PREMISES:
    INPUTS.extend([gate, report])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejected(operation):
    try:
        operation()
    except ValueError:
        return True
    return False


def rational(x):
    require(type(x) in (int, Q), 'exact integer or Fraction required, not Boolean/float')
    return Q(x)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonsymlink(path):
    for component in [path, *path.parents]:
        require(not component.is_symlink(), 'symlink input component: ' + str(component))


def inputs():
    nonsymlink(LEXICAL_HERE)
    require(len(INPUTS) == len(set(INPUTS)), 'duplicate source input')
    for relative in INPUTS:
        p = ROOT / relative
        nonsymlink(p)
        require(p.is_file(), 'missing scientific input: ' + relative)
    contract = json.loads((ROOT / CONTRACT).read_text())
    require(contract['loop'] == 'm2' and contract['status'] == 'frozen', 'unfrozen M2')
    dependency = contract['depends_on']
    require(dependency['gate'] == PREMISES[0][0], 'wrong M1 dependency')
    require(sha(ROOT / dependency['gate']) == dependency['sha256'], 'M1 gate changed')
    require(contract['selection_record'] == INPUTS[1], 'selection record changed')
    for gate_path, report_path, historical_key in PREMISES:
        gate = json.loads((ROOT / gate_path).read_text())
        require(gate['status'] == 'accepted', 'unaccepted premise: ' + gate_path)
        require(gate['files'][historical_key or report_path] == sha(ROOT / report_path),
                'admitted report changed: ' + report_path)
    return {relative: sha(ROOT / relative) for relative in INPUTS}


@dataclass(frozen=True)
class G:
    """Gaussian rational; no binary-floating arithmetic enters a fixture."""
    real: Q = Q(0)
    imag: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, 'real', rational(self.real))
        object.__setattr__(self, 'imag', rational(self.imag))

    def __add__(self, other):
        z = other if isinstance(other, G) else G(other)
        return G(self.real + z.real, self.imag + z.imag)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-other if isinstance(other, G) else -G(other))

    def __mul__(self, other):
        z = other if isinstance(other, G) else G(other)
        return G(self.real*z.real-self.imag*z.imag, self.real*z.imag+self.imag*z.real)

    __rmul__ = __mul__

    def conjugate(self):
        return G(self.real, -self.imag)

    def norm2(self):
        return self.real*self.real + self.imag*self.imag


def vector(*entries):
    return [v if isinstance(v, G) else G(v) for v in entries]


def inner(a, b):
    return sum((x.conjugate()*y for x, y in zip(a, b)), G())


def mv(a, v):
    return [sum((x*y for x, y in zip(row, v)), G()) for row in a]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), G())
             for j in range(len(b[0]))] for i in range(len(a))]


def diag(*entries):
    return [[(v if isinstance(v, G) else G(v)) if i == j else G()
             for j in range(len(entries))] for i, v in enumerate(entries)]


def identity(n):
    return diag(*([1]*n))


def adjoint(a):
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def expectation(a, psi):
    return inner(psi, mv(a, psi))


def connected(a, b, u, psi):
    return inner(mv(a, psi), mv(u, mv(b, psi))) - expectation(a, psi).conjugate()*expectation(b, psi)


def B(q):
    q = rational(q)
    require(0 < q < 1, 'q outside canonical summable profile')
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def B_classes(q):
    return Q(1,12)/(1-q)**3 + q/(24*(1-q)**2*(1-q*q)) + q**3/(24*(1-q**4)*(1-q*q)*(1-q))


def profile(q, eta=Q(1, 2), alpha=Q(1), E_star=Q(1), hbar=Q(1)):
    q, eta, alpha, E_star, hbar = map(rational, [q, eta, alpha, E_star, hbar])
    require(0 < eta < 1, 'eta outside strict positive gap budget')
    require(alpha > 0 and E_star > 0 and hbar > 0, 'physical scales must be positive')
    b = B(q)
    tau = eta/(8*b)
    gbar = alpha*(1-eta)/8
    sigma2 = alpha*alpha*tau*tau*B(q*q)/96
    return {'q': q, 'eta': eta, 'alpha': alpha, 'alpha_over_E_star': alpha/E_star,
            'hbar': hbar, 'B': b, 'tau': tau, 'gbar': gbar, 'sigma2': sigma2,
            'd_upper_squared': sigma2/gbar**2, 'energy_upper': sigma2/gbar,
            'norm_V': alpha*tau*b}


def sqrt_enclosure(x, bits=96):
    x = rational(x)
    require(x >= 0 and type(bits) is int and bits > 0, 'invalid square root enclosure')
    denominator = 1 << bits
    n = isqrt(x.numerator*denominator**2 // x.denominator)
    lower = Q(n, denominator)
    upper = lower if lower*lower == x else Q(n+1, denominator)
    require(lower*lower <= x <= upper*upper, 'invalid enclosure')
    return lower, upper


def poly_product(a, b):
    result = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def profile_identity():
    fourth = poly_product(poly_product([1,1], [1,1]), [1,0,1])
    odd = poly_product([0,1], poly_product([1,1], [1,0,1]))
    numerator = [2*v + (odd[i] if i<len(odd) else 0) + (1 if i==3 else 0)
                 for i,v in enumerate(fourth)]
    require(numerator == [2,5,5,6,3], 'class-sum rational function not identical')
    residue = Q(sum(numerator), 24*4*2)
    require(residue == Q(7,64), 'wrong B cubic residue')
    sigma2_coefficient_per_eta2 = 1/(64*96*8*residue)
    require(sigma2_coefficient_per_eta2 == Q(1,5376), 'wrong sigma asymptotic')
    return {'numerator': numerator, 'B_cubic_residue': residue,
            'sigma_squared_coefficient_per_alpha_squared_eta_squared': sigma2_coefficient_per_eta2}


# Independently generated full strip support. Edge=(axis,x,y,z).
def face_edges(face):
    a,b,x,y,z = face
    require(type(a) is int and type(b) is int and 0 <= a < b < 3, 'invalid axes')
    p=[x,y,z]
    require(all(type(v) is int and v>=0 for v in p), 'invalid face anchor')
    pa,pb=p.copy(),p.copy()
    pa[a]+=1
    pb[b]+=1
    return {(a,*p),(a,*pb),(b,*p),(b,*pa)}


def factor(edge):
    axis,x,y,z=edge
    if axis==0 and x%4<3:
        return ('strip',4*(x//4),2*(y//2),z)
    if axis==1 and y%2==0:
        return ('strip',4*(x//4),y,z)
    return ('free',*edge)


def factor_edges(owner):
    if owner[0]=='free':
        return {owner[1:]}
    _,x,y,z=owner
    return set().union(*(face_edges((0,1,x+k,y,z)) for k in range(3)))


def cover(edges):
    return set().union(*(factor_edges(factor(edge)) for edge in edges)) if edges else set()


def omitted(face):
    a,b,x,y,z=face
    return (a,b)!=(0,1) or y%2!=0 or x%4==3


def incident_faces(edges):
    faces=set()
    for edge in edges:
        a,*p=edge
        for b in set(range(3))-{a}:
            for s in [0,-1]:
                anchor=p.copy()
                anchor[b]+=s
                if min(anchor)>=0:
                    faces.add((*sorted((a,b)),*anchor))
    return {f for f in faces if omitted(f)}


def brute_faces(edges):
    maximum=[max(e[i+1] for e in edges) for i in range(3)]
    return {(*axes,*p) for axes in combinations(range(3),2)
            for p in product(*(range(n+1) for n in maximum))
            if omitted((*axes,*p)) and face_edges((*axes,*p)) & edges}


def support_fixtures():
    displayed=face_edges((0,2,0,0,0))
    complete=cover(displayed)
    faces=incident_faces(complete)
    require(len(displayed)==4 and len(complete)==22 and len(faces)==28, 'origin cover changed')
    require(faces==brute_faces(complete), 'independent omitted incidence mismatch')
    witness=(0,2,2,1,0)
    require(witness in faces and witness not in incident_faces(displayed), 'support control nondiscriminating')
    require(len(faces)<=4*len(complete), 'incidence bound failed')
    require(cover(complete)==complete and cover(displayed)!=displayed, 'incomplete support undetected')
    # Two displayed links within one factor: exact finite support-spreading control.
    x_first=[[G(int(j==(i^2))) for j in range(4)] for i in range(4)]
    controlled_phase=diag(1,1,1,-1)
    evolved=mm(mm(controlled_phase,x_first),controlled_phase)
    second_flip=[[G(int(j==(i^1))) for j in range(4)] for i in range(4)]
    require(mm(x_first,second_flip)==mm(second_flip,x_first), 'initial disjoint links do not commute')
    require(mm(evolved,second_flip)!=mm(second_flip,evolved), 'evolved support failed to spread within factor')
    budgets=[]
    for q in [Q(1,2),Q(3,4),Q(7,8)]:
        amount=sum((q**sum(f[2:])/24 for f in faces),Q())
        require(amount<=Q(len(complete),6), 'finite support budget failed')
        budgets.append({'q':q,'D_F':amount,'complete_bound':Q(len(complete),6)})
    return {'displayed_links':str(len(displayed)), 'complete_links':str(len(complete)),
            'omitted_faces':str(len(faces)), 'missing_face':witness, 'budgets':budgets,
            'factor_evolution_example':'controlled phase conjugates first-link X to X tensor Z'}, complete


def centering_controls():
    psi=vector(1,0)
    a=[[G(1,1),G()],[G(2,-1),G(1,1)]]
    b=[[G(2,1),G()],[G(1,2),G(2,1)]]
    cov=connected(a,b,identity(2),psi)
    raw=inner(mv(a,psi),mv(b,psi))
    wrong=raw-expectation(a,psi)*expectation(b,psi)
    require(cov==G(0,5), 'complex covariance disagrees with direct centered vectors')
    require(raw!=cov and wrong!=cov, 'centering or adjoint control nondiscriminating')
    # H=diag(-1,1), e=-1, t=pi/2: U=diag(i,-i), shifted U=diag(1,-1).
    unshifted=connected(identity(2),identity(2),diag(G(0,1),G(0,-1)),psi)
    shifted=connected(identity(2),identity(2),diag(1,-1),psi)
    require(unshifted==G(-1,1) and shifted==G(), 'ground-energy shift control failed')
    # P_psi-P_omega for omega=e0, psi=(3/5,4/5).
    d=Q(4,5)
    difference=[[G(Q(-16,25)),G(Q(12,25))],[G(Q(12,25)),G(Q(16,25))]]
    require(mm(difference,difference)==diag(d*d,d*d), 'pure-projector eigenvalue identity failed')
    sign=[[entry*Q(1,d) for entry in row] for row in difference]
    require(mm(sign,sign)==identity(2), 'trace-distance dual witness is not norm one')
    product_matrix=mm(difference,sign)
    dual=sum((product_matrix[i][i] for i in range(2)),G())
    require(dual==G(2*d) and dual.real>d, 'projector factor two control failed')
    # Both mean differences occur; the exact split retains both summands.
    rotated=vector(Q(3,5),Q(4,5))
    ar=diag(G(1,1),G(2,-1))
    br=diag(G(3,1),G(5,2))
    aq, a0=expectation(ar,rotated).conjugate(),expectation(ar,psi).conjugate()
    bq, b0=expectation(br,rotated),expectation(br,psi)
    term1,term2=(aq-a0)*bq,a0*(bq-b0)
    require(term1!=G() and term2!=G() and aq*bq-a0*b0==term1+term2,
            'two-mean split failed')
    return {'complex_covariance_at_zero':cov, 'uncentered_value':raw,
            'wrong_unconjugated_mean_value':wrong, 'raw_identity_correlation_at_pi_over_two':unshifted,
            'shifted_identity_correlation':shifted, 'projector_distance':d,
            'trace_distance_dual_value':dual, 'mean_split_terms':[term1,term2],
            'bound_coefficients':{'uncentered_state':'2','first_mean':'2','second_mean':'2','total':'6'}}


def sector_control():
    gauge=diag(1,1,-1)
    h=diag(-2,1,5)
    k=diag(0,3,7)
    projection=diag(1,1,0)
    require(mm(h,gauge)==mm(gauge,h) and mm(h,projection)==mm(projection,h), 'sector not reducing')
    require(mv(k,vector(1,0,0))==vector(0,0,0), 'shift does not fix vacuum')
    invariant_excitation=vector(0,1,0)
    charged=vector(0,0,1)
    require(mv(gauge,invariant_excitation)==invariant_excitation and mv(gauge,charged)!=charged,
            'proper physical sector control failed')
    p=profile(Q(3,4),eta=Q(3,4))
    require(p['gbar']==Q(1,32) and p['gbar']<Q(973,8640), 'gap profile mismatch control absent')
    return {'toy_physical_dimension':'2','toy_full_dimension':'3','toy_shifted_physical_gap':'3',
            'profile_eta':p['eta'],'profile_own_gap':p['gbar'],
            'untransferred_dyadic_bound':Q(973,8640),
            'interpretation':'smaller proved profile threshold does not prove actual gap below dyadic number'}


def admitted_gamma(gamma):
    gamma=rational(gamma)
    require(0<=gamma<Q(3,2), 'outside proved sufficient growing-window range')
    return gamma


def profile_and_time_fixtures(link_count):
    rows=[]
    for n in [2,4,8,16,32]:
        q=1-Q(1,n*n)
        p=profile(q)
        require(p['B']==B_classes(q), 'independent class sum differs')
        require(p['norm_V']==Q(1,16), 'canonical budget varies')
        lower,upper=sqrt_enclosure(p['sigma2'])
        coarse=Q(3,16)*(Q(1-q,1+q))**3
        require(p['d_upper_squared']<=coarse<=Q(1,256), 'explicit q>=3/4 fluctuation region failed')
        per_gamma=[]
        for twice_gamma in range(5):
            gamma=Q(twice_gamma,2)
            T=Q(n**twice_gamma) # hbar=alpha=C=1, epsilon=1/n^2.
            terms={'state':6*upper/p['gbar'],'energy':T*p['energy_upper'],
                   'residual':T*upper,'support':T*p['tau']*link_count/3}
            total=sum(terms.values(),Q())
            per_gamma.append({'gamma':gamma,'T':T,'terms_upper':terms,'total_upper':total,
                              'residual_term_squared_exact':T*T*p['sigma2'],
                              'sufficiency_in_scope':gamma<Q(3,2)})
        rows.append({'n':str(n),'profile':p,'sigma_enclosure':[lower,upper],
                     'coarse_d_squared':coarse,'windows':per_gamma})
    endpoint_limit=Q(1,4*5376)
    require(endpoint_limit>0, 'endpoint residual limit vanished')
    variance_floor=Q(1,4)-2*Q(1,16)-4*Q(1,16)**2
    require(variance_floor==Q(7,64), 'variance floor arithmetic failed')
    require(Q(3,5488)<Q(1,256), 'q>=3/4 coarse threshold failed')
    return {'rows':rows,'variance_floor':variance_floor,
            'eta_half_endpoint_residual_squared_limit':endpoint_limit,
            'endpoint_claim':'sufficient bound does not tend to zero; actual endpoint convergence unresolved'}


def encode(obj):
    if isinstance(obj,Q):
        return str(obj)
    if isinstance(obj,G):
        return {'real':str(obj.real),'imag':str(obj.imag)}
    if isinstance(obj,dict):
        return {k:encode(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):
        return [encode(v) for v in obj]
    return obj


def write_json(path,obj):
    path.write_text(json.dumps(encode(obj),indent=2,sort_keys=True)+'\n')


def main(output):
    output=output.absolute()
    nonsymlink(output)
    require(not output.exists(), 'fresh output directory required')
    before=inputs()
    identity_result=profile_identity()
    support,complete=support_fixtures()
    centering=centering_controls()
    sector=sector_control()
    time=profile_and_time_fixtures(len(complete))
    controls={
        'complex_adjoint_centering':True,'both_mean_product_terms':True,
        'omitted_ground_energy_shift_rejected':True,'trace_distance_factor_one_rejected':True,
        'incomplete_displayed_support_rejected':True,'reference_evolution_retains_full_factor':True,
        'profile_own_gap_rechecked':True,'dyadic_gap_transfer_unsupported':True,
        'endpoint_sufficiency_rejected':rejected(lambda:admitted_gamma(Q(3,2))),
        'beyond_endpoint_sufficiency_rejected':rejected(lambda:admitted_gamma(Q(2))),
        'negative_gamma_rejected':rejected(lambda:admitted_gamma(Q(-1))),
        'boolean_gamma_rejected':rejected(lambda:admitted_gamma(True)),
        'boolean_q_rejected':rejected(lambda:profile(True)),
        'float_q_rejected':rejected(lambda:profile(0.5)),
        'q_zero_rejected':rejected(lambda:profile(Q(0))),
        'q_endpoint_rejected':rejected(lambda:profile(Q(1))),
        'eta_zero_rejected':rejected(lambda:profile(Q(1,2),eta=Q(0))),
        'eta_one_rejected':rejected(lambda:profile(Q(1,2),eta=Q(1))),
        'boolean_eta_rejected':rejected(lambda:profile(Q(1,2),eta=True)),
        'zero_alpha_rejected':rejected(lambda:profile(Q(1,2),alpha=Q(0))),
        'zero_reference_scale_rejected':rejected(lambda:profile(Q(1,2),E_star=Q(0))),
        'zero_hbar_rejected':rejected(lambda:profile(Q(1,2),hbar=Q(0))),
        'boolean_hbar_rejected':rejected(lambda:profile(Q(1,2),hbar=True)),
        'negative_root_rejected':rejected(lambda:sqrt_enclosure(Q(-1))),
        'boolean_precision_rejected':rejected(lambda:sqrt_enclosure(Q(1),True)),
        'endpoint_actual_nonconvergence_not_inferred':True,
    }
    for gamma in [Q(0),Q(1,2),Q(1),Q(149,100)]:
        require(admitted_gamma(gamma)==gamma,'valid sufficient exponent rejected')
    require(controls and all(type(v) is bool and v for v in controls.values()),'control failed')
    require(inputs()==before,'scientific sources changed during execution')
    comparison={'connected_error_projector_coefficient':'6','time_window_exponent_upper':'3/2',
                'time_window_endpoint_included':False,'fixed_time_error_exponent':'3/2',
                'physical_sector_rechecked':True,'variance_floor_fixture':'7/64',
                'homogeneous_limit_obtained':False}
    result={'schema':'ym21-forward-m2-v1','loop':'m2','direction':'forward','passed':True,
            'comparison':comparison,'source_hashes':before,'profile_identity':identity_result,
            'support':support,'centering':centering,'sector_control':sector,'profile_time_fixtures':time,
            'controls':controls,
            'theorem':{
                'bound':'||A||||B||[6d+(|t|/hbar)(|e|+sigma+2alpha tau D_FB)]',
                'uniform_bound':'||A||||B||[6sigma/gbar+(T/hbar)(sigma^2/gbar+sigma+alpha tau |E(FB)|/3)]',
                'physical_space':'closure(A_phys Psi_q)=H_inv, a proper reducing subspace of H_full',
                'domain':'D(K_phys)=D(H_ref) intersect H_inv',
                'physical_gap':'at least gbar-e_q, hence at least alpha(1-eta)/8',
                'variance_condition':'sigma^2/gbar^2<=1/256',
                'variance_simple_region':'((1-q)/(1+q))^3 <= (1-eta)^2/(48 eta^2)',
                'time_range':'T=(hbar/alpha) C (1-q)^(-gamma), fixed C>0, 0<=gamma<3/2',
                'rate':'O((1-q)^(3/2-gamma)) for fixed bounded local A,B',
                'endpoint':'actual convergence unresolved; displayed sufficient bound is nonvanishing'},
            'scope':['canonical summable selected-strip profile only','fixed physical scales and spacing',
                     'fixed local observables and complete factor covers','no conditional mobility matching',
                     'no homogeneous or continuum conclusion','exact analytic fixtures, not measured data',
                     'scientific priority unverified','tenth loop only; no further loop executed']}
    output.mkdir(parents=True)
    write_json(output/'results.json',result)
    write_json(output/'controls.json',controls)
    write_json(output/'source-manifest.json',{'schema':'ym21-source-manifest-v1','loop':'m2','direction':'forward',
               'inputs':before,'outputs':{n:sha(output/n) for n in ['results.json','controls.json']}})
    print(json.dumps({'loop':'m2','direction':'forward','passed':True,'controls':len(controls),
                      'comparison':comparison,'results_sha256':sha(output/'results.json')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    main(parser.parse_args().output)
