"""Portable cold independent admission of the complete Round16 Loop2 evidence."""
import argparse,copy,hashlib,importlib.util,json,tempfile
from pathlib import Path
from fractions import Fraction as Q
from polynomial_oracle import enclose,exact,degree,quotient,project,boundary_moment
from shared_projector import graph_data

PRECISION='1/1000000000000'
IDS=('zero','negative_shared','omitted_shared','half_shared','full_shared','outer_zero','unequal_signed')


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


class Review:
    """Source-bound expected collection from the independent coefficient oracle."""
    def __init__(self,producer):
        self.producer=Path(producer).resolve();self.loop1=self.producer.parent/'loop1'
        self.source=digest(self.producer/'series.py')
        self.loop1pins={name:digest(self.loop1/name) for name in ('graph.json','two_cube.py','output/exact_evidence.json')}
        required={'graph.json':'9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62','two_cube.py':'13a82e2b804f07d7dbe8951f600ded429d4924b042162ec79d60c2889b767a80','output/exact_evidence.json':'f0120c5508014a9f49e241eac666a56b7b1a86cac323f0eb364cec5974de333e'}
        if self.loop1pins!=required:raise ValueError('frozen Loop1 input mismatch')
        self.graph=json.loads((self.loop1/'graph.json').read_text());self.data=graph_data(self.graph)
        self.faces=list(self.data['words']);s=self.faces.index(self.data['shared']);left=next(i for i,f in enumerate(self.faces) if f in self.data['left'])
        def base(h):
            out=['1/8']*11;out[s]=h;return out
        zero=['0']*11;outerzero=zero.copy();outerzero[s]='1/8';unequal=base('1/16');unequal[left]='-1/16'
        self.parameters={'zero':zero,'negative_shared':base('-1/8'),'omitted_shared':base('0'),'half_shared':base('1/16'),'full_shared':base('1/8'),'outer_zero':outerzero,'unequal_signed':unequal}
        self.cache={}

    def unchanged(self):
        if digest(self.producer/'series.py')!=self.source:raise ValueError('producer source changed during review')
        if any(digest(self.loop1/file)!=sha for file,sha in self.loop1pins.items()):raise ValueError('frozen graph dependency changed')

    def certificate(self,couplings,N):
        degree(N);key=(tuple(couplings),N)
        if key not in self.cache:self.cache[key]=enclose(self.graph,couplings,N)
        e=self.cache[key];M=sum(map(abs,map(Q,couplings)),Q(0));R=e['tail'];interval=e['expectation'];width=interval[1]-interval[0]
        return {'schema':'ym16-two-cube-taylor-v1','source_sha256':self.source,'loop1_input_hashes':dict(self.loop1pins),
          'face_order':self.faces.copy(),'couplings':couplings.copy(),'degree':N,'precision':PRECISION,
          'scope':{'graph':'adjacent two cubes with shared face included once','measure':'normalized product Haar on20links','observable':'product of all11 normalized face traces; fixed for every fixture','generator':'none; finite Euclidean action'},
          'bookkeeping':'epsilon scales original action; distinct face insertion before argument substitution; evaluate epsilon1',
          'absolute_exponent_bound':str(M),'tail':{'ratio':str(M/Q(N+2)),'remainder':str(R),'first_omitted_degree':N+1},
          'polynomial_coefficients':{'Z':list(map(str,e['Z'])),'A':list(map(str,e['A']))},
          'polynomial_values':{'Z':str(sum(e['Z'])),'A':str(sum(e['A']))},
          'enclosures':{'Z':list(map(str,e['Z_interval'])),'A':list(map(str,e['A_interval'])),'expectation':list(map(str,interval))},
          'width':str(width),'precision_status':'target-met' if width<=Q(PRECISION) else 'insufficient-width',
          'sign_status':'positive' if interval[0]>0 else 'negative' if interval[1]<0 else 'zero' if interval[0]==interval[1]==0 else 'inconclusive'}

    def difference(self,N):
        full=self.certificate(self.parameters['full_shared'],N);omitted=self.certificate(self.parameters['omitted_shared'],N)
        f0,f1=map(Q,full['enclosures']['expectation']);o0,o1=map(Q,omitted['enclosures']['expectation']);interval=(f0-o1,f1-o0);width=interval[1]-interval[0]
        return {'degree':N,'full':full,'omitted':omitted,'difference_interval':list(map(str,interval)),'width':str(width),'precision':PRECISION,
          'status':'target-met' if interval[0]>0 and width<=Q(PRECISION) else 'insufficient','sign_status':'positive' if interval[0]>0 else 'inconclusive'}

    def expected(self):
        self.unchanged();refinement=[self.difference(N) for N in (0,6,12,18,24)]
        return {'schema':'ym16-two-cube-collection-v1','source_sha256':self.source,'loop1_input_hashes':dict(self.loop1pins),
          'primary_target':'E_all11(full shared1/8)-E_all11(omitted shared0), fixed outer1/8, same observable and graph',
          'required_fixture_ids':list(IDS),'refinement':refinement,
          'fixtures':[{'id':name,'certificate':self.certificate(self.parameters[name],24)} for name in IDS],
          'degree_cap':24,'primary_index':4,'primary_status':refinement[-1]['status']}

    def verify(self,record):
        self.unchanged()
        if not same(record,self.expected()):raise ValueError('independent collection, coefficient, interval or parameter mismatch')
        target=record['refinement'][4];lo,hi=map(Q,target['difference_interval'])
        if lo<=0 or hi-lo>Q(PRECISION):raise ValueError('primary finite target not certified')
        self.unchanged();return True


def load(path):
    spec=importlib.util.spec_from_file_location('ym16_forward_series',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def run(producer,output):
    producer=Path(producer).resolve();output=Path(output);output.mkdir(parents=True,exist_ok=False)
    review=Review(producer);p=load(producer/'series.py');record=json.loads((producer/'output/collection.json').read_text());checks=[]
    def check(name,condition):
        if not condition:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError,FileNotFoundError):check(name,True);return
        raise RuntimeError('invalid input accepted: '+name)
    check('cold independent reconstruction of complete fixed collection',review.verify(record))
    check('producer complete replay also passes',p.verify_collection(record))
    for row in record['refinement']:
        N=row['degree'];check('every full and omitted total-degree coefficient at N='+str(N),same(row,review.difference(N)))
    for fixture in record['fixtures']:
        check('independent fixed fixture '+fixture['id'],same(fixture['certificate'],review.certificate(review.parameters[fixture['id']],24)))
    check('coarse failures retained exactly',[(r['status'],r['sign_status']) for r in record['refinement']]==[('insufficient','inconclusive'),('insufficient','inconclusive'),('insufficient','positive'),('target-met','positive'),('target-met','positive')])
    check('all eleven zero-coupling observable vanishes exactly',review.certificate(review.parameters['zero'],24)['enclosures']['expectation']==['0','0'])
    omitted=review.certificate(review.parameters['omitted_shared'],24)
    check('outer-only comparator independently certified nonzero',Q(omitted['enclosures']['expectation'][0])>0)
    check('outer-only first nonzero degree is five',all(Q(c)==0 for c in omitted['polynomial_coefficients']['A'][:5]) and Q(omitted['polynomial_coefficients']['A'][5])==Q(41,81*2**18)*Q(1,8)**5)
    check('single shared derivative at zero matches raw Loop1 projector',boundary_moment(1,1,2)/Q(2**5*2**4)**2==Q(1,524288))
    check('insertion carries no extra formal epsilon or coupling',project(1,1)==Q(1,2) and p.character_series(1,Q(0),0,True)==(Q(1,2),))
    check('character cancellation keeps impossible projection exactly zero',all(project(power,label)==0 for power in range(6) for label in range(power+1,8)))
    # Each mutation attacks the saved complete record, not a mere status tag.
    mutants=[]
    def mutate(name,fn):
        bad=copy.deepcopy(record);fn(bad);mutants.append((name,bad))
    mutate('missing required fixture',lambda b:b['fixtures'].pop())
    mutate('empty fixture inventory',lambda b:b.update(fixtures=[],required_fixture_ids=[]))
    mutate('omitted coarse failure',lambda b:b['refinement'].pop(0))
    mutate('Boolean degree cap',lambda b:b.update(degree_cap=True))
    mutate('wrong source hash',lambda b:b.update(source_sha256='0'*64))
    mutate('wrong frozen graph hash',lambda b:b['loop1_input_hashes'].update({'graph.json':'0'*64}))
    mutate('changed shared parameter',lambda b:b['refinement'][-1]['full']['couplings'].__setitem__(review.faces.index(review.data['shared']),'1/16'))
    mutate('changed individual signed coefficient',lambda b:b['fixtures'][-1]['certificate']['couplings'].__setitem__(0,'1/8'))
    mutate('wrong all-outer insertion',lambda b:b['refinement'][-1]['full']['scope'].update(observable='product of ten outer traces'))
    mutate('partition substituted for numerator',lambda b:b['refinement'][-1]['full']['polynomial_coefficients'].update(A=b['refinement'][-1]['full']['polynomial_coefficients']['Z'].copy()))
    mutate('normalization tail discarded',lambda b:b['refinement'][-1]['full']['enclosures'].update(Z=[b['refinement'][-1]['full']['polynomial_values']['Z']]*2))
    mutate('numerator tail discarded',lambda b:b['refinement'][-1]['full']['enclosures'].update(A=[b['refinement'][-1]['full']['polynomial_values']['A']]*2))
    mutate('forged coarse pass',lambda b:b['refinement'][0].update(status='target-met'))
    mutate('outer baseline falsely set to zero',lambda b:b['refinement'][-1]['omitted']['enclosures'].update(expectation=['0','0']))
    mutate('missing coefficient',lambda b:b['refinement'][-1]['full']['polynomial_coefficients']['A'].pop())
    mutate('coefficient changed',lambda b:b['refinement'][-1]['full']['polynomial_coefficients']['A'].__setitem__(1,'0'))
    mutate('enlarged precision request',lambda b:b['refinement'][-1].update(precision='1'))
    for name,bad in mutants:
        reject('independent rejects '+name,lambda b=bad:review.verify(b))
        reject('producer rejects '+name,lambda b=bad:p.verify_collection(b))
    full=review.parameters['full_shared']
    for n in (True,False,-1,25,6.0,'6'):reject('producer strict degree '+repr(n),lambda n=n:p.certify(full,n))
    for tol in (True,'0','-1','nan','1/0',1,'0.000000000001'):reject('producer precision '+repr(tol),lambda tol=tol:p.certify(full,24,tol))
    for badvalue in (True,'2','1/0','0.125',Q(1,8)):
        bad=full.copy();bad[0]=badvalue;reject('producer coefficient contract '+repr(badvalue),lambda b=bad:p.certify(b,24))
    reject('producer incomplete coefficients',lambda:p.certify(full[:-1],24))
    reject('producer excessive total exponent at coarse degree',lambda:p.certify(['1']*11,0))
    reject('independent strict Boolean degree',lambda:degree(True))
    reject('independent invalid normalization',lambda:quotient((0,1),(0,1)))
    reject('independent inverted numerator interval',lambda:quotient((1,0),(1,2)))
    check('signed quotient uses all four corners',quotient((Q(-3),Q(2)),(Q(2),Q(5)))==(Q(-3,2),Q(1)))
    c=p.certify(full,24);c['polynomial_coefficients']['A'][0]='9'
    reject('mutated certificate rejected',lambda:p.verify(c))
    check('mutable returned certificate cannot corrupt polynomial cache',same(p.certify(full,24),review.certificate(full,24)))
    cached=p.polynomials(full,24)
    check('producer cached polynomial coefficients are immutable tuples',type(cached) is tuple and all(type(row) is tuple for row in cached))
    # Source staleness is tested only on copies in the caller-selected output tree.
    with tempfile.TemporaryDirectory(prefix='source-control-',dir=output) as td:
        directory=Path(td);source=directory/'series.py';source.write_bytes((producer/'series.py').read_bytes());module=load(source)
        source.write_bytes(source.read_bytes()+b'\n# deliberate source change\n')
        reject('producer source change after import detected',module.unchanged)
    manifest=json.loads((producer/'manifest.json').read_text())
    check('every frozen producer manifest file matches',bool(manifest['files']) and all(digest(producer/file)==sha for file,sha in manifest['files'].items()))
    review.unchanged();target=record['refinement'][-1]
    result={'schema':'ym16-independent-loop2-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'input_sha256':{'producer/series.py':review.source,'producer/output/collection.json':digest(producer/'output/collection.json'),'producer/manifest.json':digest(producer/'manifest.json'),**{'loop1/'+file:sha for file,sha in review.loop1pins.items()}},
      'primary_difference_interval':target['difference_interval'],'primary_width':target['width'],'primary_degree':24,'required_precision':PRECISION,
      'refinement':[{'degree':r['degree'],'difference_interval':r['difference_interval'],'width':r['width'],'status':r['status'],'sign_status':r['sign_status']} for r in record['refinement']],
      'fixture_ids':list(IDS),'coefficient_oracle':'ordinary character polynomial projections and Catalan Haar moments; direct shared-boundary polynomial integration',
      'scope':'The fixed finite Euclidean two-cube observable difference only; no physical-time or uniform/continuum gap claim.'}
    (output/'review.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'independent_collection.json').write_text(json.dumps(review.expected(),indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks),'lower':float(Q(target['difference_interval'][0])),'width':float(Q(target['width']))}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--producer',required=True);parser.add_argument('--output',required=True);args=parser.parse_args();run(args.producer,args.output)
