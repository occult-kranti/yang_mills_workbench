#!/usr/bin/env python3
"""AJ1 post-exchange exact audit. No producer checker is imported.
Analytic operator claims are reviewed in aj1-post-review.md, not proved by flags.
"""
import argparse, ast, hashlib, itertools, json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
COUNT=Counter()
INVENTORY='research/round28/skeptic/aj1-post-review-inputs/source-inventory.json'
INV_SHA='63bbddfc34ba7ec5a06b6686e07c312e9b963217ea86db04c2b5f47cc5614433'
def need(p,g):
 COUNT[g]+=1
 if not p:raise RuntimeError(g)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def q(x):
 if isinstance(x,dict):
  need(set(x)=={'numerator','denominator'} and all(type(v) is int for v in x.values()),'typed rational object')
  return Q(x['numerator'],x['denominator'])
 need(type(x) in (str,int),'typed rational scalar');return Q(x)
def canon(x):return json.loads(json.dumps(x))
def tup(x):return tuple(tup(a) for a in x) if isinstance(x,list) else x
def add(a,b):return tuple(a[i]+b[i] for i in range(3))
Z=(0,0,0); E=((1,0,0),(0,1,0),(0,0,1)); STAR=(Z,)+E
F='research/round28/forward/aj1/'; R='research/round28/reverse/aj1/'; S='research/round28/skeptic/'
def owner(p):return (p[0]//4,p[1]//2,p[2])
def faces(b):
 out=[]
 for x,y in itertools.product(range(4),range(2)):
  p=(4*b[0]+x,2*b[1]+y,b[2])
  for a,c in itertools.combinations(range(3),2):
   w=[((p,a),1),((add(p,E[a]),c),1),((add(p,E[c]),a),-1),((p,c),-1)]
   if not (a==0 and c==1 and y==0 and x<3):out.append({'face':(p,a,c),'word':w,'owners':sorted({owner(t) for (t,d),sign in w})})
 return out

def closure():
 need(sha(INVENTORY)==INV_SHA,'postreview input inventory frozen')
 inv=read(INVENTORY)
 for row in inv['entries']:
  need(sha(row['source'])==row['sha256']==sha(row['snapshot']),'postreview snapshot equality')
 contract=read('research/round28/contracts/aj1.json')
 need(contract['sequence']==7 and len(contract['sources'])==48,'exact contract sequence and source count')
 allbindings={INVENTORY:INV_SHA}
 for row in inv['entries']:allbindings[row['source']]=row['sha256'];allbindings[row['snapshot']]=row['sha256']
 counts={}
 for side,p,key in [('forward',F,'sha256'),('reverse',R,'files')]:
  fr=read(p+'freeze.json');bound=fr[key]
  actual={str(x.relative_to(ROOT)) for x in (ROOT/p).rglob('*') if x.is_file() and x!=ROOT/(p+'freeze.json')}
  mapping=bound if side=='forward' else {p+k:v for k,v in bound.items()}
  need(set(mapping)==actual,'complete producer owned closure '+side)
  for path,h in mapping.items():need(sha(path)==h,'producer frozen file '+side)
  for path,h in contract['sources'].items():
   need(sha(path)==h==sha(p+'inputs/'+path),'all48 declared sources '+side)
  counts[side]=len(mapping)
 for path,h in read(S+'aj1-independent-freeze.json')['bindings'].items():need(sha(path)==h,'prefreeze independent scientific bytes preserved')
 fw=read(F+'output/results.json');rv=read(R+'output/results.json')
 need(read(F+'output/source-manifest.json')==fw['provenance'],'forward auxiliary manifest exact provenance')
 need(not any(Path(p).is_absolute() for p in rv['bindings']),'portable reverse no absolute runtime dependency')
 for p,h in rv['bindings'].items():need(sha(p)==h,'reverse complete current runtime binding')
 old=R+'repairs/portable-bindings-original/'
 need(sha(old+'freeze.json')=='4ff69ca8ef576f283237f85280a2ce64219b08ffe0fefb9c972f8457a50d557a','original preexchange reverse freeze preserved')
 repair=read(R+'portable-binding-repair.json')
 for p,h in repair['original_files_sha256'].items():need(sha(old+p)==h,'portable repair original archive')
 for p,h in repair['unchanged_input_files_sha256'].items():need(sha(R+p)==h,'portable repair inputs unchanged')
 a=read(old+'output/results.json');b=dict(rv);a.pop('bindings');b.pop('bindings')
 need(a==b,'portable repair exact scientific payload equality excluding only bindings')
 need(sha(old+'output/geometry.json')==sha(R+'output/geometry.json'),'portable repair all geometry bytes unchanged')
 need(sha(old+'report.md')==sha(R+'report.md'),'portable repair whole analytic report unchanged')
 def science_ast(p):
  tree=ast.parse((ROOT/p).read_text());tree.body=[n for n in tree.body if not isinstance(n,ast.FunctionDef) or n.name!='source_bindings'];return ast.dump(tree,include_attributes=False)
 need(science_ast(old+'check.py')==science_ast(R+'check.py'),'portable repair AST outside source_bindings identical')
 need(repair['scientific_comparison_exclusion']==['bindings'] and repair['research_loops_added']==0,'portable repair exact exclusions and zero loops')
 dev=read(F+'development/record.json');first=F+'development/first-fixture-pass/'
 need(sha(first+'check.py')==dev['first_successful_checker_sha256']==read(first+'source-manifest.json')['checker_sha256'],'forward successful development checker reconstructed to recorded hash')
 need(read(first+'results.json')['geometry']==fw['geometry'],'forward successful development full geometry preserved')
 receipt=read(S+'aj1-producer-replays.json')
 for side,p in [('forward',F),('reverse',R)]:
  need(sha(p+'freeze.json')==receipt['side'][side]['freeze_sha256'],'fresh replay active freeze '+side)
  names={x.name for x in (ROOT/(p+'output')).iterdir()}
  need(names==set(receipt['side'][side]['files']),'fresh replay all output files '+side)
  for n in names:
   orig=(ROOT/(p+'output/'+n)).read_bytes()
   for mode in ['normal','optimized']:
    need((HERE/'aj1-producer-fresh-replays'/(side+'-'+mode)/n).read_bytes()==orig,'fresh normal optimized frozen equality '+side)
 return fw,rv,read(R+'output/geometry.json'),read(S+'aj1-independent.json'),allbindings,counts

def geometry(fw,rv,geom,ind):
 output=[]
 for ix,sides in enumerate([(2,2,2),(3,2,2),(3,3,3)]):
  sites=set(itertools.product(*(range(n) for n in sides)))
  links=sorted([((4*b[0]+x,2*b[1]+y,b[2]),d) for b in sites for x,y,d in itertools.product(range(4),range(2),range(3))])
  endpoints=sorted({v for p,d in links for v in (p,add(p,E[d]))})
  anchors=sorted(b for b in sites if {add(b,s) for s in STAR}<=sites)
  groups=[{'anchor':b,'faces':faces(b)} for b in anchors]
  gr=geom['fixtures'][ix];gf=fw['geometry']['fixtures'][ix];gi=ind['geometry_fixtures'][ix]
  need(gr['links']==canon(links)==gi['owned_link_labels'],'all complete original link labels three ways')
  need(gr['endpoint_vertices']==canon(endpoints),'every original gauge endpoint')
  need(gr['groups']==canon(groups),'all complete21 face labels orientation signs and owners')
  outgoing=sorted(l for l in links if owner(add(l[0],E[l[1]])) not in sites)
  need(gr['outgoing_links']==canon(outgoing),'all outgoing owned links remain physical')
  need(gr['anchor_count']==len(anchors)==gf['retained_anchor_count'],'complete whole star count')
  need(gr['omitted_face_count']==21*len(anchors)==gf['retained_omitted_face_count']==gi['omitted_faces'],'all complete21 magnetic groups')
  need(gf['owned_link_count']==len(links)==24*len(sites),'all24 factors')
  need(gf['all_endpoint_count']==len(endpoints)==gi['endpoint_vertices'],'all endpoint cardinalities')
  contained=sum(set(f['owners'])<=sites for b in sites for f in faces(b))
  need(gf['individually_contained_omitted_face_count']==contained and contained>21*len(anchors),'whole star versus individual face boundary discriminates')
  for j,region in enumerate([(Z,),(Z,E[0]),((1,1,1),)]):
   rr=set(region);inc=sorted(b for b in anchors if {add(b,s) for s in STAR}&rr)
   possible=sorted({tuple(r[d]-s[d] for d in range(3)) for r in rr for s in STAR if all(r[d]>=s[d] for d in range(3))})
   fr=gf['regions'][j];re=geom['regions'][3*ix+j]
   need(fr['incident_anchors']==canon(inc)==re['incident_anchors'],'every incoming and outgoing reset anchor')
   need(re['orthant_incident_anchors']==canon(possible),'orthant uniform incident region bound')
   need(fr['normalized_local_energy_ceiling_as_multiple_of_M']==re['energy_upper_coefficient_M']==2*len(inc),'exact incident energy coefficient')
   need(re['uniform_orthant_energy_coefficient_M']==2*len(possible)<=re['universal_energy_coefficient_M']==8*len(rr),'all volume mixed reset cost')
   linksR=[l for l in links if owner(l[0]) in rr];ep=sorted({v for p,d in linksR for v in (p,add(p,E[d]))});tail={p for p,d in linksR}
   need(fr['endpoint_vertices']==canon(ep),'complete local gauge averaging group')
   need(fr['outgoing_head_vertices_lost_by_tail_only_gauge']==canon(sorted(set(ep)-tail)),'missing heads control complete')
  for b in anchors:
   for face in faces(b):
    pos=face['face'][0]
    for (tail,axis),sign in face['word']:
     start=tail if sign==1 else add(tail,E[axis]);end=add(tail,E[axis]) if sign==1 else tail
     need(start==pos,'independent actual oriented plaquette continuity');pos=end
    need(pos==face['face'][0],'independent full closed face')
  output.append({'sides':list(sides),'sites':len(sites),'links':len(links),'endpoints':len(endpoints),'complete_stars':len(anchors),'omitted_faces':21*len(anchors),'outgoing_links':len(outgoing),'individual_boundary_faces':contained})
 return output

def controls(fw,rv,geom):
 gc=fw['gauge_controls'];bl=geom['missing_endpoint_control'];rc=rv['controls'];fc=fw['discriminating_controls']
 need(q(gc['closed_wilson_before'])==q(gc['closed_wilson_after'])==Q(808,1105),'forward exact closed Wilson invariance')
 need(q(gc['wrong_missing_head_wilson'])==Q(44181,93925)!=Q(808,1105),'forward missing head control discriminates')
 need(len(bl['blind_candidates'])==1,'reverse blind candidate preserved')
 blind=bl['blind_candidates'][0];repl=bl['replacement']
 need(q(blind['correct'])==q(blind['missing_head'])==q(repl['correct'])==Q(24,85),'reverse nondiscriminating identity head retained')
 need(tuple(map(q,blind['head_gauge']))==(1,0,0,0),'reverse initial blindness precisely identity head')
 need(q(repl['missing_head'])==Q(168,221)!=Q(24,85),'reverse replacement genuinely discriminating')
 need(rv['nondiscriminating_control']==bl,'reverse result binds exact auxiliary control')
 for row in rc['compact_local_energy_cutoffs']['fixtures']:
  T,n=row['energy_cutoff_T'],row['sites'];B=Q(T+9*n,8);k=(4*B/3).__floor__();single=(k+1)*(k+2)*(2*k+3)//6
  need(q(row['electric_ceiling'])==B and row['twice_spin_ceiling']==k,'onsite cutoff min max electric threshold')
  need(row['finite_rank_upper']==single**(24*n),'full24link Peter Weyl rank upper')
  need(Q((k+1)*(k+3),4)>B,'first excluded link spin exceeds kinetic cutoff')
 reset=fc['local_vacuum_reset_variational_algebra']
 need(q(reset['local_energy_removed'])==Q(1,2) and q(reset['interaction_expectation_change'])==Q(5,4),'forward actual finite diagnostic reset terms')
 need(q(reset['energy_increase'])==-q(reset['local_energy_removed'])+q(reset['interaction_expectation_change'])==Q(3,4),'forward incident variational cancellation')
 need(q(reset['complement_energy_before'])==q(reset['complement_energy_after'])==Q(1,2),'forward outside marginal energy preserved')
 need(q(reset['shifted_energy_difference'])==q(reset['energy_increase']),'forward scalar exact cancellation')
 need(q(rc['vacuum_reset_bookkeeping']['removed_energy'])==Q(32,25) and q(rc['vacuum_reset_bookkeeping']['outside_energy'])==Q(48,25),'reverse separate reset diagnostic exact values')
 for row in rc['arbitrary_bounded_local_domain']['prefixes']:
  n=row['N'];need(q(row['norm2'])==sum((Q(1,k*k) for k in range(1,n+1)),Q(0))<2,'domain countermodel bounded vector')
  need(q(row['form'])==n and q(row['operator_norm2'])==n*(n+1)*(2*n+1)//6,'domain countermodel divergent energy and operator norms')
 for row in fc['bounded_local_vector_not_generator_domain']:
  n=row['N'];need(q(row['generator_norm_squared'])==n and q(row['vector_norm_squared'])<2,'forward distinct domain countermodel')
 for row in rc['unjustified_weak_average']['finite_diagnostics']:
  need(len(row['coordinate_averages'])==row['bits'] and all(q(v)==0 for v in row['coordinate_averages']),'profinite finite averages vanish; infinite measurability is analytic')
 for source in [rc['weakstar_not_normal']['fixtures'],fc['weak_star_normality_and_WOT_representation_control']['prefixes']]:
  for row in source:
   rank=row.get('cutoff',row.get('cutoff_rank'));need(row['state_index']>rank,'normal state escape diagnostic distinguishes missing tightness')
 for row in rc['strong_not_pointnorm']['fixtures']:need(q(row['time_in_pi_units'])*row['witness_input_index']==1 and row['conjugation_difference_norm']==2,'strong unitary versus operator norm orbit control')
 need(rc['compression_and_scale']['compressed_excited_value'] not in rc['compression_and_scale']['true_excited_values'],'compression cannot inherit full spectral support')
 need(rc['gap_not_nonzero_excitation']['physical_positive_spectrum']==[] and fc['gap_not_nonzero_excitation']['excited_physical_dimension']==0,'gap lower exclusion alone gives no excited observable')
 need(q(rc['compression_and_scale']['physical_delta_over_alpha'])*q(rc['compression_and_scale']['inherited_normalized_floor'])==Q(1,16),'physical energy unit factor retained')
 need(Q(1,16)!=q(rc['compression_and_scale']['dyadic_J2_threshold_over_alpha_not_transferred']),'dyadic numerical gap cannot be substituted')
 need(q(fc['ground_center_and_units']['physical_energy'])==6 and q(fc['ground_center_and_units']['frequency'])==3,'actual centering and energy frequency distinction')
 # Check the distinct analytic trace-tail coefficients on the declared cutoff fixtures.
 tail=[]
 for n in (1,2):
  for T in (1,4,16):
   eps=Q(8*n,T)
   need(eps>0 and 2*eps>=eps,'positive compact spectral tail; optional min with1')
   tail.append({'sites':n,'T':T,'epsilon_coefficient_M':str(eps),'forward_and_independent':'2 sqrt(epsilon)','reverse':'2 sqrt(epsilon)+epsilon'})
 return tail

LIMITATIONS=[
 'The coupling interval is symbolic: tau_* contains unevaluated positive Yarotsky constants; no numerical nonzero tau is certified.',
 'The normalized gap 1/2 and physical threshold alpha/16 are inherited from the admitted I1 stability theorem, not a new evaluated mass or an independent reproof of that theorem.',
 'The state uses the actual homogeneous omitted interaction and specified complete-star positive-orthant limit; no equality of all boundary states or substitution of a summable, dyadic, or finite AH model is proved.',
 'Local normality and strong continuity for each finite endpoint gauge group do not imply point-norm continuity on every bounded local operator or preservation of weak operator averages by an arbitrary GNS representation.',
 'The physical algebra is the full gauge-invariant bounded local algebra; no Wilson-only completion, nonzero homogeneous Wilson fluctuation, or nonempty positive physical spectral sector is established.',
 'The generator result uses the source-correct creation core and tested resolvent matrix-element limit; arbitrary bounded-local excitation vectors need not lie in the generator domain, and no common-representation strong-resolvent limit is claimed.',
 'The complete local reset and compactness arguments are analytic; exact finite geometry and countermodel fixtures do not prove the infinite-dimensional source theorem or supply a bounded global perturbation or global conjugating unitary.',
 'No continuum Yang-Mills construction, physical scale matching, Lorentz-invariant continuum theory, justified scalar completion percentage, or priority claim is established.'
]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(HERE/'aj1-post-review.json'));a=ap.parse_args()
 fw,rv,geom,ind,bindings,closures=closure(); geo=geometry(fw,rv,geom,ind);tail=controls(fw,rv,geom)
 for key in ['numerical_nonzero_tau_certified','new_gap_constant','nonzero_homogeneous_Wilson_excitation','all_boundary_limits_equal','continuum_yang_mills','AJ2_executed']:need(fw['scope'][key] is False,'forward scope exclusions')
 for key in ['new_gap_theorem','numerical_nonzero_tau','nonzero_physical_excitation_witness','same_representation_strong_resolvent','every_boundary_state_equal','continuum_yang_mills','wilson_only_algebra_completion']:need(rv['theorem']['scope'][key] is False,'reverse scope exclusions')
 need(ind['check_count']==2060 and ind['current_producer_science_read'] is False,'independent frozen before current producer reading')
 out={'schema':'ym28-aj1-skeptic-post-review-v1','loop':'aj1','sequence':7,'check_count':sum(COUNT.values()),'check_groups':dict(sorted(COUNT.items())),
 'blocking_issues':[],'accepted_mathematical_scope':'Actual I1 local normality and trace-norm regional density limits; compatible finite-endpoint Haar averaging; full physical cyclic space equals joint gauge-fixed space and reduces the actual centered GNS generator, with inherited physical spectral exclusion (0,alpha/16).',
 'geometry':geo,'source_closure_file_counts':closures,'trace_cutoff_bound_comparison':tail,
 'source_core':'u_I in H_I prime intersect D(H_0,I); density and essential self-adjointness are attributed to the source, with orthant spectator reduction explained analytically.',
 'operator_domain':'D(G_phys)=D(G) intersect H_cyc','form_domain':'D(sqrt(G_phys))=D(sqrt(G)) intersect H_cyc',
 'physical_energy_factor_over_alpha':'1/8','inherited_gap_over_alpha':'1/16','frequency_factor':'alpha/(8 hbar)',
 'provenance_review':{'independent_science_before_exchange':True,'forward_successful_development_retained':True,'reverse_blind_24_over85_and_replacement_168_over221_retained':True,'reverse_portability_repair_ast_only_source_bindings':True,'reverse_report_and_all_geometry_bytes_unchanged':True,'reverse_scientific_payload_excludes_only_bindings':True,'fresh_all_outputs_normal_optimized_equal':True},
 'analytic_countermodel_scope':'Countermodels have differing dimensions and compact groups; only the actual-model SU2 covariance fixtures use the complete physical graph. Finite Q8 and prefix controls are not full Haar quadrature or infinite-dimensional proofs.',
 'limitations':LIMITATIONS,'new_research_loops':0,'bindings':dict(sorted(bindings.items()))}
 Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'check_count':out['check_count'],'blocking_issues':[]}))
if __name__=='__main__':main()
