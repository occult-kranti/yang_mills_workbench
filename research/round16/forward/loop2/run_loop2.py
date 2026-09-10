"""Execute the predeclared two-cube action comparison and adversarial acceptance gates."""
import copy,csv,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
import series as s
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid evidence accepted: '+name)
c=s.make_collection();gate('complete collection replay',s.verify_collection(c));byid={x['id']:x['certificate'] for x in c['fixtures']}
gate('complete ordered fixture inventory',tuple(byid)==s.FIXTURE_IDS and len(byid)==7)
gate('all fixed fixture certificates replay',all(s.verify(x) for x in byid.values()))
gate('coarse failures retained',all(x['status']=='insufficient' for x in c['refinement'][:3]))
gate('degrees18and24 meet difference target',all(x['status']=='target-met' for x in c['refinement'][3:]))
gate('difference lower positive final',F(c['refinement'][-1]['difference_interval'][0])>0)
gate('allzero observable exactlyzero',byid['zero']['enclosures']['expectation']==['0','0'])
gate('omitted shared observable nonzero',byid['omitted_shared']['sign_status']=='positive')
gate('negative shared fixture discriminates',byid['negative_shared']['sign_status']=='negative')
gate('unequal individualface bound parameters',len(set(byid['unequal_signed']['couplings']))==3)
gate('outerzero inserted observable staysnonzero',byid['outer_zero']['sign_status']=='positive')
gate('omitted leading degree5 independently predicted',F(byid['omitted_shared']['polynomial_coefficients']['A'][5])==F(41,81*2**18*8**5))
gate('no inserted epsilon atzero face',s.character_series(1,F(0),0,True)==(F(1,2),))
gate('partition Haar trivial channel atzero',s.character_series(0,F(0),0,False)==(F(1),))
# Returned coefficient tuples are immutable; validation precedes memoization.
co=s.character_series(1,F(0),6,True)
reject('immutable returned coefficient cache',lambda:co.__setitem__(0,F(0))) if hasattr(co,'__setitem__') else gate('immutable returned coefficient cache',type(co) is tuple)
reject('Boolean cached label',lambda:s.character_series(True,F(0),6,True))
reject('Boolean cached degree',lambda:s.character_series(1,F(0),True,True))
reject('Boolean insertion flag',lambda:s.character_series(1,F(0),6,1))
reject('float coupling API',lambda:s.certify([0.125]*11))
reject('Boolean coupling API',lambda:s.certify([True]*11))
reject('missing face coefficient',lambda:s.certify(['0']*10))
reject('coupling cap',lambda:s.certify(['2']*11))
reject('Boolean degree',lambda:s.certify(['0']*11,True))
reject('negative degree',lambda:s.certify(['0']*11,-1))
reject('degree cap24',lambda:s.certify(['0']*11,25))
reject('Boolean precision',lambda:s.certify(['0']*11,24,True))
reject('zero precision',lambda:s.certify(['0']*11,24,'0'))
reject('negative precision',lambda:s.certify(['0']*11,24,'-1'))
reject('noncanonical precision',lambda:s.certify(['0']*11,24,'2/4'))
reject('invalid tail ratio',lambda:s.certify(['1']*11,0))
full=byid['full_shared']
mutations=[
('missing source inventory',lambda a:a.update(loop1_input_hashes={})),
('wrong graph hash',lambda a:a['loop1_input_hashes'].update({'graph.json':'0'*64})),
('altered face order',lambda a:a['face_order'].reverse()),
('changed shared coefficient',lambda a:a['couplings'].__setitem__(1,'0')),
('wrong total degree',lambda a:a.update(degree=18)),
('Boolean nested tail order',lambda a:a['tail'].update(first_omitted_degree=True)),
('missing normalization tail',lambda a:a['enclosures'].update(Z=[a['polynomial_values']['Z']]*2)),
('missing numerator tail',lambda a:a['enclosures'].update(A=[a['polynomial_values']['A']]*2)),
('extra epsilon insertion',lambda a:a['polynomial_coefficients']['A'].__setitem__(1,'0')),
('dropped mixed fusion channel',lambda a:a['polynomial_coefficients']['A'].__setitem__(1,str(F(a['polynomial_coefficients']['A'][1])/2))),
('wrong observable removed shared trace',lambda a:a['scope'].update(observable='product outer10traces')),
('forged zero width',lambda a:a.update(width='0')),
('unreviewed premise',lambda a:a.update(assume='mass gap'))]
for name,mutate in mutations:
    a=copy.deepcopy(full);mutate(a);reject(name,lambda a=a:s.verify(a))
for name,mutate in [
('missing required fixture',lambda a:a['fixtures'].pop()),
('reordered fixture identifiers',lambda a:a['required_fixture_ids'].reverse()),
('missing failed refinement',lambda a:a['refinement'].pop(0)),
('forged difference status',lambda a:a['refinement'][0].update(status='target-met')),
('forgot omitted baseline',lambda a:a['refinement'][-1].update(difference_interval=a['refinement'][-1]['full']['enclosures']['expectation'])),
('forged primary index',lambda a:a.update(primary_index=True)),
('unknown collection field',lambda a:a.update(skipped=[]))]:
    a=copy.deepcopy(c);mutate(a);reject(name,lambda a=a:s.verify_collection(a))
reject('mismatched primary fixture',lambda:s.difference(byid['half_shared'],byid['omitted_shared']))
reject('mismatched primary degrees',lambda:s.difference(full,c['refinement'][-2]['omitted']))
original=s.FIXTURE_IDS
try:
    s.FIXTURE_IDS=original[:-1];reject('inmemory missing fixture inventory',s.make_collection)
finally:s.FIXTURE_IDS=original
(out/'collection.json').write_text(json.dumps(c,indent=2)+'\n')
(out/'primary.json').write_text(json.dumps(c['refinement'][-1],indent=2)+'\n')
with (out/'refinement.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['degree','difference_lower','difference_upper','width','lower_float','upper_float','width_float','status'])
    for r in c['refinement']:w.writerow([r['degree'],*r['difference_interval'],r['width'],*[float(F(x)) for x in r['difference_interval']],float(F(r['width'])),r['status']])
with (out/'coupling.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['fixture','couplings_json','shared','expectation_lower','expectation_upper','midpoint_float','sign_status'])
    for row in c['fixtures']:
        cert=row['certificate'];lo,hi=map(F,cert['enclosures']['expectation'])
        w.writerow([row['id'],json.dumps(cert['couplings'],separators=(',',':')),cert['couplings'][1],str(lo),str(hi),float((lo+hi)/2),cert['sign_status']])
r=c['refinement'][-1]
result={'status':'passed','gate_count':len(gates),'gates':gates,'source_sha256':s.SOURCE_SHA,'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'collection_sha256':hashlib.sha256((out/'collection.json').read_bytes()).hexdigest(),'primary_status':r['status'],
 'difference_lower_float':float(F(r['difference_interval'][0])),'difference_width_float':float(F(r['width'])),
 'full_midpoint_float':float(sum(map(F,r['full']['enclosures']['expectation']))/2),'omitted_midpoint_float':float(sum(map(F,r['omitted']['enclosures']['expectation']))/2),
 'refinement_degrees':[r['degree'] for r in c['refinement']],'required_fixtures':list(s.FIXTURE_IDS),
 'scope':'Exact finite same-observable shared-action comparison; no general sign, physical spectral or continuum theorem.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='gates'},indent=2))
