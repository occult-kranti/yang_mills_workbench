#!/usr/bin/env python3
"""AK2 exact source, geometry, derivative and implication audits. No old imports."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[3]
CONTRACT = 'research/round28/contracts/ak2.json'
CONTRACT_SHA = 'ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601'
O = (0,0,0)
E = ((1,0,0),(0,1,0),(0,0,1))
S = (O,)+E
REGION = {O,E[2]}


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owned_path(rel):
    require(not Path(rel).is_absolute() and '..' not in Path(rel).parts, 'unsafe local path')
    p=ROOT/rel
    require(OWN in p.parents, 'runtime dependency not in owned directory')
    for q in (p,)+tuple(p.parents):
        if q==ROOT:
            break
        require(not q.is_symlink(), 'symlink dependency')
    return p


def bindings():
    invp=OWN/'inputs/source-inventory.json'
    inv=json.loads(invp.read_text()); result={}; originals={}; snaps=set()
    for item in inv['entries']:
        rel=item['snapshot']; require(rel not in snaps,'duplicate snapshot'); snaps.add(rel)
        h=sha(owned_path(rel)); require(h==item['sha256'],'changed snapshot '+rel)
        result[rel]=h
        if item.get('external_instruction_snapshot'):
            require(Path(item['source']).is_absolute(),'external provenance not absolute')
        else:
            src=item['source'];require(not Path(src).is_absolute() and '..' not in Path(src).parts,'nonportable original')
            require(src not in originals,'duplicate original')
            originals[src]=(h,rel);result[src]=h
    require(originals[CONTRACT][0]==CONTRACT_SHA==inv['contract_sha256'],'contract hash')
    contract=json.loads(owned_path(originals[CONTRACT][1]).read_text())
    require(contract['sequence']==10 and contract['loop']=='ak2','wrong final loop')
    require(len(contract['sources'])==50,'required source count')
    for src,h in contract['sources'].items():
        require(src in originals and originals[src][0]==h,'required source missing or wrong '+src)
    freeze=OWN/'inputs/freeze.json'; frozen=json.loads(freeze.read_text())['bindings']
    actual={str(p.relative_to(ROOT)) for p in (OWN/'inputs').rglob('*') if p.is_file() and p!=freeze}
    require(actual==set(frozen),'input freeze coverage')
    for rel,h in frozen.items():
        require(sha(owned_path(rel))==h,'input freeze mismatch');result[rel]=h
    for p in (freeze,invp,OWN/'report.md',OWN/'source-reading.json',Path(__file__).resolve()):
        result[str(p.relative_to(ROOT))]=sha(p)
    return dict(sorted(result.items())),contract


def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))


def owner(v):
    return v[0]//4,v[1]//2,v[2]


def linkset(sites):
    return {((4*b[0]+x,2*b[1]+y,b[2]),a) for b in sites
            for x in range(4) for y in range(2) for a in range(3)}


def head(link):
    return plus(link[0],E[link[1]])


def endpoints(links):
    return {v for e in links for v in (e[0],head(e))}


def face(p,a,b):
    return [((p,a),1),((plus(p,E[a]),b),1),((plus(p,E[b]),a),-1),((p,b),-1)]


def anchor_faces(b):
    return [(p,a,c,face(p,a,c)) for p in sorted({e[0] for e in linkset({b})})
            for a,c in combinations(range(3),2)]


def selected(f):
    p,a,b,_=f
    return (a,b)==(0,1) and p[0]%4<3 and p[1]%2==0


def geometry(contract):
    local=linkset(REGION);vertices=endpoints(local);word=face(O,0,2)
    require(len(local)==48 and len(vertices)==36,'complete local geometry')
    require([owner(e[0]) for e,sign in word]==[O,O,E[2],O],'original Wilson owners')
    require([sign for e,sign in word]==[1,1,-1,-1],'inverse orientations')
    require(len({e for e,sign in word})==4,'distinct Wilson links')
    pos=O
    for e,sign in word:
        start,end=(e[0],head(e)) if sign==1 else (head(e),e[0])
        require(start==pos,'broken path');pos=end
    require(pos==O,'unclosed path')
    sel={e for b in REGION for f in anchor_faces(b) if selected(f) for e,sign in f[3]}
    require(len(sel)==20 and len(local-sel)==28,'selected/free factors')
    base=[f for f in anchor_faces(O) if not selected(f)]
    require(len(base)==21,'omitted anchor count')
    require(set().union(*({owner(e[0]) for e,sign in f[3]} for f in base))==set(S),'full interaction star')
    rows=[]
    for sides in contract['parameters']['geometry_fixtures']:
        sites=set(product(*(range(n) for n in sides))); es=linkset(sites)
        anchors={b for b in sites if {plus(b,s) for s in S}<=sites}
        omitted=[f for b in anchors for f in anchor_faces(b) if not selected(f)]
        n=sides[0]
        require(len(es)==24*n**3 and len(endpoints(es))==8*n**3+14*n*n,'cuboid analytic counts')
        require(len(anchors)==(n-1)**3 and len(omitted)==21*(n-1)**3,'whole-star count')
        require(all({e for e,sign in f[3]}<=es for f in omitted),'retained outgoing word lost')
        require(all(owner(e[0]) in sites for e in es),'unique ownership')
        rows.append({'sides':sides,'links':len(es),'endpoints':len(endpoints(es)),
                     'whole_stars':len(anchors),'selected_faces':3*len(sites),
                     'omitted_faces':len(omitted),'active_W_links':4})
    return {'wilson_word':word,'region':sorted(REGION),'links':sorted(local),
            'endpoint_actions':[{'vertex':v,'outgoing':[e for e in sorted(local) if e[0]==v],
                'incoming':[e for e in sorted(local) if head(e)==v]} for v in sorted(vertices)],
            'selected_links':sorted(sel),'free_links':sorted(local-sel),'cuboids':rows}


def mul(a,b):
    w,x,y,z=a;v,i,j,k=b
    return (w*v-x*i-y*j-z*k,w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i,w*k+x*j-y*i+z*v)


def inv(a):
    return a[0],-a[1],-a[2],-a[3]


def scale(c,a):
    return tuple(c*x for x in a)


def multiply_all(items):
    out=(F(1),F(0),F(0),F(0))
    for x in items:
        out=mul(out,x)
    return out


def holonomy(values,word):
    return multiply_all([values[e] if sign==1 else inv(values[e]) for e,sign in word])


def derivatives():
    pool=[(F(1,2),)*4,(F(3,5),F(4,5),F(0),F(0)),
          (F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17))]
    require(all(sum(x*x for x in q)==1 for q in pool),'unit quaternion normalization')
    require(mul(pool[1],pool[2])!=mul(pool[2],pool[1]),'fixture accidentally commuting')
    es=sorted(linkset(REGION));word=face(O,0,2)
    vals={e:pool[(i*3+1)%4] for i,e in enumerate(es)}
    raw=holonomy(vals,word);w=raw[0];require(w*w<1,'gradient fixture degenerate')
    factors=[vals[e] if sign==1 else inv(vals[e]) for e,sign in word]
    records=[];total_grad=F(0);total_casimir=F(0);cw2=F(0);signed_inverse=[]
    cos,sin=F(3,5),F(4,5)
    for index,(e,sign) in enumerate(word):
        grad=F(0);casimir=F(0)
        for a in range(3):
            generator=tuple(F(1,2) if j==a+1 else F(0) for j in range(4))
            g2=mul(generator,generator)
            first=mul(generator,vals[e]) if sign==1 else scale(-1,mul(inv(vals[e]),generator))
            second=mul(g2,vals[e]) if sign==1 else mul(inv(vals[e]),g2)
            first_factors=list(factors);first_factors[index]=first
            second_factors=list(factors);second_factors[index]=second
            d=multiply_all(first_factors)[0];dd=multiply_all(second_factors)[0]
            qplus=tuple(cos if j==0 else sin if j==a+1 else F(0) for j in range(4))
            vp=dict(vals);vm=dict(vals);vp[e]=mul(qplus,vals[e]);vm[e]=mul(inv(qplus),vals[e])
            wp=holonomy(vp,word)[0];wm=holonomy(vm,word)[0]
            independent_d=(wp-wm)/(4*sin)
            independent_dd=(wp+wm-2*w)/(8*(1-cos))
            require(d==independent_d,'signed original-link derivative')
            require(dd==independent_dd==-w/4,'Casimir half-angle normalization')
            grad+=d*d;casimir-=dd;cw2-=2*d*d+2*w*dd
            records.append({'link':e,'orientation':sign,'axis':a,'first':d,'second':dd,
                            'symmetric_displacement_first':independent_d,
                            'symmetric_displacement_second':independent_dd})
            if sign==-1 and d:
                signed_inverse.append({'link':e,'axis':a,'correct':d,'wrong_inverse_sign':-d,
                                       'signed_comparison_rejects':-d!=independent_d,
                                       'squared_comparison':'nondiscriminating_retained'})
        require(grad==(1-w*w)/4 and casimir==F(3,4)*w,'per-link gradient and Casimir')
        total_grad+=grad;total_casimir+=casimir
    require(total_grad==1-w*w and total_casimir==3*w,'four-link coefficient')
    double=2*w*total_casimir-cw2
    require(cw2==8*w*w-2 and double==2*total_grad,'double commutator on test constant')
    require(signed_inverse and all(x['signed_comparison_rejects'] for x in signed_inverse),'inverse-sign replacement blind')
    gauges={v:pool[(i+2)%4] for i,v in enumerate(sorted(endpoints(es)))}
    moved={e:mul(mul(gauges[e[0]],vals[e]),inv(gauges[head(e)])) for e in es}
    require(holonomy(moved,word)==mul(mul(gauges[O],raw),inv(gauges[O])),'full gauge covariance')
    return {'wilson':w,'first_second_derivatives':records,'sum_gradient_squares':total_grad,
            'total_C_W':total_casimir,'total_C_W_squared':cw2,'double_commutator_value':double,
            'inverse_sign_controls':signed_inverse,'all_endpoint_covariance':True,
            'wrong_generator_scale_energy_factor':4}


def measure_checks():
    vmin=F(1,5);moment=F(1);g=F(1,16);upper=F(10)
    tail=moment/upper;window=vmin-tail;rate=moment/vmin
    require(tail==F(1,10) and window==F(1,10) and rate==5,'frozen targets')
    free_var=F(1,4);free_energy=F(3)
    require(free_var*free_energy==F(3,4)<moment,'all-zero-coupling normalization')
    require(2*free_var*free_energy>moment,'missing commutator half blind')
    require(4*free_var*free_energy>moment,'wrong kinetic normalization blind')
    escape=[]
    for n in (2,4,16):
        h=g+F(n,2);p=F(1,n)
        m=(1-p)*g+p*h
        require(m==F(9,16) and m-g==F(1,2),'first moment loss fixture')
        # Real/imaginary parts of the Cauchy transform at z=i.
        real=(1-p)*g/(g*g+1)+p*h/(h*h+1)
        imag=(1-p)/(g*g+1)+p/(h*h+1)
        dr=real-g/(g*g+1);di=imag-1/(g*g+1)
        require(dr*dr+di*di<=(2*p)**2,'bounded resolvent difference')
        escape.append({'n':n,'mass':1,'first_moment':m,'limit_first_moment':g,
                       'uniform_unit_bounded_test_error_ceiling':2*p,
                       'cauchy_difference_squared':dr*dr+di*di})
    prefixes=[]
    for n in (4,8,16):
        norm=sum((F(1,4*k*k) for k in range(1,n+1)),F(0))
        energy=sum((F(k*k,4*k*k) for k in range(1,n+1)),F(0))
        require(norm<F(1,2) and energy==F(n,4),'bounded operator domain countermodel')
        prefixes.append({'n':n,'vector_norm_squared':norm,'form_energy_over_alpha':energy})
    for energy in (F(0),g,F(1),F(3),F(10)):
        values=[energy*min(F(1),max(F(0),2-energy/L)) for L in (F(1),F(2),F(4),F(16))]
        require(all(0<=x<=energy for x in values) and values==sorted(values) and values[-1]==energy,
                'nonnegative C0 moment cutoffs')
    # At the diagnostic time alpha*t/hbar=log(2), no exponent approximation occurs.
    bad_energy=F(20);bad_heat=vmin*F(1,2)**20;required_heat=vmin*F(1,2)**5
    require(bad_energy>upper and vmin*bad_energy>moment and bad_heat<required_heat,
            'gap and variance alone control blind')
    require(vmin*rate==moment and vmin*F(1,2)**5==required_heat,'Jensen extremal diagnostic')
    mean=F(1,2);amplitude=F(1,4);excited=F(4)
    raw_mass=mean*mean+amplitude*amplitude;center_mass=amplitude*amplitude
    centered_heat=center_mass*F(1,2)**4;raw_heat=mean*mean+centered_heat
    require(raw_heat>raw_mass/F(2),'uncentered plateau control blind')
    require(excited*center_mass==excited*(raw_mass-mean*mean),'centering first moment invariance')
    alpha,delta,hbar,ground,gap=F(24),F(3),F(2),F(-5),F(2)
    physical=delta*((ground+gap)-ground);frequency=physical/hbar
    require(delta==alpha/8 and physical==6 and frequency==3,'physical scale')
    require(delta*(ground+gap)!=physical and gap!=physical and physical!=frequency,'omitted scalar/delta/hbar controls')
    require(delta*((ground+11+gap)-(ground+11))==physical,'joint scalar shift')
    cap=F(1,65536);hypothetical_c1=cap;hypothetical_c2=F(1)
    radius=min(hypothetical_c1,1/(2*hypothetical_c2))/7
    test_tau=cap/2
    require(0<radius<test_tau<cap,'both coupling conditions')
    return {'units':'all spectral energies in this exact diagnostic section are divided by fixed positive alpha unless labeled otherwise',
            'inherited_mass_floor':vmin,'physical_first_moment_ceiling_over_alpha':moment,
            'window_in_alpha_units':[g,upper],'window_mass_floor':window,
            'lower_heat_prefactor':vmin,'lower_heat_rate_times_hbar_over_alpha':rate,
            'limiting_form_domain_supported':True,'limiting_operator_domain_asserted':False,
            'limiting_first_moment_equality_asserted':False,
            'all_zero_coupling_free_corner':{'variance':free_var,'overlapping_energy_over_alpha':free_energy,
                'first_moment_over_alpha':free_var*free_energy,'wrong_missing_half':2*free_var*free_energy,
                'wrong_generator_scale':4*free_var*free_energy},
            'first_moment_loss_at_infinity':escape,'bounded_operator_domain_countermodel':prefixes,
            'gap_variance_without_moment':{'mass':vmin,'energy_over_alpha':bad_energy,'window_mass':0,
                'heat_at_log2':bad_heat,'false_claimed_lower':required_heat,'first_moment_over_alpha':vmin*bad_energy},
            'centering':{'abstract_gap':1,'mean':mean,'raw_mass':raw_mass,'centered_mass':center_mass,
                'raw_heat_at_log2':raw_heat,'centered_heat_at_log2':centered_heat,'first_moment':excited*center_mass},
            'physical_scalar_fixture':{'alpha':alpha,'delta':delta,'hbar':hbar,'raw_ground':ground,
                'physical_excitation':physical,'frequency':frequency},
            'coupling_control':{'hypothetical_only':True,'c1':hypothetical_c1,'c2':hypothetical_c2,
                'possible_tau_star':radius,'test_tau':test_tau,'extra_cap':cap,
                'cap_without_symbolic_condition_rejected':True},
            'nonnegative_compact_cutoff_checks':True}


def encode(x):
    if isinstance(x,F):
        return str(x)
    raise TypeError(type(x).__name__)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);require(out.is_absolute() and not out.exists(),'output must be fresh absolute directory')
    b,c=bindings()
    result={'schema':'ym28-ak2-reverse-results-v1','loop':'ak2','sequence':10,'passed':True,
            'bindings':b,'geometry':geometry(c),'derivatives':derivatives(),'spectral_controls':measure_checks(),
            'scope':{'actual_homogeneous_targets_supported':True,'current_opposite_science_read':False,
                'eleventh_investigation_executed':False,'numerical_stability_radius_evaluated':False,
                'source_theorem_inherited':True,'continuum_claim':False}}
    out.mkdir(parents=True,exist_ok=False)
    (out/'results.json').write_text(json.dumps(result,default=encode,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'results_sha256':sha(out/'results.json')},sort_keys=True))


if __name__=='__main__':
    main()
