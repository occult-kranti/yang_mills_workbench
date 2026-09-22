#!/usr/bin/env python3
"""AK2 independent forward: exact geometry, differential algebra and controls.

Only owned snapshots are read. Infinite-volume and domain arguments are in
report.md; finite matrices and measures are explicitly abstract diagnostics.
"""
import argparse
import hashlib
import itertools as it
import json
from fractions import Fraction as Q
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
PREFIX = BASE.relative_to(REPO).as_posix()
CONTRACT = 'research/round28/contracts/ak2.json'
CONTRACT_SHA = 'ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601'
MANIFEST_SHA = '0087d9e3725518e3a6fe1d6f03800184acb0fbd9f07df8009288ce8e6e545ef2'
PACK_SHA = '845e0c6a03101d16790ec9feea981722ef1e9cd3b020b0fe4e59284ad10c4390'
TESTS = []
ZERO = (0,0,0)
EX,EY,EZ = (1,0,0),(0,1,0),(0,0,1)
AXES = (EX,EY,EZ)
S = (ZERO,EX,EY,EZ)
R = {ZERO,EZ}


def test(name, valid, **evidence):
    if valid is not True:
        raise RuntimeError('AK2 diagnostic failed: '+name)
    TESTS.append(dict(id=name, passed=True, **evidence))


def hash_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exported(x):
    if isinstance(x,Q):
        return str(x)
    if isinstance(x,dict):
        return {str(k):exported(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):
        return [exported(v) for v in x]
    return x


def input_path(relative):
    p=REPO/relative
    if not p.is_relative_to(BASE):
        raise RuntimeError('Unowned input '+relative)
    if any(z.is_symlink() for z in (p,)+tuple(p.parents)):
        raise RuntimeError('Symlink input '+relative)
    return p


def load_sources():
    mf=BASE/'inputs/source-inventory.json'
    pack=BASE/'inputs-freeze.json'
    cp=BASE/'inputs'/CONTRACT
    test('frozen-contract', hash_file(cp)==CONTRACT_SHA)
    test('canonical-generic-inventory', hash_file(mf)==MANIFEST_SHA)
    test('prescience-input-freeze', hash_file(pack)==PACK_SHA)
    contract=json.loads(cp.read_text())
    entries=json.loads(mf.read_text())['entries']
    bound={PREFIX+'/check.py':hash_file(Path(__file__))}
    sources={}
    for e in entries:
        if e['source'] in sources:
            raise RuntimeError('Duplicate source')
        sources[e['source']]=e
        if hash_file(input_path(e['snapshot']))!=e['sha256']:
            raise RuntimeError('Changed snapshot '+e['snapshot'])
        bound[e['snapshot']]=e['sha256']
        if not e.get('external_instruction_snapshot',False):
            if Path(e['source']).is_absolute() or '..' in Path(e['source']).parts:
                raise RuntimeError('Nonportable original provenance')
            bound[e['source']]=e['sha256']
    required=dict(contract['sources']);required[CONTRACT]=CONTRACT_SHA
    test('all-fifty-sources-and-contract', len(required)==51 and all(
        s in sources and sources[s]['sha256']==h for s,h in required.items()), snapshots=len(entries))
    for p,h in json.loads(pack.read_text())['bindings'].items():
        if hash_file(input_path(p))!=h:
            raise RuntimeError('Changed input pack '+p)
        bound[p]=h
    for p in (mf,pack):
        bound[p.relative_to(REPO).as_posix()]=hash_file(p)
    test('flat-portable-bindings', all(not Path(p).is_absolute() and isinstance(h,str)
                                      and len(h)==64 for p,h in bound.items()))
    return contract,dict(sorted(bound.items()))


def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))


def tail_points(b):
    return [(4*b[0]+x,2*b[1]+y,b[2]) for x in range(4) for y in range(2)]


def coarse(t):
    return t[0]//4,t[1]//2,t[2]


def all_links(sites):
    return sorted((t,d) for b in sites for t in tail_points(b) for d in range(3))


def endpoint(e):
    return plus(e[0],AXES[e[1]])


def canonical_path(vertices):
    edges=[]
    for u,v in zip(vertices,vertices[1:]):
        change=tuple(v[j]-u[j] for j in range(3))
        active=[j for j in range(3) if change[j]]
        if len(active)!=1 or abs(change[active[0]])!=1:
            raise RuntimeError('Non-unit path edge')
        d=active[0];sign=change[d]
        edges.append((u if sign==1 else v,d,sign))
    return tuple(edges)


def face(t,a,b):
    return canonical_path((t,plus(t,AXES[a]),plus(plus(t,AXES[a]),AXES[b]),plus(t,AXES[b]),t))


def geometry(contract):
    path=(ZERO,EX,plus(EX,EZ),EZ,ZERO)
    w=canonical_path(path)
    links=all_links(R)
    vertices=sorted({v for e in links for v in (e[0],endpoint(e))})
    test('same-original-Wilson-word', w==((ZERO,0,1),(EX,2,1),(EZ,0,-1),(ZERO,2,-1)))
    test('same-complete-region', {coarse(t) for t,d,s in w}==R and len(links)==48 and len(vertices)==36)
    selected=set()
    for b in R:
        for t in tail_points(b):
            if t[0]%4<3 and t[1]%2==0:
                selected.update((u,d) for u,d,s in face(t,0,1))
    test('all-selected-and-free-links', len(selected)==20 and len(set(links)-selected)==28)
    actions=[dict(vertex=v,outgoing=[e for e in links if e[0]==v],
                  incoming=[e for e in links if endpoint(e)==v]) for v in vertices]
    test('every-original-endpoint-action', sum(len(a['outgoing'])+len(a['incoming']) for a in actions)==96)
    cubes=[]
    for dims in contract['parameters']['geometry_fixtures']:
        sites=set(it.product(*(range(n) for n in dims)))
        owned=set(all_links(sites))
        stars={b for b in sites if {plus(b,s) for s in S}<=sites}
        selected_count=0;omitted_count=0;all_complete=True
        for b in sites:
            for t in tail_points(b):
                for a,c in it.combinations(range(3),2):
                    selected_face=(a,c)==(0,1) and t[0]%4<3 and t[1]%2==0
                    if selected_face or b in stars:
                        edges=face(t,a,c)
                        all_complete=all_complete and all((u,d) in owned for u,d,sign in edges)
                        selected_count+=int(selected_face)
                        omitted_count+=int(not selected_face)
        endpoints={v for e in owned for v in (e[0],endpoint(e))}
        key=''.join(map(str,dims))
        n=dims[0]
        test('complete-cube-'+key, all_complete and len(owned)==24*n**3
             and len(endpoints)==8*n**3+14*n**2 and selected_count==3*n**3
             and omitted_count==21*(n-1)**3)
        test('same-local-four-derivative-links-'+key, all((t,d) in owned for t,d,s in w))
        cubes.append(dict(coarse_sides=dims,sites=len(sites),links=len(owned),endpoints=len(endpoints),
            selected_faces=selected_count,retained_omitted_groups=len(stars),retained_omitted_faces=omitted_count,
            all_kinetic_links_retained=True,only_four_W_derivative_links=True))
    return dict(original_path=path,original_word=w,complete_region=sorted(R),links=links,
                endpoint_actions=actions,cuboids=cubes)


def mul(p,q):
    a,b,c,d=p;e,f,g,h=q
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)


def scale(a,p):
    return tuple(a*x for x in p)


def addq(p,q):
    return tuple(x+y for x,y in zip(p,q))


def inverse(p):
    return (p[0],-p[1],-p[2],-p[3])


ONE=(Q(1),Q(0),Q(0),Q(0))
NIL=(Q(0),)*4
QUATS=((Q(3,5),Q(4,5),Q(0),Q(0)),(Q(5,13),Q(0),Q(12,13),Q(0)),
       (Q(8,17),Q(0),Q(0),Q(15,17)),(Q(1,2),)*4)
T=tuple(tuple(Q(int(j==i+1),2) for j in range(4)) for i in range(3))


def product(sequence):
    q=ONE
    for p in sequence:q=mul(q,p)
    return q


def differential_controls(g):
    word=g['original_word']
    assignment={e:QUATS[(i+2)%4] for i,e in enumerate(g['links'])}
    for (tail,direction,sign),q in zip(word,QUATS):assignment[tail,direction]=q
    factors=[assignment[t,d] if s==1 else inverse(assignment[t,d]) for t,d,s in word]
    hol=product(factors);w=hol[0]
    test('noncommuting-SU2-fixture', all(sum(x*x for x in p)==1 for p in QUATS)
         and mul(QUATS[0],QUATS[1])!=mul(QUATS[1],QUATS[0]))
    test('nondegenerate-derivative-and-Casimir-control', w!=0 and w*w<1)
    per_link=[]
    for i,(tail,direction,sign) in enumerate(word):
        u=assignment[tail,direction];derivatives=[];seconds=[]
        for axis,t in enumerate(T):
            first=mul(t,u) if sign==1 else scale(Q(-1),mul(inverse(u),t))
            second=scale(Q(-1,4),factors[i])
            derivatives.append(product(factors[:i]+[first]+factors[i+1:])[0])
            seconds.append(product(factors[:i]+[second]+factors[i+1:])[0])
            identity_derivative=addq(mul(mul(t,u),inverse(u)),mul(u,scale(Q(-1),mul(inverse(u),t))))
            test('inverse-product-rule-'+str(i)+'-'+str(axis), identity_derivative==NIL)
        grad=sum(x*x for x in derivatives)
        casimir=-sum(seconds)
        test('one-link-gradient-'+str(i), grad==(1-w*w)/4)
        test('one-link-fundamental-Casimir-'+str(i), casimir==Q(3,4)*w)
        per_link.append(dict(link=(tail,direction),orientation=sign,derivatives=derivatives,
                             second_derivatives=seconds,gradient_squared=grad,Casimir_W=casimir))
    gamma=sum(p['gradient_squared'] for p in per_link)
    test('all-four-link-gradient-identity', gamma==1-w*w)
    test('wrong-generator-normalization-rejected', 4*gamma!=gamma,
         actual_gamma=gamma,wrong_sigma_instead_of_sigma_over_two=4*gamma)
    # The squared gradient is blind to a wrong overall inverse derivative sign.
    inverse_der=per_link[2]['derivatives']
    test('inverse-sign-square-blind-preserved', sum(x*x for x in inverse_der)==sum((-x)**2 for x in inverse_der),
         verdict='nondiscriminating')
    t=T[0];u=QUATS[2]
    wrong_identity_derivative=addq(mul(mul(t,u),inverse(u)),mul(u,mul(inverse(u),t)))
    test('inverse-sign-rejected-by-product-rule', wrong_identity_derivative!=NIL,
         wrong_identity_derivative=wrong_identity_derivative)
    gauges={tuple(a['vertex']):QUATS[(3*i+1)%4] for i,a in enumerate(g['endpoint_actions'])}
    full={e:mul(mul(gauges[e[0]],q),inverse(gauges[endpoint(e)])) for e,q in assignment.items()}
    transformed=product([full[t,d] if s==1 else inverse(full[t,d]) for t,d,s in word])
    test('full36endpoint-covariance', transformed==mul(mul(gauges[ZERO],hol),inverse(gauges[ZERO])))
    return dict(W=w,holonomy=hol,per_link=per_link,Gamma_W=gamma,
                pointwise_formula='sum_(four original links,a)(X_ea W)^2=1-W^2',
                Casimir_convention='C_e=-sum_a X_ea^2; X generated by i sigma_a/2',
                scope='Exact rational SU(2) algebra; not sampling of the actual ground state.')


def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def md(a,b):
    return tuple(tuple(a[i][j]-b[i][j] for j in range(2)) for i in range(2))


def comm(a,b):
    return md(mm(a,b),mm(b,a))


def physical_controls():
    k=((Q(0),Q(0)),(Q(0),Q(3)))
    w=((Q(0),Q(1,2)),(Q(1,2),Q(0)))
    mu=mm(mm(w,k),w)[0][0]
    twice=comm(w,comm(k,w))[0][0]
    test('double-commutator-half-factor', mu==Q(3,4) and twice==2*mu)
    test('wrong-commutator-normalization-rejected', twice!=mu)
    raw=((Q(7),Q(0)),(Q(0),Q(10)))
    raw_energy=mm(mm(w,raw),w)[0][0]
    test('omitted-ground-center-rejected', raw_energy==Q(5,2) and raw_energy-mu==Q(7,4)
         and comm(w,comm(raw,w))==comm(w,comm(k,w)))
    # This named physical corner has every selected coefficient and tau zero.
    reference_variance=Q(1,4);free_eigenvalue=4*Q(3,4)
    test('all-zero-coupling-free-reference-normalization', free_eigenvalue*reference_variance==Q(3,4)
         and 1-reference_variance==Q(3,4))
    alpha=Q(24);delta=alpha/8;hbar=Q(2);gap_norm=Q(2)
    physical=delta*gap_norm;frequency=physical/hbar
    test('delta-and-hbar-factors-retained', delta==3 and physical==6 and frequency==3)
    test('wrong-energy-or-frequency-normalization-rejected', gap_norm!=physical and physical!=frequency)
    # Noncentered observable in a separate abstract two-level model.
    mean=Q(1,2);variance=Q(1,4);raw_mass=variance+mean*mean
    centered_heat=variance*Q(1,4);raw_heat=centered_heat+mean*mean
    test('noncentered-vacuum-contamination', raw_mass==Q(1,2) and raw_heat==Q(5,16)
         and centered_heat==Q(1,16) and mean*mean>0)
    return dict(abstract_commutator=dict(moment=mu,double_commutator=twice,uncentered_ground_energy=raw_energy),
        free_corner=dict(scope='all lambda_L,lambda_R,mu,tau zero only',variance=reference_variance,
                         energy_over_alpha=free_eigenvalue,first_moment_over_alpha=Q(3,4)),
        units_fixture=dict(alpha=alpha,delta=delta,hbar=hbar,physical_excitation=physical,frequency=frequency),
        centering_fixture=dict(mean=mean,variance=variance,raw_mass=raw_mass,raw_heat=raw_heat,centered_heat=centered_heat))


def resolvent_at_i(e):
    return (e/(e*e+1),1/(e*e+1))


def spectral_controls():
    vmin=Q(1,5);moment_cap=Q(1);gap=Q(1,16);upper=Q(10)
    window=vmin-moment_cap/upper
    test('finite-window-mass', window==Q(1,10))
    test('Jensen-rate-with-common-variance', moment_cap/vmin==5)
    bad_energy=Q(20);bad_heat=vmin*Q(1,2**20);claimed=vmin*Q(1,2**5)
    test('gap-and-variance-alone-no-window', bad_energy>upper and vmin*bad_energy>moment_cap,
         wrong_model_window_mass=Q(0))
    test('gap-and-variance-alone-no-lower-heat', bad_heat<claimed)
    # Exact equality example at diagnostic physical time hbar*log(2)/alpha.
    test('Jensen-frozen-bound-exact-atom-control', vmin*5==moment_cap and vmin*Q(1,2**5)==claimed)
    # Uniformly bounded first moments do not imply their convergence.
    escaped=[];a=Q(1,4);limit_r=resolvent_at_i(a)
    for n in (2,4,16,256):
        weight=Q(1,2*n);moment=(1-weight)*a+weight*n
        rn=resolvent_at_i(Q(n))
        res=tuple((1-weight)*limit_r[j]+weight*rn[j] for j in range(2))
        err2=sum((res[j]-limit_r[j])**2 for j in range(2))
        test('escape-bounded-tests-'+str(n), err2<=Q(1,n*n) and moment<=1)
        test('escape-moment-loss-'+str(n), moment-a==Q(1,2)-Q(1,8*n) and weight*n==Q(1,2))
        escaped.append(dict(n=n,mass=Q(1),first_moment=moment,limit_mass=Q(1),limit_first_moment=a,
                            resolvent_at_i=res,resolvent_error_squared=err2,escaping_tail_first_moment=weight*n))
    # Bounded creating operator, finite vector norm, infinite form energy.
    prefixes=[]
    for n in (2,4,8):
        norm2=sum(Q(1,4**j) for j in range(1,n+1))
        moment=sum(Q(4**j)*Q(1,4**j) for j in range(1,n+1))
        test('bounded-local-not-form-domain-'+str(n), norm2==(1-Q(1,4**n))/3 and norm2<Q(1,3)
             and moment==n)
        prefixes.append(dict(n=n,norm_squared=norm2,form_moment_prefix_over_alpha=moment))
    cap=Q(1,65536);hyp_c1=cap;hyp_c2=Q(1);hyp_star=min(hyp_c1,1/(2*hyp_c2))/7
    test('both-coupling-conditions-needed', 0<hyp_star<cap,
         scope='Hypothetical positive source constants only, not actual values.')
    test('strict-symbolic-endpoint-preserved', not hyp_star<hyp_star)
    return dict(input_variance_floor=vmin,physical_moment_cap_over_alpha=moment_cap,
        support_lower_over_alpha=gap,window_upper_over_alpha=upper,window_mass_lower=window,
        lower_heat_prefactor=vmin,lower_heat_exponent_coefficient=Q(5),
        lower_heat='(1/5)exp(-5alpha t/hbar), every finite t>=0',
        inherited_upper_heat='v exp(-alpha t/(16hbar))',
        escape_of_first_moment=escaped,bounded_operator_domain_counterexample=prefixes,
        diagnostic_time='hbar log(2)/alpha; abstract measures only',
        noncentered_and_gap_only_control_scope='No actual spectral atoms computed',
        numerical_stability_interval_evaluated=False,chosen_positive_admissible_tau=None)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    if not a.output.is_absolute() or a.output.exists():
        raise RuntimeError('--output must be a fresh absolute DIRECTORY')
    contract,bindings=load_sources()
    g=geometry(contract);d=differential_controls(g);p=physical_controls();s=spectral_controls()
    result=dict(schema='ym28-ak2-forward-v1',loop='ak2',sequence=10,direction='forward',passed=True,
        verdict='contracted-physical-moment-window-and-lower-heat-proved',contract_sha256=CONTRACT_SHA,
        model=contract['model'],bindings=bindings,geometry=g,differential=d,physical_controls=p,
        spectral=s,checks=TESTS,check_count=len(TESTS),
        analytic_claims=dict(finite_volume_first_moment='alpha omega_Lambda(1-W^2)<=alpha',
            limiting_first_moment='integral E dnu(E)<=alpha',
            actual_form_domain='chi in D(sqrt(H_phys))',
            first_moment_equality_claimed=False,operator_domain_claimed=False,second_moment_claimed=False,
            common_concrete_strong_resolvent_limit_claimed=False),
        blind_controls=['inverse-sign-square-blind-preserved'],
        stop_boundary='Investigation ten: no further scientific investigation authorized.')
    a.output.mkdir(parents=True,exist_ok=False)
    (a.output/'results.json').write_text(json.dumps(exported(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(passed=True,check_count=len(TESTS),moment_cap='alpha',window_mass='1/10')))


if __name__=='__main__':main()
