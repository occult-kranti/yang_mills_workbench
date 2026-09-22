#!/usr/bin/env python3
"""Additive AK2 post-exchange audit; independent exact arithmetic, no evaluator imports."""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='research/round28/'
PACK=HERE/'ak2-post-review-inputs'
INVENTORY_SHA='8a6e5329c1a12aac45a623fe46096f6745ddccb767b59d4583810054813eec34'
CONTRACT_SHA='ce7044e37b6263bc32767dddbfa28b95860c1c2f54064737a4577f195a6fd601'
FROZEN={'forward':('ce0e3aefea9cc699d66a205a3093ca9cb2126ead6f87f22fd05b83d39d13881d',91),
        'reverse':('fee1e8b39c5f2f07766d3ba098d73cb3f3ae29d2480a753ca09fecc3f18218a5',74)}
CHECKS=[]
BINDINGS={}
SOURCES={}


def check(ok,name):
    if not ok:raise ValueError(name)
    CHECKS.append({'name':name,'passed':True})


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def safe(rel):
    if not isinstance(rel,str) or Path(rel).is_absolute() or '..' in Path(rel).parts:
        raise ValueError('unsafe repository path: '+str(rel))
    walk=ROOT
    for part in Path(rel).parts:
        walk/=part
        if walk.is_symlink():raise ValueError('symlink input: '+rel)
    return walk


def data(src):return json.loads(SOURCES[src]['path'].read_text())


def frac(x):return F(x['numerator'],x['denominator']) if isinstance(x,dict) else F(x)


def inputs():
    ip=PACK/'source-inventory.json'
    check(sha(ip)==INVENTORY_SHA,'immutable postreview input inventory')
    inv=json.loads(ip.read_text());declared=set()
    for e in inv['entries']:
        src,snap,h=e['source'],e['snapshot'],e['sha256'];p=safe(snap);safe(src)
        check(PACK in p.parents and p.is_file(),'owned review snapshot: '+src)
        check(src not in SOURCES and snap not in declared,'unique review source and snapshot: '+src)
        check(sha(p)==h,'snapshot bytes: '+src)
        SOURCES[src]={'path':p,'sha256':h};declared.add(snap)
        BINDINGS.update({src:h,snap:h})
    actual={str(p.relative_to(ROOT)) for p in PACK.rglob('*') if p.is_file() and p!=ip}
    check(actual==declared and len(actual)==317,'all 317 review snapshots declared exactly')
    BINDINGS[str(ip.relative_to(ROOT))]=sha(ip)
    for p in [Path(__file__).resolve(),HERE/'ak2-post-review.md']:
        BINDINGS[str(p.relative_to(ROOT))]=sha(p)
    c=BASE+'contracts/ak2.json';contract=data(c)
    check(SOURCES[c]['sha256']==CONTRACT_SHA and contract['sequence']==10 and len(contract['sources'])==50,
          'unchanged tenth contract and 50 sources')
    for p,h in contract['sources'].items():check(SOURCES[p]['sha256']==h,'contract original: '+p)
    for side,(h,count) in FROZEN.items():
        prefix=BASE+side+'/ak2/';fp=prefix+'freeze.json'
        check(SOURCES[fp]['sha256']==h,'original independent producer freeze: '+side)
        files=data(fp)['bindings'];actual={p for p in SOURCES if p.startswith(prefix) and p!=fp}
        check(set(files)==actual and len(files)==count,'entire frozen producer closure: '+side)
        for p,digest in files.items():check(SOURCES[p]['sha256']==digest,'frozen producer bytes: '+p)
        r=data(prefix+'output/results.json');check(r['passed'] is True,'producer result passed: '+side)
        for p,digest in r['bindings'].items():check(SOURCES[p]['sha256']==digest,'producer runtime binding: '+side+':'+p)
    independent=BASE+'skeptic/ak2-independent-freeze.json'
    check(SOURCES[independent]['sha256']=='08ab8f8b7278fb0db731b5b43a09b53b76a6617972ec01761657c2e2dee706f1',
          'independent skeptical freeze identity')
    f=data(independent)
    check(len(f['bindings'])==81 and f['current_producer_science_read'] is False,'81 original skeptical files before exchange')
    for p,h in f['bindings'].items():check(SOURCES[p]['sha256']==h,'independent frozen bytes: '+p)
    replay=data(BASE+'skeptic/ak2-post-producer-replay.json')
    check(replay['all_fresh_normal_optimized_exact_outputs_equal'] is True and len(replay['runs'])==4,
          'four fresh whole-output producer replays')
    seen=set()
    for r in replay['runs']:
        expected={'results.json':SOURCES[BASE+r['direction']+'/ak2/output/results.json']['sha256']}
        check(r['files']==r['frozen_files']==expected and r['exit_code']==0
              and r['fresh_absolute_directory'] is True,'entire exact replay set: '+r['direction']+':'+r['mode'])
        script=r['command'][3 if r['mode']=='optimized' else 2]
        check(Path(script).is_absolute() and r['cwd']!=str(ROOT),'absolute replay outside repository: '+r['direction']+':'+r['mode'])
        seen.add((r['direction'],r['mode']))
    check(seen=={(s,m) for s in FROZEN for m in ('normal','optimized')},'both execution modes for both producers')
    check(SOURCES[BASE+'skeptic/ak2-post-root-closure.json']['sha256']=='af698fa20faa31d00b1580ed037dd4aee713998c7a68127d711aa73ff85e18b2',
          'root exchange closure receipt')
    # Parse the frozen failed source without importing or executing it.
    old=BASE+'forward/ak2/attempts/syntax-001/check.py'
    try:ast.parse(SOURCES[old]['path'].read_text())
    except SyntaxError as exc:check(exc.lineno==246,'original pre-execution syntax failure preserved')
    else:raise ValueError('preserved syntax failure no longer present')
    ast.parse(SOURCES[BASE+'forward/ak2/check.py']['path'].read_text())
    check('No output directory or scientific result was generated' in SOURCES[BASE+'forward/ak2/attempts/syntax-001/failure.txt']['path'].read_text(),
          'failure record distinguishes parsing from scientific execution')
    note=data(BASE+'experts/newton/ak2-comparison-sources.json')
    for p,h in note['bindings'].items():check(SOURCES[p]['sha256']==h,'Newton comparison direct evidence: '+p)
    check(note['additional_research_loops']==0 and note['new_scientific_execution'] is False,
          'Newton comparison adds no investigation')


def compare():
    f=data(BASE+'forward/ak2/output/results.json')
    r=data(BASE+'reverse/ak2/output/results.json')
    s=data(BASE+'skeptic/ak2-independent.json')
    fg,rg,sg=f['geometry'],r['geometry'],s['geometry']
    check(fg['links']==rg['links']==sg['links'] and len(sg['links'])==48,'three-way full 48 original links')
    check(fg['endpoint_actions']==rg['endpoint_actions']==sg['endpoint_actions'] and len(sg['endpoint_actions'])==36,
          'three-way complete 36 endpoint actions')
    check(fg['complete_region']==rg['region']==sg['region'],'same complete two-site region')
    fw=[[ [p,a],sign] for p,a,sign in fg['original_word']]
    check(fw==rg['wilson_word']==sg['word'],'three-way original signed Wilson word')
    check(fg['original_path']==sg['path'],'same original closed path')
    cubes=[]
    for n,fc,rc,sc in zip((2,3,4),fg['cuboids'],rg['cuboids'],sg['cuboids']):
        check(fc['coarse_sides']==rc['sides']==sc['sides']==[n,n,n],'three-way prescribed cube '+str(n))
        check(fc['links']==rc['links']==sc['links']==24*n**3,'all original cube links '+str(n))
        check(fc['endpoints']==rc['endpoints']==sc['endpoints']==8*n**3+14*n*n,'all cube endpoints '+str(n))
        check(fc['retained_omitted_groups']==rc['whole_stars']==sc['whole_stars']==(n-1)**3,'whole-star boundary '+str(n))
        check(fc['retained_omitted_faces']==rc['omitted_faces']==sc['omitted_faces']==21*(n-1)**3,'all omitted faces '+str(n))
        check(fc['selected_faces']==rc['selected_faces']==sc['selected_face_count']==3*n**3,'all selected faces '+str(n))
        cubes.append({'side':n,'links':24*n**3,'endpoints':8*n**3+14*n*n,'whole_stars':(n-1)**3})
    fs,rs,ss=f['spectral'],r['spectral_controls'],s['certificate']
    for fk,rk,sk,value in [
        ('input_variance_floor','inherited_mass_floor','input_variance_lower',F(1,5)),
        ('physical_moment_cap_over_alpha','physical_first_moment_ceiling_over_alpha','physical_first_moment_upper_over_alpha',F(1)),
        ('window_mass_lower','window_mass_floor','closed_window_mass_lower',F(1,10)),
        ('lower_heat_prefactor','lower_heat_prefactor','lower_heat_prefactor',F(1,5)),
        ('lower_heat_exponent_coefficient','lower_heat_rate_times_hbar_over_alpha','lower_heat_exponent_coefficient_alpha_t_over_hbar',F(5))]:
        check(frac(fs[fk])==frac(rs[rk])==frac(ss[sk])==value,'same independently derived target constant: '+fk)
    check(frac(fs['support_lower_over_alpha'])==frac(rs['window_in_alpha_units'][0])==frac(ss['inherited_lower_spectral_edge_over_alpha'])==F(1,16),
          'same inherited lower spectral support')
    check(frac(fs['window_upper_over_alpha'])==frac(rs['window_in_alpha_units'][1])==frac(ss['closed_window_upper_over_alpha'])==10,
          'same closed upper window endpoint')
    check(F(1,5)-F(1)/10==F(1,10) and F(1)/F(1,5)==5,'independent Markov and Jensen constants')
    check(f['analytic_claims']['first_moment_equality_claimed'] is False
          and rs['limiting_first_moment_equality_asserted'] is False
          and s['scope']['limiting_first_moment_equality_claim'] is False,'upper moment only in all three proofs')
    check(f['analytic_claims']['operator_domain_claimed'] is False
          and rs['limiting_operator_domain_asserted'] is False
          and s['scope']['infinite_operator_domain_or_second_moment_claim'] is False,'no infinite operator-domain claim')
    check(s['current_producer_science_read'] is False and s['check_count']==515,'independent source predates exchange')
    check(f['check_count']==len(f['checks'])==67 and all(c['passed'] is True for c in f['checks']),
          '67 forward published checks; no invented reverse count')
    return f,r,s,cubes


def derivatives(f,r,s):
    payloads=[]
    for side,w,rows,gamma in [
        ('forward',frac(f['differential']['W']),f['differential']['per_link'],frac(f['differential']['Gamma_W'])),
        ('skeptic',frac(s['differential_and_gauge']['W']),s['differential_and_gauge']['link_derivatives'],frac(s['differential_and_gauge']['gamma']))]:
        all_gamma=F(0);all_c=F(0)
        for i,row in enumerate(rows):
            ds=list(map(frac,row['derivatives' if side=='forward' else 'first_derivatives']))
            dds=list(map(frac,row['second_derivatives']))
            check(len(ds)==len(dds)==3 and all(x==-w/4 for x in dds),side+' actual second derivatives '+str(i))
            one=sum(x*x for x in ds);casimir=-sum(dds)
            check(one==(1-w*w)/4 and casimir==F(3,4)*w,side+' original link coefficient '+str(i))
            all_gamma+=one;all_c+=casimir
        check(all_gamma==gamma==1-w*w and all_c==3*w and gamma>0,side+' all-four-link derivative identity')
        cw2=2*w*all_c-2*gamma
        check(cw2==8*w*w-2 and 2*w*all_c-cw2==2*gamma,side+' independent Leibniz double-commutator check')
        payloads.append({'side':side,'W':w,'Gamma':gamma,'C_W':all_c,'C_W_squared':cw2})
    rd=r['derivatives'];w=frac(rd['wilson']);all_gamma=F(0);all_c=F(0)
    check(len(rd['first_second_derivatives'])==12,'reverse complete twelve signed derivatives')
    for i,row in enumerate(rd['first_second_derivatives']):
        d,dd=frac(row['first']),frac(row['second'])
        check(d==frac(row['symmetric_displacement_first']) and dd==frac(row['symmetric_displacement_second'])==-w/4,
              'reverse independent exact displacement '+str(i))
        all_gamma+=d*d;all_c-=dd
    check(all_gamma==frac(rd['sum_gradient_squares'])==1-w*w and all_c==frac(rd['total_C_W'])==3*w,
          'reverse all-four-link derivative identity')
    cw2=frac(rd['total_C_W_squared']);double=frac(rd['double_commutator_value'])
    check(cw2==8*w*w-2 and double==2*w*all_c-cw2==2*all_gamma,'reverse full double commutator')
    check(all(x['squared_comparison']=='nondiscriminating_retained' and x['signed_comparison_rejects'] is True
              for x in rd['inverse_sign_controls']),'reverse blind squares and signed replacements retained')
    check(f['blind_controls']==['inverse-sign-square-blind-preserved']
          and len(s['differential_and_gauge']['blind_controls'])==2,'forward and skeptic blind channels preserved')
    payloads.append({'side':'reverse','W':w,'Gamma':all_gamma,'C_W':all_c,'C_W_squared':cw2})
    return payloads


def local_character_control(s):
    frozen=s['controls']['bounded_local_domain_control'];prefixes=[]
    for row in frozen['prefixes']:
        n=row['prefix'];norm=F(0);energy=F(0)
        for k in range(1,n+1):
            spin=F(2**k,2);weight=F(3,4**k)
            norm+=weight;energy+=weight*4*spin*(spin+1)
        check(norm==frac(row['norm_squared'])==1-F(1,4**n),'local character norm prefix '+str(n))
        check(energy==frac(row['form_energy_over_alpha'])==3*n+6*(1-F(1,2**n))>=3*n,
              'four original character Casimirs and divergent energy prefix '+str(n))
        prefixes.append({'terms':n,'norm_squared':norm,'physical_energy_over_alpha':energy})
    check(len(s['geometry']['links'])==48 and len(s['geometry']['endpoint_actions'])==36,'complete local character factor and endpoint group')
    raw=frac(s['differential_and_gauge']['W'])
    moved=frac(s['differential_and_gauge']['gauge_attempts'][-1]['full_half_trace'])
    check(raw==moved,'original full endpoint action preserves holonomy class')
    def character(n,w):
        a,b=F(1),2*w
        if n==0:return a
        for j in range(2,n+1):a,b=b,2*w*b-a
        return b
    for n in (2,4,8,16):check(character(n,raw)==character(n,moved),'local spin character class invariance '+str(n))
    # Basis: Omega_R tensor e0,e1 followed by f_R tensor e0,e1.
    local_times_identity=[[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
    wrong_global_vacuum_rank=[[0,0,1,0],[0,0,0,0],[1,0,0,0],[0,0,0,0]]
    witness=[0,1,0,0]
    matvec=lambda a:[sum(a[i][j]*witness[j] for j in range(4)) for i in range(4)]
    check(matvec(local_times_identity)==[0,0,0,1] and matvec(wrong_global_vacuum_rank)==[0,0,0,0],
          'local A_R tensor identity differs from a global vacuum projector')
    return {'attributed_to':'independent skeptic before exchange; locality notation clarified additively',
            'local_region_links':48,'endpoint_actions':36,'Omega_R':'normalized constant Haar vector on H_R',
            'f_R':'sqrt(3) sum_(k>=1)2^-k character_(spin 2^(k-1)) of original holonomy on H_R',
            'A_R':'|f_R><Omega_R|+|Omega_R><f_R|','extension':'A_R tensor identity outside R',
            'global_vacuum_projector_used':False,'local_vectors_endpoint_invariant':True,'prefixes':prefixes}


def controls(f,r,s):
    fcorner=f['physical_controls']['free_corner'];rcorner=r['spectral_controls']['all_zero_coupling_free_corner']
    check(frac(fcorner['variance'])==frac(rcorner['variance'])==frac(s['controls']['free_corner']['variance'])==F(1,4),
          'same explicitly free-corner Wilson norm')
    check(frac(fcorner['energy_over_alpha'])==frac(rcorner['overlapping_energy_over_alpha'])==3,
          'four fundamental Casimirs at free corner')
    check(frac(fcorner['first_moment_over_alpha'])==frac(rcorner['first_moment_over_alpha'])
          ==frac(s['controls']['free_corner']['first_moment_over_alpha'])==F(3,4),'same free-corner first moment')
    losses={}
    for row in f['spectral']['escape_of_first_moment']:
        n=row['n'];check(frac(row['first_moment'])==F(3,4)-F(1,8*n)
                         and frac(row['limit_first_moment'])==F(1,4),'forward distinct moment-loss example '+str(n))
    losses['forward']=F(1,2)
    for row in r['spectral_controls']['first_moment_loss_at_infinity']:
        check(frac(row['first_moment'])==F(9,16) and frac(row['limit_first_moment'])==F(1,16),
              'reverse distinct moment-loss example '+str(row['n']))
    losses['reverse']=F(1,2)
    own=s['controls']['moment_loss'];check(frac(own['limit_of_first_moments_over_alpha'])-frac(own['limit_first_moment_over_alpha'])==F(1,10),
          'skeptic distinct mass-one-fifth moment-loss example')
    losses['skeptic']=F(1,10)
    c=r['spectral_controls']['centering'];mass=frac(c['centered_mass']);moment=frac(c['first_moment'])
    check(c['abstract_gap']==1 and mass==F(1,16) and moment==F(1,4),'preserve reverse stale label and actual mass/moment')
    check(moment/mass==4 and frac(c['centered_heat_at_log2'])==F(1,256)
          and frac(c['raw_heat_at_log2'])==F(65,256),'reconstruct reverse implemented excited level four and heats')
    note=data(BASE+'experts/newton/ak2-comparison-sources.json')['reverse_centering_metadata_clarification']
    check(note['status']=='stale unused diagnostic metadata' and note['implemented_gap_over_alpha']==4
          and note['retrospective_intentional_lower_bound_claimed'] is False,'producer-authored explicit stale-label clarification')
    endpoint=s['controls']['closed_window_endpoint_control']
    check(frac(endpoint['inclusive_mass'])==F(1,5)>frac(endpoint['incorrect_exclusive_mass'])==F(3,20),
          'skeptic attributed closed-window endpoint fixture')
    check(frac(endpoint['heat_at_unit_time_lower'])>frac(endpoint['frozen_envelope_at_unit_time_upper'])>0,
          'skeptic attributed exact Taylor heat enclosure')
    return {'lost_moment_over_alpha':losses,'reverse_centering':{'stale_unused_label':1,'implemented_excitation_and_gap_over_alpha':4,
            'centered_mass':mass,'first_moment_over_alpha':moment,'centered_heat_at_log2':F(1,256),'raw_heat_at_log2':F(65,256),
            'retrospective_lower_bound_reinterpretation':False,'actual_state_theorem_affected':False}}


LIMITATIONS=[
    'Fixed actual homogeneous I1/AJ1/AJ2/AK1 whole-star orthant state, original origin xz Wilson, full physical completion and fixed positive scales only.',
    'Requires |tau|<unevaluated tau_* and |tau|<=2^-16; no evaluated numerical stability interval or chosen positive numerical coupling.',
    'Limiting first moment is bounded above; no equality across the limit, evaluated interacting moment or sharp constants.',
    'Actual infinite form domain follows; no infinite operator domain, second moment or automatic bounded-local domain principle.',
    'Closed-window mass is not an eigenatom, threshold atom, lowest overlapping energy or sharp long-time rate.',
    'Finite nonnegative imaginary-time bounds retain hbar and imply no real-time magnitude decay, experimental confirmation or measured mass.',
    'Inherited source and boundary premises remain; finite checks and independent implementations are not physical observations or replacements for infinite-volume proof. Reading depths and blind/failed controls are disclosed.',
    'No other-boundary/model transfer, continuum solution, priority or historical validation, or defensible Millennium-problem percentage. Investigation ten is the stopping boundary.'
]


def encode(x):
    if isinstance(x,F):return str(x)
    raise TypeError(type(x).__name__)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);out=parser.parse_args().output
    if not out.is_absolute() or out.exists():raise ValueError('--output must be a fresh absolute file')
    inputs();f,r,s,cubes=compare();diff=derivatives(f,r,s);local=local_character_control(s);diagnostics=controls(f,r,s)
    result={'schema':'ym28-ak2-post-review-v1','loop':'ak2','sequence':10,'passed':True,'check_count':len(CHECKS),
            'checks':CHECKS,'bindings':dict(sorted(BINDINGS.items())),'blocking_objections':[],'limitations':LIMITATIONS,
            'supported':{'same_actual_homogeneous_state_and_original_origin_Wilson':True,'physical_first_moment_upper_over_alpha':'1',
                'actual_physical_form_domain':True,'closed_window_in_alpha_units':['1/16','10'],'closed_window_mass_lower':'1/10',
                'lower_heat_prefactor':'1/5','lower_heat_exponent_alpha_t_over_hbar':'5','all_finite_nonnegative_imaginary_times':True,
                'strict_symbolic_tau_star_and_extra_cap_required':True,'source_constants_evaluated':False,
                'limiting_first_moment_equality_claim':False,'infinite_operator_domain_or_second_moment':False,
                'common_concrete_strong_resolvent_claim':False,'physical_moment_from_reference_energy_relabelling':False,
                'actual_spectral_atom_or_lowest_overlap_claim':False,'real_time_decay_claim':False,
                'all_three_frozen_closures_unchanged':True,'four_fresh_full_output_replays_equal':True,
                'local_character_control_attributed_to_independent_skeptic':True,'local_rank_operator_extended_by_identity':True,
                'reverse_stale_gap_label_acknowledged':True,'reverse_stale_label_reinterpreted_as_lower_bound':False,
                'forward_preexecution_syntax_failure_preserved':True,'reading_depths_disclosed':True,
                'new_external_primary_retrievals':0,'new_research_loops':0,'eleventh_science_investigation':False,
                'continuum_or_scientific_priority_or_completion_percentage_claim':False},
            'cube_comparison':cubes,'differential_comparison':diff,'local_character_clarification':local,
            'attributed_controls':diagnostics,'final_admission_spec_review':'pending root-approved specification'}
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,default=encode,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'check_count':len(CHECKS),'sha256':sha(out)}))


if __name__=='__main__':main()
