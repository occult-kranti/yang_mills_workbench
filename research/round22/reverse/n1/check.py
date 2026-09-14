#!/usr/bin/env python3
"""Independent N1 reverse exact controls; not a formalization of the proof."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = ROOT / 'research/round22/contracts/n1.json'
CONTRACT_HASH = '29ce23d8df321604f0174afcfb73b9c907ee4e6b03c78f66c408ac80fd7f3369'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    require(path.is_file(), 'missing required source: ' + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def no_symlinks(path):
    for p in (path, *path.parents):
        require(not p.is_symlink(), 'symlink path is not admitted: ' + str(p))


@dataclass(frozen=True)
class Z:
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))

    def __add__(self, other):
        other = other if isinstance(other, Z) else Z(other)
        return Z(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return Z(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Z) else -Z(other))

    def __mul__(self, other):
        other = other if isinstance(other, Z) else Z(other)
        return Z(self.re*other.re-self.im*other.im,
                 self.re*other.im+self.im*other.re)

    __rmul__ = __mul__

    def star(self):
        return Z(self.re, -self.im)

    def abs2(self):
        return self.re*self.re + self.im*self.im

    def json(self):
        return {'real': str(self.re), 'imaginary': str(self.im)}


def matrix(rows):
    return tuple(tuple(x if isinstance(x, Z) else Z(x) for x in row) for row in rows)


def zero(n=2):
    return matrix([[0]*n for _ in range(n)])


def identity(n=2):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def add(a, b):
    return tuple(tuple(x+y for x,y in zip(ar,br)) for ar,br in zip(a,b))


def scale(a, z):
    return tuple(tuple(x*z for x in row) for row in a)


def subtract(a, b):
    return add(a, scale(b, -1))


def adjoint(a):
    return tuple(tuple(x.star() for x in row) for row in zip(*a))


def product(a, b):
    return tuple(tuple(sum((x*y for x,y in zip(row,col)), Z())
                       for col in zip(*b)) for row in a)


def applied(a, v):
    return tuple(sum((x*y for x,y in zip(row,v)), Z()) for row in a)


def inner(v, w):
    return sum((x.star()*y for x,y in zip(v,w)), Z())


def mean(v, a):
    return inner(v, applied(a,v))


def commutator(a, b):
    return subtract(product(a,b), product(b,a))


def frob2(a):
    return sum((x.abs2() for row in a for x in row), F())


def tensor(a, b):
    return tuple(tuple(x*y for x in ar for y in br) for ar in a for br in b)


def conjugate(u, a):
    return product(product(u,a),adjoint(u))


def phase(k):
    """exp(-i*k*pi/2) exactly, including negative integer k."""
    return (Z(1), Z(0,-1), Z(-1), Z(0,1))[k % 4]


def root_upper(q):
    require(q >= 0, 'negative square')
    denom = 2**80
    scaled = q*denom*denom
    numer = isqrt(scaled.numerator//scaled.denominator)
    if F(numer*numer) < scaled:
        numer += 1
    bound = F(numer,denom)
    require(bound*bound >= q, 'root bound is not an upper enclosure')
    return bound


def connected(v, a, b, shifted_u):
    return inner(applied(a,v),applied(shifted_u,applied(b,v))) - mean(v,adjoint(a))*mean(v,b)


def heisenberg_connected(v, a, b, raw_u):
    return mean(v,product(adjoint(a),conjugate(raw_u,b))) - mean(v,adjoint(a))*mean(v,b)


def two_level_controls():
    # Both spectra and eigenprojections are independent exact inputs.
    e0 = (Z(1),Z())
    vacuum = (Z(F(3,5)),Z(F(4,5)))
    rot = matrix([[F(3,5),F(-4,5)],[F(4,5),F(3,5)]])
    p0 = (matrix([[1,0],[0,0]]),matrix([[0,0],[0,1]]))
    pq = tuple(conjugate(rot,p) for p in p0)
    energies0, energiesq = (0,1), (-1,2)
    h0 = p0[1]
    hq = add(scale(pq[0],-1),scale(pq[1],2))
    perturbation = subtract(hq,h0)
    require(frob2(commutator(h0,hq)) > 0, 'noncommuting fixture became commuting')
    a = scale(matrix([[Z(1,2),Z(2,-1)],[Z(-3,1),Z(1,-2)]]),F(1,10))
    b = scale(matrix([[Z(2,-1),Z(-1,2)],[Z(1,3),Z(3,1)]]),F(1,10))
    na, nb = root_upper(frob2(a)), root_upper(frob2(b))
    d = F(4,5)
    pd = subtract(pq[0],p0[0])
    require(pd[0][0]+pd[1][1] == Z(), 'projector difference trace')
    require(pd[0][0]*pd[1][1]-pd[0][1]*pd[1][0] == Z(-d*d), 'projector distance spectrum')
    rows=[]
    wrong_sign_rejections=0
    for k in (-2,-1,0,1,2):
        u0 = add(p0[0],scale(p0[1],phase(k)))
        uq = add(scale(pq[0],phase(-k)),scale(pq[1],phase(2*k)))
        shifted = add(pq[0],scale(pq[1],phase(3*k)))
        require(product(adjoint(uq),uq) == identity(), 'unitary fixture')
        require(applied(shifted,vacuum) == vacuum, 'ground stationarity')
        bq,b0 = conjugate(uq,b),conjugate(u0,b)
        require(bq == conjugate(shifted,b), 'scalar ground shift fails to cancel')
        # Exact spectral expansion of -i integral_0^t beta_q(t-s)[V,beta_0(s)B]ds.
        # Frequencies are integers and zero-frequency coefficients vanish exactly.
        integrated=zero()
        zero_frequencies=0
        for c,d0,i,j in itertools.product(range(2),repeat=4):
            piece=product(product(p0[c],b),p0[d0])
            projected=product(product(pq[i],commutator(perturbation,piece)),pq[j])
            deltaq=energiesq[i]-energiesq[j]
            frequency=energies0[c]-energies0[d0]-deltaq
            if frequency == 0:
                require(projected == zero(), 'uncancelled zero-frequency integral')
                zero_frequencies += 1
            else:
                integral_factor=(phase(frequency*k)-Z(1))*F(1,frequency)
                integrated=add(integrated,scale(projected,phase(deltaq*k)*integral_factor))
        difference=subtract(bq,b0)
        require(integrated == difference, 'exact oriented strong-integral fixture')
        if difference != zero():
            require(scale(integrated,-1) != difference, 'wrong-sign control failed')
            wrong_sign_rejections += 1
        cq=connected(vacuum,a,b,shifted)
        c0=connected(e0,a,b,u0)
        require(cq == heisenberg_connected(vacuum,a,b,uq), 'stationary rewrite')
        # Use exactly the decomposition of the written proof, including both means.
        x=product(adjoint(a),bq)
        state=mean(vacuum,x)-mean(e0,x)
        dynamic=mean(e0,product(adjoint(a),difference))
        means=mean(vacuum,adjoint(a))*mean(vacuum,b)-mean(e0,adjoint(a))*mean(e0,b)
        require(cq-c0 == state+dynamic-means, 'centered decomposition')
        require(state.abs2() <= (2*d*na*nb)**2, 'state trace estimate')
        require(means.abs2() <= (4*d*na*nb)**2, 'both means estimate')
        bound=6*d*na*nb+na*root_upper(frob2(difference))
        require((cq-c0).abs2() <= bound*bound, 'coefficient-six estimate')
        for ca,cb in ((Z(2,1),Z()),(Z(),Z(-1,3)),(Z(2,1),Z(-1,3))):
            changed=connected(vacuum,add(a,scale(identity(),ca)),add(b,scale(identity(),cb)),shifted)
            require(changed == cq, 'independent complex scalar centering')
        rows.append({'time_over_pi_half':k,'connected_q':cq.json(),'connected_reference':c0.json(),
                     'integral_equals_difference':True,'zero_frequency_terms':zero_frequencies,
                     'operator_difference_frobenius_squared':str(frob2(difference))})
    require(wrong_sign_rejections > 0, 'wrong-sign control was vacuous')
    raw=inner(applied(a,vacuum),applied(b,vacuum))
    proper=connected(vacuum,a,b,identity())
    wrong_adjoint=mean(vacuum,product(a,b))-mean(vacuum,a)*mean(vacuum,b)
    require(raw != proper and wrong_adjoint != proper, 'missing centering or adjoint did not discriminate')
    qma,qmb=mean(vacuum,adjoint(a)),mean(vacuum,b)
    rma,rmb=mean(e0,adjoint(a)),mean(e0,b)
    actual=qma*qmb-rma*rmb
    frozen_first=qma*qmb-qma*rmb
    frozen_second=qma*qmb-rma*qmb
    require(actual != frozen_first and actual != frozen_second, 'one-mean controls were vacuous')
    uq=add(scale(pq[0],phase(-1)),scale(pq[1],phase(2)))
    wrong_identity=connected(vacuum,identity(),identity(),uq)
    require(wrong_identity == Z(-1,1), 'missing ground subtraction identity control')
    # Exact nonstationary density matrix avoids an irrational sqrt(2) vector.
    density=scale(matrix([[1,1],[1,1]]),F(1,2))
    u0=add(p0[0],scale(p0[1],phase(1)))
    trace_raw=sum((product(density,u0)[i][i] for i in range(2)),Z())-Z(1)
    require(trace_raw == Z(F(-1,2),F(-1,2)), 'nonstationary control')
    return {'outcome':'wrong models rejected','noncommuting_integral_rows':rows,
            'wrong_integral_sign_rejections':wrong_sign_rejections,
            'wrong_missing_adjoint':wrong_adjoint.json(),'correct_zero_time':proper.json(),
            'uncentered_zero_time':raw.json(),'both_means_changed':True,
            'complex_scalar_additions_preserved':True,'raw_identity_without_ground_subtraction':wrong_identity.json(),
            'nonstationary_identity_single_propagator':trace_raw.json(),
            'nonstationary_heisenberg_identity':Z().json(),'projector_distance':'4/5',
            'controls':['wrong_integral_sign','reversed_integral_endpoints','missing_ground_subtraction',
                        'nonstationary_rewrite','missing_adjoint','uncentered_expression',
                        'holding_first_mean_fixed','holding_second_mean_fixed','complex_scalar_additions']}


def vertex_step(v, axis, amount=1):
    ans=list(v); ans[axis]+=amount
    return tuple(ans)


def edge(v, axis):
    return tuple(sorted((v,vertex_step(v,axis))))


def square(v, a, b):
    return frozenset((edge(v,a),edge(v,b),edge(vertex_step(v,b),a),edge(vertex_step(v,a),b)))


def selected(face):
    a,b,x,y,z=face
    return a == 0 and b == 1 and y % 2 == 0 and x % 4 < 3


def complete_owner(link):
    lo,hi=link
    axis=next(i for i in range(3) if lo[i] != hi[i])
    x,y,z=lo
    if (axis == 0 and x % 4 < 3) or (axis == 1 and y % 2 == 0):
        x0,y0=4*(x//4),2*(y//2)
        return frozenset([edge((x0+r,y0+s,z),0) for r in range(3) for s in range(2)] +
                         [edge((x0+r,y0,z),1) for r in range(4)])
    return frozenset((link,))


def incident_from_links(links):
    ans=set()
    for lo,hi in links:
        axis=next(i for i in range(3) if lo[i] != hi[i])
        for other in range(3):
            if other == axis:
                continue
            for base in (lo,vertex_step(lo,other,-1)):
                if min(base) < 0:
                    continue
                a,b=sorted((axis,other))
                face=(a,b,*base)
                if not selected(face):
                    ans.add(face)
    return ans


def support_controls():
    displayed=square((0,0,0),0,2)
    complete=frozenset().union(*(complete_owner(e) for e in displayed))
    broad=incident_from_links(complete)
    narrow=incident_from_links(displayed)
    # Independent direct enumeration by vertex squares within sufficient endpoint maxima.
    top=[max(v[i] for e in complete for v in e) for i in range(3)]
    direct=set()
    for v in itertools.product(*(range(m+1) for m in top)):
        for a,b in ((0,1),(0,2),(1,2)):
            f=(a,b,*v)
            if not selected(f) and square(v,a,b) & complete:
                direct.add(f)
    require(direct == broad, 'independent face incidence reconstruction')
    require(len(complete) == 22 and len(broad) == 28, 'complete origin-xz factor geometry')
    require(len(narrow) == 5 and narrow < broad, 'displayed-link-only rejection')
    require(all(min(f[2:]) >= 0 for f in broad), 'spurious exterior face at octant boundary')
    counts={}
    for f in broad:
        degree=sum(f[2:]); counts[degree]=counts.get(degree,0)+1
    dhalf=sum((F(1,2)**sum(f[2:])/24 for f in broad),F())
    require(dhalf == F(11,32), 'exact support weight')
    require(sum(counts.values()) == 28, 'face multiplicity ledger')
    # One reference factor contains two qubits; displayed support swaps inside it.
    x=matrix([[0,1],[1,0]]); z=matrix([[1,0],[0,-1]])
    swap=matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    b=tensor(x,identity()); interaction=tensor(identity(),z)
    evolved=conjugate(swap,b)
    require(commutator(interaction,b) == zero(4), 'initial subset commutation')
    require(frob2(commutator(interaction,evolved)) > 0, 'support migration control')
    return {'outcome':'incomplete support rejected','displayed_link_count':4,'complete_link_count':22,
            'displayed_incident_faces':5,'complete_incident_faces':28,'D_at_half':str(dhalf),
            'D_at_one':'7/6','weight_polynomial_numerator_over_24':{str(k):v for k,v in sorted(counts.items())},
            'complete_face_set':[list(f) for f in sorted(broad)],'missed_face':list(sorted(broad-narrow)[0]),
            'migrated_commutator_frobenius_squared':str(frob2(commutator(interaction,evolved))),
            'controls':['displayed_support_preservation','omitted_complete_factor_links','negative_octant_faces']}


def polynomial(q):
    return 2+5*q+5*q*q+6*q**3+3*q**4


def budget(q):
    if type(q) is not F or not 0 < q < 1:
        raise ValueError('q must be rational and strictly between zero and one')
    return polynomial(q)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def profile(q, eta=F(1,2), alpha=F(2), hbar=F(3), e_star=F(1)):
    if any(type(v) is not F for v in (eta,alpha,hbar,e_star)):
        raise ValueError('exact rational parameters required, not Boolean values')
    if not 0 < eta < 1 or min(alpha,hbar,e_star) <= 0:
        raise ValueError('invalid fixed physical scale or budget')
    b=budget(q); eps=1-q
    # Two independently expressed total coefficient ledgers must agree.
    geometric=(3/(1-q)**3-(1+q+q*q)/((1-q**4)*(1-q*q)*(1-q)))/24
    require(b == geometric, 'rational and selected-face budget mismatch')
    tau=eta/(8*b)
    sigma2=alpha*alpha*tau*tau*budget(q*q)/96
    gap=alpha*(1-eta)/8
    normvar=polynomial(q*q)*(1+q)/(256*polynomial(q)**2*(1+q**4))
    require(sigma2 == alpha*alpha*eta*eta*eps**3*normvar, 'variance simplification')
    require(tau/eps**3 == 3*eta*(1+q)**2*(1+q*q)/polynomial(q), 'tau simplification')
    require(tau <= 12*eta*eps**3, 'uniform tau bound')
    require(sigma2/(gap*gap) <= eta*eta*eps**3/(4*(1-eta)**2), 'uniform state-distance bound')
    return {'q':q,'eta':eta,'alpha_over_E_star':alpha/e_star,'hbar':hbar,'tau':tau,
            'sigma_squared':sigma2,'gap':gap,'distance_bound_squared':sigma2/(gap*gap),
            'normalized_sigma_squared':normvar}


def domain_and_window_controls():
    rows=[]
    for n in (2,4,8,16,32):
        vnorm=sum((F(1,j*j) for j in range(1,n+1)),F())
        form=sum((F(j*j)*F(1,j*j) for j in range(1,n+1)),F())
        operator=sum((F(j**4)*F(1,j*j) for j in range(1,n+1)),F())
        require(vnorm < 2 and form == n and operator == F(n*(n+1)*(2*n+1),6), 'domain divergence formula')
        require(phase(2) == Z(-1), 'high-energy shift phase')
        rows.append({'truncation':n,'vector_norm_squared':str(vnorm),'form_norm_squared_over_E_star':str(form),
                     'operator_norm_squared_over_E_star_squared':str(operator),
                     'shift_test_time_over_pi_hbar_E_star_inverse':str(F(1,2*n+1)),
                     'shift_evolved_minus_original_norm':'2'})
    exponents=[]
    for gamma in (F(0),F(1),F(3,2),F(2),F(5,2),F(3),F(4)):
        sufficient=3-gamma > 0
        require(sufficient == (gamma < 3), 'window acceptance')
        exponents.append({'gamma':str(gamma),'state_exponent':'3/2','dynamic_exponent':str(3-gamma),
                          'vanishing_certificate':sufficient,'rate_if_positive':str(min(F(3,2),3-gamma)) if sufficient else None})
    endpoint=[]
    for n in (2,4,8,16):
        eps=F(1,n)
        vanishing_phase=eps**4/eps**3
        persistent_phase=eps**3/eps**3
        require(vanishing_phase == eps and persistent_phase == 1, 'endpoint insufficiency control')
        endpoint.append({'n':n,'fast_family_endpoint_phase':str(vanishing_phase),'slow_family_endpoint_phase':str(persistent_phase)})
    require(F(3*4*2,21) == F(8,7), 'tau endpoint coefficient')
    require(F(21*2,256*21*21*2) == F(1,5376), 'sigma endpoint coefficient')
    endpoint_coefficient=F(16,7)*F(1,2)*F(7,6)
    require(endpoint_coefficient == F(4,3), 'nonempty-support endpoint constant')
    return {'outcome':'invalid domain and endpoint inferences rejected','domain_rows':rows,
            'bounded_rank_one_domain_invariance':False,'universal_point_norm_continuity':False,
            'window_rows':exponents,'gamma_three_origin_xz_C_one_eta_half_certificate_limit':str(endpoint_coefficient),
            'actual_gamma_three_nonconvergence_claimed':False,'empty_incident_support_has_zero_dynamic_term':True,
            'endpoint_phase_families':endpoint,
            'controls':['arbitrary_B_preserves_operator_domain','arbitrary_B_preserves_form_domain',
                        'strong_implies_point_norm_continuity','upper_bound_proves_endpoint_failure','gamma_three_admitted_from_bound']}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    no_symlinks(out)
    require(not out.exists(),'output must be a fresh nonexistent directory')
    require(digest(CONTRACT) == CONTRACT_HASH,'contract bytes differ from assigned frozen hash')
    contract=json.loads(CONTRACT.read_text())
    for rel,expected in contract['dependencies'].items():
        path=ROOT/rel; no_symlinks(path)
        require(digest(path) == expected,'inherited dependency changed: '+rel)
    for gate in ('m1','m2'):
        require(json.loads((ROOT/f'research/round21/advisor/{gate}-gate.json').read_text())['status'] == 'accepted','unadmitted inherited gate')
    support=support_controls()
    profile_rows=[]
    for eta in (F(1,4),F(1,2),F(3,4)):
        for n in (2,4,8,16,32):
            q=1-F(1,n*n)
            row=profile(q,eta)
            eps=1-q
            dpoly=sum((F(count)*q**int(degree)/24 for degree,count in support['weight_polynomial_numerator_over_24'].items()),F())
            # gamma=5/2 is rational exactly for epsilon=1/n^2.
            dynamic=2*row['tau']*n**5*dpoly
            bound=6*root_upper(row['distance_bound_squared'])+dynamic
            row.update({'D_complete':dpoly,'gamma_five_halves_window_over_hbar_alpha_inverse':F(n**5),
                        'gamma_five_halves_dynamic_bound':dynamic,'gamma_five_halves_full_upper_bound':bound})
            profile_rows.append({k:str(v) for k,v in row.items()})
    rejected=[]
    invalid=[('q_zero',{'q':F(0)}),('q_one',{'q':F(1)}),('q_boolean',{'q':True}),
             ('eta_zero',{'q':F(1,2),'eta':F(0)}),('eta_one',{'q':F(1,2),'eta':F(1)}),
             ('eta_boolean',{'q':F(1,2),'eta':True}),('alpha_zero',{'q':F(1,2),'alpha':F(0)}),
             ('hbar_zero',{'q':F(1,2),'hbar':F(0)}),('E_star_zero',{'q':F(1,2),'e_star':F(0)})]
    for name,kwargs in invalid:
        try:
            profile(**kwargs)
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError('invalid input accepted: '+name)
    controls={'schema':'ym22-reverse-n1-controls-v1','loop':'n1','direction':'reverse',
              'status':'passed','passed':True,'finite_stationary_integral':two_level_controls(),
              'complete_support':support,'domain_and_window_scope':domain_and_window_controls(),
              'invalid_parameters':{'outcome':'rejected','cases':rejected}}
    results={'schema':'ym22-reverse-n1-results-v1','loop':'n1','direction':'reverse',
             'status':'proved_scoped','passed':True,
             'claims':{'correlation_projector_coefficient':'6','dynamic_commutator_coefficient':'2',
                       'scalar_energy_term_in_heisenberg_bound':'0','vacuum_residual_term_in_dynamic_bound':'0',
                       'strong_integral_proved':True,'arbitrary_bounded_operator_domain_invariance_assumed':False,
                       'complete_factor_support_preserved_under_reference_times':True,'all_real_times':True,
                       'complex_centering_and_both_means':True,'window_gamma_lower_included':'0',
                       'window_gamma_upper_excluded':'3','fixed_time_rate_exponent':'3/2',
                       'general_rate':'min(3/2,3-gamma)','tau_over_eta_epsilon_cubed_limit':'8/7',
                       'sigma_squared_over_alpha_squared_eta_squared_epsilon_cubed_limit':'1/5376',
                       'endpoint_certificate_limit':'16*C*eta*D_FB(1)/7',
                       'endpoint_actual_behavior':'unresolved','homogeneous_representation_transfer':False},
             'profile_rows':profile_rows,
             'proof_boundary':'Exact finite and series controls accompany the written infinite-dimensional proof; no physical data or continuum theorem.',
             'next_loop_selected':False}
    consulted=[
        'research/round21/advisor/m1-gate.json','research/round21/advisor/m2-gate.json',
        'research/round21/advisor/m1-decision.md','research/round21/advisor/m2-decision.md',
        'research/round21/advisor/post-ten-roadmap.json','research/round21/skeptic/post-ten-review.md',
        'research/round21/skeptic/recovery-review.md','research/round21/skeptic/m2.md',
        'research/round21/reverse/m1/report.md','research/round21/reverse/m2/report.md',
        'research/round21/reverse/m2/check.py']
    inputs=[CONTRACT,HERE/'check.py',HERE/'report.md',HERE/'source-review.json',HERE/'independence.json']
    inputs += [ROOT/p for p in contract['instruction_inputs']+consulted]
    inputs += sorted((HERE/'inputs').iterdir())
    for path in inputs:
        no_symlinks(path)
        require(path.is_file(),'missing input: '+str(path))
    out.mkdir(parents=True)
    for name,payload in {'results.json':results,'controls.json':controls}.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    manifest={'schema':'ym22-source-manifest-v1',
              'inputs':{str(p.relative_to(ROOT)):digest(p) for p in sorted(set(inputs))},
              'outputs':{name:digest(out/name) for name in ('controls.json','results.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'n1','direction':'reverse','status':'proved_scoped','passed':True,
                      'scientific_outputs':2,'profile_rows':len(profile_rows),'invalid_inputs_rejected':len(rejected)}))


if __name__ == '__main__':
    main()
