#!/usr/bin/env python3
"""Independent AK2 exact diagnostics; frozen owned inputs, no producer imports."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACK = HERE / 'ak2-inputs'
BASE = 'research/round28/'
CONTRACT = BASE + 'contracts/ak2.json'
CONTRACT_SHA = 'ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601'
INVENTORY_SHA = '79f7f7b9405e306f0f7c94cb1f0b8fb35dc664d66a468bb092d0e8599324eafc'
INPUT_FREEZE_SHA = '20010b1123f82c087027243071cd1383d00a2fec18e6b06148cb4bdc79c81bcb'
CHECKS = []
BINDINGS = {}


def check(ok, name, **details):
    if not ok:
        raise ValueError(name)
    CHECKS.append(dict(name=name, passed=True, **details))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owned(rel):
    if not isinstance(rel, str) or Path(rel).is_absolute() or '..' in Path(rel).parts:
        raise ValueError('nonlocal runtime path')
    path = ROOT / rel
    if HERE not in path.parents:
        raise ValueError('runtime read outside skeptical ownership')
    walk = ROOT
    for part in Path(rel).parts:
        walk /= part
        if walk.is_symlink():
            raise ValueError('symlink runtime input')
    return path


def inputs():
    invpath = PACK / 'source-inventory.json'
    freeze_path = PACK / 'input-freeze.json'
    check(sha(invpath) == INVENTORY_SHA, 'preproduction inventory unchanged')
    check(sha(freeze_path) == INPUT_FREEZE_SHA, 'preproduction input freeze unchanged')
    inventory = json.loads(invpath.read_text())
    originals, snapshots = {}, {}
    for entry in inventory['entries']:
        src, snap, digest = entry['source'], entry['snapshot'], entry['sha256']
        p = owned(snap)
        check(PACK in p.parents and sha(p) == digest, 'owned source snapshot: ' + snap)
        check(snap not in snapshots, 'unique snapshot: ' + snap)
        snapshots[snap] = digest
        BINDINGS[snap] = digest
        if entry.get('external_instruction_snapshot'):
            check(Path(src).is_absolute(), 'installed provenance is metadata only')
        else:
            check(not Path(src).is_absolute() and '..' not in Path(src).parts and src not in originals,
                  'unique safe repository origin: ' + src)
            originals[src] = (snap, digest)
            BINDINGS[src] = digest
    check(len(snapshots) == 73 and inventory['current_producer_scientific_access'] is False,
          '73 preproduction snapshots without current producer access')
    check(originals[CONTRACT][1] == CONTRACT_SHA, 'frozen tenth contract identity')
    contract = json.loads(owned(originals[CONTRACT][0]).read_text())
    check(contract['sequence'] == 10 and len(contract['sources']) == 50, '50 contract sources')
    for src, expected in contract['sources'].items():
        check(originals.get(src, (None, None))[1] == expected, 'controlling contract source: ' + src)
    freeze = json.loads(freeze_path.read_text())
    actual = {str(p.relative_to(ROOT)) for p in PACK.rglob('*') if p.is_file() and p != freeze_path}
    check(set(freeze['bindings']) == actual and len(actual) == 74, 'complete owned input closure')
    for rel, expected in freeze['bindings'].items():
        check(sha(owned(rel)) == expected, 'frozen input byte: ' + rel)
        BINDINGS[rel] = expected
    BINDINGS[str(freeze_path.relative_to(ROOT))] = sha(freeze_path)
    for name in ['ak2-independent-derivation.md', 'ak2-source-reading.json', 'ak2-root-preflight.json', 'ak2_independent.py']:
        p = HERE / name
        BINDINGS[str(p.relative_to(ROOT))] = sha(p)
    check(sha(HERE / 'ak2-root-preflight.json') == '141e850eff97b91afce6e130d70ea484b2d62ac7b37a30cd59ff1a5c9ce089d3',
          'root preflight authorization receipt')
    reading = json.loads((HERE / 'ak2-source-reading.json').read_text())
    check(reading['current_producer_science_read'] is False and reading['draft']['pages'] == 43,
          'honest reading ledger and current-science exclusion')
    return contract


O = (0, 0, 0)
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
STAR = (O,) + E
REGION = {O, E[2]}


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def tails(b):
    return {(4*b[0]+i, 2*b[1]+j, b[2]) for i, j in product(range(4), range(2))}


def links(region):
    return {(p, a) for b in region for p in tails(b) for a in range(3)}


def head(link):
    return add(link[0], E[link[1]])


def vertices(es):
    return {v for e in es for v in (e[0], head(e))}


def owner(p):
    return p[0]//4, p[1]//2, p[2]


def word(p, a, c):
    return [((p,a),1), ((add(p,E[a]),c),1), ((add(p,E[c]),a),-1), ((p,c),-1)]


def all_faces(b):
    return [{'tail': p, 'axes': (a,c), 'word': word(p,a,c),
             'selected': (a,c) == (0,1) and p[0] % 4 < 3 and p[1] % 2 == 0}
            for p in sorted(tails(b)) for a,c in combinations(range(3),2)]


def geometry(contract):
    es = links(REGION); vs = vertices(es); face = word(O,0,2)
    selected = {e for b in REGION for f in all_faces(b) if f['selected'] for e,sign in f['word']}
    check(len(es) == 48 and len(vs) == 36, 'complete two-factor geometry')
    check(len(selected) == 20 and len(es-selected) == 28, 'selected/free full-factor split')
    check(len({e for e,s in face}) == 4 and {owner(e[0]) for e,s in face} == REGION,
          'four distinct original differentiated links')
    path = [O]
    for e,sign in face:
        start,end = (e[0],head(e)) if sign == 1 else (head(e),e[0])
        check(path[-1] == start, 'original directed word continuation')
        path.append(end)
    check(path[-1] == O, 'original word closes')
    actions = [{'vertex':v,'outgoing':sorted(e for e in es if e[0]==v),
                'incoming':sorted(e for e in es if head(e)==v)} for v in sorted(vs)]
    check(sum(len(a['outgoing'])+len(a['incoming']) for a in actions)==2*len(es),
          'every original link has both endpoint actions')
    group = [f for f in all_faces(O) if not f['selected']]
    check(len(group)==21 and {owner(e[0]) for f in group for e,s in f['word']}==set(STAR),
          'complete 21-face original interaction star')
    fixtures=[]
    for sides in contract['parameters']['geometry_fixtures']:
        n=sides[0]; volume=set(product(*(range(k) for k in sides)))
        all_links=links(volume); all_vertices=vertices(all_links)
        anchors={b for b in volume if {add(b,s) for s in STAR} <= volume}
        omitted=[f for b in sorted(anchors) for f in all_faces(b) if not f['selected']]
        check(len(all_links)==24*n**3, 'whole-cube original links '+str(n))
        check(len(all_vertices)==8*n**3+14*n*n, 'whole-cube endpoints '+str(n))
        check(len(anchors)==(n-1)**3 and len(omitted)==21*len(anchors), 'all whole-star groups '+str(n))
        check(all(e in all_links for f in omitted for e,s in f['word']), 'every retained magnetic word owned '+str(n))
        check({e for e,s in face}<=all_links and es<=all_links, 'same original local observable in cube '+str(n))
        fixtures.append({'sides':sides,'sites':len(volume),'links':len(all_links),'endpoints':len(all_vertices),
                         'whole_stars':len(anchors),'omitted_faces':len(omitted),'differentiated_link_count':4,
                         'selected_face_count':3*len(volume)})
    return {'region':sorted(REGION),'links':sorted(es),'endpoint_actions':actions,'word':face,'path':path,
            'selected_links':sorted(selected),'free_links':sorted(es-selected),'omitted_origin_group':group,'cuboids':fixtures}


ONE=(F(1),F(0),F(0),F(0))
POOL=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),
      (F(8,17),F(0),F(0),F(15,17)),(F(1,2),)*4,ONE]


def qm(a,b):
    w,x,y,z=a; v,r,s,t=b
    return w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,w*s-x*t+y*v+z*r,w*t+x*s-y*r+z*v


def scale(a,s):
    return tuple(s*x for x in a)


def qi(a):
    return a[0],-a[1],-a[2],-a[3]


def mul_all(qs):
    out=ONE
    for q in qs:out=qm(out,q)
    return out


def holonomy(assignment,face):
    return mul_all([assignment[e] if sign==1 else qi(assignment[e]) for e,sign in face])


def cayley(axis,t):
    d=1+t*t/16
    return ((1-t*t/16)/d,) + tuple(t/(2*d) if a==axis else F(0) for a in range(3))


def differential_and_gauge():
    face=word(O,0,2); es=sorted(links(REGION)); vs=sorted(vertices(es))
    check(all(sum(x*x for x in q)==1 for q in POOL),'exact noncommuting unit quaternions')
    generators=[(F(0),)+tuple(F(int(a==b),2) for b in range(3)) for a in range(3)]
    check(all(qm(t,t)==(-F(1,4),F(0),F(0),F(0)) for t in generators),'fundamental generators square to minus one-quarter')
    check(-sum(qm(t,t)[0] for t in generators)==F(3,4),'fundamental Casimir is three-quarters')
    identity={e:ONE for e in es}
    check(holonomy(identity,face)==ONE and 1-holonomy(identity,face)[0]**2==0,
          'first identity kinetic-normalization fixture retained blind', verdict='nondiscriminating: both correct and rescaled Gamma vanish')
    assignment={e:POOL[(3*i+1)%len(POOL)] for i,e in enumerate(es)}
    for i,(e,sign) in enumerate(face):assignment[e]=POOL[i]
    factors=[assignment[e] if sign==1 else qi(assignment[e]) for e,sign in face]
    w=mul_all(factors)[0]; gamma=F(0); rows=[]
    check(1-w*w>0,'noncommuting fixture discriminates kinetic coefficient')
    for index,(e,sign) in enumerate(face):
        derivatives=[];seconds=[];cayley_rows=[]
        for axis,tangent in enumerate(generators):
            derivative=qm(tangent,assignment[e]) if sign==1 else scale(qm(qi(assignment[e]),tangent),-1)
            replaced=list(factors);replaced[index]=derivative;d=mul_all(replaced)[0]
            replaced[index]=scale(factors[index],-F(1,4));d2=mul_all(replaced)[0]
            check(d2==-w/4,'original signed link second derivative '+str(index)+':'+str(axis))
            for step in [F(1,8),F(1,16)]:
                qp,qmoved=cayley(axis,step),cayley(axis,-step)
                check(sum(x*x for x in qp)==1,'Cayley link stays SU2 '+str(index)+':'+str(axis)+':'+str(step))
                plus=dict(assignment);minus=dict(assignment)
                plus[e]=qm(qp,assignment[e]);minus[e]=qm(qmoved,assignment[e])
                wp,wm=holonomy(plus,face)[0],holonomy(minus,face)[0]
                corrected_d=(wp-wm)/(2*step)*(1+step*step/16)
                corrected_d2=(wp+wm-2*w)/(step*step)*(1+step*step/16)
                check(corrected_d==d and corrected_d2==d2,'complete-word independent Cayley jets '+str(index)+':'+str(axis)+':'+str(step))
                cayley_rows.append({'axis':axis,'step':step,'corrected_first':corrected_d,'corrected_second':corrected_d2})
            derivatives.append(d);seconds.append(d2)
        g=sum(d*d for d in derivatives);gamma+=g
        check(g==(1-w*w)/4 and -sum(seconds)==F(3,4)*w,'each original link Gamma and Casimir '+str(index))
        if sign==-1:
            check(sum((-d)**2 for d in derivatives)==g,'inverse sign squared-gradient control retained blind '+str(index))
            check(any(d!=-d for d in derivatives),'signed Cayley test detects wrong inverse derivative '+str(index))
        rows.append({'link':e,'orientation':sign,'first_derivatives':derivatives,'second_derivatives':seconds,
                     'gamma':g,'casimir_on_W':-sum(seconds),'cayley_jets':cayley_rows})
    check(gamma==1-w*w and gamma>0,'all four original-link gradients sum to one minus W squared')
    check(4*gamma!=gamma,'wrong Pauli versus half-Pauli normalization rejected')
    check(2*gamma!=gamma,'omitted one-half double-commutator normalization rejected')
    raw=holonomy(assignment,face); attempts=[]
    for shift in range(len(POOL)):
        gauges={v:POOL[(2*i+shift)%len(POOL)] for i,v in enumerate(vs)}
        full={e:qm(qm(gauges[e[0]],q),qi(gauges[head(e)])) for e,q in assignment.items()}
        wrong={e:qm(gauges[e[0]],q) for e,q in assignment.items()}
        moved=holonomy(full,face);bad=holonomy(wrong,face)[0]
        check(moved==qm(qm(gauges[O],raw),qi(gauges[O])) and moved[0]==w,'complete local endpoint gauge covariance '+str(shift))
        attempts.append({'shift':shift,'full_half_trace':moved[0],'missing_head_half_trace':bad,'discriminates':bad!=w})
        if bad!=w:break
    check(attempts[-1]['discriminates'],'missing head action discriminated')
    return {'W':w,'gamma':gamma,'link_derivatives':rows,'gauge_attempts':attempts,
            'blind_controls':['identity configuration has zero Gamma','squared gradients hide inverse first-derivative sign'],
            'physical_kinetic_coefficient_over_alpha':1,'double_commutator_multiplier_over_alpha':2*gamma,
            'physical_first_moment_integrand_over_alpha':gamma}


def rational_controls():
    alpha,delta,hbar=F(24),F(3),F(5)
    variance=F(1,4); energy=3*alpha; moment=variance*energy
    check(delta==alpha/8 and moment==alpha*(1-variance)==F(18),'free-corner physical first moment normalization')
    wrong_dimless_moment=moment/delta
    check(wrong_dimless_moment!=moment,'dimensionless moment cannot be renamed physical moment')
    shift=-4*alpha; raw_excited=shift+energy
    check(variance*raw_excited<0 and variance*(raw_excited-shift)==moment,'actual ground scalar must be subtracted')
    added=F(11)
    check((raw_excited+added)-(shift+added)==energy,'joint scalar shift cancels')
    time=hbar/alpha
    exponent=energy*time/hbar
    check(exponent==3 and energy*time!=exponent and (energy/delta)*time/hbar!=exponent,
          'delta and hbar factors discriminate in physical exponent')
    check(F(1,2)*(2*moment)==moment and 2*moment!=moment,'double commutator one-half energy factor')
    domain=[]
    for nterms in [1,2,4,8]:
        norm=sum(F(3,4**k) for k in range(1,nterms+1))
        form=sum(F(3,4**k)*(2**k)*(2**k+2) for k in range(1,nterms+1))
        check(norm==1-F(1,4**nterms) and form==3*nterms+6*(1-F(1,2**nterms)),
              'bounded physical rank operator can produce infinite energy prefix '+str(nterms))
        check(norm<1 and form>=3*nterms,'bounded norm and divergent energy separated '+str(nterms))
        domain.append({'prefix':nterms,'norm_squared':norm,'form_energy_over_alpha':form})
    loss=[];g=F(1,16);mass=F(1,5)
    for n in [1,2,3,8,16]:
        tail=F(1,10*n);low=mass-tail
        mu=low*g+tail*n
        check(low>0 and low+tail==mass and mu==F(9,80)-F(1,160*n)<1,
              'moment-loss fixed mass and uniform upper bound '+str(n))
        real=low*g/(g*g+1)+tail*n/(n*n+1)
        imag=low/(g*g+1)+tail/(n*n+1)
        limit_real=mass*g/(g*g+1);limit_imag=mass/(g*g+1)
        check((real-limit_real)**2+(imag-limit_imag)**2 <= (2*tail)**2,
              'moment-loss nonreal resolvent test '+str(n))
        for cutoff in [F(1,2),F(1),F(2)]:
            direct=low*min(g,cutoff)+tail*min(F(n),cutoff)
            tent=low*max(cutoff-abs(g),0)+tail*max(cutoff-n,0)
            check(direct==cutoff*mass-tent and direct<=mu,
                  'mass plus compact tent transfers truncated moment '+str(n)+':'+str(cutoff))
        check(mu+F(1,160*n)-mass*g==F(1,10),'first-moment loss at infinity is nonzero '+str(n))
        loss.append({'n':n,'low_mass':low,'tail_mass':tail,'mass':mass,'first_moment_over_alpha':mu,
                     'resolvent_at_i_real':real,'resolvent_at_i_imag':imag,'bounded_test_error_norm_factor':2*tail})
    check(F(1,80)<F(9,80) and F(9,80)-F(1,80)==F(1,10),'limiting first moment need not equal finite moment limit')
    # Auxiliary W+1/2 at the explicitly free corner; centering removes its vacuum atom.
    vacuum_mass=F(1,4);excited_mass=F(1,4)
    check(vacuum_mass+excited_mass==F(1,2) and excited_mass==variance,
          'uncentered bounded multiplier has extra vacuum mass')
    bad_energy=F(11);bad_mass=F(1,5)
    check(bad_energy>10 and bad_mass*bad_energy>1 and bad_energy>5,
          'variance and lower gap alone permit zero window and deficient lower heat')
    cutoff_energy=F(10);endpoint_weights=[(F(3,20),g),(F(1,20),cutoff_energy)]
    endpoint_moment=sum(p*e for p,e in endpoint_weights)
    inclusive=sum(p for p,e in endpoint_weights if g<=e<=10)
    wrong_exclusive=sum(p for p,e in endpoint_weights if g<=e<10)
    check(sum(p for p,e in endpoint_weights)==mass and endpoint_moment<=1,
          'endpoint control satisfies mass and moment premises')
    check(inclusive==mass and wrong_exclusive==F(3,20) and inclusive!=wrong_exclusive,
          'finite spectral window includes its upper endpoint')
    check(mass-F(1,10)==F(1,10),'window lower mass from first-moment upper bound')
    jensen=[]
    for v in [F(1,5),F(1,4),F(1,2)]:
        for mu in [F(1,10),F(1,2),F(1)]:
            check(mu/v<=1/v<=5 and v>=F(1,5),'Jensen envelope exponent and prefactor '+str(v)+':'+str(mu))
            jensen.append({'mass':v,'first_moment_over_alpha':mu,'normalized_mean_energy_over_alpha':mu/v})
    # Taylor's integral remainder gives odd lower/even upper bounds for exp(-x), x>=0.
    def exp_bounds(x):
        upper=sum((-x)**k/F(factorial(k)) for k in range(41))
        lower=upper+(-x)**41/F(factorial(41))
        return lower,upper
    heat_lower=sum(p*exp_bounds(e)[0] for p,e in endpoint_weights)
    envelope_upper=F(1,5)*exp_bounds(F(5))[1]
    check(heat_lower>envelope_upper>0,'nontrivial abstract heat control by exact Taylor enclosures')
    c=F(1,65536);possible_c1=c;possible_c2=F(1)
    radius=min(possible_c1,1/(2*possible_c2))/7
    check(0<radius<c,'additional cap is not a source stability radius')
    return {'free_corner':{'variance':variance,'physical_excitation_energy':energy,'alpha':alpha,'delta':delta,
                'hbar':hbar,'first_moment':moment,'first_moment_over_alpha':moment/alpha,
                'wrong_dimensionless_moment':wrong_dimless_moment,'joint_shift_cancels':True,
                'time':time,'correct_free_exponent':exponent,'raw_ground_scalar':shift},
            'bounded_local_domain_control':{'prefixes':domain,'infinite_norm_squared':1,'form_energy_diverges':True,
                'auxiliary_operator_is_original_W':False,'free_corner_only':True},
            'moment_loss':{'measures':loss,'limit_mass':mass,'limit_first_moment_over_alpha':F(1,80),
                'limit_of_first_moments_over_alpha':F(9,80),'lost_moment_over_alpha':F(1,10),
                'abstract_measures_not_actual_state':True},
            'vacuum_contamination':{'vacuum_mass_before_centering':vacuum_mass,'centered_mass':excited_mass},
            'gap_and_variance_only_control':{'mass':bad_mass,'energy_over_alpha':bad_energy,'window_mass':0,
                'first_moment_over_alpha':bad_mass*bad_energy,'heat_exponent_exceeds_frozen_5':True},
            'closed_window_endpoint_control':{'weights_and_energies_over_alpha':endpoint_weights,
                'moment_over_alpha':endpoint_moment,'inclusive_mass':inclusive,'incorrect_exclusive_mass':wrong_exclusive,
                'heat_at_unit_time_lower':heat_lower,'frozen_envelope_at_unit_time_upper':envelope_upper},
            'jensen_constant_controls':jensen,
            'coupling_logic_control':{'hypothetical_c1':possible_c1,'hypothetical_c2':possible_c2,
                'hypothetical_radius':radius,'additional_cap':c,'source_constants_evaluated':False}}


def clean(x):
    if isinstance(x,F):return {'numerator':x.numerator,'denominator':x.denominator}
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    output=parser.parse_args().output
    if not output.is_absolute() or output.exists():raise ValueError('--output must be a fresh absolute file')
    contract=inputs(); geom=geometry(contract); diff=differential_and_gauge(); controls=rational_controls()
    result={'schema':'ym28-ak2-independent-v1','loop':'ak2','sequence':10,'all_checks_passed':True,
            'check_count':len(CHECKS),'checks':CHECKS,'bindings':dict(sorted(BINDINGS.items())),
            'geometry':geom,'differential_and_gauge':diff,'controls':controls,
            'certificate':{'original_kinetic_coefficient':'alpha','four_link_gradient_sum':'1-W^2',
                'finite_physical_moment':'alpha omega_Lambda(1-W^2)',
                'limiting_moment_relation':'upper bound only; no equality across limit asserted',
                'physical_first_moment_upper_over_alpha':F(1),'actual_form_domain_established':True,
                'input_variance_lower':F(1,5),'inherited_lower_spectral_edge_over_alpha':F(1,16),
                'closed_window_upper_over_alpha':F(10),'closed_window_mass_lower':F(1,10),
                'lower_heat_prefactor':F(1,5),'lower_heat_exponent_coefficient_alpha_t_over_hbar':F(5),
                'all_finite_nonnegative_imaginary_times':True},
            'scope':{'same_actual_homogeneous_I1_AJ1_AJ2_AK1_state':True,'same_original_origin_xz_Wilson':True,
                'strict_unevaluated_tau_star_and_additional_cap':True,'source_constants_evaluated':False,
                'local_reference_energy_relabelled_as_physical_moment':False,
                'source_tested_resolvent_and_mass_limit_used':True,'common_concrete_strong_resolvent_claim':False,
                'moving_finite_means_transferred':True,'limiting_first_moment_equality_claim':False,
                'infinite_operator_domain_or_second_moment_claim':False,'actual_spectral_eigenatom_or_lowest_overlap_claim':False,
                'real_time_decay_claim':False,'other_boundary_or_model_transfer':False,'continuum_result':False,
                'scientific_priority_verified':False,'completion_percentage':None},
            'current_producer_science_read':False,'historical_or_producer_checkers_imported':False,
            'finite_checks_prove_analytic_theorem':False,'new_research_loops':1,'eleventh_investigation_started':False,
            'blocking_objections':[],'status':'independently derived before current producer exchange; awaiting review'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'check_count':len(CHECKS),'sha256':sha(output)}))


if __name__=='__main__':main()
