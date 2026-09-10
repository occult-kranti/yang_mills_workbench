"""Independent radical, trial-matrix and full-gap inequality-direction verifier."""
from fractions import Fraction as Q
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile

HERE=Path(__file__).resolve().parent
SOURCE_BYTES=Path(__file__).read_bytes()
ALGEBRA_PIN='7b42b151cfbf9b9379aa6e9c4e804332feff9de596bbd5a1a5c6750bc0c69400'
if hashlib.sha256((HERE/'independent_algebra.py').read_bytes()).hexdigest()!=ALGEBRA_PIN:raise ValueError('independent algebra source changed')
spec=importlib.util.spec_from_file_location('ym15_trial_independent_algebra',HERE/'independent_algebra.py')
alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
FORWARD_PINS={
 'B1/cube.py':'d0df83cd06d062ae525f91bfc2c53eb4beacfdb8d467fe2000449e2e20a38107',
 'B1/graph.json':'4e85817855a880ce5f48e6b3995adca6852557d55103623bb0d686295f334f65',
 'B1/output/moments.json':'863d88c35c36e9ffbdd7f28698aa64544e2abcef3af33efad990788dbe012739',
 'C1/spectral_bound.py':'0fcad91d2bc6c22ec65614f38b6367c1a8145f5d889fe187b966d32a8ce315f8'}
SCOPE={'graph':'one cube, six simple square loops','group':'SU(2)',
 'Hilbert':'untruncated gauge-invariant link L2 Haar; Gauss all8vertices, no charges',
 'operator':'H=alpha*sum_e J_e^2-sum_p lambda_p Tr(U_p)/2',
 'interpretation':'full-operator lower bound from independent E1 lower and trial E0 upper',
 'uniform_threshold':'open; this is a finite cube result'}


def rational(v):
    if type(v) is not str or len(v)>20000:raise ValueError('canonical rational string required')
    try:out=Q(v)
    except(ValueError,ZeroDivisionError):raise ValueError('invalid rational')
    if str(out)!=v:raise ValueError('noncanonical rational')
    return out


def serial(v):return json.dumps(v,sort_keys=True,allow_nan=False,separators=(',',':'))


class Review:
    def __init__(self,forward_root):
        self.root=Path(forward_root)
        self.paths={name:self.root/name for name in FORWARD_PINS}
        self.paths.update({'C2/variational.py':self.root/'C2/variational.py','independent/self':Path(__file__),
          'independent/algebra':HERE/'independent_algebra.py','independent/derivation':HERE/'derivation.md',
          'independent/C1_derivation':HERE.parent/'C1/derivation.md','independent/B1_derivation':HERE.parent/'B1/derivation.md'})
        self.snapshot={name:self.read(path) for name,path in self.paths.items()}
        self.hashes={name:hashlib.sha256(data).hexdigest() for name,data in self.snapshot.items()}
        expected={**FORWARD_PINS,'independent/algebra':ALGEBRA_PIN,
           'independent/derivation':'167431afb9d177e9f3655efc7d673e8c16695bb58110230f831768a48eda3ac4',
           'independent/C1_derivation':'90aee6331f40a32fde3c4af0667a4ac23d8bfd421e0b078be2bc9d322b32fa75',
           'independent/B1_derivation':'b1b44e8950316ab3d3c87bb2eb9def4ffd77eaa8adf5540fb71dba4b362cd864'}
        if any(self.hashes[name]!=pin for name,pin in expected.items()) or self.snapshot['independent/self']!=SOURCE_BYTES:
            raise ValueError('reviewed graph, moments, operator or proof sources changed')
        moments=json.loads(self.snapshot['B1/output/moments.json'])
        if serial(moments['character_gram'])!=serial([[p,q,str(int(p==q))] for p in range(6) for q in range(6)]) or serial(moments['character_triples'])!=serial([[p,q,r,'0'] for p in range(6) for q in range(6) for r in range(6)]):
            raise ValueError('complete trial fixtures required')

    @staticmethod
    def read(path):
        if not path.is_file() or path.is_symlink():raise ValueError('regular required nonsymlink input missing')
        return path.read_bytes()

    def unchanged(self):
        if any(self.read(path)!=self.snapshot[name] for name,path in self.paths.items()):raise ValueError('source changed after review creation')

    def verify(self,cert):
        self.unchanged()
        if type(cert) is not dict:raise ValueError('certificate object required')
        alpha=rational(cert.get('alpha'));precision=rational(cert.get('precision'));bits=cert.get('bits')
        if alpha<=0 or precision<=0 or type(bits) is not int or not 0<=bits<=4096:raise ValueError('positive scales and strict integer precision bits required')
        values=cert.get('couplings')
        if type(values) is not list or len(values)!=6:raise ValueError('six couplings required')
        couplings=tuple(map(rational,values));delta=3*alpha;norm=sum(map(abs,couplings),Q(0));squares=sum(v*v for v in couplings);radicand=delta*delta+squares
        interval=cert.get('sqrt_interval')
        if type(interval) is not list or len(interval)!=2:raise ValueError('two radical endpoints required')
        lo,hi=map(rational,interval)
        if not 0<=lo<=hi or lo*lo>radicand or hi*hi<radicand:raise ValueError('exact radical square inequalities fail')
        if lo==hi:
            if lo*lo!=radicand:raise ValueError('false exact radical')
        else:
            scale=2**bits
            if (lo*scale).denominator!=1 or hi-lo!=Q(1,scale) or not lo*lo<radicand<hi*hi:
                raise ValueError('claimed dyadic radical cell is not canonical')
        # A different algorithm supplies an independent bracket, not a rounded sqrt.
        newton_lo,newton_hi,_=alg.bracket_radical(radicand)
        if max(lo,newton_lo)>min(hi,newton_hi):raise ValueError('independent Newton radical interval disjoint')
        e0=((delta-hi)/2,(delta-lo)/2);bound=((delta+lo)/2-norm,(delta+hi)/2-norm)
        status='certified-positive' if bound[0]>0 else 'zero-bound-insufficient' if bound[0]==bound[1]==0 else 'negative-bound-insufficient' if bound[1]<0 else 'inconclusive-enclosure'
        common=len(set(map(abs,couplings)))==1;ratio=abs(couplings[0])/alpha if common else None
        sign=alg.common_sign(ratio) if common else None
        range_status={'positive':'strictly-positive-exact-bound','zero':'zero-bound-insufficient','negative':'negative-bound-insufficient'}[sign] if common else 'not-common-magnitude'
        matrix=alg.trial_matrix(alpha,couplings)
        expected={'schema':'ym15-cube-variational-gap-v1','source_sha256':self.hashes['C2/variational.py'],
          'input_hashes':FORWARD_PINS,'scope':SCOPE,'alpha':str(alpha),'couplings':list(map(str,couplings)),
          'bits':bits,'precision':str(precision),'delta':str(delta),'L':str(norm),'Q':str(squares),'radicand':str(radicand),
          'sqrt_interval':[str(lo),str(hi)],'gram':[[str(int(i==j)) for j in range(7)] for i in range(7)],
          'trial_hamiltonian':[[str(v) for v in row] for row in matrix],
          'trial_minimum_interval':list(map(str,e0)),'full_E0_upper':str(e0[1]),'full_E1_lower':str(delta-norm),
          'gap_bound_interval':list(map(str,bound)),'certified_gap_lower':str(bound[0]),
          'bound_interval_width':str(bound[1]-bound[0]),'precision_status':'target-met' if bound[1]-bound[0]<precision else 'insufficient-precision',
          'status':status,'common_magnitude_ratio':str(ratio) if common else None,'common_range_status':range_status}
        try:matches=serial(cert)==serial(expected)
        except(ValueError,TypeError):matches=False
        if not matches:raise ValueError('independent trial, inequality direction or semantic replay mismatch')
        self.unchanged()
        return {'lower':str(bound[0]),'upper':str(bound[1]),'status':status,'precision_status':expected['precision_status']}


def verify(certificate,forward_root):
    """Cold public admission: reconstruct context and exact proof arithmetic."""
    return Review(forward_root).verify(certificate)


FIXTURE_IDS=['central-bits0','central-bits8','central-bits24','central-bits48','zero','negative','heterogeneous','scaled','boundary','beyond']
RATIOS=['0','1/4','2/5','9/20','49/100','1/2','51/100','13/25','12/23','53/100','11/20','3/5']


def verify_collection(collection,forward_root):
    review=Review(forward_root)
    if type(collection) is not dict or set(collection)!={'schema','fixtures','coupling_rows','ordered_fixture_ids'} or collection['schema']!='ym15-c2-fixture-collection-v1':raise ValueError('strict full collection envelope required')
    if serial(collection['ordered_fixture_ids'])!=serial(FIXTURE_IDS) or type(collection['fixtures']) is not list or len(collection['fixtures'])!=10:raise ValueError('complete ordered fixture set required')
    params=[('1',['1/2']*6,bits) for bits in (0,8,24,48)]+[
       ('1',['0']*6,48),('1',['-1/2']*6,48),('1',['1/2','-1/4','0','1/8','-1/8','0'],48),
       ('2',['1']*6,48),('1',['12/23']*6,48),('1',['3/5']*6,48)]
    certificates={}
    for entry,name,(alpha,coeffs,bits) in zip(collection['fixtures'],FIXTURE_IDS,params):
        if type(entry) is not dict or set(entry)!={'id','certificate'} or entry['id']!=name:raise ValueError('fixture name/order mismatch')
        cert=entry['certificate'];review.verify(cert)
        if cert['alpha']!=alpha or cert['couplings']!=coeffs or type(cert['bits']) is not int or cert['bits']!=bits or cert['precision']!='1/1000000000000':raise ValueError('fixture parameters changed')
        certificates[name]=cert
    rows=collection['coupling_rows']
    if type(rows) is not list or len(rows)!=len(RATIOS):raise ValueError('complete coupling ledger required')
    for row,ratio in zip(rows,RATIOS):
        if type(row) is not dict:raise ValueError('coupling row object required')
        r=rational(ratio);lo=rational(row.get('c2_lower'));hi=rational(row.get('c2_upper'))
        root_lo=2*(lo+6*r)-3;root_hi=2*(hi+6*r)-3;rad=9+6*r*r
        if not 0<=root_lo<=root_hi or root_lo*root_lo>rad or root_hi*root_hi<rad:raise ValueError('coupling row square-root or inequality direction invalid')
        if root_lo!=root_hi and ((root_lo*2**48).denominator!=1 or root_hi-root_lo!=Q(1,2**48)):raise ValueError('coupling row does not retain declared dyadic accuracy')
        status='certified-positive' if lo>0 else 'zero-bound-insufficient' if lo==hi==0 else 'negative-bound-insufficient' if hi<0 else 'inconclusive-enclosure'
        expected={'ratio':ratio,'ratio_float':float(r),'c1_lower':str(3-6*r),'c2_lower':str(lo),'c2_upper':str(hi),'c2_lower_float':float(lo),'status':status}
        if serial(row)!=serial(expected):raise ValueError('coupling display or exact ledger metadata mismatch')
    return certificates


def audit(forward_root,output_dir):
    root=Path(forward_root);path=root/'C2/output/certificates.json';data=path.read_bytes();collection=json.loads(data)
    certificates=verify_collection(collection,root);review=Review(root);final=certificates['central-bits48'];checks=[]
    def gate(name,test=True):
        if not test:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    gate('all10 ordered fixtures and12 coupling rows independently replayed')
    gate('C1 zero-margin fixture now has a positive full-operator lower bound',Q(final['certified_gap_lower'])>Q(12,100) and final['precision_status']=='target-met')
    gate('central bits0 retains inconclusive sign bound',certificates['central-bits0']['status']=='inconclusive-enclosure')
    gate('coarse bits0,8,24 retain insufficient precision',all(certificates['central-bits'+str(bits)]['precision_status']=='insufficient-precision' for bits in(0,8,24)))
    gate('exact boundary12/23 remains zero-bound-insufficient',certificates['boundary']['sqrt_interval']==['75/23','75/23'] and certificates['boundary']['gap_bound_interval']==['0','0'] and certificates['boundary']['status']=='zero-bound-insufficient')
    gate('beyond threshold remains an insufficient lower bound',certificates['beyond']['status']=='negative-bound-insufficient')
    gate('zero-coupling trial handles absent bright direction',certificates['zero']['trial_minimum_interval']==['0','0'] and certificates['zero']['certified_gap_lower']=='3')
    gate('common negative couplings preserve the bound',certificates['negative']['gap_bound_interval']==final['gap_bound_interval'])
    scaled=certificates['scaled']
    gate('coefficient scaling matches matrix and radicand',Q(scaled['radicand'])==4*Q(final['radicand']) and all(Q(scaled['trial_hamiltonian'][i][j])==2*Q(final['trial_hamiltonian'][i][j]) for i in range(7) for j in range(7)))
    for name in ('central-bits48','zero','heterogeneous'):
        c=certificates[name];samples=alg.polynomial_check(Q(c['alpha']),tuple(map(Q,c['couplings'])))
        gate('independent7x7 characteristic polynomial '+name,len(samples)==8)
    for r in map(Q,RATIOS):
        gate('independent threshold squaring algebra at '+str(r),9+6*r*r-(12*r-3)**2==6*r*(12-23*r))
    prediction=json.loads((HERE/'prediction.json').read_bytes());pred=tuple(map(Q,prediction['central_gap_expression_interval']));observed=tuple(map(Q,final['gap_bound_interval']))
    gate('independent Newton prediction and dyadic bound overlap',max(pred[0],observed[0])<=min(pred[1],observed[1]))
    def reject(name,mutation):
        try:review.verify(mutation)
        except(ValueError,TypeError):gate(name);return
        raise ValueError('invalid variational certificate accepted '+name)
    for field,value in [('schema','bad'),('source_sha256','0'*64),('input_hashes',{}),('alpha','0'),('alpha',True),
      ('bits',True),('bits',-1),('bits',4097),('precision','0'),('delta','1'),('L','0'),('Q','0'),('radicand','9'),
      ('sqrt_interval',['0','0']),('sqrt_interval',list(reversed(final['sqrt_interval']))),
      ('certified_gap_lower',final['gap_bound_interval'][1]),('full_E0_upper',final['trial_minimum_interval'][0]),
      ('full_E1_lower','3'),('status','zero-bound-insufficient'),('common_magnitude_ratio','0'),('common_range_status','zero-bound-insufficient')]:
        c=copy.deepcopy(final);c[field]=value;reject('mutation '+field+' '+str(value),c)
    c=copy.deepcopy(final);c['gram'][0][0]='2';reject('wrong trial Gram normalization',c)
    c=copy.deepcopy(final);c['trial_hamiltonian'][0][1]='-1/2';reject('missing magnetic one-half factor',c)
    c=copy.deepcopy(final);c['trial_hamiltonian'][1][2]='1';reject('invented trial potential cross entry',c)
    c=copy.deepcopy(final);c['certified_gap_lower']=c['sqrt_interval'][0];reject('trial two-level gap promoted to full gap',c)
    c=copy.deepcopy(final);c['scope']['interpretation']='two-sided enclosure of full gap';reject('bound-expression interval promoted to gap interval',c)
    c=copy.deepcopy(final);c['scope']['uniform_threshold']='proved';reject('uniform Hamiltonian threshold promotion',c)
    c=copy.deepcopy(final);c['full_E0_lower']=c['trial_minimum_interval'][0];reject('trial eigenvalue promoted to ground-energy lower bound',c)
    for name,mutate in [('missing zero fixture',lambda d:d['fixtures'].pop(4)),('duplicate fixture',lambda d:d['fixtures'].__setitem__(0,d['fixtures'][1])),
      ('forged order manifest',lambda d:d.update(ordered_fixture_ids=[])),('missing coupling row',lambda d:d['coupling_rows'].pop()),
      ('fake row lower',lambda d:d['coupling_rows'][0].update(c2_lower='100')),('row float alias',lambda d:d['coupling_rows'][0].update(ratio_float=False)),
      ('extra collection premise',lambda d:d.update(extra='continuum'))]:
        c=copy.deepcopy(collection);mutate(c)
        try:verify_collection(c,root)
        except(ValueError,TypeError):gate('collection '+name)
        else:raise ValueError('invalid collection accepted '+name)
    for filename in ('C2/variational.py','B1/output/moments.json','C1/spectral_bound.py'):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'forward'
            for folder in('B1','C1','C2'):shutil.copytree(root/folder,target/folder)
            local=Review(target);local.verify(final);p=target/filename;p.write_bytes(p.read_bytes()+b'\n')
            try:local.verify(final)
            except ValueError:gate('warmed source mutation '+filename)
            else:raise ValueError('changed source accepted')
    gate('cold public admission independently reconstructs result',verify(final,root)['status']=='certified-positive')
    gate('evidence unchanged at end',path.read_bytes()==data);review.unchanged()
    result={'schema':'ym15-C2-independent-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),'reviewed_inputs':review.hashes,
      'collection_sha256':hashlib.sha256(data).hexdigest(),'certificates_replayed':10,
      'central':{'alpha':'1','lambda':'1/2','certified_gap_lower':final['certified_gap_lower'],
          'bound_expression_interval':final['gap_bound_interval'],'width':final['bound_interval_width']},
      'common_threshold':'12/23','original_uniform_goal':'open',
      'limits':['The reported interval encloses a proven lower-bound expression, not the actual gap from both sides.',
                'Only the trial eigenvalue upper endpoint bounds the full ground energy from above.',
                'The finite cube improvement does not extract a volume-uniform threshold or continuum mass.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'central_lower_display':float(Q(final['certified_gap_lower']))}));return result


if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: verify_variational.py FORWARD_ROOT OUTPUT_DIR')
    audit(*sys.argv[1:])
